"""Choix du moteur de l'agent (cycle 012) : API par défaut, skill Claude Code en repli, démo = API simulée.

- mode démo activé : flux API simulé (po_assist.demo), aucun appel, rien n'est facturé ;
- moteur « api » : appel réel (po_assist.api_agent). Sans identifiants, ou si l'API refuse la requête dès le premier
  paquet (clé invalide, modèle inaccessible), repli automatique sur le skill : le pack est exporté pour Claude Code ;
- moteur « skill » choisi explicitement : export du pack pour le skill local.
"""
from __future__ import annotations

from . import api_agent, demo, handoff, settings
from .linear import LinearClient
from .store import Store

ENGINES = {"api": "API Claude (recommandé)", "skill": "Skill Claude Code, en local (repli)"}
NO_KEY = ("Aucune clé API détectée : repli sur le skill Claude Code local. Pour utiliser l'API, définissez "
          "ANTHROPIC_API_KEY (fichier .env à la racine du dépôt, chargé par le lanceur) ou `ant auth login`.")


def resolve(cfg: dict | None = None) -> dict:
    """Moteur effectif avant lancement : {"engine": "demo"|"api"|"skill", "fallback_reason": str|None}."""
    cfg = cfg or settings.load()
    if cfg["demo_mode"]:
        return {"engine": "demo", "fallback_reason": None}
    if cfg["engine"] == "api" and not api_agent.has_credentials():
        return {"engine": "skill", "fallback_reason": NO_KEY}
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
