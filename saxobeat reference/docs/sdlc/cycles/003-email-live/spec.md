# Spec: make e-mail live (Brevo, mail.saxobeat.fr, app.saxobeat.fr)

| | |
|---|---|
| **Cycle** | 003 |
| **Stage** | Spec (approved 2026-10-30; sending domain and app address changed by the owner the same day, [decisions.md](decisions.md) D1, D4) |
| **Intent** | [intent.md](intent.md) (approved 2026-10-30) |

## Behaviour when finished
- Saxobeat sends its e-mails through Brevo from `Saxobeat <no-reply@mail.saxobeat.fr>`, authenticated for `saxobeat.fr` (DKIM, SPF and DMARC pass); a reply goes to the owner (Reply-To). (changed 2026-10-30, D1)
- Every link in an e-mail (invitation, welcome, password reset, unsubscribe) opens `https://app.saxobeat.fr`, never `localhost` or the `onrender.com` name. (changed 2026-10-30, D4)
- A reset link that was **e-mailed** works once and for **1 hour**. A reset link the operator makes by hand in the console keeps working for **3 days**. The e-mail says "1 hour" (in English and French).
- Nobody receives an e-mail they did not expect: the AI-ready e-mails and digests (the "candidate e-mails") stay paused in the console until the owner turns them on on purpose. Invitations, welcomes and resets (the "account e-mails") always go.
- The first real invitation goes to one friend, only after the Gmail and Outlook tests and a rehearsal to the owner's own second address.

## Acceptance criteria
Each one must be checkable in `verify.md`. "Owner" means the owner does it or reads it, because it needs their accounts; the evidence is a screenshot, a copied header or a yes/no, never a secret.

