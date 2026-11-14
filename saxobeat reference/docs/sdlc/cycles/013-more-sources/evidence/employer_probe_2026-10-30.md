# Probe of three employer career sites (2026-10-30)

Read-only: one GET of the job link the owner gave, `/robots.txt`, and the sitemap or feed where one was named. Nothing was stored in the app.

| Employer | Link given | What it is | Existing adapter that could read it | Robots (read 2026-10-30) |
|---|---|---|---|---|
| Accenture | accenture.com/fr-fr/careers/jobdetails?id=R00345449_fr-fr | Own site. The job page carries a schema.org `JobPosting`. `https://www.accenture.com/fr-fr/jobpostings-sitemap.xml` answers 200 and lists 173 job pages (`/fr-fr/careers/jobdetails?id=R…_fr-fr`) | `sitemapjobs` (with `job_pattern` for `jobdetails`); to be tried | `*/careers/jobsearch?` is disallowed (the search page); the sitemap and job pages are not |
| Capgemini | capgemini.com/fr-fr/jobs/207491-fr_FR+sap_btp/ | WordPress site with a `cg-jobs` plugin; the job page has no `JobPosting` (only `Article`); no job sitemap among the fr-fr sitemaps (job-sitemap and jobs-sitemap answer 404); the list is drawn by a script | none found | nothing disallowing /jobs seen in the lines read; full terms not read |
| Saegus | careers.saegus.com/jobs/3761896-… | Teamtailor on its own domain. `https://careers.saegus.com/jobs.rss` answers 200 with 16 jobs; job page has a `JobPosting` | `teamtailor` with `host: careers.saegus.com` | `/jobs/internal/` disallowed; sitemap listed |

Not verified: each site's terms of use; whether Accenture's sitemap lists only current jobs; Capgemini's hiring system behind the script (a Workday or API call may exist: not looked for).
