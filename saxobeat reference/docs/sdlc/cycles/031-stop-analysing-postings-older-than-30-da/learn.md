# Learn: stop analysing postings older than 30 days

| | |
|---|---|
| **Cycle** | 031 |
| **Stage** | Learn |

## What happened vs what we expected
- **The request:** "don't analyse job listings over 30 days old; I believe the cutoff is currently 2 months." The belief was right (60 days, per candidate, default in `jobs/models.py`).
- **Success measure (intent.md, as confirmed, six criteria; spec had eleven):** all met locally. New default 30 and stored limits untouched; dated postings by their own date; undated postings by the day the job was imported, in the arrival filter, the refilter and the nightly age-out; nothing past the limit is scored or offered to the AI; the limit switched off hides nothing; no data written. Suite 1,623 before, 1,632 after. `verify.md`: 11 of 11 pass.
- **What the first run will do (measured on the 29 Oct dump, local copy):** with today's date applied, candidate 1 would lose 840 dated and 106 undated postings out of 1,632 visible views (58 %); the test profile 3,508 and 1,009 out of 8,781. Most of the dated ones were already going to be hidden by the owner's own manual move to 30 on the host (not checked, not in the dump). The undated part is the new effect and **grows daily**: the database only goes back to 29 Sep 2026, so no undated job was over 30 days old on 29 Oct, and 106 are today.
- **Not met or not checked:** nothing deployed or measured on the host; Postgres suite not run (the age-out query plan was seen on the local Postgres: 11 ms, no text read); the French help text was not looked at on screen.

## What we learned
- **The undated rule is a ratchet, not a one-off.** Because the import date is the proxy, an undated posting ages out 30 days after it was first seen, whatever the employer does. That is what the owner asked for ("a best-guess proxy for the listing date"), but a long-open undated posting that the employer still lists will disappear from the inbox after a month.
- **A candidate's view has no `first_seen_at` of its own**: `CandidateJob` reads the job's through `__getattr__` and has only `created_at`. I had it wrong in the intent, spec and plan (the line I cited, `models.py:420`, belongs to `JobSource`); I found it by a failing test while building and corrected all three files the same day. The design did not change because the job's `first_seen_at` was the answer anyway.
- **Hard-coded dates in tests are time bombs.** Two tests (`test_greenhouse_adapter_and_run` with 2026-09-20, `test_jibe` with 2026-10-02) failed as soon as the default dropped to 30, and the first would have failed on 19 Nov at the old 60 anyway. Fixed with dates relative to now.
- **One mail test failed once in a full run and passed alone, in its file and in the next full run** (`test_the_ai_email_tells_the_new_picks_once_and_at_most_every_12_hours`). Not reproduced; a possible clock-ordering flake like cycle 015's.
- **Repost handling is separate:** `Job.first_listed_at` (the chain's first date) would also age reposts; the owner chose the job's own `first_seen_at`, so an undated repost looks young.
- **Docker Desktop had to be started** to restore the dump (a local, reversible step); the local container was left running.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| The age rule now: default 30, every source, undated aged from the import date, hidden jobs not scored | `docs/PRD.md` (the Age line under hard filters), edited 2026-11-06 | [x] |
| A literal date in a test ages out; generate dates relative to now | house-stack `reference/gotchas.md`, added 2026-11-06 | [x] |
| Cycle 031 state, the 2026-11-06 estimate and the board lesson | Claude project memory `project-sdlc-cycles`, updated 2026-11-06 | [x] |
| The first-run effect and the undated ratchet, for the push decision | this file and `evidence/counts.md` | [x] |
| The possible flaky mail test | next-cycle candidate below | [ ] deferred 2026-11-06, owner's decision |
| Existing candidates' stored limits on the host were moved by hand by the owner, not by a migration: a new candidate is the only case the code default reaches | noted here; no doc needs it | [x] |

## Process feedback
- **What worked:** the evidence step (restoring the real dump on a scratch database and counting) turned "the first run will hide some jobs" into numbers before any deploy, and found that the undated rule does nothing on the dump but bites today, which the unit tests alone could not have shown. "Tests first, watch them fail, then the code" caught the wrong claim about the view's date.
- **What slowed us down:** I carried two plan-time assumptions about the data model (the view's own date) from a line I had not traced to its class; trace a field to its model before writing it into a spec. The live board lagged because I had refreshed only `BOARD.md`; from cycle 030 on I refreshed both after each step that moved a cycle.
- **Gate handling:** "approved, build until you need me" for the plan stage, then a single question at the end about commit and push, kept the owner's decisions (commit, push, acceptance) with the owner and the build uninterrupted.

## Next cycle candidates
- **Look at the flaky mail test** if it fails again (`tests/test_mail.py`, the 12-hour grouping): reach is the suite's trust, not users.
- **Reposts of undated postings** (use `first_listed_at` so a repost keeps its original age): belongs with cycle 022 (reposted after applied) if the inbox shows reposts of old roles.
- **Read the host's real effect after the deploy:** count the views hidden for age on the host by candidate, before and after (read-only counts on Neon cost allowance: say it out loud first).
