# Every runner write to a candidate's rows (review of 2026-10-29)

Read in the code at `2035a74`. A **window** is a row read, then written later from what was read, so a change the candidate makes in between is lost. Each row's outcome is filled in as the slice that handles it lands.

| # | Where | What it writes | Window? | Outcome |
|---|---|---|---|---|
| W1 | `matching.expire` | status `new` → `expired`, plus a history line | Yes: selects the `new` rows, then updates them by id with no status check | **fixed** (slice 2): the `UPDATE` carries `status='new'`; history lines only for the rows it changed; test `test_a_job_shortlisted_while_the_runner_expires_it_stays_shortlisted` failed before, passes after |
| W2 | `matching._sync_candidate`, a reopened job | status `expired` → `new` (`set_status` saves the status as read) | Yes | **fixed** (slice 3): a conditional `UPDATE … WHERE status='expired'` (`matching._reopen`), the history line only when it changed the row; test `test_a_job_moved_while_the_runner_reopens_it_keeps_the_move` failed before, passes after |
| W3 | `matching._sync_candidate`, a changed job | `hidden_reason` (`save(update_fields=…)` on a row read as `new`) | Small: a wrong hiding reason on a job the candidate now follows | **fixed** (slice 4): `UPDATE … WHERE status='new'`; test `test_a_job_taken_up_while_the_runner_judges_it_again_gets_no_hiding_reason` failed before |
| W4 | `matching.refilter` | `hidden_reason` by id | Small: same as W3 | **fixed** (slice 4): same guard, counted only when it changed the row; test `test_refilter_leaves_a_job_taken_up_meanwhile_alone` failed before |
| W5 | `matching.age_out` | `hidden_reason` (age) | No: one `UPDATE … WHERE status = 'new' AND hidden_reason = ''` | no window |
| W6 | `scoring.score_job` | deterministic fields and `final_score` | Partly: AI fields are never written, but `final_score` blends the AI score read before the write | **fixed** (slice 5): the database blends `final_score` from the row's own `ai_score` in the write (`scoring.blended`); the earlier read of the score is gone (same number of reads as before); test `test_an_ai_review_imported_while_the_runner_scores_is_the_one_blended` failed before (40 instead of 75), passes on SQLite and Postgres |
| W7 | `blocks.block` (web) | `hidden_reason` (blocked) by id | Small: ids from a list read moments before | **fixed** (slice 4): `WHERE status='new' AND hidden_reason=''`; test `test_blocking_leaves_a_job_taken_up_meanwhile_alone` failed before |
| W8 | `ingest`, `freshness` | `Job`, `JobSource` only | No: shared catalogue rows, nothing a candidate changes | no window |
