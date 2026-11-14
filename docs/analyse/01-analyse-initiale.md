# Analyse initiale du challenge « Agent IA au service d'un Product Owner »

> **Source :** [docs/brief/brief.md](../brief/brief.md) · **Date :** 2026-11-14 · **Statut :** première lecture, à valider

---

## 1. Synthèse en 5 points

- **Le vrai sujet n'est pas l'IA, c'est la décision du PO.** Le brief demande un agent qui *aide à décider* (critère « Compréhension métier », 20 %), pas un simple générateur de texte.
- **Trois blocs obligatoires, à enchaîner :** Comprendre (feedbacks) → Arbitrer (priorisation) → Formaliser (user stories). La valeur se trouve dans l'enchaînement et dans la **traçabilité** feedback → fonctionnalité → story.
- **60 % de la note ne porte pas sur le code :** compréhension métier, démarche et présentation pèsent 20 % chacune. Le **journal de démarche** doit commencer dès maintenant.
- **Aucune donnée n'est fournie :** le jeu de données fictif est un livrable caché. Sa qualité conditionne la démo.
- **La proportionnalité est évaluée :** une solution simple, robuste et défendable vaut mieux qu'une architecture complexe (« solution réfléchie […] plutôt qu'une solution parfaite »).

---

## 2. Lecture du besoin métier

### 2.1 Persona et irritants

| Élément | Constat tiré du brief | Conséquence pour l'agent |
|---|---|---|
| Persona | PO d'une startup SaaS (plateforme de gestion de projet) | Vocabulaire produit, pas de jargon technique IA dans l'interface |
| Irritant 1 | Submergé de feedbacks multicanaux (emails, tickets, commentaires) | Ingestion hétérogène, déduplication, synthèse par thèmes |
| Irritant 2 | Backlog à reprioriser **en permanence** | Repriorisation rapide et rejouable (nouveaux feedbacks, poids modifiés) |
| Irritant 3 | Rédaction de user stories chronophage | Génération structurée et éditable, pas une boîte noire |
| Besoin implicite | « L'aider à **prendre ses décisions** » | Recommandations **justifiées et sourcées** ; le PO garde la main (human-in-the-loop) |

### 2.2 Chaîne de valeur cible

1. **Collecter** : feedbacks bruts multicanaux.
2. **Comprendre** : classer (bug / demande / question / éloge), mesurer le sentiment, regrouper par thème, extraire les demandes.
3. **Relier** : rapprocher chaque demande d'un élément existant du backlog, ou créer un nouvel élément.
4. **Arbitrer** : scorer (RICE, MoSCoW…), justifier, permettre au PO d'ajuster.
5. **Formaliser** : produire la user story, ses critères d'acceptation et une estimation.
6. **Exporter** : vers le backlog (Markdown, CSV Jira/Linear…).

> **Fil rouge proposé :** chaque story générée doit pouvoir répondre à la question « pourquoi ? » en citant les feedbacks clients qui la justifient.

---

## 3. Éléments nécessaires : inventaire complet

### 3.1 Données à constituer (prérequis bloquant)

| # | Élément | Contenu minimal | Pourquoi |
|---|---|---|---|
| D1 | **Fiche produit fictive** | Nom, proposition de valeur, modules (tâches, Gantt, équipes…), plans tarifaires | Ancrer l'agent dans un contexte crédible |
| D2 | **Base clients** | 15 à 30 comptes anonymisés : segment (TPE / PME / ETI), plan, ARR, ancienneté | Pondérer le *Reach* et l'impact business (churn) |
| D3 | **Corpus de feedbacks** | 50 à 80 items sur 3 canaux, avec date, client et canal | Matière de la démo |
| D4 | **Backlog existant** | 15 à 25 éléments : statut, estimation, priorité actuelle | Tester le rapprochement et la repriorisation |
| D5 | **Contexte stratégique** | 2 ou 3 objectifs du trimestre (OKR), capacité de l'équipe | Critère d'alignement stratégique, arbitrage sous contrainte |
| D6 | **Vérité terrain** | Thèmes attendus, demandes attendues par feedback | Mesurer la qualité de l'agent (tests / évaluations) |

**Pièges à intégrer volontairement dans D3 pour une démo convaincante :**

- Doublons formulés différemment (même besoin, mots différents).
- Email contenant plusieurs demandes à la fois.
- Bugs déguisés en demandes de fonctionnalité, et inversement.
- Demandes contradictoires entre segments (ex. : simplicité pour les TPE, paramétrage avancé pour les ETI).
- Signaux faibles de churn sur un compte à fort ARR.
- Bruit (messages hors sujet, éloges sans demande).
- Optionnel : mélange français / anglais.

