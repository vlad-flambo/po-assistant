# The first sweep on the hosted app (plan slice 10, second half)

| What | Value | Source |
|---|---|---|
| Hosted dry run, console page, 2026-11-03 | 17 waiting | owner's word (`hosted_dry_run.md`) |
| The owner ran the sweep | 2026-11-04 (time not stated), "seems to have worked" | owner's word |
| Pipeline page banner afterwards, 2026-11-04 | "**18** applications with no answer were presumed rejected by the app in the last 7 days. See them in Rejected · Open one to put it back to Applied" | owner's paste of the live banner |
| Before/after counts files from the runbook | **none saved** (`counts_prod1_before_sweep.json`, `counts_prod1_after_sweep.json` are not in this folder) | folder listing, 2026-11-04 |

## 17 yesterday, 18 today: explained by the clock, not by a surprise
The banner counts the candidate's jobs that are Rejected with `auto_rejected_at` in the last 7 days; it can only be the first sweep's rows (no earlier sweep, no put-back reported). The sweep moves what is past 30 days *when it runs*, and the count grows with the date. On the restored 29 Oct dump (scratch copy, dropped afterwards), the same rule gives, by the day the sweep runs (cutoff = that day at 12:00 minus 30 days): **2 Nov 17, 3 Nov 17, 4 Nov 18, 5 Nov 28** (the dump holds 11 applications dated 5 Oct, so tomorrow's count jumps). The hosted page said 17 on 3 Nov and the banner says 18 on 4 Nov: the same two numbers the dump predicts. Applications that became Applied on 29 Sep to 2 Oct are 17 of the 18; the 18th is dated 5 Oct before noon.

## What this does and does not prove
- **Proved:** the sweep ran on the host and moved 18 applications (banner count, owner's paste); the new column and table work there; the banner renders in English on the live pipeline page.
- **Not proved:** that "dry run = sweep" at the same moment on the host (no dry run of 4 Nov and no counts compare exist); that the history grew by exactly 18 lines; that nothing else changed. Criterion 15 is therefore **met on the local copy and consistent on the host, not measured on the host**.
- If the owner wants it measured after the fact: `scripts/db_counts.py` gives the table counts now, but with no "before" file only the absolute figures can be read; the `auto: no answer after 30 days` history lines (18 expected) can be counted on the host with one read-only query, which I will not run without the owner's word.
