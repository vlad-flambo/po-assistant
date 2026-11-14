# Plan: places and remote options in Settings for standard mode

| | |
|---|---|
| **Cycle** | 030 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

## Slices
Thin, ordered, each verifiable alone. Each slice names the acceptance criteria it moves. Nothing here touches Neon, a migration or any stored data; the only outward step (deploy) is the owner's, after the last slice.

| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | **One function that writes the places.** `conversation.set_places(candidate, cities, remote_france, remote_cities, remote_only)` validates keys against `city_registry.CITIES`, writes the four keys into the Config's filters (every other key and the keywords untouched) and mirrors `cities` and `remote_france` into `candidate.preferences`; an empty city list is stored as empty. No view, no page yet. | `jobs/conversation.py`, `tests/test_conversation.py` | New unit tests: the four keys change, a Config with every other filter at a non-default value and keywords and profile text is otherwise identical before and after; preferences mirror the filters; unknown keys are dropped; empty list stored. Then the whole `test_conversation.py` and `test_core.py` pass. | 2, 4, 5 | done |
| 2 | **The save action.** `POST /settings/places/` (`settings_places`): `@login_required`, `@require_POST`, `@impersonation.personal`; reads the four fields, calls `set_places`, starts `matching.recompute_in_background(candidate)`, adds a message ("Your places are saved. Your jobs are being sorted again."), redirects to Settings. | `jobs/views.py` (or `views_cv.py`), `jobs/urls.py`, `tests/test_onboarding.py` or a new `tests/test_settings_places.py` | Client tests: standard candidate saves and filters change; a viewing-as operator is refused and nothing changes; a GET is refused (405); the old whole-form POST by a standard candidate still redirects and blanks nothing; the power whole-form save is unchanged. Recompute is monkeypatched in the tests that only check the save. | 2, 5, 6, 7 | done |
| 3 | **The card.** In `settings.html`, outside the `{% if power %}` block and only when `not power`: the Cities ticks, "Accept remote roles anywhere in France", the extra remote-role cities, "Remote only", a Save button posting to the new URL; "no ticks means no location limit" under the cities; Save disabled with the existing "Only <name> can do this" title when viewing as. Context for it in `settings_view` (the standard branch). French strings added to `locale/fr` and the catalogue compiled the way the project does. | `jobs/templates/jobs/settings.html`, `jobs/views.py`, `locale/fr/LC_MESSAGES/django.po` (and `.mo` if the project tracks it) | Tests: the standard Settings page contains the four controls, pre-ticked from the Config; the power page does not contain the card and keeps `#cities`, `#remote_cities`, `#remote_france`, `#remote_only` (the ids the mobile-screens test checks, `tests/test_screens_mobile.py:65`); `tests/test_i18n.py` passes. Then a look at it in the in-app browser at phone width (375 px) and desktop. | 1, 7, 8 | done |
| 4 | **The guided page and the card agree.** Check, and fix if a test shows it, that the "Where?" question reads what `set_places` wrote (it prefers `preferences["cities"]`, `views_cv.py:203`), including "Remote in France too"; and that a later guided save does not undo the card's remote cities and "Remote only" (`conversation.apply` writes only `cities` and `remote_france` of the places). | `jobs/views_cv.py` and `jobs/conversation.py` only if a test fails; `tests/test_conversation.py` | Two-way test: card then "Where?" shows the same; "Where?" then card shows the same; remote cities and "Remote only" survive a guided save. | 4 | done |
| 5 | **Drill on a local copy.** On a scratch SQLite database with a Paris job, a Hong Kong job, a remote job in France and an on-site posting: save only Hong Kong ticked, run the refilter and rescore the background pass runs (called directly, not through the thread), read the reasons; save Paris back; toggle "remote in France" and "Remote only". Record the outputs in `evidence/`. | `evidence/drill.md` (a short script in the scratchpad, not committed unless useful) | The expected hidden reasons per job after each save, and a score on a job that came back. | 3 | done |
| 6 | **Full suite and verify.** Run `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider`; write `verify.md` with one row per criterion; the owner looks at the card on their phone. | `verify.md`, `evidence/` | The suite's pass count against the 1,192 recorded in memory (2026-10-29; the number has probably moved, so the baseline is taken before slice 1); the owner's phone check. | 1 to 9 | done |

## Order and dependencies
- 1 before 2 (the view calls the function), 2 before 3 (the card posts to the view), 4 after 3 (it needs both pages), 5 after 4, 6 last.
- Slice 0, before any change: run the suite once to record the baseline pass count and any failing test already there (this tree has other cycles' uncommitted edits, so a failure may not be ours).
- Nothing waits on the owner until slice 6 (the phone check) and the deploy decision.

## Rollback
- Every slice is code only: `git revert` of its commit, or discarding the uncommitted edits to its files. No data, migration or hosted setting is involved, so nothing needs undoing in a database.
- A candidate who saved through the card keeps their places after a revert: the stored keys are the same ones the old pages use, so nothing is orphaned.

## Risks
- **Recompute cost:** the background pass rescored every visible job (it reads posting text), as one press of the Search-breadth dial does. On the host that is read cost on Neon for one person per save. Mitigation: a candidate presses Save rarely; a cheaper pass (score only newly visible jobs) is a follow-up, not part of this plan. Say it in the verify cost line.
- **Two stores of the places** (`Config.filters` and `candidate.preferences`): the reason slice 1 has one function and slice 4 has a two-way test.
- **Uncommitted work of other cycles in the tree** (git status shows edits to `seed_employers.py` and the SDLC files): stage only this cycle's paths.
- **Translation drift:** a new string without a French entry fails `tests/test_i18n.py`; slice 3 owns it.

## Gate
- [x] Owner approved the slices (2026-11-06)

## As run
(log of the build, newest last; all 2026-11-06)
- **Baseline.** First attempt from PowerShell with `$env:DATABASE_URL=''`: PowerShell deletes the variable, so pytest-django tried the `.env`'s PostgreSQL and failed on a connection error after about 9 minutes (nothing connected, nothing written). Re-run from Git Bash with `DATABASE_URL=` (empty): **1,610 passed**, 102.7 s.
- **Slice 1 done.** `conversation.set_places` added; it also marks "where" answered, so the recap shows the card's answer. 3 tests, `test_conversation.py` + `test_core.py` 75 passed.
- **Slice 2 done.** `settings_places` in `views_cv.py` and `settings/places/` in `urls.py`, `@personal` like `ai_consent`. 7 tests in the new `tests/test_settings_places.py` (including the two-way "Where?" test planned for slice 4) passed first time.
- **Slice 3 done.** Card in `settings.html` for `not power`; `settings_view` gives `remote_france` and `remote_only`; four strings added with `manage.py i18n extract`, translated and compiled (the catalogue diff holds only these). Phone-width look: the two remote labels were clipped chips, changed to the power form's plain wrapping labels; rechecked. 3 more tests; 53 passed across the settings, i18n, mobile and standard-mode files.
- **Slice 4 done** inside slice 2's tests (guided page shows what the card saved; a guided save replaces cities and remote_france, keeps the rest). No code change was needed in `views_cv.py`.
- **Slice 5 done.** Drill on a scratch SQLite (`evidence/drill.md`), then a real click-through on a scratch dev server in the in-app browser (tick Hong Kong, Save, the message shows).
- **Slice 6 done.** Full suite **1,623 passed**; `verify.md` written.
