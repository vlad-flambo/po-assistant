# What each page of the app reads from the database (scratch estimate, 2026-10-30)

`scripts/step_pages.py` through `measure_reads.ps1`: a signed-in test client on a scratch copy of the 29 Oct dump (migrated to the current schema), one request per page, bytes counted by statement (an estimate, about 5 % under the container's real figure). The scratch copy is a day older than prod1 and has more pending AI tasks, so absolute numbers on prod1 will differ; the ranking should not.

| Page or action | Bytes read, before | After the fix |
|---|---:|---:|
| Operator: **Insights** (`/insights/`) | **37.3 MB** | **5.3 MB (-86 %)** |
| Operator: console **AI export** (`/ops/ai/export/`, 17 s) | **30.7 MB** | not changed |
| The calculation behind the console's **AI import preview** (calibration effect and backtest) | **13.5 MB** each time | not changed (it needs the texts to score again) |
| Operator: Pipeline | 0.53 MB | |
| Standard user: Insights | 0.70 MB | |
| Everything else (inbox, archive, companies, settings, CV, every other console page) | under 0.11 MB each | |

- **The Insights fix** (`jobs/services/insights.py`): the page loaded every kept and dismissed job with its full text to read titles and scores. It now defers the text; a test fails on the old code. 1,320 tests pass.
- **The AI export page** builds a preview of every file on every view (and refreshes the queue): its cost grows with the number of due tasks. On prod1 right now fewer are due than on the scratch copy, so its real cost is lower; not changed here.
- **The import preview** must score the candidate's visible jobs again with the proposed weights: the texts are needed. A cache of the result would save repeats; not built.
- **Why it matters for the cycle:** these are the web app's reads (`W`). They are paid by whoever opens the page, so a few views by the owner in a day can cost hundreds of MB, which would explain both today's 0.31 GB and part of October's unexplained 1.5 GB.
