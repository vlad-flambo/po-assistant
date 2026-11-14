# Intent: import job-alert e-mails (LinkedIn, WTTJ, APEC, Indeed)

| | |
|---|---|
| **Cycle** | 018 |
| **Stage** | Intent (drafted 2026-10-30, for later; no question asked yet) |
| **Date** | 2026-10-30 |
| **Owner** | Vlad |
| **Born from** | Cycle 013, question Q2: the owner moved it out and called it low priority |
| **Importance** | 2/5 (owner, 2026-10-30): low priority, because it would need a complex e-mail access set-up for each user |

## The request, in your words
> move step 2 as a separate intent. I'd say low priority as it would require complex email access set up for users

## Why now / the pain
LinkedIn, Indeed, APEC and (for the rest of its jobs) Welcome to the Jungle publish no feed, only alert e-mails. The PRD planned three ways to use them; none is built. Not urgent: the catalogue gets jobs from employers' own boards.

## Goal
Bring the jobs from alert e-mails into the inbox without giving the app standing access to a mailbox.

## Success measure
*(to be set when the cycle is picked up)* for example: the share of imported alert jobs that are new to the catalogue, and the minutes a person spends per week.

## Not doing (this cycle)
- Standing access to a person's main mailbox (PRD.md §5: answered, no).
- Bypassing any anti-bot protection (a standing rule).

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| Three options: (1) upload or paste an alert e-mail, per-sender parsers; (2) a supervised Claude session with the person's own Gmail connector writes a `saxobeat.jobs.v1` file; (3) a forward-only mailbox read over IMAP | PRD.md §5 'Alert emails' |
| PRD recommended option 1 first; option 3 "not planned unless 1 and 2 prove too manual" | PRD.md §5 |
| Alerts carry title, company, place and link, not the description | PRD.md §5 |
| Pasting a single job link into the inbox already works (and sharing a link on Android) | PRD_mobile.md M5 |
| The owner's reason for low priority: every user would need an e-mail access set-up | owner, 2026-10-30 |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Which of the three options (PRD.md §13 Q6)? | Option 1, paste or upload: no access set-up for anyone, and per-sender parsers can start with LinkedIn and WTTJ | | open |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Each platform's alert format can change without notice; terms of each platform to be reviewed before a parser is built.

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
