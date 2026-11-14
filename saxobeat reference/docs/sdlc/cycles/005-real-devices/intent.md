# Intent: real phones, real laptops, and a browser test harness

| | |
|---|---|
| **Cycle** | 005 |
| **Stage** | Intent (drafted, nothing approved) |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Born from** | The PRD audit of 2026-10-29: outstanding items moved here from the PRDs (see the table below). |
| **Importance** | 4/5 (claude, 2026-10-30): the phone is the main interface and was only simulated, never tried on a real device |

## The request, in your words
> Do a full audit of the PRD files. I want to migrate anything outstandin into the ai sdlc framework, using the ai-sdlc skill

### What this cycle inherits from the PRDs
| Item | Where it came from |
|---|---|
| Installing the app, swiping with a finger and the Android share target were only simulated | PRD_mobile.md progress row, §12 M5 |
| Playwright headless check decided (D6) but not installed | PRD_mobile.md §13 D6, §12 |
| Acceptance at 360×740 and 390×844: only 375 px was measured | PRD_mobile.md §14, §12 |
| Bring-your-own-AI copy and share sheet never checked on a real laptop and phone | PRD_ai_backoffice.md §12 'What was built' |
| The view-as band takes two lines on a phone | PRD_users_and_emails.md (this session's browser check) |

## Why now / the pain
The phone-first interface and the share-to-AI flow were built against a simulated phone; the clipboard and share sheet cannot be tested in the browser pane.

## Goal
Every phone flow the PRDs promise is checked on a real device, and the layouts are checked automatically at three phone sizes.

## Success measure
A checklist ticked on the owner's phone and laptop with screenshots in `evidence/`; a Playwright script in the repo that loads the main candidate pages at 360, 375 and 390 px wide on a local demo database and fails on a horizontal scroll or a missing element. *(draft, to confirm)*

## Not doing (this cycle)
- New phone gestures (cycle 010).
- Testing on the hosted database (use a local demo database).

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| `pyproject.toml`'s dev group has babel only: no Playwright | audit 2026-10-29 |
| A throwaway SQLite demo database with a test operator and candidate worked for browser checks in this session | this session (scratch scripts, not in the repo) |
| Share target and install prompt are in `jobs/views_pwa.py` and the manifest | `jobs/views_pwa.py` |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Which phone(s)? | The owner's own phone plus one friend's of the other OS, if one is willing | | open |
| Q2 | Playwright: in the repo as a dev tool, run by hand? | Yes: dev dependency, a `scripts/` entry point and a short README section; no CI (there is none) | | open |
| Q3 | Keep a demo-database seed script in the repo for these checks? | Yes, with test values only and an unusable password (sign-in by session) | | open |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Playwright downloads browsers (a few hundred MB): owner to agree before installing.

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
