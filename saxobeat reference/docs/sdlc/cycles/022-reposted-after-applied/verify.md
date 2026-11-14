# Verify: reposted after applied

| | |
|---|---|
| **Cycle** | 022 |
| **Stage** | Verify (drafted 2026-11-04; the host read and the filter finding added the same evening) |
| **Spec** | [spec.md](spec.md) |

## Evidence per acceptance criterion
Tests are in `tests/test_repost_applied.py` (56 tests); "look" is [evidence/look_2026-11-04.md](evidence/look_2026-11-04.md).

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Banner on a repost, for every application state and every state of the repost | pass | `test_the_repost_says_it_was_listed_before_with_the_date_the_status_and_a_link` (6 application states x New, Shortlisted, Dismissed = 18 cases: date, status label, link, and no banner on the application itself); service tests for applied, interviewing, offer, accepted, rejected, withdrawn, the auto-rejected one, and the Shortlisted-then-Rejected non-case |
| 2 | The whole chain, not the parent | pass | `test_a_role_listed_three_times_is_one_chain_whichever_posting_was_applied_to`, `test_the_newest_application_comes_first` |
| 3 | The warning is about other roles only; the generic list does not repeat the role | pass | `test_the_warning_about_two_applications_is_for_other_roles_only`; mutation check (breaking the line makes it fail); the existing `test_an_application_to_the_same_employer_shows_with_a_warning_for_six_months` passes unchanged |
| 4 | Inbox row tag (desktop) and, by decision D1, the first chip of the phone card; the row stays listed | pass | `test_the_repost_row_carries_a_same_role_tag_and_stays_in_the_inbox`, `test_the_employer_tag_stays_for_another_role_next_to_the_same_role_tag`, `test_the_phone_card_leads_with_already_applied_and_keeps_the_two_chip_rule`, `test_a_card_of_a_job_that_is_not_a_repost_of_an_application_has_no_such_chip`; look (chip "↺ déjà postulé" on the card at 375 px). The desktop row at 900 px and wider has no screenshot (DOM only) |
| 5 | Pointer on the earlier job | pass | `test_the_application_points_at_the_newest_posting_of_the_role_open_or_closed`, `test_an_application_in_the_middle_of_the_chain_points_forward_only`, `test_no_pointer_without_a_newer_posting_or_without_an_application`, `test_another_candidates_private_posting_is_not_a_pointer`; look (`#listed-again` with link to the repost) |
| 6 | The filter, chip, off by default, a view that is an application stays | pass | `test_the_filter_is_off_by_default_and_hides_only_reposts_of_applied_roles_when_on`, `..._a_posting_that_is_itself_an_application_stays_under_the_filter`, `..._follows_an_application_in_any_state_and_ignores_a_shortlisting`; look (one row off, none on, checkbox and chip) |
| 7 | Nobody else is affected | pass | `test_a_candidate_who_did_not_apply_sees_no_banner`, `test_another_candidates_application_is_never_found`, `test_another_employer_or_candidate_gets_no_same_role_tag`, `test_the_filter_never_looks_at_another_candidates_applications` |
| 8 | Nothing stored, no migration, no write on a view | pass | `manage.py makemigrations --check --dry-run`: "No changes detected"; `test_looking_at_the_pages_writes_nothing_to_the_jobs_tables` (four URLs, after the app's own first-visit inserts) |
| 9 | Speed: same queries for few and many rows; the job page adds one query | pass (query counts only; time at scale is 14) | `test_the_book_still_costs_one_query_and_the_same_role_lookup_none`, `test_the_inbox_runs_the_same_queries_for_few_rows_and_for_many` (3 vs 15 rows), `test_the_filter_costs_the_same_queries_for_few_rows_and_for_many`, `test_the_pointer_costs_one_query_and_only_on_an_application` |
| 10 | French | pass | 6 new strings translated; `i18n missing` empty; `tests/test_i18n.py` passes; the look ran in French (banner, pointer, chip, filter, all in French) |
| 11 | Tests, suite with no new failure | pass | 54 new tests; full SQLite suite 1,606 passed, 0 failed (112 s, 2026-11-04, after the last code change but one: the no-write test came after; the new file alone was re-run: 54 passed) |
| 12 | The real case on the host | partial | [evidence/host_read_2026-11-04.md](evidence/host_read_2026-11-04.md): 36143 shows the banner with the link to 31673 and its status, the generic line names only the other role; 31673 shows the pointer to 36143 (open); the chain assumption holds. **Not seen on the host:** the tag or chip on 36143's inbox row (the owner dismissed 36143, so it is not in the inbox) and the filter (it hung, see 14) |
| 13 | Phone width | pass | look: `scrollWidth` = `innerWidth` = 375 on the repost page, the application page and the inbox; screenshots of the repost page, the application page and the card |
| 14 | The filter at the host's size (added after the host hung) | partial | First design (correlated `EXISTS`): count over 20 s and top 30 over 20 s on 24,000 views, cancelled; two requests to the host did not answer and the host went down for some minutes. Fix (D2): count 0.039 s, top 30 0.024 s (candidate 1), 0.010 s and 0.016 s (candidate 3); `test_the_filter_is_not_a_correlated_subquery_per_row`; suite 1,610 pass. **Pending: the fix is committed and pushed (`13a60ae`, the owner's word 2026-11-10) but not yet read on the host: the browser pane was signed out, see next.md "Pick up here"** |

## Tests
- `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider`: **1,606 passed** (after slice 8); after the filter fix **1,610 passed** (2026-11-04 evening), the new file has 56 tests. The cycle-015 test that fails on Postgres (equal timestamps) was not run here: this suite is SQLite.
- Mutation check on the warning rule (slice 2); restored, tests green.

## Not verified
- **Time at scale was not measured before the push** (only query counts): that is how the filter's first design reached the host; see 14 and decisions.md D2.
- The inbox tag or chip on a real row: 36143 is dismissed, so no row of the first inbox page carries it.
- **The host.** Nothing here proves 36143's chain starts at 31673: the page's own "first listed 28 Oct" is consistent with it, only slice 10 will show it.
- **Postgres.** The new queries (`Exists`, `Coalesce`) ran on SQLite only; they are standard Django ORM and run on Postgres, but no test ran there. The owner's first look on the host covers it, or `DATABASE_URL=` pointing at a local Postgres with the migrations applied (the local copy is behind by a migration, so it was not used).
- The desktop row at 900 px and wider has no screenshot.
- English wording at phone width was not looked at (the look ran in French).

## Verdict
- [ ] Accepted by owner
- [ ] Sent back (what, to which stage)
