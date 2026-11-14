# Plan: move to a fresh Neon project, keep the old one as a fallback

| | |
|---|---|
| **Cycle** | 002 |
| **Stage** | Build done except slice 8 (the watch); see [verify.md](verify.md) |
| **Spec** | [spec.md](spec.md), approved 2026-10-29 |

## Who does what
- **Owner (you):** everything in the Neon and Render dashboards, and every edit to `.env` that holds a connection string.
- **Claude:** the scripts and commands that run from this PC. They read strings from `.env` into environment variables, print only yes/no or counts, never a string.

## Slices
Each slice stops at its check. Nothing in production changes until slice 6.

| # | Slice | Who | Touches | Check | Criteria | Status |
|---|-------|-----|---------|-------|----------|--------|
| 1 | Prepare: confirm prod1's settings, save the old string outside the repo, fill `.env` | Owner, then Claude verifies | `.env` | Claude reports only: both lines exist, hosts are Neon, prod1's host has no `-pooler`, region is eu-central-1 | 1, 2 | **done 2026-10-29** with one deviation, see "As run" |
| 2 | Row-count helper, tested on the local database | Claude | `scripts/db_counts.py` (new) | Runs on the local Docker Postgres, prints a count per table, and its compare mode flags a deliberate difference | (tool for 3, 4) | **done** |
| 3 | Note the old project's counts | Claude | `docs/sdlc/cycles/002-fresh-neon-project/evidence/counts_fallback_2026-10-29.json` | The file lists every table; the read is a few KB | 3 | **done** |
| 4 | Restore the 10:05 dump into prod1 | Claude | prod1 only | `pg_restore` exits 0; warnings read and explained | 4 (part) | **done** |
| 5 | Compare counts and read prod1's transfer | Claude (counts), owner (Neon figure) | `evidence/counts_prod1_*.json` | Every table equal; Neon's figure for prod1 still near zero | 4, 5 | **done**: counts identical; prod1's Neon figure near zero after the restore (owner, 2026-10-29) |
| 6 | **The switch:** Render `DATABASE_URL` = prod1 | Owner | Render settings | The new deploy is live; `/healthz` says `ok`; owner logs in as `vlad`; the Inbox matches and the second load is under about 2 s | 6, 7 | switched; 6 **met**; 7 waits for the owner's look at the Inbox |
| 7 | Move the PC to prod1: rename the `.env` lines | Owner, then Claude verifies | `.env` | `saxobeat-runner.cmd check` passes; Claude reports the hosted line is Neon and not the fallback's | 8 | **done** (the `.env` was already in place from slice 1) |
| 8 | Watch: fallback quiet, prod1 climbing slowly | Owner reads Neon, Claude records | `verify.md` | A few hours later the fallback's figure has not moved | 9 | todo |

Criteria 10 and 11 hold in every slice (no secret exposed, rollback available).

## Order and why
1 → 2 → 3 first, because they change nothing in production and give us the old counts while the fallback still has headroom. 4 and 5 touch only prod1, which nothing uses yet. 6 is the only step that can affect the live app, and it is one edit. 7 comes after 6 on purpose: the runner is manual, so a short period with `.env` still on the old project hurts nothing. 8 closes the loop.

## The commands (no secret on any of them)
- Slice 2 to 5, counts: `uv run python scripts/db_counts.py <ENV_VAR_NAME>` reads the string from the variable (set from `.env` by a wrapper line), prints `table  count`, and can save JSON. `uv run python scripts/db_counts.py --compare a.json b.json` lists every difference and exits non-zero if any.
- Slice 4, restore, from PowerShell in the project folder. The string is taken from `.env` into `SAXOBEAT_RESTORE_URL` for this process only and passed to Docker by name, so it is not on the command line:
  ```
  docker run --rm -e SAXOBEAT_RESTORE_URL -v "${PWD}\data\backups:/b:ro" postgres:17 sh -c 'pg_restore --clean --if-exists --no-owner -d "$SAXOBEAT_RESTORE_URL" /b/saxobeat_2026-10-29_100546.dump'
  ```
- Slice 6 is a dashboard edit: Render, service `saxobeat`, Environment, `DATABASE_URL`, save, wait for the deploy.
- Slice 7, `.env`: the line `SAXOBEAT_HOSTED_DATABASE_URL` (the old string) becomes `SAXOBEAT_FALLBACK_DATABASE_URL`; the line `SAXOBEAT_NEW_DATABASE_URL` becomes `SAXOBEAT_HOSTED_DATABASE_URL`.

## Rollback
| Slice | If it goes wrong |
|-------|------------------|
| 1 to 3 | Nothing in production changed: stop, fix, repeat |
| 4, 5 | prod1 is unused: recreate it (or restore again with `--clean`) and retry |
| 6 | Put the old string back in Render's `DATABASE_URL`; the app returns to the old project (still at 10:05 state, plus anything written to prod1 in between, which is lost) |
| 7 | Rename the two `.env` lines back |
| 8 | Not an action: it only reads |

