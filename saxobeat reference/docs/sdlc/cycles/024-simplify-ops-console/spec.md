# Spec: simplify-ops-console

| | |
|---|---|
| **Cycle** | 024 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |

## Behaviour when finished
The operator opens `/ops/` and sees a top bar of seven areas: **Today · Candidates · Sources · Runs · Feedback · AI · More**. Three of them open onto a second row of tabs:

| Area | Second row | Opens on |
|---|---|---|
| AI | Export · Import · Queue · Settings | Export |
| Sources | Sources · Jungle radar | Sources |
| More | E-mails · Exports · Auto-reject · Data & backups | E-mails |

The other four (Today, Candidates, Runs, Feedback) have no second row. Every page says in one line, under its title, what it is for. **No address changes**: each page keeps its current `/ops/...` path, so bookmarks, tests and the PC runner are untouched.

Today leads with what the owner opens daily: sources that failed, source proposals to decide, new feedback, candidates who joined in the last 7 days, then the last source run with "Refresh now". The AI work shrinks to one line ("AI: 12 waiting, 1 late") linking to the AI area. The AI pages carry a compact status strip (counts, pause, runner sync, on-time rate) so the information that used to fill Today is one click away, not gone.

## Acceptance criteria
Each one must be checkable in `verify.md`.
1. [ ] The operator's main bar (`nav.opsnav`) holds exactly seven area links, in the order above, followed by "← Candidate app" and "Log out". The 14 old entries are gone from it.
2. [ ] Each of the 14 former pages marks the right area as active; AI, Sources and More show their second row with the right tab active (Instructions highlights *Settings*; the source-detect page highlights *Sources*). A test walks every `ops_*`, `sources`, `source_detect`, `runs`, `jungle`, `people`, `data` page name.
3. [ ] No address changed: every existing `/ops/...` path still answers 200 for the operator and "not found" for a candidate (the existing role test's address list passes unmodified apart from nav wording).
4. [ ] Every console page has a non-empty one-line purpose under its heading, in a common element (`p.purpose`); the Candidates page's heading reads "Candidates" like its tab (it read "People").
5. [ ] Import no longer shows its "Recent exports" table; it links to Exports. The Exports page still lists exports and keeps "send the outstanding ones again". The runner-folder report (files waiting, files held back) moves to the Import tab, where its fix is.
6. [ ] The AI pages show a one-line status strip: pieces waiting and with an agent, late count, a pause notice when paused, the runner's last sync (with the 8-hour stale warning), the on-time rate. Today no longer shows the pack cards or the runner folder card.
7. [ ] Today shows, in this order: failed sources, proposals to decide, new feedback, candidates joined in the last 7 days, last source run with "Refresh now" (and the 8-hour quiet-runner warning), then the one AI line. A block with nothing to show is left out; if all are empty it says "Nothing needs you today." The warning badges on Feedback and Sources stay in the bar.
8. [ ] No function is lost: every action reachable from the old bar is reachable in the new one (a test follows a link to each of the 14 former pages from the new bar and Today), and no form, button or setting was removed except the Import "Recent exports" table.
9. [ ] The full test suite passes on SQLite, with the tests whose nav wording changed updated (named in `plan.md`) and new tests for criteria 1, 2, 4, 5, 6 and 7.
10. [ ] Seen in a real browser on a local server, as the operator, at desktop width and at about 800 px: each of the seven areas and each second-row tab renders without overflow, with screenshots in `evidence/`.

## Design in brief
- **One template, one helper.** `ops/base.html` renders the seven-link bar and, from a small template tag (`ops_area` in `jobs_extras`), the second row for the current page. The tag holds the one table mapping each page name to its area and tab, so the nav cannot drift from the page list. The `nav.opsnav` class stays on the main bar (the existing test finds it by that).
- **Status strip** is an inclusion tag over the existing `queue.summary()`, `queue.on_time()` and the runner report in `AiSettings`: no new queries beyond what Today already runs, shown only on AI pages.
- **Today** is rebuilt in `views_ops.today` and `ops/today.html` from facts the view already collects (failing sources, proposals, last run, runner quiet) plus two small ones: new feedback count (the nav's `new_feedback_count` already computes it) and candidates joined within 7 days (`user.date_joined`).
- **Purpose line:** one `<p class="muted purpose">` per template.
- **Rejected:**
  - Merging all AI pages into a single long page: Export alone has a form and a preview, and the tabs keep each address and test intact.
  - New addresses with redirects (`/ops/ai/...` to something else): the tabs do the grouping, so nothing needs to move and nothing can break.
  - Deleting the Jungle radar, Data & backups or Exports pages: owner's decision (Q2, Q4): fold, don't delete.

## Interfaces and data
- Templates: `jobs/templates/jobs/ops/base.html` (new bar and second row), `ops/today.html` (rebuilt), `ops/import.html` (table out, runner report in), `ops/_ai_strip.html` and `ops/_subnav.html` (new partials), a purpose line in each of the console templates (ops/*, sources, runs, jungle, data, people).
- `jobs/templatetags/jobs_extras.py`: the `ops_area` and `ops_ai_strip` tags.
- `jobs/views_ops.py`: `today` context trimmed and extended; `import_page` gains the runner report; `exports_page` unchanged.
- No model, migration, URL, setting or environment variable changes. No change to the candidate app.

## Constraints
- Operator space only; English only (stays so on purpose).
- Nothing reaches the hosted app until the owner pushes and deploys; verification is local (SQLite, `SAXOBEAT_MAIL=console`, tests per PROJECT.md). The live site cannot be read without a login, so the real `/ops/` is checked by the owner after deploy.
- The working tree holds other cycles' changes (021 to 023 and `seed_employers.py`): stage only this cycle's paths.

## Out of scope
- Trimming the stat tiles at the top of Sources (some repeat what Today and Runs show). They sit on a page the owner uses daily; say so in Verify if the owner wants them cut.
- Changing what any feature does, deleting any page or its code (decision Q4), the candidate app, translating the Console.
- Updating `docs/PRD_ai_backoffice.md` to the new layout: done in the Learn stage.

## Gate
- [x] Owner approved this spec (2026-11-04, "Approve spec")
