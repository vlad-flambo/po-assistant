"""Base de travail de l'agent (data/po_assist.db) : exports, tâches, imports, résultats."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS exports (
    id          TEXT PRIMARY KEY,
    pack        TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    file        TEXT NOT NULL,
    task_count  INTEGER NOT NULL,
    instructions_version INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS tasks (
    export_id  TEXT NOT NULL REFERENCES exports(id),
    task       TEXT NOT NULL,
    kind       TEXT NOT NULL,
    subject    TEXT NOT NULL,
    status     TEXT NOT NULL CHECK (status IN ('exported','done','skipped','refused')),
    reason     TEXT,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (export_id, task)
);
CREATE TABLE IF NOT EXISTS imports (
    sha256      TEXT PRIMARY KEY,
    file        TEXT NOT NULL,
    export_id   TEXT NOT NULL,
    imported_at TEXT NOT NULL,
    summary     TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS results (
    kind        TEXT NOT NULL,
    subject     TEXT NOT NULL,
    export_id   TEXT NOT NULL,
    task        TEXT NOT NULL,
    output      TEXT NOT NULL,
    agent       TEXT,
    imported_at TEXT NOT NULL,
    PRIMARY KEY (kind, subject)
);
"""


class Store:
    def __init__(self, path: Path | None = None):
        self.path = Path(path or config.assist_db())
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def result(self, kind: str, subject: str) -> dict | None:
        r = self.conn.execute("SELECT * FROM results WHERE kind = ? AND subject = ?", (kind, subject)).fetchone()
        return {**dict(r), "output": json.loads(r["output"])} if r else None

    def results(self, kind: str) -> dict[str, dict]:
        return {r["subject"]: {**dict(r), "output": json.loads(r["output"])}
                for r in self.conn.execute("SELECT * FROM results WHERE kind = ? ORDER BY subject", (kind,))}

    def subjects_done(self, kind: str) -> set[str]:
        return {r[0] for r in self.conn.execute("SELECT subject FROM results WHERE kind = ?", (kind,))}

    def open_tasks(self, pack: str | None = None) -> list[dict]:
        sql = "SELECT t.*, e.pack FROM tasks t JOIN exports e ON e.id = t.export_id WHERE t.status = 'exported'"
        params = ()
        if pack:
            sql += " AND e.pack = ?"
            params = (pack,)
        return [dict(r) for r in self.conn.execute(sql, params)]

    def exports(self) -> list[dict]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM exports ORDER BY created_at DESC")]

    def imports(self) -> list[dict]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM imports ORDER BY imported_at DESC")]
