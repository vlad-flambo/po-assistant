# Learn: Revolut People source

| | |
|---|---|
| **Cycle** | 020 |
| **Stage** | Learn |

## What happened vs what we expected
The success measure was a written decision with evidence, and, if "build", a `revolutpeople` source that reads Worklife's 4 postings on a local copy with fixture tests and the suite green.
- Decision and evidence: written (the link is a Revolut People career site; Revolut's own jobs are not behind it).
- Source: built, 16 tests, a live read on a scratch Postgres stored 4 jobs and then 0 new (5 requests per run), suite 1,434 pass. **Met.**
- What did not go to plan: I recommended parking it (importance 2); the owner chose to build. robots.txt of revolutpeople.com forbids the API, which I read only after the build; the owner then chose to override it for this tenant (decisions.md D1). The source is seeded off; the terms of use are unread; the hosted database was not touched.

## What we learned
- A `people-jobs.com/<tenant>/...` link is a frame around `revolutpeople.com/<tenant>/public/careers/...`; the tenant is an employer (Worklife), not Revolut. Its public JSON API (list plus one call per job) works without login; unknown tenants answer 403 "Invalid token", so tenants can only be found from links.
- Revolut's own jobs are on `revolut.com/careers`: a separate site, Cloudflare-challenged for plain HTTP, all positions in the page data when a real browser loads it. The bookmarklet is the only route (owner confirmed).
- `revolutpeople.com` and `people-jobs.com` robots.txt say `Disallow: /`, so the API is off limits under the project's rule; the owner overrode it per source (`"ignore_robots": true`).
- A source on the complete-listing list must not skip a job on a server error: the runner would close it as "no longer listed". The adapter raises on 5xx and skips only 404.
- Reach is tiny so far: 0 of 250 listed employers use the platform.
- I made about 35 requests to a site before reading its robots.txt. The spec for a new source must carry "robots.txt and terms read" as a criterion (cycle 013 had it as S2.1; this cycle did not).

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| Revolut People facts (tenant wrapper, open API, tenants unguessable, 0 of 250 employers) | project memory `project-sdlc-cycles` and `evidence/revolut_people_probe_2026-11-03.md` | [x] |
| Revolut's own jobs stay on the bookmarklet; the `unsupported_employers.csv` Revolut line (blocked, 403) is still accurate (the block is a Cloudflare challenge) | `docs/unsupported_employers.csv` (no change needed; shared file with cycle 013's uncommitted edits) | [x] |
| Read robots.txt and terms before the first request to any new site, and make it a spec criterion | project memory (new feedback `feedback-robots-first`) | [x] |
| The same rule as a line in the SDLC skill's safety rules (`.claude/skills/ai-sdlc/SKILL.md`) | the playbook | [ ] deferred: owner to say yes (not edited unasked), 2026-11-03 |
| Per-source robots override `ignore_robots`, with the owner's decision | `decisions.md` D1, adapter docstring and help text, seed comment | [x] |
| Complete-listing sources raise on 5xx instead of skipping a job | the adapter's comment and `test_a_failing_server_stops_the_run_instead_of_hiding_a_job` | [x] |
| Worklife on the hosted database: terms read and link checked (owner, 2026-11-03); `seed_hosted_sources.ps1 -Step 3` added and pushed; the hosted write (Neon snapshot, dry run, apply) and enabling | cycle `next.md` | [x] hosted write run by the owner on 2026-11-04 ("seems to work", owner's word); enabling and the first pass: see `next.md` |
| The stale statement in `docs/PRD.md` ("Revolut ... block requests") now has its reason | cycle 006 (stale docs) | [ ] deferred 2026-11-03: minor, for cycle 006 |

## Process feedback
- The two approval gates worked: Q1, spec and plan were approved in two short answers, and the one surprise (robots.txt) was caught before anything was enabled.
- What would have caught it earlier: a "robots.txt and terms" row in the spec template for any cycle that reads a new site.
- The README table and `seed_employers.py` are edited by two sessions; staging only my hunks through the index (`git hash-object` and `update-index --cacheinfo`) kept the commit clean.
- Counting requests: print the counter to a file; the first live read's counter output was lost in a traceback.

## Next cycle candidates
- A radar probe for `revolutpeople` in `probe.py`, and a tenant search, if a second tenant appears (importance 1-2).
- Parsing a salary from the title ("78k€ à 87k€"), if more tenants use that habit (importance 1).
- The skill rule above, and the spec-template row, as a small playbook change.
