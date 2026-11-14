# Intent: more sources (employers' own sites, VC boards, aggregators, Personio)

| | |
|---|---|
| **Cycle** | 013 |
| **Stage** | Intent approved 2026-10-30; Spec approved 2026-10-30 ([spec.md](spec.md), employers step); Plan drafted ([plan.md](plan.md)) |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Born from** | The PRD audit of 2026-10-29: outstanding items moved here from the PRDs (see the table below). |
| **Importance** | 3/5 (claude, 2026-10-30): new channels bring jobs friends would not see; legal review still to do |

## The request, in your words
> Do a full audit of the PRD files. I want to migrate anything outstandin into the ai sdlc framework, using the ai-sdlc skill

Added 2026-10-30 (owner, `/ai-sdlc`):
> add employer sources
> check if there is an intent that already treats this topic. if so, add this to it and let's get it started.
> accenture https://www.accenture.com/fr-fr/careers/jobdetails?id=R00345449_fr-fr&src=LINKEDINJP
> capgemini https://www.capgemini.com/fr-fr/jobs/207491-fr_FR+sap_btp/
> saegus https://careers.saegus.com/jobs/3761896-manager-agile-design-thinking-innovation/0425e2fd-f017-4265-a963-0f00e1a31bc0

Order, 2026-10-30 (owner):
> first, let's pick back the other employer lists, all in the data folder. I want to ensure those are also included in step 1. then step 3, then step 4. move step 2 as a separate intent. I'd say low priority as it would require complex email access set up for users

