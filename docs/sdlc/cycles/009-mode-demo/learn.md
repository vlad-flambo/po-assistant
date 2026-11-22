# Learn: mode démo

| | |
|---|---|
| **Cycle** | 009 |
| **Stage** | Learn |
| **Date** | 2026-11-22 |

## What happened vs what we expected
- Les 8 critères passent : rien n'est révélé avant le lancement, progression visible (8,4 s pour 80 tâches), couverture 80 / 30 / 30, cache valide en mode strict, bandeau sur toutes les pages.

## What we learned
- **L'honnêteté envers le jury est une fonctionnalité** : le bandeau 🎬 dit que le flux est simulé et que les résultats viennent d'un vrai passage de l'agent.
- **Rejouer le vrai pipeline** (export, vérification, import) plutôt qu'un affichage figé : la démo prouve le mécanisme.
- **Le test navigateur a trouvé un vrai défaut** (priorisation lançable avant l'analyse), corrigé.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| Mode démo et sa mention | `README.md`, guide §3, `docs/presentation.md` | [x] |

## Process feedback
- La qualité des 25 stories ajoutées au cache n'a été vérifiée qu'en structure ; risque accepté avec la vérification.

## Next cycle candidates
- Relire un échantillon des 25 stories du cache avant la présentation (T-012, T-013, T-023, T-025 signalées par le skill).
