# Verify: stop analysing postings older than 30 days

| | |
|---|---|
| **Cycle** | 031 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence (command and output, measurement, screenshot, link) |
|---|-----------|--------|-------------------------------------------------------------|
| 1 | New default 30; stored limits never changed by the code | pass | `tests/test_stale.py::test_the_default_is_thirty_days_and_a_stored_limit_is_never_changed_by_the_code` (a fresh Config reads 30; stored 60, 45 and None read back unchanged). `jobs/models.py:16`. |
| 2 | Dated postings use their own date | pass | `::test_a_dated_posting_is_judged_by_its_own_date_whatever_the_import_date` (31 days hidden, 29 kept; dated 5 days and imported 90 kept; dated 40 and imported yesterday hidden). |
| 3 | Undated postings, on arrival | pass | `::test_an_undated_posting_is_judged_by_the_day_it_was_imported` (31 hidden, 29 kept, on the job and on a view), `::test_the_import_date_is_the_jobs_own_not_the_date_a_candidate_got_their_view` (a view made just now for a job imported 31 days ago is hidden), `::test_a_job_arriving_through_a_run_is_judged_by_its_import_date_when_undated` (`matching.judge`, the function a run uses). |
| 4 | Undated postings, refilter | pass | `::test_changing_the_limit_hides_and_brings_back_undated_postings_in_a_refilter` (60, 30, 60: visible, hidden with reason `age`/30, visible) and `::test_a_refilter_reads_the_import_date_with_the_jobs_not_one_query_per_job` (queries equal for 2 and for 10 jobs; with `job__first_seen_at` taken out of `FILTER_FIELDS` the same test fails, 15 against 7, checked). |
| 5 | Undated postings, nightly age-out | pass | `::test_the_nightly_age_out_hides_undated_postings_by_their_import_date_and_leaves_the_rest` (hides undated-old and dated-old; leaves undated-young, dated-recent imported long ago, `keep_visible`, an applied job; the full refilter then finds nothing more). It failed first (1 hidden instead of 2), then passed with the new query. The older `tests/test_phase15.py` age-out test (no text read) still passes. |
| 6 | No scoring or AI offer past the limit | pass | `::test_nothing_past_the_limit_is_scored_or_offered_to_the_ai` (dated-45, undated-45 and a recent job: only the recent one has a `Score`; `selection.waiting` returns neither old job). |
| 7 | Switched off | pass | `::test_no_limit_means_no_age_rule_for_dated_and_undated_postings` (None and 0, in the filter) and `::test_the_nightly_age_out_does_nothing_when_the_limit_is_off`. |
| 8 | Size of the one-off effect known before it ships | pass | `evidence/counts.md` and the outputs: on the 29 Oct dump, candidate 1 has 485 of 1,632 visible views dated over 30 days (30 %), candidate 3 has 1,742 of 8,781; **no undated job was over 30 days old at dump time** (the database only goes back to 29 Sep 2026), but with today's date applied the undated ones are 106 (candidate 1) and 1,009 (candidate 3) and growing daily; the dated figure today would be 840 and 3,508. Age-out query: 11.3 ms with the undated branch against 12.0 ms without, no text read. |
| 9 | No data change | pass | `git diff` has no file under `jobs/migrations` and no command that writes settings; the only touched `jobs/` code is `models.py` (default), `services/filters.py`, `services/matching.py`, and the template/catalogue. The counts ran on a scratch database (`scratch031`, dropped), read-only. The dump's stored limits were both 60 (the owner's manual move on the host is not in it, not checked). |
| 10 | Help text and French | pass | The age box's help text now reads "Applies to every source, employer boards included. A posting's age is its posting date, or the day it was imported when it has none…"; `manage.py i18n missing` prints nothing; `tests/test_i18n.py` 28 passed; the French reads "…ou à défaut le jour où elle a été importée…", with the archive page named as elsewhere ("Filtrées & archives"). Not looked at in the browser. |
| 11 | Regression | pass | Full suite from Git Bash: **1,632 passed** (baseline 1,623 before this cycle). Tests updated: the default test, `test_a_run_drops_postings…` (now sets its own limit of 60), `test_core.py:93`'s comment. Two tests that carried a hardcoded date and would now age out were given a recent date: `test_greenhouse_adapter_and_run` (`first_published` was 2026-09-20) and `test_a_job_parked_as_awaiting_page_joins…` (`posted_date` was 2026-10-02). |

## Tests
- Baseline before the cycle: 1,623 passed. After: 1,632 passed (18 in `test_stale.py`, 9 more than before counting the default test replaced).
- Two runs of the suite showed one failure in the first (`tests/test_jibe.py::test_a_job_parked_as_awaiting_page…`, a real consequence of the new default, fixed as above) and one in the second (`tests/test_mail.py::test_the_ai_email_tells_the_new_picks_once_and_at_most_every_12_hours`) that passed alone, in its own file and in the third full run; not reproduced and not related to ages as far as I can see (it concerns a 12-hour mail spacing). Worth watching.

## Not verified
- **The host:** nothing deployed or committed. The effect on the real inbox is an estimate from the 29 Oct dump with today's date applied (`counts_today_output.txt`); the host's own stored limits (moved to 30 by the owner) were not read.
- **Postgres:** the suite ran on SQLite only; the new query is plain ORM `Q`, and its plan was seen on the local Postgres (a seq scan of `jobs_job`, 11 ms for 1,632 views).
- **Settings page in the browser:** the changed help text was not looked at on screen; it is a `title` attribute.
- **The date a source gives is trusted** as is: a posting with a wrong or very old `posted_at` is hidden by it, as before.
- **Reposts:** an undated repost has a new import date and counts as young (out of scope by the spec; `first_listed_at` was not used).

## Verdict
- [x] Accepted by owner (2026-11-06)
- [ ] Sent back (what, to which stage)
