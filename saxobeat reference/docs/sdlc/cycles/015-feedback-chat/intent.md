# Intent: a feedback chat, always one tap away

| | |
|---|---|
| **Cycle** | 015 |
| **Stage** | Intent (approved 2026-10-29); Spec drafted |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Importance** | 4/5 (claude, 2026-10-30): the channel that turns what users say into the next cycles |

## The request, in your words
> I want to create a simple, always accessible interface in the app, allowing users to give me feedback on the app
> The goal is to collect all the relevant info from them, so I can build a corresponding intent file
> it should be a clearly visible icon opening a chat like interface.
> all programatic, no gen ai api or things like this.
> just a simple way to collect opinions, evaluate how useful to them the feature would be etc.

## Why now / the pain
Today feedback from friends reaches the owner by whatever channel they pick (message, chat, in person), unstructured: no page, no device, no "how much would you use it", nothing that turns straight into an intent file. The app now has several users (multi-user since cycle PRD_multi_user, standard/power modes, phone-first UI), so the owner can no longer ask each one. *(How many active users: to be verified from the People page.)*

## Goal
Any signed-in person can open a feedback chat from every page in one tap, answer a few short scripted questions, and the owner receives a structured record complete enough to start a new intent file from it, with no AI service involved.

## Success measure
*(draft, to confirm)*
1. The icon is visible and reachable in one tap on every signed-in page, on a phone and on a desktop, without covering the tab bar, the action bar or the toasts.
2. A person can finish an "idea" in under 60 seconds with at most 6 short answers (everything optional except the first).
3. The operator reads every item on one console page, sees where it came from (page, device, mode, language, date), and can copy it as an intent-file draft in the SDLC template's shape.
4. Adds no database read to pages other than the feedback ones (the icon costs no query; cycles 001 and 002 were about cutting reads).
5. Real use: at least 5 pieces of feedback from at least 3 different friends within two weeks of going live, after the owner tells them about the icon once (Q10).

