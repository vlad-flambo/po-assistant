# Journal de démarche

Trace chronologique pour la restitution (critère « Démarche », 20 %) : hypothèses, étapes, impasses, et usage de l'IA avec la façon dont chaque production a été vérifiée.

## Registre de l'usage de l'IA

| Date | Tâche déléguée | Outil | Vérification humaine |
|---|---|---|---|
| 2026-11-14 | Transcription du brief PDF en Markdown | Claude Code | À confirmer par Vlad : relecture face au PDF |
| 2026-11-14 | Première analyse du brief (`docs/analyse/01-analyse-initiale.md`) | Claude Code | Relue par Vlad ; décisions Q1 à Q7 arbitrées par lui |
| 2026-11-14 | Lecture et synthèse de la documentation saxobeat (PRD lus par l'agent principal, 33 cycles synthétisés par un sous-agent) | Claude Code | Faits cités avec leur fichier source dans `cycles/001/intent.md` ; relecture par Vlad à faire |
| 2026-11-14 | Spec du jeu de données (schéma, pièges, critères) | Claude Code | Modèle Linear vérifié par recherche web (objets Customer et CustomerNeed) ; spec soumise à l'approbation de Vlad |
| 2026-11-14 | Rédaction des 80 feedbacks (3 sous-agents en parallèle, un par canal) | Claude Code (sous-agents) | Faits imposés par une matrice écrite avant ; fusion par script contrôlé ; recherche de fuites ; 11 tests ; 5 textes lus par l'agent principal ; 10 soumis à Vlad |
| 2026-11-14 | Mise en place du pilotage en cycles `ai-sdlc` (7 cycles) | Claude Code | Découpage issu de la WBS validée par Vlad |

## Journal

### 2026-11-14 (samedi)

- **Lecture du brief** : 3 blocs obligatoires (Comprendre, Arbitrer, Formaliser) ; 60 % de la note hors code ; aucune donnée fournie.
- **Hypothèses posées par Vlad** : PO sous Linear, intégration simulée sur SQLite, base commitée, données dérivées de saxobeat.
- **Choix de méthode** : cycles `ai-sdlc` (intent → spec → plan → build → verify → learn) pour garder une trace décision par décision.
- **Obstacle** : le dépôt `Vlad-Flambo/saxobeat` n'est pas accessible depuis la session cloud. En attente d'un accès ou d'une description.
- **Point d'attention** : des indices (non vérifiés) suggèrent que saxobeat est un outil de recherche d'emploi, alors que le brief parle d'une plateforme de gestion de projet. Arbitrage demandé (cycle 001, Q1).
- **Déblocage** : Vlad ajoute la documentation de saxobeat (`saxobeat reference/`), qui remplace l'accès au code. La branche `main` ayant divergé, elle a été fusionnée dans la branche de travail (pas de réécriture d'historique).
- **Constat** : saxobeat est un suivi de recherche d'emploi (alpha, 10 à 30 candidats), pas une plateforme de gestion de projet. Il faut décider comment le présenter (Q8 du cycle 001).
- **Décisions** : saxobeat projeté au printemps 2027 (Free / Plus / B2B) pour coller au brief ; lot Q2 à Q7 validé ; intent du cycle 001 fermé.
- **Choix de conception** : les feedbacks entrent dans la file Triage de Linear, reliés à leur client (mécanique réelle des « Customer Requests »). 9 types de pièges sont injectés pour tester l'agent, et la vérité terrain reste hors de la base.
- **Option écartée** : génération par gabarits (Faker), jugée trop artificielle, et génération par LLM au build (pas de clé, non déterministe).
- **Construction du jeu de données** : matrice d'allocation d'abord (qui écrit quoi, avec quels pièges), textes ensuite. L'IA rédige ; elle ne choisit ni les faits ni les réponses attendues.
- **Ce que la vérification a attrapé** : 19 étiquettes P9 oubliées dans mes propres annotations (la règle est désormais calculée et testée), 2 dates incohérentes, une répartition par canal hors tolérance, et 3 incohérences d'offre signalées par les sous-agents rédacteurs. Leçon : ce qui peut se calculer à partir des données ne doit pas être annoté à la main.
