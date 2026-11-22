# Démarche et choix techniques

> Livrable n° 2 du test. Le journal chronologique détaillé est dans [journal.md](journal.md). Chaque étape a laissé un dossier dans [sdlc/cycles/](sdlc/cycles/) (intention, spec, plan, vérification), avec un tableau de bord dans [sdlc/BOARD.md](sdlc/BOARD.md).

## 1. Le problème, vu du Product Owner

| Constat du brief | Ce que j'en ai retenu | Réponse de l'agent |
|---|---|---|
| Le PO est submergé de feedbacks multicanaux | Le volume n'est pas le seul problème : un même besoin revient sous des formes différentes, par des canaux différents, de clients qui ne pèsent pas pareil | Chaque feedback est relié à un besoin unique (issue existante ou nouveau besoin), avec la citation qui le prouve. On compte des **clients distincts**, pas des messages |
| Le backlog est à reprioriser en permanence | Reprioriser coûte cher parce que les preuves sont dispersées. Le PO doit pouvoir rejouer un arbitrage en quelques secondes | Les scores sont **calculés** (donc rejouables) à partir d'estimations **modifiables**. Le PO peut régler les poids (« et si… ») et voir le sprint proposé dans la capacité restante |
| Le PO a besoin d'aide pour **décider** | L'agent recommande, le PO décide. Une recommandation sans justification ne sert à rien | Chaque estimation porte une justification sourcée. Rien n'est écrit dans Linear sans un clic du PO |

**Fil rouge :** chaque user story peut répondre à « pourquoi ? » en remontant jusqu'aux feedbacks clients qui la fondent.

## 2. Hypothèses posées

| Hypothèse | Décidée par | Pourquoi |
|---|---|---|
| Le produit du PO est **saxobeat**, mon projet de suivi de recherche d'emploi, **projeté au printemps 2027** (offres Free / Plus / Business) | Vlad | Un vrai produit, documenté par 7 PRD et 33 cycles, rend les données crédibles. La projection fournit des clients payants, des segments et du volume, ce qu'attend le brief (« startup SaaS ») |
| Le PO travaille dans **Linear**, et tous les canaux s'y déversent (file Triage, demandes clients) | Vlad | Outil courant des startups ; il relie nativement une demande client à une issue |
| **Pas de vraie intégration** : une base SQLite au format Linear, versionnée | Vlad | Démo déterministe ; un seul module à remplacer pour passer au vrai Linear |
| D'abord **pas d'API de LLM** (un skill Claude Code traite des fichiers exportés), puis **l'API par défaut (Mistral ou Claude), le skill en repli** | Vlad | Le skill a permis de livrer vite, sans clé, sur une architecture éprouvée sur saxobeat. L'API est ensuite devenue le comportement par défaut, comme dans une vraie intégration ; Mistral a été ajouté parce que c'est la clé disponible (cycle 013) ; le skill reste le repli sans clé |
| Le PO pense en RICE et MoSCoW, avec des OKR trimestriels et une capacité de 20 points par sprint | Recommandation acceptée | Les frameworks cités par le brief, appliqués à un contexte crédible |

## 3. Le chemin suivi

Le travail a été mené en **cycles courts** (méthode `ai-sdlc` : intention → spec → plan → construction → vérification → apprentissage), avec la validation de Vlad à chaque porte.

| Cycle | Résultat | Points saillants |
|---|---|---|
| Analyse | Lecture du brief, inventaire des éléments nécessaires | 60 % de la note porte sur autre chose que le code : le journal de démarche a été ouvert dès le premier jour |
| 001 · Données | 80 feedbacks, 30 issues, 60 clients, vérité terrain, 11 tests | Feedbacks **définis avant d'être écrits** (matrice : canal, client, cible, pièges), puis rédigés par 3 agents en parallèle |
| 002 · Socle | Échange de fichiers, faux connecteur Linear, skill `po-agent` | Vérification avant import, citations obligatoires, import idempotent, fichiers partiels acceptés |
| 003 · Comprendre | Agrégats (besoins, thèmes, tendances, alertes) et évaluation | Vrai passage du skill sur les 80 feedbacks, mesuré contre la vérité terrain |
| 004 · Arbitrer | Pack priorisation, RICE, score pondéré, plan de sprint | L'IA estime, le code calcule |
| 005 · Formaliser | Pack rédaction, publication dans Linear, exports | Stories reliées à leurs preuves |
| 006 · Interface | Streamlit, 7 pages | Testée sans navigateur (AppTest) |

### Ce qui a été essayé puis abandonné

