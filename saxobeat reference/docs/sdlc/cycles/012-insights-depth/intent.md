# Intent: what my applications teach me (the rest of F11)

| | |
|---|---|
| **Cycle** | 012 |
| **Stage** | Intent (drafted, nothing approved) |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Born from** | The PRD audit of 2026-10-29: outstanding items moved here from the PRDs (see the table below). |
| **Importance** | 2/5 (claude, 2026-10-30): Insights is power mode only; the funnel already exists |

## The request, in your words
> Do a full audit of the PRD files. I want to migrate anything outstandin into the ai sdlc framework, using the ai-sdlc skill

### What this cycle inherits from the PRDs
| Item | Where it came from |
|---|---|
| Breakdowns by score band, source kind, channel, company size, focus job, and a plain sentence | PRD_competitive_features.md §5 F11 status line |

## Why now / the pain
Only the funnel and delays exist; the breakdowns that say what works are not built.

## Goal
A candidate sees which kinds of applications get answers, in one plain sentence and a few numbers.

## Success measure
The Insights page shows the five breakdowns with the small-sample warning (`SMALL_SAMPLE = 15`) and one sentence; tests cover a small and a large sample. *(draft, to confirm)*

## Not doing (this cycle)
- Standard mode (Insights is power only).

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| `services/pipeline_stats.py` has the funnel and delays, `SMALL_SAMPLE = 15` | audit 2026-10-29 |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Worth it now, with few applications per friend? | Later: after cycle 007 shows enough applications; keep the cycle at Intent | | open |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- None known yet.

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
