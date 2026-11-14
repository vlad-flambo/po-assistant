# Intent: make e-mail live (Brevo, mail.stoyan.ovh, jobs.stoyan.ovh)

| | |
|---|---|
| **Cycle** | 003 |
| **Stage** | Intent (approved 2026-10-30) |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Born from** | The PRD audit of 2026-10-29: outstanding items moved here from the PRDs (see the table below). |
| **Importance** | 4/5 (claude, 2026-10-30): nothing is e-mailed yet: invitations and resets depend on passing links by hand; blocks cycle 009 |

## Change of 2026-10-30 (owner, see [decisions.md](decisions.md) D1)
The owner chose a new domain after the intent was approved: the sending domain is **`mail.saxobeat.fr`**, the sender **`no-reply@mail.saxobeat.fr`**, the Brevo account is set up with it. The app stays on `jobs.stoyan.ovh` for now (later the same day the owner moved the target to `app.saxobeat.fr`, [decisions.md](decisions.md) D4). The goal and the success measure below are updated; the facts table keeps what was true when it was written (at that time `mail.stoyan.ovh` had no records and was never used).

## The request, in your words
> Do a full audit of the PRD files. I want to migrate anything outstandin into the ai sdlc framework, using the ai-sdlc skill

### What this cycle inherits from the PRDs
| Item | Where it came from |
|---|---|
| U4/U5 are deployed but nothing is sent: `SAXOBEAT_MAIL` is not set on Render or the PC | PRD_users_and_emails.md status line; DEPLOY.md §7 |
| The app on its own address `jobs.stoyan.ovh` (D8) | PRD_users_and_emails.md §7.2, D8 |
| A reset link lasts 3 days, not the 1 hour the PRD asked for | PRD_users_and_emails.md §7.3 and §9 'What was built' |
| Bounces and complaints (the provider's webhook stops sending to a bouncing address) | PRD_users_and_emails.md register R3 |

## Why now / the pain
The e-mail code is live since 28 October but switched off: invitations, password resets and the AI-ready e-mails still depend on the owner passing links by hand.

## Goal
Friends get Saxobeat's e-mails in their inbox (not spam), sent from `no-reply@mail.saxobeat.fr`, with links on `app.saxobeat.fr` (changed 2026-10-30, D1 and D4; was `mail.stoyan.ovh` and `jobs.stoyan.ovh`).

## Success measure
A test e-mail lands in the inbox (not spam) in Gmail and Outlook with DKIM, SPF and DMARC passing for the Brevo-authenticated `saxobeat.fr` (changed 2026-10-30, D1; was `mail.stoyan.ovh`); one real invitation is sent and used; the console's E-mails page shows it sent; the links in it open `https://app.saxobeat.fr` with a valid certificate (checked after the move, D4), not the `onrender.com` name. *(confirmed by the owner, 2026-10-30)*

## Not doing (this cycle)
- Reminder and alert e-mails (cycle 009).
- A nicer HTML e-mail (cycle 011).

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| Sending goes through Brevo's HTTPS API with django-anymail; `SAXOBEAT_MAIL` is one of brevo, resend, console, off, and is `off` by default when `DJANGO_DEBUG=0` | `config/settings.py`, `jobs/mail.py` |
| **Step 1 of DEPLOY.md §7 is already done:** `jobs.stoyan.ovh` is a CNAME to `saxobeat.onrender.com`, and it serves the app (HTTP 302 to `/login/`) with a valid certificate (CN `jobs.stoyan.ovh`, Google Trust Services, issued 2026-10-27, valid to 2027-01-25; curl's verify result 0) | `Resolve-DnsName` and `curl`, read-only, 2026-10-30 14:31 UTC |
| **Not done yet:** `mail.stoyan.ovh` has no DNS records at all (no TXT, no DKIM CNAME, no DMARC at `_dmarc.mail.stoyan.ovh` or `_dmarc.stoyan.ovh`), so Brevo's domain is not authenticated | `Resolve-DnsName`, read-only, 2026-10-30 |
| The root `stoyan.ovh` has its mail at OVH (MX `mx1-3.mail.ovh.net`, SPF `v=spf1 include:mx.ovh.com -all`). The sending subdomain is a separate name with its own records, so Brevo's records on `mail.stoyan.ovh` do not touch the owner's own mailbox. The address given as reply-to may be on that OVH mailbox: **to be verified** by the owner | same lookup |
| Whether `SAXOBEAT_PUBLIC_URL` is already set on Render is unknown to Claude (no access to Render's settings). Without it the links use `RENDER_EXTERNAL_HOSTNAME`, which is the `onrender.com` name, not `jobs.stoyan.ovh` | `config/settings.py:171` |
| An e-mailed reset link is made by `reset_path()` with Django's `default_token_generator`, so the 3-day `PASSWORD_RESET_TIMEOUT` applies to it; a 1-hour limit for e-mailed links needs a second generator and a confirm view that accepts both | `jobs/accounts.py:114-116`, `config/settings.py:130` |
| `render.yaml` already allows `jobs.stoyan.ovh` and lists `SAXOBEAT_MAIL`, `BREVO_API_KEY`, `SAXOBEAT_PUBLIC_URL`, `SAXOBEAT_MAIL_REPLY_TO` as values to fill (sync: false) | `render.yaml` |
| The owner's steps (CNAME, Render custom domain, Brevo domain records, DMARC, API key, env on Render and the PC, a test) are written down | DEPLOY.md §7 |
| Brevo's free plan: 300 e-mails a day, from third-party reviews dated 2026: **still to be verified**. Brevo's pricing page is drawn by JavaScript (Claude's fetch returned only the title) and its help centre refused the fetch (HTTP 403), so the owner reads it on the Brevo dashboard when creating the account | PRD_users_and_emails.md §7.1; fetch attempts 2026-10-30 |
| `PASSWORD_RESET_TIMEOUT` is 3 days for every reset link, including the ones the operator makes by hand | `config/settings.py` |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | How long should an e-mailed reset link last? | 1 hour for links sent by e-mail (a second token generator), 3 days kept for the links the operator makes by hand | **1 hour for e-mailed links; 3 days kept for the operator's hand-made links** (owner, 2026-10-30, "Yes, 1 hour"). Consequence for the spec: a second token generator for e-mailed links, and a confirm view that accepts a token from either generator | answered |
| Q2 | Bounce handling in this cycle? | No: park it until real volume shows bounces (watch the console's failures meanwhile) | **Parked** (owner, 2026-10-30, "all yes"). Note: the app marks an e-mail SENT when Brevo's API accepts it (`jobs/mail.py:131`), so a later bounce is invisible to it; Brevo's own dashboard lists bounces. Reopen as its own cycle (register R3) if a friend reports a missing e-mail or the dashboard shows repeated bounces | parked |
| Q3 | DMARC policy? | Start at `p=none` with reports to the owner; move to `quarantine` after two weeks of clean reports | **`p=none` with reports to the owner, at `_dmarc.mail.stoyan.ovh`; `quarantine` after two weeks of clean reports** (owner, 2026-10-30, "all yes"). The move to `quarantine` is a one-line DNS edit after this cycle's measure is met, so it goes to `next.md`/learn, not into the acceptance criteria | answered |
| Q4 | Who receives the first real invitation? | A friend the owner chooses, after the Gmail and Outlook tests pass | **The Gmail and Outlook tests first (console *Send a test*, inbox not spam, "signed by mail.stoyan.ovh"), then one relaxed friend the owner names when the tests pass** (owner, 2026-10-30, "all yes"). Claude's addition, folded into the tests: a test to a second address of the owner's own comes before any friend | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Secrets: the Brevo API key goes to Render's settings and `.env` only, never chat or the repo.
- A domain misconfiguration sends e-mail to spam: test before any real invitation.

## Gate
- [x] All open questions answered or parked (Q1, Q3, Q4 answered, Q2 parked; owner, 2026-10-30)
- [x] Goal and success measure confirmed by the owner (2026-10-30, "Confirm both")