### 3.2 Fonctionnalités à spécifier (les 3 blocs)

#### Bloc A · Comprendre

| Capacité | Attendu du brief | Approfondissement possible |
|---|---|---|
| Ingestion multicanal | Emails, tickets, commentaires | Normalisation vers un schéma unique, anonymisation des données personnelles |
| Motifs et tendances | Motifs récurrents, tendances | Clustering par thème, évolution dans le temps, ventilation par segment ou ARR |
| Extraction des demandes | Demandes de fonctionnalités | Verbatim cité, déduplication, rapprochement avec le backlog |

#### Bloc B · Arbitrer

| Capacité | Attendu du brief | Approfondissement possible |
|---|---|---|
| Scoring multicritère | Différents critères | Poids configurables par le PO |
| Frameworks | MoSCoW, RICE… | RICE + MoSCoW au minimum ; option WSJF ou Valeur / Effort |
| Justification | Expliquer et justifier | Justification qui cite les feedbacks, niveau de confiance, simulation « et si » |

> **Principe d'architecture recommandé :** *le LLM estime les entrées, le code calcule le score.* Le Reach est compté à partir des données ; Impact, Confidence et Effort sont proposés par le LLM avec justification ; le calcul RICE reste déterministe, testable et reproductible.

#### Bloc C · Formaliser

| Capacité | Attendu du brief | Approfondissement possible |
|---|---|---|
| User stories | Structurées selon les standards | « En tant que… je veux… afin de… », contrôle INVEST, découpage d'epic |
| Critères d'acceptation | Pertinents | Format Gherkin (Étant donné / Quand / Alors), cas limites, exigences non fonctionnelles |
| Estimation de complexité | Complexité relative | Points Fibonacci ou tailles de t-shirt, avec justification et hypothèses |

### 3.3 Socle technique (décisions à prendre)

