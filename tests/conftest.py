import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def env(tmp_path, monkeypatch):
    """Copies temporaires : la base Linear, une base de travail vide, un dossier d'échange vide."""
    linear = tmp_path / "linear.db"
    shutil.copy(ROOT / "data" / "linear.db", linear)
    monkeypatch.setenv("PO_LINEAR_DB", str(linear))
    monkeypatch.setenv("PO_ASSIST_DB", str(tmp_path / "po_assist.db"))
    monkeypatch.setenv("PO_HANDOFF_DIR", str(tmp_path / "handoff"))
    monkeypatch.setenv("PO_SETTINGS_FILE", str(tmp_path / "settings.json"))
    return tmp_path
