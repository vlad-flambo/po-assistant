# Next: invitation codes for sign-up

Each line is one action: `- [ ] [owner|claude|both] <date, optional> text`. Tick it when it is done, add new ones as the cycle moves. This file is what the cycle board shows as "what next?".

- [x] [owner] Say your request in your own words (it goes in intent.md, unedited)
- [x] [claude] Gather the facts (code, docs, files) and draft the open questions in intent.md
- [x] [owner] 2026-11-06 Answer questions 1 to 9 (all recommendations accepted, Q7 renamed "invitation code", Q8 parked)
- [x] [claude] Record each answer in intent.md the moment it is given
- [x] [owner] 2026-11-06 Confirm the goal and the three-part success measure (intent gate closed)
- [x] [claude] 2026-11-06 Write the spec (18 criteria, decisions D1 to D4)
- [x] [owner] 2026-11-06 Approve the spec, D1 to D4 included
- [x] [claude] 2026-11-06 Write the plan (10 slices, 9 local, the last one the owner's)
- [x] [owner] 2026-11-06 Approve the slices ("build until you need me")
- [x] [claude] 2026-11-06 Build slices 1 to 9 locally and write verify.md (16 pass, 1 partial, 1 pending; suite 1706 on SQLite and on Postgres)
- [ ] [owner] 2026-11-06 Read verify.md; say if 20 sign-ups an hour is too loose (one account is about 8 MB, so 160 MB an hour; room for about 40 accounts in Neon's 0.5 GB): one constant in `jobs/accounts.py`
- [x] [owner] 2026-11-06 Agree to the commit: done as 154897f (local, not pushed; README and BOARD left for the commit that holds the other cycles' edits, `seed_employers.py` left out)
- [x] [owner] 2026-11-06 Pushed and deployed; People page seen ("looks good"); `/signup/?code=Skaleet` read live by me
- [ ] [owner] Test the links: sign up through the Skaleet link with an address of yours (the screen is live), then open `/invite/` on a phone (code, link, Share button) and tell me what you see
- [x] [claude] 2026-11-10 Refreshed BOARD.md and the live board
- [x] [claude] 2026-11-10 Drafted learn.md and moved the findings: DEPLOY.md (section 6, Accounts), PRD_users_and_emails.md (outstanding list, register R6 and R7), PRD_multi_user.md (Comptes row), the house-stack gotchas; folded this cycle into docs/sdlc/HANDOFF.md for the move to a Mac
- [ ] [claude] After the owner's verdict: tick criteria 13 and 18 in verify.md, tick the last row of learn.md, set the README row to closed, refresh the board
