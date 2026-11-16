# Verify: bloc B arbitrer la priorisation

| | |
|---|---|
| **Cycle** | 004 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |
| **Date** | 2026-11-16 |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence (command and output, measurement, screenshot, link) |
|---|-----------|--------|-------------------------------------------------------------|
| 1 | Estimations de l'agent | pass | Passage réel : 30/30 importés, 0 refus ; 8 Must (32 pts), 9 Should, 12 Could, 1 Won't |
| 2 | Scores calculés | pass | `test_scores_are_computed_by_code_and_follow_po_overrides` |
| 3 | Corrections du PO | pass | même test (overrides) ; page ⚖️ (éditeur) rendue sans erreur (`test_every_ui_page_renders`) |
| 4 | Proposition de sprint | pass | `test_cycle_proposal_respects_capacity` ; données réelles : 9,5 pts disponibles sur 20, 3 issues Todo du cycle 8 non retenues |

## Verdict
- [ ] Accepted by owner
- [ ] Sent back (what, to which stage)
