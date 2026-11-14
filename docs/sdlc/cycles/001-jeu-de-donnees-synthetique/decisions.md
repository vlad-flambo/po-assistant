# Decisions: jeu de données synthétique

One entry per decision, newest last. Do not edit old entries: add a new one that supersedes.
Ces décisions de cadrage valent pour tout le projet ; les cycles suivants y renvoient.

## D1. Le PO utilise Linear ; tous les canaux s'y déversent
- **Date:** 2026-11-14
- **Context:** le brief ne précise pas l'outillage du PO. Il faut une hypothèse de stack crédible.
- **Options considered:** Jira, Linear, outil maison.
- **Decision:** Linear. Emails, tickets de support et commentaires arrivent tous dans Linear.
- **Why:** choix de Vlad ; Linear est l'outil courant des startups SaaS et sait relier des demandes clients à des issues.
- **Consequences:** le modèle de données de l'agent reprend les concepts Linear (issues, Triage, customers, customer requests).

## D2. Intégration Linear simulée, branchée sur SQLite
- **Date:** 2026-11-14
- **Context:** une vraie intégration coûterait du temps et un compte, sans valeur pour l'évaluation.
- **Options considered:** API Linear réelle ; mock en mémoire ; base SQLite au format Linear.
- **Decision:** l'agent se comporte comme s'il était connecté à Linear, mais lit et écrit une base SQLite locale.
- **Why:** choix de Vlad ; c'est simple, déterministe en démo et testable.
- **Consequences:** une couche « connecteur Linear » isole l'accès aux données ; une vraie intégration remplacerait cette seule couche (argument d'architecture pour le jury).

## D3. La base SQLite est commitée sur GitHub
- **Date:** 2026-11-14
- **Context:** les données sont entièrement fictives.
- **Options considered:** générer la base au lancement ; la commiter.
- **Decision:** la base est commitée dans le dépôt.
- **Why:** décision de Vlad, par simplicité ; aucun risque de confidentialité puisque rien n'est réel.
- **Consequences:** le jury peut cloner et lancer sans étape de génération. Le script de construction reste versionné pour la reproductibilité.

## D4. Le jeu de données part du projet `Vlad-Flambo/saxobeat`
- **Date:** 2026-11-14
- **Context:** un produit réel rend les feedbacks plus crédibles qu'un produit inventé.
- **Decision:** les feedbacks et le backlog sont dérivés de saxobeat. Le rôle exact de saxobeat reste à trancher (Q1 de `intent.md`).
- **Consequences:** dépend de l'accès au dépôt, refusé sur cette session le 2026-11-14.

## D5. Réponses de Vlad aux questions de l'analyse initiale
- **Date:** 2026-11-14
- **Decision:** échéance lundi 16/11 au soir ; interface web légère ; FR + une part d'EN ; RICE + MoSCoW (WSJF en option) ; pas de vraie intégration Jira/Linear, export Markdown/CSV ; pilotage en cycles ai-sdlc, suivis par le tableau de bord du skill (`docs/sdlc/BOARD.md`).
- **Why:** recommandations de `docs/analyse/01-analyse-initiale.md` §7 acceptées par Vlad.

## D6. La documentation de saxobeat sert de contexte produit et de base d'exemples (complète D4)
- **Date:** 2026-11-14
- **Context:** le dépôt `Vlad-Flambo/saxobeat` reste inaccessible depuis la session ; Vlad a ajouté sa documentation dans `saxobeat reference/docs/`.
- **Decision:** saxobeat est le produit que gère le PO fictif (réponse à Q1). Les PRD, l'étude de concurrence et les 33 cycles sdlc de saxobeat fournissent le contexte de l'application et les exemples à partir desquels on construit feedbacks, clients et backlog.
- **Why:** consigne de Vlad du 2026-11-14 ; un produit réel et documenté rend le jeu de données crédible et défendable devant le jury.
- **Consequences:** le code source n'est pas nécessaire. L'écart avec le brief (« plateforme de gestion de projet ») est à assumer dans la présentation ; la manière de le présenter est tranchée par Q8.
