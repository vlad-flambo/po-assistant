# Spec: bloc B arbitrer la priorisation

| | |
|---|---|
| **Cycle** | 004 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |
| **Date** | 2026-11-16 |

> Documentation allégée (décision Q7 du cycle 002, Vlad, 2026-11-16) : intent et spec réunis, l'échéance étant le soir même. Conception détaillée : `README.md` et `docs/demarche.md`.

## Acceptance criteria
1. [x] L'agent estime Impact, Confiance, Effort (Fibonacci), MoSCoW et l'OKR servi, avec une justification sourcée.
2. [x] Le code calcule Reach (personnes ou clients), RICE et un score pondéré dont le PO règle les poids.
3. [x] Le PO peut corriger chaque estimation ; scores et plan se recalculent.
4. [x] Proposition de sprint dans la capacité restante (capacité moins le reste à faire des issues en cours), Must d'abord.

## Gate
- [x] Owner approved this spec (approbation préalable : lot Q1 à Q7 du cycle 002, « Je valide, go », Vlad, 2026-11-16)
