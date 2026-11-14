# Live look at the 24 flagged "covered" employers (2026-11-03, slice 5)

The 24 from [recheck_2026-10-30.md](recheck_2026-10-30.md) (3 missing, 13 empty, 8 suspect), read on a fresh scratch copy of the 29 Oct dump. Two read-only checks, both with the app's own code: (1) each source fetched with its adapter (at most 5 jobs where the adapter takes a cap); (2) for the slug-based systems (SmartRecruiters, Greenhouse, Lever, Ashby, Workable, Teamtailor), **the company name the board's own API reports**, because the adapters label every job with the company name from the source's configuration, so a name match on the jobs proves nothing (my first pass made that mistake, and a first version of the second pass took the company name instead of the board id: both corrected before anything was concluded). Requests: about 60. The owner's review (slice 4) is replaced by my recommendations below: **they are applied to the local lists and to the "switch off" list, and are reversible; say so if you disagree with any.**

## Result: 6 wrong or test boards, 3 stale claims, 15 real boards

| Employer | Source type | Board's own name | Jobs on the board | What it is | Recommendation |
|---|---|---|---|---|---|
| 10x Banking | workable | 10x Banking | 4 | real small board (4 jobs, UK) | keep the source; the list line stays |
| Accenture | recruitee | - | - | no source existed: the claim was a stale guess (seeded off in step 1) | set the list line back to unknown |
| Cegid | smartrecruiters | Cegid | 1 | real board (the API names it Cegid), 1 job, Canada | keep the source; the list line stays |
| Celonis | greenhouse | Celonis | 225 | real board, 225 jobs (one titled "(Demo)"), 8 in France | keep the source; the list line stays |
| Lyra | smartrecruiters | Lyra | 1 | real board (named Lyra), 1 job, Egypt | keep the source; the list line stays |
| Monext (Crédit Mutuel Arkéa) | smartrecruiters | MONEXT | 6 | real board (MONEXT), 6 jobs, in Aix-en-Provence | keep the source; the list line stays |
| Oliver Wyman | lever | - | 2 | small board, 2 jobs, no name from the API | keep the source; the list line stays |
| Trade Republic | greenhouse | - | 0 | its Greenhouse board is empty now | **switch the hosted source off; set the list line to unknown** |
| Google Cloud | recruitee | - | - | no source existed: a stale guess | set the list line back to unknown |
| Unit | ashby | - | 2 | small board, 2 jobs (Tel Aviv), no name from the API | keep the source; the list line stays |
| Energy Pool | smartrecruiters | - | 0 | SmartRecruiters knows no such company id: the board does not exist (a wrong guess) | **switch the hosted source off; set the list line to unknown** |
| Bénéteau | successfactors | - | - | SuccessFactors site from its own careers link: 5 jobs, 1 in France | keep the source; the list line stays |
| Coface | smartrecruiters | Coface | 227 | real board, 227 jobs, none in Paris / Ile-de-France | keep the source; the list line stays |
| Esker | teamtailor | - | 0 | its Teamtailor feed answers 404 (it fails on every pass) | **switch the hosted source off; set the list line to unknown** |
| EssilorLuxottica | smartrecruiters | EssilorLuxottica Demo | 7 | the board's name is "EssilorLuxottica Demo": a demo account | **switch the hosted source off; set the list line to unknown** |
| GTT (Gaztransport & Technigaz) | smartrecruiters | GTT | 30 | real board (GTT), 30 jobs, in Yvelines | keep the source; the list line stays |
| Legrand | oraclehcm | - | - | Oracle site from its own careers link: the read with a Paris keyword returns nothing (not an identity problem) | keep the source; the list line stays |
| LVMH | smartrecruiters | LVMH | 59 | real board, 59 jobs, none in your cities | keep the source; the list line stays |
| Publicis Groupe | smartrecruiters | - | 0 | SmartRecruiters knows no such company id (a wrong guess; its jobs are on iCIMS, robots forbid the list) | **switch the hosted source off; set the list line to unknown** |
| Rémy Cointreau | successfactors | - | - | SuccessFactors site: 5 jobs, none in France | keep the source; the list line stays |
| SES | successfactors | - | - | SuccessFactors site: 5 jobs, none in France | keep the source; the list line stays |
| Sodexo | smartrecruiters | Sodexo | 155 | real board, 155 jobs, none in your cities | keep the source; the list line stays |
| Google | recruitee | - | - | no source existed: a stale guess | set the list line back to unknown |
| Uber | smartrecruiters | Uber | 1 | the board holds one job, titled "Test UAT": a test account | **switch the hosted source off; set the list line to unknown** |

## Why 14 real boards were "empty" or "suspect"
The runner (and the re-check) look at what the source **stored**: its adapters skip jobs outside the owner's cities before they are read in full (SmartRecruiters, SuccessFactors) or the re-check judged small boards without a job in France as suspect. These boards are the right ones; they simply have no job in Paris or Ile-de-France today (LVMH 59 jobs, Sodexo 155, Coface 227, Celonis 225). Nothing to correct.

## What was changed
- **The four `data/employer_coverage*.csv` lists:** 10 lines (9 employers) set from `covered` back to `unknown` with the reason: Accenture, Google, Google Cloud (stale claims), Energy Pool, Publicis Groupe, Trade Republic, Esker, Uber, EssilorLuxottica. Dated copies of the four files before the change are in `data/archive/` (`*_before_cycle013_2026-11-03.csv`). Best status across the lists: **covered 252 to 243, unknown 327 to 336, unsupported 14** (the consulting verdicts are not written yet: S2.8 waits for the hosted sources).
- **The "switch off" list for the owner's hosted step (slice 12 or 21), six sources, to be disabled on the Sources page (not deleted):** `Energy Pool (smartrecruiters)`, `Publicis Groupe (smartrecruiters)`, `Trade Republic (greenhouse)`, `Esker (teamtailor)`, `Uber (smartrecruiters)`, `EssilorLuxottica (smartrecruiters)`. They read nothing useful, or the wrong company's jobs; `Esker` fails on every pass. The hosted database may have changed since the 29 Oct dump: the dry-run listing shows the names.

## Not verified
Whether Legrand's Oracle site really has no job for the keyword (a different question from identity); that the six are the only wrong ones among the 245 `ok` sources (the check was on the flagged ones); the Wipro-style case of an `ok` board with no job in France.
