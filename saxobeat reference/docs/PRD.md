# Saxobeat: Job Opportunity Tracker — PRD

Status: v0.1 (2026-09-29), updated 2026-10-12 · Owner: Vlad

## Outstanding work (moved to SDLC cycles on 2026-10-29)

What this PRD still asks for is now tracked as cycles in `docs/sdlc/` ([the audit](sdlc/cycles/006-stale-docs/evidence/prd_audit_2026-10-29.md)). This PRD stays the product-level reference; the cycles carry the work.

- Alert e-mail import, the `jobs.v1` format, the remaining aggregators, Personio, the legal review of sources, open question 6: [013](sdlc/cycles/013-more-sources/intent.md)
- Pages under 2 s on the hosted app, hosted backup retention: [004](sdlc/cycles/004-hosted-checks/intent.md)
- The inbox remote filter (§7.1): [011](sdlc/cycles/011-settings-polish/intent.md)
- Precision, recall and triage-time measures (§2): [007](sdlc/cycles/007-success-measures/intent.md)
- Stale statements (deployment, Render Postgres, Task Scheduler, rerun round, source lists): [006](sdlc/cycles/006-stale-docs/intent.md)
- Full-text search: [the backlog](sdlc/backlog.md)

---

> **This is the single-user product spec, and it still describes how the engine works** (sources, dedupe, filters, scoring, statuses). Since then the app became multi-user and hosted: where a section below says "single user", "SQLite", "Litestream" or "free tier", the current truth is in [PRD_multi_user.md](PRD_multi_user.md) (accounts, candidates, Postgres, Render, onboarding, suggested sources; phases 1-6 built), [DEPLOY.md](DEPLOY.md) (hosting) and [PRD_competitive_features.md](PRD_competitive_features.md) (next features, FR/EN interface). Those sections are marked *(superseded)* instead of rewritten, so the original reasoning stays readable.

## 1. Problem

My CV is atypical and spans many skill areas, so my job search has to be deliberately wide: many sources, many role titles, many keywords. A wide net produces a lot of noise. Checking each site by hand is slow, and I lose track of what I've seen, dismissed, or applied to.

## 2. Goal

A local, single-user app *(superseded: now a hosted multi-user app, see above)* that:

1. **Collects** job postings from many sources on a schedule, with no manual checking.
2. **Scores** each posting for relevance to me, so I only spend attention on the top of the list.
3. **Stores** everything needed to apply in the database (description, link, contact, deadline, etc.). *(Postgres now; SQLite only when `DATABASE_URL` is unset.)*
4. **Tracks** the state of every opportunity, from "new" to "offer" or "rejected", through a very simple UI.

### Success metrics

- **Triage time:** reviewing a day's new postings takes under 5 minutes.
- **Precision:** of postings scored ≥ 70, at least 60% are ones I'd shortlist (measured from my own dismiss/shortlist actions).
- **Recall:** fewer than 1 in 10 postings I'd have wanted are scored below the "hidden" threshold (spot-checked via a "show low scores" view).
- **Freshness:** a new posting appears in the app within 24h of publication, and within one refresh cycle of being scraped.
- **No lost applications:** every application has a status and a timeline.

### Custom first, product later

This is built for me first, with no compromise to my workflow. It may become a product, so a few cheap seams are kept from day one, and nothing else is built for a hypothetical customer:

- Everything personal (profile, filters, keywords, sources, weights) is **data in the DB or config**, never code.
- Sources, scorers and notifiers sit behind **interfaces**.
- No hardcoded paths, names or secrets.
- Deferred until it is a product: accounts and auth, multi-tenancy (a `user_id` column and per-user DB), billing, hosted scheduling, and a legal review of every source.
- **Update, 2026-10-12:** accounts, multi-tenancy and hosting are now built (phases 1-6 of the multi-user PRD). Still deferred: billing, public sign-up, and the legal review of every source.

## 3. Non-goals (v1)

- ~~Multi-user, accounts, auth, cloud hosting.~~ *Reversed: built in the multi-user PRD (invitation-only accounts, Render hosting; the Render deployment itself is not done yet).*
- Auto-submitting applications. The app helps me apply and does not apply for me.
- CV/cover-letter generation (candidate for v2).
- Scraping sites whose terms or bot-protection forbid it (see §5).
- Mobile app. A responsive page is enough.

