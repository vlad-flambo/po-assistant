# Intent: Cloud AI agent step

| | |
|---|---|
| **Cycle** | 027 |
| **Stage** | Intent |
| **Date** | 2026-11-05 |
| **Owner** | Vladimir Stoyanov |
| **Importance** | 3/5 (claude, 2026-11-05): 257 of 258 AI tasks came back done by hand-fed agent sessions; running them without the owner at the PC would remove the 24 h promise's dependence on the owner being available |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
Part of the 2026-11-05 request (full text in cycle 025): "I want to run everything on the cloud." The "everything" includes the AI step that today needs the owner's PC and an agent session.

## Why now / the pain
- The AI hand-off: `manage.py ai sync` writes pack files into a folder on the PC, **a person points an agent at the folder** (skill `saxobeat-ai-batch`), the agent writes results files, and `ai sync` imports them (DEPLOY.md "The AI folder on the PC"). The 24-hour promise to candidates therefore depends on the owner sitting at the PC.
- Eight packs ran this way between 23 and 28 October: 257 of 258 tasks came back done (DEPLOY.md, cycle 004).

## Goal
The AI packs are written, processed by an agent and imported without the owner at the PC, with a way to see what ran and to stop it.

## Success measure
1. A pack created on pre-prod is processed and imported by the cloud path alone, and the console shows it done.
2. The refused-result path (a bad results file held back whole) still works (the existing check).
3. Cost per pack and the model used are written down.

## Not doing (this cycle)
- Changing the pack format or the prompts.
- Candidates bringing their own keys.

## What we already know (facts, with where they came from)
- The files are self-contained, "any agent, no setup" (PRD_ai_backoffice.md §2 goal 4), so any agent that can read and write files, with database access through `ai sync`, can do the middle step.
- PRD_ai_backoffice.md §3 puts "the app calling an LLM API" and "running the agent automatically" **out of scope** (register item R3 in the backlog). The owner can change that; it is a product decision, not a technical one.
- Candidates' CVs travel in these files (contact details removed): moving the middle step to a cloud agent sends them to wherever it runs.
- Cloud options (unverified): a scheduled Claude Code routine (the `schedule` skill) that clones the repo, runs `ai sync`, processes the folder with the skill and imports; or a job calling the Anthropic API directly. Both need the database address as a secret in that environment.

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | Do you want to lift "the app never calls a model" / R3 for this? | Not the app: keep the app model-free and put the agent in a separate scheduled job (a routine), so the product rule stays true. | | open |
| 2 | Start after 026? | Yes: it needs the cloud runner's environment pattern (secrets, pre-prod rehearsal). Park until 025 and 026 reach verify. | | open |

## Constraints and risks
- Depends on 025 and 026. Subscription or API cost is the owner's to approve.
- Personal data leaving the PC: say so to the candidates if it changes what DEPLOY.md tells them.

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
