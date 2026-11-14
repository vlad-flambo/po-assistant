# Consulting batch B: McKinsey, Deloitte, EY, Sia Partners (2026-11-03, step 2 slice 16)

(BCG: [bcg_2026-11-03.md](bcg_2026-11-03.md). Sopra Steria, Wavestone, Capgemini Invent: already covered, [slice 14](consulting_duplicates_2026-11-03.md).) Method as in step 1: discovery from the employer's own site (robots obeyed), a scan of the careers page, a live read with the app's own adapter and no database, robots, terms, then a seed entry with a test or a row in `unsupported_employers.csv`. Requests: about 130, not counted exactly (the plan said about 80 for these four): EY's sitemap is 2 MB and was read four times.

## Verdicts
| Employer | Verdict | Why |
|---|---|---|
| **EY** | **source** (`successfactors`), seeded off | `careers.ey.com` is a worldwide SAP SuccessFactors site (8,796 job addresses in its sitemap). Config `{"url": "https://careers.ey.com", "company": "EY", "location": "Paris", "max_jobs": 60}`: the place word **Paris** in the job address keeps **161 jobs** (EY France: `Paris-La-Défense-…-92037`). See the finding below |
| **McKinsey & Company** | `blocked` | mckinsey.com answers HTTP 403 to the app's requests (bot protection); left alone, no workaround |
| **Deloitte** | `no_feed_found` | its France careers page (`deloitte.com/fr/fr/careers`, results at `/careers/content/job/results.html`) draws the list with a script the page does not name; the France sitemap (1,817 pages) holds no job page; robots.txt allows reading, so the stop is technical, not a refusal |
| **Sia Partners** | `needs_adapter` | public server-rendered pages: about 55 list pages (`/fr/opportunities?page=N`) and one page per job (`/fr/career/<name>`), robots allows them, but the job pages carry no structured data (no JobPosting, a title and page text only): reading them well needs an adapter for this one site, which the approved scope excludes (an adapter only when three or more employers share a system) |

## Finding: the city test reads US ZIP codes as Paris postal codes
With the app's usual city rules the EY sitemap gives 325 matches, of which **219 (67 %) are US jobs** whose address ends in a state and ZIP such as `TX-75219` (Dallas), `CA-94…`; the others include `Karachi-…-75600`. The rules treat 75, 77, 78 and 91 to 95 followed by three digits as an Ile-de-France postal code. On a French site that is right; on a worldwide one it fills the 60-new-pages-a-run cap with the wrong jobs first and stores hundreds of US roles. My first live read of EY (before I looked at the addresses) printed "Paris" for Dallas jobs for this reason, and my first fixtures held them. The adapter's own `location` option (a place word looked for in the address instead of the cities) avoids it, so EY is seeded with `"location": "Paris"`, and a test (`test_without_the_place_word_the_usual_city_test_lets_the_dallas_zip_through`) keeps the reason visible. **The shared city test itself was not changed** (out of scope): any other worldwide SuccessFactors or sitemap source of the catalogue could have the same effect; a later check could look for US-looking jobs among the stored ones.

## Terms and robots (criterion S2.1, read 2026-11-03)
| Employer | Page read | Automated reading | Reuse | robots.txt |
|---|---|---|---|---|
| EY | `ey.com/en_us/legal-and-privacy` and its Legal Statement | **not addressed** | a copyright notice: site material may not be reproduced or transmitted without permission; RSS feeds and podcasts for personal, non-commercial use; linking allowed except framing (a small model's summary, not legal advice); job postings not named | `careers.ey.com/robots.txt`: disallows apply, talent community, e-mail, services and pre-apply paths; the sitemap and job pages are open |
| McKinsey, Deloitte, Sia Partners | not read: no source is added | | | Deloitte: only the sitemap index is listed; Sia: ordinary rules |

## Checks
- `tests/test_ey_source.py` (4 tests on real EY data: three Paris jobs, a Dallas job with ZIP 75219, one in Mumbai, a search page): seeded off with the place word; only the Paris jobs are kept and the Dallas and Mumbai pages never opened; the false positive without the place word; a run stores each job once.
- **Postgres rehearsal** on the scratch copy (the real runner, `max_jobs` 5): run 1 `ok fetched=5 new=5`, run 2 `new=0`; descriptions 9,900 to 13,400 characters, language `fr`. Its first attempt ended in an error that was not EY's: the scratch copy is the 29 Oct schema, and the code now expects `jobs_candidatejob.auto_rejected_at` (migrations 0041 to 0043, another session's work, committed or not: not mine). **I applied 0041 to 0043 to the scratch copy only**; the same three migrations will have to reach the hosted database when that work is deployed, and slice 20's measurement runs on the migrated copy.
- The three `unsupported_employers.csv` rows (dated 2026-11-03) and the existing list test (`needs_adapter` was allowed in step 1).

## Not done here
EY's full 161-job read (slice 20 measures it); the owner's hosted step (slice 21); the lists in `data/` (S2.8).
