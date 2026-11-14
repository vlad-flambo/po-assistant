# Intent: settings and small interface gaps

| | |
|---|---|
| **Cycle** | 011 |
| **Stage** | Intent (drafted, nothing approved) |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Born from** | The PRD audit of 2026-10-29: outstanding items moved here from the PRDs (see the table below). |
| **Importance** | 2/5 (claude, 2026-10-30): small gaps, each one minor |

## The request, in your words
> Do a full audit of the PRD files. I want to migrate anything outstandin into the ai sdlc framework, using the ai-sdlc skill

### What this cycle inherits from the PRDs
| Item | Where it came from |
|---|---|
| Keyword weights as chips with a weight control (still `term: weight` text boxes) | PRD_ai_backoffice.md §7, §12 'What was built' |
| Per-candidate AI weight (one global setting today) | PRD_ai_backoffice.md §12 |
| Focus cap adjustable 1-5 (`LIMIT = 3`) | PRD_competitive_features.md §11 decision 2, F7 |
| Breadth: preview how many jobs each level shows | PRD_competitive_features.md F4 risk row |
| Inbox remote filter | PRD.md §7.1 |
| 5-second Undo after blocking an employer | PRD_users_and_emails.md §5.1, §9 |
| A dot on the tab when an AI result is ready | PRD_ai_backoffice.md §6.3, §12 |
| French amounts written the French way (55 000 €, not €55-65k) | PRD_competitive_features.md F13 |
| A nicer HTML e-mail (links behind words, job cards) | PRD_users_and_emails.md §9 |

## Why now / the pain
Small gaps left from four PRDs; each is minor, together they are what a friend notices.

## Goal
Close the small interface gaps the PRDs promised, in one pass.

## Success measure
Each item is either built with a test or explicitly dropped by the owner in `decisions.md`. *(draft, to confirm)*

## Not doing (this cycle)
- Anything that changes the score formula.

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| Standard mode hides the keyword settings: chips matter for power users only | PRD_users_and_emails.md §4.5 |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Which of the nine items to do, which to drop? | Do: undo after block, tab dot, French amounts, remote filter, nicer e-mail. Drop: per-candidate AI weight. Later: keyword chips, focus cap, breadth preview | | open |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- None known yet.

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
