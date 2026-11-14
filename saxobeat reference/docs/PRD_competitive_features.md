# PRD — Features learned from the competition

| | |
|---|---|
| **Status** | Agreed: open questions answered 9 October 2026 (§11); F13 (French + English interface) added as a result |
| **Date** | 9 October 2026 |
| **Author** | Vladimir (product), written with Claude |
| **Builds on** | [COMPETITION.md](COMPETITION.md) (market analysis), [PRD_multi_user.md](PRD_multi_user.md) (phases 1–6, built on 9 October 2026) |
| **Progress (20 Oct 2026)** | **Phases 7a, 7, 8 and 9 are built:** F13 (French + English interface), F1 (score breakdown), F2 (freshness and reposts), F3 (filtered-out summary), F5 (gone quiet and follow-ups), F4 (search breadth), F6 (employer history), F7 (focus jobs), F8 (what I sent), F9 (contacts from the LinkedIn export), F10 (pay, days at home and English read from the ad), plus a basic half of F11 (pipeline conversion and response times, now drawn as Sankey diagrams) and the personal **dream employers** list. Not built: F12 and the rest of F11 (by source, by focus job). Next in the agreed order: deploy to Render, then the alpha with a few friends, then phase 10. |
| **Scope** | The competitor features worth adopting, adapted to Saxobeat's model: employers' own career pages, rule-based scoring, Paris / Île-de-France, never applies on the user's behalf |

---

## Outstanding work (moved to SDLC cycles on 2026-10-29)

What this PRD still asks for is now tracked as cycles in `docs/sdlc/` ([the audit](sdlc/cycles/006-stale-docs/evidence/prd_audit_2026-10-29.md)). This PRD stays the product-level reference; the cycles carry the work.

- F12 VC portfolio boards: [013](sdlc/cycles/013-more-sources/intent.md)
- The rest of F11 (breakdowns, plain sentence): [012](sdlc/cycles/012-insights-depth/intent.md)
- Focus cap 1-5, breadth preview counts, French amounts (F13): [011](sdlc/cycles/011-settings-polish/intent.md)
- F2 spot-check and ingest time, F10 sample of 100, §12 measures: [007](sdlc/cycles/007-success-measures/intent.md)
- Pages under 2 s hosted (§8): [004](sdlc/cycles/004-hosted-checks/intent.md)
- Stale header and §8 'nothing sends an email': [006](sdlc/cycles/006-stale-docs/intent.md)
- §10 'Later' (MCP connector, commute view, autofill, questions per stage), F10 transposition check: [the backlog](sdlc/backlog.md)

---

## 1. Context

The competition analysis found two advantages that no rival has for Paris:
- **Supply:** employers' own career pages, read directly and deduplicated.
- **A score that can explain itself,** because it is computed by rules, not by an AI model.

It also found that the best products are ahead on four things:
- explaining *why* a job fits;
- flagging stale and reposted jobs;
- keeping applications moving after they are sent;
- using the candidate's own network.

Most of the data needed already exists in Saxobeat:

| Already in the code | Where |
|---|---|
| Score parts: keyword score, profile similarity, seniority adjustment, matched keywords; a "Why this score" panel | `Score`, `services/scoring.py`, `detail.html` |
| First seen / last seen per job and per source; closed and reopened jobs | `Job.first_seen_at`, `Job.expired_at`, `JobSource`, `services/ingest.py` |
| The reason a hard filter hid a job, and a view of hidden jobs | `CandidateJob.hidden_reason`, "Filtered & archive" |
| Follow-up dates that turn red in the pipeline; applied date; CV version as free text | `CandidateJob.follow_up_at`, `applied_at`, `cv_version` |
| Salary fields from sources that give them; minimum-salary filter | `Job.salary_*`, `filters.py` |
| Company profiles keyed by cleaned employer name | `Company`, `employers.clean_name` |
| Paris area with La Défense, Boulogne, Issy… and postcodes 75/92/93/94 | `cities.py` |
| Learning from decisions (block/boost suggestions) | `services/insights.py` |

So most of this PRD is about **showing** what the app already knows, plus three new pieces of data: missing keywords, reposts, and the candidate's contacts.

## 2. Goals

1. **Trust the score:** every score explains itself in one glance: what matches, what is missing, and a verdict.
2. **Spend attention on live, real jobs:** new, reposted and closed jobs are obvious.
3. **Fewer, better applications that don't stall:** nothing sent is forgotten, and the few jobs that matter get full preparation.
4. **Use the network:** show who the candidate knows at each employer, from their own data.
5. **Keep every principle intact:** no auto-apply, no AI needed, no scraping of LinkedIn, everything per candidate.

## 3. Out of scope

