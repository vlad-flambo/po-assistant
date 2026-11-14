# Plan: simplify-ops-console

| | |
|---|---|
| **Cycle** | 024 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

## Slices
Thin, ordered, each verifiable alone. Tests run as PROJECT.md says: `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider`. Everything here is code in the working tree and local: nothing touches the hosted app until slice 8.

| # | Slice | Files touched | Check | Criteria | Who | Status |
|---|-------|---------------|-------|----------|-----|--------|
| 1 | **The bar and the second rows.** `ops_area` tag holds the one table page name to area and tab; `ops/base.html` renders seven area links and, under them, the second row (`ops/_subnav.html`). `nav.opsnav` stays on the main bar only. Update the one existing nav assertion in `test_roles.py` | `jobs/templatetags/jobs_extras.py`, `jobs/templates/jobs/ops/base.html`, `jobs/templates/jobs/ops/_subnav.html`, `tests/test_roles.py`, new `tests/test_ops_nav.py` | new test: seven links in order; for every console page name the right area and tab is marked (Instructions marks Settings, source-detect marks Sources); existing role and ops tests pass | 1, 2, 3 | claude | done 2026-11-04 |
| 2 | **Purpose lines and the Candidates heading.** One `<p class="muted purpose">` under the heading of each console page; the People page's heading becomes "Candidates" | the 14 console templates (`ops/*`, `sources`, `runs`, `jungle`, `data`, `people`) | test over every console page name: a non-empty `p.purpose` and one `h1`; Candidates page h1 reads "Candidates" | 4 | claude | done 2026-11-04 |
| 3 | **Import without the duplicate table.** Remove "Recent exports" from Import, link to Exports; move the runner-folder report (files waiting, files held back) onto Import; its context comes from `AiSettings.runner_report` | `ops/import.html`, `jobs/views_ops.py` (`import_page`) | test: Import has no "Recent exports", has the Exports link and the held-back list; Exports page still lists and resends | 5 | claude | done 2026-11-04 |
| 4 | **The AI status strip.** `ops_ai_strip` inclusion tag over `queue.summary()`, `queue.on_time()` and the runner report, partial `ops/_ai_strip.html`, shown on the AI pages only (export, import, queue, settings, instructions) | `jobs/templatetags/jobs_extras.py`, `ops/_ai_strip.html`, `ops/_subnav.html` or `base.html` | test: strip on the five AI pages and not elsewhere; paused and stale-runner states render their notice | 6 | claude | done 2026-11-04 |
| 5 | **Today rebuilt.** Order: failed sources, proposals, new feedback, candidates joined in the last 7 days, last run with Refresh now and the quiet-runner warning, one AI line; empty blocks left out, "Nothing needs you today." when all are; remove the pack cards and runner card from Today | `jobs/views_ops.py` (`today`), `ops/today.html` | tests: each block appears with the right data and in the right order; the all-empty message; the AI line links to the AI area; the existing "1 to decide" test passes | 6, 7 | claude | done 2026-11-04 |
| 6 | **Nothing lost, full suite.** One test follows a link to each of the 14 former pages from the new bar or Today and gets 200; run the whole suite | `tests/test_ops_nav.py` | the new test; full suite green (baseline per memory: 1,192 passed, 0 known failures: confirm the current count before starting) | 8, 9 | claude | done 2026-11-04 |
| 7 | **Real-browser check.** Start the local dev server, sign in as the operator on a SQLite copy with some data, open each of the seven areas and each second-row tab at about 1280 px and 800 px, screenshots in `evidence/`, console errors read | `evidence/` | screenshots and a "no overflow, no console error" note per page | 10 | claude | done 2026-11-04 |
| 8 | **Ship.** Owner reviews the diff and the screenshots, then commits (or tells me to, own paths only), pushes and Render deploys; owner opens `https://app.saxobeat.fr/ops/` and clicks through | none (owner's accounts) | owner opens the live Console: seven entries, each tab loads | all (live) | owner | todo |

## Order and dependencies
- 1 first: every later slice relies on the page-to-area table and the second row. 2 to 5 are independent of each other once 1 is in; the order above puts the cheapest and least risky first and the biggest change (Today) after the pieces it links to exist.
- 4 before 5: Today's AI line points at the AI area and drops the cards the strip now shows.
- 6 needs all of 1 to 5. 7 needs 6 green: no screenshots of a broken tree. 8 is the only slice that touches the hosted app, so it is last and the owner's.
- Commits: one commit for the cycle's own paths after slice 6, when the owner agrees; the working tree also holds other cycles' changes (021 to 023, `seed_employers.py`) and they are not staged.

## Rollback
- Slices 1 to 7 are working-tree edits to templates, one view and two tags, with no migration and no data change: `git restore` the cycle's paths (before commit) or `git revert` the commit (after).
- Slice 8: revert the commit and redeploy; the old bar returns because no address or data changed.

## Risks
- **Existing tests that read the nav or the Today text** (`test_roles.py`, `test_ops.py` line 42, `test_shell.py`): slice 1 and 5 update only their wording and the changes are listed in the "As run" log, never a weakened check.
- **The second-row partial changing page widths** or wrapping badly at about 800 px: caught in slice 7.
- **The status strip adds queries to five pages**: it reuses what Today already ran, so no page costs more than Today did; checked in slice 4 by counting queries on one AI page.
- **Dev data is thin**: Today's blocks and the strip need rows to show; slice 7 seeds a few (a failed run, a proposal, a feedback chat, a queued task) in the throwaway SQLite database, never in a hosted one.
- **The live site cannot be read from here**, so slice 8's check is the owner's.

## As run
*2026-11-04, after the plan was approved.*

- **Slice 1 (bar and second rows):** done. `OPS_AREAS`, `OPS_TABS`, `OPS_PAGES` and the `ops_areas` / `ops_tabs` tags are at the end of `jobs/templatetags/jobs_extras.py`; `ops/base.html` now loops over them and draws the second row (`div.opstabs`, styled in `app.css`) inside the sticky header. Differences from the plan: the second row is inline in `base.html`, not a separate `_subnav.html` partial (it is three lines); Feedback's and Sources' badges are computed in the tag. `tests/test_ops_nav.py` (19 tests) covers criteria 1, 2 and 3 and already holds slice 6's "every former page is reachable from the bar" test; the existing nav assertion in `tests/test_roles.py` (`test_the_console_has_its_own_menu...`) now lists the seven areas instead of "Jungle radar" and "Data & backups", which moved to the second rows (wording only, no check weakened).
- **Check run:** `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider tests/test_ops_nav.py tests/test_roles.py tests/test_ops.py tests/test_shell.py tests/test_auto_reject_console.py tests/test_accounts.py`: 106 passed (first run: 1 failed, a mistake in my own new reachability test (it skipped the first link), fixed in the test, not in the code).
- **Not yet seen in a browser** (slice 7).
- `source_detect` returns JSON, not a page, so it is in the page table (for any caller) but not in the page walk.

- **Slice 2 (purpose lines):** done. Six templates already had an explanatory paragraph: it became the purpose line (`class="purpose"` added); the other nine got a new one. People page heading is now "Candidates". Tests added to `tests/test_ops_nav.py`.
- **Slice 3 (Import):** done. "Recent exports" table removed from `ops/import.html`; `_runner_folder()` in `views_ops.py` feeds a "PC runner's AI folder" card (last sync, stale warning, files waiting, files held back) and a link to More, Exports.
- **Slice 4 (AI strip):** done as a simple tag (`ops_ai_strip`) that renders `ops/_ai_strip.html` and returns nothing outside the AI area; `base.html` calls it once. Query count measured: Today cost 25 (before), the queue page 24 with the strip.
- **Slice 5 (Today):** done. `today` view rewritten (one aggregate query for the AI line, new-feedback and 7-day candidate queries added, the pack summary and on-time queries dropped from Today). Joined-in-7-days excludes operator accounts.
- **Slice 6 (suite):** the first full run had 3 failures, all old tests that looked for AI facts on Today (`test_ai_running`, `test_ai_sync`, `test_ops_ai`). They were repointed to the page that holds the fact now (the AI pages, Import), same assertions otherwise. Second full run: 1499 passed.
- **Slice 7 (browser):** done, partly (see verify.md criterion 10). Login took three attempts (the field is called "E-mail" but takes the username; the first two submissions never reached the server). Found at 800 px: the right side of the bar wraps to a second row; tightened the area links' padding in `app.css` (still wraps below about 905 px, accepted). The iframe measurement I tried first was refused by the app's X-Frame-Options, so pages were measured by navigating instead. The local server and the throwaway password file were removed afterwards.

## Gate
- [x] Owner approved the slices (2026-11-04, "Approve plan")
