# Plan: mode démo

| | |
|---|---|
| **Cycle** | 009 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

## Slices
| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | Compléter le cache : 25 stories rédigées par le skill (pack exporté dans un espace temporaire, sous-agent sans vérité terrain) | `handoff/demo/E-20261117-110405-redaction.*` | Dry-run strict : 25 prêts, 0 refus | 5, 6 | done |
| 2 | Réglages persistants | `po_assist/settings.py`, `config.py` | Test : défaut, persistance | 1 | done |
| 3 | Moteur démo : export réel puis résultats tirés du cache | `po_assist/demo.py` | Tests : parcours complet, sujet absent → ignoré | 3, 5, 6 | done |
| 4 | Interface : « Lancer l'agent », progression, bandeau, ⚙️ Réglages, suppression du bouton « Charger » | `app.py` | AppTest dans les deux modes ; parcours navigateur | 2, 4, 7 | done |
| 5 | Documentation | `README.md`, `docs/presentation.md` | Relecture | — | done |

## Rollback
Désactiver le mode démo dans ⚙️ Réglages rend l'ancien comportement (skill). Code : `git revert`.

## Gate
- [x] Owner approved the slices (consigne « A enchainer directement si tout est clair », Vlad, 2026-11-17)

## As run
| Heure | Tranche | Ce qui s'est passé |
|---|---|---|
| 2026-11-17 | 1 | Pack de 25 stories exporté dans un espace temporaire et confié au skill en arrière-plan ; rendu : 25/25, 0 refus en strict ; cache complet (80 / 30 / 30) |
| 2026-11-17 | 2 à 4 | Construits pendant que le skill rédigeait ; 35 tests verts, le test de couverture restait rouge jusqu'à l'arrivée des stories |
| 2026-11-17 | 4 | **Défaut trouvé au test navigateur** : la priorisation pouvait être lancée avant l'analyse (16 issues sans preuves ni besoins nouveaux). Corrigé dans le pack (aucune tâche sans analyse) et dans l'interface ; test ajouté |
| 2026-11-17 | 4 | Parcours complet rejoué dans le navigateur : analyse → priorisation → rédaction → 5 stories affichées |