- Auto-apply, bulk emails to recruiters, form autofill (Simplify-style autofill may come much later; see §10).
- Looking up recruiters' personal data from third-party databases (NextRaise "Find HR"): a GDPR risk in France.
- Any automation inside LinkedIn.
- AI-generated text (letters, tailored CVs). The existing "export for an agent" files stay the way to get AI help.
- Payment and pricing (COMPETITION.md §6.5 has notes for later).
- Mobile app, browser extension (the bookmarklet stays).

## 4. Users

Same roles as the multi-user PRD:
- **Candidates** (10–30, by invitation) get every feature below in their own space.
- **The operator** gets one source feature (F12).

All candidate data is per candidate (`CandidateJob`, `Config`, new per-candidate tables). Catalogue facts (reposts, salary, work mode) are computed once on `Job` and shared.

## 5. Features

Each feature lists the competitor it comes from, what the user sees, the rules, the data, and acceptance criteria. Sizes: S ≤ 1 day, M 2–4 days, L a week or more.

### Wave A — Explain and freshen (small, mostly on existing data)

#### F1. Score breakdown: matches, gaps, verdict — *S/M*
*Built 13 Oct 2026.* `scoring.analyse_keywords` returns what the score was made of; `Score` stores `missing_keywords`, `excluded_hits`, `title_hits` and `key_counts` (migration 0024; older scores show the new blocks once they are scored again: *Settings → Rescore*). The job page shows the verdict (≥ 70 strong, ≥ 45 good, below weak; "based on your keywords and profile, no AI"), the count line ("6 of your 9 key words · keywords · profile similarity · level"), and Matches (with "in title" and level words), Missing (key words of weight ≥ 3, strongest first, at most 8) and Against (excluded words and the level words, e.g. title says “junior”: −15). With an AI review its scorecard stays first and the breakdown folds below it. The inbox row names the top 2 matches and the top missing word. Words found only in an employer's boilerplate count as missing, so a word is never both. Tests: `tests/test_phase7.py`.
*Seen at:* NextRaise ("22 of 31 skills", top gaps), AIJobmatch (Key matches / Areas for growth), LinkedIn Job Match, Useful Apply fit check.

**What the user sees**
- On the job page, the "Why this score" panel becomes three short blocks plus a verdict:
  - **Matches:** matched keywords, strongest first. Title hits are marked "in title".
  - **Missing:** the candidate's keywords of weight ≥ 3 that the posting does not mention, strongest first, at most 8.
  - **Against:** excluded keywords found, and the seniority signal ("title says Junior: −10").
  - **Verdict:** *Strong fit* / *Good fit* / *Weak fit*, from the score bands already used for colours (≥ 70, ≥ 45, below). The verdict has no AI behind it and says so: "based on your keywords and profile".
- A count line: "6 of your 9 key words · profile similarity 62 · level fits".
- In the inbox row, on hover or a second line: the top 2 matches and the top missing keyword.

**Rules**
- "Missing" uses the same matching as the score: normalised text, whole words, and the employer's boilerplate ignored. So a keyword is never shown as both matched and missing.
- When an AI review exists, its scorecard stays the main view; the rule-based breakdown folds below it.

**Data**
- `Score.missing_keywords` (JSON list) and `Score.excluded_hits` (JSON list), filled by `keyword_score` at scoring time.
- Re-scoring after a profile change refreshes them (it already re-scores on `profile_version`).

**Acceptance**
- For 20 sampled jobs, every keyword appears in exactly one of Matches / Missing / Against, or in none.
- The verdict always matches the score band.
- No extra queries on the inbox page beyond the score already loaded.

#### F2. Freshness badges: new, reposted, closed — *M*
*Built 13 Oct 2026.* `services/freshness.py`; `Job.repost_key`, `repost_of`, `repost_count`, `first_listed_at` (migration 0024). Checked as each new job is stored (ingest); `manage.py backfill_reposts` does the existing catalogue (5 seconds on 26,000 jobs; 26 reposts found so far, since the history is short). The earlier posting must be 7 to 180 days older and closed, or not listed for 2 days (the employer re-created it under another id); two open postings of one role at once are not reposts. Badges on the inbox row, the job page and the pipeline cards: *new* (48 h), *open N days* (over 30), *reposted ×N* (hover: first listed), *closed*. Inbox: "Hide reposts", "Newest first", and a posting that has closed leaves the inbox. `purge_old_jobs` keeps the first job of a chain while a later one remains. Not yet measured: the 50-badge precision spot-check, which needs a catalogue with more history.
*Seen at:* Jobright (claims to filter fake and stale jobs), Useful Apply (drops "three-week-old reposts"), JobCopilot criticised for ghost jobs.

**What the user sees**
- **New:** first seen in the last 48 hours.
- **Open N days:** days since the employer first listed it, or since first seen. Shown when over 30 days ("open 45 days").
- **Reposted ×N:** the same employer listed the same role before (see rules), with "first listed 12 Aug" on hover.
- **Closed:** gone from the employer's site (`expired_at` set). The job stays in the pipeline with a grey "closed" tag. In the inbox, closed jobs drop out unless already acted on.
- **Inbox controls:** "Hide reposts" toggle and a "Newest first" sort.

