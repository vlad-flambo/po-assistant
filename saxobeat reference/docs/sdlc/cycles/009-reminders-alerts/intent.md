# Intent: reminder and alert e-mails, and web push

| | |
|---|---|
| **Cycle** | 009 |
| **Stage** | Intent (drafted, nothing approved) |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Born from** | The PRD audit of 2026-10-29: outstanding items moved here from the PRDs (see the table below). |
| **Importance** | 3/5 (claude, 2026-10-30): reminders and alerts help every candidate; needs cycle 003 first |

## The request, in your words
> Do a full audit of the PRD files. I want to migrate anything outstandin into the ai sdlc framework, using the ai-sdlc skill

### What this cycle inherits from the PRDs
| Item | Where it came from |
|---|---|
| E-mails to the operator: new sign-up, source proposal, runner silent, files in problems, AI late (one morning summary) | PRD_users_and_emails.md register R1 |
| Reminder e-mails: follow-ups due, an interview tomorrow with the cheat sheet link | PRD_users_and_emails.md register R2 |
| Web push for the installed app | PRD_ai_backoffice.md register R4 |

## Why now / the pain
The operator learns about problems only by opening the console, and candidates miss follow-ups and interview preparation unless they open the app.

## Goal
The right person is told the right thing at the right time, without opening the app.

## Success measure
The operator gets one morning summary when something needs him; a candidate gets a reminder the day before an interview and when a follow-up is due; each can be switched off. *(draft, to confirm)*

## Not doing (this cycle)
- SMS.
- Making e-mail live (cycle 003, a prerequisite).

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| The outbox, dedupe keys, unsubscribe links and the runner's `mail send` step exist | `jobs/mail.py` |
| Follow-up dates and interview times are stored | `CandidateJob.follow_up_at`, `Interview.scheduled_at` |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Web push in this cycle? | No: e-mail first; push once friends install the app (cycle 005 tells) | | open |
| Q2 | Operator summary: daily or only when something is wrong? | Only when something needs action, at most once a day | | open |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Depends on cycle 003 (e-mail live).

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
