# Spec: jeu de données synthétique

| | |
|---|---|
| **Cycle** | 001 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |
| **Date** | 2026-11-14 |

## Behaviour when finished

- **Pour l'agent (cycles 002 à 006)** : `data/linear.db` est un espace Linear fictif, « saxobeat · printemps 2027 », figé au **lundi 12 avril 2027** (date de la démo).
  - La file **Triage** contient 80 feedbacks arrivés depuis le 1er février par 3 canaux : tickets de support, e-mails, feedback chat. Chacun est relié au client qui l'a émis.
  - Le backlog compte 30 issues, dérivées du vrai backlog de saxobeat, avec leur état, leur priorité, leur estimation et leurs demandes clients historiques.
  - Le contexte produit est disponible : 3 objectifs (initiatives), des projets, les sprints, l'équipe et sa capacité.
- **Pour Vlad et le jury** :
  - Les fichiers source (`data/seed/*.json`) sont lisibles et relisibles.
  - Une seule commande reconstruit la base à l'identique.
  - `data/README.md` explique le schéma, la provenance des données et leur caractère fictif.
- **Pour les évaluations** : `data/ground_truth.json` donne, pour chaque feedback, la bonne réponse attendue de l'agent. Ce fichier n'est jamais chargé dans la base.

## Acceptance criteria
Each one must be checkable in `verify.md`.

1. [ ] **Construction reproductible** : `uv run python scripts/build_db.py` crée `data/linear.db` à partir de `data/seed/` uniquement. Deux constructions successives produisent un dump SQL identique (même empreinte SHA-256).
2. [ ] **Schéma** : la base contient les 12 tables listées sous « Interfaces and data », avec leurs colonnes. `PRAGMA foreign_key_check` ne renvoie rien et `PRAGMA integrity_check` renvoie `ok`.
3. [ ] **Feedbacks** :
   - 80 issues sont à l'état Triage, créées entre le 2027-02-01 et le 2027-04-11.
   - Répartition par canal : 28 tickets de support, 24 e-mails, 28 feedback chat (± 2 par canal).
   - Chaque feedback a exactement une `customer_need` qui le relie à son client.
4. [ ] **Backlog** :
   - 30 issues hors Triage, réparties entre les états Backlog, Todo, In Progress, In Review, Done et Canceled (au moins 2 issues par état).
   - Chacune a une priorité de 0 à 4 et un type (Bug, Feature ou Improvement).
   - Les issues prêtes à être planifiées ont une estimation.
   - Au moins 20 des 30 issues citent leur origine saxobeat (cycle ou section de PRD) dans `source_metadata`.
5. [ ] **Clients** :
   - 60 clients au total.
   - Entre 8 et 10 comptes B2B, chacun avec un ARR en euros, une taille, et un statut parmi active, at_risk et churned.
   - Les autres sont des candidats B2C en offre Free ou Plus.
   - Au moins 25 demandes clients historiques (antérieures au 2027-02-01) sont rattachées aux issues du backlog.
6. [ ] **Contexte** :
   - 3 initiatives (OKR) et au moins 4 projets rattachés à ces initiatives.
   - Des sprints de 2 semaines couvrent la période, et un sprint en cours contient le 2027-04-12.
   - 8 utilisateurs internes et 3 utilisateurs d'intégration (Zendesk, e-mail, feedback chat).
   - La capacité de l'équipe (points par sprint) figure dans `workspace_meta`.
7. [ ] **Langue** : entre 14 et 20 feedbacks sont rédigés en anglais, les autres en français.
8. [ ] **Pièges** : chacun des 9 types de pièges listés plus bas apparaît au moins 2 fois, d'après `ground_truth.json`.
9. [ ] **Vérité terrain** :
   - 100 % des 80 feedbacks ont une entrée complète (type, thèmes, demandes attendues, issue cible, sentiment, risque de churn, pièges).
   - Chaque issue cible existe dans la base, sauf les cibles `NEW:<slug>` (« créer une issue »).
   - Le script de construction ne lit jamais `ground_truth.json` (vérifié par un test).
