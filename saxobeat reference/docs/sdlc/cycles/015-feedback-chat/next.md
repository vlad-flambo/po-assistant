# Next: cycle 015

Each line is one action: `- [ ] [owner|claude|both] <date, optional> text`. Tick it when it is done, add new ones as the cycle moves. This file is what the cycle board shows as "what next?".

- [x] [owner] Answer Q1 to Q11 in intent.md (done 2026-10-29; Q7 parked)
- [x] [owner] Approve the intent, the spec and the plan (2026-10-29)
- [x] [claude] Slices 1 to 5: baselines, model and script, the two endpoints, the button and sheet, the console page (committed: f8d4141, c07e2b6, dd863f7, 623f710)
- [x] [claude] Slice 6: the French pass (5 tests, the 70 sentences listed for reading) (2026-10-30; committed as 449aad9)
- [x] [claude] Slice 7: the person's own export and the restore carry their feedback (9 tests; committed as 449aad9)
- [x] [claude] Slice 8, my part: 1,264 tests pass on SQLite and on Postgres, no outside calls found, the migration's SQL on Postgres, the diff written for review (committed as 449aad9)
- [x] [owner] French wording: "i trust you" (2026-10-30): not read by the owner, recorded as an accepted risk
- [x] [owner] Read the diff, `evidence/code_diff_for_review.patch` (about 740 lines of app code and 860 of tests; the weight is in `jobs/feedback.py`, `views_feedback.py`, `_feedback_sheet.html`, `backup.py`), and say OK to commit slices 6 and 7 ("OK, commit", 2026-10-30; the go to slice 9 is still to be said)
- [ ] [owner] Look at the screenshots in `evidence/screens/` (the button, the chat in English and French, the console page) and say if the look and the place are right
- [ ] [owner] **Before any push of `main` for another cycle:** slices 1 to 5 are already committed on `main`, so pushing it ships the feedback button and migration 0041 to everyone (another session's note says the same). Tell me first if you would rather hold the push until slice 9, or I can move cycle 015's commits to a branch
- [x] [claude] Slice 9 prepared (2026-10-30): the hosted database read once (no `jobs_feedback`, 58 migrations), the runbook in `evidence/slice9_runbook.md`, the admin registration to delete a test chat (uncommitted)
- [x] [owner] "commit the admin" (8acf7f8)
- [x] [owner] Decided to ship with cycle 001's runner-side code; Neon snapshot of prod1 taken (2026-10-30)
- [x] [claude] Slice 9: pushed (d1718a0..8acf7f8); the host serves the new version; counts after: jobs_feedback 0 rows, migrations 58 to 59, no table shrank
- [x] [owner] Test chat sent on the real site and marked read on the console (the row exists: id 1, kind problem, 2026-10-30 09:57 UTC)
- [x] [owner] Test chat deleted in the admin (counts after: jobs_feedback 0, admin log 1 deletion; criterion 15 met)
- [x] [owner] Criterion 11: "yes worked" (2026-10-30)
- [x] [owner] Decided: add a Delete button to the console's Feedback page (2026-10-30)
- [x] [claude] Delete button built (criterion 18; 1,270 tests pass; not committed, not pushed)
- [x] [owner] Commit and push of the Delete button (a18ca9b, pushed 2026-10-30; the route is live on the host)
- [x] [owner] Phone test chat (id 2) deleted with the new Delete button (counts after: jobs_feedback 0; criterion 18 met on the host)
- [x] [owner] Slice 10: "tested on phone" (2026-10-30), no details given
- [x] [owner] Criterion 13: "yes, no issue seen" (2026-10-30)
- [ ] [owner] Decide whether to fix the existing sheets that open top-left on wide screens (a one-line CSS change in `dialog.sheet`, outside this cycle)
- [ ] [owner] Read the People page and tell me how many people use the app (fills the "unknown" fact; not blocking)
- [x] [claude] Commit slices 6 and 7 (449aad9, not pushed)
- [x] [claude] verify.md drafted (2026-10-30): 15 of 18 pass, 3 open (11 the paste, 13 the phone keyboard and layout, 17 real use); not committed
- [ ] [owner] Slice 11: tell the friends about the round button once; about two weeks later we read the console: at least 5 chats from at least 3 friends (the owner's own tests are deleted, so they will not count)
- [x] [owner] Verify accepted (2026-10-30)
- [ ] [owner] Slice 11: send the friends the invitation with the instructions, and tell me the date it went out; the two-week count (5 chats from 3 friends) is read 14 days after, on the console
- [ ] [claude] Read the console at the two-week date (counts and fields only unless the owner asks for the text), draft learn.md with the success measure compared, and propose the cycles the feedback suggests
