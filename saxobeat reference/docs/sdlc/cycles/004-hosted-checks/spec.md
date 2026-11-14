# Spec: check the hosted app after the 28 October deploys

| | |
|---|---|
| **Cycle** | 004 |
| **Stage** | Spec approved 2026-10-29; next: Plan ([plan.md](plan.md)) |
| **Intent** | [intent.md](intent.md), approved 2026-10-29 |

## Behaviour when finished
Nothing in the app changes. What changes is what we know: each claim the PRDs and DEPLOY.md leave "not verified" about the hosted app is either backed by evidence in `verify.md` or turned into a fix.

## Acceptance criteria
Each one is checked in `verify.md` with its evidence (a screenshot, a pasted log line, a figure with its time).

**The 28 October deploys**
1. [ ] Render's latest deploy is live, built from `ff08c0c` or later, and its log shows migrations up to `0040_email` applied (owner pastes the lines).
2. [ ] Migration 0039's printed lines (what each line of the old blocked list now blocks) are read, and each caught employer is one the owner meant to block; any wrong catch is unblocked.
3. [ ] Console → Candidates shows every friend in Standard mode and the owner in Power mode.
4. [ ] Viewing as one friend shows a standard inbox (picks or "coming up", or best matches without AI) and stops cleanly; the session appears in the console's list.

**Speed** (second load, browser network panel, `jobs` page request only)
5. [ ] Inbox, job page, pipeline and settings: under 2 s each as the owner, and as a standard friend (view as).
6. [ ] Console Today and Candidates: under 2 s each.
A page over 2 s is recorded with its time and becomes a fix (in this cycle if small, else a new cycle).

**Recovery**
7. [ ] Neon's restore history length for `saxobeat-prod1` on the Free plan is read in its settings and recorded, with the date.
8. [ ] The last weekly backup file exists on the PC with its date (the runner makes it at most once a week). *(Changed after the cycle closed, by cycle 001's D3 on 2026-10-30: the runner now makes it at most once a month, `--min-age-hours 720`, and keeps the last 6. This cycle's check, the newest file and its date, is unchanged.)*

**AI with a real agent**
9. [ ] The console's Exports and Import history show the AI pack processed on 2026-10-28: export id, pack, number of results imported (a record, not a new run, per intent Q2).

**Docs**
10. [ ] DEPLOY.md's "Not verified yet" section is replaced by what this cycle verified, with the date.

## Design in brief
- The owner does the checks that need his accounts (Render's log, Neon's settings, his browser); Claude prepares the checklist, records the evidence and fixes what fails.
- Page timings are taken in the owner's browser, not by a script against the hosted app: a script would add load and reads, and the first load after Neon's 5-minute pause is not what we measure (the second is).
- Rejected: reading table counts on the hosted database (cycle 001's observation must stay clean, intent Q3).

## Interfaces and data
No code change unless a check fails. `docs/DEPLOY.md` (criterion 10). Evidence in `evidence/`.

## Constraints
- Reads from Neon only by page loads (kilobytes each): no table scans, no runner pass, no backup (cycle 001).
- Nothing from the fallback project is read (cycle 002).
- Screenshots must not show connection strings or keys.

## Out of scope
- Real-phone checks (cycle 005).
- Making e-mail live (cycle 003).

## Gate
- [x] Owner approved this spec (2026-10-29)
