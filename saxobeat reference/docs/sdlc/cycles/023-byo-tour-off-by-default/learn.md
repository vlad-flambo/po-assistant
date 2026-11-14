# Learn: the AI "how it works" tutorial opens at most once

| | |
|---|---|
| **Cycle** | 023 |
| **Stage** | Verify (a draft of the learn lessons, written 2026-11-10 before the owner's phone check; nothing below is ticked) |

## What happened vs what we expected
- Expected (intent.md): the ⓘ tutorial under "Prepare with your AI" opens at most once per browser, then only when ⓘ is tapped.
- Round 1 (`e0dd20b`, deployed 2026-11-04) marked it seen only when ⓘ or a button was tapped. The owner's phone check **failed**: left alone, it came back on every job page; after one tap on ⓘ it did not (owner's word).
- Round 2 (`d90a6f2`, pushed by the owner and **live on the host, read 2026-11-10**): opening by itself counts as seen. Node test 13/16 red on the round 1 code then 16/16; suite 1,608 pass before and after; a drill on the mobile preset starting from no tap passes. Verify: 7 pass, 1 partial (hover popover, by diff only), 1 pending.
- **Not yet measured:** the success measure's last line, the owner's phone with two job pages and no touch (criterion 9). Until the owner says so, this cycle is not closed.

## What we learned
- A first-visit tutorial that needs a tap to count as seen is shown again to everyone who never taps, and on a phone that is most people: the popover covers the page and the ⓘ is small.
- Both my checks in round 1 (the Node test and the browser drill) began from a tap, so they could not show the person who does nothing. The owner's real phone found it in one try.
- The service worker was not the cause: `/static/` is network first (`sw.js:21`) and the host caches `ui.js` for 60 s (`Cache-Control: max-age=60`), both read on 2026-11-04.
- "Deployed" was said before the code was on the host: on 2026-11-04 `origin/main` lacked the round 2 commit. A plain GET of the public static file (`/static/jobs/ui.js`) shows in seconds whether a front-end fix is live; do it before asking the owner to test on a phone.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| The tutorial now opens once per browser, and opening counts as seen (ⓘ opens it on demand) | `docs/PRD_ai_backoffice.md` line about "the tutorial shows on hover / tap and the first time" (about line 424) | [ ] |
| Verify a first-visit or "shown once" behaviour from the passive path first (no tap), on the real device or its preset | the ai-sdlc skill, Verify stage (one line), owner's decision | [ ] |
| Check a front-end deploy by reading the live static file before the phone test | `docs/DEPLOY.md` (one line) | [ ] |

## Process feedback
- What worked: writing the failing case first (the Node test red on the deployed code) made round 2 small and certain; the amended spec kept round 1 as a record instead of rewriting it.
- What slowed us: round 1's acceptance criteria said "closes it with ⓘ", which encoded the tap I assumed; the owner's intent ("not on by default") was about the person who does nothing. Test the intent's person, not the implementation's path.
- Nine sessions shared one working tree on 2026-11-10; committing only this cycle's paths (README staged as HEAD plus one row) kept the history clean but cost extra steps each time.

## Next cycle candidates
- The "During the beta, AI is not instant…" line in the AI card (parked as Q3 in intent.md): reopen if it is also in the way.
