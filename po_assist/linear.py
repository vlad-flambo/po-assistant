"""Faux connecteur Linear : lit (et, sur action explicite, écrit) data/linear.db.

L'interface imite un client d'API Linear : l'application ne sait pas qu'elle parle à SQLite.
Remplacer cette classe par un vrai client GraphQL serait le seul changement pour se brancher sur Linear.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from . import config


def _row(r: sqlite3.Row | None) -> dict | None:
    if r is None:
        return None
    d = dict(r)
    if "source_metadata" in d and isinstance(d["source_metadata"], str):
        d["source_metadata"] = json.loads(d["source_metadata"] or "{}")
    return d


class LinearClient:
    def __init__(self, path: Path | None = None):
        self.path = Path(path or config.linear_db())
        if not self.path.exists():
            raise FileNotFoundError(f"Espace Linear introuvable : {self.path}")
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

    # ---------- lecture ----------
    def meta(self) -> dict:
        out = {}
        for k, v in self.conn.execute("SELECT key, value FROM workspace_meta"):
            try:
                out[k] = json.loads(v)
            except (json.JSONDecodeError, TypeError):
                out[k] = v
        return out

    def _issues(self, where: str, params=()) -> list[dict]:
        sql = f"""SELECT i.*, s.name AS state_name, s.type AS state_type, p.name AS project_name,
                         (SELECT group_concat(l.name, '|') FROM issue_labels il JOIN labels l ON l.id = il.label_id
                          WHERE il.issue_id = i.id) AS label_names
                  FROM issues i JOIN workflow_states s ON s.id = i.state_id
                  LEFT JOIN projects p ON p.id = i.project_id
                  WHERE {where} ORDER BY i.created_at, i.identifier"""
        rows = []
        for r in self.conn.execute(sql, params):
            d = _row(r)
            d["labels"] = d.pop("label_names").split("|") if d.get("label_names") else []
            rows.append(d)
        return rows

    def triage_issues(self) -> list[dict]:
        """Feedbacks entrants encore en Triage, avec le client qui les a émis."""
        issues = self._issues("s.type = 'triage'")
        needs = {r["issue_id"]: r["customer_id"] for r in self.conn.execute("SELECT issue_id, customer_id FROM customer_needs")}
        for i in issues:
            i["customer_id"] = needs.get(i["id"])
        return issues

    def backlog_issues(self) -> list[dict]:
        return self._issues("s.type != 'triage' AND i.state_id != 'st_duplicate'")

    def issue(self, identifier: str) -> dict | None:
        rows = self._issues("i.identifier = ?", (identifier,))
        return rows[0] if rows else None

    def customers(self) -> dict[str, dict]:
        return {r["id"]: dict(r) for r in self.conn.execute("SELECT * FROM customers")}

    def customer_needs(self, issue_identifier: str | None = None) -> list[dict]:
        sql = "SELECT n.*, i.identifier AS issue_identifier FROM customer_needs n LEFT JOIN issues i ON i.id = n.issue_id"
        if issue_identifier:
            return [dict(r) for r in self.conn.execute(sql + " WHERE i.identifier = ? ORDER BY n.created_at", (issue_identifier,))]
        return [dict(r) for r in self.conn.execute(sql + " ORDER BY n.created_at")]

    def projects(self) -> list[dict]:
        return [dict(r) for r in self.conn.execute(
            "SELECT p.*, ini.name AS initiative_name FROM projects p LEFT JOIN initiatives ini ON ini.id = p.initiative_id ORDER BY p.name")]

    def initiatives(self) -> list[dict]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM initiatives ORDER BY name")]

    def cycles(self) -> list[dict]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM cycles ORDER BY number")]

    def current_cycle(self) -> dict | None:
        ref = self.meta().get("reference_date")
        r = self.conn.execute("SELECT * FROM cycles WHERE starts_at <= ? AND ends_at >= ?", (ref, ref)).fetchone()
        return dict(r) if r else None

    # ---------- écriture (actions explicites du PO) ----------
    def _now(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def link_feedback(self, triage_identifier: str, target_identifier: str, body: str | None = None) -> None:
        """Rattache un feedback de Triage à une issue : demande client sur la cible, feedback marqué Duplicate."""
        fb, target = self.issue(triage_identifier), self.issue(target_identifier)
        if not fb or fb["state_type"] != "triage":
            raise ValueError(f"{triage_identifier} n'est pas un feedback en Triage")
        if not target:
            raise ValueError(f"Issue inconnue : {target_identifier}")
        need = self.conn.execute("SELECT * FROM customer_needs WHERE issue_id = ?", (fb["id"],)).fetchone()
        with self.conn:
            self.conn.execute(
                "INSERT INTO customer_needs (id, customer_id, issue_id, project_id, body, priority, source_type, created_at) "
                "VALUES (?, ?, ?, NULL, ?, ?, ?, ?)",
                (f"need_link_{fb['id']}_{target['id']}".lower().replace("-", "_"), need["customer_id"], target["id"],
                 body or need["body"], need["priority"], need["source_type"], fb["created_at"]))
            self.conn.execute("UPDATE issues SET state_id = 'st_duplicate', duplicate_of_id = ?, updated_at = ? WHERE id = ?",
                              (target["id"], self._now(), fb["id"]))

    def create_issue(self, title: str, description: str, *, priority: int = 0, estimate: int | None = None,
                     project_id: str | None = None, labels: list[str] | None = None,
                     state_id: str = "st_backlog", creator_id: str = "usr_camille") -> str:
        n = self.conn.execute("SELECT MAX(CAST(substr(identifier, 5) AS INTEGER)) FROM issues").fetchone()[0] or 0
        ident = f"SAX-{max(n + 1, 301)}"
        now = self._now()
        with self.conn:
            self.conn.execute(
                "INSERT INTO issues (id, identifier, team_id, title, description, state_id, priority, estimate, creator_id, "
                "project_id, created_at, updated_at, source_type, source_metadata) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (ident, ident, "team_sax", title, description, state_id, priority, estimate, creator_id, project_id,
                 now, now, "internal", json.dumps({"origin": "po-assist"}, ensure_ascii=False)))
            for lab in labels or []:
                self.conn.execute("INSERT OR IGNORE INTO issue_labels (issue_id, label_id) VALUES (?, ?)", (ident, lab))
        return ident

    def add_comment(self, identifier: str, body: str, user_id: str = "usr_camille") -> str:
        issue = self.issue(identifier)
        if not issue:
            raise ValueError(f"Issue inconnue : {identifier}")
        n = self.conn.execute("SELECT COUNT(*) FROM comments").fetchone()[0] + 1
        cid = f"com_po_{n}"
        with self.conn:
            self.conn.execute("INSERT INTO comments (id, issue_id, user_id, body, created_at) VALUES (?,?,?,?,?)",
                              (cid, issue["id"], user_id, body, self._now()))
        return cid

