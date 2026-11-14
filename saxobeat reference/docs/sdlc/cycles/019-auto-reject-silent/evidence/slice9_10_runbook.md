# Slices 9 and 10 runbook: put auto-reject on the hosted app, then the first sweep

Prepared 2026-11-03. **Nothing here has been done to the hosted app.** Every step below is yours; I touch no hosted database. Commit `a1b74a1` holds the cycle (local, not pushed).

## What is true now
| Fact | Evidence |
|---|---|
| The only new migration is `0043_auto_reject`: one nullable `timestamptz` column on `jobs_candidatejob` and one tiny table `jobs_pipelinesettings`; no existing data is rewritten | `jobs/migrations/0043_auto_reject.py`; applied on a Postgres copy (`evidence/rehearsal.md`, 32 KB sent) |
| The host runs `python manage.py migrate --noinput` before it starts the web server | `scripts/entrypoint.sh` |
| A push carries **3 commits**: `a1b74a1` (this cycle), `a98e460` (the ai-sdlc skill made project-independent) and `254c964` (the `saxobeat-add-employer` skill). The two others are skill files and have no effect on the app | `git log --oneline origin/main..HEAD` after `git fetch`, 2026-11-03 |
| On the 29 Oct dump the sweep would move **17** (SQL count = dry run = sweep); the host is newer, and about 22 more applications were within 9 days of the 30-day mark on 3 Nov, so the hosted count can be higher | `evidence/applied_counts.md`, `evidence/rehearsal.md` |
| Nothing sweeps until **you** run the command or the runner: the web app never calls the sweep | `jobs/services/auto_reject.py` is called only by `manage.py auto_reject` |

