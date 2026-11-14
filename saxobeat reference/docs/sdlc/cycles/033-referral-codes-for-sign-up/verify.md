# Verify: invitation codes for sign-up

| | |
|---|---|
| **Cycle** | 033 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |
| **Written** | 2026-11-06, after slices 1 to 9; nothing is committed or deployed yet |

## Evidence per acceptance criterion
Tests are in `tests/test_invitation_codes.py` (63 tests) unless another file is named.

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Public `/signup/`, code field, `?code=` fills it, login page links to it | pass | `test_the_sign_up_page_is_public_and_a_link_fills_the_code_in`; look at 375 px: code filled with "Skaleet", `scrollWidth` 375 = 375, inputs 44 px high at 16 px, the login page shows "Inscrivez-vous avec un code d'invitation" (`evidence/look_2026-11-06.md`) |
| 2 | A valid code makes an account like `/join/` does; many uses | pass | `test_a_code_makes_an_account_like_an_invitation_does` (logged in, welcome e-mail queued, settings row, redirect), `test_a_code_is_many_use_and_each_account_records_it` (three accounts on one code), `test_the_language_of_the_page_is_the_language_of_the_account`; made a real "Lucie" through the page in the browser |
| 3 | No valid code, no account; one calm message; typed fields kept | pass | `test_no_valid_code_no_account_and_the_page_does_not_say_why` (empty, unknown, switched off), `test_an_account_error_keeps_the_code_and_the_other_fields` |
| 4 | Case and spaces ignored | pass | `test_a_code_matches_without_regard_to_case_and_spaces`; the page test signs up with " skaleet " |
| 5 | 10 wrong codes lock the page, even for the right code; reuses `FailedLogin` | pass | `test_ten_wrong_codes_lock_the_page_for_that_address_only_and_for_a_while`, `test_the_sign_up_page_locks_after_ten_wrong_codes_even_for_the_right_one` (429, then open again after the window), `test_wrong_codes_and_sign_ups_do_not_lock_anyone_out_of_the_login_page`; no new table (migration 0044 has one table, `InvitationCode`) |
| 6 | Brake of 3 per address and 20 in all per hour (D1) | pass | `test_the_brake_limits_one_address_to_three_accounts_an_hour` (also asserts the constants 3 and 20), `test_the_brake_limits_everybody_together`, `test_the_page_stops_a_flood_from_one_address_and_says_to_come_back` (429 and "try again in an hour"). **Note:** 20 accounts an hour would add about 160 MB (criterion 16): the owner may want a lower overall number |
| 7 | `/join/` unchanged; records "invitation link" | pass | `tests/test_accounts.py` passes with no edit to its expectations (51 pass with the new file at slice 3); `test_an_invitation_link_still_works_and_records_its_origin` |
| 8 | The operator makes, names, switches codes; rules on names | pass | `test_the_operator_makes_a_code_and_sees_its_link_and_count`, `test_a_bad_code_name_gives_a_message_and_makes_nothing` (3 cases), `test_a_taken_code_name_is_refused_even_with_another_case_or_a_candidates_code`, `test_switching_a_code_off_stops_new_sign_ups_and_leaves_the_accounts`, `test_only_an_operator_can_see_or_use_the_code_pages`; seen on the console page |
| 9 | *Came through* on each person; summary adds up | pass | `test_every_person_shows_where_they_came_from_and_the_summary_adds_up`, `test_the_origin_summary_adds_up_to_the_number_of_accounts`; on the scratch app: Skaleet 1 + candidates' codes 0 + invitation links 1 + before codes 2 = 4 accounts |
| 10 | The operator switches a candidate's code off and on | pass | `test_the_operator_switches_a_candidates_own_code_off_and_on_from_their_row` (their link refuses while off) |
| 11 | Migration marks used invitations; counts equal | pass | `evidence/migration-0044-2026-11-06.md` (29 Oct dump: 2 candidates, 3 users, 4 invitations before and after; 1 account marked "invitation", 1 blank); `test_the_migration_marks_only_the_accounts_that_used_an_invitation`; `makemigrations --check`: no changes |
| 12 | `/invite/`: login, one code of 8 readable characters, never a second, no edit, view-as never makes one | pass | `test_the_invite_page_needs_a_login`, `test_a_candidate_gets_one_code_of_eight_readable_characters_and_keeps_it`, `test_two_first_visits_at_once_end_with_the_same_code` (a simulated race: the loser reads the winner's), `test_a_random_clash_with_an_existing_code_draws_again`, `test_there_is_nothing_to_edit_on_the_invite_page` (POST answers 405), `test_a_candidate_has_at_most_one_code` (database refuses), `test_viewing_as_a_candidate_never_makes_their_code` |
| 13 | Code, link, copy, share where offered, friend count as a number, friend shown in the console | partial | The page, link, both copy buttons, the count and the console text are tested and were looked at (`test_a_friend_who_signs_up_through_the_link_is_counted_and_seen_by_the_operator`; inviter sees "1 friend", never the friend's address). **The share button was not seen working:** the browser used has no share sheet, so the button stayed hidden (correct), and `navigator.share` itself is untested here: the owner's phone check |
| 14 | Reachable from Settings and More in both modes; French complete; 375 px; 44 px | pass | `test_the_invite_page_is_one_tap_from_settings_and_more_in_both_modes` (4 cases), `tests/test_i18n.py` passes (1,282 strings, 0 missing), look at 375 px: `/invite/` no sideways scroll, buttons 44 px, `/more/` shows "Inviter des amis". A stray quote in a French line was found in the look and fixed, with a regression assertion |
| 15 | Deleting an inviter: code goes, friends keep origin text, dead code opens nothing, handful of statements | pass | `test_deleting_the_inviter_removes_their_code_and_leaves_the_friends_with_their_origin` (under 80 statements, summary count stays 2), `test_a_deleted_inviters_code_signs_nobody_up_any_more`, `test_a_person_who_deletes_their_own_account_takes_their_code_with_them`; the guard test in `tests/test_account_delete.py` failed between slices 2 and 7 as planned and passes with `InvitationCode` listed |
| 16 | What one new account costs, and how many Neon can hold | pass | `evidence/cost-2026-11-06.md`: about **8 MB** and 30,675 job views per account on the 29 Oct catalogue, first backfill 53 to 59 s. Against Neon's 0.5 GB with the app at about 180 MB (DEPLOY.md, older figure; the owner's 2026-11-05 reading of 0.55 GB is across projects): room for about **40 such accounts**, and 20 in an hour would be 160 MB. The dump predates the 30-day purge, so the host's figure may be smaller; to be re-read on the host before the deploy |
| 17 | Suite on SQLite and once on Postgres; `makemigrations --check` | pass | SQLite: `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider` → **1706 passed** (74.6 s, 2026-11-06). Local Postgres 17 (Docker, localhost): whole suite **1706 passed** (135 s). `makemigrations --check --dry-run`: "No changes detected" |
| 18 | Owner's step after the deploy: first code, sign up through it, read criteria 1 to 3 on the host | pending | Waits for the commit, the push and the deploy (owner); then I read `/signup/`, the People table and the new person's origin |

## Read on the host (2026-11-06, after the owner's deploy; I read, I made no account)
- `https://app.saxobeat.fr/signup/?code=Skaleet`, not logged in: 200, heading "Créez votre compte", the code field already holds "Skaleet", fields code, name, e-mail, password, confirm, and a link to `/login/` (read with the in-app browser, DOM).
- `https://app.saxobeat.fr/invite/`, not logged in: redirected to `/login/?next=/invite/` (login required, as tested).
- The owner reports the People page looks right ("looks good", 2026-11-06). **Not yet done by the owner:** signing up through a link, and the phone check of the share button. Criteria 13 and 18 stay `partial` and `pending` until then; I will not make an account on the host myself.

## Tests
- New: `tests/test_invitation_codes.py`, 63 tests (model, account logic, sign-up page, console, invite page, deleting an account).
- Existing and untouched: `tests/test_accounts.py`, `tests/test_account_delete.py` (its guard now lists `InvitationCode`), `tests/test_i18n.py`.
- One regression found by the suite and fixed in this cycle: `test_the_people_page_counts_each_candidates_jobs_without_joining_them` (a 12-statement cap) failed when the new console section added queries; the summary now takes two queries and the friend count is a subquery, so the page stays under the cap.
- One slip of mine found and fixed while building: an edit that replaced the end of `accounts.py` (login throttle, reset links, delete) was caught at once by the suite and restored from git before anything else ran; the file's diff against HEAD was read afterwards and shows only the intended changes.
- Known failures: none (SQLite and Postgres).

## Not verified
- **On the host:** nothing (criterion 18 is the owner's deploy). The migration has not run on Neon; the host's catalogue size and its real cost per account are not read.
- **The share sheet** on a real phone (criterion 13), Safari, and the English wording of the invite page on a phone.
- **Real concurrency:** the one-code race is simulated (an insert between the look and the create), not run with two threads; the brakes are counted before the insert, so two sign-ups at the very same moment can pass a limit by one or two.
- **Proxy addresses:** the per-address limits read the first `X-Forwarded-For` entry, as the login throttle does. A whole office behind one address shares the limit of 3 accounts an hour (a team signing up together through "Skaleet" from one office would be held back for an hour).
- **E-mail:** welcome e-mails to new accounts go through Brevo's 300 a day; Outlook and iCloud inboxes still untested (cycle 003).
- **The console at phone widths**; the People table is wider than 800 px (it was before).
- The French wording read by the owner.

## Verdict
- [ ] Accepted by owner
- [ ] Sent back (what, to which stage)
