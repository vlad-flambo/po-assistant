"""Moteur API (cycles 010 et 013) : le même pack, envoyé à une API (Mistral ou Claude) au lieu du skill local.

Le pack exporté est découpé en paquets de tâches. Pour chaque paquet, une requête est envoyée avec :
- en `system`, mis en cache : le brief de l'agent, les instructions, le format et le contexte (identiques d'un paquet à
  l'autre, donc relus depuis le cache à partir du deuxième paquet) ;
- en message : les tâches du paquet ;
- une sortie structurée (`output_config.format`) qui garantit la forme JSON des résultats.
Les résultats sont écrits dans le fichier habituel, puis vérifiés et importés comme ceux du skill.

Le fournisseur se déduit du modèle (cycle 013) : `mistral-*` passe par l'API chat completions de Mistral (appel HTTP
direct, `response_format` json_schema strict, repris une fois en `json_object` si le schéma est rejeté) ; `claude-*`
passe par le SDK anthropic comme au cycle 010. Aucune clé n'est stockée ici : MISTRAL_API_KEY pour Mistral ;
ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN ou un profil `ant auth login` pour Claude.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Callable

from . import handoff
from .linear import LinearClient
from .packs import PACKS
from .store import Store

DEFAULT_MODEL = "mistral-large-latest"  # cycle 013 : la clé disponible chez le PO est une clé Mistral
MODELS = {
    "mistral-large-latest": "Mistral Large (recommandé)",
    "mistral-medium-latest": "Mistral Medium",
    "mistral-small-latest": "Mistral Small",
    "claude-opus-5-5": "Claude Opus 5.5",
    "claude-sonnet-5-5": "Claude Sonnet 5.5",
    "claude-haiku-5-5": "Claude Haiku 5.5",
}
PROVIDERS = {"mistral": "Mistral", "anthropic": "Claude"}
CREDENTIAL_VARS = {"mistral": ("MISTRAL_API_KEY",), "anthropic": ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}
# Dollars par million de jetons : entrée, sortie.
# Claude : référence claude-api du 2026-11-03 ; écriture en cache 1,25 × l'entrée, lecture 0,1 × l'entrée.
# Mistral : estimations (agrégateurs, 2026-11-22 ; pages officielles non lisibles depuis la session), à vérifier sur
# mistral.ai/pricing. Pour Large, le tarif le plus haut relevé, pour ne pas sous-estimer.
PRICES = {"mistral-large-latest": (1.36, 4.18), "mistral-medium-latest": (1.50, 7.50),
          "mistral-small-latest": (0.15, 0.60),
          "claude-opus-5-5": (4.00, 20.00), "claude-sonnet-5-5": (2.00, 10.00), "claude-haiku-5-5": (0.10, 0.50)}
PRICES_ESTIMATED = {m for m in PRICES if m.startswith("mistral-")}
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


def provider_of(model: str) -> str:
    return "mistral" if model.startswith(("mistral-", "ministral-", "magistral-", "codestral-")) else "anthropic"


def has_credentials(model: str | None = None) -> bool:
    """Indique seulement si des identifiants semblent disponibles ; ne lit ni n'affiche jamais leur valeur."""
    prov = provider_of(model or DEFAULT_MODEL)
    if any(os.environ.get(v) for v in CREDENTIAL_VARS[prov]):
        return True
    return prov == "anthropic" and (Path.home() / ".config" / "anthropic").exists()


def missing_key_hint(model: str | None = None) -> str:
    """Où mettre la clé du fournisseur du modèle (texte pour l'interface ; jamais la valeur)."""
    if provider_of(model or DEFAULT_MODEL) == "mistral":
        return "définissez MISTRAL_API_KEY (par exemple dans un fichier .env à la racine du dépôt, chargé par le lanceur)"
    return ("définissez ANTHROPIC_API_KEY (par exemple dans un fichier .env à la racine du dépôt, chargé par le "
            "lanceur) ou connectez-vous avec `ant auth login`")


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
    pin, pout = PRICES.get(model, PRICES[DEFAULT_MODEL])
    return round((usage.get("input_tokens", 0) * pin
                  + usage.get("cache_creation_input_tokens", 0) * pin * 1.25
                  + usage.get("cache_read_input_tokens", 0) * pin * 0.1
                  + usage.get("output_tokens", 0) * pout) / 1_000_000, 4)


