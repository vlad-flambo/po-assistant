# AI-native SDLC, the way we work here

One **cycle** = one small outcome, taken through six stages. Every stage leaves a file in `cycles/NNN-name/`, so the next session (or agent) starts from the files, not from the chat.

```
intent → spec → plan → build → verify → learn
  ▲                                       │
  └───────────── next cycle ◄─────────────┘
```

| # | Stage | File | Question it answers | Human gate |
|---|-------|------|---------------------|------------|
| 1 | **Intent** | `intent.md` | Why, for whom, what does "done" look like, what are we NOT doing? | You confirm the goal and success measure |
| 2 | **Spec** | `spec.md` | What exactly will be true when finished? (acceptance criteria, constraints, out of scope) | You approve the spec |
| 3 | **Plan** | `plan.md` | In what thin slices, in what order, touching which files, with which tests? | You approve the slices |
| 4 | **Build** | commits + `build-log.md` | One slice at a time, tests first where it makes sense | Per-slice review of the diff |
| 5 | **Verify** | `verify.md` | Evidence for each acceptance criterion (test output, measurement, drill) | You accept or send back |
| 6 | **Learn** | `learn.md` | What changed in our understanding, docs, memory, rules? | You pick what becomes permanent |

## Rules

1. **Intent is interrogated, not dictated.** The agent grills (one question at a time, with a recommended answer) until the open questions in `intent.md` are closed or explicitly parked.
2. **No code before the spec is approved.** Exploration and throwaway spikes are fine, but they are labelled as spikes and never merged as the answer.
3. **Slices are small enough to verify alone.** Each slice has its own check.
4. **Evidence over assertion.** `verify.md` points at output, numbers or a drill result, not "it works".
5. **Decisions are written down** in the cycle's `decisions.md` with the reason, so they are not re-argued.
6. **Learn feeds back.** Durable findings go to `docs/DEPLOY.md` / the product PRDs, the project memory, or the repo's rules, and the cycle ends with a list of what moved where.

## Where things live

```
docs/sdlc/
├── README.md              this file
├── templates/             copy one per stage when you start a cycle
│   ├── intent.md  spec.md  plan.md  verify.md  learn.md  decisions.md  next.md
└── cycles/
    ├── 001-local-db-replica/     cycle 1 (in the Intent stage)
    └── NNN-short-name/           one folder per cycle
```

Starting a cycle: create `cycles/NNN-short-name/`, copy `templates/intent.md` into it, and begin there. Other stage files are copied when the cycle reaches that stage, so the folder always shows how far the cycle got.

## Relationship to the existing PRDs

The product PRDs in `docs/` (`PRD.md`, `PRD_multi_user.md`, `PRD_mobile.md`, `PRD_ai_backoffice.md`, `PRD_users_and_emails.md`, `PRD_competitive_features.md`) are the **product-level source of truth** and stay as they are. A cycle's `spec.md` is the per-outcome equivalent: small, testable, finished in days. When a cycle changes the product's behaviour, `learn.md` says which PRD or doc gets the update. Large themes can still get a PRD; a cycle then implements one slice of it and links to it from `intent.md`.

## The board and "what next?"

- **The method as a skill:** `.claude/skills/ai-sdlc/SKILL.md` (committed with the repo, and installed for every project at `~/.claude/skills/ai-sdlc`). It is project-independent: it says how to run each stage, the grill-me protocol, the evidence and secrets rules, and how to keep the board current. What is specific to Saxobeat (Python command, secrets, hosts, board link) is in [PROJECT.md](PROJECT.md). Ask for "what next?" at any time.
- **State comes from the files.** `.claude/skills/ai-sdlc/scripts/sdlc_status.py` reads every `cycles/*/` folder: a stage's file and the checkboxes in its Gate (or, for Verify, its Verdict; for Learn, the "What moves where" table) say whether the stage is done. Nothing is typed in twice.
- **"What next?" comes from `next.md`** in each cycle: one line per action, `- [ ] [owner|claude|both] <date, optional> text`. It is the one judgment call, so whoever moves a cycle updates it.
- **The cycle board** is a private artifact: https://claude.ai/artifact/NVff2m66eVpfzbUdr1AmpJ. It shows the recommended next step, every open action, and each cycle's six stages with its criteria counts. [BOARD.md](BOARD.md) shows the same facts as a table that any viewer can read (generated, never edited by hand). To refresh both after a change, follow `reference/board.md` in the skill.

## Importance and dismissed cycles

