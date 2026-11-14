# Bytes read per runner step (slices 1 to 4)

Method: the local Postgres container's sent-bytes counter, read before and after one step on a **fresh restore** of `saxobeat_2026-10-29_100546.dump` (38 tables, 173,937 rows). Calibration: a step reading every job text got 177,292,015 bytes of payload and the counter said 179,160,197 (+1.05 %). Raw lines: [measurements.jsonl](measurements.jsonl). MB below is 10^6 bytes.

**Correction, 2026-10-29 evening (see [source_pass_profile.md](source_pass_profile.md) section 4):** the `ai sync` line below (32.2 MB) is a **cold-cache, first-file** cost, not a per-run cost. About 17.2 MB of it is the corpus word counts (kept in `data\cache` by the runner afterwards) and about 13.3 MB is the **onboarding file** it built (the candidate's visible jobs, with their texts). A second `ai sync` on the same copy, with nothing pending, read **0.09 MB**. The same cold-cache 17 MB sits inside the rescore lines and in the cold source pass.

| Step | Bytes sent | MB | Notes |
|------|-----------:|---:|-------|
| `backup_database` (run 1, run 2) | 227,043,380 / 227,027,473 | **227.0** | Dump file 65.5 MB: the wire carries 3.5 times the file |
| `run_sources --all` (1), cold cache | 58,835,604 | **58.8** | 325 sources, 22,102 postings fetched, 930 new against a snapshot a few hours old; 36.0 min |
| `run_sources --all` (2), warm | 64,454,250 | **64.5** | 325 sources, 21,927 postings fetched, 48 new; 23.3 min |
| `ai sync` (run 1, run 2) | 32,242,758 / 32,245,332 | **32.2** | "1 file to do, 0 results imported" |
| `mail send` (run 1, run 2) | 1,101,581 / 1,101,581 | **1.1** | 0 digests decided at this snapshot: low end |
| rescore, candidate #0 (1,634 views) | 36,028,972 / 36,013,240 | 36.0 | after a profile change; includes about 17 MB of corpus word counts on a cold cache |
| rescore, candidate #1 (8,781 views) | 101,387,311 | 101.4 | |
| `purge_old_jobs --days 90` | 2,459 / 2,459 | ~0 | nothing older than 90 days yet; grows from about January 2027 |
| app start on a restored copy (drill) | 14,104 | ~0 | |

## The link lookup of the source pass (`ingest._links_of`), over all 35,741 links
| Shape of the query | Bytes sent | MB |
|---|---:|---:|
| current (every job column except the text) | 35,235,240 | **35.2** |
| `raw` deferred | 26,163,933 | **26.2** |
| only the columns the unchanged-posting path uses | 8,500,560 | **8.5** |

Table sizes (scratch copy): `jobs_job` 144.1 MB, `jobs_jobsource` 19.4 MB, `jobs_candidatejob` 14.1 MB, `jobs_score` 9.7 MB, `jobs_statuschange` 2.7 MB, `jobs_run` 1.4 MB; 194.0 MB in all. `jobs_job.description_text` payload 177.3 MB over 31,968 jobs; `jobs_jobsource.raw` payload **8.9 MB** over 35,741 links; 10,589 jobs are engaged by a candidate (a status other than new).

## What the numbers say
- **A full source pass costs about 60 MB whether it finds 930 new postings or 48**: the cost is not the new postings, it is looking at the roughly 22,000 that are already known (the links, one query per source, `ingest.py:109`). The warm pass was not cheaper than the cold one.
- **The three reads that matter, in the order a month of use makes them matter:** the **backup (227 MB each)**, the **source pass (about 60 MB per run: the link lookup 69 % of a source's own reads, plus the word-count sample, 17 MB on a cold cache and a smaller increment after)** and, a long way behind, **building an AI file** (an onboarding file read 13 MB of job texts; a plain `ai sync` is 0.1 MB in steady state, see the correction above). The rescore (36 to 101 MB) is large but only happens after a profile change.
- **Job texts are the bulk of the database** (177 MB of the 227 MB), and `ai sync` and the rescore read them. The source pass does not load them. **An earlier guess, that the links' `raw` payload dominates the source pass, was wrong**: `raw` is 8.9 MB in total. The link lookup is about 22 MB of a pass today (62 % of 35 MB) and could be about 5 MB; roughly 38 MB of each pass is still unexplained.
- **One real fault surfaced:** the source "Esker (teamtailor)" errored in both passes (`fetched=0`). Not part of this cycle; a candidate for cycle 014.
- The 29 Oct snapshot is a few hours older than the data a real run meets; pass 1 shows how many new postings that adds (930), which cost little (compare the two passes).
