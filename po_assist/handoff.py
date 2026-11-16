"""Échange de fichiers avec l'agent (modèle saxobeat : « le fichier est le skill »).

export  -> handoff/to-do/<export_id>.pack.json   (tout ce dont l'agent a besoin)
agent   -> handoff/to-do/<export_id>.results.json (écrit par le skill Claude Code po-agent)
import  -> vérification sans écriture, aperçu, puis application dans po_assist.db
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from . import config
from .linear import LinearClient
from .packs import PACKS
from .store import Store

PACK_SCHEMA = "po-assist.pack.v1"
RESULTS_SCHEMA = "po-assist.results.v1"

AGENT_BRIEF = """\
Tu es l'agent IA de PO Assist. Tu assistes Camille, Product Owner de saxobeat (un SaaS de suivi de recherche d'emploi),
qui travaille dans Linear. Ce fichier est un lot de travail (« pack ») exporté par l'application : il contient tout ce dont
tu as besoin. Tu joues le rôle qu'aurait une API de modèle de langage : tu lis les tâches, tu produis un résultat structuré
par tâche, et l'application l'importe après vérification.

Règles :
1. Traite les tâches dans l'ordre, par paquets d'environ 20, sans en sauter. Si une tâche est impossible, renvoie-la avec
   "skipped" et la raison, plutôt que d'inventer.
2. N'invente jamais un fait, un chiffre, un client ou une demande qui n'est pas dans le fichier. Les citations ("quote")
   sont copiées mot pour mot depuis le texte de la tâche : l'application vérifie qu'elles s'y trouvent.
3. Respecte exactement le format de sortie décrit dans "output_format" (types, valeurs autorisées). Un résultat hors
   format est refusé à l'import.
4. Écris un seul fichier JSON, à côté de ce pack, nommé exactement comme indiqué dans "results_file". Si la session
   risque de s'arrêter, écris les résultats déjà faits : un fichier partiel est importé, le reste repartira au prochain export.
5. Avant de finir, relis la "checklist". Puis donne au PO un compte rendu en 3 lignes : nombre de tâches traitées,
   ignorées, et ce qui t'a semblé incertain.
