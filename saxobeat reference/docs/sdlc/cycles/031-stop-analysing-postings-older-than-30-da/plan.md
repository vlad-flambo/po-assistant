# Plan: stop analysing postings older than 30 days

| | |
|---|---|
| **Cycle** | 031 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

## Slices
Thin, ordered, each verifiable alone. Each slice names the acceptance criteria it moves. Everything is code and local; nothing is written to Neon or to any stored setting. Each slice starts with its tests failing for the right reason, then the code that turns them green.

| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | **One definition of a posting's date, and the rule that uses it.** A small function in `filters.py` (`listing_date(job)`): `posted_at`, else the job's own `first_seen_at` (a view proxies both to its job). `hidden_reason`'s last rule uses it. | `jobs/services/filters.py`, `tests/test_stale.py` (new tests), `tests/test_core.py:90-93` (the "nothing to judge" assertion now says the opposite) | New tests: dated 31 vs 29 days; both dates (dated 5 days / imported 90 days kept; dated 40 / imported yesterday hidden); undated imported 31 vs 29 days hidden vs kept; a `CandidateJob` made today for a job imported 31 days ago is hidden; limit empty or 0 hides nothing. | 2, 3, 7 | done |
| 2 | **The refilter reads the import date.** `FILTER_FIELDS` gains `job__first_seen_at` (still nothing else, no posting text). | `jobs/services/matching.py`, `tests/test_stale.py` | A candidate with an undated job imported 45 days ago: limit 60 shows it, limit 30 hides it (`refilter`), limit back to 60 brings it back; the refilter's query count is unchanged (the existing "refilter loads only these fields" test, if there is one, still passes). | 3, 4 | done |
| 3 | **The nightly age-out.** `age_out`'s query becomes "dated and older than the cutoff, or undated and imported before it", still in one `UPDATE` and reading no text. | `jobs/services/matching.py`, `tests/test_stale.py` | New tests: undated old view hidden; dated-recent but imported-long-ago view untouched; `keep_visible` untouched; status not new untouched; limit off hides nothing. Then a scoring test: dated 45-day-old, undated 45-day-old and recent jobs, `refilter` then `rescore`: only the recent one has a score, and the AI selection query returns none of the old two. | 5, 6, 7 | done |
| 4 | **The new default and the old tests.** `default_filters()["max_age_days"]` 60 to 30; `test_the_default_is_sixty_days` and any test that read 60 as "the default" updated; a test that a stored 60 or 45 reads back unchanged. | `jobs/models.py`, `tests/test_stale.py`, others only if the suite shows them | The new and old stale tests; then `tests/test_core.py`, `test_phase7.py`, `test_screens_mobile.py`, `test_phase8.py` (the files that mention `max_age_days`). | 1, 11 | done |
| 5 | **Help text and French.** The age box's `title` in `settings.html` says "the posting date, or the day it was imported when there is none"; French entry added with `manage.py i18n extract`, translated, compiled. | `jobs/templates/jobs/settings.html`, `locale/fr/LC_MESSAGES/django.po` and `.mo` | `manage.py i18n missing` prints nothing; `tests/test_i18n.py` passes; the power Settings page still has `#max_age_days`. | 10 | done |
| 6 | **Read-only counts on a local copy of the 29 Oct dump** (the size of the one-off effect). Check Docker Desktop is running (`docker info`), restore `data/backups/saxobeat_2026-10-29_100546.dump` into a scratch database of the local container as cycle 029 did, migrate to the current code, run a read-only script: per candidate, the stored `max_age_days`, then how many visible new views would be hidden (a) by the undated rule at 30 days, and (b) by 30 instead of the stored limit on dated postings; time the new `age_out` query. Drop the scratch database at the end. | `evidence/counts.md` (and the script, kept in `evidence/`) | Counts and the timing in `evidence/`; the script has a guard (refuses a database whose name is not the scratch one) and issues only `SELECT`s; no Neon connection string is read. If Docker is down it stops and asks, rather than hanging. | 8, 9 | done |
| 7 | **Full suite and verify.** Run `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider` from Git Bash; write `verify.md`, one row per criterion; show the owner the counts of slice 6. | `verify.md`, `evidence/` | The suite against the baseline of 1,623 passed (2026-11-06, after cycle 030); no migration in `git diff`. | 1 to 11 | done |

