# Unsupported employers

The list itself is **[unsupported_employers.csv](unsupported_employers.csv)**: one row per employer with a status, the blocker, how to reach
their jobs anyway, and when it was checked. Edit the CSV, not this page. Supported employers are in
`jobs/management/commands/seed_employers.py`.

| Status | Meaning |
|---|---|
| `blocked` | The site refuses automated requests (HTTP 403) |
| `closed_system` | Hiring system with no public feed (Phenom, Avature, Taleo) |
| `needs_adapter` | A hiring system the app has no adapter for yet (HR Manager, JOIN), whose jobs are public |
| `needs_api_key` | Feed exists but needs a key we do not have (Homerun) |
| `no_feed_found` | The careers page shows no hiring system we can read |
| `not_probed` | Never checked, or checked only briefly: worth probing |
| `partial` | Only partly readable (see below) |

Reach any of them by pasting a job link into the inbox, or via alert emails once that import exists.

## Seeing coverage of your own employer list

`manage.py employer_coverage` reads your list of target employers (a CSV in `data/`) and writes `data/employer_coverage.csv` with a status per employer:

- `covered`: a source in the app already watches them
- `supportable`: their careers link is a board the app can read (`--add` creates the sources)
- `unsupported`: on the list above with a verified blocker
- `unknown`: hiring system not identified yet (a normal careers page). `--probe` looks for it on the public feeds of the common hiring systems and turns hits into `supportable`; what it finds on systems the app cannot read yet (SmartRecruiters, Recruitee) is noted in the detail column

## Welcome to the Jungle (investigated 2026-10-01)

- Its search index (Algolia) does exist, and the site publishes a search-only key, but that key only works for requests that claim to come from welcometothejungle.com. That is a deliberate restriction, so the app does not forge the header.
- Its job pages carry full structured data, but after a few dozen automated requests they answer every request with an empty HTTP 202 (bot protection). The app does not try to get round that.
- Its published sitemap (listed in robots.txt) is open: about 90,000 listings, each URL giving company, job title and city, with a last-modified date. The `welcometothejungle` source reads only that, filtered by your keywords, companies and cities. Jobs arrive **without a description**, so open the link to read them. It is created switched off by `seed_employers`.
- Adding a Welcome to the Jungle link by hand fails with an explanation, for the same reason.
- Update: job pages are reachable at a slow pace (the first ones answered normally after the earlier block lifted). The Jungle page reads them best-first within a daily limit and stops at the first challenge. See the README.
