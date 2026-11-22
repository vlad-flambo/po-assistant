# Verify: mode démo

| | |
|---|---|
| **Cycle** | 009 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |
| **Date** | 2026-11-17 |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence (command and output, measurement, screenshot, link) |
|---|-----------|--------|-------------------------------------------------------------|
| 1 | Mode démo par défaut, réglage persistant | pass | `test_demo_mode_is_on_by_default_and_survives_reset` |
| 2 | Rien n'est révélé avant le lancement ; bouton « Charger » supprimé | pass | `test_nothing_is_revealed_before_the_po_runs_the_agent` ; navigateur : « Aucune analyse importée » après « Réinitialiser » ([parcours](evidence/parcours_navigateur_2026-11-17.md)) |
| 3 | Export réel, puis fichier de résultats issu du cache (agent « pré-calculé »), `skipped` hors cache | pass | `test_demo_run_plays_the_real_pipeline_step_by_step`, `test_subject_missing_from_cache_is_skipped_never_invented` |
| 4 | Progression visible, entre 3 et 10 s | pass | Navigateur : 8,4 s pour 80 tâches ([capture](evidence/1-resultats-prets.png)) |
| 5 | Couverture 80 / 30 / 30 | pass | `demo.coverage()` = 80 analyses, 30 estimations, 30 stories ; `test_every_prioritized_need_has_a_cached_story` |
| 6 | Cache valide en mode strict | pass | `test_demo_results_pass_strict_validation_on_a_fresh_workspace` ; dry-run strict des 25 nouvelles stories : 0 refus |
| 7 | Bandeau sur toutes les pages | pass | `test_every_ui_page_renders_in_both_modes` (présent en démo, absent sinon) |
| 8 | Tests | pass | `uv run pytest` : 46 passed ([evidence/pytest_2026-11-17.txt](evidence/pytest_2026-11-17.txt)) |

## Not verified
- La qualité des 25 nouvelles stories, au-delà de la validation de structure : elles ont été produites par le skill (sous-agent sans vérité terrain) et aucune n'a été relue en entier. Le skill signale lui-même ses incertitudes : T-023 et T-025 sans citation, T-012 et T-013 estimées sous hypothèse.
- Le comportement sur le Mac de Vlad (testé sous Linux, Chromium).

## Verdict
- [x] Accepted by owner (Vlad, 2026-11-22 : « I accept »)
- [ ] Sent back (what, to which stage)
