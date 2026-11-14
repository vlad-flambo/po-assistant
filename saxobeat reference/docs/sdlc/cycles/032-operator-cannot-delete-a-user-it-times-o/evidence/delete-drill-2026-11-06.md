# Delete drill, 2026-11-06 (claude, local temporary SQLite, nothing hosted touched)

Script: `drill_delete.py` (this folder). Run from Git Bash in the repo root with `SAXOBEAT_DB=<temp file>`; builds one account with N job views, each with one score and one status change, then times `accounts.delete_account(user)` and counts the SQL statements.

| Views | Scores | Status changes | Time | Queries | Result |
|---|---|---|---|---|---|
| 36,271 (the size of the reported account) | 36,271 | 36,271 | 32.3 s | 7,700 | all deleted; the 36,271 shared jobs untouched |

Reading: on a local file database, with no network, the cascade alone costs 32 s (Python loading about 110,000 rows to delete them) and 7,700 round trips. The real account has more child tables filled (interviews, AI tasks, cheat sheets), so it is a floor. On Render (0.5 CPU, `WEB_CONCURRENCY=1`) talking to Neon over the network, every one of the 7,700 round trips adds its latency (at 10 ms each: +77 s), which is consistent with passing gunicorn's 120 s timeout. The latency figure is an assumption, not measured.
