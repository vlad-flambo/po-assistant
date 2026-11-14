# Learn: check the hosted app after the 28 October deploys

| | |
|---|---|
| **Cycle** | 004 |
| **Stage** | Learn done 2026-10-29: cycle closed |
| **Verify** | [verify.md](verify.md), accepted by the owner 2026-10-29 |

## What happened vs what we expected
- **Success measure** (intent): every "not verified" claim about the hosted app is backed by evidence or turned into a fix. **Met:** 10 of 10 criteria pass, no fix needed, DEPLOY.md's "Not verified yet" (dated 23 October) is now "Verified on the host (2026-10-29)".
- **Expected** a possible wrong block from migration 0039 (the riskiest data change of the 28 October deploys). **Found** none; the owner found the blocking interface itself unintuitive instead (cycle 016).
- **Found** what we had not looked for: prod1's recovery is thin. Neon rewinds 6 hours, and no dump of prod1 exists while cycle 001 holds the backup back.
- **Cost:** about half an hour of the owner's time, one session for Claude; no read of the hosted database beyond page loads (cycle 001's measurements stayed clean).

## What we learned
- **The owner's eye was enough for most checks.** Modes, View as and speed were confirmed in a sentence each; asking for screenshots and a timings table was more than the owner needed. Speed is therefore judged, not timed: fine while nobody complains, worth a figure when cycle 005 tests real phones.
- **Record a deploy by its date, not only by its commit.** Render's Events list shows commit messages first; `d1718a0` was missed at a first look and recorded as not deployed, then withdrawn (F1). Asking for "the latest deploy's date and commit" avoids the false alarm.
- **A check cycle is where risks surface.** The 6-hour window was a single line in Neon's settings, but it changes what a mistake costs: until the monthly backup runs, a manual snapshot before any risky change is the safety net.

## What moves where
| Finding | Goes to | Done |
|---|---|---|
| What was verified on the host, and what still is not (e-mail, real phones, page times as figures) | `docs/DEPLOY.md`, "Verified on the host (2026-10-29)" | [x] |
| Neon restores 6 h plus manual snapshots; take a snapshot before risky changes | `docs/DEPLOY.md` (same section); the owner's action in `next.md` | [x] |
| No dump of prod1 until the backup runs (monthly since cycle 001's D3) | cycle 001 (it owns the backup); stated in DEPLOY.md | [x] |
| The blocking interface: an icon, the list on the Companies page | cycle 016, intent drafted | [x] |
| Page times as figures | cycle 005 (real devices) | [x] |
| The audit rows sent to 004 marked done | `cycles/006-stale-docs/evidence/prd_audit_2026-10-29.md` | [x] |
| Cycle 014's fixes are live (`d1718a0`, 15:53) | cycle 014's learn.md | [x] |

## Process feedback
- **Worked well:** a numbered checklist of the owner's steps with "where to click" and "send me"; the owner answered all seven in one message.
- **Slowed us down:** a finding (F1) recorded and committed before asking one more question. When evidence says something is missing, ask the owner to look once more before writing it down as a finding.

## Next cycle candidates
- None new beyond 016; 005 (real devices) picks up the page times.
