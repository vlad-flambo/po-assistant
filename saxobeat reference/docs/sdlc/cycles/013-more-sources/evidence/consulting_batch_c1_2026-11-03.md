# Consulting batch C, first half (2026-11-03, step 2 slice 17)

Alvarez & Marsal, Bain & Company, CGI, Cognizant, Eurogroup Consulting, HCLTech, IBM Consulting, Inetum (Infosys already has a `blocked` row, slice 14). Method as in step 1 and batch B: discovery from the employer's own site (robots obeyed), a scan of the careers page, then a targeted look at each lead (a live read with the app's adapter and no database, sitemaps, the page's own scripts). Requests: about 90, not counted exactly (the plan said about 90). **No source results: 8 rows in `unsupported_employers.csv`**, dated 2026-11-03. No source is added, so no terms line is needed (S2.1 applies to added sources).

## Verdicts
| Employer | Status | What was found |
|---|---|---|
| Alvarez & Marsal | `blocked` | alvarezandmarsal.com answers HTTP 403 to the app's requests; left alone, no workaround. Its 14 France jobs in the catalogue come through aggregators |
| Bain & Company | `no_feed_found` | careers page and `find-a-role` page found; no hiring system, no JobPosting data, no job-list address in the page: the list is script-loaded |
| CGI | `needs_adapter` | jobs are on **Njoyn** (`cgi.njoyn.com`), linked from `cgi.com/en/careers`; no adapter |
| Cognizant | `no_feed_found` | `careers.cognizant.com` looks like Phenom (the `/global/en/search-results` shape) but its `/widgets` answers 405 to the Phenom request, so the existing adapter does not fit; its sitemap lists 16,992 job addresses in 8 locales (none French), and a job page carries no structured data |
| Eurogroup Consulting | `needs_adapter` | jobs are on **Recruitment Platform** (`eurogroup.recruitmentplatform.com`, 5 links on its careers page); no adapter |
| HCLTech | `no_feed_found` | **readable but useless**: `careers.hcltech.com` is an SAP SuccessFactors site whose sitemap lists 15,144 job pages, and the existing `successfactors` adapter reads that kind; **none of the addresses names France or a French city** (checked for 17 city words), so a source would bring nothing for this app's cities. Worth another look if HCLTech opens jobs in France |
| IBM Consulting | `no_feed_found` | `ibm.com/careers/search` is script-loaded; the page and the two script bundles read (a third answered 404) name no job-list address (the search service is not named in them); `careers.ibm.com` is the older site |
| Inetum | `no_feed_found` | careers page is an AEM search page; none of the country sitemaps read (global, Portugal) lists a job page; the mentions of SuccessFactors and Workday on the page are job titles |

## Counts and reading
**0 sources, 8 listed:** 1 `blocked`, 2 `needs_adapter` (CGI on Njoyn, Eurogroup on Recruitment Platform), 5 `no_feed_found`. Hiring systems without an adapter now seen across step 1 and step 2: HR Manager (Banking Circle), JOIN (Taurus), Njoyn (CGI), Recruitment Platform (Eurogroup), a custom HTML site (Sia Partners). **None is shared by three employers**, so S2.5's rule (an adapter only when three or more of these employers share a system) builds none. The consulting firms that are readable are the ones on the common systems (BCG on Phenom, EY on SuccessFactors, Sopra Steria and Wavestone on SmartRecruiters, Capgemini through its own JSON): the large networks and the strategy firms mostly use closed, script-loaded or protected sites.

## Not verified
Whether any of the `no_feed_found` employers would show a list to a real browser's own requests (the app does not simulate one); IBM's and Cognizant's job-list addresses (not named in what was read); that CGI's Njoyn and Eurogroup's Recruitment Platform have a usable public list.
