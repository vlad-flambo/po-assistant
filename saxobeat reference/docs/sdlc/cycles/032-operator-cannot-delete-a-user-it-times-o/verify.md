# Verify: deleting an account takes a handful of statements, not thousands

| | |
|---|---|
| **Cycle** | 032 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence (command and output, measurement, screenshot, link) |
|---|-----------|--------|-------------------------------------------------------------|
| 1 | Speed: 36,271 views, under 10 s and under 50 statements | pass | SQLite temp file: **0.6 s, 33 statements** (before: 40.9 s, 72,945). `evidence/after-sqlite-2026-11-06.md`, `evidence/baseline-2026-11-06.md`. Local Postgres: 2.3 s, 32 statements. |
| 2 | Same result; the other person on the same jobs keeps everything | pass | `test_deleting_one_person_removes_all_of_theirs_and_leaves_the_other_person_on_the_same_jobs_untouched` (14 tables compared before and after); the existing `test_the_operator_deletes_an_account_...` and `test_a_person_deletes_their_own_account_...` pass unchanged. The two tests that describe behaviour passed on the old code first (slice 2). Drill output: 36,271 shared jobs, the other person's 1,000 views and user kept. |
| 3 | Private jobs go fast too (drill with 5,000) | pass | SQLite: 0.8 s, 43 statements (before: 47.3 s, 83,056). Postgres fresh database: 3.2 s, 42 statements. `test_the_private_jobs_go_with_their_sources_and_views_but_approved_sources_stay`. The guard also found two more tables under a job (`PageFetch`, `FetchAttempt`): added, see `decisions.md`. |
| 4 | Nothing forgotten, now or later (guard test over the relation graph, hidden relations included) | pass | `test_the_bulk_delete_covers_every_table_that_hangs_off_a_candidate_or_a_private_job`: failed on the old code naming 17 models, passes now; fails if a model is missing or listed without cascading. `test_the_guard_knows_the_models_of_this_app` checks it sees `Impersonation` (`related_name="+"`). |
| 5 | All or nothing | pass | `test_a_failure_in_the_last_step_leaves_everything_in_place`: a forced failure in `user.delete()` leaves the candidate, the user and all 14 tables' rows. |
| 6 | The operator is told, no hang or 500 | pass | `test_when_the_delete_fails_the_operator_is_told_nothing_was_deleted_and_the_account_is_whole`; and for the person, `test_when_the_delete_fails_the_person_stays_signed_in_and_is_told_so` (an extra: their page used to sign them out before deleting). On Postgres each statement is also capped at 30 s so a slow plan fails into this message. |
| 7 | Both entry points use it; full suite passes | pass | Full suite from Git Bash (`SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q`): 1,642 passed, 1 failed: `test_every_string_marked_in_the_code_has_a_french_translation` (my new message had no French). Fixed with `manage.py i18n extract`, the French text, `i18n compile`; `tests/test_i18n.py`, `test_account_delete.py`, `test_accounts.py` re-run: 60 passed. The whole suite was not run a second time. |
| 8 | Also right on Postgres | partial | 32 account tests pass on a local Postgres 17; drill limits met in 6 of 7 runs (2.3 to 5.2 s, 32 to 43 statements). **One run sat 9 minutes on one DELETE and was stopped; not reproduced in 4 more tries, cause unknown** (`evidence/after-postgres-2026-11-06.md`). Mitigation: 30 s statement timeout on Postgres. |
| 9 | Hosted: weiersto+0611@gmail.com deleted after deploy | pass | The owner pushed (`56e7d48` is on origin/main) and deleted the account from People on 2026-11-06: "Deleted weiersto+0611@gmail.com and their data (36271 job views, 0 private jobs). It was quick." Not timed, so no number; the 120 s limit that failed before was not reached. |

## Tests
- `tests/test_account_delete.py` (new, 10 tests) and `tests/test_accounts.py` (existing, 22): 32 pass on SQLite and on local Postgres.
- Full suite on SQLite: 1,642 passed, 1 failed (translation, fixed afterwards, see criterion 7). No other failure, in this cycle's code or in the other cycles' work in the working tree.
- Added for the guard and the size: a statement-count test (300 views, at most 80 statements) that fails on the old code.

## Not verified
- The time of the delete **on the hosted app** and the Render to Neon latency: not measured (the owner called it quick; the local numbers are 0.6 to 5 s against a 120 s limit).
- Whether the 9-minute stall on Postgres can happen on Neon. If it did, the 30 s statement timeout turns it into the "Nothing was deleted" message and the operator would report it; the account stays whole.
- The second full-suite run after the translation fix (only the translation, account and i18n files were re-run).
- Anything on Neon's own Postgres version: the drill ran on Postgres 17 from docker-compose.

## Verdict
- [x] Accepted by owner (2026-11-06: "it was quick. i consider this a success"). Criterion 8 stays partial: the one unexplained Postgres stall was not discussed as a risk and is carried into learn.md as an open item.
- [ ] Sent back (what, to which stage)