## Order and dependencies
- 1, then 2 and 3 (both depend on the date function, not on each other), then 4 (the default changes only after the rule is right, so a mid-way commit never ships a half rule), then 5, 6, 7.
- Slice 6 needs Docker Desktop (the owner's machine; I have started it in earlier cycles); it does not depend on the UI string, so it can move earlier if Docker is up and slices 1 to 3 are green.
- This tree holds cycle 030's uncommitted edits (`settings.html`, `views.py`, locale files, tests): slice 5 edits `settings.html` and the catalogue too. Stage only this cycle's hunks (`git add -p`), or let the owner commit cycle 030 first.

## Rollback
- Every slice is code only: `git revert` of its commit, or discarding the uncommitted edits to its files. No data or migration is involved, so there is nothing to undo in a database.
- A deployed change is reversed by reverting the commit: jobs hidden for age by the nightly job come back on the next refilter once the old rule is back (a hidden reason is recomputed, not a deletion). Candidates keep their stored limits throughout.

## Risks
- **Hiding more than expected on first run.** The undated rule applies to every undated job already in the inbox: slice 6 measures how many, so the owner knows before the deploy. Hidden jobs stay in "Filtered & archive" with their reason.
- **A view made today for an old job looking young** (checked in slice 1: a view has only `created_at` of its own; `first_seen_at` reads the job's, so the risk I wrote here at the plan stage does not exist; the test stays as a guard).
- **Other callers of `hidden_reason`** (jungle ranking, radar rows, the AI backtest) now also see undated old jobs as aged out; the backtest sets `max_age_days` to `None` itself (`jobs/ai/backtest.py:71`) so it is unaffected; the others' tests run in the full suite.
- **Shared tree and catalogue:** cycle 030's uncommitted locale and `settings.html` edits overlap slice 5's files (see Order).
- **Postgres not run:** the suite runs on SQLite; the new `Q` with `isnull` is plain ORM, and slice 6's timing runs on the local Postgres.

## Gate
- [x] Owner approved the slices (2026-11-06: "approved, build until you need me")

## As run
(log of the build, newest last; all 2026-11-06)
- Baseline: 1,623 passed (after cycle 030, from Git Bash).
- Live cycle board refreshed first (it had last been refreshed 2026-11-05): `cycles.json` and `actions.json` regenerated into the scratchpad, uploaded, both datasets updated (versions 129 and 153), the two old assets deleted.
- **Slice 1 done.** Tests first (2 failed for the right reason), then `filters.listing_date` and the rule. **Correction:** `CandidateJob` has no `first_seen_at` of its own (it is `JobSource`'s, `models.py:420`), it reads the job's through `__getattr__`; the plan's, the spec's and the intent's remarks about a view's own date were wrong and are fixed. `listing_date` is simply `posted_at or first_seen_at`. `tests/test_core.py:93`'s comment updated. 65 passed in `test_stale.py` + `test_core.py`.
- **Slice 2 done.** `job__first_seen_at` added to `FILTER_FIELDS`; two tests (hide/restore by limit; query count equal for 2 and 10 jobs, which fails without the field: 15 against 7).
- **Slice 3 done.** `age_out` query is `Q(posted_at<cutoff) | Q(posted_at null, first_seen_at<cutoff)`; tests for the nightly job, the off switch, and "nothing past the limit is scored or offered to the AI".
- **Slice 4 done.** Default 60 to 30 (`jobs/models.py:16`). Two tests broke for honest reasons: one assumed the default was 60 (now sets 60 itself), and `test_greenhouse_adapter_and_run` carried a hardcoded `first_published` of 2026-09-20 that had aged past 30 (and would have past 60 on 19 Nov): now generated as 3 days ago.
- **Slice 5 done.** Help text, French (aligned with the existing "Filtrées & archives"), catalogue compiled, i18n tests pass.
- **Slice 6 done.** Docker Desktop was down; I started it (local, reversible) and the Postgres container, restored the 29 Oct dump into `scratch031`, ran read-only SQL, dropped the database. Findings in `evidence/counts.md`: no undated job was over 30 days at dump time (the database starts 2026-09-29), but 106 and 1,009 are today; 485 of candidate 1's 1,632 visible views are dated over 30 days. Query cost 11 ms.
- **Slice 7 done.** Full suite: a second hardcoded date in `tests/test_jibe.py` (posted 2026-10-02) failed, fixed with a recent date; then 1,631 passed with one mail test that failed once and passed alone and in the next full run; final **1,632 passed**. `verify.md` written.
