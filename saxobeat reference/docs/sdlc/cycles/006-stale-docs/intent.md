# Intent: bring the PRDs and DEPLOY.md up to date

| | |
|---|---|
| **Cycle** | 006 |
| **Stage** | Intent (drafted, nothing approved) |
| **Date** | 2026-10-29 |
| **Owner** | Vlad |
| **Born from** | The PRD audit of 2026-10-29: outstanding items moved here from the PRDs (see the table below). |
| **Importance** | 2/5 (claude, 2026-10-30): stale docs mislead readers and agents; no effect on users |

## The request, in your words
> Do a full audit of the PRD files. I want to migrate anything outstandin into the ai sdlc framework, using the ai-sdlc skill

### What this cycle inherits from the PRDs
| Item | Where it came from |
|---|---|
| PRD.md: 'Render deployment not done', 'Render Postgres', 'Task Scheduler', the rerun round, the source lists (Allianz/Phenom listed as unusable), '24 sources', LLM budget settings | PRD.md §3, §5, §6.4, §6.5, §7-§9, §11 M4 |
| PRD_competitive_features.md: 'Next: deploy to Render', 'Nothing sends an email', F13's 'Not done' line, breadth stored in filters | header, §6, §8, F13 |
| PRD_mobile.md: 'no `<table>`' test vs the stack tables, 'Waking up / free tier sleeps' | §9, §11, §15 |
| PRD_multi_user.md: status 'rien n'est encore déployé', hosting choice (Render Postgres vs Neon) | en-tête, §5, §6 |
| PRD_ai_backoffice.md: 'Not yet run on the hosted app' (depends on cycle 004) | status line |
| DEPLOY.md: 'Not verified yet' dated 23 October | DEPLOY.md, end |

## Why now / the pain
Six PRDs and DEPLOY.md say things the code and the hosting no longer do; a reader (or an agent) starting from them is misled.

## Goal
Every statement the audit found stale is either corrected or clearly marked as history, and each PRD says where its open work now lives.

## Success measure
Every row of the audit's stale list is ticked in `verify.md` with the line that fixed it; a grep for the stale phrases finds none outside history notes. *(draft, to confirm)*

## Not doing (this cycle)
- Rewriting the PRDs.
- Changing code.

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| The audit list of stale statements (14 in PRD.md, 13 in the competitive PRD, 11 in the mobile PRD, plus the others above) | PRD audit 2026-10-29 (this cycle's evidence) |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Fix in place, or add a dated status note? | A dated 'Status on <date>' note at the top of each PRD, plus in-place fixes only where a sentence would mislead | | open |
| Q2 | Mark old numbers (test counts, CSS sizes) as history or remove them? | Leave them: they are dated history and harmless | | open |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Wait for cycle 004 for the statements that need a hosted check.

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
