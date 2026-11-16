"""Bloc A (COMPRENDRE) : agrégats déterministes calculés à partir des analyses importées.

L'IA classe chaque feedback (pack « analyse ») ; le code compte, regroupe et date. Aucun chiffre ne vient du LLM.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date, timedelta

from .linear import LinearClient
from .packs.analyse import THEMES
from .store import Store

KIND = "feedback_analysis"


def _week(ts: str) -> str:
    d = date.fromisoformat(ts[:10])
    return (d - timedelta(days=d.weekday())).isoformat()


def load(linear: LinearClient | None = None, store: Store | None = None) -> dict:
    linear, store = linear or LinearClient(), store or Store()
    customers = linear.customers()
    feedbacks = {i["identifier"]: i for i in linear.triage_issues()}
    # les feedbacks déjà rattachés dans Linear (Duplicate) restent comptés : on lit toutes les analyses connues
    analyses = store.results(KIND)
    for ident in analyses:
        if ident not in feedbacks:
            i = linear.issue(ident)
            if i:
                needs = linear.customer_needs(ident)
                i["customer_id"] = needs[0]["customer_id"] if needs else None
                feedbacks[ident] = i
    return {"linear": linear, "customers": customers, "feedbacks": feedbacks, "analyses": analyses,
            "backlog": {b["identifier"]: b for b in linear.backlog_issues()}, "meta": linear.meta()}


def reach_of(customer: dict) -> int:
    """Personnes touchées : 1 pour un candidat, le nombre de sièges pour un compte Business."""
    return int(customer.get("size") or 1) if customer["segment"] == "b2b" else 1


def demands(data: dict) -> list[dict]:
    """Une ligne par besoin (issue du backlog ou NEW:<slug>), avec ses preuves."""
    by_target: dict[str, dict] = defaultdict(lambda: {"feedbacks": [], "quotes": [], "summaries": [], "customers": set(),
                                                     "churn": set(), "weeks": Counter(), "historic": 0})
    for ident, res in data["analyses"].items():
        fb = data["feedbacks"].get(ident)
        if not fb:
            continue
        out = res["output"]
        for r in out.get("requests", []):
            d = by_target[r["target"]]
            d["feedbacks"].append(ident)
            d["quotes"].append({"feedback": ident, "quote": r["quote"], "customer_id": fb["customer_id"]})
            d["summaries"].append(r["summary"])
            d["customers"].add(fb["customer_id"])
            d["weeks"][_week(fb["created_at"])] += 1
            if out.get("churn_risk"):
                d["churn"].add(fb["customer_id"])
    # demandes historiques déjà rattachées aux issues du backlog (avant la période)
    for n in data["linear"].customer_needs():
        tgt = n["issue_identifier"]
        if tgt in data["backlog"] and n["created_at"] < "2027-02-01":
            d = by_target[tgt]
            d["historic"] += 1
            d["customers"].add(n["customer_id"])
    ref = date.fromisoformat(data["meta"]["reference_date"])
    recent_from = (ref - timedelta(days=28)).isoformat()
    rows = []
    for tgt, d in by_target.items():
        cs = [data["customers"][c] for c in d["customers"] if c in data["customers"]]
        b = data["backlog"].get(tgt)
        recent = sum(n for w, n in d["weeks"].items() if w >= recent_from)
        rows.append({
            "target": tgt,
            "title": b["title"] if b else _best_summary(d["summaries"]),
            "is_new": b is None,
            "state": b["state_name"] if b else "À créer",
            "priority": b["priority"] if b else None,
            "estimate": b["estimate"] if b else None,
            "project": b["project_name"] if b else None,
            "feedbacks": sorted(set(d["feedbacks"])),
            "mentions": len(d["feedbacks"]),
            "historic_requests": d["historic"],
            "customers": len(cs),
            "b2c": sum(c["segment"] == "b2c" for c in cs),
            "b2b": sum(c["segment"] == "b2b" for c in cs),
            "plus": sum(c["plan"] == "plus" for c in cs),
            "reach": sum(reach_of(c) for c in cs),
            "arr_b2b_eur": sum(c["revenue_eur"] for c in cs if c["segment"] == "b2b" and c["status"] != "churned"),
            "churn_customers": len(d["churn"]),
            "arr_at_risk_eur": sum(data["customers"][c]["revenue_eur"] for c in d["churn"]
                                   if data["customers"][c]["status"] != "churned"),
            "recent_4w": recent,
            "previous": len(d["feedbacks"]) - recent,
            "quotes": d["quotes"],
            "summaries": d["summaries"],
        })
    rows.sort(key=lambda r: (-r["customers"], -r["mentions"], r["target"]))
    return rows


def _best_summary(summaries: list[str]) -> str:
    return min(summaries, key=len) if summaries else ""


def themes(data: dict) -> list[dict]:
    weeks = sorted({_week(f["created_at"]) for f in data["feedbacks"].values()})
    rows = []
    for tid, label in THEMES.items():
        series = Counter()
        neg = 0
        for ident, res in data["analyses"].items():
            if tid in res["output"].get("themes", []):
                fb = data["feedbacks"].get(ident)
                if fb:
                    series[_week(fb["created_at"])] += 1
                    neg += res["output"].get("sentiment") == "negative"
        total = sum(series.values())
        half = len(weeks) // 2
        first, second = sum(series[w] for w in weeks[:half]), sum(series[w] for w in weeks[half:])
        rows.append({"theme": tid, "label": label, "count": total, "negative": neg,
                     "first_half": first, "second_half": second, "trend": second - first,
                     "weekly": [series[w] for w in weeks], "weeks": weeks})
    return sorted(rows, key=lambda r: -r["count"])


def alerts(data: dict) -> dict:
    churn, shipped, follow_up = [], [], []
    for ident, res in sorted(data["analyses"].items()):
        out, fb = res["output"], data["feedbacks"].get(ident)
        if not fb:
            continue
        c = data["customers"].get(fb["customer_id"], {})
        if out.get("churn_risk"):
            churn.append({"feedback": ident, "customer_id": c.get("id"), "customer": c.get("name"), "segment": c.get("segment"),
                          "plan": c.get("plan"), "arr_eur": c.get("revenue_eur", 0), "status": c.get("status"),
                          "summary": out["summary"], "date": fb["created_at"][:10]})
        for r in out.get("requests", []):
            b = data["backlog"].get(r["target"])
            if b and b["state_type"] in ("completed", "canceled"):
                shipped.append({"feedback": ident, "target": r["target"], "state": b["state_name"], "title": b["title"],
                                "note": r.get("target_status_note"), "customer": c.get("name")})
        if out.get("follow_up_question"):
            follow_up.append({"feedback": ident, "customer": c.get("name"), "question": out["follow_up_question"]})
    churn.sort(key=lambda x: -(x["arr_eur"] or 0))
    return {"churn": churn, "already_decided": shipped, "follow_up": follow_up}


def overview(data: dict) -> dict:
    a = data["analyses"].values()
    types = Counter(r["output"]["type"] for r in a)
    sentiments = Counter(r["output"]["sentiment"] for r in a)
    channels = Counter(f["source_type"] for f in data["feedbacks"].values() if f["identifier"] in data["analyses"])
    return {"feedbacks": len(data["feedbacks"]), "analysed": len(data["analyses"]), "types": dict(types),
            "sentiments": dict(sentiments), "channels": dict(channels)}
