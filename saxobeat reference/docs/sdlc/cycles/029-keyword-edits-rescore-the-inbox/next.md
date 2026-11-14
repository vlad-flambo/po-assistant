# Next: keyword edits rescore the inbox

Each line is one action: `- [ ] [owner|claude|both] <date, optional> text`. Tick it when it is done, add new ones as the cycle moves. This file is what the cycle board shows as "what next?".

- [x] [claude] 2026-11-05 Gather the facts (code, tests, PRDs, 29 Oct dump on a scratch copy), draft intent.md
- [x] [owner] 2026-11-05 Question 1 answered: keep the button (no automatic rescore after a save); goal, success measure and questions 2-7 reworded around it
- [x] [owner] 2026-11-05 Question 2 answered: yes, the inbox shows a line "your scores are older than your settings" with the button
- [x] [owner] 2026-11-05 Questions 3 to 7 accepted as recommended (background button, pipeline jobs, rescore_pending for restarts, hash on each score, power mode only)
- [ ] [owner] 2026-11-05 Say the request in your own words (replaces the relayed 021 finding in intent.md)
- [x] [owner] 2026-11-06 Goal and success measure confirmed; Intent gate closed
- [x] [claude] 2026-11-05 Dropped the scratch database `scratch029` (restore the 29 Oct dump again for the spec drill)
- [x] [claude] 2026-11-06 Drafted spec.md (18 acceptance criteria, decisions D1 to D4 to confirm)
- [x] [owner] 2026-11-06 Spec approved, D1 to D4 as drafted
- [x] [claude] 2026-11-06 Drafted plan.md (12 slices; D2 confirmed by reading dream.refresh)
- [x] [owner] 2026-11-06 Plan approved (12 slices; 11 and 12 are the owner's)
- [ ] [claude] Build slice 1 (the hash, `scoring.inputs_hash`): next action, nothing built yet; read "Resume here" at the end of plan.md first (migration number is now 0045; the dump and `.env` do not travel to another computer)
- [ ] [owner] Copy `data/backups/saxobeat_2026-10-29_100546.dump` to the new computer (gitignored, needed for slices 2 and 9), or say to take a fresh backup
