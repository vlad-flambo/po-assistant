# Slice 1: the replay harness and the baseline (2026-11-04)

**Setup.** The 29 Oct 2026 dump (`data/backups/saxobeat_2026-10-29_100546.dump`, 31,968 jobs) restored into the scratch database `replay021` of the local Docker Postgres and migrated to the current code (0041 to 0043). `replay_harness.py` (this folder) re-scores every scored view of a candidate **in memory** with the app's own `deterministic_breakdown`, with the candidate's config as it is in the dump, and compares with the stored scores. It writes nothing and switches the word-count file cache off. Nothing was read from Neon. Raw outputs: `harness_output_c1.txt`, `harness_output_c3.txt`.

## Does the replay reproduce today's scores?

| | C-01 vlad (8,849 views) | C-03 Proto Type (9,463 views) |
|---|---|---|
| Views stored with the config's profile version | 1,653 (of which 1,634 are in the inbox: status new) | all 9,463 |
| Keyword score equal to 0.1 | 33.0 % of those rows | **97.6 %** |
| Similarity within 3 points | 99.6 % | 83.5 % (mean difference 1.5) |
| Deterministic score within 3 points | 68.6 % | **98.4 %** (mean difference 0.56, max 7.6) |
| Stored match no longer found by the replay | **0** | 31 rows |
| Replay keyword score higher / lower than stored | 1,107 higher / **0 lower** | 192 higher / 31 lower |

How to read it:
- **C-03: the harness reproduces the stored scores.** The 31 rows where a stored match is no longer found are all explained by the employer-boilerplate rule (the employer's postings counted at another time): with that rule off, all 31 stored matches are found again (checked, 31 of 31).
- **C-01: the stored scores are older than the keyword list in the dump.** On the rows stored with the current profile version, the replay is never lower and never loses a stored match, but is higher on 1,107 of 1,653: exactly what keywords added **after** those rows were scored would do (editing keywords does not bump `profile_version`, `jobs/views.py:995`, and the rescore runs in the background). Also, only 1,653 of C-01's 8,849 scored views carry the current version; the rest were stored under versions 1, 3 and 4. So for C-01 the replay is not compared with the stored values; **before and after are both replayed with the same config** (that is the baseline of the spec).
- **Direct proof on the job of the feedback.** `replay_job33238.py` scores the text of job 33238 (saved in `job_33238.md`) in memory with C-01's config of the dump: **keyword 36.7, similarity 13.3, level +3, deterministic 32.7, key words found 0 of 37**, hits "télétravail" and "product management", and the same 8 missing key words as the host's page. The host page showed 33 (keyword 37, similarity 15): the 1.7-point similarity difference is the word counts (the host's postings corpus is newer than the dump's). So the harness reproduces the score the owner saw, and **the 33 is not an effect of stale stored scores.**

## Baseline (today's rules, glossary absent), by language

| Candidate | Language | Postings | Deterministic mean | Keyword mean | Similarity mean | At or above floor 35 | 0 key words |
|---|---|---|---|---|---|---|---|
| C-01 | French | 5,718 | 27.3 | 32.8 | 11.7 | 10.9 % | 89.0 % |
| C-01 | English | 3,094 | 41.5 | 40.9 | 34.9 | 65.9 % | 64.8 % |
| C-03 | French | 7,003 | 24.9 | 34.3 | 17.0 | 10.7 % | 68.8 % |
| C-03 | English | 2,447 | 21.9 | 31.4 | 5.3 | 1.9 % | 95.5 % |

- C-01 on today's keyword list: French is **14.2 points lower** than English (the earlier 11.8 was on stored, partly older scores).
- **C-03 is the other way round**: English postings score lower than French ones. Its "keywords" are the leftovers of a developer's CV import (`01`, `05`, `CSS`, `SDL`, `2021`, `ISTY`...), so it is a poor test of the language gap; it is still a second profile for the "does not go down" checks (criteria 6, 10, 14). The same-role control (criterion 12) is judged on C-01; C-03 is reported, not judged, for that criterion. *To be confirmed with the owner at the spec's verify.*
- Timing on this PC, glossary absent: C-01 setup (similarity model and boilerplate counts, scratch Postgres) 75 s, scoring 8,849 views 25 s (2.9 ms each); C-03 65 s and 25 s for 9,463 views. The reference for criterion 16.

## Not done in this slice
- The same-role control baseline (needs the role concepts of the glossary, slice 2). It is produced in slice 6 by running the harness with the glossary off.
