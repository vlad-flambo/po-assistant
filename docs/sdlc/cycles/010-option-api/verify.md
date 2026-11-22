# Verify: option API

| | |
|---|---|
| **Cycle** | 010 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |
| **Date** | 2026-11-17 |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence (command and output, measurement, screenshot, link) |
|---|-----------|--------|-------------------------------------------------------------|
| 1 | Réglages moteur et modèle | pass | `test_estimate_and_engine_setting` ; page ⚙️ Réglages rendue en mode API (`test_ui_in_api_mode_shows_cost_on_the_button`) |
| 2 | Schémas conformes aux sorties structurées | pass | `test_output_schemas_respect_structured_output_limits` (3 packs) |
| 3 | Paquets et préfixe mis en cache identique | pass | `test_api_run_batches_caches_constrains_and_imports` : 4 appels pour 80 tâches, `system` identique avec `cache_control` |
| 4 | Fichier de résultats habituel, vérifié et importé | pass | même test : 80 acceptés, agent « api / claude-opus-5-5 » |
| 5 | Refus, erreur d'un paquet, clé absente ou invalide | pass | `test_refusal_on_one_batch_skips_only_that_batch`, `test_error_after_paid_batches_keeps_their_results`, `test_invalid_key_on_first_batch_stops_everything_cleanly`, `test_no_credentials_means_no_export_and_a_clear_message` |
| 6 | Coût estimé avant, réel après | pass | `test_estimate_and_engine_setting` ; bouton « Lancer l'agent (API, ≈ … $) » (`test_ui_in_api_mode_shows_cost_on_the_button`) ; coût réel calculé sur l'usage renvoyé |
| 7 | Repli côté serveur | pass | appel simulé : `fallbacks="default"` et bêta `server-side-fallback-2026-07-01` |
| 8 | `.env` chargé, ignoré par git | partial | `.gitignore` contient `.env` ; `bash -n` sans erreur ; chargement non exercé par un test |
| 9 | Tests sans réseau ni clé | pass | `tests/test_api.py` : 10 passed ; aucun appel réel |
| 10 | Essai réel avec la clé de Vlad | not checked | Écarté par Vlad le 2026-11-22 (« 010 -> skipping this ») : pas de clé Claude ; l'essai réel d'une API se fait avec Mistral (cycle 013, critère 8) |

## Not verified
- **Aucun appel réel n'a été fait** : pas de clé dans l'environnement de développement. Ce que le client simulé ne prouve pas : la réponse réelle de l'API au schéma (compilation, refus éventuel d'un mot-clé), la qualité des résultats du modèle, le taux de lecture en cache réel, le coût exact.
- **Tarifs** : ceux de la référence du 2026-11-03 ; le prix de lecture en cache de Haiku 5.5 est une estimation (0,1 × l'entrée).
- **Estimation du coût** : grossière (4 caractères ≈ 1 jeton, jetons de sortie moyens par type de tâche).

## Verdict
- [ ] Accepted by owner
- [ ] Sent back (what, to which stage)
