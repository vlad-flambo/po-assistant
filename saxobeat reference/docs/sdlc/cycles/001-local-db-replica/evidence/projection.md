# Projection of Neon transfer per month (the web app's own rate `W` is still missing)

Status 2026-10-29 night: every runner input is measured, and the model changed twice today (see "What changed" at the end). The owner's pattern is **3 to 5 runner runs a week, that is 13 to 22 a month**.
The target is **under 2.5 GB a month; with a 20 % margin that is 2,000 MB or less in total, counting `W`**. `W` (the web app's reads on prod1) comes from cycle 002's reading (2026-10-30) and every total below **excludes it**: "room for W" says how much each scenario leaves.

## Measured inputs (MB = 10^6 bytes; raw lines in [measurements.jsonl](measurements.jsonl); the profile in [source_pass_profile.md](source_pass_profile.md))
| Input | MB | How |
|---|---:|---|
| A source pass (`run_sources --all`): mean of 58.8 (cold) and 64.5 (warm) | 61.6 | measured, two passes. The runner's own step takes only the sources **due**, so this is the conservative end |
| `ai sync`, steady state (cache warm, nothing pending) | **0.1** | measured: 0.09 MB on a second run. The 32.2 MB recorded earlier is a cold-cache, first-file cost |
| `ai sync` building an onboarding or analysis file | about 13 each, rare | measured inside the first run: loads 1,634 views with their texts |
| `mail send`, with or without a digest due | 1.1 to 1.2 | measured (the 129 MB a month digest guess is **dropped**) |
| **A run, by hand, in steady state** = source pass + `ai sync` + mail | **about 63** | sum (was 94.9) |
| A full backup | 227.0 | measured, two runs |
| One standard-mode inbox page of the web app | 1.1 before, **0.15 after** | measured on the scratch copy (part of `W`) |

## Reductions built and measured
| | What | Effect | Status |
|---|---|---:|---|
| R2a | The link lookup in `ingest` reads only the columns a run uses | **-16.5 MB a run** (the lookup -80 %: 708,856 to 143,222 bytes on 10 sources; 35.2 to 8.5 MB over all links) | **built, tested, awaiting review** |
| R2b | The ranking pool (`selection.waiting`) no longer loads job texts | **-0.96 MB per standard-mode inbox page view** (1.11 to 0.15 MB); the digest and the console use it too | **built, tested, awaiting review** |
| R2c, R2d | Corpus recounted in full every 30 days, not 7 (about -50 MB a month); candidates and configs once per run (about -10 MB a run) | estimates | **not built, not needed** at these numbers |
| R3 | A read-through cache of job texts | | **not needed** |

## Scenarios, in MB per month: runner and monthly backup, before the web app
Run cost x runs + 227 (backup). "Room for W" = 2,000 minus the total.

| Runs a month | No reduction (63 a run) | With R2a (46.4 a run) |
|---|---:|---:|
| **13** (3 a week) | 1,045 (room 955) | **830 (room 1,170)** |
| **22** (5 a week) | 1,611 (room 389) | **1,248 (room 752)** |

- **The runner now fits at both ends of the owner's pattern**, with or without R2a; R2a widens the room by about 215 MB (13 runs) to 360 MB (22 runs).
- **How much `W` can be** under the target: about 1,170 MB at 3 runs a week, about 750 MB at 5 runs a week (both with R2a).
- With R2a, **a backup every two weeks** (454 MB a month) would also fit: 13 runs about 1,057 MB, 22 runs about 1,475 MB, before `W`. A weekly backup (908 MB) fits at 3 runs a week (about 1,511 MB, room 489) and barely at 5 (about 1,929 MB, room 71). D3 (monthly) stands; this only says the owner could relax it.
- Neon does not know about the PC's habits: the figures assume the runner keeps its cache in `data\cache` between runs (it does, `pc_runner.ps1`). A run after the cache was deleted pays about 17 MB once.

## First observation of `W` (2026-10-30, from cycle 002's reading)
Sum of all projects 4.89 GB, old project still 95.1 %: **prod1 used about 135 MB (±10) in roughly one day of web use, no runner.** That day held the cycle 004 checks, so it is probably above a normal day, but if it were typical it would be about 4 GB a month: **more than the whole target**, so it is not a safe assumption either way. The standard-inbox fix (1.1 to 0.15 MB a page) is not deployed yet. `W` is now the only input that can change the verdict.

## What is still unknown, and who answers it
1. **`W` over more days**: the owner's daily reading (sum with two decimals, old project's percentage, the time), from now until the push, then after it (slice 9). Until then the verdict stays open: runner 830 to 1,250 MB plus a `W` somewhere between about 0.5 and 4 GB a month.
2. About 10 MB of a full source pass is still not attributed (see the profile); it does not change a decision.
3. Whether the real runner's step (due sources only) costs less than the `--all` pass measured: very likely, not measured.

## What changed in the model today (for the learn stage)
- A guess of 129 MB a month for digests was wrong: a due digest costs 0.1 MB.
- `ai sync` at 32.2 MB a run was wrong as a steady-state figure: it was a first run (cold cache plus one onboarding file). The steady state is 0.1 MB.
- The "38 MB of a pass unexplained" was the sum of many small repeated reads, mostly the link lookup (69 % of a source's own reads).
- The first measurement of `W`'s kind: a standard inbox page cost 1.1 MB, because it loaded the whole ranking pool with job texts. Fixed (R2b).
