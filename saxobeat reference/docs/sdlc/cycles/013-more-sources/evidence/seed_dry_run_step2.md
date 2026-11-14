# Step 2's seed, rehearsed on a fresh scratch copy (2026-11-03, slice 19)

A fresh restore of the newest dump (328 sources, 31,968 jobs), migrated to the current schema (0041 to 0043, scratch only). Local Postgres only; the hosted database is untouched.

## What changed
`scripts/seed_hosted_sources.ps1` has `-Step 1` (the default: the ten sources of step 1, as before), `-Step 2` (the five consulting sources: Boston Consulting Group, EY, Onepoint, PwC, PwC Campus) and `-Step all` (fifteen). The listing of existing sources now also looks for the consulting names.

## The rehearsal
| Step | Result |
|---|---|
| Existing sources | 328 (326 on); checksum of id, name, type, config, on/off, interval and status `d085b0d2d0c218eb976d4127cc338850` (the same as step 1's rehearsal on the same dump) |
| Dry run `-Step 1`, `-Step 2`, `-Step all` | `10`, `5` and `15 would be created, 0 already present. Nothing was written.` All switched **off**; sources still 328 and the checksum unchanged |
| `-Step 2 -Apply` without `-SnapshotTaken` | refuses ("needs -SnapshotTaken"); rows stay 328 |
| `-Step 2 -Apply -SnapshotTaken` | `5 sources added`; counts compared: **1 difference, `jobs_source: 328 vs 333`**; re-run `0 sources added, 5 already present`; still 326 on |
| Existing sources after | the checksum of the 328 is unchanged; the five new ones are ids 337 to 341, all off |

## The owner's commands (slice 21, after the Neon snapshot; slice 12's step 1 can come first or together with `-Step all`)
First the dry run, read what it lists:

```
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\seed_hosted_sources.ps1 -Step 2
```

Then the write, only after the snapshot of prod1 exists:

```
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\seed_hosted_sources.ps1 -Step 2 -Apply -SnapshotTaken
```

(Replace `-Step 2` with `-Step all` to do both steps in one go.)

## Not done here
The lists in `data/` (S2.8) wait for the sources to exist on the hosted database.
