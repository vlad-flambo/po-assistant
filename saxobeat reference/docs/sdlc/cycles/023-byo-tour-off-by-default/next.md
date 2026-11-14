# Next: the AI "how it works" tutorial opens at most once

Each line is one action: `- [ ] [owner|claude|both] <date, optional> text`. Tick it when it is done, add new ones as the cycle moves. This file is what the cycle board shows as "what next?".

- [x] [owner] Say your request in your own words (it goes in intent.md, unedited): came through feedback #5
- [x] [claude] Gather the facts (code, docs), draft the open questions in intent.md
- [x] [owner] 2026-11-04 Answer Q1, Q2, Q3; confirm the goal and the success measure
- [x] [owner] 2026-11-04 Approve spec.md (9 criteria) and plan.md (5 slices)
- [x] [claude] 2026-11-04 Build slices 1 to 4 (Node test, the one-line change, the suite, the browser drill) and draft verify.md
- [x] [owner] 2026-11-04 Say yes to the commit: done, commit e0dd20b (only this cycle's paths; BOARD.md and the other cycles' README rows left out)
- [x] [owner] 2026-11-04 Pushed and deployed (owner's word; live ui.js read by me, contains the fix)
- [x] [owner] 2026-11-04 Phone check: the tutorial comes back on the second job page (criterion 9 fails)
- [x] [owner] 2026-11-04 Said what happened: left the tutorial alone and it came back; after one tap on ⓘ it did not
- [x] [owner] 2026-11-04 Approve the round 2 amendment (spec.md) and slices 6 to 9
- [x] [claude] 2026-11-04 Build slices 6 to 8: test red first (13/16), the change, suite 1,608 pass before and after, drill on the mobile preset
- [x] [owner] 2026-11-10 Commit round 2 (`d90a6f2`) and push: done; read by me on 2026-11-10: the live `ui.js` has the round 2 line and not the round 1 one
- [ ] [owner] **The one thing left:** on your phone open two job pages and touch nothing; tell me whether the tutorial shows on the second (criterion 9). If you cleared site data or use another browser it can show once more: that is the first visit
- [ ] [claude] On your word: record criterion 9 in verify.md, finish `learn.md` (a draft exists since 2026-11-10: update `PRD_ai_backoffice.md` about line 424, then tick the rows), tick the gates, close the cycle (README row, board)
- [ ] [claude] If it still shows on the second page: reopen the spec (what did the phone do? same browser? installed app?) and diagnose from the live script before changing code
