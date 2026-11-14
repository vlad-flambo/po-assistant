# Intent: invitation codes for sign-up

| | |
|---|---|
| **Cycle** | 033 |
| **Stage** | Intent |
| **Date** | 2026-11-06 |
| **Owner** | Vladimir Stoyanov |
| **Importance** | 4/5 (owner, 2026-11-06): the owner's score, no reason given; set by the owner over my 3/5 (claude, 2026-11-06: opening the app to more people and tracking where they come from, today single-use links by hand, no count of people waiting) |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

The folder is still called `033-referral-codes-for-sign-up` (the request's word); the feature is now named **invitation code** (Q7).

## The request, in your words

> new feature
> I want to open the app to more people.
> I still want to track where candidates come from.
> Goal adding a referal code feature.
> Console:
>
> * I can create codes like "Skaleet", allowing people to sign in by filling a referral code on the sign up screen
> * Candidates can create referrals and invite friends (like I already do in console). Only one referral code per candidate though. No customisation or editing
>
> I want to keep the link system. The link includes the referral code, it is pre-filled on sign up screen

Follow-up, 2026-11-06: "importance 4"; rename the feature "Invitation code" to avoid the clash with referral elsewhere; "accept all recommendations" for the questions.

## Why now / the pain

The owner wants to open the app beyond the people they invite one by one. Today every account needs a **single-use invitation link that the operator makes on *People* and hands over** (or e-mails). That does not scale past a few dozen people, and the only record of where someone came from is the free-text note on the invitation. No count of people waiting; no number yet.

## Goal

Anyone who holds an invitation code can create an account on a sign-up screen, and every account records which code it came through, so the owner can see where candidates come from. Candidates get one code of their own to bring friends in.

## Success measure

*(draft, waiting for the owner's confirmation)*
1. A code made in the console ("Skaleet") lets a stranger create an account by typing it, or by opening a link with the code already filled in; without a valid code nobody can sign up.
2. Every new account shows its origin (an operator code, a candidate's code, or an operator invitation link); the console shows, per code, how many accounts came through it.
3. A candidate sees their own code and link in the app, cannot change it or make a second one, and a friend who signs up through it is counted under that candidate.

## Not doing (this cycle)

- Rewards, points or any perk for referring.
- Editing, customising or adding a second code for a candidate.
- Open sign-up without a code.
- Changing the operator's existing single-use invitation links.
- Inviting by e-mail from a candidate's page (Q2): later cycle, with a limit.
- Confirming that the e-mail address belongs to the person (Q8): parked.
- A maximum number of sign-ups or an end date on a code (Q3).

## What we already know (facts, with where they came from)

- Sign-up exists only through a single-use link `/join/<token>/`: [`jobs/accounts.py`](../../../../jobs/accounts.py) (`create_invitation`, `open_invitation`, `sign_up`), [`jobs/views_accounts.py`](../../../../jobs/views_accounts.py) `join`, [`join.html`](../../../../jobs/templates/jobs/join.html). There is **no sign-up screen** to type a code into: the login page says "No account yet? Accounts are by invitation." (read 2026-11-06).
- `Invitation` (`jobs/models.py:762`): token, a private note, optional e-mail (pre-fills the form), created by, 14-day expiry, used by, revoked. It is single use; an invitation code is a different thing (many uses, shared). **The word "invitation" already names the single-use link**, so the console and the documents must tell "invitation link" (one person) from "invitation code" (many).
- The operator makes invitations on *People* (`/ops/people/`), with an optional e-mail sent through Brevo (`mail.send_invitation`). Candidates have no way to invite anyone today.
- `Candidate` has no field for where the person came from (`jobs/models.py:50`); `sign_up` sets the candidate's language from the page it was opened in.
- The word **"referral" is already taken** in the app: *Ask for a referral* (`referral.html`, `/job/<id>/referral/<contact>/`) is the message a candidate writes to a contact at an employer about a job. Same word, other meaning (read 2026-11-06).
- E-mail is live (Brevo, 300 a day, from `mail.saxobeat.fr`; PRD_users_and_emails, DEPLOY.md §7). Neon's free allowance is 0.5 GB of storage and 5 GB read per month (DEPLOY.md), and a candidate deleting their account is now cheap (cycle 032).
- The e-mail address is the login, and the sign-up does not confirm that the address belongs to the person (`accounts.sign_up`). With invitations that was the operator's check; with open codes nobody checks it (Q8, parked).

## Open questions (grilled one at a time)

| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | "Keep the link system": do the operator's single-use `/join/<token>/` links stay exactly as they are, and a code adds a second way in: a sign-up screen with a code field, and a multi-use link `/signup/?code=SKALEET` that opens it with the code filled in? | Yes: invitations untouched; the code link is the one shared by the operator for a group and by a candidate for friends | Accepted as recommended (owner, 2026-11-06) | answered |
| 2 | Can a candidate invite by **e-mail from the app** as you do in the console, or only copy and share their code and link? | Copy and share only for now (copy button, phone share sheet): an e-mail form on every candidate's page lets anyone send mail from our domain to any address; e-mail invites can be a later cycle with a limit | Accepted as recommended (owner, 2026-11-06) | answered |
| 3 | What can you do with a code you made? | A code is its own name (letters, digits, dash), not case-sensitive, many uses, no end date; you can switch it off and on; no maximum | Accepted as recommended (owner, 2026-11-06) | answered |
| 4 | A candidate's code | Made automatically on first visit to the invite page (about 8 readable characters), fixed for life, shown with the link and a copy button | Accepted as recommended (owner, 2026-11-06) | answered |
| 5 | What does the console show about origin? | Per code the number of accounts and the list of people; on each person on *People* "came through Skaleet / Marie's code / an invitation link"; existing accounts show "invitation link" if they used one and "before codes" otherwise (no guessing) | Accepted as recommended (owner, 2026-11-06) | answered |
| 6 | Where does the sign-up screen live? | A public `/signup/` page with the code field, linked from the login page ("No account yet? Enter an invitation code"); a wrong code gets one calm message and attempts are limited like wrong passwords | Accepted as recommended (owner, 2026-11-06) | answered |
| 7 | The name in the interface | (my recommendation was "invite code" for candidates and "referral code" in the console) | **Changed by the owner: "Invitation code" everywhere** (candidates, console, documents); the job message keeps "Ask for a referral"; the single-use link is called "invitation link" to tell the two apart (Q7 follow-up for the spec: French wording "code d'invitation" / "lien d'invitation") | answered |
| 8 | Do we confirm the e-mail address belongs to the person before the account works? | Not in this cycle: noted as a risk; the reset e-mail is the first time it is tested | Accepted as recommended: parked (owner, 2026-11-06) | parked |
| 9 | Does a candidate who deletes their account change anything for the friends they brought? | No: friends keep their accounts and the count stays as a number; the code stops working for new sign-ups | Accepted as recommended (owner, 2026-11-06) | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks

- **Opening sign-up is the real change**: today the operator decides who gets in; with a shared code (and every candidate's own code) a link in a group chat can bring in dozens of people. Cost side: Neon's 0.5 GB storage and 5 GB a month read, Brevo's 300 a day (welcome e-mail per new account), and the PC runner's scoring time per new candidate. The owner can switch a code off (Q3) as the brake.
- Guessing codes: a public code field is an open door for guessing short codes; the attempts need a limit (Q6) and candidates' codes need enough characters.
- Wrong address typed at sign-up means a login that cannot be reset (Q8, parked).
- A candidate's code spreads further than the owner's: the owner can switch off a candidate's code too (to be written in the spec).
- Not an irreversible step for data: a new table and a field on the candidate; the sign-up screen goes live only with a deploy the owner decides.

## Gate
- [x] All open questions answered or parked
- [x] Goal and success measure confirmed by the owner (2026-11-06)
