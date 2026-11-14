# Decisions: make e-mail live

One entry per decision, newest last. Do not edit old entries: add a new one that supersedes.

## D1. Send from a new domain, `mail.saxobeat.fr`, as `no-reply@mail.saxobeat.fr`; the app stays on `jobs.stoyan.ovh` for now
- **Date:** 2026-10-30
- **Context:** The intent, spec and plan (all approved the same day) assumed Brevo would send from `mail.stoyan.ovh` as `hello@mail.stoyan.ovh`, with the owner's DNS at the `stoyan.ovh` host. The owner then registered `saxobeat.fr`, set up the Brevo account with the sending subdomain `mail.saxobeat.fr`, and chose `no-reply@mail.saxobeat.fr` as the sender. `mail.stoyan.ovh` was never given any DNS record (checked 2026-10-30).
- **Options considered:** (a) keep `mail.stoyan.ovh` as written; (b) the new domain, as the owner chose; (c) the new domain and move the app to `jobs.saxobeat.fr` in the same cycle.
- **Decision:** (b). Sending domain `mail.saxobeat.fr`, sender `Saxobeat <no-reply@mail.saxobeat.fr>`. The app stays on `https://jobs.stoyan.ovh`, so `SAXOBEAT_PUBLIC_URL` is unchanged. Moving the app to a `saxobeat.fr` address is the owner's later step, not part of this cycle.
- **Why:** The owner's own words: "I'm going with a new domain saxobeat.fr". A product name on its own domain is a better sender than a personal domain, and the work done so far (the 1-hour reset link, the pause, the push) does not depend on the domain.
- **Consequences:**
  - Intent goal and success measure, spec criteria 1, 3, 4, 8 and 9, the interfaces and out-of-scope lists, and plan slices 6 to 8 are rewritten for the new domain, each marked "changed 2026-10-30 (D1)". The old text is in git history (`6f504a7`).
  - The deployed code's default sender is still `Saxobeat <hello@mail.stoyan.ovh>`, so the sender must be set by the environment variable `SAXOBEAT_MAIL_FROM` on Render and in the PC's `.env` (one more setting: five, not four). The default in `config/settings.py`, `render.yaml` and the docs is changed later, in the learn step.
  - The sender `no-reply@` cannot receive replies; `SAXOBEAT_MAIL_REPLY_TO` stays in the plan so a friend who answers reaches the owner.
  - **The DKIM signature is probably for `saxobeat.fr`, not `mail.saxobeat.fr`** (Brevo's DKIM records are named under `saxobeat.fr`: `brevo1._domainkey.saxobeat.fr`, `brevo2._domainkey.saxobeat.fr`). The headers expected in slices 8 and 9 are `dkim=pass` (any Brevo signature for `saxobeat.fr`), `spf=pass`, `dmarc=pass`; the exact `header.d=` is read from the first test, not assumed.
  - Links in e-mails point to `jobs.stoyan.ovh` while the sender is `saxobeat.fr`: a mismatch some filters score slightly; accepted until the app moves.

## D2. Keep the DMARC record Brevo's setup put on the root (`p=none`, reports to Brevo); no record of our own
- **Date:** 2026-10-30
- **Context:** Q3 had said DMARC `p=none` with reports to the owner, at `_dmarc.mail.stoyan.ovh`. With the new domain (D1) the lookup found `_dmarc.saxobeat.fr` already set: `v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com`. It covers `mail.saxobeat.fr` by inheritance (no `sp=`). There is no record on `_dmarc.mail.saxobeat.fr`.
- **Options considered:** (a) keep Brevo's record as it is; (b) add `_dmarc.mail.saxobeat.fr` with `rua=` to the owner, so the subdomain has its own policy and its reports reach the owner.
- **Decision:** (a), the owner's choice ("Keep the DMARC record Brevo put on the root").
- **Why:** The policy is the same (`none`); the reports go to Brevo, which summarises them, so there is nothing for the owner to read; one record fewer to maintain.
- **Consequences:** Supersedes the "reports to the owner" half of Q3 (the `p=none` first, `quarantine` after two weeks of clean reports half stands, but "clean reports" now means what Brevo's dashboard shows). The record is on the root, so a stricter policy there would also apply to the owner's own IONOS mailbox on `saxobeat.fr`: when it is time to tighten, put the stricter record on `_dmarc.mail.saxobeat.fr` only. That step is a candidate for the next cycle, not this one.

## D3. Allow only Render's current outbound address (74.220.51.142) at Brevo, and leave the IP protection on
- **Date:** 2026-10-30
- **Context:** The first test e-mail failed with Brevo 401 "unrecognised IP address 74.220.51.142": Brevo's Authorised IPs protection refuses API calls from addresses not on its list. Render's outbound addresses are shared across a region and a service "might use any IP address within its associated ranges" (Render's documentation, fetched 2026-10-30), and the PC's home address is not static.
- **Options considered:** (a) switch Brevo's IP blocking off (Claude's recommendation); (b) allow Render's whole outbound range, if Brevo accepts a range (not verified); (c) allow just the one address in the error message.
- **Decision:** (c), the owner's choice: "added the one IP for now. If IP change, I'll bring it up for a solution. For the moment, keep it that way."
- **Why:** Keeps Brevo's protection on, which limits where the key can be used from, at the price of possible failures later. The owner accepts that and will raise it if it happens.
- **Consequences:**
  - **A failure to expect:** if Render sends from another address in its range (a redeploy, a restart, a region change), the next e-mail fails with the same 401. The signs: the E-mails page shows failures, and an invitation or reset is not delivered. Every account e-mail is affected (invitation, welcome, reset, changed), not only tests. The fix then is the owner's: add the new address, or choose (a) or (b).
  - **The PC is not on the list.** A run on the PC that sends mail (`manage.py mail send`) would fail with the same 401. Today that cannot matter: candidate e-mails are paused, and account e-mails are sent by the web app on Render. If the owner unpauses candidate e-mails, this decision has to be revisited first.
  - A failed e-mail is kept and retried up to three times; after that its state is *failed* and the console offers a retry. A friend whose invitation or reset failed has to be told by hand.
  - Acceptance criterion 18-style claims ("it works on the host") are only as good as the day they were measured; the criterion stays checkable, and this risk goes into `learn.md` and `verify.md` as an accepted risk, dated 2026-10-30.

## D4. Move the app to `app.saxobeat.fr` now, before anyone signs up; keep `jobs.stoyan.ovh` attached
- **Date:** 2026-10-30
- **Context:** D1 left the app on `jobs.stoyan.ovh` "for now" and called the move the owner's later step. The owner then decided: "I prefer to do it now before people sign up", and chose the host `app.saxobeat.fr`. Read-only lookups before the move: `app.saxobeat.fr` has no CNAME and no A record, and `saxobeat.fr` has no wildcard.
- **Options considered:** (a) stay on `jobs.stoyan.ovh`; (b) a subdomain of `saxobeat.fr` (`app.`), one CNAME to the Render service; (c) the root `saxobeat.fr`, which needs an A record next to the IONOS mailbox's MX, SPF and the Brevo and DMARC records.
- **Decision:** (b), `https://app.saxobeat.fr`. The old address `jobs.stoyan.ovh` stays attached on Render and in the allowed lists for now (invitations already sent, unsubscribe links in e-mails already sent, and the capture bookmarklet, which is built from the host the person was on when they installed it).
- **Why:** The owner's wish; the sender (`mail.saxobeat.fr`) and the links then share one organisational domain, which removes the mismatch D1 had accepted; and no friend has signed up yet, so nobody has to sign in again or reinstall anything.
- **Consequences:**
  - Four settings change: on Render `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` (add the new host, keep the old) and `SAXOBEAT_PUBLIC_URL` (the new address); in the PC's `.env` `SAXOBEAT_PUBLIC_URL`. A missing host gives a 400, a missing origin gives a 403 on every form.
  - Spec: criteria 3 and 10 name the new address; a new criterion 19 checks the move itself; the risk row about the link and sender mismatch is closed. Plan: a new slice 7b, and the rehearsal (slice 9) and the first friend (slice 10) wait for it, so the first real e-mails already link to the new address.
  - `render.yaml` and the docs (DEPLOY.md section 7, PRD_users_and_emails.md section 7.2 and D8) name the new address; the docs in the learn step.
  - Nothing changes at Brevo (the sender domain and Render's allowed address stay as they are).

## D5. `jobs.stoyan.ovh` is removed from Render, on purpose (supersedes the "keep it attached" part of D4)
- **Date:** 2026-10-30
- **Context:** D4 moved the app to `app.saxobeat.fr` and said to keep `jobs.stoyan.ovh` attached. Claude's checks at 17:30 and 17:35 UTC found it no longer served a certificate (TLS handshake failure) and asked why. The owner answered: "i removed the old jobs.stoyan.ovh domain".
- **Options considered:** (a) keep the old address attached (D4); (b) remove it now, while no friend has signed up.
- **Decision:** (b), the owner's own action. No e-mail with a link on the old address has been sent (only test e-mails), nobody has an account, no bookmarklet or installed app has been handed out, so nothing depends on it.
- **Why:** One address only, and it is cheaper to remove it before anyone uses it than after.
- **Consequences:**
  - D4's reasons for keeping it (invitations, unsubscribe links and bookmarklets already out) do not apply yet; they would have applied later.
  - A test e-mail sent before the move may contain a link to the old address: it no longer works. Harmless.
  - The CNAME `jobs` at the OVH DNS host for `stoyan.ovh` now points at a Render service that no longer has that name: the owner can delete it (a tidy-up, not blocking).
  - `render.yaml` no longer lists the old address; the spec's criterion 19 no longer asks for it to answer. The address of the service itself, `saxobeat.onrender.com`, still answers.
