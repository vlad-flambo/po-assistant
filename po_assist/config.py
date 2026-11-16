"""Chemins par défaut, surchargeables par variables d'environnement (utilisées par les tests).

L'application travaille sur une copie de l'espace Linear (data/workspace/linear.db), créée au premier lancement
depuis la base versionnée data/linear.db : une démo (rattacher, créer des issues) ne modifie jamais le dépôt.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED_LINEAR = ROOT / "data" / "linear.db"
WORKSPACE = ROOT / "data" / "workspace"


def linear_db() -> Path:
    if "PO_LINEAR_DB" in os.environ:
        return Path(os.environ["PO_LINEAR_DB"])
    path = WORKSPACE / "linear.db"
    if not path.exists():
        WORKSPACE.mkdir(parents=True, exist_ok=True)
        shutil.copy(SEED_LINEAR, path)
    return path


def assist_db() -> Path:
    return Path(os.environ.get("PO_ASSIST_DB", WORKSPACE / "po_assist.db"))


def handoff_dir() -> Path:
    return Path(os.environ.get("PO_HANDOFF_DIR", ROOT / "handoff"))


def reset_workspace() -> None:
    """Repart de l'état initial : copie neuve de Linear, base de travail vide (les fichiers d'échange restent)."""
    for p in (WORKSPACE / "linear.db", WORKSPACE / "po_assist.db"):
        p.unlink(missing_ok=True)
    linear_db()