**Rules**
- **A repost** is a new `Job` whose cleaned employer name and normalised title equal those of an earlier job first seen 7–180 days before. The earlier job must be closed, or listed under another external id.
- **Same title at the same employer in two cities** (two open postings at once) is *not* a repost.
- **Date shown:** the employer's own posting date when the source gives one; otherwise first seen.

**Data (shared catalogue)**
- `Job.repost_of` (FK to the earliest job, nullable), `Job.repost_count`, `Job.first_listed_at` (earliest first-seen across the chain).
- Computed at ingest for new jobs, with an index on (cleaned company, normalised title).
- A one-off backfill command.
- Retention (`purge_old_jobs`, 90 days) keeps the chain's earliest job while a later one exists.

**Acceptance**
- Spot-check 50 badges: ≥ 90% correct.
- Ingest time per run grows by under 10%.
- Backfill runs in under 5 minutes on the current catalogue.

#### F3. Filtered-out view, with counts and "loosen" — *S*
*Built 13 Oct 2026.* "Filtered out & archive → Auto-hidden" opens on a summary grouped by stored reason (one query; the top 8 reasons, then "other reasons"), each with the count, **see them** (`?reason=`) and **loosen** (Settings, at the field of that rule). The label says "Filtered out: N", not "this week": the app does not record when a job was hidden.
*Seen at:* LoopCV "Rejected matches".

**What the user sees**
- "Filtered & archive" opens on a summary: "Hidden this week: 212 — location 140 · language 41 · older than 60 days 20 · blocked word 'intern' 11".
- Each line has **see them** (filters the list) and, where it makes sense, **loosen** (opens Settings at that rule).
- Each hidden job still shows its reason (already there).

**Data:** none new; a grouped count on `CandidateJob.hidden_reason` by reason type (text before the colon).

**Acceptance:** the counts add up to the hidden total; one query per page.

#### F4. Search breadth: Strict / Balanced / Broad — *S/M*
*Built 16 Oct 2026.* `services/breadth.py` (it stores nothing of its own: it writes `min_score`, the `ile_de_france` city, `remote_france` and `seniority_factor` in `Config.filters` and reads them back to say Strict / Balanced / Broad / Custom). The dial is in Settings (with the table) and as a compact switch above the inbox; clicking it saves the four settings and re-runs the filters and scores in the background (`matching.recompute_in_background`). The inbox hides jobs under the floor (35 by default) unless Min score is typed in the bar; they are under **Low score** in the archive, which now means "below your floor". New `ile_de_france` city (77, 78, 91, 95 and about fifty towns) and `cities.in_france`.
*Seen at:* Useful Apply (Strict / Balanced / Broad), LoopCV (Low / Middle / High).

**What the user sees**
- One three-way control at the top of Settings (and a compact switch in the inbox). It sets presets; the detailed settings stay below for anyone who wants them.

