# Verify: move to a fresh Neon project, keep the old one as a fallback

| | |
|---|---|
| **Cycle** | 002 |
| **Stage** | Verify, accepted by the owner 2026-10-30 (10 of 11 criteria met, criterion 2 accepted as a risk) |
| **Spec** | [spec.md](spec.md) |
| **Date** | 2026-10-29 |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | prod1 is Postgres 17, Frankfurt, no `-pooler` | **pass** | Probe of the active hosted database: `server_version 17.11`, host in `eu-central-1`, no `-pooler`, `sslmode=require` (checked read-only on `.env`, nothing printed) |
| 2 | Old string saved outside the repo, kept as `SAXOBEAT_FALLBACK_DATABASE_URL` | **partial, accepted risk** (owner, 2026-10-29) | The variable exists in `.env` (gitignored, untracked) and points to the old project. It sits in the project folder, not in a separate store. Accepted: both strings live in one file on one PC, so losing `.env` loses the rollback string (the data itself stays in Neon) |
| 3 | Dump on disk, old row counts noted | **pass** | `data/backups/saxobeat_2026-10-29_100546.dump` (62.3 MB, valid header, 38 tables with data); `evidence/counts_fallback_2026-10-29.json` (38 tables, 173,937 rows) |
| 4 | prod1 counts equal the old project's after the restore | **pass** | `db_counts.py --compare` of `counts_fallback_2026-10-29.json` and `counts_prod1_after_restore_2026-10-29.json`: "Identical: every table has the same number of rows". Also identical in the local rehearsal |
| 5 | prod1's transfer figure near zero after the restore | **pass** | Read by the owner in Neon's dashboard after the restore: near zero |
| 6 | `/healthz` ok, login works | **pass** | `/healthz` 200 `ok` on `jobs.stoyan.ovh` and `saxobeat.onrender.com`. After the owner's login: prod1 latest `last_login` 2026-10-29 10:04:09 UTC; old project's latest `last_login` still 2026-10-28 11:40:23 UTC, so the app writes to prod1 and not to the old project |
| 7 | Inbox shows the same jobs, second load under about 2 s | **pass** | Owner's check: "matches" and under about 2 s |
| 8 | `saxobeat-runner.cmd check` passes | **pass** | Output: "Checked: uv found. Hosted address in .env: yes.", exit 0 |
| 9 | A few hours later: the fallback's figure stopped moving, prod1's climbs slowly | **pass** (read 2026-10-30; the owner gave no clock time) | **Reading 2026-10-30 (owner): sum of all projects 4.89 GB; `saxobeat-fallback1` still "You've used 95.1%".** The old project did not move (95.1 % both days, resolution 0.05 % = 2.5 MB). **prod1 = 4.89 − 0.951 × 5 = 0.135 GB (about 135 MB, ±10 MB)**, which agrees with 4.89 − 4.76 = 0.13 GB. That is about 2.7 % of its 5 GB in roughly one day of web use only (the runner was not started); that day included the cycle 004 checks, so it is probably not a typical day. Cycle 001 uses it as a first observation of `W`. Earlier notes follow. | The owner's dashboard shows only **one figure: the sum of all projects** (the Projects page; no per-project figure was found there). **Per-project evidence, 2026-10-29 (owner):** the old project `saxobeat-fallback1` shows a banner **"You've used 95.1%"** of its 5 GB, that is about 4.755 GB, against a sum of 4.76 GB: so **virtually all the usage belongs to the old project, and prod1 is at about 0 to 10 MB** (rounding of both figures). It also confirms that the allowance is counted per project. Rollback headroom: the old project has only about 0.245 GB left until the next period. **Baseline reference: 4.76 GB, read by the owner on 2026-10-29 after the switch and the commits** (clock time not noted), with the old project's last read by us at about 10:05 UTC. Tomorrow's reading minus 4.76 GB = what prod1 used (web use only; the runner is not started), **assuming the fallback is not used**, which is assumed, not shown: nothing points at it any more (Render's login went to prod1; the runner is not run), and its rows and last login did not change after the switch (`evidence/counts_fallback_after_switch_2026-10-29.json`). prod1's own page shows no banner (it appears only from 80 %, per the owner), so **tomorrow: read the sum (two decimals) and the old project's percentage, with the time; prod1 = sum − percentage × 5 GB**, resolution about 15 MB. Expected for the old project: still 95.1 % |
| 10 | No connection string in the repo, a commit, the chat, or a command line | **pass** | A search of the repo (without `.env`, `data/`, `uv.lock`) finds only the public local example `postgres://saxobeat:saxobeat@localhost...` that was already there; `.env` and the dumps are gitignored; the evidence files hold counts only, no host. Strings travelled in environment variables, never on a command line |
| 11 | Rollback possible at every step | **pass** | Old string kept in `.env` as `SAXOBEAT_FALLBACK_DATABASE_URL`; rollback is Render's `DATABASE_URL` and `.env`'s `SAXOBEAT_HOSTED_DATABASE_URL` set back to it |

## Tests
No application code changed. The new script `scripts/db_counts.py` was tested by hand on the local database (counts, save, compare identical, compare with a deliberate difference, `--expect-empty` on a non-empty database, unset variable). It has no automated test in the suite.

## Not verified
- Whether 135 MB a day is typical for prod1 (one atypical day; cycle 001 slice 9 reads it daily).
- That Neon will not suspend prod1's compute for another reason, and how `Render` behaves over a full day: only the first hour was observed.
- The restore was not exercised through the app's own "restore" path, only through `pg_restore`.

## Verdict
- [x] Accepted by owner (2026-10-30, after criterion 9: 10 criteria passed, criterion 2 accepted as a risk)
- [ ] Sent back (what, to which stage)
