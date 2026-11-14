# Next: cycle 001

Each line is one action: `- [ ] [owner|claude|both] <date, optional> text`. Tick it when it is done, add new ones as the cycle moves.

- [x] [owner] Review plan.md and approve or change the slices
- [x] [claude] Slices 1 to 3: the guarded measurement script, the bytes of every runner step, the restore drill
- [x] [owner] Say yes to slice 4 (real-site fetches into the scratch database only)
- [x] [claude] Slice 4: two full source passes measured (about 60 MB each, whether 930 or 48 postings are new)
- [x] [owner] Your pattern: 3 to 5 runner runs a week (13 to 22 a month)
- [x] [claude] Table sizes and the link lookup measured: raw is only 8.9 MB; the slim lookup saves about 16.5 MB per pass
- [x] [owner] Backup cadence: monthly (D3). Applied in `pc_runner.ps1`: 227 MB a month instead of 908
- [x] [claude] The source pass profiled by SQL statement and a due digest measured: the corpus word counts are 94 % of a cold sample, links 69 % of a source's own reads, a digest costs 0.1 MB
- [x] [claude] Slice 7a built: the slim link lookup (-80 % on the lookup), test added, old and new code replayed on the same postings
- [x] [claude] Slice 7b built: the web inbox no longer reads the ranking pool's job texts (1.1 MB to 0.15 MB a standard-mode page view); `ai sync` measured at 0.1 MB in steady state; 1,249 tests pass
- [x] [owner] Review the two diffs (`jobs/services/ingest.py` with `tests/test_phase15.py`; `jobs/ai/selection.py` with `tests/test_ai_engine.py`) and say "commit it" or what to change; read the finding on two links to one job in [evidence/source_pass_profile.md](evidence/source_pass_profile.md) section 2
- [x] [owner] Confirm D5: keep the two small reductions, build nothing more until `W` is read (confirmed 2026-10-30)
- [x] [both] 2026-10-30 First reading: prod1 used about 135 MB in about one day (atypical: cycle 004 checks); see evidence/projection.md
- [x] [owner] 2026-10-30 Pushed (local main equals origin/main, last commit 10:41): the two read reductions are on GitHub; Render shows `8acf7f8` deployed (auto-deploy, 44.9 s, "8m ago" when the owner pasted it at about 11:02 local), so both reductions are live from then
- [x] [owner] 2026-10-30 First run done (about 11:45 to 12:21, no stop rule hit on the log; see evidence/first_run_prod1_2026-10-30.md)
- [x] [owner] 2026-10-30 Reading after the first run: 4.97 GB at 14:12 (about 80 MB since the morning's 4.89, inside the expected 60 to 90 MB and far under the 0.20 GB rule)
- [ ] [owner] Daily from 2026-11-04 (first reading: 0.31 GB at 10:17): read the sum (two decimals) and the time, and add one line: how many runner runs since the last reading and anything unusual (a profile or keyword change, the console's AI export or import pages). Seven days of that closes criterion 9
- [x] [owner] Pushed `main` on 2 Nov (the Insights fix, 37 MB to 5 MB a page view, is on GitHub; `origin/main` was at `bbcf82e` on 4 Nov)
- [ ] [owner] Optional: in Neon, look for a usage graph or billing history that still shows 31 Oct and 1 Nov per project
- [x] [claude] verify.md drafted 2026-10-30: 9 of 11 criteria pass, 4 and 9 wait for `W`, 5 holds on them
- [ ] [claude] Finish slice 5 with `W`: the final projection, then verify (criteria 1 to 11) and, after the push and a week of readings (slice 9), close
- [x] [claude] Cycle 004's spec (criterion 8) and `backup_on_pc.md` now say monthly, with a note that D3 changed it
- [ ] [owner] Standing rule: do not run the runner, `ai sync` or a backup against the hosted database until the plan says how