def estimate(pack_name: str, *, linear: LinearClient | None = None, store: Store | None = None,
             subjects: list[str] | None = None, model: str = DEFAULT_MODEL) -> dict:
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
    cached = provider_of(model) == "anthropic"  # cache de prompt Mistral non vérifié : supposé absent
    usage = {"cache_creation_input_tokens": fixed // 4 if cached else 0,
             "cache_read_input_tokens": (fixed // 4) * (n_batches - 1) if cached else 0,
             "input_tokens": sum(len(json.dumps(it["input"], ensure_ascii=False)) for it in items) // 4
             + (0 if cached else (fixed // 4) * n_batches),
             "output_tokens": OUTPUT_TOKENS_PER_TASK[pack.kind] * len(items)}
    return {"tasks": len(items), "batches": n_batches, "usd": cost_usd(model, usage)}


class _Refused(Exception):
    """La requête est refusée pour de bon (clé, droits, modèle) : inutile d'insister sur les paquets suivants."""


class _Transient(Exception):
    """Ce paquet a échoué (quota, serveur, réseau, requête rejetée) ; les suivants peuvent passer."""


class MistralHTTPError(Exception):
    def __init__(self, status: int, detail: str = ""):
        super().__init__(f"HTTP {status}" if status else detail)
        self.status, self.detail = status, detail


class MistralClient:
    """Appel direct de l'API chat completions de Mistral. La clé n'est lue que pour l'en-tête, jamais affichée."""
    URL = "https://api.mistral.ai/v1/chat/completions"
    RETRY_STATUS = {429, 500, 502, 503, 504}

    def __init__(self, api_key: str | None = None, timeout: float = 600.0, attempts: int = 3, sleep=time.sleep):
        self._key = api_key or os.environ.get("MISTRAL_API_KEY", "")
        self.timeout, self.attempts, self.sleep = timeout, attempts, sleep

    def chat(self, payload: dict) -> dict:
        import httpx2
        last = MistralHTTPError(0, "aucun essai")
        for attempt in range(self.attempts):
            try:
                r = httpx2.post(self.URL, json=payload, timeout=self.timeout,
                                headers={"Authorization": f"Bearer {self._key}", "Accept": "application/json"})
            except httpx2.HTTPError as e:
                last = MistralHTTPError(0, type(e).__name__)
            else:
                if r.status_code == 200:
                    return r.json()
                last = MistralHTTPError(r.status_code, r.text[:300])
                if r.status_code not in self.RETRY_STATUS:
                    raise last
            if attempt + 1 < self.attempts:
                self.sleep(2.0 * 2 ** attempt)
        raise last


def _client(provider: str):
    if provider == "mistral":
        return MistralClient()
    import anthropic
    return anthropic.Anthropic()


def _send_anthropic(client, model: str, system: list[dict], message: str, schema: dict, k: int) -> dict:
    import anthropic
    try:
        with client.beta.messages.stream(
            model=model, max_tokens=MAX_TOKENS, system=system,
            messages=[{"role": "user", "content": message}],
            output_config={"effort": EFFORT, "format": {"type": "json_schema", "schema": schema}},
            betas=BETAS, fallbacks="default",
        ) as stream:
            msg = stream.get_final_message()
    except (anthropic.AuthenticationError, anthropic.PermissionDeniedError, anthropic.NotFoundError) as e:
        raise _Refused(type(e).__name__) from e
    except (anthropic.RateLimitError, anthropic.APIStatusError, anthropic.APIConnectionError) as e:
        raise _Transient(f"erreur de l'API sur le paquet {k} ({type(e).__name__})") from e
    usage = {key: getattr(msg.usage, key, 0) or 0
             for key in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")}
    reason = None
    if msg.stop_reason == "refusal":
        cat = getattr(getattr(msg, "stop_details", None), "category", None)
        reason = f"refus du modèle sur le paquet {k}" + (f" ({cat})" if cat else "")
    elif msg.stop_reason == "max_tokens":
        reason = f"réponse tronquée sur le paquet {k} (max_tokens)"
    text = next((b.text for b in msg.content if getattr(b, "type", None) == "text"), "")
    return {"text": text, "usage": usage, "reason": reason}


def _mistral_text(content) -> str:
    if isinstance(content, list):  # contenu en morceaux : on garde les morceaux de texte
        return "".join(c.get("text", "") for c in content if isinstance(c, dict))
    return content or ""


def _send_mistral(client, model: str, system: list[dict], message: str, schema: dict, k: int) -> dict:
    system_text = system[0]["text"]
    strict = {"type": "json_schema", "json_schema": {"name": "results", "schema": schema, "strict": True}}
    payload = {"model": model, "response_format": strict,
               "messages": [{"role": "system", "content": system_text}, {"role": "user", "content": message}]}
    try:
        try:
            data = client.chat(payload)
        except MistralHTTPError as e:
            if e.status not in (400, 422):
                raise
            # Schéma rejeté : une reprise en mode JSON simple, le schéma dans les instructions (vérifié à l'import)
            payload = {**payload, "response_format": {"type": "json_object"},
                       "messages": [{"role": "system", "content": system_text + "\n\n# Schéma JSON imposé de la "
                                     "réponse\n" + json.dumps(schema, ensure_ascii=False)},
                                    {"role": "user", "content": message}]}
            data = client.chat(payload)
    except MistralHTTPError as e:
        if e.status in (401, 403, 404):
            raise _Refused(f"HTTP {e.status}") from e
        what = f"HTTP {e.status}" if e.status else e.detail
        raise _Transient(f"erreur de l'API sur le paquet {k} ({what})") from e
    u = data.get("usage") or {}
    cached = ((u.get("prompt_tokens_details") or {}).get("cached_tokens")) or 0
    usage = {"input_tokens": (u.get("prompt_tokens") or 0) - cached, "cache_creation_input_tokens": 0,
             "cache_read_input_tokens": cached, "output_tokens": u.get("completion_tokens") or 0}
    choice = (data.get("choices") or [{}])[0]
    finish = choice.get("finish_reason")
    reason = None
    if finish in ("length", "model_length"):
        reason = f"réponse tronquée sur le paquet {k} ({finish})"
    elif finish == "error":
        reason = f"erreur du modèle sur le paquet {k}"
    return {"text": _mistral_text((choice.get("message") or {}).get("content")), "usage": usage, "reason": reason}


SENDERS = {"anthropic": _send_anthropic, "mistral": _send_mistral}


def run(pack_name: str, *, subjects: list[str] | None = None, model: str = DEFAULT_MODEL, client=None,
        linear: LinearClient | None = None, store: Store | None = None, limit: int | None = None,
        on_progress: Callable[[int, int], None] | None = None) -> dict | None:
    """Exporte le pack, le fait traiter par l'API paquet par paquet, écrit le fichier de résultats."""
    if model not in PRICES:
        raise ApiAgentError(f"Modèle inconnu : {model}")
    provider = provider_of(model)
    linear, store = linear or LinearClient(), store or Store()
    if client is None:
        if not has_credentials(model):
            raise ApiAgentError(f"Aucune clé API {PROVIDERS[provider]} détectée : {missing_key_hint(model)}.")
        client = _client(provider)
    send = SENDERS[provider]
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
            reply = send(client, model, system, message, schema, k)
        except _Refused as e:
            if k > 1:  # des paquets ont déjà été traités (et payés) : on garde leurs résultats
                reason = f"requête refusée sur le paquet {k} ({e})"
                problems.append(reason)
                results += [{"task": t["task"], "kind": t["kind"], "skipped": reason} for t in group]
                if on_progress:
                    on_progress(k, len(groups))
                continue
            pack_path.unlink(missing_ok=True)  # rien n'a été traité : pas de pack orphelin
            store.conn.execute("DELETE FROM tasks WHERE export_id = ?", (doc["export_id"],))
            store.conn.execute("DELETE FROM exports WHERE id = ?", (doc["export_id"],))
            store.conn.commit()
            raise ApiAgentError(f"L'API {PROVIDERS[provider]} refuse la requête ({e}) : vérifiez la clé et le "
                                "modèle.") from e
        except _Transient as e:
            reply, reason = None, str(e)
        if reply is not None:
            for key in usage:
                usage[key] += reply["usage"].get(key, 0)
            reason = reply["reason"]
            if not reason:
                try:
                    got = [r for r in json.loads(reply["text"]).get("results", []) if r.get("task") in ids]
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
