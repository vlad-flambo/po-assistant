# Plan: runner and data correctness

| | |
|---|---|
| **Cycle** | 014 |
| **Stage** | Plan approved 2026-10-29; Build done 2026-10-29; next: Verify ([verify.md](verify.md)) |
| **Spec** | [spec.md](spec.md), approved 2026-10-29 |

## Slices
Thin, ordered, each verifiable alone. Every code slice is **test first**: the test reproduces the window and fails on today's code, then the fix makes it pass. A window is reproduced by changing the row between the function's read and its write (a small hook the test patches, the way `tests/` already patches services), never by timing.

| # | Slice | Files touched | Check | Criteria | Status |
|---|-------|---------------|-------|----------|--------|
| 1 | Keep the review table (W1-W8) in `evidence/runner_writes_review.md`, each row's outcome filled as the slices land | `evidence/` | the file lists W1-W8 with an outcome each | 7 | done |
| 2 | **W1** `matching.expire`: one transaction per chunk; the `UPDATE` carries `status='new'`; the history lines are written for the rows that update changed, read back by id and `status_changed_at` | `jobs/services/matching.py`, `tests/test_runner_writes.py` (new) | test: a job shortlisted between read and write stays shortlisted and has no `new → expired` line; the existing expiry tests still pass | 1 | done |
| 3 | **W2** reopening a job: a conditional `UPDATE … WHERE status='expired'`, the history line only when it changed one row | `matching.py`, test | test: a job the candidate moved after the runner's read is not put back to `new` | 2 | done |
| 4 | **W3, W4, W7** `hidden_reason`: written with `WHERE status='new'` in the same statement (`_sync_candidate`, `refilter`, `blocks.block`) | `matching.py`, `blocks.py`, tests | test per function: a job taken up meanwhile gets no hiding reason | 3 | done |
| 5 | **W6** final score: computed in the `UPDATE` from the stored `ai_score` (a `Case` over `ai_score IS NULL`), so an AI review imported meanwhile is the one blended. If that reads more from Neon than today, fall back to a short `select_for_update` re-read; the choice and its reason go in `decisions.md` | `jobs/services/scoring.py`, test | test: an AI score written between read and write is the one in `final_score`; the existing scoring tests pass | 4 | done |
| 6 | Backup names: microseconds in the file name (`%Y-%m-%d_%H%M%S_%f`); `newest`/`prune` keep working on old names | `jobs/management/commands/backup_database.py` | `test_backup_keeps_the_latest_files_and_skips_when_one_is_recent` passes on SQLite on Windows | 5 | done |
| 7 | Full suite on both databases, nothing deselected; results pasted in `verify.md` | — | `DATABASE_URL= uv run pytest -q` and the same on the local Postgres: 0 failed | 6 | done |

## Order and dependencies
Slice 1 first (it is the checklist). Slices 2-4 are the user-visible windows, most harmful first (W1 marks a followed job as gone; W2 undoes a move; W3/W4/W7 only add a wrong hidden reason). Slice 5 is independent. Slice 6 is independent and small. Slice 7 closes. Each code slice is one commit.

## Rollback
Each slice is one commit: `git revert <sha>` undoes it alone. No migration and no data change, so a revert restores today's behaviour exactly. Nothing is deployed until the owner pushes.

## Risks
- A conditional update can make a test that relied on the old (racy) behaviour fail: read such a failure as a finding, not a reason to loosen the guard.
- W6's database expression must give the same number as `blend()` to one decimal, on SQLite and Postgres: the test compares both.
- The other session works in the same checkout: commit only this cycle's paths.

## Gate
- [x] Owner approved the slices (2026-10-29)

## As run
- 2026-10-29 slice 1: review table in `evidence/runner_writes_review.md`.
- 2026-10-29 slice 2 (W1): added the hook `matching._between_read_and_write` (no behaviour) and the test; it failed on today's code (`expired` instead of `shortlisted`). Fix: the status check moved into the `UPDATE`, the history lines written for the rows it changed. 104 expiry-related tests pass on SQLite.
- 2026-10-29 slices 3 and 4 (W2, W3, W4, W7): hooks first at each decision point; the four new tests failed on today's code. Fixes: `matching._reopen` (conditional update instead of `set_status` on the row as read), and `status='new'` in the `hidden_reason` updates of `_sync_candidate`, `refilter` and `blocks.block`. One commit for both slices: they touch the same function. Full suite on SQLite: 1,189 passed, 1 failed (the backup test, slice 6).
- 2026-10-29 slice 5 (W6): the test failed on today's code (final score 40 instead of 75). Fix: `score_job` writes the deterministic fields, then the database blends `final_score` from the row's own `ai_score` (`scoring.blended`: `Case`, `Least` for the dream bonus, `Round` to one decimal); the read of the old score before the write is gone, so the reads stay the same. Decision recorded in `decisions.md` (D1). Passes on SQLite and Postgres.
- 2026-10-29 slice 6: backup names carry microseconds (`%Y-%m-%d_%H%M%S_%f`); `newest`/`prune` sort by file time, so older names still work. The backup test passes on SQLite on Windows. Full suite on SQLite: 1,192 passed, 0 failed.
- 2026-10-29 slice 7: full suite 1,192 passed on SQLite and 1,192 passed on the local Postgres 17 (179 s). Build done; evidence in `verify.md`.