## Risks and how the order handles them
- The fallback has little transfer left: only slice 3 reads it (a few KB), so there is no 200 MB read.
- A table differs after the restore: slice 5 stops the cycle before slice 6.
- The Render deploy fails: Render keeps serving the old deploy until the new one is healthy; slice 6's rollback is one edit.
- Windows and Docker quirks in slice 4 (paths, `host.docker.internal` is not needed here since the target is remote): tried first against the local database (slice 2's database), restoring a copy of the same dump into a scratch database, so a mistake shows before prod1 is touched. This local rehearsal costs nothing on Neon.

## As run (log, newest last)
**2026-10-29, slice 1.** The owner put prod1's string straight into `SAXOBEAT_HOSTED_DATABASE_URL` in `.env` and kept the old string as a **comment line** in the same file (instead of `SAXOBEAT_NEW_DATABASE_URL` plus a `SAXOBEAT_FALLBACK_DATABASE_URL` variable). Checked read-only, nothing printed:
- `.env` is gitignored and not tracked by git.
- The active hosted line: Neon host, no `-pooler`, `eu-central-1`, `sslmode=require`. A probe of that database: **Postgres 17.11, 0 tables in `public`, 7.5 MB**: it is the new, empty prod1 (criterion 1 met).
- The commented line is a different Neon host, also without `-pooler`, in `eu-central-1`: the old project.
- Consequences for the next slices:
  - Half of slice 7 is already done: **the PC's hosted address now means prod1**. The runner, `ai sync` and the backup command would act on the empty prod1 until the restore: they are not to be run until slice 5 passes.
  - Slice 4's restore target is `SAXOBEAT_HOSTED_DATABASE_URL` (not `SAXOBEAT_NEW_DATABASE_URL`). Safety check added to slice 4: refuse to restore unless the target has 0 tables in `public`, since `--clean` drops tables.
  - Slice 3 needs the old string as a variable. A comment line cannot be read by the scripts: the owner turns it into `SAXOBEAT_FALLBACK_DATABASE_URL=...` (remove the `#`, add the name). Nothing reads that variable except the count script.
  - Criterion 2 ("saved outside the repo") is met only in part: the string is in `.env`, which is gitignored but sits in the project folder. A copy in a password manager is recommended, the owner's call.

**2026-10-29 10:4x to 10:53, slices 2 to 5.**
- Slice 2: `scripts/db_counts.py` written and tested on the local database: counts, save, compare (identical and a deliberate difference), `--expect-empty` (exit 2 on a non-empty database), unset variable (exit 3). A first compare failed on a byte-order mark that Windows PowerShell wrote into my test file; the reader now accepts one.
- Slice 3: old project (fallback) counted: 38 tables, 173,937 rows, Postgres 17.11. Evidence: `evidence/counts_fallback_2026-10-29.json`.
- Rehearsal (not in the plan's table, planned in its risks): the dump restored into a scratch database in the local Docker gave identical counts to the old project, which also shows the dump itself holds everything. Two errors on the first try, both about default privileges for the Neon-only role `neon_superuser`; the restore now **leaves out the two `DEFAULT ACL` entries** of the dump (a table-of-contents filter, `-L`), and exits 0. The scratch database was dropped.
- Slice 4: guard passed (prod1 had no tables). One failed attempt: my `grep` pattern lost its quotes inside Docker and the shell stopped before `pg_restore` ran; prod1 was verified still empty before the retry. Retry: **`pg_restore` exit 0 in 14 s**, 327 entries restored.
- Slice 5, counts: prod1 vs old project, **identical, every table** (38 tables, 173,937 rows). Evidence: `evidence/counts_prod1_after_restore_2026-10-29.json`. Criterion 4 met.
- Slice 5, Neon figure: the owner read prod1's Network transfer after the restore: **near zero**. Criterion 5 met: data sent into Neon does not count (as the docs say). Slice 5 done; criteria 1 to 5 all met.
**2026-10-29, slices 6 and 7.**
- Slice 6: the owner set Render's `DATABASE_URL` to prod1 and saved. `/healthz` answered `ok` on `jobs.stoyan.ovh` and `saxobeat.onrender.com`; this alone proves nothing, since Render serves the old deploy until the new one is healthy.
- Proof that the app writes to prod1: after the owner's login, **prod1's latest `last_login` is 2026-10-29 10:04:09 UTC** (40 s before the query), while the **old project's is still 2026-10-28 11:40:23 UTC**. Criterion 6 met. The first idea, comparing `django_session` row counts, showed no change in either database, because a login from an existing session replaces its row instead of adding one: a weak marker, kept here as a lesson.
- Slice 7: `saxobeat-runner.cmd check` passes (uv found, hosted address in `.env`: yes, exit 0). Criterion 8 met. Evidence: `evidence/counts_prod1_after_switch_2026-10-29.json` and `evidence/counts_fallback_after_switch_2026-10-29.json` (both unchanged from before).
- Observation: the old project already has the email tables (`jobs_mailsettings`, `jobs_outgoingemail`), so its schema is at least as new as the uncommitted `email` branch. That is how it was before the move; the move changes nothing about it. Worth remembering when deciding what Render deploys (the Render service builds from `main`).

## Gate
- [x] Owner approved the slices (2026-10-29)
