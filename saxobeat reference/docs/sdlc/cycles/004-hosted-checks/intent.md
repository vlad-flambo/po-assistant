# Intent: check the hosted app after the 28 October deploys

| | |
|---|---|
| **Cycle** | 004 |
| **Stage** | Intent approved 2026-10-29; Spec drafted ([spec.md](spec.md)) |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Born from** | The PRD audit of 2026-10-29: outstanding items moved here from the PRDs (see the table below). |
| **Importance** | 4/5 (claude, 2026-10-30): proved the hosted app works (migrations, backups, speed); closed |

## The request, in your words
> Do a full audit of the PRD files. I want to migrate anything outstandin into the ai sdlc framework, using the ai-sdlc skill

### What this cycle inherits from the PRDs
| Item | Where it came from |
|---|---|
| Pages under 2 s on the hosted app: never measured | PRD.md §10; PRD_multi_user.md §10 phase 4; PRD_competitive_features.md §8 |
| Migrations 0037-0040 ran on the hosted database; migration 0039's log of what the old blocked list now blocks; friends shown in standard mode | PRD_users_and_emails.md §9; this session's push of 28 October |
| Neon's restore history length (how far back a point-in-time restore goes) | PRD.md §12 'Data loss'; DEPLOY.md |
| The AI back office 'not yet run on the hosted app or with a real agent' | PRD_ai_backoffice.md status line |
| DEPLOY.md's 'Not verified yet' section is dated 23 October | DEPLOY.md, end |

## Why now / the pain
Five deploys landed on 28 October (modes, view-as, blocked employers, e-mail, Starter plan) and the speed target has never been measured anywhere; the PRDs still call several things 'not verified'.

## Goal
Know, with evidence, that the hosted app is fast enough, fully migrated and recoverable, and that the AI hand-off works end to end there.

## Success measure
A table of second-load times for six pages, each under 2 s or explained; the migration list ends at 0040; migration 0039's log read; the restore window recorded; one AI pack exported, processed by an agent and imported on the hosted app. *(draft, to confirm)*

## Not doing (this cycle)
- Reducing Neon reads (cycle 001).
- Real-phone checks (cycle 005).

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| Render is on the Starter plan (never sleeps) since 28 October; Neon's free compute still pauses after about 5 idle minutes | `render.yaml`, DEPLOY.md |
| The live database is `saxobeat-prod1` since 29 October; the old project is a fallback that must not be read | cycle 002, project memory |
| Every read from Neon counts against 5 GB a month: page timings move kilobytes, a full check of all tables does not | cycle 001 and 002 |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Which pages, measured how? | Second load of inbox, job page, pipeline, settings, console Today and Candidates, in the browser's network panel, as the operator and as a standard friend (view as) | Accepted as recommended (2026-10-29) | answered |
| Q2 | Has an AI pack already gone through a real agent on the hosted app? | Owner knows: if yes, record when; if no, one small onboarding or screening pack is enough | Yes: done on 2026-10-28, none since (owner, 2026-10-29). The criterion becomes a record from the console's Exports and Import history, not a new run | answered |
| Q3 | Do the checks wait for cycle 001's 7-day observation? | No for page timings (they move kilobytes); yes for anything that reads whole tables | Accepted as recommended (2026-10-29) | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Reads during cycle 001's observation window blur its baseline: keep these checks small and log them in cycle 001's plan.

## Gate
- [x] All open questions answered or parked (2026-10-29)
- [x] Goal and success measure confirmed by the owner (2026-10-29, as drafted)
