# Spec: move to a fresh Neon project, keep the old one as a fallback

| | |
|---|---|
| **Cycle** | 002 |
| **Stage** | Spec approved 2026-10-29; next: Plan ([plan.md](plan.md)) |
| **Intent** | [intent.md](intent.md), approved 2026-10-29 |

## Behaviour when finished
- The live app on Render reads and writes `saxobeat-prod1`, a Neon project that holds the data of the 2026-10-29 10:05 dump.
- The PC runner scripts (`saxobeat-runner.cmd`, `saxobeat-ai.cmd`) point at `saxobeat-prod1` through the same variable as before, `SAXOBEAT_HOSTED_DATABASE_URL`.
- `saxobeat-fallback1` (the old project) is not read or written by anything. It is a snapshot of 10:05 and a way back.
- Nothing about the app's behaviour changes for the user. The only change a candidate could notice is the loss of anything done after 10:05 (none: only the owner uses the app).

## Acceptance criteria
Each is checked in `verify.md` with its evidence.

**Before the switch**
1. [ ] `saxobeat-prod1` is Postgres 17, in Frankfurt (`aws-eu-central-1`), and the string in use has no `-pooler` in its host.
2. [ ] The old connection string is saved outside the repo (for example a password manager), and a local `.env` line keeps it as `SAXOBEAT_FALLBACK_DATABASE_URL`.
3. [ ] The dump `data/backups/saxobeat_2026-10-29_100546.dump` is on disk, and the old project's row count per table is noted.

**After the restore, before touching Render**
4. [ ] The row count of every table in prod1 equals the old project's count (the dump is a snapshot, so they must match exactly, unless something wrote to the old project after 10:05: then the differences are explained).
5. [ ] prod1's Network transfer figure in Neon is still near zero after the restore (confirms that data sent in does not count, intent Q6).

**After the switch**
6. [ ] `/healthz` on the Render address says `ok`, and logging in as `vlad` works.
7. [ ] The Inbox shows the same jobs as before the switch, and the second page load is under about two seconds.
8. [ ] `saxobeat-runner.cmd check` passes (it reads nothing from the database). No full run is started: that waits for cycle 001's measurements.
9. [ ] A few hours later, the fallback's Network transfer figure has stopped moving and prod1's climbs slowly.

**Always**
10. [ ] No connection string appears in the repo, in a commit, in this chat, or on a command line (it travels in `.env` or an environment variable).
11. [ ] Rollback is possible at every step: before the Render change nothing in production has changed; after it, the same two edits in reverse put the app back on the fallback.

## Design in brief
- **Approach:** restore the existing dump into the empty prod1 with `pg_restore --clean --if-exists --no-owner` (the command already in `docs/DEPLOY.md`), then switch two settings. No code change, no migration of the schema by hand: Render's start script runs `migrate` on boot and finds the migrations already applied.
- **Secrets stay in `.env`.** The owner adds the new string as `SAXOBEAT_NEW_DATABASE_URL` in `.env` (gitignored). The restore and the count comparison read it from there into an environment variable of the process and never print it. At the switch the owner renames the lines: the old `SAXOBEAT_HOSTED_DATABASE_URL` becomes `SAXOBEAT_FALLBACK_DATABASE_URL`, and the new string becomes `SAXOBEAT_HOSTED_DATABASE_URL`. Rollback is the same rename the other way.
- **Order of the switch:** Render's `DATABASE_URL` first (it redeploys and runs the start script), then `.env` for the PC. The restore is not repeated after that.
- **Row counts** are compared with a tiny read-only script: `select count(*)` per table, a few kilobytes of result per database, run once against each.
- **Rejected:** a fresh dump right before the switch (the owner accepted the loss since 10:05; saves another 200 MB read); logical replication into prod1 (a permanent connection, and its data counts toward the same allowance); a maintenance page (only the owner uses the app).

## Interfaces and data
| What | Change |
|------|--------|
| `.env` on the PC | new line `SAXOBEAT_NEW_DATABASE_URL` (temporary, during the restore); after the switch: `SAXOBEAT_HOSTED_DATABASE_URL` = prod1, `SAXOBEAT_FALLBACK_DATABASE_URL` = old project. Never committed |
| Render, service `saxobeat` | `DATABASE_URL` = prod1 string (no `-pooler`) |
| Neon | prod1 holds the data; the fallback project is untouched and not read or written after the switch |
| Repo | `docs/DEPLOY.md` updated in the Learn stage (project names, the fallback, the two `.env` lines). A helper script for row counts, if it earns a place, goes under `scripts/` |
| Schema, code | none |

## Constraints
- Neon Free plan caps per project: 5 GB transfer, 100 CU-hours. The fallback has little transfer left (about 0.3 GB when this was written), so **nothing in this cycle may read it more than the count query** (and the rollback, if needed).
- Windows PC with Docker (`postgres:17` image for `pg_restore`); the Docker route is the one already used for backups.
- Only the owner uses the live app, so no downtime window is announced. Neon wakes prod1 on the first connection (a few seconds).
- Secrets: see criterion 10.

## Risks
| Risk | Mitigation |
|------|------------|
| The restore fails halfway (version mismatch, timeout) | prod1 is empty and not yet used by anything: drop its tables or recreate the project, retry. Nothing in production is touched |
| Row counts differ | Do not switch. Find the cause (the dump, a write to the old project after 10:05, a failed table) before going on |
| The Render redeploy fails (wrong string, `-pooler`, SSL) | Render keeps the previous deploy serving until the new one is healthy; fix the variable or set it back to the fallback string |
| The PC `.env` and Render point at different projects for a while | The runner is manual and not started until the checks pass |
| The old string is lost, so rollback is impossible | Criterion 2 comes first |
| prod1's transfer behaves unexpectedly (a restore counts) | Criterion 5 is read before the switch; if it counts, the allowance is reduced by about 200 MB, and the plan says so |

## Out of scope
- Cutting the runner's reads (cycle 001).
- Deleting `saxobeat-fallback1`, or refreshing it.
- A scheduled runner, a replica, a local copy.

## Gate
- [x] Owner approved this spec (2026-10-29)
