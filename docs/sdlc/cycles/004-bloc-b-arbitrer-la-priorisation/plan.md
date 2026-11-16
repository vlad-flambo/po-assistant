# Plan: bloc B arbitrer la priorisation

| | |
|---|---|
| **Cycle** | 004 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

> **Plan reconstitué après coup** (2026-11-16, à la demande de Vlad) : avec la documentation allégée décidée en Q7 du cycle 002, la construction a été menée sans `plan.md` préalable. Ce fichier retrace les tranches réellement exécutées, à partir des commits et des comptes rendus. Il ne prétend pas avoir été écrit avant.

## Slices
| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | Pack « priorisation » : estimations de l'agent (Impact, Confiance, Effort, MoSCoW, OKR, justification) | `po_assist/packs/priorisation.py` | Export de 30 besoins ouverts | 1 | done |
| 2 | Scores calculés : Reach, RICE, score pondéré, corrections du PO | `po_assist/scoring.py` | Tests ; passage réel : 30/30 importés | 2, 3 | done |
| 3 | Proposition de sprint dans la capacité restante | `po_assist/scoring.py` | 9,5 pts libres sur 20 ; 3 issues Todo non retenues | 4 | done |
| 4 | Bascule du Reach personnes / clients (ajoutée après lecture des résultats réels) | `po_assist/scoring.py` | Test : Reach en clients < Reach en personnes | 2 | done |

## Rollback
Aucune action irréversible : pas de service hébergé, la base Linear versionnée n'est jamais modifiée (l'application travaille sur une copie dans `data/workspace/`). Chaque tranche est un commit, annulable par `git revert`.

## Gate
- [x] Owner approved the slices (approbation préalable de la démarche : lot Q1 à Q7 du cycle 002, « Je valide, go », Vlad, 2026-11-16 ; plan reconstitué après coup à sa demande, « oui, fais les deux », 2026-11-16)

## As run
| Heure | Tranche | Ce qui s'est passé |
|---|---|---|
| 2026-11-16 09:10 | 1 à 3 | Commit 3562bdf |
| 2026-11-16 09:11 | 4 | Biais découvert sur l'export réel : un compte de 300 sièges place un besoin en tête ; bascule ajoutée plutôt que de trancher dans le code |
