# Intent: finish the phone interactions

| | |
|---|---|
| **Cycle** | 010 |
| **Stage** | Intent (drafted, nothing approved) |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Born from** | The PRD audit of 2026-10-29: outstanding items moved here from the PRDs (see the table below). |
| **Importance** | 2/5 (claude, 2026-10-30): phone polish beyond the inbox; the phone already works |

## The request, in your words
> Do a full audit of the PRD files. I want to migrate anything outstandin into the ai sdlc framework, using the ai-sdlc skill

### What this cycle inherits from the PRDs
| Item | Where it came from |
|---|---|
| Long-press quick sheet on inbox cards (shortlist, dismiss, open, share) | PRD_mobile.md §7.1 |
| Swipe the pipeline list to change stage; long-press → Move to… | PRD_mobile.md §7.3 |
| To-do list: one-tap 'Followed up' and 'Not interested' | PRD_mobile.md §7.3 |
| Contacts as a searchable list of people | PRD_mobile.md §7.6 |

## Why now / the pain
The mobile PRD's interactions beyond the inbox swipe were not built.

## Goal
The pipeline and to-dos are as quick on a phone as the inbox.

## Success measure
Each interaction works on a real phone (cycle 005's checklist) and has a test; a to-do is cleared in one tap. *(draft, to confirm)*

## Not doing (this cycle)
- New pages.

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| `static/jobs/ui.js` handles horizontal swipe and button clicks only | audit 2026-10-29 |
| The pipeline uses `?stage=` links and a '⋯' menu | `pipeline.html` |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | All four, or the to-dos and pipeline first? | To-dos and pipeline first (daily use); long-press and contacts search after | | open |
| Q2 | Long-press on a laptop? | No: buttons are already there | | open |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Gestures that clash with scrolling: check on real phones (cycle 005).

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
