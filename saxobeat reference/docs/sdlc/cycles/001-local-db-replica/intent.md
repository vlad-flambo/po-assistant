# Intent: a local copy of the Neon database

| | |
|---|---|
| **Cycle** | 001 |
| **Stage** | Intent approved 2026-10-29; next: Spec (after cycle 002) |
| **Date** | 2026-10-28 |
| **Owner** | Vlad |
| **Importance** | 4/5 (claude, 2026-10-30): protects the hosting allowance (the runner's reads from Neon); most of it is already live |

## The request, in your words
> I have a hosted db on neon. Is there a way to keep a slave copy on my machine? Goal is to have an extra backup locally, and minimise the bandwith use for my runner processes.

## Why now / the pain
- Neon's free plan allows 5 GB of network transfer a month. In October 2026 the runner reached 84 % of it in six days (each run re-read the job texts for every candidate).
- Fixes of 28 October (counting in the database, word counts cached in `data\cache`, age rule as one update) cut a day's matching read from about 150 MB to under 5 MB. Expected total now: about 1.5 GB a month, mostly the weekly full backup (about 200 MB per read).
- **2026-10-28, from the owner:** still on the free plan, and already above 4.5 GB of the 5 GB for this month after only a few days. The cap may be reached before the month ends, with unknown consequences for the live app.
- **2026-10-29 10:05, one-off backup through the Neon address** (at the owner's request, for safety and as a possible migration source): `data/backups/saxobeat_2026-10-29_100546.dump`, 62.3 MB on disk, valid custom-format header, 38 tables with data. It read about 200 MB from Neon: note the Neon figure before and after to measure the real cost.
- Backups today: weekly `pg_dump` taken through the hosted address into `data/backups/` (last 8 kept). Neon's own point-in-time history on the free plan is short.

## Goal
Hold a second, local copy of the data that is (a) an extra backup under your control and (b) used by the runner so it reads less from Neon.

**Priority (Q1): less bandwidth first.** The local copy is judged by how much it cuts the runner's reads from Neon; being an extra backup is a bonus, not a requirement.

## Success measure
1. **Neon network transfer under 2.5 GB a month** (Q6), read from Neon's Network transfer figure over a full billing period, with the web app, the runner, `ai sync` and backups all counted.
2. *(Proposed, to confirm)* A restore drill: the local copy restores into an empty Postgres 17 and the app starts on it.

## Not doing (this cycle)
- Moving the web app off Neon or changing the database provider.
- A live, permanent replication connection (the runner is manual, Q4).
- A self-repairing copy (a rebuild is acceptable, Q5).
- Scheduling the runner again.
- Reducing the web app's own reads, unless the measurement shows it is a large share (Q7 working assumption: it is not).

## What we already know
| Fact | Source |
|------|--------|
| The runner (`scripts/pc_runner.ps1`) sets `DATABASE_URL` to the hosted address and does all its reading and writing there | `scripts/pc_runner.ps1` |
| Runner steps: `run_sources`, `purge_old_jobs --days 90`, `backup_database` (weekly), `ai sync`, `mail send`; scheduled every 3 hours | `scripts/pc_runner.ps1`, `docs/DEPLOY.md` §4 |
| A local Postgres 17 already exists via Docker Compose | `docker-compose.yml` |
| **Checked 2026-10-28 on this PC:** no Task Scheduler entry for the runner exists (all non-Microsoft tasks listed), and no runner process is running. So the runner is started by hand (`saxobeat-runner.cmd`, `saxobeat-ai.cmd`) or on another machine. `.env` here: `DATABASE_URL` points to localhost, `SAXOBEAT_HOSTED_DATABASE_URL` points to Neon, so development and tests do not touch Neon | read-only checks |
| Backup dumps in `data/backups/` (54 to 62 MB compressed, which means about 200 MB read each time): 22 Oct 19:06, 23 Oct 20:11, 26 Oct 10:43, 28 Oct 12:06 and 28 Oct 12:29. Which of them went through the Neon address is unknown. Two in one day contradicts the weekly rule (`--min-age-hours 168`), so at least one was made by hand | `data/backups/` listing, 2026-10-28 |
| No cache files in `data\cache`: the post-fix runner has probably not completed a run on this PC yet, so the 28 October fixes are **not yet measured in production** | `data\cache` listing, 2026-10-28 |
| Render's web service reads Neon on every request (`SAXOBEAT_RUN_SOURCES=0` there, it reads no sources) | `render.yaml` |
| Neon free: 0.5 GB storage (app uses about 180 MB), 100 compute hours a month, suspends after 5 idle minutes, 5 GB transfer a month | `docs/DEPLOY.md` |
| Neon supports logical replication as a publisher; there is no physical streaming replica to an outside server. Logical replication does not carry schema changes or sequences | Postgres/Neon documentation; **to be re-checked against Neon's current docs in the spec stage** |
| A connected subscriber may keep Neon's compute from suspending (compute hours), and an offline subscriber makes Neon hold changes (storage) | same, **to be verified** |
| The Free plan's 5 GB network transfer is per project and shared across Postgres, Object Storage and Functions. **Data sent through logical replication counts toward it**, so approach A spends the same 5 GB it is meant to save | [Neon plans](https://neon.com/docs/introduction/plans), fetched 2026-10-28 |
| When network transfer runs out, compute is suspended until the next billing period or an upgrade (existing connections drop, no new ones). The anchor date of the period is not stated in the docs | [Neon plans](https://neon.com/docs/introduction/plans); [free plan FAQ](https://neon.com/faqs/free-plan-limits-and-quotas) |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | Which goal comes first: a fresher backup than the weekly dump, or less bandwidth? | Bandwidth: the weekly dump already covers "a backup", a live replica earns its keep on reads | **Less bandwidth.** The local backup is a by-product, not the driver. The weekly dump stays as the backup. (2026-10-28) | answered |
| 2 | After the 28 October fixes, what does the runner still read from Neon that hurts (weekly backup, first-run word counts, big re-scores)? Is the transfer problem still real? | Measure a month first; if projected use is under 3 GB, a replica may be unnecessary | **Real.** Free plan, already over 4.5 GB of 5 GB this month "in a few days" (2026-10-28). **Most of it arrived before the 28 October fixes** (owner, 2026-10-28). Not yet known: the daily rate since the fixes. To measure: note the Neon figure now and again after 24 hours of normal running; that difference is the post-fix daily rate. | answered, post-fix rate to be measured |
| 3 | What replication lag is acceptable, given the runner writes jobs and then matches against them? | Matching reads local, writes go to Neon; accept lag of minutes only if matching never needs rows written seconds ago | **Acceptable** (owner, 2026-10-29): a run may work from a copy taken at its start; changes made on the web app during the run are picked up by the next run. Neon stays the source of truth. To check in the spec: effects that must be immediate (for example blocking an employer) must still hold at the next run. | answered |
| 4 | Is the PC always on? The runner runs every 3 hours | If not always on, avoid a permanent subscription: sync on demand at the start of a run | **The runner stays manual** (owner, 2026-10-29): started by hand, a few times a week at most. No permanent connection to Neon; any local copy catches up on demand at the start of a run. Scheduling it again is a later decision. | answered |
| 5 | If the local copy breaks, rebuild from a dump or must it self-heal? | Rebuild; simpler and the data is small (about 200 MB) | **Rebuild is fine** (owner, 2026-10-29), provided it is a single command. A rebuild reads about 200 MB from Neon, so it counts against the 2.5 GB budget. | answered |
| 6 | What is the success measure (GB a month, restore drill, both)? | Both: transfer under 2 GB a month and a restore drill that passes from the local copy | **Under 2.5 GB a month** of Neon network transfer (owner, 2026-10-29). The restore drill is proposed as a second check and is to be confirmed at the gate. | answered (drill to confirm) |
| 7 | Who else reads from Neon besides the runner? The web app on Render reads on every page, and `ai sync` and `mail send` run in the runner too. Neon's figure counts all of them | Find out the split before building anything: a replica that fixes the runner but not the web app does not meet the goal | Owner (2026-10-29): the dashboard only shows the last 24 hours, so no certainty, but it **looks like spikes when the runner is on**. Weak evidence: working assumption is that the runner side (runs, `ai sync`, backups) dominates, to be confirmed by the 24-hour measurement and by measuring the bytes a run reads on a local copy. | answered (working assumption) |
| 9 | How is the runner started in practice: by hand, or scheduled on another machine? How many full runs (and `ai sync` runs) since 22 Oct? | Count them: each pre-fix run read about 150 MB, so about 30 runs would explain 4.5 GB by themselves | **By hand** (owner, 2026-10-28). Traces on this PC: backup dumps on 22, 23, 26 Oct and **two on 28 Oct (12:06 and 12:28)**; AI job-screening files generated on 23, 26, 27 and 28 Oct (each `ai sync` read Neon); **no word-count cache files** in `data\cache`. **About 10 full runs** since 22 Oct (owner). Rough arithmetic, to be checked against the daily chart: about 10 pre-fix runs at about 150 MB is about 1.5 GB, plus about 4 backups at about 200 MB is about 0.8 GB, plus `ai sync` reads (size unknown): about 2.5 to 3 GB. That leaves **about 1.5 to 2 GB unexplained**: the web app on Render, `ai sync`, or runs that were bigger than estimated. | answered |
| 8 | When does the billing period reset, and what happens at 5 GB (compute blocked, app down)? Do we need a stopgap until then? | Stopgap now: pause the scheduled runner and the weekly backup until the reset | Reset date not shown in the dashboard; the project was created on 22 Oct, so the owner assumes the cycle anchors on the 22nd (**unverified**; next reset would be about 22 Nov, 25 days away). At the cap Neon's docs say compute is **suspended until the next billing period or until you upgrade**: the web app and the runner would both fail to connect. Data is not deleted. | answered; stopgap decision open |

Status: `open`, `answered`, `parked`.

## Constraints and risks
- Windows PC with Docker, runner scheduled in Task Scheduler.
- Neon free-plan caps (transfer, compute hours, storage); the connection string must never be pasted in chat or committed.
- Replica adds a moving part to maintain next to a runner that already works.

## Candidate approaches (not decided; for the spec stage)
- **A. Logical replication** Neon → local Postgres 17. Live, but ties up compute and needs DDL handled on both sides.
- **B. Scheduled refresh** of the local database from a dump (or table-level sync) at the start of a run. Simple, no permanent connection, higher cost per refresh.
- **C. Incremental pull** of only changed rows by a timestamp column into the local database. Cheapest on bandwidth, most code.
- **D. Do nothing new**: keep the weekly dump, restore drill only, watch the transfer figure for a month.
- **F. Stopgap: a fresh Neon project** (owner idea, 2026-10-29). **Taken, as its own [cycle 002](../002-fresh-neon-project/intent.md)**: new project `saxobeat-prod1` created, old one renamed `saxobeat-fallback1` and kept as a recovery copy. The Free plan's 5 GB is per project (Neon plans page), so a new project starts with a new allowance. It buys time and gives a clean baseline for the measurements; it does not reduce reads, so the problem returns. Needs: a current dump, restore into a new Postgres 17 project in Frankfurt (no pooler), then `DATABASE_URL` on Render and `SAXOBEAT_HOSTED_DATABASE_URL` in `.env`. Writes made on the web app between the dump and the switch would be lost. Not yet verified: how many free projects the plan allows, and whether a restore (data going in) counts toward transfer.
- **E. Upgrade the Neon plan**: lifts the cap and the suspension risk; it does not reduce reads. Cost to be checked on Neon's pricing page in the spec stage.

## Shortlist for the spec stage
*Revised 2026-10-29 by [decisions.md](decisions.md) D1, after a read-only map of the code: B and C (a local working copy that the runner writes through) are deferred, because most tables are written by both the runner and the web app, ids are auto-increment, there is no change timestamp, and deletions cascade. The spec ([spec.md](spec.md)) measures first, then reduces the specific heavy reads in code (R1 to R3), and keeps the full copy as a last resort. The list below is the original.*

- **A. Logical replication**: out (permanent connection, and its data counts toward the same 5 GB).
- **B. On-demand refresh of a local copy at the start of a run**: in.
- **C. Incremental pull of changed rows into the local copy**: in, as the likely refinement of B (a first fill reads about 200 MB, later runs only changes).
- **D. Do nothing new** (the 28 October fixes alone): kept as the baseline. Measure first: if one manual run plus a day of web use stays far below budget, the spec may reduce to measurement, a restore drill and fixing the backup rule.
- **E. Paid plan**: kept as the fallback if the budget cannot be met.

## Before the spec (measurements to take)
**Baseline reference (owner, 2026-10-29, after the move to `saxobeat-prod1`): 4.76 GB**, the sum of all projects on the Neon Projects page (the owner found no per-project figure). The old project's own page shows "You've used 95.1%" (about 4.755 GB): so at that moment **prod1 had used about nothing** (the whole sum was the old project's), and the October figure of 4.755 GB is the real cost of the first 7 days on the old project. Every later reading is compared with it; the difference is what prod1 used, as long as the old project (`saxobeat-fallback1`) is not read. Per-project figures: Neon's docs say each project's Overview page shows its own usage, and the project details API returns `data_transfer_bytes` on all plans (needs an API key, a secret: keep it out of chat and the repo).
1. Today's Neon Network transfer figure, and again after 24 hours of normal use (post-fix daily rate, web app included). Done as: 4.76 GB on 2026-10-29, then the reading of 2026-10-30.
2. Bytes one full manual run reads from Neon after the fixes, measured on a local copy as in the earlier work.
3. Bytes of `ai sync` and `mail send` per run.
4. Confirm the billing period reset date on Neon's billing page.

## Gate
- [x] All open questions answered or parked (Q1 to Q9; Q8 reset date still to confirm)
- [x] Goal and success measure confirmed by the owner (2026-10-29): under 2.5 GB a month of Neon transfer
- [x] Restore drill kept as a second success check (2026-10-29): the local copy restores into an empty Postgres 17 and the app starts on it
- [x] Owner approved the intent (2026-10-29). **Spec waits for cycle 002 (the move to `saxobeat-prod1`) and for the measurements above**, which start cleanly on the new project.
