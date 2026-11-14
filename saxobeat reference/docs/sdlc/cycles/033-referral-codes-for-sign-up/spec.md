# Spec: invitation codes for sign-up

| | |
|---|---|
| **Cycle** | 033 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) (confirmed 2026-11-06; Q1 to Q9 answered, Q8 parked) |
| **Stack** | house-stack: Django, htmx-free server pages, SQLite locally and Postgres on Neon; no deviation. Conventions read: public pages are the few listed (login, invitation, reset link, `/healthz`), lockout counters live in the database, French and English for every candidate page, 44 px targets, 16 px inputs on phones |

## Behaviour when finished

**For someone who wants in.** The login page links to a public sign-up page. They type an invitation code (or open a link that already carries it), fill in name, e-mail and password, and get an account exactly as an invitation link gives one today. Without a valid code nobody gets in.

**For the operator.** On *People* the operator makes codes with a name ("Skaleet"), sees each code's link and how many accounts came through it, and switches a code on or off. Every person in the list shows where they came from, and a summary adds up to the total number of accounts. The operator can also switch one candidate's own code off.

**For a candidate.** An *Invite friends* page shows their one code and its link, with a copy button and (on phones) a share button, and the number of friends who joined. The code is made the first time they open the page, never changes, and cannot be edited or doubled.

**Unchanged.** The operator's single-use `/join/<token>/` links work exactly as before. Nothing is e-mailed from a candidate's page. Existing accounts keep everything.

## Acceptance criteria

Each one is checkable in `verify.md`. "Test" means a test in `tests/test_invitation_codes.py` (or the existing suites) unless said otherwise.

**The sign-up screen**
1. [ ] `/signup/` answers without a login. It shows a code field and the sign-up form (name, e-mail, password twice). `/signup/?code=SKALEET` shows the code already filled in. The login page links to `/signup/` in place of "Accounts are by invitation" (test, and a look at 375 px).
2. [ ] With an active code and valid details an account is created exactly as `/join/` creates one: logged in, own empty settings, language of the page it was opened in, welcome e-mail queued, redirect to the welcome page. Any number of people can use the same code (test: three sign-ups with one code).
3. [ ] No valid code, no account. An empty, unknown, or switched-off code gives the same single calm message, writes nothing, and keeps what was typed (not the passwords). The message does not say which of the three it was (test).
4. [ ] A code matches without regard to case and surrounding spaces: "  skaleet " opens "Skaleet" (test).
5. [ ] Wrong codes are limited like wrong passwords: after 10 wrong codes from one address within 15 minutes, `/signup/` answers 429 with a wait message, even for a right code, until the window passes. It reuses `FailedLogin`: no new table (test with a frozen clock).
6. [ ] A brake on floods (decision D1): at most 3 sign-ups per address per hour and 20 per hour in all; beyond that the page says to try again later and creates nothing; the three counts are tests, and the limits are named constants (test).
7. [ ] The existing `/join/<token>/` flow is unchanged: the existing account tests pass without edits to their expectations, and an account made that way records its origin as "invitation link" (test).

