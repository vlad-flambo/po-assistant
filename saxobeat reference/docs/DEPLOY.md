# Hosting Saxobeat (web on Render, database on Neon, sources read from your PC)

## The shape

```
  Your PC (residential address)                 Hosted (EU)
  ┌──────────────────────────────┐              ┌──────────────────────────────┐
  │ scripts/pc_runner.ps1         │  writes to   │ Postgres  <── web app         │
  │  run_sources (reads the sites)│ ───────────► │  (candidates log in here)     │
  │  purge_old_jobs, auto_reject, │              │  SAXOBEAT_RUN_SOURCES=0       │
  └──────────────────────────────┘              └──────────────────────────────┘
```

- The **web app** only shows data. It never fetches from the job sites (`SAXOBEAT_RUN_SOURCES=0`), so the sites never see a datacenter address and a hosted instance cannot be used to scrape. The Refresh, Run and radar-check buttons answer "sources are read from the operator's PC".
- The **PC** reads the sources on a schedule and writes into the hosted database, for every candidate (`services/matching.py` judges and scores each new job per person).
- The database is **Postgres everywhere** (development, tests, hosting). The app is one Docker image (`Dockerfile`), so it runs on any host that runs a Dockerfile.
- Accounts are **by invitation only**: the operator makes a link under *Operator → People* and sends it by hand. There is no email service.

## Which host

**Web on Render (free web service), database on Neon (free Postgres).** Koyeb was the first choice, but its free offer was reported discontinued after Mistral's acquisition (October 2026), so Render is the front end. The same image runs on any host that runs a Dockerfile, so another host stays possible later.

