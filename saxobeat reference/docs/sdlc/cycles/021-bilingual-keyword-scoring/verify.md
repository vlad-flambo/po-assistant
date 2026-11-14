# Verify: bilingual keyword scoring

| | |
|---|---|
| **Cycle** | 021 |
| **Stage** | Verify (accepted by the owner 2026-11-04) |
| **Spec** | [spec.md](spec.md) |

## What was done on the host (2026-11-04, by me at the owner's word, after the owner's Neon snapshot of prod1)
| Step | Result | Evidence |
|---|---|---|
| Push of the cycle's commits | `origin/main` held `4ec24c8` after a fetch (the owner's push) | plan, slice 10 |
| Limited preview, 200 newest inbox jobs per candidate, read only | C-01: 44 rise above the floor, 0 fall. C-03: 1 rise. C-04: 0. 2.6 MB of posting text read, `Nothing was written.` | `evidence/hosted_preview_limit200.txt` |
| Full preview, candidate 1, read only | 2,980 inbox jobs, 16.6 MB of text: against the stored scores **624 rise above the floor and 11 fall** (989 English: 18 rise, 11 fall; 1,814 French: 604 rise, 0 fall); the glossary alone: 636 rise, **0 fall** | `evidence/hosted_preview_c1.txt` |
| **Rescore of candidate 1** (owner: "Yes, candidate 1 only") | `2980 jobs scored again` | `evidence/hosted_rescore_c1.txt` |
| Preview again right after (400 newest inbox jobs) | 0 rise, 0 fall against the stored scores: the stored scores now are the new ones (a signal that can only be true if the rescore wrote them) | `evidence/hosted_preview_after_rescore.txt` |
| Job 33238 on the host data, in memory | status `interviewing`, so the rescore (inbox only) leaves its stored score at 33.1; scored now with the current code: keyword 39.8, similarity 43.0, level +3, **43.7** (floor 35), found through the glossary: "remote" as "télétravail" | `evidence/hosted_job_33238.txt` |
| Job pages on the host after the rescore | six rescored French postings show "found as: …" words next to the owner's keywords (for example "Chef de Projet Implémentation", "télétravail", "paiements", "plateforme", "Intelligence Artificielle Générative") | browser pane, 2026-11-04 |

The 11 English postings that fall below the floor are not the glossary's (it makes 0 fall): their stored scores were older than the owner's keyword list (see `plan.md`, slice 1 notes), so the rescore brought them to today's rules.

