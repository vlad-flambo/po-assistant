# Intent: simplify-ops-console

| | |
|---|---|
| **Cycle** | 024 |
| **Stage** | Intent |
| **Date** | 2026-11-04 |
| **Owner** | Vladimir Stoyanov |
| **Importance** | 3/5 (owner, 2026-11-04): set by the owner, no reason given (claude had 2/5: one user, no evidence of a loss; the owner uses the Console daily) |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
> simplify the ops view
> https://app.saxobeat.fr/ops/
>
> right now, too many sections, unclear what does what, probably a few legacy views that need cleanup

## Why now / the pain
Too many sections in the Console, no clear line between them, and some pages that are probably leftovers. (No count of visits or mistakes exists; the pain is the owner's own.)

## Goal
The operator opens the Console and sees a few clearly named areas, each with one obvious job: Today · Candidates · Sources · Runs · Feedback · AI · More. Pages that duplicate another are folded into it, and the daily page (Today) leads with the daily items.

## Success measure
*(answers to Q4 to Q6 accepted 2026-11-04; the owner's approval of the whole intent is the open gate line)*
1. The top bar has 7 entries (Today, Candidates, Sources, Runs, Feedback, AI, More), down from 14.
2. Every page has a one-line "what this is for" under its title, and no two pages show the same thing (Import's "Recent exports" table and the Exports page, for instance).
3. Every old `/ops/...` address redirects to its new home: none returns "not found".
4. Today leads with the daily items (failing sources, proposals to decide, new feedback, new candidates, last run, Refresh now); its AI part is one line linking to the AI view.
5. No function is lost: everything that could be done before can still be done (Jungle radar through Sources; Exports, Auto-reject, E-mails and Data & backups through More; Export, Import, queue and settings through AI).
6. The test suite passes.

## Not doing (this cycle)
- Deleting code or retiring a page (decision Q4): pages are folded and redirected; code is deleted only for a page the owner later calls dead.
- Changing what the AI hand-off, sources or e-mail features do (only where they are shown).
- The candidate app (Inbox, Pipeline, Settings...): this is the operator space only.
- Translating the Console (it stays English on purpose, PRD_competitive_features §8).

## What we already know (facts, with where they came from)
*Read from the code on 2026-11-04 (`jobs/templates/jobs/ops/base.html`, `jobs/urls.py`, `jobs/views_ops.py`, each template). The live site needs a login, so nothing was read from it.*

- **The top bar has 14 entries** (plus "← Candidate app" and "Log out"): Today, Export, Import, AI queue, Exports, AI settings, Auto-reject, Candidates, E-mails, Feedback, Sources, Runs, Jungle radar, Data & backups.
- **What each page does:**

| Page | Does | Overlap or doubt |
|---|---|---|
| Today | AI counts per pack, PC runner folder, last source run, proposals, candidate count, failing sources, "Refresh now" | repeats bits of Export, Sources, Runs, Candidates |
| Export | pick candidates and packs, preview, download the AI files | the AI hand-off is 5 pages: Export, Import, AI queue, Exports, AI settings |
| Import | upload results, preview, apply; also a "Recent exports" table | the table duplicates the Exports page |
| AI queue | filterable task list, cancel / requeue | |
| Exports | history of exports, "send the outstanding again" | duplicated by Import's table |
| AI settings (+ Instructions, linked only from it) | pause, screening thresholds, calibration, PC runner switches | the screening thresholds also appear in Export's "Job screening settings"; pause also on Today |
| Auto-reject | one number (days before a silent application is rejected) | not AI at all; a whole nav entry for one field (cycle 019) |
| Candidates (`/ops/people/`) | invite, accounts, mode, view-as, reset, delete, view-as log, invitations | page title says "People", nav says "Candidates" |
| E-mails | counts, send now, pause, test, log | |
| Feedback | the in-app feedback chats | |
| Sources | 11 stat tiles, proposals to decide, add a source, the list | stats tiles overlap Today and Runs |
| Runs | one table of runs | failures already shown on Today and Sources |
| Jungle radar | Welcome to the Jungle employer radar and slow page reading | template last changed 2026-10-09 (the radar rework); the Sources page says it "is not listed here" |
| Data & backups | download or restore a full backup | a single-user-era feature; the hosted database is backed up daily by the PC runner (page's own text); template last changed 2026-10-06 |

- The Console was built in one go on 2026-10-23 as the AI back-office (A0); Feedback, E-mails, Candidates and Auto-reject were bolted on as flat nav entries in cycles since (git log of `ops/base.html`).
- Tests touch the console URLs (`tests/test_auto_reject_console.py`, `test_ai_running.py`, `test_accounts.py` and others), so renaming URLs means updating tests; the old addresses can stay as redirects.
- The `/ops/` addresses are linked from the candidate app only through the "Console" link (base.html, more.html).
- **Usage (owner, 2026-11-04):** daily Today, Candidates, Sources, Runs, Feedback; weekly Export, Import; the other seven were not named. So the daily surface is sources, people and feedback, and the AI hand-off is a weekly job. Today, the daily page, leads with the AI section (the weekly work), while its daily items (failing sources, proposals, new feedback) are at the bottom or absent.
- The PC runner scripts (`scripts/*.ps1`, `*.cmd` in the repo root) contain no `/ops/` address (grep, 2026-11-04); a bookmark of the owner's is the remaining unknown.

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | Which pages do you really open: daily, weekly, almost never? | Daily: Today, Export, Import. Weekly: Candidates, Sources, Feedback. Rare: the rest (AI queue, Exports, Auto-reject, E-mails, Runs, Jungle radar, Data) | Owner, 2026-11-04. **Daily:** Today, Candidates, Sources, Runs, Feedback. **Weekly:** Export, Import. Not named (so read as rare or never, to confirm in Q2): AI queue, Exports, AI settings, Auto-reject, E-mails, Jungle radar, Data & backups. | answered |
| 2 | Which pages are the legacy ones you suspected? | Jungle radar and Data & backups, plus Exports (duplicated by Import) | Owner, 2026-11-04: nothing is to be retired outright. **(a)** everything about AI goes in a single view; **(b)** Jungle radar becomes a view reached through Sources; **(c)** Data & backups and Exports are bundled with the other rarely used views, such as E-mails. | answered |
| 3 | The AI view: one page with sections, or one top-bar entry with sub-tabs (Export, Import, Queue, Settings)? | One entry "AI" with a status strip on top (counts, pause, runner folder, on time) and sub-tabs below; each tab keeps its own address, so tests and the runner's links are untouched | Owner, 2026-11-04: "Yes, as proposed". | answered |
| 3b | Where do Auto-reject, Exports and the Instructions page go? | Auto-reject (not AI) and Exports (your word: with the rare views) go in the rare bundle; Instructions stays inside the AI view's Settings tab | Owner, 2026-11-04: "Yes, as proposed". | answered |
| 4 | Retire for real (delete code) or only hide and fold? | Fold and hide first; delete code only for pages you say are dead; old addresses redirect | Owner, 2026-11-04: accepted. | answered |
| 5 | Success measure: with the agreed bar (Today · Candidates · Sources · Runs · Feedback · AI · More) it is at most 7 top entries, not 6; plus a one-line purpose on every page. Right? | Yes: 7 entries, a one-line purpose under each page title, no old address answers "not found" (each redirects), tests pass | Owner, 2026-11-04: accepted. | answered |
| 6 | Today is the daily page but leads with the weekly AI work. Reorder it around the daily items (failing sources, proposals to decide, new feedback, new candidates, last run, Refresh now) and shrink the AI part to one line linking to the AI view? | Yes | Owner, 2026-11-04: accepted. | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

**Shape so far (draft, from the owner's answers to Q1 and Q2):** the top bar becomes Today · Candidates · Sources · Runs · Feedback · AI · More, 7 entries instead of 14. Sources reaches the Jungle radar; AI holds Export, Import, queue and settings; More holds E-mails, Exports, Data & backups (and probably Auto-reject). The shape is agreed (Q3, 3b answered, 2026-11-04). The draft success measure ("at most 6") becomes 7; settled in Q5.

## Constraints and risks
- A page that looks dead may still be used by the PC runner or a bookmark: check the runner scripts before removing any address.
- Removing Data & backups removes the only portable backup download in the UI (the daily database backup is separate): needs the owner's word.
- Many cycles share this working tree: stage only this cycle's paths.

## Gate
- [x] All open questions answered or parked
- [x] Goal and success measure confirmed by the owner (2026-11-04, "Approve intent")
