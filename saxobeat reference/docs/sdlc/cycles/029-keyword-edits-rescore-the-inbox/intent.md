# Intent: keyword edits rescore the inbox

| | |
|---|---|
| **Cycle** | 029 |
| **Stage** | Intent |
| **Date** | 2026-11-05 |
| **Owner** | Vlad |
| **Importance** | 3/5 (claude, 2026-11-05): reach: every candidate whose keywords change (the owner's own inbox: 218 of 1,634 jobs sit on the wrong side of the floor, 2026-10-29 dump); pain: a silently out-of-date ranking, nothing breaks; a manual rescore exists but only in power mode |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
Not yet said in the owner's own words for this cycle: it comes from cycle 021, where the owner's finding was (as relayed, not verbatim) that *stored scores older than the keyword list were found by replay, and the rescore of candidate 1's inbox on the host (2,980 jobs) fixed it that once*. Cycle 021's `learn.md` offered it as a new cycle: "make a keyword or profile edit rescore the whole inbox reliably and say when it finished". **To be replaced by the owner's words when they give them.**

## Why now / the pain
- A keyword edit changes what the score *should* be, but the stored scores of the jobs already in the inbox stay as they were. The owner's inbox in the 29 Oct dump: of 1,634 visible jobs, **1,063 would score 1 point or more higher** with the list as it was saved, none lower, and **218 (13 %) sit below the floor of 35 but would be above it** (`evidence/baseline.md`). The order of the top 50 is the same; the visible list is not.
- Nothing says so. The inbox shows no "out of date" line, the profile version does not move on a keyword edit, and nothing records when keywords were edited. The only way anyone saw it was a replay on a scratch copy (cycle 021).
- The fix on 4 Nov (a command-line rescore of 2,980 jobs, 16.6 MB read from Neon) was a one-off: the next keyword edit brings the problem back.

## Goal
The owner decided (Q1, 2026-11-05) that **rescoring stays a button the candidate presses**, not something a save starts by itself. So the goal is: when a candidate has changed anything that feeds their scores, the app **says so** (the scores are older than their settings), one press brings the jobs they act on up to date, and the app says when that finished, or that it did not, even across a restart.

## Success measure
(Confirmed by the owner, 2026-11-06.)
1. **Drill on a scratch copy of the 29 Oct dump:** change candidate 1's keywords through the Settings save; the inbox then shows an "older than your settings" line (no false negative: every path that changes a scoring input shows it). Press the button; once the pass reports done, the replay finds **0 rows** (inbox and pipeline) whose stored score differs from the replayed one by more than rounding (today: 1,063 of 1,634 by 1 point or more), and the line is gone and shows when the scores were updated.
2. **No false alarm:** with nothing changed since the last pass the line does not show (drill: save settings unchanged, no line).
3. **Visible state and restart:** while a pass runs the page says so; a process kill half way leaves the page saying scores may be out of date, never "updated", and the next start of the web process or the runner finishes the pass.
4. **Cost:** a save reads no posting text; a pass reads each posting at most once; pressing the button during a pass starts no second pass; one pass of an inbox of about 3,000 jobs reads no more than the 16.6 MB of cycle 021's rescore.
5. **No regression:** imported AI reviews are kept, the full suite passes on SQLite and on Postgres, and nothing is read from or written to Neon during the drill.

## Not doing (this cycle)
- **An automatic rescore after a save** (owner, Q1, 2026-11-05: keep the button). The save stays free of Neon reads.
- Changing how a score is computed (cycle 021 closed that: glossary, language-aware similarity).
- Rescoring candidates 3 and 4 on the host (their inbox is about 10,000 jobs each, about 55 MB of reads per pass; they are test profiles).
- Making the rescore cheaper by reading less text (a separate candidate from cycle 021), except as far as Q5 and Q7 need it.
- Mentions-are-not-roles scoring and the other-language scale calibration (other 021 candidates).
- Anything on the hosted database before the owner approves a plan.

## What we already know (facts, with where they came from)
Code facts re-read on 2026-11-05 (HEAD `9d9ff6d` plus other sessions' uncommitted work, none of it in these files):
- **A save on the Settings page does not rescore anything.** `settings_view`, action `save` (`jobs/views.py:1013-1047`) writes keywords, weights and filters and shows "Settings saved. Use the buttons below to apply them to existing jobs." It bumps `cfg.profile_version` **only** when `profile_text` changed (`views.py:1015-1016`). *This corrects the brief this cycle started from, which said keyword edits start the background pass.*
- **Who does start `recompute_in_background`:** the Search-breadth dial (`views.py:1053`), the CV pages' target roles and undo-tuning (`views_cv.py:264, 272`), the end of onboarding (`views_cv.py:89`), and the AI tuning's `run_pending` (`jobs/ai/onboarding.py:80`). **Not** started after: a Settings save, the Insights "boost word" (`insights.apply_suggestion` sets a keyword at weight 3, `jobs/services/insights.py:113-119`), removing a keyword chip on the welcome review (`views_cv.py:150`), the `import_keywords` and `import_cv` commands (`import_cv` rescores itself, line 59).
- **The manual route:** the "Rescore new jobs" button (power mode only, inside `{% if power %}` in `settings.html`) calls `runner.rescore_all` **inside the request** (`views.py:1062-1064`), no thread; gunicorn's timeout is 120 s (`scripts/entrypoint.sh`). Locally, the cold setup of a rescore (similarity model and employer counts, file cache off) took 43 s (`evidence/baseline.md`); with Neon latency on top, whether a real inbox fits in 120 s on the host is **not measured**.
- **What a pass covers:** `matching.rescore` takes views with `status=new` and `hidden_reason=""` only (`jobs/services/matching.py:238`). Pipeline jobs (applied, interviewing, shortlisted...) keep their old score: 111 such scored views for candidate 1 in the dump; job 33238 reads 33 on the host for that reason (cycle 021 `verify.md` criterion 13).
- **The background pass** (`matching.recompute_in_background`, `matching.py:250-269`) is a daemon thread running `backfill`, `refilter`, `rescore`; `_recomputing` (a set in process memory) only blocks a second pass for the same candidate in the same process. Nothing is stored about it: no start, no end, no failure, no "pending". A deploy or restart of the web process kills the thread; with two workers (`WEB_CONCURRENCY` default 2 in the entrypoint, 1 on Render per DEPLOY.md) the guard is per process. `matching.recomputing()` exists and nothing calls it (grep, no template).
- **A flag for this already exists, for one case:** `Candidate.rescore_pending` (`models.py:79`), set by the AI tuning (`ai/onboarding.py:53, 68`) and cleared by `run_pending`, which the PC runner runs to the end (`ai/sync.py:108`, `management/commands/ai.py:103`) and the web server runs in the background (`views_ops.py:234`). That is the pattern for surviving a restart. It is not used by any keyword edit.
- **What a stored score records:** `Score.profile_version` (the config's version at scoring), `created_at`; no keyword hash, no timestamp of the config. `Config` has no `updated_at`. The inbox of candidate 1 in the dump was scored in one pass, 93 s, all at version 5, and is 1,063 rows behind the list saved a day later (`evidence/baseline.md`, sections 1 and 2).
- **Tests:** every test that touches `recompute_in_background` replaces it with a stub (`tests/test_phase8.py:31`, `test_onboarding.py:182`, `test_ai_onboarding.py:248`); `tests/test_runner_writes.py` has no rescore or recompute test; `tests/test_rescore_preview.py` covers the `rescore` command. **No test starts the real thread or checks that a keyword edit leads to a rescore.**
- **Other inputs that make a stored score stale**, besides keywords and profile text: `keyword_weight`, the seniority factor (the breadth dial; it does recompute), the dream-employer bonus (`Score.employer_bonus`), the glossary and the language scale (a code or switch change, rescored by hand per DEPLOY.md), and the similarity corpus as postings arrive (about 1.7 points on one job in cycle 021; not counted here).
- **Cost:** about 5.5 KB of posting text per rescored job (DEPLOY.md; cycle 021 `cost.md`): 16.6 MB for 2,980 jobs; about 55 MB for an inbox of 10,000. Neon's free allowance is 5 GB a month of network transfer; 0.49 GB used on 2026-11-05 (owner's reading, sum of all projects, cycle 021 `verify.md`). A pass per edit with no limit would spend the allowance: ten edits of a 3,000-job inbox a day is about 166 MB a day, about 5 GB in 30 days (arithmetic on the figures above; assumes nothing else reads).
- **The runner is started by hand a few times a week** (DEPLOY.md, status since 2026-10-29), so "the runner finishes it" alone is not timely.
- **Evidence this was real for the owner:** 28 Oct to 29 Oct the owner's include list went from 40 to 56 entries (48 added, 32 removed, 6 re-weighted) and the exclude list from 10 to 15; the profile version went 4 to 5 (`evidence/config_diff_output.txt`).

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | When the candidate saves settings that feed the score, should the rescore start by itself, or stay a button? | (was: start by itself) | **Keep the button** (owner, 2026-11-05) | answered |
| 2 | Since the button stays, what tells the candidate it is needed? | A line on the inbox, whenever the scores are older than the settings or the scoring rules: "Your scores are older than your settings: 1,063 jobs. [Score again]" with the button right there (and "Scores updated 11:42" once done). Without it nobody knows to press the button: that is how the owner's inbox fell behind. | **Yes, show the line** (owner, 2026-11-05) | answered |
| 3 | The button runs inside the web request today (120 s limit, cold setup 43 s locally). Should it start a background pass and return at once? | Yes: the button starts the pass in the background and the page shows "Updating your scores..." until it ends; the same code path for every trigger. | **Accepted as recommended** (owner, 2026-11-05) | answered |
| 4 | Should the pass cover the pipeline (applied, interviewing, shortlisted, withdrawn, rejected) as well as the inbox? | Yes, those statuses (111 views for candidate 1, negligible cost), not dismissed or expired (about 5,000 and 300 views nobody reads). That fixes job 33238's "33" for good. | **Accepted as recommended** (owner, 2026-11-05) | answered |
| 5 | What happens when the process dies mid-pass? | Reuse `rescore_pending`: set when the button is pressed, cleared only when the pass ends; the web process at start and the runner at each run finish a pending pass; the line says "may be out of date" meanwhile. Redo the pass, do not resume a position (idempotent, minutes). | **Accepted as recommended** (owner, 2026-11-05) | answered |
| 6 | How does the app know scores are older than the settings: `profile_version`, or a hash on each score? | A hash of the scoring inputs (keywords, weights, profile text, seniority factor, dream employers, a scoring-rules version) stored on each `Score` (nullable column), compared with the config's current hash. It gives the line in Q2 its count and catches a code change (a new glossary) too. `profile_version` stays for AI reviews. | **Accepted as recommended** (owner, 2026-11-05) | answered |
| 7 | Who sees the line and the button? | Power mode only, where the keyword forms and the button already are. Standard mode never edits keywords by hand, and its automatic paths (CV targets, onboarding, tuning) already rescore. The Insights "boost word" is power mode too. | **Accepted as recommended** (owner, 2026-11-05) | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Neon's network allowance (5 GB a month) is the scarce thing: every rescore reads posting text; a measurement or a drill never runs on the hosted database, only on a scratch copy.
- A new column on `Score` (Q5) is a migration on the hosted database: irreversible-class, only inside an approved plan, with a rehearsal on the local copy first.
- The web process is a single Render service with 512 MB; a pass loads the similarity model and the employer counts: memory and time of a pass on the host are not measured.
- Other sessions are changing files in the same working tree; this cycle's paths are `docs/sdlc/cycles/029-*` and the 029 row of the README.

## Gate
- [x] All open questions answered or parked (Q1 to Q7, 2026-11-05)
- [x] Goal and success measure confirmed by the owner (2026-11-06)
