# The hosted write (2026-11-03, slices 12 and 21)

Run by Claude **at the owner's explicit request** ("You run it"), after the owner had taken the Neon snapshot of prod1 and after the dry run ([hosted_dry_run_2026-11-03.md](hosted_dry_run_2026-11-03.md)). Command: `scripts/seed_hosted_sources.ps1 -Step all -Apply -SnapshotTaken` (the address is read from `.env` for that one process and never printed).

## Result
| Check | Result |
|---|---|
| Dry run inside the script | `15 would be created, 0 already present` |
| The write | **`15 sources added, 0 already present`** |
| Table counts before and after (`data/counts_before_013.json`, `data/counts_after_013.json`) | **1 difference: `jobs_source: 331 vs 346`**; every other table identical (39 tables, 233,786 rows before and 233,801 after: the 15 new rows) |
| Re-run of the seed | `0 sources added, 15 already present` |
| State of the new sources | all 15 **switched off** (the seed creates them with `enabled = False`) |

The fifteen: Saegus (teamtailor), Capgemini (capgemini), Accenture (sitemapjobs), Backbase (greenhouse), Checkout.com (ashby), Fenergo (workable), Payhawk (greenhouse), Finastra (workday), Murex (workday), SWIFT (workday), Boston Consulting Group (phenom), EY (successfactors), Onepoint (workday), PwC (workday), PwC Campus (workday).

## What this does and does not change
- **No job is read from any of them yet:** they are off, and the runner runs only enabled sources. The first reads happen when sources are switched on.
- **The Neon snapshot taken before is the way back**; the new rows can also be disabled or deleted by name.
- **Not done:** the six wrong sources are still on (Energy Pool 178, Esker 232, EssilorLuxottica 196, Publicis Groupe 217, Trade Republic 53, Uber 287); none of the fifteen is enabled; the lists in `data/` (S2.8) are not yet updated for the consulting rows.

## Later the same day: the six switched off and batch 1 switched on (Claude, at the owner's request: "Yes, do both")
A checked script (`scratchpad` only, not in the repo): every row's id and exact name had to match what the dry run showed, or nothing would change; then one transaction updated `enabled` on 11 rows. Nothing was deleted.
| Change | Rows |
|---|---|
| **Switched off** (were on) | Energy Pool (smartrecruiters) 178, Esker (teamtailor) 232, EssilorLuxottica (smartrecruiters) 196, Publicis Groupe (smartrecruiters) 217, Trade Republic (greenhouse) 53, Uber (smartrecruiters) 287 |
| **Switched on** (batch 1; were off; interval 360 min, status approved) | Saegus (teamtailor) 341, Murex (workday) 349, Payhawk (greenhouse) 347, Checkout.com (ashby) 345, Accenture (sitemapjobs) 343 |
| Counts | 346 sources in all; **enabled 329 to 328**, as expected (329 - 6 + 5) |

A first attempt (a script passed to the Django console as an argument, then through stdin) failed to parse and changed nothing: the counts before and after were identical (346 / 329); the successful run was a standalone script.

**What happens next:** the five have never run, so they are due at the next runner pass (the owner's, by hand, as always). Expected extra Neon transfer for them: about 2.6 MB once (Saegus 0.9, Checkout.com 0.7, Accenture 0.5, Murex 0.2, Payhawk 0.2, from step 1's measurements, excluding the one-off cache read that every run pays) and about 0.4 MB a pass afterwards; Accenture needs three runs to read its 173 pages. The six switched off no longer cost anything.

## The first pass with batch 1 (2026-11-03, read from the hosted run records, read only)
The owner ran the by-hand pass. **335 runs in the window, 331 ok and 4 errors; 533 new jobs.** The five batch-1 sources, all `ok`: Saegus 16 new (of 16), Murex 20 (of 20), Payhawk 52 (of 52), **Checkout.com 165 (of 174)**, Accenture 56 (of 60; its next two runs read the other pages): **309 of the 533 new jobs**. Errors in the pass: Esker (404, switched off just before), **Doctolib (greenhouse): 404 on `boards-api.greenhouse.io/v1/boards/doctolib` since 2 November (it was ok on 30 October): its board is probably gone**, Papernest (teamtailor): 404 once (ok on 2 November), Orus (sitemapjobs): error at 10:53, ok at 10:55. Neon: transfer 0.22 GB month to date, storage 0.54 GB (see `001-local-db-replica/evidence/neon_readings.md`).

