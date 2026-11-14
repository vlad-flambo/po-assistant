# Intent: Environments: prod, pre-prod, testbed

| | |
|---|---|
| **Cycle** | 025 |
| **Stage** | Intent |
| **Date** | 2026-11-05 |
| **Owner** | Vladimir Stoyanov |
| **Importance** | 4/5 (claude, 2026-11-05): every push to main deploys to prod today (render.yaml autoDeployTrigger defaults to commit) while the working tree holds other cycles' work; 022's note says one unreleased change can make the host stop answering; unlocks 026 to 028 |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
> new intent: I want to run everything on the cloud. If pertinent, split this into separate cycles. This includes: runner pc, be able to trigger this on a dedicated Render instance. The free tier is probably going to be ok for ad-hoc runs. Should this be a separate repo or app? Or do I just deploy the app a second time on a separate instance with ability to do the runs, pointing to same db? Open to suggestions on this.
>
> Is there a way to orchestrate a prod + pre-prod + testbed set of environments? Each probably hooked to a separate db. We could have a job to sync pre-prod + testbed with prod info, so those dbs stay current. I don't want every commit to trigger deployments on prod.
>
> Also, I want to be able to do the dev on a Claude instance in the cloud. Probably would be good to have a testbed db, so dev doesn't eat up the prod bandwidth. We could use the fallback1 db to start.

(Said on 2026-11-05. It was split into four cycles: this one is the environments part; the runner is 026, the AI step 027, the cloud dev workspace 028.)

## Why now / the pain
- **Every push to `main` deploys to prod.** `render.yaml` sets no `autoDeployTrigger`, and Render's default is `commit`; DEPLOY.md records a push deploying by itself (`d1718a0`, 29 October). The working tree holds several cycles' work at once (git status on 2026-11-05 shows 15 modified files from 021/022 and others), and cycle 022's board note says an unreleased change "can make the site stop answering".
- **There is nowhere to try a change on the host** before candidates see it. Rehearsals of anything that writes to Neon run on a local copy of the data, and the local copy of prod1 is stale (last written 2026-10-22, board note of 2026-11-02).
- **Dev reads prod.** Anything that wants real volume (rescore previews, runner measurements) spends prod1's 5 GB monthly allowance; Neon counts every byte read out.

## Goal
Three separate environments, each with its own web service and its own database, where a commit can reach pre-prod and testbed freely and reaches prod only when the owner decides, and where pre-prod and testbed hold current data from prod without costing prod's allowance more than a small, known amount per refresh.

