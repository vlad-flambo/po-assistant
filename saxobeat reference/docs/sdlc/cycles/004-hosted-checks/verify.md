# Verify: check the hosted app after the 28 October deploys

| | |
|---|---|
| **Cycle** | 004 |
| **Stage** | Verify: accepted by the owner 2026-10-29; next: Learn ([learn.md](learn.md)) |
| **Spec** | [spec.md](spec.md) |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Latest deploy live, built from `ff08c0c` or later, migrations up to `0040_email` | pass | Render lists `4fa860f` and `ff08c0c` (28 Oct); the log shows `0037_impersonation`, `0038_candidate_mode`, `0039_blocked_employers`, `0040_email` each `OK` ([evidence/deploy_log.txt](evidence/deploy_log.txt)). Today's push `d1718a0` (cycle 014's fixes, no migration) is the latest deploy: "Deployed Oct 29, 2026 at 3:53:05 PM GMT+1" |
| 2 | Migration 0039's blocks are ones the owner meant | pass | The owner checked the blocked employers in the app: "seems to work fine", nothing unblocked. The printed lines were not pasted ([evidence/blocks_0039.md](evidence/blocks_0039.md)). The interface itself → cycle 016 |
| 3 | Friends in Standard, owner in Power | pass | The owner, Console → Candidates, 2026-10-29: "yes" (no screenshot kept, so no e-mail address in the repo) |
| 4 | View as one friend: standard inbox, stops cleanly, listed | pass | The owner, 2026-10-29: "yes" |
| 5 | Candidate pages under 2 s, as the owner and as a friend | pass (judged, not measured) | The owner went through them: "seems good". No figure written down ([evidence/timings.md](evidence/timings.md)) |
| 6 | Console Today and Candidates under 2 s | pass (judged, not measured) | Same as 5 |
| 7 | Neon's restore history for prod1 recorded, with the date | pass | 2026-10-29, Neon → `saxobeat-prod1`: restore to any point in the **last 6 hours**, plus **manual snapshots**. See finding F2 |
| 8 | The newest backup file on the PC, with its date | pass | `saxobeat_2026-10-29_100546.dump`, 65.4 MB, 10:06: the old project's ([evidence/backup_on_pc.md](evidence/backup_on_pc.md)). The criterion says "weekly": since cycle 001's D3 the backup is monthly |
| 9 | The 2026-10-28 AI pack: export id, pack, results imported | pass | `E-20261028-104425` (runner, job screening, 5 tasks: 4 done, 1 other) and `E-20261028-123150` (command, onboarding, 1 task: done); eight packs since 23 Oct, 257 of 258 tasks done ([evidence/ai_exports.md](evidence/ai_exports.md)) |
| 10 | DEPLOY.md's "Not verified yet" replaced, with the date | pass | `docs/DEPLOY.md`, section "Verified on the host (2026-10-29)" |

## Findings
- **F1 (withdrawn). Today's push did deploy.** The owner first did not see `d1718a0` in Render's list and it was recorded as not deployed; on a second look it was there, deployed 2026-10-29 at 15:53. Cycle 014's fixes are live. Note for later: the local `main` carries cycle 015's unfinished feedback chat (migration 0041), so the next push ships it; that is the other session's call.
- **F2. prod1's safety net is short.** Neon restores the last 6 hours only, and no dump of prod1 exists (cycle 001 holds the backup back). A mistake noticed the next day could only be undone from the old project's 10:05 snapshot (losing everything since the move). A **manual snapshot** is made inside Neon, nothing is read out to the PC, so it should not count against the 5 GB transfer allowance (check prod1's figure afterwards); take one now, and again before any risky change (a migration, a bulk unblock), until the monthly backup runs.
- **F3. Speed is judged, not measured.** Good enough for this cycle (nobody complains, the owner saw no slow page). A figure is worth taking when cycle 005 tests real phones.

## Not verified
- The 28 October deploy's printed 0039 lines themselves (the owner checked the result in the app instead).
- Page times as numbers (F3).

## Verdict
- [x] Accepted by owner (2026-10-29)
- [ ] Sent back (what, to which stage)
