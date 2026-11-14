# Intent: stop analysing postings older than 30 days

| | |
|---|---|
| **Cycle** | 031 |
| **Stage** | Intent |
| **Date** | 2026-11-06 |
| **Owner** | Vlad |
| **Importance** | 3/5 (claude, 2026-11-06): reach: every candidate's inbox; pain: postings 30 to 60 days old are still scored and shown, which the owner does not want; nothing breaks; no feedback count yet |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
> also, don't analyse jobs listing that are over 30 days old. I believe cutoff is currently 2 months.

## Why now / the pain
- The owner wants postings older than 30 days left out; today they stay in the inbox for 60 days (confirmed below), so a month of stale postings is scored and shown.

## Goal
A posting older than 30 days is not analysed (not scored, not sent to the AI) and does not sit in the inbox. Its age is the posting date when it has one, and otherwise the day it was imported into the database (the job's own `first_seen_at`, a best-guess proxy for the listing date: owner, 2026-11-06). Thirty days is the new default; a power user can still change it.

## Success measure
(Proposed; to be confirmed by the owner.)
1. A new candidate's age limit is 30 days (today 60), and a posting dated 31 days ago is hidden with the reason "older than 30 days" while one dated 29 days ago is kept (drill on a local copy). A power user who types another value keeps it.
2. **Undated postings:** a posting with no posting date imported 31 days ago is hidden for age, one imported 29 days ago is kept, and a dated posting still uses its own date, not its import date. This holds in the filter run on arrival, in the refilter, and in the nightly age-out (all three, since each has its own age code, `filters.py:69` and `matching.py:219-228`).
3. No scoring or AI task is created for a job past the limit (check on a local copy: the count of scored views older than 30 days, dated or not, is 0 after one pass).
4. Nothing already acted on (shortlisted, applied, interviewing) is hidden by the change; "keep visible" jobs stay (the existing rule, `jobs/services/matching.py:227`).
5. The size of the one-off effect is known before it ships: on a local copy of the 29 Oct dump, how many visible undated postings older than 30 days and how many dated 30-to-60-day ones would be hidden (read-only count, in `evidence/`).
6. No data is changed on the hosted database; no existing candidate's stored limit is touched (owner did that by hand).

## Not doing (this cycle)
- Changing how a score is computed.
- Changing existing candidates' stored limits (the owner moved them by hand, 2026-11-06).
- Anything on the hosted database before the owner approves a plan.

## What we already know (facts, with where they came from)
- The cutoff is the per-candidate hard filter `max_age_days`, default **60 days** (`jobs/models.py:16`), editable in power mode (`settings.html:68`). The owner's belief ("2 months") is correct, read 2026-11-06.
- It is applied last among the filter rules, against the posting date only when there is one (`jobs/services/filters.py:65-71`), and again by a nightly `age_out` (`jobs/services/matching.py:219-228`). Hidden jobs are not scored: scoring takes views with an empty hidden reason (`matching.py:238`).
- The AI analysis already looks only at jobs first seen in the last 14 days (`freshness_days`, `jobs/models.py:820`, `jobs/ai/selection.py:32`), so it is not what keeps a 30 to 60 day old posting alive.
- Employer-board sources are already seeded with 30 days (`seed_employers.py:43`; WTTJ source default 30, `sources/welcometothejungle.py:69`).
- A new default only reaches new candidates: existing ones have 60 stored in their config (the owner says they moved them to 30 by hand, 2026-11-06; to verify with a count). Tests pin 60 in places (`tests/test_stale.py:30,35`; `tests/test_i18n.py:120` is about reading old text, not the default).
- Undated postings: the age rule needs `job.posted_at` (`filters.py:69`, test `tests/test_core.py:93` pins "no posting date: nothing to judge") and `age_out` filters on `job__posted_at__lt` only, so an undated posting is never hidden for age today. `Job.first_seen_at` (default: now, `jobs/models.py:258`) is the import date; **Correction (2026-11-06, found while building):** I had written that `CandidateJob` has its own `first_seen_at` (the date the view was made); that line (`models.py:420`) belongs to `JobSource`. `CandidateJob` has only `created_at`, and `view.first_seen_at` reads the job's own date through the view's `__getattr__`, so Q4's worry about a backfilled view looking young does not arise; the answer (the job's `first_seen_at`) stands. The refilter loads only `FILTER_FIELDS`, which has `job__posted_at` and not the import date (`matching.py:198-199`).

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | Is 30 days the new default that a power user can still change, or a fixed limit for everyone? | The new default (30); power users keep their box | **New default** (owner, 2026-11-06) | answered |
| 2 | Existing candidates who still have 60: move them to 30 (a one-off data change, on the hosted database only inside an approved plan), or only new candidates? | Move those at exactly 60 to 30; leave anyone with another value | **No: "i did it manually"** (owner, 2026-11-06). So no data change in this cycle; the code only changes the default for new candidates. To be verified by a read-only count of stored `max_age_days` values, locally first | answered |
| 3 | A posting with no posting date: leave as is (never aged out), or age it from the day we first saw it? | Leave as is for this cycle | **Use the date it was imported into the database as its date, and age it out on that** (owner, 2026-11-06). In scope now | answered |
| 4 | "Imported into the database" is the job's own `first_seen_at` (when any candidate's source first brought it), not the candidate's own view date (a view made later by a backfill would look young). Right? | Yes, the job's `first_seen_at` | **Yes, the job's `first_seen_at`; the goal is a best-guess proxy for the listing date** (owner, 2026-11-06) | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Moving existing candidates is a write to the hosted database: rehearse on a local copy, then only inside an approved plan, with a count before and after.
- A shorter limit hides jobs in the inbox for everyone at once; the "Filtered & archive" page keeps them with the reason, and raising the limit brings them back after a refilter.

## Gate
- [x] All open questions answered or parked
- [x] Goal and success measure confirmed by the owner (2026-11-06)
