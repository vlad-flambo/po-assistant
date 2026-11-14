import os
from django.conf import settings
settings.CACHE_DIR = ""
from jobs.models import Config, Job
from jobs.services import scoring, breadth
text = open(r"docs/sdlc/cycles/021-bilingual-keyword-scoring/evidence/job_33238.md", encoding="utf-8").read().split("\n---\n", 1)[1].strip()
job = Job(title="Change Manager IA H/F", company="eXalt", description_text=text, language="fr")   # never saved
cfg = Config.objects.get(candidate_id=1)
sim = scoring.cached_similarity(cfg)
boiler = scoring.company_boilerplate(cfg, {"eXalt"})
print("eXalt postings in the dump:", Job.objects.filter(company="eXalt").count(), "| boilerplate terms for eXalt:", sorted(boiler.get("eXalt", [])))
for label, b in (("with eXalt boilerplate rule", boiler), ("without it", {})):
    r = scoring.deterministic_breakdown(job, cfg, sim, b)
    print(f"[{label}] keyword {r.keyword:.1f} | similarity {r.similarity:.1f} | seniority {r.seniority:+.0f} | deterministic {r.deterministic:.1f} | floor {breadth.floor(cfg.filters)}")
    print("   hits:", r.analysis.hits, "| key found", r.analysis.key_found, "of", r.analysis.key_total)
    print("   missing:", r.analysis.missing)
