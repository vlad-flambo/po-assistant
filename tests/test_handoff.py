"""Cycle 002 : export, vérification, import idempotent, fichiers partiels, connecteur Linear."""
from __future__ import annotations

import json
from pathlib import Path

from po_assist import handoff
from po_assist.linear import LinearClient
from po_assist.store import Store

ROOT = Path(__file__).resolve().parent.parent
GT = {f["identifier"]: f for f in json.loads((ROOT / "data" / "ground_truth.json").read_text())["feedbacks"]}


def perfect_output(subject: str, text: str) -> dict:
    """Ce qu'un agent parfait répondrait (d'après la vérité terrain), avec une citation prise dans le texte."""
    g = GT[subject]
    quote = " ".join(text.split()[:8])
    return {"type": g["type"], "themes": g["themes"][:3], "sentiment": g["sentiment"], "churn_risk": g["churn_risk"],
            "summary": g["notes"][:200],
            "requests": [{"summary": r["summary"], "target": r["target"], "target_status_note": None, "quote": quote}
                         for r in g["requests"]],
            "follow_up_question": "Pouvez-vous préciser ?" if "P8" in g["traps"] else None}


def write_results(pack_path: Path, mutate=None, only=None) -> Path:
    pack = json.loads(pack_path.read_text())
    results = []
    for t in pack["tasks"]:
        if only and t["task"] not in only:
            continue
        res = {"task": t["task"], "kind": t["kind"], "output": perfect_output(t["subject"], t["input"]["text"])}
        if mutate:
            res = mutate(res, t)
        if res:
            results.append(res)
    out = pack_path.with_name(pack["results_file"])
    out.write_text(json.dumps({"schema": "po-assist.results.v1", "export_id": pack["export_id"], "pack": pack["pack"],
                               "agent": "test", "results": results}, ensure_ascii=False))
    return out


def test_linear_connector_reads_workspace(env):
    c = LinearClient()
    assert len(c.triage_issues()) == 80 and len(c.backlog_issues()) == 30
    assert all(i["customer_id"] for i in c.triage_issues())
    assert c.current_cycle()["name"] == "Cycle 8"


# Critère 1
def test_export_is_self_contained_and_anonymous(env):
    path = handoff.export("analyse")
    pack = json.loads(path.read_text())
    for key in ["schema", "export_id", "pack", "results_file", "task_count", "agent_brief", "instructions",
                "output_format", "results_envelope", "context", "tasks", "checklist"]:
        assert key in pack, key
    assert pack["task_count"] == len(pack["tasks"]) == 80
    assert len(pack["context"]["backlog"]) == 30 and len(pack["context"]["themes"]) == 12
    names = {c["name"] for c in LinearClient().customers().values()}
    customers_blob = json.dumps([t["input"]["customer"] for t in pack["tasks"]], ensure_ascii=False)
    assert not any(n in customers_blob for n in names)
    assert handoff.export("analyse") is None  # tout est déjà exporté


# Critère 2
def test_valid_results_are_applied(env):
    res = write_results(handoff.export("analyse"))
    pv, msg = handoff.import_file(res)
    assert len(pv.accepted) == 80 and not pv.refused, msg
    store = Store()
    assert len(store.results("feedback_analysis")) == 80
    assert store.open_tasks("analyse") == []
    assert (env / "handoff" / "done" / res.name).exists()


# Critère 3
def test_invalid_results_are_refused_with_reasons(env):
    pack_path = handoff.export("analyse")

    def corrupt(res, t):
        n = int(t["task"][2:])
        o = res["output"]
        if n == 1:
            o["type"] = "complaint"
        elif n == 2:
            o["themes"] = ["T99"]
        elif n == 3 and o["requests"]:
            o["requests"][0]["target"] = "SAX-999"
        elif n == 3:
            o["requests"] = [{"summary": "x", "target": "SAX-999", "target_status_note": None, "quote": "ceci n'est pas dans le texte"}]
        elif n == 4:
            o["requests"] = [{"summary": "x", "target": "NEW:test", "target_status_note": None, "quote": "phrase inventée par l'agent"}]
        return res

    res = write_results(pack_path, mutate=corrupt)
    pv = handoff.check(res)
    refused = {r["task"]: " ".join(r["reasons"]) for r in pv.refused}
    assert set(refused) == {"T-001", "T-002", "T-003", "T-004"}
    assert "type invalide" in refused["T-001"]
    assert "themes invalide" in refused["T-002"]
    assert "target inconnu" in refused["T-003"]
    assert "quote absente" in refused["T-004"]
    # mode strict : rien n'est écrit
    msg = handoff.apply(pv, strict=True)
    assert "Rien importé" in msg and Store().results("feedback_analysis") == {}
    # mode normal : les 76 valides passent, les 4 refusés restent à refaire
    pv2 = handoff.check(res)
    handoff.apply(pv2)
    assert len(Store().results("feedback_analysis")) == 76
    assert handoff.status()["packs"]["analyse"]["to_do"] == 4


def test_unknown_export_or_garbage_is_fatal(env):
    bad = env / "bad.results.json"
    bad.write_text("pas du json")
    assert "JSON illisible" in handoff.check(bad).fatal
    bad.write_text(json.dumps({"schema": "po-assist.results.v1", "export_id": "E-inconnu", "pack": "analyse", "results": []}))
    assert "export inconnu" in handoff.check(bad).fatal


# Critère 4
def test_reimport_is_a_no_op(env):
    res = write_results(handoff.export("analyse"))
    copy = env / "copy.results.json"
    copy.write_bytes(res.read_bytes())
    handoff.import_file(res)
    pv, msg = handoff.import_file(copy)
    assert pv.already_imported and "Déjà importé" in msg
    assert len(Store().results("feedback_analysis")) == 80


# Critère 5
def test_partial_and_skipped_results(env):
    pack_path = handoff.export("analyse")

    def skip_some(res, t):
        if t["task"] in ("T-010", "T-011"):
            return {"task": t["task"], "kind": t["kind"], "skipped": "texte illisible"}
        return res

    first = [f"T-{k:03d}" for k in range(1, 21)]
    res = write_results(pack_path, mutate=skip_some, only=set(first))
    pv, _ = handoff.import_file(res)
    assert len(pv.accepted) == 18 and len(pv.skipped) == 2 and len(pv.missing) == 60
    st = handoff.status()["packs"]["analyse"]
    assert st["done"] == 18 and st["exported"] == 60 and st["to_do"] == 2
    nxt = json.loads(handoff.export("analyse").read_text())
    assert nxt["task_count"] == 2  # les 2 ignorées repartent, pas celles encore en cours


def test_fenced_json_pasted_from_chat_is_accepted(env):
    res = write_results(handoff.export("analyse"))
    res.write_text("```json\n" + res.read_text() + "\n```")
    assert len(handoff.check(res).accepted) == 80


def test_link_and_create_in_linear(env):
    c = LinearClient()
    c.link_feedback("SAX-201", "SAX-110")
    assert c.issue("SAX-201")["state_name"] == "Duplicate"
    assert len(c.customer_needs("SAX-110")) == 5
    ident = c.create_issue("Ajouter les entretiens à l'agenda", "desc", labels=["lbl_feature"])
    assert ident == "SAX-301" and c.issue(ident)["labels"] == ["Feature"]
