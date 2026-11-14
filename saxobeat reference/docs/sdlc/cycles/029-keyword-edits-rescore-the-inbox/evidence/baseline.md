# Baseline: how far candidate 1's stored scores are from their own keyword list (2026-11-05)

**Setup.** The 29 Oct 2026 dump (`data/backups/saxobeat_2026-10-29_100546.dump`) restored into the scratch database `scratch029` of the local Docker Postgres (`saxobeat-db-1`), migrated to the current code (0041 to 0043). Cycle 021's `replay_harness.py` (read only, glossary switched off with `SAXOBEAT_GLOSSARY=0` so that only the owner's keyword edits can explain a difference) replayed candidate 1's 8,849 scored views in memory: 43 s setup, 18 s scoring. Nothing was read from or written to Neon. The scratch database is dropped at the end of the session.

## 1. Where candidate 1's views sit (SQL on `scratch029`)

| Status | Visible | Scored | Stored with the current profile version (5) | Older version | Never scored |
|---|---|---|---|---|---|
| new (the inbox) | yes | 1,634 | **1,634** | 0 | 0 |
| new | hidden by a filter | 1,416 | 0 | 1,416 | 17,080 |
| dismissed | yes | 4,999 | 13 | 4,986 | 1 |
| applied, interviewing, shortlisted, withdrawn, rejected | yes | 111 | 6 | 105 | 0 |
| expired | yes or hidden | 689 | 0 | 689 | 4,788 |

- All 1,634 visible inbox scores were created between 2026-10-28 11:38:00 and 11:39:33 UTC: one rescore pass, 93 seconds, one profile version. So the stored version **cannot** tell the inbox from itself: every row carries version 5, and the rows are still behind the config.
- The brief's figure "1,634 of 3,050 visible inbox views" is the 1,634 visible plus 1,416 new views a filter hides (their scores are older and invisible to the owner; a refilter that shows them scores them again).

## 2. How far the inbox is from the keyword list in the dump (`stale_inbox_output.txt`)

Replay of the 1,634 visible inbox rows with the config of the 29 Oct dump, against the stored deterministic score:

| | Rows |
|---|---|
| Replay higher by 1 point or more | 1,063 (65 %) |
| Replay lower by 1 point or more | **0** |
| Replay higher by 5 or more / by 10 or more | 210 / 10 |
| Mean / median / largest difference | +2.54 / +2.40 / +16.0 |
| Cross the inbox floor of 35 (below it stored, at or above it replayed) | **218 (13 %)**; none go the other way |
| Same 50 best jobs, stored order against replayed order | 50 of 50 |
| Same 100 best jobs | 92 of 100 |

Reading: the ordering at the top is almost the same, but **13 % of the inbox sits on the wrong side of the floor**, in one direction (jobs the owner's own newer keywords would have shown). That is what a keyword list extended after scoring does. Replay is never lower, never loses a stored match.

## 3. What the keyword list did between the two dumps (`config_diff_output.txt`, candidate 1)

28 Oct dump (12:29 local) to 29 Oct dump (10:06): profile version 4 to 5, keyword weight 0.7 both. Include list 40 to 56 entries: 48 added (for example "Product Manager" 5, "AI Delivery" 5, "AI Transformation" 5, "Head of Operations" 4), 32 removed (mostly lower-case duplicates such as "product", "ops", "ai"), 6 re-weighted; exclude list 10 to 15. **The list was largely rewritten in about a day and nothing in the data records when.** The dump has no timestamp on `Config`, so the moment of an edit cannot be told from the database, only its effect (section 2).

Not established: whether the 28 Oct 11:38 rescore ran before or after the last edit. The rows say only that the config of 29 Oct 10:06 scores higher than what was stored.

## Not done in this baseline
- No other candidate was replayed (candidate 3: 8,781 visible inbox views; its keywords are a CV import's leftovers, not a user's edits).
- No measure of the cost of a rescore on Neon beyond cycle 021's: about 5.5 KB of posting text per job, 16.6 MB for 2,980 jobs.
- Whether the synchronous "Rescore new jobs" button completes inside gunicorn's 120 s limit on the host with a real inbox: not measured (it was run from the command line on 4 Nov, not from the page).
