# The first runner run on prod1 (slice 10), 2026-10-30

Started by the owner by hand with `saxobeat-runner.cmd` after the reading of about 11:39 (sum 4.9 GB, one decimal). It ended about 12:21 (the AI files are stamped 12:21:03), so it took about **35 to 40 minutes**. Log pasted by the owner; the parts that matter:

```
Using the hosted database.
...  (about 325 sources, every one "ok" except Esker)
Esker (teamtailor): error, fetched=0 new=0   (404 Not Found for https://eskerinc.teamtailor.com/jobs.rss)
Deleted 0 job(s) not listed for 90 days (with their views, scores and links: 0 rows).
The newest backup (saxobeat_2026-10-29_100546.dump) is recent enough: nothing to do.
AI: 4 files to do (Job screening, Onboarding), 0 results imported, 1 problem, 1 task late
  wrote 2026-10-30_122103_saxobeat_onboarding.md
  wrote 2026-10-30_122103_saxobeat_job_screening.md
  held back 2026-10-23_213434_saxobeat_job_screening_results.json: The file cannot be used: this export is not known here: 'E-20261023-213434'
E-mail: 0 AI-ready and 0 digest(s) decided, 0 sent.
Done: the hosted database is up to date.
```

## Against the runbook
| Expectation | Result |
|---|---|
| First line "Using the hosted database." | yes |
| Every due source read; Esker errors as before | yes: one error, Esker |
| Purge: nothing | yes (0 jobs) |
| Backup skipped (not due) | yes: "recent enough: nothing to do" |
| No e-mail | yes: "0 sent" |
| `ai sync` writes files | yes: two files into `C:\Users\Vladimir Stoyanov\Saxobeat AI\to-do` (onboarding, job screening) |
| No stop rule hit | none hit on the log; the Neon delta (the 0.20 GB rule) is still to be read |
| Neon transfer for the run: about 60 to 90 MB | **about 80 MB** (4.97 GB at 14:12, against 4.89 GB in the morning; web use since the morning is inside it): see [neon_readings.md](neon_readings.md) |

## Two findings from the log (neither is caused by this cycle)
1. **Esker (teamtailor) is a dead source:** its jobs page returns 404 (`eskerinc.teamtailor.com/jobs.rss`), on every pass since 29 October. Fix or disable the source: a candidate for cycle 013 or the backlog.
2. **A stale AI results file is held back at every `ai sync`:** `2026-10-23_213434_saxobeat_job_screening_results.json` answers export `E-20261023-213434`, which exists in the **local** database (made by the runner on 23 October, when the runner still used the local one) but is unknown to the hosted one. The file sits in `Saxobeat AI\problems` and is counted as "1 problem" each run. Harmless; it can be left or deleted by the owner (the agent's answers in it are for jobs already judged since).
