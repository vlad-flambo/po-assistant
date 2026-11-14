# Intent: blocking an employer, an icon and a list where companies live

| | |
|---|---|
| **Cycle** | 016 |
| **Stage** | Intent (drafted 2026-10-29, for later; no question asked yet) |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Born from** | Cycle 004, slice 2: checking migration 0039's blocks on the hosted app ([evidence](../004-hosted-checks/evidence/blocks_0039.md)) |
| **Importance** | 2/5 (claude, 2026-10-30): blocking works; it is only hard to find and manage |

## The request, in your words
> seems to work fine
> however, I find the interface un-intuitive. -> start an intent file for later. it should be a block icon rather than text + manage the list in the Companies page rather than settings

## Why now / the pain
Blocking works (cycle 004 found no wrong block), but it is hard to find and to manage:
- on a job page, blocking is a small grey word "block" after the employer's name and "profile", easy to miss and to confuse with a link;
- the list of blocked employers is an accordion in Settings, away from the Companies page where a person thinks about employers.

## Goal
A person blocks an employer with one recognisable icon wherever the employer is shown, and sees and undoes their blocks on the Companies page.

## Success measure
*(draft, to confirm)*
1. A block icon (the same one everywhere, with a tooltip and an accessible name) replaces the text "block" on the job page, and the "⊘ Block" button on the company page.
2. The Companies page has a "Blocked" section or filter listing every blocked employer, with Unblock on each row; Settings no longer has the list (at most a link to it).
3. Blocking and unblocking still go through the existing pages (`companies/block/`, `companies/unblock/`): no change to what a block hides.
4. Works on a phone at 375 px (the icon is a 44 px touch target) and in French.

## Not doing (this cycle)
- Changing what a block does (whole employer, exact name, the similar-names list unticked by default: PRD_users_and_emails D-decisions stand).
- Undo after blocking (cycle 011 holds it); blocks as a signal for scoring (backlog R5).

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| Job page: `profile · block`, "block" a small muted text link to the confirm page | `jobs/templates/jobs/detail.html:8` |
| Company page: a "⊘ Block" button, or a red "Blocked" tag with Unblock | `jobs/templates/jobs/company.html:9-10` |
| Settings: "Blocked employers" accordion with a count and an Unblock per row | `jobs/templates/jobs/settings.html:142-148` |
| The Companies page exists (`/companies/`), with start and dream actions | `jobs/urls.py:38-45` |
| Blocking asks for confirmation on its own page (similar names offered, unticked) | `jobs/templates/jobs/block_employer.html` |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | Where should the icon appear: job page, company page, inbox cards, all three? | Job page and company page; not on inbox cards (a mis-tap there hides a whole employer) | | open |
| 2 | Does the icon still go to the confirm page, or block at once with an undo? | Keep the confirm page (it offers similar names); undo stays in cycle 011 | | open |
| 3 | On the Companies page: a section at the bottom, or a "Blocked" filter tab? | A filter tab, like the page's other lists | | open |
| 4 | Which icon? | A circle with a bar (⊘), the one the company page already uses | | open |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Standard-mode friends see a trimmed interface: the icon must fit there too (they block employers as well).
- Templates shared with other cycles (`detail.html`, `settings.html`) may be edited elsewhere at the same time: check before building.

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
