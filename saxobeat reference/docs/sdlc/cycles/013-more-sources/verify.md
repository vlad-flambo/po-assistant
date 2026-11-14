# Verify: more sources (step 1 employers' own sites, step 2 consulting)

| | |
|---|---|
| **Cycle** | 013 |
| **Stage** | Verify, DRAFT 2026-11-04, the one-week readings added 2026-11-10; waiting for the owner's verdict |
| **Spec** | [spec.md](spec.md) (criteria 1 to 13) and [step2-consulting.md](step2-consulting.md) (S2.1 to S2.9) |

Evidence files are in [evidence/](evidence/). Results are from the files and the hosted state read on 2026-11-04; the owner's own look ("seems to work fine", 2026-11-04) is noted where it applies.

## Evidence per acceptance criterion: step 1
| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Terms first | partial | Terms and robots lines dated before creation for Saegus, Accenture, Capgemini (`employer_terms_2026-10-30.md`) and the priority-A sources (`priority_a_verdicts_2026-10-30.md`: Greenhouse, Ashby, Murex, Amundi read). **Not read: Finastra, SWIFT, Fenergo/Workable** (HTTP 403 to the tool). The owner accepted that on 2026-11-03 (decisions.md D2) |
| 2 | Read-only re-check of "covered" | pass | `employer_recheck` command + 13 tests; 252 checked: ok 228, suspect 8, mismatch 0, empty 13, missing 3, error 0; changes no database (`recheck_2026-10-30.md`) |
| 3 | Accenture's false "covered" caught | pass | Accenture, Google and Google Cloud are `missing` in the re-check; lists corrected (`recheck_live_2026-11-03.md`) |
| 4 | Every suspect, mismatch and empty resolved | pass | Live look at the 24 flagged: 15 real boards, 6 wrong or test boards, 3 stale claims; the six wrong sources switched off on the hosted database on 2026-11-03 (nothing deleted); four lists corrected (`recheck_live_2026-11-03.md`, `hosted_write_2026-11-03.md`) |
| 5 | Saegus | pass | Seed entry, `tests/test_saegus_source.py`, live read 16 jobs, all Paris (plan "As run", slice 6); ran on hosted at the owner's pass of 2026-11-03 |
| 6 | Accenture | pass | `tests/test_accenture_source.py`; trial on the scratch Postgres: 5 jobs once each, run 2 adds 5 new; a currency bug of the shared reader found and fixed (slice 7). **Accenture needs one more run** on hosted to read its 173 pages (60 a run) |
| 7 | Capgemini, bounded | pass | New adapter `capgemini.py`, 9 tests, rehearsal 134 fetched then 0 new (`capgemini_look_2026-10-30.md`); hosted run 2026-11-03: 397 fetched, 387 new |
| 8 | The 18 priority-A employers | pass | 8 sources (Backbase, Checkout.com, Fenergo, Payhawk, Amundi, Finastra, Murex, SWIFT) + 10 listed in `unsupported_employers.csv` (`priority_a_verdicts_2026-10-30.md`) |
| 9 | Adapter tests, full suite | pass | Full suite 1,443 passed, 0 failed (`DATABASE_URL=` SQLite, 2026-11-04); 1,264 on 2026-10-30 |
| 10 | Reproducible and safe creation | pass | `seed_employers --dry-run/--only`, checksum of the 328 existing sources unchanged (`seed_dry_run.md`); Neon snapshot taken by the owner before the write; **the write itself was run by Claude at the owner's request, not by the owner as the spec said** (`hosted_dry_run_2026-11-03.md`, `hosted_write_2026-11-03.md`) |
| 11 | Neon reads measured | accepted | Steady state 0.633 MB a pass for the ten step-1 sources, 26.43 MB once (`new_sources_measurement_2026-10-30.md`); accepted by the owner 2026-10-30 (D1). Hosted month-to-date transfer after pass 2: 0.26 GB (owner's reading, 2026-11-03) |
| 12 | The lists match the verdicts | pass | After 2026-11-04: covered 259, unsupported 39, unknown 295 (baseline 252, 14, 327) (`hosted_write_2026-11-03.md`). `data/` files are gitignored; the counts are copied here |
| 13 | The new-job share after one week | pass | Read 2026-11-10: 2,016 new jobs in Paris / Ile-de-France since 2026-11-03, 1,052 (52.2 %) from the cycle's sources; includes the one-off first-pass backlog (`weekly_reading_2026-11-10.md`) |

## Evidence per acceptance criterion: step 2 (consulting)
| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 14 (S2.1) | Terms first | partial | BCG, EY, Onepoint terms recorded before seeding. Onepoint's terms forbid "extraction" of the Site's content without authorization; PwC's legal pages unreadable (HTTP 403). Both enabled on the owner's decision of 2026-11-03 (D2); the owner was to read PwC's notice in a browser: **not confirmed** |
| 15 (S2.2) | BCG | pass | `phenom` source, 44 France jobs (43 Paris/IDF), feedback #3's job is in the list; `tests/test_bcg_source.py`; Postgres rehearsal (`bcg_2026-11-03.md`); on hosted, 44 jobs at the third pass |
| 16 (S2.3) | No duplicates | pass | 5 of 28 need no new source: Sopra Steria, Wavestone, Eviden (via Atos), Capgemini Invent (via Capgemini), Infosys (already `blocked`) (`consulting_duplicates_2026-11-03.md`) |
| 17 (S2.4) | A verdict for each of the 25 | pass | Batches B, C1, C2: sources BCG, EY, Onepoint, PwC, PwC Campus; the rest already covered or in `unsupported_employers.csv`; HCLTech, Wipro and Sword Group readable but no France jobs (`consulting_batch_b/c1/c2_2026-11-03.md`) |
| 18 (S2.5) | Tests; no new adapter without three employers | pass | EY 4 tests, BCG 3, Onepoint/PwC in `test_consulting_sources.py`; no adapter built in step 2; suite 1,443 |
| 19 (S2.6) | Reproducible and safe | pass | `-Step 1|2|all` in `seed_hosted_sources.ps1`, dry runs 10 / 5 / 15, `-Apply` refuses without `-SnapshotTaken`, existing 328 unchanged (`seed_dry_run_step2.md`); hosted: 15 sources added, only `jobs_source` changed (331 to 346) |
| 20 (S2.7) | Neon reads and relevance | partial | BCG and EY measured: 108 requests, steady state 0.034 MB a pass, +2.1 MB once, 101 stored jobs in Paris/IDF (`new_sources_measurement_step2_2026-11-03.md`). Onepoint and PwC were not measured (terms open). The owner chose to enable all after the Neon readings of 2026-11-03 |
| 21 (S2.8) | The lists match | partial | Lists updated 2026-11-04 (see criterion 12); the consulting-only counts against the 2026-11-03 baseline (13 covered, 29 unknown) are **not broken out** |
| 22 (S2.9) | The weekly measure | pass | Read 2026-11-10: 967 consulting jobs new in Paris / Ile-de-France in the first week, 48.0 % of the 2,016 new jobs there (incl. the first-pass backlog; Capgemini 400, EY 162, Accenture 126, PwC 117); the next reading, 2026-11-17, is the first steady week (`weekly_reading_2026-11-10.md`) |

## Added after the specs (owner's requests, same cycle)
| What | Result | Evidence |
|---|---|---|
| Doctolib and Papernest repaired (greenhouse board and Workday site gone) | pass | New boards found, created, old two switched off (Doctolib on Ashby: 149 jobs, 55 in Paris; Papernest on Workday wd502); third pass: Doctolib 152 and Papernest 23 new jobs (`hosted_write_2026-11-03.md`) |
| EY `max_jobs` correction | pass | The limit caps the whole list: 60 saw only the 60 most recent Paris jobs; 200 on hosted and in the seed (step2 "As run") |
| Batch of 24 French fintechs (2026-11-04) | pass | 6 skipped as present, 4 sources (Epsor, Kaiko, Marble, Qonto on Ashby) created ON, `Qonto (lever)` off, 10 slugs added to the Welcome to the Jungle source, 5 listed; `tests/test_fr_fintech_batch.py` (7 tests); owner's pass: "seems to work fine" (`batch_fr_fintech_2026-11-04.md`, commit `105c79c`) |

## Tests
Full suite on SQLite (`DATABASE_URL=`), 2026-11-04: **1,443 passed, 0 failed** (warnings only). New or changed test files of this cycle: `test_employer_recheck`, `test_saegus_source`, `test_accenture_source`, `test_capgemini_source`, `test_priority_a_sources`, `test_bcg_source`, `test_ey_source`, `test_consulting_sources`, `test_moved_boards`, `test_fr_fintech_batch`, plus additions to `test_more`, `test_careers`, `test_employers`. Postgres rehearsals on the scratch copy for Accenture, Capgemini, the ten step-1 sources, BCG and EY.

## Not verified
- A steady-state week: the 2026-11-10 reading includes the one-off first-pass backlog; the owner's weekly figure from 2026-11-17 is the first steady one. The per-candidate view (what an account sees after its filters) is not measured.
- Finastra, SWIFT, Fenergo and PwC terms (unread), Onepoint's "extraction" clause (accepted by the owner, D2).
- Accenture's full 173 pages on hosted (one more run); how its sitemap treats closed jobs.
- Neon usage after the third pass and after the fintech batch (no reading given); the Neon transfer so far is 0.26 GB of 5 GB (2026-11-03).
- The `data/` lists do not yet include the fintech batch's ten employers.
- Stored jobs from worldwide sources may include US jobs matched as Paris by the ZIP-code test (found with EY; the shared test was not changed).
- `Valiantys (lever)` switched off on hosted by someone else; not by this cycle.

## Verdict
- [ ] Accepted by owner
- [ ] Sent back (what, to which stage)
