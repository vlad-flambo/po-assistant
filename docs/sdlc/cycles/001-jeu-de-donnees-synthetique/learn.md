# Learn: jeu de données synthétique

| | |
|---|---|
| **Cycle** | 001 |
| **Stage** | Learn |
| **Date** | 2026-11-16 |

## What happened vs what we expected
- Les 5 mesures de succès sont atteintes : reconstruction identique en une commande, volumes respectés (80 / 30 / 60), chaque piège présent au moins 2 fois, vérité terrain complète, échantillon de 10 feedbacks approuvé par Vlad.
- Le jeu de données a ensuite servi pour de vrai : l'analyse réelle du skill a été mesurée contre lui (cycle 003), ce qui était son but.

## What we learned
- **Ce qui se calcule ne s'annote pas à la main** : 19 étiquettes P9 sur 43 avaient été oubliées. La règle est désormais calculée et testée.
- **Définir avant d'écrire** : la matrice d'allocation (canal, client, cible, pièges) a permis de déléguer la rédaction à 3 agents sans perdre la maîtrise des faits.
- **Les agents rédacteurs relisent aussi** : ils ont signalé 3 incohérences d'offre dans les données de l'agent principal.
- **Les vrais retours de saxobeat** (feedback chat structuré : valeur, impact, fréquence) font un excellent modèle de canal : ils donnent des signaux exploitables pour la priorisation.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| Méthode de construction et pièges | `data/README.md` | [x] |
| Leçons (calculer plutôt qu'annoter, définir avant d'écrire, contrôle croisé par les agents) | `docs/demarche.md` §3 et §4, `docs/journal.md` | [x] |
| Argumentaire pour le jury (« l'IA rédige, elle ne choisit pas les faits ») | `docs/presentation.md` (diapositive 8) | [x] |

## Process feedback
- Le lot de questions avec recommandations (Q2 à Q7) a tenu le délai : une seule validation au lieu de six allers-retours.
- Spec complète pour ce cycle (12 critères), allégée pour les suivants (Q7 du cycle 002) : un compromis assumé face à l'échéance.

## Next cycle candidates
- Une vérité terrain pour la priorisation (les décisions passées du PO), pour mesurer aussi le bloc B.
- Davantage de volume (pagination des packs, comme sur saxobeat).
