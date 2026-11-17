"""Moteur API (cycle 010) : le même pack, envoyé à l'API Claude au lieu du skill local.

Le pack exporté est découpé en paquets de tâches. Pour chaque paquet, une requête est envoyée avec :
- en `system`, mis en cache : le brief de l'agent, les instructions, le format et le contexte (identiques d'un paquet à
  l'autre, donc relus depuis le cache à partir du deuxième paquet) ;
- en message : les tâches du paquet ;
- une sortie structurée (`output_config.format`) qui garantit la forme JSON des résultats.
Les résultats sont écrits dans le fichier habituel, puis vérifiés et importés comme ceux du skill.
Aucune clé n'est stockée ici : le SDK lit ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN ou un profil `ant auth login`.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Callable

from . import handoff
from .linear import LinearClient
from .packs import PACKS
from .store import Store

MODELS = {
    "claude-opus-5-5": "Claude Opus 5.5 (recommandé)",
    "claude-sonnet-5-5": "Claude Sonnet 5.5",
    "claude-haiku-5-5": "Claude Haiku 5.5",
}
# Dollars par million de jetons : entrée, sortie (référence claude-api du 2026-11-03).
# Écriture en cache : 1,25 × l'entrée ; lecture en cache : 0,1 × l'entrée (estimation pour Haiku).
PRICES = {"claude-opus-5-5": (4.00, 20.00), "claude-sonnet-5-5": (2.00, 10.00), "claude-haiku-5-5": (0.10, 0.50)}
# Jetons de sortie moyens par tâche (avec la réflexion), pour l'estimation avant envoi.
OUTPUT_TOKENS_PER_TASK = {"feedback_analysis": 900, "prioritization": 700, "user_story": 4000}
BETAS = ["server-side-fallback-2026-07-01"]
EFFORT = "high"
MAX_TOKENS = 64000

API_PREFACE = """\
MODE API : tu es appelé directement par l'application, paquet par paquet. N'écris aucun fichier. Réponds uniquement
par l'objet JSON {"results": [...]} décrit par le schéma imposé : une entrée par tâche du message, avec son identifiant
de tâche et son kind, et soit "output" (conforme au format du pack), soit "skipped" (la raison) si la tâche est
impossible. Le reste des règles du brief s'applique (aucune invention, citations mot pour mot).
"""


class ApiAgentError(RuntimeError):
    """Erreur qui arrête tout le lancement (clé absente ou refusée, modèle inconnu)."""


def has_credentials() -> bool:
    """Indique seulement si des identifiants semblent disponibles ; ne lit ni n'affiche jamais leur valeur."""
    if os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"):
        return True
    return (Path.home() / ".config" / "anthropic").exists()


def results_schema(pack) -> dict:
    task_entry_output = {
        "type": "object",
        "properties": {"task": {"type": "string"}, "kind": {"type": "string", "enum": [pack.kind]},
                       "output": pack.output_schema},
        "required": ["task", "kind", "output"], "additionalProperties": False}
    task_entry_skipped = {
        "type": "object",
        "properties": {"task": {"type": "string"}, "kind": {"type": "string", "enum": [pack.kind]},
                       "skipped": {"type": "string"}},
        "required": ["task", "kind", "skipped"], "additionalProperties": False}
    return {"type": "object",
            "properties": {"results": {"type": "array", "items": {"anyOf": [task_entry_output, task_entry_skipped]}}},
            "required": ["results"], "additionalProperties": False}


