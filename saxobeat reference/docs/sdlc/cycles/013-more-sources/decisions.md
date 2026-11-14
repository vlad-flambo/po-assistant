# Decisions: employers' own career sites (cycle 013)

One entry per decision, newest last. Do not edit old entries: add a new one that supersedes.

## D1. Accept the Neon cost of the ten new sources; Backbase, Fenergo and SWIFT stay switched off
- **Date:** 2026-10-30 (owner, in the session: "Accept, 3 stay off")
- **Context:** Slice 11 ran the ten new sources on a local copy: 111 site requests, +0.63 MB of Neon reads per pass for all ten, +8.6 MB once for the first pass, +794 jobs of which about 496 are in Paris / Ile-de-France. Backbase, Fenergo and SWIFT brought 0 jobs in the owner's cities and 83 jobs in all ([evidence](evidence/new_sources_measurement_2026-10-30.md)).
- **Options considered:** accept and enable all ten; accept and keep the three useless ones off; leave all off until later.
- **Decision:** accept the figure; the seven others (Saegus, Capgemini, Accenture, Checkout.com, Payhawk, Finastra, Murex) may be enabled, in batches after a by-hand run; **Backbase, Fenergo and SWIFT stay switched off**.
- **Why:** the three cost storage and reads for no job the owner can use; the cost of the other seven is about 1 % of a pass.
- **Consequences:** the three are still created (switched off) by the seed, so they can be turned on later if the owner's cities change; Finastra stays off until its terms of use have been read in a browser (slice 9). The slice 12 steps are the owner's.

## D2. Enable all the remaining new sources, whatever their open terms questions (supersedes D1's "three stay off")
- **Date:** 2026-11-03 (owner, in the session: "Yes, all of them", answering whether "the other sources" included Onepoint, PwC and Finastra, after being told what was open for each)
- **Context:** after the first two by-hand passes (Capgemini, batch 1, BCG and EY on), seven new sources were still off: Onepoint (its site terms forbid "extraction" of the Site's content without authorization; bots not mentioned; the jobs are on a Workday-hosted site), PwC and PwC Campus (the legal notice was unreadable by the tool), Finastra, SWIFT and Fenergo (terms unread), Backbase, and, with SWIFT and Fenergo, no job in the owner's cities (D1).
- **Options considered:** keep each off until its terms are read or decided (my recommendation); enable only those with a value for the owner's cities; enable all.
- **Decision:** enable all seven.
- **Why:** the owner's call on a personal tool that reads public job pages; the cost is small (see the evidence); the sources can be switched off by name at any time.
- **Consequences:** the terms of Onepoint (the "extraction" clause), PwC, Finastra, SWIFT and Fenergo were **not** all read or resolved: the decision is the owner's, recorded here, and a point for the product-level review of sources (PRD.md §2). Backbase, Fenergo and SWIFT will store jobs that are outside the owner's cities (about 83 jobs, measured in step 1). All 15 new sources are now on.
