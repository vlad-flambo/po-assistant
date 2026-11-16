"""Chemins par défaut, surchargeables par variables d'environnement (utilisées par les tests)."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def linear_db() -> Path:
    return Path(os.environ.get("PO_LINEAR_DB", ROOT / "data" / "linear.db"))


def assist_db() -> Path:
    return Path(os.environ.get("PO_ASSIST_DB", ROOT / "data" / "po_assist.db"))


def handoff_dir() -> Path:
    return Path(os.environ.get("PO_HANDOFF_DIR", ROOT / "handoff"))