| # | Décision | Options | Recommandation initiale |
|---|---|---|---|
| T1 | Langage | Python, TypeScript | **Python** (écosystème LLM et tests, cohérent avec l'outillage du dépôt) |
| T2 | Modèle LLM | Claude, autres | **Claude**, avec sorties structurées (schémas JSON / tool use) |
| T3 | Forme d'agent | Pipeline fixe / agent conversationnel avec outils / hybride | **Hybride** : outils déterministes (ingérer, analyser, scorer, rédiger) orchestrés par un agent conversationnel |
| T4 | Interface (UX 15 %) | CLI, Streamlit, application web, Slack | **Application web légère** : chat + vues (tableau de bord des thèmes, backlog scoré, éditeur de story) |
| T5 | Stockage | Fichiers JSON, SQLite | **JSON ou SQLite** : proportionné, sans infrastructure |
| T6 | Tests | Unitaires, évaluations LLM | Unitaires sur le déterministe (scoring, parsing) + **évaluations** sur la vérité terrain (D6) + LLM simulé (mock) pour la CI |
| T7 | Export | Markdown, CSV, API Jira/Linear | **Markdown + CSV** ; une intégration API seulement en bonus |
| T8 | Fiabilité de la démo | Live, cache, vidéo | Live + **cache des réponses** + **vidéo de secours** |

### 3.4 Documentation (critère Démarche, 20 %)

- **Journal de démarche** tenu au fil de l'eau : hypothèses, itérations, impasses abandonnées.
- **Registre IA** : ce qui a été délégué aux assistants IA, et comment chaque production a été vérifiée.
- **Décisions techniques** (ADR courts) : choix, alternatives écartées, justification.
- **README** : installation, lancement, scénario de démo.
- **Outil disponible :** le skill `ai-sdlc` déjà présent dans le dépôt (cycles intent → spec → plan → build → verify → learn) produit exactement cette trace. Il est recommandé de l'activer dès maintenant.

### 3.5 Présentation (20 %)

| Séquence | Durée | Éléments à préparer |
|---|---|---|
| Démonstration | 10 min | Scénario narratif (ex. : « le lundi matin du PO ») qui enchaîne les 3 blocs sur les mêmes données |
| Architecture | 5 min | 1 schéma + 3 choix clés justifiés |
| Démarche & difficultés | 5 min | 2 ou 3 impasses réelles et la façon dont elles ont été résolues |
| Questions | 10 min | Fiche de réponses : hallucinations, coût, montée en charge, contrôle de l'IA, limites |
| Transverse | – | Support de présentation, vidéo de secours, données de démo figées |

---

## 4. Correspondance avec les critères d'évaluation

| Critère | Poids | Éléments qui y répondent | Levier différenciant |
|---|---|---|---|
| Compréhension métier | 20 % | D1–D5, chaîne de valeur, human-in-the-loop | Pondération par ARR / risque de churn, alignement OKR |
| Démarche | 20 % | Journal, registre IA, ADR | Cycles `ai-sdlc` avec preuves |
| Qualité technique | 15 % | T1–T7, tests, évaluations | « Le LLM estime, le code calcule » |
| Expérience utilisateur | 15 % | T4, export, édition | Traçabilité cliquable feedback → story |
| Complétude | 10 % | 3 blocs couverts en profondeur | Simulation « et si » sur les poids |
| Présentation | 20 % | Scénario, support, fiche Q&R | Démo narrative de bout en bout |

---

## 5. Registre des risques initial

| # | Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Sur-ingénierie (critère de proportionnalité) | Élevée | Moyen | Périmètre MVP figé avant le build ; bonus seulement après |
| R2 | Données fictives trop « propres », démo peu crédible | Moyenne | Élevé | Pièges volontaires (§3.1) ; relecture critique du corpus |
| R3 | Non-déterminisme du LLM en démo live | Moyenne | Élevé | Sorties structurées, température basse, cache, vidéo de secours |
| R4 | Hallucinations (demandes ou chiffres inventés) | Moyenne | Élevé | Citations obligatoires des feedbacks sources ; calculs en code |
| R5 | Démarche non documentée a posteriori | Élevée | Élevé | Journal tenu dès J1 |
| R6 | Dépassement du temps de démo (10 min) | Moyenne | Moyen | Scénario minuté, répétitions |
| R7 | Dépendance réseau / API le jour J | Faible | Élevé | Mode hors ligne avec réponses en cache |

---

## 6. WBS de haut niveau (proposition)

1. **Cadrage**
   1. Valider cette analyse et les décisions ouvertes (§7)
   2. Initialiser `docs/sdlc` et le journal de démarche
2. **Données**
   1. Fiche produit + base clients + contexte stratégique (D1, D2, D5)
   2. Corpus de feedbacks avec pièges (D3)
   3. Backlog existant (D4)
   4. Vérité terrain (D6)
3. **Agent : MVP**
   1. Socle : schémas de données, client LLM, stockage
   2. Bloc A · Comprendre
   3. Bloc B · Arbitrer
   4. Bloc C · Formaliser
   5. Interface
4. **Qualité**
   1. Tests unitaires
   2. Évaluations sur la vérité terrain
5. **Approfondissements** (selon le temps disponible) : simulation « et si », export Jira/Linear, tendances temporelles
6. **Restitution**
   1. Documentation finale (démarche, ADR, README)
   2. Support de présentation et schéma d'architecture
   3. Scénario de démo, vidéo de secours, fiche Q&R
   4. Répétitions minutées

---

## 7. Décisions (arbitrées par Vlad le 2026-11-14)

| # | Question | Recommandation | Décision |
|---|---|---|---|
| Q1 | Date de restitution et temps disponible ? | À préciser | **Lundi 16/11 au soir** |
| Q2 | Interface ? | Web app légère (chat + vues) | **Oui** |
| Q3 | Langue de l'agent et des données ? | FR, corpus partiellement bilingue | **Oui** |
| Q4 | Frameworks de priorisation ? | RICE + MoSCoW ; WSJF en option | **Oui** |
| Q5 | Intégration réelle à un outil ? | Non ; export CSV / Markdown | **Oui** : Linear est simulé, branché sur SQLite |
| Q6 | Piloter avec le skill `ai-sdlc` ? | Oui | **Oui** : `docs/sdlc/` |
| Q7 | Kanban ou Gantt ? | Selon la date | **Tableau de bord des cycles `ai-sdlc`** (`docs/sdlc/BOARD.md`) |

### Hypothèses de travail ajoutées (Vlad, 2026-11-14)

- Le PO utilise **Linear** ; emails, tickets et commentaires s'y déversent tous.
- **Pas de vraie intégration** : l'agent fait comme s'il était connecté à Linear, mais lit une **base SQLite**.
- Le jeu de données synthétique est **dérivé du projet GitHub `Vlad-Flambo/saxobeat`**.
- Les données étant fictives, la **base SQLite est commitée sur GitHub**.

Suivi détaillé : `docs/sdlc/cycles/001-jeu-de-donnees-synthetique/decisions.md`.
