# Verify: the AI "how it works" tutorial opens at most once

| | |
|---|---|
| **Cycle** | 023 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence (command and output, measurement, screenshot, link) |
|---|-----------|--------|-------------------------------------------------------------|
| 1 | First visit, no flag: the tutorial is open and the flag is set at that moment | pass | Round 2, phone preset: clean storage, page 1 not touched: open, `aria-expanded="true"`, flag "1" (`evidence/browser_drill_round2.md`); Node cases 1a and 1b (1b red on round 1: `node_test_round2_before.txt`) |
| 2 | With no tap on page 1, page 2 loads it closed | pass | Failing before: Node cases 2 and 2' FAIL on the deployed round 1 code (13/16). After: 16/16 (`node_test_round2_after.txt`). Phone preset: page 2 and a return to page 1 loaded closed with no tap |
| 3 | Closing with ⓘ, and tapping a button, leave the next page closed | pass | Node cases 2c, 2d and 3 (three buttons). Round 1 browser drill (desktop) did both with real clicks; not repeated in round 2 (a tap cannot change the outcome now that opening sets the flag) |
| 4 | ⓘ opens and closes on demand; opening by hand keeps the flag | pass | Phone preset: ⓘ opens, closes, opens again; flag stays "1"; reload loads closed (via `element.click()`, not a touch gesture); Node cases 4a to 4e |
| 5 | Storage blocked: loads closed, nothing throws | pass | Node cases 5a and 5b only (a throwing localStorage); not tried in a real browser |
| 6 | The hover popover still works | partial | By diff only: round 2 changes two lines of the click and first-visit code, `app.css` has no `byo` line in its diff. Not seen on a hover device |
| 7 | The AI card and the beta line are unchanged | pass | `git diff --stat` for `_ai_card.html` and `detail.html`: empty |
| 8 | No server change; the suite passes with the same count | pass | Round 2: 1,608 passed, 0 failed before and after (`pytest_round2_before.txt`, `pytest_round2_after.txt`); this cycle's code files are `ui.js` and the Node test only. (Round 1 could not show the same count because another session changed the tree) |
| 9 | On the owner's phone, two job pages, **touching nothing**: the tutorial is not shown on the second | pending | Round 1 failed here (owner's word). Round 2 is committed (`d90a6f2`), pushed (owner's word) and **live: read by me 2026-11-10** (`/static/jobs/ui.js` has `if (!seen()) { show(true); remember(); }` and not the round 1 line). Waiting for the owner's phone check: two job pages, touch nothing. |

## Tests
- `node tests/js/byo_tour_test.js`: 16 cases. Round 2: 13/16 on the deployed round 1 code (1b, 2 and 2' fail), 16/16 after the change. It runs the real block of `ui.js` against a fake page, so it proves the logic, not the rendering.
- `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider`: round 2, 1,608 passed and 0 failed before and after.
- Browser drill, round 2: mobile preset (touch user agent, 375 px), local scratch SQLite, one test user, every step starting from no tap: criteria 1, 2 and 4. Round 1 (desktop) is in `evidence/browser_drill.md`.
- Round 1 history: criterion 9 failed on the owner's phone because only a tap marked the box seen (spec amendment, decisions.md D1).

## Not verified
- On the owner's phone after the round 2 deploy (criterion 9): pending. Round 2 is committed and live on the host (read 2026-11-10).
- A real touch gesture on ⓘ (the pane did not draw, so `element.click()` stood in), criterion 5 and 6 in a real browser.
- That the installed app takes the new script on its next load: expected from `sw.js:21` (network first for `/static/`, 60 s cache on the host, both read on 2026-11-04), to be seen on the phone.

## Verdict
- [ ] Accepted by owner
- [ ] Sent back (what, to which stage): round 1 sent back to Spec on 2026-11-04 (criterion 9 failed); round 2 built, waiting for the commit, the deploy and the owner's phone check
