# Learn: make e-mail live (Brevo, mail.saxobeat.fr, app.saxobeat.fr)

| | |
|---|---|
| **Cycle** | 003 |
| **Stage** | Learn done 2026-11-03; the cycle's open items are carried in `next.md` |
| **Verify** | [verify.md](verify.md), accepted by the owner 2026-11-03 **with risks** (9 pass, 7 partial, 3 not met) |

## What happened vs what we expected
- **Success measure** (intent, as changed by D1 and D4): a test e-mail in the inbox at Gmail and Outlook with authentication passing, one real invitation sent and used, the E-mails page showing it sent, links opening `https://app.saxobeat.fr` with a valid certificate. **Met in part:** Gmail inbox yes (header lines not seen), iCloud spam, Outlook not tried, no real invitation sent yet; the E-mails page and the certificate are right.
- **Expected** a code change (the 1-hour reset link) and a mostly owner-side set-up. **Found** the same, but two plan changes by the owner (D1 new sending domain, D4 app on `app.saxobeat.fr`) and two Brevo surprises: the IP allow-list (401) and the sender setup. All code work and its tests landed on day one (1,303 passed); every delay since was set-up or waiting for the owner's accounts.
- **Not expected:** the iCloud result. A new domain starts in spam at some providers, and nothing in the code or DNS is wrong as far as we have seen.
- **Cost:** two Claude sessions plus the owner's time at Brevo, IONOS and Render; no money; no read of the hosted database.

## What we learned
- **"It worked" is not "it arrived".** The app marks an e-mail *sent* when Brevo accepts it. The first "sent" never reached the inbox until the sender was fixed in Brevo. Always ask where the message landed, not what the page says.
- **A provider's IP allow-list and a shared host do not mix.** Brevo's *Authorised IPs* gave a 401 on Render's shared outbound address; the owner allowed the one address (D3) and kept the protection. It is an accepted failure waiting to happen, and it is now written in DEPLOY.md §7 with its sign (the 401 text on the E-mails page).
- **Move the domain before anyone uses it.** The move to `app.saxobeat.fr` and removing `jobs.stoyan.ovh` cost a morning because nobody had an account, a link or a bookmarklet to break.
- **A host setting and a form setting fail differently.** A wrong allowed host is a 400 on every page; a wrong CSRF origin is a 403 only on submit, so a page load proves nothing (criterion 19 still awaits a form submitted on the new host).
- **New sending domains start cold.** Mail to Gmail was fine, to iCloud it went to spam. Small steady volume and "Not junk" marks are the only levers; nothing to build.
- **The full suite has an order-dependent failure.** On 2026-11-03 `tests/test_auto_reject.py::test_putting_it_back_to_applied_restarts_the_month` failed in a full run (1 failed, 1,338 passed) and passed alone, so it depends on test order or the date; unrelated to e-mail, and not looked into here.

## What moves where
| Finding | Goes to | Done |
|---|---|---|
| The brevo set-up as done: new domains, five settings, the sender in Brevo, the IP allow-list and its fix, the off switch, the DMARC tightening on the sub-domain only | `docs/DEPLOY.md` §7 | [x] |
| One-hour e-mailed link vs three-day hand-made link | `docs/DEPLOY.md` (forgot-password paragraph), `docs/PRD_users_and_emails.md` §7.3 (already said one hour) and §9 | [x] |
| Domain `saxobeat.fr`, `no-reply@mail.saxobeat.fr`, the app on `app.saxobeat.fr` | `docs/PRD_users_and_emails.md` status, §7.2, D8 | [x] |
| The deployed default sender was still the old domain | `config/settings.py` default changed to `Saxobeat <no-reply@mail.saxobeat.fr>` (mail, accounts and ops tests pass); `render.yaml` carries the key | [x] (live after the next push) |
| Outlook, header lines, the rehearsal, the first friend, a reset e-mail made on the host, a form on the new host | `next.md` (owner, not blocking Learn); a short line in `verify.md` is the record | open |
| The unknown failed e-mail (F2) | `next.md` (owner reads the row; if it is the Brevo 401, D3 happened) | open |
| Candidate e-mails stay paused; counts before any unpause; the PC is not on Brevo's list | a later decision (new intent when wanted); slice 11 of the plan is **not done** | open |
| Bounces and complaints (R3) | parked; Brevo's dashboard lists them; reopen if a friend reports a missing e-mail | open |
| The English e-mail is marked `lang="fr"` in its HTML (found while checking the templates) | cycle 011 (small gaps) | open |
| DMARC to `quarantine` after two weeks of clean Brevo reports, on `_dmarc.mail.saxobeat.fr` only | a later cycle | open |
| The order-dependent test failure above | a small fix, any cycle that touches auto-reject | open |
| Cycle 009 (reminders) was waiting for e-mail | unblocked in principle; the pause and the first friend still gate real use | noted |

## Process feedback
- **Worked well:** pausing candidate e-mails before switching mail on; putting every owner step in `next.md` as a line the board shows; writing the decisions (D1 to D5) as the owner changed course, so the spec could be edited with "changed" marks instead of rewritten.
- **Slowed us down:** `next.md` drifted behind the chat (answered actions stayed open for days), so "what next?" was wrong for a while; and the spec's 19 criteria include four that only the owner can see, so verify waited on the owner's accounts. Next time tick the line in the same turn as the answer, and say in the spec which criteria are code-only and can close first.

## Next cycle candidates
- **Unpause candidate e-mails** for friends, after the counts and a first friend report (new intent).
- **DMARC tightening** and **bounce handling** (small, after two weeks of Brevo reports or a missing e-mail).
- **Cycle 009** (reminders) and **011** (the `lang="fr"` finding, a nicer HTML e-mail).