## 4. User and context

One user (me), running the app locally on Windows. Data stays on my machine. The only outbound calls are to job sources and, for scoring, an LLM API.

*(Superseded.)* Today: the operator (me) plus 10 to 30 invited candidates, each with their own profile, filters, scores and pipeline over a shared catalogue. The app is meant to be hosted in the EU (web on Render), while the sources are still read from my PC. The app itself calls no LLM API.

## 5. Sources

Sources are **pluggable adapters** behind one interface: `fetch() -> list[RawPosting]`. New sources should take about an hour to add.

Two kinds of source, both first-class:

- **Employer sources:** a specific company (its ATS board or career page). I maintain the list of employers I care about.
- **Aggregation platforms:** job boards and search engines, queried with my search terms.

Priority order favors sources that expose **APIs, RSS or public JSON**. Those are stable and cheap. Sources without a feed are covered through **job-alert emails** (the platform sends me the alert, the app parses it) rather than by fighting their bot protection.

#### Shortlist (v1 scope)

France Travail was considered and dropped: its offers are not of the quality wanted.

| # | Source | Kind | Access method | Verdict |
|---|---|---|---|---|
| 1 | **Welcome to the Jungle** | Aggregator, startups/scale-ups | Its search index only accepts calls claiming to come from its own pages, and its job pages answer automated requests with bot protection, so neither is used. **Built:** discovery through its published job sitemap (title, company, city, date, no description), filtered by keywords, companies and cities. Alert emails for the rest | **Partial.** Switched off by default; open the link to read a job |
| 2 | **LinkedIn** | Aggregator | No public jobs API. Alert emails only in v1. Any scraper needs a login or hits bot detection and risks the account | **Must-have via alerts.** No credentialed scraping |
| 3 | **Indeed** | Aggregator | No public API for aggregators; alert emails | Via alerts |
| 4 | **APEC** | Aggregator, cadres/managers | No official API; alert emails | Via alerts. Important if targeting cadre roles |
| 5 | **Adzuna** (France) | Aggregator | Official API, free key (~1,000 calls/month) | Include: cheap breadth |
| 6 | **Jooble** | Aggregator | Official API, free key per country but small lifetime quota | Optional |
| 7 | **Careerjet** | Aggregator | Official partner API (affiliate ID) | Optional |
| 8 | **Hellowork** (ex-RegionsJob), **Cadremploi**, **Free-Work** (IT/freelance), **Malt** (freelance), **Les Jeudis** (tech), **JobTeaser** | Aggregators | Alert emails or RSS where offered | Add per need, all through the email parser |
| 9 | **Greenhouse / Lever / Ashby / Workable / Teamtailor / Workday / Oracle HCM** (built); SmartRecruiters / Personio (not yet) | Employers | Public board JSON/RSS per company. Workday and Oracle HCM are the big-corporate systems; both are narrowed with a search text such as "Paris" | **Built.** The most reliable feed. Probed and seeded for 23 employers (see below) |
| 10 | **Career page (generic)** | Employers | schema.org `JobPosting` JSON-LD adapter (listing links, then detail pages) | **Built.** For employers without an ATS feed. No per-site selectors |
| 11 | **Remotive, RemoteOK, We Work Remotely, Himalayas, HN "Who is hiring"** | Aggregators, remote | API/RSS | Cheap; on if remote roles are in scope |
| 12 | **Public sector** (Place de l'emploi public, Choisir le service public) | Aggregators | Alert emails / RSS | Only if relevant to me |
| 13 | **Manual add** | Either | Paste a URL | **Built.** JSON-LD if present, else the page text. A job added on purpose is never auto-hidden |

#### Alert emails, without giving the app my mailbox

Some platforms (LinkedIn, WTTJ, APEC, Indeed) offer no feed, only alert emails. The app does **not** get standing access to my mailbox. Three ways to use those alerts, from least to most access:

1. **Upload or paste (recommended first).** I save or forward an alert email and drop the `.eml`/`.html` file (or pasted text) on an "Import alerts" page. Per-sender parsers pull the jobs out. The app sees only what I hand it, when I hand it.
2. **A supervised Claude session (same hand-off as the AI review).** A Claude Cowork/Claude Code session with my own Gmail connector reads the alert emails while I watch, and writes an import file (`saxobeat.jobs.v1`: title, company, location, link, description if the email has it). I import that file. The app never touches email, and I see what is read.
3. **A forward-only mailbox (optional).** A Gmail filter forwards only the alert senders to a separate address. The app reads only that mailbox over IMAP with an app password. It cannot see my main inbox. Not planned unless 1 and 2 prove too manual.

Alert emails carry a title, company, location and link, not the full description, so imported alerts are scored on that, and the AI review can be given the link to read.

#### Employers seeded (feeds probed and confirmed)

`manage.py seed_employers` adds 24 sources (23 employers plus eFinancialCareers). Start-ups and scale-ups: Mistral AI, Hugging Face, Dataiku, Pigment, Dust, Contentsquare, Qonto, PayFit, Swan, Ledger, Spendesk, Lydia Solutions (Sumeria), N26, Adyen, Celonis, Swile, EPI Company (Wero), Mambu (iCIMS, read as a career page), Temenos (Workday). Banks: Citi and Barclays (Workday, Paris), JPMorgan Chase and Lazard (Oracle HCM, Paris).

**No usable feed** (their hiring systems are closed or block automated requests): Revolut and Finacle (block requests), Allianz (Phenom), AXA, BNP Paribas, Crédit Agricole, Société Générale (Taleo), BPCE/Natixis, Bpifrance, HSBC and Bank of America (Avature), Goldman Sachs, Morgan Stanley, UBS, Deutsche Bank, Crédit Mutuel, La Banque Postale, Rothschild, ODDO BHF, Santander, BBVA, ING, the Japanese banks, Kyutai (Homerun), Alma. For these: paste a job link in the inbox, or use the alert-email import once built (bank career sites almost all offer email alerts). Adding one later means finding its system (the careers page usually links to it) and, if it is Workday or Oracle HCM, adding a source; anything else needs a new adapter.

#### eFinancialCareers

A finance job board with no API, searched **by keyword** rather than by location alone (its `/search` path is disallowed by robots.txt, so the source uses the public job-listing pages a visitor opens: `/en/jobs/<keyword>/in-paris,-france`). Each listing page embeds up to 15 complete jobs (company, date, location, full description) and pages with `?page=N`, so a keyword search costs one request per page instead of one per job. Config: `keywords` (a list, editable in the UI), `location`, `pages` (default 2, so 30 jobs per keyword) and `crawl_delay` (10 seconds, as its robots.txt asks). A run takes about keywords x pages x 10 seconds. Starting keywords: structured, operations, fintech, core banking, stakeholder, automation. It identifies itself as `Mozilla/5.0 (compatible; saxobeat/0.1; ...)`, because the site rejects a bare bot name. Unofficial, so it could stop working, and I have not reviewed the site's terms of use.

Other aggregators follow the same idea: Adzuna and Remotive take `queries`, and any new aggregator source should search on keywords first and filter on location second.

#### Build order for sources

1. *(done)* ATS boards (Greenhouse, Lever, Ashby, Workable, Teamtailor), Adzuna, Remotive, career-page JSON-LD, manual add.
2. Alert import by upload/paste (option 1 above), starting with WTTJ and LinkedIn parsers.
3. The supervised-session import format (option 2).
4. Remaining aggregators and the opt-in WTTJ index adapter.

## 6. Core flow

```
Scheduler ──► Source adapters ──► Normalize ──► Dedupe ──► Hard filters ──► Relevance scoring ──► DB ──► UI
                                                              │                                          ▲
                                                     (auto-hidden, kept)                       my actions feed back
```

### 6.1 Normalize

Map every posting to one schema (see §8): title, company, location, remote type, salary (min/max/currency/period, if stated), employment type, seniority, language, description (full text and HTML), posted date, deadline, apply URL, apply method (link/email/ATS), contact, source, source ID, raw payload.

### 6.2 Dedupe

The same job often appears on several sources. Match on a canonical key: normalized company + normalized title + location, with fuzzy fallback, plus exact URL/ID match. Merge into one job with multiple `job_sources` rows. Never show duplicates. Keep every source link, and prefer the company's own apply URL.

### 6.3 Hard filters (cheap, deterministic, run first)

Configurable rules that hide a posting from the inbox without deleting it:

- **Locations:** two lists from a registry (`jobs/cities.py`). `cities` (Paris to start) are acceptable for any role. `remote_cities` (London to start) are acceptable for **remote roles only**: the time zone works and there is no commuting. A remote role anywhere else is hidden, and so is a remote role that names no place (unknown time zone). "Remote" means the source flags it, or its location or title says so. Each city has aliases (Paris covers Île-de-France, La Défense, Boulogne-Billancourt, 75/92/93/94 postcodes). A role that is not remote and has no stated location, or only a country, is kept because it cannot be ruled out. Adding a city is one registry entry.
- Language of the posting (derived from the CV: fr, en, bg, ru).
- Minimum salary, when stated (postings with no salary pass).
- Blocklists: companies and title keywords. Seeded from the CV's seniority with junior words (stage, alternance, intern, junior...).
- Age: ignore postings older than N days (default 30 since cycle 031, was 60; it applies to every source, employer boards included). A posting's age is its posting date, or the day the job was first imported when it has none (`filters.listing_date`). Hidden jobs are not scored and not sent to the AI.

Hidden postings are reachable via a "Filtered out" view that shows *which rule* fired. This is essential for tuning, because a wide search means the filters will be wrong sometimes.

### 6.4 Relevance scoring

**No API is assumed.** Scoring is deterministic and runs inside the app, then an optional human-in-the-loop AI review is added on top.

1. **Profile from the CV.** `manage.py import_cv` loads the CV (contact details redacted) as the profile, extracts weighted keywords (core skills, held job titles, and a few French equivalents from a short fixed list), the languages, and junior-title blocklist.
2. **App score (0–100)** = `keyword_weight` (default 0.7) × keyword score + (1 − `keyword_weight`) × similarity, plus a title seniority adjustment (senior words up, junior words down).
   - *Keyword score:* weights run 1 to 5 and each step is worth three times the one below (1, 3, 9, 27, 81 points), so one match on a top-weight keyword is a clear-cut signal and beats a pile of generic ones. Whole-word matches that ignore case and accents (an English and a French spelling that differ only by an accent count once, at the higher weight). A title hit counts 1.5x. Boosts saturate smoothly toward 100. A penalty is linear and stronger: a 5 is close to a veto. Keywords that appear in most of an employer's postings (its "About us" text) are ignored for that employer unless they are in the title.
     **Bilingual (cycle 021, 2026-11-04).** A keyword is also found through its equivalent in the other language: `jobs/glossary.py` is a reviewed list of about 130 English/French concepts ("AI" = "IA" = "intelligence artificielle", "change management" = "conduite du changement", "product manager" = "chef de produit"...), with marks for terms that must not be searched in one language ("ai" is the verb "j'ai" in French) and a guard against false friends ("stage"). A keyword written as such counts exactly as before; an equivalent adds a boost only when nothing was counted for that concept, so a concept never counts twice. The matched list shows the candidate's own words, and the job page adds "found as: <the posting's words>". Exclusion words are not expanded. `SAXOBEAT_GLOSSARY=0` goes back to literal matching.
   - *Similarity:* sparse TF-IDF cosine between the profile (CV plus keyword list) and the posting, IDF learned from the stored postings. No model download, no API, runs on the free tier. **Language-aware (cycle 021):** postings written in the language the profile is *not* written in are compared with a reference that also holds the keywords' terms in that language, and scaled with a lower constant (0.032 against 0.06), so a French posting is not under-scored because the CV is in English (and the other way round for a French CV). The constant was calibrated on one candidate's data.
3. **AI review (manual, batched).** The app exports the best app-scored, not yet reviewed jobs as JSON (CV, rubric, jobs). I run it through a Claude session (Cowork or Claude Code, with the `saxobeat-review` skill) which writes a scores file, and the app imports it. Each imported score carries reasons, concerns, and matched/missing skills.
   **Rerun.** When the review skill changes, earlier reviews may be wrong. A *rerun round* (started by the user) marks all existing reviews as due; a rerun batch then holds reviewed jobs whose review predates the round, filtered by earlier verdict (default: don't apply), ranked by the app's own score so a harsh earlier verdict cannot bury a job. The file never carries the earlier verdict. Importing a review overwrites the previous one entirely, which also takes the job out of the pool, so successive batches march down the list without repeats.
4. **Final score** = `ai_weight` × AI score + (1 − `ai_weight`) × app score when a review exists, otherwise the app score. Re-scoring after a profile change keeps imported reviews.

**Feedback loop (v1 lightweight):** every dismiss can carry a reason (*wrong domain / too senior / too junior / location / pay / company / other*). Shortlist and dismiss actions are stored as labeled data, to tune keywords and filters later.

### 6.5 Scheduling

- A runner that refreshes each source on its own interval (default every 6h).
- *(Superseded for the hosted setup.)* The hosted web app never reads the sources (`SAXOBEAT_RUN_SOURCES=0`); the operator's PC does, with `scripts/pc_runner.ps1` in Task Scheduler, writing into the hosted database (see DEPLOY.md). `POST /cron/run/` (token-protected) still exists for an installation that runs its own sources. Original design: on Render's free tier an instance sleeps after ~15 minutes idle and cannot schedule itself, so an external scheduler (GitHub Actions cron, every 3h) calls it.
- Locally, `python manage.py run_sources` does the same. "Refresh now" in the UI runs everything on demand, in a background thread, one run at a time.
- Each run is logged (started, finished, per-source counts, errors, LLM cost).

## 7. UI (deliberately simple)

Server-rendered Django templates with a little HTMX. No SPA framework. Login required, since it is hosted publicly. Five screens *(the candidate menu is now Inbox, Pipeline, Interviews, Companies, Insights, Settings; Sources, Runs, Jungle radar, AI review and Data live in an Operator menu; the look is a token-based dark theme with three palettes, see the README)*:

1. **Inbox (default):** new, unreviewed postings sorted by score. Each row shows score, title, company, location/remote, salary if any, source(s), age, and a one-line reason. Keyboard-driven triage (`j/k` move, `s` shortlist, `d` dismiss with reason, `o` open original). Filters: score threshold, source, remote, date. Bulk dismiss below a threshold.
2. **Job detail:** full description, structured fields, score breakdown (reasons/concerns/skill match), all source links, my notes, and a status control. Buttons: *Open apply link*, *Copy contact email*, *Mark applied*.
3. **Pipeline:** every job I've acted on, grouped by status (list view; a kanban is optional). Shows the date of the last status change and highlights follow-ups due.
4. **Filtered out / Archive:** hidden and dismissed jobs, with the reason each is hidden, so I can rescue false negatives.
5. **Settings:** profile document, weights/keywords, hard-filter rules, source configs, schedule, LLM budget, and run history/errors.

### Application statuses

`New → Shortlisted → Applied → Interviewing → Offer → Accepted`
with terminal states `Rejected`, `Withdrawn`, `Dismissed`, and `Expired` (shown as **No longer available**: the app sets it when a source drops the posting, and since 13 October 2026 the person can set it too, from the job page's quick button or its status menu; pressing the button again undoes it).

Every transition is timestamped in a history table. A job carries its application fields directly: date applied, channel, CV version used (free text), notes, and an optional follow-up date. (There is one application per job, so no separate table.)

## 8. Data model *(single-user shape; superseded for personal data)*

Everything useful for applying lives in the DB. Raw payloads are kept so re-parsing is possible without re-fetching.

Implemented as Django models in `jobs/models.py`; this is the logical shape. **Since the multi-user work, the personal columns of `jobs` (`status`, `status_changed_at`, `applied_at`, `channel`, `cv_version`, `follow_up_at`, `notes`, `hidden_reason`) and the `scores`, `status_history` and `config` tables live per person** on `CandidateJob`, `Score`, `StatusChange` and `Config`, each tied to a `Candidate`. `jobs`, `job_sources`, `sources` and `runs` stay shared. See PRD_multi_user.md §7.

```
sources        id, type, name, config_json, enabled, interval_minutes, last_run_at
runs           id, source_id, started_at, finished_at, status, fetched, new_jobs, error
jobs           id, canonical_key, title, company, location, remote_type, country,
               salary_min, salary_max, currency, salary_period, employment_type, seniority,
               language, description_text, description_html, posted_at, deadline_at,
               apply_url, apply_method, contact_name, contact_email,
               first_seen_at, last_seen_at, expired_at,
               hidden_reason, content_hash,
               status, status_changed_at, applied_at, channel, cv_version, follow_up_at, notes
job_sources    id, job_id, source_id, external_id, url, raw_json, first_seen_at, last_seen_at
scores         job_id (1:1), profile_version, rule_score (keywords), similarity_score, seniority_adj,
               deterministic_score, matched_keywords, ai_score, reasons, concerns, matched_skills,
               missing_skills, reviewer, reviewed_at, final_score, created_at
status_history id, job_id, from_status, to_status, changed_at, note, dismiss_reason
config         singleton: profile_text, profile_version, keywords, filters, llm settings
```

Search is a plain `icontains` for now; SQLite FTS5 is a later optimization.

## 9. Technical approach

Optimized for low maintenance and minimal moving parts. Decided: Python and Django. *(The hosting bullets below are superseded: Postgres everywhere, Render paid plans, no Litestream. See DEPLOY.md.)*

- **Stack:** Django 6 (ORM, auth, admin, migrations) with server-rendered templates and HTMX. `httpx` for fetching. Gunicorn with a single worker (SQLite has one writer, and the run lock is per process), WhiteNoise for static files.
- **Database:** *(superseded: Postgres everywhere, including development and tests; SQLite only as a fallback when `DATABASE_URL` is unset. A single gunicorn worker is no longer a constraint.)* Originally: SQLite, everywhere.
- **Persistence on Render free** *(superseded: Render Postgres, plus `manage.py backup_database` run daily from the PC)*: the free tier has an ephemeral disk, and free Postgres expires after 30 days, so SQLite is replicated with **Litestream** to S3-compatible storage (Cloudflare R2 free tier) and restored at boot. See [DEPLOY.md](DEPLOY.md).
- **Scoring:** in-app and deterministic (keywords, TF-IDF similarity, seniority), pure Python. The AI step is a file hand-off to a Claude session run by me, so no Anthropic API key is needed.
- **Scheduling:** *(superseded: the PC runner, see 6.5.)* Originally external cron (GitHub Actions) hitting `/cron/run/`, since the free instance sleeps. Locally, the `run_sources` management command.
- **Config:** personal settings in the DB (edited in the UI); secrets in environment variables or `.env`, never in the DB or the repo.
- **Backups:** *(superseded: `manage.py backup_database` writes a `pg_dump` file to `data/backups/` daily from the PC runner, restore verified on a scratch database.)* The Data page export (operator) and *Download my data* (candidate) are the portable backups and the way to migrate between platforms (see 9.1). Originally the safety net was a Litestream replica (72h retention); Litestream has been removed.

### 9.1 Data export and import

One portable JSON file (`saxobeat.backup.v1`, optionally gzipped, named with a leading timestamp) holds settings, sources, and every job with its source links, score or AI review and status history. It excludes users, passwords, sessions and API keys. It is keyed by natural keys (job fingerprint, source type and name), not database ids, and fields are read by name, so older backups import and unknown fields from newer ones are ignored.

- **Merge** never deletes: adds missing jobs, links, history and sources; the newest decision on a job wins; blank notes are filled; an AI review is adopted only if missing or newer; this installation's own source config and (unless fresh) settings stand; merged jobs are refiltered and rescored with the local settings.
- **Replace** restores exactly, keeping job ids, in a single transaction.
- Available on the Data page and as `export_data` / `import_data`. Import refuses while a source run is in progress, caps decompressed size, and rejects files that are not backups with a clear message.

## 10. Non-functional requirements

- **Private:** no telemetry. Data lives in my own database (hosted in an EU region for several people). Nothing is sent to an AI service by the app; the AI review happens when I hand an exported file to my own Claude session. The hosted app is behind a login, and the cron endpoint behind a token.
- **Idempotent runs:** re-running never creates duplicates or loses status.
- **Resilient:** partial failures are isolated and visible.
- **Fast UI:** Inbox loads in under 300 ms for 10k jobs locally. Hosted, the target is under 2 s on common pages (PRD_multi_user.md §10); not yet measured on the host.
- **Observable:** run log and per-source health in the UI.
- **Legal/ethical:** respect robots.txt and API terms. No credential-based scraping of sites that forbid it.

## 11. Milestones

1. **M1: Skeleton.** *(done)* Models, migrations, source-adapter interface, sources (Greenhouse, Lever, Ashby, Adzuna, Remotive), normalize and dedupe, `run_sources` command.
2. **M2: Inbox + statuses.** *(done)* Inbox and Job detail, shortlist/dismiss, status history, Pipeline view.
3. **M3: Filters + scoring.** *(done)* Hard filters with city list and "Filtered out" view, CV import, deterministic scoring, score breakdown UI, AI review export/import and skill.
4. **M4: Scheduling + more sources.** *(done; the Render deployment itself is untested, and the hosting design changed, see DEPLOY.md)* Refresh now, run history, cron endpoint, source-failure banner, career-page and manual-add sources. Still to build: alert import (see above).
5. **M5: Feedback loop.** *(done)* Dismiss reasons, bulk dismiss below a score, an Insights page that suggests title words, companies and keywords from my decisions (one-click apply), and a check of whether the AI review agrees with my choices. FTS search is left as an optimization.

## 12. Risks

| Risk | Mitigation |
|---|---|
| Scraping breaks or gets blocked | Prefer APIs/ATS endpoints, adapter isolation, per-source health alerts, email-alert ingestion for hostile sites |
| Wide net floods the inbox | Two-stage filter and scoring, score threshold, bulk dismiss, and the feedback loop |
| Deterministic scoring misses nuance | The AI review on top of the best candidates; a "low scores" view to catch false negatives; scores show their parts (keywords, similarity, level) |
| Scores are wrong or opaque | Always show the score parts and matched keywords (and the AI reasons/concerns), keep a "low scores" view, log labeled outcomes to tune weights |
| Duplicates across sources | Canonical-key + fuzzy dedupe, multi-source `job_sources` |
| Data loss | Never delete (only expire/hide); daily `pg_dump` copy kept off the host by the PC runner; hosted Postgres backups depend on the plan (check the dashboard) |
| Hosting prices or limits change | Everything also runs locally; the deployment is one Dockerfile plus `render.yaml` and a standard Postgres, so it moves to any host |

## 13. Open questions

*Status 2026-10-12: questions 2 to 4 and 7 were settled in practice by the Settings page and the CV import (language and seniority filters, salary minimum, review batch size); question 8 is covered by the CV onboarding's draft profile and target roles. Open product questions now live in PRD_multi_user.md §12 and PRD_competitive_features.md §11.*

These change filters and source choice, so answers are needed before M1/M3:

1. **Remote:** answered: remote roles are accepted only in Paris or London; anywhere else the time zone is too hard.
2. **Languages:** which posting languages should be kept (FR/EN/other)?
3. **Salary/contract:** minimum pay, contract types (permanent, freelance, fixed-term)?
4. **Seniority range** and any hard deal-breakers?
5. **Sources:** answered: 14 Paris employers given; 12 seeded (see above). More employers welcome.
6. **Email alerts:** answered: no standing mailbox access. See "Alert emails, without giving the app my mailbox": which of the 3 options?
7. **AI review cadence:** how many jobs per batch is comfortable to review in a Claude session (default 40)?
8. **Directions and deal-breakers:** the CV is loaded, but it only shows where you have been. A few lines on where you want to go and what to avoid would sharpen the keywords (Settings > Penalize) and the AI review.
9. **Object storage:** *(obsolete: Postgres replaced the SQLite replica, so no bucket is needed.)*
