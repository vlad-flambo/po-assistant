# Spec: cut the runner's reads from Neon

| | |
|---|---|
| **Cycle** | 001 (folder keeps its first name, `local-db-replica`) |
| **Stage** | Spec approved 2026-10-29; next: Plan ([plan.md](plan.md)) |
| **Intent** | [intent.md](intent.md), approved 2026-10-29. **This spec changes its shortlist: see "What changed since the intent"** |
| **Decisions** | [decisions.md](decisions.md) |

## What changed since the intent
The intent's leading approaches were B and C: a local copy of the database that the runner works on, refreshed from Neon at the start of a run. A read-only map of the code (2026-10-29) found why that is much harder than it looked, and the spec follows the evidence:

- **Shared tables.** `Job`, `CandidateJob`, `Score`, `StatusChange`, `Candidate`, `Config`, `Source`, `AiTask` and others are written by **both** the runner and the web app. The runner already overwrites a user's triage in a window of milliseconds (`matching.expire` updates by primary key with no status guard, `matching.py:139-143`; `apply_tuning` saves a whole settings row). On a copy that is a run old, that window becomes the whole run.
- **Ids.** All keys are auto-increment (`BigAutoField`): two databases inserting would collide, and ids appear in agent files (`T-<id>`, `C-<id>`) and e-mail links (`/job/<id>/`).
- **No change signal.** There is no `auto_now` and no real `updated_at` anywhere; several tables have no timestamp at all. Deletions cascade widely (purge, account deletion, source deletion) and would have to be replayed on the copy.
- **Nothing to reuse.** There is no database router and no incremental copy code (`copy_sqlite_to_postgres` is a one-time full copy).
- **The heavy reads are few and specific** (below), and the cheap fixes for them need none of that machinery.

So this cycle **measures first, reduces the specific reads in code, and keeps the full working copy as a last resort** that would need its own cycle. Cycle 002 showed the pattern: measuring and rehearsing locally cost nothing on Neon.

## Behaviour when finished
- There is a **table of bytes read from the database per runner step** (`run_sources`, `purge_old_jobs`, `ai sync`, `mail send`, the backup, a rescore), measured on a scratch local copy, with the method written down.
- There is a **projection of Neon transfer per month** for a stated usage pattern, built from those bytes and from the web app's own rate measured on `saxobeat-prod1`.
- The reads that the projection says matter are **reduced in code, one at a time, each with before and after bytes**, until the projection is under 2.5 GB a month with a margin. Users see no difference.
- The weekly backup has a **profile chosen from the measurements** (how often, and whether everything or only what cannot be recomputed), and a restore from it was **rehearsed**.
- A week after the changes run on prod1, **Neon's own figure agrees with the projection**.

## Acceptance criteria
Each is checked in `verify.md` with its evidence.