## Not doing (this cycle)
- Any generative-AI call or outside service for sorting, summarising or answering: the questions are scripted, the reading is by the owner.
- E-mail or push notifications to the owner or to the person (cycle 009 covers alerts); the owner reads a console page.
- Replies from the owner inside the chat, a public roadmap, voting on other people's ideas.
- Screenshots, file uploads, screen recording.
- Analytics or tracking of what people click (this asks, it does not watch).

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| The app has a scripted, no-AI chat already: five questions as `.chat` and `.bubble` styles, one question per page | `jobs/conversation.py`, `jobs/templates/jobs/ask.html`, `jobs/static/jobs/app.css` lines 435 to 439 |
| One shared page frame for every candidate page, with the top bar, a fixed phone tab bar (Inbox, Pipeline, Interviews, More) and a toast area; the tab bar is hidden from 900 px | `jobs/templates/jobs/base.html`, `app.css` lines 158 to 178 |
| The login, join and reset pages use the same frame but have no `user` and no tab bar | `base.html` (`{% if user.is_authenticated %}`) |
| HTMX is bundled; `ui.js` carries the page scripts; a service worker exists | `jobs/static/jobs/` |
| The operator console is a separate frame with a nav row of pages (People, E-mails, ...); a feedback page would be one more link | `jobs/templates/jobs/ops/base.html` |
| The interface is in French and English with gettext (`locale/fr`) | `base.html`, `locale/fr/LC_MESSAGES` |
| `Candidate` has `mode` (standard/power), `language`, `name`; the account page lets a person delete themselves, and personal rows cascade from `Candidate` | `jobs/models.py`, `views_accounts.py` `delete_me` |
| A context processor already runs on every page (`roles`), and the tab-bar numbers are lazy so a page that does not draw them costs no query | `jobs/access.py` |
| An employer-suggestion form with a monthly allowance exists, a precedent for per-person limits | `jobs/templates/jobs/suggest.html` |
| Neon's allowance was the pressure of cycles 001 and 002: every extra query on every page matters | `docs/sdlc/cycles/001-*`, `002-*` |
| Number of active users and what they have already said informally | **unknown, to be verified** (People page) |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | What does the chat ask about first: which kinds of feedback does it offer? | Three scripted paths: **an idea / a missing feature**, **something is broken or confusing**, **what I think of something that exists** (a page or a feature). Each opens its own short question list. | Accepted as recommended (2026-10-29). | answered |
| Q2 | What are the questions on the "idea" path? | Five, each skippable but the first: (1) what do you want to do, in your words; (2) how useful would it be (4 buttons: *Nice to have / I'd use it weekly / I'd use it every day / I can't do without*); (3) what do you do today instead (free text or "nothing"); (4) how often would you need it (daily, weekly, once a month, once); (5) anything else. | Accepted as recommended (2026-10-29). The questions for the other two paths are settled in the spec. | answered |
| Q3 | What does the app attach on its own? | Page (route name), the job or company it was on if any, device class (phone/desktop from screen width), mode, language, app date; shown to the person in the first bubble ("You are on Pipeline") so nothing is hidden. | Accepted as recommended (2026-10-29). | answered |
| Q4 | Where does the icon live and who sees it? | Every signed-in page (candidates, and the operator in their own app; not on the console). A round speech-bubble button bottom-right, above the phone tab bar and action bar; hidden on the login, join and reset pages; hidden while viewing as someone else. | Accepted as recommended (2026-10-29). | answered |
| Q5 | Is the feedback tied to the person? | Yes, to their account (they are friends, the owner may want to ask more), and the chat says so in its first line. Deleted with the account. | Accepted as recommended (2026-10-29). | answered |
| Q6 | What does the owner get? | A console page "Feedback" (new / read / turned into a cycle) with a filter by kind, and a button "Copy as intent draft" that prints the item in the shape of `templates/intent.md` (request in their words, page, usefulness, today's workaround). | Accepted as recommended (2026-10-29). | answered |
| Q7 | Do people see what happened to their feedback? | Park it: no list of "your feedback" in this cycle; the chat ends with "Thank you, I read every one". | Accepted: parked for a later cycle (2026-10-29). | parked |
| Q8 | A limit against spam or accidents? | 20 messages a day and 2,000 characters per free text, per person. | Accepted as recommended (2026-10-29). | answered |
| Q9 | How is the chat built (no AI, programmatic)? | A script of questions in one Python file (like `conversation.py`), each answer posted with HTMX; the open chat is a bottom sheet (the app already has `dialog.sheet`); the session is saved at the first answer so a half-finished chat still reaches the owner. | Accepted as recommended (2026-10-29). | answered |
| Q10 | How much real use means success? | At least 5 feedback items from at least 3 different friends in the first two weeks, after the owner tells them about the icon once. | Accepted as recommended (2026-10-29). | answered |
| Q11 | French copy: who writes it? | I write both languages; the owner reads the French once (as for PRD_mobile D10). | Accepted as recommended (2026-10-29). | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- **No reads on other pages**: the icon is drawn in `base.html` with no query. A person's draft feedback is only read on the feedback endpoints.
- **Personal text is stored**: free text can contain anything (names, salary). It lives in the owner's database only, goes away with the account, and is not sent to any outside service. The export file is for the owner alone.
- **Layout collisions on a phone**: the tab bar (58 px), the action bar on job pages, the toasts and the save bar all sit at the bottom; the button must not hide them or be hidden by them. Needs a check on a real phone width (cycle 005's tooling when available).
- **Standard mode users** see a trimmed app; the chat must not need any power-mode page.
- **A chat that asks too much gets abandoned**: partial answers must still be kept.
- A new table means a migration on the hosted Neon database (small, additive); the plan will guard it as cycle 002 did.

## Gate
- [x] All open questions answered or parked (approved by the owner 2026-10-29)
- [x] Goal and success measure confirmed by the owner (2026-10-29)
