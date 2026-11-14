# Verify: simplify-ops-console

| | |
|---|---|
| **Cycle** | 024 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |

*Built and checked locally on 2026-11-04. Nothing is committed, pushed or deployed; the live `/ops/` has not been seen (it needs a login), so criteria are proven on the code and a local server, and slice 8 (yours) is the live check.*

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence (command and output, measurement, screenshot, link) |
|---|-----------|--------|-------------------------------------------------------------|
| 1 | The main bar holds exactly seven area links, in order, then "← Candidate app" and "Log out" | pass | `tests/test_ops_nav.py::test_the_bar_has_seven_areas_then_the_way_back_and_nothing_else`; the bar read in the browser (`evidence/today-1024.jpg`, `evidence/more-emails-1280.jpg`) |
| 2 | Each of the former pages marks the right area, and the right tab in the second row | pass | `test_each_page_marks_its_area_and_its_tab` (15 pages: every `ops_*`, `sources`, `jungle`, `runs`, `people`, `data`, Instructions marking Settings); the tab labels and marks read from the live DOM of all 15 pages at 800 px (`evidence/browser-check.md`) |
| 3 | No address changed; each still 200 for the operator, "not found" for a candidate | pass | `test_the_old_addresses_are_the_same_and_closed_to_candidates`; `tests/test_roles.py` address lists pass with only its nav wording changed; no URL file in the diff (`git diff --stat` lists no `urls.py`) |
| 4 | Every page has a one-line purpose in `p.purpose`, one `h1`; the Candidates page reads "Candidates" | pass | `test_every_console_page_says_in_one_line_what_it_is_for` (15 pages), `test_the_candidates_page_is_called_candidates_like_its_area`; read in the DOM of all 15 pages at 800 px |
| 5 | Import has no "Recent exports" table and links to Exports; Exports still lists and resends; the runner-folder report is on Import | pass | `test_import_has_the_runner_report_and_no_copy_of_the_exports_table`; the existing Exports tests (`tests/test_ops_ai.py`) pass unchanged |
| 6 | AI pages show the one-line status strip; Today has no pack cards or runner card | pass | `test_the_ai_strip_is_on_the_ai_pages_and_nowhere_else` (15 pages), `test_the_ai_strip_says_what_is_waiting_late_paused_and_stale`, `test_today_no_longer_carries_the_pack_cards_or_the_runner_folder`; the strip seen in `evidence/ai-export-800.jpg`; queries: Today cost 25 before, the AI queue page costs 24 with the strip (`test_an_ai_page_costs_no_more_queries_than_today_did`) |
| 7 | Today in the agreed order, empty blocks left out, "Nothing needs you today.", badges stay | pass | `test_today_shows_the_daily_items_in_the_order_the_owner_reads_them`, `test_today_with_nothing_to_do_says_so_and_still_shows_the_last_run_and_the_ai_line`, `test_the_badges_stay_on_sources_and_feedback`; Today seen with all blocks filled (`evidence/today-1024.jpg`) |
| 8 | No function lost; every former page is one or two clicks from the bar | pass | `test_every_former_page_is_one_or_two_clicks_from_the_bar` (follows the bar and each area's second row to all 14 former pages, each 200). The only element removed is Import's duplicate table (criterion 5); the two Export/Import facts that lived on Today (pack breakdown, runner folder, on-time rate) are in the AI strip and on Import. |
| 9 | Full suite passes; tests whose nav wording changed updated and named; new tests for 1, 2, 4, 5, 6, 7 | pass | `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider`: **1499 passed**, 0 failed (2026-11-04). `tests/test_ops_nav.py`: 56 tests, all new. Changed existing tests (wording or the page the fact moved to, no check weakened): `test_roles.py` (the bar's entries), `test_ai_running.py` (on-time rate now on the AI page), `test_ai_sync.py` (runner report now on Import), `test_ops_ai.py` (Today's AI line, pack breakdown on the AI page). Listed in `plan.md` "As run". |
| 10 | Each of the seven areas and each tab seen in a real browser at desktop width and about 800 px, no overflow, screenshots in `evidence/` | partial | Local server on a throwaway SQLite database, signed in as a throwaway operator. Measured in the DOM at 800 px on all 15 console pages: no horizontal overflow, one `h1`, a purpose line, correct area and tabs, strip only on AI pages. At 1280 px only the E-mails page and the bar height were measured (one row, 55 px); screenshots exist for 3 pages (`evidence/`). At 800 px the right-hand side of the bar ("← Candidate app", "Log out") wraps onto a second row (the whole bar needs about 905 px). Details and what was not traced: `evidence/browser-check.md`. |

## Tests
- Full suite, 2026-11-04: **1499 passed**, no failures, no known failures. (The first full run after slice 5 had 3 failures: three old tests that looked for AI facts on Today, which this cycle moved on purpose; they were repointed to where the fact now is, with the same assertions, and the suite re-run.)
- The `tests/test_ops_nav.py` mistake on its first run (my own reachability test skipped the first link) was fixed in the test.

## Not verified
- **The live Console** at `https://app.saxobeat.fr/ops/` (login needed here): the owner's slice 8. In particular the real data shapes (many candidates, long source lists) were not seen; the check used a few seeded rows.
- **Layout at 1280 px beyond one page**, and **screenshots of 12 of the 15 pages**: the DOM measurements stand in for them (weaker than looking).
- **The browser console message** "An unknown error occurred when fetching the script" repeated on every page, not traced to a request (the dev server log shows no 5xx or traceback), and not compared with the old Console. Probably the pane's tooling; unconfirmed.
- **Sources stat tiles**, the Export page's candidate table clipping at 800 px: unchanged, outside this cycle (spec "Out of scope").
- **Phone widths**: the Console is desktop-first; nothing below 800 px was looked at.

## Verdict
- [x] Accepted by owner (2026-11-04, criterion 10 partial: the live site and phone widths are the owner's own look)
- [ ] Sent back (what, to which stage)
