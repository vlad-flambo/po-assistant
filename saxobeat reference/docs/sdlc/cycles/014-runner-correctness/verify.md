# Verify: runner and data correctness

| | |
|---|---|
| **Cycle** | 014 |
| **Stage** | Verify: accepted by the owner 2026-10-29; next: Learn ([learn.md](learn.md)) |
| **Spec** | [spec.md](spec.md) |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | W1: a job changed between `expire`'s read and write keeps its status, no `new → expired` line | pass | `tests/test_runner_writes.py::test_a_job_shortlisted_while_the_runner_expires_it_stays_shortlisted`: failed on the code before the fix (`expired` instead of `shortlisted`), passes after; commit `72f8fbf` |
| 2 | W2: a reopened job goes back to `new` only if still `expired` at the write | pass | `test_a_job_moved_while_the_runner_reopens_it_keeps_the_move` failed before, passes after; `test_a_reopened_job_nobody_touched_comes_back` passes; commit `44758e2` |
| 3 | W3, W4, W7: `hidden_reason` written only on rows still `new`, in the same statement | pass | `test_a_job_taken_up_while_the_runner_judges_it_again_gets_no_hiding_reason`, `test_refilter_leaves_a_job_taken_up_meanwhile_alone`, `test_blocking_leaves_a_job_taken_up_meanwhile_alone`: all failed before, pass after; commit `44758e2` |
| 4 | W6: the final score blends the AI score stored at the moment of the write | pass | `test_an_ai_review_imported_while_the_runner_scores_is_the_one_blended`: failed before (final 40 instead of 75), passes after on SQLite and Postgres; decision D1; commit `31910e3` |
| 5 | The backup test passes on SQLite on Windows | pass | `tests/test_accounts.py::test_backup_keeps_the_latest_files_and_skips_when_one_is_recent` passes in the full SQLite run; commit `f3c7f4d` |
| 6 | The full suite passes on SQLite and Postgres, nothing deselected | pass | SQLite (`DATABASE_URL= uv run pytest -q`): **1,192 passed, 0 failed** (2026-10-29). Local Postgres 17 (`uv run pytest -q --create-db`): **1,192 passed, 0 failed** in 179 s (2026-10-29) |
| 7 | The review table kept with each row's outcome | pass | [evidence/runner_writes_review.md](evidence/runner_writes_review.md): W1-W4, W6, W7 fixed; W5, W8 no window |

## Tests
Nine new tests in `tests/test_runner_writes.py`. Each plays the candidate at `matching._between_read_and_write()`, a no-op hook placed where a runner pass has decided and not yet written; the hook was added first and every window's test was seen failing on the old code before its fix. No existing test had to change.

## Not verified
- **Real concurrency** (two processes, the runner on the PC and the web app on Render) was not run: the tests reproduce the interleaving deterministically through the hook. The guards are single SQL statements, so they hold under real concurrency by construction; the hook shows the old code lost the change and the new code does not.
- **On the hosted database**: nothing was run there (cycle 001's measurements must stay clean). The change ships with the next push.
- **Reads from Neon**: not measured. By design W1 and W2 read no more than before (W1 now reads the changed ids once, after the update, instead of reading the rows before it), and W6 drops a read and adds one, so the count is the same.

## Verdict
- [x] Accepted by owner (2026-10-29)
- [ ] Sent back (what, to which stage)