## Before the push
1. **Neon snapshot of prod1** (your account: the Neon console, take a manual snapshot). prod1 restores only about 6 hours back and no dump of it exists (cycle 004).
2. **Counts before** (optional but they make slice 10's comparison exact), in PowerShell from the repository folder:
```powershell
$line = Get-Content .env | Where-Object { $_ -match '^\s*SAXOBEAT_HOSTED_DATABASE_URL\s*=' } | Select-Object -First 1
$env:SAXOBEAT_HOSTED_DATABASE_URL = ($line -split '=', 2)[1].Trim().Trim('"').Trim("'")
uv run python scripts/db_counts.py SAXOBEAT_HOSTED_DATABASE_URL --save docs/sdlc/cycles/019-auto-reject-silent/evidence/counts_prod1_before_push.json
Remove-Item Env:SAXOBEAT_HOSTED_DATABASE_URL
```
   The address is never printed. Expect no `jobs_pipelinesettings` table. (Or say "about to push" and I take them.)
3. **Do not start `saxobeat-runner.cmd` or `pc_runner.ps1`** (nor `ai sync`, `mail send` or any command against the hosted database) from this tree until step 2 of "After the push" below is true: the code selects the new column and would fail on the host.

## The push
```bash
git push origin main
```
Render builds, runs the migration, then starts. If the migration failed the new container would exit before serving and Render would keep the old version.

## After the push
1. Render shows **Live** on the new commit and its log has `Applying jobs.0043_auto_reject... OK`. (cycle 004: Render once skipped a commit; if nothing starts within a few minutes, look at Render's Events.)
2. **Open the console page** `https://app.saxobeat.fr/ops/auto-reject/` (signed in as the operator). **If it loads, the migration is applied**: the page reads the new table and runs the sweep's dry-run read on the new column, which can only work with both in place. The page also tells you **how many applications are already past the delay**: that number is the hosted dry-run count (read only, one query; the first visit creates the one settings row, default 30).
3. Write that number down (or tell me).

## Slice 10: the first sweep
**Decide on the number.** Plausible: about 17 to 40. If it is above 60, or does not look like the applications you know are older than a month, **stop and tell me**; to be safe in the meantime, set the delay to **0** on that page and Save (nothing can then move).

If it looks right, run **only the sweep** (about 15 KB of reads, no source pass), by hand:
```powershell
$line = Get-Content .env | Where-Object { $_ -match '^\s*SAXOBEAT_HOSTED_DATABASE_URL\s*=' } | Select-Object -First 1
$env:SAXOBEAT_HOSTED_DATABASE_URL = ($line -split '=', 2)[1].Trim().Trim('"').Trim("'")
$env:DATABASE_URL = $env:SAXOBEAT_HOSTED_DATABASE_URL
$env:SAXOBEAT_MAIL = "off"          # .env has a live mail key; this command sends nothing, this makes sure
uv run python scripts/db_counts.py SAXOBEAT_HOSTED_DATABASE_URL --save docs/sdlc/cycles/019-auto-reject-silent/evidence/counts_prod1_before_sweep.json
uv run python manage.py auto_reject --dry-run     # the same number as the page; writes nothing
uv run python manage.py auto_reject               # the first real sweep
uv run python scripts/db_counts.py SAXOBEAT_HOSTED_DATABASE_URL --save docs/sdlc/cycles/019-auto-reject-silent/evidence/counts_prod1_after_sweep.json
uv run python scripts/db_counts.py --compare docs/sdlc/cycles/019-auto-reject-silent/evidence/counts_prod1_before_sweep.json docs/sdlc/cycles/019-auto-reject-silent/evidence/counts_prod1_after_sweep.json
Remove-Item Env:DATABASE_URL, Env:SAXOBEAT_HOSTED_DATABASE_URL, Env:SAXOBEAT_MAIL
```
**Expected differences:** `jobs_statuschange` grows by exactly the number moved; every other table you did not use meanwhile is unchanged (`jobs_candidatejob` keeps its row count: statuses change, rows do not). The dry run's number, the sweep's "moved N" and the history growth must be the same N. The runner's own next pass will also run this step (it moves 0 when nothing new is due).

## Slice 11: look at it (about ten minutes, your own account on the host)
1. **Pipeline** page: the banner "N applications with no answer were presumed rejected by the app in the last 7 days", the **Rejected** column with the "Auto-rejected" tag on those cards (not on the ones you rejected yourself).
2. **Open one**: the tag next to the score, the box "On <date> the app moved this application from Applied to Rejected: there was no answer after 30 days…", the history line in words.
3. **Press "Put back to Applied" on one**: it is Applied again, the tag and the box are gone, the follow-up date is set; the banner count goes down by one.
4. **Insights**: "No answer, presumed rejected: N" under "How long answers take", and a "No answer" box in the diagram; the rejection figures did not include them.
5. **French** (language switch): the same texts in French.
6. **Console**: the delay field saves (try 31, then 30 again); a non-operator account gets a 404 on the page.
Then tell me "deployed and checked" (or what looked wrong) and I write `verify.md` row by row.

## Rollback
- **Stop it moving anything, at once:** set the delay to **0** in the console. Jobs already tagged keep the tag and their put-back button.
- **Undo the first sweep for one job:** "Put back to Applied" on its page. For all of them at once I write and rehearse on a copy a one-off script (the sweep's rows are exactly those with `auto_rejected_at` set and a history line "auto: no answer after N days"); say so if you need it.
- **Take the feature out:** revert `a1b74a1` and push. The column and the table stay and harm nothing; the code that reads them goes.
- **A failed deploy:** nothing to undo; Render keeps the old version. The Neon snapshot is the belt and braces.

## Not verified in advance
- That Render deploys this push the first time, and the exact text of its log line.
- The hosted number and what the hosted applications look like (the dump is from 29 Oct).
- The look of the pages on your real phone (checked here at 375 px in a browser, not on a device).
- The French wording, which you have still to read (the strings are listed in `locale/fr/LC_MESSAGES/django.po`: search "présum" and "Refus présumé").
