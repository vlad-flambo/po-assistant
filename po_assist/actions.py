"""Actions explicites du PO vers Linear, et exports (Markdown, CSV)."""
from __future__ import annotations

import csv
import io

from . import insights
from .linear import LinearClient
from .store import Store

PRIORITY_FROM_MOSCOW = {"must": 1, "should": 2, "could": 3, "wont": 4}


def story_markdown(target: str, s: dict, prio: dict | None = None) -> str:
    us = s["user_story"]
    lines = [f"**En tant que** {us['as_a']}, **je veux** {us['i_want']}, **afin de** {us['so_that']}.", "",
             "## Contexte", s["context"], "", "## Critères d'acceptation"]
    for k, c in enumerate(s["acceptance_criteria"], 1):
        lines += [f"**{k}. {c['title']}**", f"- *Étant donné* {c['given']}", f"- *Quand* {c['when']}", f"- *Alors* {c['then']}", ""]
    if s["non_functional"]:
        lines += ["## Exigences non fonctionnelles"] + [f"- {x}" for x in s["non_functional"]] + [""]
    if s["out_of_scope"]:
        lines += ["## Hors périmètre"] + [f"- {x}" for x in s["out_of_scope"]] + [""]
    lines += ["## Estimation", f"{s['estimate_points']} points : {s['estimate_rationale']}", ""]
    if s["split_proposal"]:
        lines += ["## Découpage proposé"] + [f"- {x}" for x in s["split_proposal"]] + [""]
    if s["open_questions"]:
        lines += ["## Questions ouvertes"] + [f"- {x}" for x in s["open_questions"]] + [""]
    inv = ", ".join(f"{k[0].upper()} {'✓' if v['ok'] else '✗'}" for k, v in s["invest"].items())
    lines += [f"INVEST : {inv}"]
    if prio:
        lines += [f"Priorisation : RICE {prio['rice']} · MoSCoW {prio['moscow']} · {prio['rationale']}"]
    lines += ["", f"_Rédigé par PO Assist à partir des feedbacks ({target})._"]
    return "\n".join(lines)


def push_story(target: str, *, linear: LinearClient | None = None, store: Store | None = None,
               prio: dict | None = None, link_feedbacks: bool = True) -> str:
    """Crée (besoin nouveau) ou complète (issue existante) l'issue Linear, puis rattache les feedbacks sources."""
    linear, store = linear or LinearClient(), store or Store()
    res = store.result("user_story", target)
    if not res:
        raise ValueError(f"Aucune story importée pour {target}")
    s = res["output"]
    body = story_markdown(target, s, prio)
    if target.startswith("NEW:"):
        ident = linear.create_issue(s["title"], body, estimate=s["estimate_points"],
                                    priority=PRIORITY_FROM_MOSCOW.get((prio or {}).get("moscow"), 0))
    else:
        ident = target
        linear.add_comment(ident, "Story rédigée par PO Assist :\n\n" + body)
    if link_feedbacks:
        data = insights.load(linear, store)
        for d in insights.demands(data):
            if d["target"] == target:
                for fb in d["feedbacks"]:
                    if linear.issue(fb)["state_type"] == "triage":
                        linear.link_feedback(fb, ident)
    with store.conn:
        store.conn.execute("CREATE TABLE IF NOT EXISTS pushes (target TEXT PRIMARY KEY, issue TEXT, pushed_at TEXT)")
        store.conn.execute("INSERT OR REPLACE INTO pushes VALUES (?, ?, datetime('now'))", (target, ident))
    return ident


def stories_markdown(store: Store | None = None, prio_rows: list[dict] | None = None) -> str:
    store = store or Store()
    prio = {r["target"]: r for r in (prio_rows or [])}
    parts = ["# User stories rédigées par PO Assist", ""]
    for target, res in store.results("user_story").items():
        parts += [f"# {res['output']['title']} ({target})", "", story_markdown(target, res["output"], prio.get(target)), "", "---", ""]
    return "\n".join(parts)


def stories_csv(store: Store | None = None, prio_rows: list[dict] | None = None) -> str:
    """CSV au format d'import de Linear (Title, Description, Priority, Estimate, Labels)."""
    store = store or Store()
    prio = {r["target"]: r for r in (prio_rows or [])}
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["Title", "Description", "Priority", "Estimate", "Labels", "Source"])
    for target, res in store.results("user_story").items():
        s, p = res["output"], prio.get(target, {})
        w.writerow([s["title"], story_markdown(target, s, p or None), PRIORITY_FROM_MOSCOW.get(p.get("moscow"), 0),
                    s["estimate_points"], "PO Assist", target])
    return buf.getvalue()
