# PRD — Standard and power modes, blocked employers, viewing as a candidate, and e-mail

| | |
|---|---|
| **Status** | **Built, U1 to U5 (28 October 2026)**, tests on SQLite and Postgres. **E-mail is live since 2026-10-30 (cycle 003):** Brevo, sending domain `mail.saxobeat.fr`, the app on `app.saxobeat.fr`, candidate e-mails paused; tried with Gmail (inbox) and iCloud (spam), not yet with Outlook or a real invitation (DEPLOY.md §7, [003's verify](sdlc/cycles/003-email-live/verify.md)). Differences from this text are under §9. |
| **Date** | 28 October 2026 |
| **Author** | Vladimir (product), written with Claude |
| **Builds on** | [PRD_multi_user.md](PRD_multi_user.md) (candidates, invitations, operator links handed over by hand), [PRD_ai_backoffice.md](PRD_ai_backoffice.md) (AI tasks, job screening selection, the `/ops/` console; its §3 put e-mail out of scope and its §9 said the console never acts inside a candidate's space: **this PRD changes both**), [PRD_mobile.md](PRD_mobile.md) (the phone-first candidate interface), [DEPLOY.md](DEPLOY.md) (Render free web service, Neon, the PC runner) |
| **Scope** | (1) a **standard mode** for candidates, the default, with a trimmed interface whose inbox shows the AI's picks; the current interface becomes **power mode**, switched on by the operator only; (2) **blocked employers**: a candidate hides an employer for good; (3) **view as**: the operator sees and uses the app as a given candidate, logged; (4) **e-mail**: account e-mails, "your AI results are ready", and a digest of new matches, sent through a free hosted service. |
| **In one line** | Friends get a short list of jobs worth applying to and an e-mail when it changes; the operator keeps the full tool, and can step into anyone's account to see what they see. |

---

## Outstanding work (moved to SDLC cycles on 2026-10-29)

What this PRD still asks for is now tracked as cycles in `docs/sdlc/` ([the audit](sdlc/cycles/006-stale-docs/evidence/prd_audit_2026-10-29.md)). This PRD stays the product-level reference; the cycles carry the work.

- E-mail live (Brevo, `mail.saxobeat.fr`), `app.saxobeat.fr`, the one-hour reset link: done in [003](sdlc/cycles/003-email-live/verify.md) (2026-11-03, accepted with open risks). R3 bounces: still parked; unpausing candidate e-mails is a later decision
- Deploy checks (migrations 0037-0040, migration 0039's log, friends in standard mode): [004](sdlc/cycles/004-hosted-checks/intent.md)
- The view-as band on a real phone: [005](sdlc/cycles/005-real-devices/intent.md)
- Undo after blocking, a nicer HTML e-mail: [011](sdlc/cycles/011-settings-polish/intent.md)
- R1 operator e-mails, R2 reminders: [009](sdlc/cycles/009-reminders-alerts/intent.md)
- §13 success measures: [007](sdlc/cycles/007-success-measures/intent.md)
- R4 candidates choose their mode, R5 blocks as a signal: [the backlog](sdlc/backlog.md)
- **Invitation codes (cycle 033, 2026-11-06):** sign-up is no longer only by the operator's single-use link. A public `/signup/` takes an *invitation code* (made by the operator on *People*, or the one code each candidate has on *Inviter des amis*), records where each account came from, and is limited (10 wrong codes per address per 15 minutes; 3 sign-ups per address and 20 in all per hour). Single-use invitation links are unchanged; the invitation e-mail is still the operator's only e-mail for new people (a candidate cannot e-mail an invitation from the app yet). [Spec](sdlc/cycles/033-referral-codes-for-sign-up/spec.md), [verify](sdlc/cycles/033-referral-codes-for-sign-up/verify.md).

---

## 1. Problem

| Area | Today (read in the code on 28 October 2026) | What goes wrong |
|---|---|---|
| **Interface** | One interface for everybody, built for the operator: a search field and a *Filters* sheet (breadth, minimum score, added, salary, English, reposts, employers, AI reviewed, apply / don't apply, sort), a CSV export, a "clear the noise" bulk dismiss, the bookmarklet, the keyboard hint *"j/k move · s shortlist · d dismiss · o open · Enter details"* (`jobs/templates/jobs/inbox.html`, `_filters.html`). The inbox holds every job that passed the person's filters: hundreds. | A friend opens the app and sees a scoring engine. The useful part (the few jobs the AI said to apply to) is one filter among ten. |
| **Blocking an employer** | Possible, but hidden: a *Blocked companies (one per line)* text box in Settings (`filters.blocked_companies`), matched as a **substring** of the employer's name (`jobs/services/filters.py`); *Insights* suggests blocks after repeated dismissals. | Nobody finds it. Substring matching can catch the wrong employer (a short name inside a longer one). No way to block from the job itself, no note of why, no list to undo from. |
| **Seeing what a candidate sees** | Not possible. The console shows per-person numbers (*People*), never their screens. | Debugging "my inbox is empty" or "this job should not be here" means guessing, or asking for screenshots. |
| **E-mail** | None. Invitations and password-reset links are copied from *People* and sent by hand (`jobs/views_accounts.py`). AI results are announced only inside the app (`_ai_card.html`, the inbox strip). | Candidates do not know their AI reviews landed unless they open the app; the operator is the postman for every invitation and forgotten password. |

## 2. Goals

1. **A short, useful inbox for most people.** In standard mode the inbox shows the jobs worth applying to, never an empty screen on day one, and a single search to find anything else.
2. **Power mode stays exactly as it is,** for the operator and anyone he switches on. Modes hide things; they never delete data or change scores.
3. **Block an employer in two taps,** from a job, a company or the dismiss sheet; its jobs disappear now and in future; undo from one list.
4. **See any candidate's app as they see it, and act in it when needed,** with a banner that cannot be missed and a log of every session.
5. **E-mail that arrives:** account e-mails (invitation, welcome, password reset), one e-mail when AI results land, an optional digest; sent through a free hosted service from a verified domain, in the candidate's language, each kind switchable off by the candidate.
6. **Still free to run.** No new paid service; the e-mail provider's free tier covers 30 candidates with room to spare.

## 3. Out of scope

- Push notifications (register R4 of the AI PRD stays open), SMS.
- E-mails to the operator (new sign-up, source proposal, runner silent, files in *problems*): register R1 below.
- Reminder e-mails for follow-ups and interviews: register R2.
- A candidate switching modes themselves.
- Sharing blocks between candidates, or using them in the shared company profiles.
- Changing the score formula or the job screening selection (§4.3 reuses it as it is).

## 4. Standard mode and power mode

### 4.1 Who gets what

- `Candidate.mode`: `standard` (default) or `power`.
- **Every existing candidate becomes `standard`**, except the operator's own candidate, which becomes `power`.
- Only the operator switches it: console → *Candidates* → a person → *Mode*, or from the impersonation banner (§6). The candidate never sees a switch, nor the words "standard" or "power".
- Switching never touches data: statuses, notes, filters, keywords, scores are the same in both modes. A power setting changed earlier (keywords, breadth) keeps applying in standard mode; it is only not shown.

### 4.2 The standard inbox

```
┌─────────────────────────────────────────────┐
│ Inbox  4 picks · 6 coming            🔍  +  │
├─────────────────────────────────────────────┤
│ ✦ Head of Customer Success · Qonto     82   │
│   AI: apply · "Strong match on…"            │
│ ✦ VP Customer Operations · Alan        78   │
│ …                                           │
│ ── Coming up ─────────────────────────────  │
│ Customer Success Director · Swile      64   │
│   ✦ AI review · ready by Thu 10:30          │
│ …                                           │
└─────────────────────────────────────────────┘
```

**What is shown (D1, settled):**

| Section | Jobs | Order | Label |
|---|---|---|---|
| **Picks** | New jobs (not dismissed, shortlisted, applied…) the AI reviewed with verdict **apply** | Best final score first | ✦ AI: apply, with the first line of the AI's analysis |
| **Coming up** | New jobs **selected for an AI review** that have none yet: exactly the jobs `jobs/ai/selection.py` picks (top share, minimum score, per-candidate bounds, freshness) | Best rules score first | ✦ AI review · ready by … (the existing pending component) |
| **No AI consent** | For a candidate who declined AI: the same selection rule, without the AI, becomes their whole inbox: *"Your best matches"* | Best score first | The score, no AI label |

Not in the standard inbox: jobs the AI said **don't apply**, jobs below the selection, jobs hidden by filters. They are not deleted: search reaches them (§4.4), and the operator sees them in power mode or by viewing as the person.

Empty states:
- Nothing yet (a new candidate whose first jobs are being sorted): *"We're sorting the jobs for you. Your first picks arrive by Thu 10:30."*
- Nothing new: *"No new picks right now. We'll e-mail you when there are."* (if the AI-ready e-mail is on, §7) and a link *Search all jobs*.

Header count: *"4 picks · 6 coming"* instead of *"312 new"*. The tab badge counts picks only.

Swipe, shortlist and dismiss work as today. The "+" (add a job by link) stays: it is how a friend saves a job seen elsewhere.

### 4.3 What leaves the inbox in standard mode

| Removed | Note |
|---|---|
| The *Filters* button and sheet (breadth, minimum score, added, salary, English, reposts, employers, AI filters, sort) | Filters still apply as set; they are only not shown. |
| The search field as a permanent bar | Replaced by a search icon (§4.4). |
| The keyboard hint *"j/k move · s shortlist · d dismiss · o open · Enter details"* | The keys keep working on a laptop (harmless, undocumented). |
| *Export CSV*, *Clear the noise* (bulk dismiss), the bookmarklet | Power only. |
| *"Hide the N 'don't apply' jobs"* chip, *"N hidden below 50 · Show"* note | Meaningless when the inbox shows picks only. |
| *Filtered out & archive* button | Becomes *Dismissed jobs* under *More* (§4.5), to undo a dismiss. |

### 4.4 Search

- A magnifier icon in the inbox header (phone and laptop). Tap: a search field opens in place of the title, focused, with a close ✕.
- It searches **all the candidate's jobs that passed their filters and are not dismissed**, not only the picks; otherwise it would find nothing new. Matching is today's: every word on its own, in the title, the company or the text.
- Results are one list, best score first, each labelled: *AI: apply*, *AI: don't apply*, *AI review coming*, or nothing. Closing the search returns to the picks.
- The query stays in the URL (`?q=`), so back works and a result page can be shared with the operator.

### 4.5 Elsewhere in standard mode (D5, settled)

The same logic applied to the other pages:

| Page | Standard | Power only |
|---|---|---|
| **Menu** (tab bar / top bar) | Inbox, Pipeline, Interviews, More | — |
| **More** | Companies (with *Blocked employers*, §5), Dismissed jobs, Settings, language, log out | Contacts, Insights, Filtered out & archive |
| **Job page** | Title, company, signals (pay, remote, English), the AI review if any, *Why this job* in plain words (the AI's two sentences, or the 3 strongest reasons from the rules), Prepare with your AI, interviews, notes | The keyword breakdown, CV ↔ job match, score parts, platform details |
| **Settings** | My CV, *What I'm looking for* (the conversation), cities, *What we look for for you* (the screening brief), e-mails (§7.5), blocked employers, AI consent, account | Search breadth, keyword weights, profile text, blocked title words, max age, languages, salary floor as fields |
| **Pipeline, Interviews, Companies** | As today | — |

### 4.6 Power mode

Exactly today's interface. The operator's own candidate is `power`. A friend switched to `power` sees everything above; nothing else changes for them.

## 5. Blocked employers

### 5.1 Blocking

From three places, the same sheet:

1. **The job page** (and the card's long-press / "…" menu): *Block this employer*.
2. **The company page**: a *Block* button next to *Dream employer*.
3. **The dismiss sheet** ("Why dismiss?"): a new reason *Bad experience with this employer*, which offers *Also hide every job from Acme?* [Block] [Just this job].

The sheet:

```
Hide every job from Acme?
Now and in the future. Jobs already in your pipeline stay.
( ) Bad past experience   ( ) Not for me   ( ) Other
[ Private note (optional)                       ]
Also block: [ ] Acme Consulting   [ ] Acme Labs
                         [ Cancel ]  [ Block ]
```

- **Also block** lists the other employer names in the catalogue that clean to a close name (same root after `employers.clean_name`), **not ticked** (D12): blocking "Capgemini" can take "Capgemini Invent" and "Capgemini Engineering" with it only if the candidate ticks them.
- After blocking: the job leaves the screen with an *Undo* toast (5 s), as a dismiss does.

### 5.2 What a block does

| Effect | Detail |
|---|---|
| **New jobs** from the employer | Hidden by the filters with the existing reason `blocked_company` (power: visible in *Filtered out*). |
| **Jobs already in the inbox** | Hidden at once (the candidate's view of that employer's jobs is judged again). |
| **Jobs in the pipeline** (shortlisted, applied, interviewing, offer…) | **Untouched**: they are the candidate's history. |
| **AI** | Open `job_review` tasks for the employer's jobs are cancelled; none are created; company research is not requested for them. |
| **Search, digest, picks, dream bonus** | The employer never appears. A blocked employer cannot be a dream employer (blocking clears the flag, with a line saying so). |
| **Privacy** | Private to the candidate; never in a shared company profile, never counted across candidates. The operator sees it only by viewing as the person. |

### 5.3 Matching: by employer, not by substring

Today a blocked line matches when it appears anywhere in the employer's name. New: a block is a **company key** (the cleaned name, as `Company.key` and `dream.py` already use), matched for equality, plus the names ticked under *Also block*. On migration each existing line becomes a block on every catalogue employer whose cleaned name contains it, listed to the operator once (console log) so a surprising catch can be fixed.

### 5.4 Where blocks live

`Company` (per candidate) gains `blocked` (bool), `blocked_at`, `block_reason` (`bad_experience` / `not_for_me` / `other`), `block_note`. `filters.blocked_companies` is migrated into these rows and then read from them; the Settings text box becomes the **Blocked employers** list (name, reason, date, *Unblock*), also reachable from *Companies*. *Insights*' "hide company" suggestion creates the same block.

Unblocking brings back every hidden job from that employer that is still open, and says how many: *"Acme unblocked: 3 jobs back in your inbox."*

## 6. Viewing as a candidate (impersonation)

### 6.1 How it works

- Console → *Candidates* → a person → **View as**. The operator lands on that person's inbox, in their mode (standard or power) and their language.
- From then on every candidate page is that person's: the middleware sets `request.candidate` to them (`jobs/middleware.py`), while `request.user` stays the operator. Everything in the candidate space hangs off `request.candidate`, so the pages need no change.
- **Full act-as (D2, settled):** the operator can do what the candidate can: dismiss, shortlist, add notes, change filters and settings, run the conversation again, block an employer.
- A banner on every page, fixed at the top, in a warning colour, on phone and laptop:
  > **Viewing as C-07 · Marie** · standard mode · changes are made on their behalf · [Switch to power] [Stop]
- **Stop** (or logging out, or 60 minutes without a request) ends the session and returns to the console page it started from.
- `/ops/` pages stay open to the operator during a session; the banner stays on candidate pages only.

### 6.2 What act-as does not allow

Things that belong to the person, not to support: changing their **password** or **e-mail**, **deleting** their account, changing their **AI consent**, downloading **their data** export, connecting a **contacts** export. These buttons are shown disabled with *"Only Marie can do this"*.

Viewing as someone must not fake their activity:
- nothing is marked **seen** (AI cards, "new" dots, the ready strip), and their *last seen* does not move;
- no e-mail is triggered by an action taken during the session (for example a tuned search undone);
- product numbers (onboarding time, open rates) leave the session out.

### 6.3 Trail

- `Impersonation`: operator, candidate, started_at, ended_at, how it ended, number of changes.
- Every change made during a session is stored as today, plus `acted_by = operator` (on `StatusChange` and on the settings history). It is shown **in the console only**.
- **No log in the candidate's space at this stage (D6):** the candidate's pages never mention a session, and the job history shows the change without who made it. The privacy note says, once, that the operator can view and act in an account to help.

## 7. E-mail

### 7.1 The service

**Render's free web service blocks outbound SMTP (ports 25, 465, 587) since September 2025**, so mail goes through an **HTTPS API**. The PC runner can call the same API.

| Provider | Free tier | For Saxobeat | |
|---|---|---|---|
| **Brevo** (Paris, ex-Sendinblue) | 300 e-mails a day (≈ 9,000 a month), transactional API included, no card | EU company and data, French, room for 30 candidates × several e-mails a day and a burst of invitations | **Recommended (D7)** |
| **Resend** | 3,000 a month, 100 a day, one domain | The nicest API and dashboard; 100 a day is tight on an import day with 30 candidates plus digests; US company | Fallback |
| SendGrid | Free plan retired in 2025 | — | No |

Free-tier figures come from third-party reviews dated 2026: **check Brevo's own pricing page when signing up**, including whether the free plan adds a Brevo mention to transactional e-mails.

**Volume estimate**, 30 candidates: AI-ready ≤ 30 a day (one per person, §7.3), digests ≤ 30 a day (daily) or ≤ 30 a week, account e-mails a handful. Peak ≈ 70 a day: inside both free tiers, with Brevo leaving 4× headroom.

**Code:** `django-anymail`, which speaks to Brevo, Resend and others behind Django's normal `send_mail`, so changing provider is one setting. `SAXOBEAT_MAIL` = `brevo` | `resend` | `console` (prints, for development and tests) | `off`. The API key lives in the environment only (Render settings, the PC's `.env`).

### 7.2 The domain: `saxobeat.fr` (D3, D8; changed 2026-10-30 by cycle 003, was `stoyan.ovh`)

- Send from a **subdomain** of it, `mail.saxobeat.fr`, so a deliverability problem never touches the root domain's mailbox. From: `Saxobeat <no-reply@mail.saxobeat.fr>` (it cannot receive mail); Reply-To: the operator's address, so a reply reaches a human.
- DNS records (done by the operator): the provider's **DKIM** CNAMEs, the `mail` CNAME that carries the SPF and return-path, a Brevo code, and Brevo's **DMARC** record on the root (`p=none`, reports to Brevo; kept, [decision D2](sdlc/cycles/003-email-live/decisions.md)). Tried with Gmail (inbox) and iCloud (spam); Outlook not yet.
- **The app is on `app.saxobeat.fr`** (D8, moved by cycle 003, [D4](sdlc/cycles/003-email-live/decisions.md)): a CNAME to the Render service, added as a custom domain in Render (free, with its certificate), and in `DJANGO_ALLOWED_HOSTS` / `DJANGO_CSRF_TRUSTED_ORIGINS`. Links in e-mails use it; the `onrender.com` address keeps working. The first address, `jobs.stoyan.ovh`, was removed on purpose before anybody signed up ([D5](sdlc/cycles/003-email-live/decisions.md)).

### 7.3 Which e-mails (D4, settled)

| E-mail | Sent when | To | Content | Can be turned off |
|---|---|---|---|---|
| **Invitation** | The operator creates an invitation with an e-mail on *People* (the field exists: `Invitation.email`) and ticks *Send it* (default on) | The invited address | Who invites, what Saxobeat is in two lines, the join link (14 days). | — (the operator chooses per invite; the copy link stays) |
| **Welcome** | Right after sign-up | The new candidate | Login reminder, what happens next (inbox sorted now, AI within 24 h if they agreed), link to the app. | No |
| **Password reset** | *Forgot password?* on the login page (new, self-service) | The account's address | A one-hour single-use link (Django's reset tokens). The page always answers *"If an account exists, we sent a link"*; limited to 3 requests an hour per address and 10 per IP address. | No |
| **Password changed** | After any password change or reset | The account | *"Your password was changed. Not you? Reply to this e-mail."* | No |
| **AI results ready** | AI results for the candidate were imported (console or runner) | The candidate | One e-mail, everything since the last one: *"3 new picks: Head of CS at Qonto, … · Your CV analysis is ready · Your search was tuned (6 keywords added) [See what changed]"*. Picks link straight to the job. | Yes |
| **Digest of new matches** | Daily (around 8:00) or weekly (Monday 8:00), as the candidate chose | The candidate | Up to 5 new jobs since the last digest: in standard mode the picks and coming-up jobs, in power mode the best scores; each with company, score, one line; *"and 12 more in your inbox"*. Not sent when there is nothing new. | Yes: off / daily / weekly |

**One AI e-mail, not one per file.** Imports queue the news on the candidate; it is sent at most **once per 12 hours** per person, collecting everything that landed (several job screening parts, the onboarding result). The first onboarding result after sign-up is sent at once: it is the first impression.

**Defaults:** AI results ready **on** for people who agreed to AI; digest **weekly** for standard mode, **off** for power mode (D9).

### 7.4 How sending works

- **`OutgoingEmail`** (outbox): candidate (or address, for an invitation), kind, language, subject, body (text and HTML), a **dedupe key** (e.g. `ai_ready:C-07:2026-10-28T08`, `digest:C-07:2026-W44`), state `queued` → `sent` | `failed` | `skipped` (switched off, no address, quota), provider message id, attempts, created / sent at.
- **Account e-mails** are sent at once by the web request that causes them (a password reset cannot wait for the runner); on failure they stay `queued` and the page says *"We couldn't send the e-mail; try again in a minute"*.
- **AI-ready and digest e-mails** are queued by the import and by the matching step, and sent by `manage.py mail send`, run at the end of every PC runner sync and by the console's *Send now*. The same dedupe key is never sent twice, so a file imported twice or a runner run twice sends nothing more.
- A failed send is retried at the next run, three times at most, then shown on the console.
- Every candidate e-mail is in the **candidate's language** (French or English), plain and short, with a text version; links carry no personal data in the URL beyond a signed token.
- **Unsubscribe:** every AI-ready and digest e-mail has a one-click *Stop these e-mails* link (signed token, no login) and the `List-Unsubscribe` / `List-Unsubscribe-Post` headers, which Gmail and Yahoo require of bulk senders.

### 7.5 Settings and console

- Candidate *Settings → E-mails*: the address (= the login), *AI results ready* on/off, *Digest* off / daily / weekly. The AI line is hidden for people without AI consent.
- Console *E-mails* page: today's count against the provider's daily cap, the outbox (filter by kind, state, candidate), failures with the provider's message, *Send a test e-mail to me*, *Send now*, a switch to pause all candidate e-mails (account e-mails always go).

### 7.6 Privacy

- E-mails carry job titles, companies and scores: no CV text, no AI analysis text beyond its first line, no note.
- The provider sees the address and the e-mail's content: the privacy note names it (Brevo, EU) and why.
- Account deletion deletes the person's outbox rows.
- The provider's contact lists are not used: Saxobeat sends transactional e-mails one by one; nothing is synced to a marketing list.

## 8. Data model (sketch)

- `Candidate.mode` (`standard` | `power`, default `standard`); migration sets the operator's candidate to `power`.
- `Company.blocked`, `blocked_at`, `block_reason`, `block_note`; data migration from `Config.filters["blocked_companies"]`, after which the key is no longer read.
- `Impersonation` (operator, candidate, started_at, ended_at, end_reason, changes); `StatusChange.acted_by` (null = the candidate); the same field on the settings history if one exists, otherwise a line in `Impersonation`.
- `Candidate.email_prefs` (JSON: `ai_ready` bool, `digest` `off|daily|weekly`, `last_digest_at`, `last_ai_mail_at`), `OutgoingEmail` (§7.4).
- Code: `jobs/services/picks.py` (the standard inbox: picks, coming up, no-AI fallback, reusing `jobs/ai/selection.py`), `jobs/services/blocks.py` (block, unblock, matching, effects), `jobs/impersonation.py` (start, stop, middleware hook, guards), `jobs/mail/` (`send.py`, `kinds.py` one entry per e-mail, templates under `jobs/templates/jobs/mail/` in both languages), `manage.py mail send|test`.

## 9. Phases

| # | Phase | Size | Result |
|---|---|---|---|
| **U1** | **View as** | S | Console *View as*, the middleware switch, the banner, the guards of §6.2, no "seen" while viewing, `Impersonation` and `acted_by` (console only). First, because it is the tool to build and check U2 with real accounts. |
| **U2** | **Standard mode** | M | `Candidate.mode`, the console switch, the standard inbox (picks, coming up, no-AI fallback, empty states, count, badge), the search icon, everything §4.3 removes; then §4.5 once D5 is confirmed. A test that a standard page contains none of the power-only elements. |
| **U3** | **Blocked employers** | S | Block from job, company and dismiss sheet; *Also block*; effects of §5.2 (including AI task cancellation); key matching and migration; *Blocked employers* list; unblock. |
| **U4** | **E-mail foundation and account e-mails** | M | Provider account and domain records (operator), `django-anymail`, `OutgoingEmail`, `manage.py mail send|test`, invitation by e-mail, welcome, self-service password reset with its limits, password changed, console *E-mails* page. |
| **U5** | **AI-ready e-mail and digest** | M | Queued from imports and matching, 12-hour grouping, the digest (daily / weekly, mode-aware), unsubscribe links and headers, Settings → E-mails, the runner step. |

U3 needs nothing from the others and can be built at any time. U4 needs the operator's DNS step before it can be tried for real (it can be built and tested with `SAXOBEAT_MAIL=console`).

**What was built (28 October 2026), where it differs from the text above:**

- *View as* (U1): no log in the candidate's space (D6); a language picked while viewing is kept for the session, never saved on their account.
- *Standard mode* (U2): Settings leaves out the whole scoring form rather than some of its fields, because that form saves every field at once and hidden fields would be blanked; places are set in *What I'm looking for* and, since cycle 030, also in a small card of their own in Settings (cities, remote anywhere in France, extra remote-role cities, remote only; its own Save at `/settings/places/`, which writes only those four filters, keeps the guided answer in step and sorts the jobs again in the background). The search icon opens a search row (a link), not a floating field.
- *Blocked employers* (U3): no 5-second *Undo* after blocking; the message says how many jobs left, and *Unblock* is in Settings and on the company page. Very short names (like "Axa") only match themselves, as everywhere employers are compared.
- *E-mail* (U4, U5): a reset link made by the operator lasts three days (the existing setting), while one that is **e-mailed** lasts one hour, as §7.3 says (changed by cycle 003: a second token generator for e-mailed links). AI-ready e-mails and digests are decided when `manage.py mail send` runs (end of every PC runner pass and of `saxobeat-ai.cmd`), after a console import, and from the console's *Send now*; nothing is queued at import time. The first AI e-mail tells what landed in the last two days only. The HTML e-mail is the text in a card, with the links written out.

## 10. Decisions

| # | Question | Decision / recommendation |
|---|---|---|
| D1 | What does the standard inbox show before or without an AI verdict? | **Settled 28 Oct:** *apply* picks first, then the jobs selected for an AI review as *coming up*; without AI consent, the same selection by score. Never empty on day one. |
| D2 | Viewing as a candidate: read-only or acting? | **Settled 28 Oct:** full act-as, logged, with the exceptions of §6.2. |
| D3 | Sending domain? | **Settled 28 Oct:** the operator has a domain; send from a subdomain of it. |
| D4 | Which e-mails in the first version? | **Settled 28 Oct:** account e-mails, AI results ready, digest of new matches. Operator alerts and reminders are in the register. |
| D5 | Standard mode beyond the inbox (§4.5): hide Contacts, Insights, the keyword breakdown and the scoring settings? | **Settled 28 Oct:** yes, as in the table. |
| D6 | Tell the candidate when the operator viewed their account? | **Settled 28 Oct:** no log in the candidate's space at this stage; the console keeps the trail; one sentence in the privacy note. |
| D7 | Provider? | **Settled 28 Oct:** **Brevo** free (EU, 300 a day); Resend as the fallback; the code is provider-neutral (anymail). |
| D8 | Serve the app on its own domain? | **Settled 28 Oct:** yes, on `jobs.stoyan.ovh`; **changed 30 Oct (cycle 003 D4): `app.saxobeat.fr`** (§7.2). |
| D9 | Digest default? | **Settled 28 Oct:** weekly for standard, off for power; daily on request. |
| D10 | Existing friends: switched to standard at once? | **Settled 28 Oct:** yes, with no note. |
| D11 | Jobs in the pipeline when their employer is blocked? | **Settled 28 Oct:** untouched (§5.2). |
| D12 | *Also block* similar employer names, ticked by default? | **Settled 28 Oct:** listed, **not** ticked (§5.1). |

## 11. Acceptance

- A new candidate lands in standard mode; the operator's candidate is in power mode; only the operator can switch, and switching back and forth changes no data.
- A standard inbox shows only *apply* picks and *coming up* jobs (or the selection by score without AI consent), never the filter sheet, the CSV export, the bulk dismiss, the bookmarklet or the keyboard hint; a new candidate never sees an empty inbox without a "ready by" time.
- Search in standard mode finds a job that is neither a pick nor coming up, and labels it.
- Blocking an employer from a job hides every open inbox job from it at once and every future one, leaves pipeline jobs untouched, cancels its queued AI reviews, and unblocking brings the open ones back with a count. A block on "Axa" does not hide a job at an employer whose name merely contains those letters.
- During *View as*, every candidate page shows the banner; the operator can dismiss a job and the console records it as his; password, e-mail, deletion, AI consent and data export are refused; nothing is marked seen; the session appears in the console and nowhere in the candidate's pages; it ends after 60 minutes idle.
- With the provider set up, an invitation, a welcome, a reset and a "password changed" e-mail reach a Gmail and an Outlook inbox (not spam), in French and English.
- Importing results for 5 candidates sends exactly one AI e-mail to each consenting candidate who has it on; importing the same file again, or running the runner twice, sends nothing more.
- A digest is not sent when there is nothing new; *Stop these e-mails* works without logging in and from Gmail's own unsubscribe button.
- No e-mail contains CV text or a private note.
- All new candidate strings exist in French and English.

## 12. Risks

| Risk | Mitigation |
|---|---|
| The standard inbox feels empty (few *apply* verdicts, AI late). | *Coming up* jobs with their time; the no-AI fallback; search. Watch picks per active candidate per week. |
| A good job is never seen because the AI said *don't apply*. | Search reaches it with its label; the operator can switch the person to power; the AI PRD's rule stands: the AI labels, it never removes a job. |
| Act-as is used carelessly, or the candidate feels watched. | The banner, the exceptions, the console log, the privacy note, nothing marked seen. |
| E-mails land in spam. | A verified subdomain with DKIM, SPF, DMARC; plain short e-mails; one AI e-mail per 12 h at most; unsubscribe headers; tested on Gmail and Outlook before the friends. |
| The free tier changes or a cap is hit. | Volume ≈ a quarter of Brevo's cap; the console shows today's count; anymail makes switching provider one setting; account e-mails go first. |
| An e-mail is sent twice or to the wrong person. | Dedupe keys; one outbox row per person; tests import a file twice and expect one e-mail. |
| Substring blocks migrated wrongly. | The migration lists what each old line now blocks, for the operator to check once. |

## 13. Success measures

- Standard candidates: at least one shortlist or apply per active week for 60 % of them; median time on the inbox per visit down, actions per visit up.
- AI-ready e-mails: at least half opened; at least a third followed by a visit within a day.
- Password resets handled with no operator action: all of them.
- Zero e-mails reported as spam by a friend in the first month.
- *View as* used to answer every "my inbox looks wrong" report without screenshots.

## 14. References in the repository

- Inbox and filters: `jobs/templates/jobs/inbox.html`, `_filters.html`, `_cards.html`, `inbox` in `jobs/views.py`; visibility: `jobs/services/visibility.py`; menus: `jobs/templates/jobs/base.html`, `more.html`.
- The job screening selection reused for *coming up*: `jobs/ai/selection.py`; the pending component: `jobs/templates/jobs/_ai_card.html`.
- Blocks today: `filters.blocked_companies` in `jobs/models.py` (`default_filters`), `hidden_reason` in `jobs/services/filters.py`, `jobs/reasons.py`, the *Insights* suggestion in `jobs/services/insights.py`; company keys and the dream bonus: `Company` in `jobs/models.py`, `jobs/services/dream.py`, `employers.clean_name`.
- Who is looking: `jobs/middleware.py` (`request.candidate`), `jobs/access.py` (the operator gate).
- Accounts: `jobs/accounts.py` (invitations with an e-mail field, sign-up, failed-login limits, reset links), `jobs/views_accounts.py` (*People*).
- Runner: `scripts/pc_runner.ps1`, `manage.py ai sync`; hosting: [DEPLOY.md](DEPLOY.md), `render.yaml`.

## 15. Register: later

| # | Issue | First idea |
|---|---|---|
| R1 | E-mails to the operator | New sign-up, source proposal, runner silent for 12 h, files in *problems*, AI tasks late: one morning summary to the operator. |
| R2 | Reminder e-mails | Follow-ups due, an interview tomorrow (with the cheat sheet link). |
| R3 | Bounces and complaints | The provider's webhook marks an address as bouncing and stops sending to it. |
| R4 | Candidates choosing their mode | A *Show more tools* switch in Settings, if friends ask for it. |
| R6 | E-mail invitations from a candidate | A candidate e-mails a friend their invitation code from the app (cycle 033 left it out: it lets anyone send mail from our domain to any address); needs a per-person limit and the 300-a-day cap in mind. |
| R7 | Confirming the address at sign-up | A code sign-up does not prove the address is the person's (cycle 033, Q8, parked); a typo means a login that cannot be reset. A confirmation e-mail would fix it. |
| R5 | Blocks as a signal | Many people blocking the same employer could inform the operator, if candidates agree; not before. |

## Sources (checked 28 October 2026)

- Render free web services and SMTP: [render.com changelog](https://render.com/changelog/free-web-services-will-no-longer-allow-outbound-traffic-to-smtp-ports), [Render community thread](https://community.render.com/t/outbound-smtp-connection-timeout-on-free-tier/39168).
- Brevo free plan: [Brevo free SMTP page](https://www.sendinblue.com/free-smtp-server/), [costbench.com](https://costbench.com/software/marketing-automation/brevo/free-plan), [dev.to pricing review](https://dev.to/techsifted/brevo-pricing-2026-every-plan-explained-with-the-hidden-costs-4oe3).
- Resend free tier: [costbench.com](https://costbench.com/software/email-api/resend/free-plan/), [automationatlas.io](https://automationatlas.io/answers/resend-free-tier-explained-2026/).
- SendGrid's free plan retired: [dev.to](https://dev.to/thiago_alvarez_a7561753aa/resend-vs-sendgrid-2026-sendgrid-killed-its-free-tier-now-what-2gh4).
