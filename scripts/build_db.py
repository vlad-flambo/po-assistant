"""Construit data/linear.db, un espace Linear fictif, à partir de data/seed/*.json.

Bibliothèque standard uniquement. Déterministe : mêmes fichiers source, même dump SQL.
Ne lit jamais data/ground_truth.json (réservé aux évaluations).

    uv run python scripts/build_db.py [--out chemin.db]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = ROOT / "data" / "seed"
DEFAULT_OUT = ROOT / "data" / "linear.db"

SCHEMA = """
CREATE TABLE workspace_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE teams (
    id   TEXT PRIMARY KEY,
    key  TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
);
CREATE TABLE users (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    display_name TEXT NOT NULL,
    email        TEXT NOT NULL UNIQUE,
    role         TEXT NOT NULL CHECK (role IN ('po','dev','design','support','integration')),
    active       INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE workflow_states (
    id       TEXT PRIMARY KEY,
    team_id  TEXT NOT NULL REFERENCES teams(id),
    name     TEXT NOT NULL,
    type     TEXT NOT NULL CHECK (type IN ('triage','backlog','unstarted','started','completed','canceled')),
    position INTEGER NOT NULL
);
CREATE TABLE labels (
    id        TEXT PRIMARY KEY,
    name      TEXT NOT NULL,
    color     TEXT NOT NULL,
    parent_id TEXT REFERENCES labels(id)
);
CREATE TABLE initiatives (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT NOT NULL,
    target_date TEXT,
    status      TEXT NOT NULL
);
CREATE TABLE projects (
    id            TEXT PRIMARY KEY,
    name          TEXT NOT NULL,
    description   TEXT NOT NULL,
    state         TEXT NOT NULL,
    initiative_id TEXT REFERENCES initiatives(id),
    lead_id       TEXT REFERENCES users(id),
    start_date    TEXT,
    target_date   TEXT
);
CREATE TABLE cycles (
    id        TEXT PRIMARY KEY,
    team_id   TEXT NOT NULL REFERENCES teams(id),
    number    INTEGER NOT NULL,
    name      TEXT NOT NULL,
    starts_at TEXT NOT NULL,
    ends_at   TEXT NOT NULL
);
CREATE TABLE issues (
    id              TEXT PRIMARY KEY,
    identifier      TEXT NOT NULL UNIQUE,
    team_id         TEXT NOT NULL REFERENCES teams(id),
    title           TEXT NOT NULL,
    description     TEXT NOT NULL,
    state_id        TEXT NOT NULL REFERENCES workflow_states(id),
    priority        INTEGER NOT NULL CHECK (priority BETWEEN 0 AND 4),
    estimate        INTEGER,
    assignee_id     TEXT REFERENCES users(id),
    creator_id      TEXT NOT NULL REFERENCES users(id),
    project_id      TEXT REFERENCES projects(id),
    cycle_id        TEXT REFERENCES cycles(id),
    duplicate_of_id TEXT REFERENCES issues(id),
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    completed_at    TEXT,
    canceled_at     TEXT,
    source_type     TEXT NOT NULL CHECK (source_type IN ('support_ticket','email','feedback_chat','internal')),
    source_metadata TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE issue_labels (
    issue_id TEXT NOT NULL REFERENCES issues(id),
    label_id TEXT NOT NULL REFERENCES labels(id),
    PRIMARY KEY (issue_id, label_id)
);
CREATE TABLE comments (
    id         TEXT PRIMARY KEY,
    issue_id   TEXT NOT NULL REFERENCES issues(id),
    user_id    TEXT NOT NULL REFERENCES users(id),
    body       TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE customers (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    domain      TEXT,
    segment     TEXT NOT NULL CHECK (segment IN ('b2c','b2b')),
    plan        TEXT NOT NULL CHECK (plan IN ('free','plus','business')),
    revenue_eur INTEGER NOT NULL DEFAULT 0,
    size        INTEGER,
    status      TEXT NOT NULL CHECK (status IN ('active','at_risk','churned')),
    owner_id    TEXT REFERENCES users(id),
    created_at  TEXT NOT NULL
);
CREATE TABLE customer_needs (
    id          TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES customers(id),
    issue_id    TEXT REFERENCES issues(id),
    project_id  TEXT REFERENCES projects(id),
    body        TEXT NOT NULL,
    priority    INTEGER NOT NULL DEFAULT 0 CHECK (priority IN (0,1)),
    source_type TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
CREATE INDEX idx_issues_state ON issues(state_id);
CREATE INDEX idx_needs_issue ON customer_needs(issue_id);
CREATE INDEX idx_needs_customer ON customer_needs(customer_id);
"""

# Utilisateur d'intégration qui crée l'issue de Triage, par canal.
INTEGRATION_CREATOR = {
    "support_ticket": "usr_int_zendesk",
    "email": "usr_int_email",
    "feedback_chat": "usr_int_chat",
}
CHANNEL_LABEL = {
    "support_ticket": "lbl_canal_support",
    "email": "lbl_canal_email",
    "feedback_chat": "lbl_canal_chat",
}
ISSUE_COLUMNS = [
    "id", "identifier", "team_id", "title", "description", "state_id", "priority",
    "estimate", "assignee_id", "creator_id", "project_id", "cycle_id", "duplicate_of_id",
    "created_at", "updated_at", "completed_at", "canceled_at", "source_type", "source_metadata",
]


def load(name: str) -> dict:
    path = SEED / name
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def insert(conn: sqlite3.Connection, table: str, row: dict) -> None:
    cols = list(row)
    conn.execute(
        f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join('?' for _ in cols)})",
        [row[c] for c in cols],
    )


def dumps(value) -> str:
    return json.dumps(value or {}, ensure_ascii=False, sort_keys=True)


def insert_issue(conn, issue: dict, label_ids: dict[str, str]) -> None:
    row = {c: issue.get(c) for c in ISSUE_COLUMNS}
    row["id"] = row["id"] or issue["identifier"]
    row["team_id"] = row["team_id"] or "team_sax"
    row["updated_at"] = row["updated_at"] or issue["created_at"]
    row["priority"] = row["priority"] if row["priority"] is not None else 0
    row["source_type"] = row["source_type"] or "internal"
    row["source_metadata"] = dumps(issue.get("source_metadata"))
    insert(conn, "issues", row)
    for name in issue.get("labels", []):
        insert(conn, "issue_labels", {"issue_id": row["id"], "label_id": label_ids.get(name, name)})


def build(out: Path) -> Path:
    workspace = load("workspace.json")
    customers = load("customers.json")
    backlog = load("backlog.json")
    feedbacks = load("feedbacks.json")

    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    conn = sqlite3.connect(out)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)

    with conn:
        for key, value in sorted(workspace.get("workspace_meta", {}).items()):
            insert(conn, "workspace_meta", {"key": key, "value": value if isinstance(value, str) else dumps(value)})
        for table in ["teams", "users", "workflow_states", "labels", "initiatives", "projects", "cycles"]:
            # Les étiquettes parentes d'abord (clé étrangère parent_id).
            rows = workspace.get(table, [])
            if table == "labels":
                rows = sorted(rows, key=lambda r: r.get("parent_id") is not None)
            for row in rows:
                insert(conn, table, row)
        label_ids = {r["name"]: r["id"] for r in workspace.get("labels", [])}
        label_ids.update({r["id"]: r["id"] for r in workspace.get("labels", [])})

        for row in customers.get("customers", []):
            insert(conn, "customers", row)

        # Backlog : issues d'abord (les doublons pointent vers d'autres issues), puis le reste.
        issues = backlog.get("issues", [])
        for issue in issues:
            insert_issue(conn, {**issue, "duplicate_of_id": None}, label_ids)
        for issue in issues:
            if issue.get("duplicate_of_id"):
                conn.execute("UPDATE issues SET duplicate_of_id = ? WHERE id = ?",
                             (issue["duplicate_of_id"], issue.get("id") or issue["identifier"]))
            iid = issue.get("id") or issue["identifier"]
            for c in issue.get("comments", []):
                insert(conn, "comments", {"issue_id": iid, **c})
            for n in issue.get("customer_needs", []):
                insert(conn, "customer_needs", {"issue_id": iid, "project_id": None, "priority": 0,
                                                "source_type": "internal", **n})

        # Feedbacks : chacun devient une issue en Triage + une demande client.
        for fb in feedbacks.get("feedbacks", []):
            channel = fb["source_type"]
            issue = {
                "identifier": fb["identifier"],
                "title": fb["title"],
                "description": fb["description"],
                "state_id": "st_triage",
                "priority": 0,
                "creator_id": INTEGRATION_CREATOR[channel],
                "created_at": fb["created_at"],
                "source_type": channel,
                "source_metadata": fb.get("source_metadata"),
                "labels": [CHANNEL_LABEL[channel], *fb.get("labels", [])],
            }
            insert_issue(conn, issue, label_ids)
            insert(conn, "customer_needs", {
                "id": f"need_{fb['identifier'].lower().replace('-', '_')}",
                "customer_id": fb["customer_id"],
                "issue_id": fb["identifier"],
                "project_id": None,
                "body": fb.get("need_body") or fb["description"],
                "priority": fb.get("need_priority", 0),
                "source_type": channel,
                "created_at": fb["created_at"],
            })

    problems = conn.execute("PRAGMA foreign_key_check").fetchall()
    if problems:
        raise SystemExit(f"Clés étrangères invalides : {problems[:5]}")
    conn.execute("VACUUM")
    conn.close()
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    out = build(args.out)
    conn = sqlite3.connect(out)
    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ["users", "customers", "issues", "customer_needs", "comments"]}
    conn.close()
    print(f"{out.relative_to(ROOT) if out.is_relative_to(ROOT) else out} : " +
          ", ".join(f"{k}={v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
