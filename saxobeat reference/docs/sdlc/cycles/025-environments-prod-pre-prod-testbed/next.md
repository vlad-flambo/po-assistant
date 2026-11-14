# Next: Environments: prod, pre-prod, testbed

Each line is one action: `- [ ] [owner|claude|both] <date, optional> text`. Tick it when it is done, add new ones as the cycle moves. This file is what the cycle board shows as "what next?".

- [x] [owner] Say your request in your own words (it goes in intent.md, unedited)
- [x] [claude] Gather the facts and draft the open questions in intent.md
- [x] [owner] Answer question 1: full copy for now (2026-11-05), reconsider as the user base grows
- [x] [owner] Answer question 7: neutralise friends' e-mails and password hashes in the copies (2026-11-05)
- [x] [owner] Answer questions 2 to 6: all five accepted as recommended (2026-11-06)
- [x] [owner] Confirm the goal and success measure (2026-11-10, "draft confirmed")
- [x] [claude] 2026-11-10 Drafted spec.md (20 acceptance criteria, decisions D1 to D5 to confirm)
- [ ] [owner] Read spec.md and approve it, or say what to change (D4: the two small app changes, banner and mail guard, are the one point the intent did not cover)
- [ ] [claude] After the spec is approved: write plan.md (slices; the owner's account steps listed one by one; the one switch of prod's branch is a single, rollback-able edit)
