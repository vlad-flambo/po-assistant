# Verify: Revolut People source

| | |
|---|---|
| **Cycle** | 020 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |

## What the owner must know first
**`revolutpeople.com/robots.txt` forbids reading the API** (`Disallow: /`; only `/public/careers`, terms and privacy allowed; `people-jobs.com/robots.txt` the same). I read it after the build and after the first live read; the spec had missed it (my omission; the probe's ~25 requests and the first scratch read's 10 were made without the check).

**Owner's decision D1 (2026-11-03, "Override the rule", against my recommendation): read it anyway, per source.** The override is explicit and narrow: the adapter still obeys robots.txt unless the source's config has `"ignore_robots": true`; only Worklife is seeded with it (off); every other adapter and the shared check are unchanged. See [decisions.md](decisions.md). Not covered by the override and still open for the owner: the terms of use of revolutpeople.com (not read), and enabling the source.

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Registered `revolutpeople`, platform name, help line | pass | `test_the_adapter_is_registered_and_named` |
| 2 | Postings with text, date, company, `ats` | pass | `test_each_posting_gets_its_text_date_and_public_link` (real Worklife answers of 2026-11-03 as fixtures) |
| 3 | Link `people-jobs.com/<tenant>/apply/<id>` | pass in code; **link opens fine in the owner's browser (owner's word, 2026-11-03)** | same test; the page was blank in my browser pane |
| 4 | Location and remote type | pass | `test_places_become_a_location...`, `test_remote_and_missing_places` |
| 5 | No guessed salary | pass | `test_salary_is_not_guessed_from_the_title` |
| 6 | Failure handling | **changed on purpose**: a 404 detail is skipped; a 5xx on a detail or the list **raises**. Skipping a job on a server error would let the runner close a live job as "no longer listed" | `test_a_posting_taken_down...`, `test_a_failing_server_stops_the_run...` |
| 7 | Unknown tenant is an error naming it | pass | `test_an_unknown_tenant_is_an_error_naming_it_not_zero_jobs` |
| 8 | Complete-listing type, closing test | pass, mutation-checked: without the `runner.py` entry the test fails | `test_a_run_stores_four_jobs_once_and_closes...` |
| 9 | Link recognition | pass | `test_revolut_people_links_are_recognised` (5 positive, 5 negative links) |
| 10 | How-to text | pass | `test_the_type_has_a_how_to_text` |
| 11 | Worklife seeded off, dry run, second run adds 0 | pass | scratch Postgres `measure_rp_20261103`: "1 would be created", then "1 sources added", then "0 sources added, 1 already present"; source row `enabled = f` |
| 12 | Live read, 4 jobs once over two runs | pass, with the final adapter and the override flag: run 1 ok, fetched 4, new 4, 5 requests; run 2 ok, fetched 4, new 0, 5 requests; 4 jobs, 4 distinct links, all `Worklife`, `Paris` (one hybrid) | [evidence/live_read_2026-11-03.md](evidence/live_read_2026-11-03.md); a first read before the robots finding gave the same counts; both scratch databases dropped |
| 13 | Full suite | pass | 1,434 passed on SQLite (`DATABASE_URL=`), 2026-11-03, after the robots change; not run on Postgres |
| 14 | Nothing written to the hosted database | pass | only the scratch database `measure_rp_20261103` was written, then dropped; `SAXOBEAT_HOSTED_DATABASE_URL` and the fallback were set to `measurement-disabled` for those runs |

## Tests
`tests/test_revolutpeople_source.py` (16 tests: registration, postings, company default, locations, salary, 404, 5xx, unknown tenant, closing, link recognition, how-to, robots refusal with the real file, the owner's `ignore_robots` flag (and that a source without it still refuses), the seed entry, robots allowing). Related files pass. Full suite 1,434 passed.

## Not verified
- The terms of use of revolutpeople.com: **read by the owner on 2026-11-03** (owner's word; I have not seen their content, and the override D1 stands).
- The suite on Postgres (only the new source's runs were rehearsed there).
- The adapter against any tenant other than `worklife`; the robots-allows case is only mocked.

- The hosted run (2026-11-04): the owner ran the Step 3 seed on prod and says it seems to work; I have not read the hosted row or any run back. The owner then enabled Worklife and says the first by-hand pass stored its 4 jobs (owner's word, also not read back by me).

## Verdict
- [x] Accepted by owner (2026-11-03, "accept the verify record"; accepted with the risks listed under "Not verified" and the robots.txt override D1)
- [ ] Sent back (what, to which stage)
