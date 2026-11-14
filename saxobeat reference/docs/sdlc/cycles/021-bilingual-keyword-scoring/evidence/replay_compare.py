"""Cycle 021: compare two replays saved by replay_harness.py (--save): the baseline (glossary off) and a later one.

    uv run python docs/sdlc/cycles/021-bilingual-keyword-scoring/evidence/replay_compare.py BASELINE.json AFTER.json [--examples N] [--md out.md]

Prints, for the candidate of the files:
  - whether any keyword or deterministic score changed where it must not (identical check), and whether any keyword score went DOWN (spec criterion 6);
  - the means and the floor shares by language, before and after;
  - the same-role control (spec criterion 12): for each role concept of the glossary with at least 20 French and 20 English postings having a term of
    the concept in the title, the mean deterministic score of each language and the gap; the mean of the absolute gaps;
  - how many postings rise above and fall below the floor, by language, with examples (criterion 14c);
  - the no-harm checks of criterion 14 (English mean, applied and AI 70+ jobs under the floor).
Needs no database for the numbers; the role concepts come from jobs/glossary.py (importing it needs Django settings only).
"""

from __future__ import annotations

import json
import os
import re
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, str(ROOT))

import django

django.setup()

from jobs import glossary
from jobs.text import normalize

PIPELINE = {"applied", "interviewing", "offer", "shortlisted", "withdrawn", "rejected"}


