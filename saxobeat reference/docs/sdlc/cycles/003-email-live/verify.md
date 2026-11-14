# Verify: make e-mail live (Brevo, mail.saxobeat.fr, app.saxobeat.fr)

| | |
|---|---|
| **Cycle** | 003 |
| **Stage** | Verify: accepted with risks by the owner 2026-11-03; next: Learn ([learn.md](learn.md)) |
| **Spec** | [spec.md](spec.md) |

Result words: **pass** (evidence seen or the owner's word), **partial** (some of it proven), **not met** (not done yet), each with its source. "Owner's word" means said in chat, not seen by Claude.

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Brevo shows `mail.saxobeat.fr` authenticated, DNS records resolve, DMARC `p=none` covers it | pass | Owner 2026-10-30: "Brevo shows mail.saxobeat.fr as Authenticated"; Claude's read-only lookup the same day ([evidence/dns_check_2026-10-30_saxobeat_fr.md](evidence/dns_check_2026-10-30_saxobeat_fr.md)); DMARC kept as Brevo's root record (D2) |
| 2 | Brevo's free-plan limits written down | partial | 300 a day (owner, dashboard), API "looks like" included, custom domain evidenced by the authenticated domain; the monthly limit and any Brevo footer were **not given** ([evidence/brevo_limits.md](evidence/brevo_limits.md)). Daily cap equals the limit (300) |
| 3 | Render has the five settings; the E-mails page shows them | pass | E-mails page, owner 2026-11-02: "provider brevo · from Saxobeat <no-reply@mail.saxobeat.fr> · links to https://app.saxobeat.fr". The key is shown nowhere |
| 4 | The PC's `.env` has the same five | pass | Checked by names and shape only, 2026-10-30 (plan slice 7, "As run"). Note: the PC's `.env` public address was to change with D4; checked on the owner's word |
| 5 | The API key is nowhere in the repo, chat or a command line | pass | No key-shaped string in the repo or its history, `.env` is git-ignored (2026-10-30). Not rechecked since |
| 6 | Candidate e-mails paused before mail is switched on; the count read before unpausing | partial | Pause on: owner "Paused" 2026-10-30 and the page line "Candidate e-mails (AI-ready, digest) are paused". The **count has not been read** (slice 11) |
| 7 | The off switch works; the rollback is in DEPLOY.md §7 | pass | The test (`SAXOBEAT_MAIL=off` gives *skipped*) passes (mail tests, 2026-11-03). The rollback is in DEPLOY.md §7 step 6, written 2026-11-03 |
| 8 | Test e-mail to Gmail: inbox, `dkim=pass`, `spf=pass`, `dmarc=pass` | partial | Inbox, no issue: owner 2026-10-30. The header lines and `header.d=` were **never seen** |
| 9 | The same test to Outlook | **not met** | Deferred 2026-10-30, no Outlook account (accepted risk). New data: an **iCloud** test on 2026-11-03 landed in **spam** ([evidence/deliverability_icloud_2026-11-03.md](evidence/deliverability_icloud_2026-11-03.md)), so the new domain does start in spam at some providers |
| 10 | Rehearsal: a real invitation to a second own address, link on `app.saxobeat.fr`, account created, welcome e-mail | **not met** | Not done |
| 11 | One real invitation to one friend | **not met** | Not done; depends on 10 |
| 12 | No `localhost`, `onrender.com` or `127.0.0.1` in any received e-mail link | partial | The E-mails page says the links go to `https://app.saxobeat.fr`; the links in a received invitation, welcome or reset were **not read** |
| 13 | An e-mailed reset link works inside 1 hour, refused after | pass | `test_an_emailed_reset_link_works_for_an_hour_and_not_after`, suite run 2026-10-30 ([evidence/local_run_2026-10-30.md](evidence/local_run_2026-10-30.md)) |
| 14 | A hand-made reset link works at 2 days, refused at 3 days and 1 minute | pass | `test_a_hand_made_reset_link_keeps_working_for_three_days`, same run |
| 15 | Both kinds work once only; a tampered link is refused | pass | The two existing tests pass unchanged, same run |
| 16 | The reset e-mail says "1 hour" in English and French | pass | `test_the_reset_email_says_one_hour_in_both_languages`, same run. The French wording is Claude's, the owner may change it |
| 17 | The whole suite passes on SQLite | partial | 1,303 passed on 2026-10-30. Rerun 2026-11-03 on today's tree (with the other session's uncommitted work): **1,338 passed, 1 failed**: `tests/test_auto_reject.py::test_putting_it_back_to_applied_restarts_the_month`, which **passes alone** (order or date dependent, not an e-mail test). The mail, accounts and ops tests pass (47) |
| 18 | The change is live on the host; a reset e-mail made on the host carries "1 hour" | partial | Pushed and deployed 2026-10-30 (owner: "Live"). **No reset e-mail from the host has been read yet**, so the wording on the host is not seen |
| 19 | `app.saxobeat.fr`: valid certificate, redirects to sign-in, **a form works there**, E-mails page reads the new address, `saxobeat.onrender.com` still answers | partial | Certificate, redirect (302), the login page (200), the host check and the onrender address: Claude's lookups ([evidence/app_move_check_2026-10-30.md](evidence/app_move_check_2026-10-30.md)); the E-mails page line: owner. **A form submitted on `app.saxobeat.fr` is not confirmed** (the CSRF origin setting shows only as a 403 on submit); it is probably true if the owner sent the iCloud test from the console on that address, but that was not said |

**Score: 9 pass, 7 partial (2, 6, 8, 12, 17, 18, 19), 3 not met (9, 10, 11).**

## Findings
- **F1. The new domain starts in spam at iCloud (2026-11-03).** Delivered, not refused. Reputation is the likely cause; authentication is not shown to be at fault, because the header lines were not seen. Mitigation is small steady volume and recipients marking "Not junk"; nothing to change in the code or DNS yet.
- **F2. One e-mail failed after retries (7 days to 2026-11-03).** It was *waiting* on 2026-11-02 and *failed* on 2026-11-03. Kind, address and error text are not known. If the error is Brevo's 401 for an unrecognised IP, that is D3 happening, and every account e-mail would be at risk. This must be read before the first friend.
- **F3. Gmail's header lines were never captured**, so "authenticated" rests on Brevo's dashboard and the inbox result, not on a copied `dkim=pass`.
- **F4. The deployed default sender is still `hello@mail.stoyan.ovh`**; e-mail works only because `SAXOBEAT_MAIL_FROM` is set on Render. A redeploy that loses that setting would send from a domain with no DNS. **Fixed in the learn step** (default changed to `no-reply@mail.saxobeat.fr`; live after the next push).

## Not verified
- Outlook, Hotmail and Live delivery (criterion 9); Gmail's `spf`, `dkim`, `dmarc` lines and `header.d=` (8).
- The rehearsal and the first friend (10, 11), and the links in a received e-mail (12).
- A reset e-mail made on the host (18); a form submitted on `app.saxobeat.fr` (19).
- D3's risk: Render's outbound address changing (the PC is not on Brevo's allowed list either).
- The unknown failed e-mail (F2); the one failing test in a full run (17).

## Verdict (owner)
- [x] Accepted with the open items above listed as accepted risks (then Learn) (owner, 2026-11-03: "Accept with risks")
- [ ] Sent back to Build: do the rehearsal (10), read the failed e-mail (F2), then the first friend (11)
