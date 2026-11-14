# Stored scores by posting language (candidate C-01 "vlad"), 2026-11-04

**Source.** The backup `data/backups/saxobeat_2026-10-29_100546.dump` (the hosted data as of 29 Oct 2026, 31,968 jobs), restored into a scratch database in the local Docker Postgres (`replay021`), migrated to the current code (0041 to 0043), read with `replay_lang.py` (this folder), then dropped. Nothing read from Neon, nothing written to the dev database or to the host. The scores are the ones **stored** in the dump (no re-scoring). Job 33238 is not in it (it is newer).

**Candidate.** C-01 `vlad`: 56 include keywords, 37 of weight 3 or more (the same 37 the job page shows), `keyword_weight` 0.7, inbox floor 35.

## All scored postings, by the posting's language

| Language | Postings | Deterministic mean (median) | Keyword mean | Similarity mean | At or above floor 35 | With 0 key words found |
|---|---|---|---|---|---|---|
| French | 5,718 | 27.9 (24.2) | 34.0 | **10.7** | **11.5 %** | 75.5 % (of 5,105 counted) |
| English | 3,094 | 39.7 (37.3) | 44.4 | **30.0** | **56.8 %** | 49.4 % (of 1,612 counted) |
| unknown | 37 | 30.8 | 37.2 | 12.1 | 21.6 % | 78.6 % |

Gap French minus English: deterministic -11.8; keyword -10.4 (worth 0.7 x 10.4 = about 7 points); similarity -19.3 (worth 0.3 x 19.3 = about 6 points).

## Postings the AI also reviewed (a more homogeneous group)

| Language | Reviewed | Deterministic mean | Keyword mean | Similarity mean | At or above floor |
|---|---|---|---|---|---|
| French | 803 | 40.7 | 46.7 | **18.1** | 51.8 % |
| English | 1,667 | 47.1 | 47.3 | **36.2** | 74.9 % |

Among them the keyword means are the same (46.7 against 47.3) and the similarity means are 18 points apart.

## Postings with an AI score of 70 or more, and postings moved into the pipeline

| Group | French | English |
|---|---|---|
| AI score 70 or more | 11 postings, deterministic mean 59.5, all at or above the floor | 23 postings, mean 73.6, all at or above the floor |
| Pipeline (applied or beyond) | 38, mean 59.2, 94.7 % at or above the floor | 73, mean 69.7, 98.6 % at or above the floor |

## What this does and does not show

- **Shows:** with the same candidate, stored French postings score about 12 points lower than English ones, and 11.5 % of them reach the inbox against 56.8 %. Part of the gap is the keywords and part is the similarity half.
- **Does not show the cause.** French and English postings are not the same roles: the French pool may simply hold fewer relevant jobs. No same-role control has been run yet.
- **Cannot show the false negatives.** The AI reviews and the pipeline are filled **after** the floor: the groups above are survivors (all of the AI >= 70 group is above the floor for that reason). A job like 33238, cut by the floor and found by hand, is by construction not in them.
- Counts "0 key words" only for rows already re-scored with `key_counts` (older rows are empty), so those percentages rest on fewer rows.
- The 29 Oct dump is 6 days old; the hosted data has more postings and may have a changed keyword list.
