# Verify: socle agent : hand-off par fichiers et faux connecteur Linear

| | |
|---|---|
| **Cycle** | 002 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |
| **Date** | 2026-11-16 |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence (command and output, measurement, screenshot, link) |
|---|-----------|--------|-------------------------------------------------------------|
| 1 | Export du pack « analyse » complet et anonyme | pass | `test_export_is_self_contained_and_anonymous` ; pack réel de 80 tâches, 106 Ko (`handoff/demo/E-20261116-090512-analyse.pack.json`) |
| 2 | Résultats valides appliqués | pass | `test_valid_results_are_applied` ; passage réel du skill : « 80 prêts, 0 refusés, 0 ignorés, 0 sans résultat » |
| 3 | Résultats invalides refusés avec une raison, mode strict | pass | `test_invalid_results_are_refused_with_reasons` (type, thème, cible, citation inventée) ; `test_unknown_export_or_garbage_is_fatal` |
| 4 | Réimport sans effet | pass | `test_reimport_is_a_no_op` |
| 5 | Fichier partiel et tâches ignorées | pass | `test_partial_and_skipped_results` |
| 6 | Skill `po-agent` | pass | `.claude/skills/po-agent/SKILL.md` ; utilisé 3 fois par des sous-agents qui n'ont pas vu la vérité terrain (analyse 80, priorisation 30, rédaction 5) |
| 7 | Tests sans LLM ni réseau | pass | `uv run pytest` : 30 passed ([evidence/pytest_2026-11-16.txt](evidence/pytest_2026-11-16.txt)) |

## Not verified
- Que les sous-agents n'aient effectivement pas ouvert `data/ground_truth.json` : c'est une consigne, pas un contrôle technique (le fichier est dans le même dépôt).
- Le dry-run du skill a échoué une fois parce qu'un module était en cours d'écriture ; le skill a fait sa propre vérification, puis l'import réel est passé sans refus.

## Verdict
- [ ] Accepted by owner
- [ ] Sent back (what, to which stage)
