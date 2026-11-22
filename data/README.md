# Données : espace Linear fictif « saxobeat · printemps 2027 »

> **Données entièrement fictives.** saxobeat est un vrai projet personnel (un suivi de recherche d'emploi, synthèse de sa documentation dans `docs/analyse/02-contexte-saxobeat.md`). Sa projection au printemps 2027 est inventée pour ce test : offres Free, Plus et Business, clients, équipe, chiffres. Les noms de personnes et d'entreprises clientes sont inventés, et toutes les adresses utilisent le domaine réservé `.example`. Les employeurs cités comme *sources d'offres* (Capgemini, Accenture, LinkedIn…) ne sont pas des clients.

## Ce que contient la base

`linear.db` (SQLite) imite un espace de travail Linear, figé au **lundi 12 avril 2027**, premier jour du cycle 8 :

| Élément | Volume | Détail |
|---|---|---|
| Feedbacks en **Triage** | 80 | Du 1er février au 11 avril 2027. Répartis en 28 tickets de support (Zendesk), 24 e-mails et 28 messages du feedback chat. 15 sont en anglais. Chacun est relié à son client par une demande client (`customer_needs`) |
| Backlog | 30 issues | États Backlog, Todo, In Progress, In Review, Done et Canceled. 26 sont dérivées du vrai backlog de saxobeat (`source_metadata.origin`) |
| Demandes clients historiques | 28 | Antérieures au 1er février, rattachées aux issues du backlog |
| Clients | 60 | 10 comptes Business (cabinets d'outplacement, écoles, coachs) avec ARR, dont 2 à risque et 1 perdu ; 50 candidats (29 Free, 21 Plus) |
| Contexte | – | 3 objectifs (initiatives), 6 projets, des cycles de 2 semaines, une équipe de 8 personnes, une capacité de 20 points par cycle (`workspace_meta`) |

### Schéma

Les tables reprennent les noms de l'API Linear (en snake_case) : `teams`, `users`, `workflow_states`, `labels`, `initiatives`, `projects`, `cycles`, `issues`, `issue_labels`, `comments`, `customers`, `customer_needs`, ainsi que `workspace_meta` pour le contexte (date de référence, offres, métriques, capacité). Le schéma complet est dans `scripts/build_db.py`.

- **Priorité** (convention Linear) : 0 aucune, 1 urgente, 2 haute, 3 moyenne, 4 basse.
- **Estimation** : points Fibonacci.
- **`issues.source_type`** : `support_ticket`, `email`, `feedback_chat` (feedbacks entrants) ou `internal` (backlog).
- **`issues.source_metadata`** (JSON) :
  - ticket : expéditeur, numéro ZD ;
  - e-mail : expéditeur, objet ;
  - feedback chat : parcours idée / problème / avis, page, appareil, mode, réponses ;
  - backlog : origine dans saxobeat.

## Reconstruire et vérifier

```bash
uv run python scripts/build_db.py          # reconstruit data/linear.db depuis data/seed/
uv run pytest tests/test_dataset.py        # vérifie volumes, cohérence, pièges, fiction
```

La construction n'utilise que la bibliothèque standard et produit un résultat déterministe : deux constructions donnent le même dump SQL. La base est commitée (décision D3) pour qu'on puisse cloner et lancer sans étape de génération.

## Fichiers

| Fichier | Rôle |
|---|---|
| `seed/workspace.json` | Équipe, utilisateurs, états, étiquettes, objectifs, projets, cycles, contexte |
| `seed/customers.json` | Clients |
| `seed/backlog.json` | Issues du backlog, commentaires, demandes historiques |
| `seed/feedbacks.json` | Feedbacks entrants (deviennent des issues en Triage) |
| `ground_truth.json` | **Réservé aux évaluations** : réponse attendue pour chaque feedback (type, thèmes, demandes et issue cible, sentiment, risque de churn, pièges). Jamais chargé dans la base ni montré à l'agent |

## Comment le jeu a été construit

1. **Contexte** : la documentation de saxobeat (PRD, étude de concurrence, 33 cycles) a été synthétisée dans `docs/analyse/02-contexte-saxobeat.md`.
2. **Backlog** : dérivé des cycles et des registres réels de saxobeat, puis complété par la projection 2027 (offre Business, paywall).
3. **Matrice d'allocation** : chaque feedback a été défini avant d'être écrit (canal, client, date, langue, type, thèmes, issue cible, pièges). Cela garantit les volumes et la vérité terrain.
4. **Rédaction** : 3 agents IA, un par canal, ont rédigé les textes à partir de cette matrice, sans pouvoir modifier les faits. L'agent principal a relu et fusionné leurs textes.
5. **Vérification** : tests automatisés et relecture humaine d'un échantillon (voir `docs/sdlc/cycles/001-jeu-de-donnees-synthetique/verify.md`).

### Les 9 pièges injectés (détail dans `ground_truth.json`)

1. Doublons formulés différemment.
2. Plusieurs demandes dans un même message.
3. Bug présenté comme une demande, ou l'inverse.
4. Besoins contradictoires entre B2C et B2B.
5. Signal de churn d'un compte Business.
6. Bruit ou éloge sans demande.
7. Demande déjà livrée ou refusée.
8. Feedback vague.
9. Client qui revient plusieurs fois.
