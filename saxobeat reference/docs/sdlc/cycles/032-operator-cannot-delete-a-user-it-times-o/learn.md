# Learn: deleting an account takes a handful of statements, not thousands

| | |
|---|---|
| **Cycle** | 032 |
| **Stage** | Learn |

## What happened vs what we expected
- **Measure 1 (speed, under 10 s and 50 statements for 36,271 views):** met locally, 0.6 s and 33 statements on SQLite (was 40.9 s, 72,945), 2.3 s and 32 on a local Postgres.
- **Measure 2 (same result, nothing shared touched):** met; 14 tables compared before and after in a test with a second person on the same jobs.
- **Measure 3 (no hang):** met in tests (forced failure leaves everything, operator sees "Nothing was deleted").
- **Measure 4 (the real account deleted on the hosted app):** met on 2026-11-06. The owner pushed, deleted weiersto+0611@gmail.com (36,271 job views, 0 private jobs), saw the confirmation, and called it quick and a success. The time was not measured.
- The cause I proposed at Intent (Django's cascade, row by row, over a network) was right, but my first size was wrong by a factor of ten: the 7,700 statements I reported came from a capped query log; the real number was 72,945.

## What we learned
- Deleting an account through Django's cascade scales with the number of rows, not the number of tables. For an account with tens of thousands of job views, that is a minute locally and past the web server's limit when the database is across a network.
- The guard test paid for itself at once: it found two tables (`PageFetch`, `FetchAttempt`) that my own reading of the models had missed, and it needs `include_hidden=True` because `Impersonation` has `related_name="+"`.
- A test written first, on the old code, separated "behaviour to keep" (passed on the old code) from "what the change adds" (failed on the old code). That made the rewrite safe to do in one go.
- A local Postgres is worth running even when SQLite is fast: one drill run stalled 9 minutes on a single `DELETE ... IN (SELECT ...)`. I could not reproduce it (4 more runs, 2.3 to 5.2 s), and I did not capture the plan. The cause is unknown. A 30 s statement timeout bounds the damage; it does not explain it.
- The old "delete my account" page signed the person out before deleting, so a failure would have left them signed out with the account still there. It now deletes first.
- The suite caught the missing French string on the first full run, as intended; it was committed with this learn step.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| Deleting is bulk, seconds, all or nothing; a failure shows "Nothing was deleted"; new models must be added to the lists in `jobs/accounts.py` | `docs/DEPLOY.md` (Switch off / delete) | [x] |
| Django cascade cost, bulk delete with a guard test, `statement_timeout`, the 9-minute stall | house-stack `reference/gotchas.md` | [x] |
| A capped query log undercounts a big drill; count with `connection.execute_wrapper` | house-stack `reference/gotchas.md` | [x] |
| Cycle 032 state (commit, deploy, verdict) | project memory `project-sdlc-cycles` | [x] (state written on 2026-11-06; add "closed" with the next memory pass) |
| French text of the new error (it was left out of the first commit: the catalogue then carried other cycles' edits; by the end only mine) | `locale/fr/LC_MESSAGES/django.po` and `.mo`, committed with this learn step | [x] |
| The unexplained Postgres stall | a reading if it ever shows on the host: a "Nothing was deleted" message from the 30 s timeout is the signal; then capture `EXPLAIN` and `pg_stat_activity` before ending it | [x] deferred 2026-11-06 on purpose: acted on only if it happens (no date: it is a trigger, not a task) |

## Process feedback
- **Worked well:** measuring before designing (the baseline script), writing the tests on the old code before the rewrite, and a guard test instead of a hand-checked list. The owner's one-word gates kept the cycle moving at one decision per message.
- **Slowed us down:** (1) a headline number from a capped log, noticed only because a second, exact counter disagreed: when a number goes into the intent, say how it was counted. (2) Committing a cycle that touches a shared file (`django.po`, the README table, `BOARD.md`) when other sessions have uncommitted edits in it: I left those out, which meant a commit whose own tests need a file that is not in it. The skill could say: when a cycle changes a shared catalogue, say at Plan time how it will be committed.
- **For the skill:** a drill that writes to a throwaway database needs a refusal guard written first (this one refuses anything but a temp SQLite file or a localhost Postgres). That was in the plan and it removed a real risk (`.env` points at Neon).

## Next cycle candidates
- Nothing that follows from this one. If the unexplained stall ever shows on the host, a small cycle to capture the plan and decide whether the delete needs a different shape (for example `DELETE ... USING`).
- Existing candidates elsewhere on the board are unchanged.