| | Strict | Balanced (default) | Broad |
|---|---|---|---|
| Inbox score floor | 55 | 35 | 0 |
| Area | Paris + inner suburbs (today's Paris list) | same | **Whole Île-de-France** (adds postcodes 77, 78, 91, 95 and their main towns: Versailles, Saint-Quentin-en-Yvelines, Massy-Saclay, Cergy, Marne-la-Vallée…) |
| Remote elsewhere in France | no | no | yes |
| Seniority penalty | full | full | halved |

**Rules**
- **Changing the dial re-runs the candidate's filters** (no scraping); it takes effect at once.
- **Editing a detailed setting** shows the dial as "Custom".

**Data**
- `Config.filters["breadth"]`.
- A new `ile_de_france` area in `cities.py`, next to `paris`.
- A score floor in the filters; today `min_score` exists only as a URL parameter.

**Acceptance**
- Switching Strict → Broad → Strict returns exactly the original inbox.
- An Île-de-France-only test job (e.g. "Guyancourt, 78") is hidden in Strict and shown in Broad.

### Wave B — Follow-through

#### F5. "Gone quiet" and a follow-up nudge — *S*
*Built 13 Oct 2026.* `services/followup.py`; `CandidateJob.followups` (migration 0024). Marking a job Applied sets the follow-up date to +7 days; Settings → Follow-ups holds both delays (7 and 10 by default, empty or 0 = off). The pipeline has a **To do** strip (gone quiet first, then follow-ups due, then interviews in the next 48 hours; three queries, no job text) and a "gone quiet" tag on cards. On an applied job: *Draft a follow-up* (a built-in French or English message in the posting's language, with a switch, copy button), *Download for an agent* (`?for=followup`, the same posting-language rule as the other agent files), *I followed up* (history note, next nudge a week later) and, after two follow-ups, *No reply: mark as rejected*.
*Seen at:* Useful Apply ("gone quiet", follow-up email), Huntr, Careerflow.

**What the user sees**
- **When a job is marked Applied** and has no follow-up date, the date is set to applied + 7 days (adjustable in Settings; blank = off).
- **Gone quiet:** an application with no status change and no interview after 10 days gets a "gone quiet" tag in the pipeline. It moves to the top of a **"To do"** strip above the pipeline columns, together with follow-ups due and interviews in the next 48 hours.
- **Follow-up help:**
  - "Draft follow-up" downloads a short handoff file for an agent (same mechanism as the screening-answers file in `briefing.py`): the posting, the date applied, the stage, and instructions for a polite two-line follow-up in the posting's language.
  - Alternatively, a plain built-in template (French and English) with the company, role and date filled in, ready to copy. No AI needed.
- **"Followed up"** records a note in the status history and sets the next follow-up 7 days later. After the second follow-up, the app suggests "mark as no reply → Rejected".
- **A month of silence (built 3-4 Nov 2026, cycle 019, `services/auto_reject.py`):** an Applied job with no change for more than the delay (one global value in the operator console, `/ops/auto-reject/`, default 30, 0 = off; counted from `status_changed_at`, follow-ups do not reset it) is moved to Rejected by the PC runner's `auto_reject` step, unless it has an interview stage or is a focus job. It gets the tag **Auto-rejected** (`CandidateJob.auto_rejected_at`) on the card and the job page, an info box with **Put back to Applied** (which restarts the month), a history line "no answer after N days (automatic)", and a 7-day banner on the pipeline with the count. Insights show these apart as **No answer**: they are not counted as rejections and are not an employer's answer in the delay to rejection.

**Data**
- `CandidateJob.followups` (small integer).
- Gone-quiet is computed from `status_changed_at` and interviews; nothing else is stored.

**Acceptance**
- An application dated 11 days ago with no change shows "gone quiet".
- Adding an interview stage clears it.
- The To-do strip loads in one query per list.

#### F6. Employer history on every job — *S*
*Built 16 Oct 2026.* `services/employer_history.py`: one `Book` per request holds the candidate's engaged jobs (one query) and every employer is looked up in it. Job page: "You applied to X before: …", other shortlisted jobs, and an amber warning when an application to the same employer is under six months old (183 days) and this job is not applied yet. Inbox and archive rows carry a small tag (↺ applied 12 Aug, ★ n shortlisted). The company page already listed every job with its status.
*Seen at:* LoopCV (never applies to the same company twice within 6 months).

**What the user sees**
- On the job page and inbox row, when the candidate has history with this employer: "You applied to Qonto on 12 Aug (Senior PM, rejected 3 Sep) · 2 other jobs shortlisted".
- An amber warning when an application to the same employer is under 6 months old: "Recruiters may see both applications". It is a warning, not a block.
- The company page lists every job of that employer with the candidate's status.

**Data:** none new; grouped by `employers.clean_name` over the candidate's `CandidateJob`s.

**Acceptance:** shown for exact and cleaned-name matches ("Qonto SAS" = "Qonto"); one extra query per page, not per row.

#### F7. Focus jobs (a capped "dream job" flag) — *S/M*
*Built 16 Oct 2026.* `services/focus.py`; `CandidateJob.focus_at` and `referral_asked` (migration 0027). Three at most among live jobs (shortlisted, applied, interviewing, offer): a closed application keeps its flag but frees its slot. The count is made with the candidate's row locked. A fourth click offers the three to replace. The Pipeline has a **Focus** lane with the checklist: company profile written, cheat sheet started, CV copy kept, referral asked (manual tick), applied. The "a contact found" step arrives with F9. Focus jobs come first in the To do strip. The agent exports hold only new jobs, which cannot be focus jobs, so there was nothing to reorder there.
*Seen at:* Greenhouse "My Dream Job" (one a month; those applicants are hired about 5× more often).

**What the user sees**
- A ★ **Focus** action on shortlisted or applied jobs.
- **Limit:** at most **3 active focus jobs** per candidate; a fourth asks which one to drop.
- **Focus jobs have their own lane** at the top of the pipeline, with a preparation checklist that ticks itself from existing data:
  - company profile written;
  - cheat sheet started;
  - CV version recorded (F8);
  - a contact found (F9);
  - referral asked (manual tick);
  - applied.
- Focus jobs are listed first in the To-do strip and in the agent exports.

**Data:** `CandidateJob.focus_at` (datetime, null = not focus); the checklist is computed.

**Acceptance:** the cap holds under concurrent clicks; un-focusing keeps all data.

#### F8. What I sent: application packet — *S*
*Built 16 Oct 2026.* `ApplicationPacket` (migration 0026), one per job: a copy of the CV text and the letter, with the job's `channel`. An applied job offers **Keep a copy of what you sent**; the job page then reads "What I sent: CV of 12 Aug · letter · via LinkedIn" with a page to view, edit the letter, replace the CV copy or delete it. The agent files (screening answers, follow-up, cheat sheet) carry "What the candidate sent" when a copy exists. It is part of backups, and deleted with the account.
*Seen at:* Huntr "application packets".

**What the user sees**
- Marking a job Applied offers to **keep a copy of what was sent**:
  - the current CV, snapshotted from My CV;
  - an optional cover letter or message (pasted text);
  - the channel (already a field).
- The job page shows "Sent: CV of 12 Aug · letter" with a view link.
- The cheat sheet skeleton and the agent exports use the snapshot, not today's CV.

**Data**
- New `ApplicationPacket` (candidate_job, cv_markdown, letter, created_at). Text only, no files.
- The free-text `cv_version` field stays for older applications.

**Acceptance**
- Editing My CV after applying does not change the packet.
- Deleting the account deletes packets (cascade, covered by the existing delete-me test pattern).

### Wave C — Reach and signals

#### F9. My contacts at each employer (from my LinkedIn export) — *M*
*Built 20 Oct 2026.* `Contact` (migration 0029), `services/contacts.py`, `views_contacts.py`. **Contacts** page (from Companies → *My contacts*): the three steps to get the export, upload, how many contacts were read and how many are at an employer the app has jobs from, the employers with the most contacts, replace (a new file replaces the old one) and delete. The file is read past LinkedIn's notes lines, the email column is never read, dates in English or French. A `Book` per request finds contacts by employer in one query (same cleaned name, or one name is the other's leading words: "BNP Paribas" / "BNP Paribas CIB"; no alias table was needed). Job rows show *2 contacts*; the job page and the company page list name, position, date connected and the LinkedIn link (opened by the candidate); **Ask for a referral** opens an editable message in the posting's language (switchable) with copy, and *I asked for a referral* ticks the focus checklist. A focus job's checklist gains *A contact found*. Contacts are not in backups, and go with the account.
*Seen at:* Jobright Insider Connections, NextRaise referrals. Referrals produced about a quarter of cadre hires in 2025 (APEC).

**What the user sees**
- A **Contacts** page:
  - **Upload.** The candidate uploads `Connections.csv` from LinkedIn's own *Get a copy of your data* export. The page explains how to get it, in 3 steps.
  - **What it shows:** how many contacts were read and how many match an employer in the catalogue.
  - **Replace and delete:** buttons for both.
- **Badges:** jobs and company pages show **"2 contacts"**. A click lists name, position and the date connected, with a link to their LinkedIn profile, opened by the candidate.
- **"Ask for a referral":** fills a short, editable message (French or English) with the contact's first name, the role and the job link, ready to copy. The app sends nothing.

**Rules**
- **Matching:** the contact's *Company* goes through `employers.clean_name`, then is compared to the job's cleaned employer name. An alias list per company handles names like "BNP Paribas CIB" / "BNP Paribas".
- **Only this export:** the app never visits LinkedIn and never enriches contacts from any other source.

**Data and privacy**
- **Storage:** new `Contact` (candidate, first name, last name, profile URL, company, cleaned company key, position, connected_on). Email addresses in the export are **not stored**.
- **Privacy:** private to the candidate. Not in the operator's views, not in backups shared outside the candidate's export, deleted with the account.
- **Third parties:** these are other people's personal data, uploaded by the candidate for their own use. The privacy note says so. A re-upload replaces the previous set.

**Acceptance**
- A 1,000-line export imports in under 5 seconds.
- Email columns are dropped.
- A second candidate never sees the first one's contacts (leak test on every new view).

#### F10. Salary and work-mode signals — *M*
*Built 20 Oct 2026.* `services/signals.py` (patterns, French and English); `Job.salary_source`, `Job.remote_days`, `Job.english` (migration 0028); computed when a job is stored and when a page or a pasted text brings a description, and for the existing jobs by `manage.py backfill_signals [--all]` (run on the dev database: 28,822 jobs, 5,781 with a pay read from the text). The source's own pay always wins; a pay read from the text says *from the ad*. Chips on rows and job pages (pay, *2 days remote* / *hybrid* / *full remote*, *English-speaking*); inbox filters *Salary stated* and *English-speaking*; the company page lists the pay seen in the last 12 months (other people's private jobs left out). The salary filter now also sees the pay read from the text. Precision: the hand-labelled sample in `tests/test_signals.py` (about 40 pay texts, 40 remote texts, 14 English ones) is gated at 95 % precision for pay, and two random samples of the real ads were read by hand to remove false readings (a deal size, `401K`, a schedule, "remote-first", "unless posted as fully remote").
*Seen at:* Jobright (H-1B filter), LinkedIn and Indeed salary insights, Hired (salary up front). The EU pay-transparency directive should put more salary ranges in French ads; France's transposition status is unverified.

