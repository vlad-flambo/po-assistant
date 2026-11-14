# Next: cycle 003

Each line is one action: `- [ ] [owner|claude|both] <date, optional> text`. Tick it when it is done, add new ones as the cycle moves. This file is what the cycle board shows as "what next?".

- [x] [owner] 2026-10-30 Answer Q1-Q4, confirm goal and success measure (Intent closed)
- [x] [owner] 2026-10-30 Approve spec.md and plan.md
- [x] [claude] 2026-10-30 Slices 1-3: reset-link tests, the code, a local run (full suite 1,303 passed)
- [x] [both] 2026-10-30 Slice 4: pushed `main` (`a18ca9b..6f504a7`), deploy Live (owner's word)
- [x] [owner] 2026-10-30 Slice 5: candidate e-mails paused in the console (owner's word)
- [x] [owner] 2026-10-30 New sending domain `mail.saxobeat.fr`, sender `no-reply@mail.saxobeat.fr` (decisions.md D1); D2 Brevo's DMARC kept
- [x] [owner] 2026-10-30 Slice 6: Brevo Authenticated, 300 e-mails a day, API key generated (`evidence/brevo_limits.md`)
- [x] [owner] 2026-10-30 Slice 7: the five settings on Render and in `.env`; `.env` checked by names and shape, git-ignored, no key-shaped string in the repo or its history
- [x] [owner] 2026-10-30 D3: only Render's address `74.220.51.142` allowed at Brevo (accepted risk: a different Render address fails again, the PC is not on the list)
- [x] [owner] 2026-10-30 Slice 8: the Gmail test landed in the inbox, no issue (owner's word); the sender issue was in Brevo's sender setup
- [x] [owner] 2026-10-30 Slice 8, Outlook: deferred (no Outlook account); criterion 9 stays open, accepted risk
- [x] [owner] 2026-10-30 D4: the app moves to `app.saxobeat.fr` before people sign up; slice 7b done: DNS, certificate and the allowed host proven by Claude's checks (`evidence/app_move_check_2026-10-30.md`), the E-mails page reads "links to https://app.saxobeat.fr"
- [x] [owner] 2026-10-30 D5: `jobs.stoyan.ovh` removed from Render on purpose
- [x] [claude] 2026-11-02 Ticked the actions that were answered but still open here (slice 7b, the Render checks, the old-domain question, the superseded slice 8 line); slice 9's text now names `app.saxobeat.fr`
- [x] [owner] 2026-11-03 iCloud test e-mail: delivered, landed in spam (`evidence/deliverability_icloud_2026-11-03.md`); no Build work left in code, owner said "move on"
- [x] [claude] 2026-11-03 Drafted `verify.md` (9 pass, 7 partial, 3 not met: 9, 10, 11)
- [x] [owner] 2026-11-03 Verdict on `verify.md`: "Accept with risks" (9 pass, 7 partial, 3 not met)
- [x] [claude] 2026-11-03 Learn: `learn.md`, DEPLOY.md §7, PRD_users_and_emails.md (status, §7.2, §9, D8), default sender in `config/settings.py` (47 mail, accounts and ops tests pass; a full run: 1,338 passed, 1 failed, an order-dependent test in `test_auto_reject.py`, passes alone)
- [ ] [owner] Carried over, not blocking: the console's E-mails page, open the **failed** row (it was *waiting* on 2 Nov) and tell me its kind, address and error text (verify F2; if it is the Brevo 401, D3 has happened). Do this before the first friend
- [ ] [owner] Carried over: the rehearsal (invite a second address of yours, create the account on `app.saxobeat.fr`, then "Forgot password": "1 hour", links to `app.saxobeat.fr`), then the first friend, ideally Outlook/Hotmail/Live (criteria 9 to 12, 18, 19)
- [ ] [owner] (optional) which address you had open when you sent the iCloud test: if `app.saxobeat.fr`, it also proves a form works there (criterion 19)
- [ ] [owner] Say "close 003" to mark the cycle Closed in the README when you are content with the carried items; they stay listed above
- [x] [owner] 2026-11-02 "Commit docs": Claude committed the cycle 003 documents and `render.yaml` as `51581c8` (own paths only, not pushed)
- [x] [owner] 2026-11-02 "Push now": `c4ea86f..51581c8` pushed to `origin/main` (only `51581c8` was still unpushed: the earlier commits, including cycle 001's Insights fix, were already on `origin`). Render's live settings do not depend on `render.yaml`
- [ ] [owner] (tidy-up, not blocking) delete the CNAME `jobs` at the OVH DNS host for `stoyan.ovh`, it now points at nothing
- [ ] [owner] (optional, not blocking) paste the SPF, DKIM, DMARC lines from Gmail's "Show original" of the test e-mail, and one line on what you changed in Brevo's sender setup (for DEPLOY.md)
- [ ] [claude] Not done, a later decision: slice 11 (counts of who an unpause would e-mail, with the owner's OK); asked for only when the owner wants to unpause candidate e-mails
- [ ] [both] Next cycle candidates are in `learn.md` (unpause candidate e-mails, DMARC tightening, bounces, 009 and 011); the push of the learn-step commit is the owner's call
