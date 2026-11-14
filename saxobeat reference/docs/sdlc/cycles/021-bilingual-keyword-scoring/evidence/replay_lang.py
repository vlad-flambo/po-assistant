# Read-only: compare stored scores by posting language, for one candidate, on the LOCAL Postgres copy. Writes nothing.
import statistics as st
from jobs.models import Candidate, CandidateJob, Config, Score
from jobs.services import breadth

cands = list(Candidate.objects.all())
for c in cands:
    print("candidate", c.pk, getattr(c, "name", ""), getattr(c, "code", ""), str(c)[:40])
cfg = Config.objects.get(pk=1)
cand = cfg.candidate
floor = breadth.floor(cfg.filters)
inc = cfg.keywords.get("include") or {}
print("candidate of config 1:", cand.pk, "| include", len(inc), "| weight>=3:", sum(1 for w in inc.values() if float(w) >= 3), "| floor", floor, "| keyword_weight", cfg.keyword_weight)
print("sample of keywords:", list(inc.items())[:12])

rows = (Score.objects.filter(job__candidate=cand)
        .values_list("job__job__language", "deterministic_score", "rule_score", "similarity_score", "key_counts", "ai_score", "job__status", "final_score"))
rows = list(rows)
print("scored rows", len(rows))

def summary(label, sub):
    if not sub:
        print(f"{label:34} n=0"); return
    det = [r[1] for r in sub]; kw = [r[2] or 0 for r in sub]; sim = [r[3] or 0 for r in sub]
    zero = sum(1 for r in sub if r[4] and r[4][0] == 0)
    known = sum(1 for r in sub if r[4])
    print(f"{label:34} n={len(sub):6} det mean={st.mean(det):5.1f} med={st.median(det):5.1f} | kw mean={st.mean(kw):5.1f} | sim mean={st.mean(sim):5.1f} "
          f"| >=floor {100*sum(d>=floor for d in det)/len(det):4.1f}% | 0 key words {100*zero/max(known,1):4.1f}% (of {known})")

by = {lang: [r for r in rows if r[0] == lang] for lang in ("fr", "en", "")}
print("\n== all scored postings, by language ==")
for lang, sub in by.items():
    summary(f"lang={lang or 'unknown'}", sub)

print("\n== postings the AI reviewed as good fits (ai_score >= 70): did the rules let them through? ==")
for lang, sub in by.items():
    summary(f"lang={lang or 'unknown'} ai>=70", [r for r in sub if r[5] is not None and r[5] >= 70])
print("\n== AI-reviewed, any score ==")
for lang, sub in by.items():
    summary(f"lang={lang or 'unknown'} reviewed", [r for r in sub if r[5] is not None])

pipeline = {"applied", "interview", "interviewing", "offer", "screening", "phone_screen", "technical", "final"}
print("\nstatuses present:", sorted({r[6] for r in rows}))
print("\n== postings the candidate moved into the pipeline (applied or beyond) ==")
for lang, sub in by.items():
    summary(f"lang={lang or 'unknown'} pipeline", [r for r in sub if r[6] in CandidateJob.PIPELINE])

# top missing words in French vs English for the AI>=70 group
from collections import Counter
for lang in ("fr", "en"):
    cnt = Counter(); n = 0
    for r in Score.objects.filter(job__candidate=cand, ai_score__gte=70, job__job__language=lang).values_list("missing_keywords", flat=True):
        n += 1; cnt.update(r or [])
    print(f"\nlang={lang}: most-missed key words among {n} AI>=70 postings:", cnt.most_common(8))
