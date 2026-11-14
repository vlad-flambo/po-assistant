# Plan: check the hosted app after the 28 October deploys

| | |
|---|---|
| **Cycle** | 004 |
| **Stage** | Plan approved 2026-10-29; Build in progress |
| **Spec** | [spec.md](spec.md), approved 2026-10-29 |

## Slices
Most slices are the owner's, because they need his accounts or his browser. For each, the owner pastes the result in the chat (text or a screenshot with no secret in it); Claude records it in `evidence/` and in `verify.md`. Nothing here writes to the hosted database except slice 2's possible unblocking, which the owner does himself in the app.

| # | Who | Slice | Where | Evidence | Criteria | Status |
|---|-----|-------|-------|----------|----------|--------|
| 1 | owner | Render → the service → *Events*: the latest deploy is live and built from `ff08c0c` or later; open its log and copy the lines from `Running migrations` to the end of the migrations | Render dashboard | the pasted lines, in `evidence/deploy_log.txt` | 1 | done |
| 2 | owner, then claude | From the same log, copy the lines migration 0039 printed (`candidate N: '<line>' now blocks …`). Claude lists every caught employer; the owner says which he did **not** mean to block, and unblocks those in Settings → Blocked employers (his own) or via View as (a friend's) | Render log; the app | the lines and the owner's verdict per employer, in `evidence/blocks_0039.md` | 2 | done |
| 3 | owner | Console → Candidates: a screenshot of the Mode column | the app | screenshot, `evidence/modes.png` | 3 | done |
| 4 | owner | View as one friend: their inbox (a screenshot), then Stop; the session is listed under "Viewing as" | the app | two screenshots | 4 | done |
| 5 | owner | Page timings: for each page, load it, wait, load it again; in the browser's network panel read the time of the page's own request (not images or scripts). As himself: inbox, job page, pipeline, settings, console Today, console Candidates. Viewing as a friend: inbox, job page, pipeline, settings | the app, browser dev tools (F12 → Network) | the table in `evidence/timings.md` (Claude prepares it with empty cells) | 5, 6 | done |
| 6 | claude | A page over 2 s: find why (queries, sizes) on a local copy, never on the hosted database; fix it in this cycle if small (one commit, test), else open a cycle | local | the finding and the fix or the new cycle's number | 5, 6 | not needed |
| 7 | owner | Neon → `saxobeat-prod1` → Settings → restore / history retention: read the window and the plan's limit, with the date | Neon console | the figure, in `verify.md` | 7 | done |
| 8 | claude | The newest file in `data/backups/` on this PC: its name, date and size | this PC | the listing, in `verify.md` | 8 | done |
| 9 | owner | Console → AI → Exports and Import: a screenshot of the 2026-10-28 export and its import (export id, pack, results imported) | the app | screenshot | 9 | done |
| 10 | claude | Rewrite DEPLOY.md's "Not verified yet" with what this cycle verified and the date | `docs/DEPLOY.md` | the diff | 10 | done |

## Order and dependencies
Slices 1-2 first: they are about data that may be wrong today (a block that hides good jobs). 3-4 next (two minutes). 5 any time (a quiet moment gives cleaner timings); 6 only if 5 finds a slow page. 7-9 any time. 10 last, from the evidence.

## Rollback
Nothing to roll back except slice 2's unblocks (a block can be set again from the job or company page) and slice 6's fix (one commit, `git revert`).

## Risks
- Timings vary (Neon waking, network): the second load is the measure; a page near 2 s is measured three times and the median recorded.
- Screenshots of the console show friends' e-mail addresses: they stay in `evidence/` only if the owner agrees, otherwise they are cropped or described in words.

## Gate
- [x] Owner approved the slices (2026-10-29)

## As run
- 2026-10-29 slice 8 (Claude): newest file in `data/backups/` is `saxobeat_2026-10-29_100546.dump` (65.4 MB, 10:06), the old project's dump used for the move (`evidence/backup_on_pc.md`). **Finding:** no dump of `saxobeat-prod1` exists yet, because the runner's backup step is held back during cycle 001's measurements; until then prod1's only recovery is Neon's own restore history (slice 7) plus the 10:06 dump of the old project.
- 2026-10-29 slice 5 prepared: the table to fill is `evidence/timings.md`.
- 2026-10-29 the owner's checks (slices 1-5, 7, 9): migrations 0037-0040 OK on the 28 October deploy, and today's push `d1718a0` deployed at 15:53 (first missed in the list, so finding F1 was raised and then withdrawn); blocks fine, the blocking interface to redo (cycle 016); modes and View as fine; pages judged fast, not timed; Neon restores 6 hours plus manual snapshots; two packs on 28 October. Slice 6 not needed. Slice 10 done: DEPLOY.md's section is now "Verified on the host (2026-10-29)". All in `verify.md`.
