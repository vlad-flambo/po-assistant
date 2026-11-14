# Slices 10 and 11 runbook: put bilingual scoring on the hosted app, then the rescore

Prepared 2026-11-04. **Nothing here has been done to the hosted app.** Every step below is yours; I touch no hosted database. The cycle is committed locally (`81f6e6d`, `1e98d31`, `1376e64`, and the `rescore` command added after them, see `git log`), not pushed.

## What is true now
| Fact | Evidence |
|---|---|
| **No migration.** The push changes code and the French catalogue only | `git diff --stat` of the cycle's commits has no `jobs/migrations/` file |
| **The push alone changes no stored score.** Scores change only when postings are scored again: a rescore, or the runner scoring new and changed postings (those new ones are scored with the new rules at once) | `jobs/services/matching.py` (`rescore`, `score_views`); nothing at startup rescores |
| The job page "found as" and the glossary work from the first request after the push, but the stored scores and lists on it are the old ones until the rescore | `scoring.found_as` reads the stored matched keywords |
| `SAXOBEAT_GLOSSARY=0` in the host's environment switches the glossary off (then rescore again to get today's scores back) | `config/settings.py` |
| Two commands are new: `manage.py rescore_preview` (writes nothing) and `manage.py rescore [--candidate N]` (writes the deterministic scores of each inbox job, keeping AI reviews) | `jobs/management/commands/` |
| What a rescore reads: the posting text of each candidate's inbox (status new, not hidden). On the 29 Oct dump that was about 3,000 jobs for C-01 (about 20 MB); the preview prints the exact figure first | `tests/test_rescore_preview.py`; the preview's `MB of posting text` line |

## Slice 10: the push (yours)
1. Read `git log --oneline origin/main..HEAD` after `git fetch`: the push carries other cycles' commits too. Mine are the ones starting "Cycle 021".
2. `git push origin main`. Render builds and starts (no migration to apply).
3. Check the job page of job 33238 still opens: https://app.saxobeat.fr/job/33238/ (still shows 33 until the rescore).

## Slice 11: the rescore (yours, after a Neon snapshot)
1. **Neon snapshot of prod1** (manual, your account; prod1 restores only about 6 hours back).
2. **Look first, change nothing.** In PowerShell from the repository folder, with the hosted address set for this one process only (the address is never printed):
```powershell
$line = Get-Content .env | Where-Object { $_ -match '^\s*SAXOBEAT_HOSTED_DATABASE_URL\s*=' } | Select-Object -First 1
$env:DATABASE_URL = ($line -split '=', 2)[1].Trim().Trim('"').Trim("'")
$env:SAXOBEAT_MAIL = "console"
uv run python manage.py rescore_preview --limit 200
Remove-Item Env:DATABASE_URL
```
   **Run all the lines together, in the same PowerShell window.** The first line printed by the command tells you where it read: it must say `on a remote server` (the hosted database). `on this PC` means `DATABASE_URL` was not set and it read the local Docker database (which is behind the code and fails with "WITHIN GROUP is required": nothing read from the host, nothing written; this happened once on 2026-11-04).
   `--limit 200` reads only each candidate's 200 newest inbox jobs (a few MB): it shows the kind of moves and the MB per job. Multiply the MB by the inbox size to know what the full preview and the rescore will read (each reads the same texts; the preview reads them twice, glossary off and on, in memory). Neon's allowance resets on the 1st: **say the figure out loud before the full run** (cycle 001/002 rule).
3. **Full preview** (same lines, without `--limit`), then write its output to `evidence/hosted_preview.md` (or paste it to me). Check: the numbers look like the replay (for C-01 about a quarter to a third of the French inbox jobs rise above the floor, almost none fall), and `Nothing was written.` ends it.
4. **The rescore**, one candidate first (yours is candidate 1):
```powershell
uv run python manage.py rescore --candidate 1
```
   then open the inbox and job 33238 (it should now read about 50 with "found as" words), then the others: `uv run python manage.py rescore`. Do not run the PC runner from this tree against the hosted database at the same time (it would score too).
5. **To go back:** set `SAXOBEAT_GLOSSARY=0` in Render's environment (redeploys) and run `rescore` again; or restore the Neon snapshot.

## Stop conditions
- The preview says more than a few hundred jobs **fall** below the floor: stop and tell me (the replay had none).
- The preview's volume does not fit what you want to spend: run it for one candidate (`--candidate 1`) or not at all and rescore only yours.
- Anything that prints an error: stop; nothing is written by the preview.
