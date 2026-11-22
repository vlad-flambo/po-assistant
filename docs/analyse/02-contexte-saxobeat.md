# Contexte produit : saxobeat

> **Sources :** documentation interne de saxobeat (7 PRD et études, 33 cycles sdlc), retirée du dépôt public le 2026-11-22 pour confidentialité : cette synthèse en tient lieu, les noms de fichiers cités sont ceux de cette documentation · **Date :** 2026-11-14 · **Usage :** contexte de l'application et base d'exemples pour le jeu de données (cycle 001, décision D6)
> Les PRD ont été lus directement ; les cycles ont été synthétisés par un sous-agent, et ses citations ont été vérifiées par sondage (cycles 017, 021, 015).

---

## 1. Le produit en bref

| Élément | Constat | Source |
|---|---|---|
| Proposition de valeur | « Every Paris job that fits you — straight from employers' own sites, scored in a way you can read, and followed through to the interview. No spam, no auto-apply. » | `COMPETITION.md` §8 |
| Problème | Une recherche d'emploi large produit beaucoup de bruit ; vérifier chaque site à la main est lent, et on perd le fil de ce qu'on a vu, écarté ou postulé | `PRD.md` §1 |
| Flux cœur | Sources → normalisation → dédoublonnage → filtres durs → score → Inbox → Pipeline | `PRD.md` §6 |
| Stade | Alpha hébergée, sur invitation (codes d'invitation depuis le 2026-11-06), gratuite | `PRD_multi_user.md`, cycle 033 |
| Plateforme | Web app Django, pensée d'abord pour le téléphone (installable), en français et en anglais ; Render + Neon (offre gratuite) ; e-mails via Brevo | `DEPLOY.md`, cycles 003 et 025 |
| Volumétrie réelle | ~30 000 offres, ~325 sources, 2 à 4 candidats actifs (l'objectif de l'alpha est de 10 à 30) | cycles 022 et 033, `PRD_multi_user.md` |

### Rôles

| Rôle | Qui | Ce qu'il fait |
|---|---|---|
| Candidat, mode **standard** | Amis, premiers utilisateurs | Inbox courte, page offre, pipeline, entretiens |
| Candidat, mode **power** | Utilisateurs avancés | En plus : mots-clés et poids, Insights, recalcul des scores |
| **Opérateur** | Le fondateur | Console `/ops/` : candidats, sources, exécutions, feedback, back office IA |

### Modules (vocabulaire réutilisable pour les feedbacks et le backlog)

- **Inbox** : offres scorées ; balayage (swipe) sur téléphone, raccourcis clavier sur ordinateur.
- **Page offre** : bloc « Why this score », carte IA, blocage d'un employeur, demande de recommandation.
- **Pipeline** : statuts de New à Offer, relances, rejet automatique après un mois de silence.
- **Entretiens** : cheat sheet par entretien.
- **Entreprises et contacts** : employeurs favoris ou bloqués, contacts importés de LinkedIn.
- **Insights** : apprentissage à partir des décisions du candidat.
- **Réglages** : villes, CV, mots-clés.
- **Onboarding** : import du CV, puis conversation « ce que je cherche ».
- **Sources** : connecteurs vers les systèmes de recrutement (Greenhouse, Lever, Workday…), lien collé, bookmarklet, partage depuis Android.
- **Back office IA** : packs de fichiers traités par un agent ; promesse de résultat « sous 24 h ».
- **E-mails** : invitation, réinitialisation, résultats IA.

---

## 2. Canaux de feedback existants (modèle pour le jeu de données)

**Feedback chat intégré** (cycle 015) : un bouton sur chaque page ouvre une conversation scriptée, sans IA.

| Parcours | Questions (5 étapes) | Échelles |
|---|---|---|
| **Idée** | Ce que vous voulez · valeur · ce que vous faites aujourd'hui · fréquence · autre chose | Valeur : Nice to have / chaque semaine / chaque jour / je ne peux pas m'en passer |
| **Problème** | Ce qui s'est passé · où · impact · fréquence · autre chose | Impact : petite gêne / me ralentit / je n'ai pas pu faire ce que je voulais. Fréquence : à chaque fois / parfois / une fois |
| **Avis** | Quel espace · valeur · ce qui marche · ce que vous changeriez · autre chose | Valeur sur 5 niveaux |

- **Contexte joint automatiquement** : page, offre ou entreprise concernée, téléphone ou ordinateur, mode, langue, date.
- **Côté console** : chaque feedback a un état (new, read, turned into a cycle) et un bouton « Copy as intent draft ».

**Les 4 feedbacks réels enregistrés** (tous émis par le fondateur ; aucun ami n'a encore utilisé le bouton) :

| # | Type | Citation (verbatim) | Devenu |
|---|---|---|---|
| 1 | Problème, Inbox | « remove the shortcuts explanation, takes too much space and limited value » | Cycle 017 (écarté) |
| 3 | Idée, Inbox | « Add consulting employers / Example / https://careers.bcg.com/… », avec « I can't do without it » | Cycle 013 |
| 4 | Problème, page offre | « This job is a match, but deterministic score is only 33 […] DO job descriptions in French get consistently underscored because there are less keyword matches ? » | Cycle 021 |
| 5 | Problème, page offre | « The information i shouldn't be always on by default on the AI section. It's not very practical » | Cycle 023 |

> **Conséquence :** la structure du feedback chat (type, valeur, impact, fréquence, contexte) est un excellent modèle pour le canal « commentaires » du brief. Elle fournit aussi des signaux directement utilisables pour RICE (Reach, Impact).

---

## 3. Thèmes récurrents (base des motifs à injecter dans les feedbacks)

| # | Thème | Exemples réels | Cycles |
|---|---|---|---|
| T1 | Pertinence du score : faux négatifs, scores pas à jour | Offre en français scorée 33 malgré un entretien obtenu | 008, 021, 029, 031 |
| T2 | Couverture des sources | Cabinets de conseil, fintechs, Revolut, alertes e-mail | 013, 018, 020 |
| T3 | Irritants d'interface et fonctions difficiles à trouver | Blocage d'un employeur « un-intuitive », aide trop présente | 016, 017, 023, 011 |
| T4 | Le mode standard en retard sur le mode power | Villes non modifiables, recalcul réservé au mode power | 029, 030, 011 |
| T5 | Suivi des candidatures | Employeurs silencieux, offres republiées, relances | 019, 022, 009, 010 |
| T6 | Mobile jamais testé sur un vrai téléphone | Gestes, mise en page | 005, 010 |
| T7 | Fiabilité et performance | Suppression d'un compte qui expire (40,9 s), blocage de l'hébergement | 014, 022, 032 |
| T8 | Notifications et e-mails | Rappels, résultats IA, e-mails classés en spam (iCloud) | 003, 009 |
| T9 | Délai et transparence de l'IA | Promesse « sous 24 h », explication du score | 008, 023, `PRD_ai_backoffice.md` |

---

## 4. Backlog existant (base des issues Linear)

- **33 cycles** avec type, importance (1 à 5) et statut : un modèle direct pour des issues avec priorité et état.
- **`backlog.md` et registres des PRD** : lancement automatique de l'agent, fraîcheur des fiches entreprises, dossier de candidature, choix du mode par le candidat, recherche plein texte, vue trajet domicile-travail, connecteur MCP, pré-remplissage assisté, etc.
- **18 fonctionnalités repérées chez les concurrents** avec leur effort estimé en S / M / L (`COMPETITION.md` §7) : une base pour les estimations de complexité.

## 5. Éléments de marché (pour les segments et la pondération)

| Élément | Valeur | Source |
|---|---|---|
| Prix du marché | 20 à 40 $ par mois ; abonnements trimestriels ; crédits pour ce que l'IA rédige | `COMPETITION.md` §6.3 |
| Prix envisagé pour saxobeat | 9 à 15 € par mois, ou 29 à 39 € par trimestre | `COMPETITION.md` §6.5 |
| Outplacement (B2B potentiel) | 3 000 à 25 000 € par personne, généralement payé par l'employeur | `COMPETITION.md` §6.4 |
| Concurrents clés | LinkedIn Job Match, Welcome to the Jungle, Jobright, Useful Apply, LoopCV, Talya | `COMPETITION.md` §2 |
| Contraintes | RGPD, pas d'auto-candidature, pas de scraping de LinkedIn | `COMPETITION.md` §9, `PRD_competitive_features.md` §3 |

## 6. Écart avec le brief et options de présentation

- **Le brief** décrit « une startup SaaS [qui] développe une plateforme de gestion de projet ». **saxobeat** est un outil de suivi de recherche d'emploi en alpha gratuite.
- **Point commun défendable :** une recherche d'emploi se pilote comme un projet (pipeline par étapes, échéances, relances, tableau de bord).
- **Ce qui manque à saxobeat pour coller au brief :** une base de clients payants, des segments et du volume. C'est l'objet de la question Q8 du cycle 001 (horizon fictif).
