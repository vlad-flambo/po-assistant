# Intent: Cloud runner for sources

| | |
|---|---|
| **Cycle** | 026 |
| **Stage** | Intent |
| **Date** | 2026-11-05 |
| **Owner** | Vladimir Stoyanov |
| **Importance** | 3/5 (claude, 2026-11-05): the PC must be on and the owner present for each run; but the binding limit today is Neon's 5 GB transfer, not the PC, and datacenter addresses may be refused by the job sites (unverified) |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
Part of the 2026-11-05 request (full text in cycle 025): "I want to run everything on the cloud. ... This includes: runner pc, be able to trigger this on a dedicated Render instance. The free tier is probably going to be ok for ad-hoc runs. Should this be a separate repo or app? Or do I just deploy the app a second time on a separate instance with ability to do the runs, pointing to same db? Open to suggestions on this."

## Why now / the pain
- Sources are read only by `scripts/pc_runner.ps1` on the owner's PC, started by hand a few times a week ("no task is scheduled", DEPLOY.md §4). The PC has to be on and the owner at it.
- The design choice behind that: the web app never fetches (`SAXOBEAT_RUN_SOURCES=0`) so the job sites never see a datacenter address (DEPLOY.md, `config/settings.py:146`). Moving the runner to the cloud **reverses that choice**, so the first thing to learn is whether the sites still answer.

## Goal
Sources are read, and the database kept tidy (purge, auto-reject, backup, mail), by a cloud job that the owner can start on demand from a phone and, later, on a schedule, without the PC.

## Success measure
1. One run started from the cloud reads the same sources as a PC run and writes the same kinds of rows (compared on pre-prod, not prod): same per-source outcome list, same counts within a stated tolerance.
2. Per source, whether it answers from a datacenter address is measured and written down; any source that refuses is listed with its error.
3. The owner starts a run with one action (button, link or command) from a device that is not the PC.
4. The cost in Neon transfer per run equals the PC's (about 46 to 63 MB, cycle 001) or the difference is explained.

## Not doing (this cycle)
- The AI step (027).
- Running more often than the Neon cap allows: cadence stays the owner's call (cycle 001's runbook).
- Rotating addresses, proxies or anything meant to hide that the reader is a script (the project's rule is to respect each site's robots.txt and terms, "Robots first").

## What we already know (facts, with where they came from)
- The runner steps (`pc_runner.ps1`): `run_sources`, `purge_old_jobs --days 90`, `auto_reject`, `backup_database` (monthly; needs Docker or `pg_dump`, writes `data/backups/` on the PC), `ai sync`, `mail send`.
- An HTTP trigger already exists: `POST /cron/run/` with a bearer token (`SAXOBEAT_CRON_TOKEN`) starts a background run on an instance that has `SAXOBEAT_RUN_SOURCES=1` (`jobs/views.py:896`, written for "an external scheduler"). It runs in a thread inside the web process, so a sleeping or restarted free instance can lose it.
- Render **free** web services cannot run one-off jobs and, as far as the docs say, cron jobs and background workers are not free (render.com/docs/free, read 2026-11-05; the price of a cron job is to be checked). Free services sleep after 15 idle minutes.
- Options to compare (my read, all unverified until a spike):

  | | Where it runs | Free? | Trigger | Catch |
  |---|---|---|---|---|
  | A | GitHub Actions, same repo (`workflow_dispatch` and `schedule`) | yes, within its minutes allowance | a button in GitHub, its phone app, or the API | datacenter address (Azure); runs `manage.py` directly, no web service; secrets kept in GitHub |
  | B | A second Render web service from the same image, `SAXOBEAT_RUN_SOURCES=1`, driven by `/cron/run/` | free plan, may sleep | any HTTP call | thread lost on restart; datacenter address; a second public service to protect |
  | C | A Render cron job from the same image | paid (to check) | schedule or manual | cost, plus a datacenter address |
  | D | Stay on the PC | free | by hand | the PC |

- **A separate repo is not needed**: the runner is `manage.py` commands of this same app and image (`Dockerfile`), so a second repo would copy code and drift. A second *deployment* of the same image is enough (option B or C), pointing at the same database as prod, or at pre-prod's for rehearsal.
- Neon counts reads whether they come from the PC or from a cloud job (public network transfer, 5 GB per project a month).

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | Is reading the sites from a datacenter address acceptable to you (it reverses a stated design choice)? | Yes, but only after a read-only spike on pre-prod shows which sources answer; any source that blocks stays on the PC or is switched off. | | open |
| 2 | Which option: A (GitHub Actions), B (second free Render service), C (Render cron)? | A first: free, no extra public service, one-tap trigger; B only if you want to stay on Render. | | open |
| 3 | Scheduled or only on demand? | On demand first (the Neon cap decides cadence); a schedule once a week of readings agrees. | | open |
| 4 | The monthly backup: where does the dump go from a cloud job? | Keep it a PC task for now (it needs a place to keep the file); revisit with object storage. | | open |

## Constraints and risks
- Depends on 025: the spike and the rehearsal need pre-prod and its own database.
- A secret in a cloud job (the database address) must be a secret of that service, never in the repo or on a command line (PROJECT.md).
- A datacenter address may be refused or rate-limited by some sources (unverified).

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
