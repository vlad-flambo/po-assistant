# Learn: cut the runner's reads from Neon

| | |
|---|---|
| **Cycle** | 001 |
| **Stage** | Learn: drafted 2026-10-30, before the verdict; rows marked "later" wait for the seven days of readings |

## What happened vs what we expected
- **Goal (intent):** under 2.5 GB a month of Neon transfer with a 20 % margin (2,000 MB), runner kept manual, a restore drill kept as the second check. **Expected at the start:** a local copy of the database (the intent's B and C) would be needed.
- **What we found instead:** no local copy was needed. Measured on a scratch copy, a run by hand costs about **63 MB** (46 MB after the slim link lookup), a full backup 227 MB, so with the monthly backup the runner is **830 to 1,250 MB a month** at 3 to 5 runs a week. The one input still open is the web app's own rate (about 135 MB on one atypical day). Whether the whole stays under 2,000 MB is for criteria 4 and 9, with the owner's daily readings.
- **The restore drill passes** (the app starts on a restored dump: `/healthz`, the login page, 3 users, no migration pending).
- **Expected size of the work:** nine slices, three reductions. **Actual:** two small reductions plus a cadence change; the text cache and the local copy were never built.

## What we learned
- **Measure before building, and measure the steady state.** The code-based guesses were wrong in four places: `JobSource.raw` is 8.9 MB, not the bulk of a pass; digests cost 0.1 MB, not 129 MB a month; `ai sync` costs 0.1 MB, not 32 MB (the 32 MB was a cold cache plus one onboarding file); a local copy was not needed. The first reading of a step with a cache is its worst case.
- **The scarce resource was a cadence, not a volume.** The biggest single line was the weekly full backup (908 MB a month for 227 MB each); changing how often it runs removed more than any code change.
- **The web app was reading the same pool the runner was:** a standard-mode inbox page loaded the whole ranking pool with job texts (1.1 MB a page view; 0.15 MB since 30 October). Found by profiling by SQL statement, not by looking at the runner.
- **A narrower write is not always the same write:** deferring columns on a model changes what `save()` writes back. Two links to one job in a batch lost part of a change before and after; the new code loses less (4 of 31,968 jobs in a dense replay). A proper fix, one handling of a job per batch, belongs to a runner-correctness cycle.
- **The cap is per project** and the dashboard shows only the sum of all projects: a per-project reading is `sum − percentage × 5 GB` from the old project's banner.
- **A scratch copy of real data plus a guard script** made every measurement safe: three of three bad addresses refused, nothing touched Neon, no e-mail, no leftover.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| The runner's cost per run, the monthly backup, what the 29 October overrun was and was not, the restart | `docs/DEPLOY.md` §4 and §5 | [x] 2026-10-30 |
| The restart steps, stop rules and the optional prod1 dump | `evidence/restart_runbook.md` | [x] 2026-10-30 |
| The runner's backup cadence | `scripts/pc_runner.ps1` (`--min-age-hours 720 --keep 6`) | [x] |
| The measurement scripts (`measure_reads.ps1` and the `step_*` scripts) and `drill_check.py` | repo `README.md` file table (a short line: "measurement scripts for cycle 001") | [ ] later: with the verdict |
| State of the cycle, the standing rule and its lifting | project memory `project-sdlc-cycles` | [x] |
| "Measure the second run: the first run of a cached step is its worst case; and profile by statement before choosing what to reduce" | `.claude/skills/ai-sdlc/SKILL.md`, "Evidence over assertion" (owner to pick) | [ ] owner |
| The web rate `W` and the first measured whole run on prod1 | `evidence/projection.md` and `verify.md` | [ ] later: readings from 2026-10-31 |
| A runner fix for "one job handled once per batch" (the stale write-back) | `docs/sdlc/backlog.md` | [ ] later |
| The Esker (teamtailor) source fails on every pass | `docs/sdlc/backlog.md` or cycle 013 | [ ] later |
| `calibration.visible_views` loads job texts the onboarding file does not use (about 12 MB per onboarding file) | `docs/sdlc/backlog.md` | [ ] later |

## Process feedback
- **Worked well:** grill-me with a recommended answer kept each decision one question long; writing every number into `evidence/` the moment it was measured made two later corrections (ai sync, digests) easy to make and to show; the guard script made it possible to say "go on" without fear.
- **Slowed us down:** my first projection used numbers that turned out to be first-run costs; a profile by statement should come before a projection, not after. The cycle README table is edited by two sessions at once: staging only one's own row by hand worked but is fragile.
- **To improve the playbook:** a "steady state vs first run" check in the evidence rules (above), and a standing line in `next.md` for observations that need days (the daily reading) so the cycle can be drafted as done-except-observation.

## Next cycle candidates
- The runner fix for one job per batch (a stale write-back when two links point to one job).
- Esker (teamtailor) source failing on every pass (with cycle 013, more sources).
- Making the runner scheduled again once a week of readings agrees (a small cycle, or part of this one's slice 10).
- A per-project Neon reading without the old project's banner (if Neon ever shows it).
