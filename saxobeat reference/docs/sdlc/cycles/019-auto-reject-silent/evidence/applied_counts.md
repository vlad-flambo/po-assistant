# Applied jobs older than 30 days (plan slice 1)

Read on **2026-11-03** from a scratch Postgres copy, `measure_20261103112421`, restored from `data/backups/saxobeat_2026-10-29_100546.dump` by `scripts/measure_reads.ps1 -KeepDb` (the dump is the old project's, taken 2026-10-29 10:06; the latest change in it is 2026-10-28 14:54 UTC). Local only: the hosted database was not touched. The scratch database is kept for slice 7.

**Stale by design:** the hosted database (prod1) has moved on since 29 Oct. These are the numbers the code will meet on a copy of that state, not the hosted numbers. The hosted count comes from the dry run (slice 10).

## Result

| What | Count |
|---|---|
| Candidate jobs in all statuses | 61,393 (new 46,790; expired 9,492; dismissed 5,000; **applied 60**; rejected 46; interviewing 2; withdrawn 2; shortlisted 1) |
| Applied, all belong to one candidate | 60 (candidate id 1) |
| Applied and older than 30 days **on 2026-10-29** (the dump's own date) | **0** |
| Applied and older than 30 days **as of 2026-11-03** (same data, clock moved on) | **17** |
| of these 17: with an interview stage / focus job / with follow-ups | 0 / 0 / 0 |
| So the sweep would move, on this data, as of 2026-11-03 | **17** |

Age of the 60 Applied jobs by `status_changed_at`, as of 2026-11-03: under 14 days 14; 14-20 days 7; 21-29 days 22; 30-44 days 17; 45 or more 0. So 22 more would cross 30 days within nine days.

## What the rows showed (findings)

1. **No history behind the 17.** None of them has a `StatusChange` line, and `status_changed_at` is 2026-09-29 to 2026-10-02: they were put in the Applied status by the multi-user migration or an import, not by a click in the app. Their `status_changed_at` is therefore the import day, which is the same as or later than the real application day: the clock can only be late for them, never early (safe direction). Six of the 60 have no `applied_at` either, so the sweep must use `status_changed_at` (as the spec says) and not depend on `applied_at`.
2. **All 17 would move on the first sweep** (Q4: accepted, same tag and undo); the banner would show 17 on the pipeline page of that one candidate.
3. **Rejections today:** 46 rejected jobs, 43 with the note "changed on the job page" and 3 "moved in pipeline"; none with "no reply", so the manual path has not been used on this data. The 46 are not touched by this cycle.
4. Cycle 019's spec needs no change from these findings. The "follow-ups do not reset the clock" rule has no case in this data (0 follow-ups).

## SQL used

```sql
select status, count(*) from jobs_candidatejob group by 1;
select count(*) filter (where status_changed_at < timestamp '2026-10-29 10:06' - interval '30 days') as old_at_dump,
       count(*) filter (where status_changed_at < timestamp '2026-11-03 12:00' - interval '30 days') as old_today,
       count(*) filter (where status_changed_at < timestamp '2026-11-03 12:00' - interval '30 days'
                          and exists (select 1 from jobs_interview i where i.job_id = c.id)) as with_interview,
       count(*) filter (where status_changed_at < timestamp '2026-11-03 12:00' - interval '30 days' and focus_at is not null) as focus,
       count(*) filter (where status_changed_at < timestamp '2026-11-03 12:00' - interval '30 days'
                          and not exists (select 1 from jobs_interview i where i.job_id = c.id) and focus_at is null) as would_move
from jobs_candidatejob c where status = 'applied';
```

Result row: `0 | 17 | 0 | 0 | 17`. The restore record (counts and bytes only) is in `restore.jsonl` next to this file.

## Not verified
- The hosted number (prod1 has newer data than this dump). Slice 10's dry run gives it.
- Whether other candidates exist on the host with Applied jobs: the dump holds one candidate with Applied jobs.
