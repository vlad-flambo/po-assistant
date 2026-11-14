# Spec: places and remote options in Settings for standard mode

| | |
|---|---|
| **Cycle** | 030 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |

## Behaviour when finished
- A **standard-mode** candidate opens Settings and sees a card, "Where you want to work" (name to be settled in the build), above the AI and language cards. It holds four things, the same as the power form:
  1. **Cities**: one tick per city in the registry (today Paris, Île-de-France, London, Hong Kong, Singapore), the candidate's current ones ticked. None ticked means no location limit, and the card says so.
  2. **Accept remote roles anywhere in France** (tick).
  3. **Also accept these cities, for remote roles only** (one tick per city).
  4. **Remote only** (tick: drops postings explicitly on-site or hybrid).
- It has its own **Save**. Saving writes those four filters and nothing else, then filters and scores the candidate's jobs again in the background and says so ("Your places are saved. Your jobs are being sorted again."), because standard mode has none of the apply buttons the power page shows.
- The guided "Where?" question and the card read and write the **same** stored places, so reopening either one shows what the other saved.
- A **power-mode** candidate keeps today's page unchanged (the same boxes already sit in the Hard filters group); the new card is not shown to them.
- An operator **viewing as** a candidate cannot save the card ("Only <name> can do this", the existing refusal).
- Nothing changes for any candidate until they save: no data is moved, no rescoring on deploy.

## Acceptance criteria
Each one is checkable in `verify.md`.
1. [ ] **Shows, standard mode:** the Settings page of a standard candidate contains the four controls above, pre-ticked from `filters["cities"]`, `["remote_france"]`, `["remote_cities"]`, `["remote_only"]`; the page of a power candidate does not contain the new card (and still has its existing boxes).
2. [ ] **Saves, standard mode:** a POST of the card changes exactly those four keys in the candidate's `Config.filters`. A test that sets every other filter (max age, languages, salary floor, blocked words, min score, seniority factor, follow-up days) to a non-default value and every keyword and the profile text, saves the card, and finds all of them unchanged.
3. [ ] **The inbox follows:** on a local copy, after saving a card with only Hong Kong ticked, a Paris job is hidden with the reason "location" and a Hong Kong job is kept; after saving it back with Paris ticked, the Paris job returns and has a score once the background pass ends. A remote role in France is hidden or shown with the "remote anywhere in France" tick; an on-site posting is dropped with "Remote only" on and returns when off.
4. [ ] **One list, not two:** after saving the card, `ask` question "Where?" shows the same ticks and "Remote in France too" matches; after saving the "Where?" answer, the card shows it. (`candidate.preferences["cities"]` and `["remote_france"]` are updated with the filters, so the guided page does not show an older answer and a later guided save does not undo the card.)
5. [ ] **Nothing ticked:** saving with no city ticked stores an empty list and the card shows the "no location limit" wording; no error.
6. [ ] **Viewing as:** a POST from an operator viewing as a candidate changes nothing and shows "Only <name> can do this".
7. [ ] **No old-page damage:** a power candidate's full Settings form posted from an old page still saves as today (existing tests pass), and a standard candidate's POST of the old whole-form is still refused with a redirect, with no field blanked.
8. [ ] **French:** the card's new texts are in the French catalogue (`locale/fr`), and the i18n test passes.
9. [ ] **Regression:** the full suite passes on SQLite (`SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider`), and nothing is read from or written to Neon.

## Design in brief
- **A separate action, not the big form.** The standard page keeps refusing the whole-form POST (`jobs/views.py:1009-1010`). A new small view (for example `settings_places`, `POST /settings/places/`, `@login_required`, `@require_POST`, `@impersonation.personal`, like `ai_consent` in `jobs/views_cv.py:229-231`) takes only the four fields. This keeps the "one form saves every field" rule intact.
- **One function writes the places.** A function in `jobs/conversation.py` (next to `apply`) sets `filters["cities"]`, `["remote_france"]`, `["remote_cities"]`, `["remote_only"]` in the Config and mirrors `cities` and `remote_france` into `candidate.preferences`, then returns. The view then starts `matching.recompute_in_background(candidate)` and redirects to Settings with a message. Validation as in the power save: keys must be in `city_registry.CITIES`.
- **Template:** the card sits in `jobs/templates/jobs/settings.html` outside the `{% if power %}` block, shown when `not power`; chips and spacing as in the house design system (phone first, one blue theme), reusing the existing `chip` style of `ask.html`.
- **Rejected:**
  - *Show the whole power form to standard mode* (a bigger change; the form deliberately saves every field at once and would blank unseen ones).
  - *Only link to the guided "Where?" question* (what exists today; it cannot set the remote cities or "Remote only").
  - *Make the guided "Where?" question the single store and have the card write only the preferences* (the guided `apply` rewrites the Config from the answers and would reset the other filters in a surprising order; one function writing both is simpler to test).
- **Cost:** `recompute_in_background` makes missing views, judges every new view again and scores all visible ones (`jobs/services/matching.py:250-269`, same as the Search-breadth dial). It reads posting text. The cost is the same as one press of the dial; a cheaper pass (score only the jobs that just became visible) is a plan-stage option, not a requirement.

## Interfaces and data
- New URL `settings/places/` (name `settings_places`) in `jobs/urls.py`; one view in `jobs/views.py` or `jobs/views_cv.py`; one function in `jobs/conversation.py`; the card in `settings.html`; French strings in `locale/fr/LC_MESSAGES/django.po` (compile as the project does).
- No migration. No new field. Existing keys only: `Config.filters["cities" | "remote_france" | "remote_cities" | "remote_only"]`, `Candidate.preferences["cities" | "remote_france"]`.
- No setting or environment variable.

## Constraints
- **Mobile first** and the house design system (`house-stack`: `design-system.md`); the card must work at phone width.
- **Neon:** nothing is rehearsed or written on the hosted database; the drill runs on a local copy (SQLite). The deploy is a normal code deploy the owner decides; it changes no data.
- **Privacy:** none new; places were already stored.
- **Tests:** add them next to the existing standard-mode and settings tests (`tests/test_core.py::test_settings_save_cities_and_weights`, `tests/test_onboarding.py`, `tests/test_conversation.py`); run with the project's command (PROJECT.md).

## Out of scope
- The onboarding place choice itself (done, owner, 2026-11-06), and the default ticks in the "Where?" question (Paris only today; Île-de-France is not pre-ticked).
- Showing other power settings to standard mode; changing the power form; changing how a job's location is matched to a city; adding destinations.
- Making the recompute cheaper (a separate candidate if it matters; cycle 029 covers the "scores are out of date" line).
- Any change to the hosted database or to existing candidates' stored places.

## Gate
- [x] Owner approved this spec (2026-11-06)
