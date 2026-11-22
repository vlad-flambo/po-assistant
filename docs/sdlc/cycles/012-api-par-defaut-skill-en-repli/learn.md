# Learn: API par défaut, skill en repli

| | |
|---|---|
| **Cycle** | 012 |
| **Stage** | Learn |
| **Date** | 2026-11-22 |

## What happened vs what we expected
- Les 6 critères passent : API par défaut, repli automatique sur le skill (pas de clé, clé refusée), démo en flux API simulé, documentation et diapositives alignées.
- Limite assumée à la clôture : le moteur par défaut n'avait jamais été appelé pour de vrai ; c'est l'objet du cycle 013 (Mistral).

## What we learned
- **Un défaut doit avoir un repli** : sans clé, l'outil reste utilisable et le dit.
- **Rendre le moteur interchangeable a payé** : ajouter Mistral (013) n'a touché ni le pack ni la vérification.
- **Les diapositives hors du dépôt ont été perdues** à la migration de compte : tout livrable vit désormais dans le dépôt (`docs/presentation/deck/`).

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| API par défaut, skill en repli, démo simulée | `README.md`, guide §4, `docs/demarche.md`, diapositives 5 et 9 | [x] |
| Livrables versionnés dans le dépôt | `docs/presentation.md`, `docs/journal.md` (2026-11-22) | [x] |

## Process feedback
- Décision prise par demande directe, choix Q1 à Q4 relus après coup : acceptable pour un changement réversible.

## Next cycle candidates
- Essai réel d'une API (cycle 013, Mistral).
