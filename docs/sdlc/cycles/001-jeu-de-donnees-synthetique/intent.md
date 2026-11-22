# Intent: jeu de données synthétique

| | |
|---|---|
| **Cycle** | 001 |
| **Stage** | Intent |
| **Date** | 2026-11-14 |
| **Owner** | Vlad |
| **Importance** | 5/5 (claude, 2026-11-14): bloque tous les autres cycles ; le brief ne fournit aucune donnée, et la démo comme les tests en dépendent |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
> Il faut prévoir de générer un jeu de données synthétique. Il sera basé sur un de mes projets GitHub existants (owner Vlad-Flambo repo saxobeat)
>
> Il faut éclaircir quelques hypothèses de travail comme la stack technique du PO.
> Pour les tickets, supposons que le PO utilise linear. On ne va pas faire une vraie intégration. On fait comme si c'était le cas.
> Tous les tickets des différents canaux se déversent sur linear.
> L'outil fera comme s'il était connecté. Mais en réalité, il se plugera sur une une db SQLite directement
>
> Décision importante. Comme toutes les données sont fictives, j'accepte de mettre la db sur GitHub par simplicité

## Why now / the pain
- Le brief ne fournit aucune donnée : « Vous constituez vous-même les exemples » (`docs/brief/brief.md`, §01).
- Les cycles 002 à 006 (agent, 3 blocs, interface) et la démo (cycle 007) ne peuvent pas être construits ni testés sans ces données.
- L'échéance est lundi 16/11 au soir : le jeu de données doit être prêt samedi 14/11.

## Goal
Disposer d'une base SQLite versionnée, structurée comme un espace Linear, qui contient des feedbacks multicanaux crédibles portant sur un produit réel (dérivé de `saxobeat`), un backlog existant et un contexte produit. Elle doit suffire à démontrer les 3 blocs du brief et à mesurer la qualité de l'agent.

## Success measure
1. `data/linear.db` est commitée et se reconstruit à l'identique depuis les fichiers source par une seule commande.
2. Volumes atteints (Q3) : 80 feedbacks sur 3 canaux, 30 issues de backlog, 60 clients dont 8 à 10 comptes B2B.
3. Chaque type de piège listé dans la spec est présent au moins 2 fois.
4. 100 % des feedbacks ont une étiquette de vérité terrain (type, thème, demande attendue), stockée **hors** de la base lue par l'agent.
5. Vlad relit un échantillon de 10 feedbacks et les juge crédibles.

## Not doing (this cycle)
- Aucun appel à l'API Linear réelle, aucun compte Linear.
- Aucune donnée réelle de client (employeur actuel ou autre).
- Le code de l'agent (cycle 002 et suivants).