## Success measure
1. A commit pushed to the development branch does **not** change what is running at `app.saxobeat.fr` (shown by Render's deploy list for prod: no new deploy).
2. Pre-prod and testbed each answer `/healthz` and run the app against their own database (shown by a write made there that is absent from prod1).
3. One command or button refreshes testbed and pre-prod from prod; its cost in prod1 reads is measured and written down; the copies hold the same candidates as prod (row counts match) but no copy can send an e-mail to a real address (checked by a query on addresses and by a send attempt that ends *skipped*). Revisit "full copy" when the user base grows (owner, 2026-11-05).
4. Promoting a tested commit to prod is one deliberate action by the owner, and the way back is written down and rehearsed.

## Not doing (this cycle)
- Moving the runner, the AI step, or the dev workspace to the cloud (026, 027, 028).
- Changing the app's behaviour. Only deployment, configuration and data-refresh scripts change.
- Traffic splitting, blue/green, or paid Neon/Render tiers beyond what the owner approves.
- Replacing Neon or Render.

## What we already know (facts, with where they came from)
- Prod web: Render **Starter** (about 7 USD a month), Frankfurt, auto-deploys from `main` (`render.yaml`; DEPLOY.md "Verified on the host"). Custom domain `app.saxobeat.fr`, DNS at IONOS (DEPLOY.md §7).
- Render's Blueprint has `autoDeployTrigger: off | commit | checksPass`, a per-service `branch`, and optional pull-request previews (`previews.generation`) (render.com/docs/blueprint-spec, read 2026-11-05). Render **free** web services: 750 instance hours a month per workspace, sleep after 15 idle minutes (about a minute to wake), no one-off jobs (render.com/docs/free, read 2026-11-05). Prod is Starter, so free pre-prod and testbed services should fit inside the 750 hours.
- Neon free plan, per project: 5 GB network transfer a month, 100 compute hours, 10 branches (root included); **branches share the project's compute and transfer** (neon.com/docs/introduction/plans, read 2026-11-05). So a Neon branch of prod1 would spend prod1's own allowance; a separate project would not. The same page says **1 GB storage per project**, while DEPLOY.md says 0.5 GB: to check in the console.
- Two Neon projects exist: `saxobeat-prod1` (live) and `saxobeat-fallback1` (a 2026-10-29 snapshot, nothing reads or writes it; counters reset on 1 November, so it has its full 5 GB again) (DEPLOY.md §8).
- A full dump of prod1 reads about **227 MB** (measured 2026-10-29, cycle 001); data sent in does not count. Job postings are most of the data (about 180 MB in total, DEPLOY.md); candidates' CVs and profiles are a small part (to be measured per table: `scripts/step_table_sizes.py` exists).
- **Personal data:** CVs are personal data; friends' accounts are real people (DEPLOY.md "Security notes").
- **Mail:** the PC's `.env` holds a live Brevo key; `SAXOBEAT_MAIL=off` makes every e-mail end *skipped* (DEPLOY.md §7 step 6). A copy of prod's candidates with mail on would e-mail real people.
- No `.github` folder, so no CI exists; tests run on SQLite with `SAXOBEAT_MAIL=console DATABASE_URL=` (PROJECT.md). Local branches: `main`, `email`, `runner-reads-less`, `users-modes-blocklist`; the remote has only `main`.
- One Docker image runs everything; `scripts/entrypoint.sh` runs `migrate` and `ensure_admin` on boot (so a new database gets its schema when a service first starts).

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | What data do pre-prod and testbed hold? | Jobs, sources, employers and settings copied as they are (public data, most of the bytes); **candidates' personal data left out**: only your own candidate account is kept (or synthetic ones); friends' accounts, CVs, profiles and applications are not copied. A selective dump also reads less from prod1 than the 227 MB full one. | **Full copy, for now** (owner, 2026-11-05): "I want to be able to simulate the flow and views of others for debugging. If the user base grows, we can reconsider." Recommendation (selective copy) not taken; the safeguards it implied move to questions 6 and 7. | answered |
| 2 | How are they kept current: a Neon branch of prod1, or a dump restored into a separate project? | Selective dump restored into a **separate** project: `fallback1` for testbed now, a new free project for pre-prod. A branch would spend prod1's transfer and compute, which is what we want to protect. | Accepted as recommended (owner, 2026-11-06) | answered |
| 3 | Which branch deploys where? | `main` -> pre-prod (after CI passes); a `release` branch (or tag) -> prod with `autoDeployTrigger: off`, deployed by hand from Render (or by fast-forwarding `release`); testbed from a `dev` branch or a manual deploy. | Accepted as recommended (owner, 2026-11-06) | answered |
| 4 | Do we add CI (GitHub Actions running the test suite on every push)? | Yes: the free tier is enough, it is what `checksPass` needs, and it is the gate between pre-prod and prod. | Accepted as recommended (owner, 2026-11-06) | answered |
| 5 | How many Render services and at what plan? | Pre-prod and testbed on the **free** plan (they may sleep); prod stays Starter. All three from one `render.yaml` Blueprint, or one Blueprint per environment. | Accepted as recommended (owner, 2026-11-06) | answered |
| 6 | Do pre-prod and testbed send e-mail? | Never: `SAXOBEAT_MAIL=off` set in the Blueprint for both, and the Brevo key not given to them. Now more important, because the copies hold real friends' addresses. | Accepted as recommended (owner, 2026-11-06) | answered |
| 7 | (new, from the answer to 1) With a full copy, are the contact channels and logins neutralised in the copies? | Yes: after each refresh, friends' e-mail addresses become `<id>@example.invalid` and their password hashes are made unusable, so a copy can never e-mail or be logged into as a friend, even if mail is switched on by mistake. You log in as yourself and use *View as* to see their flows and views (it exists in the app). CVs, profiles, applications and scores stay intact, which is what debugging needs. | **Yes, neutralise** (owner, 2026-11-05). The step runs only against a copy: it must refuse to run if the target is prod1 (guard check in the plan), and the owner's own account keeps its address and password. | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- **The copies hold friends' real CVs** (owner's choice on question 1, 2026-11-05). A copy must never e-mail candidates (questions 6 and 7), and the operator, plus anyone given the testbed's address (cycle 028's cloud session), can read them: DEPLOY.md tells candidates only that the operator can see CVs, so a sentence there should say copies exist for debugging. Pre-prod and testbed need a login wall (the app is invitation-only already) and the testbed's address is a secret.
- A full dump of prod1 reads about 227 MB each refresh against prod1's 5 GB, so refresh on demand, not on a schedule, until the cost is measured.
- Neon free storage is per project; fallback1 holds a full snapshot already (read the figure in the console before restoring anything into it, and keep its counts first: it is also the recovery copy).
- Free Render services sleep and can be restarted at any time (render.com/docs/free); fine for pre-prod and testbed, not for prod.
- Changing prod's deploy trigger and the Render settings are outward actions: the owner performs them (accounts); nothing is switched on prod without an approved plan.
- Rehearse the dump and restore on the local Docker first (recipe in DEPLOY.md §8, steps 3 to 5).

## Gate
- [x] All open questions answered or parked (7 of 7, 2026-11-06)
- [x] Goal and success measure confirmed by the owner (2026-11-10: "draft confirmed")
