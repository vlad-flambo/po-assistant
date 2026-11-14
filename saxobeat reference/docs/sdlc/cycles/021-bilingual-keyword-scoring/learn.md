# Learn: bilingual keyword scoring

| | |
|---|---|
| **Cycle** | 021 |
| **Stage** | Learn (2026-11-04) |

## What happened vs what we expected
**Success measure (intent):** (1) French and English postings of the same role within about 10 points on the replay; (2) job 33238 above the floor of 35; no harm to English postings or to the AI-reviewed good fits.

| Measure | Before | After |
|---|---|---|
| Same-role gap French/English, mean absolute (C-01, 15 roles) | 10.6 | **3.2** |
| Whole-pool gap French/English (C-01, deterministic mean) | 14.2 | 6.2 |
| French postings at or above the floor (C-01 replay) | 10.9 % | 38.2 % (English 65.9 % to 67.7 %) |
| Job 33238 | 33 on the host | **49.8** on the replay, **43.7** on the host data (stored score stays 33 because the job is in the pipeline, not the inbox) |
| English mean, protected jobs under the floor | - | +0.6 and +1.4; none of 117 |
| Candidate 1's host inbox | stored scores older than the keyword list for part of it | rescored: 2,980 jobs; 624 rise above the floor, 11 fall (not the glossary's) |
| Neon cost (owner's reading 2026-11-05) | 0.31 GB at 10:17 on 4 Nov | 0.49 GB network transfer this month (cap 5 GB), compute 3.11 CU-hrs, storage 0.55 GB; my reads about 40 MB of posting text of that |

The outcome matches the measure. It was reached with the glossary and the language-aware similarity; the word-set matching fallback of the spec was not needed.

## What we learned
- **The owner's hypothesis was right, and it was two causes, not one.** The keyword half missed French words, and the similarity half is scaled on a profile in the postings' language: French postings had a mean similarity of 11.7 against 34.9 for English ones. Fixing only the keywords would have closed half the gap.
- **The language that needs a boost is the one the profile is not written in, not "French".** A French-CV test candidate showed French postings over-scored by the first design; the rule became symmetric (decisions D5). Anything calibrated on one candidate's language must be checked on the other direction.
- **The 33 was real, not stale.** The harness reproduced it from the posting text (32.7 against 33). But the same harness showed **stored scores lag keyword edits**: editing keywords does not bump `profile_version` and the background rescore did not reach the whole inbox (1,653 of 8,849 stored scores carried the current version for C-01).
- **A rescore covers the inbox only** (status new, not hidden). A job moved into the pipeline keeps the score it had; that is why 33238 still reads 33 on the host.
- **Mentions are not roles.** An equivalent such as "VP product" or "directeur des opérations" in a posting's body raises a weight-4 keyword even when the posting only names that person. The literal keywords already did this; the glossary adds more ways to reach it. "COO" was removed from a concept after the first replay for the same reason.
- **A threshold met at exactly the limit is not met.** The first cost run gave 1.50 against a limit of 1.5; caching two lookups brought it to 1.24.
- **Running a hosted command needs the database named on its first line.** The first hosted preview ran against the local Docker database (the address was not set for that process) and failed harmlessly; the commands now print which database they read.
- **Scripted edits need a check.** A patch script wrote a NUL byte into `scoring.py` and dropped CRLF endings on a few files; `file`, `ast.parse` and `git diff --stat` caught both.

## What moves where
| Finding | Goes to | Done |
|---|---|---|
| Scoring now bridges English and French: glossary, equivalents, language-aware similarity, the switch `SAXOBEAT_GLOSSARY` | `docs/PRD.md` (scoring section) | [x] |
| New commands `rescore_preview`, `rescore`; how to rescore after a scoring change; the switch | `docs/DEPLOY.md` | [x] |
| Cycle state, the host actions taken, what is left (candidates 3 and 4 not rescored, constant 0.032 calibrated on one candidate) | project memory `project-sdlc-cycles` | [x] |
| The cycle's row | `docs/sdlc/README.md` | [x] |
| Scores shift for every candidate: the calibration bands (cycle 008) may need a new reading | cycle 008's intent (a fact line) | [x] |
| Stored scores lag keyword edits; a rescore covers the inbox only | a new cycle candidate (below) | [x] deferred: offered as a new cycle, to start when the owner asks, 2026-11-05 |
| The other-language scale 0.032 needs a check on a French-profile candidate with a good keyword list | here, and in `decisions.md` D4/D5; to revisit when such data exists | [x] |
| "State which database a hosted command reads on its first line" | project memory (a rule for hosted commands) | [x] |

## Process feedback
- The playbook worked well for a measured claim: baseline first, a harness that reproduces the number the owner saw, then thresholds fixed in the spec. The decision point after slice 6 would have caught a failure early; it did not trigger.
- The spec had to be reworded twice during the build (criterion 5, criteria 9 and 10) because a test on a second candidate showed the first wording was too narrow. Spec criteria that name a language ("French") deserve a second look for symmetry.
- The plan said the owner's runbook steps were the owner's; at slice 11 the owner asked me to run them. A plan could say "owner, or Claude at the owner's explicit word" for read-only hosted steps.
- Long replays (5 to 10 minutes) were run in the background with notifications; the machine is shared, so timing criteria need a ratio and an "alone" run, not an absolute number.

## Next cycle candidates
- **Keyword edits and the rescore:** make a keyword or profile edit rescore the whole inbox reliably and say when it finished; today stored scores can lag the keyword list (found in this cycle, outside its scope). Importance candidate 3/5.
- **Calibrate the other-language scale with more candidates** when a French-profile candidate with real keywords exists.
- **Rescore candidates 3 and 4** (about 100 MB of reads) if they become real users; or make the rescore cheaper (read only the postings whose score could change).
- **Mentions are not roles:** score a keyword found only in the body after a "report to / reports to / sous la responsabilité de" lead-in lower, or not at all (the false positives seen in the examples).
