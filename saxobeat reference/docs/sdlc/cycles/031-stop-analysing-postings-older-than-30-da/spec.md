# Spec: stop analysing postings older than 30 days

| | |
|---|---|
| **Cycle** | 031 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |

## Behaviour when finished
- A posting's **age** is its posting date when the source gives one, and otherwise the day it was imported into the database (the job's own `first_seen_at`, a best-guess proxy for the listing date). Dated postings keep using their own date.
- **The limit is 30 days by default** for every new candidate (it was 60). A power user can still type another number in "Hide postings older than (days)", or clear it for no limit. Existing candidates keep what is stored (the owner moved them to 30 by hand; nothing in this cycle writes to stored settings).
- A posting older than the limit is **hidden for age** ("older than 30 days") wherever the age rule runs: when a job arrives, in a refilter after any settings change, and in the nightly age-out of jobs that grew old. Hidden jobs are **not scored and not sent to the AI** (scoring only takes visible jobs, `jobs/services/matching.py:238`), so a job past the limit costs no analysis.
- What is not touched: jobs the candidate has acted on (shortlisted, applied, interviewing, and so on), jobs restored or added by hand (`keep_visible`), and postings that have neither a posting date nor an import date (none exist: `first_seen_at` is never empty).
- The Settings help text for the age box says what is now true: the posting date, or the day it was imported when there is none.

## Acceptance criteria
Each one is checkable in `verify.md`.
1. [ ] **New default:** `default_filters()["max_age_days"] == 30` and a fresh `Config` carries it; a stored value, whatever it is, is never changed by the code (a Config saved with 60 or 45 reads back 60 or 45).
2. [ ] **Dated postings:** `filters.hidden_reason` hides a job dated 31 days ago with `age` and days 30, keeps one dated 29 days ago, and for a job with both dates uses `posted_at` (a posting dated 5 days ago and imported 90 days ago is kept; one dated 40 days ago and imported yesterday is hidden).
3. [ ] **Undated postings, on arrival:** a job with no `posted_at` and `first_seen_at` 31 days ago is hidden for age through the same function and through `matching.judge` on a candidate's view (a view reads its job's own import date; it has no `first_seen_at` of its own, only `created_at`); one imported 29 days ago is kept. A view created today for a job imported 31 days ago is still hidden.
4. [ ] **Undated postings, refilter:** `matching.refilter` loads the import date and hides/shows undated jobs the same way (a test with a candidate whose limit changes from 60 to 30 and back; the job returns when the limit is raised).
5. [ ] **Undated postings, nightly age-out:** `matching.age_out` hides a visible new view whose job has no `posted_at` and an import date older than the limit, and leaves one whose job is dated recently (even if imported long ago) and one with `keep_visible` untouched; status other than new is never touched.
6. [ ] **No scoring past the limit:** after `refilter` and `rescore` on a candidate with a dated 45-day-old job, an undated job imported 45 days ago, and a recent one, only the recent job has a score (and an `AiTask` selection query returns none of the two old ones).
7. [ ] **Switched off:** an empty or zero limit hides nothing for age, dated or undated.
8. [ ] **Size of the one-off effect is known before it ships** (read-only count in `evidence/`): on a local copy of the 29 Oct dump, how many visible views of each candidate would be hidden by (a) the new undated rule at 30 days, and (b) the 30-day limit on dated postings, compared with the limit they have in the dump. Nothing is written to the dump copy or to Neon.
9. [ ] **No data change:** the diff of the cycle contains no migration, no command that writes settings, and no change to existing candidates' stored `max_age_days`; a read-only local count shows the stored values of the dump copy (for the record, since the owner's manual change is on the host).
10. [ ] **Help text and French:** the age box's help text mentions the import date; the new string is in `locale/fr` and `manage.py i18n missing` prints nothing; `tests/test_i18n.py` passes.
11. [ ] **Regression:** the existing age tests are updated for the new default and the undated rule (`tests/test_stale.py`, `tests/test_core.py:90-93` whose comment "no posting date: nothing to judge" is now false), and the full suite passes on SQLite (from Git Bash, as PROJECT.md says).

## Design in brief
- **One definition of a posting's date** in `jobs/services/filters.py` (a small function, for example `listing_date(job)`): `posted_at`, else the job's `first_seen_at`. It works on a job or on a candidate's view alike (a view proxies `posted_at` and `first_seen_at` to its job). `hidden_reason` uses it in its last rule instead of `job.posted_at` alone.
- **Refilter loads the import date:** `FILTER_FIELDS` (`matching.py:198-199`) gains `job__first_seen_at`, so the refilter still loads nothing else and reads no posting text.
- **Nightly age-out:** the query in `age_out` becomes "dated and older, or undated and imported earlier than the cutoff" (two conditions OR-ed on the database), still reading no text.
- **Default:** `default_filters()` 60 to 30 in `jobs/models.py`.
- **Help text:** one string changed in `settings.html` (`title` of the age label) plus its French entry.
- **Rejected:**
  - *Move existing candidates by a migration or command* (the owner did it by hand; a data write on Neon is outside this cycle).
  - *Use `first_listed_at` (the repost chain's first date) for undated postings* (it would also age reposts, which is cycle 022's subject; the owner chose the job's own `first_seen_at`; `freshness.badges` already shows `first_listed_at` as "open for more than 30 days").
  - *Use the candidate view's creation date* (`CandidateJob.created_at`: a view made later by a backfill would look young: Q4; the job's `first_seen_at` is what a view reads anyway).
  - *A separate "not analysed" flag* (hidden for age already means not scored; one reason code, no second state).

## Interfaces and data
- Code only: `jobs/models.py` (default), `jobs/services/filters.py` (date and rule), `jobs/services/matching.py` (`FILTER_FIELDS`, `age_out`), `jobs/templates/jobs/settings.html` (help text), `locale/fr` (string and `.mo`), tests.
- No migration, no new field, no setting or environment variable, no command that writes data.
- The same function serves other callers of `hidden_reason` (jungle ranking, radar rows): they now also treat an undated old posting as aged out, which is the intended consistency.

## Constraints
- **Neon:** nothing read or written on the hosted database; the counts of criterion 8 run on a local copy of the 29 Oct dump (a scratch SQLite or the local Postgres container), read-only.
- **Effect on the inbox:** the first refilter or nightly age-out after deploy hides, for each candidate who has limit 30, the undated postings imported more than 30 days ago and dated ones between 30 and their old limit; they stay in "Filtered & archive" with the reason and come back if the limit is raised. Criterion 8 gives the numbers so the owner knows before the deploy.
- **Cost:** the age-out query adds an OR on indexed-or-not columns of `jobs_job` per candidate; to be timed on the local copy (it reads no text).
- Mobile first and design system: no UI change beyond a help-text string.

## Out of scope
- Existing candidates' stored limits (done by hand by the owner).
- Repost handling, `first_listed_at`, the "open for more than 30 days" badge.
- Changing how a score is computed; the AI's own 14-day freshness window (`AiSettings.freshness_days`).
- A source's own `max_age_days` option (employer boards already seeded at 30).
- Anything on the hosted database.

## Gate
- [x] Owner approved this spec (2026-11-06)
