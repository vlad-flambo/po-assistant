# Where a source pass's reads go (profile by SQL statement), and what a due digest costs

Measured 2026-10-29 on a fresh scratch restore of the 29 Oct dump, through `scripts/measure_reads.ps1` (nothing touched Neon, no e-mail sent). Raw lines: [measurements.jsonl](measurements.jsonl). The owner's go-ahead for a few real-site fetches into the scratch copy: "i want the build to go on" (2026-10-29), inside slice 4's earlier approval.

## 1. Profile: 10 real sources (the first approved source of each type), `scripts/step_profile_sources.py`
It does what `runner.run_all` does, with a counter on the rows each statement gets back (an **estimate** from the values; the container's counter is the real total: 19,156,033 bytes against an estimate of 18,149,519, so the estimate is **5 % low**, framing included in the real figure only).
Sources: greenhouse, remotive, ashby, workable, lever, teamtailor, careerpage, workday, oraclehcm, recruitee: 838 postings fetched, 20 new.

| Statement (shape) | Statements | Rows | Bytes (estimate) | Share |
|---|---:|---:|---:|---:|
| **The corpus word counts: the latest 3,000 job titles and the first characters of their texts** (`corpus.py:78`, `LEFT(description_text, n)`) | 6 | 3,000 | **17,095,721** | **94 %** |
| The link lookup (`ingest._links_of`: links, their jobs, `raw`) | 10 | 818 | 708,856 | 3.9 % |
| `jobs_candidatejob` rows for new jobs | 20 | 73 | 131,836 | 0.7 % |
| `jobs_config` full rows (profile text, keywords): once per source in `matching.sync`, again in `age_out` | 12 | 12 | 79,224 | 0.4 % |
| `jobs_candidate` rows (per source) | 26 | 42 | 51,960 | 0.3 % |
| The source's known external ids (`adapter.known_ids`) | 10 | 1,146 | 21,737 | 0.1 % |
| Everything else (jobs of the same key, filters, scores, inserts) | | | about 40,000 | 0.2 % |

- **The corpus is read by the first source whose new jobs get scored, then kept** (here source 3; source 1's nine new jobs were not scored) (in memory for 6 hours, in `SAXOBEAT_CACHE_DIR` between runs). In this scratch the cache was empty, so it paid the **full count: 17.1 MB**. Its design (`corpus.py`): a full count at most once a week, otherwise only the texts that joined or left the 3,000-job sample. **In steady state a run pays about `2 x new postings x 5.7 KB`** (slice 4's warm pass, with 930 new, is about 10.6 MB of its 64.5 MB) **and a week pays one full 17.1 MB**.
- **Without the corpus, a source costs about 103 KB** of reads (1.03 MB for 10 sources), of which the link lookup is **69 %**. Times 325 sources that is about 33 MB, which is the "38 MB unexplained" of slice 5's draft: it was the sum of many small, repeated reads, mostly the link lookup, not one thing.
- **Per source, outside the link lookup, the same candidates and configs are read again for every source** (`wanted_places`, `matching.sync`): about 31 KB a source, **about 10 MB a pass** for 325 sources. They could be read once per run (idea R2b, not built).
- **What is still not attributed:** about 10 MB of the 59 to 65 MB measured for a full pass (the sample is 10 mostly small sources). A third full pass with this profiler would close it; it does not change a decision, so it is not done.

## 2. The slim link lookup (R2a), built and measured
`ingest._links_of` now reads only the columns a run uses (`LINK_COLUMNS`: link id, source, external id, url; job id, content hash, expired, last seen) instead of whole rows.
- **Same 10 sources:** the link lookup goes from **708,856 to 143,222 bytes (-80 %)**; the sample's container total goes from 19,156,033 to 18,423,111 (-0.73 MB; the corpus is most of the sample). For a whole pass, slice 5's full-table measure (35.2 MB to 8.5 MB over all links, 62 % touched) says **about -16.5 MB a pass**.
- **Results identical?** `scripts/step_ingest_replay.py` replays one saved posting list (60 sources, 5,339 postings, every 7th with an edited text, every 11th job marked gone first; made from the scratch copy, so it is the same on every restore) through `ingest.ingest`, once with the old code and once with the new, on two restores, and compares the tables:
  - `jobs_jobsource`: **identical** (same hash).
  - `jobs_job`: **identical on 31,964 of 31,968 jobs**; the same counts (791 changed, 1,861 reopened). **Four jobs differ**, in `apply_method`, `apply_url`, `employment_type`, `posted_at`.
  - **Why (a finding, not a regression):** each of the four has two links from the same source in one batch, one a changed posting and one reopened. Each link holds its own copy of the job, read before the batch started. The second copy's save writes back its **stale** columns over the first one's change. The old code wrote **every** loaded column back (undoing the change entirely); the new code writes only the four columns it loaded. Both lose part of the change; the new loses less, and the job corrects itself at the next run (its stored hash then differs). Rare (4 in 5,339, in a replay made dense on purpose) and not made worse; the proper fix (one job handled once per batch) belongs to a runner-correctness cycle, as in cycle 014.
- **A test** (`test_the_link_lookup_reads_only_what_a_run_uses_and_saving_a_changed_job_keeps_the_rest`) fails on the old code and passes on the new; the whole suite passes (1,247 tests on SQLite; one test of the other session's feedback-console work was set aside because it is not finished there).

## 3. A due digest, `scripts/step_due_digest.py`
At the snapshot no digest was due (1.1 MB for `mail send`). I made one due on the scratch copy (cleared `last_digest_at`; the candidate without an address got one; the power-mode candidate's digest, off by default, switched on): **1,224,222 bytes (1.2 MB)**, with an AI-ready e-mail and a digest queued, nothing sent (`SAXOBEAT_MAIL=off`). **A due digest costs almost nothing**: 0.1 MB. The earlier guess of **129 MB a month for digests was wrong and is dropped**; `mail send` is about 1.1 to 1.2 MB a run with 2 candidates (it grows with the number of candidates).

## 4. `ai sync` profiled, and what the web inbox reads (both change the model)
**`ai sync`, by statement** (`scripts/step_profile_sources.py command ai sync`, fresh restore, empty cache): 30.7 MB estimated, 32.1 MB counted.
| Statement | Rows | Bytes (estimate) | What it is |
|---|---:|---:|---|
| The corpus word counts (latest 3,000 titles and texts) | 3,000 | 17,201,940 | cold cache: kept in `data\cache` afterwards |
| `jobs_candidatejob` + job (with its text) + score, one candidate | 1,634 | 12,183,398 | `calibration.visible_views`, for the **onboarding file** it was building |
| The same for the candidate's applied jobs | 111 | 1,056,189 | `backtest.applied_views`, same file |
| Everything else (configs, candidates, tasks, settings) | | about 0.2 MB | |
- **A second `ai sync` on the same copy, nothing pending, cost 86,007 bytes (0.09 MB).** So the 32 MB I had recorded as "the cost of `ai sync`" was the **first** run: a cold word-count cache plus one onboarding file. In the runner's steady state (the cache lives in `data\cache`, see `pc_runner.ps1`) `ai sync` is about **0.1 MB**, plus about 13 MB each time an onboarding or analysis file is built (rare: when a person joins or asks).
- **Consequence: the "R2b, `ai sync` stops loading texts" of the draft is mostly moot.** I made the one-line change anyway (`selection.waiting` defers the job text: the pool is ranked by the database and used by id) because the **web app** runs the same function (below). It did not change `ai sync` (32.1 MB before and after, as expected, since `ai sync` does not run the pool query).
- An optional later saving: `calibration.visible_views` loads texts that `current()` does not use (about 12 MB per onboarding file). Not built.

**The web inbox, one page view** (`scripts/step_inbox_page.py`: a signed-in test client on the scratch copy, the app's own statements):
| Page | Old `selection` | New `selection` |
|---|---:|---:|
| Standard-mode inbox (candidate #3, no AI consent yet, a small pool) | **1,108,415 bytes (1.1 MB)** | **152,897 (0.15 MB), -86 %** |
| Power-mode inbox (candidate #1) | 148,237 | 148,173 |
- The standard inbox ran `picks.of` on every view, which loaded the whole waiting pool **with job texts** just to take the top share by id. The page's HTML is the same size before and after (6,505 bytes). The cost grows with the pool: a standard user with a larger pool paid more per page view.
- This is a measured piece of **`W`**, the web app's own rate: 1.1 MB a page view saved for a standard-mode user. The rest of `W` is still to be read from Neon.
