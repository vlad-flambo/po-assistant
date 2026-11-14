# Rehearsal on a scratch Postgres copy (plan slice 7)

Run on **2026-11-03** against the scratch database `measure_20261103124053`, restored from `data/backups/saxobeat_2026-10-29_100546.dump` (the dump is at migration 0040; the old scratch copy `measure_20261103112421` of slice 1 had been dropped meanwhile, probably by another session's `measure_reads.ps1 -Clean`, so slice 1's count was re-run here). Local Postgres only; the hosted addresses, the mail key and the cache and AI folders were set to harmless values for every command (`SAXOBEAT_MAIL=console`). Nothing hosted was touched.

| # | Step | Result |
|---|------|--------|
| 1 | `manage.py migrate` (applies 0041, 0042, 0043) | OK, 32 KB sent |
| 2 | State before | 0 flagged, 60 Applied, 46 Rejected, 17,001 history lines, no settings row |
| 3 | Independent SQL count of the rule (`status='applied'`, `status_changed_at < now() - 30 days`, no focus, no interview) | **17** |
| 4 | `auto_reject --dry-run` | "would move 17 to Rejected", "Nothing was written"; 13.6 KB sent; afterwards 0 flagged, 46 Rejected, 17,001 history lines (only the one settings row was created) |
| 5 | `auto_reject` (the real sweep) | "moved 17 to Rejected"; 14.5 KB sent |
| 6 | After the sweep, by SQL | 17 flagged; 63 Rejected (46 + 17); 43 Applied (60 - 17); of the 17 flagged: all Rejected, all with `follow_up_at` cleared, all with `status_changed_at = auto_rejected_at` |
| 7 | History lines written | 17 lines, note "auto: no answer after 30 days", applied to rejected (17,001 to 17,018) |
| 8 | Any flagged row with an interview or focus | 0 |
| 9 | Second sweep | "moved 0"; 1.7 KB sent; history lines still 17,018; flagged still 17 |
| 10 | One job put back through the app code (`set_status(APPLIED, note=PUT_BACK_NOTE)`) | Applied, flag cleared, follow-up date set again; a sweep right after moves nothing (`{}`); 16 flagged left |

**The three numbers agree:** independent SQL count 17 = dry run 17 = real sweep 17 (criterion 15). The dry run at the beginning of slice 3 on the first scratch copy also said 17.

**Cost (criterion 16):** the sweep sent 14.5 KB from the database, the second sweep 1.7 KB, the dry run 13.6 KB (measured as the bytes the Postgres container sends, `/proc/net/dev` before and after, as in cycle 001; an idle second moved 0 bytes). For comparison a source pass reads about 60 MB. No job text is read (a test asserts `description_text` never appears in the sweep's SQL); the sweep is 7 SQL statements for a small batch.

**Postgres-only bugs:** none found (the migration and the sweep ran as written; the new tests also pass on Postgres).

## Not verified here
- The hosted database (prod1) is newer than this dump: its real count comes from slice 10's dry run.
- Reading on Neon's dashboard (the container counter is a proxy for what Neon counts as transfer, as in cycle 001).
