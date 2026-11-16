# Plan: interface web du PO

| | |
|---|---|
| **Cycle** | 006 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

> **Plan reconstitué après coup** (2026-11-16, à la demande de Vlad) : avec la documentation allégée décidée en Q7 du cycle 002, la construction a été menée sans `plan.md` préalable. Ce fichier retrace les tranches réellement exécutées, à partir des commits et des comptes rendus. Il ne prétend pas avoir été écrit avant.

## Slices
| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | Copie de travail de la base Linear et rejeu de la démo (résultats pré-calculés, réinitialisation) | `po_assist/config.py`, `handoff.py` | Test de rejeu sur une base vierge | 2 | done |
| 2 | Application Streamlit, 7 pages | `app.py` | AppTest : chaque page sans erreur | 1, 3 | done |
| 3 | Captures de secours | `docs/captures/` | 7 captures Playwright, relues | — | done |

## Rollback
Aucune action irréversible : pas de service hébergé, la base Linear versionnée n'est jamais modifiée (l'application travaille sur une copie dans `data/workspace/`). Chaque tranche est un commit, annulable par `git revert`.

## Gate
- [x] Owner approved the slices (approbation préalable de la démarche : lot Q1 à Q7 du cycle 002, « Je valide, go », Vlad, 2026-11-16 ; plan reconstitué après coup à sa demande, « oui, fais les deux », 2026-11-16)

## As run
| Heure | Tranche | Ce qui s'est passé |
|---|---|---|
| 2026-11-16 09:12 | 2 | Commit d6b185d. Avertissement Streamlit (`use_container_width` obsolète) corrigé |
| 2026-11-16 09:14 | 1 | Commit 2f75aa6 : tests de rejeu et de rendu |
| 2026-11-16 09:17 | 3 | Commit 665ef69 |
