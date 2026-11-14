# Verify: presume an application rejected after a month of silence

| | |
|---|---|
| **Cycle** | 019 |
| **Stage** | Verify done 2026-11-04: accepted by the owner (host look read-only, then put-back and console save, all on the host) |
| **Spec** | [spec.md](spec.md) |

## Evidence per acceptance criterion
Test files: `tests/test_auto_reject.py` (data model, backup), `test_auto_reject_sweep.py` (the rule, races, cost, command), `test_auto_reject_console.py`, `test_auto_reject_views.py`, `test_auto_reject_insights.py`. **82 tests**, all pass on SQLite and on Postgres.

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | The rule: Applied, more than N days, no interview, not focus, then Rejected with one history line, flag set, follow-up cleared | **pass** (local) | `test_a_silent_application_is_rejected_with_the_tag_and_a_history_line`, `test_the_month_is_more_than_30_days_not_30` (29, 30 and 31 days). On the host: 18 moved (`evidence/hosted_first_sweep.md`, banner, owner's paste); the history line itself was not looked at on the host |
| 2 | Left alone: newer, other statuses, interview stage, focus; follow-ups do not reset the clock | **pass** (local) | `test_only_applied_jobs_are_moved` (9 statuses), `..._an_interview_stage_...`, `..._a_focus_job_...`, `test_follow_ups_do_not_reset_the_month` |
| 3 | The candidate's move between the read and the write wins | **pass** (local) | four race tests (shortlisted, interview added, made focus, one job of two); **mutation-checked**: with the UPDATE weakened exactly those four fail |
| 4 | A second sweep changes 0 rows and writes 0 lines | **pass** (local, Postgres copy) | `test_a_second_sweep_changes_nothing`; `evidence/rehearsal.md` step 9 (moved 0, history lines unchanged at 17,018). Not run twice on the host |
| 5 | Delay 0 moves nothing, tags stay | **pass** (local) | `test_delay_zero_switches_it_off_...`, `test_zero_is_accepted_and_switches_it_off`, `test_the_command_says_so_when_it_is_switched_off` |
| 6 | Console field: 0 to 365, default 30, refused otherwise, operator only | **pass** (local) / seen on the host | `test_auto_reject_console.py` (7 refused inputs, limits, candidate 404, visitor refused), `test_roles`; browser check `evidence/screens/console_*.jpg`. On the host the owner read the field's page and its count line on 2026-11-03; on 2026-11-04 (after the sweep) the page loads for the operator and says "0 applications already past 30 days are waiting". Saving tried on the host the same day: 31 saved ("Saved: 31 days. 0 applications already past it…", count line "past 31 days"), then 30 saved again; the field now reads 30 |
| 7 | A changed delay changes the next sweep | **pass** (local) | `test_a_changed_delay_changes_what_the_next_sweep_moves` (45 then 30) |
| 8 | Tag and info box on the job page, EN and FR; none for a hand rejection | **pass** (local) and **seen on the host in English, 2026-11-04** (job 12568: chip "Auto-rejected", box with date, "no answer after 30 days" and the "Put back to Applied" button, history line "Applied → Rejected no answer after 30 days (automatic)" with Undo). French not looked at on the host | `test_an_auto_rejected_job_shows_the_tag_the_box_and_the_button`, `..._rejected_by_hand_shows_neither...`, `test_the_page_is_in_french_...`; screenshots `evidence/screens/job_page_*.jpg` (scratch database) |
| 9 | Put back: Applied, tag gone, month restarts, line written, `applied_at` kept, follow-up set; not re-swept | **pass** (local) and **pressed on the host, 2026-11-04 12:15** (owner's word, done by Claude in the owner's session on job 12568, 360learning): the box and tag disappeared, history gained "Rejected → Applied: put back after an automatic rejection" (3 lines, the sweep's line kept), Applied went 43 → 44, banner 18 → 17, the console still says 0 waiting (not re-swept) | `test_putting_it_back_restarts_the_month_and_removes_the_tag`, `test_a_job_put_back_is_left_alone_until_a_new_month_has_passed`; clicked in the browser on the scratch database; Postgres copy: put back, sweep right after moved nothing |
| 10 | Any other change of status clears the flag | **pass** (local) | parametrised model test (7 statuses), `test_moving_it_any_other_way_removes_the_tag_too`, `test_undoing_the_sweeps_line_from_the_history_puts_the_job_back` |
| 11 | Pipeline card tag, EN and FR, without a history read | **pass** (local) and **seen on the host in English, 2026-11-04**: the Rejected list shows exactly 18 "Auto-rejected" cards (counted from the page text); the hand-rejected cards (e.g. Papernest, Ipsen, PayPlug) carry no tag. French not looked at on the host | `test_the_card_in_the_rejected_column_carries_the_tag`, `..._in_french`, `test_the_tags_cost_no_extra_query_and_read_no_history` (same query count with 4 flagged and 4 plain cards); screenshot `pipeline_rejected_french_phone_375.jpg` |
| 12 | History line translated with the number of days | **pass** (local) | `test_the_history_shows_the_sweeps_line_in_words`, French variant |
| 13 | 7-day banner with count and link; gone after 7 days | **pass** (local) and **seen on the host** | `test_the_banner_counts_what_the_app_moved_in_the_last_7_days`, `..._disappears_by_itself_after_7_days_...`, singular. On the host the owner pasted the live banner on 2026-11-04: "18 applications with no answer were presumed rejected by the app in the last 7 days. See them in Rejected · Open one to put it back to Applied" |
| 14 | Insights: "no answer" apart from rejections and delays | **pass** (local) and **seen on the host, 2026-11-04**: stat "No answer, presumed rejected 18 · not counted as rejections"; diagram link "Applied → No answer: 18", legend "49 rejected · 18 no answer". French not looked at | `test_auto_reject_insights.py` (9 tests: standing, ends, delays, put-back, diagram, page, French). A bug found on the way and fixed: the sweep's line and the put-back would otherwise have counted as an employer's answer |
| 15 | Dry run = real sweep = independent SQL count | **pass on the local copy**; host **consistent, not measured** | Postgres copy: SQL 17 = dry run 17 = sweep 17 (`evidence/rehearsal.md`). Host: dry run 17 on 3 Nov (page), 18 moved on 4 Nov; the dump predicts 17 and 18 for those two days (`evidence/hosted_first_sweep.md`); no same-moment dry run or before/after counts were saved on the host |
| 16 | Cost: one read, one conditional UPDATE per chunk, no job text | **pass** (local) | `evidence/sweep_cost.md`: sweep 14.5 KB, no-op 1.7 KB, dry run 13.6 KB; 7 statements; `test_the_sweep_reads_no_job_text_...`. Not measured on Neon's own dashboard |
| 17 | Migration on SQLite and Postgres; full suite passes on both | **partly met** | Migration applied on SQLite, on the Postgres scratch copy and on the host (the console page loads). SQLite full suite **1,436 passed, 0 failed (2026-11-04)**. Postgres: this cycle's files and the related suites (165 tests) pass; the **full** Postgres run on 2026-11-03 was 1,417 passed and **1 failed**: `test_feedback_console.py::test_the_list_shows_who_when_where_and_every_answer_newest_first` (cycle 015), not touched here: it orders by `created_at` and this PC's clock gives equal timestamps for back-to-back calls (2000 of 2000 pairs), so the order is a tie on Postgres. Not re-run in full on 2026-11-04 |
| 18 | `i18n missing` empty | **pass** | `manage.py i18n missing` prints nothing (2026-11-04); 17 new strings with French |

## Tests
- SQLite, full suite, 2026-11-04: **1,436 passed**.
- Postgres, this cycle's five files plus `test_roles`, `test_pipeline_stats`, `test_backup`: 165 passed. Full Postgres suite 2026-11-03: 1,417 passed, 1 failed (above, unrelated, cycle 015).
- Mutation checks that failed as they should: weakened UPDATE (4 race tests), removed `auto_rejected_at` from the backup merge fields (1 test).
- Two tests of mine were flaky on this PC for the same clock-tie reason (a later change not later than an earlier one) and now date things apart.

## Not verified
- **On the host, still not done:** the French wording (needs switching the language); a non-operator getting 404 on the console page (no second account tried). Looked at read-only on 2026-11-04: Rejected cards, one job page, Insights, console page (see rows 8, 11, 14, 6). The number of auto history lines was not counted separately, but the 18 tagged cards, the 18 on Insights and the banner's 18 agree.
- That the host's history grew by exactly 18 lines and nothing else moved: no before/after counts exist.
- The hosted dry run on the day of the sweep (only the 3 Nov reading of 17).
- The pages on a real phone (checked at 375 px in a browser).
- Neon's own transfer figure for the sweep (the container counter was the proxy).
- French wording read by a French reader (the owner has not read it).

## Verdict
- [x] Accepted by owner (2026-11-04, in chat, after the host look and reading the French wording from the catalogue; the two small wording notes (gender of "présumée refusée", "Remettre" vs "Repasser") were left as they are; criterion 17 stays partly met: the full Postgres suite was not re-run on 2026-11-04 and one unrelated cycle-015 test fails there)
- [ ] Sent back (what, to which stage)
