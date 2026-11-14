# Next: reposted after applied

Each line is one action: `- [ ] [owner|claude|both] <date, optional> text`. Tick it when it is done, add new ones as the cycle moves. This file is what the cycle board shows as "what next?".

- [x] [owner] Say your request in your own words (it goes in intent.md, unedited)
- [x] [claude] Gather the facts (code, docs, files), draft the open questions in intent.md
- [x] [owner] Answer question 1: link with a banner (2026-11-04); question 2 answered by Claude's read of the host pages
- [x] [owner] Answer question 3: banner on the repost's page, tag on its inbox row, pointer on the older job (2026-11-04)
- [x] [owner] Questions 4 and 5 accepted as recommended (2026-11-04)
- [x] [owner] Goal and success measure confirmed (2026-11-04); Intent gate closed
- [x] [claude] Draft spec.md (13 acceptance criteria)
- [x] [owner] Spec approved (2026-11-04)
- [x] [claude] Draft plan.md (10 slices)
- [x] [owner] Plan approved (2026-11-04)
- [x] [claude] Build slices 1 to 8 done (54 tests, suite 1,606 pass, look at 375 px); D1 added a phone-card chip
- [x] [owner] Commit allowed (2026-11-04)
- [x] [claude] Committed `0455313` (this cycle's paths only; README staged as HEAD plus the 022 row, the other sessions' README edits left in the working tree)
- [x] [owner] Pushed `0455313`; Render deployed it (2026-11-04)
- [x] [claude] Read 36143 and 31673 on the host (banner and pointer as expected); found that the filter hung the host; fixed (D2), suite 1,610 pass
- [x] [owner] Commit of the filter fix allowed (2026-11-05); committed `13a60ae` (README staged as HEAD plus the 022 row; BOARD.md left out because it now lists other sessions' uncommitted cycles)
- [x] [owner] Pushed `13a60ae` (the owner's word, 2026-11-10; I did not read Render's Events page to confirm that the deploy is Live)
- [ ] [owner] Sign in on app.saxobeat.fr in the browser pane (I never type passwords: the pane was reopened signed out on 2026-11-10)
- [ ] [claude] After the sign-in: read the host once for criteria 12 and 14: `/job/36143/` (banner), `/job/31673/` (pointer), `/` (header, row count, how long it took) and then `/?reapplied=hide` as ONE request with a 30-second limit and the time said. If it answers in about a second the fix is live; if it hangs, stop at once and tell the owner (the first design took the host down). Save the readings in `evidence/host_read_<date>.md`, update verify.md rows 12 and 14, then ask for the verdict
- [ ] [claude] Draft learn.md after the verdict: PRD_mobile.md (the "already applied" first chip on a card), the process rule (time any query over a candidate's whole list of views on the local copy before a push), decisions D1 and D2

## Pick up here (written 2026-11-10 for the move to another computer)
- **Code is finished and pushed:** `0455313` (banner, pointer, tag, phone chip, filter) and `13a60ae` (the filter rewritten after it hung the host). Suite 1,610 pass on SQLite; the new queries have never run on a Postgres test run, only on the 57k-view local copy and on the host.
- **Open: criteria 12 and 14 on the host** (verify.md, "partial"). Everything else passes. The host read needs the owner signed in.
- **Do not** request `/?reapplied=hide` on the host before the fix is known to be live; check Render's Events page for the deploy of `13a60ae` first.
- **Files that matter:** `spec.md` (14 criteria), `decisions.md` (D1 phone chip, D2 filter rewrite), `evidence/host_read_2026-11-04.md` (the first read and the hang), `evidence/look_2026-11-04.md` (375 px look), `tests/test_repost_applied.py` (56 tests), `jobs/services/employer_history.py`.
- **Scratch things on the Windows PC only (not in git, not needed):** the throwaway SQLite look database and scripts in the scratchpad.
