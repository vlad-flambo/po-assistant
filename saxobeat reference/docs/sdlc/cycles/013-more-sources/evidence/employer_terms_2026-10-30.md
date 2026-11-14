# Terms of use of three employers' sites, read 2026-10-30

Read by fetching each page and asking whether it addresses automated access or reuse (summaries by a small model, not legal advice; the clauses quoted are as returned). The standing rule (PRD.md §3 and §13): respect robots.txt and API terms; no scraping of a site whose terms or bot protection forbid it.

| Employer | Page read | Automated access | Reuse of content | Robots.txt (2026-10-30) |
|---|---|---|---|---|
| Accenture | accenture.com/us-en/support/terms-of-use | Not addressed | Copying, republishing, distribution forbidden without written consent; use "solely for your personal, non-commercial use". Job postings not mentioned | Search page (`*/careers/jobsearch?`) disallowed; sitemap and job pages are not |
| Capgemini | capgemini.com/fr-fr/conditions-generales-dutilisation/ (Section 6) | Not addressed | Use without written permission forbidden; copying, downloading, printing for personal, non-commercial purposes allowed. Job postings not mentioned | Nothing disallowing jobs seen; no usable feed found anyway (see the probe) |
| Saegus | saegus.com/mentions-legales (company site; its careers site is Teamtailor) | Not addressed | Reproduction or distribution without prior written permission forbidden (Art. 4-style clause) | `/jobs/internal/` disallowed; `jobs.rss` and sitemap open |

## Reading
- None of the three forbids automated reading; none mentions robots or job postings. Under the standing rule all three pass.
- All three restrict **reproduction without written consent**. Saxobeat shows each job's title, link and a description to the candidate, like every existing source, so the posture is the same as for the sources already live; the PRD defers the product-level legal review (PRD.md §2). This is a flag for that review, not a block.
- Saegus: `jobs.rss` is a feed the hiring system publishes for syndication (to be verified in Teamtailor's documentation); it is the lightest way to read them.
- Accenture: read only the job sitemap and job pages, never `careerssearch`/`jobsearch`.

Not verified: the careers-site terms of Saegus on Teamtailor itself; any separate Accenture or Capgemini careers-site terms (the pages read are the general terms); whether Capgemini has a feed (a separate question, Q4).
