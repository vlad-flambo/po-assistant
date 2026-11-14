# Next: cycle 019

Each line is one action: `- [ ] [owner|claude|both] <date, optional> text`. Tick it when it is done, add new ones as the cycle moves. This file is what the cycle board shows as "what next?".

- [x] [owner] 2026-11-03 Answer the six intent questions (Q2 changed to a global console value)
- [x] [owner] 2026-11-03 Confirm the goal and success measure
- [x] [owner] 2026-11-03 Approve the spec (18 criteria, 7-day banner)
- [x] [owner] 2026-11-03 Approve the plan (11 slices)
- [x] [claude] 2026-11-03 Slices 1-8: count, data model, sweep, console, candidate view, Insights, Postgres rehearsal, runner step (all local, not committed)
- [x] [owner] 2026-11-03 "commit it": committed as a1b74a1 (not pushed)
- [x] [owner] 2026-11-03 Slice 9 done (pushed, Render updated, page loads; steps were in `evidence/slice9_10_runbook.md`): take a Neon snapshot of prod1, then push (the migration 0043 reaches the host); check Render shows Live on the new commit and the migration applied. Do NOT run `pc_runner.ps1` or any command against the hosted database from the new tree before that
- [x] [owner] 2026-11-04 Slice 10: first sweep run; the live banner says 18 moved (the dump predicts 17 on 3 Nov and 18 on 4 Nov); no counts files, noted as a caveat in `evidence/hosted_first_sweep.md`
- [x] [claude] 2026-11-04 `verify.md` drafted from the local evidence and the owner's first sweep (18 criteria; 13 of them look-at-the-host items are marked)
- [x] [claude] 2026-11-04 Slice 11, read-only part, on the host with the owner signed in: 18 tags on the Rejected cards, box and history line on a job page, Insights 18, console page loads (recorded in `verify.md`)
- [x] [claude] 2026-11-04 Slice 11, with the owner's yes: pressed "Put back to Applied" on 360learning (banner 18 → 17, no re-sweep) and saved the delay 31 then 30 in the console
- [x] [owner] 2026-11-04 Read the French wording (from the catalogue) and gave the verdict: Accepted by owner
- [x] [claude] 2026-11-04 `learn.md` written; PRD F5 and project memory updated; cycle closed (the push of the doc commits is the owner's)