**What the user sees**
- Chips on rows and job pages:
  - **€55–65k** (shown "from the ad" when parsed from the text);
  - **2 days remote** / **hybrid** / **full remote**;
  - **English-speaking**.
- **Inbox filters:** "salary stated" and "English-speaking".
- **Company pages:** the salary ranges seen for that employer in the last 12 months.

**Rules (deterministic extraction from the description, French and English)**
- **Salary:** "45-55 k€", "45 000 € – 55 000 € bruts annuels", "€60,000–€70,000", "jusqu'à 80K". Ignore "selon profil" and package words with no number. Monthly and daily rates are converted with the existing period table. The source's own salary fields win when present.
- **Remote days:** "2 jours de télétravail", "télétravail partiel", "hybrid (3 days in office)", "full remote".
- **English-speaking:** the job's language is English, or "anglais courant / fluent English / English-speaking environment".

**Data**
- `Job.salary_source` (source | text).
- `Job.remote_days` (small integer, null).
- `Job.english` (boolean, null).
- All computed at ingest and by a backfill.

**Acceptance**
- Precision ≥ 95% on a hand-labelled sample of 100 French and English ads (salary and remote days). Recall is reported, not gated.

#### F11. Results by stage and source (outcome funnel)
*Status (13 Oct 2026): the first half is built as a basic dashboard on Insights (conversion from stage to stage, where applications stand, and response times: median, fastest, slowest to a first answer, an interview and a rejection, plus how long the unanswered ones have waited, with a caution under 15 applications). The split by source and by focus job is still to do.* — *M*
*Seen at:* Teal advanced metrics, Careerflow search analytics.

