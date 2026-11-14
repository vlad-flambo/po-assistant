# Intent: keep score 50 meaning the same over time

| | |
|---|---|
| **Cycle** | 008 |
| **Stage** | Intent (drafted, nothing approved) |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Born from** | The PRD audit of 2026-10-29: outstanding items moved here from the PRDs (see the table below). |
| **Importance** | 3/5 (claude, 2026-10-30): score drift would slowly hurt every candidate, but it is not visible yet |

## The request, in your words
> Do a full audit of the PRD files. I want to migrate anything outstandin into the ai sdlc framework, using the ai-sdlc skill

### What this cycle inherits from the PRDs
| Item | Where it came from |
|---|---|
| Score calibration feedback loop: keep '50' meaning the same across candidates over time | PRD_ai_backoffice.md register R1, D15 |
| Screening brief drift as a search goes on | PRD_ai_backoffice.md register R2 |

## Why now / the pain
Calibration happens once, at onboarding; the job screening line (top share, minimum 50) and every comparison between people depend on it holding.

## Goal
Each candidate's share of jobs at 50 or more stays in the target band, and their screening brief follows what they actually do.

## Success measure
A per-candidate drift report (share at 50+, AI verdicts against the rules score near the line, dismiss and apply rates by band) and a re-tuning that brings a drifting candidate back into the band. *(draft, to confirm)*

## Not doing (this cycle)
- Changing the score formula itself.

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| Calibration recomputes up to 3,000 jobs in memory with proposed weights | `jobs/ai/calibration.py` |
| The applied-jobs benchmark holds a tuning that would miss more than 10 % of applied jobs | PRD_ai_backoffice.md §8.4 |

## Added 2026-11-04 (from cycle 021)
Scores shifted for every candidate when the bilingual glossary went live: French postings gained about 8 points on average for an English-profile candidate and 604 of 1,814 French inbox jobs of candidate 1 rose above the floor. Any calibration reading taken before 2026-11-04 compares scores made under the old rules (`docs/sdlc/cycles/021-bilingual-keyword-scoring/verify.md`).

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | What triggers a re-tuning? | Out of band for 7 days, or 10 dismissals of jobs the AI said to apply to; at most once a month per person | | open |
| Q2 | Automatic or through the operator? | Through the onboarding pack and the operator's preview, as today | | open |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Rescoring a broad candidate reads about 50 MB from Neon (cycle 001): run it in the runner.

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
