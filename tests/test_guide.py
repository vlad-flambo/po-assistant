"""Cycle 011 : le guide utilisateur reste fidèle à l'interface (libellés cités, images, page ❓ Guide)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "docs" / "guide-utilisateur.md"
APP = "\n".join((ROOT / f).read_text(encoding="utf-8") for f in ("app.py", "po_assist/runner.py"))


def _cited_labels() -> list[str]:
    return re.findall(r"\*\*« (.+?) »\*\*", GUIDE.read_text(encoding="utf-8"))


def _dynamic_prefixes() -> set[str]:
    """Début des libellés construits avec des f-strings (« Importer {n} résultat(s) » → « Importer »)."""
    return {m.strip() for m in re.findall(r'f"([^"{]{6,})\{', APP)}


def test_every_cited_label_exists_in_the_app():
    labels = _cited_labels()
    assert len(labels) >= 30, len(labels)
    prefixes = _dynamic_prefixes()
    missing = []
    for label in labels:
        core = label.rstrip("…").strip()
        if core in APP:
            continue
        if any(core.startswith(p) for p in prefixes):  # libellé dynamique : « Importer N résultat(s) »
            continue
        missing.append(label)
    assert not missing, f"libellés du guide absents de l'interface : {missing}"


def test_every_image_exists():
    images = re.findall(r"^!\[.*?\]\((.+?)\)\s*$", GUIDE.read_text(encoding="utf-8"), re.M)
    assert len(images) >= 10
    assert all((GUIDE.parent / i).exists() for i in images), [i for i in images if not (GUIDE.parent / i).exists()]


def test_guide_follows_the_validated_outline():
    text = GUIDE.read_text(encoding="utf-8")
    for heading in ["## 1. Démarrer", "## 2. Vue d'ensemble", "## 3. Le parcours pas à pas", "## 4. Passer en mode réel",
                    "## 5. Lire les résultats", "## 6. Réglages et remise à zéro", "## 7. Dépannage", "## 8. Glossaire",
                    "## 9. Annexe technique"]:
        assert heading in text, heading


def test_readme_links_to_the_guide():
    assert "docs/guide-utilisateur.md" in (ROOT / "README.md").read_text(encoding="utf-8")


def test_guide_page_renders_with_its_images(env):
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.run()
    at.sidebar.radio[0].set_value("❓ Guide").run()
    assert not at.exception, [e.value for e in at.exception]
    assert any("Guide utilisateur de PO Assist" in m.value for m in at.markdown)
    assert len(at.get("image")) >= 10