**What the user sees**
- An **Outcomes** block on Insights:
  - **Funnel:** applied → answered (any change after Applied) → interview → offer, with counts and rates.
  - **Breakdowns:** by score band (≥ 70 / 45–70 / below), by source kind (employer site / job board / my captures), by channel, by company size when known.
  - **Response time:** median days from applied to first answer.
- **One plain sentence on top**, e.g. "Your 70+ jobs get an answer 3× as often as the rest", shown only when at least 15 applications back it.

**Data:** none new: `StatusChange`, `Interview`, `CandidateJob`, `JobSource`.

**Acceptance:** numbers match a hand count on the operator's own history (60 applications); a candidate with fewer than 15 applications sees counts but no sentence.

### Interface language

#### F13. French and English interface — *L*
*Decided 9 Oct 2026 (§11, question 7).* Not taken from a competitor, but every French player (WTTJ, HelloWork, APEC) is in French, and the alpha users are Paris-based.

**What the user sees**
- **Candidate space in both languages.** Every candidate page, message, email and error page exists in French and English.
- **Choosing the language:**
  - a FR / EN switch in the header and in Settings;
  - the choice is saved on the account;
  - before login, the browser's language decides.
- **Formats follow the language:** dates ("12 août" / "12 Aug") and numbers ("55 000 €" / "€55,000").
- **Content follows the posting, not the interface.** Message templates (F5 follow-up, F9 referral request), the agent handoff instructions and the cheat-sheet skeleton default to the posting's language, with a switch to the other one. Postings themselves are never translated.

**Rules**
- **Scope:** the candidate space, login, sign-up, password reset, invitation and error pages. The operator space (sources, runs, radar, AI review, backups) stays English; it has one user.
- **Text written by the app inside data** must be stored as a code, not as English text, so it can be shown in either language. This covers hidden-job reasons (`hidden_reason`, e.g. "location not in Paris"), score verdicts, freshness badges and status names. Existing stored reasons are migrated to codes.
- **Translation is part of building each feature.** From the moment F13 lands, a candidate-facing feature counts as done only when it exists in both languages. A test fails when a catalogue string has no French translation.

**Data**
- `Candidate.language` (`fr` | `en`, default from the browser at sign-up).
- `CandidateJob.hidden_reason` becomes a code plus parameters (e.g. `{"code": "location", "cities": ["paris"]}`).
- Django translation catalogues (`locale/fr/LC_MESSAGES`).

