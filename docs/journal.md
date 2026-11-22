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
| 2026-11-16 | Code de l'application (connecteur, packs, scores, interface, tests) | Claude Code | 30 tests ; chaque page de l'interface testée sans navigateur ; chiffres du script de démo recoupés avec les données (3 corrigés) |
| 2026-11-16 | Travail de l'agent : analyse (80), priorisation (30), rédaction (5) | Skill `po-agent` exécuté par des sous-agents qui n'ont pas vu la vérité terrain | Validation automatique à l'import (0 refus) ; analyse mesurée contre la vérité terrain |
| 2026-11-16 | Diapositives de restitution (14) | Claude Code | Aperçu rendu et relu ; un titre raccourci ; chiffres repris des données vérifiées |
| 2026-11-17 | 25 stories supplémentaires pour le cache du mode démo | Skill `po-agent` (sous-agent sans vérité terrain) | Dry-run strict : 25/25 ; structure validée ; contenu non relu en entier |
| 2026-11-17 | Moteur API (référence officielle `claude-api` chargée avant d'écrire) | Claude Code | Signature du SDK vérifiée ; 10 tests avec client simulé ; aucun appel réel (pas de clé) |
| 2026-11-17 | Guide utilisateur (texte et captures) | Claude Code | Test des 45 libellés distincts cités contre l'interface ; parcours suivi dans un navigateur jusqu'à l'envoi dans Linear ; 3 captures relues |
| 2026-11-14 | Mise en place du pilotage en cycles `ai-sdlc` (7 cycles) | Claude Code | Découpage issu de la WBS validée par Vlad |

## Journal

### 2026-11-14 (samedi)

- **Lecture du brief** : 3 blocs obligatoires (Comprendre, Arbitrer, Formaliser) ; 60 % de la note hors code ; aucune donnée fournie.
- **Hypothèses posées par Vlad** : PO sous Linear, intégration simulée sur SQLite, base commitée, données dérivées de saxobeat.
- **Choix de méthode** : cycles `ai-sdlc` (intent → spec → plan → build → verify → learn) pour garder une trace décision par décision.
- **Obstacle** : le dépôt `Vlad-Flambo/saxobeat` n'est pas accessible depuis la session cloud. En attente d'un accès ou d'une description.
- **Point d'attention** : des indices (non vérifiés) suggèrent que saxobeat est un outil de recherche d'emploi, alors que le brief parle d'une plateforme de gestion de projet. Arbitrage demandé (cycle 001, Q1).
- **Déblocage** : Vlad ajoute la documentation de saxobeat (`saxobeat reference/`, retiré du dépôt public le 2026-11-22, voir plus bas), qui remplace l'accès au code. La branche `main` ayant divergé, elle a été fusionnée dans la branche de travail (pas de réécriture d'historique).
- **Constat** : saxobeat est un suivi de recherche d'emploi (alpha, 10 à 30 candidats), pas une plateforme de gestion de projet. Il faut décider comment le présenter (Q8 du cycle 001).
- **Décisions** : saxobeat projeté au printemps 2027 (Free / Plus / B2B) pour coller au brief ; lot Q2 à Q7 validé ; intent du cycle 001 fermé.
- **Choix de conception** : les feedbacks entrent dans la file Triage de Linear, reliés à leur client (mécanique réelle des « Customer Requests »). 9 types de pièges sont injectés pour tester l'agent, et la vérité terrain reste hors de la base.
- **Option écartée** : génération par gabarits (Faker), jugée trop artificielle, et génération par LLM au build (pas de clé, non déterministe).
- **Construction du jeu de données** : matrice d'allocation d'abord (qui écrit quoi, avec quels pièges), textes ensuite. L'IA rédige ; elle ne choisit ni les faits ni les réponses attendues.
- **Ce que la vérification a attrapé** : 19 étiquettes P9 oubliées dans mes propres annotations (la règle est désormais calculée et testée), 2 dates incohérentes, une répartition par canal hors tolérance, et 3 incohérences d'offre signalées par les sous-agents rédacteurs. Leçon : ce qui peut se calculer à partir des données ne doit pas être annoté à la main.

### 2026-11-16 (lundi)

- **Pivot d'architecture (Vlad)** : pas d'API Anthropic. L'IA passe par un skill Claude Code qui traite des payloads exportés par l'application, puis l'application importe la réponse. C'est le modèle déjà en production sur saxobeat (« le fichier est le skill »).
- **Conséquence** : pas de chat dans l'interface. Le PO valide entre chaque étape, et la vérification à l'import devient le garde-fou principal.
- **Construction en une journée** : socle d'échange (002), Comprendre (003), Arbitrer (004), Formaliser (005), interface (006). Documentation allégée, comme décidé en Q7.
- **Premier vrai passage de l'agent** (80 feedbacks, en un seul passage, sans voir la vérité terrain) : types 84 %, thème principal 96 %, rattachement au backlog 98 % / 95 %, 22 besoins nouveaux sur 22, aucun risque de churn manqué. L'erreur la plus fréquente : des bugs classés en améliorations (5 cas).
- **Biais découvert à l'usage** : compté en personnes (sièges Business), le Reach donne la priorité aux comptes Business ; compté en clients, ce sont les bugs B2C qui passent devant. Plutôt que de trancher dans le code, la bascule est laissée au PO. C'est un argument de démo.
- **Erreurs rattrapées dans mes propres documents** : une assertion de test fausse (5 mentions et non 7) et 3 chiffres du script de démo, corrigés après recoupement avec les données.
- **Clôture du cycle 001** : échantillon de 10 feedbacks relu et approuvé par Vlad. Le travail passe sur `main` (branche unique à partir de maintenant).

### 2026-11-17 (mardi)

- **Cycle 008, lanceur Mac** : `PO Assist.command` (double-clic, port 8007, cas « déjà lancé », « port pris » et « uv absent » traités). 4 scénarios testés sous Linux ; reste la vérification par Vlad sur son Mac.
- **Cycle 009, mode démo (par défaut)** : le PO joue le vrai parcours ; à chaque « Lancer l'agent », le résultat d'un vrai passage du skill, calculé à l'avance, arrive en environ 8 s puis passe par la vérification et l'import habituels. 25 stories ajoutées au cache par le skill pour couvrir toute sélection. Un bandeau signale le mode, par honnêteté envers le jury.
- **Défaut attrapé par le test navigateur** : la priorisation pouvait être lancée avant l'analyse ; elle est désormais conditionnée.
- **Cycle 010, option API** : moteur au choix (skill local ou API). Même pack, envoyé par paquets avec instructions en cache et sorties structurées, coût estimé avant puis réel après. Aucun appel réel possible ici : l'essai revient à Vlad.
- **Cycle 011, guide utilisateur** : `docs/guide-utilisateur.md`, aussi affiché dans l'application (page ❓ Guide, une seule source). Un test garantit que chaque bouton ou page cité existe à l'écran, pour que le guide ne se périme pas sans qu'on le sache.
- **Cycle 012, API par défaut** (demande de Vlad) : l'API devient le moteur par défaut, le skill Claude Code le repli automatique (pas de clé, clé refusée), et la démo simule le flux API (coût annoncé, paquets, coût simulé, rien n'est facturé). Décision 002-D1 remplacée par 012-D1. Guide, README, démarche, script de présentation et slides réécrits en conséquence ; une erreur rattrapée dans le guide (exemple de coût à 0,38 $ au lieu de 1,53 $).
