# Learn: simplify-ops-console

| | |
|---|---|
| **Cycle** | 024 |
| **Stage** | Learn |

## What happened vs what we expected
The success measure (intent Q5) was: at most 7 top entries, a one-line purpose on every page, no old address answering "not found", tests pass. Result: the bar went from 14 entries to 7 areas, every one of the 15 console pages has a purpose line, no address changed (so nothing needed a redirect), and the suite passes (1,499). Verify: 9 criteria passed and criterion 10 (real browser) was partial; the owner accepted the verdict on 2026-11-04 with that gap known. The live `/ops/` was never seen by me (login), the owner's look is the live check.

## What we learned
- "Fold, don't delete" was cheaper than expected: a single page-to-area table in `jobs_extras.py` drives the bar, the tabs and the AI strip, so a new console page needs one line there (and a purpose line), not a template change.
- Moving facts between pages breaks old tests on purpose: three tests looked for AI facts on Today. They were repointed to the page the fact moved to, assertions kept. A cycle that moves facts should list those tests in the plan.
- The bar needs about 905 px on one row; at 800 px its right side ("← Candidate app", "Log out") wraps. Accepted; the Console is desktop-first.
- The page that said the most (Today) was the one doing the most unrelated jobs; splitting it by "what needs me today" vs "what the AI back office is doing" is what made the rest simple.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| The new bar, tabs, purpose lines, AI strip and the new Today | `docs/PRD_ai_backoffice.md` §9 (layout note and the Today row) | [x] |
| The runner-folder report is on AI → Import, not Today | `docs/DEPLOY.md` (the runner section) | [x] |
| Cycle 024 built, accepted, committed `4d29c37` (not pushed) | `docs/sdlc/README.md` row 024, memory note `project-ops-console-cycle-024` | [x] |
| Adding a console page: one line in `OPS_PAGES` and a `p.purpose` | memory note (how to apply) | [x] |

## Process feedback
- The three owner gates (intent, spec, plan) were quick because each stage opened with a concrete shape to answer yes or no to; the "propose a bar, then ask" pattern worked better than open questions.
- Checking a page in the browser at one width only (800 px) left criterion 10 partial. A plan with a UI change should name the widths and the number of pages to screenshot up front.
- The README table is edited by several sessions; staging only one's own row needs plumbing (`git update-index --cacheinfo`). A per-cycle status file would avoid that.

## Next cycle candidates
- Tighten the bar below 905 px (shorter labels or moving "← Candidate app" and "Log out" into More), if the owner works on a narrow window.
- The Export page's candidate table clips at 800 px (predates this cycle).
- The Sources stat tiles (left as they are).
- The repeated browser-console message "An unknown error occurred when fetching the script": not traced, probably the pane's tooling.
