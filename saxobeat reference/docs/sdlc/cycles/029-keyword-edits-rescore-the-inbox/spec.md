# Spec: keyword edits rescore the inbox

| | |
|---|---|
| **Cycle** | 029 |
| **Stage** | Spec (drafted 2026-11-06) |
| **Intent** | [intent.md](intent.md) |

## Behaviour when finished
Power-mode candidates only (standard mode never edits keywords by hand and keeps its automatic paths).

Every stored score records **what it was scored with**: a short hash of the inputs that decide a score (keywords and exclusions, keyword weight, AI weight, profile text, the seniority factor of the breadth dial, the glossary switch, and a scoring-rules version number kept in the code). The app compares it with the hash of the candidate's settings as they are now. That comparison is the only definition of "out of date"; `profile_version` is not used for it.

The inbox has one status line, in one of four states:

| State | Shown when | The line says | Button |
|---|---|---|---|
| **Out of date** | no pass pending and at least one scored job in scope has a different (or no) stamp | "Your scores are older than your settings: *N* jobs." | **Score again** |
| **Updating** | a pass was started and its heartbeat is under 2 minutes old | "Updating your scores..." | none |
| **Interrupted** | a pass was started, did not finish, and its heartbeat is older than 2 minutes | "The last update did not finish: your scores may be out of date." | **Score again** |
| **Up to date** | nothing pending and nothing stale | a small muted line: "Scores updated <date, time>" (nothing if no pass has ever run) | none |

"In scope" means the jobs a pass covers: **the inbox (new, not hidden) and the pipeline** (shortlisted, applied, interviewing, offer, accepted, rejected, withdrawn). Dismissed, expired and hidden views are out of scope.

The button starts the pass **in the background and returns at once**; the page then says "Updating your scores...". The Settings page's "Rescore new jobs" button does the same (every job in scope, stamped or not) and its line shows the same state. A pass records a heartbeat as it goes. If the process dies, the next start of the web server, or the next run of the PC runner, finds the pending pass and finishes it without anyone pressing anything; because each finished row carries the new stamp, the redone pass only scores the rows still behind.

A save of settings stays free: it starts no pass and reads no posting text. The line appears on the next page view, because the count is a database count of stamps, wherever the edit came from (Settings save, an Insights "boost word", removing a keyword chip, a command).

