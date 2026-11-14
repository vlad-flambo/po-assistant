# Learn: places and remote options in Settings for standard mode

| | |
|---|---|
| **Cycle** | 030 |
| **Stage** | Learn |

## What happened vs what we expected
- **The request changed shape twice.** It started as "ask which international destinations at onboarding" (Paris/IDF/HK/SG ticked individually, Paris/IDF by default, editable later like a power user). On the first read I found no yes/no "international" question in the code, only a "Where?" question that already lists every registry city; the owner then said the onboarding part was already done and narrowed it to *"just the editability of the cities to standard same as power mode"*, and on Q1 and Q3 widened it to the three remote options. What was built is the narrowed, widened version.
- **Success measure (intent.md, as confirmed):** all four met. (1) the card shows the four controls pre-ticked and saves them: yes, `verify.md` rows 1 and 2; (2) it touches nothing else: tested with every other filter at a non-default value; (3) the guided "Where?" question and the card agree in both directions: tested; (4) nothing ticked means no location limit and is not an error: tested and seen in the drill. 9 of 9 criteria pass; suite 1,610 before, 1,623 after.
- **Not met or not checked:** the owner's phone check and acceptance were given on 2026-11-06 (accepted at the Verify gate); the card was seen at 375 px in the in-app browser, not on Render. The cost of the background re-sort on a real-size inbox was not measured.
- **What it cost:** about a day of conversation, six slices, one visual fix (two labels clipped as pills on a phone), one wrong claim in my own intent (below).

## What we learned
- **The big Settings form saves every field at once**, so standard mode got a small card with its own action instead of some of the fields: the pattern for any future "one thing from the power settings, for standard mode" (cycle 016's blocked-employers list followed the same idea).
- **The places live in two stores.** `Config.filters["cities"]` (what the inbox filters on) and `Candidate.preferences["cities"]` (what the guided "Where?" question pre-ticks and what the onboarding agent reads). `conversation.set_places` now writes both; any other place that changes the cities must go through it, or the pages will disagree.
- **A plain Settings save re-sorts nothing.** I had written in the intent that the power save starts a background recompute; reading the view showed it only says "use the buttons below" (`views.py:1047`), and only the Search-breadth dial calls `recompute_in_background`. I corrected the record the same day. Standard mode has no apply buttons, so the card's save starts the recompute itself. That pass rescores every visible job and reads posting text: the cost is one press of the dial, per save.
- **"Remote only" and the remote cities have no guided-question equivalent**: only the Settings card sets them for a standard candidate.
- **Onboarding pre-ticks Paris only**, not Île-de-France (`views_cv.py:203`), and the "Where?" list shows London, which is not among the destinations the owner named as supported (Paris, Île-de-France, Hong Kong, Singapore). The owner chose not to touch either in this cycle.
- **A PowerShell trap:** `$env:DATABASE_URL=''` deletes the variable, so my first baseline test run tried the `.env` PostgreSQL (it failed on connection after about 9 minutes; nothing was written). Fixed in the notes below.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| Standard mode has a places card in Settings (what it saves, the route, the background re-sort) | `docs/PRD_users_and_emails.md` (the standard-mode note under "Out of scope / settled"), edited 2026-11-06 | [x] |
| Run the test suite from Git Bash; PowerShell's empty-variable assignment deletes the variable | `docs/sdlc/PROJECT.md` Tests row, edited 2026-11-06 | [x] |
| The same, with the new baseline (1,610 before, 1,623 after cycle 030) | Claude project memory `reference-running-tests`, edited 2026-11-06 | [x] |
| The same trap, for every project on this PC | house-stack `reference/gotchas.md`, added 2026-11-06 | [x] |
| Cycle 030 state | Claude project memory `project-sdlc-cycles`, updated 2026-11-06 | [x] |
| The live cycle board must be refreshed after every step that moves a cycle, not only `BOARD.md`: it was a day stale (last refreshed 5 Nov) when the owner asked | the ai-sdlc skill: have `sdlc_status.py --markdown` print "live board: refresh the datasets too" when `PROJECT.md` names a live board. Proposed to the owner, not edited: the skill is shared by every project | [ ] deferred 2026-11-06, owner's decision |
| A cheaper re-sort after a places change (score only the jobs that just became visible, not all) | next-cycle candidate below | [ ] deferred 2026-11-06, owner's decision |

## Process feedback
- **What worked:** writing the success measure and the spec as numbered, checkable criteria made `verify.md` mostly a matter of pointing at tests; the narrowing by the owner mid-way cost nothing because the intent was a file, not a chat. The drill on a scratch SQLite and a real click-through caught the clipped labels that no test would.
- **What slowed us down:** (1) I built the first reading of the request (an "international" question) from the owner's description before finding it was not in the code; one more look at the screen, or asking for a screenshot first, would have saved the first round. (2) I refreshed `BOARD.md` after each step but not the live board, so the live board lagged a day. (3) I wrote a claim about the recompute in the intent from the call site next to the line I read, not from the function; read the whole function before stating what a save does.
- **Gate handling:** "approved, build until you need me" worked well as a standing instruction for the plan stage; the owner's decisions (commit, push, acceptance) stayed with the owner.

## Next cycle candidates
- **Cheaper re-sort after a places change** (and after other filter changes): score only the jobs that just became visible. Reach: every candidate who saves a place; the cost is per save and grows with the inbox (cycle 029 measured about 16.6 MB read for about 3,000 jobs).
- **Align onboarding with the supported destinations:** pre-tick Île-de-France with Paris, and decide whether London stays in the "Where?" list (today it does; the owner named only Paris, Île-de-France, Hong Kong, Singapore). The original request asked for both; the owner set them aside here.
- **Make the live board refresh automatic** (skill improvement above).
