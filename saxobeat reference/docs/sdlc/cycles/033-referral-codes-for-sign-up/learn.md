# Learn: invitation codes for sign-up

| | |
|---|---|
| **Cycle** | 033 |
| **Stage** | Learn (**drafted 2026-11-10, before the owner's verdict**: the owner has not yet tried the links on the host; see `next.md`) |

## What happened vs what we expected
- **Success measure 1** (a stranger signs up with a code typed or in a link; nobody without a valid code): met in tests (`tests/test_invitation_codes.py`, 63 tests), seen working on a scratch app at 375 px, and the sign-up page is live on the host with the code pre-filled (read 2026-11-06). **Not yet tried by the owner on the host.**
- **Success measure 2** (every account shows its origin; the console counts per code): met in tests and on the scratch app (Skaleet 1 + candidates' codes 0 + invitation links 1 + before codes 2 = 4 accounts). The owner saw the People page on the host ("looks good", 2026-11-06).
- **Success measure 3** (a candidate's one fixed code, counted friends): met in tests; the phone check of the share button is the owner's.
- **Cost, not in the measure but the main surprise:** one new account is about **8 MB and 30,675 job views** (first backfill 53 to 59 s), ten times what the spec assumed ("thousands of rows"). Neon's free 0.5 GB holds about 40 such accounts beyond what the app uses; 20 sign-ups an hour (the approved brake) would add about 160 MB.
- Suite: 1,706 pass on SQLite and on local Postgres (the cycle-015 Postgres failure no longer shows).

## What we learned
- **Opening sign-up turns "who gets in" from the operator's decision into a cost question.** What a sign-up costs (rows, megabytes, minutes of CPU, e-mails) has to be measured before the numbers of a brake are chosen; the measure took one script and changed the story.
- The sign-up brake and the wrong-code lock needed no new table: `FailedLogin` (name, address, time, swept after two days) carries them under two reserved names. The price: the login throttle's address count had to learn to ignore those names (found while writing the tests, not by luck: a test for exactly that).
- Putting origin on the candidate as a snapshot (`origin_label`) plus a nullable link (`origin_code`) keeps the history readable when the inviter is deleted. The bulk delete of cycle 032 uses raw DELETEs, which skip Django's set-null: the friends' link must be cleared by hand first, and the guard test of cycle 032 is what made the new table impossible to forget.
- "Referral" and "invitation" were both taken in the app (the job message and the single-use link): naming the feature before building avoided a clash in the console and the documents.
- Existing behaviour found on the way: the first user to sign up claims a candidate row that has no user yet (`Candidate.for_user`), which bit two of my tests.
- **A slip worth keeping:** a Python replace that took everything from a marker to the end of the file cut the tail off `jobs/accounts.py`; the suite failed at once and git restored it. Replace bounded ranges only.
- Not decided and not built, on purpose: e-mail invitations from a candidate (R6), confirming the e-mail address at sign-up (R7, Q8 parked).

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| Invitation codes: how they work, the brake, the cost per account, switch-off as the brake | `docs/DEPLOY.md` (section 6 and *Accounts*) | [x] 2026-11-10 |
| Sign-up is no longer by single-use link only | `docs/PRD_users_and_emails.md` (outstanding list) and `docs/PRD_multi_user.md` (Comptes row) | [x] 2026-11-10 |
| E-mail invitation from a candidate (R6) and e-mail confirmation (R7) as later items | `docs/PRD_users_and_emails.md` register | [x] 2026-11-10 |
| Measure what one new account costs before choosing a flood brake; the table `FailedLogin` can carry attempt counts | house-stack `reference/gotchas.md` (user-level skill, outside this repository) | [x] 2026-11-10 |
| The cycle's state, files, numbers and gotchas | project memory `project-sdlc-cycles` (outside this repository; see `docs/sdlc/HANDOFF.md` for how to carry it) | [x] 2026-11-10 |
| The owner's verdict on `verify.md`, criteria 13 and 18, and the number for the brake (20 an hour: keep or lower) | `verify.md`, then this file | [ ] waits for the owner |

## Process feedback
- Worked well: measuring the cost on a restored dump before building (slice 1), and a plan whose guard test was *expected* to fail between slices 2 and 7: it did, and then it was the safety net.
- Slowed down: the board refresh (upload, read versions, batch update, delete old blobs) is eight tool calls after every step; a script that does the four Artifact steps would save most of them. Candidate for the ai-sdlc skill.
- The working tree held other cycles' uncommitted edits (README, BOARD, `locale/fr`, `seed_employers.py`, five untracked cycle folders): committing only this cycle's paths was right at the time and left a pile that had to be swept when the owner changed computers. A short "commit the docs of the other cycles" habit at the end of each session would avoid it.

## Next cycle candidates
- **E-mail invitation from a candidate (R6)**, with a per-person limit.
- **Confirm the e-mail address at sign-up (R7).**
- **A lower or editable flood brake** if the owner wants the number in the console instead of in code.
- Showing the inviter who joined (decision D2 said no; reopen if friends ask).