Added 2026-11-03 (owner, through the feedback chat: feedback #3, an idea from C-01 (vlad) on 2026-10-31, Inbox, phone, standard mode, language en; pasted as an intent draft):
> Add consulting employers
> Example
> https://careers.bcg.com/global/en/job/BCG1US56128EXTERNALENGLOBAL/Lead-Principal-AI-Tech-Architect-%E2%80%94-Paris-BCG-Platinion?utm_source=linkedin&utm_medium=phenom-feeds&Source+=LinkedIn+Job+Board

Answers in the chat: what do you do today instead? "Nothing, I just can't"; how useful? "I can't do without it"; how often? "Every week".

### What this cycle inherits from the PRDs
| Item | Where it came from |
|---|---|
| ~~Importing job-alert e-mails (WTTJ, LinkedIn); open question 6, which of three options~~ **moved 2026-10-30 to [cycle 018](../018-alert-emails/intent.md)** (owner: low priority) | PRD.md §5 'Alert emails', §11 M4, §13 Q6 |
| ~~The `saxobeat.jobs.v1` import format for a supervised session~~ **moved to cycle 018** | PRD.md §5 option 2 |
| Aggregators: Jooble, Careerjet, Hellowork, RemoteOK, We Work Remotely, Himalayas, HN, public sector | PRD.md §5 rows 6-8, 11, 12 |
| Personio | PRD.md §5 row 9 |
| VC portfolio boards (Getro, Consider) | PRD_competitive_features.md F12, phase 10 |
| **Added 2026-10-30:** three employers' own career sites: Accenture, Capgemini, Saegus (the owner's request above); none is in `seed_employers.py` or `docs/unsupported_employers.csv` | owner, 2026-10-30 |
| **Added 2026-10-30:** the employer lists in `data/` (the general list of 265, the Next40 / French Tech 120, CAC 40 / SBF 120 / ETI, international employers): 593 distinct employers with a coverage status | owner, 2026-10-30; `data/employer_coverage*.csv` |
| **Added 2026-11-03:** consulting employers (feedback #3): the lists already hold 25 "5. Conseil & intégrateurs" employers still `unknown` (priority B: 8, C: 17), which this cycle's approved spec put out of scope until priority A was measured | owner, 2026-11-03; `data/employer_coverage.csv` |
| Legal review of every source; eFinancialCareers' terms not reviewed | PRD.md §2, §5 |

## Why now / the pain
The catalogue misses whole channels (alerts, aggregators, VC boards); the PRDs planned them and the legal review was deferred.

## Goal
Add the sources that bring jobs friends would not otherwise see, each checked against its terms first, in this order: employers' own career sites (the three and the lists in `data/`), then VC boards, then aggregators. The first spec covers the employers only; VC boards and aggregators each get their own spec when their turn comes.

## Success measure
*(redrafted 2026-10-30, to confirm)* For the employers step:
1. Every employer marked "covered" in the four lists has been re-checked, and the wrong ones are listed and corrected (a count, with Accenture's Recruitee board as the first).
2. Saegus, Accenture and Capgemini each end with a verdict: a working source with a test, or a recorded reason (Capgemini may be parked).
3. Each of the 18 priority-A unknown employers ([list](evidence/priority_a_unknown_2026-10-30.md)) ends with a verdict: a source added, or listed in `unsupported_employers.csv` with the reason.
4. After a week, the share of jobs from the new sources that are new to the catalogue and in the candidates' cities.

For VC boards and aggregators: the same per-source tests (terms recorded, an adapter with a test, the new-job share after a week).

## Not doing (this cycle)
- Bypassing any anti-bot protection (a standing rule).
- Alert e-mail import: moved to cycle 018.
- Priority B and C unknown employers (until A has been measured).

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| `jobs/sources/` has no adapter for these; Personio is labelled unsupported in `employers.py` | audit 2026-10-29 |
| Sources are read from the operator's PC only | DEPLOY.md |
| Saegus is Teamtailor on its own domain: `careers.saegus.com/jobs.rss` answers 200 with 16 jobs, and the app has a `teamtailor` adapter | probe, [evidence](evidence/employer_probe_2026-10-30.md) |
| Accenture's job pages carry a `JobPosting` and its fr-fr job sitemap lists 173 job pages: the `sitemapjobs` adapter may read it; robots.txt disallows only the search page | probe, same file |
| Capgemini's job page has no `JobPosting` and no job sitemap was found; the list is drawn by a script: no existing adapter fits yet | probe, same file |
| Coverage of the 593 distinct employers in the four lists (best status across files): **252 covered, 327 unknown, 14 unsupported**; the lists were last probed 2026-10-01 to 2026-10-05; `data/` is gitignored (local files only) | `data/employer_coverage*.csv`, read 2026-10-30 |
| Priority A employers still unknown: 19 in the general list and 1 in Next40 (B: 53 and 10; C: 72 and 45); **18 after merging the four lists** (two are covered in another list) | same files; [list](evidence/priority_a_unknown_2026-10-30.md) |
| **A "covered" status can be false.** Accenture is "covered: recruitee source, on" in two lists, but `accenture.recruitee.com` holds 2 jobs, both in the Netherlands, one titled "(Sample)": it is not Accenture France. The slug guess found a stranger's board | probe of `accenture.recruitee.com/api/offers`, 2026-10-30 |
| Accenture's real jobs are therefore probably not read today (the hosted catalogue was not queried; the coverage files date from 2-5 October); Capgemini is "unknown" in two lists (its SuccessFactors address did not answer) | same files |
| This cycle was chosen for the request because it is the open "more sources" cycle; it covered channels, and now also employers' own sites | claude, 2026-10-30 |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Which first? | Per source: terms first, then build. Order: employers (the three + the lists in `data/`), then alert e-mails, then VC boards, then aggregators after measuring overlap | **Employers (the three and the lists in `data/`), then VC boards, then aggregators; alert e-mails out to their own low-priority cycle 018** (owner, 2026-10-30) | answered |
| Q2 | Alert e-mails: which of the three options? | Moved to [cycle 018](../018-alert-emails/intent.md) Q1 | Moved out of this cycle by the owner, 2026-10-30 | parked |
| Q3 | For the three employers: watch each employer's whole list of jobs (as a source), not only the one job in each link? | Yes: the link only shows which hiring system each uses; the source then brings every matching job. The three jobs linked are caught by the first run | Yes, whole lists (owner, 2026-10-30) | answered |
| Q4 | Capgemini has no adapter that fits: look a little further for a feed behind its script (no bypassing), and park it if none is found? | Yes: park it in `unsupported_employers.csv` as `no_feed_found` with the reason, and keep paste-a-link for it | Yes (owner, 2026-10-30) | answered |
| Q5 | Order: Saegus first (config only), then Accenture (try `sitemapjobs`), then Capgemini? Each only after its terms are read | Yes | Yes (owner, 2026-10-30) | answered |
| Q6 | For the other employers in `data/`: first re-check the 252 "covered" (the Accenture error shows a slug guess can find a stranger's board), then work the 327 unknown, priority A first? | Yes: re-check first, by asking each covered source for a few jobs and comparing company and city with the employer (a read-only script); then the unknown A employers (18 once the lists are merged: 19 + 1, two of which another list marks covered); B and C only after measuring what A brings | Yes, as recommended (owner, 2026-10-30) | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- More runs read more from Neon (cycle 001).

## Gate
- [x] All open questions answered or parked (2026-10-30: Q1, Q3-Q6 answered, Q2 moved to cycle 018)
- [x] Goal and success measure confirmed by the owner (2026-10-30, redrafted measure)

## Step 2 (added 2026-11-03): consulting employers, Q7 to Q9 answered; criteria and slices in [step2-consulting.md](step2-consulting.md), awaiting the owner's approval
Kept apart from the gate above on purpose: the intent of step 1 stays approved and the board keeps showing the build stage.

### What we already know (step 2)
| Fact | Source |
|---|---|
| The lists in `data/` hold 25 category-5 employers still `unknown`: **priority B** Boston Consulting Group, Capgemini (Invent), Deloitte, EY, McKinsey & Company, Sia Partners, Sopra Steria, Wavestone; **priority C** Alvarez & Marsal, Bain & Company, CGI, Cognizant, Eurogroup Consulting, HCLTech, IBM Consulting, Inetum, Infosys, KPMG, Kearney, Magellan Partners, Onepoint, Publicis Sapient, PwC, TCS (BaNCS), Wipro. Three more consulting-like rows sit in other lists (IBM, Eviden (Atos), Sword Group) | `data/employer_coverage*.csv`, 2026-11-03 |
| 13 consulting-like employers are marked covered (Accenture was the false one, fixed by this cycle's work; Alten, Atos, Aubay, BearingPoint, Devoteam, Forvis Mazars, Keyrus, Oliver Wyman, Roland Berger, Talan, Thoughtworks have sources) | same files; the 2026-10-30 re-check |
| **BCG's example link is a Phenom site and the existing `phenom` adapter reads it**: `{"host": "careers.bcg.com", "site": "global/en", "countries": ["France"]}`; robots.txt allows the job pages and the sitemap; 3 jobs read live, all in Paris, descriptions 4,200 to 5,700 characters | one live read with the adapter (no database), 2026-11-03 |
| The example job (a BCG Platinion role in Paris) comes from a Phenom feed shared with LinkedIn (`utm_medium=phenom-feeds`); the adapter's own job addresses are numeric (`/global/en/job/60809`) | the pasted link; the live read |
| The machinery of step 1 applies as it is: the discovery routine (with its Workday-link fix), the re-check, `seed_employers --only`, `scripts/seed_hosted_sources.ps1`, the per-source terms line and the Postgres rehearsal | cycle 013, slices 1 to 11 |
| The owner's own answers: "I can't do without it", needed "every week", nothing done today instead | feedback #3 |

### Open questions (step 2)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q7 | Where does this go: as a second step of cycle 013 (its own criteria and slices, the same machinery, one cycle to close), or as a cycle of its own? | Step 2 of 013: the lists, the method and the seed script are the same; the spec and plan get an addendum for the owner to approve. Slice 12 (the owner's hosted step for the first ten sources) is not delayed by it | Step 2 of 013 (owner, 2026-11-03) | answered |
| Q8 | Which employers: the 25 unknown category-5 rows (B first, then C), plus any consulting firm you name that is not in the lists? | Yes, B first (BCG, McKinsey, Deloitte, EY, Wavestone, Sia Partners, Sopra Steria, Capgemini Invent), then C; the same verdict for each: a source with a test, or a line in `unsupported_employers.csv` with the reason | Accepted as recommended (owner, 2026-11-03) | answered |
| Q9 | Success measure? | Each of the 25 ends with a verdict; and after a week, the number of consulting jobs in your cities that are new to the catalogue (you said you need it every week) | Accepted as recommended (owner, 2026-11-03) | answered |