- **Importance (1 to 5)** ranks the cycles. It sits in the header table of each `intent.md` (`| **Importance** | 4/5 (claude, 2026-10-30): reason |`), is first assessed by Claude from reach, pain, what the cycle unlocks and the risk of waiting, and is overruled by the owner (`(owner, date)`). 5 critical (data, hosting, nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. The board shows it as five dots with a "Sort by importance" button; "what next?" uses it only to break ties.
- **Dismissed** is a decision, not a deletion: the intent gets `| **Status** | Dismissed YYYY-MM-DD by the owner: reason |`, its `next.md` is ticked, the folder stays as the record, and the board shows it as Dismissed with the date and drops its actions.

## Status of cycles

| Cycle | Imp. | Topic | Stage |
|-------|------|-------|-------|
| 001 | 4 | Cut the runner's reads from Neon (local copy of the database) | Verify drafted 2026-10-30: 9 of 11 criteria pass (two read reductions live since 10:55, D5 confirmed); learn drafted; the runner may restart by hand now (D6, `evidence/restart_runbook.md`); criteria 4 and 9 wait for the web app's daily Neon readings from 2026-10-31 |
| 002 | 5 | Move to a fresh Neon project, keep the old one as a fallback | **Closed 2026-10-30**: 10 of 11 criteria met (criterion 2 accepted as a risk); prod1 used about 135 MB in its first day, the old project unchanged at 95.1 %; left open: deleting or refreshing `saxobeat-fallback1` after a clean month |
| 003 | 4 | Make e-mail live: Brevo, the sending domain, the app's own address | Intent started 2026-10-30: facts checked (`jobs.stoyan.ovh` already serves with a valid certificate; `mail.stoyan.ovh` has no DNS records yet); Intent and Spec (18 criteria) approved 2026-10-30, bounces parked; Plan (12 slices) approved 2026-10-30; Build: slices 1-3 done (the 1-hour e-mailed reset link, code and tests, 1,303 tests pass, committed `6f504a7`, pushed and Live on Render 2026-10-30, owner's word); slices 4 and 5 done (candidate e-mails paused, owner's word); **sending domain changed 2026-10-30 by the owner to `mail.saxobeat.fr`** (D1), Brevo's DNS records found in place; slices 6 and 7 done (Brevo Authenticated, 300 a day, DMARC kept; the five settings on Render and `.env`, the E-mails page reads provider brevo; owner's word and page line); slice 8: the Gmail test landed in the inbox (owner's word), the Outlook test is deferred to a friend (accepted risk); **app address moving to `app.saxobeat.fr` (D4, 2026-10-30)**, slice 7b with the owner (DNS, Render, settings), then the rehearsal and the first friend |
| 004 | 4 | Check the hosted app: speed, migrations, backups, AI with a real agent | **Closed 2026-10-29**: 10 of 10 criteria pass (speed judged, not timed); DEPLOY.md now says what is verified on the host; left open: the owner's manual Neon snapshot of prod1 (it restores only 6 h, no dump yet) |
| 005 | 4 | Real phones and a headless browser check (Playwright) | Intent: drafted from the PRD audit, questions open |
| 006 | 2 | Bring the PRDs and DEPLOY.md up to date (stale statements) | Intent: drafted from the PRD audit, questions open |
| 007 | 3 | Measure what the PRDs promised (success measures) | Intent: drafted from the PRD audit, questions open |
| 008 | 3 | Score calibration over time, screening brief drift | Intent: drafted from the PRD audit, questions open |
| 009 | 3 | Reminders and alerts: operator summary, follow-ups, interviews, push | Intent: drafted from the PRD audit, questions open |
| 010 | 2 | Finish the phone interactions (long-press, pipeline swipe, one-tap to-dos, contacts search) | Intent: drafted from the PRD audit, questions open |
| 011 | 2 | Settings and small gaps (keyword chips, AI weight, focus cap, undo, remote filter, ...) | Intent: drafted from the PRD audit, questions open |
| 012 | 2 | Insights: the rest of F11 (by score band, source, channel, size, focus) | Intent: drafted from the PRD audit, questions open |
| 013 | 3 | More sources: employers' own career sites (Accenture, Capgemini, Saegus and the lists in `data/`), VC boards, aggregators, Personio, legal review per source | **Built and verified, waiting for the owner's verdict (2026-11-10)**: 22 criteria in [verify.md](cycles/013-more-sources/verify.md), 17 pass, 1 accepted, 4 partial. Hosted: 21 sources of the cycle on (own career sites, consulting, Doctolib and Papernest repaired, a batch of French fintechs with Qonto moved to Ashby); first-week reading: 2,016 new jobs in Paris / Ile-de-France, 52.2 % from the cycle's sources, 48.0 % from consulting sources (includes the one-off first-pass backlog); next reading 2026-11-17; learn.md follows the verdict |
| 014 | 5 | Runner and data correctness (expire guard, the failing backup test) | **Closed 2026-10-29**: six overwrite windows fixed, 0 known test failures on SQLite and Postgres; live since the deploy of `d1718a0` (2026-10-29 15:53) |
| 015 | 4 | A feedback chat, always one tap away (scripted, no AI): collect ideas and their usefulness for new intents | Verify accepted by the owner 2026-10-30: 17 of 18 criteria pass (11 and 13 on the owner's word), 1 open (17, real use, read after two weeks); live on the host since 2026-10-30; slice 11 (the two-week count) starts when the invitations go out, then learn |
| 016 | 2 | Blocking an employer: an icon instead of text, the blocked list on the Companies page instead of Settings | Intent drafted 2026-10-29 for later (from cycle 004's check of the blocks); 4 questions open |
| 017 | 1 | Remove the keyboard-shortcuts explanation line from the inbox (feedback #1 from C-01) | **Dismissed 2026-10-30** at the Intent stage by the owner: it does not seem to affect most users; no code changed; reopen if more feedback asks for it |
| 018 | 2 | Import job-alert e-mails (LinkedIn, WTTJ, APEC, Indeed) without standing mailbox access, moved out of 013 | Intent drafted 2026-10-30 for later (owner: low priority); 1 question open |
| 019 | 3 | Presume an application rejected after a month without an answer, with a tag and an info box saying the app did it | **Closed 2026-11-04**: Applied jobs with no answer for more than the delay (one console value, default 30, 0 = off; interview and focus jobs exempt) are Rejected by the runner's `auto_reject` step with an "Auto-rejected" tag, an info box and a one-tap put-back; Insights show them as "No answer"; 82 new tests (SQLite 1,436 pass); live on the host, first sweep moved 18 (the dump predicts 17 then 18; no before/after counts, so consistent rather than measured); owner looked and accepted; left open: the cycle-015 test that fails on Postgres (equal timestamps), the doc commits are not pushed |
| 020 | 2 | Read career sites built on Revolut People (found through a Worklife link), and could it give Revolut's own jobs? | **Closed 2026-11-04**: a `revolutpeople` source reads Worklife's jobs (16 tests, suite 1,434 pass, committed `f0d03cf`; live on the host since the owner's Step 3 seed, Worklife enabled, first pass stored 4 jobs, owner's word, not read back by me); revolutpeople.com's robots.txt forbids the API, so the owner overrode it per source (`ignore_robots`, decisions.md D1); Revolut's own jobs stay on the bookmarklet; left open: the robots-first rule for the SDLC skill (owner's yes) and the PRD.md Revolut line (cycle 006) |

Cycles 003 to 014 come from the **PRD audit of 2026-10-29** ([the full list](cycles/006-stale-docs/evidence/prd_audit_2026-10-29.md)), in the owner's order: get things live and checked first (003-006), then the rest. Ideas the PRDs only parked are in [backlog.md](backlog.md): each becomes a cycle when it is worth doing.
| 021 | 4 | Bilingual keyword scoring (feedback #4: a French job that led to an interview scored 33) | **Closed 2026-11-05**: verify accepted by the owner (16 of 18 criteria pass, 2 partial). Same-role French/English gap 10.6 to 3.2 points on the replay; job 33238 49.8 on the replay and 43.7 on the host data (stored 33 stays: it is in the pipeline); candidate 1's inbox rescored on the host (2,980 jobs), candidates 3 and 4 not; Neon 0.49 GB this month. Left open: calibrate the other-language scale (0.032) on a French-profile candidate, keyword edits do not reliably rescore the inbox (new cycle candidate), mentions of a title count like roles |
| 022 | 2 | A job you applied to is reposted by the employer: how to treat the second posting (status, merge, or a link with a banner) | Intent: facts gathered 2026-11-04 (repost detection exists but only as a badge with no link to the application; local copy: 0 of 556 repost views affected); Q1 answered (link with a banner, no new status, no merge) and Q2 (host shows the repost badge: detection works); Q3 answered (banner on the repost's page, tag on its inbox row, pointer on the older job); Q4 and Q5 accepted as recommended (no auto-hide, tag and banner plus a filter; shown normally after a rejection); all questions answered, goal and success measure confirmed 2026-11-04; Spec approved 2026-11-04 (13 criteria: banner, tag and pointer from the existing repost chain, a filter, no migration, no new status); Plan approved; Build: slices 1 to 8 done 2026-11-04 (54 new tests, suite 1,606 pass, no migration; phone-card chip added, decisions.md D1); committed `0455313` and pushed (live 2026-11-04); Verify drafted: banner and pointer read on the host as expected, **but the filter hung the host** (a per-row EXISTS: over 20 s on 24,000 views; fix D2 measured 0.01 to 0.04 s, suite 1,610 pass), 12 of 14 criteria pass; the fix is not committed or deployed, owner's word on both next |
| 023 | 2 | The AI "how it works" information should not be on by default on the job page (feedback #5 from C-01) | Spec, plan and round 1 built and deployed 2026-11-04; the owner's phone check failed (the box came back when left alone: only a tap marked it seen). **Round 2 built 2026-11-04** (opening by itself counts as seen; Node test 13/16 red then 16/16, suite 1,608 pass before and after, drill on the mobile preset with no tap); verify 7 pass, 1 partial, 1 pending; waiting for the commit, the deploy and the owner's phone check (touch nothing on two job pages) |
| 024 | 3 | Simplify the ops Console: too many sections, unclear what does what | **Verify accepted by the owner 2026-11-04, Learn done**: 14 bar entries became 7 areas (Today, Candidates, Sources, Runs, Feedback, AI, More) with tab rows, a purpose line on every page, an AI status strip and a rebuilt Today; no address changed, nothing deleted; 9 criteria pass, 1 partial (live site and phone widths); 1,499 tests pass; committed `4d29c37`, not pushed; left open: push, deploy and click through the live `/ops/` (owner, slice 8) |
| 025 | 4 | Environments: prod, pre-prod, testbed (no deploy to prod on every commit; separate databases; refresh from prod) | Spec drafted 2026-11-10 (20 criteria, D1 to D5) after the intent was confirmed: three Render services from one Blueprint (prod from a `release` branch, no auto-deploy), separate Neon projects, full copy of prod with e-mails and passwords neutralised, CI; waiting for the owner's approval of the spec. Unblocks 026 to 028 |
| 026 | 3 | Cloud runner for sources | Intent: drafted 2026-11-05; needs 025; first question: is a datacenter address acceptable to the job sites (spike on pre-prod) |
| 027 | 3 | Cloud AI agent step | Intent: drafted 2026-11-05; parked until 025 and 026 reach verify |
| 028 | 3 | Cloud dev workspace | Intent: drafted 2026-11-05; needs 025 (testbed content and refresh) |
| 029 | 3 | keyword edits rescore the inbox | **Plan approved 2026-11-06, build not started** (intent, spec of 18 criteria and plan of 12 slices approved; slice 1, the stamp hash, is next; no code written). A Settings save starts no rescore (the brief was wrong); owner chose to keep the button, to show an "older than your settings" line, a hash stamp on each score, a background pass finished by the next start. Hand-over for another computer written 2026-11-10 ("Resume here" at the end of plan.md): migration number is now 0045, the dump and `.env` do not travel |
| 030 | 5 | international destinations chosen individually | Intent confirmed 2026-11-06 (narrowed by the owner: the onboarding choice is done; standard mode edits cities and the three remote options in Settings, in a card of its own); spec and plan approved 2026-11-06; built (six slices, code only, no data), Verify written: 9 of 9 criteria pass, suite 1,623 passed; accepted by the owner 2026-11-06; learn written; committed in 106a224 (with 031) and in `origin/main` since another session's push (head b1afe41, 2026-11-10; host deploy not checked by me); **closed** apart from a look on the host |
| 031 | 3 | stop analysing postings older than 30 days | Intent: Q1 to Q3 answered 2026-11-06 (new default 30; owner moved existing candidates by hand, so no data change; undated postings age from their import date); Q4 answered (the job's own `first_seen_at`, a best-guess proxy for the listing date); intent confirmed 2026-11-06; spec and plan approved 2026-11-06; built (seven slices, code only), Verify written: 11 of 11 criteria pass, suite 1,632 passed; first-run effect counted on the 29 Oct dump; accepted by the owner 2026-11-06; learn written; committed in 106a224 (with 030) and in `origin/main` since another session's push (head b1afe41, 2026-11-10; host deploy not checked by me); **closed** apart from reading the host's real effect |
| 032 | 4 | operator cannot delete a user, it times out | **Closed 2026-11-06**: 36,271 views delete in 0.6 s and 33 statements instead of 41 s and 72,945 (local Postgres 2.3-5.2 s); verify accepted by the owner after deleting weiersto+0611@gmail.com on the host ("quick"); 8 of 9 pass, 8 partial (one unexplained 9-minute stall on a local Postgres, bounded by a 30 s timeout); learn moved to DEPLOY.md and house-stack; commits 56e7d48 and the learn commit |
| 033 | 4 | invitation codes for sign-up (open the app to more people, track where candidates come from) | Intent, Spec (18 criteria, D1 to D4) and Plan (10 slices) approved 2026-11-06; **built locally 2026-11-06 (slices 1 to 9) and Verify written: 16 of 18 criteria pass, 13 partial (share sheet not seen), 18 pending (the owner's deploy)**; suite 1,706 pass on SQLite and on Postgres; one account measured at about 8 MB (so 20 sign-ups an hour = 160 MB: the owner decides D1's number); nothing committed or deployed; waiting for the owner: read verify, agree the commit, deploy, make "Skaleet" and sign up through it |
