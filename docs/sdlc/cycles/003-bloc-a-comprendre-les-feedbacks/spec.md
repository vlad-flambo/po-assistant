# Spec: bloc A comprendre les feedbacks

| | |
|---|---|
| **Cycle** | 003 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |
| **Date** | 2026-11-16 |

> Documentation allégée (décision Q7 du cycle 002, Vlad, 2026-11-16) : intent et spec réunis, l'échéance étant le soir même. Conception détaillée : `README.md` et `docs/demarche.md`.

## Acceptance criteria
1. [x] Chaque feedback est classé (type, 1 à 3 thèmes, sentiment, risque de churn) et ses demandes sont extraites avec une citation exacte et une cible (issue ou `NEW:<slug>`).
2. [x] Les besoins sont agrégés par le code : clients distincts, portée (sièges Business), ARR à risque, tendance sur 4 semaines, citations.
3. [x] Les thèmes ont une série hebdomadaire et une tendance.
4. [x] Alertes : risques de départ triés par ARR, demandes déjà livrées ou refusées, questions de relance pour les feedbacks vagues.
5. [x] La qualité est mesurée contre la vérité terrain (`python -m po_assist.evaluate`).

## Gate
- [x] Owner approved this spec (approbation préalable : lot Q1 à Q7 du cycle 002, « Je valide, go », Vlad, 2026-11-16)