**Measure (before any code changes)**
1. [ ] A scratch copy of the 29 Oct dump exists in the local Postgres, and a **measurement method** is recorded: the database container's sent-bytes counter read before and after each step (idle noise measured, was 0 bytes over 3 s on 2026-10-29), one step at a time, each against a fresh restore of the same dump.
2. [ ] A **table of bytes per step** is in `evidence/`, covering `run_sources` (one full run, with its first run's cache building and a second run with the cache warm), `purge_old_jobs --days 90`, `ai sync`, `mail send`, a backup (`pg_dump`), and a rescore of one candidate.
3. [ ] The **three biggest reads are named with their bytes**, replacing the code-evidence guesses (the weekly dump; `JobSource` rows with their `raw` payload per listed posting; full `description_text` loads in `score_views`, the AI selection pool, the mail digest and the corpus recount).
4. [ ] A **projection** exists: runner steps per month at a stated pattern (the owner's: manual, a few runs a week), plus the web app's daily rate taken from prod1 (the sum minus the old project's share, over at least one full day), plus backups. It states its assumptions.

**Decide**
5. [ ] A decision in `decisions.md` says which of the reductions R1 to R3 are needed to reach a projection **under 2.5 GB a month with at least 20 % margin**, and which are not. If the projection is already under, the answer is "none", and the cycle ends with measurement, a backup profile and the drill.

**Reduce (only what criterion 5 selects, one slice each)**
6. [ ] Each applied reduction has **before and after bytes** for its step on the same scratch copy, and the **test suite passes** (`DATABASE_URL=`, one known failing backup test).
7. [ ] **No behaviour change for users:** for the same dump and the same inputs, the runner's results are identical before and after: same row counts per table and the same scores (compared with `db_counts.py` and a hash of `Score` values, on the scratch copy).
8. [ ] The **backup profile** is applied, and a restore of a dump made with it into an empty Postgres 17 gives a working app (rehearsal as in cycle 002: counts as expected, `/healthz` and a login on a local server pointed at it). This is the **restore drill** of the intent.

**Observe (after the changes run on prod1)**
9. [ ] After **7 days** of normal use, Neon's transfer for prod1 (the sum minus the old project's share, read daily) agrees with the projection within **±30 %**, and the projected month is under 2.5 GB.

**Always**
10. [ ] **Nothing during measurement touches Neon, sends an e-mail, or writes outside scratch locations:** the measurement runs with `DATABASE_URL` set to the scratch database only and `SAXOBEAT_HOSTED_DATABASE_URL` removed from the process, `SAXOBEAT_MAIL` unset, and `SAXOBEAT_AI_DIR` and `SAXOBEAT_CACHE_DIR` pointed at scratch folders. The scratch copy holds real candidate data: it stays local and is dropped afterwards.
11. [ ] No connection string appears in the repo, a commit, the chat or a command line.

## The reductions, in order (each only if criterion 5 selects it)
| # | Reduction | What it touches | Risk | Evidence it is worth it (code map, to be measured) |
|---|-----------|-----------------|------|-----------------------------------------------------|
| R1 | **Backup profile:** a monthly full dump, and between them a dump that leaves out the data of tables that can be rebuilt (decided table by table in the plan, validated by the drill) | `backup_database.py` (an option such as `--exclude-table-data`), `pc_runner.ps1` flags | A table wrongly judged rebuildable: guarded by the drill and a written list | The dump reads about 200 MB each time, the one read that is certain and large |
| R2 | **Defer what is not used:** `JobSource.raw` in `ingest._links_of` (`ingest.py:109`), and `description_text` where a step only ranks (check `selection.waiting`, `selection.py:28`, and the mail digest picks) | `ingest.py`, `ai/selection.py`, `ai/export.py`, `mail.py` | A step that did use the text: caught by criterion 7 and the tests | The code loads them with no `defer`; whether the text is needed is checked per call site |
| R3 | **A read-through text cache:** a small local store (a file next to `data\cache`) of `Job.description_text` keyed by job id and `content_hash`, filled on first read and used by `score_views`, `rescore`, the AI export and the corpus recount; only new or changed jobs are fetched from Neon | a new module and its call sites | A stale text served: the key includes the hash, so a changed text is a miss | The text is about 5.7 KB per job on average (inferred), 3000 jobs is about 17 MB per recount; extends what `data\cache` already does for word counts |
| (R4) | A local working copy with a push-up | everything | **High** (see above): its own cycle, only if R1 to R3 cannot reach the target | Not proposed here |

## Interfaces and data
| What | Change |
|------|--------|
| `scripts/measure_reads.ps1` (new) | Restores the dump into a scratch database, runs one runner step, prints the bytes the container sent. Refuses to run unless `DATABASE_URL` points to localhost; removes `SAXOBEAT_HOSTED_DATABASE_URL`, `SAXOBEAT_MAIL` from its process; sets the scratch folders |
| `evidence/` in this cycle | the bytes table, the projection, before/after tables |
| `backup_database.py`, `pc_runner.ps1` | an option and its use, only if R1 is selected |
| `ingest.py`, `ai/selection.py`, `ai/export.py`, `mail.py` | `defer` / narrower queries, only if R2 is selected |
| a text-cache module | only if R3 is selected |
| `docs/DEPLOY.md` | the measured figures and the backup profile, in the Learn stage |
| Schema, app behaviour | none |

## Constraints
- **The runner stays manual and nothing runs against prod1** until this cycle says how (the baseline must stay clean for the weekly projection). All measurement is local.
- Never run `scripts/pc_runner.ps1` or `saxobeat-runner.cmd` for the measurement: both read `.env` and use the **hosted** address when it is set.
- The scratch copy holds real candidate names and CVs: keep it local, drop it after, and never let `mail send` send (criterion 10).
- Windows PowerShell; `uv run python`; Postgres 17 in Docker (`saxobeat-db-1`).

## Risks
| Risk | Mitigation |
|------|------------|
| A measurement script touches Neon or sends e-mail | Criterion 10; the script refuses unless the target is localhost and strips the hosted variables; mail is unset |
| The 29 Oct snapshot is older than the data the runner meets in practice, so a run on it reads more new postings than a typical run | State the age; measure two runs (the first, then the second, which is the steady state) and report both |
| `run_sources` fetches real job sites during measurement | It is what the runner does every time; limit to one full run plus one repeat; owner agrees to it in the plan |
| R2 or R3 changes what a run produces | Criterion 7 (identical results on the scratch copy) before anything goes near prod1 |
| The web app turns out to be the largest reader | Then the target needs web-side work: record it, and the spec's scope is revisited (not assumed away) |
| The existing races (the runner overwriting a user's triage) get worse with any caching | Reductions here only change what is read, never what is written; the races are recorded in `learn.md` as a candidate for a separate cycle |

## Out of scope
- A local working copy with synchronisation (R4), a router, or replication.
- Fixing the runner's overwrite windows (recorded as a finding).
- Scheduling the runner, changing the plan or host, reducing the web app's own reads (unless the measurement says they dominate, then a new decision).

## Gate
- [x] Owner approved this spec (2026-10-29), including the change from the intent's B/C (D1 in decisions.md)
