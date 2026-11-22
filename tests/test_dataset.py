"""Vérifie le jeu de données synthétique (cycle 001, critères 1 à 10 de spec.md)."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sqlite3
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "linear.db"
GT = ROOT / "data" / "ground_truth.json"
BUILD = ROOT / "scripts" / "build_db.py"

spec = importlib.util.spec_from_file_location("build_db", BUILD)
build_db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_db)


def dump_hash(path: Path) -> str:
    conn = sqlite3.connect(path)
    digest = hashlib.sha256("\n".join(conn.iterdump()).encode()).hexdigest()
    conn.close()
    return digest


@pytest.fixture(scope="module")
def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@pytest.fixture(scope="module")
def gt():
    return json.loads(GT.read_text(encoding="utf-8"))


def triage(db):
    return db.execute("SELECT * FROM issues WHERE state_id = 'st_triage' ORDER BY identifier").fetchall()


def backlog(db):
    return db.execute("SELECT * FROM issues WHERE state_id != 'st_triage' ORDER BY identifier").fetchall()


# 1. Construction reproductible, et base commitée à jour
def test_build_is_deterministic_and_committed_db_is_current(tmp_path):
    a = build_db.build(tmp_path / "a.db")
    b = build_db.build(tmp_path / "b.db")
    assert dump_hash(a) == dump_hash(b)
    assert dump_hash(a) == dump_hash(DB), "data/linear.db n'est pas à jour : relancer scripts/build_db.py"


# 2. Schéma et intégrité
def test_schema_and_integrity(db):
    tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    assert tables == {"workspace_meta", "teams", "users", "workflow_states", "labels", "initiatives", "projects",
                      "cycles", "issues", "issue_labels", "comments", "customers", "customer_needs"}
    assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    assert db.execute("PRAGMA foreign_key_check").fetchall() == []


# 3. Feedbacks en Triage
def test_feedbacks(db):
    rows = triage(db)
    assert len(rows) == 80
    assert all("2027-02-01" <= r["created_at"][:10] <= "2027-04-11" for r in rows)
    channels = Counter(r["source_type"] for r in rows)
    for channel, target in {"support_ticket": 28, "email": 24, "feedback_chat": 28}.items():
        assert abs(channels[channel] - target) <= 2, channels
    for r in rows:
        n = db.execute("SELECT COUNT(*) FROM customer_needs WHERE issue_id = ?", (r["id"],)).fetchone()[0]
        assert n == 1, r["identifier"]
        assert r["title"].strip() and len(r["description"]) > 10, r["identifier"]


# 4. Backlog
def test_backlog(db):
    rows = backlog(db)
    assert len(rows) == 30
    states = Counter(r["state_id"] for r in rows)
    for s in ["st_backlog", "st_todo", "st_progress", "st_review", "st_done", "st_canceled"]:
        assert states[s] >= 2, states
    type_labels = {"lbl_bug", "lbl_feature", "lbl_improvement"}
    for r in rows:
        assert 0 <= r["priority"] <= 4
        labels = {x[0] for x in db.execute("SELECT label_id FROM issue_labels WHERE issue_id = ?", (r["id"],))}
        assert len(labels & type_labels) == 1, r["identifier"]
        if r["state_id"] in ("st_todo", "st_progress", "st_review"):
            assert r["estimate"], r["identifier"]
    origins = [json.loads(r["source_metadata"]).get("origin", "") for r in rows]
    assert sum("saxobeat" in o for o in origins) >= 20


# 5. Clients et demandes historiques
def test_customers(db):
    rows = db.execute("SELECT * FROM customers").fetchall()
    assert len(rows) == 60
    b2b = [r for r in rows if r["segment"] == "b2b"]
    assert 8 <= len(b2b) <= 10
    assert all(r["revenue_eur"] > 0 and r["size"] and r["status"] in ("active", "at_risk", "churned") for r in b2b)
    assert all(r["plan"] in ("free", "plus") for r in rows if r["segment"] == "b2c")
    historic = db.execute("""SELECT COUNT(*) FROM customer_needs n JOIN issues i ON i.id = n.issue_id
                             WHERE i.state_id != 'st_triage' AND n.created_at < '2027-02-01'""").fetchone()[0]
    assert historic >= 25
    late = db.execute("""SELECT n.id FROM customer_needs n JOIN customers c ON c.id = n.customer_id
                         WHERE n.created_at < c.created_at""").fetchall()
    assert late == [], "demandes antérieures à la création du client"


# 6. Contexte produit
def test_context(db):
    assert db.execute("SELECT COUNT(*) FROM initiatives").fetchone()[0] == 3
    assert db.execute("SELECT COUNT(*) FROM projects WHERE initiative_id IS NOT NULL").fetchone()[0] >= 4
    roles = Counter(r[0] for r in db.execute("SELECT role FROM users"))
    assert roles["integration"] == 3 and sum(roles.values()) - roles["integration"] == 8
    cycles = db.execute("SELECT starts_at, ends_at FROM cycles ORDER BY number").fetchall()
    for (s1, e1), (s2, _) in zip(cycles, cycles[1:]):
        assert date.fromisoformat(e1) - date.fromisoformat(s1) == timedelta(days=13)
        assert date.fromisoformat(s2) == date.fromisoformat(e1) + timedelta(days=1)
    assert any(s <= "2027-04-12" <= e for s, e in cycles)
    meta = dict(db.execute("SELECT key, value FROM workspace_meta").fetchall())
    assert int(meta["team_capacity_points_per_cycle"]) > 0
    assert meta["reference_date"] == "2027-04-12"


# 7. Langue
def test_languages(db, gt):
    langs = Counter(json.loads(r["source_metadata"])["language"] for r in triage(db))
    assert 14 <= langs["en"] <= 20 and langs["en"] + langs["fr"] == 80
    expected = {f["identifier"]: f["language"] for f in gt["feedbacks"]}
    assert all(json.loads(r["source_metadata"])["language"] == expected[r["identifier"]] for r in triage(db))


# 8. Pièges
def test_traps(gt):
    counts = Counter(t for f in gt["feedbacks"] for t in f["traps"])
    for trap in gt["traps"]:
        assert counts[trap] >= 2, (trap, counts)


def test_p9_matches_data(db, gt):
    historic = {r[0] for r in db.execute("""SELECT n.customer_id FROM customer_needs n JOIN issues i ON i.id = n.issue_id
                                            WHERE i.state_id != 'st_triage'""")}
    owner = {r[0]: r[1] for r in db.execute("""SELECT n.issue_id, n.customer_id FROM customer_needs n
                                               JOIN issues i ON i.id = n.issue_id WHERE i.state_id = 'st_triage'""")}
    seen = set()
    for r in triage(db):
        f = next(f for f in gt["feedbacks"] if f["identifier"] == r["identifier"])
        c = owner[r["id"]]
        assert ("P9" in f["traps"]) == (c in seen or c in historic), r["identifier"]
        seen.add(c)


# 9. Vérité terrain
def test_ground_truth(db, gt):
    ids = {r["identifier"] for r in triage(db)}
    entries = gt["feedbacks"]
    assert {f["identifier"] for f in entries} == ids and len(entries) == 80
    backlog_ids = {r["identifier"] for r in backlog(db)}
    for f in entries:
        assert f["type"] in {"bug", "feature_request", "improvement", "question", "praise", "noise"}
        assert f["sentiment"] in {"negative", "neutral", "positive"}
        assert isinstance(f["churn_risk"], bool)
        assert set(f["themes"]) <= set(gt["themes"])
        assert set(f["traps"]) <= set(gt["traps"])
        for req in f["requests"]:
            assert req["summary"]
            assert req["target"] in backlog_ids or re.fullmatch(r"NEW:[a-z0-9-]+", req["target"]), req
        if f["type"] in {"praise", "noise"} or "P8" in f["traps"]:
            assert f["requests"] == []
    assert "ground_truth" not in BUILD.read_text(encoding="utf-8").replace("Ne lit jamais data/ground_truth.json", "")


# 10. Fiction et confidentialité
def test_fiction_and_privacy(db):
    for (email,) in db.execute("SELECT email FROM users"):
        assert email.endswith(".example")
    for (domain,) in db.execute("SELECT domain FROM customers WHERE domain IS NOT NULL"):
        assert domain.endswith(".example")
    meta = dict(db.execute("SELECT key, value FROM workspace_meta").fetchall())
    assert "fictives" in meta["disclaimer"]
    text = "\n".join(db.iterdump()).lower()
    for addr in re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", text):
        assert addr.endswith(".example"), addr
    # Termes personnels interdits (employeurs, nom), stockés en empreintes SHA-256 pour ne pas les publier
    forbidden = {"bdeadc4a9972526d070a899df19f30b42f297086b36d523ae44866618eefcb80",
                 "4b6f06d9bd2c9d5ca10302c4703a13c815fbaacd23f97bb7750122889737ffc7",
                 "578d179a488febf486ab9fc00c84924100515271e2278e8ef0152eec6360a500",
                 "1b8d4aa083095b5fe68b6fdbd72fe301036e3bc35df3862843a554b3a02a8659"}
    for word in set(re.findall(r"[a-z0-9]+", text)):
        assert hashlib.sha256(word.encode()).hexdigest() not in forbidden, word
