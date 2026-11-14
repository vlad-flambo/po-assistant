# Decisions: bilingual keyword scoring

One entry per decision, newest last. Do not edit old entries: add a new one that supersedes.

## D1. A keyword written as such in the posting keeps its own boost; an equivalent adds a boost only where nothing was counted for the concept
- **Date:** 2026-11-04 (slice 4)
- **Context:** Spec criterion 5 says two keywords of one concept count as one at the higher weight; criterion 6 says no posting's keyword score goes down. They clash for a candidate who wrote both "Product Manager" and "chef de produit" (both weight 5): a posting that contains both words scores today with two boosts, and counting one would lower it.
- **Options considered:** (a) merge the candidate's own keywords of one concept into one count always (criterion 5 as written; some scores go down); (b) keep the literal matching exactly as before for words found as written, and let the glossary add a boost only when no keyword of the concept was found as written (criterion 6 kept).
- **Decision:** (b). For a concept: every keyword found as the candidate wrote it counts as today; if none was, the best boost among the keywords found only through an equivalent (weight, 1.5x in the title) is added once. All the keywords found, either way, are shown as matched and counted in "key words found of N" (the total N does not change).
- **Why:** it keeps every existing score as it is (criterion 6, tested with the glossary off and on, 0 differences with it off), and an equivalent can never count a concept twice, which is the harm criterion 5 guards against. Criterion 5's text is read in that sense; the owner is told at slice 4.
- **Consequences:** two keywords of one concept both written as such in a posting still count twice, as before the glossary: that is the candidate's own list.

## D2. The employer-boilerplate rule also covers the equivalents
- **Date:** 2026-11-04 (slice 4)
- **Context:** The rule ignores a keyword found only in the body when the employer's "About us" text has it (it is in most of the employer's postings). With equivalents, the same company text can carry the French term.
- **Decision:** an equivalent found in the body counts unless that term is boilerplate for the employer or the candidate's own keyword is; a title match always counts. The employer counts (`company_boilerplate`) are made over the keywords' terms **and** their equivalents (`scoring.search_terms`).
- **Why:** spec criterion 8. **Cost:** more patterns in the one counting query per chunk of employers: measured in slice 9.
- **Consequences:** `company_boilerplate` can return equivalent terms; the existing tests keep passing.

## D3. The posting's language for the "not in French" marks is `Job.language`
- **Date:** 2026-11-04 (slice 4)
- **Decision:** the marks of the glossary ("ai" is not an equivalent in French postings) use `Job.language`; a blank language searches every term (no protection, as before). The similarity half (slice 5) falls back to `detect_language` when `Job.language` is blank.
- **Why:** the language is set when a posting is ingested; detecting it again for every scoring would cost time for 4 % of the postings.

## D4. The French similarity scale is 0.032 (English stays 0.06), and the French reference is the profile plus the French terms of the keywords' concepts
- **Date:** 2026-11-04 (slice 5)
- **Context:** On C-01's replay, French postings with a role in the title have a mean similarity of 12.1 against English ones at 35.3 (2.9 times lower). A French reference (the English reference plus the French terms of every keyword's concept) lifts the French mean to 18.6, still 1.9 times under the English 35.3: the reference remains mostly English words. A reference made only of the keywords and their French terms gives French 20.7 (and would be useless for English postings: 15.4), so it is no better as a French reference and loses the profile's own words.
- **Options considered:** (a) English reference for every posting and a French scale only; (b) the French reference as implemented plus a French scale; (c) a French reference without the profile text; (d) a scale worked out for each candidate from the stored postings (needs the postings' texts at run time: a Neon read the runner avoids, cycles 001 and 002).
- **Decision:** (b). French scale `similarity.SCALES["fr"] = 0.032` (0.06 / 1.9, rounded); English unchanged, so English similarity is exactly what it was.
- **Why:** it makes the mean similarity of French and English postings of the same role equal on C-01 (35.3 against 18.6 x 1.9 = 35.3 by construction), which is what the intent asks for ("the language does not change the score"). It is a **judgement on one candidate's data** (the second candidate's keywords are junk and cannot calibrate it); a candidate with a much longer or shorter profile may need another constant.
- **Consequences:** French similarity values are about 1.9 times what they were with the English reference; the replay checks (criteria 12 to 14) show the result. To revisit with more candidates' data: this constant, and (d) if the Neon read cost allows.

## D5. The "other language" is the one the profile is NOT written in (not always French)
- **Date:** 2026-11-04 (slice 6, after the first replay of C-03)
- **Context:** D4 built a French reference and a French scale. On C-03, whose profile is a **French** CV, the French postings already scored above the English ones (17.0 against 5.3) and the French scale lifted them to 31.8: the 1.9 factor belongs to a French posting read against an English profile, not to French postings. A French-profile candidate would have had French postings over-scored, a regression the spec's "no harm" is there to catch.
- **Decision:** the model has a **native** language (the one the profile is written in, `scoring.profile_language`, `detect_language` on the profile text, English when too short to tell) and an **other** one. Postings written in the other language are compared with the reference plus the keywords' terms in that language (`scoring.other_reference`) and scaled with `SCALES["other"]` (0.032); every other posting, in the native language or of unknown language, is compared with the reference as before (scale 0.06).
- **Why:** it is the same mechanism for an English-profile candidate (French postings are "other", exactly D4) and a French-profile one (English postings are "other"). C-01 is unchanged by this decision (its profile is English). The 0.032 factor is still calibrated on C-01 only and is assumed to be as large the other way round: **to be checked with a French-profile candidate who has a good keyword list** (C-03's keywords are junk).
- **Consequences:** spec criterion 10 reads "postings in the profile's own language keep the same similarity as today"; for C-01 that is the English postings, for a French-profile candidate the French ones. The spec text is reworded at slice 6.