## Evidence per acceptance criterion
| # | Criterion (short) | Result | Evidence |
|---|---|---|---|
| 1 | Glossary file of concepts, with its self-checks | pass | `jobs/glossary.py` (133 concepts); `tests/test_glossary.py`, 16 tests: empty side, term in two concepts, no letter, one-language line, false friends, normalization |
| 2 | Covers the keywords of C-01 and C-03, title words | **partial** | C-01: 50 of 56 keywords have a concept, the 6 others have a reason (`evidence/keyword_coverage.md`). C-03: 1 of 40: its keywords are numbers, tool and school names of a CV import with no equivalent to add. Title words: 107 (FR) and 90 (EN) of the 200 most frequent are used in a concept, the rest listed (`evidence/title_words_coverage.md`) |
| 3 | False-friend guard, owner reads each concept | pass | `FALSE_FRIENDS` in the glossary and `test_false_friends_are_in_no_concept`; owner read the whole list: "Looks fine" (2026-11-04) |
| 4 | A keyword is a hit through its equivalent, same rules (title 1.5x, cut, boilerplate) | pass | `tests/test_scoring_bilingual.py`: keyword alone, equivalent alone, both, neither, title and body, whole words, company text |
| 5 | One concept, one count (reworded, `decisions.md` D1) | pass | `test_one_concept_is_boosted_once...`, `test_a_keyword_written_as_such_is_scored_exactly_as_before...` |
| 6 | No keyword score goes down; exclusions untouched | pass, with a note | replay, glossary on against off: 0 down on 8,849 (C-01) and 9,463 (C-03) postings; glossary off equals the baseline on all 18,312 (`evidence/baseline.md`, `slice6_summary.md`). Exclusions: the code path is unchanged and `test_exclusions_are_not_expanded` passes; not compared byte for byte on C-01's 15 words |
| 7 | Labels and counts are the candidate's; `key_total` unchanged | pass | `test_the_key_total_does_not_depend_on_the_glossary`; the "found as" words are worked out when the page is shown, no column (plan) |
| 8 | Boilerplate treats a concept as boilerplate; extra work measured | **partial** | implemented at term level, not "any term of the concept" (`decisions.md` D2: an equivalent found in the body is ignored if it or the candidate's own keyword is the employer's company text); cost in criterion 16 |
| 9 | Posting and profile language | pass | `tests/test_similarity_language.py` (`test_the_posting_language`, `test_the_profile_language`) |
| 10 | Own-language similarity unchanged; other language with its reference and scale | pass | replay: 0 differences on 3,094 English (C-01) and 7,003 French (C-03) postings; scale 0.032 and the symmetric rule in `decisions.md` D4, D5 |
| 11 | Reference cached like the model, no extra read | pass | `test_the_model_is_cached_per_profile_and_glossary_setting`; the host preview used the runner's word-count cache and no extra text |
| 12 | Same-role control, at most 10 | pass | C-01: mean absolute gap **10.6 before, 3.2 after** (15 roles); C-03 reported: 3.2 to 2.5 (`evidence/replay_after_c1.md`, `replay_after_c3.md`) |
| 13 | Job 33238 above 35 | pass | replay **49.8**; host data **43.7** (`evidence/job_33238_replay_after.txt`, `hosted_job_33238.txt`). Its stored score on the host stays 33.1 because the job is `interviewing` and a rescore covers the inbox only |
| 14 | No harm: English mean, protected jobs, crossings listed | pass | (a) English mean +0.6 (C-01), +1.4 (C-03); (b) 0 of 117 applied-or-AI-70+ jobs fall; (c) counts and examples in the replay files, read by the owner: "Looks fine"; host: 0 falls by the glossary |
| 15 | "found as" on the job page, English and French | pass, English on the host | `tests/test_job_explain.py` (English and French text, label kept, no extra text when the own word matched); host pages checked in the English interface; **French on the host not looked at** |
| 16 | Cost: scoring at most 1.5 times, one counting query | pass, with a note | scoring **1.24 times**; the counts: still one query per chunk but 2.2 times the work on a cold cache (`evidence/cost.md`); a first run gave 1.50 and was improved |
| 17 | Rescore dry run: counts, writes nothing, equals a real rescore | pass | `tests/test_rescore_preview.py` (SQL captured: no write; counts equal a real rescore's); on the host: preview 624 and 11, then 0 and 0 after the rescore |
| 18 | Full suite on SQLite and Postgres | pass | 1,552 passed on SQLite and on the local Postgres (2026-11-04) |

## Tests
Full suite after the last code change: **1,552 passed** on SQLite (4 min 12 s) and on Postgres (5 min 44 s). New tests: 16 glossary, 13 keyword scoring, 9 similarity and language, 7 job explanation, 7 preview and rescore. No known failure.

## Not verified
- The French interface on the host (the "found as" wording was checked in English there; in French by a test).
- Candidates 3 and 4 were **not rescored** (about 100 MB of reads for almost no change); their stored scores are the old ones. Candidate 4 shows no change in the limited preview; candidate 3 one.
- The scale 0.032 was calibrated on one candidate; it was not checked on a French-profile candidate with a good keyword list (none exists in the data).
- The cost of the larger employer count on **Neon** (compute): not measured; the runner will show it at its next pass.
- Neon read allowance: the readings I made total about 40 MB of posting text (2.6 + 16.6 + the rescore's 16.6 + 2.4, plus rows and counts). **Owner's reading of Neon on 2026-11-05 (sum of all projects, this month): network transfer 0.49 GB, compute 3.11 CU-hrs, storage 0.55 GB, history 0 GB.** Cycle 001's daily series had 0.31 GB at 10:17 on 4 Nov, so about 0.18 GB came in since, of which my reads and the rescore are a part (the runner and the web app account for the rest: not separable from the sum). Far from the 5 GB cap.
- Quality of the postings that rise: the examples read by the owner look fine; two patterns to know are a mere mention of a title ("Executive Assistant to VP Product" matches "Head of Product" through "VP product"; a posting that names the "directeur des opérations" matches "Head of Operations"), which the literal keywords already did for their own words.
- **A transient 502** from the hosted app was seen at about 18:16 to 18:19 (local time) right after the rescore and ended by 18:21; the cause is not known (Render restart or the rescore's reads); the owner may want to look at Render's Events.

## Verdict
- [x] Accepted by owner ("Accept", 2026-11-04; criteria 2 and 8 stay partial as written)
- [ ] Sent back (what, to which stage)
