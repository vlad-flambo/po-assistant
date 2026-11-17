# Plan: lanceur Mac (port 8007)

| | |
|---|---|
| **Cycle** | 008 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

## Slices
| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | Port 8007 par défaut | `.streamlit/config.toml` | `uv run streamlit run app.py` répond sur 8007 | 6 | done |
| 2 | Le lanceur | `PO Assist.command` | 4 scénarios sous Linux : démarrage normal, déjà lancé, port pris, uv absent ; `bash -n` ; mode 100755 | 1 à 5 | done |
| 3 | Documentation | `README.md`, `docs/presentation.md` | Relecture | 7 | done |
| 4 | Vérification sur le Mac | — | Double-clic par Vlad | 8 | pending |

## Rollback
Supprimer les deux nouveaux fichiers ; aucune donnée n'est touchée.

## Gate
- [x] Owner approved the slices (approbation préalable : « je valide les recommandations, go », Vlad, 2026-11-17)

## As run
| Heure | Tranche | Ce qui s'est passé |
|---|---|---|
| 2026-11-17 | 1 | `.streamlit/config.toml` : port 8007, statistiques désactivées ; lancement manuel vérifié sur 8007 |
| 2026-11-17 | 2 | `PO Assist.command` écrit pour bash 3.2 ; 4 scénarios passés du premier coup sous Linux ; mode 100755 |
| 2026-11-17 | 3 | README (« Démarrer ») et liste d'avant démo mis à jour ; 30 tests toujours verts |
