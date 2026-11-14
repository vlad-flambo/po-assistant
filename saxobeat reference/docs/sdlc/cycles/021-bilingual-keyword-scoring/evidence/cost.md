# Slice 9: what the glossary costs (criterion 16), 2026-11-04

Method: `cost.py` (this folder), run alone on the scratch copy `replay021` (local Docker Postgres, the 29 Oct dump), candidate C-01, a fixed random sample of 1,000 scored postings (221 employers, 6.1 MB of text, loaded before timing). Raw output: `cost_output.txt`. This PC is shared with other work, so the absolute times move from one run to the next (the same scoring took 8.8 s, then 9.4 s with the glossary off); the ratios are what counts.

| | Glossary off | Glossary on | Ratio |
|---|---|---|---|
| Scoring 1,000 postings in memory (best of 3) | 9.36 s | 11.62 s | **1.24** (limit 1.5) |
| Employer-boilerplate counts, cold cache, 221 employers | 57.8 s | 127.8 s | 2.21 |
| Statements for those counts | 2 (1 counting query) | 2 (1 counting query) | same |
| Terms counted | 56 | 218 | 3.9 |
| Text model build (word counts already read) | 0.01 s | 0.07 s | - |

- **Scoring:** within the limit. A first run gave 1.50 (limit 1.5, not met); the lookups were then made cheap (the keyword's concept and its equivalents are looked up already normalized and kept by `lru_cache`), which gave 1.24.
- **Still one counting query** per chunk of employers, as the criterion asks, but it counts 218 terms instead of 56, so the database does about 2.2 times the work for it. It is read by `company_boilerplate` and kept for 6 hours per employer (`CACHE_TTL`), so a runner pass pays it once per employer per 6 hours, not once per posting. On Neon that is compute time on the database, not data sent. **Not measured on Neon** (nothing was read from it); to be looked at when the owner runs the rescore (slice 11).
- **No new read of job texts** for the glossary. The rescore reads the texts it always read (what `matching.rescore` reads); `manage.py rescore_preview` states the volume per candidate.
- A possible later saving if the counting turns out to matter on the host: count only the equivalents that occur at all in the postings, or only for the keywords of weight 3 or more. Not done: it is not needed to meet the criterion.
