# Intent: Cloud dev workspace

| | |
|---|---|
| **Cycle** | 028 |
| **Stage** | Intent |
| **Date** | 2026-11-05 |
| **Owner** | Vladimir Stoyanov |
| **Importance** | 3/5 (claude, 2026-11-05): dev only works on the owner's PC today; a testbed database keeps dev reads off prod1's 5 GB allowance; depends on 025 |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
Part of the 2026-11-05 request (full text in cycle 025): "Also, I want to be able to do the dev on a Claude instance in the cloud. Probably would be good to have a testbed db, so dev doesn't eat up the prod bandwidth. We could use the fallback1 db to start."

## Why now / the pain
- Development happens only on the owner's Windows PC (PowerShell, `uv`, Docker for Postgres). The `.env` with the live hosted address and a live Brevo key sits on that PC.
- Anything dev does with real volume reads prod1's 5 GB monthly transfer; a testbed database is meant to take that load.

## Goal
A Claude session in the cloud can clone the repo, run the tests, run the app against the testbed database, and open a pull request, without ever holding prod's database address or the Brevo key. The testbed is a full copy of prod (owner, 2026-11-05, cycle 025 Q1), so the session can see friends' CVs there: that exposure is accepted for now and reconsidered as the user base grows.

## Success measure
1. A cloud session runs the project's test command green from a clean start, using only a setup script kept in the repo.
2. It runs the app against the testbed database and loads a page (shown by a row written in the testbed and absent from prod1).
3. A search of the cloud session's environment shows no prod database address and no live mail key (variable names only, never values).
4. A change made there reaches pre-prod through a pull request and CI (cycle 025), not prod.

## Not doing (this cycle)
- Giving a cloud session any write access to prod.
- Moving the owner's other work (docs, board) off the PC.

## What we already know (facts, with where they came from)
- Tests use SQLite and need no database or secret: `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider` (PROJECT.md), about 45 seconds; 1,499 passed in cycle 024.
- The repo is on GitHub (`vlad-flambo/saxobeat`, remote `origin`, only `main` on the remote). Recent commits are not pushed yet (board notes); a cloud session sees only what is pushed.
- The working tree has uncommitted changes of other cycles (git status, 2026-11-05): a cloud session would not have them.
- `docker compose` Postgres (development) is not likely to exist in a cloud sandbox; SQLite or the testbed on Neon replaces it (to verify).
- The testbed's content and refresh come from cycle 025. Decided 2026-11-05 (025 Q1): a **full copy of prod including friends' CVs**; `fallback1` already is one (as of 29 October). A cloud session with its address can read those CVs.

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | Use fallback1 as the testbed right away? | Yes, once 025 question 7 is settled (contact channels neutralised: no copy can e-mail or be logged into as a friend); but it is also the recovery copy of 29 October, so record its counts first and take the recovery role from a fresh Neon snapshot of prod1 instead. | | open |
| 2 | Where do the cloud session's secrets live? | In that session's own environment settings, testbed address only; nothing from `.env`. | | open |
| 3 | Which cloud sessions: Claude Code on the web, or the desktop app's cloud sessions? | Whichever you already have access to; the setup script is the same. | | open |

## Constraints and risks
- Depends on 025 (testbed, branches, CI). Neon projects have separate connection strings, so the testbed's string gives access to friends' CVs (full copy), so it is still a secret: in the session's environment settings only, never in the repo.
- Everything unpushed is invisible to the cloud: the push policy (the owner's call) decides what dev can start from.

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