## Capgemini switched on (2026-11-03, after the first pass; Claude, with the same checks)
The owner explained the storage figure (it counts prod1 and fallback1 together: about double prod1's 260 MB is normal), which was the only reason the switch-on had been held. `Capgemini (capgemini)` id 342: a checked standalone script (the row had to exist once and be off), one update: **enabled 328 to 329**; interval 1440 minutes (once a day), config `{"country_code": "fr-fr", "pages": 15}`. It runs at the owner's next by-hand pass: 13 pages of about 1 MB read from Capgemini's API by the PC; **Neon's side: about +6.3 MB once** (about 405 new jobs in Paris / Ile-de-France, measured in step 1's slice 11) **and about +0.27 MB a pass afterwards**.

## The second pass, and BCG and EY switched on (2026-11-03)
**Second by-hand pass (read from the run records):** 322 runs, 320 ok, 2 errors; **Capgemini ok: 397 fetched, 387 new jobs** (estimated 405); 600 new jobs in all; 35,318 jobs in the catalogue. Neon (owner's reading): transfer 0.22 to **0.26 GB** (+0.04 GB, web use included), compute 1.23 to 1.66 CU-hrs, storage 0.54 GB unchanged. The two errors are Papernest (teamtailor) and Doctolib (greenhouse), both `404`: their boards look gone (Doctolib since 2 November; Papernest failed once on the 3rd and again now).
**Switched on, at the owner's "you can enable the other sources"** (a checked standalone script, one update): `Boston Consulting Group (phenom)` id 351 and `EY (successfactors)` id 352, both every 360 minutes with `max_jobs` 60: **enabled 329 to 331**. EY reads at most 60 new pages a run, so its 161 Paris jobs take three runs. **Not enabled** (their own conditions still open): Onepoint and PwC / PwC Campus (terms questions), Finastra, SWIFT, Fenergo (terms unread; SWIFT, Fenergo and Backbase also bring no jobs in the owner's cities), Backbase.

## The remaining seven switched on (2026-11-03; owner: "Yes, all of them"; decisions.md D2)
A checked standalone script (each row had to exist once and be off), one update: **enabled 331 to 338**. `Onepoint (workday)` 353 (search Paris, `max_jobs` 100), `PwC (workday)` 354 (Neuilly, 100), `PwC Campus (workday)` 355 (Neuilly, 60), `Finastra (workday)` 348 (Paris, 100), `SWIFT (workday)` 350 (Paris, 100), `Fenergo (workable)` 346, `Backbase (greenhouse)` 344; all every 360 minutes. **All fifteen new sources are on.** Still off: the six wrong sources (Energy Pool, Esker, EssilorLuxottica, Publicis Groupe, Trade Republic, Uber) and the two special sources (LinkedIn browser captures, Manual).
**What to expect at the next by-hand pass:** about 130 job pages read from the Workday sites (Onepoint and PwC up to 100 new pages each, PwC Campus up to 41, Finastra about 7, SWIFT 1), Fenergo's 30 and Backbase's 63 jobs from one request each; Neon: about +3 to 5 MB once (step 1: about 0.01 MB a new Workday job; Backbase 0.2 MB, Fenergo 0.1 MB) and about +0.2 MB a pass afterwards (estimate, not measured for Onepoint and PwC); the next two passes read the rest of Onepoint and PwC.

## Doctolib and Papernest moved boards (2026-11-03; owner: "find the new boards", with the two links; the add-employer workflow)
Both old sources had failed with 404 (Doctolib's Greenhouse board since 2 November; Papernest's Teamtailor feed). The owner gave the new links.
- **Doctolib:** `careers.doctolib.fr/jobs/` is not a hiring system address, so it was investigated (robots.txt open; the page embeds `jobs.ashbyhq.com/doctolib` 149 times, no `jobs.rss`, a WordPress site). **Ashby, board `doctolib`**: live test without a database: **149 jobs, 55 in Paris, 11 in Nantes, 54 in Berlin**, descriptions and dates on all 149.
- **Papernest:** the Workday address is recognised by the app (`workday`, tenant `papernest` on `wd502`, site `External_Careers_Global`, search "Paris"); live test: 5 jobs read, all in Paris, descriptions and dates complete.
- **Added** to `seed_employers.py` (uncommitted, like the rest of the cycle's edits) as `("Doctolib", "ashby", ...)` and `("Papernest", "workday", ...)`, with `tests/test_moved_boards.py` (2 tests, 70 related tests pass), and **created on the hosted database** with `seed_employers --only Doctolib --only Papernest` (dry run first: 2 would be created, 0 present): **`Doctolib (ashby)` id 357 and `Papernest (workday)` id 358, both on, every 360 minutes**.
- **The old two switched off** (not deleted; a checked script): `Doctolib (greenhouse)` 129 and `Papernest (teamtailor)` 189. Counts: 349 sources, **enabled 340 to 338**.
- **Not run:** I did not start the runner for them: they are due at the owner's next by-hand pass (about +1 MB for Doctolib's 149 jobs and a few MB for Papernest's Workday reads; the new rows' interval is 360 minutes).
- The `data/` lists: the two employers' source type and detail updated (ashby, workday).

## The third by-hand pass, with every new source on (2026-11-04, 09:16 to 09:51 UTC; read from the run records, read only)
**336 runs, all `ok`, none in error; 477 new jobs; 36,217 jobs in the catalogue; 338 sources on.** Latest run of each new source: Capgemini (daily, last 3 Nov 15:39: 397 stored), BCG 44 stored (0 new: complete), **EY 60 fetched, 81 stored**, Onepoint 113, PwC 112, PwC Campus 43 (all complete), Finastra 7, SWIFT 1, Fenergo 23, Backbase 64, **Doctolib (ashby) 152 stored (26 new)**, **Papernest (workday) 23 stored (22 new)**, Saegus 16, Murex 20, Payhawk 52, Checkout.com 177, **Accenture 120 stored (55 new this run; 173 pages in all: one more run)**. The Neon reading for this pass was not given.
**Correction (mine): EY's `max_jobs` is not a cap on new pages.** In the SuccessFactors adapter it limits the whole list considered, known jobs included (`wanted[:cap]`), so with 60 EY only ever saw its 60 most recent Paris jobs (81 stored over two runs as the window moved), and my earlier statements that EY "needs three runs to read its 161 jobs" (this file, the step 2 measurement and plan) were wrong. The sitemap adapter (Accenture) does cap only new pages, which is why Accenture does complete in three runs. **Fixed:** `max_jobs` 200 on the hosted source (a checked update of that one config key) and in `seed_employers.py`; the next EY run opens about 80 new pages once and then reads almost nothing.
**Also seen:** `Valiantys (lever)` is off on the hosted database (not changed by me). 349 sources, 338 on.

## The `data/` lists brought up to date (S2.8 and step 1's criterion 12), 2026-11-04
Dated copies first (`data/archive/*_before_s28_2026-11-04.csv`). 24 lines set to **covered** (BCG, EY, Onepoint, PwC, Capgemini and Capgemini Invent, Eviden through Atos, Amundi, Accenture, Backbase, Checkout.com, Fenergo, Payhawk, Finastra, Murex, SWIFT, and the two that already existed under another name: Sopra Steria, Wavestone) and 30 lines to **unsupported** (the consulting and priority-A employers listed in `unsupported_employers.csv` as blocked, no_feed_found or needs_adapter). Best status across the four lists (593 employers): **covered 259, unsupported 39, unknown 295**, against the baselines 252 / 14 / 327 (2026-10-30) and 243 / 14 / 336 (after the re-check on 2026-11-03).