def load(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return d["meta"], {r["job"]: r for r in d["rows"]}


def mean(xs):
    xs = list(xs)
    return st.mean(xs) if xs else float("nan")


def has(term: str, text: str) -> bool:
    return term in text and re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", text) is not None


def role_control(rows: dict, key: str = "det", min_n: int = 20):
    out = []
    for concept in glossary.role_concepts():
        groups = {"fr": [], "en": []}
        for r in rows.values():
            if r["lang"] not in groups:
                continue
            title = normalize(r["title"])
            if any(has(t, title) for t in concept.terms):
                groups[r["lang"]].append(r[key])
        if len(groups["fr"]) >= min_n and len(groups["en"]) >= min_n:
            out.append((concept.en[0], len(groups["fr"]), mean(groups["fr"]), len(groups["en"]), mean(groups["en"])))
    return out


def main() -> int:
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        return 1
    n_examples = int(args[args.index("--examples") + 1]) if "--examples" in args else 10
    md = args[args.index("--md") + 1] if "--md" in args else None
    meta0, base = load(args[0])
    meta1, new = load(args[1])
    floor = meta1["floor"]
    lines: list[str] = []

    def say(s=""):
        print(s)
        lines.append(s)

    say(f"# Replay comparison, candidate {meta1['candidate']} ({len(new)} postings), glossary {meta0.get('glossary_on')} -> {meta1.get('glossary_on')}, floor {floor}\n")
    common = [j for j in new if j in base]
    kw_down = [j for j in common if new[j]["kw"] < base[j]["kw"] - 1e-9]
    kw_up = [j for j in common if new[j]["kw"] > base[j]["kw"] + 1e-9]
    sim_changed = [j for j in common if abs(new[j]["sim"] - base[j]["sim"]) > 1e-9]
    say(f"- keyword score: {len(kw_up)} up, {len(kw_down)} DOWN, {len(common) - len(kw_up) - len(kw_down)} unchanged; similarity changed on {len(sim_changed)}")
    say("\n## By language\n")
    say("| Language | n | det before | det after | kw before | kw after | sim before | sim after | floor share before | after |\n|---|---|---|---|---|---|---|---|---|---|")
    for lang in ("fr", "en", ""):
        js = [j for j in common if new[j]["lang"] == lang]
        if not js:
            continue
        f = lambda rows, k: mean(rows[j][k] for j in js)
        sh = lambda rows: 100 * sum(rows[j]["det"] >= floor for j in js) / len(js)
        say(f"| {lang or 'unknown'} | {len(js)} | {f(base, 'det'):.1f} | {f(new, 'det'):.1f} | {f(base, 'kw'):.1f} | {f(new, 'kw'):.1f} | {f(base, 'sim'):.1f} | {f(new, 'sim'):.1f} | {sh(base):.1f}% | {sh(new):.1f}% |")
    fr = [j for j in common if new[j]["lang"] == "fr"]
    en = [j for j in common if new[j]["lang"] == "en"]
    say(f"\nWhole-pool gap (English minus French, deterministic mean): before {mean(base[j]['det'] for j in en) - mean(base[j]['det'] for j in fr):.1f}, after "
        f"{mean(new[j]['det'] for j in en) - mean(new[j]['det'] for j in fr):.1f}")

    say("\n## Same-role control (role concepts of the glossary, at least 20 postings of each language with a term of the concept in the title)\n")
    before, after = role_control(base), role_control(new)
    after_by = {r[0]: r for r in after}
    say("| Role concept | FR n | FR before | FR after | EN n | EN before | EN after | gap before (EN-FR) | gap after |\n|---|---|---|---|---|---|---|---|---|")
    gaps_b, gaps_a = [], []
    for name, nf, mf, ne, me in before:
        a = after_by.get(name)
        if not a:
            continue
        gaps_b.append(abs(me - mf))
        gaps_a.append(abs(a[4] - a[2]))
        say(f"| {name} | {nf} | {mf:.1f} | {a[2]:.1f} | {ne} | {me:.1f} | {a[4]:.1f} | {me - mf:+.1f} | {a[4] - a[2]:+.1f} |")
    if gaps_b:
        say(f"\nRoles compared: {len(gaps_b)}. **Mean absolute gap: before {mean(gaps_b):.1f}, after {mean(gaps_a):.1f}** (criterion 12: at most 10 after).")
    else:
        say("\nNo role concept has 20 postings in each language.")

    say("\n## Crossing the floor\n")
    up = [j for j in common if new[j]["det"] >= floor > base[j]["det"]]
    down = [j for j in common if new[j]["det"] < floor <= base[j]["det"]]
    for lang in ("fr", "en", ""):
        say(f"- {lang or 'unknown'}: {sum(new[j]['lang'] == lang for j in up)} rise above the floor, {sum(new[j]['lang'] == lang for j in down)} fall below it")
    protected = [j for j in common if base[j]["status"] in PIPELINE or (base[j]["ai"] or 0) >= 70]
    fell = [j for j in protected if j in down]
    say(f"- applied-or-beyond jobs and AI 70+ jobs: {len(protected)}; falling from above the floor to below: {len(fell)} (criterion 14b: none)")
    en_b, en_a = mean(base[j]["det"] for j in en), mean(new[j]["det"] for j in en)
    say(f"- English mean deterministic: {en_b:.1f} -> {en_a:.1f} ({en_a - en_b:+.1f}; criterion 14a: not below -1)")

    def example(j):
        n, b = new[j], base[j]
        how = ", ".join(f"{k} (via {v})" for k, v in []) or ""
        return f"| {j} | {n['lang']} | {n['title'][:60]} | {n['company'][:25]} | {b['det']} | {n['det']} | {', '.join(n['hits'][:4])} |"

    import random

    rng = random.Random(21)
    for title, js in (("Examples: rise above the floor", up), ("Examples: fall below the floor", down)):
        say(f"\n### {title} (the {n_examples} biggest moves)\n")
        say("| Job | Lang | Title | Company | Before | After | Hits after |\n|---|---|---|---|---|---|---|")
        for j in sorted(js, key=lambda j: -abs(new[j]["det"] - base[j]["det"]))[:n_examples]:
            say(example(j))
        if len(js) > n_examples:
            say(f"\n### {title} ({n_examples} drawn at random, seed 21, so the list is not only the biggest moves)\n")
            say("| Job | Lang | Title | Company | Before | After | Hits after |\n|---|---|---|---|---|---|---|")
            for j in sorted(rng.sample(js, n_examples)):
                say(example(j))
    if md:
        Path(md).write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("wrote", md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
