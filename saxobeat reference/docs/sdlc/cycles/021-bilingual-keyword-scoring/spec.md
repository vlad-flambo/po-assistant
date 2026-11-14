# Spec: bilingual keyword scoring

| | |
|---|---|
| **Cycle** | 021 |
| **Stage** | Spec (approved 2026-11-04) |
| **Intent** | [intent.md](intent.md) |

## Behaviour when finished
- A keyword of a candidate counts as found in a posting when the keyword **or its equivalent in the other language** is there. "AI" is found as "IA" or "intelligence artificielle", "change management" as "conduite du changement", "customer operations" as "opérations client(s)", "product manager" as "chef de produit" (and the other way round: a candidate who typed "chef de produit" now matches "product manager" postings). It counts once at the keyword's own weight: a posting with both languages does not score twice.
- The "Why this score" panel keeps showing **the candidate's own words** (matched, missing, key words found of N) and says, in small text, which word of the posting made the match when it was the other language ("found as: conduite du changement").
- The similarity half of the score no longer depends on the CV being in the posting's language: a posting written in the language the profile is **not** written in (a French posting for an English CV, an English posting for a French CV) is compared with a reference text that also holds the keywords' terms in that language and is scaled on such postings; a posting in the profile's own language is compared exactly as today. *(Reworded at slice 6: the first wording said "French" only; see `decisions.md` D5.)*
- This holds for **every candidate**, with no list to edit. Nothing is translated or sent anywhere: the equivalents come from a reviewed word list shipped with the app (the same rules-and-lists rule as `jobs/cvprofile.py`).
- Exclusion words ("penalty" keywords) are **not** expanded (see Design, option 5).
- Scores already stored change only when the owner runs a rescore on the host (after a Neon snapshot), and a dry run first says how many postings would cross the inbox floor.

## Acceptance criteria
Each one must be checkable in `verify.md`.

**The word list**
1. [ ] A glossary file (`jobs/glossary.py` or a data file next to it) holds **concepts**: each is a list of terms in English and French that mean the same thing for a job search ("ai", "ia", "intelligence artificielle"). Terms are stored normalized like `text.normalize` (no accents, lower case). A test loads it and fails on: an empty concept, a term in two concepts, a term with no letters, a concept with only one language when it is marked bilingual.
2. [ ] It covers every one of C-01's 56 include keywords that has a standard equivalent, and the 40 of C-03; the ones with none are listed in `verify.md` with the reason (a name, an acronym the same in both languages such as "sql"). It also covers the role titles and functions of the postings' titles most often found in the 29 Oct dump (the 200 most frequent title words of each language, with the ones that matter for a job search written as concepts).
3. [ ] A **false-friend guard**: a short list in the tests (for example "stage", "contrat", "consultant", "actuellement", "manager" read as "gerant", "assistant" read as "assistant(e)") of pairs that must not be in one concept; the test fails if one is. Each concept is read once by the owner (French wording and meaning) before the spec stage closes: ticked in `verify.md`.