## What we already know (facts, with where they came from)
- **Données fictives et base commitée sur GitHub** : décision de Vlad, 2026-11-14 (chat).
- **Linear simulé** : tous les canaux se déversent dans Linear ; l'outil se comporte comme s'il était connecté, mais lit une base SQLite (Vlad, 2026-11-14).
- **Le dépôt `Vlad-Flambo/saxobeat` n'est pas accessible depuis cette session** (`add_repo` refusé le 2026-11-14). Vlad a fourni à la place la documentation du produit dans `saxobeat reference/docs/` (commit `2815bc4`, 2026-11-14) : 7 PRD et études, plus le dossier `sdlc/` complet de saxobeat (33 cycles). Consigne de Vlad : « utilises ces documents comme contexte de l'application, et comme base d'exemples pour les jeux de données ».
- **Ce qu'est saxobeat** (`saxobeat reference/docs/PRD.md` §1-2, `PRD_multi_user.md` §1-4) : un suivi d'opportunités d'emploi. Il collecte les offres d'environ 325 sources (sites carrières des employeurs via Greenhouse, Lever, Workday…, plus des agrégateurs), les dédoublonne, les filtre, leur donne un score explicable (mots-clés + TF-IDF + séniorité) et suit les candidatures (Inbox → Pipeline → Entretiens). Il est en alpha hébergée (Render + Neon, e-mails Brevo, `app.saxobeat.fr`) avec 2 rôles : **opérateur** (Vlad) et **candidats** (10 à 30, sur invitation). Il est gratuit, en français et en anglais, et une interface mobile est prévue (`PRD_mobile.md`).
- **Des signaux produit réutilisables existent** : les registres « à traiter plus tard » des PRD (`PRD_ai_backoffice.md` §18, `PRD_users_and_emails.md` §15), 18 fonctionnalités vues chez les concurrents (`COMPETITION.md` §7), des mesures de succès (`PRD_competitive_features.md` §12), des tarifs du marché et une piste de prix pour saxobeat (9 à 15 € par mois, `COMPETITION.md` §6.5), et le canal de feedback intégré à l'application (cycle 015 « feedback-chat » ; synthèse des cycles en cours).
- **Canal de feedback réel à imiter** (cycle 015, `spec.md`) : un feedback chat scripté en 3 parcours (idée, problème, avis) de 5 étapes, avec des échelles de valeur, d'impact et de fréquence, et un contexte joint (page, appareil, mode, langue). **Seuls 4 feedbacks réels existent**, tous émis par le fondateur (#1, #3, #4, #5 ; citations vérifiées dans les cycles 017 et 021). Synthèse complète : `docs/analyse/02-contexte-saxobeat.md`.
- **Backlog réel** : 33 cycles typés (bug, feature, UX, ops, dette) avec importance et statut, plus `backlog.md` et les registres des PRD (`docs/analyse/02-contexte-saxobeat.md` §4).
- **Écart avec le brief, désormais confirmé** : saxobeat est un outil de recherche d'emploi destiné à des particuliers, pas une « plateforme de gestion de projet » vendue par une startup SaaS (`docs/brief/brief.md` §01). Ce qui le rapproche du cadre attendu : le pipeline de candidatures fonctionne comme un projet suivi par étapes (kanban, relances, échéances).
- **Le brief situe le produit** : « une startup SaaS développe une plateforme de gestion de projet » (`docs/brief/brief.md`, §01).
- **Modèle de données Linear** (de mémoire ; l'existence des objets `Customer` et `CustomerNeed` dans l'API GraphQL est confirmée par la doc Linear « Managing Customers », recherche du 2026-11-14) : Team, Project, Cycle, Issue (state, priority 0 à 4, estimate, labels), une boîte de réception *Triage* pour les tickets entrants, des Customers et des Customer Requests qui relient une demande client à une issue, et des intégrations (Intercom, Zendesk, Front, Slack, email) qui créent des issues en Triage.
- **Aucune clé `ANTHROPIC_API_KEY` dans ce conteneur** (vérifié le 2026-11-14, oui/non seulement) : la génération ne peut pas reposer sur un appel API au moment du build.

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Quel rôle joue saxobeat dans le jeu de données ? | saxobeat **devient le produit** que gère le PO fictif. Ses fonctionnalités réelles fondent les feedbacks et le backlog | Oui : « utilises ces documents comme contexte de l'application, et comme base d'exemples pour les jeux de données » (Vlad, 2026-11-14) | answered |
| Q2 | Fidélité du modèle Linear dans SQLite ? | Sous-ensemble fidèle, noms calqués sur l'API Linear : `teams`, `users`, `workflow_states` (Triage, Backlog, Todo, In Progress, In Review, Done, Canceled, Duplicate), `labels`, `projects`, `initiatives`, `cycles`, `issues` (identifiant SAX-123, priorité 0 à 4, estimation, canal source), `comments`, `customers`, `customer_needs`. Chaque feedback entre comme une issue en **Triage** ; le travail de l'agent consiste à la rattacher à une issue du backlog (`customer_need`) ou à en proposer une nouvelle | Oui : « Je valide » (Vlad, 2026-11-14) | answered |
| Q3 | Volumes et période ? | 80 feedbacks du 1er février au 11 avril 2027 (10 semaines ; la démo se joue le lundi 12 avril 2027). Canaux : 35 % tickets de support, 30 % e-mails, 35 % feedback chat. 60 clients : environ 50 candidats B2C (Free / Plus) et 8 à 10 comptes B2B (cabinets d'outplacement, écoles, coachs) avec ARR. 30 issues de backlog tirées des cycles saxobeat, de `backlog.md` et de `COMPETITION.md` §7. Une équipe de 8 personnes (PO, 4 devs, 1 designer, 2 support) | Oui : « Je valide » (Vlad, 2026-11-14) | answered |
| Q4 | Méthode de génération ? | Contenu rédigé par Claude Code dans des fichiers JSON lisibles (`data/seed/`), à partir des exemples saxobeat ; un script Python déterministe (`scripts/build_db.py`) construit `data/linear.db`. Aucun appel API au build ; la génération est reproductible, relisible et vérifiée par un test de comptage | Oui : « Je valide » (Vlad, 2026-11-14) | answered |
| Q5 | Où ranger la vérité terrain ? | Fichier séparé (`data/ground_truth.json`) : pour chaque feedback, son type, son thème, la demande attendue et l'issue cible. Il n'est jamais chargé dans la base lue par l'agent ; il sert aux évaluations des cycles 003 à 005 | Oui : « Je valide » (Vlad, 2026-11-14) | answered |
| Q6 | Langue des feedbacks ? | Environ 80 % en français, 20 % en anglais | Oui aux recommandations (Vlad, 2026-11-14, réponse à la Q3 de l'analyse) | answered |
| Q8 | Horizon fictif : saxobeat tel qu'il est aujourd'hui (alpha gratuite, 10 à 30 amis) ou projeté en startup SaaS ? | **Projection datée** (« saxobeat, printemps 2027 ») : quelques milliers de candidats, une offre payante (Free / Plus à 12 €/mois, selon `COMPETITION.md` §6.5) et une offre B2B naissante (cabinets d'outplacement, écoles, coachs). Elle colle au brief (« startup SaaS »), donne du volume et des segments à pondérer pour RICE. Tout ce qui est projeté est signalé comme fictif | Oui : « projection printemps 2027 » (Vlad, 2026-11-14) | answered |
| Q7 | Contexte produit à inclure ? | 3 OKR du printemps 2027, stockés comme `initiatives` Linear : (1) conversion Free → Plus, (2) activation (onboarding en moins de 4 minutes), (3) lancement de l'offre B2B. Plus la capacité de l'équipe (≈ 20 points par cycle de 2 semaines) et le cycle Linear en cours | Oui : « Je valide » (Vlad, 2026-11-14) | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- ~~Bloquant : contenu de saxobeat inaccessible~~ levé le 2026-11-14 par la documentation ajoutée dans `saxobeat reference/`.
- **Écart au brief** si saxobeat n'est pas une plateforme de gestion de projet : risque sur le critère « Compréhension métier » (20 %) si l'écart n'est pas expliqué.
- **Données trop propres**, donc démo peu crédible : pièges volontaires (doublons, demandes multiples, contradictions, signaux de churn, bruit).
- **Délai** : le jeu de données doit être prêt samedi soir pour tenir lundi soir.

## Gate
- [x] All open questions answered or parked
- [x] Goal and success measure confirmed by the owner (« Je valide », Vlad, 2026-11-14)
