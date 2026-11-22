# Verify: Moteur API Mistral

| | |
|---|---|
| **Cycle** | 013 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |

## Evidence per criterion
| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Défaut Mistral Large, 6 modèles choisissables | pass | `test_default_model_is_mistral_and_both_providers_are_offered` ; capture `docs/guide/11-reglages.jpg` |
| 2 | Faux client : 4 paquets, json_schema strict, 80 importés, coût depuis `usage` | pass | `test_mistral_run_batches_constrains_and_imports` |
| 3 | Schéma rejeté → reprise `json_object` | pass | `test_rejected_schema_is_retried_once_in_json_mode` (8 appels pour 4 paquets) |
| 4 | 401/403/404 au 1er paquet : arrêt propre, repli ; après paquets payés : résultats gardés | pass | `test_refused_key_on_first_batch_stops_cleanly_and_runner_falls_back` (×3), `test_refusal_after_paid_batches_keeps_their_results` |
| 5 | 429/5xx/réseau : essais puis paquet ignoré ; tronqué / illisible : paquet ignoré | pass | `test_one_bad_batch_skips_only_that_batch` (×4), `test_client_retries_rate_limits_then_succeeds_and_never_leaks_the_key` |
| 6 | Sans `MISTRAL_API_KEY` : repli nommant la variable ; clé jamais affichée | pass | `test_no_mistral_key_falls_back_with_the_right_variable_name`, `test_settings_page_names_the_mistral_key` ; l'erreur HTTP ne contient pas la clé |
| 7 | Moteur Claude inchangé, suite verte | pass | 15 tests Claude verts (modèle fixé), 71 au total : [evidence/pytest_2026-11-22.txt](evidence/pytest_2026-11-22.txt) |
| 8 | Essai réel avec la clé de Vlad | pass | 2026-11-22, sur le Mac, dans un espace de test isolé : 5 analyses envoyées à `mistral-large-latest` en 1 paquet, coût réel 0,0312 $, import « 5 prêts, 0 refusés, 0 ignorés, 0 sans résultat ». Schéma strict accepté (avec `anyOf`), sans reprise `json_object` : [evidence/mistral-live_2026-11-22.md](evidence/mistral-live_2026-11-22.md) |

## Not verified
- Vérifié par l'essai réel du 2026-11-22 : forme des réponses, `json_schema` strict avec `anyOf`, alias `mistral-large-latest`. Pas vérifié : Medium et Small, un lot complet (80 tâches, 4 paquets), les 429 et 5xx en vrai, et les tarifs officiels (le coût réel est calculé avec les tarifs estimés du code, pas lu sur une facture Mistral).
- La qualité des analyses de Mistral n'est pas mesurée (page 🎯 Qualité) : l'essai prouve que le moteur fonctionne, rien de plus (demande de Vlad, 2026-11-22).
- Le cache de prompt Mistral n'est pas exploité (`cached_tokens` est seulement compté s'il est renvoyé).

## Verdict
- [x] Accepted by the owner (after criterion 8) : « Yes, accept and commit » (Vlad, 2026-11-22)
