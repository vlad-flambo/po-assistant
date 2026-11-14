# Slice 6: the success measure, measured (2026-11-04)

Replays of the final code on the scratch copy of the 29 Oct dump (dropped afterwards), glossary on against the baseline (glossary off): `replay_after_c1.md`, `replay_after_c3.md` (full tables and examples), `job_33238_replay_after.txt`. Harness and comparison scripts are in this folder.

| Check (spec criterion) | Threshold | C-01 vlad (English profile) | C-03 Proto Type (French profile, junk keywords) |
|---|---|---|---|
| 6: no keyword score goes down | 0 down | **0 down**, 2,904 up | **0 down**, 44 up |
| 10: similarity of postings in the profile's own language unchanged | 0 differences | **0** of 3,094 English | **0** of 7,003 French |
| 12: same-role control, mean absolute gap FR/EN | at most 10 | **10.6 before, 3.2 after** (15 roles) | 3.2 before, 2.5 after (14 roles) |
| 13: job 33238 above 35 | above 35 | **49.8** (keyword 39.8, similarity 63.1, level +3; the host showed 33) | - |
| 14a: English mean does not fall by more than 1 | at least -1 | 41.5 to 42.0 (+0.6) | 21.9 to 23.3 (+1.4) |
| 14b: applied or beyond, AI 70+: none falls under the floor | 0 | **0 of 117** | 0 of 0 |
| 14c: crossings counted | counted | French: 1,561 rise, 0 fall; English: 54 rise, 0 fall | English (the other language here): 72 rise, 0 fall |

Also:
- **Whole pool, C-01:** French mean 27.3 to 35.8, English 41.5 to 42.0; gap 14.2 to 6.2. Share at or above the floor: French 10.9 % to 38.2 %, English 65.9 % to 67.7 %.
- **Outside check against the AI reviews (not a criterion):** among French postings the AI also reviewed, the rank correlation between the deterministic score and the AI score goes from 0.27 to 0.32 (English: 0.43, unchanged); of the French postings with an AI score of 60 or more, 76 % were above the floor before and 99 % after (English: 98 % both). The French postings that rise above the floor have a mean AI score of 18.8, between the ones already above (27.2) and the ones still below (11.2).
- **What drives the rises (C-01):** the keyword half through `customer care` (service/relation client), `remote`/`télétravail`, `platform`/`plateforme`, `banking`/`banque`, `hybrid`, `GenAI`, `payments`; the similarity half for every French posting (mean 11.7 to 32.9). The random examples in `replay_after_c1.md` show that some rising French postings are only loosely related to the owner's search (a Linux systems engineer, a repo trader): they pass because the floor is lenient (two English postings in three pass it); the glossary does not make French stricter or looser than English, it makes them alike.
- **C-03** shows the effect the symmetric rule (decision D5) is for: with the first, French-only version its French postings were over-scored; with the symmetric rule they do not move and its English ones (the other language for a French CV) rise.

**Decision point (slice 6): passed.** Job 33238 is above 35 and the same-role gap is under 10 without the word-set matching option of the spec, which stays unused.

**Not shown:** the real inbox counts on the host (the rescore preview on the host database is the owner's slice 11); the value of 0.032 on a French-profile candidate with a good keyword list (none exists in the data); the Neon cost of the larger boilerplate count (`cost.md`).
