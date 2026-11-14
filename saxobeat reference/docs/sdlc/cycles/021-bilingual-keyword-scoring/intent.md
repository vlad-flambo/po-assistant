# Intent: bilingual keyword scoring

| | |
|---|---|
| **Cycle** | 021 |
| **Stage** | Intent (started 2026-11-04; all 6 questions answered, goal and success measure confirmed 2026-11-04) |
| **Date** | 2026-11-04 |
| **Owner** | Vlad |
| **Born from** | Feedback #4: a problem from C-01 (vlad), 2026-11-02 |
| **Importance** | 4/5 (claude, 2026-11-04): scoring decides which jobs a candidate ever sees, and feedback #4 (C-01, every time, "could not do what I came to do") says a matching job that led to an interview scored 33 and would have been cut; one feedback so far, how many French postings are under-scored is not counted yet |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
> This job is a match, but deterministic score is only 33. So it wouldn't have made the cut, despite me landing a job interview.
> What c
>
> (the feedback text is cut at "What c" in the saved chat; the next answers follow)
>
> Anything else you want to add? what can we do to fix this ?
> DO job descriptions in French get consistently underscored because there are less keyword matches ?
> Maybe there should always be a bilingual set of keywords

## Why now / the pain
- How much did it get in your way? "I could not do what I came to do". Does it happen every time? "Every time" (both from the feedback chat, #4).
- The pain is a false negative: a job the candidate got an interview for scored 33, below the line where jobs are picked, so the app would never have shown it. A missed job costs more than a wrong one shown.
- No count yet of how many stored postings are affected (see Q2).

## Goal
For every candidate, a posting that fits the candidate is scored by what it asks for, not by the language it is written in: a French posting and an English one for the same role land close to each other.

## Success measure
Two checks (from Q4, accepted):
1. On a replay of the stored postings, French and English postings **of the same role** score within about 10 points of each other on average for the same candidate (today the whole pools are 11.8 points apart, and the same-role control is part of the spec).
2. Job 33238 (Change Manager IA H/F, eXalt) scores **above the inbox floor of 35** on the same replay (today 33).

And no harm: English postings do not lose more than a point or two on average, and no stored AI-reviewed good fit (AI score 70 or more) falls under the floor.

## Not doing (this cycle)
- Translating postings (PRD F13: "Postings are never translated").
- Changing the AI review or its weight (the question is the deterministic score only).
- Any change before the cause is measured (Q2).

## What we already know (facts, with where they came from)
- **Said by** C-01 (vlad) through the feedback chat (#4) on 2026-11-02, on "A job", desktop, standard mode, language en; where: "On this page" (the job page). The feedback context holds page, device, mode and language but **no job id**, so the job is not identified (`jobs/models.py:934`, field `context`). Source: the request text above and the model.
- **How the score is made** (`jobs/services/scoring.py:274-285`): deterministic = `keyword_weight` x keyword score + (1 - `keyword_weight`) x similarity, plus a seniority adjustment from the title.
- **Keywords match literally.** Accents and case are folded, so "operations" and "opérations" are one term, but "project management" and "gestion de projet" are two unrelated terms (`scoring.py:59-67`, `_has` on normalized text, whole words). A French posting scores only on keywords the candidate listed in French.
- **A posting with no keyword hit gets 30** (the neutral point of the keyword score, `scoring.py:94,122`). So 33 in total is what a posting with almost no hit and a low similarity would get. *Unverified* until the job is identified and replayed.
- **Similarity is also language-bound.** The text model is TF-IDF between the posting and the profile (CV text plus the keyword labels) (`jobs/services/similarity.py`, `scoring.py:238-240`). Stopwords are in both languages, but an English CV and English keywords share few tokens with a French posting, so its cosine is low too. The comment in `reference_text` ("incl. French equivalents so both languages land in the same vector") holds only if the candidate's keyword list really contains French equivalents.
- **French equivalents are not generated.** The only French terms are a short fixed list used when a profile is drafted from a CV (`jobs/cvprofile.py:46-49`, about 25 terms) and whatever the candidate typed. PRD.md:157 says the CV import extracts "French equivalents"; the code adds them only from that list. Each candidate's actual keyword list lives in the hosted database and was not read.
- `Job.language` already exists (`jobs/models.py:249`), so the postings' language is known and a replay can split French from English.
- **The feedback row itself lives only on the hosted database** (the local SQLite has no `jobs_feedback` table). It was not read: a Neon read costs allowance (PROJECT.md). The owner wrote it, so the owner can give the job.
- **The job (read on the host, 2026-11-04, the job page of 33238 with the owner signed in; one page view, no script, nothing written).** "Change Manager IA H/F", eXalt, Paris, CDI hybrid, published 5 Oct 2026; a recruiter screen was on 2 Nov 2026. "Why this score": **33 = "Weak fit based on your keywords and profile, no AI"**; "0 of your 37 key words"; keywords 37; profile similarity 15; level fits (title word "manager" +3). Matched: *télétravail* and *product management* (the second only through eXalt's "About us" paragraph: "Product & Project Management", "méthodes du Product Management"). Missing key words listed: AI Delivery, AI Transformation, chef de produit, customer operations, Product Manager, AI Adoption Lead, AI Builder, AI Delivery Lead.
- **What the posting says instead** (the page's description, in French): "Consultant en conduite du changement **IA**", "transformation numérique", "solutions d'**intelligence artificielle**", "piloter le changement organisationnel", "gestion rigoureuse des projets", "plans de formation et de communication". So the role is the candidate's AI-change profile, in French words: **"IA" is the French for "AI", and the key words are written "AI ..."**, so none of the AI terms can match. This supports the owner's hypothesis for this job.
- **Two causes, not one (to be separated by the replay in Q2).** (1) Language: IA, intelligence artificielle, conduite du changement, transformation have no equivalent in the list. (2) The list holds long English role phrases ("AI Adoption Lead", "AI Delivery Lead", "AI Builder"): a literal phrase like that is rare even in an English posting, so part of the gap would remain in English. Whether French postings are lower overall is **not shown by one job**.
- **No AI review was in play** ("no AI" on the page), so the final score is the deterministic 33. The inbox takes rules scores at or above a floor, 35 by default (`jobs/ai/backtest.py:34,76`, `breadth.floor(cfg.filters)`): 33 is 2 points under it. This is probably "the cut" the owner means (to confirm in Q6).
- **The replay (2026-11-04, local scratch copy of the 29 Oct dump, nothing read from Neon: [evidence/replay_by_language.md](evidence/replay_by_language.md)).** For C-01, stored scores of 8,849 postings: French 5,718 postings, deterministic mean 27.9, **11.5 % at or above the floor 35**; English 3,094, mean 39.7, **56.8 % at or above the floor**. Gap of 11.8 points = keywords -10.4 (x 0.7, about 7 points) and **similarity -19.3 (10.7 against 30.0, x 0.3, about 6 points)**. Among postings the AI also reviewed, keyword means are equal (46.7 and 47.3) while similarity still differs by 18 points (18.1 and 36.2). So the language effect is **in both halves**, and the similarity half is the steadier one: it is scaled on English text (`STRONG_MATCH_COSINE = 0.06`, `similarity.py:26`) against an English CV.
- **Limits of the replay.** French and English postings are not the same roles, so the gap is an upper bound on the language effect, not the effect itself (a same-role control is not run). And the jobs the floor cuts are not in the AI-reviewed or pipeline groups by construction, so those groups cannot count the false negatives; job 33238 was found by hand.
- The owner's hypothesis, "French postings get consistently underscored because of fewer keyword matches", is **plausible from the code but not measured**. What would confirm it: replay the scoring on the stored postings and compare the French and English averages for the same candidate, on the local copy (no Neon reads).

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Which job was it, and what do its score numbers say? | Give the link; I read the job page | **Change Manager IA H/F, eXalt** (job 33238, https://app.saxobeat.fr/job/33238/), given by the owner 2026-11-04. I read its page on the host with the owner's session: final 33, keywords 37, profile similarity 15, 0 of 37 key words, "level fits" (+3, the word "manager"). Details in the facts below. | answered |
| Q2 | Measure before deciding: may I replay the scoring of your stored postings on the local copy and compare French with English (averages, and how many French postings fall below the pick line)? | Yes: local copy only, no Neon read, nothing written | "Yes, local only" (owner, 2026-11-04). Done on a scratch copy of the 29 Oct dump, then dropped: [evidence/replay_by_language.md](evidence/replay_by_language.md). French postings score 11.8 points lower (27.9 against 39.7) and 11.5 % reach the floor against 56.8 %; about 7 points of the gap are keywords and 6 are the similarity half. Cause (language or role mix) not separated yet. | answered |
| Q3 | Whose keywords are we fixing: yours only, or every candidate (a rule in the app, not a list you edit)? | Every candidate: the app should not depend on each person typing both languages | Accepted as recommended (owner, 2026-11-04). | answered |
| Q4 | What number would tell you it is fixed? | French and English postings of the same role within about 10 points on the replay, and the #4 job above the pick line | Accepted as recommended (owner, 2026-11-04). | answered |
| Q6 | Is "the cut" the inbox floor (35 by default), and is yours at 35? | Yes: the job missed it by 2 points; I read the value from your settings page, not from the database | Accepted as recommended (owner, 2026-11-04). The floor is 35 in the 29 Oct dump (`breadth.floor`); the settings page was not re-read. | answered |
| Q5 | Which directions do we take to the spec (not decided now): (a) the app adds the other-language equivalents to every keyword automatically (fixes the keyword half), (b) a bilingual list you edit, (c) the similarity half made language-aware: the reference text carries both languages and the scale is checked on French postings | Take (a) and (c) to the spec together, since the replay shows the gap in both halves; keep (b) as the fallback | Accepted as recommended (owner, 2026-11-04): (a) and (c) go to the spec, (b) is the fallback. | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- The app is bilingual and postings are mixed French and English (PRD_competitive_features F13): a fix must not hurt English postings or double count a term that is the same in both languages ("sales", "reporting").
- Adding keywords moves every candidate's scores, so the rescoring runs on all stored jobs: it must go through the runner and not read the hosted database for a measurement (cycle 001 and 002 Neon rules).
- Equivalents generated by hand or by a model can be wrong (false friends: "consultant", "manager", "contrat"). A wrong equivalent raises the score of the wrong jobs.
- Scores already stored and the AI reviews blended in them (`ai_weight`) will change after a fix; calibration (cycle 008) may need a new reading.

## Gate
- [x] All open questions answered or parked (Q1 to Q6 answered, 2026-11-04)
- [x] Goal and success measure confirmed by the owner ("Confirm, go to spec", 2026-11-04)
