# Neon reads of the ten new sources, measured on the scratch copy (2026-10-30, slice 11)

How: `scripts/measure_reads.ps1` restored the 29 Oct dump into a scratch Postgres on this PC (`measure_20261030180412`, 328 sources, 31,968 jobs; never a hosted address), then `scripts/step_new_sources.py` seeded the ten sources, enabled them **in the scratch copy only**, and ran each through the real runner (`runner.run_source`, hosted addresses, mail and AI disabled, owner's cities from the dump: Paris and Ile-de-France, remote Paris and London). Figures are the bytes the Postgres container **sent** (what Neon counts as transfer), in decimal MB. The real fetch from each site is **run 1**; **run 2** replays the same postings with no network, so every job is already known (the steady state). Raw lines: `new_sources_run.jsonl` and `measurements.jsonl` in this folder.

## Result
| Source | Requests (all to its own host) | Fetched, new jobs | Run 1 MB sent | Run 2 (steady) MB sent | Stored jobs in Paris / Ile-de-France |
|---|---|---|---|---|---|
| Saegus (teamtailor) | 1 | 16, 16 | 18.01 (see below) | 0.008 | 16 of 16 |
| Capgemini (capgemini) | 13 | 415, 405 | 6.32 | 0.266 | 409 of 409 |
| Accenture (sitemapjobs) | 62 | 60, 57 | 0.51 | 0.076 | 38 of 59 |
| Backbase (greenhouse) | 1 | 63, 56 | 0.21 | 0.058 | **0 of 56** |
| Checkout.com (ashby) | 1 | 168, 159 | 0.73 | 0.109 | 7 of 161 |
| Fenergo (workable) | 1 | 30, 26 | 0.11 | 0.049 | **0 of 26** |
| Payhawk (greenhouse) | 1 | 49, 49 | 0.21 | 0.015 | 5 of 49 |
| Finastra (workday) | 8 | 7, 5 | 0.06 | 0.040 | 5 of 5 |
| Murex (workday) | 21 | 20, 20 | 0.23 | 0.009 | 16 of 20 |
| SWIFT (workday) | 2 | 1, 1 | 0.04 | 0.004 | **0 of 1** |
| **Total** | **111** | | **26.43** | **0.633** | **about 496 of 794** |

The whole measured step: 27,086,732 bytes sent (the script prints 25.8 "MB", which is MiB), 176.5 s, exit code 0. All ten runs `ok`, none with an error. The catalogue grew by **794 jobs and 825 links** (31,968 to 32,762 jobs).

## What it means for Neon
- **Steady state: about 0.63 MB per pass for all ten sources together** (0.06 MB each). Cycle 001 measured about 60 MB for a whole pass of the 328 sources, so the ten add about **1 %**. At 13 to 22 runs a month: about **8 to 14 MB a month**.
- **First pass only: about 8.6 MB more** than steady state, once (the new jobs' own reads and writes: Capgemini 6.3 MB for 405 new jobs is most of it).
- **Saegus's 18 MB is not Saegus.** It was the first source in a fresh process, so it paid the cold read of the job-text sample that the runner keeps in its cache folder afterwards (cycle 001 measured about 17.1 MB for it). The cache folder here was new, so every real run pays it once anyway; it is not a cost of these sources. *(Inference from the figure and cycle 001's, not measured separately.)*
- **Not measured here:** what the 794 extra jobs cost in the steps that scale with the catalogue: the monthly backup (the dump is read in full: about +2.5 % of its size), rescoring and scoring of new jobs for each candidate, the weekly digests, the inbox page. Stored size: jobs average 4.5 KB in `jobs_job`, so about +3.6 MB of storage for the 794.
- **Requests to the sites: 111** (expected about 200, at most about 330): well under the plan's 400. Capgemini's 13 requests are about 1 MB each (6.3 MB downloaded by this PC, not by Neon).

## What the stored jobs look like
Descriptions are present for all but 1 job (an Accenture page whose own text is `**`); 2 Accenture jobs have no place. Average description 2,400 to 8,700 characters.

## For the owner's decision at slice 12
- **Backbase, Fenergo and SWIFT bring 0 jobs in Paris or Ile-de-France** (83 jobs stored for nothing). I recommend leaving them **off**.
- **Checkout.com** (7 of 161) and **Payhawk** (5 of 49) store every job they list worldwide, because boards are not filtered by city at ingest; small cost (about 0.9 MB), small gain.
- **Capgemini (409) and Accenture (38 of 59 so far; 173 pages in total, up to 60 new per run)** are the real additions, with Saegus (16), Murex (16) and Finastra (5).
- The figure for the owner to accept before enabling anything on the hosted database: **about +0.63 MB per pass, +8.6 MB once for the first pass, 111 requests to the sites for the first pass.**

## Not verified
Hosted behaviour (Render and Neon): everything here ran on a local Postgres 17; the hosted Neon version and its connection pooling were not exercised. The effect of the extra jobs on scoring, backup and digests. Accenture's remaining 113 pages (two more runs). A second day's run of Capgemini (daily interval): whether jobs that disappear are expired correctly (the runner's rules apply; not exercised).
