# Intent: socle agent et faux connecteur Linear

| | |
|---|---|
| **Cycle** | 002 |
| **Stage** | Intent |
| **Date** | 2026-11-14 |
| **Owner** | Vlad |
| **Importance** | 5/5 (claude, 2026-11-14): rien ne fonctionne sans : client LLM, schemas, acces SQLite facon Linear, tests |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
> Cycle issu de l'analyse initiale (`docs/analyse/01-analyse-initiale.md`, WBS §6), validée par Vlad le 2026-11-14. Intent à approfondir quand le cycle démarre.

## Why now / the pain
Dépend du cycle 001 (schéma de la base).

## Goal
Un socle Python testé : client Claude avec sorties structurées, couche « connecteur Linear » qui lit et écrit la base SQLite du cycle 001, et une suite de tests qui tourne sans clé API (LLM simulé).

## Success measure
<how we will know, measurable: a number, a drill that passes, a behaviour>

## Not doing (this cycle)
-

## What we already know (facts, with where they came from)
-

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
-

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
