"""Mode démo (cycle 009) : le skill est remplacé par ses vrais résultats, calculés à l'avance et tenus cachés.

Le parcours reste le vrai : l'application exporte le pack, puis ce module dépose le fichier de résultats
que le skill avait produit pour exactement ces sujets, et le PO vérifie et importe comme d'habitude.
Un sujet absent du cache revient « ignoré » : rien n'est jamais inventé.
"""
from __future__ import annotations

import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

from . import config, handoff
from .linear import LinearClient
from .store import Store

AGENT = "po-agent (résultats pré-calculés d'un vrai passage du skill, mode démo)"


@lru_cache(maxsize=4)
def _cache(demo_dir: str) -> dict[tuple[str, str], dict]:
    out = {}
    for rf in sorted(Path(demo_dir).glob("*.results.json")):
        pf = rf.with_name(rf.name.replace(".results.json", ".pack.json"))
        if not pf.exists():
            continue
        subject_of = {t["task"]: t["subject"] for t in json.loads(pf.read_text(encoding="utf-8"))["tasks"]}
        doc = json.loads(rf.read_text(encoding="utf-8"))
        for r in doc["results"]:
            if "output" in r and r["task"] in subject_of:
                out[(r["kind"], subject_of[r["task"]])] = {"output": r["output"], "agent": doc.get("agent"), "file": rf.name}
    return out


def cache() -> dict[tuple[str, str], dict]:
    return _cache(str(config.demo_dir()))


def coverage() -> dict[str, int]:
    return dict(Counter(kind for kind, _ in cache()))


def simulated_seconds(task_count: int) -> float:
    """Durée affichée de la « progression » : environ 0,1 s par tâche, entre 3 et 10 s."""
    return max(3.0, min(10.0, 0.1 * task_count))


def run(pack_name: str, *, subjects: list[str] | None = None, linear: LinearClient | None = None,
        store: Store | None = None) -> dict | None:
    """Exporte le pack (comme en vrai) puis dépose à côté le fichier de résultats tiré du cache."""
    linear, store = linear or LinearClient(), store or Store()
    pack_path = handoff.export(pack_name, linear=linear, store=store, subjects=subjects)
    if pack_path is None:
        return None
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    c = cache()
    results, missing = [], []
    for t in pack["tasks"]:
        hit = c.get((t["kind"], t["subject"]))
        if hit:
            results.append({"task": t["task"], "kind": t["kind"], "output": hit["output"]})
        else:
            missing.append(t["subject"])
            results.append({"task": t["task"], "kind": t["kind"],
                            "skipped": "pas de résultat pré-calculé pour ce sujet (mode démo)"})
    results_path = pack_path.with_name(pack["results_file"])
    results_path.write_text(json.dumps({"schema": handoff.RESULTS_SCHEMA, "export_id": pack["export_id"],
                                        "pack": pack_name, "agent": AGENT, "results": results},
                                       ensure_ascii=False, indent=2), encoding="utf-8")
    return {"pack": pack_path, "results": results_path, "tasks": len(results), "missing": missing,
            "seconds": simulated_seconds(len(results))}