| | What it is | Cost | What you accept |
|---|---|---|---|
| **Render web service** | the app, from this repo (`render.yaml`), Frankfurt | Starter (about 7 USD a month, 512 MB, 0.5 CPU; from Render's pricing page: re-check). Since 28 October 2026 `render.yaml` says `plan: starter` | Starter **never sleeps**, so nobody waits for the image to start. The free plan slept after 15 minutes without a visit and woke in about a minute (the image starts and the migrations are checked); it still works if you set `plan: free` again. One worker with 4 threads (`WEB_CONCURRENCY=1`) is what 512 MB holds. |
| **Neon database** | Postgres 17, Frankfurt | free | 0.5 GB of storage (the app uses about 180 MB), 100 compute hours a month, and it suspends after 5 minutes idle (a few seconds to wake). **5 GB of network transfer per project per month, counted on data read out of the database** (Neon's docs say per project; the Projects page of the console shows only the sum of all projects, and a project's own figure is on its Overview page and in the API field `data_transfer_bytes`) (the web app's reads and the PC's reads alike; data sent in does not count). At the cap Neon suspends the compute until the next monthly period or an upgrade: the web app and the runner both stop, and no data is lost. |

`render.yaml` creates **no** database: the data stays on Neon. The caps that matter for the data are Neon's.

## One-time setup

You do the account steps yourself: accounts, passwords and connection strings are yours, and none of them goes in a chat.

### 1. The database on Neon (done 2026-10-22)

1. Create a Neon account and a project. **Pick Postgres 17** (the version the local database and the backup tools use) and an **EU region** (Frankfurt, `aws-eu-central-1`).
2. Open *Connect*, switch **Connection pooling off** and copy the connection string: its host has **no `-pooler`**, and it ends with `?sslmode=require`. The pooled address does not suit the app (it multiplexes connections between requests, which Django's persistent connections and the data copy do not expect).
3. It is a secret: it is the key to all the data. Keep it in `.env` and in Render's settings only.

### 2. Move your existing data up (once; done 2026-10-22)

In PowerShell, from the project folder, with the local database running (`docker compose up -d`):

```
uv run python manage.py backup_database --keep 14        # makes data\backups\saxobeat_<date>.dump from your local database (the newest file there is the one to use)
docker run --rm -v "${PWD}/data/backups:/b" postgres:17 pg_restore --clean --if-exists --no-owner -d "<the Neon connection string>" /b/saxobeat_<date>.dump
```

The restore puts your tables in Neon, including your account `vlad` and its password. Look at *Monitoring → Storage* in Neon afterwards. If `pg_restore` complains about the server version, the Neon project is not on Postgres 17: create it again with 17.

### 3. The web service on Render

1. **Push first.** Render builds from GitHub: everything you want live must be on `main`.
2. In Render: *New → Blueprint*, connect the GitHub account and pick `vlad-flambo/saxobeat` (branch `main`). `render.yaml` describes one **free** web service in Frankfurt (Docker, health check `/healthz`) and no database. Read the plan shown on the screen before you apply.
3. Render asks for the variables the blueprint leaves empty. Fill in:
   - `DATABASE_URL`: the Neon string from step 1 (no `-pooler`).
   - `DJANGO_SECRET_KEY`: a long random string. Make one on your PC: `uv run python -c "import secrets; print(secrets.token_urlsafe(50))"`. Keep it: changing it later logs everybody out and kills pending reset links.
   - `SAXOBEAT_ADMIN_USER` / `SAXOBEAT_ADMIN_PASSWORD`: a login for a second operator, created on first boot if it does not exist (your own `vlad` account is already in the database). A long password.
   - `DJANGO_DEBUG` (`0`), `SAXOBEAT_RUN_SOURCES` (`0`) and `WEB_CONCURRENCY` (`1`) are already set in `render.yaml`.
   If the first deploy fails because a value was left empty, add it under *Environment* on the service and deploy again.
4. Wait for the first deploy (a few minutes: the image builds, then `scripts/entrypoint.sh` applies the migrations). Render gives the address `https://<name>.onrender.com`; the app reads its own host name from Render, so no host setting is needed.
5. Open `/healthz` (it says `ok`), then log in as `vlad`: the Inbox should show your jobs.
6. Note the address: it is the one you give to people. A custom domain can be added later in Render's *Settings → Custom Domains*.

### 4. The PC runner

1. Put the Neon connection string in `.env` as `SAXOBEAT_HOSTED_DATABASE_URL=...` (`.env` is not committed).
2. Run `scripts/pc_runner.ps1` by hand once and check it ends without an error.
3. Start it by hand with `saxobeat-runner.cmd` (the one-click version of the script), or, to run on its own, create a Task Scheduler task that runs
   `powershell -NoProfile -ExecutionPolicy Bypass -File C:\path\to\saxobeat\scripts\pc_runner.ps1` every few hours.
   On a Mac: `saxobeat-runner.command` by hand, or `scripts/com.saxobeat.runner.plist` (launchd, every 3 hours; install commands in its header).
   It reads every due source into the hosted database, purges jobs nobody follows after 90 days, presumes rejected the applications nobody answered for more than the delay set in the console (*Auto-reject*, default 30 days, 0 switches it off; a few KB of reads; each is tagged and put back in one tap), and makes a full backup at most once a month (a copy reads about 227 MB; weekly did not fit 3 to 5 runs a week, see `docs/sdlc/cycles/001-local-db-replica`). The first connection after a pause wakes Neon, which takes a few seconds.

   *Status since 2026-10-29:* **no task is scheduled and the runner is started by hand**, a few times a week at most, while Neon's transfer cap is the constraint (see §5 and `docs/sdlc/cycles/001-local-db-replica`). Cycle 001 has now measured it: a run reads about 46 MB (63 MB before the 30 October change to the link lookup) and a full backup 227 MB once a month. It restarts by hand following `docs/sdlc/cycles/001-local-db-replica/evidence/restart_runbook.md`; schedule it again only when a week of Neon readings agrees with the projection.

### 5. Look before you invite anyone

- The Inbox after a quiet half hour: on Starter Render stays awake, but Neon's free compute still pauses after about 5 idle minutes, so the first page can take a few seconds more; then it is fast. Look at the second page load: under about two seconds.
- **Waking up:** once the app has been opened in a browser, a small service worker shows a "Waking up…" page while Render starts the service (it reloads by itself). The very first visit, before the worker exists, still waits for the host. The worker stores only the style, scripts and icons, never a page or personal data.
- Neon's *Storage* figure, and again after a few PC runs: it must stay under 0.5 GB. If it climbs, shorten the purge (`purge_old_jobs --days 60` in `pc_runner.ps1`).
- Neon's *Network transfer* (data read out of the database; 5 GB a month on the free plan). It is the cap that bites, not storage: in October 2026 it reached 84 % in six days, because each run read the job texts again for every candidate. Since 28 October a run reads only what it needs:
  - the employer "About us" check is counted by the database, which sends back numbers, not texts;
  - the text model's word counts are kept in `data\cache` between runs and brought up to date with the postings that came in;
  - the age rule is applied by one update, without reading the jobs;
  - the full backup (about 227 MB read, measured on 29 October) is monthly.
  Measured on a copy of the data: a day's matching went from about 150 MB to under 5 MB, plus about 17 MB for the first run, and again once a week, to count the words from scratch. That was the 28 October estimate (about 1.5 GB a month with weekly backups). Measured on 29 and 30 October, a run by hand is about 63 MB (a source pass 62, `ai sync` 0.1 once its cache is warm, mail 1; the 32 MB first recorded for `ai sync` was a cold cache plus one onboarding file), and about 46 MB since the 30 October change to the link lookup and a full backup 227 MB (`docs/sdlc/cycles/001-local-db-replica/evidence/`); the backup is now monthly, and a new candidate adds little. Scoring every job again for one person (after a tuned search, about 50 MB for a broad search) is the largest one-off.
- **What actually happened (29 October 2026):** the first Neon project passed 4.5 GB of its 5 GB within days of 22 October. The estimate above came before measurement. The likely causes: about ten full runs by hand before the fix (about 150 MB each), four or five full backups (about 200 MB each) and several `ai sync` runs. Those add up to about 3 GB at most; the other 1.5 GB or so is unexplained (the web app's own reads are a suspect, but it was only judged from the last 24 hours of the dashboard). At the cap the compute would have been suspended until the next period, so the data was moved to a fresh project (§8). The reads are still to be measured after the fix: **`docs/sdlc/cycles/001-local-db-replica`**. Neon's *Network transfer* shows only the last 24 hours in the dashboard: write the figure down when you look.

### 6. Invite people

*Console → Candidates → Make an invitation*: with their address and "e-mail it" ticked, the invitation goes by e-mail (once e-mail is set up, §7); the link is shown too, to send yourself. They create their account (email + password), then fill in their CV and settings.

**For a group, make an invitation code instead** (cycle 033, live since 2026-11-06): *Console → Candidates → Invitation codes → Make a code* ("Skaleet"). Its link, `https://app.saxobeat.fr/signup/?code=Skaleet`, opens the sign-up page with the code filled in; anyone who types the code there can sign up, many people, no end date. *Switch off* on the code stops new sign-ups through it at once and touches no existing account: it is the brake if a link spreads further than intended. Every candidate also has one code of their own (*More → Inviter des amis*), which you can switch off from their row. **What a sign-up costs:** about 8 MB of Neon storage (30,675 job views on the 29 Oct catalogue) and about a minute of background work on the web server; Neon's 0.5 GB holds about 40 such accounts beyond what the app uses (re-read the Storage figure first).

### 7. E-mail (Brevo) and the app's own address

The app sends e-mail through Brevo's HTTPS API (Render blocks or restricts SMTP): invitations, a welcome, self-service password resets, "password changed", "your AI results are ready" and a weekly digest (docs/PRD_users_and_emails.md §7). Until it is set up, nothing is sent and the console's *E-mails* page says so.

**Done 2026-10-30 to 2026-11-03 (cycle 003, [`docs/sdlc/cycles/003-email-live`](sdlc/cycles/003-email-live/verify.md)):** the app is on `https://app.saxobeat.fr`, e-mail goes out through Brevo from `Saxobeat <no-reply@mail.saxobeat.fr>`, candidate e-mails (AI-ready, digest) are **paused** in the console, and account e-mails go. What was tried: a test e-mail landed in Gmail's inbox and in iCloud's **spam** (a days-old sending domain has no reputation yet). **Not tried yet:** Outlook, a real invitation, and a reset e-mail made on the host. The steps below are what was done, in order; the domains are the ones in use.

1. **The app's address.** At your DNS host for `saxobeat.fr` (IONOS), add a CNAME `app` → the Render service's `onrender.com` name. In Render: *Settings → Custom Domains → Add* `app.saxobeat.fr` and wait for the certificate. Put the host in `DJANGO_ALLOWED_HOSTS` and `https://app.saxobeat.fr` in `DJANGO_CSRF_TRUSTED_ORIGINS` (`render.yaml` lists them; the live values are Render's own settings). A missing host gives a plain 400 "Bad Request" on every page; a missing origin gives a 403 only when a form is submitted.
2. **A Brevo account** (free: 300 e-mails a day, API included). *Senders, domains → Domains → Add* `mail.saxobeat.fr`. Brevo shows the records to add at your DNS host: the DKIM CNAMEs (`brevo1` and `brevo2._domainkey.saxobeat.fr`), the `mail` CNAME that carries the SPF and return-path, a Brevo code, and its own DMARC record on the root (`p=none`, reports to Brevo; kept as it is). Wait until Brevo says the domain is authenticated. **Set up the sender** (`no-reply@mail.saxobeat.fr`) in Brevo too: the first test went nowhere until the sender was fixed there. Then *SMTP & API → API keys → Generate*: it is a secret, keep it in Render's settings and `.env` only. **Authorised IPs:** Brevo refuses API calls from an address not on its list (error 401 "unrecognised IP address"). Render's outbound address is shared and can change, so the one in use (`74.220.51.142` on 2026-10-30) was allowed and the protection left on (cycle 003 D3): **if e-mails start to fail with that 401, add the new address shown in the error, or switch the protection off.** The PC is not on the list, so `manage.py mail send` from the PC would fail the same way.
3. **Render → the service → Environment** (five settings): `SAXOBEAT_MAIL=brevo`, `BREVO_API_KEY=<the key>`, `SAXOBEAT_MAIL_FROM=Saxobeat <no-reply@mail.saxobeat.fr>`, `SAXOBEAT_PUBLIC_URL=https://app.saxobeat.fr`, `SAXOBEAT_MAIL_REPLY_TO=<your address>` (replies reach you; the sender itself cannot receive mail). The sender is also the code's default now; set it anyway so a deploy never depends on the default.
4. **The PC's `.env`**, the same lines: the runner sends the AI-ready e-mails and digests (`manage.py mail send` after `ai sync`), and its links must point to the public address, not to localhost. Only needed once candidate e-mails are unpaused (see the IP note in step 2).
5. **Check:** *Console → E-mails → Send a test* (or `uv run python manage.py mail test <your address>` from the PC, which hits the IP rule). The page's first line must read "provider brevo · from Saxobeat <no-reply@mail.saxobeat.fr> · links to https://app.saxobeat.fr". Look at the test in Gmail and in Outlook: in the inbox, not spam, and in the message details SPF, DKIM and DMARC pass. If it lands in spam, mark it "Not junk" and keep volume small for the first weeks. Only then invite anybody with "e-mail it" ticked.
6. **Switch it off in an emergency:** set `SAXOBEAT_MAIL=off` on Render (and in `.env`): every e-mail then ends *skipped* and nothing leaves. Revoking the API key in Brevo stops sending at once. To stop only the candidate e-mails, use the pause switch on the console's *E-mails* page.
7. **A tighter DMARC later:** Brevo's record sits on the root (`_dmarc.saxobeat.fr`), which also covers the owner's own IONOS mailbox. When the policy is tightened (`quarantine`), put the stricter record on `_dmarc.mail.saxobeat.fr` only.

The console's *E-mails* page shows every e-mail (kind, address, state, error), today's count against the 300 a day, *Send now*, a test, a retry for failures, and a switch that pauses the candidate e-mails (account e-mails always go).

### 8. Changing the Neon project (done once, 2026-10-29)

The 5 GB of transfer is **per project**, so moving the data to a new project starts a new allowance. It buys time; it does not reduce reads. What exists now:

| Project | Role | State |
|---|---|---|
| `saxobeat-prod1` | the live database | read and written by Render and by the PC (`.env`: `SAXOBEAT_HOSTED_DATABASE_URL`; Render: `DATABASE_URL`) |
| `saxobeat-fallback1` | the old project, the recovery copy | a snapshot of 2026-10-29 10:05; nothing reads or writes it. `.env`: `SAXOBEAT_FALLBACK_DATABASE_URL` (used by `scripts/db_counts.py` and for a rollback) |

**Rollback:** set Render's `DATABASE_URL` and `.env`'s `SAXOBEAT_HOSTED_DATABASE_URL` back to the fallback's string. The fallback is then as old as the snapshot: anything written to prod1 since is not in it. **And it has little room:** on 2026-10-29 its page showed "You've used 95.1%" of its 5 GB, so only about 0.245 GB of transfer was left until its next monthly period. **Neon's counters reset on the 1st of every month** (owner, 2 November 2026: every counter showed 0 that morning; the October figures were not kept), so since 1 November the fallback has its full 5 GB again; it is still as old as its 29 October snapshot, and a rollback means running on it with the same 5 GB allowance. Treat the fallback mostly as a snapshot of the data.

**The same move again** (the recipe that was run; the full log is in `docs/sdlc/cycles/002-fresh-neon-project`):

1. Create the new project: Postgres 17, Frankfurt, pooling off (no `-pooler` in the host). Put its string in `.env` under a variable name only; the strings never go in a chat, a ticket or the repo.
2. Take a dump from the old project (`manage.py backup_database`; about 200 MB read) and count the rows of every table: `uv run python scripts/db_counts.py <ENV_VAR> --save counts_old.json` (the address is read from the named environment variable and never printed; the counts cost a few KB).
3. **Rehearse on the local Docker** first: restore the dump into a scratch database (`create database restore_test`, `pg_restore ... -d restore_test`), count it, compare with `--compare`, drop it. This costs nothing on Neon.
4. Make sure the target is empty: `db_counts.py <ENV_VAR> --expect-empty` (exit 2 if it has tables: `--clean` would drop them).
5. Restore into the new project, **leaving out the dump's `DEFAULT ACL` entries**. They grant privileges to Neon's own roles (`cloud_admin`, `neon_superuser`) and fail on a server that lacks them; filter the table of contents so the restore exits 0:
   ```
   docker run --rm -e SAXOBEAT_RESTORE_URL -v "${PWD}\data\backups:/b:ro" postgres:17 sh -c 'pg_restore -l /b/<file>.dump | grep -v DEFAULT.ACL > /tmp/list.txt && pg_restore --no-owner --clean --if-exists -L /tmp/list.txt -d "$SAXOBEAT_RESTORE_URL" /b/<file>.dump'
   ```
   (`SAXOBEAT_RESTORE_URL` is set from `.env` in the PowerShell session. It is passed to Docker by name, so it never appears on a command line. The `grep` pattern has no quotes on purpose: quotes get lost on the way into Docker.)
6. Count the new project and compare with the old counts: every table must match. Check in Neon that the restore did not count as transfer.
7. Switch Render's `DATABASE_URL`, wait for the deploy, then prove the app writes to the new project: log in, then compare `max(last_login)` in both databases. (`/healthz` says `ok` from the old deploy too; and counting `django_session` rows does not work, because a login from an existing session replaces its row.)
8. In `.env`, make `SAXOBEAT_HOSTED_DATABASE_URL` the new string and keep the old one as `SAXOBEAT_FALLBACK_DATABASE_URL`; `saxobeat-runner.cmd check` should pass.

### If Render changes its terms, or you want more

The service is on Starter already (no sleeping); a bigger plan allows more workers (`WEB_CONCURRENCY`). Or point another Docker host at the same Neon database with the same variables: nothing is copied. To use a Render database instead of Neon, add a `databases:` block and `fromDatabase` for `DATABASE_URL` to `render.yaml`, restore a backup into it (`pg_restore --clean --if-exists --no-owner -d "<url>" <file>`) and point `SAXOBEAT_HOSTED_DATABASE_URL` in `.env` at it.

## Rescoring after a change to the scoring rules
Stored scores change only when postings are scored again. After a change to the scoring (for example the bilingual glossary, cycle 021): take a Neon snapshot, then, from the repository folder, with the hosted address set for one process only (see `docs/sdlc/cycles/021-bilingual-keyword-scoring/evidence/slice10_11_runbook.md` for the PowerShell lines):

- `uv run python manage.py rescore_preview [--candidate N] [--limit N]` reads, writes nothing, and says how many inbox jobs would cross the inbox floor each way, how many of those moves are the glossary's alone, and how much posting text it read. **Its first line says which database it read** (`on a remote server` is the hosted one).
- `uv run python manage.py rescore [--candidate N]` scores each candidate's inbox again (status new, not hidden; AI reviews are kept). A job in the pipeline keeps its stored score.
- `SAXOBEAT_GLOSSARY=0` in the host's environment switches the bilingual glossary off; rescore again to restore the previous scores. A rescore reads every inbox posting's text (about 5.5 KB each: 16.6 MB for 2,980 jobs); say the figure before a big run (Neon's allowance resets on the 1st).

## Accounts

- **Sign-up:** through an invitation link (single use, expires after 14 days) or an invitation code typed on `/signup/` (many uses, switched on or off by the operator; cycle 033). The email is the login. Each account records where it came from (a code, an invitation link, or "before codes"), shown on *People*.
- **Wrong codes and floods:** ten wrong codes from one address within 15 minutes lock `/signup/` for that address (stored in `FailedLogin` under the name `signup-code`; the login lock ignores these rows). A brake allows at most 3 sign-ups per address and 20 in all per hour (`SIGNUPS_PER_ADDRESS`, `SIGNUPS_IN_ALL` in `jobs/accounts.py`): 20 an hour would be about 160 MB, so lower the second one if a link spreads. An office behind one address shares the limit of 3.
- **Wrong passwords:** five wrong tries on one account, or twenty from one address, lock the login for 15 minutes (stored in the database, so it holds across workers and restarts).
- **Forgot the password:** *Forgot your password?* on the login page e-mails a link (at most 3 an hour per address, 10 per network address; the page never says whether an account exists). The operator can still make one by hand: *Console → Candidates → Reset link*. A link made by hand lasts three days and works once; a link that was **e-mailed** lasts **one hour** and works once (cycle 003); changing the password e-mails the account.
- **Switch off / delete:** the operator can switch an account off (data kept) or delete it with all its data. A candidate can delete their own account and data from *Settings* (and download a copy first). Deleting takes seconds whatever the size of the account (cycle 032, 2026-11-06: one DELETE per table, in one transaction; a 36,271-job account was deleted on the host quickly (the owner's word, not timed), where the old row-by-row cascade ran past the web server's 120 s and rolled back). If it fails, nothing is deleted and the console says "Nothing was deleted"; the cause is in the Render log. A model added later that hangs off a candidate or a job must be added to the lists in `jobs/accounts.py` (a test names it).

## Backups and restore

- `manage.py backup_database` writes a full copy (`pg_dump`, via Docker when `pg_dump` is not installed) to `data/backups/`, keeping the latest 14. The PC runner calls it at most once a month (`--min-age-hours 720`, the last 6 kept; decided in cycle 001 because weekly does not fit 3 to 5 runs a week) because each full copy reads about 227 MB from Neon, which counts against the transfer cap; you hold a copy **off the host**, taken through the hosted address. The Docker route uses `postgres:17` tools: they refuse a server on a newer Postgres, which is one more reason to create the Neon project on 17.
- **Restore** into an empty database: `pg_restore --clean --if-exists --no-owner -d "<url>" <file>`. Try it once on a scratch database before you need it:
  ```
  docker compose exec -T db psql -U saxobeat -d postgres -c "create database restore_test"
  docker compose exec -T db pg_restore -U saxobeat -d restore_test --no-owner < data/backups/<file>.dump
  ```
- A dump taken from Neon carries two `DEFAULT ACL` entries for Neon's own roles. Restoring it into a plain Postgres (the local Docker) prints two harmless errors about the role `neon_superuser` and exits 1; leave those entries out as in §8 step 5 to get a clean exit code.
- Neon's free plan keeps only a short history for point-in-time restore (check the length in its dashboard), and Render's database backups (if you ever use one) depend on the plan. A personal copy is still the one you control.
- Each person's own data can also be exported from *Settings → Download my data* (a JSON file; the operator's *Data & backups* page imports it).

## The AI folder on the PC

The PC runner also moves the AI files (see [PRD_ai_backoffice.md](PRD_ai_backoffice.md)). Its last step, `manage.py ai sync`, writes the files that are due into **`Saxobeat AI	o-do`** in your home folder (change it with `SAXOBEAT_AI_DIR` in `.env`; keep it outside the repository and outside any synced folder) and imports the `*_results.json` files an agent leaves next to them. It reads and writes the hosted database directly, like the rest of the runner: no new address, token or endpoint.

- **Your part:** point any agent at the `to-do` folder ("process every file in this folder"), or hand it the files one by one. Nothing has to be installed on the agent's side: each file holds the instructions.
- **`saxobeat-ai.cmd`** does only this step, in seconds (`saxobeat-ai.cmd open` also opens the folder). `STATUS.txt` in the folder says what is waiting, imported, held back or late; the console's *AI → Import* page shows the same after each sync (and the AI status strip shows the last sync time).
- A results file with any refused result is held back whole in `problems\` with a `.txt` saying why, and nothing from it is imported. Fix it, or upload it on the console's Import page to see the preview and import it yourself.
- Imported files go to `done\` and are deleted after 7 days. CVs travel in these files (contact details removed): delete what you do not need and do not sync the folder.

## Security notes (the instance is public)

- Every page needs a login except: the login page, `/join/<invitation>/`, password-reset links, `/healthz`, and the capture bookmark (which carries a per-person secret).
- Operator pages (everything under `/ops/`: sources, runs, radar, AI, data, people) answer "not found" to candidates. The Django admin needs a staff login.
- Secrets live only in Render's settings (Render) and your PC's `.env`, never in the database or the repo. Nothing in the app asks a candidate for a key or a password other than their own.
- The Neon connection string gives access to everything: never paste it in a chat, a ticket or the repo. If it leaks, reset the role's password in Neon and update Render and `.env`. The old project's string (`SAXOBEAT_FALLBACK_DATABASE_URL`) is just as sensitive: it holds the 29 October snapshot of everything.
- CVs are personal data. The operator can see them (say so to the people you invite). Both hosts here are in an EU region; every account can be deleted.

## Verified on the host (2026-10-29)

Checked by the owner on the live app, recorded in `docs/sdlc/cycles/004-hosted-checks/verify.md`:
- **Deploys and migrations:** the 28 October deploys (`4fa860f`, `ff08c0c`) applied migrations `0037` to `0040`; a push to `main` deploys by itself (`d1718a0`, 29 October 15:53). The web service runs on Render Starter against Neon's `saxobeat-prod1`; the PC's runner writes to the same database (cycles 001 and 002).
- **Data and accounts:** the blocks migration 0039 made from the old "Blocked companies" lists are right; friends are in Standard mode and the operator in Power; *View as* works and is listed in the console.
- **Speed:** the candidate pages and the console's Today and Candidates pages felt fast to the owner, as himself and viewing as a friend (judged, not timed).
- **AI hand-off:** eight packs ran with a real agent between 23 and 28 October, from the runner and by command: 257 of 258 tasks came back done.
- **Recovery:** Neon restores `saxobeat-prod1` to any point in the **last 6 hours**, and keeps **manual snapshots**. The PC's newest dump is the old project's (29 October, 10:06): there is no dump of prod1 until the monthly backup runs, so take a manual snapshot in Neon before any risky change.

**Still not verified:** e-mail (switched off until Brevo and the DNS are set, cycle 003), real phones (cycle 005), page times as figures, and the free-tier limits above, which come from the providers' pages.
