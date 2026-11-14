# The one-week reading (criteria 13 and S2.9), 2026-11-10

Read-only query on the hosted database on 2026-11-10 (aggregate counts; no write; script kept as `weekly_reading.py` in this session's scratchpad, not in the repo). Window: jobs first seen on or after 2026-11-03 00:00 UTC (the first full run with the cycle's sources on was 2026-11-03). "In the owner's cities" = the app's own city test for Paris and Ile-de-France, as in the earlier measurements. A job counts as "from a cycle-013 source" when one of its stored links comes from one of 21 sources (Amundi is older than the cycle: its source existed before, and it brought 0 here).

## The numbers
| | All places | Paris / Ile-de-France |
|---|---|---|
| New jobs in the whole catalogue since 2026-11-03 | 4,315 | **2,016** |
| of which only from a cycle-013 source | 1,576 | 1,046 |
| of which also found by an older source | 6 | 6 |
| of which from other sources only | 2,733 | 964 |
| **Share from the cycle's sources** | 36.7 % | **52.2 %** (1,052 of 2,016) |
| **Consulting sources** (Saegus, Accenture, Capgemini, BCG, EY, Onepoint, PwC, PwC Campus), any link | 1,083 | **967** (48.0 % of 2,016) |

By group, new jobs in Paris / Ile-de-France: step 1 own career sites 574, step 2 consulting 425, fintech batch (2026-11-04) 33, Doctolib and Papernest 20.

## By source, new jobs in Paris / Ile-de-France
Capgemini 400, EY 162, Accenture 126, PwC 117, Onepoint 65, PwC Campus 46, BCG 36, Qonto (Ashby) 24, Saegus 16, Murex 16, Doctolib 10, Papernest 10, Payhawk 7, Finastra 5, Epsor 5, Marble 4, Checkout.com 4.
**Brought none in Paris / Ile-de-France: Backbase, Fenergo, SWIFT, Kaiko, Amundi** (expected for the first four: their jobs are elsewhere; Amundi's list is old and unchanged).

## What this does and does not say
- The first week includes the **one-off backlog**: each new source's whole current list counts as "new" on its first pass (Capgemini 400 of them). A steady week will be much smaller; the next reading (2026-11-17) is the first steady one and should be compared.
- "In the owner's cities" is Paris and Ile-de-France as a proxy for the candidates' cities; the per-candidate view (the jobs a given account would actually see after its filters and scoring) was not measured.
- The shared city test can read some US ZIP codes as Paris (found with EY, fixed there by a place-word option); other worldwide sources in this list (Accenture, PwC) may carry a few such false matches: not checked.
- 6 jobs were also found by an older source, so almost all of the cycle's jobs are new to the catalogue and not duplicates of aggregator jobs (duplicates across sources are merged by the app's own matching, not measured here).
