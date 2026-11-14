# Neon reads of the consulting sources BCG and EY, on the scratch copy (2026-11-03, step 2 slice 20)

How: as in step 1's slice 11 ([new_sources_measurement_2026-10-30.md](new_sources_measurement_2026-10-30.md)): `scripts/measure_reads.ps1` restored the newest dump (29 Oct, 328 sources) into a scratch Postgres (`measure_20261103123044`, kept), `scripts/step_new_sources.py` (now taking the names of the sources, and migrating the scratch schema first) seeded and enabled the two **in the scratch copy only**, ran each through the real runner (run 1: real fetch and ingest), then replayed the same postings with no network (run 2: the steady state). Bytes are what the Postgres container sent (what Neon counts as transfer), decimal MB. Raw lines: `new_sources_run_step2.jsonl`, `measurements.jsonl`.

**Not measured: Onepoint, PwC and PwC Campus.** Their terms questions are open (Onepoint's terms forbid "extraction" of the Site's content without authorization; PwC's legal pages were unreadable): reading about 220 more pages from those sites before the owner decides would pre-empt it. Their cost is estimated below from the step 1 figures for the same Workday adapter.

## Result
| Source | Requests (all to its own host) | Fetched, new jobs | Run 1 MB sent | Run 2 (steady) MB sent | Stored jobs / in Paris or Ile-de-France |
|---|---|---|---|---|---|
| Boston Consulting Group (phenom) | 46 | 44, 40 | 18.00 (see below) | 0.012 | 42 / 41 |
| EY (successfactors) | 62 | 60, 60 | 1.93 | 0.022 | 60 / 60 |
| **Total** | **108** | | **19.93** | **0.034** | |

All runs `ok`. The whole measured step: 20,015,443 bytes sent in 140.5 s. The catalogue grew by 100 jobs (31,968 to 32,068).

## What it means for Neon
- **Steady state: about 0.03 MB per pass for the two** (against about 60 MB for a whole pass of the sources: well under 0.1 %).
- **First pass: about 2.1 MB more, once.** BCG's 18 MB includes the one-off cold read of the job-text sample that the first source of a fresh process always pays (about 17.8 MB, as in step 1: Saegus's first run showed 18.01 MB for 16 jobs); the two sources' own cost is about 0.2 MB (BCG, 40 new jobs) and 1.9 MB (EY, 60 new jobs with long French descriptions, 11,200 characters on average).
- ~~**EY needs three runs** to store all its 161 Paris-address jobs, because each run opens at most 60 new pages (`max_jobs`).~~ **Corrected 2026-11-04:** in the SuccessFactors adapter `max_jobs` caps the whole list considered (known jobs included), so EY with 60 only ever saw its 60 most recent Paris jobs; it is set to 200 now (hosted and seed) and one run covers all 161. The 108 requests are one run of each.
- **Estimate, not measured, for Onepoint, PwC and PwC Campus** (Workday, about 100 + 100 + 41 jobs): step 1's Workday sources cost about 0.01 MB per new job on the first pass and about 0.005 MB per job listed in the steady state, so about **+2 to 3 MB once and about +0.1 MB per pass** for the three.
- **Not measured here:** the effect of the extra jobs on the backup, scoring, digests and the inbox; the hosted Neon behaviour.

## For the owner's decision (slice 21)
- **BCG and EY are small in transfer and large in value**: 41 BCG jobs in Paris / Ile-de-France (the job of feedback #3 among them) and 60 EY jobs in Paris. I recommend enabling both.
- Figure to accept: **about +0.03 MB a pass for the two, +2.1 MB once, 108 requests for the first pass (EY's next two runs: about 62 each)**; with the three Workday sources, about +0.13 MB a pass and +5 MB once (estimate).
- Onepoint and PwC: decide on the terms first (see `consulting_batch_c2_2026-11-03.md`); measure them on the scratch copy if you say go.

## Not verified
The hosted behaviour; the Onepoint and PwC figures; a second day's run of BCG (new and closed jobs).
