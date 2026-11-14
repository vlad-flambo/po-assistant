# Spec: the AI "how it works" tutorial opens at most once

| | |
|---|---|
| **Cycle** | 023 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |

## Amendment, 2026-11-04 (round 2)
The first build marked the tutorial as seen only when ⓘ or a button was tapped. The owner's phone check failed (criterion 9): they left the box alone, moved on, and it came back on the next page; after one tap on ⓘ it did not come back again (owner's word). So "seen" must not need a tap: the moment the tutorial opens by itself counts as seen. Changed below: the behaviour, criteria 1, 2 and 9, the design, and the rejected option that is now chosen (decisions.md D1). Criteria 3 to 8 are as before. Round 1 stays in `plan.md` and `verify.md` as the record.

## Behaviour when finished
On a job page, the three-step tutorial under "Prepare with your AI" opens itself only once per browser, the first time: opening itself counts as seen. Every later job page loads with it closed, whether or not the person closed it or tapped anything. ⓘ opens and closes it on demand, on touch and on hover, as today. Nothing else on the page changes.

## Acceptance criteria
Each one must be checkable in `verify.md`.
1. [ ] In a browser with no `saxobeat.byo` flag, the first job page loads with the tutorial open (`#byo-tour` not hidden, ⓘ `aria-expanded="true"`) and the flag is set at that moment (`localStorage["saxobeat.byo"]` is `"1"`).
2. [ ] With **no tap at all** on the first page (the person just leaves it and moves on), a second job page (reload or another job) loads with the tutorial closed. Before the change it opens again: the case that failed on the owner's phone (to show failing first, on the code as deployed).
3. [ ] Closing it with ⓘ, and tapping any of the three buttons (Application answers, Cheat sheet, Follow-up), still leave the next job page closed (passes today).
4. [ ] After it was closed, tapping ⓘ opens it again and tapping again closes it, and opening it by hand does **not** clear the seen flag (a reload loads it closed).
5. [ ] With site storage blocked (localStorage throws), the tutorial loads closed, not open every time (unchanged: `seen()` returns true on error).
6. [ ] On a hover device the hover popover (`.byo-info:hover .byo-tour`) still works (`app.css:485` untouched).
7. [ ] The "During the beta…" line and the rest of the AI card are unchanged (Q3 parked): `_ai_card.html` has no diff.
8. [ ] No server change: no view, model, template string or translation changes, no extra database read; the full suite still passes with the same count (`SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider`).
9. [ ] The owner opens two job pages on their phone **without touching the tutorial** and does not see it on the second (owner's word, recorded in `verify.md`).

## Design in brief
In `jobs/static/jobs/ui.js` (the "Prepare with your AI" block), the first-visit line becomes `if (!seen()) { show(true); remember(); }`: it opens once and sets the flag at once. The ⓘ-close `remember()` added in round 1 becomes redundant and is taken out (the ⓘ handler goes back to its original form). About two lines.

Options rejected:
- **Never auto-open**: the owner chose "opens once" (Q2); the first-time user keeps the tutorial.
- ~~Set the flag as soon as it auto-opens~~ **now chosen** (decisions.md D1): rejected in round 1 because a first-time visitor who scrolls past gets no second chance; the phone check showed that requiring a tap leaves it open every time for people who never tap. ⓘ is still there to bring it back.
- **Keep round 1 (flag on ⓘ-close only)**: failed the owner's phone check.
- **A server-side "seen" flag**: a write and a migration for one box; out of scope in the intent.
- **Hide it from power mode only**: the box is the same in both modes and the feedback is about the box, not the mode.

## Interfaces and data
One static file changes: `jobs/static/jobs/ui.js`. The browser keeps the existing flag `localStorage["saxobeat.byo"]`; no new key. A cache-busting version of the static file (if the project uses one, to be verified in the plan) must change so phones pick up the new script; the service worker may cache `ui.js` (`tests/test_pwa.py:68` references it), so the plan checks how an update reaches an installed app.

## Constraints
- Phone-first UI (docs/PRD_mobile.md): the change must work on a touch device, where hover does not exist.
- No new database read or write (cycles 001 and 002 were about cutting reads).
- The service worker and any installed PWA may serve the old script until updated: verify how that update happens before calling it done.
- Deploying to Render and pushing are irreversible actions: only inside the approved plan, performed by the owner.

## Out of scope
- The "During the beta, AI is not instant…" line and the AI card (Q3, parked).
- Removing or rewording the tutorial text.
- A cross-device "seen" flag.

## Gate
- [x] Owner approved this spec (2026-11-04, round 1)
- [x] Owner approved the amendment (round 2, 2026-11-04)
