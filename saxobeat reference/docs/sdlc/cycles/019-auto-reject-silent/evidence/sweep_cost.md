# What the sweep costs (plan slice 7, criterion 16)

Measured 2026-11-03 on `measure_20261103124053` (a copy of the 29 Oct dump, 61,393 candidate jobs), as the bytes the local Postgres container sends while a command runs (`/proc/net/dev`, eth0, before and after):

| Command | Bytes sent by the database | Note |
|---|---|---|
| idle second (baseline) | 0 | the counter does not move on its own |
| `manage.py migrate` (0041, 0042, 0043) | 32,286 | one-off |
| `auto_reject --dry-run` | 13,639 | creates the one settings row the first time |
| `auto_reject` (moves 17) | 14,532 | |
| `auto_reject` again (moves 0) | 1,714 | |

Per pass of the PC runner (which already reads about 60 MB, cycle 001): about 2 KB when nothing is due, about 15 KB when 17 applications move. At 3 to 5 passes a week that is well under 0.1 MB a month, so it does not move the Neon projection of cycle 001.

By reading the code and a test: the read selects only `id` and `candidate_id` from `jobs_candidatejob` (never the job table, never `description_text`; `tests/test_auto_reject_sweep.py::test_the_sweep_reads_no_job_text_and_stays_a_handful_of_statements`), then one UPDATE, one SELECT of the moved ids and one INSERT of the history lines per chunk of 1,000.

The console page "Auto-reject" runs the same read (the dry-run count) on each view: about 14 KB a view.

Not measured: Neon's own dashboard (the container counter is the proxy used in cycle 001).
