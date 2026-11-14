# Next: cycle 020

Each line is one action: `- [ ] [owner|claude|both] <date, optional> text`. Tick it when it is done, add new ones as the cycle moves. This file is what the cycle board shows as "what next?".

- [x] [claude] 2026-11-03 Check the link, the open API and Revolut's own site (done: evidence/revolut_people_probe_2026-11-03.md)
- [x] [owner] 2026-11-03 Answer Q1 in intent.md (answered: build it)
- [x] [owner] 2026-11-03 Read spec.md and plan.md and approve them (approved)
- [x] [claude] 2026-11-03 Slices 1-7 (done; robots.txt found to forbid the API; the adapter refused)
- [x] [owner] 2026-11-03 Decide on robots.txt (decided: override, per source; decisions.md D1)
- [x] [claude] 2026-11-03 Per-source `ignore_robots`, Worklife seeded with it (off), live read repeated on a scratch copy (4 jobs, then 0 new), suite 1,434 pass
- [x] [owner] 2026-11-03 Answer Q2: Revolut's own jobs stay on the bookmarklet route (answered: yes)
- [x] [owner] 2026-11-03 Read verify.md and accept it (accepted)
- [x] [owner] 2026-11-03 Confirm the goal and success measure in intent.md (confirmed)
- [x] [owner] 2026-11-03 Terms of use of revolutpeople.com read; the apply link opens fine (owner's word)
- [x] [claude] 2026-11-03 Worklife added to the hosted seed script (`seed_hosted_sources.ps1 -Step 3`), suite 1,434 pass, committed and pushed
- [x] [claude] 2026-11-03 Commit my paths and write learn.md (done)
- [x] [both] 2026-11-04 (done: the owner ran the hosted seed on prod, "seems to work", owner's word; I have not read the hosted row back) After Render has deployed the push: dry run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\seed_hosted_sources.ps1 -Step 3`, then (after a Neon snapshot of prod1) the same with `-Apply -SnapshotTaken`: expect `1 sources added`, then `0`
- [ ] [owner] Then enable Worklife on the Sources page after a by-hand runner pass (5 requests, 4 jobs)
- [x] [owner] 2026-11-04 Worklife enabled and the first by-hand pass stored its 4 jobs (owner's word: "Yes, 4 jobs"); cycle closed
