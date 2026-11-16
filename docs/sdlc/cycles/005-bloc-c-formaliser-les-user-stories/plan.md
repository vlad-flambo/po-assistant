# Plan: bloc C formaliser les user stories

| | |
|---|---|
| **Cycle** | 005 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

> **Plan reconstitué après coup** (2026-11-16, à la demande de Vlad) : avec la documentation allégée décidée en Q7 du cycle 002, la construction a été menée sans `plan.md` préalable. Ce fichier retrace les tranches réellement exécutées, à partir des commits et des comptes rendus. Il ne prétend pas avoir été écrit avant.

## Slices
| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | Pack « rédaction » : story, Gherkin, INVEST, estimation, découpage, questions ouvertes | `po_assist/packs/redaction.py` | Validation de structure testée | 1, 2 | done |
| 2 | Publication dans Linear (création ou commentaire, rattachement des feedbacks) et exports Markdown / CSV | `po_assist/actions.py`, `linear.py` | Test de bout en bout | 3, 4 | done |
| 3 | Passage réel du skill sur 5 besoins choisis | `handoff/demo/` | 5/5 importés, 0 refus en mode strict ; une story relue en entier | 1 | done |

## Rollback
Aucune action irréversible : pas de service hébergé, la base Linear versionnée n'est jamais modifiée (l'application travaille sur une copie dans `data/workspace/`). Chaque tranche est un commit, annulable par `git revert`.

## Gate
- [x] Owner approved the slices (approbation préalable de la démarche : lot Q1 à Q7 du cycle 002, « Je valide, go », Vlad, 2026-11-16 ; plan reconstitué après coup à sa demande, « oui, fais les deux », 2026-11-16)

## As run
| Heure | Tranche | Ce qui s'est passé |
|---|---|---|
| 2026-11-16 09:10 | 1, 2 | Commit 3562bdf |
| 2026-11-16 09:17 | 3 | Commit 665ef69 : stories importées et versionnées pour la démo |
