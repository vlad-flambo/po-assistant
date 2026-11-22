"""Réglages de PO Assist (data/workspace/settings.json), avec leurs valeurs par défaut."""
from __future__ import annotations

import json

from . import config

DEFAULTS = {
    "demo_mode": True,          # cycle 009 : activé par défaut
    "engine": "api",            # cycle 012 : API par défaut ; "skill" (fichiers + skill Claude Code) en repli
    "api_model": "mistral-large-latest",  # cycle 013 : Mistral par défaut ; les modèles Claude restent au choix
}


def load() -> dict:
    path = config.settings_path()
    data = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
    return {**DEFAULTS, **{k: v for k, v in data.items() if k in DEFAULTS}}


def save(**changes) -> dict:
    current = load()
    unknown = set(changes) - set(DEFAULTS)
    if unknown:
        raise KeyError(f"Réglage inconnu : {', '.join(sorted(unknown))}")
    current.update(changes)
    path = config.settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return current