10. [ ] **Fiction et confidentialité** :
    - Tous les noms et domaines sont inventés ; les adresses e-mail utilisent le domaine réservé `.example`.
    - Aucune vraie personne ni vraie entreprise n'apparaît comme cliente.
    - `workspace_meta` porte la mention « données fictives ».
    - Aucune donnée personnelle tirée de `saxobeat reference/` (CV, candidatures réelles, adresses) n'est réutilisée.
11. [ ] **Tests** : `uv run pytest tests/test_dataset.py` est vert et vérifie les critères 1 à 10 de façon automatisée.
12. [ ] **Relecture** : Vlad relit 10 feedbacks tirés au hasard (graine fixe, listés dans `verify.md`) et les juge crédibles.

## Design in brief

- **Choix retenu** : contenu rédigé à la main par Claude Code dans des fichiers JSON (un fichier par famille d'objets), puis un script Python sans dépendance (`sqlite3`, bibliothèque standard) qui crée le schéma et insère les données dans un ordre stable. Identifiants et dates sont fixés dans les fichiers source, pour un résultat déterministe.
- **Options écartées** :
  - *Générateur à gabarits* (Faker et similaires) : les textes seraient répétitifs et peu crédibles, et la démo perdrait en réalisme.
  - *Appel à un LLM au moment du build* : pas de clé API dans le conteneur, résultat non déterministe, coût à chaque reconstruction.
  - *Vraie API Linear* : exclue par la décision D2.
- **Mécanique Triage** : chaque feedback entrant est une issue en Triage, créée par un utilisateur d'intégration et reliée au client par une `customer_need`. C'est le fonctionnement réel de Linear (« Customer Requests »). L'agent pourra ensuite rattacher le feedback à une issue du backlog (nouvelle `customer_need`, et l'issue de Triage passe en Duplicate) ou proposer une nouvelle issue.
- **Thèmes** : les feedbacks réutilisent les 9 thèmes réels de saxobeat (`docs/analyse/02-contexte-saxobeat.md` §3) et y ajoutent 3 thèmes propres à la projection 2027 :
  - T10 : besoins B2B (tableau de bord du conseiller, invitations en masse, reporting) ;
  - T11 : conversion Free → Plus (paywall, compréhension de l'offre) ;
  - T12 : facturation et compte.
  La répartition est volontairement déséquilibrée (2 ou 3 thèmes dominants), pour que l'agent ait de vraies tendances à détecter.
- **Écriture des feedbacks** : les 4 feedbacks réels de saxobeat servent de modèle de ton et de niveau de détail. Les feedback chat reprennent la structure réelle du cycle 015 (parcours, valeur, impact, fréquence, contexte). Les e-mails et les tickets ont une forme libre, avec objet et signature.

### Pièges à injecter (au moins 2 occurrences chacun)

| # | Piège | Ce que l'agent doit faire |
|---|---|---|
| P1 | Doublons formulés différemment | Les regrouper sous une seule demande |
| P2 | Plusieurs demandes dans un même message | Extraire chaque demande séparément |
| P3 | Bug présenté comme une demande de fonctionnalité (ou l'inverse) | Bien classer le type |
| P4 | Besoins contradictoires entre B2C et B2B | Signaler la tension au PO |
| P5 | Signal de churn chez un compte B2B à fort ARR | Le faire remonter en priorité |
| P6 | Bruit, éloge sans demande | Ne pas en tirer de demande |
| P7 | Demande déjà livrée (issue Done) ou déjà refusée (Canceled) | Rattacher et signaler, sans recréer |
| P8 | Feedback vague, sans demande actionnable | Le classer comme tel ; proposer une question de relance |
| P9 | Même client qui revient plusieurs fois | Compter les clients distincts pour le Reach, pas les messages |

## Interfaces and data

### Fichiers

| Chemin | Rôle | Commité |
|---|---|---|
| `data/seed/workspace.json` | Équipe, utilisateurs, états, étiquettes, initiatives, projets, sprints, métadonnées | oui |
| `data/seed/customers.json` | 60 clients | oui |
| `data/seed/backlog.json` | 30 issues, leurs commentaires et leurs demandes clients historiques | oui |
| `data/seed/feedbacks.json` | 80 feedbacks (issues en Triage + `customer_need`) | oui |
| `data/ground_truth.json` | Réponses attendues, réservées aux évaluations | oui |
| `data/linear.db` | Base construite | oui (décision D3) |
| `data/README.md` | Schéma, provenance, mention « fictif », commande de reconstruction | oui |
| `scripts/build_db.py` | Construction (bibliothèque standard uniquement) | oui |
| `tests/test_dataset.py` | Critères 1 à 10 | oui |
| `pyproject.toml` | Projet uv minimal (Python ≥ 3.12, pytest en dépendance de dev) ; étendu au cycle 002 | oui |

### Schéma SQLite (noms calqués sur l'API Linear, en snake_case)

| Table | Colonnes principales |
|---|---|
| `workspace_meta` | key, value (nom, date de référence 2027-04-12, mention « données fictives », capacité de l'équipe en points par sprint) |
| `teams` | id, key (`SAX`), name |
| `users` | id, name, display_name, email, role (po, dev, design, support, integration), active |
| `workflow_states` | id, team_id, name, type (triage, backlog, unstarted, started, completed, canceled), position |
| `labels` | id, name, color, parent_id (groupes : Type, Module, Canal, Segment) |
| `initiatives` | id, name, description, target_date, status |
| `projects` | id, name, description, state, initiative_id, lead_id, start_date, target_date |
| `cycles` | id, team_id, number, name, starts_at, ends_at |
| `issues` | id, identifier (`SAX-n`), team_id, title, description, state_id, priority (0 aucune, 1 urgente, 2 haute, 3 moyenne, 4 basse), estimate, assignee_id, creator_id, project_id, cycle_id, duplicate_of_id, created_at, updated_at, completed_at, canceled_at, source_type (support_ticket, email, feedback_chat, internal), source_metadata (JSON : expéditeur, objet, parcours du chat, appareil, langue, origine saxobeat…) |
| `issue_labels` | issue_id, label_id |
| `comments` | id, issue_id, user_id, body, created_at |
| `customers` | id, name, domain, segment (b2c, b2b), plan (free, plus, business), revenue_eur (ARR), size, status (active, at_risk, churned), owner_id, created_at |
| `customer_needs` | id, customer_id, issue_id, project_id, body, priority (0 normale, 1 importante), source_type, created_at |

`issue_labels` est une table de liaison et n'entre pas dans le décompte des 12 tables du critère 2.

### `ground_truth.json` (une entrée par feedback)

`identifier`, `language`, `type` (bug, feature_request, improvement, question, praise, noise), `themes` [T1 à T12], `sentiment` (negative, neutral, positive), `churn_risk` (bool), `requests` [{`summary`, `target` : `SAX-n` ou `NEW:<slug>`}], `traps` [P1 à P9], `notes`.

### Commandes

- `uv run python scripts/build_db.py` : (re)construit `data/linear.db`. Écrase le fichier existant, qui est toujours reconstructible.
- `uv run pytest tests/test_dataset.py` : vérifie le jeu de données.

## Constraints

- **Délai** : tout le cycle est livré le samedi 14 au soir ou le dimanche 15 au matin au plus tard. L'échéance finale est le lundi 16 au soir.
- **Taille** : base inférieure à 2 Mo, commitée sans LFS.
- **Confidentialité** : uniquement des données inventées ; domaines `.example` ; rien de personnel tiré de `saxobeat reference/`.
- **Aucune dépendance d'exécution** pour la construction (bibliothèque standard). pytest est la seule dépendance de développement.
- **Fiction assumée** : toute projection 2027 (plans, ARR, comptes B2B) est signalée comme fictive dans `data/README.md`.

## Out of scope

- Le code de l'agent, le faux connecteur Linear côté application (cycle 002) et l'interface (cycle 006).
- L'écriture dans la base par l'agent (au cycle 002 ; la base commitée reste l'état initial de la démo).
- Les traductions ; les vrais fichiers d'export Zendesk ou Gmail.
- Le canal « avis sur les stores d'applications » (saxobeat n'a pas d'application native).

## Gate
- [ ] Owner approved this spec
