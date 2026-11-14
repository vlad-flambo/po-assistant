"""Cycle 021: re-score the stored postings of one candidate IN MEMORY with the app's own scoring functions, and compare with what is stored.

    DATABASE_URL=postgres://...replay021 uv run python docs/sdlc/cycles/021-bilingual-keyword-scoring/evidence/replay_harness.py <candidate pk> [--save out.json]

READ ONLY. It never writes to the database it is pointed at (no `score_job`, no `update_or_create`), and it switches the word-count file cache off
(`CACHE_DIR` empty) so a run on a scratch copy cannot replace the counts the real runner keeps in data/cache. Point it only at a scratch copy.

What it replays: every scored view of the candidate (Score rows), with the candidate's current Config, the similarity model built from the
database it is pointed at, and the employer-boilerplate counts, exactly as `matching.score_views` does.
"""

from __future__ import annotations

import json
import os
import statistics as st
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, str(ROOT))

import django

django.setup()

from django.conf import settings

settings.CACHE_DIR = ""  # corpus._path() is None: no file is read or replaced

from jobs.models import Candidate, CandidateJob, Config, Score
from jobs.services import breadth, scoring


def replay(candidate_pk: int, limit: int | None = None) -> tuple[list[dict], dict]:
    cand = Candidate.objects.get(pk=candidate_pk)
    cfg = Config.get(cand)
    floor = breadth.floor(cfg.filters)
    views = (CandidateJob.objects.filter(candidate=cand, score__isnull=False).select_related("job", "score").order_by("pk"))
    if limit:
        views = views[:limit]
    views = list(views)
    t0 = time.perf_counter()
    sim = scoring.cached_similarity(cfg)
    boiler = scoring.company_boilerplate(cfg, {v.company for v in views if v.company})
    t_setup = time.perf_counter() - t0
    t1 = time.perf_counter()
    rows = []
    for v in views:
        b = scoring.deterministic_breakdown(v, cfg, sim, boiler)
        s = v.score
        rows.append(dict(
            job=v.job_id, lang=v.job.language or "", title=v.job.title, company=v.job.company, status=v.status,
            kw=round(b.keyword, 1), sim=round(b.similarity, 1), adj=b.seniority, det=round(b.deterministic, 1),
            key_found=b.analysis.key_found, key_total=b.analysis.key_total, hits=b.analysis.hits, missing=b.analysis.missing, via=b.analysis.via,
            stored_kw=s.rule_score, stored_sim=s.similarity_score, stored_adj=s.seniority_adj, stored_det=s.deterministic_score,
            stored_version=s.profile_version, ai=s.ai_score, stored_hits=s.matched_keywords or []))
    meta = dict(candidate=candidate_pk, floor=floor, keyword_weight=cfg.keyword_weight, profile_version=cfg.profile_version,
                keywords=len(cfg.keywords.get("include") or {}), seconds_setup=round(t_setup, 2), seconds_scoring=round(time.perf_counter() - t1, 2), n=len(rows),
                glossary_on=getattr(settings, "GLOSSARY_ON", None))
    return rows, meta


def _mean(xs):
    xs = list(xs)
    return st.mean(xs) if xs else float("nan")


def sanity(rows: list[dict], meta: dict) -> None:
    """Does the replay reproduce the stored scores? Tolerances: the similarity depends on word counts taken at another time."""
    print(f"\n== sanity: replay against stored scores (candidate {meta['candidate']}, {len(rows)} views, profile v{meta['profile_version']}) ==")
    same_version = [r for r in rows if r["stored_version"] == meta["profile_version"]]
    print(f"stored with the current profile version: {len(same_version)} of {len(rows)}")
    for label, subset in (("all", rows), ("current profile version", same_version)):
        if not subset:
            continue
        kw_diff = [abs(r["kw"] - (r["stored_kw"] or 0)) for r in subset]
        sim_diff = [abs(r["sim"] - (r["stored_sim"] or 0)) for r in subset]
        det_diff = [abs(r["det"] - r["stored_det"]) for r in subset]
        print(f"[{label}] keyword: equal to 0.1 in {100*sum(d <= 0.1 for d in kw_diff)/len(subset):.1f}% (max diff {max(kw_diff):.1f}) | "
              f"similarity: within 1 point in {100*sum(d <= 1 for d in sim_diff)/len(subset):.1f}%, within 3 in {100*sum(d <= 3 for d in sim_diff)/len(subset):.1f}% "
              f"(mean diff {_mean(sim_diff):.2f}) | deterministic: within 1 point in {100*sum(d <= 1 for d in det_diff)/len(subset):.1f}%, within 3 in "
              f"{100*sum(d <= 3 for d in det_diff)/len(subset):.1f}% (mean diff {_mean(det_diff):.2f}, max {max(det_diff):.1f})")
        lower = sum(1 for r in subset if r["kw"] < (r["stored_kw"] or 0) - 0.1)
        higher = sum(1 for r in subset if r["kw"] > (r["stored_kw"] or 0) + 0.1)
        lost = sum(1 for r in subset if set(r["stored_hits"]) - set(r["hits"]))
        print(f"[{label}] keyword score replayed higher than stored: {higher}, lower: {lower}; postings where a stored match is no longer found: {lost}")
        crossed = sum(1 for r in subset if (r["det"] >= meta["floor"]) != (r["stored_det"] >= meta["floor"]))
        print(f"[{label}] postings on the other side of the floor {meta['floor']} after the replay: {crossed}")


def measures(rows: list[dict], meta: dict) -> None:
    floor = meta["floor"]
    print(f"\n== replayed scores by language (floor {floor}) ==")
    for lang in ("fr", "en", ""):
        sub = [r for r in rows if r["lang"] == lang]
        if not sub:
            continue
        print(f"lang={lang or 'unknown':8} n={len(sub):5} det mean={_mean(r['det'] for r in sub):5.1f} | kw mean={_mean(r['kw'] for r in sub):5.1f} | "
              f"sim mean={_mean(r['sim'] for r in sub):5.1f} | at or above floor {100*sum(r['det'] >= floor for r in sub)/len(sub):4.1f}% | "
              f"0 key words {100*sum(r['key_found'] == 0 for r in sub)/len(sub):4.1f}%")


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    pk = int(args[0])
    out = args[args.index("--save") + 1] if "--save" in args else None
    rows, meta = replay(pk)
    print("meta:", meta)
    sanity(rows, meta)
    measures(rows, meta)
    if out:
        Path(out).write_text(json.dumps({"meta": meta, "rows": rows}, ensure_ascii=False), encoding="utf-8")
        print("saved", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
