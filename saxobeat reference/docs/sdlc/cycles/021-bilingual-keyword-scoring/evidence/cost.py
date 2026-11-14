"""Cycle 021, slice 9 (spec criterion 16): what the glossary costs. Run it ALONE on the scratch copy (nothing else heavy running).

    DATABASE_URL=postgres://...replay021 uv run python manage.py shell -c "exec(open(r'docs/sdlc/cycles/021-bilingual-keyword-scoring/evidence/cost.py', encoding='utf-8').read())"

Read only. For candidate 1 and a fixed sample of 1,000 scored postings, with the glossary off and on:
  - the time to score the 1,000 postings in memory (best of 3), texts already loaded;
  - the time and the number of SQL statements of the employer-boilerplate counts from a cold cache (`company_boilerplate`);
  - the time to build the text model (the word counts are taken from the database once and kept: not part of the difference).
"""

import random
import time

from django.conf import settings
from django.db import connection
from django.test.utils import CaptureQueriesContext

settings.CACHE_DIR = ""
from jobs.models import CandidateJob, Config
from jobs.services import scoring

cfg = Config.objects.get(candidate_id=1)
views = list(CandidateJob.objects.filter(candidate_id=1, score__isnull=False).select_related("job").order_by("pk"))
random.seed(21)
sample = random.sample(views, 1000)
companies = {v.company for v in sample if v.company}
print(f"sample: {len(sample)} postings of candidate 1, {len(companies)} employers, {sum(len(v.job.description_text) for v in sample) / 1e6:.1f} MB of text")
scoring.corpus.counts(scoring.MAX_CORPUS_DOCS, scoring.MAX_DESCRIPTION_CHARS)  # the word counts, once, outside the measures

results = {}
for on in (False, True):
    settings.GLOSSARY_ON = on
    scoring.clear_caches()
    scoring.corpus.counts(scoring.MAX_CORPUS_DOCS, scoring.MAX_DESCRIPTION_CHARS)
    t = time.perf_counter()
    sim = scoring.cached_similarity(cfg)
    t_model = time.perf_counter() - t
    with CaptureQueriesContext(connection) as ctx:
        t = time.perf_counter()
        boiler = scoring.company_boilerplate(cfg, companies)
        t_boiler = time.perf_counter() - t
    counting = [q for q in ctx.captured_queries if "SUM(CASE" in q["sql"]]
    best = None
    for _ in range(3):
        t = time.perf_counter()
        for v in sample:
            scoring.deterministic_breakdown(v, cfg, sim, boiler)
        d = time.perf_counter() - t
        best = d if best is None else min(best, d)
    terms = len(scoring.search_terms(cfg.keywords.get("include")))
    results[on] = dict(score=best, boiler=t_boiler, statements=len(ctx.captured_queries), counting=len(counting), model=t_model, terms=terms)
    print(f"glossary {'on ' if on else 'off'}: scoring 1,000 postings {best:6.2f} s | boilerplate counts {t_boiler:6.2f} s in {len(ctx.captured_queries)} statements "
          f"({len(counting)} counting queries) over {terms} terms | text model {t_model:5.2f} s")
settings.GLOSSARY_ON = True
off, on = results[False], results[True]
print(f"ratio scoring on/off: {on['score'] / off['score']:.2f} (limit 1.5) | boilerplate counts on/off: {on['boiler'] / off['boiler']:.2f} | terms {off['terms']} -> {on['terms']}")
