# The seed, rehearsed on the scratch copy (2026-10-30, slice 10)

Scratch database: a fresh restore of the 29 Oct dump (`measure_20261030174304`: 328 sources, 31,968 jobs), local Postgres only. The two trial sources of slices 7 and 8 were dropped with the old scratch database, so this started clean.

## What was added to the command
`manage.py seed_employers` now has `--dry-run` (lists what would be created, writes nothing) and `--only NAME` (repeatable; a name that is not in the list is refused before anything is written). Reason for `--only`: a plain `seed_employers` on the hosted database would also **re-create every ORIGINAL starter source that has been deleted there since, switched on**. 5 tests in `tests/test_seed_dry_run.py` (dry run writes nothing; after seeding everything is "present"; seeding twice adds nothing and an owner-edited source keeps its edits; `--only`; an unknown name is refused).

## The rehearsal
| Step | Result |
|---|---|
| Existing sources before | 328 (326 on), max id 336; checksum of their id, name, type, config, on/off, interval and status `d085b0d2d0c218eb976d4127cc338850` |
| `seed_employers --dry-run` (twice) | `10 would be created, 26 already present. Nothing was written.` (all 10 are switched **off**); sources still 328, checksum unchanged |
| `seed_employers` (real) | `10 sources added, 26 already present.` |
| `seed_employers` again | `0 sources added, 36 already present.` |
| After | 338 sources, still 326 on; **the checksum of the 328 existing sources is unchanged**; the 10 new are ids 337 to 346 |
| Script `scripts/seed_hosted_sources.ps1`, tested on this copy through `-UrlVar` | dry run by default (lists the existing sources that match these employers, then the dry run); `-Apply` alone refuses ("needs -SnapshotTaken"), rows stay 328; `-Apply -SnapshotTaken` saved the counts, added 10, compared: **1 difference, `jobs_source: 328 vs 338`**, and the re-run added 0 |

## Finding on the way: Amundi was a duplicate
The first dry run said 10 would be created, not 11: `Amundi (talentsoft)` already exists in the 29 Oct database, enabled, same address (`jobs.amundi.com`), last run 2026-10-28, 147 jobs stored. The list's entry was "Amundi (Amundi Technology)", so the earlier "unknown" was a naming gap, and slice 9's 8th source was redundant. **Its seed entry is removed; the count is now 7 new priority-A sources + Saegus, Capgemini, Accenture = 10.** I then checked the other employers for any source under another name or type (name or config): none. Existing jobs of the new employers already in the catalogue through aggregators: Accenture 38, Capgemini 16, Checkout.com 6, Saegus 2: they will merge with the new sources' jobs (a job can have several sources).

## The "switch off" list
In the 29 Oct copy there is **nothing to switch off**: no Accenture, Google or Google Cloud Recruitee source exists (slice 1). The hosted database may differ (sources added since 29 Oct): the script's first section lists every source whose name or config mentions one of these employers, so the owner sees it before anything is written. If an `Accenture (recruitee)` source (or another wrong board from the slice 4 review) is there, it is switched off on the Sources page (`enabled` off, not deleted).

## Not done here
The lists in `data/` are not corrected yet (criterion 12): the corrections wait for the owner's review (slice 4, 5), and "covered" must only be written once the sources exist in the hosted database (after slice 12). The hosted database is untouched.

## The owner's commands (slice 12, after the Neon snapshot)
First the dry run: read what it lists; nothing is written.

```
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\seed_hosted_sources.ps1
```

Then the write, only after the snapshot of prod1 exists:

```
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\seed_hosted_sources.ps1 -Apply -SnapshotTaken
```
