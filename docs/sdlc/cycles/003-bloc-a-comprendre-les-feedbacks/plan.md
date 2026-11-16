# Plan: bloc A comprendre les feedbacks

| | |
|---|---|
| **Cycle** | 003 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

> **Plan reconstitué après coup** (2026-11-16, à la demande de Vlad) : avec la documentation allégée décidée en Q7 du cycle 002, la construction a été menée sans `plan.md` préalable. Ce fichier retrace les tranches réellement exécutées, à partir des commits et des comptes rendus. Il ne prétend pas avoir été écrit avant.

## Slices
| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | Agrégats des besoins : clients distincts, portée en sièges, ARR à risque, tendance sur 4 semaines, citations | `po_assist/insights.py` | Test sur un agent parfait | 2 | done |
| 2 | Thèmes hebdomadaires et alertes (churn, déjà décidé, à clarifier) | `po_assist/insights.py` | Test sur un agent parfait | 3, 4 | done |
| 3 | Évaluation contre la vérité terrain | `po_assist/evaluate.py` | Sur l'analyse réelle : types 84 %, thème 96 %, rattachements 98 % / 95 % | 5 | done |

## Rollback
Aucune action irréversible : pas de service hébergé, la base Linear versionnée n'est jamais modifiée (l'application travaille sur une copie dans `data/workspace/`). Chaque tranche est un commit, annulable par `git revert`.

## Gate
- [x] Owner approved the slices (approbation préalable de la démarche : lot Q1 à Q7 du cycle 002, « Je valide, go », Vlad, 2026-11-16 ; plan reconstitué après coup à sa demande, « oui, fais les deux », 2026-11-16)

## As run
| Heure | Tranche | Ce qui s'est passé |
|---|---|---|
| 2026-11-16 09:07 | 1 à 3 | Commit 5e71300. Échec rattrapé : une assertion de test supposait 7 mentions au lieu de 5 ; la valeur attendue est désormais lue dans la vérité terrain |
| 2026-11-16 09:09 | 3 | Évaluation du passage réel enregistrée dans `evidence/` |
