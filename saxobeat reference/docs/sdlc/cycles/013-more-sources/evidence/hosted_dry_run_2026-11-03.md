# The hosted dry run (2026-11-03, slices 12 and 21, step 2 of 3)

Run by Claude **at the owner's request** ("snapshot taken, do the dry run yourself"), after the owner took the Neon snapshot of prod1. Read only: `scripts/seed_hosted_sources.ps1 -Step all` (a listing and `seed_employers --dry-run`) and one further read of source names and on/off flags. Nothing was written; the address is never printed. (My standing rule was that only the owner touches the hosted database; this authorisation covers these reads, not the write.)

## What the hosted database holds
- **331 sources, 329 enabled** (the 29 Oct dump had 328 and 326: three were added since).
- **`seed_employers --only` for all 15 names (`-Step all`): `15 would be created, 0 already present`, all switched off.** None of the fifteen exists yet.
- No Accenture, Google or other Recruitee source: nothing wrong to switch off there. (The listing also showed `Morgan Stanley (workday)`: a false match of my search word "ey (" inside "Stanley (", unrelated.)

## The six sources to switch off (all present and **on**)
`Energy Pool (smartrecruiters)` id 178, `Esker (teamtailor)` 232, `EssilorLuxottica (smartrecruiters)` 196, `Publicis Groupe (smartrecruiters)` 217, `Trade Republic (greenhouse)` 53, `Uber (smartrecruiters)` 287. Why: [recheck_live_2026-11-03.md](recheck_live_2026-11-03.md).

## Confirmed already covered (present and on)
`Sopra Steria (smartrecruiters)` 242, `Wavestone (smartrecruiters)` 222, `Amundi (talentsoft)` 270, `Atos (successfactors)` 253 (Eviden), `Oliver Wyman (lever)` 93.

## Next
The write: `scripts\seed_hosted_sources.ps1 -Step all -Apply -SnapshotTaken` (adds the 15, all off, with the counts compared before and after), then the six switched off and the others enabled in batches after a by-hand runner pass each.
