# Verify: API par défaut, skill en repli

| | |
|---|---|
| **Cycle** | 012 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |
| **Date** | 2026-11-17 |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence (command and output, measurement, screenshot, link) |
|---|-----------|--------|-------------------------------------------------------------|
| 1 | Défaut `api`, skill choisissable | pass | `test_estimate_and_engine_setting`, `test_default_is_api_and_no_key_falls_back_to_skill` |
| 2 | Repli automatique sur le skill | pass | `test_default_is_api_and_no_key_falls_back_to_skill`, `test_key_refused_on_first_batch_falls_back_to_skill`, `test_ui_without_key_shows_the_fallback` ; `test_api_engine_with_a_working_client_does_not_fall_back` |
| 3 | Démo = flux API simulé | pass | `test_demo_simulates_the_api_flow` (4 paquets, coût simulé, provenance) ; capture `docs/guide/02-agent-resultats-prets.jpg` (bouton « Lancer l'agent (API, ≈ 1,53 $) », « API : paquet 4/4 traité », « Coût simulé ») |
| 4 | `runner.py`, ligne de commande | pass | Tests ci-dessus ; `python -m po_assist run --help` |
| 5 | Documentation et slides | pass | Guide (test des libellés vert), README, `docs/demarche.md`, `docs/presentation.md`, PROJECT.md ; slides version 9 (15 diapositives), aperçu relu |
| 6 | Tests | pass | `uv run pytest` : 56 passed ([evidence/pytest_2026-11-17.txt](evidence/pytest_2026-11-17.txt)) |

## Not verified
- **Aucun appel réel à l'API** : le défaut est désormais un moteur qui n'a été testé qu'avec un client simulé. Le repli sur le skill couvre l'échec d'appel ; l'essai réel avec la clé de Vlad reste le critère 10 du cycle 010.
- Les slides n'ont été vérifiées qu'en aperçu (captures d'écran non chargées dans l'aperçu, comme prévu par l'outil).

## Verdict
- [x] Accepted by owner (Vlad, 2026-11-22 : « I accept »)
- [ ] Sent back (what, to which stage)
