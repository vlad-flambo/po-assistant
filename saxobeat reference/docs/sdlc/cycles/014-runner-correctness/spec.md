# Spec: runner and data correctness

| | |
|---|---|
| **Cycle** | 014 |
| **Stage** | Spec approved 2026-10-29; next: Plan ([plan.md](plan.md)) |
| **Intent** | [intent.md](intent.md), approved 2026-10-29 |

## Behaviour when finished
- A runner pass never undoes what a candidate did while it ran. When a friend shortlists, dismisses or applies to a job at the moment the runner marks it gone, reopens it or re-judges it, the friend's change stays and no false line appears in the job's history.
- A job's final score never blends an AI review that was replaced while the runner was scoring.
- The test suite passes on SQLite and on Postgres, with no known failure.

## What the review found (2026-10-29)
Every write a runner pass makes to a candidate's rows, read in the code. "Window": the row is read, then written later from what was read, so a change made in between is lost.

| # | Where | What it writes | Window? |
|---|---|---|---|
| W1 | `matching.expire` | status `new` → `expired`, plus a history line | **Yes.** It selects the `new` rows, then updates them by id without checking the status again: a shortlist made in between becomes `expired`, and the history says `new → expired` |
| W2 | `matching._sync_candidate`, reopened job | status `expired` → `new` (`set_status`) | **Yes.** `set_status` saves the status from the row as read: a friend's own change after the runner's read is overwritten |
| W3 | `matching._sync_candidate`, changed job | `hidden_reason` | **Small.** Saved on a row read as `new`: if the friend acted meanwhile, a hiding reason lands on a job they now follow (it is ignored outside `new`, but it is wrong data) |
| W4 | `matching.refilter` | `hidden_reason` | **Small.** Same as W3 (it runs after a filter change, from the web or a command) |
| W5 | `matching.age_out` | `hidden_reason` (age) | No: one `UPDATE … WHERE status = 'new' AND hidden_reason = ''` |
| W6 | `scoring.score_job` | the deterministic fields and `final_score` | **Partly.** AI fields are never written (they are not in `defaults`), but `final_score` blends the AI score read before the write: an import landing in between leaves a stale final score until the next scoring |
| W7 | `blocks.block` (web, not the runner) | `hidden_reason` (blocked) | Small: ids from a list read moments before, no status check in the update |
| W8 | `ingest`, `freshness` | `Job` and `JobSource` only | No: shared catalogue rows, nothing a candidate changes |

## Acceptance criteria
Each one is checked in `verify.md` with a test that fails before the fix and passes after it.
1. [ ] **W1:** a job whose status changes between `expire`'s read and its write keeps the new status, and gets no `new → expired` history line.
2. [ ] **W2:** a reopened job goes back to `new` only if it is still `expired` (by the runner) at the moment of the write.
3. [ ] **W3, W4, W7:** `hidden_reason` is written only on rows still `new`, in the same statement.
4. [ ] **W6:** the final score blends the AI score as stored at the moment of the write, not as read before.
5. [ ] The backup test passes on SQLite on Windows: two backups in the same second get different names.
6. [ ] The full suite passes on SQLite and on Postgres, with nothing deselected.
7. [ ] The review table above is kept in `evidence/` with each row's outcome (fixed, or no window).

## Design in brief
- **Conditional writes, not locks.** Every runner write to a candidate's row carries the condition it was decided on (`status='new'`, `status='expired'`) in its own `UPDATE`. The database applies it atomically; a row that no longer matches is simply left alone. History lines are written only for the rows the update actually changed (ids re-read after the update, within one transaction).
- **W6:** compute `final_score` in the database from the stored `ai_score` (a `Case` expression in the same `UPDATE`), or re-read `ai_score` inside a short transaction with `select_for_update`. To be decided in the plan, by what reads less from Neon.
- **Backup names:** add the microseconds (or a counter) to the file name.
- **Rejected:** row locks for the whole runner pass (they would block the web app for minutes); a version column on `CandidateJob` (a migration and a change to every write, for windows the conditional updates already close).

## Interfaces and data
`jobs/services/matching.py`, `jobs/services/scoring.py`, `jobs/services/blocks.py`, `jobs/management/commands/backup_database.py`, tests. No migration, no setting, no change to what the user sees.

## Constraints
- No extra reads from Neon per job: the guards go in the `WHERE` of writes the runner already makes (cycle 001).
- Tests run on both databases (`DATABASE_URL=` for SQLite, the local Postgres otherwise); nothing touches the hosted database.

## Out of scope
- A local working copy of the database (cycle 001, D1).
- Concurrency between two runner passes (the runner is started by hand, one at a time).

## Gate
- [x] Owner approved this spec (2026-10-29)
