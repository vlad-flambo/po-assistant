"""Bloc B (ARBITRER) : scores calculés par le code à partir des données et des estimations importées.

- RICE = Reach × Impact × Confiance / Effort (Reach mesuré, les 3 autres estimés par l'agent et ajustables par le PO).
- Score pondéré : critères normalisés 0-1 et poids réglables par le PO (simulation « et si »).
- MoSCoW : proposé par l'agent, modifiable par le PO.
- Proposition de cycle : remplir la capacité restante, Must d'abord puis par score.
"""
from __future__ import annotations

from . import insights
from .linear import LinearClient
from .store import Store

KIND = "prioritization"
MOSCOW_RANK = {"must": 0, "should": 1, "could": 2, "wont": 3}
DEFAULT_WEIGHTS = {"reach": 0.30, "impact": 0.25, "arr_at_risk": 0.20, "okr": 0.15, "trend": 0.10}
CRITERIA = {
    "reach": "Personnes touchées (candidats + sièges Business)",
    "impact": "Impact par personne (estimé par l'agent)",
    "arr_at_risk": "ARR Business en risque de churn",
    "okr": "Alignement sur un objectif du trimestre",
    "trend": "Demandes des 4 dernières semaines",
}


REACH_MODES = {"personnes": "Personnes touchées : 1 par candidat, les sièges pour un compte Business",
               "clients": "Clients distincts : 1 par candidat comme par compte Business"}


def table(linear: LinearClient | None = None, store: Store | None = None, *, weights: dict | None = None,
          overrides: dict | None = None, reach_mode: str = "personnes") -> list[dict]:
    """Une ligne par besoin estimé. overrides = {target: {impact, confidence, effort_points, moscow}} saisis par le PO."""
    linear, store = linear or LinearClient(), store or Store()
    weights = weights or DEFAULT_WEIGHTS
    overrides = overrides or {}
    data = insights.load(linear, store)
    demand = {d["target"]: d for d in insights.demands(data)}
    est = store.results(KIND)
    rows = []
    for target, res in est.items():
        o = {**res["output"], **overrides.get(target, {})}
        d = demand.get(target, {})
        b = data["backlog"].get(target)
        if b and b["state_type"] in ("completed", "canceled"):
            continue
        reach = d.get("reach", 0) if reach_mode == "personnes" else d.get("customers", 0)
        effort = o["effort_points"] or 1
        rows.append({
            "target": target, "title": b["title"] if b else d.get("title", target), "state": b["state_name"] if b else "À créer",
            "is_new": b is None, "project": b["project_name"] if b else None,
            "reach": reach, "impact": o["impact"], "confidence": o["confidence"], "effort": effort,
            "rice": round(reach * o["impact"] * o["confidence"] / effort, 1),
            "moscow": o["moscow"], "okr": o.get("okr"), "rationale": o["rationale"], "risks": o.get("risks"),
            "customers": d.get("customers", 0), "b2b": d.get("b2b", 0), "arr_at_risk_eur": d.get("arr_at_risk_eur", 0),
            "recent_4w": d.get("recent_4w", 0), "mentions": d.get("mentions", 0),
            "current_priority": b["priority"] if b else None, "overridden": target in overrides,
        })
    _weighted(rows, weights)
    rows.sort(key=lambda r: -r["rice"])
    for k, r in enumerate(rows, 1):
        r["rank_rice"] = k
    for k, r in enumerate(sorted(rows, key=lambda r: -r["weighted"]), 1):
        r["rank_weighted"] = k
    return rows


def _weighted(rows: list[dict], w: dict) -> None:
    def norm(key):
        mx = max((r[key] for r in rows), default=0) or 1
        return {r["target"]: r[key] / mx for r in rows}
    n = {k: norm(k) for k in ("reach", "arr_at_risk_eur", "recent_4w")}
    total = sum(w.values()) or 1
    for r in rows:
        parts = {
            "reach": n["reach"][r["target"]],
            "impact": r["impact"] / 3,
            "arr_at_risk": n["arr_at_risk_eur"][r["target"]],
            "okr": 1.0 if r["okr"] else 0.0,
            "trend": n["recent_4w"][r["target"]],
        }
        r["weighted"] = round(100 * sum(w.get(k, 0) * v for k, v in parts.items()) / total, 1)
        r["weighted_parts"] = parts


def cycle_proposal(rows: list[dict], linear: LinearClient | None = None, *, key: str = "rice") -> dict:
    """Propose le contenu du cycle en cours : capacité moins le reste à faire des issues déjà en cours."""
    linear = linear or LinearClient()
    meta = linear.meta()
    capacity = int(meta.get("team_capacity_points_per_cycle") or 20)
    cyc = linear.current_cycle()
    carry = []
    for b in linear.backlog_issues():
        if b["cycle_id"] == (cyc or {}).get("id") and b["state_name"] in ("In Progress", "In Review"):
            remaining = (b["estimate"] or 0) * (0.5 if b["state_name"] == "In Progress" else 0.0)
            carry.append({"target": b["identifier"], "title": b["title"], "state": b["state_name"], "remaining": remaining})
    planned_todo = [b["identifier"] for b in linear.backlog_issues()
                    if b["cycle_id"] == (cyc or {}).get("id") and b["state_name"] == "Todo"]
    left = capacity - sum(c["remaining"] for c in carry)
    picked, rest = [], []
    order = sorted([r for r in rows if r["moscow"] != "wont"], key=lambda r: (MOSCOW_RANK[r["moscow"]], -r[key]))
    budget = left
    for r in order:
        if r["effort"] <= budget:
            picked.append(r)
            budget -= r["effort"]
        else:
            rest.append(r)
    return {"cycle": cyc, "capacity": capacity, "carry_over": carry, "capacity_left": left,
            "picked": picked, "points_picked": sum(r["effort"] for r in picked), "not_picked": rest,
            "planned_todo_before": planned_todo,
            "dropped_from_plan": [t for t in planned_todo if t not in {r["target"] for r in picked}]}
