# Spec: a feedback chat, always one tap away

| | |
|---|---|
| **Cycle** | 015 |
| **Stage** | Spec (approved 2026-10-29) |
| **Intent** | [intent.md](intent.md) |

## Behaviour when finished
**A signed-in person** sees a round speech-bubble button at the bottom-right of every page of the app. One tap opens a bottom sheet that looks like a chat: the app asks in bubbles, the person answers by tapping a button or typing a short text. It starts with "What would you like to tell me?" and three buttons: *An idea or a missing feature*, *Something is broken or confusing*, *What I think of something that exists*. The first bubble says where they are ("You are on Pipeline") and that the feedback is tied to their account. Each answer is saved the moment it is given, so closing the sheet halfway loses nothing. The chat ends with "Thank you, I read every one" and a button to tell another thing. Nothing is sent to any outside service and nothing is generated: every question is written in advance.

**The operator** has a "Feedback" page in the console (next to People and E-mails), with a count of new items on its link. It lists what people said, newest first, with who, when, which page, phone or desktop, and every answer. An item can be marked *new*, *read* or *turned into a cycle* (with the cycle's number). A button **Copy as intent draft** puts the item on the clipboard in the shape of `templates/intent.md`, so starting a new intent is a paste.

## Acceptance criteria
Each one is checkable in `verify.md` (T = automated test, M = a measurement or a look, O = the owner does it on their devices).

1. **Icon on every signed-in page (T).** The button is in the HTML of every candidate page (inbox, archive, pipeline, job, followup, packet, referral, interviews, companies, company, contacts, insights, settings, email prefs, more, cv, cv_match, suggest, the welcome steps) and absent from the login, join, forgot-password and reset pages, the console pages, and while viewing as another person.
2. **No cost on other pages (T, M).** The number of database queries of the inbox, pipeline, job and settings pages is the same before and after the change (baseline recorded in `evidence/`). The sheet's content is fetched only when the button is tapped.
3. **Opening writes nothing (T).** The request that opens the chat creates no row; the first answer creates exactly one row; every later answer updates that row.
4. **Half a chat is kept (T).** After the first answer and nothing else, the row exists with `completed = false` and the console shows it as "unfinished". An empty first answer is refused and creates nothing.
5. **The three question lists are as written under "The script"** (T): idea (five steps), problem (five steps), opinion (five steps); every step but the first is skippable; choices are buttons.
6. **Context attached by the app (T).** The row records the page name, the job or company number if the page has one, phone or desktop (from the screen width at the time the sheet opened), the person's mode and language, and the time; the first bubble shows the page to the person.
7. **Limits (T).** A free-text answer over 2,000 characters is refused with a message and not stored. A person who has started 20 chats in the last 24 hours is told to come back tomorrow and no 21st row is created (see "To confirm", point 1).
8. **Only your own (T).** A person can read and write only their own feedback rows: posting an answer to another person's row gives "not found". Nobody can send feedback while viewing as someone else. A candidate who asks for the console page gets "not found".
9. **Gone with the account (T).** Deleting an account (`delete_me`) deletes that person's feedback.
10. **Console page (T).** Lists every item with the filters *kind* and *state*; the three states can be set and persist; the link shows the number of new items; the cycle number is kept.
11. **Intent draft (T, O).** The draft contains, under the headings of `templates/intent.md`, the person's words verbatim, the usefulness answer, today's workaround, the page and the person's first name. The owner copies one on desktop and one on a phone and pastes it (O).
12. **Both languages (T).** Every sentence the person or the operator sees is in the French catalogue (`locale/fr`); `tests/test_i18n.py` passes; the chat shows in the person's language.
13. **Phone layout (M, O).** At 360 px wide the button overlaps nothing: not the tab bar, the action bar on a job, the save bar in settings, or a toast, and the sheet shows the text field above the on-screen keyboard. Checked first in the browser pane at 360 and 390 px (screenshots in `evidence/`), then by the owner on a real phone.
14. **No outside calls, no e-mail (T, M).** The feedback code imports nothing from `jobs/ai`, `requests`, `anymail` or `jobs/mail`; a full chat creates no `OutgoingEmail` row; a search of the diff for network calls finds none.
15. **Live on the hosted app (O, M).** The additive migration is applied on the hosted database (guard: the table does not exist yet and the other tables' counts are unchanged), the owner sees the button on the real site, sends one test idea, sees it on the console page, and deletes it.
16. **Tests (T).** A new `tests/test_feedback.py` covers criteria 1, 3 to 10 and 12; the full suite gives the same result as before (one known failing backup test).
17. **Real use (O, later).** Within two weeks of the owner telling people about it: at least 5 items from at least 3 different friends (the intent's success measure 5). This one is read in `learn.md`, not at the verify gate.

## The script (what the chat asks)
All questions are plain text in one Python file; a choice is a button, a text is a one-line or short multi-line field with *Skip*. Steps are keyed so an answer is stored as `{key: value}`.

**Idea (the owner's Q2)**
1. `want` (text, required): "What would you like to be able to do?"
2. `value` (choice): *Nice to have* / *I'd use it every week* / *I'd use it every day* / *I can't do without it*
3. `today` (text or *Nothing, I just can't*): "What do you do today instead?"
4. `often` (choice): *Every day* / *Every week* / *Once a month* / *Once*
5. `more` (text): "Anything else?"

**Problem**
1. `what` (text, required): "What happened, and what did you expect?"
2. `where` (choice): *On this page* (the page in the first bubble) / *Somewhere else*; if *Somewhere else*, a short text asks where
3. `impact` (choice): *A small annoyance* / *It slows me down* / *I could not do what I came to do*
4. `repeat` (choice): *Every time* / *Sometimes* / *It happened once*
5. `more` (text): "Anything else?"

**Opinion**
1. `about` (choice, required): *This page* / *Inbox* / *Pipeline* / *Interviews* / *Companies* / *The AI review* / *E-mails* / *Settings* / *Something else* (then a short text names it)
2. `value` (choice): *Not useful* / *A little useful* / *Useful* / *Very useful* / *I can't do without it*
3. `good` (text): "What works well for you?"
4. `change` (text): "What would you change?"
5. `more` (text): "Anything else?"

## Design in brief
- **One model, `Feedback`**: candidate (cascade), `kind` (idea|problem|opinion), `answers` (JSON), `context` (JSON: page name, object id, device, mode, language), `completed` (bool), `state` (new|read|cycle), `cycle_ref` (short text), `created_at`, `updated_at`. One additive migration. A row is one chat.
- **The script** lives in `jobs/feedback.py` (like `jobs/conversation.py`): the three lists above, gettext-lazy strings, a function that says what comes next and checks an answer.
- **Three endpoints for people, none cached**: open (GET: the sheet's content, no write), answer (POST, HTMX: validates, saves, returns the next bubble), and nothing else; the "done" state is the last answer. A fourth for the operator list and one to change a state; the draft is rendered server-side in the page with a copy button (`navigator.clipboard`).
- **The button and the empty sheet** are in `base.html` for signed-in people who are not viewing as someone else (static markup, no query, hidden when printing). The sheet reuses `dialog.sheet` and the `.chat` and `.bubble` styles; the page that was open is sent when the sheet opens (path and screen width), and the server turns the path into a page name with Django's URL resolver, with no database read.
- **Position**: bottom-right; on a phone above the tab bar (58 px) and above the action bar and save bar on the pages that have one; from 900 px at the corner like the toasts, which move so they do not collide.
- **Rejected**:
  - *A third-party widget (Crisp, Tally, Typeform)*: the answers and the people's names would leave the owner's database, and the intent said no outside service.
  - *A "Feedback" page in the menu*: not "always one tap away" and not chat-like.
  - *Saving only at the end*: loses every half-finished chat, the most common kind.
  - *One free box*: collects opinions but not how useful it is or what they do today, the two things the owner wants to measure.
  - *Reusing the employer-suggestion table*: a different purpose and approval flow.
  - *E-mailing each item to the owner*: e-mail is not live yet (cycle 003) and the intent excluded it.

## Interfaces and data
- New: `jobs/feedback.py`, `jobs/views_feedback.py`, templates `_feedback_sheet.html`, `_feedback_step.html`, `ops/feedback.html`, migration `0041_feedback.py`, strings in `locale/fr/LC_MESSAGES/django.po` (and `.mo`), `tests/test_feedback.py`.
- Changed: `base.html` (button and empty sheet), `ops/base.html` (nav link with the new count), `urls.py` (4 routes under `feedback/` and `ops/feedback/`), `app.css` (button, positions, chat inside the sheet), `ui.js` (sends the page and screen width on open; copy button), `access.py` (the console's new-count in the existing operator context, one count query on console pages only).
- No new setting, no environment variable, no secret. The hosted database gets one new table.

## Constraints
- **Reads** (cycles 001 and 002): a candidate page loads with the same queries as today; only the feedback endpoints touch the new table; the console count is a single `COUNT` on console pages only.
- **Privacy**: free text may contain anything. It stays in the owner's database, is visible only to its author and the operator, goes with the account, and is never sent out. It is part of the database backups like every other table (to check in the plan: whether a person's own "data export" should list it).
- **No AI, no network**: criterion 14.
- **Service worker**: the open and answer endpoints must not be cached by `sw.js` (to check in the plan).
- **Hosting**: the migration is additive and small; it runs on the hosted database like cycle 002's recipe, guarded (refuse if the table already exists or counts differ), after the owner's yes.
- **Standard mode**: the chat uses no power-mode page; its button shows for both modes.
- **Accessibility**: the button has a text label for screen readers, a 44 px tap target, and the sheet closes on Escape, on the backdrop and with a Close button.

## Out of scope
- A list of "your feedback" and replies to it (Q7, parked).
- E-mail, push or chat notifications to the owner; the owner reads the console.
- Voting, a public roadmap, screenshots or files, tracking of clicks.
- Sorting, tagging or summarising feedback by machine; the operator does it by eye.
- Feedback from people who are not signed in (a login problem goes to the owner by the usual channel).
- Editing a past answer after the chat is over.

## To confirm (two interpretations I made, say if either is wrong)
1. **"20 messages a day" (Q8)** is built as **20 chats started in the last 24 hours** (a chat has up to 6 answers), not 20 individual answers. A person is unlikely to start more than a few a day, so the limit only stops accidents and abuse.
2. **The person's first name on the draft (criterion 11)** comes from `Candidate.name`, which for most accounts is the sign-in name or e-mail. If you would rather not paste an address into an intent file, the draft shows "C-02" style numbers, as the "view as" banner does.

## Changes after approval
- **2026-10-30, at the owner's request, after the first live test: criterion 18.** The console's Feedback page can delete a chat (a button on each item that asks "sure?" first; the operator only; a candidate gets "not found"; the page the operator came from is kept). Until then a chat could be removed only in the Django admin, which the owner did not find from the console. Checked in `tests/test_feedback_console.py` (5 tests) and on screen locally; it reaches the host with the next push.

## Gate
- [x] Owner approved this spec (2026-10-29, with both "To confirm" points as written)