**Built on 13 October 2026 (phase 7a).**
- **Language choice:** `Candidate.language` (blank follows the browser). Order: the signed-in person's saved choice, the `saxobeat_lang` cookie (login page, before login), the browser's `Accept-Language`, English. FR / EN pill in the header, and in Settings; `POST /language/` saves it on the account and in the cookie. A person who joins by invitation gets the language the invitation was opened in. `jobs/language.py`.
- **Catalogue:** Django gettext, `locale/fr/LC_MESSAGES/django.po` plus the compiled `django.mo` (committed, so the image needs no tooling). GNU gettext is not installed on Windows, so `manage.py i18n extract | compile | missing` does the work with Babel (a development dependency). 686 strings.
- **Everything in the candidate space is translated:** all candidate templates, error pages (404, 500, expired form), login, join, password reset, account deletion, the first-steps flow, the messages and validation errors in the Python code, the CV health check (labels, details, actions), insights texts, status names, dismissal reasons and interview choices (stored values stay English codes; only the display is translated).
- **Reasons stored as codes:** `CandidateJob.hidden_reason` is now `{"code":"location","places":"Paris"}`-style JSON (`jobs/reasons.py`); migration `0022` converts existing values (the real database: 37,000+ rows, none left unconverted) and reverses. Old texts in imported backups are still understood. The app's own history notes ("restored", "moved in pipeline"…) stay English in the database and are translated when shown.
- **Content follows the posting:** the cheat-sheet skeleton, the agent files (application, cheat sheet), the calendar event text and the bookmark's own messages are written in the posting's language (`Job.language`, else the interface language) with `translation.override`; the cheat-sheet "Start again" form and `?lang=fr|en` on the download let the person pick the other one. The company briefing follows the interface language (a company has no posting).
- **Guards:** `tests/test_i18n.py` fails when a string marked in the code is missing from the catalogue, when a translation lacks French or loses a placeholder or tag, when the `.mo` is stale, when a candidate page carries English words or an untranslated catalogue sentence in French, and when a posting-language rule breaks.
- **Left English on purpose:** the operator space (Sources, Runs, Jungle radar, AI review, Data, People) and the Django admin; CSV export column names; text written by an AI review; job postings, company names and the person's own notes. **Not done:** number and currency formats (nothing in the interface prints a currency amount: salaries are shown as the source wrote them), and the follow-up template (F5) and referral template (F9), which will use the same posting-language mechanism when built.

**Acceptance**
- Every candidate page renders in both languages with no untranslated string (checked by a test that walks the candidate URLs in French).
- Switching language changes the interface at once and leaves postings and the user's own notes untouched.
- A follow-up template for an English posting opens in English even when the interface is French.
- The operator space is unchanged.

### Operator

#### F12. VC portfolio job boards as a source type — *M*
*Seen at:* AIJobmatch, which reads 13 VC portfolio boards.

**What it is**
- A source adapter for portfolio job boards: most run on Getro or Consider, which publish structured job lists.
- Examples with many Paris companies: Partech, Eurazeo, Serena, Elaia, Index Ventures, Accel, Balderton.

**Rules**
- **Same politeness as every source:** robots.txt, rate limits, no evasion.
- **Deduplication:** jobs of employers already read directly are merged by the usual key; the employer's own board stays the preferred link.
- **Discovery:** a board can reveal employers worth adding as direct sources (like the WTTJ radar).

**Acceptance:** one Getro board and one Consider board run cleanly; duplicates with direct sources are merged; the run appears in the operator's Sources page with counts.

## 6. Data model changes (summary)

| Table | Change | Feature |
|---|---|---|
| `Score` | `missing_keywords`, `excluded_hits` (JSON) | F1 |
| `Job` (shared) | `repost_of`, `repost_count`, `first_listed_at` | F2 |
| `Job` (shared) | `salary_source`, `remote_days`, `english` | F10 |
| `Config.filters` | `breadth`, `min_score` | F4 |
| `CandidateJob` | `followups`, `focus_at` | F5, F7 |
| new `ApplicationPacket` | per candidate job | F8 |
| new `Contact` | per candidate | F9 |
| `cities.py` | `ile_de_france` area | F4 |
| `Candidate` | `language` (`fr` / `en`) | F13 |
| `CandidateJob` | `hidden_reason` stored as a code + parameters, existing values migrated | F13 |
| `locale/fr/` | translation catalogues; `USE_I18N = True`, locale middleware | F13 |

Rules:
- All migrations reversible.
- Backfills are management commands, run from the operator's PC like the source runner.
- No new table without a candidate owner, except catalogue facts on `Job`.

## 7. Phases

| # | Phase | Features | Size | When |
|---|---|---|---|---|
| 7a | **Language foundation** *(built 13 October 2026)* | F13: translation set-up, language switch, reasons stored as codes, then every existing candidate page in French | L | **Before the alpha** (decided) |
| 7 | **Explain and freshen** | F1, F2, F3, F5 (built in both languages) | M | **Before the alpha** (decided); F1 and F2 at least |
| 8 | **Focus and follow-through** | F4, F6, F7, F8 | M | After the first alpha feedback |
| 9 | **Network and signals** | F9, F10 | M–L | After phase 8 |
| 10 | **Learning** | F11, F12 | M | When candidates have ~15 applications each; F12 whenever source work is next |

