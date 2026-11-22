# Learn: option API

| | |
|---|---|
| **Cycle** | 010 |
| **Stage** | Learn |
| **Date** | 2026-11-22 |

## What happened vs what we expected
- Mesures 1 à 4 atteintes avec un client simulé : moteur choisi dans les Réglages, pack traité sans geste manuel, coût estimé avant et calculé après, messages clairs sans clé ou en cas d'erreur, paquets déjà payés conservés.
- Critère 8 partiel (chargement du `.env` non testé automatiquement ; il fonctionne sur le Mac depuis le cycle 008).
- **Critère 10 écarté par le PO** (« close 010 as skipped », 2026-11-22) : aucune clé Claude disponible. L'essai réel d'une API passe au cycle 013, avec Mistral.

## What we learned
- **Un client simulé prouve le mécanisme, pas l'intégration** : découpage, cache, schémas, refus et coût sont couverts ; la réponse réelle au schéma, la qualité et le coût exact ne le sont pas.
- **Ne pas dépendre d'un seul fournisseur** : faute de clé Claude, le moteur a été ouvert à Mistral (013) sans toucher au pack ni à la vérification.
- **Le coût annoncé avant envoi** rassure le PO et répond à une question probable du jury.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| Moteur API, coût estimé puis réel | `README.md`, guide §4.1 | [x] |
| Limite « jamais appelé pour de vrai » | `docs/demarche.md` §6 (mise à jour au cycle 013) | [x] |
| Essai réel d'une API | cycle 013, critère 8 | [x] |

## Process feedback
- Un critère qui dépend d'une ressource du PO (une clé) doit être signalé dès l'intent comme bloquant possible ; ici il est resté ouvert 5 jours avant d'être écarté.

## Next cycle candidates
- Essai réel Claude si une clé devient disponible (une commande : `run analyse --engine api --model claude-opus-5-5 --limit 5`).