**The console (*People*, operator only)**
8. [ ] The operator makes a code: 3 to 32 characters, letters, digits and dashes, shown as typed, unique without regard to case across all codes (candidates' too); a bad or taken name gives a clear message and creates nothing. The table shows name, link, accounts through it, state. Switching off stops new sign-ups through it and touches no existing account; switching on restores it (tests; non-operators get "not found").
9. [ ] Each person row shows *Came through*: the code's name ("Skaleet"), "Marie's code", "invitation link" or "before codes". A summary lists accounts per operator code, through candidates' codes (together), through invitation links, and before codes, and the numbers add up to the number of accounts (test of the sum).
10. [ ] From a candidate's row the operator switches that candidate's code off and on. While it is off their link and code give the calm message of criterion 3 (test).
11. [ ] The migration marks an existing account "invitation link" when an invitation was used by it and "before codes" otherwise; the number of accounts before and after is equal; run on a local copy of the 29 Oct dump with the counts written in `evidence/` (measurement).

**The candidate's page**
12. [ ] `/invite/` needs a login. The first visit makes one code of 8 characters from an alphabet without look-alikes (no 0/O, 1/I/L); every later visit, and two visits at once, show the same one; the database refuses a second code for the same candidate. The page has no form to edit or add a code. An operator viewing as the candidate sees the code if it exists and never creates one (tests).
13. [ ] The page shows the code, the full link (`SAXOBEAT_PUBLIC_URL` when set, else the request's address), a copy button, a share button where the browser offers sharing, and the number of friends who joined (a number only, no names). A friend who signs up through the link raises the number by one and appears in the console as "came through Marie's code" (test).
14. [ ] *Invite friends* is reachable from Settings and from the phone's More page, in standard and power mode. Every new candidate-facing string has a French translation (the i18n test passes), and at 375 px there is no sideways scroll and the buttons are at least 44 px high (test, and a look).

**Deleting an account**
15. [ ] Deleting a candidate removes their code with them and leaves no dangling reference. Friends they brought keep their accounts and still show "came through Marie's code". The inviter's code no longer signs anyone up. `tests/test_account_delete.py` (the guard over the relation graph) passes with the new table listed, and the delete stays at a handful of statements (test, with the statement count).

**Cost and safety**
16. [ ] The cost of one new account is measured on a local copy (rows and megabytes after its first backfill) and written in `verify.md` with how many such accounts Neon's 0.5 GB storage can hold, from DEPLOY.md's figures and the measurement's date (measurement).
17. [ ] The suite passes on SQLite, and once on a local Postgres before the release (house-stack tier 2), and `makemigrations --check` finds nothing left over. Pass counts and dates recorded (command output).
18. [ ] **Owner's step, after the deploy:** the owner makes the first code on the host, signs up through its link with an address of theirs, and criteria 1 to 3 are read on the host. Nothing is live until the owner deploys (owner's word, then my read).

## Design in brief

- **A new table, `InvitationCode`**, separate from `Invitation`. An invitation is one person's single-use link with an expiry; a code is shared, has many uses and no expiry. Merging them would turn "used once" and "expires in 14 days" into special cases. *Rejected: making `Invitation` multi-use.*
- **One table for both kinds of code.** An operator code has no owner; a candidate's code points at its candidate (one-to-one). Both are looked up the same way at sign-up, so a name cannot be both an operator code and a candidate's code. *Rejected: a code field on `Candidate` (operator codes have no candidate).*
- **Origin lives on the candidate and survives the code.** `Candidate.origin_kind` ("code", "invitation" or blank for before codes), `origin_label` (the text shown, written at sign-up: "Skaleet", "Marie's code") and `origin_code` (a link to the code, set null when the code goes). Counts use the link; the label keeps history readable after a deletion (Q9).
- **One page, not two steps.** `/signup/` has the code field and the form together, so the link's pre-filled code and a typed one behave the same. *Rejected: a code step then a form step (a second page for no gain).*
- **The account-creating work is shared.** `accounts.sign_up` (invitation) and the new code sign-up call one function for checks, user and candidate, language, settings row and origin, so the two ways in cannot drift apart.
- **Limits reuse what exists.** The login throttle's table `FailedLogin` (name, address, time; rows older than two days are already swept) also holds two reserved names: `signup-code` for a wrong code and `signup-ok` for an account just made, each with the caller's address. Wrong codes use the 15-minute window; the per-address brake counts `signup-ok` rows of the last hour; the overall brake counts `Candidate.created_at` of the last hour (no address needed). No new table. *Rejected: a new attempts table (one more thing to delete and test for the same facts).*
- **Candidate invites are copy and share only** (Q2). No e-mail leaves a candidate's page.

### Decisions for you to approve with this spec

- **D1: a brake on floods (criterion 6).** Not in your words, added because of what a sign-up costs. Every new account runs a catalogue backfill that creates one row per job the person can see (an inbox of thousands of rows, cycle 032's drill used 36,271), and a welcome e-mail (Brevo: 300 a day). A well-known code such as "Skaleet" could let a script fill Neon's 0.5 GB or the e-mail allowance in minutes. Recommended: 3 per address and 20 in all per hour (your switch-off button is the second brake). Counted as described under "Limits reuse what exists", so no new table; the limits are constants in `accounts.py`. Say if you want other numbers or none.
- **D2: a candidate sees a number, not names.** Friends' names and e-mails are their data; the operator sees the people, the inviter sees "3 friends joined". Say if you want names.
- **D3: one message for every refusal** (unknown, switched off, empty) so the page does not tell a guesser which codes exist.
- **D4: stored as typed, matched without case.** "Skaleet" is shown as typed; "skaleet" and "SKALEET" open it.

## Interfaces and data

- **Model** `InvitationCode`: `code` (max 32, unique without regard to case through a `Lower("code")` constraint), `candidate` (one-to-one, null for operator codes, cascade), `active` (default true), `created_by` (user, null, set null), `created_at`. Migration `0044`.
- **Candidate**: `origin_kind` (max 12, blank), `origin_label` (max 80, blank), `origin_code` (foreign key to `InvitationCode`, null, set null). A data step in the same migration fills `origin_kind = "invitation"` where `Invitation.used_by` is the candidate's user.
- **Routes**: `signup/` (public), `invite/` (login required), and new actions on `ops/people/` (`code_new`, `code_toggle`, `candidate_code_toggle`). No existing address changes.
- **Code** (`jobs/accounts.py`): `normalize_code`, `make_candidate_code`, `code_for_candidate`, `open_code`, a shared `create_account`, `sign_up_with_code`, the brakes' constants, `origin_summary`. Views in `jobs/views_accounts.py`.
- **Templates**: new `signup.html`, `invite.html`; changed `login.html`, `people.html`, `more.html`, `settings.html`. French in `locale/fr`. A small copy and share script in `jobs/static/jobs/ui.js`.
- **Deleting an account** (`accounts.delete_account`): the candidate's code is added to the one-DELETE-per-table list, and the people who came through it get `origin_code` set to null first (a raw delete does not run Django's set-null).
- **No new setting or environment variable.**

## Constraints

- Public page on a hosted app: CSRF stays on; no secret or e-mail address is put in a link; the code is not a secret (it is meant to be shared), so it must grant nothing but sign-up.
- Cost: see D1 and criterion 16. Neon 0.5 GB storage, Brevo 300 a day, the web server's one worker (a backfill runs in the background thread at the first request of a new candidate).
- Privacy: the inviter never sees a friend's name or e-mail (D2); the origin text of a person is visible to the operator only.
- No data is changed on the host until the owner deploys; the migration's data step is small and reversible by dropping the three fields.
- Migrations are never edited after they have shipped (house-stack): get 0044 right before the deploy.

## Out of scope

- Rewards or perks for inviting; editing, customising or a second code for a candidate.
- E-mail invitations sent from a candidate's page (a later cycle, with a limit).
- Confirming that an e-mail address belongs to the person (Q8, parked).
- A maximum number of sign-ups or an end date on one code; deleting a code (switch off is enough, the history stays).
- An e-mail to the operator when someone signs up (PRD_users_and_emails R1).
- Changing how invitation links are made, mailed or revoked.
- Showing the inviter who joined (D2).

## Gate
- [x] Owner approved this spec (2026-11-06, including D1 to D4)
