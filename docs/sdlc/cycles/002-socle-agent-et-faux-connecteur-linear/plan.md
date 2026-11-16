# Plan: socle agent : hand-off par fichiers et faux connecteur Linear

| | |
|---|---|
| **Cycle** | 002 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

> **Plan reconstitué après coup** (2026-11-16, à la demande de Vlad) : avec la documentation allégée décidée en Q7 du cycle 002, la construction a été menée sans `plan.md` préalable. Ce fichier retrace les tranches réellement exécutées, à partir des commits et des comptes rendus. Il ne prétend pas avoir été écrit avant.

## Slices
| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | Configuration, connecteur Linear (lecture, rattachement, création d'issue), base de travail | `po_assist/config.py`, `linear.py`, `store.py` | Lecture de 80 feedbacks et 30 issues ; cycle 8 trouvé | 1 | done |
| 2 | Échange générique : export, vérification sans écriture, aperçu, import idempotent, fichiers partiels, dossiers to-do/done/problems | `po_assist/handoff.py`, `__main__.py` | Export réel de 80 tâches (106 Ko) | 1 à 5 | done |
| 3 | Pack « analyse » et règles de validation (citations exactes) | `po_assist/packs/analyse.py`, `base.py` | `--dry-run` sur des résultats corrompus | 1, 3 | done |
| 4 | Skill Claude Code `po-agent` | `.claude/skills/po-agent/SKILL.md` | Passage réel par un sous-agent : 80/80, 0 refus | 6 | done |
| 5 | Tests sans LLM (agent parfait tiré de la vérité terrain, résultats corrompus) | `tests/conftest.py`, `tests/test_handoff.py` | 9 tests verts (20 au total) | 7 | done |

## Rollback
Aucune action irréversible : pas de service hébergé, la base Linear versionnée n'est jamais modifiée (l'application travaille sur une copie dans `data/workspace/`). Chaque tranche est un commit, annulable par `git revert`.

## Gate
- [x] Owner approved the slices (approbation préalable de la démarche : lot Q1 à Q7 du cycle 002, « Je valide, go », Vlad, 2026-11-16 ; plan reconstitué après coup à sa demande, « oui, fais les deux », 2026-11-16)

## As run
| Heure | Tranche | Ce qui s'est passé |
|---|---|---|
| 2026-11-16 09:05 | 1 à 3, 5 | Commit 6636332. Échec rattrapé : `pythonpath` manquant dans la configuration de pytest |
| 2026-11-16 09:08 | 4 | Le dry-run du skill échoue sur un module en cours d'écriture (`redaction.py`) ; le skill fait sa propre vérification ; import réel : 80 prêts, 0 refus |
