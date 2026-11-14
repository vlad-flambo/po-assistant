# Spec: Environments: prod, pre-prod, testbed

| | |
|---|---|
| **Cycle** | 025 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |
| **Drafted** | 2026-11-10 (by claude, from the answers of 2026-11-05 and 2026-11-06) |

## Behaviour when finished

- Three Render web services run the same image from one `render.yaml`:
  - **prod** (`saxobeat`, `https://app.saxobeat.fr`): Starter plan, deploys only from the `release` branch and only when the owner triggers it.
  - **pre-prod** (`saxobeat-preprod`, an `onrender.com` address): free plan, deploys from `main` once the tests have passed on GitHub.
  - **testbed** (`saxobeat-testbed`, an `onrender.com` address): free plan, deploys from `dev` on every commit (the branch cloud dev sessions, cycle 028, push to).
- Each has its own Neon project: prod on `saxobeat-prod1`, pre-prod on a new project `saxobeat-preprod1`, testbed on the project that is `saxobeat-fallback1` today (renamed `saxobeat-testbed1` once the owner has taken a Neon snapshot of prod1 to play the recovery role).
- A pre-prod or testbed database is a **full copy of prod**, made on demand by one script, with friends' e-mail addresses replaced and their passwords made unusable. The owner's own account is left as it is. The owner logs in as themselves and uses *View as* to see what a friend sees.
- A copy cannot send e-mail: the setting is off, and the code refuses to send from any environment that is not prod even if the setting is switched on by mistake.
- Pushing to `main` or `dev` never changes what candidates see at `app.saxobeat.fr`. Going live is one deliberate action by the owner (moving `release` to a commit that has already run on pre-prod), and there is a written, rehearsed way back.
- A GitHub Actions workflow runs the test suite on every push and pull request.

## Acceptance criteria
Each one must be checkable in `verify.md`.

