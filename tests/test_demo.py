"""Cycle 009 : mode démo (résultats réels du skill, pré-calculés, révélés au fil du parcours) et rendu de l'interface."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from po_assist import config, demo, handoff, scoring, settings
from po_assist.store import Store

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["🤖 Agent", "🏠 Tableau de bord", "📥 Feedbacks", "🧩 Demandes", "⚖️ Priorisation", "✍️ User stories",
         "🎯 Qualité de l'agent", "⚙️ Réglages"]


def _import(run):
    pv, _ = handoff.import_file(run["results"])
    return pv


def test_demo_mode_is_on_by_default_and_survives_reset(env):
    assert settings.load()["demo_mode"] is True
    settings.save(demo_mode=False)
    assert settings.load()["demo_mode"] is False
    with pytest.raises(KeyError):
        settings.save(inconnu=1)


def test_nothing_is_revealed_before_the_po_runs_the_agent(env):
    assert Store().results("feedback_analysis") == {}
    assert handoff.status()["packs"]["analyse"]["to_do"] == 80


def test_demo_run_plays_the_real_pipeline_step_by_step(env):
    run = demo.run("analyse")
    assert run["tasks"] == 80 and not run["missing"] and 3 <= run["seconds"] <= 10
    doc = json.loads(run["results"].read_text())
    assert doc["schema"] == "po-assist.results.v1" and "pré-calculés" in doc["agent"]
    pv = handoff.check(run["results"])
    assert len(pv.accepted) == 80 and not pv.refused  # mêmes vérifications qu'en vrai
    handoff.apply(pv)
    assert Store().results("prioritization") == {}  # l'étape suivante reste cachée
    pv = _import(demo.run("priorisation"))
    assert len(pv.accepted) == 30 and not pv.refused
    chosen = [r["target"] for r in scoring.table()][:3]
    pv = _import(demo.run("redaction", subjects=chosen))
    assert len(pv.accepted) + len(pv.skipped) == 3 and not pv.refused
    assert demo.run("analyse") is None  # tout est déjà fait


def test_every_prioritized_need_has_a_cached_story():
    cached = {s for (kind, s) in demo.cache() if kind == "user_story"}
    prioritized = {s for (kind, s) in demo.cache() if kind == "prioritization"}
    assert prioritized and prioritized <= cached, sorted(prioritized - cached)


def test_subject_missing_from_cache_is_skipped_never_invented(env, tmp_path, monkeypatch):
    partial = tmp_path / "demo"
    partial.mkdir()
    for f in (ROOT / "handoff" / "demo").glob("*"):
        if "redaction" not in f.name:
            shutil.copy(f, partial / f.name)
    monkeypatch.setenv("PO_DEMO_DIR", str(partial))
    demo._cache.cache_clear()
    _import(demo.run("analyse"))
    _import(demo.run("priorisation"))
    pv = _import(demo.run("redaction", subjects=["SAX-123"]))
    assert not pv.accepted and pv.skipped[0]["reason"].startswith("pas de résultat pré-calculé")
    demo._cache.cache_clear()


def test_demo_results_pass_strict_validation_on_a_fresh_workspace(env):
    msgs = handoff.load_demo()
    assert msgs and all(" 0 refusés" in m for m in msgs), msgs
    assert len(Store().results("feedback_analysis")) == 80


@pytest.mark.parametrize("demo_mode", [True, False])
def test_every_ui_page_renders_in_both_modes(env, demo_mode):
    from streamlit.testing.v1 import AppTest
    settings.save(demo_mode=demo_mode)
    for p in PAGES:  # base vierge
        at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
        at.run()
        at.sidebar.radio[0].set_value(p).run()
        assert not at.exception, (p, [e.value for e in at.exception])
    handoff.load_demo()
    for p in PAGES:  # après les 3 étapes
        at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
        at.run()
        at.sidebar.radio[0].set_value(p).run()
        assert not at.exception, (p, [e.value for e in at.exception])
        assert bool([i for i in at.info if "Mode démo" in i.value]) == demo_mode
