# Batch of 24 French fintechs (owner's list, 2026-11-04)

Request: "add these to the next batch. if they are already in the sources, skip them". Read-only probes on 2026-11-04 with the app's own adapters (no database writes); robots.txt allowed every page read.

## Already in the sources: skipped (6)
Alma (board alma31, 24 jobs), Leocare (Teamtailor), Lydia / Sumeria (Teamtailor jobs.lydia-app.com), Shine (Teamtailor, 55 jobs), Swan (Ashby, 6 jobs), Younited (Lever, 8 jobs).
Manager One only looked present: the name check matched the word "manager". It is not.

## Qonto: present but dead
`Qonto (lever)` (id 9) has returned 0 jobs for 3 runs. Its jobs are on Ashby board `qonto`: 50 live, 32 in Paris / Ile-de-France (Lever 0, Workable 0, Greenhouse error). Fix: add `Qonto (ashby)`, switch off `Qonto (lever)` (switched off, not deleted).

## New sources (3 + Qonto)
| Employer | Type | Board | Live jobs | Paris / IDF |
|---|---|---|---|---|
| Epsor | teamtailor | epsor.teamtailor.com | 7 | 4 |
| Kaiko | teamtailor | jobs.kaiko.ai | 3 | 0 (Amsterdam, Zurich) |
| Marble | ashby | marble | 5 | 4 |
| Qonto | ashby | qonto | 50 | 32 |

Kaiko is added anyway (the owner's list; it will show Paris jobs if it posts any).

## WelcomeKit group (Fintecture, Linxea, Sidecare, +Simple, Tiime, Basikon, MiTrust, Yomoni)
Their `*.welcomekit.co` sites are gone or show only a spontaneous-application form. Route: their slugs go into the `companies` list of the existing hosted "Welcome to the Jungle (Paris)" source (id 103). WTTJ's sitemap on 2026-11-04 had Paris listings for basikon (4), linxea (5), sidecare (4); none for fintecture, karbonalpha, mitrust, yomoni; tiime's listings are outside Paris. Slugs to add: basikon, linxea, sidecare, karbonalpha, mitrust, yomoni, fintecture, tiime, plus-simple, anaxago. karbonalpha is confirmed by the owner's WTTJ link; plus-simple and the others are unverified (harmless if unmatched).

## Listed as unsupported (5), `docs/unsupported_employers.csv`
Cashbee (only Typeform forms), Manager One (a Notion page), Paytweak and RockFi (nothing readable): `no_feed_found`. Anaxago: `partial` (links to WTTJ). Terms of these custom sites were not read because no source is added for them.

## Repo state
Seed entries and the five list rows are written; `tests/test_fr_fintech_batch.py` (7 tests) passes; full suite 1,443 passed on the scratch database.

## Hosted database: done (2026-11-04, at the owner's "Yes, do it")
One transaction with checks (names and states asserted, counts before and after): 4 sources created ON (Epsor 359, Kaiko 360, Marble 361, Qonto Ashby 362), `Qonto (lever)` (id 9) switched off, 10 slugs added to the Welcome to the Jungle source 103 `companies` (27 to 37). Sources 349 to 353, enabled 338 to 341. Only `jobs_source` rows changed. They have not run yet: the owner's next by-hand pass reads them. (The first attempt was blocked by the permission classifier until the owner approved.)
