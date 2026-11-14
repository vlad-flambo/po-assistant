# Consulting employers against the sources we already have (2026-11-03, step 2 slice 14)

A fresh restore of the newest dump (29 Oct 10:05: 328 sources), read only; no request to any site. Matched by words in a source's name or configuration, in `seed_employers.py`, and in the company of the jobs already in the catalogue (they arrive through aggregators and other sources). Word matches are leads for a human to read, not verdicts.

| Employer (as in the lists) | Existing source (name, on/off) | In `seed_employers.py` | Jobs already in the catalogue (company: count) | In `unsupported_employers.csv` |
|---|---|---|---|---|
| Boston Consulting Group | none | none | 2 (Boston Consulting Group: 2) | no |
| Capgemini (Invent) | none | Capgemini (capgemini) | 16 (Capgemini: 16) | no |
| Deloitte | none | none | 34 (Deloitte: 34) | no |
| EY | none | none | 20 (Ey: 17, EY: 3) | no |
| McKinsey & Company | none | none | 0 | no |
| Sia Partners | none | none | 0 | no |
| Sopra Steria | Sopra Steria (smartrecruiters) (ON) | none | 196 (Sopra Steria: 196) | no |
| Wavestone | Wavestone (smartrecruiters) (ON) | none | 222 (Wavestone: 222) | no |
| Alvarez & Marsal | none | none | 14 (Alvarez Marsal France: 14) | no |
| Bain & Company | none | none | 0 | no |
| CGI | none | none | 9 (Cgi: 8, CGI: 1) | no |
| Cognizant | none | none | 1 (Cognizant: 1) | no |
| Eurogroup Consulting | none | none | 0 | no |
| HCLTech | none | none | 0 | no |
| IBM Consulting | none | none | 0 | no |
| Inetum | none | none | 0 | no |
| Infosys | eFinancialCareers (Paris) (efinancialcareers) (ON) | none | 0 | blocked |
| KPMG | none | none | 3 (Kpmg France: 2, KPMG: 1) | no |
| Kearney | none | none | 0 | no |
| Magellan Partners | none | none | 0 | no |
| Onepoint | none | none | 0 | no |
| Publicis Sapient | none | none | 0 | no |
| PwC | none | none | 0 | no |
| TCS (BaNCS) | none | none | 0 | no |
| Wipro | none | none | 0 | no |
| Eviden (Atos) | Atos (successfactors) (ON) | none | 35 (Atos: 35) | no |
| Sword Group | none | none | 0 | no |

## Reading (slice 14)
**28 consulting-like employers checked; 5 need no new source, 23 remain.**
| Verdict | Employers | Why |
|---|---|---|
| **Already covered** (the lists said `unknown`: a naming gap, like Amundi in step 1) | **Sopra Steria**, **Wavestone** | enabled SmartRecruiters sources `Sopra Steria (smartrecruiters)` (`SopraSteria1`, 216 links, 196 jobs) and `Wavestone (smartrecruiters)` (`Wavestone1`, 273 links, 222 jobs), last run 2026-10-28; the company names match the employers. They were not in the 2026-10-30 re-check (the lists did not call them covered) |
| **Covered by another source** | **Eviden (Atos)** | the `Atos (successfactors)` source (`jobs.atos.net`, 38 links) carries 30 jobs that mention Eviden: Eviden is an Atos brand. *To verify when the hosted listing is read* |
| **Covered by the new Capgemini source** (seeded, not yet on the hosted database) | **Capgemini (Invent)** | its jobs come through the Capgemini job search under the brand "Capgemini Invent" (16 of the first 3 pages in step 1's rehearsal) |
| **Already has a verdict** | **Infosys** | `Finacle / Infosys` is in `unsupported_employers.csv` as `blocked` (the match on the eFinancialCareers source is only a keyword) |
| **Still to do (23)** | **priority B:** Boston Consulting Group, Deloitte, EY, McKinsey & Company, Sia Partners; **priority C:** Alvarez & Marsal, Bain & Company, CGI, Cognizant, Eurogroup Consulting, HCLTech, IBM Consulting, Inetum, KPMG, Kearney, Magellan Partners, Onepoint, Publicis Sapient, PwC, TCS (BaNCS), Wipro, Sword Group | no source, nothing in the seed |

Jobs of the 23 already in the catalogue through aggregators (they will merge with a source's jobs): Deloitte 34, EY 20, Alvarez & Marsal 14, CGI 9, KPMG 3, BCG 2, Cognizant 1; the others 0. The hosted database may differ from this copy: the owner's dry-run listing (step 1, slice 12) is the check, and slice 19's dry run compares names again.
