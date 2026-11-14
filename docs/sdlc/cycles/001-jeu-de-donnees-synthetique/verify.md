# Verify: jeu de données synthétique

| | |
|---|---|
| **Cycle** | 001 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |
| **Date** | 2026-11-14 |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence (command and output, measurement, screenshot, link) |
|---|-----------|--------|-------------------------------------------------------------|
| 1 | Construction reproductible | pass | `test_build_is_deterministic_and_committed_db_is_current` : deux constructions donnent le même dump, identique à la base commitée. SHA-256 du dump : `b02dbfc7…592d87` ; base de 292 Ko |
| 2 | Schéma et intégrité | pass | `test_schema_and_integrity` : 12 tables + `issue_labels` ; `integrity_check` = ok ; `foreign_key_check` vide |
| 3 | 80 feedbacks en Triage, répartition par canal, une demande client chacun | pass | `test_feedbacks` : 80 ; 28 support / 24 e-mail / 28 chat ; dates du 2027-02-01 au 2027-04-11 |
| 4 | Backlog de 30 issues | pass | `test_backlog` : 12/4/4/2/5/3 par état ; un type par issue ; estimations présentes en Todo, In Progress et In Review ; 26 origines saxobeat |
| 5 | Clients et demandes historiques | pass | `test_customers` : 60 clients (10 Business, 29 Free, 21 Plus) ; 28 demandes historiques ; aucune demande antérieure à la création de son client |
| 6 | Contexte | pass | `test_context` : 3 objectifs, 6 projets, cycles de 14 jours contigus, le cycle 8 contient le 2027-04-12, 8 + 3 utilisateurs, capacité de 20 points |
| 7 | Langue | pass | `test_languages` : 15 en anglais, 65 en français, conformes à la vérité terrain |
| 8 | Pièges ≥ 2 chacun | pass | `test_traps` : P1 27, P2 6, P3 4, P4 4, P5 4, P6 5, P7 4, P8 3, P9 43 ; `test_p9_matches_data` vérifie la règle de P9 |
| 9 | Vérité terrain complète et isolée | pass | `test_ground_truth` : 80 entrées, cibles valides (issues existantes ou `NEW:<slug>`), aucune demande pour le bruit et le vague ; le script de construction ne lit pas le fichier |
| 10 | Fiction et confidentialité | pass | `test_fiction_and_privacy` : toutes les adresses et domaines en `.example` ; mention « fictives » ; aucun terme personnel issu de `saxobeat reference/` (liste de termes interdits) |
| 11 | Tests verts | pass | `uv run pytest tests/test_dataset.py` : 11 passed in 0.15s ([evidence/pytest_2026-11-14.txt](evidence/pytest_2026-11-14.txt)) |
| 12 | Relecture de 10 feedbacks par Vlad | pending | Échantillon (graine 2027) : [evidence/echantillon_relecture.md](evidence/echantillon_relecture.md) — SAX-202, 211, 214, 224, 242, 245, 252, 260, 274, 275 |

## Tests
- `uv run pytest tests/test_dataset.py` : 11 tests, tous verts.
- Contrôle complémentaire hors test : aucune note de la matrice (« SAX- », piège, « limite Free »…) n'apparaît dans les textes des feedbacks. Longueur des textes : de 24 à 1 438 caractères, médiane 310.

## Not verified
- **Crédibilité des 80 textes** : seuls les 10 de l'échantillon sont relus par Vlad. Pendant la fusion, l'agent principal n'a lu que 5 textes : SAX-201, 220, 221, 228, 236.
- **Fidélité de chaque texte à sa ligne de matrice** : contrôlée par les comptes rendus des 3 sous-agents et par sondage, pas texte par texte. Une divergence éventuelle se verra aux évaluations des cycles 003 à 005, où un écart entre l'agent et la vérité terrain sera examiné au cas par cas.
- **Conformité au modèle de données Linear** : les noms de tables et de champs ont été choisis de mémoire. Seule l'existence de `Customer` et `CustomerNeed` a été vérifiée dans la documentation de Linear.

## Écarts relevés par les sous-agents (et suites)
- 3 clients avaient une offre incohérente avec leur message (Free mais recevant l'analyse IA ; Free demandant à résilier Plus) : passés en Plus (Lukas M., Mélanie C., Émilie D.).
- SAX-266 : le client annonce résilier Plus mais reste `at_risk`, car l'abonnement court jusqu'à la fin de la période. Conservé.
- SAX-222 : Rebond Cadres IDF est `churned` au 12 avril, après une non-reconduction annoncée pour fin mars. Cohérent, conservé.
- Numéros de tickets ZD : une inversion d'ordre le 25 mars (SAX-257 et SAX-258). Sans effet, conservée.

## Verdict
- [ ] Accepted by owner
- [ ] Sent back (what, to which stage)