**The keyword half**
4. [ ] In `analyse_keywords`, a keyword is a hit when its normalized term or any term of its concept is a whole-word match in the title or the description, with the same rules as today (title 1.5x, the cut at `MAX_DESCRIPTION_CHARS`, the employer boilerplate ignored for a body-only match). Tested with: the keyword alone, its equivalent alone, both together (one boost, not two), neither, in the title and in the body.
5. [ ] **One concept, one count.** An equivalent never makes a concept count twice: when no keyword of a concept is found as the candidate wrote it, the best boost among the keywords found through an equivalent (for example "customer operations" and "opérations client", both found as "opérations clientèle") is added **once**; when one is found as written, nothing is added for the others. Keywords found as written count as before. *(Reworded at slice 4, see `decisions.md` D1: the first wording, "count as one at the higher weight", would have lowered the scores of postings that contain both of the candidate's own words, against criterion 6.)*
6. [ ] **Monotone for the keyword score:** over the stored postings of C-01 and C-03 (replay), no posting's keyword score goes down, and no keyword is reported as both matched and missing. Exclusion handling is byte-identical to today (test on the 15 exclusion words of C-01).
7. [ ] **Labels.** `matched_keywords`, `missing_keywords`, `title_hits` and `key_counts` hold the candidate's own labels and counts; `key_total` is unchanged by the glossary (the 37 of C-01 stay 37). The word found in the other language is kept for display (a new JSON field or an extra entry, decided in the plan, with a migration if a column is needed).
8. [ ] The employer-boilerplate count (`company_boilerplate`, `_count_employers`) treats a concept as boilerplate for an employer when any of its terms is in most of that employer's postings, and its extra work is measured (criterion 16).

**The similarity half**
9. [ ] A posting's language is `Job.language`, else `text.detect_language`, else unknown; an unknown language (and any language other than French and English) behaves exactly as today. The profile's language is detected from the profile text (English when too short to tell). Tested for each case.
10. [ ] Postings in the profile's own language keep the **same similarity as today** (rounded to one decimal, on the stored postings of each candidate in that language: zero differences). Postings in the other language are compared with the reference made for them and scaled by a second constant (`SCALES["other"]`), chosen on the replay and written down with the reason in `decisions.md` D4 and D5.
11. [ ] The reference texts are cached like the current model (`cached_similarity`: one per profile and glossary setting, same time to live, same cap) and cost no extra read of the database beyond the word counts already read (`corpus.counts`).

**The measure of success (from the intent)**
12. [ ] **Same-role control.** On the 29 Oct replay, for each role concept of the glossary that has at least 20 French and at least 20 English postings with the concept in the title, the mean deterministic score of French and of English postings are compared; the mean of the gaps (in absolute value) is **at most 10 points**, and the number before and after is written in `verify.md` (today's whole-pool gap is 11.8 points, see `evidence/replay_by_language.md`). Run for C-01 and for C-03.
13. [ ] **Job 33238** (Change Manager IA H/F, eXalt; its text is saved in `evidence/job_33238.md` from the host page read on 2026-11-04) scores **above 35** on the replay with C-01's keywords. If it does not, the cycle stops here and the plan comes back to the owner with what is missing (see Design, "decision point"); it is not marked pass by adjusting a number.
14. [ ] **No harm.** (a) The mean deterministic score of English postings does not fall by more than 1 point for either candidate; (b) no posting that C-01 or C-03 applied to, or that has an AI score of 70 or more, falls from above the floor to below it; (c) the number of postings that **rise** above the floor and the number that **fall** below it are counted for each candidate and each language, listed in `evidence/` with ten examples of each direction read by the owner.

**Seeing it, safety and cost**
15. [ ] On a job page scored through an equivalent, "Why this score" shows the candidate's label and "found as: <word>" in small text, in English and in French; a job matched by the candidate's own word shows nothing extra. `manage.py i18n missing` reports no untranslated string for the new texts.
16. [ ] **Cost.** Scoring 1,000 stored postings takes no more than 1.5 times the time it takes today on the same machine (measured on the scratch copy, both numbers in `verify.md`); `_count_employers` (one query per employer chunk) still runs as one query per chunk with the extra terms; no new read of job texts for the sake of the glossary. Nothing is read from Neon for any measurement.
17. [ ] **Rescore dry run.** `manage.py` offers a dry run that, for each candidate, prints how many postings would cross the floor in each direction and writes nothing; on the scratch copy its counts equal the numbers a real rescore then produces and equal criterion 14(c). The real rescore is run on the host only by the owner.
18. [ ] The full test suite passes on SQLite and a Postgres rehearsal (any migration applied on a scratch Postgres copy first); the glossary tests are in the suite.

## Design in brief
- **A reviewed bilingual glossary of concepts**, applied when keywords are read (`_terms` in `scoring.py` returns, for each normalized keyword, its weight, its label and the set of terms to look for). `analyse_keywords` looks for any term of the set; everything else (title bonus, boilerplate, saturation curve, penalties) stays as it is. The change is local to the matching and monotone: it can only add hits.
- **A language-matched reference for similarity**: for French postings, reference = the profile's words that are the same in both languages (names, tools, acronyms) plus the French terms of the keywords' concepts, with its own scale constant; English postings are untouched. This addresses the 19-point similarity gap of the replay without moving English scores.
- **Why a list and not a model:** the app has no model and no API call in the scoring path, and a candidate's CV and keywords are private (`cvprofile.py`: "nothing leaves the server"); a list is testable, free, and read by the owner.
- **Decision point (not decided now).** Phrase keywords such as "AI Transformation" or "AI Adoption Lead" will still find only the phrase and its listed equivalents; the posting for 33238 says "transformation numérique ... solutions d'intelligence artificielle" without either phrase. If criterion 13 fails after the glossary and the French reference are in, the next option is **word-set matching for multi-word keywords** (all the keyword's content words, each through its concept, within about 12 words of each other). It also affects English postings, so it is built only after the owner sees the replay numbers and says yes.
- **Options rejected**
  1. A machine translation or an AI call of each posting or keyword: cost, privacy, and a result that cannot be tested (and "postings are never translated", PRD F13).
  2. Making each candidate type both languages (the intent's Q3: every candidate, no list to edit).
  3. Lowering the inbox floor for French postings: hides the cause, lets noise through.
  4. One mixed-language reference for all postings: would dilute the English reference and lower English scores (criterion 14a).
  5. Expanding the exclusion words too: a wrong penalty hides a good job, which is the failure this cycle fixes; "stage" is a penalty word in French for an internship and an ordinary word in English. Parked; reopen after the glossary has run for a while.
  6. Letting each candidate edit the equivalents: more screens; the glossary is fixed by the owner in the code for now (a wrong equivalent is corrected by a commit, a limit listed below).

## Interfaces and data
- Code: `jobs/glossary.py` (new), `jobs/services/scoring.py` (`_terms`, `analyse_keywords`, `_count_employers`, `reference_text`, `build_similarity`, `cached_similarity`), `jobs/services/similarity.py` (a per-language scale), the "Why this score" template and its view, a rescore dry-run command, tests, the locale files.
- Data: possibly one JSON field on `Score` for the "found as" words (migration, nullable, no data migration; applied on the host by the entrypoint after a snapshot the owner takes). No other schema change.
- Files in the cycle's `evidence/`: the replay script, `job_33238.md`, the replay numbers before and after, the false-friend list and its test, the 20 reviewed examples.

## Constraints
- **Neon:** no measurement reads the hosted database; replays run on a scratch copy of a dump in the local Docker Postgres (dropped afterwards). The only hosted write is the owner's rescore after the deploy.
- **Hosted actions are the owner's:** I do not deploy, migrate, rescore or push; the owner takes the snapshot and runs the rescore, after reading the dry-run counts (criterion 17).
- **Reversible:** the glossary can be switched off by one setting or by emptying the file (plan decides which), and a rescore with it off restores today's scores.
- **Bilingual app:** every new text has a French translation (`locale/`, checked by `tests/test_i18n.py`).
- **Calibration (cycle 008):** the scores shift for every candidate, so the stored calibration bands may need a new reading; named in Learn, not done here.

## Known limits (accepted by approving the spec)
- A wrong or missing equivalent cannot be fixed by the candidate, only in the code.
- Only English and French; other posting languages score as today.
- The glossary covers what it lists: an unusual term in a candidate's keywords with no entry is found in one language only, as today.
- Phrase keywords are matched as phrases (until the decision point is reached).

## Out of scope
- Translating postings, the CV, or the candidate's notes.
- The AI review, its weight, and the AI selection.
- Exclusion words (parked, option 5), the inbox floor value and the broad-search presets.
- A screen to edit equivalents; a third language.
- Calibrating the bands again (cycle 008).

## Gate
- [x] Owner approved this spec ("Approve spec", 2026-11-04, with the three checks accepted as written: phrase keywords decision point, exclusion words not expanded, "found as" text)
