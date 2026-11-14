# Plan: cut the runner's reads from Neon

| | |
|---|---|
| **Cycle** | 001 |
| **Stage** | Plan approved 2026-10-29; Build: slices 1 to 4, 6 and 7 done (8 not needed); slice 5's projection is complete except `W`; D5 proposed |
| **Spec** | [spec.md](spec.md), approved 2026-10-29 |
| **Decisions** | [decisions.md](decisions.md) |

## Who does what
- **Claude:** every script, measurement and code change. All of it runs against a scratch database in your local Docker. Nothing touches Neon.
- **Owner:** approves the slices, agrees once to the real-site fetches of slice 4, reads Neon's figures (daily, later), and decides after the numbers.

## Slices
Each slice stops at its check. Slices 1 to 5 change no application code. Slices 6 to 8 are conditional: the decision of slice 5 says which run.

| # | Slice | Who | Touches | Check | Criteria | Status |
|---|-------|-----|---------|-------|----------|--------|
| 1 | **The guarded measurement script** | Claude | `scripts/measure_reads.ps1` (new) | Restores the dump into a fresh scratch database, reads the container's sent-bytes counter, runs one step, reads it again, drops the database. Refuses (exit non-zero) when `DATABASE_URL` is not localhost, and a test with a fake remote address proves it. A no-op step prints 0 bytes. It reports other open connections to the scratch server | 1, 10 | **done 2026-10-29** (see "As run") |
| 2 | **Backup, purge and the restore drill** (the steps that need no network) | Claude | `evidence/` | Bytes of `backup_database` and `purge_old_jobs --days 90`, each twice; then the drill: the latest dump restored into an empty Postgres 17, row counts match, and the app answers `/healthz` and serves the login page on a local server pointed at it | 2 (part), 8 (drill) | **done 2026-10-29** |
| 3 | **ai sync, mail send, a rescore** | Claude | `evidence/` | Bytes of each, each twice, with `SAXOBEAT_MAIL=off` and the AI and cache folders in a scratch directory; the e-mail count in `jobs_outgoingemail` shows nothing was sent | 2 (part), 10 | **done 2026-10-29** |
| 4 | **run_sources, twice** (the first with a cold cache, the second warm) | Claude, owner agrees first | `evidence/` | Bytes of both runs; the run reads the real job sites once, from this PC, as the runner always does. Reports how many postings were new against the 29 Oct snapshot | 2 (part) | **done 2026-10-29** (owner said yes) |
| 5 | **The table, the projection and the decision** | Claude, then owner | `evidence/bytes_per_step.md`, `evidence/projection.md`, `decisions.md` D3 | Three biggest reads named with bytes (criterion 3); a projection at the owner's usage pattern with prod1's web rate (criterion 4); D3 says which of R1 to R3 are needed for under 2.5 GB with a 20 % margin, or "none" | 3, 4, 5 | table done ([bytes_per_step.md](evidence/bytes_per_step.md)); projection drafted ([projection.md](evidence/projection.md)); **waits for the web rate `W` (cycle 002's reading) and the owner's usage pattern, then D3** |
| 6 | **R1, the backup profile** (if D3 selects it) | Claude | `backup_database.py`, `pc_runner.ps1`, tests | Before and after bytes on the same scratch copy; a dump with the profile restores into an empty database and the app starts on it (the drill again); tests pass | 6, 8 | **done 2026-10-29** as a cadence change (D3), see "As run" |
| 7 | **R2, defer what is unused** (if D3 selects it) | Claude | `ingest.py`, `ai/selection.py`, tests | Before and after bytes per step; results identical on the same scratch copy (below); tests pass | 6, 7 | **done 2026-10-29** as 7a (the slim link lookup) and 7b (the ranking pool without job texts); both awaiting the owner's review and commit (D5). `ai sync` turned out to cost 0.1 MB in steady state, so nothing more is built here |
| 8 | **R3, a read-through text cache** (if D3 selects it) | Claude | a new module and its call sites, tests | As slice 7, plus a changed text is a cache miss (a test) | 6, 7 | **not needed** (D5): the savings came from not loading texts, not from caching them |
| 9 | **Observe: seven days on prod1** | Owner reads Neon, Claude records | `verify.md` | Each day: the sum and the old project's percentage; after seven days the projected month agrees with the observed week within ±30 % and is under 2.5 GB | 9 | todo, after the changes are live |
| 10 | **Restart the runner on prod1** (owner, by hand) | Owner runs, Claude records | `evidence/restart_runbook.md`, `verify.md` | One run with Neon readings before, right after and an hour later; the delta is inside 0.20 GB and matches about 60 to 90 MB; then 3 to 5 runs a week | 9 | **ready 2026-10-30** (D6 proposed); the owner's start confirms it |

Criteria 10 and 11 hold in every slice (nothing touches Neon or sends e-mail; no secret exposed).

## Order and why
Slice 1 first: every later number depends on a script that cannot hurt anything. Slices 2 and 3 need no network and no real sites, so they come before slice 4, which is the only one that fetches from outside. Slice 5 turns numbers into a decision before any code changes: if the projection is already under the target, slices 6 to 8 are not built and the cycle goes straight to slice 9 with the drill done. Slice 9 is last because it needs the changes live and a week of use.

## How a measurement is taken (slice 1, written down so slices 2 to 4 repeat it)
1. Create a scratch database, restore `saxobeat_2026-10-29_100546.dump` into it (the two `DEFAULT ACL` entries left out, as in cycle 002), verify with `scripts/db_counts.py`.
2. Check that nothing else is connected to the scratch server (`pg_stat_activity`), read the container's `eth0` sent-bytes counter from `/proc/net/dev` (idle noise was 0 bytes over 3 s on 2026-10-29), run the step, read it again.
3. The process environment for the step: `DATABASE_URL` is the scratch address; `SAXOBEAT_HOSTED_DATABASE_URL` and `SAXOBEAT_FALLBACK_DATABASE_URL` are set to the word `measurement-disabled` (an empty value is not possible: on Windows, setting an environment variable to "" deletes it, and `.env` would fill it back); `SAXOBEAT_MAIL=off` and `BREVO_API_KEY` the same word; `SAXOBEAT_AI_DIR` and `SAXOBEAT_CACHE_DIR` are scratch folders. These are set explicitly in the process because `config/settings.py` loads `.env` with `setdefault`: an unset variable would be filled from `.env`, a variable set to an empty string is not.
4. Every number is recorded with its step, its run number, the snapshot's date and the counter's start and end values. The counter includes headers and the protocol's overhead: close to what Neon counts on the wire, not identical.
5. Drop the scratch database and the scratch folders.

## Results identical before and after (slices 7 and 8)
For steps that read only the database (`rescore`, `ai sync`, `mail send`, selection), the check is: restore twice, run the old code on one and the new code on the other, compare row counts per table and a hash of `Score` values and `CandidateJob` states. For `run_sources` the input includes the live sites and is not reproducible, so the check there is the test suite plus running the changed ingest function on the **same saved posting list** against both restores. If a reduction cannot be checked this way, the plan says so for that slice before it is built.

## Rollback
| Slice | If it goes wrong |
|-------|------------------|
| 1 to 5 | Nothing changed outside scratch: drop the scratch database and folders |
| 6 to 8 | A code change on its own commit: revert the commit; the runner scripts are untouched until the owner reruns them |
| 9 | Not an action: it reads Neon's figures |

## Risks
- **A measurement reaches Neon or sends e-mail:** slice 1's guards and test; the runner scripts are never used.
- **The 29 Oct snapshot is older than real data:** slice 4 reports how many postings were new; the second run is the steady state.
- **R2 hides a use of the text:** slice 7's check and the tests.
- **The web app is the main reader:** slice 5 says so with numbers and returns to the owner; the spec's scope is then revisited.
- **Cycle 002's reading is late:** slices 1 to 4 do not need it; slice 5 does.

## As run (log, newest last)
**2026-10-29, slice 1: `scripts/measure_reads.ps1`.**
- **Refusals (3 of 3 pass):** a Neon-looking address, `db.example.com` and `localhost.evil.com` are each refused with a non-zero exit before anything is touched: the number of databases on the local server was the same before and after (6 and 6), and no evidence file was written.
- **No-op:** restores the dump (38 tables) into a fresh scratch database, measures **0 bytes** (0.2 s), and removes the scratch database and folders (0 left over). The `-Run` step's environment is restored afterwards: this session's own variables are untouched.
- **Environment a step sees** (checked with a probe that prints flags only): mail provider off; database host localhost and name `measure_...`; hosted, fallback and mail-key variables disabled; AI and cache folders inside `data\measure`. Eight of eight true. Lesson: on Windows an environment variable cannot be empty (setting it to `""` deletes it), so the values that must not leak are set to `measurement-disabled`, not to an empty string as first planned.
- **Calibration:** a step reading every `jobs_job.description_text` (31,968 rows, **177,292,015 bytes** of text payload) was measured at **179,160,197 bytes sent**: **+1.05 %**, so the counter is a faithful stand-in for what Neon would count outbound (framing and row headers included).
- **A finding for the spec:** the job texts alone are about **177 MB**, which is most of the ~200 MB a full dump reads. Any step that loads every job text costs about 170 MB; this is why R1, R2 and R3 all go after the text.
- **Evidence:** `evidence/measurements.jsonl` holds these three measurements (`noop`, `envprobe`, `calibrate`); the script appends one line per measurement (counts and bytes only, no address).
- Not yet exercised: a long step with other clients connected (it reports `other_connections`, 0 here).

**2026-10-29, slices 2 and 3** (all on a fresh restore of `saxobeat_2026-10-29_100546.dump`, each step twice; every number is in `evidence/measurements.jsonl`).

| Step | Bytes sent, run 1 / run 2 | Note |
|------|---------------------------|------|
| `backup_database` (`pg_dump`) | 227,043,380 / 227,027,473 (216.5 MiB) | The dump file is 65.5 MB; the **wire carries 3.5 times that**, because `pg_dump` compresses on the PC after receiving. About 13 % more than the 200 MB estimate in `DEPLOY.md` |
| `purge_old_jobs --days 90` | 2,459 / 2,459 | Nothing qualifies in a database whose oldest jobs are days old; it will cost more once jobs older than 90 days exist (from about January 2027) |
| `ai sync` | 32,242,758 / 32,245,332 (30.7 MB) | With "1 file to do, 0 results imported". The cost is the selection pool loading **full job texts** to rank them |
| `mail send` | 1,101,581 / 1,101,581 (1.1 MB) | "0 digests decided, 0 sent" at this snapshot: digests that are due would load the same pool as `ai sync`, so this is the low end |
| rescore, candidate #0 (1,634 views) | 36,028,972 / 36,013,240 (34.4 MB) | Includes about 17 MB for the corpus word counts, which a cold cache recounts |
| rescore, candidate #1 (8,781 views) | 101,387,311 (96.7 MB), one run | About 10 to 12 KB per view scored |
| drill: the app on a restored copy | 14,104 | |

- **Slice 2, the drill (criterion 8, part):** the 29 Oct dump restored into a scratch database; `scripts/drill_check.py` starts the app in-process on it: **`/healthz` 200 `ok`, the login page 200, 3 user accounts, 0 migrations pending**: all four pass. The sign-in itself is not tried (no password needed or known). The drill is to be repeated on a dump made with a new backup profile (slice 6).
- **Slice 3 safety (criterion 10):** `SAXOBEAT_MAIL=off` held ("0 sent"); the AI files went to a scratch folder, and the real `~/Saxobeat AI` folder had **0 files changed**; no scratch database or folder was left.
- **Mistakes on the way:** (1) my first four runs failed because a child PowerShell passes `-Run a,b,c` as one string; the script now splits it, and no longer records a failed step; the four bad lines were removed from the evidence file. (2) An interrupted run left one scratch database behind (the script cannot clean up when it is killed): `-Clean` now removes every leftover.
- **Two new scripts for the plan's record:** `scripts/drill_check.py` and `scripts/step_rescore.py` (a measurement step: it writes scores, so it is only run through the guarded script).
**2026-10-29 14:06 to 15:06, slice 4: two full `run_sources --all` passes on one scratch copy** (the owner said yes; the real job sites were fetched from this PC, the writes went only into the scratch database).
- **Pass 1, cold cache:** **58,835,604 bytes sent (58.8 MB)**, 36.0 min, 325 sources run, 324 ok, 22,102 postings fetched, **930 new** against the few-hours-old snapshot.
- **Pass 2, warm cache:** **64,454,250 bytes (64.5 MB)**, 23.3 min, 325 sources, 21,927 fetched, **48 new**.
- **The warm pass was not cheaper.** So a source pass costs about **60 MB regardless of how many postings are new**: it is the looking-up of roughly 22,000 known postings (links, with their `raw` payload, `ingest.py:109`) that costs, not the new ones. A hypothesis, tested by slice 7's before/after.
- One source failed in both passes: **Esker (teamtailor)**, `fetched=0` (a real fault, not caused by the measurement; noted for cycle 014).
- Clean: no scratch database or folder left; `SAXOBEAT_MAIL=off` held; nothing was written to Neon.
- **Slice 5, drafted:** the full table is in [evidence/bytes_per_step.md](evidence/bytes_per_step.md), a draft projection with scenarios in [evidence/projection.md](evidence/projection.md). At 3 runs a week with weekly backups the runner alone would be about **2.27 GB a month**, over the 2.0 GB working target before the web app counts; a monthly backup alone brings that to about 1.59 GB plus `W`. The decision D3 needs `W` and the owner's pattern.

**2026-10-29, slice 5 (continued): the owner's pattern and a correction.**
- **Owner's pattern:** **3 to 5 runner runs a week** (13 to 22 a month). The projection now uses it: [evidence/projection.md](evidence/projection.md).
- **A hypothesis refuted by measurement.** The plan, the spec and the earlier log guessed that the links' `raw` payload dominates the source pass. Measured: `jobs_jobsource.raw` is **8.9 MB in total**; the link lookup over all links reads 35.2 MB today, **26.2 MB** with `raw` deferred and **8.5 MB** with only the columns the unchanged-posting path uses (`scripts/step_links_query.py`; three runs on fresh restores, all in `measurements.jsonl`). A pass touches about 62 % of the links, so the slim lookup saves about **16.5 MB per pass of about 60**; about **38 MB of each pass remains unexplained** (needs a profile by statement). R2's first part is therefore "the slim link lookup", which supersedes "defer `raw`" in the spec's wording.
- **Table sizes:** `jobs_job` 144 MB, `jobs_jobsource` 19 MB, `jobs_candidatejob` 14 MB, `jobs_score` 10 MB; 194 MB in all; 10,589 jobs are engaged by a candidate (`scripts/step_table_sizes.py`).
- **R1 reconsidered:** a smaller dump that leaves out `jobs_job` would break the foreign keys of the candidates' own triage and the job texts are most of the database, so R1's useful form is the **cadence** of the full backup (monthly, or every two weeks), to be proven in slice 6's drill.
- **Preview of the verdict** (not D3, which waits for `W`): at 3 runs a week, a monthly backup plus the slim lookup is about 1,375 MB before `W`; at 5 runs a week it is about 2,081 MB, over the 2,000 MB target before `W`, so `ai sync` and the rest of the source pass would have to shrink too. The weekly full backup does not fit at either rate.
- **Slice 6 (R1), done: the owner chose a monthly full backup** (D3 in decisions.md). `scripts/pc_runner.ps1` now calls `backup_database --min-age-hours 720 --keep 6` (was 168 and 8); the script still parses; `docs/DEPLOY.md` (steps, section 5 and the Backups section) says monthly and gives the measured 227 MB. Nothing was run against Neon. **Before and after:** the backup line of the projection goes from 908 MB a month (4 x 227) to 227 MB, **-681 MB a month**. The dump itself is unchanged, so criterion 8's drill (slice 2) still holds and does not need repeating. Cost to the owner: up to a month of work at risk in a disaster, apart from Neon's own short history and `saxobeat-fallback1` (the 29 Oct snapshot). A manual backup resets the 30-day clock (the gate reads the newest local file).
- **Another cycle is affected:** cycle 004's spec (criterion 8) and its evidence file expect the runner's weekly backup (`--min-age-hours 168`). They need updating by whoever owns that cycle; not edited here.
- Two more measurement steps added to the record: `scripts/step_table_sizes.py` and `scripts/step_links_query.py` (read only).

- **Preview, not the projection** (slice 5 does that properly, with `run_sources` and the web rate still missing): at the owner's pattern of about 12 runs a month, `ai sync` alone is about 390 MB, and a weekly backup about 910 MB, together about 1.3 GB before `run_sources` and the web app. The three largest known reads are the **backup (227 MB each)**, the **rescore (when it happens)** and **`ai sync` (32 MB each)**, and all three are dominated by job texts.

**2026-10-29 evening, slice 5 (the profile and the digest) and slice 7a.** Full detail: [evidence/source_pass_profile.md](evidence/source_pass_profile.md).
- **Docker Desktop was not running** at the start (the scratch database lives in it); I started it and waited for the daemon.
- **Profile of 10 real sources** (`scripts/step_profile_sources.py`, owner's go-ahead "i want the build to go on", scratch copy only): the container sent **19.2 MB**, of which the corpus word counts are **17.1 MB (94 %)** (the latest 3,000 job texts, read in full once per cold cache and kept for a week by `corpus.py`). Without it a source costs about **103 KB**, **69 % of it the link lookup**; the "38 MB unexplained" of a pass is the sum of those many small reads (links 23 MB, candidates and configs read again for every source about 10 MB). About 10 MB of a full pass stays unattributed. The estimate of bytes per statement is 5 % under the container's real total.
- **A due digest** (`scripts/step_due_digest.py`, made due on the scratch copy): **1.2 MB**. The guess of 129 MB a month for digests was wrong and is dropped.
- **Slice 7a, built:** `ingest._links_of` reads only the columns a run uses (`LINK_COLUMNS`). The link lookup goes from **708,856 to 143,222 bytes (-80 %)** on the same 10 sources. A new test fails on the old code and passes on the new; **1,247 tests pass** (one test of another session's unfinished feedback-console work was set aside). **Replay of one saved posting list through the old and the new code** (`scripts/step_ingest_replay.py`, 60 sources, 5,339 postings, on two restores): `jobs_jobsource` identical; `jobs_job` identical on **31,964 of 31,968**; the four that differ are a stale write-back when two links of one source point to one job (one changed, one reopened, in the same batch): the old code undid the whole change, the new loses less. Reported as a finding, not fixed here.
- **Two corrections found the same night** (details in [source_pass_profile.md](evidence/source_pass_profile.md) section 4): **`ai sync` costs 0.1 MB in steady state** (the 32.2 MB was a cold cache plus one onboarding file; a second run on the same copy read 86 KB), and **a standard-mode inbox page of the web app read 1.1 MB** because it loaded the whole ranking pool with job texts. Slice 7b is therefore the one-line fix in `ai/selection.py` (the pool is ranked by the database and used by id): **1.11 MB to 0.15 MB a page view (-86 %)**, a test that fails on the old code, **1,249 tests pass**.
- **Projection and D5 (proposed):** a run is about 63 MB (not 94.9); the runner with the monthly backup is **1,045 to 1,611 MB a month** with no reduction and **830 to 1,248** with 7a, before `W`; R2c, R2d and R3 are not needed. D4 (drafted earlier the same night) is superseded by D5. See [projection.md](evidence/projection.md) and [decisions.md](decisions.md).
- **Mistakes on the way:** my first replay compared two fingerprints that held this run's clock (a "gone" marker made with `now()`); I fixed it with a fixed time and added a per-column fingerprint before calling the difference real. Writing the dump of changed columns to the short Windows temp path failed silently; a project-local path works.

## Gate
- [x] Owner approved the slices (2026-10-29)
