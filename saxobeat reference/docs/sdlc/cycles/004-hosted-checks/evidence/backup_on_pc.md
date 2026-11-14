# The newest backup on the PC (slice 8)

Listed by Claude on 2026-10-29 from `data/backups/` (local folder, gitignored):

| File | Size | Made |
|---|---|---|
| `saxobeat_2026-10-29_100546.dump` | 65.4 MB | 2026-10-29 10:06 (the dump of the old project taken for cycle 002's move) |
| `saxobeat_2026-10-28_122846.dump` | 65.3 MB | 2026-10-28 12:29 |
| `saxobeat_2026-10-28_120609.dump` | 56.9 MB | 2026-10-28 12:06 |

~~The weekly backup step (`backup_database --min-age-hours 168`) will next make one on or after 2026-11-05, when the runner runs.~~ *(Superseded by cycle 001's D3, 2026-10-30: the step is now `--min-age-hours 720 --keep 6`, so the next one is due 30 days after the newest file on the PC, that is on or after 2026-11-28 for the 29 Oct dump, when the runner runs.)* Note: until cycle 001's measurements allow it, the runner's backup step is not run against the hosted database (project memory), so the newest dump of **prod1** itself does not exist yet; the 10:06 dump is the old project's, from which prod1 was restored.
