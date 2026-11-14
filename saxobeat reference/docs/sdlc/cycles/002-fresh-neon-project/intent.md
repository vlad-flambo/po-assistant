# Intent: move to a fresh Neon project, keep the old one as a fallback

| | |
|---|---|
| **Cycle** | 002 |
| **Stage** | Intent approved 2026-10-29; Spec drafted ([spec.md](spec.md)) |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Born from** | [Cycle 001](../001-local-db-replica/intent.md), option F. Cycle 001 stays about cutting reads; this cycle is the move itself. |
| **Importance** | 5/5 (claude, 2026-10-30): moved off the nearly full Neon project (old one at 95.1 %); closed |

## The request, in your words
> I created the new db, project named saxobeat-prod1. [...] I think I'll keep the other db, and treat it as a recovery solution. Renamed to "saxobeat-fallback1". Inactive for now.

## Why now / the pain
- The old project had already used more than 4.5 GB of its 5 GB monthly transfer, with about 25 days to the next period (reset date unverified). At the cap Neon suspends compute until the next period or an upgrade, which would take the web app and the runner down.
- Neon's Free plan allowance is per project, so a new project starts with a new 5 GB.

## Goal
Run Saxobeat on `saxobeat-prod1` with the data intact and no loss of service the owner would notice, keeping `saxobeat-fallback1` (the old project) untouched as a recovery copy.

## Success measure
The nine checks in Q5 all pass: Render serves from `saxobeat-prod1` with the same data as the 10:05 dump, the runner's `check` passes, the fallback stops being read, and prod1's transfer figure is tracked daily from near zero.

## Not doing (this cycle)
- Reducing the reads themselves (cycle 001).
- Deleting the fallback project.
- Moving off Neon.

## What we already know
| Fact | Source |
|------|--------|
| New project: `saxobeat-prod1`. Old project renamed `saxobeat-fallback1`, inactive for now | owner, 2026-10-29 |
| Renaming a project should not change its connection string; to confirm when the strings are checked | to verify |
| Source for the data: `data/backups/saxobeat_2026-10-29_100546.dump` (taken 10:05, valid, 38 tables with data); anything changed on the web app since is not in it | cycle 001 notes |
| Restore command: `pg_restore --clean --if-exists --no-owner -d "<url>" <file>` (via Docker `postgres:17`), as in `docs/DEPLOY.md` | `docs/DEPLOY.md` |
| What changes at the switch: `DATABASE_URL` on Render (no `-pooler` host) and `SAXOBEAT_HOSTED_DATABASE_URL` in `.env`. Render's start script applies migrations on boot | `render.yaml`, `scripts/entrypoint.sh`, `.env` |
| The two projects must be both Postgres 17 for the dump tools; to confirm that prod1 is on 17 and in Frankfurt | to verify |
| Connection strings never go in chat or the repo | `docs/DEPLOY.md` |

## Open questions (to grill later)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | Restore from the 10:05 dump, or take a fresh one right before the switch? | A fresh one right before, to shrink the loss window; the old project has little transfer left, so it is a one-time 200 MB read | **Restore the 10:05 dump** (`saxobeat_2026-10-29_100546.dump`), accepting the loss of anything changed on the web app after 10:05 on 2026-10-29 (owner decision against the recommendation). No further read from the old project is needed. | answered |
| 2 | How is data loss between dump and switch handled (the web app is live, others may triage)? | Do dump, restore and Render switch in one sitting, accept a short gap; no maintenance page | **Only the owner uses the live app** (2026-10-29), so the loss since 10:05 is limited to the owner's own changes, which can be redone. Restore and Render switch in one sitting, no maintenance page, no notice to anyone. | answered |
| 3 | What does "inactive" mean for the fallback: Render and the runner no longer point at it, and nothing reads it | After the switch, confirm in the fallback's monitoring that reads stop | **Accepted as recommended** (2026-10-29): after the switch Render and `.env` no longer point at `saxobeat-fallback1`; confirmed by its transfer figure no longer moving, not by the rename. | answered |
| 4 | When is the fallback refreshed, or retired? | Never refreshed; kept as a snapshot until prod1 has a clean month, then decide | **Accepted as recommended** (2026-10-29): never refreshed; a snapshot of 2026-10-29 10:05 until prod1 has a clean month, then delete it or replace it with a newer dump. | answered |
| 5 | What are the checks before and after the switch (row counts per table, a login, the Inbox, the runner `check`)? | A short list in the spec, with counts compared old vs new | **Accepted as proposed** (2026-10-29), nine checks, to become the spec's acceptance criteria: (before) 1 prod1 is Postgres 17, Frankfurt, no `-pooler` host; 2 old connection strings saved outside the repo; 3 the 10:05 dump on disk and the old project's row counts per table noted. (after the restore, before Render) 4 row counts per table match; 5 prod1's transfer figure still near zero. (after the switch) 6 `/healthz` ok and login as `vlad`; 7 the Inbox shows the same jobs, second page load under about 2 s; 8 `saxobeat-runner.cmd check` passes (a full run waits for cycle 001's measurements); 9 a few hours later the fallback's figure no longer moves and prod1's climbs slowly. | answered |
| 6 | Does Neon allow this many free projects, and does restore data count as transfer? | Check on Neon's pages; read prod1's transfer figure right after the restore | **Looked up 2026-10-29.** The Free plan allows 100 projects, and each has its own allowances (5 GB transfer, 100 CU-hours); the page does not discuss creating several free projects on purpose. Only **outbound** traffic counts as public network transfer ([network transfer](https://neon.com/docs/introduction/network-transfer)), so a `pg_restore` into prod1 should not count; to confirm by reading prod1's figure right after the restore. An app connecting from Render likely counts as egress (not stated explicitly). | answered, confirm after the restore |
| 7 | Rollback: if prod1 misbehaves, switch Render and `.env` back to the fallback | Keep the old strings noted outside the repo; rollback is the same two edits in reverse | **Accepted as recommended** (2026-10-29): rollback is the same two edits in reverse (`DATABASE_URL` on Render, `SAXOBEAT_HOSTED_DATABASE_URL` in `.env`). The owner keeps the old connection strings outside the repo (for example a password manager) *before* the switch. After a rollback the fallback is behind prod1. | answered |

## Gate
- [x] Open questions answered or parked (Q1 to Q7; Q6's restore-cost confirmation happens after the restore)
- [x] Goal and success measure confirmed by the owner (2026-10-29)
- [x] Owner approved moving to the spec stage (2026-10-29)