**Why this order.**
- **Phase 7a comes first** because every later feature adds candidate-facing text; translating as we build costs far less than translating everything afterwards. It also moves stored reasons to codes before more of them pile up.
- **Phase 7 needs almost no new data** and answers the two questions every new user asks: "why this score?" and "is this job real?".
- **Phase 8 shapes how people apply,** which is worth checking with alpha users first.
- **Phase 9 adds personal data (contacts),** so it waits until the privacy basics have run for a while.
- **Phase 10 needs history** to mean anything.

## 8. Acceptance (whole PRD)

- Every feature above meets its own criteria.
- The full test suite stays green on Postgres, and each feature adds tests: unit tests for rules, and a view test proving one candidate cannot see another's data.
- No candidate page gets slower than 2 s on the hosted setup; the inbox query count does not grow per row.
- Nothing in these features contacts LinkedIn, sends an email, or submits an application.

## 9. Privacy and risks

| Risk | Mitigation |
|---|---|
| Contacts are third parties' personal data (F9) | Only from the candidate's own export; minimal fields, no emails; private; deleted with the account or on re-upload; stated in the privacy note |
| Repost detection marks a real new role as a repost (F2) | Conservative rule (same employer + same title, earlier one closed or different id); a hover shows the evidence; it only labels, never hides by default |
| Salary extraction picks the wrong number (e.g. company revenue) (F10) | Require a currency or "k€"/"K" plus a salary context word nearby; "from the ad" label; precision gate before release |
| The breadth dial surprises users by changing many settings (F4) | Preview of how many jobs each position shows; "Custom" state; reversible |
| Focus cap feels arbitrary (F7) | Explained in one line with the Greenhouse figure; cap adjustable in Settings (1–5) |
| Feature creep toward AI writing | Out of scope; agent export files remain the route |

## 10. Later, not in this PRD

- **Connector for Claude (MCP):** read inbox, pipeline and company profiles from a Claude session. It replaces the file exports for AI reviews and cheat sheets. *Seen at:* LoopCV.
- **Commute view:** travel time from home by RER/metro as a filter or score input. *Seen at:* Huntr map view.
- **Assisted autofill,** where the candidate clicks Submit. *Seen at:* Simplify.
- **Interview question list** per stage from the posting and company profile (could join the cheat sheet earlier if cheap).
- **Grounding rule for any future AI writing:** facts come only from the CV. *Seen at:* Useful Apply "zero fabrication".

## 11. Decisions (answered 9 October 2026)

| # | Question | Decision |
|---|---|---|
| 1 | Phase 7 before the alpha? | **Yes** (F1 and F2 at least). |
| 2 | Focus cap | **3 active, adjustable 1–5.** |
| 3 | Gone-quiet delay and automatic follow-up date | **Follow-up at applied + 7 days, "gone quiet" at 10 days, both adjustable; blank turns them off.** |
| 4 | Broad = whole Île-de-France + remote anywhere in France? | **Yes:** Broad covers all of Île-de-France, and remote roles elsewhere in France only in Broad. |
| 5 | Contacts upload (F9): hold contacts' names and positions? | **Yes,** minimal fields, no emails, private (§9). |
| 6 | Follow-up help | **Both:** built-in template and agent file. |
| 7 | Language | **The interface offers French and English** (new feature F13, phase 7a). Everything else — message templates, agent instructions, cheat-sheet skeleton — **defaults to the posting's language**. |

Defaults taken for F13 (say if any should change):
- **Operator space stays English.** It has one user.
- **First language:** the browser's language at sign-up; changeable at any time.
- **Postings are never translated.** Neither are the user's own notes.

## 12. Success measures

- **Trust:** in the alpha, at least 4 of 5 users say the score explanation is clear (short survey after two weeks).
- **Freshness:** fewer than 1 in 10 shortlisted jobs turn out closed or stale when the candidate opens them (spot-check).
- **Follow-through:** at least 80% of applications older than 10 days have a follow-up or a final status.
- **Focus:** focus jobs get an interview at a higher rate than other applications (F11, once there is data).
- **Network:** at least half of the alpha users upload contacts; at least one referral asked per active user per month.

## 13. References in the repository

- Scoring: `jobs/services/scoring.py`.
- Score panel: `jobs/templates/jobs/detail.html`.
- Inbox row: `jobs/templates/jobs/_row.html`.
- Ingest and closed jobs: `jobs/services/ingest.py`.
- Retention: `purge_old_jobs`.
- Hard filters: `jobs/services/filters.py`.
- Areas: `jobs/cities.py`.
- Pipeline: `jobs/templates/jobs/pipeline.html`.
- Agent handoff files: `jobs/services/briefing.py`.
- Insights: `jobs/services/insights.py`.
- Employer names: `jobs/employers.py`.
- Company profiles: `Company` model.
- Market analysis behind each feature: [COMPETITION.md](COMPETITION.md) §7.
