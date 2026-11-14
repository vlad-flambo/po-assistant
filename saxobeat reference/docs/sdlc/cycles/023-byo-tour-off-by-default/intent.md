# Intent: the AI "how it works" information should not be on by default

| | |
|---|---|
| **Cycle** | 023 |
| **Stage** | Spec |
| **Date** | 2026-11-04 |
| **Owner** | Vlad |
| **Born from** | Feedback #5: a problem from C-01 (vlad) |
| **Importance** | 2/5 (claude, 2026-11-04): no evidence yet beyond feedback #5 (1 user, every time, slows them down); one tutorial box on one page, power mode on phone |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
> The information i shouldn’t be always on by default on the AI section.
> It’s not very practical

## Why now / the pain
- How much did it get in your way? It slows me down
- Does it happen every time? Every time

## Goal
On the job page, the "how it works" tutorial under "Prepare with your AI" no longer opens itself every time: a person sees it open at most once, and after that it only opens when they tap ⓘ.

## Success measure
In a clean browser on a phone, power mode: (a) the first job page opens the tutorial; (b) after closing it with ⓘ, the next job page loads with it closed (today it opens again); (c) after tapping any of the three buttons, the next job page loads with it closed (as today); (d) ⓘ still opens it on demand, on touch and on hover; (e) with site storage blocked it stays closed rather than opening every time (as `seen()` does today). Checked by a browser run on the preview, and by you on your phone: the box does not come back on a second job page.

## Not doing (this cycle)
- Removing the tutorial or the AI card: only changing when the tutorial shows.
- The "During the beta, AI is not instant…" line in the AI card (Q3, parked; reopen if it is also in the way).
- A server-side "seen" flag that follows the person across devices (one box does not justify a write; a new device sees it once).

## What we already know (facts, with where they came from)
- Said by C-01 (vlad) through the feedback chat (#5) on 2026-11-04, on a job page, phone, power mode, language en. "Where did it happen? On this page."
- The job page has two things that could be "the information on the AI section" (code read 2026-11-04):
  1. **The "how it works" tutorial** under "Prepare with your AI" (`jobs/templates/jobs/detail.html:113-119`): the ⓘ button and a three-step box (①②③ plus "your data goes only where you paste it"). It is hidden in HTML but `jobs/static/jobs/ui.js:168` opens it on page load when `localStorage["saxobeat.byo"]` is not set.
  2. **The AI card** (`jobs/templates/jobs/_ai_card.html`, included at `detail.html:163`), shown when AI work is queued, late or ready: a title, a status line, and the line "During the beta, AI is not instant: you'll get it within 24 h at the latest. Check back soon." on every state.
- **Why the tutorial would show "every time"** (from the code, *not yet reproduced*): the flag is set only by `remember()`, which is called when a button is tapped (`ui.js:163`, `:201`, `:209`). Closing the box with ⓘ does not set it, so a person who reads it and closes it, or never taps a button, gets it open again on the next job page. The flag is per browser (localStorage), so a new device or cleared site data brings it back.
- The product docs say the tutorial "shows on hover / tap and the first time" (`docs/PRD_ai_backoffice.md:424`): showing it the first time was a deliberate choice (cycle A5), so it is a product decision to change, not a bug.
- No tests mention the tutorial's first-visit behaviour (`grep` of `byo` in the test folder found none: to be verified, the tests live elsewhere than `jobs/tests`).

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | Which box is "the information"? The three-step tutorial under "Prepare with your AI" (opens itself), or the grey "During the beta, AI is not instant…" line in the AI card? | The tutorial: it is the one that opens by default and covers the buttons | The ⓘ tutorial under "Prepare with your AI" (owner, 2026-11-04) | answered |
| 2 | Should the tutorial still open once, the very first time, for a new person? | Yes if the first tap or the ⓘ marks it as seen; closed from then on | Yes: opens once for a new browser; closing it with ⓘ or tapping a button counts as seen, then it stays closed (owner accepted, 2026-11-04) | answered |
| 3 | Is the beta line in the AI card in scope too (shorter, or shown once)? | No, park it unless Q1 says it is the one | Parked: out of scope this cycle (owner accepted, 2026-11-04) | parked |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- The tutorial is what lets a first-time user get an answer from their own assistant without other help (`docs/PRD_ai_backoffice.md:424`): hiding it for everyone could hurt new users. Hence Q2.
- A localStorage flag is per browser and per origin, so "seen" does not follow the person across devices; a server-side flag would cost a write and is probably not worth it for one box (not decided).

## Gate
- [x] All open questions answered or parked
- [x] Goal and success measure confirmed by the owner (2026-11-04)
