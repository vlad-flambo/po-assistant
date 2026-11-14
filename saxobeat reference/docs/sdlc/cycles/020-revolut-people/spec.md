# Spec: Revolut People source (`revolutpeople`)

| | |
|---|---|
| **Cycle** | 020 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |

## Behaviour when finished
A source of type `revolutpeople`, configured with a tenant name, reads that employer's public job list from Revolut People and stores each posting with its full text, like the Recruitee or Teamtailor sources. Worklife (tenant `worklife`, 4 jobs on 2026-11-03) is seeded as the first one, **switched off** (new sources go in disabled; the owner enables them). Pasting a `people-jobs.com/<tenant>/...` or `revolutpeople.com/<tenant>/...` link into the app's "add an employer" flow proposes this source. Revolut's own jobs are not covered and stay on the bookmarklet route.

## Acceptance criteria
Each one must be checkable in `verify.md`.
1. [ ] The adapter is registered as `revolutpeople`, named "Revolut People" where platform names are shown (`platforms.py`), with a help line saying what the config is.
2. [ ] From the recorded Worklife answers (list of 4, detail of each), `fetch()` returns one posting per job with: external id (the posting UUID), title, company ("Worklife" from config, else the tenant), the HTML description and its plain text, `posted_at` from `creation_date_time`, apply method `ats`.
3. [ ] The posting's link is `https://people-jobs.com/<tenant>/apply/<id>` (the public address LinkedIn uses), also used as apply link. Whether it opens in the owner's browser is checked by the owner (decision D1).
4. [ ] Location: real places only ("Paris"); the pseudo-places "Hybrid" and "Remote" give `hybrid` / `remote` in `remote_type` and are left out of the location text; country from the location's country; a posting with no location stores none.
5. [ ] Salary is not guessed: structured salary fields stay empty (the figure is only in the title text, which is kept as is).
6. [ ] A posting whose detail call fails (HTTP 404/5xx) is skipped and the others are still returned; a list call that fails raises, so the runner shows the source as in error (not as empty).
7. [ ] A tenant that does not exist (HTTP 403 `Invalid token`) raises a clear error naming the tenant, not "0 jobs".
8. [ ] `revolutpeople` is in the runner's complete-listing types, so a job removed from the public list is marked closed on the next run, as for Recruitee; a test shows a second run with 3 of 4 jobs closes the fourth.
9. [ ] Link recognition: `people-jobs.com/worklife/apply/<id>`, `people-jobs.com/worklife`, `revolutpeople.com/worklife/public/careers/...` all give `("revolutpeople", {"tenant": "worklife"})`; `www.revolutpeople.com` and a bare `people-jobs.com` give none.
10. [ ] The how-to text for the type exists (`howto.py`), saying where the tenant name is in the link.
11. [ ] Worklife is in `seed_employers.py` with `enabled False`; the dry run on a scratch copy lists it as to be created, a second run adds 0.
12. [ ] A live read on a scratch copy (not hosted) stores Worklife's 4 jobs once each over two runs (no duplicates); request count stated before running: 1 list + 4 details = 5 per run.
13. [ ] The full test suite passes (no new failures; the known order-dependent `test_auto_reject` failure noted in memory is not mine).
14. [ ] Nothing is written to the hosted database in this cycle; the seed on the host is a separate owner step, listed in `next.md`.

## Design in brief
- Two calls, both `GET`, JSON: `https://revolutpeople.com/api/<tenant>/external/v2/postings` (list) and `.../postings/<id>` (detail: HTML description, `creation_date_time`, `type`). Same shape as `recruitee.py`: `get_json` from `jobs/sources/http.py` with the honest user agent (checked: it answers 200).
- One detail call per job (the list has no text). A short pause between them (as `smartrecruiters.py` does). The list carries no change date, so every run re-reads every detail; the cost is small (4 jobs) and the help line says "one request per job".
- Rejected: reading the HTML pages (Cloudflare challenge, no need); guessing tenants for other employers (hundreds of requests for few hits); parsing salary from titles ("78k€ à 87k€", "55k à 60k€ fixe + variable (4k€)": too many shapes, and a wrong number is worse than none); a probe for `revolutpeople` in the radar (`probe.py`, left for when a second tenant exists).

## Interfaces and data
- New: `jobs/sources/revolutpeople.py`; `tests/test_revolutpeople_source.py`; `tests/fixtures/revolutpeople_worklife_list.json` and `..._detail.json` (the real answers of 2026-11-03: public job ads, no personal data).
- Changed: `jobs/sources/__init__.py` (import), `jobs/platforms.py`, `jobs/employers.py` (link recognition), `jobs/sources/howto.py`, `jobs/services/runner.py` (`COMPLETE_LISTING_TYPES`), `jobs/management/commands/seed_employers.py`.
- No migration, no setting, no new dependency.

## Constraints
- Terms of use of revolutpeople.com are **not read** (the site's pages are behind a challenge for plain HTTP, so my fetch tool cannot read them): the owner reads them in a browser before enabling the source (as for Finastra in cycle 013). The source stays off until then.
- The API is undocumented and may change; a change shows as an error on the Sources page, not silently as 0 jobs (criteria 6 and 7).
- Requests: five per run for Worklife; no pause needed between runs.

## Out of scope
- Revolut's own jobs (`revolut.com/careers`); the bookmarklet route stays.
- Salary extraction, other tenants, the radar probe, an alert when a tenant appears.
- Enabling the source or seeding the hosted database.

## Gate
- [x] Owner approved this spec (2026-11-03, "Approve both")
