# Plan: Revolut People source

| | |
|---|---|
| **Cycle** | 020 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

## Slices
Thin, ordered, each verifiable alone. Everything here changes nothing in production.

| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | Save the real Worklife list and detail answers as fixtures (2 requests, read-only) | `tests/fixtures/revolutpeople_worklife_*.json` | files parse; 4 jobs in the list; no personal data | 2 | todo |
| 2 | The adapter, registration, platform name; tests for postings, location/remote mapping, link, failures | `jobs/sources/revolutpeople.py`, `__init__.py`, `platforms.py`, `tests/test_revolutpeople_source.py` | new tests pass | 1-7 | todo |
| 3 | Complete-listing type, and the closing test | `jobs/services/runner.py`, the test file | second run with 3 of 4 jobs closes the fourth | 8 | todo |
| 4 | Link recognition and the how-to text | `jobs/employers.py`, `jobs/sources/howto.py`, tests | link cases of criterion 9 pass | 9, 10 | todo |
| 5 | Seed Worklife (off), dry run, rehearsal on a scratch copy | `seed_employers.py`, evidence | dry run lists 1 to create; second run 0 | 11 | todo |
| 6 | Live read on the scratch copy, two runs (5 requests each, stated before running) | evidence `live_read.md` | 4 jobs, no duplicates after run 2 | 12 | todo |
| 7 | Full suite, then `verify.md` | `verify.md`, `evidence/` | suite green; one row per criterion | 13, 14 | todo |

## Order and dependencies
1 first (the tests read the fixtures); 2 before 3 and 4; 5 needs 2; 6 needs 5; 7 last. The scratch copy for 5 and 6 is the local Postgres container (Docker Desktop running), a fresh one, as in cycle 013.

## Rollback
Nothing is deployed: each slice is a commit (or uncommitted change) that can be reverted with `git revert` or by deleting the new files; the seed only touches a scratch copy. The hosted seed is a separate owner step and, like the other sources, it is one disabled row that can be deleted from the Sources page.

## Risks
- The API changes or Cloudflare starts challenging it: shows as a source error (criteria 6, 7), source stays off meanwhile.
- The `people-jobs.com` link may not open for everyone (the iframe was blank in my browser pane): the owner checks it (D1); the fallback is the `revolutpeople.com/<tenant>/public/careers/apply/<id>` link.
- Worklife's descriptions are French/English mixed with HTML lists: stored as given.
- Terms of use unread: the source stays off until the owner has read them.

## Gate
- [x] Owner approved the slices (2026-11-03, "Approve both")

## As run (2026-11-03)
- Slice 1 done: list plus 4 details fetched (5 requests, honest user agent) and saved as `revolutpeople_worklife_list.json` and `_details.json`. Note: the detail has no `type` key (that was the location's type); spec text corrected in effect, nothing depends on it.
- Slice 2 done: adapter, registration, platform name, 10 tests. Slice 3 done: `COMPLETE_LISTING_TYPES`, closing test; a mutation (entry removed) fails it.
- Deviation, slice 2: a 5xx on a detail raises instead of skipping (spec criterion 6 said skip 404 and 5xx): skipping would make the runner close a live job.
- Slice 4 done: `detect_system` for `people-jobs.com/<tenant>` and `revolutpeople.com/<tenant>/public/careers`, how-to text, tests.
- Slice 5 done on a fresh scratch Postgres `measure_rp_20261103`: dry run 1 to create, apply 1 added, again 0 added.
- Slice 6 done (10 requests): run 1 fetched 4 new 4, run 2 fetched 4 new 0, no duplicates.
- **Found after slices 5 and 6, while collecting evidence for verify: robots.txt of revolutpeople.com disallows the API.** Not checked in the spec (my miss). Fixed by making `fetch` obey robots.txt (2 tests, one with the real file). The live read of slice 6 can no longer be repeated by the app. See verify.md.
- Slice 7 done: full suite 1,432 pass on SQLite; scratch database dropped; `verify.md` written.
- **Owner's decision D1 (2026-11-03): "Override the rule".** Done as a per-source flag `ignore_robots` (the default stays "obey"); Worklife seeded with it, off; decisions.md written; 2 tests. Slice 6 repeated with the final adapter on a fresh scratch Postgres (10 requests: 4 jobs, then 0 new, 4 distinct links); suite 1,434 pass; scratch database dropped.
