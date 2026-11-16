"""Cycles 004 et 005 : priorisation (estimations importées, scores calculés) et rédaction (stories, Linear, exports)."""
from __future__ import annotations

import json

from po_assist import actions, handoff, scoring
from po_assist.linear import LinearClient
from po_assist.store import Store
from tests.test_handoff import write_results


def _results(pack_path, make):
    pack = json.loads(pack_path.read_text())
    out = pack_path.with_name(pack["results_file"])
    out.write_text(json.dumps({"schema": "po-assist.results.v1", "export_id": pack["export_id"], "pack": pack["pack"],
                               "agent": "test", "results": [{"task": t["task"], "kind": t["kind"], "output": make(t)}
                                                            for t in pack["tasks"]]}, ensure_ascii=False))
    return out


def estimate(t):
    ev = t["input"]["evidence"]
    must = ev["arr_at_risk_eur"] > 0
    return {"impact": 2 if must else 1, "confidence": 0.8, "effort_points": t["input"]["team_estimate"] or 5,
            "moscow": "must" if must else ("should" if ev["customers"] >= 3 else "could"),
            "okr": "ini_b2b" if ev["b2b"] else None, "rationale": f"{ev['customers']} clients l'ont demandé, test.", "risks": None}


def story(t):
    return {"title": f"Story {t['subject']}", "user_story": {"as_a": "candidat", "i_want": "x", "so_that": "y"},
            "context": "contexte", "acceptance_criteria": [{"title": f"c{k}", "given": "g", "when": "w", "then": "t"} for k in range(3)],
            "non_functional": [], "out_of_scope": [], "invest": {k: {"ok": True, "note": ""} for k in
                                                                 ["independent", "negotiable", "valuable", "estimable", "small", "testable"]},
            "estimate_points": 5, "estimate_rationale": "simple", "split_proposal": [], "open_questions": []}


def _pipeline():
    handoff.import_file(write_results(handoff.export("analyse")))
    handoff.import_file(_results(handoff.export("priorisation"), estimate))


def test_prioritization_pack_covers_open_needs(env):
    handoff.import_file(write_results(handoff.export("analyse")))
    pack = json.loads(handoff.export("priorisation").read_text())
    subjects = {t["subject"] for t in pack["tasks"]}
    assert "SAX-123" in subjects and "NEW:bug-emails-spam" in subjects
    assert not subjects & {"SAX-101", "SAX-129", "SAX-102"}  # ni livré, ni refusé, ni déjà en cours
    assert {o["id"] for o in pack["context"]["okrs"]} == {"ini_conversion", "ini_activation", "ini_b2b"}


def test_scores_are_computed_by_code_and_follow_po_overrides(env):
    _pipeline()
    rows = scoring.table()
    r = next(x for x in rows if x["target"] == "SAX-123")
    assert r["rice"] == round(r["reach"] * r["impact"] * r["confidence"] / r["effort"], 1)
    assert rows == sorted(rows, key=lambda x: -x["rice"])
    by_clients = {x["target"]: x for x in scoring.table(reach_mode="clients")}
    assert by_clients["SAX-123"]["reach"] == r["customers"] < r["reach"]
    boosted = {x["target"]: x for x in scoring.table(overrides={"NEW:bug-emails-spam": {"impact": 3, "effort_points": 1}})}
    assert boosted["NEW:bug-emails-spam"]["overridden"]
    only_okr = scoring.table(weights={"okr": 1.0})
    assert all(x["weighted"] in (0.0, 100.0) for x in only_okr)


def test_cycle_proposal_respects_capacity(env):
    _pipeline()
    plan = scoring.cycle_proposal(scoring.table())
    assert plan["points_picked"] <= plan["capacity_left"] < plan["capacity"]
    assert plan["carry_over"]  # des issues sont déjà en cours dans le cycle 8
    musts = [r for r in plan["picked"] if r["moscow"] == "must"]
    assert plan["picked"][: len(musts)] == musts


def test_redaction_then_push_to_linear_and_exports(env):
    _pipeline()
    pack = json.loads(handoff.export("redaction", subjects=["SAX-123", "NEW:bug-emails-spam"]).read_text())
    assert [t["subject"] for t in pack["tasks"]] == ["SAX-123", "NEW:bug-emails-spam"]
    assert pack["tasks"][0]["input"]["quotes"]
    res = _results(handoff.config.handoff_dir() / "to-do" / f"{pack['export_id']}.pack.json", story)
    pv, _ = handoff.import_file(res)
    assert len(pv.accepted) == 2
    rows = scoring.table()
    ident = actions.push_story("NEW:bug-emails-spam", prio=next(r for r in rows if r["target"] == "NEW:bug-emails-spam"))
    c = LinearClient()
    assert ident.startswith("SAX-3") and "Critères d'acceptation" in c.issue(ident)["description"]
    assert all(c.issue(fb)["state_name"] == "Duplicate" for fb in ["SAX-205", "SAX-229"])
    actions.push_story("SAX-123")
    assert c.conn.execute("SELECT COUNT(*) FROM comments WHERE issue_id = 'SAX-123'").fetchone()[0] == 2
    assert "Story SAX-123" in actions.stories_markdown(Store(), rows)
    assert actions.stories_csv(Store(), rows).startswith("Title,Description,Priority,Estimate")


def test_story_validation_rejects_incomplete_output(env):
    from po_assist.packs.redaction import RedactionPack
    bad = story({"subject": "x"}) | {"acceptance_criteria": [{"title": "a"}], "estimate_points": 13, "split_proposal": []}
    errs = RedactionPack().validate(bad, "x", {})
    assert any("acceptance_criteria" in e for e in errs) and any("split_proposal" in e for e in errs)
