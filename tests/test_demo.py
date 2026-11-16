"""Les résultats réels de l'agent (handoff/demo/) se rejouent sur une base vierge et l'interface s'affiche."""
from __future__ import annotations

from pathlib import Path

from po_assist import handoff, scoring
from po_assist.store import Store

ROOT = Path(__file__).resolve().parent.parent


def test_demo_results_replay_on_a_fresh_workspace(env):
    msgs = handoff.load_demo()
    assert msgs and not any("refus" in m and " 0 refusés" not in m for m in msgs), msgs
    store = Store()
    assert len(store.results("feedback_analysis")) == 80
    if any("priorisation" in p.name for p in (ROOT / "handoff" / "demo").glob("*.results.json")):
        assert scoring.table()
    handoff.load_demo()  # rejouer une seconde fois ne casse rien
    assert len(store.results("feedback_analysis")) == 80


def test_every_ui_page_renders(env):
    from streamlit.testing.v1 import AppTest
    handoff.load_demo()
    pages = ["🤖 Agent", "🏠 Tableau de bord", "📥 Feedbacks", "🧩 Demandes", "⚖️ Priorisation", "✍️ User stories",
             "🎯 Qualité de l'agent"]
    for p in pages:
        at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
        at.run()
        at.sidebar.radio[0].set_value(p).run()
        assert not at.exception, (p, [e.value for e in at.exception])
