# Cycle board

Generated 2026-11-10 11:10 by the ai-sdlc skill from `cycles/*/`. Do not edit by hand: change the cycle's files and run the script again.

Stages: `x` done, `o` in progress, `-` up next, `.` later, `~` dismissed.

## What next?

**Your move**

- 002 Move to a fresh Neon project, keep the old one as a fallback: Give the verdict in verify.md (accepted, or sent back) (due 2026-10-30)
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): Read Finastra's and SWIFT's terms of use in a browser (my fetch tool got HTTP 403) before enabling those two sources; Fenergo's too if you like (evidence/priority_a_verdicts_2026-10-30.md) (due 2026-10-30)
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): No up-to-date local copy of prod1 exists (checked: the local `saxobeat` database was last written 2026-10-22, the clones 2026-10-09, the newest dump is 2026-10-29; the runner writes straight to the hosted database). So step 2 (the dry run, which only reads the source names) is the way to see the hosted sources; run it while the runner is working, it writes nothing (due 2026-11-02)
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): Decide on Onepoint (its terms forbid "extraction" of the Site's content without authorization; the jobs are on a Workday-hosted site, bots not mentioned) and read PwC's legal notice (carrieres.pwc.fr/fr/legal.html) in a browser, before either is enabled; details in evidence/consulting_batch_c2_2026-11-03.md (due 2026-11-03)
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): Accept the step 2 Neon figure (BCG and EY: +0.03 MB a pass, +2.1 MB once) and say which to enable (I recommend both); Onepoint and PwC wait for your terms decisions. Then slice 21: `seed_hosted_sources.ps1 -Step 2` (dry run first), see evidence/seed_dry_run_step2.md (due 2026-11-03)
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): In the hosted step (slice 12 or 21), switch OFF these six sources on the Sources page (not delete): Energy Pool (smartrecruiters), Publicis Groupe (smartrecruiters), Trade Republic (greenhouse), Esker (teamtailor), Uber (smartrecruiters), EssilorLuxottica (smartrecruiters). Why, and what I changed in the lists: evidence/recheck_live_2026-11-03.md; tell me if you disagree with any (due 2026-11-03)
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): Two sources are failing and worth a look: Doctolib (greenhouse board 404 since 2 November) and Papernest (404 once); I can switch Doctolib off or find its new board if you say so (due 2026-11-03)
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): Optional: the Neon reading after this pass (the Workday sources and Doctolib read for the first time); and whether you switched Valiantys (lever) off yourself (I did not) (due 2026-11-04)
- 024 Simplify-ops-console: Slice 8, after the commit (4d29c37): push, deploy on Render, open https://app.saxobeat.fr/ops/ and click through the seven areas (due 2026-11-04)
- 029 Keyword edits rescore the inbox: Say the request in your own words (replaces the relayed 021 finding in intent.md) (due 2026-11-05)
- 033 Invitation codes for sign-up: Read verify.md; say if 20 sign-ups an hour is too loose (one account is about 8 MB, so 160 MB an hour; room for about 40 accounts in Neon's 0.5 GB): one constant in `jobs/accounts.py` (due 2026-11-06)
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): Give the verdict in verify.md (22 criteria: 17 pass, 1 accepted, 4 partial; the partials are terms not read for Finastra, SWIFT, Fenergo and PwC, Onepoint's clause, Onepoint and PwC not measured, consulting-only list counts): accepted, or sent back (due 2026-11-10)
- 002 Move to a fresh Neon project, keep the old one as a fallback: Optional: keep a copy of the old connection string in a password manager (criterion 2, accepted risk)
- 030 International destinations chosen individually (narrowed: edit the cities in Settings in standard mode): After the deploy: open Settings as a standard candidate on the host and see the places card; decide the two deferred rows in learn.md
- 001 A local copy of the Neon database: Daily from 2026-11-04 (first reading: 0.31 GB at 10:17): read the sum (two decimals) and the time, and add one line: how many runner runs since the last reading and anything unusual (a profile or keyword change, the console's AI export or import pages). Seven days of that closes criterion 9
- 001 A local copy of the Neon database: Optional: in Neon, look for a usage graph or billing history that still shows 31 Oct and 1 Nov per project
- 001 A local copy of the Neon database: Standing rule: do not run the runner, `ai sync` or a backup against the hosted database until the plan says how
- 003 Make e-mail live (Brevo, mail.stoyan.ovh, jobs.stoyan.ovh): Carried over, not blocking: the console's E-mails page, open the **failed** row (it was *waiting* on 2 Nov) and tell me its kind, address and error text (verify F2; if it is the Brevo 401, D3 has happened). Do this before the first friend
- 003 Make e-mail live (Brevo, mail.stoyan.ovh, jobs.stoyan.ovh): Carried over: the rehearsal (invite a second address of yours, create the account on `app.saxobeat.fr`, then "Forgot password": "1 hour", links to `app.saxobeat.fr`), then the first friend, ideally Outlook/Hotmail/Live (criteria 9 to 12, 18, 19)
- 003 Make e-mail live (Brevo, mail.stoyan.ovh, jobs.stoyan.ovh): (optional) which address you had open when you sent the iCloud test: if `app.saxobeat.fr`, it also proves a form works there (criterion 19)
- 003 Make e-mail live (Brevo, mail.stoyan.ovh, jobs.stoyan.ovh): Say "close 003" to mark the cycle Closed in the README when you are content with the carried items; they stay listed above
- 003 Make e-mail live (Brevo, mail.stoyan.ovh, jobs.stoyan.ovh): (tidy-up, not blocking) delete the CNAME `jobs` at the OVH DNS host for `stoyan.ovh`, it now points at nothing
- 003 Make e-mail live (Brevo, mail.stoyan.ovh, jobs.stoyan.ovh): (optional, not blocking) paste the SPF, DKIM, DMARC lines from Gmail's "Show original" of the test e-mail, and one line on what you changed in Brevo's sender setup (for DEPLOY.md)
- 003 Make e-mail live (Brevo, mail.stoyan.ovh, jobs.stoyan.ovh): Next cycle candidates are in `learn.md` (unpause candidate e-mails, DMARC tightening, bounces, 009 and 011); the push of the learn-step commit is the owner's call [both]
- 004 Check the hosted app after the 28 October deploys: F2: take a manual snapshot of saxobeat-prod1 in Neon
- 005 Real phones, real laptops, and a browser test harness: Answer Q1-Q3 in intent.md (or accept the recommended answers)
- 015 A feedback chat, always one tap away: Look at the screenshots in `evidence/screens/` (the button, the chat in English and French, the console page) and say if the look and the place are right
- 015 A feedback chat, always one tap away: **Before any push of `main` for another cycle:** slices 1 to 5 are already committed on `main`, so pushing it ships the feedback button and migration 0041 to everyone (another session's note says the same). Tell me first if you would rather hold the push until slice 9, or I can move cycle 015's commits to a branch
- 015 A feedback chat, always one tap away: Decide whether to fix the existing sheets that open top-left on wide screens (a one-line CSS change in `dialog.sheet`, outside this cycle)
- 015 A feedback chat, always one tap away: Read the People page and tell me how many people use the app (fills the "unknown" fact; not blocking)
- 015 A feedback chat, always one tap away: Slice 11: tell the friends about the round button once; about two weeks later we read the console: at least 5 chats from at least 3 friends (the owner's own tests are deleted, so they will not count)
- 015 A feedback chat, always one tap away: Slice 11: send the friends the invitation with the instructions, and tell me the date it went out; the two-week count (5 chats from 3 friends) is read 14 days after, on the console
- 021 Bilingual keyword scoring: Optional: look at Render's Events for the 502 seen at about 18:16 to 18:19 on 2026-11-04 after the rescore (cause unknown)
- 025 Environments: prod, pre-prod, testbed: Read spec.md and approve it, or say what to change (D4: the two small app changes, banner and mail guard, are the one point the intent did not cover)
- 033 Invitation codes for sign-up: Test the links: sign up through the Skaleet link with an address of yours (the screen is live), then open `/invite/` on a phone (code, link, Share button) and tell me what you see
- 007 Measure what the PRDs promised: Answer Q1-Q3 in intent.md (or accept the recommended answers)
- 008 Keep score 50 meaning the same over time: Answer Q1-Q2 in intent.md (or accept the recommended answers)
- 009 Reminder and alert e-mails, and web push: Answer Q1-Q2 in intent.md (or accept the recommended answers)
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): Slice 12, step 1: take a manual Neon snapshot of prod1 (the way back; Neon restores prod1 only about 6 hours otherwise)
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): Slice 12, step 2: run the dry run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\seed_hosted_sources.ps1`, read what it lists (existing sources for these employers; 10 would be created, all off) and tell me what it printed, without any address
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): Slice 12, step 3: the write, `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\seed_hosted_sources.ps1 -Apply -SnapshotTaken`: expect `10 sources added`, then one difference `jobs_source`, then `0 sources added`
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): Slice 12, step 4: on the Sources page switch on, in this order, after a by-hand runner pass each (runbook `001-local-db-replica/evidence/restart_runbook.md`: read Neon before and after): first Saegus, Murex, Payhawk, Checkout.com, Accenture; then Capgemini (the big one: 13 pages, about 405 jobs); Finastra only after reading its terms of use in a browser. Backbase, Fenergo and SWIFT stay off
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): Optional, weekly: the next reading on 2026-11-17 (first steady week) and the Neon figures; whether you switched Valiantys (lever) off yourself (I did not)
- 029 Keyword edits rescore the inbox: Copy `data/backups/saxobeat_2026-10-29_100546.dump` to the new computer (gitignored, needed for slices 2 and 9), or say to take a fresh backup
- 031 Stop analysing postings older than 30 days: After the deploy: read how many views the host hid for age, per candidate, before and after (read-only counts cost Neon allowance: say it first); evidence/counts.md is the 29 Oct estimate
- 006 Bring the PRDs and DEPLOY.md up to date: Answer Q1-Q2 in intent.md (or accept the recommended answers)
- 010 Finish the phone interactions: Answer Q1-Q2 in intent.md (or accept the recommended answers)
- 011 Settings and small interface gaps: Answer Q1 in intent.md (or accept the recommended answer)
- 012 What my applications teach me (the rest of F11): Answer Q1 in intent.md (or accept the recommended answer)
- 016 Blocking an employer, an icon and a list where companies live: When you pick this cycle up: answer Q1-Q4 in intent.md (recommended answers drafted)
- 016 Blocking an employer, an icon and a list where companies live: Confirm the goal and success measure
- 018 Import job-alert e-mails (LinkedIn, WTTJ, APEC, Indeed): Answer Q1 in intent.md when the cycle is picked up (low priority: no date)
- 020 Revolut People career sites as a source: Then enable Worklife on the Sources page after a by-hand runner pass (5 requests, 4 jobs)
- 022 Reposted after applied: Sign in on app.saxobeat.fr in the browser pane (I never type passwords: the pane was reopened signed out on 2026-11-10)
- 023 The AI "how it works" information should not be on by default: **The one thing left:** on your phone open two job pages and touch nothing; tell me whether the tutorial shows on the second (criterion 9). If you cleared site data or use another browser it can show once more: that is the first visit

**My move (the agent)**

- 002 Move to a fresh Neon project, keep the old one as a fallback: Commit the pending doc edits and the closing result in one commit (due 2026-10-30)
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): Then: switch on Capgemini (about 405 jobs, 13 pages a run), later BCG and EY; the one-week reading (slice 13) counts from this first full run (2026-11-03) (due 2026-11-03)
- 002 Move to a fresh Neon project, keep the old one as a fallback: Optional: fix the stale "Not verified yet" section at the end of docs/DEPLOY.md
- 001 A local copy of the Neon database: Finish slice 5 with `W`: the final projection, then verify (criteria 1 to 11) and, after the push and a week of readings (slice 9), close
- 003 Make e-mail live (Brevo, mail.stoyan.ovh, jobs.stoyan.ovh): Not done, a later decision: slice 11 (counts of who an unpause would e-mail, with the owner's OK); asked for only when the owner wants to unpause candidate e-mails
- 005 Real phones, real laptops, and a browser test harness: Draft spec.md once the intent is approved
- 015 A feedback chat, always one tap away: Read the console at the two-week date (counts and fields only unless the owner asks for the text), draft learn.md with the success measure compared, and propose the cycles the feedback suggests
- 025 Environments: prod, pre-prod, testbed: After the spec is approved: write plan.md (slices; the owner's account steps listed one by one; the one switch of prod's branch is a single, rollback-able edit)
- 033 Invitation codes for sign-up: After the owner's verdict: tick criteria 13 and 18 in verify.md, tick the last row of learn.md, set the README row to closed, refresh the board
- 007 Measure what the PRDs promised: Draft spec.md once the intent is approved
- 008 Keep score 50 meaning the same over time: Draft spec.md once the intent is approved
- 009 Reminder and alert e-mails, and web push: Draft spec.md after cycle 003 closes
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): List each source's terms and robots rules in evidence/
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): Slice 5 after your answer: live look at the empty/suspect boards (at most 5 jobs each; I state the request count first)
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): Slice 4 and 5 still wait for the owner's review of `evidence/recheck_2026-10-30.md` (24 employers); slice 13 (the one-week reading) starts after the first full run
- 013 More sources (employers' own sites, VC boards, aggregators, Personio): After the verdict: write learn.md (findings: US ZIP codes read as Paris, `max_jobs` meanings, Qonto moved boards silently, a board that goes empty stays "ok", WelcomeKit gone; destination of each), then close the cycle
- 026 Cloud runner for sources: Wait for 025 to reach spec, then grill questions 1 to 4 (the datacenter-address question first)
- 027 Cloud AI agent step: Wait for 025 and 026 to reach verify, then grill questions 1 and 2 (parked until then)
- 028 Cloud dev workspace: Wait for 025 question 1 and 2 (testbed content and refresh), then grill questions 1 to 3
- 029 Keyword edits rescore the inbox: Build slice 1 (the hash, `scoring.inputs_hash`): next action, nothing built yet; read "Resume here" at the end of plan.md first (migration number is now 0045; the dump and `.env` do not travel to another computer)
- 006 Bring the PRDs and DEPLOY.md up to date: Write the audit's stale list into evidence/ and draft spec.md
- 010 Finish the phone interactions: Draft spec.md once the intent is approved
- 011 Settings and small interface gaps: Draft spec.md once the intent is approved
- 022 Reposted after applied: After the sign-in: read the host once for criteria 12 and 14: `/job/36143/` (banner), `/job/31673/` (pointer), `/` (header, row count, how long it took) and then `/?reapplied=hide` as ONE request with a 30-second limit and the time said. If it answers in about a second the fix is live; if it hangs, stop at once and tell the owner (the first design took the host down). Save the readings in `evidence/host_read_<date>.md`, update verify.md rows 12 and 14, then ask for the verdict
- 022 Reposted after applied: Draft learn.md after the verdict: PRD_mobile.md (the "already applied" first chip on a card), the process rule (time any query over a candidate's whole list of views on the local copy before a push), decisions D1 and D2
- 023 The AI "how it works" information should not be on by default: On your word: record criterion 9 in verify.md, finish `learn.md` (a draft exists since 2026-11-10: update `PRD_ai_backoffice.md` about line 424, then tick the rows), tick the gates, close the cycle (README row, board)
- 023 The AI "how it works" information should not be on by default: If it still shows on the second page: reopen the spec (what did the phone do? same browser? installed app?) and diagnose from the live script before changing code

## Cycles

| # | Cycle | Imp. | Now | Intent | Spec | Plan | Build | Verify | Learn | Criteria | Touched |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 001 | A local copy of the Neon database | 4/5 | Verify | x | x | x | x | o | o | 9/11 | 2026-11-04 |
| 002 | Move to a fresh Neon project, keep the old one as a fallback | 5/5 | Learn | x | x | x | x | x | o | 11/11 | 2026-10-30 |
| 003 | Make e-mail live (Brevo, mail.stoyan.ovh, jobs.stoyan.ovh) | 4/5 | Closed | x | x | x | x | x | x | 9/19 | 2026-11-03 |
| 004 | Check the hosted app after the 28 October deploys | 4/5 | Closed | x | x | x | x | x | x | 10/10 | 2026-10-30 |
| 005 | Real phones, real laptops, and a browser test harness | 4/5 | Intent | o | . | . | . | . | . |  | 2026-10-30 |
| 006 | Bring the PRDs and DEPLOY.md up to date | 2/5 | Intent | o | . | . | . | . | . |  | 2026-10-30 |
| 007 | Measure what the PRDs promised | 3/5 | Intent | o | . | . | . | . | . |  | 2026-10-30 |
| 008 | Keep score 50 meaning the same over time | 3/5 | Intent | o | . | . | . | . | . |  | 2026-11-04 |
| 009 | Reminder and alert e-mails, and web push | 3/5 | Intent | o | . | . | . | . | . |  | 2026-10-30 |
| 010 | Finish the phone interactions | 2/5 | Intent | o | . | . | . | . | . |  | 2026-10-30 |
| 011 | Settings and small interface gaps | 2/5 | Intent | o | . | . | . | . | . |  | 2026-10-30 |
| 012 | What my applications teach me (the rest of F11) | 2/5 | Intent | o | . | . | . | . | . |  | 2026-10-30 |
| 013 | More sources (employers' own sites, VC boards, aggregators, Personio) | 3/5 | Verify | x | x | x | x | o | . | 12/13 | 2026-11-10 |
| 014 | Runner and data correctness | 5/5 | Closed | x | x | x | x | x | x | 7/7 | 2026-10-30 |
| 015 | A feedback chat, always one tap away | 4/5 | Learn | x | x | x | x | x | - | 17/18 | 2026-10-30 |
| 016 | Blocking an employer, an icon and a list where companies live | 2/5 | Intent | o | . | . | . | . | . |  | 2026-10-30 |
| 017 | Remove the shortcuts explanation from the inbox | 1/5 | Dismissed 2026-10-30 | ~ | ~ | ~ | ~ | ~ | ~ |  | 2026-10-30 |
| 018 | Import job-alert e-mails (LinkedIn, WTTJ, APEC, Indeed) | 2/5 | Intent | o | . | . | . | . | . |  | 2026-10-30 |
| 019 | Presume an application rejected after a month of silence | 3/5 | Closed | x | x | x | x | x | x | 17/18 | 2026-11-04 |
| 020 | Revolut People career sites as a source | 2/5 | Learn | x | x | x | x | x | o | 12/14 | 2026-11-04 |
| 021 | Bilingual keyword scoring | 4/5 | Closed | x | x | x | x | x | x | 16/18 | 2026-11-05 |
| 022 | Reposted after applied | 2/5 | Verify | x | x | x | x | o | . | 12/14 | 2026-11-10 |
| 023 | The AI "how it works" information should not be on by default | 2/5 | Verify | x | x | x | x | o | o | 7/9 | 2026-11-10 |
| 024 | Simplify-ops-console | 3/5 | Closed | x | x | x | x | x | x | 9/10 | 2026-11-04 |
| 025 | Environments: prod, pre-prod, testbed | 4/5 | Spec | x | o | . | . | . | . |  | 2026-11-10 |
| 026 | Cloud runner for sources | 3/5 | Intent | o | . | . | . | . | . |  | 2026-11-05 |
| 027 | Cloud AI agent step | 3/5 | Intent | o | . | . | . | . | . |  | 2026-11-05 |
| 028 | Cloud dev workspace | 3/5 | Intent | o | . | . | . | . | . |  | 2026-11-05 |
| 029 | Keyword edits rescore the inbox | 3/5 | Build | x | x | x | o | . | . |  | 2026-11-10 |
| 030 | International destinations chosen individually (narrowed: edit the cities in Settings in standard mode) | 5/5 | Learn | x | x | x | x | x | o | 9/9 | 2026-11-10 |
| 031 | Stop analysing postings older than 30 days | 3/5 | Learn | x | x | x | x | x | o | 11/11 | 2026-11-10 |
| 032 | Operator cannot delete a user, it times out | 4/5 | Closed | x | x | x | x | x | x | 8/9 | 2026-11-06 |
| 033 | Invitation codes for sign-up | 4/5 | Verify | x | x | x | x | o | o | 16/18 | 2026-11-10 |
