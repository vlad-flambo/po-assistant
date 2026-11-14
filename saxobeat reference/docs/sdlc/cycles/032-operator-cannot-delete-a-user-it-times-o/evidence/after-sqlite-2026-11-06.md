# After the change, SQLite (temporary file), 2026-11-06 (claude)

Same script and same accounts as `baseline-2026-11-06.md`; new `accounts.delete_account` (one DELETE per table, children first).

| Account | Before | After | Result |
|---|---|---|---|
| 36,271 views, 0 private jobs | 40.9 s, 72,945 statements | **0.6 s, 33 statements** | all of theirs gone; 36,271 shared jobs, the other person's 1,000 views and user kept |
| 36,271 views + 5,000 private jobs | 47.3 s, 83,056 statements | **0.8 s, 43 statements** | same, and the 5,000 private jobs gone |

Limits of the spec (under 10 s, under 50 statements): met in both. The statement count does not grow with the size (`test_the_number_of_statements_does_not_grow_with_the_size_of_the_account` pins it at 80 for 300 views in the suite).

A first version of the rewrite kept Django's `candidate.delete()` for the last step; it ran the collector's existence checks on 15 empty tables (43 statements, and 53 with private jobs: over the limit). Replaced by one raw DELETE after an UPDATE that frees the approved sources the person proposed.
