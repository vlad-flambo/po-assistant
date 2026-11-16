"""Mesure la qualité des analyses importées contre la vérité terrain (data/ground_truth.json).

Utilisé par les développeurs et dans la démo (« comment sait-on que l'agent est fiable ? »).
L'agent, lui, ne voit jamais ce fichier.
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import combinations

from .config import ROOT
from .store import Store


def _f1(p: float, r: float) -> float:
    return 2 * p * r / (p + r) if p + r else 0.0


def evaluate(store: Store | None = None, gt_path=None) -> dict:
    store = store or Store()
    gt = {g["identifier"]: g for g in json.loads((gt_path or ROOT / "data" / "ground_truth.json").read_text())["feedbacks"]}
    res = {k: v["output"] for k, v in store.results("feedback_analysis").items() if k in gt}
    n = len(res)
    if not n:
        return {"analysed": 0}
    type_ok = sum(res[k]["type"] == gt[k]["type"] for k in res)
    confusion = Counter((gt[k]["type"], res[k]["type"]) for k in res if res[k]["type"] != gt[k]["type"])
    # thème principal : le premier thème de l'agent figure-t-il parmi les thèmes attendus ?
    with_theme = [k for k in res if gt[k]["themes"]]
    theme_ok = sum(bool(res[k]["themes"]) and res[k]["themes"][0] in gt[k]["themes"] for k in with_theme)
    churn_tp = sum(res[k]["churn_risk"] and gt[k]["churn_risk"] for k in res)
    churn_p = sum(res[k]["churn_risk"] for k in res)
    churn_t = sum(gt[k]["churn_risk"] for k in res)
    # rattachement aux issues existantes (SAX-n)
    exp = {(k, r["target"]) for k in res for r in gt[k]["requests"] if not r["target"].startswith("NEW:")}
    got = {(k, r["target"]) for k in res for r in res[k]["requests"] if not r["target"].startswith("NEW:")}
    link_p = len(exp & got) / len(got) if got else 0.0
    link_r = len(exp & got) / len(exp) if exp else 0.0
    # besoins nouveaux : deux feedbacks du même NEW attendu reçoivent-ils le même NEW chez l'agent ?
    def new_groups(src):
        g = {}
        for k in res:
            for r in src[k]["requests"]:
                if r["target"].startswith("NEW:"):
                    g.setdefault(r["target"], set()).add(k)
        return g
    exp_new, got_new = new_groups(gt), new_groups(res)
    exp_pairs = {p for ks in exp_new.values() for p in combinations(sorted(ks), 2)}
    got_pairs = {p for ks in got_new.values() for p in combinations(sorted(ks), 2)}
    pair_p = len(exp_pairs & got_pairs) / len(got_pairs) if got_pairs else 0.0
    pair_r = len(exp_pairs & got_pairs) / len(exp_pairs) if exp_pairs else 0.0
    new_found = sum(any(r["target"].startswith("NEW:") for r in res[k]["requests"])
                    for k in res if any(r["target"].startswith("NEW:") for r in gt[k]["requests"]))
    new_expected = sum(any(r["target"].startswith("NEW:") for r in gt[k]["requests"]) for k in res)
    no_request = [k for k in res if not gt[k]["requests"]]
    no_request_ok = sum(not res[k]["requests"] for k in no_request)
    req_count_ok = sum(len(res[k]["requests"]) == len(gt[k]["requests"]) for k in res)
    traps = {}
    for trap in ["P2", "P3", "P5", "P6", "P7", "P8"]:
        ks = [k for k in res if trap in gt[k]["traps"]]
        if trap == "P2":
            ok = sum(len(res[k]["requests"]) >= len(gt[k]["requests"]) for k in ks)
        elif trap == "P3":
            ok = sum(res[k]["type"] == gt[k]["type"] for k in ks)
        elif trap == "P5":
            ok = sum(res[k]["churn_risk"] for k in ks)
        elif trap in ("P6", "P8"):
            ok = sum(not res[k]["requests"] for k in ks)
        else:  # P7 : rattaché à l'issue Done/Canceled attendue
            ok = sum({r["target"] for r in gt[k]["requests"]} <= {r["target"] for r in res[k]["requests"]} for k in ks)
        traps[trap] = {"ok": ok, "total": len(ks)}
    return {
        "analysed": n,
        "type_accuracy": type_ok / n,
        "type_confusions": {f"{a}→{b}": c for (a, b), c in confusion.most_common()},
        "main_theme_accuracy": theme_ok / len(with_theme) if with_theme else None,
        "churn": {"precision": churn_tp / churn_p if churn_p else 0.0, "recall": churn_tp / churn_t if churn_t else 0.0,
                  "found": churn_tp, "expected": churn_t, "flagged": churn_p},
        "backlog_links": {"precision": link_p, "recall": link_r, "f1": _f1(link_p, link_r), "expected": len(exp), "proposed": len(got)},
        "new_needs": {"feedbacks_with_new_found": new_found, "expected": new_expected,
                      "grouping_precision": pair_p, "grouping_recall": pair_r},
        "no_request_correct": {"ok": no_request_ok, "total": len(no_request)},
        "request_count_exact": req_count_ok / n,
        "traps": traps,
    }


def report_markdown(m: dict) -> str:
    if not m.get("analysed"):
        return "Aucune analyse importée."
    pct = lambda x: f"{100 * x:.0f} %"
    lines = [
        f"| Mesure | Résultat |", "|---|---|",
        f"| Feedbacks évalués | {m['analysed']} |",
        f"| Type correct | {pct(m['type_accuracy'])} |",
        f"| Thème principal correct | {pct(m['main_theme_accuracy'])} |",
        f"| Rattachement au backlog (précision / rappel) | {pct(m['backlog_links']['precision'])} / {pct(m['backlog_links']['recall'])} ({m['backlog_links']['expected']} attendus) |",
        f"| Besoins nouveaux repérés | {m['new_needs']['feedbacks_with_new_found']} / {m['new_needs']['expected']} |",
        f"| Regroupement des besoins nouveaux (précision / rappel) | {pct(m['new_needs']['grouping_precision'])} / {pct(m['new_needs']['grouping_recall'])} |",
        f"| Risque de churn (précision / rappel) | {pct(m['churn']['precision'])} / {pct(m['churn']['recall'])} ({m['churn']['expected']} attendus) |",
        f"| Aucune demande inventée (éloges, bruit, vague) | {m['no_request_correct']['ok']} / {m['no_request_correct']['total']} |",
    ]
    names = {"P2": "Plusieurs demandes", "P3": "Bug / demande déguisés", "P5": "Churn Business", "P6": "Bruit, éloges",
             "P7": "Déjà livré ou refusé", "P8": "Feedback vague"}
    lines += ["", "| Piège | Réussi |", "|---|---|"] + [f"| {t} · {names[t]} | {v['ok']} / {v['total']} |" for t, v in m["traps"].items()]
    if m["type_confusions"]:
        lines += ["", "Confusions de type (attendu → agent) : " + ", ".join(f"{k} ×{v}" for k, v in m["type_confusions"].items())]
    return "\n".join(lines)


if __name__ == "__main__":
    print(report_markdown(evaluate()))
