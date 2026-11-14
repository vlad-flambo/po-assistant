# Hosted dry run (plan slices 9 and 10, first half)

Read by the owner on **2026-11-03** from the console page `https://app.saxobeat.fr/ops/auto-reject/` after the push (owner's word, pasted into the chat):

> 17 applications already past 30 days are waiting to be moved at the next runner pass.

| What | Value | How we know |
|---|---|---|
| Push done, Render updated | yes | owner's word, 2026-11-03 (the exact Render log line `Applying jobs.0043_auto_reject... OK` was not quoted) |
| Migration 0043 applied on the host | yes, by inference | the page loaded: it reads `jobs_pipelinesettings` and runs the sweep's dry-run query on `auto_rejected_at`, which cannot work without both |
| Hosted dry-run count at the default delay of 30 days | **17** | the page's own line (the same dry run as `manage.py auto_reject --dry-run`) |
| Count on the 29 Oct dump as of 3 Nov | 17 | `evidence/applied_counts.md`, `evidence/rehearsal.md` |

The hosted count equals the dump's: inside the 17 to 40 range the runbook called plausible, and no surprise. About 22 more Applied jobs were within nine days of the 30-day mark on 3 Nov, so the number grows over the next days; the first real sweep moves whatever the count is at that moment.

Not yet known: whether the owner took counts before the push (`counts_prod1_before_push.json` is not in the folder), and Render's exact log line.
