# Spec: employers' own career sites (step 1 of cycle 013)

| | |
|---|---|
| **Cycle** | 013 |
| **Stage** | Spec approved 2026-10-30 |
| **Intent** | [intent.md](intent.md) |

## Behaviour when finished
- The employer lists in `data/` say the truth: every employer marked "covered" has been checked against its real board, the wrong ones are corrected, and every one of the 18 priority-A unknown employers is either watched by a source or listed in `docs/unsupported_employers.csv` with a reason.
- Saegus, Accenture and Capgemini are handled first: Saegus and Accenture are sources that bring their whole list of jobs (in the candidates' cities); Capgemini is a source if a lawful feed turns up, otherwise it is parked with the reason.
- Nothing is read from a site whose terms or bot protection forbid it; for each new source the terms and robots rules are recorded before it is added.
- VC boards and aggregators are not touched (their own specs, later). Alert e-mails are cycle 018.

## Acceptance criteria
Each one must be checkable in `verify.md`.
1. [ ] **Terms first.** For every source added in this step, a line in `evidence/` records the page read, what it says about automated reading and reuse, and robots.txt, dated, *before* the source is created. (Saegus, Accenture, Capgemini: done 2026-10-30, [evidence](evidence/employer_terms_2026-10-30.md).)
2. [ ] **A read-only re-check of "covered".** *(Amended 2026-10-30, before the plan: the first wording would have passed Accenture, whose Recruitee board names itself "accenture".)* A script (`manage.py employer_recheck`, name to confirm in the plan) takes every employer that is "covered" in the four lists (252 on 2026-10-30) and reads what its source has **already stored** in a local copy of the database (no request to any site). *(Amended again 2026-10-30, during slice 1: 3 of the 252 claims name a source that does not exist in the database, so a sixth verdict `missing` is needed: no source by that name, nor one starting with the employer's name.)* It gives each a verdict: `ok` (the stored jobs' company names match the employer's cleaned name, and the board looks like a real one: more than a handful of jobs, none titled like a sample or test), `suspect` (the name matches but the board looks wrong: fewer than 5 jobs in all and none in the candidates' country or cities, or a sample/test title), `mismatch` (the company names do not match), `empty` (no stored job) or `error`. Only the `empty` and `suspect` ones may then be asked live for at most 5 jobs. It writes `data/employer_recheck.csv` and changes no database, no source and no list. The evidence file gives the five counts and names every `suspect`, `mismatch` and `empty`.
3. [ ] **Accenture's false "covered" is caught.** *(Amended during slice 1: the 29 Oct database holds no Accenture source, so the wrong board is not there to switch off.)* The re-check marks Accenture `missing` (the lists say "recruitee source, on"; the database has none, and the real `accenture.recruitee.com` is two Dutch sample jobs, not Accenture France), likewise Google and Google Cloud (also "recruitee"), and the lists are corrected. If a source of that board exists in the hosted database now (created after 29 Oct), slice 12 switches it off.
4. [ ] **Every `suspect`, `mismatch` and `empty` is resolved.** Each is corrected (a right source, or the wrong one switched off and the employer set back to `unknown`) or accepted by the owner with the date. The coverage files then contain no "covered" employer whose source failed the re-check.
5. [ ] **Saegus.** A `teamtailor` source with `host: careers.saegus.com` and `company: Saegus` is created; a test reads a saved copy of `jobs.rss` and returns the jobs with title, place, link and description; a live read on the operator's PC returns at least one job (count recorded).
6. [ ] **Accenture.** A `sitemapjobs` source reads `https://www.accenture.com/fr-fr/jobpostings-sitemap.xml` with `job_pattern` set for `jobdetails` (the default pattern would match none of them, and a job's identity is in the `?id=` part of the address, which the adapter's id rule ignores). A trial of 5 pages returns title, place, description and a stable id; two consecutive runs store each job once. Any change to `sitemapjobs.py` comes with a test and leaves the existing sources' behaviour unchanged. It never reads the `jobsearch` pages.
7. [ ] **Capgemini, bounded.** A look limited to: its robots-allowed public pages and sitemaps, the public job-list address that its own page calls (if robots.txt allows it), and its hiring system's published feed. No login, no forged headers, no bot-protection workaround. The result is either a source with a test (as for 5), or a `no_feed_found` row in `docs/unsupported_employers.csv` with the reason and the date.
8. [ ] **The 18 priority-A employers.** Each has a verdict in `evidence/`: a source added (criteria 1 and 9 apply) or a row in `unsupported_employers.csv` (status, blocker, how to reach their jobs anyway, date). The count of each is recorded.
9. [ ] **Every new adapter or adapter change has tests** (a saved real response, no live calls in the suite), and the full suite passes with `DATABASE_URL=` on SQLite (1,264 on 2026-10-30), with 0 new failures.
10. [ ] **Sources are created reproducibly and safely.** New sources are added to `seed_employers.py` (idempotent, by name). Before the owner runs it on the hosted database, a dry run lists exactly what will be created and nothing existing is changed; the hosted write is done by the owner, with a Neon snapshot taken just before (the rule from cycle 015).
11. [ ] **Neon reads are measured.** The extra reads per run from the new sources are measured on the local copy (the cycle-001 scripts) and stated; the owner accepts the figure before the sources are enabled on the hosted database.
12. [ ] **The lists match the verdicts.** `employer_coverage*.csv` and `unsupported_employers.csv` are updated; the final counts (covered, unknown, unsupported) are recorded next to the 2026-10-30 baseline (252, 327, 14). The `data/` files are gitignored, so the counts and the list of changes are copied into `evidence/`.
13. [ ] **The new-job share, one week after the first full run** (success measure 4): jobs from the new sources that are new to the catalogue and in the candidates' cities, as a count and a share. It may be read after the cycle's verify stage; if so, `learn.md` carries it, dated.

## Design in brief
- **Re-check before adding.** The Accenture error came from a guessed board name that belongs to someone else. The re-check uses the board names already found by the 2026-10 probe (`data/employer_probe.csv`: system and slug) and the lists' careers links, asks the public feed for a few jobs, and compares the company name and the places. Unclear verdicts go to the owner, not to a rule.
- **Existing adapters first** (`teamtailor`, `sitemapjobs`, `careerpage`, the ATS ones). A new adapter only when a whole family of employers needs one, and then with its own test and its own line in the plan.
- **The 18 in order of the lists' categories**, each probed with the same method (careers link, hiring system, public feed, robots, terms); the ones that stay unreadable go to `unsupported_employers.csv`, which already exists for this.
- **Rejected:** adding only the three employers (the owner asked for the lists too); re-probing all 327 unknown (thousands of requests for priority B and C employers, before A has been measured); trusting the coverage files as they are (the Accenture error); adding sources by hand in the hosted Sources page (not reproducible, no review).

## Interfaces and data
- New: the re-check command and `data/employer_recheck.csv` (local, gitignored).
- Changed: `jobs/management/commands/seed_employers.py` (new sources); possibly `jobs/sources/sitemapjobs.py` (the id from the address's query, only if the trial shows it is needed); `docs/unsupported_employers.csv` and `.md`; tests in `tests/`.
- Written outside the repo: the hosted `jobs_source` table (new rows, one wrong row disabled), by the owner, in an approved plan slice.
- Evidence in this cycle's `evidence/`: the re-check result, per-source terms lines, the 18 verdicts, the Neon-read measurement.

## Constraints
- **Terms and robots.** robots.txt obeyed (the adapters check it); no anti-bot workaround; one polite request rate (the adapters already pause).
- **Neon free plan.** Each source adds reads to every run (about 60 MB a pass for the whole catalogue today, cycle 001); the increase is measured and accepted before enabling on the hosted database.
- **Secrets** are never printed; the hosted database is written only by the owner (rule from cycles 001, 002 and 015).
- **Real-site reads.** The re-check and the trials read public pages from the operator's PC: a few hundred requests spread out, not a crawl; I ask before running anything larger.
- **Windows + `uv run python`**, tests with `DATABASE_URL=` (SQLite).

## Out of scope
- Priority B and C unknown employers (until A is measured).
- VC boards and aggregators (own specs), alert e-mails (cycle 018), Personio.
- The product-level legal review of sources (PRD.md §2): this step records each site's terms, nothing more.
- Any change to scoring, the inbox or the candidate interface.

## Risks
- A "covered" employer may be wrong in a way the company-name test cannot see (a parent company's board). The owner reviews the unclear ones.
- Accenture's sitemap may list jobs that are closed; the run's own expiry rules apply, and the trial checks a few against their pages.
- Some of the 18 may be readable only by a new adapter; those become a list for a later step, not work in this one.

> **Step 2 (consulting employers, added 2026-11-03)** has its own criteria and slices in [step2-consulting.md](step2-consulting.md), with its own approval line; this file's gate is not affected.

## Gate
- [x] Owner approved this spec (2026-10-30)