6. Ne lis aucun autre fichier du dépôt pour répondre (en particulier pas data/ground_truth.json) : tout le contexte utile est ici.
"""

CHECKLIST = [
    "Une entrée dans results par tâche du pack (output ou skipped), avec le même identifiant de tâche et le même kind.",
    "Toutes les valeurs énumérées sont dans les listes autorisées.",
    "Chaque citation est copiée mot pour mot depuis le texte de la tâche.",
    "Le fichier est du JSON valide, nommé comme results_file, à côté du pack.",
]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _dirs() -> dict[str, Path]:
    base = config.handoff_dir()
    d = {k: base / k for k in ("to-do", "done", "problems")}
    for p in d.values():
        p.mkdir(parents=True, exist_ok=True)
    return d


# ---------------------------------------------------------------- export
def export(pack_name: str, *, linear: LinearClient | None = None, store: Store | None = None,
           subjects: list[str] | None = None, limit: int | None = None, out_dir: Path | None = None) -> Path | None:
    """Écrit le pack des tâches à faire. Renvoie None s'il n'y a rien à faire."""
    pack = PACKS[pack_name]
    linear = linear or LinearClient()
    store = store or Store()
    pending = {t["subject"] for t in store.open_tasks(pack_name)}
    all_items = pack.items(linear, store, subjects) if pack_name == "redaction" else pack.items(linear, store)
    items = [it for it in all_items if it["subject"] not in pending or subjects]
    if subjects:
        items = [it for it in items if it["subject"] in set(subjects)]
    if limit:
        items = items[:limit]
    if not items:
        return None
    created = _now()
    export_id = f"E-{created[:19].replace('-', '').replace(':', '').replace('T', '-')}-{pack_name}"
    if store.conn.execute("SELECT 1 FROM exports WHERE id = ?", (export_id,)).fetchone():
        export_id += f"-{len(store.exports())}"
    tasks = [{"task": f"T-{k:03d}", "kind": pack.kind, "subject": it["subject"], "input": it["input"]}
             for k, it in enumerate(items, 1)]
    doc = {
        "schema": PACK_SCHEMA,
        "export_id": export_id,
        "pack": pack_name,
        "instructions_version": pack.version,
        "exported_at": created,
        "reference_date": linear.meta().get("reference_date"),
        "results_file": f"{export_id}.results.json",
        "task_count": len(tasks),
        "agent_brief": AGENT_BRIEF,
        "instructions": pack.instructions,
        "output_format": pack.output_format,
        "results_envelope": {
            "schema": RESULTS_SCHEMA, "export_id": export_id, "pack": pack_name, "agent": "<nom de l'agent>",
            "results": [{"task": "T-001", "kind": pack.kind, "output": "<objet décrit dans output_format>"},
                        {"task": "T-002", "kind": pack.kind, "skipped": "<raison>"}]},
        "context": pack.context(linear, store),
        "tasks": tasks,
        "checklist": CHECKLIST,
    }
    out = (out_dir or _dirs()["to-do"]) / f"{export_id}.pack.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    with store.conn:
        store.conn.execute("INSERT INTO exports VALUES (?,?,?,?,?,?)",
                           (export_id, pack_name, created, out.name, len(tasks), pack.version))
        store.conn.executemany("INSERT INTO tasks VALUES (?,?,?,?,?,?,?)",
                               [(export_id, t["task"], t["kind"], t["subject"], "exported", None, created) for t in tasks])
    return out


# ---------------------------------------------------------------- import
@dataclass
class Preview:
    file: Path
    sha256: str
    export_id: str | None = None
    pack: str | None = None
    agent: str | None = None
    already_imported: str | None = None
    fatal: str | None = None
    accepted: list[dict] = field(default_factory=list)   # {task, subject, output}
    refused: list[dict] = field(default_factory=list)    # {task, subject, reasons}
    skipped: list[dict] = field(default_factory=list)    # {task, subject, reason}
    missing: list[str] = field(default_factory=list)     # tâches du pack sans résultat

    def summary(self) -> str:
        if self.fatal:
            return f"Refusé : {self.fatal}"
        if self.already_imported:
            return f"Déjà importé le {self.already_imported} : rien à faire."
        return (f"{self.pack} ({self.export_id}) : {len(self.accepted)} prêts, {len(self.refused)} refusés, "
                f"{len(self.skipped)} ignorés par l'agent, {len(self.missing)} sans résultat")


def _load_results(text: str) -> dict:
    text = text.strip()
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.S)  # bloc collé depuis un chat
    return json.loads(fence.group(1) if fence else text)


def check(path: Path, *, linear: LinearClient | None = None, store: Store | None = None) -> Preview:
    """Vérifie un fichier de résultats sans rien écrire."""
    path = Path(path)
    raw = path.read_bytes()
    pv = Preview(file=path, sha256=hashlib.sha256(raw).hexdigest())
    store = store or Store()
    seen = store.conn.execute("SELECT imported_at FROM imports WHERE sha256 = ?", (pv.sha256,)).fetchone()
    if seen:
        pv.already_imported = seen[0]
        return pv
    try:
        doc = _load_results(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        pv.fatal = f"JSON illisible ({e})"
        return pv
    if doc.get("schema") != RESULTS_SCHEMA:
        pv.fatal = f"schéma attendu {RESULTS_SCHEMA}, reçu {doc.get('schema')!r}"
        return pv
    pv.export_id, pv.pack, pv.agent = doc.get("export_id"), doc.get("pack"), doc.get("agent")
    tasks = {r["task"]: dict(r) for r in store.conn.execute("SELECT * FROM tasks WHERE export_id = ?", (pv.export_id,))}
    if not tasks:
        pv.fatal = f"export inconnu : {pv.export_id}"
        return pv
    pack = PACKS.get(pv.pack)
    if pack is None:
        pv.fatal = f"pack inconnu : {pv.pack}"
        return pv
    linear = linear or LinearClient()
    ctx = pack.validation_context(linear, store)
    answered = set()
    for res in doc.get("results") or []:
        tid = res.get("task")
        t = tasks.get(tid)
        if t is None:
            pv.refused.append({"task": tid, "subject": None, "reasons": ["tâche inconnue dans cet export"]})
            continue
        if tid in answered:
            pv.refused.append({"task": tid, "subject": t["subject"], "reasons": ["tâche en double dans le fichier"]})
            continue
        answered.add(tid)
        if t["status"] == "done":
            continue  # déjà appliquée par un import précédent (fichier partiel puis complet)
        if res.get("kind") != t["kind"]:
            pv.refused.append({"task": tid, "subject": t["subject"], "reasons": [f"kind attendu {t['kind']}"]})
            continue
        if "skipped" in res:
            pv.skipped.append({"task": tid, "subject": t["subject"], "reason": str(res["skipped"])})
            continue
        output = res.get("output")
        reasons = ["output absent ou non objet"] if not isinstance(output, dict) else pack.validate(output, t["subject"], ctx)
        if reasons:
            pv.refused.append({"task": tid, "subject": t["subject"], "reasons": reasons})
        else:
            pv.accepted.append({"task": tid, "subject": t["subject"], "output": output})
    pv.missing = sorted(tid for tid, t in tasks.items() if tid not in answered and t["status"] == "exported")
    return pv


def apply(pv: Preview, *, store: Store | None = None, strict: bool = False) -> str:
    """Applique un aperçu vérifié. En mode strict, un seul refus bloque tout le fichier."""
    store = store or Store()
    if pv.fatal or pv.already_imported:
        return pv.summary()
    if strict and pv.refused:
        return f"Rien importé (mode strict) : {len(pv.refused)} résultat(s) refusé(s)."
    now = _now()
    pack = PACKS[pv.pack]
    with store.conn:
        for a in pv.accepted:
            store.conn.execute("INSERT OR REPLACE INTO results VALUES (?,?,?,?,?,?,?)",
                               (pack.kind, a["subject"], pv.export_id, a["task"],
                                json.dumps(a["output"], ensure_ascii=False, sort_keys=True), pv.agent, now))
            store.conn.execute("UPDATE tasks SET status = 'done', reason = NULL, updated_at = ? WHERE export_id = ? AND task = ?",
                               (now, pv.export_id, a["task"]))
        for s in pv.skipped:  # la tâche est close ; le sujet repartira au prochain export
            store.conn.execute("UPDATE tasks SET status = 'skipped', reason = ?, updated_at = ? WHERE export_id = ? AND task = ?",
                               (s["reason"], now, pv.export_id, s["task"]))
        for r in pv.refused:
            if r["subject"]:
                store.conn.execute("UPDATE tasks SET status = 'refused', reason = ?, updated_at = ? WHERE export_id = ? AND task = ?",
                                   ("; ".join(r["reasons"]), now, pv.export_id, r["task"]))
        store.conn.execute("INSERT INTO imports VALUES (?,?,?,?,?)", (pv.sha256, pv.file.name, pv.export_id, now, pv.summary()))
    return f"Importé : {pv.summary()}"


def import_file(path: Path, *, dry_run: bool = False, strict: bool = False,
                linear: LinearClient | None = None, store: Store | None = None) -> tuple[Preview, str]:
    store = store or Store()
    pv = check(path, linear=linear, store=store)
    if dry_run:
        return pv, f"Aperçu (rien n'est écrit) : {pv.summary()}"
    msg = apply(pv, store=store, strict=strict)
    _file_away(pv)
    return pv, msg


def _file_away(pv: Preview) -> None:
    """Range le pack et ses résultats : done/ si tout est passé, problems/ (avec une note) sinon."""
    d = _dirs()
    if pv.file.parent.resolve() != d["to-do"].resolve():
        return
    ok = not pv.fatal and not pv.refused
    target = d["done"] if ok else d["problems"]
    pack_file = pv.file.with_name(pv.file.name.replace(".results.json", ".pack.json"))
    for f in (pv.file, pack_file):
        if f.exists():
            shutil.move(str(f), target / f.name)
    if not ok:
        lines = [pv.summary()] + [f"{r['task']} {r['subject']}: {'; '.join(r['reasons'])}" for r in pv.refused]
        (target / f"{pv.file.stem}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def status(*, linear: LinearClient | None = None, store: Store | None = None) -> dict:
    linear, store = linear or LinearClient(), store or Store()
    out = {"triage": len(linear.triage_issues()), "backlog": len(linear.backlog_issues()),
           "reference_date": linear.meta().get("reference_date"), "packs": {}}
    for name, pack in PACKS.items():
        pending = {t["subject"] for t in store.open_tasks(name)}
        out["packs"][name] = {"to_do": sum(1 for it in pack.items(linear, store) if it["subject"] not in pending),
                              "exported": len(pending),
                              "done": len(store.subjects_done(pack.kind))}
    return out


def register_pack(pack_path: Path, *, store: Store | None = None) -> str:
    """Enregistre un pack produit ailleurs (ex. handoff/demo/) pour pouvoir en importer les résultats."""
    store = store or Store()
    doc = json.loads(Path(pack_path).read_text(encoding="utf-8"))
    if doc.get("schema") != PACK_SCHEMA:
        raise ValueError(f"{pack_path} n'est pas un pack {PACK_SCHEMA}")
    eid = doc["export_id"]
    if not store.conn.execute("SELECT 1 FROM exports WHERE id = ?", (eid,)).fetchone():
        with store.conn:
            store.conn.execute("INSERT INTO exports VALUES (?,?,?,?,?,?)", (eid, doc["pack"], doc["exported_at"],
                               Path(pack_path).name, doc["task_count"], doc["instructions_version"]))
            store.conn.executemany("INSERT INTO tasks VALUES (?,?,?,?,?,?,?)",
                                   [(eid, t["task"], t["kind"], t["subject"], "exported", None, doc["exported_at"])
                                    for t in doc["tasks"]])
    return eid


def load_demo(*, store: Store | None = None, linear: LinearClient | None = None, upto: str | None = None) -> list[str]:
    """Rejoue les résultats pré-calculés de handoff/demo/ dans l'ordre analyse → priorisation → rédaction."""
    store = store or Store()
    demo = config.ROOT / "handoff" / "demo"
    msgs = []
    for pack in ["analyse", "priorisation", "redaction"]:
        for pf in sorted(demo.glob(f"*-{pack}.pack.json")):
            register_pack(pf, store=store)
            rf = pf.with_name(pf.name.replace(".pack.json", ".results.json"))
            if rf.exists():
                pv = check(rf, linear=linear, store=store)
                msgs.append(f"{rf.name} : {apply(pv, store=store)}")
        if pack == upto:
            break
    return msgs

