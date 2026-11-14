# Plan: jeu de données synthétique

| | |
|---|---|
| **Cycle** | 001 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

## Slices
Thin, ordered, each verifiable alone. Each slice names the acceptance criteria it moves.

| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | Projet uv minimal, schéma SQLite et script de construction (sur des fichiers source vides) | `pyproject.toml`, `scripts/build_db.py` | Le script crée les 12 tables ; `integrity_check` = ok | 1, 2 | done |
| 2 | Espace de travail (équipe, utilisateurs, états, étiquettes, initiatives, projets, sprints, métadonnées) et 60 clients | `data/seed/workspace.json`, `data/seed/customers.json` | Construction OK ; comptages | 5, 6, 10 | done |
| 3 | Backlog : 30 issues, commentaires, demandes clients historiques, origine saxobeat | `data/seed/backlog.json` | Construction OK ; états, priorités, ≥ 20 origines saxobeat | 4, 5 | done |
| 4 | Matrice d'allocation des 80 feedbacks (canal, date, client, langue, type, thèmes, cible, pièges) : le squelette de la vérité terrain | `data/ground_truth.json` (squelette) | Répartitions conformes ; chaque piège ≥ 2 ; cibles existantes | 3, 7, 8, 9 | done |
| 5 | Rédaction des 80 feedbacks à partir de la matrice (3 sous-agents en parallèle, un par canal), puis relecture et fusion par l'agent principal | `data/seed/feedbacks.json`, `data/ground_truth.json` (complété) | Chaque texte respecte sa ligne de matrice (relecture) ; construction OK | 3, 7, 9 | in progress |
| 6 | Tests automatisés et documentation des données | `tests/test_dataset.py`, `data/README.md`, `data/linear.db` | `uv run pytest` vert ; deux constructions → même SHA-256 | 1 à 11 | todo |
| 7 | Vérification et relecture par Vlad de 10 feedbacks (graine fixe) | `verify.md`, `evidence/` | Verdict de Vlad | 12 | todo |

## Order and dependencies

- Le schéma (1) précède les données.
- Les clients et l'espace de travail (2) précèdent le backlog (3), qui y fait référence.
- Le backlog (3) précède la matrice (4), puisque les cibles des feedbacks sont des issues du backlog.
- La matrice (4) précède la rédaction (5) : c'est elle qui garantit les volumes, les pièges et la cohérence entre les 3 sous-agents. Les sous-agents ne choisissent ni les cibles ni les pièges ; ils écrivent le texte.
- Les tests (6) arrivent en dernier, mais le script de construction est lancé à chaque tranche.

## Rollback

- Rien n'est irréversible : aucun service extérieur, et la base est toujours reconstructible depuis `data/seed/`.
- Chaque tranche fait l'objet d'un commit séparé ; un `git revert` du commit suffit pour l'annuler.

## Risks

- **Incohérence entre sous-agents** (ton, identifiants) : la matrice fixe les identifiants ; une relecture et un test de cohérence ont lieu à la fusion.
- **Feedbacks trop « propres »** : consigne de style (fautes de frappe occasionnelles, longueur variable, ton émotionnel réel), d'après les 4 feedbacks réels de saxobeat.
- **Délai** : si la tranche 5 déborde, réduire à 60 feedbacks avec l'accord de Vlad (et noter l'écart au critère 3).

## Gate
- [x] Owner approved the slices (« Go » du 2026-11-14 : Vlad a validé l'enchaînement « j'écris le plan et je le lance dans la foulée »)

## As run
| Heure | Tranche | Ce qui s'est passé |
|---|---|---|
| 2026-11-14 | 1 | Schéma (12 tables + liaison) et script de construction ; essai sur fichiers vides : `integrity_check` = ok |
| 2026-11-14 | 2 | 11 utilisateurs (8 + 3 intégrations), 6 projets, 3 objectifs, 9 cycles (le cycle 8 démarre le 2027-04-12, jour de la démo) ; 60 clients (10 Business, ARR actif 144 600 €) |
| 2026-11-14 | 3 | 30 issues (12/4/4/2/5/3 par état), 28 demandes historiques, 26 origines saxobeat. **Échec rattrapé** : 2 demandes datées avant la création de leur client ; corrigé et ajouté comme test |
| 2026-11-14 | 4 | Matrice de 80 lignes. **Échecs rattrapés** : répartition par canal hors tolérance (chat 35, support 23) → 7 feedbacks changés de canal ; 1 feedback antérieur à son client → date décalée ; **19 étiquettes P9 manquantes dans mes propres annotations** → P9 désormais calculé à partir des données, et un test vérifie la règle |
| 2026-11-14 | 5 | 3 sous-agents lancés en parallèle (support, e-mail, chat), avec la matrice comme consigne contraignante |
