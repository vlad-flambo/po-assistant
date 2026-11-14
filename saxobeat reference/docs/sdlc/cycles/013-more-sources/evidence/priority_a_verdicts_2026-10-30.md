# The 18 priority-A employers: verdicts (2026-10-30, slice 9)

Method for each: the careers link in the lists (or the home page), the hiring system behind it (`jobs/careers.py` discovery, robots.txt obeyed, then a scan of the careers page for any known hiring-system host), a live read with the app's own adapter (no database), robots.txt of the exact endpoints, and the terms page. The earlier probe (1 Oct) had only guessed board names on seven public systems; none of these had been looked at through their own site. List: [priority_a_unknown_2026-10-30.md](priority_a_unknown_2026-10-30.md). Request count: about 190, not counted exactly (the plan said about 10 per employer).

## Result: 7 new sources, 1 already covered, 10 stay out

*(Corrected the same day, in slice 10: Amundi was first counted as a new source; the 29 Oct database already holds an enabled `Amundi (talentsoft)` source on the same address, last run 28 Oct, 147 jobs stored. The list's entry was "Amundi (Amundi Technology)", so the earlier "unknown" was a naming gap.)*
| # | Employer | Verdict | Hiring system and address | Read live (adapter, no database) |
|---|---|---|---|---|
| 1 | Backbase | **source** (`greenhouse`) | Greenhouse board `workatbackbase` (found by a web search; the 1 Oct guess `backbase` had missed it) | 63 jobs, company "Backbase"; **none in Paris / Ile-de-France** (Amsterdam, Hyderabad, Sydney...) |
| 2 | Checkout.com | **source** (`ashby`) | Ashby board `checkout.com`, linked from its careers page | 166 jobs, 8 in Ile-de-France |
| 3 | Fenergo | **source** (`workable`) | Workable account `fenergocareers`, linked from its careers page | 30 jobs, **none in Paris** (Singapore...) |
| 4 | Payhawk | **source** (`greenhouse`) | Greenhouse EU board `payhawkio` (embedded in `payhawk.com/fr/recrutement`) | 49 jobs, 5 in Paris |
| 5 | Amundi (Amundi Technology) | **already covered** by the existing `Amundi (talentsoft)` source (not seeded again) | `jobs.amundi.com`, a Cegid Talentsoft site (linked from `about.amundi.com/join-us`) | first 5 jobs: title and description complete, no place text (so the Paris count is unknown) |
| 6 | Finastra | **source** (`workday`) | `finastra.wd3.myworkdayjobs.com/FINC`, linked from finastra.com (this crashed the discovery: fixed, see below) | 5 jobs on the "Paris" search, all in Paris |
| 7 | Murex | **source** (`workday`) | `murex.wd3.myworkdayjobs.com/MurexCareerPage1` | 5 jobs, all in Paris |
| 8 | SWIFT | **source** (`workday`) | `swift.wd3.myworkdayjobs.com/Join-Swift` | the "Paris" search returns 1 job, in London: **close to nothing for Paris** |
| 9 | Banking Circle | `needs_adapter` | HR Manager (`candidate.hr-manager.net`), linked from its careers page | not read: no adapter |
| 10 | Taurus | `needs_adapter` | JOIN (`join.com`), linked from its careers page | not read: no adapter |
| 11 | Vermeg | `no_feed_found` | careers page found, no hiring system in it (script-loaded list) | none |
| 12 | Tuum | `no_feed_found` | `tuum.com`'s robots.txt could not be read: **left alone**; `tuum.tech/careers` 404 | none |
| 13 | SimCorp | `no_feed_found` | no careers page from simcorp.com (404); a third-party site says Workday, tenant and site not found | none |
| 14 | Shares | `no_feed_found` | the list's careers link 404s; no jobs link on the home page | none |
| 15 | Nickel (BNP Paribas) | `partial` | its careers page is hosted on Welcome to the Jungle | via the WTTJ source (off by default) |
| 16 | SBS (74Software) | `partial` | a web search shows its jobs on Welcome to the Jungle (company `sbs`), not opened here | via the WTTJ source |
| 17 | Kyriba | `partial` | `kyriba.com`'s robots.txt could not be read: **left alone**; a web search shows WTTJ (company `kyriba`), not opened here | via the WTTJ source |
| 18 | Universal Banking (ex-Finastra) | `partial` | still part of Finastra until the sale to Pollen Street Capital closes (reported: end 2026 or early 2027) | its jobs are in the Finastra Workday board |

Counts: **7 new sources, 1 already covered, 10 in `docs/unsupported_employers.csv`** (2 `needs_adapter`, 4 `no_feed_found`, 4 `partial`). No `blocked`: nothing was refused by a site. Backbase, Fenergo and SWIFT are valid boards that list almost nothing in Paris: the owner may leave them switched off (decision at slice 12).

## Terms and robots (criterion 1; read 2026-10-30, before any source exists)
| Source | What was read | Automated reading | Reuse of content | robots.txt of the endpoint |
|---|---|---|---|---|
| Backbase, Payhawk (Greenhouse) | Greenhouse Job Board API doc (docs.greenhouse.io/job-board.html) | the doc says "authentication is not required for any GET endpoints"; no rule on rates or automated use | none stated | boards-api.greenhouse.io: allowed |
| Checkout.com (Ashby) | Ashby public job posting API doc (developers.ashbyhq.com) | the page does not say it is public or authless; its example request has no key; no rule on rates | none stated | `api.ashbyhq.com/robots.txt` answers **401 (no rules published)**; my helper reads that as "not allowed", but the API adapters (Greenhouse, Lever, Ashby, Workable, Workday) never consult robots and the 40 Ashby sources already live work the same way |
| Fenergo (Workable) | no terms page read: the board is Workable's own career widget address (`apply.workable.com/api/v3/...`, the one its public page calls) | not addressed (nothing read) | not read | apply.workable.com: allowed |
| Amundi (Talentsoft; source already existed) | `about.amundi.com/legal-notices` | not addressed; forbids "excessive use" | "reproduction ... strictly forbidden without the prior written consent of Amundi" | jobs.amundi.com: allowed |
| Murex (Workday) | `murex.com/en/terms-of-use` | not addressed | copying and reuse forbidden unless authorised, reproduction "for information purposes only" | murex.wd3.myworkdayjobs.com: allowed |
| **Finastra (Workday)** | `finastra.com/terms-conditions`: **not read** (the fetch tool got HTTP 403) | **unknown** | **unknown** | finastra.wd3.myworkdayjobs.com: allowed |
| **SWIFT (Workday)** | `swift.com/about-us/legal`: **not read** (HTTP 403) | **unknown** | **unknown** | swift.wd3.myworkdayjobs.com: allowed |

Reading: where read, nothing forbids automated reading, and every general terms page forbids reproducing content without consent: the same posture as the sources already live (PRD.md §2 defers the product-level review). **Two terms are unread (Finastra, SWIFT): the owner should read them in a browser before enabling those two sources**; they are seeded switched off. Fenergo's terms were not read either; Workable's page is the public one its own careers site calls.

## A bug found and fixed on the way
`jobs/careers.py` (the discovery routine, also behind `manage.py employer_coverage --discover`) crashed with `KeyError: 'workday'` whenever a home page linked to a Workday site: Finastra, Murex and SWIFT all did, and Finastra's 1 Oct run had recorded "error: KeyError". Now such a link is reported ("links to workday (not checked here): <address>") and the discovery goes on. Test in `tests/test_careers.py`. Other employers in the lists that link to Workday, Oracle or other systems the quick check does not know were also hit by this and may deserve a re-run of the discovery (slice 5 / a later step).

## Not verified
Whether Finastra's, SWIFT's and Fenergo's terms forbid anything; Amundi's place text (its jobs carry none); that the three Welcome to the Jungle slugs (`sbs`, `kyriba`, Nickel's) exist; any Paris job count beyond the first 5 of Amundi, Finastra and Murex; ingest into Postgres (slice 11 runs all new sources through the scratch copy: the Accenture currency bug showed why).
