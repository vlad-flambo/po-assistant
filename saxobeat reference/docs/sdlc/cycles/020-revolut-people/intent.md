# Intent: Revolut People career sites as a source

| | |
|---|---|
| **Cycle** | 020 |
| **Stage** | Intent |
| **Date** | 2026-11-03 |
| **Owner** | Vladimir |
| **Importance** | 2/5 (claude, 2026-11-03): one employer found (Worklife, 4 postings), 0 of 250 listed employers use it, no customer list found; but the API is open and the adapter is small |

## The request, in your words
> I stumbled on this job https://skaleet.slack.com/archives/D09SWTGA0B0/p1793702947842049 [a people-jobs.com link] from the url, I get the suspicion that the website uses Revolut People. Can you check that ? If it is the case, can you investigate if its worth building that connector ? if so, will it allow me to access revolut job listings ?

## Why now / the pain
A Head of Product job in Paris (Worklife, 78-87k€) reached you through a LinkedIn post, on a career site Saxobeat cannot read today. Nothing hurts yet beyond that one case.

## Goal
Decide whether Saxobeat should read career sites built on Revolut People, and say plainly whether that would give access to Revolut's own jobs.

## Success measure
The decision is written with its evidence (done below); if the answer is "build", a source of type `revolutpeople` reads Worklife's 4 postings into Saxobeat on a local copy, with fixture tests and the suite still green.

## Not doing (this cycle)
- Reading Revolut's own careers site by machine (blocked by Cloudflare; the Send to Saxobeat bookmarklet route stays).
- Guessing tenant slugs for hundreds of employers.
- Any write to the hosted database.

## What we already know (facts, with where they came from)
All in [evidence/revolut_people_probe_2026-11-03.md](evidence/revolut_people_probe_2026-11-03.md) (about 25 requests, claude, 2026-11-03):
- **Yes, it is Revolut People.** `people-jobs.com/<tenant>/...` is an iframe wrapper around `revolutpeople.com/<tenant>/public/careers/...`; the form says "Powered by Revolut People". The tenant here is `worklife`: the employer is **Worklife** (Paris), a customer of the product, not Revolut.
- **The API is open.** `GET https://revolutpeople.com/api/<tenant>/external/v2/postings` (list) and `.../postings/<id>` (detail with HTML description and creation date) answer plain `curl` with JSON, no login. Worklife has 4 postings. Salary is only in the title text. An unknown tenant answers 403 "Invalid token".
- **It will not give Revolut's own jobs.** The `revolut` tenant answers 403 like a made-up one. `revolut.com/careers` is a separate site; its 291 positions (7 in Paris) are readable only in a real browser, and plain HTTP gets a Cloudflare challenge (already in `docs/unsupported_employers.csv`). Revolut's Paris jobs of today are listed in the evidence file.
- **Reach is small or unknown.** 0 of the 250 employers in `data/employer_careers.csv` use it; the product targets small and medium businesses in Europe and the UK; no customer list found.
- **Cost is small.** `jobs/sources/recruitee.py` is the model: one JSON list, one detail call per job, about 60 lines, a fixture test, a registration line.
- **robots.txt forbids it** (read after the build): `revolutpeople.com` and `people-jobs.com` say `Disallow: /` with only `/public/careers`, terms and privacy allowed, so the API is off limits under the project's rule; the adapter now refuses (verify.md). This overturns the "open API, cheap, buildable" reading above.
- Not verified: the platform's terms of use, rate limits, any tenant other than `worklife`.

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Build the `revolutpeople` source now, or park it? | **Park the adapter**, but add Worklife to your radar by hand today; build it when a second tenant shows up (an alert, a LinkedIn link). Reason: one employer with 4 jobs does not pay for a cycle yet. If Worklife matters to you, say so and I build it (one session, off by default like the other sources) | "Build it" (owner, 2026-11-03, against my recommendation) | answered |
| Q2 | Revolut's own jobs: stay on the bookmarklet route? | Yes. Revolut Paris has 7 openings today; the bookmarklet reads them in your browser. No machine route exists | "Yes, the bookmarklet stays" (owner, 2026-11-03) | answered |

Status: `open`, `answered`, `parked`.

## Constraints and risks
- Terms of use of revolutpeople.com not read; read them before enabling a source (as done for the other employers in cycle 013).
- The API is an undocumented front-end API (`external/v2`); it can change without notice. The same is true of the other sources we use (Capgemini, Phenom).

## Gate
- [x] All open questions answered or parked (Q1 and Q2 answered 2026-11-03)
- [x] Goal and success measure confirmed by the owner (2026-11-03, "Confirm")
