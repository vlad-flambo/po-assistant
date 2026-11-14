# Learn: runner and data correctness

| | |
|---|---|
| **Cycle** | 014 |
| **Stage** | Learn done 2026-10-29: cycle closed (the push is the owner's) |
| **Verify** | [verify.md](verify.md), accepted by the owner 2026-10-29 |

## What happened vs what we expected
- **Success measure** (intent): a test reproduces the overwrite and passes after the fix; the full suite passes on SQLite and Postgres. **Met:** nine new tests, each seen failing on the old code; 1,192 passed on both databases, with no known failure for the first time.
- **Expected** one known window (`expire`, from cycle 001's notes). **Found** six: the review of every runner write (W1-W8) turned up the reopen (W2), three hiding-reason writes (W3, W4, W7) and a stale blend of the final score (W6). Two writes had no window.
- **Cost:** one afternoon, in the planned seven slices; slices 3 and 4 were committed together because they touched the same function.

## What we learned
- **Read, then write back is the pattern to avoid.** Every window had the same shape: a row read, a decision taken, the row saved from what was read. Putting the decision's condition in the `UPDATE` closes it with no lock, no version column and no extra read.
- **A no-op hook makes a race testable.** `matching._between_read_and_write()` sits where a runner pass has decided and not yet written; a test patches it to play the candidate. It reproduced every window deterministically, with no timing and no threads.
- **The database can do the arithmetic.** The final score's blend moved into the write (`scoring.blended`), which also removed a read: correctness and Neon's allowance pulled the same way.
- **A test that always fails hides the next failure.** The backup test failed on Windows for a month (two backups in the same second shared a name); fixing it gives a suite with zero known failures, so any red is news.
- **Not covered:** real two-process concurrency (by construction the guards are single statements), and the hosted database (the fixes ship with the next push).

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| The rule: a runner write carries its condition in its own statement; the test hook | `jobs/services/matching.py` module docstring | [x] |
| The test baseline: 1,192 passed, 0 known failures, on SQLite and on the local Postgres; how to run both | project memory `reference-running-tests` | [x] |
| Cycle 014 closed; the fixes not live until the next push | project memory `project-sdlc-cycles`; `docs/sdlc/README.md` status | [x] |
| The audit rows for `matching.expire` and the backup test now done | `cycles/006-stale-docs/evidence/prd_audit_2026-10-29.md` ("Elsewhere" table) | [x] |
| The fixes reach the hosted app | the owner's push of 2026-10-29 (`ff08c0c..d1718a0`) deployed by Render at 15:53 (cycle 004's deploy log) | [x] |

## Process feedback
- **Worked well:** the review table as slice 1 (it turned one known bug into six found ones); test first with the hook; one commit per slice with the slice number in the message; a full run on both databases as its own slice.
- **Slowed us down:** another session edits `docs/sdlc/README.md` at the same time, so its status rows had to be staged line by line. Suggestion for the playbook: let `sdlc_status.py` write the status table, so no one edits it by hand.

## Next cycle candidates
- Two runner passes at once (out of scope here: the runner is started by hand, one at a time). Only worth a cycle if the runner is ever scheduled.