**The domain and Brevo (owner)**
1. [ ] **Brevo shows `mail.saxobeat.fr` as authenticated**, and the DNS answers match: each record Brevo asked for resolves with `Resolve-DnsName` (`mail.saxobeat.fr` CNAME to Brevo's brand host, which carries the SPF and the return-path; `brevo1` and `brevo2._domainkey.saxobeat.fr` DKIM CNAMEs; Brevo's `brevo-code` TXT on `saxobeat.fr`), and a DMARC record with `p=none` covers the sending domain (Q3; Brevo's record at `_dmarc.saxobeat.fr` covers the subdomain by inheritance, its reports go to Brevo; kept by the owner, D2). Evidence: Brevo's domain page and `evidence/dns_check_2026-10-30_saxobeat_fr.md`. (changed 2026-10-30, D1). On 2026-10-30 the records were already in place (Claude's read-only lookup); Brevo's "authenticated" was confirmed by the owner the same day.
2. [ ] **Brevo's real free-plan limits are read and written down** (daily and monthly sending limits, whether the API and a custom domain are included, any Brevo footer added to e-mails), with the date and "owner, Brevo dashboard". `SAXOBEAT_MAIL_DAILY_CAP` equals the daily limit, or the difference is explained.

**The settings (owner, no secret shown)**
3. [ ] **Render has the five settings** (`SAXOBEAT_MAIL=brevo`, `BREVO_API_KEY`, `SAXOBEAT_MAIL_FROM=Saxobeat <no-reply@mail.saxobeat.fr>`, `SAXOBEAT_PUBLIC_URL=https://app.saxobeat.fr`, `SAXOBEAT_MAIL_REPLY_TO`), shown by the console's *E-mails* page: provider `brevo`, the sender `no-reply@mail.saxobeat.fr`, and the public address `https://app.saxobeat.fr`. The key itself appears nowhere. (changed 2026-10-30, D1 and D4)
4. [ ] **The PC's `.env` has the same five**, checked by variable names only, so the runner's e-mails (`manage.py mail send`) use the same provider and public address.
5. [ ] **The API key is nowhere in the repo, the chat or a command line:** `git grep` for Brevo's key prefix (`xkeysib-`) finds nothing, and `.env` is ignored by git.

**Safe switch-on (owner, with Claude's counts)**
6. [ ] **Candidate e-mails are paused before mail is switched on.** The console's pause switch is on, and the *E-mails* page says so. Before it is turned off, the number of people who would receive an AI-ready e-mail or a digest is read (counts only) and the owner decides. Evidence: the page, and the count with its date.
7. [ ] **The off switch works:** with `SAXOBEAT_MAIL=off` an e-mail ends in the state *skipped* and nothing leaves (existing test, `tests/test_mail.py` line 173, passes). The rollback is written in DEPLOY.md §7: set it to `off` on Render and in `.env`.

**Deliverability (owner)**
8. [ ] **A test e-mail to Gmail** (console *E-mails → Send a test*) arrives in the **inbox, not spam**, and Gmail's "Show original" reads `dkim=pass`, `spf=pass` and `dmarc=pass`, with the sender `no-reply@mail.saxobeat.fr`; the `header.d=` of the DKIM signature is copied as it is (probably `saxobeat.fr`, D1). Evidence: the copied header lines. (changed 2026-10-30, D1)
9. [ ] **The same test to Outlook:** inbox, not spam, and the message headers show DKIM, SPF and DMARC passing, sender `no-reply@mail.saxobeat.fr`. (changed 2026-10-30, D1)
10. [ ] **A rehearsal:** a real invitation (not a test) to a second address of the owner's own arrives, its link opens `https://app.saxobeat.fr/join/...` with a valid certificate, and an account is created from it. The welcome e-mail arrives too.

**The first real use (owner)**
11. [ ] **One real invitation to one friend** the owner names (Q4), only after 8, 9 and 10 pass: the console's *E-mails* page shows it *sent*, the friend creates their account, and the friend confirms it reached their inbox (not spam). Evidence: the console row (kind, state, time), the new account's existence by count, the friend's reply in the owner's words.
12. [ ] **Links point to the public address in every kind sent:** in the received invitation, welcome and reset e-mails, and in the unsubscribe link of one candidate e-mail if any is sent, no link contains `localhost`, `onrender.com` or `127.0.0.1`.

**The reset link (code, Claude)**
13. [ ] **An e-mailed reset link is accepted inside 1 hour and refused after it** (a test that moves the clock: at 59 minutes the password can be changed, at 61 minutes the page says the link is not valid).
14. [ ] **A hand-made reset link (console *Reset password*) is accepted at 2 days and refused at 3 days and 1 minute**, so it still behaves as today.
15. [ ] **Both kinds still work once only**, and a tampered link is still refused (the existing tests `test_a_reset_link_sets_a_new_password_once` and `test_a_tampered_reset_link_is_refused` pass unchanged).
16. [ ] **The reset e-mail says "1 hour"** in English and in French, not "3 days" and not "0 days" (a test on the e-mail text in both languages). The hand-made link message in the console still says it is valid "for a few days".
17. [ ] **The whole test suite passes** on SQLite (`DATABASE_URL=` empty), with no test removed or weakened. The baseline is the count at the start of the slice (1,249 on 2026-10-30, one test of another session aside, see the plan).
18. [ ] **The change is live on the host:** the latest Render deploy contains it (date and commit read from Render's Events), and an e-mailed reset link made on the host is accepted at once and carries the 1-hour wording. (Pushing is the owner's decision.)
19. [ ] **The app answers on `https://app.saxobeat.fr`:** a valid certificate (checked with `curl` and `openssl`, read-only), the address redirects to the sign-in page, **signing in and one form work there** (no 400 "Bad Request", no 403 CSRF error), the E-mails page reads "links to https://app.saxobeat.fr", and the service's own address `saxobeat.onrender.com` still answers (the old `jobs.stoyan.ovh` was removed on purpose, D5). Evidence: Claude's lookup and `curl` output in `evidence/`, the owner's word and page line for the sign-in. (changed 2026-10-30, D4)

## Design in brief
- **Mail itself needs no new code.** The sending code (django-anymail with Brevo, the queue, the cap, the console page) is built and tested; this cycle is DNS, a Brevo account, environment settings and tests, mostly the owner's.
- **One small code change, the reset-link lifetime (Q1):** a second token generator for e-mailed links, with its own salt and a 1-hour limit, and a confirm view that accepts a token from either generator. `send_password_reset()` makes its link with the new generator; `reset_path()` (the operator's hand-made link) keeps the default generator and the 3-day `PASSWORD_RESET_TIMEOUT`. The e-mail template says hours instead of days.
- **Turn it on in a safe order:** pause candidate e-mails, set the Render environment, run the tests (8, 9), the rehearsal (10), then the friend (11). Unpausing candidate e-mails is a separate decision and is not part of this cycle's measure.
- **Rejected options:**
  - *Set `PASSWORD_RESET_TIMEOUT` to 1 hour for everything:* the operator's hand-over links, which are passed by message and often opened the next day, would expire (Q1 answer).
  - *Store each reset token in the database and expire it there:* more tables and code than one small generator; Django's tokens already stop working after one use.
  - *Build bounce handling now:* parked by the owner (Q2).
  - *A strict DMARC policy from day one:* a small mistake would send the first invitations to spam (Q3).

## Interfaces and data
- **Code:** `jobs/accounts.py` (a second generator, next to `reset_path`), `jobs/mail.py` (`send_password_reset` uses it and passes "1 hour"), `jobs/views_mail.py` (`ResetConfirmView` accepts both), `jobs/templates/jobs/mail/password_reset.txt` and the French translation file (hours wording).
- **Tests:** `tests/test_mail.py` and `tests/test_accounts.py` (criteria 13 to 16).
- **No migration, no new setting.** The existing `PASSWORD_RESET_TIMEOUT` stays 3 days.
- **Environment (owner):** `SAXOBEAT_MAIL`, `BREVO_API_KEY`, `SAXOBEAT_PUBLIC_URL`, `SAXOBEAT_MAIL_REPLY_TO` on Render and in `.env`, and now also `SAXOBEAT_MAIL_FROM` (the deployed default is still the old domain, D1); optionally `SAXOBEAT_MAIL_DAILY_CAP`.
- **DNS at IONOS (the DNS host of `saxobeat.fr`):** Brevo's records (found in place 2026-10-30, see the evidence file). The root domain's own records (IONOS mail: MX and SPF) are not touched. `stoyan.ovh` is no longer involved in sending. (changed 2026-10-30, D1)
- **Docs that change** (named in `learn.md`): DEPLOY.md §7 (step 1 done, the pause step, the rollback), PRD_users_and_emails.md §7.3 and §9 (1 hour, e-mail live).

## Constraints
- **Secrets:** the Brevo key goes only into Render's settings and the PC's `.env`, never into chat, a file in the repo or a command line (a tool prints yes or no, never the value).
- **Cost:** Brevo's free plan; nothing is bought. If Brevo requires a card or a paid plan, stop and ask.
- **Privacy:** e-mails carry titles, employers and scores, never CV text or notes (PRD §7.6, unchanged).
- **Reach:** the first real send is one friend. Candidate e-mails stay paused through the whole cycle.
- **A 1-hour link covers the whole visit:** Django checks the token again when the new password is submitted, so a person who opens the link at 55 minutes and types for 10 minutes will be refused and must ask again. Accepted.
- **Claude does not use the owner's Brevo, Render or DNS accounts and does not run the runner against the hosted database;** those steps are the owner's.

## Risks
| Risk | What reduces it |
|---|---|
| E-mail lands in spam | Records checked first (criterion 1); Gmail and Outlook tests (8, 9) before any friend |
| Existing friends get unexpected e-mails when mail is switched on | Candidate e-mails paused first (6); the count is read before unpausing |
| ~~The sender is `saxobeat.fr` and the links are `jobs.stoyan.ovh` (a mismatch some filters score slightly)~~ | Closed by D4: the links are on `app.saxobeat.fr`, the sender on `mail.saxobeat.fr`, one organisational domain |
| A stricter DMARC later would also apply to the owner's own IONOS mailbox, because the record sits on the root | When tightening, put the stricter record on `_dmarc.mail.saxobeat.fr` only (learn step) |
| Links point to `onrender.com` or `localhost` | `SAXOBEAT_PUBLIC_URL` on Render and in `.env` (3, 4); checked in received e-mails (12) |
| A bounce is invisible to the app | Parked (Q2); Brevo's dashboard lists bounces; reopen if a friend reports a missing e-mail |
| The reset change breaks the operator's links | Criteria 14 and 15, written before the change |

## Out of scope
- Bounce and complaint handling (register R3), parked in Q2.
- Reminder and alert e-mails (cycle 009), a nicer HTML e-mail (cycle 011).
- Turning candidate e-mails (AI-ready, digest) on for friends, and moving DMARC to `quarantine` after two weeks of clean reports: both are decisions after this cycle, listed in `learn.md`.
- Receiving mail at `no-reply@mail.saxobeat.fr` (the sending subdomain has no mailbox; replies go to the reply-to address).
- ~~Removing `jobs.stoyan.ovh` from Render~~: done by the owner on 2026-10-30 (D5). *(Moving the app itself to `app.saxobeat.fr` is no longer out of scope: D4, criterion 19.)*
- Running the runner or `mail send` against the hosted database from this session.

## Gate
- [x] Owner approved this spec (2026-10-30, "Approve spec")
