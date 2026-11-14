# After the change, local Postgres 17 (docker-compose), 2026-11-06 (claude)

A throwaway database `saxobeat_drill32` in the local `saxobeat-db-1` container (localhost only: the drill refuses any other host; the `.env` address, which is Neon, was never used). Dropped afterwards, with its `test_` twin.

| Run | Account | Time | Statements | Result |
|---|---|---|---|---|
| 1 | 36,271 views, 0 private jobs | 2.3 s | 32 | all of theirs gone; shared jobs, the other person's views and user kept |
| 2 | 36,271 views + 5,000 private jobs | **did not finish in 9 min: stopped** | | see below |
| 3 | same as 2, on a freshly created database | 3.2 s | 42 | as run 1, and the private jobs gone |
| 4 | 36,271 views, after TRUNCATE | 2.3 s | 32 | as run 1 |
| 5 | same, after TRUNCATE and ANALYZE of empty tables | 3.0 s | 32 | as run 1 |
| 6 | 36,271 + 5,000, after TRUNCATE (the original sequence) | 3.0 s | 42 | as run 3 |
| 7 | 36,271 + 5,000, with the 30 s statement timeout added | 5.2 s | 43 | as run 3 |

`tests/test_account_delete.py` and `tests/test_accounts.py` (32 tests): all pass on this Postgres (36 s).

**Run 2 is unexplained.** It sat on `DELETE FROM jobs_score WHERE id IN (SELECT ... JOIN jobs_candidatejob ... WHERE candidate_id = 2)` for 9 minutes (state active; I did not capture the wait event or the plan before ending it). The same statement took well under a second in runs 1, 3, 4, 5, 6 and 7. I tried to reproduce it three ways (truncate; truncate plus analyze on empty tables; the original sequence) and could not. The suspicion is a bad plan from stale statistics (an `IN (subquery)` planned as a nested loop over 36,000 rows), which is not proven. Mitigation added: on Postgres the delete runs with `SET LOCAL statement_timeout = '30s'`, so a bad plan makes the delete fail fast, roll back, and show the operator's error message, instead of running into the web server's 120 s. This does not prevent the slow plan, it bounds it; whether it can happen on Neon is not known (not measured; see `verify.md`, "not verified").
