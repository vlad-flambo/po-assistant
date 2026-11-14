# Intent: runner and data correctness

| | |
|---|---|
| **Cycle** | 014 |
| **Stage** | Intent approved 2026-10-29; Spec drafted ([spec.md](spec.md)) |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Born from** | The PRD audit of 2026-10-29: outstanding items moved here from the PRDs (see the table below). |
| **Importance** | 5/5 (claude, 2026-10-30): six windows where data could be overwritten; closed |

## The request, in your words
> Do a full audit of the PRD files. I want to migrate anything outstandin into the ai sdlc framework, using the ai-sdlc skill

### What this cycle inherits from the PRDs
| Item | Where it came from |
|---|---|
| `matching.expire` has no status guard: a runner pass can overwrite a status the candidate changed meanwhile | cycle 001 finding (project memory) |
| The backup test fails on SQLite/Windows: two backups in one second get the same file name | project memory 'Running tests'; this session's test runs (it passes on Postgres) |

## Why now / the pain
The runner and the web app both write the same rows; a lost update is silent. A test that always fails hides new failures.

## Goal
No runner pass undoes a candidate's change, and the test suite is green on both databases.

## Success measure
A test reproduces the overwrite and passes after the fix; the full suite passes on SQLite and Postgres. *(draft, to confirm)*

## Not doing (this cycle)
- A local working copy of the database (cycle 001 D1).

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| Runner and web write the key tables; ids are auto-increment; no change timestamps | cycle 001 spec |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Other overwrite windows to look for in this cycle? | Yes: review every bulk `update()` the runner makes on `CandidateJob` | Accepted as recommended (2026-10-29) | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- None known yet.

## Gate
- [x] All open questions answered or parked (2026-10-29)
- [x] Goal and success measure confirmed by the owner (2026-10-29, as drafted)
