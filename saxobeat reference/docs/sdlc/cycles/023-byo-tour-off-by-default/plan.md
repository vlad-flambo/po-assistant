# Plan: the AI "how it works" tutorial opens at most once

| | |
|---|---|
| **Cycle** | 023 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

## Slices
Thin, ordered, each verifiable alone. Each slice names the acceptance criteria it moves. Slices 1 to 4 change nothing in production; the only outward step is 5, and it is the owner's.

| # | Who | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-----|-------|---------------|------------------------------------|----------|--------|
| 1 | claude | A Node test in the style of `tests/js/sw_test.js`: it runs the "Prepare with your AI" block of `ui.js` against a fake DOM and a fake `localStorage` (and one that throws), and checks each behaviour | `tests/js/byo_tour_test.js` (new) | `node tests/js/byo_tour_test.js` on the **unchanged** `ui.js`: every case passes except the one for criterion 2 (closing with ⓘ then loading again opens it). That red result is saved in `evidence/` | 1-6 (as a test) | done 2026-11-04 |
| 2 | claude | The change: when ⓘ closes the open tutorial, call `remember()`; opening by hand does not | `jobs/static/jobs/ui.js` (about 2 lines, block at 157-168) | The Node test is green. `git diff --stat` for the cycle shows only `ui.js` and the new test | 2, 3, 4, 5 | done 2026-11-04 |
| 3 | claude | The full suite on SQLite, to prove nothing else moved | none | `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider`: same pass count as before the change (the count before is taken first, on a clean checkout of the working tree, and saved in `evidence/`) | 7, 8 | done 2026-11-04 (no failure; count not comparable, see log) |
| 4 | claude | A real-browser drill in the in-app preview on the local SQLite copy (never Neon: `.env` has an empty `DATABASE_URL`): clean storage, job page, close ⓘ, second job page; then a button tap on a clean storage; then storage blocked | none | Screenshots and the `localStorage` value in `evidence/`; criteria 1 to 6 each ticked from what the page showed. If there is no local login or job to open, say so in verify.md and fall back to the Node test plus a Django test client render of the page | 1-6 | done 2026-11-04 (desktop viewport) |
| 5 | owner | Commit (agent, on the owner's yes), then push and the Render deploy (owner). Then on the phone: open two job pages, close the tutorial on the first, check it does not come back on the second | none | The owner says what the phone showed; recorded as "owner's word" in verify.md | 9 | todo |

### Round 2 (2026-11-04, after the failed phone check; needs the owner's approval with the amended spec)
| # | Who | Slice | Files touched | Check | Criteria | Status |
|---|-----|-------|---------------|-------|----------|--------|
| 6 | claude | In the Node test, change the first-visit case to also expect the flag set, and add the missed case: no tap on page 1, page 2 must load closed | `tests/js/byo_tour_test.js` | Run on the **code as committed in round 1** (e0dd20b): the new "no tap" case fails and nothing else does; output saved as `evidence/node_test_round2_before.txt` | 1, 2 | done 2026-11-04 (red: 13/16, only 1b, 2 and 2' fail on the round 1 code) |
| 7 | claude | The change: `if (!seen()) { show(true); remember(); }`; take out the ⓘ-close `remember()` of round 1 | `jobs/static/jobs/ui.js` | Node test green; `git diff` for the file is about 2 lines | 1-5 | done 2026-11-04 |
| 8 | claude | Suite on SQLite (a before count taken first, in the same tree) and a real-browser drill with the **mobile preset** (touch, 375 px): clean storage, page 1 untouched, page 2 closed; ⓘ opens it by hand; a button tap still works | none | Counts and the drill's reads in `evidence/` | 1-8 | done 2026-11-04 |
| 9 | owner | Commit (agent), push and deploy (owner), then the phone: open two job pages and touch nothing | none | The owner's word on whether the tutorial shows on the second page | 9 | todo |

Order and rollback as in round 1 (`git revert` of the round 2 commit, then redeploy). The risk that matters this time: a drill with a tap hid the gap in round 1, so every check of round 2 starts from "no tap".

## Order and dependencies
Test first (slice 1) so the failing case is on record before the fix. Slice 2 is the whole change. Slices 3 and 4 are read-only checks and can run in either order. Slice 5 needs 2 to 4 done and the owner's yes to commit; pushing and deploying are irreversible and stay with the owner.

## Rollback
Slices 1 to 4: revert `ui.js` (`git checkout -- jobs/static/jobs/ui.js`) and delete the test file; nothing else was touched. Slice 5: revert the commit and redeploy; because `sw.js` fetches `/static/` network-first (checked 2026-11-04, `sw.js:21`), phones get the old script on their next load, and the flag a browser already stored (`saxobeat.byo`) is harmless in both versions.

## Risks
- The service worker and the browser's own cache could serve the old `ui.js` for a short while. Checked: the worker is network-first for `/static/`, and WhiteNoise's default cache lifetime is short (to be confirmed in slice 5 on the phone). No cache-busting edit is planned.
- The Node test runs `ui.js` against a fake DOM, so it proves the logic, not the rendering: that is why slice 4 (a real browser) and slice 5 (the real phone) exist.
- `ui.js` holds other blocks in the same file; slice 2 must leave them untouched (the diff check in slice 2).
- The working tree holds other cycles' changes (BOARD.md, README.md, `seed_employers.py`, cycles 021 and 022): commit only this cycle's paths.

## Gate
- [x] Owner approved the slices (2026-11-04, round 1)
- [x] Owner approved the round 2 slices (2026-11-04)

## As run
- 2026-11-04 Plan approved by the owner. `ui.js` had no diff at the start; `jobs/static/jobs/app.css` showed as modified by something else (not this cycle's: not touched, not committed here).
- 2026-11-04 Slice 1: wrote `tests/js/byo_tour_test.js` (13 cases, runs the block between the "Prepare with your AI" and "The feedback chat" comments of `ui.js` against a fake page and a fake localStorage, also one that throws). On the **unchanged** `ui.js`: 12 of 13 pass, only 2b fails ("close with ⓘ, then the next page loads it closed"), as planned. Output in `evidence/node_test_before.txt`. Baseline `pytest` started in the background before the edit; `ui.js` is not edited until it finishes.
- 2026-11-04 Baseline: `pytest` on SQLite before the edit: **1,461 passed, 1 failed** (`tests/test_ops_nav.py::test_every_former_page_is_one_or_two_clicks_from_the_bar`, `evidence/pytest_before.txt`). That file is untracked and the ops templates are modified in the tree: another session's work in progress, not this cycle's.
- 2026-11-04 Slice 2: one line changed in `jobs/static/jobs/ui.js` (`if (!tour.hidden) remember();` added to the ⓘ click handler). `git diff --stat` for the file: 1 insertion, 1 deletion. Node test after: 13 of 13 pass (`evidence/node_test_after.txt`).
- 2026-11-04 Slice 3: `pytest` after the edit: **1,479 passed, 0 failed** (`evidence/pytest_after.txt`). The count is not the same as before (1,462 collected then, 1,479 now): the tree changed between the runs under another session (`tests/test_ops_nav.py` and `tests/test_roles.py` among them), so "same count" could not be shown; no failure remains, and the tests that read `ui.js` (`test_pwa.py`, `test_shell.py`) pass.
- 2026-11-04 Slice 4: first try at the scratch database failed (`IntegrityError: jobs_job.canonical_key` unique, so a first drill job was made with an empty key and left behind, harmless in the scratch file). The preview needed a scratch wrapper outside the repo and a temporary `.claude/launch.json` entry; both removed (`git checkout -- .claude/launch.json`, file clean). Drill result in `evidence/browser_drill.md`: criteria 1, 2, 3, 4 seen in a real browser (desktop viewport).
- 2026-11-04 Checks by diff: `_ai_card.html` and `detail.html` have no diff (criterion 7); no `byo` line in the (other session's) `app.css` diff (criterion 6, hover rule untouched).
- 2026-11-04 Phone check after the deploy (owner's word): the tutorial came back on the second page when they just left it on the first; after one tap on ⓘ it did not come back. Round 1 had the tap path only; cause and amended spec in `spec.md` and `decisions.md` D1. Lesson for the playbook: the drill and the Node test both started from a tap, so they could not show the person who never taps.
- 2026-11-04 Round 2, slice 6: the Node test now also expects the flag set on first open (1b) and has the no-tap case (2, 2'). On the round 1 code (e0dd20b, as deployed): 13/16 pass, exactly 1b, 2 and 2' fail (`evidence/node_test_round2_before.txt`). Baseline suite taken first: 1,608 passed, 0 failed (`pytest_round2_before.txt`).
- 2026-11-04 Round 2, slice 7: `ui.js` now has `if (!seen()) { show(true); remember(); }` and the ⓘ handler is back to `show(tour.hidden)`. Node test 16/16 (`node_test_round2_after.txt`).
- 2026-11-04 Round 2, slice 8: suite after: 1,608 passed, 0 failed, the same count as before (`pytest_round2_after.txt`). Drill on the mobile preset (touch user agent, 375 px), starting from no tap: page 1 open with the flag set, page 2 and a return to page 1 closed, ⓘ opens and closes on demand, a reload after opening by hand loads closed (`evidence/browser_drill_round2.md`). Hiccup: a pointer click on ⓘ failed twice (the pane did not draw: screenshot timeout), so the ⓘ steps used `element.click()` from the page; said in the evidence. `.claude/launch.json` restored, scratch server stopped, viewport back to desktop.
