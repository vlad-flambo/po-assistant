# Plan: option API

| | |
|---|---|
| **Cycle** | 010 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

## Slices
| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | SDK `anthropic` et vérification de ses paramètres (`output_config`, `fallbacks`, `betas`, `cache_control` sur `beta.messages.stream`) | `pyproject.toml`, `uv.lock` | Inspection de la signature (2.9.0) | 2, 3, 7 | done |
| 2 | Schémas de sortie par pack | `po_assist/packs/*.py` | Test : `additionalProperties: false` partout, aucune contrainte non prise en charge | 2 | done |
| 3 | Moteur API : paquets, cache, sorties structurées, repli, erreurs, coût | `po_assist/api_agent.py`, `__main__.py` | Tests avec client simulé | 3 à 7 | done |
| 4 | Réglages et interface (moteur, modèle, état de la clé, coût sur le bouton) | `app.py`, `settings.py` | AppTest en mode API | 1, 6 | done |
| 5 | `.env` chargé par le lanceur, ignoré par git | `PO Assist.command`, `.gitignore` | `bash -n` | 8 | done |
| 6 | Essai réel avec la clé de Vlad | — | `uv run python -m po_assist run analyse --engine api --limit 5` puis import | 10 | pending |

## Rollback
Moteur « skill » dans ⚙️ Réglages ; aucun appel n'est fait sans clic. Code : `git revert`.

## Gate
- [x] Owner approved the slices (consigne « A enchainer directement si tout est clair », Vlad, 2026-11-17)

## As run
| Heure | Tranche | Ce qui s'est passé |
|---|---|---|
| 2026-11-17 | 1 | Référence officielle chargée (skill `claude-api`) ; SDK 2.9.0 installé ; paramètres vérifiés sur la signature plutôt que supposés |
| 2026-11-17 | 2 à 5 | 10 tests verts du premier coup (client simulé) ; cas « clé refusée après des paquets payés » corrigé avant les tests : leurs résultats sont gardés |
