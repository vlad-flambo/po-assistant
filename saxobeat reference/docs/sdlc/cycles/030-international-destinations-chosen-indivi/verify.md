# Verify: places and remote options in Settings for standard mode

| | |
|---|---|
| **Cycle** | 030 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence (command and output, measurement, screenshot, link) |
|---|-----------|--------|-------------------------------------------------------------|
| 1 | Shows in standard mode; not shown to power | pass | `tests/test_settings_places.py::test_the_standard_settings_page_has_the_card_ticked_from_the_saved_places` (four controls pre-ticked from the saved filters, all five registry cities, no power fields) and `::test_the_power_settings_page_has_no_card_and_keeps_its_own_boxes` (no card, `#cities` `#remote_cities` `#remote_france` `#remote_only` still there). Seen in the in-app browser at 375 px on a scratch server, 2026-11-06: the card sits under the language card; two remote labels first rendered as clipped chips, fixed to wrapping checkbox labels (slice 3). |
| 2 | Saves exactly the four keys | pass | `::test_saving_the_card_changes_no_other_setting` (max age, languages, salary floor, blocked words, min score, keywords and profile text unchanged) and `tests/test_conversation.py::test_set_places_writes_the_four_place_filters_and_nothing_else` (diff of the filters is a subset of the four keys; profile version unchanged). |
| 3 | The inbox follows | pass | `evidence/drill.md`: scratch SQLite, four jobs, six saves, refilter and rescore run directly. Only Hong Kong ticked: Hong Kong visible and scored, Paris hidden (`location`); Paris plus "remote anywhere in France": the Lyon remote role visible; plus Remote only: the on-site Paris job hidden (`not_remote`); Remote only off: it returns with a score; nothing ticked: all four visible. In the real browser, tick Hong Kong and Save showed "Vos lieux sont enregistrés. Vos offres sont en cours de nouveau tri." |
| 4 | One list, not two | pass | `::test_the_card_and_the_guided_where_question_show_the_same_places` (card, then the "Where?" page shows the same ticks and "Remote in France too"; a guided save then replaces the filters' cities and remote_france) and `tests/test_conversation.py::test_set_places_keeps_the_conversations_answer_in_step_and_drops_unknown_keys` (preferences mirror the filters, "where" is marked answered). |
| 5 | Nothing ticked | pass | `::test_nothing_ticked_means_no_location_limit_and_is_not_an_error` (302, `cities == []`); drill step 5 (all four jobs visible); the wording is on the card. |
| 6 | Viewing as | pass | `::test_the_operator_viewing_as_a_candidate_cannot_change_their_places` ("can do this" shown, cities unchanged, recompute not started); the card's Save is disabled with the existing title when viewing as (template; the refusal is the tested part). |
| 7 | No old-page damage | pass | `::test_the_old_whole_form_post_from_a_standard_candidate_is_still_refused_and_blanks_nothing`; the existing power save tests (`test_core.py::test_settings_save_cities_and_weights`, `test_screens_mobile.py`) pass unchanged in the full run. |
| 8 | French | pass | `uv run python manage.py i18n missing` prints nothing after the four strings were added and compiled; `tests/test_i18n.py` passes; `::test_the_card_is_in_french_for_a_french_candidate`; seen in French in the browser. |
| 9 | Regression | pass | `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider` (from Git Bash): **1,623 passed**, 0 failed, 106.7 s. Baseline before slice 1: 1,610 passed (102.7 s); 13 new tests. Nothing was read from or written to Neon: the drill and the browser run used a scratch SQLite file. |

## Tests
- Baseline before any change: 1,610 passed. After: 1,623 passed (10 in the new `tests/test_settings_places.py`, 3 in `tests/test_conversation.py`).
- A first baseline attempt from PowerShell (`$env:DATABASE_URL=''`) removed the variable, so pytest-django tried to create a test database through the `.env`'s `DATABASE_URL` and failed on a connection error after about 9 minutes: nothing connected, nothing was created or written (the error is `OperationalError` from psycopg at connection time). The suite was then run from Git Bash, where `DATABASE_URL= cmd` sets an empty value, as PROJECT.md and the memory note say. PROJECT.md and the memory note now say the PowerShell form is wrong.

## Not verified
- **On the host:** nothing deployed; the card has not been seen on Render, and the background pass has not been timed on a real-size inbox (the cost of one pass is the same as one press of the Search-breadth dial; cycle 029's measure is 16.6 MB read for about 3,000 jobs).
- **The owner's phone check** (plan slice 6): the card was seen at 375 px in the in-app browser, not on a phone.
- **Postgres:** the suite ran on SQLite only; no Postgres-specific code was added.
- The recompute thread itself is monkeypatched in the save tests and run directly in the drill; the thread start is the existing `recompute_in_background` used by the breadth dial.

## Verdict
- [x] Accepted by owner (2026-11-06, after the owner's phone check)
- [ ] Sent back (what, to which stage)
