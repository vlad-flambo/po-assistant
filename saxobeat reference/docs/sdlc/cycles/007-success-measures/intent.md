# Intent: measure what the PRDs promised

| | |
|---|---|
| **Cycle** | 007 |
| **Stage** | Intent (drafted, nothing approved) |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Born from** | The PRD audit of 2026-10-29: outstanding items moved here from the PRDs (see the table below). |
| **Importance** | 3/5 (claude, 2026-10-30): without measures there is no way to tell whether the alpha works for friends |

## The request, in your words
> Do a full audit of the PRD files. I want to migrate anything outstandin into the ai sdlc framework, using the ai-sdlc skill

### What this cycle inherits from the PRDs
| Item | Where it came from |
|---|---|
| Precision ≥ 60 %, recall, triage under 5 minutes | PRD.md §2 |
| 5 active friends a month after the alpha, onboarding under 10 min, hosting under 15 USD a month | PRD_multi_user.md §13 |
| Alpha survey, freshness spot-check, referral rate; 50-badge precision spot-check; ingest time +<10 %; F10 sample of 100 ads (the test has about 40+40) | PRD_competitive_features.md §12, F2, F10 |
| Timed triage with two friends, phone share of visits | PRD_mobile.md §16 |
| Onboarding completion ≥ 80 %, median under 4 min, ≥ 95 % AI tasks on time, results opened within 2 days | PRD_ai_backoffice.md §16 |
| Picks acted on, AI-ready e-mails followed by a visit, resets without the operator | PRD_users_and_emails.md §13 |

## Why now / the pain
Every PRD sets success measures and none is measured; there is no way to tell whether the alpha works for friends.

## Goal
The few measures that matter are reported from data the app already stores, in one place the owner looks at.

## Success measure
A console page (or command) shows the chosen measures for the last 7 and 30 days, each with its definition, and the owner reads it once a week. *(draft, to confirm)*

## Not doing (this cycle)
- Tracking pixels or third-party analytics.
- Measures that need data the app does not store yet, unless the owner picks them.

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| The console's Today page already shows yesterday's AI on-time rate | PRD_ai_backoffice.md §9 |
| Status changes, onboarding times and AI task times are stored | `StatusChange`, `Candidate.onboarded_at`, `AiTask` |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Which measures first? | Five: onboarding completion and time, weekly active friends, AI tasks on time, picks shortlisted or applied per active friend, phone share of visits | | open |
| Q2 | E-mail open tracking? | No (privacy, and Apple's mail privacy makes it unreliable); count visits within a day of an e-mail instead | | open |
| Q3 | Phone share of visits: from what? | Render's request logs are not kept; store a daily count by device type in the app (no personal data) | | open |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Each extra query on hosted pages costs Neon transfer: compute measures in the PC runner or at most once a day.

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
