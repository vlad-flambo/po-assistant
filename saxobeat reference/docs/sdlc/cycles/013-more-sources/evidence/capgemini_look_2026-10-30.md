# Capgemini: the bounded look (2026-10-30, slice 8)

Limits kept: public pages and their own scripts only; the address the page itself calls; robots.txt read for both hosts; no login, no forged header, no bot-protection workaround. 11 requests to capgemini.com or its API host (plan: about 20), then 6 more for the rehearsal below.

## What was found
| Question | Answer | How |
|---|---|---|
| Which hiring system is behind the page? | None visible: the job list is drawn by the site's own `cg-jobs` plugin from an open JSON address named in the page (`cg_jobs_jobstream_url = https://cg-jobstream-api.azurewebsites.net/api`) | the saved job page (no request) and its JavaScript bundle (1 request) |
| What does the page call? | `GET <api>/job-search?country_code=fr-fr&size=100&page=N[&search=..&location=..]` for the list and `GET <api>/job-details/<id>` for one job; plain GETs, no key, no cookie, no login | the bundle, offline |
| Does it answer? | Yes: HTTP 200 JSON, `total` 1,163 jobs for fr-fr; 100 jobs a page (1.1 MB, 1.2 s); each row: id, ref, source, title, brand (Capgemini, Capgemini Engineering, Capgemini Invent, Sogeti), location, contract_type, experience_level, apply_job_url, description (HTML) and description_stripped | 5 requests |
| Is there a posting date? | No: `updated_at` / `indexed_at` are the day the index was rebuilt (the same day for every row) | the rows |
| Can it filter by place? | `location=Paris` matches only the exact place text (5 jobs, all "PARIS CEDEX 16"); `search=Paris` is full text (151 jobs, 95 of the first 100 pass our own Paris / Ile-de-France rules). So the adapter reads all pages and filters by our city rules itself | 2 requests |
| robots.txt | `capgemini.com/robots.txt`: `Allow: /` and nothing about jobs; the API host has no robots.txt (404, so nothing is forbidden) | 2 requests |
| Terms | The general terms (Section 6) forbid reproduction without written consent and do not mention automated reading: same posture as the other sites ([employer_terms_2026-10-30.md](employer_terms_2026-10-30.md)). No separate terms for the API were found | read earlier today |
| Job page address | `https://www.capgemini.com/fr-fr/jobs/<ref>+<source lower-case>/`, e.g. `.../384488-fr_FR+sap_btp/` answers 200 | 1 request |

## Verdict
**A source is possible, with a new small adapter** (`jobs/sources/capgemini.py`, type `capgemini`): no existing adapter reads this JSON. It is the site's own interface, not a published API, so it can change without notice (the same standing as the eFinancialCareers source). Not parked: no `unsupported_employers.csv` row for Capgemini.

## What was built and checked
- `jobs/sources/capgemini.py`, registered; seeded **switched off**, once a day (`interval_minutes` 1440): `("Capgemini", "capgemini", {"country_code": "fr-fr", "pages": 15})`. The form's how-to line is in `jobs/sources/howto.py`.
- `tests/test_capgemini_source.py`, 9 tests on four real rows (a fixture): the Paris filter, complete fields, no filter without cities, paging and a job listed twice, the `pages` limit, deleted or unpublished rows skipped, robots.txt obeyed, two runs store each job once, an API error is raised.
- **Postgres rehearsal** on the scratch copy (the real runner, `pages: 3`, 6 requests): run 1 `fetched=134 new=132` (134 links, 132 distinct jobs: two jobs appear in two listings), run 2 `fetched=134 new=0`, counts unchanged; by brand Capgemini 85, Engineering 31, Invent 16, Sogeti 2; average description 4,000 characters; no empty place.
- Whole suite: 1,303 passed, 0 failed (`DATABASE_URL=` SQLite).

## Cost to know about
A full run reads about 12 pages, roughly 13 MB, from Capgemini's API (the owner's PC downloads it; Neon sees only what is stored). About 700 of the 1,163 jobs may match Paris / Ile-de-France by our rules (60 of the first 100 do): that is a large addition to the catalogue and to the runner's reads. Slice 11 measures it.

## Not verified
Whether the API keeps answering without the site's cookies for long; how it treats a burst of requests (we pause 0.5 s between pages); whether jobs that disappear from the list are dropped (the runner's expiry rules apply). The ids (`<ref>_<source>`) are stable in the two runs.
