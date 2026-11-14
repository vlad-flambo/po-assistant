# Next: bilingual keyword scoring

Each line is one action: `- [ ] [owner|claude|both] <date, optional> text`. Tick it when it is done, add new ones as the cycle moves. This file is what the cycle board shows as "what next?".

- [x] [owner] 2026-11-04 Said the request in your own words (it is in intent.md, from feedback #4)
- [x] [claude] 2026-11-04 Gathered the facts from the code and drafted the open questions Q1 to Q5
- [x] [owner] 2026-11-04 Q1: gave the job (Change Manager IA H/F, eXalt, job 33238); [claude] read its score page on the host (33 = keywords 37, similarity 15, 0 of 37 key words)
- [x] [owner] 2026-11-04 Q2: "Yes, local only"
- [x] [claude] 2026-11-04 Replayed the stored scores by language on a scratch copy of the 29 Oct dump (dropped after): `evidence/replay_by_language.md`
- [x] [owner] 2026-11-04 Q3 to Q6: accepted my recommendations
- [x] [owner] 2026-11-04 Confirmed the goal and the success measure ("Confirm, go to spec")
- [x] [claude] 2026-11-04 Drafted spec.md (18 criteria) and saved the 33238 text in evidence/job_33238.md
- [x] [owner] 2026-11-04 Approved the spec ("Approve spec")
- [x] [claude] 2026-11-04 Drafted plan.md (12 slices, no migration, decision point after slice 6)
- [x] [owner] 2026-11-04 Approved the plan ("Approve plan")
- [x] [claude] 2026-11-04 Slice 1 done: replay harness and baseline (`evidence/baseline.md`); 33238 replays at 32.7 (host page: 33); the scratch database `replay021` is kept for slices 2 to 9
- [x] [claude] 2026-11-04 Slices 2 to 9 built and checked (job 33238 replays at 49.8; same-role gap 10.6 to 3.2; 1,552 tests pass on SQLite and Postgres; nothing committed): `evidence/slice6_summary.md`, `cost.md`, decisions D1 to D5
- [x] [owner] 2026-11-04 Slice 3: read the glossary and the crossing examples: "Looks fine" (no line to change)
- [x] [owner] 2026-11-04 "Commit my paths"; [claude] committed as 81f6e6d (build, docs, evidence) and 1e98d31 (an unused filter another cycle's commit had picked up), through a temporary index so other sessions' staged work was left alone; not pushed
- [x] [owner] 2026-11-04 Slice 10: "Pushed"; [claude] checked `origin/main` has 4ec24c8 and the job page of 33238 opens (still 33: no rescore yet)
- [x] [owner] 2026-11-04 Slice 11, first part: Neon snapshot done; "do the run yourself against the hosted address"; [claude] ran `rescore_preview --limit 200` on the host (read only, 2.6 MB of posting text, `evidence/hosted_preview_limit200.txt`)
- [x] [owner] 2026-11-04 Slice 11: "Yes, candidate 1 only"; [claude] ran the full preview (16.6 MB read) and the rescore of candidate 1 (2,980 jobs), checked afterwards (`verify.md`)
- [x] [claude] 2026-11-04 `verify.md` drafted (16 pass, 2 partial)
- [x] [owner] 2026-11-04 Verdict on `verify.md`: "Accept"; Neon reading 2026-11-05: 0.49 GB network transfer, 3.11 CU-hrs, 0.55 GB storage (fine)
- [ ] [owner] Optional: look at Render's Events for the 502 seen at about 18:16 to 18:19 on 2026-11-04 after the rescore (cause unknown)
- [x] [owner] 2026-11-04 Candidates 3 and 4 left unrescored for now (listed under "Not verified", which the owner accepted)
- [x] [claude] 2026-11-05 `learn.md` written; PRD.md, DEPLOY.md, cycle 008's intent and project memory updated; cycle closed (the push of the docs commits is the owner's)
