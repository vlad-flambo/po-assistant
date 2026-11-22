# Learn: socle agent et faux connecteur Linear

| | |
|---|---|
| **Cycle** | 002 |
| **Stage** | Learn |
| **Date** | 2026-11-22 |

## What happened vs what we expected
- Les 4 mesures de succès sont atteintes : aller-retour complet export → skill → import sur les 80 feedbacks sans clé API (80 prêts, 0 refus) ; résultats invalides refusés avec une raison ; réimport sans effet ; tests sans LLM.
- Le socle a tenu sans modification de format quand l'API (010, 012) puis Mistral (013) sont arrivés : seul le transport a changé.

## What we learned
- **Le pack auto-suffisant découple le moteur** : instructions, format, contexte et tâches dans un seul fichier ; skill, API Claude et API Mistral traitent le même pack.
- **La vérification à l'import est le vrai garde-fou** : citations mot pour mot, cibles connues, format strict. Elle a rendu acceptables des moteurs non vérifiés (API simulée, Mistral).
- **Consigne n'est pas contrôle** : rien n'empêche techniquement un agent de lire `data/ground_truth.json` (même dépôt) ; c'est une limite à dire au jury.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| Architecture pack / vérification / import | `README.md` (moteurs, schéma), `docs/demarche.md` §5 | [x] |
| Limite « vérité terrain dans le même dépôt » | `docs/demarche.md` §6 (à ajouter si le jury creuse : la sortir du dépôt de travail de l'agent) | [x] |

## Process feedback
- Plan reconstitué après coup (cycles 002 à 006 menés d'un trait sous l'échéance) : la trace existe, mais les portes Spec et Plan n'ont pas été des moments de décision.

## Next cycle candidates
- Sortir la vérité terrain du périmètre de lecture de l'agent (contrôle technique au lieu d'une consigne).
