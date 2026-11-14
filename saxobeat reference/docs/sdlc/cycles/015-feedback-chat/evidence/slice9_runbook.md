# Slice 9 runbook: put the feedback chat on the hosted app

Prepared 2026-10-30. Nothing here has been done to the hosted app except one read-only count (below). The push is the owner's.

## What is true now (measured, not assumed)
| Fact | Evidence |
|---|---|
| The hosted database (prod1, Neon, Postgres 17.11) has 38 tables, 173,949 rows, **no `jobs_feedback` table**, and **58 rows in `django_migrations`** | `counts_prod1_before_push.json`, read 2026-10-30 (a few kilobytes, nothing written) |
| The code has 59 migrations; **0041 is the only one the host lacks** (`git diff --name-status origin/main..HEAD -- jobs/migrations` shows one added file) | checked 2026-10-30 |
| 0041 is one `CREATE TABLE`, its foreign key and three indexes; it alters no existing table, in a transaction | `migration_0041_postgres.sql` |
| The host runs `python manage.py migrate --noinput` before the web server starts (`scripts/entrypoint.sh`), and Render checks `/healthz` | `scripts/entrypoint.sh`, `render.yaml` |
| Local `main` is **12 commits ahead of `origin/main`**; 1,264 tests pass on SQLite and on local Postgres | `git log origin/main..HEAD`, `tests_after_*.txt` |

## What a push of `main` ships (all 12 commits, not only this cycle)
- **Cycle 015, the feedback chat** (slices 1 to 8): the button on every signed-in page for everyone, the console's Feedback page, the migration, the export and restore change, the French.
- **Cycle 001's code**, committed by another session: `jobs/ai/selection.py` (the AI pool no longer loads job texts), `jobs/services/ingest.py` (a run reads only the columns it needs), `scripts/pc_runner.ps1` (the full backup monthly instead of weekly), and its measuring scripts. These act on the PC runner's side; the hosted web does not run them, but they are deployed with the rest.
- **Documents** of cycles 001, 002, 004, 014, 015 (no effect on the app).

Not part of the push: anything outside `main`. If you would rather ship only the chat, or hold it, the commits can be moved to a branch first (say so; I would tell you the plan before moving anything).

## Before the push (owner, about five minutes)
1. **Decide**: ship now, with cycle 001's runner-side code in the same push? If not, stop here.
2. **Neon snapshot** (recommended, your account): take a manual snapshot of prod1 in the Neon console. Cycle 004 found that prod1 restores only about 6 hours back and that no dump of it exists. The migration is additive, so the risk is low, but the snapshot costs nothing.
3. **Say "commit the admin"**: `jobs/admin.py` and a test are changed but not committed (they add Feedback to the Django admin so a test chat can be deleted; without them there is no way to delete one from the screen). They must be committed before the push.
4. **Fresh counts right before you push** (the saved ones are from this morning and the app is live), in PowerShell from the repository folder:
```powershell
$line = Get-Content .env | Where-Object { $_ -match '^\s*SAXOBEAT_HOSTED_DATABASE_URL\s*=' } | Select-Object -First 1
$env:SAXOBEAT_HOSTED_DATABASE_URL = ($line -split '=', 2)[1].Trim().Trim('"').Trim("'")
uv run python scripts/db_counts.py SAXOBEAT_HOSTED_DATABASE_URL --save docs/sdlc/cycles/015-feedback-chat/evidence/counts_prod1_before_push2.json
Remove-Item Env:SAXOBEAT_HOSTED_DATABASE_URL
```
   (or tell me "about to push" and I take them; the address is never printed either way.) Expect: no `jobs_feedback`, `django_migrations 58`.

## The push (owner)
```bash
git push origin main
```
Render builds and starts the new version by itself. If the migration failed, the new container would exit before serving and Render would keep the old version running; the transaction would leave the database as it was.

## After the push (about ten minutes)
1. **Render's log** shows `Applying jobs.0041_feedback... OK` and then the server starting; the deploy turns "Live".
2. **Counts after** (same command, `--save ...counts_prod1_after_push.json`), then `uv run python scripts/db_counts.py --compare <before> <after>`. **Expected differences:** `jobs_feedback` appears with 0 rows; `django_migrations` goes 58 to 59. Tables the app uses all day (sessions, jobs, scores and so on) may have grown; **no table may have fewer rows than before**. A shrunk table is the alarm: stop and tell me.
3. **Look** at the real site (hard refresh; the service worker fetches the new CSS and script from the network first): the round button is bottom-right on a page, on a phone width too.
4. **Send one test idea** from your own account, then open the console's **Feedback** page: it is there with the count "1" in the nav, and **Copy as intent draft** gives a draft.
5. **Delete the test chat**: `/admin/jobs/feedback/` (after the admin commit), tick it, Delete. Counts: `jobs_feedback` back to 0.
6. **Tell me "deployed"** and I record the evidence, tick criterion 15 and take the "after" counts for you.

## Rollback
- **The button must go away fast:** revert the cycle's commits (or just the `base.html` block) and push. The button disappears at once. The empty table stays and harms nothing (`migrate jobs 0040` on the host would drop it; I would write that step with you if you want it).
- **A failed deploy:** nothing to undo; Render keeps the old version.
- **No data of yours is touched by this migration**, so there is nothing to restore; the Neon snapshot is a belt and braces.

## Not verified in advance
- That Render deploys this push the first time (cycle 004 saw Render skip one commit once; if the deploy does not start within a few minutes, look at Render's Events).
- The on-screen keyboard on a real phone (slice 10) and the clipboard paste of a draft (criterion 11).
- The French wording, which you have still to read (`french_to_read.md`).
