# Restarting the runner on prod1 (cycle 001, slice 10)

Written 2026-10-30 at the owner's request ("restart the runners asap"). The owner starts the runner by hand, as before; nothing here schedules it.

## Why it is safe to start now
| Check | State |
|---|---|
| The reads that cost most are reduced and live | The slim link lookup and the cheaper inbox are in `8acf7f8`, deployed by Render on 2026-10-30 (about 10:55) |
| The runner fits the Neon cap | With the monthly backup, **about 830 to 1,250 MB a month** at 3 to 5 runs a week, before the web app; prod1's whole allowance is 5,000 MB and it has used about 135 MB ([projection.md](projection.md)) |
| No e-mail can leave | `SAXOBEAT_MAIL` is not set in `.env` and there is no mail key, so the provider is off (cycle 003 turns it on). `mail send` only queues |
| The backup will not run by surprise | The newest file in `data\backups` is `saxobeat_2026-10-29_100546.dump`, so the 30-day gate lets the first one through on or after **2026-11-28** |
| A way back exists | Neon restores prod1 only about 6 hours back, plus manual snapshots; `saxobeat-fallback1` is the 29 Oct state. A run writes ordinary new postings and scores; cycle 014 closed the overwrite windows |

## What to expect (the first run since 29 October)
- The first line says **"Using the hosted database."** If it says "No hosted address in .env: using the local database.", stop.
- `run_sources`: nearly every source is due, so about **25 to 40 minutes**; Esker (teamtailor) reports an error, as before.
- `purge_old_jobs`: nothing to purge (no job is older than 90 days yet).
- `backup_database`: skips (not due).
- `ai_sync`: writes the files for the agents into the "Saxobeat AI" folder if tasks are waiting.
- `mail`: "0 sent".
- **Expected Neon transfer for the whole run: about 60 to 90 MB**: a source pass about 45 to 60 MB (the slim lookup is in), the word-count sample counted in full **once** (about 17 MB, because the cache in `data\cache` was built against another database), `ai sync` about 0.1 MB, mail about 1 MB.

## Steps (owner)
1. **Before:** read Neon's Network transfer (the sum, two decimals) and the old project's percentage (95.1 % expected), and note the time. Optionally take a manual Neon snapshot of prod1 first.
2. **Check first, no reads:** `saxobeat-runner.cmd check` only checks that everything is in place (nothing is read, nothing is written). Then **run once** with `saxobeat-runner.cmd` (or `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\pc_runner.ps1`). Do not run it in parallel with anything else.
3. **After:** read the same two numbers right after it ends, and once more about an hour later (the dashboard can lag). Send me the three readings with their times and the runner's last lines.
4. **Then:** 3 to 5 runs a week, by hand, as you planned. Do **not** schedule it yet.

## Stop rules
- The run fails with an error: do not run it again more than once; send me the output.
- A single run moves the sum by **more than 0.20 GB**: stop, do not run again, send the numbers. The projection is wrong and the cycle goes back to the plan.
- Anything that looks like e-mail being sent: stop.

## Optional, recommended: a dump of prod1 itself
Only a 6-hour restore window and a manual snapshot protect prod1 (cycle 004's finding). After the first successful run, one manual `uv run python manage.py backup_database` costs about **227 MB** (4.5 % of the allowance), gives the first dump of prod1 and, because the gate reads the newest file, moves the monthly clock to a month from then. Your call.

## What I do with the readings
The first run's delta is the first real measurement of a whole run on prod1 (criterion 9's runner part); the daily readings give the web rate. I record both in [projection.md](projection.md) and [verify.md](../verify.md).