| Idée de départ | Pourquoi elle a été abandonnée | Ce qui l'a remplacée |
|---|---|---|
| Lire le code de saxobeat sur GitHub | Dépôt inaccessible depuis la session cloud | La documentation produit fournie par Vlad, synthétisée dans [analyse/02-contexte-saxobeat.md](analyse/02-contexte-saxobeat.md) |
| Clé API Anthropic pour la démo en direct | Décision de Vlad : pas d'API, pour tenir le délai | Skill Claude Code et échange de fichiers ; l'API est revenue ensuite comme moteur par défaut, le skill en repli, la démo simulant le flux API |
| Un chat dans l'interface | Impossible sans API, et contraire au contrôle du PO | Des vues qui montrent les preuves ; la conversation a lieu dans Claude Code |
| Générer les feedbacks par gabarits (Faker) ou par LLM au build | Textes répétitifs ; pas de clé ; résultat non déterministe | Matrice d'allocation, puis rédaction par des agents, figée dans des fichiers JSON |
| Étiqueter à la main les « clients qui reviennent » | J'en avais oublié 19 sur 43 | Une règle calculée à partir des données, et testée |
| Reach = sièges Business, sans alternative | Biais découvert à l'usage : un compte de 300 sièges écrase tous les besoins B2C | Une bascule « personnes » / « clients » qui rend l'arbitrage B2B / B2C visible |
| FastAPI + HTMX (comme saxobeat) | Trop long pour l'échéance | Streamlit, proportionné au besoin |

## 4. Ce que j'ai délégué à l'IA, et comment je l'ai contrôlé

| Délégué | À qui | Contrôle |
|---|---|---|
| Transcription du brief PDF | Claude Code | Relecture face au PDF |
| Synthèse des 33 cycles saxobeat | Sous-agent | Citations vérifiées par sondage dans les fichiers sources |
| Rédaction des 80 feedbacks | 3 sous-agents, un par canal | Les faits étaient imposés par la matrice. Script de fusion avec contrôle des identifiants et des langues, recherche de fuites de la vérité terrain dans les textes, 11 tests, relecture d'un échantillon. Les sous-agents ont signalé 3 incohérences dans **mes** données |
| Analyse, priorisation et rédaction (le travail de l'agent lui-même) | Le skill `po-agent`, dans des sessions qui n'ont jamais vu la vérité terrain | Validation automatique à l'import (format, cibles, **citations exactes**), puis mesure contre la vérité terrain |
| Le code (connecteur, packs, scores, interface) | Claude Code, sous ma direction | 71 tests automatisés ; chaque étape a été validée par Vlad aux portes des cycles |

**Ce que j'ai vérifié moi-même, et ce qui reste hors vérification :** voir les fichiers `verify.md` des cycles. En résumé : 5 textes de feedbacks lus en entier par l'agent principal, 10 soumis à Vlad ; la qualité de la priorisation et de la rédaction est jugée sur pièces (pas de vérité terrain pour elles).

## 5. Choix techniques

| Choix | Motif | Alternative écartée |
|---|---|---|
| **Python + SQLite + Streamlit** | Le plus court chemin vers un outil utilisable ; une seule langue ; zéro infrastructure | Application web complète (FastAPI, React) : disproportionnée pour un test |
| **Faux connecteur Linear** (`LinearClient`) | Le reste de l'application ignore SQLite ; se brancher sur le vrai Linear ne demande de remplacer qu'un module (API GraphQL) | Lire SQLite partout : pas de couture pour l'intégration |
| **Packs auto-suffisants** (« le fichier est le skill ») | N'importe quel agent peut les traiter ; aucune configuration côté agent ; versionnés par instructions | Prompts dispersés dans le code |
| **« L'IA estime, le code calcule »** | Reach, RICE, ARR et tendances sont exacts et rejouables ; le LLM ne fait que du jugement, toujours justifié | Demander le score au LLM : non reproductible, non auditable |
| **Citations obligatoires et vérifiées** | Bloque les demandes inventées ; rend chaque besoin traçable jusqu'au client | Faire confiance au résumé |
| **Vérité terrain séparée** | Permet de **mesurer** l'agent (84 % de types justes, 98 % de rattachements justes) au lieu de l'affirmer | Évaluation au jugé |
| **Base de travail séparée** (`data/workspace/`) | La démo n'altère jamais les données versionnées ; on réinitialise d'un clic | Écrire dans la base du dépôt |

## 6. Limites et suite

- **Moteur API essayé pour de vrai sur un petit lot seulement** : les deux fournisseurs (Mistral, Claude) sont testés avec un client simulé (découpage, schémas, refus, erreurs, essais, coût). Essai réel le 2026-11-22 avec la clé Mistral de Vlad (cycle 013) : 5 analyses par Mistral Large, schéma imposé accepté en mode strict, import sans refus, 0,03 $, 1 min 15 s. Pas encore mesurés : la qualité de Mistral, un lot complet, le moteur Claude en réel (pas de clé). Les tarifs Mistral affichés restent des estimations. Le repli sur le skill protège l'usage si l'appel échoue.
- **Temps de traitement** : avec le skill, un pack de 80 feedbacks prend quelques minutes ; en démo, le flux API simulé dure environ 8 secondes.
- **Priorisation et rédaction sans vérité terrain** : leur qualité se juge sur pièces. La suite serait de comparer les classements de l'agent aux décisions réelles du PO.
- **Reach** : le compter en personnes ou en clients est un vrai choix produit, laissé au PO. Une pondération par segment, fixée en équipe, serait plus juste.
- **Passage au réel** : remplacer `LinearClient` par le client GraphQL de Linear, et brancher la file Triage sur les vrais canaux (Zendesk, e-mail, chat intégré).