## Acceptance criteria
Each one must be checkable in `verify.md`.
1. [ ] **The hash.** One function gives the same value for equal inputs whatever the order of keys; the value changes when each of these changes alone: an include keyword (added, removed, re-weighted), an exclude keyword, the keyword weight, the AI weight, the profile text, the seniority factor, the glossary switch, the scoring-rules version. It does **not** change when only a city, a blocked title word or employer, the language list, the age limit, the minimum score, the follow-up days or the dream-employer list changes (the dream bonus refreshes itself, per `dream.py`). One test per input, plus one for the non-inputs.
2. [ ] **The stamp is written by every scoring path.** A score written by the runner's scoring of a new job, by `score_views`, by a pass and by the `rescore` command carries the hash of the settings used for that scoring (loaded once at the start of the pass, so an edit made during a pass leaves its rows stale). Test: edit the keywords between two chunks of a pass, assert the rows of the pass count as out of date afterwards.
3. [ ] **The line after an edit.** For a power-mode candidate with a scored inbox, saving changed keywords makes the inbox show "Out of date" with a count equal to the number of in-scope scored views whose stamp differs. Saving the same settings again shows no line. The same holds after an Insights "boost word" and after removing a keyword chip on the welcome review. Tests for each path, and a test that a save of a non-input (a city) shows nothing.
4. [ ] **Unstamped means out of date.** Scores written before this change have no stamp; they count as out of date, so the first view after deployment shows the line for every power-mode candidate with scores, and one press stamps them. No migration step rewrites a score row (a stamp of "current" on old rows would be a false statement; see Design D1).
5. [ ] **The button starts a background pass and returns.** The POST answers with a redirect before any scoring: a test captures the SQL of the request and finds no read of `description_text`, no `score` write, and a started pass (flag and heartbeat set). The Settings "Rescore" button does the same.
6. [ ] **One pass per candidate, across workers.** A second press during a pass starts nothing. Starting is an atomic claim in the database (an update that succeeds for one caller only), so two starts at the same instant (two workers, or a web start and the runner) run one pass. Tested with two claims in a row and with two threads.
7. [ ] **What a pass covers.** It scores new, not-hidden views and the pipeline statuses; it leaves dismissed, expired and hidden views alone; imported AI reviews are kept (`ai_score` and review text unchanged, `final_score` recomputed by the existing blend). The inbox button's pass scores only the rows whose stamp differs; the Settings button and the `rescore` command score every row in scope (Design D3).
8. [ ] **Done is said only when it is true.** The flag is cleared, and the "updated" time stored, **only when the last chunk has been written**. A pass that raises leaves the flag set, shows "Interrupted" after the heartbeat grows old, and never shows "Scores updated" for it. Test: a pass whose third chunk raises.
9. [ ] **Updating.** While a pass runs, the heartbeat advances at least once per chunk and the line says "Updating your scores..." with no button; a heartbeat older than 2 minutes with the flag still set shows "Interrupted" with the button. Test with a frozen clock.
10. [ ] **Restart.** A pending, stale-heartbeat pass is claimed and finished by the web process at start and by the PC runner at each run. The start hook does nothing under tests, migrations or management commands other than the server. The existing AI-tuning path (`rescore_pending` set by a tuning or its undo) now clears the flag at the end of the pass, not at its start; a test shows a tuned search whose pass was killed is finished at the next start.
11. [ ] **Standard mode and the other paths.** A standard-mode candidate sees no line and no button. The breadth dial, the CV targets, the end of onboarding and AI tuning still start their passes, and those passes stamp their rows.
12. [ ] **Cost.** A save and an inbox render read no posting text: the render adds at most **one** query (the stamp count and the state), and that query selects no `description_text` (captured SQL). A pass reads each posting's text at most once. The inbox's query count does not depend on the number of rows shown.
13. [ ] **The drill, on a scratch copy of the 29 Oct dump (Postgres).** Candidate 1: change the keywords through the Settings save → the line shows with the count; press the button → the response comes back before the pass ends; the pass finishes; the cycle-021 replay harness (glossary as in the config) finds **0 rows** in scope whose stored deterministic score differs from the replay by 0.1 or more (today 1,063 of 1,634 inbox rows by 1 point or more); the line reads "Scores updated". Recorded for information, not judged: seconds, text read, the pass process's peak memory. Then kill the pass half way and show the "Interrupted" line, then start the server and show the pass finished by itself and the count at 0.
14. [ ] **The migration.** Three nullable columns and nothing else: `Score.scored_with` (short text), `Candidate.scores_updated_at`, `Candidate.rescore_heartbeat_at`. `makemigrations --check` reports nothing after it; it applies to a restore of the dump on the local Postgres without rewriting a row (no `UPDATE`, no default backfill), and migrates backwards. Rehearsed there before any hosted step.
15. [ ] **French.** Every new string (the four lines, the buttons, the date format) is translated in `locale/fr` and compiled.
16. [ ] **Phone and the design system.** At 375 px the line and its button show without horizontal scroll, the button is at least 44 px high, and the new CSS uses tokens only (the `.msg` component with its `.warning` variant for the out-of-date and interrupted states); no literal colour is added (grep on the diff).
17. [ ] **Tests.** New tests cover criteria 1 to 12 and 14; the suite passes on SQLite and on the local Postgres with no new failure; both counts are stated in `verify.md`.
18. [ ] **On the host (after the owner's deploy and word).** After the migration is applied on prod1: the line shows for candidate 1 (unstamped rows); the cost of the first pass is said before it is pressed (about 16.6 MB for the 2,980 inbox jobs, plus about 111 pipeline jobs) and Neon's transfer is read before and after; the owner presses the button (or says to press it for them); the pass ends by itself and the line reads "Scores updated"; a second view shows no line. Said who looked.

## Design in brief
- **A stamp per score, a state per candidate.** `Score.scored_with` is the first 16 hex characters of a SHA-1 over a canonical JSON of the inputs in criterion 1. The "state" lives on the candidate: the existing `rescore_pending`, plus `rescore_heartbeat_at` and `scores_updated_at`. Out of date is a count over `Score` joined to the candidate's in-scope views; it reads no text.
- **One pass function for every trigger.** The button, the Settings button, the dial, the CV paths, AI tuning, the restart finisher and the runner all call the same claim-then-run function; it sets the flag, advances the heartbeat after each chunk of 500, writes the stamp through `score_job`, and clears the flag and sets `scores_updated_at` after the last chunk.
- **The claim is a conditional UPDATE** (`rescore_pending` and no fresh heartbeat), so it holds across workers and processes; `_recomputing` in memory is no longer the guard.
- **The page shows the state, it never starts a pass.** Rendering the inbox only reads.

**Decisions made while drafting, to confirm at approval**
- **D1: old rows stay unstamped and count as out of date** (the honest reading: nobody knows what they were scored with). Cost: every power-mode candidate sees the line once after the deploy; a press stamps the rows. Rejected: stamping old rows "current" at migration (it would hide the owner's own case, 1,063 of 1,634 rows behind in the 29 Oct data); stamping them from a replay (reads every text).
- **D2: the dream-employer list is not in the hash**, because `dream.refresh` rewrites the bonus when the list changes (to be checked in the plan: if it does not reach every candidate's rows, it goes into the hash).
- **D3: two buttons, two scopes.** The inbox line scores only rows whose stamp differs (cheap, and it makes a redone pass resume where the killed one stopped). The Settings button and the `rescore` command score every row in scope, so a drift the hash cannot see (the similarity corpus, about 1.7 points in cycle 021) can still be cleared by hand.
- **D4: "interrupted" is a heartbeat older than 2 minutes**, not a process check, so it works across workers and restarts. A chunk of 500 jobs takes a few seconds, so 2 minutes has wide margin; the number is a constant to revisit if the host is slower.

**Options rejected**
- **A rescore at every save:** the owner chose the button (Q1).
- **Rescore synchronously for small inboxes:** the cold setup alone was 43 s locally against a 120 s request limit; one rule beats a size threshold.
- **`profile_version` as the signal:** it does not move on a keyword edit, and all 1,634 inbox rows of the owner carried the same version while 1,063 were behind.
- **A "dirty" flag set by each edit path:** it drifts when a new path is added (three paths today bypass any rescore); a stamp on the data cannot miss a path.
- **A timestamp on `Config`** compared with `Score.created_at`: needs every edit path to remember to set it, and a restart half way could not tell which rows are done.

## Interfaces and data
- **Data:** migration `0045` (the next free number on 2026-11-10; `0044` is cycle 033's invitation codes: take the next free one at build time): `Score.scored_with` (CharField, null), `Candidate.scores_updated_at`, `Candidate.rescore_heartbeat_at` (DateTimeField, null). `rescore_pending` exists.
- **Code:** `jobs/services/scoring.py` (the hash, the rules version constant, the stamp in `score_job`), `jobs/services/matching.py` (scope, claim, chunked pass with heartbeat, state, the count), `jobs/ai/onboarding.py` (`run_pending` clears at the end), `jobs/services/runner.py` (finish pending at each run), `jobs/views.py` (`inbox` context, `settings_view` rescore action, one new POST view), `jobs/urls.py` (one URL, name settled in the plan), `jobs/templates/jobs/inbox.html` and `settings.html`, a small partial for the line, the web start hook (mechanism chosen in the plan), `locale/fr`.
- **No** new environment variable, no setting, no change to how a score is computed.
- **Deploy:** the usual push (the owner's step) applies the migration through the entrypoint; the hosted migration is irreversible-class and goes only inside the approved plan, after the rehearsal in criterion 14.

## Constraints
- Neon's network allowance (5 GB a month, 0.49 GB used on 2026-11-05) is the scarce thing: the state and the count read no text; a pass reads each posting once; every measurement and the drill run on a scratch copy of the dump, never on the hosted database (`SAXOBEAT_HOSTED_DATABASE_URL` is not touched before criterion 18).
- Render web: 512 MB, one worker, 4 threads (DEPLOY.md); a pass runs in a thread of the web process: its peak memory is measured in the drill (criterion 13) before the host runs one.
- The tests run with `SAXOBEAT_MAIL=console DATABASE_URL=` (SQLite) and, for the final count, on the local Postgres (PROJECT.md). The suite already stubs `recompute_in_background`; the new tests exercise the real function with a synchronous runner, not a stub.
- Other sessions edit the same working tree: stage only this cycle's paths (and the README as HEAD plus the 029 row).

## Out of scope
- Starting a pass by itself after a save (owner, Q1).
- Changing how a score is computed, or the glossary and scale (cycle 021).
- Reading less text per rescore (a separate candidate), beyond skipping rows already stamped current.
- Rescoring candidates 3 and 4 on the host, and any use by standard mode.
- A progress bar with a percentage (the line says "Updating", with no count of done jobs).
- Reconsidering the keywords themselves, or showing which keyword edit made the scores stale.

## Risks
- **A hash that misses an input** would show "up to date" while scores differ. Mitigation: criterion 1 tests each input; criterion 13 checks the result against an independent replay; the Settings button and the command still score everything.
- **A false alarm after the deploy** (D1): every power-mode candidate sees the line once. Accepted, and said in the release note to the owner.
- **A pass on the web process during a deploy** is killed by it; that is what criteria 8 to 10 are for, and it is tested by a kill, not assumed.
- **The first host pass reads Neon** (about 16.6 MB plus the pipeline); said before, measured after.

## Gate
- [x] Owner approved this spec (2026-11-06, D1 to D4 as drafted)