**Deploy control**
1. [ ] `render.yaml` defines three services with the settings above (prod: `plan: starter`, `branch: release`, `autoDeployTrigger: off`; pre-prod: `plan: free`, `branch: main`, `autoDeployTrigger: checksPass`; testbed: `plan: free`, `branch: dev`, `autoDeployTrigger: commit`), and Render's settings pages show the same.
2. [ ] The switch changes nothing for candidates: the branch `release` was created at the commit prod was running just before, and the deployed commit shown on Render and `/healthz` are the same before and after (commit hash named in the evidence).
3. [ ] A commit pushed to `main` and one pushed to `dev` each deploy to their service and create **no** deploy on prod (Render's deploy list for prod, read before and after).
4. [ ] A commit whose tests fail on GitHub is **not** deployed to pre-prod (shown once, on a throwaway commit, with the GitHub run and Render's deploy list).

**CI**
5. [ ] `.github/workflows/` runs `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider` on a Linux runner on every push and pull request to `main`, `dev` and `release`; it is green at the commit that closes the cycle. A second job runs the suite against Postgres 17 and is reported, and it is made required only if it is green on three consecutive pushes (decision D3).

**Environments and databases**
6. [ ] Pre-prod and testbed each answer `/healthz` with `ok` and run on their own Neon project: a change made by the operator on the testbed (a setting) is absent from prod1 and from pre-prod (counts or timestamps compared), and a login on a copy does not move `max(last_login)` on prod1.
7. [ ] Each environment has its own `DJANGO_SECRET_KEY`, set in Render and never in the repository; a session cookie from one is refused by the others.
8. [ ] The environment's name (`prod`, `preprod` or `testbed`) is set by `SAXOBEAT_ENV` and shown on every page of a copy ("Pre-prod: a copy of prod, not real"); prod shows nothing new.

**Refresh and neutralise**
9. [ ] One script (`scripts/refresh_copy.py`, Python so it runs on Windows and macOS) refreshes a copy from prod1. Its first line says which database it reads and which it writes, without addresses. It reads the connection strings from environment variables by name (`SAXOBEAT_HOSTED_DATABASE_URL` as the source, `SAXOBEAT_PREPROD_DATABASE_URL` or `SAXOBEAT_TESTBED_DATABASE_URL` as the target) and never prints them.
10. [ ] The script **refuses**, writing nothing, when the target is not one of the two copy variables, when the target host equals the source host, or when the target database holds data and `--replace` is not given. Each refusal is shown with a run and a before/after row count of prod1.
11. [ ] After a refresh, every table's row count in the copy equals prod1's (compared with `scripts/db_counts.py`), except tables the neutralising step changes by design (none are deleted).
12. [ ] After neutralising, in the copy: no user other than the operator has an e-mail address that does not end in `@example.invalid`; no such user has a usable password; every other column that holds an e-mail address (the plan lists them from a scan of the schema: today `auth_user.email`, `jobs_outgoingemail.to_address` and `jobs_invitation.email`; `jobs/models.py:270` `contact_email` holds a recruiter's address a candidate typed, which the app never mails: the plan says whether it is neutralised too) is neutralised the same way; the operator can log in; CVs, profiles, applications and scores keep their counts.
13. [ ] The neutralising step runs only when `SAXOBEAT_ENV` is `preprod` or `testbed`: against a prod environment it exits with an error and changes nothing (test, and one attempt shown).
14. [ ] On both copies a send attempt ends *skipped*: the console E-mails page says the provider is off, and a test shows that `SAXOBEAT_ENV` other than `prod` forces the provider off even when `SAXOBEAT_MAIL=brevo` is set.
15. [ ] The Neon reading on prod1 for one full refresh is recorded (before and after, two decimals, time) and stays under 0.30 GB (a full dump measured 227 MB on 2026-10-29). Each copy's storage is read in the console and fits its project's limit (and the record says whether the free limit is 0.5 or 1 GB, which the docs disagree on).

**Recovery and promotion**
16. [ ] Before the old fallback project is overwritten: a manual Neon snapshot of prod1 exists (the new recovery copy), and the fallback's row counts were saved with `db_counts.py --save` (file kept in the cycle's `evidence/`).
17. [ ] Promotion is documented as one command (`git push origin <commit>:release`, or the equivalent button) and was rehearsed once with a commit that is already live (prod redeploys it, `/healthz` ok). The way back (Render's rollback to the previous deploy, or moving `release` back) was rehearsed on pre-prod and its steps are written down.
18. [ ] `docs/DEPLOY.md` has an "Environments" section: the shape, who deploys what, how to refresh, promote and roll back, the personal-data note for friends ("copies of the data exist for debugging; the operator and the development session can read them") and the free-plan limits. `.env.example` lists the two new variable names (it is hidden from git today by the `.env.*` rule in `.gitignore`: the plan adds `!.env.example` so it is tracked).

**Safety**
19. [ ] No connection string or key appears in the repository, in a workflow file or in a CI log (searched), and none was typed on a command line.
20. [ ] The full suite is green on SQLite at the closing commit, with tests for criteria 8, 12 (the neutralise functions on a throwaway database), 13 and 14.

## Design in brief

- **One Blueprint, three services** (`render.yaml`). Render matches a service by name, so the existing `saxobeat` service takes its new branch and trigger from the file; the two new ones are created. Secrets stay `sync: false` (typed in Render by the owner).
- **Git flow:** `main` is the integration branch (pre-prod), `release` is what prod runs, `dev` is the testbed's and cloud sessions'. Promotion moves `release` forward. Only the owner pushes `release`.
- **CI first:** GitHub Actions, `uv sync --frozen`, the project's test command. It makes `checksPass` possible and gates pre-prod.
- **Copies from prod by dump and restore into separate Neon projects** (a Neon branch of prod1 would spend prod1's transfer and compute: intent Q2). The script reuses what cycle 002 proved (`pg_dump`/`pg_restore` through Docker `postgres:17`, the `DEFAULT ACL` filter, `db_counts.py`).
- **Neutralising is a Django management command** (`neutralise_copy`) run by the script against the target only, guarded by `SAXOBEAT_ENV`. It changes addresses to `<id>@example.invalid` and sets unusable passwords with Django's own function, so no hash or token is invented.
- **The environment name** is one new setting (`SAXOBEAT_ENV`, default `prod`), used for the banner and for the mail guard.
- **Rejected:**
  - *Neon branches for the copies*: shared transfer and compute with prod1, which is the thing being protected.
  - *Render pull-request previews as the testbed*: need a paid-plan feature set and a database per preview; a fixed service is simpler.
  - *A selective copy*: the owner chose a full copy for debugging other people's flows (intent Q1).
  - *Keeping `main` as prod's branch and holding commits back*: relies on discipline, which is today's problem.
  - *PowerShell-only refresh script*: the owner is moving to macOS; Python runs on both.

## Interfaces and data

- New: `.github/workflows/tests.yml`; `scripts/refresh_copy.py`; `jobs/management/commands/neutralise_copy.py`; the `SAXOBEAT_ENV` setting and banner (a template change); the mail guard in `config/settings.py` or the mail service; tests.
- Changed: `render.yaml`; `docs/DEPLOY.md`; `.env.example`; `docs/sdlc/PROJECT.md` (hosts and variables); later, house-stack `reference/hosting.md` "Environments" (learn step).
- Environment variables (names only): `SAXOBEAT_ENV`; in `.env` on the owner's machine: `SAXOBEAT_PREPROD_DATABASE_URL`, `SAXOBEAT_TESTBED_DATABASE_URL` (the old `SAXOBEAT_FALLBACK_DATABASE_URL` is renamed when the project is). On Render: per service `DATABASE_URL`, `DJANGO_SECRET_KEY`, `SAXOBEAT_ENV`, `SAXOBEAT_MAIL=off`, `SAXOBEAT_RUN_SOURCES=0`, `WEB_CONCURRENCY=1`, the operator login for the copy. No migration.
- The two copies use their `onrender.com` address (the app reads `RENDER_EXTERNAL_HOSTNAME`, `config/settings.py:39`), so no DNS change and no `DJANGO_ALLOWED_HOSTS` value is needed for them; prod keeps `app.saxobeat.fr`.

## Constraints

- **Personal data:** the copies hold friends' real CVs (owner's choice, intent Q1). Their addresses are the only thing neutralised. The copy's address is not public knowledge but the app answers on the internet: the login wall and the invitation-only sign-up apply, and no operator link is sent from a copy.
- **Free plans:** a free Render service sleeps after 15 idle minutes and counts instance hours only while awake (750 a month for the workspace, render.com/docs/free, 2026-11-05). **Never add a pinger or uptime check to a copy.** Neon free: 5 GB transfer and 100 compute hours per project.
- **Prod's Neon allowance:** a refresh reads about 227 MB from prod1. On demand only, with a figure written down, until the owner decides otherwise.
- **Migrations and rollback:** code can be rolled back, a migration cannot. Only promote a commit whose migrations ran on pre-prod against the copy of prod, and write migrations that the previous code survives (the cycle-by-cycle rule becomes a line in DEPLOY.md).
- **Outward actions that are the owner's** (accounts): creating the Neon project, the snapshot, applying the Blueprint, changing prod's branch and trigger, creating the Render services and their variables, pushing `release`. The plan lists each with its check and rollback. Nothing touches prod before the plan's one switch slice.
- **Intent says "no app behaviour change"; this spec adds two small ones** (the environment banner and the mail guard), both inert on prod. Say no to approve the spec without them.
- **Secrets** (PROJECT.md): connection strings travel in environment variables set for one process, never printed.

## Out of scope

- The cloud runner (026), the cloud AI step (027), the cloud dev workspace (028).
- Scheduling the refresh (on demand only for now); sanitising CV text.
- A custom domain for the copies; paid plans; a Render Postgres.
- Anonymising anything but contact channels (decided in intent Q7).
- Postgres required in CI before it is shown stable (D3).

## Decisions to confirm

| # | Decision | Recommendation |
|---|----------|----------------|
| D1 | Branch names: `main` (pre-prod), `release` (prod), `dev` (testbed) | As written. |
| D2 | The testbed deploys from `dev` on every commit (not by hand) | Yes, so a cloud session's push shows up without a click. |
| D3 | The Postgres CI job is required only once it is green three pushes in a row | Yes: the suite has passed on both before (cycle 014), but a Linux runner has not been tried. |
| D4 | The two small app changes (banner, mail guard) are allowed | Yes. |
| D5 | The testbed project is renamed `saxobeat-testbed1` after the snapshot | Yes; the old name keeps saying "recovery copy", which it will no longer be. |

## Gate
- [ ] Owner approved this spec
