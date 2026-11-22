"""Choix du moteur de l'agent (cycle 012) : API par défaut, skill Claude Code en repli, démo = API simulée.

- mode démo activé : flux API simulé (po_assist.demo), aucun appel, rien n'est facturé ;
- moteur « api » : appel réel (po_assist.api_agent), à Mistral ou à Claude selon le modèle (cycle 013). Sans identifiants, ou si l'API refuse la requête dès le premier
  paquet (clé invalide, modèle inaccessible), repli automatique sur le skill : le pack est exporté pour Claude Code ;
- moteur « skill » choisi explicitement : export du pack pour le skill local.
"""
from __future__ import annotations

from . import api_agent, demo, handoff, settings
from .linear import LinearClient
from .store import Store

ENGINES = {"api": "API Mistral ou Claude, selon le modèle (recommandé)", "skill": "Skill Claude Code, en local (repli)"}


def no_key_message(model: str) -> str:
    prov = api_agent.PROVIDERS[api_agent.provider_of(model)]
    return (f"Aucune clé API {prov} détectée : repli sur le skill Claude Code local. Pour utiliser l'API, "
            f"{api_agent.missing_key_hint(model)}.")


def resolve(cfg: dict | None = None) -> dict:
    """Moteur effectif avant lancement : {"engine": "demo"|"api"|"skill", "fallback_reason": str|None}."""
    cfg = cfg or settings.load()
    if cfg["demo_mode"]:
        return {"engine": "demo", "fallback_reason": None}
    if cfg["engine"] == "api" and not api_agent.has_credentials(cfg["api_model"]):
        return {"engine": "skill", "fallback_reason": no_key_message(cfg["api_model"])}
    return {"engine": cfg["engine"], "fallback_reason": None}


def run(pack_name: str, *, subjects: list[str] | None = None, cfg: dict | None = None,
        linear: LinearClient | None = None, store: Store | None = None, on_progress=None, client=None,
        pace: float = 0.0, limit: int | None = None) -> dict | None:
    """Lance l'agent avec le moteur effectif. Renvoie None s'il n'y a rien à traiter."""
    cfg = cfg or settings.load()
    linear, store = linear or LinearClient(), store or Store()
    r = resolve(cfg) if client is None else {"engine": "demo" if cfg["demo_mode"] else cfg["engine"], "fallback_reason": None}
    engine, reason = r["engine"], r["fallback_reason"]
    out = None
    if engine == "demo":
        out = demo.run(pack_name, subjects=subjects, linear=linear, store=store, model=cfg["api_model"],
                       pace=pace, on_progress=on_progress)
    elif engine == "api":
        try:
            out = api_agent.run(pack_name, subjects=subjects, model=cfg["api_model"], client=client, linear=linear,
                                store=store, limit=limit, on_progress=on_progress)
        except api_agent.ApiAgentError as e:
            engine, reason = "skill", f"{e} Repli sur le skill Claude Code local."
    if engine == "skill":
        path = handoff.export(pack_name, linear=linear, store=store, subjects=subjects, limit=limit)
        out = {"pack": path} if path else None
    if out is not None:
        out.update(engine=engine, fallback_reason=reason)
    return out