def system_blocks(doc: dict) -> list[dict]:
    """Partie stable de chaque requête, en un bloc mis en cache. Sérialisation triée : aucun octet ne varie."""
    text = "\n\n".join([
        doc["agent_brief"], API_PREFACE,
        "# Instructions du pack « " + doc["pack"] + " »\n" + doc["instructions"],
        "# Format de sortie\n" + json.dumps(doc["output_format"], ensure_ascii=False, sort_keys=True, indent=1),
        "# Contexte\n" + json.dumps(doc["context"], ensure_ascii=False, sort_keys=True, indent=1),
        "# Checklist\n" + "\n".join("- " + c for c in doc["checklist"]),
    ])
    return [{"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}]


def batches(tasks: list[dict], size: int) -> list[list[dict]]:
    return [tasks[i:i + size] for i in range(0, len(tasks), size)]


def cost_usd(model: str, usage: dict) -> float:
    pin, pout = PRICES.get(model, PRICES["claude-opus-5-5"])
    return round((usage.get("input_tokens", 0) * pin
                  + usage.get("cache_creation_input_tokens", 0) * pin * 1.25
                  + usage.get("cache_read_input_tokens", 0) * pin * 0.1
                  + usage.get("output_tokens", 0) * pout) / 1_000_000, 4)


def estimate(pack_name: str, *, linear: LinearClient | None = None, store: Store | None = None,
             subjects: list[str] | None = None, model: str = "claude-opus-5-5") -> dict:
    """Estimation grossière avant envoi (4 caractères ≈ 1 jeton), sans appel à l'API."""
    linear, store = linear or LinearClient(), store or Store()
    pack = PACKS[pack_name]
    items = pack.items(linear, store, subjects) if pack_name == "redaction" else pack.items(linear, store)
    pending = {t["subject"] for t in store.open_tasks(pack_name)}
    items = [it for it in items if it["subject"] not in pending or subjects]
    if subjects:
        items = [it for it in items if it["subject"] in set(subjects)]
    if not items:
        return {"tasks": 0, "batches": 0, "usd": 0.0}
    fixed = len(pack.instructions) + len(json.dumps(pack.context(linear, store), ensure_ascii=False)) + 6000
    n_batches = len(batches(items, pack.batch_size))
    usage = {"cache_creation_input_tokens": fixed // 4,
             "cache_read_input_tokens": (fixed // 4) * (n_batches - 1),
             "input_tokens": sum(len(json.dumps(it["input"], ensure_ascii=False)) for it in items) // 4,
             "output_tokens": OUTPUT_TOKENS_PER_TASK[pack.kind] * len(items)}
    return {"tasks": len(items), "batches": n_batches, "usd": cost_usd(model, usage)}


def _client():
    import anthropic
    return anthropic.Anthropic()


def run(pack_name: str, *, subjects: list[str] | None = None, model: str = "claude-opus-5-5", client=None,
        linear: LinearClient | None = None, store: Store | None = None, limit: int | None = None,
        on_progress: Callable[[int, int], None] | None = None) -> dict | None:
    """Exporte le pack, le fait traiter par l'API paquet par paquet, écrit le fichier de résultats."""
    import anthropic
    if model not in PRICES:
        raise ApiAgentError(f"Modèle inconnu : {model}")
    linear, store = linear or LinearClient(), store or Store()
    if client is None:
        if not has_credentials():
            raise ApiAgentError("Aucune clé API détectée. Définissez ANTHROPIC_API_KEY (par exemple dans un fichier "
                                ".env à la racine du dépôt, chargé par le lanceur) ou connectez-vous avec `ant auth login`.")
        client = _client()
    pack = PACKS[pack_name]
    pack_path = handoff.export(pack_name, linear=linear, store=store, subjects=subjects, limit=limit)
    if pack_path is None:
        return None
    doc = json.loads(pack_path.read_text(encoding="utf-8"))
    system = system_blocks(doc)
    schema = results_schema(pack)
    usage = {"input_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 0}
    results, problems = [], []
    groups = batches(doc["tasks"], pack.batch_size)
    for k, group in enumerate(groups, 1):
        ids = {t["task"] for t in group}
        message = ("Traite ces " + str(len(group)) + " tâches et réponds par l'objet JSON {\"results\": [...]}.\n\n"
                   + json.dumps([{"task": t["task"], "kind": t["kind"], "input": t["input"]} for t in group],
                                ensure_ascii=False, indent=1))
        reason = None
        try:
            with client.beta.messages.stream(
                model=model, max_tokens=MAX_TOKENS, system=system,
                messages=[{"role": "user", "content": message}],
                output_config={"effort": EFFORT, "format": {"type": "json_schema", "schema": schema}},
                betas=BETAS, fallbacks="default",
            ) as stream:
                msg = stream.get_final_message()
        except (anthropic.AuthenticationError, anthropic.PermissionDeniedError, anthropic.NotFoundError) as e:
            if k > 1:  # des paquets ont déjà été traités (et payés) : on garde leurs résultats
                msg, reason = None, f"requête refusée sur le paquet {k} ({type(e).__name__})"
                problems.append(reason)
                results += [{"task": t["task"], "kind": t["kind"], "skipped": reason} for t in group]
                if on_progress:
                    on_progress(k, len(groups))
                continue
            pack_path.unlink(missing_ok=True)  # rien n'a été traité : pas de pack orphelin
            store.conn.execute("DELETE FROM tasks WHERE export_id = ?", (doc["export_id"],))
            store.conn.execute("DELETE FROM exports WHERE id = ?", (doc["export_id"],))
            store.conn.commit()
            raise ApiAgentError(f"L'API refuse la requête ({type(e).__name__}) : vérifiez la clé et le modèle.") from e
        except (anthropic.RateLimitError, anthropic.APIStatusError, anthropic.APIConnectionError) as e:
            msg, reason = None, f"erreur de l'API sur le paquet {k} ({type(e).__name__})"
        if msg is not None:
            u = msg.usage
            for key in usage:
                usage[key] += getattr(u, key, 0) or 0
            if msg.stop_reason == "refusal":
                cat = getattr(getattr(msg, "stop_details", None), "category", None)
                reason = f"refus du modèle sur le paquet {k}" + (f" ({cat})" if cat else "")
            elif msg.stop_reason == "max_tokens":
                reason = f"réponse tronquée sur le paquet {k} (max_tokens)"
            else:
                text = next((b.text for b in msg.content if getattr(b, "type", None) == "text"), "")
                try:
                    got = [r for r in json.loads(text).get("results", []) if r.get("task") in ids]
                    results += got
                    ids -= {r["task"] for r in got}
                    if ids:
                        reason = f"tâche absente de la réponse du paquet {k}"
                except (json.JSONDecodeError, AttributeError):
                    reason = f"réponse illisible sur le paquet {k}"
        if reason:
            problems.append(reason)
            results += [{"task": t["task"], "kind": t["kind"], "skipped": reason} for t in group if t["task"] in ids]
        if on_progress:
            on_progress(k, len(groups))
    results_path = pack_path.with_name(doc["results_file"])
    results_path.write_text(json.dumps({"schema": handoff.RESULTS_SCHEMA, "export_id": doc["export_id"],
                                        "pack": pack_name, "agent": f"api / {model}", "results": results},
                                       ensure_ascii=False, indent=2), encoding="utf-8")
    return {"pack": pack_path, "results": results_path, "tasks": len(doc["tasks"]), "batches": len(groups),
            "usage": usage, "usd": cost_usd(model, usage), "problems": problems, "model": model}
