# Plan: deleting an account takes a handful of statements, not thousands

| | |
|---|---|
| **Cycle** | 032 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

## Slices
Thin, ordered, each verifiable alone. Each slice names the acceptance criteria it moves. Slices 1 to 7 are the agent's, local only, and change nothing hosted; slice 8 is the owner's and is the only one that does.

| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | **Baseline.** Make the drill realistic (per view: a score, a status change; on a share of them an interview, a cheat sheet, a packet, an AI task; plus N private jobs), make it refuse any database that is not a temporary SQLite file or a localhost Postgres, and measure the **current** code. | `evidence/drill_delete.py`, `evidence/baseline-2026-11-06.md` | Drill prints time, statements and rows left; the baseline is recorded before anything changes | 1, 3 (the "before") | done |
| 2 | **Tests first.** Add the tests that must hold before and after: two candidates on the same shared jobs (the other keeps everything), all-or-nothing (forced failure in the last step leaves everything), and the guard test over the relation graph (written to compare against the table list of slice 3, so it fails until slice 3 lands). | `tests/test_account_delete.py` | The same-result and all-or-nothing tests pass on the **old** code (they describe behaviour to keep); the guard test fails with the model names it expects | 2, 4, 5 | done |
| 3 | **The bulk delete.** Rewrite `accounts.delete_account`: one DELETE per table, children before parents, one transaction; the table list written once next to the function. Same name, same return. Private jobs get the same treatment (their views, scores, sources, then the jobs). | `jobs/accounts.py` | Slice 2's tests all pass, including the old `test_the_operator_deletes_an_account_...` and `test_a_person_deletes_their_own_account_...` untouched | 2, 3, 4, 5, 7 | done |
| 4 | **The operator sees an error, not a hang.** The "delete" action catches a failure, shows "Nothing was deleted: ..." and redirects back to People; the person's own page shows its existing error style. | `jobs/views_accounts.py`, `locale/fr/LC_MESSAGES/django.po` (only if the person-facing text is new; the operator console is English), `tests/test_account_delete.py` | Forced-error test: the account is unchanged and the People page carries the message | 6 | done |
| 5 | **Drill after, on SQLite.** Rerun slice 1's drill on the new code. | `evidence/after-sqlite-2026-11-06.md` | Under 10 s and under 50 statements for 36,271 views, and for 5,000 private jobs | 1, 3 | done |
| 6 | **Postgres.** Start the local database from `docker-compose.yml` (the daemon must be running), create a separate drill database in it, and run the drill and `tests/test_account_delete.py` and `tests/test_accounts.py` against it. `DATABASE_URL` is set for these processes to the localhost address only, never the `.env` one (Neon). If Docker will not start, record "not checked", not "pass". | `evidence/after-postgres-2026-11-06.md` | Same limits as slice 5; the three test files pass on Postgres | 8 | done |
| 7 | **Whole suite, then Verify.** Full suite from Git Bash; write `verify.md` with one row per criterion (criterion 9 `pending`). | `docs/sdlc/cycles/032-.../verify.md` | `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider`: no new failure | 7 | done |
| 8 | **Ship and delete the account (owner).** The owner agrees to the commit; commit only the paths of this cycle (the working tree holds other cycles' changes); the owner pushes and deploys on Render, then opens People and deletes weiersto+0611@gmail.com (typing the address). I note the time it took and tick criterion 9 on the owner's word. | none for the agent (commit by agreement); owner on the hosted app | The row disappears from the People page and the page answers without a timeout | 9 | todo |

## As run (2026-11-06)
- **Slice 1:** drill made realistic and exact (`connection.execute_wrapper` counts every statement). Baseline: 40.9 s / 72,945 statements (36,271 views), 47.3 s / 83,056 (plus 5,000 private jobs). The first measurement's "7,700 queries" was an undercount (Django's query log keeps 9,000 entries): corrected in evidence and intent.
- **Slice 2:** 10 tests written first; on the old code the 6 behaviour tests passed and the statement-count and guard tests failed as intended. The guard named 17 models, among them `PageFetch` and `FetchAttempt`, which the plan had not listed (they hang off a job).
- **Slice 3:** `delete_account` rewritten (lists `VIEW_TABLES`, `CANDIDATE_TABLES`, `JOB_TABLES`, `BULK_DELETED`). First version used `candidate.delete()` at the end: 43 / 53 statements, so the last step became an UPDATE plus one raw DELETE (33 / 43).
- **Slice 4:** both entry points catch a failure. Added to the plan: the person's own page now deletes before signing out. French string added with the repo's `manage.py i18n` after the suite caught it.
- **Slice 5:** SQLite after: 0.6 s / 33 and 0.8 s / 43.
- **Slice 6:** Postgres (docker, localhost only): 2.3 to 5.2 s, 32 to 43 statements, 32 tests pass; **one run stalled 9 minutes on one DELETE and was not reproduced**; a 30 s `statement_timeout` was added for Postgres. Drill databases dropped.
- **Slice 7:** full suite 1,642 passed, 1 failed (the French string, fixed; 60 related tests re-run). `verify.md` written: 7 pass, 1 partial (8), 1 pending (9, the owner's).
- **Slice 8:** waiting for the owner.

## Order and dependencies
- Baseline first, so "before" and "after" come from the same script. Tests next, on the old code, so they define the behaviour to keep and cannot be shaped by the new code. Then the rewrite, then the error handling (it depends on nothing but is only testable once the function exists).
- Slices 5 and 6 need slice 3. Slice 7 needs all of 1 to 6. Slice 8 needs the owner's agreement to the commit and the push, and comes last because it is the only irreversible step and the only one on the hosted database.
- Slice 3 touches one function; slice 4 one view branch: neither touches a migration, a setting or a page layout.

## Rollback
- Slices 1 to 7: code and tests in the working tree before any commit; undo with `git checkout -- jobs/accounts.py jobs/views_accounts.py` and delete the new test and evidence files. Nothing hosted or persistent was touched, and the temporary databases are removed after each run.
- Slice 8, the code: `git revert` of the one commit and a redeploy. Not needed for data: there is no migration.
- Slice 8, the deletion itself: **not reversible** (that is the request). Before it, the owner can decide whether Neon's point-in-time restore window is enough as a safety net; nothing in the plan depends on it.

## Risks
- **`_raw_delete` is a private Django method.** It is used by Django itself and stable across versions, but a Django upgrade could change it. Mitigation: the tests in slice 2 run in the suite on every change; the Django version in use is noted in `learn.md`.
- **A table missing from the list** would make the last DELETE fail on a foreign key (loudly, and rolled back), not leave stray rows: Postgres enforces the keys. The guard test (criterion 4) catches it in the suite first.
- **Postgres plans** differ from SQLite for `IN (subquery)` deletes on 36,000+ rows: that is why slice 6 exists. If the Postgres drill is slow, the fallback within the same design is deleting by `candidate_id` joins (`USING`), decided then and recorded in `decisions.md`.
- **The local drill's database could be confused with a real one.** The drill script refuses anything that is not a temp SQLite file or a localhost address, and prints only the kind of database, never an address.
- **Other cycles' edits are in the same working tree** (`jobs/models.py`, `jobs/views.py`, tests): stage only this cycle's paths, and run the suite knowing other work-in-progress may fail on its own.

## Gate
- [x] Owner approved the slices (2026-11-06)
