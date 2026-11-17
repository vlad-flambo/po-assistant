# Plan: API par défaut, skill en repli

| | |
|---|---|
| **Cycle** | 012 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

## Slices
| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | Défaut `api`, `runner.py` (résolution et repli), démo en flux API simulé | `settings.py`, `runner.py`, `demo.py` | Tests du repli et de la démo | 1 à 4 | done |
| 2 | Interface et ligne de commande | `app.py`, `__main__.py` | AppTest, test du bandeau de repli | 2, 3 | done |
| 3 | Guide (texte, captures), README, démarche, présentation, PROJECT.md | `docs/`, `README.md` | Test des libellés du guide ; captures relues | 5 | done |
| 4 | Slides | artefact Slides | Aperçu rendu | 5 | done |

## Gate
- [x] Owner approved the slices (demande directive de Vlad, 2026-11-17)

## As run
| Heure | Tranche | Ce qui s'est passé |
|---|---|---|
| 2026-11-17 | 1, 2 | 4 tests rouges attendus après le changement (ils encodaient l'ancien défaut) ; le test des libellés du guide a signalé « Lancer la rédaction (agent) », qui n'existe plus, comme prévu. 5 tests ajoutés ; 56 verts |
| 2026-11-17 | 3 | Guide réécrit (§ 1, 3, 4, 6 à 9) ; 12 captures refaites. **Correction** : l'exemple de coût du guide (≈ 0,38 $) était faux, l'estimation réelle est ≈ 1,53 $ pour 80 feedbacks avec Opus 5.5 ; corrigé partout |
| 2026-11-17 | 4 | Slides : diapositive « Démo · Lancer l'agent » ajoutée (15 au total), architecture, ce qui a changé, clôture, 3 captures de démo remplacées, notes mises à jour ; aperçu sans débordement |
