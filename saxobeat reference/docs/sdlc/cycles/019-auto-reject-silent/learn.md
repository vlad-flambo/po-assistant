# Learn: presume an application rejected after a month of silence

| | |
|---|---|
| **Cycle** | 019 |
| **Stage** | Learn done 2026-11-04: cycle closed (the push of the doc commits is the owner's) |
| **Verify** | [verify.md](verify.md), accepted by the owner 2026-11-04 |

## What happened vs what we expected
Success measure (intent), one line at a time:
- **A silent Applied job is Rejected by the app, once, with a history line.** Met: tests on SQLite and Postgres, a rehearsal on a copy of the data, and on the host a first sweep that moved **18** applications (banner), each with the line "no answer after 30 days (automatic)" (read on one job).
- **Tag and explanation on the job page and the card, EN and FR.** Met: seen on the host in English (18 tagged cards, the box, the button); French read from the catalogue by the owner, not looked at on the host.
- **Jobs that are not silent are never touched; a put-back is not re-rejected.** Met in tests (four race tests, mutation-checked); on the host the put-back of one job was not swept again (console: 0 waiting).
- **One value in the console, default 30, 0 = off.** Met: saved 31 then 30 on the host.
- **Insights keep them apart.** Met: "No answer, presumed rejected: 18 · not counted as rejections", a "No answer" box in the diagram.
- **The count before the build and the number the first sweep moves match.** **Only partly met.** On the copy of the data: SQL 17 = dry run 17 = sweep 17. On the host: the page said 17 on 3 Nov and the sweep moved 18 on 4 Nov; the dump projects exactly 17 then 18, so the difference is the calendar, but no before/after counts were saved on the host, so it is consistent, not measured.
- **Cost:** one session over two days, in the 11 planned slices; 82 new tests; the sweep reads about 14.5 KB.

## What we learned
- **A count that depends on the date is not a fixed number.** "Applications older than 30 days" grew from 17 to 18 to 28 in three days. Any "the first run will move N" promise needs the date next to it, and the measure should be "the dry run and the real run, taken at the same moment, match".
- **An automatic change must not look like an answer.** The first Insights build counted the sweep's own history line, and the put-back line, as an employer's answer. Anything the app writes into the history needs a rule for the statistics (here `is_presumption`), found by asking "what reads this line?".
- **Every place that lists the fields of a row has to learn a new field.** The backup merge silently dropped the tag until `_STATE_FIELDS` listed `auto_rejected_at` (found only by a test that merges a backup).
- **The cycle 014 pattern carried over unchanged:** the status in the `UPDATE`, one hook for the race, one read for the ids only. Writing the sweep was quick because of it.
- **This PC's clock gives equal timestamps to back-to-back calls** (2000 of 2000 pairs). Tests that need "later than" on Postgres must date things apart; two of mine and one of cycle 015 were flaky for this reason.
- **A "one-time notice" is better as a 7-day banner:** it needs no stored "seen" flag and disappears by itself (the spec's change from the intent).
- **Not covered:** French on the host, a non-operator getting 404 on the host, the pages on a real phone, Neon's own transfer figure, the full Postgres suite on 4 Nov.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| The feature as built: delay, exemptions, tag, box, put-back, banner, "No answer" in Insights | `docs/PRD_competitive_features.md` F5 (new bullet) | [x] |
| Runner step and the console page | `docs/DEPLOY.md` (updated in the build) and `scripts/pc_runner.ps1` | [x] |
| Cycle 019 closed; the host state (18 moved, one put back, delay 30) | project memory `project-sdlc-cycles`; `docs/sdlc/README.md` status row | [x] |
| Test baseline now 1,436 on SQLite; Postgres: the cycle-015 test `test_feedback_console` fails on equal timestamps | project memory `reference-running-tests`; the fix belongs to cycle 015 | [x] |
| The rule "the app's own history lines need a statistics rule" | project memory `project-sdlc-cycles` (one line) | [x] |

## Process feedback
- **Worked well:** the Postgres rehearsal as its own slice (it gave the three-way count 17 = 17 = 17 and the cost figures), the runbook for the two host steps, and mutation-checking the race tests.
- **Slowed us down:** the host steps ran without saved before/after counts, so the main promise of the intent could not be measured afterwards. Suggestion for the playbook: a runbook step that changes the host must name the one number to write down before and after, and the verify row for it says "measured" or "consistent".
- **Slowed us down:** other sessions edit `docs/sdlc/README.md` and the board at the same time, so only row 019 could be staged. Same suggestion as in cycle 014.

## Next cycle candidates
- Fix `test_feedback_console` for equal timestamps on Postgres (small, belongs with cycle 015).
- If French readers find "Remettre en « Postulée »" stiff, change it to "Repasser en « Postulée »" (one string).
- An e-mail or a digest line about presumed rejections belongs to cycle 009 (reminders), not here.
