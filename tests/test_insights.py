"""Cycle 003 : agrégats (demandes, thèmes, alertes) et évaluation contre la vérité terrain."""
from __future__ import annotations

from po_assist import evaluate, handoff, insights
from tests.test_handoff import GT, write_results


def _import_perfect():
    res = write_results(handoff.export("analyse"))
    handoff.import_file(res)


def test_demands_count_distinct_customers_and_reach(env):
    _import_perfect()
    data = insights.load()
    rows = {r["target"]: r for r in insights.demands(data)}
    expected = sum(r["target"] == "SAX-110" for f in GT.values() for r in f["requests"])
    alerts_ = rows["SAX-110"]  # alertes e-mail : mentions dans la file + 4 demandes historiques
    assert alerts_["mentions"] == expected and alerts_["historic_requests"] == 4
    assert alerts_["customers"] <= alerts_["mentions"] + alerts_["historic_requests"]
    dash = rows["SAX-123"]  # tableau conseiller : réclamé par des comptes Business → reach en sièges
    assert dash["b2b"] >= 3 and dash["reach"] > dash["customers"]
    assert dash["arr_at_risk_eur"] >= 36000  # Cap Rebond
    spam = rows["NEW:bug-emails-spam"]
    assert spam["is_new"] and spam["mentions"] == 4 and spam["recent_4w"] >= 2


def test_themes_and_alerts(env):
    _import_perfect()
    data = insights.load()
    th = insights.themes(data)
    assert th[0]["theme"] == "T10"  # Business, thème dominant et en hausse
    assert th[0]["trend"] > 0
    al = insights.alerts(data)
    assert al["churn"][0]["arr_eur"] == 36000
    assert {a["target"] for a in al["already_decided"]} >= {"SAX-129", "SAX-119"}
    assert insights.overview(data)["analysed"] == 80


def test_evaluation_of_a_perfect_agent(env):
    _import_perfect()
    m = evaluate.evaluate()
    assert m["type_accuracy"] == 1.0 and m["churn"]["recall"] == 1.0
    assert m["backlog_links"]["f1"] == 1.0 and m["new_needs"]["grouping_recall"] == 1.0
    assert "Type correct" in evaluate.report_markdown(m)
