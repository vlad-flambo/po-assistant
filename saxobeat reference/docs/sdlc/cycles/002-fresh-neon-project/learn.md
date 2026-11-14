# Learn: move to a fresh Neon project, keep the old one as a fallback

| | |
|---|---|
| **Cycle** | 002 |
| **Stage** | Learn: done 2026-10-30 except "delete or refresh `saxobeat-fallback1`" (later, after a clean month) |
| **Verify** | [verify.md](verify.md) |

## What happened vs what we expected
- **Expected:** a quick move: restore a dump, change two settings, no service interruption.
- **Happened:** exactly that, with no visible interruption: slices 1 to 7 ran in one sitting, about an hour from the dump (10:05) to the proof of the first login (about 11:04, local time). The restore took 14 seconds. Every one of the 38 tables (173,937 rows) matched the old project, and the login written after the switch landed in the new project.
- **Success measure:** the nine checks of the intent: eight pass at the time of writing; the ninth (the old project goes quiet, the new one climbs slowly) is read in Neon on 2026-10-30. Criterion 2 passes in part, accepted as a risk.
- **Not what was asked originally:** the move did not reduce what the runner reads. That is cycle 001, which is still waiting for its measurements.

## What we learned
- The Free plan's 5 GB of transfer is **per project** and counts only data **out**; a restore into a new project is free. A fresh project is a cheap stopgap, not a fix.
- Neon's docs say the 5 GB allowance is **per project** ([network transfer](https://neon.com/docs/introduction/network-transfer), [plans](https://neon.com/docs/introduction/plans)), but the dashboard figure the owner can see is **one sum of all projects** (4.76 GB on 2026-10-29, now the baseline reference). **Observed the same day:** the old project's own page shows a banner "You've used 95.1%" (about 4.755 GB) while the sum is 4.76 GB, so the usage is counted per project and prod1 had used about nothing. prod1's own page shows **no banner** (checked by the owner): the banner appears only from 80 % of the monthly allowance (the owner's understanding, not confirmed in the docs). So prod1's usage is read as **the sum minus the old project's percentage times 5 GB**, with a resolution of about 15 MB (the sum has two decimals, the percentage one). The API field `data_transfer_bytes` would give prod1's own number directly.
- **The rollback has little room:** the old project has only about 0.245 GB of allowance left until the next period, so a rollback would work for hours or a day or two of web use, not for weeks. Treat the fallback as a data snapshot more than as a place to run the app.
- At the cap Neon **suspends the compute** until the next period or an upgrade. The app would have stopped, not just slowed.
- **The runner was never scheduled** on this PC: `DEPLOY.md` described a 3-hourly task that did not exist. Estimates built on that description were wrong; the leftover files (dumps, AI files, an empty cache folder) told more than a guess.
- A dump taken from Neon carries default-privilege entries for Neon's own roles, which fail on a plain Postgres. Leaving those two entries out gives a clean exit code.
- **Proof of "the app writes to the new database"**: `max(last_login)` in both databases. `/healthz` is not proof (the old deploy answers `ok` until the new one is healthy), and a `django_session` row count is not either (a login from an existing session replaces its row).
- A rehearsal on the local Docker against the very same dump caught two problems (the role errors, the BOM in my test file) at no cost on Neon. Worth repeating for any restore.
- A second quoting problem showed up in the first real restore: a `grep` pattern with double quotes lost them on the way into `docker run` and the shell stopped before `pg_restore`. The guard ("target must be empty") and the check afterwards (prod1 still empty) made it harmless.
- Both connection strings and every restore travelled in environment variables, set from `.env` in the PowerShell session and passed to Docker by name: nothing sensitive reached a command line, a file in the repo or the chat.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| The two projects, roles, rollback, the full move recipe, the `DEFAULT ACL` filter, the proof by `last_login` | `docs/DEPLOY.md` §8 | [x] |
| The runner is manual; the transfer cap and what happens at it; what actually happened in October | `docs/DEPLOY.md` §4, §5, "Which host" table | [x] |
| Backup frequency (monthly since cycle 001's D3; not daily) and the `DEFAULT ACL` note | `docs/DEPLOY.md` "Backups and restore" | [x] |
| The helper `scripts/db_counts.py` | repo `README.md` file table | [x] |
| Cycle state, the rule "no runner, `ai sync` or backup against the hosted database until cycle 001's measurements are planned" | project memory `project-sdlc-cycles` | [x] |
| The reading of both Neon figures (criterion 9: prod1 about 135 MB in about one day, the old project unchanged at 95.1 %) and the first observation of the web rate | `verify.md` and cycle 001's `evidence/projection.md` | [x] 2026-10-30 |
| Delete or refresh `saxobeat-fallback1` | decide once prod1 has had a clean month (intent Q4) | [ ] later |

## Process feedback
- **Worked well:** one question at a time with a recommended answer; recording each answer in the file the moment it was given; the plan's order (everything that changes nothing first, one single production edit, an easy rollback); evidence files with counts only.
- **Slowed us down:** the playbook itself had to be found (it was not in the repo), and a few answers were guessed in the first drafts (the runner schedule). Stating facts with their source in the intent file, as done here, avoided repeating that.
- **Add to the playbook:** "rehearse on a local copy" as a standard slice for anything that writes to a hosted service; "prove, don't observe" (a health check is not proof the right backend is in use).
- **Stale text found in `DEPLOY.md` and left alone** (out of scope): the "Not verified yet" section at the end still says no Render service exists and that nothing was run on a host, and "Saxobeat AI\to-do" contains a tab character in place of `\t`.

## Next cycle candidates
1. **Cycle 001, Spec**, once prod1 has a clean day: the measurements (the daily rate on web use alone, bytes of one manual run, of `ai sync` and `mail send`), then B or C, or D (do nothing new) if the numbers say so.
2. A password-manager copy of the fallback string (criterion 2).
3. Fix the stale "Not verified yet" section of `DEPLOY.md`.
