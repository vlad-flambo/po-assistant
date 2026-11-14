# Intent: remove the shortcuts explanation from the inbox

| | |
|---|---|
| **Cycle** | 017 |
| **Stage** | Intent: **dismissed 2026-10-30** (see Decision) |
| **Date** | 2026-10-30 |
| **Owner** | Vlad |
| **Born from** | Feedback #1: a problem from C-01 (vlad) |
| **Status** | Dismissed 2026-10-30 by the owner: it does not seem to affect most users |
| **Importance** | 1/5 (claude, 2026-10-30): one line on a desktop in power mode; does not affect most users |

## Decision: dismissed, 2026-10-30
The owner dismissed this intent: it does not seem to affect most users (the line shows only in power mode on a desktop, one line, already hidden on phones and touch screens). No spec, plan or build. The code is unchanged. Q1 and Q2 stay unanswered on purpose and the gate below stays unticked: nothing was confirmed. If more people say the same through the feedback chat, reopen it from this file (the facts below are still valid: one line at `inbox.html:22`, the keys are separate code).

## The request, in your words
> remove the shortcuts explanation, takes too much space and limited value

## Why now / the pain
- How much did it get in your way? It slows me down
- Does it happen every time? Every time

## Goal
(draft, to confirm) The inbox no longer spends a line of screen on explaining the keyboard shortcuts, so the first jobs sit higher on the page.

## Success measure
(draft, to confirm) The line "j/k move · s shortlist · d dismiss · o open · Enter details" is gone from the inbox in power mode on a desktop, in English and in French; the list starts one line higher; nothing else on the page moves or breaks.

## Not doing (this cycle)
- Removing the shortcuts themselves (see Q1: not yet decided).
- Touching the standard-mode inbox (it has no shortcuts and no hint already).
- Redesigning the inbox's other controls (the bookmarklet, "clear the noise"): not asked.

## What we already know (facts, with where they came from)
- Said by C-01 (vlad) through the feedback chat (#1) on 2026-10-30, on Inbox, desktop, power mode, language en.
- Where did it happen? On this page
- The explanation is one line, `<p class="small muted kbd-hint">`, at `jobs/templates/jobs/inbox.html:22`, between the filter bar and the bookmarklet (read in the repo, 2026-10-30).
- It is already hidden on phones and touch screens by `.kbd-hint` in `jobs/static/jobs/app.css:201`; so only a desktop shows it (read in the repo).
- The keys themselves are a separate piece of code, a `keydown` handler in the same template from line 51 (j, k, s, d, o, Enter); removing the line does not touch it (read in the repo).
- The standard-mode inbox has no hint and no shortcuts (`inbox_standard.html:2`).
- One test asserts the line is there: `tests/test_shell.py:107` (`kbd-hint`); it would change with the line.
- The labels live in the French catalogue (`locale/fr/LC_MESSAGES/django.po`: "move", "shortlist", ...); some words ("dismiss", "open", "details") are probably shared with other pages, so they stay (to be verified when building).
- Docs that name the line: `docs/PRD_mobile.md` (lines 162 and 292: "shown only with a keyboard"), `docs/PRD_users_and_emails.md` line 32, `docs/PRD.md` line 178 (the keys, not the line). They would need a note in Learn.

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Remove only the explanation line and keep the keys working (j/k/s/d/o/Enter)? | Yes: keep the keys. You asked for the explanation to go, the keys cost no space, and you may already use them. If you want the keys gone too, say so. | | open |
| Q2 | Should the shortcuts be findable anywhere else (e.g. a small "?" or a line on the Settings page)? | No: not this cycle. You said the value is limited; add it back only if someone asks. | | open |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Desktop must not regress otherwise (PRD_mobile.md criterion 8 and 9 say the keyboard flow stays; they name the keys, not the explanation line).
- Small, one template line, one test line, docs notes: no spec stage worth a long document; keep the later stages short.
- No data change, no deploy risk beyond a normal push (a push is for the owner to ask for).

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
