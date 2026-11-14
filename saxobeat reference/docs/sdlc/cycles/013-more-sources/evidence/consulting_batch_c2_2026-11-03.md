# Consulting batch C, second half (2026-11-03, step 2 slice 18)

KPMG, Kearney, Magellan Partners, Onepoint, Publicis Sapient, PwC, TCS (BaNCS), Wipro, Sword Group. Method as before: discovery from the employer's own site (robots obeyed), a scan of the careers page, a targeted look at each lead with the app's own adapters (no database), robots and terms. Requests: about 110, not counted exactly (the plan said about 90). **Result: 3 sources (Onepoint, and PwC through its two Workday sites), 7 employers listed in `unsupported_employers.csv`** (dated 2026-11-03).

## Sources (seeded switched off)
| Source | System and address | Live read (adapter, no database) | Size |
|---|---|---|---|
| **Onepoint** | Workday `onepoint.wd3.myworkdayjobs.com`, site `OnepointFR`, linked from its careers page (this is the page that crashed the discovery in step 1 until the Workday-link fix) | first 5 jobs on the "Paris" search: all in Paris, company "Onepoint", descriptions complete | 267 jobs; 226 match "Paris"; places mostly Paris, some Nantes and Casablanca |
| **PwC** (experienced hires) | Workday tenant `pwc`, site `Global_Experienced_Careers`, linked from `carrieres.pwc.fr`; search word **Neuilly** (Neuilly-sur-Seine, PwC France's address, in Ile-de-France) | first 4: all Neuilly-sur-Seine, company "PwC", descriptions complete | 112 results for "Neuilly" |
| **PwC Campus** (stages, young graduates) | same tenant, site `Global_Campus_Careers`, search word **Neuilly** | counted through the site's own search (41 results), not read in full | 41 results |

The word "France" does not work for PwC (it brings Rome and Milan: the search is a loose text match), and "Paris" gives only 40, mostly Neuilly again; "Neuilly" is the precise one. PwC's other France offices (Toulouse, Bordeaux, Lyon...) are outside the owner's cities and are not read.

## Listed (7)
| Employer | Status | What was found |
|---|---|---|
| KPMG | `no_feed_found` | `kpmg.com` careers pages and `emplois.kpmg.fr` (KPMG France's own platform): no hiring system, no job data, script-loaded |
| Kearney | `needs_adapter` | jobs on Recruiting Solutions (`kearney.recsolu.com`); no adapter |
| Magellan Partners | `no_feed_found` | robots.txt could not be read: the site is left alone |
| Publicis Sapient | `blocked` | jobs are on Publicis Groupe's iCIMS site (`publicisgroupe.icims.com`) whose **robots.txt forbids reading the job list** (the app's own check said so); `careers.publicissapient.com/job-search` is script-loaded |
| TCS (BaNCS) | `no_feed_found` | `tcs.com/careers` leads to its own iBegin platform; no readable list |
| Wipro | `no_feed_found` | **readable but useless:** `careers.wipro.com` is SAP SuccessFactors (6,530 job addresses) and none names a French city |
| Sword Group | `no_feed_found` | **readable but useless:** Workable board `sword-group`, 121 jobs, every one in the United Kingdom |

## Terms and robots (criterion S2.1, read 2026-11-03)
| Source | Page read | Automated reading | Reuse and extraction | robots.txt of the endpoint |
|---|---|---|---|---|
| Onepoint | `groupeonepoint.com/fr/conditions-generales-dutilisation/` | not addressed (no word about bots or crawlers) | **"toute reproduction, extraction, divulgation, distribution" of the Site is forbidden without prior authorization, "même pour une partie non substantielle"**; a section also forbids use that could interrupt or harm the Site (a small model's summary, not legal advice) | `onepoint.wd3.myworkdayjobs.com`: the app's check allows the Workday API |
| **PwC** (both sources) | `carrieres.pwc.fr/fr/legal.html` and `pwc.fr/fr/mentions-legales.html`: **not read** (HTTP 403 to the fetch tool) | **unknown** | **unknown** | `pwc.wd3.myworkdayjobs.com`: allowed |

**Two decisions for the owner before enabling, which is why both are seeded off:**
1. **Onepoint.** Its site terms forbid "extraction" of the Site's content without authorization. They do not mention bots, and the jobs are on a Workday-hosted careers site that the terms do not name, but a reader may take "extraction" to cover this. The standing rule is no scraping of a site whose terms forbid it: this is the owner's call (and a point for the product-level review).
2. **PwC.** The two legal pages were not readable by the tool: read them in a browser before enabling.

## Checks
`tests/test_consulting_sources.py` (3 Workday entries: the keys, the narrow search, switched off, one company name for both PwC sources, seeded once; the seven listed rows and none of them also a source). The three Workday sources were **not** rehearsed on Postgres here to spare requests: the Workday adapter already ran on Postgres in step 1 (slice 11), and slice 20 runs all new sources through the scratch copy. Full suite: see the plan log.

## Not verified
The full read of PwC's and Onepoint's lists (slice 20); PwC's terms; whether "Neuilly" misses PwC France roles in Paris or La Defense (the "Paris" search found 40 results, mostly Neuilly; the owner can compare with the site); IBM-style script-loaded lists a real browser would show.
