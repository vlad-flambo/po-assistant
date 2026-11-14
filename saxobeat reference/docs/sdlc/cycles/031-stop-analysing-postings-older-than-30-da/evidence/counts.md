# Cycle 031, slice 6: what the 30-day rule would hide (read-only counts, 2026-11-06)

**Setup.** The 29 Oct 2026 dump (`data/backups/saxobeat_2026-10-29_100546.dump`, 31,968 jobs) restored into the scratch database `scratch031` of the local Docker Postgres (`saxobeat-db-1`; I started Docker Desktop for it). Only `SELECT`s and `EXPLAIN ANALYZE` of selects were run (`counts.sql`, `counts_extra.sql`, `counts_today.sql`; each refuses any database whose name is not `scratch031`); outputs are the `*_output.txt` files. Nothing was read from or written to Neon; the scratch database is dropped.

## What the dump says (as of its own time, 29 Oct 10:06)
- **Stored limits:** both candidates in the dump have `max_age_days` = 60. (The owner has since moved the host's candidates to 30 by hand; that is not in the dump, so it was not checked here.)
- **Visible new views, and those older than 30 days by the new rule:** candidate 1 (vlad): 1,632 visible, **485 dated older than 30 days (30 %)**, 0 undated imported over 30 days before. Candidate 3 (Proto Type, a test profile): 8,781 visible, 1,742 dated older than 30 days (20 %), 0 undated.
- **Scored views that would be hidden:** candidate 1 485 of 1,632; candidate 3 1,738 of 8,771.
- **Undated postings:** 3,143 of 31,968 jobs (9.8 %) have no posting date at all. At dump time none was imported more than 30 days earlier, because the database only goes back to **2026-09-29** (oldest `first_seen_at`); 2,342 of them were imported in the week of 5 Oct, 359 in the week of 12 Oct, 285 and 157 in the next two weeks.
- **Dated views by age (candidate 1, as of the dump):** 107 are under 7 days, 199 7 to 14, 552 14 to 30, 308 30 to 45, 176 45 to 60, 1 over 60. So 484 of the 485 that the new default hides are in the 30-to-60-day band the old limit kept.

## The estimate for today (the same data with "now" = 6 Nov; counts_today_output.txt)
| Candidate | Visible new views in the dump | Dated, over 30 days | Undated, imported over 30 days ago |
|---|---|---|---|
| 1 (vlad) | 1,632 | 840 | 106 |
| 3 (Proto Type) | 8,781 | 3,508 | 1,009 |

These are what a limit of 30 would take out of the inbox as it stood on 29 Oct if it were applied today: more than half of candidate 1's visible inbox (946 of 1,632, 58 %). Most of it is the dated 30-to-60-day band, which the owner's manual move to 30 on the host has presumably already hidden (not verified); the undated part (106 and 1,009) is what this cycle adds, and it grows each day as the early-October imports pass 30 days.

## Cost of the new age-out query
`EXPLAIN ANALYZE` of the select for candidate 1 (the one with most views per the query, 1,632 visible): **11.3 ms** with the undated branch, **12.0 ms** the old dated-only form. Both are a sequential scan of `jobs_job` (17,588 rows pass) joined to the candidate's rows by the existing index; the extra `OR` costs nothing measurable. No text column is read.
