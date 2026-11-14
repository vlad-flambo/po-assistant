# PRD — Saxobeat multi-utilisateur (phase suivante)

| | |
|---|---|
| **Statut** | Phases 1 à 6 **construites** (code, tests, vérifications locales) ; **rien n'est encore déployé** chez l'hébergeur. Questions du §12 : 1 et 4 tranchées, 2 et 3 en attente. |
| **Date** | 8 octobre 2026 (mis à jour le 12 octobre 2026) |
| **Auteur** | Vladimir (produit), rédigé avec Claude |
| **Portée** | Passer d'une appli mono-utilisateur locale à une appli hébergée pour 10 à 30 personnes (amis, premiers utilisateurs) |

---

## Travail restant (déplacé vers les cycles SDLC le 2026-10-29)

Ce que ce PRD demande encore est suivi sous forme de cycles dans `docs/sdlc/` ([l'audit](sdlc/cycles/006-stale-docs/evidence/prd_audit_2026-10-29.md)). Le PRD reste la référence produit ; les cycles portent le travail.

- Temps de réponse sur l'hébergeur, runner vers la base hébergée (phase 4) : [004](sdlc/cycles/004-hosted-checks/intent.md)
- Indicateurs de réussite (§13) : [007](sdlc/cycles/007-success-measures/intent.md)
- Statut « rien n'est déployé » et choix d'hébergement, devenus faux (Render + Neon) : [006](sdlc/cycles/006-stale-docs/intent.md)

---

## 1. Contexte

Saxobeat est aujourd'hui un suivi d'opportunités d'emploi **personnel** : Django 6.1, SQLite, HTMX, uv. Il collecte les offres des sites carrières des employeurs (Greenhouse, Lever, Ashby, Workday, Phenom, Talentsoft, etc.) et d'agrégateurs, les dédoublonne, masque ce qui ne convient pas avec des filtres durs, calcule un score déterministe (mots-clés + similarité TF-IDF avec le CV + séniorité) et propose un tri simple (inbox, pipeline).

**État mesuré le 8 octobre 2026**

| Mesure | Valeur |
|---|---|
| Offres (`Job`) | ~24 350 |
| Liens offre-source (`JobSource`) | ~25 900 |
| Offres scorées | ~6 600 |
| Sources actives | ~325 |
| Taille de la base SQLite | ~520 Mo (`jobs_job` 314 Mo dont ~284 Mo de texte de description ; `jobs_jobsource` 200 Mo, surtout des charges brutes) |
| Tests | 532, tous verts (au 8 octobre) ; **708** au 12 octobre ; **733** au 13 octobre (dont 28 sur les deux langues), sur SQLite et sur Postgres |

Tout ce qui est personnel (profil, mots-clés, filtres, statuts, notes, scores, avis IA, historique) est aujourd'hui stocké **sur les mêmes tables que les offres** et dans un enregistrement de configuration unique (`Config`). Il n'y a ni notion de candidat, ni séparation entre ce qui relève de l'opérateur (sources, exécutions) et ce qui relève du candidat.

## 2. Objectifs

1. **Plusieurs candidats, un catalogue partagé.** Chaque candidat a son profil, ses filtres, ses scores, ses statuts, son pipeline. Les offres et les sources sont communes.
2. **Séparer deux espaces.** Un espace *opérateur* (sources, exécutions, Welcome to the Jungle, données, sauvegardes) réservé à Vladimir, et un espace *candidat* épuré.
3. **Désencombrer l'interface** : un menu court par rôle, une page = une tâche.
4. **Onboarding guidé** : CV → Markdown, score ATS préliminaire, profil de départ extrait du CV.
5. **Hébergement géré, ~10–15 $/mois**, sur Postgres.
6. Ne **jamais** dégrader l'expérience actuelle de Vladimir : il devient le candidat n° 1 avec tout son historique.

## 3. Hors périmètre (cette phase)

- Avis IA par candidat (export/import de fichiers, clé API personnelle, crédits payés). Reporté : seul le scoring déterministe est livré. *Repris le 23 octobre 2026 dans [PRD_ai_backoffice.md](PRD_ai_backoffice.md) (résultats instantanés, IA sous 24 h via fichiers traités par l'opérateur, console opérateur).*
- Inscription publique ouverte.
- Sources privées par candidat (le catalogue reste partagé).
- Géolocalisation générale : on reste sur Paris / Île-de-France, avec quelques villes ajoutées à la main au besoin.
- Applications mobiles, paiement, facturation.
- Exécution du scraping sur le serveur (voir §6).

**Suite décidée le 9 octobre 2026** : les fonctions inspirées de la concurrence (explication du score, fraîcheur, relances, contacts…) et l'interface bilingue français / anglais font l'objet d'un document séparé, [PRD_competitive_features.md](PRD_competitive_features.md) (phases 7a à 10). **La phase 7a (interface en français et en anglais) est construite depuis le 13 octobre 2026** : l'espace candidat existe en deux langues, le choix est enregistré sur le compte, et les motifs de masquage des offres sont stockés sous forme de codes (migration 0022). L'étude de marché est dans [COMPETITION.md](COMPETITION.md).

## 4. Utilisateurs et rôles

| Rôle | Qui | Accès |
|---|---|---|
| **Opérateur** | Vladimir uniquement | Tout : espace opérateur + son propre espace candidat |
| **Candidat** | 10 à 30 amis et premiers utilisateurs, sur invitation | Espace candidat uniquement ; peut *proposer* un site carrières |

## 5. Décisions prises

| Sujet | Décision |
|---|---|
| Scraping | Reste **sur le PC de Vladimir** (IP résidentielle) et écrit directement dans la base hébergée. Le serveur ne fait que servir les pages. |
| Hébergement | Géré, ~10–15 $/mois. **Choix retenu : Render** (web Starter + Postgres Basic-256mb, Francfort, ~13 $/mois d'après la page de tarifs du 9 octobre 2026) ; l'option Neon gratuit du §6 reste un repli. |
| Base de données | **Postgres** dès le début du chantier multi-utilisateur, y compris en développement. |
| Scoring | Déterministe uniquement (mots-clés + similarité CV). Pas d'IA pour l'instant. |
| Comptes | Sur invitation, e-mail + mot de passe. *Depuis le 6 novembre 2026 (cycle 033) :* aussi par **code d'invitation** saisi sur `/signup/` (codes créés par l'opérateur, et un code par candidat), avec l'origine de chaque compte enregistrée ; le lien d'invitation à usage unique reste. |
| Échelle | 10 à 30 utilisateurs : scorer chaque offre pour chaque candidat de façon planifiée, sans file d'attente. |
| Sources | Catalogue partagé. Un candidat peut proposer un site carrières ; il reste **en attente** jusqu'à approbation de l'opérateur. |
| Profil de départ | Brouillon extrait du CV, que le candidat modifie. |
| Marchés | Paris / Île-de-France. |
| Rétention | Offres vues dans les ~90 derniers jours + toute offre sur laquelle un candidat a agi. On abandonne le HTML des descriptions et les charges brutes. |
| Score ATS | Deux scores : **santé du CV** d'abord, puis **adéquation à un poste cible**. |

## 6. Architecture cible

```
  PC de l'opérateur                       Hébergé (région UE)
 ┌────────────────────┐                ┌──────────────────────────┐
 │ Runner de sources  │  DATABASE_URL  │ Postgres                 │
 │ ingestion + dédup  ├───────────────►│  catalogue partagé       │
 │ matching/scoring   │                │  profils et données      │
 │ Welcome to the     │                │  candidats               │
 │ Jungle, captures   │                ├──────────────────────────┤
 └────────────────────┘                │ Application web Django   │
                                       │  espace candidat         │
                                       │  espace opérateur        │
                                       └──────────────────────────┘
```

- Le runner tourne comme aujourd'hui (commandes de gestion) mais avec `DATABASE_URL` pointant vers la base hébergée (SSL). Après chaque ingestion, une étape de *matching* évalue filtres et scores pour chaque candidat.
- Le serveur web reste léger : pas de scraping, pas de tâche longue. Un petit plan suffit.
- Les sources difficiles (Welcome to the Jungle, captures LinkedIn) restent côté PC.

### Hébergement recommandé
Render (service web Starter, ~7 $) + Postgres géré. Option économique : Neon gratuit (~0,5 Go) tant que la rétention maintient la base sous ce seuil ; sinon un petit Postgres payant (~6–7 $ de plus). **Vérifier les tarifs au moment de la décision.** Un VPS à ~5 € est moins cher par capacité mais oblige à administrer soi-même (Docker, sauvegardes, mises à jour). Le plan gratuit de Render n'est pas adapté : mise en veille après 15 min d'inactivité, disque effacé à chaque redémarrage, base gratuite expirant au bout de 30 jours.

### Palier gratuit : ce qui compte vraiment (analyse du 9 octobre 2026)
Le stockage n'est pas le problème : 135 Mo aujourd'hui, 250 à 500 Mo projetés (1 Go sur Neon Free). Les vraies limites sont le **transfert réseau (5 Go/mois)** et les **heures de calcul (100 CU-heures)**. D'où la phase 1.5 : ne jamais lire le texte des offres pour une liste, ne construire le modèle de texte qu'une fois par plage de quelques heures, écrire par lots. Les lignes par candidat ne sont créées que pour les offres qui passent les filtres (~24 % du catalogue : ~40 Mo pour 30 candidats, contre ~170 Mo si toutes les offres étaient stockées). Repli payant : Neon Launch à l'usage, environ 1 à 5 $/mois.

### Quand quitter SQLite
Dès qu'il y a plus d'un écrivain (runner + requêtes web + scoring) ou un déploiement hébergé. Le critère n'est pas la taille mais la concurrence. On passe donc à Postgres au début de la phase 1 et on l'utilise aussi en développement pour éviter les divergences.

## 7. Modèle de données

### Catalogue partagé (existant, allégé)
- `Job` : perd tous les champs personnels (`status`, `status_changed_at`, `applied_at`, `channel`, `cv_version`, `follow_up_at`, `notes`, `hidden_reason`, `keep_visible`, …).
- `Source`, `JobSource`, `Run` : inchangés, plus sur `Source` un statut `pending / approved` et `requested_by` (candidat qui l'a proposée).

### Nouveau : par candidat
- **`Candidate`** : lien vers un utilisateur ; texte du profil ; CV en Markdown ; paramètres (villes, mots-clés et poids, mots interdits, filtres, âge maximal, langues, salaire minimal) ; jeton personnel de capture.
- **`CandidateJob`** (une ligne par couple candidat / offre) : `status`, notes, date de candidature, canal, relance, `keep_visible`, `hidden_reason`, scores (règles, similarité, séniorité, final), mots-clés trouvés, historique.
- **`StatusChange`** passe sur `CandidateJob`.
- Volume : 30 candidats × ~24 000 offres < 1 M de petites lignes, confortable pour Postgres.

### Scoring
Ajuster le modèle de texte une seule fois sur le catalogue, puis comparer le vecteur de chaque candidat. Coût faible. Les avis IA existants de Vladimir sont migrés vers son `CandidateJob`.

### Migration
Vladimir devient le candidat n° 1 : sa configuration, ses statuts, notes, historiques et scores sont copiés sans perte. Migration réversible et testée sur une copie.

### Rétention
Purge planifiée : offres non vues depuis ~90 jours et sans action d'un candidat ; suppression de `description_html` et réduction des charges brutes. Objectif : base sous ~0,4 Go à l'usage courant.

## 8. Exigences fonctionnelles

### Espace candidat
- **Inbox, Pipeline, Archive & filtrées, Page offre, Insights, Réglages** : mêmes fonctions qu'aujourd'hui, mais filtrées par le candidat connecté.
- **Réglages** : profil, CV, villes, mots-clés, filtres.
- **Proposer un site carrières** : coller un lien ; l'appli reconnaît le système (aide « Remplir depuis un lien ») et crée une source *en attente*.
- **Export CSV, bookmarklet LinkedIn**, téléchargement de contexte pour un agent : conservés.
- Menu court (5 entrées environ), pas de vocabulaire technique (« runs », « sources », « jungle »).

### Espace opérateur
- Sources (y compris la file d'approbation), exécutions, Welcome to the Jungle, données et sauvegardes, gestion des invitations et des comptes.
- Visible uniquement par l'opérateur.

### Comptes
- Invitation par lien généré par l'opérateur (aucun service d'e-mail requis au départ).
- Connexion e-mail + mot de passe ; réinitialisation par lien généré par l'opérateur.
- Limitation du nombre d'essais de connexion.

### Onboarding (phase 5)
1. Téléversement du CV (PDF ou DOCX) → conversion locale en Markdown, sans IA.
2. **Santé du CV** (règles) : texte extractible, sections standard trouvées, dates et coordonnées lisibles, absence de tableaux ou colonnes bloquants, longueur raisonnable. Score et liste d'actions.
3. **Profil de départ** extrait du CV : intitulés, compétences, séniorité ; présenté dans une étape de revue modifiable, clairement présenté comme un brouillon.
4. Choix de la ville et des postes cibles.
5. **Adéquation au poste cible** : couverture des mots-clés et compétences d'un poste choisi parmi le catalogue.

## 9. Phases et priorités

| # | Phase | Taille | Résultat attendu |
|---|---|---|---|
| 1 | **Postgres et allègement** | S | `DATABASE_URL`, suite de tests verte sur Postgres, suppression de `description_html` et des charges brutes inutiles, base sous la limite d'un petit palier. |
| 1.5 | **Coût d'exploitation sur base distante** *(fait le 9 octobre 2026)* | S | Listes sans texte des offres (page d'inbox : 1,4 Mo → 0,08 Mo) ; modèle de texte et « boilerplate » par employeur construits une fois et gardés 6 h ; ingestion par lots (≈ 5 requêtes par offre → ≈ 0,1) ; commande `purge_old_jobs` (rétention). Motif : limites du palier gratuit de Neon (transfert 5 Go/mois, 100 CU-heures) et latence d'écriture depuis le PC. |
| 2 | **Modèle multi-candidat** *(fait le 9 octobre 2026)* | L (le plus risqueux) | `Candidate` + `CandidateJob`, migration de Vladimir comme candidat n° 1, scoring et filtres par candidat, toutes les vues filtrées par l'utilisateur. L'expérience mono-utilisateur est inchangée. Détail : le catalogue (`Job`, sources, runs) est partagé ; statut, notes, score, entretiens, fiches, réglages et sauvegardes sont par candidat ; une capture faite dans le navigateur d'un candidat lui reste privée (question n° 1, défaut retenu) ; les offres connues du seul Welcome to the Jungle n'ont pas de vue (signaux du radar). Migrations 0017/0018 réversibles ; chiffres de Vladimir identiques avant/après (inbox 4 803, 60 candidatures, 7 entretiens, 1 867 revues IA). |
| 3 | **Séparation opérateur / candidat et désencombrement** *(fait le 9 octobre 2026)* | M | Deux espaces, deux menus, rôles, pages simplifiées. Détail : l'opérateur est un superutilisateur (`jobs/access.py`) ; les pages de la machinerie (sources, exécutions, radar Jungle, revue IA, import/sauvegardes) répondent 404 à un candidat, et un test impose que chaque URL soit classée (opérateur / candidat / ouverte par jeton). Menu candidat : Inbox, Pipeline, Interviews, Companies, Insights, Settings ; « Filtered out & archive » s'ouvre depuis l'inbox ; menu « Operator » réservé à l'opérateur. Plus de plateformes, d'avis IA ni de bouton d'actualisation côté candidat ; un candidat exporte ses seules données (« Download my data »). Hors périmètre, renvoyé à la phase 4 : invitations, réinitialisation de mot de passe, limitation des essais de connexion. |
| 4 | **Hébergement et alpha** *(code fait le 9 octobre 2026 ; déploiement réel à faire)* | M | Appli en ligne (région UE), runner du PC qui écrit dans la base hébergée, invitations, sauvegardes. Alpha avec 3 à 5 amis. *Le §12 recommandait des profils créés à la main ; l'onboarding (phase 5) étant déjà construit, les amis peuvent se créer eux-mêmes par invitation.* |
| 5 | **Onboarding** *(fait le 9 octobre 2026)* | M | CV → Markdown, score de santé, profil extrait, score d'adéquation. |
| 6 | **Sources proposées par les candidats** *(fait le 9 octobre 2026)* | S | File d'approbation, quota de propositions par candidat. |

**État au 9 octobre 2026.**
- *Phase 4 (code)* : invitations à usage unique (14 jours) et page *People* de l'opérateur ; inscription e-mail + mot de passe ; liens de réinitialisation générés par l'opérateur ; blocage 15 min après 5 échecs par compte ou 20 par adresse ; désactivation et suppression de compte (aussi en libre-service) ; `SAXOBEAT_RUN_SOURCES=0` côté hébergement (le serveur n'interroge jamais les sites, tout se lit depuis le PC) ; `Dockerfile`, `render.yaml` (web + Postgres, Francfort) et `scripts/pc_runner.ps1` ; `manage.py backup_database` (pg_dump, restauration vérifiée sur une base de test). **Reste à faire par l'opérateur** : créer le service et la base chez l'hébergeur, autoriser l'adresse du PC, monter les données, planifier le runner, mesurer le temps de réponse réel avant d'inviter (docs/DEPLOY.md). Rien de tout cela n'a été exécuté chez l'hébergeur.
- *Phase 5* : CV PDF/DOCX/Markdown → Markdown (local, sans IA, fichier non conservé) ; score de santé /100 avec chaque point expliqué ; profil de départ extrait (titres, compétences, langues, mots-clés pondérés) présenté comme un brouillon modifiable ; choix des villes et des postes cibles ; page *My CV* et adéquation CV ↔ offre du catalogue (couverture des compétences et mots récurrents).
- *Phase 6* : lien proposé → source *en attente* (jamais lue avant approbation, rien n'est récupéré à la proposition) ; limites par personne (3 en attente, 10 par mois) ; file d'approbation de l'opérateur avec correction du type et des réglages, refus motivé visible du candidat.

**Refonte visuelle et pages d'erreur (9 octobre 2026, hors phases).** Réponse à la question n° 4 du §12 : le nom Saxobeat est gardé, mais l'apparence est refaite. Thème sombre unique, système de styles dans `jobs/static/jobs/app.css` (aucune couleur en dur dans les gabarits) et trois palettes au choix, mémorisées dans le navigateur : **Midnight** (indigo, par défaut), **Graphite** (neutre, accent émeraude), **Ember** (noir chaud, accent orange). L'impression (fiches d'entretien) reste noir sur blanc. En plus : la déconnexion mène à la page de connexion de l'appli (plus à celle de l'admin Django) ; `/admin/` est fermé à toute personne qui n'est pas opérateur (non connecté : renvoi vers la connexion de l'appli ; candidat : 404) ; pages 404, 500 et « page expirée » (CSRF) dans le style de l'appli.

**Configuration d'hébergement corrigée et vérifiée en local (9 octobre 2026).** `render.yaml` : Postgres 17 (`postgresMajorVersion`), disque de 1 Go, **pas de liste d'adresses autorisées** (une liste vide bloquerait aussi le PC de l'opérateur ; on pourra la renseigner plus tard avec l'adresse du PC) ; service web Starter avec `SAXOBEAT_RUN_SOURCES=0`. Litestream n'est plus utilisé (la base est Postgres). Image Docker construite et lancée contre une base de test, sauvegarde et restauration vérifiées, `/healthz` répond. Les faits Render ont été relus dans leur documentation le 9 octobre 2026 ; les tarifs sont à revérifier au moment du déploiement.

**Ordre actuel de la suite.** Déploiement réel (docs/DEPLOY.md) → phase 7a (interface FR/EN) → phase 7 (score expliqué, fraîcheur, filtrées, relances) → alpha avec 3 à 5 amis → phases 8 à 10 (voir PRD_competitive_features.md §7).

**Pourquoi cet ordre.** La phase 2 conditionne tout le reste. L'alpha à la phase 4, avant l'onboarding, apporte un retour réel plus tôt ; si l'alpha n'est pas souhaité, l'onboarding passe avant l'hébergement (voir §12).

## 10. Critères d'acceptation par phase

- **Phase 1** — toute la suite de tests passe sur Postgres ; la base de Vladimir, une fois allégée, tient sous ~0,4 Go ; une exécution complète de sources fonctionne sur Postgres.
- **Phase 2** — après migration, Vladimir retrouve le même nombre d'offres dans son inbox, ses statuts, notes et historiques à l'identique ; deux candidats de test voient chacun uniquement leurs propres statuts et scores ; modifier les filtres de l'un ne change rien chez l'autre ; la migration est réversible.
- **Phase 3** — un candidat ne peut atteindre aucune URL de l'espace opérateur (403 ou 404) ; le menu candidat tient en 5 entrées environ ; aucun terme technique dans l'espace candidat.
- **Phase 4** — l'appli répond en moins de 2 s sur les pages courantes ; les sauvegardes sont automatiques et une restauration a été testée ; une invitation permet de créer un compte et de se connecter ; le runner du PC alimente la base hébergée. *État : invitation, comptes, sauvegarde et restauration vérifiés en local et par les tests ; temps de réponse sur l'hébergeur et runner du PC vers la base hébergée **non mesurés** (aucun déploiement).*
- **Phase 5** — un CV réel de test est converti en Markdown lisible ; le score de santé explique chaque point retiré ; le profil extrait est modifiable avant d'être enregistré.
- **Phase 6** — une source proposée n'est jamais exécutée avant approbation ; un candidat dépassant son quota est bloqué avec un message clair.

## 11. Sécurité, vie privée et risques

- **Données personnelles.** Les CV sont des données personnelles : hébergement en région UE, bouton « supprimer mon compte et mes données », export des données, note de confidentialité précisant que l'opérateur peut voir les CV. Pas de CV dans les journaux.
- **IP personnelle.** Les sites proposés par les candidats sont lus depuis la connexion de Vladimir : l'approbation préalable protège cette IP ; le rythme, les temps d'attente et les règles de robots.txt existants restent obligatoires. **Aucun contournement** de protections anti-bot.
- **Secrets.** Aucune clé d'API ni mot de passe dans les formulaires ; variables d'environnement uniquement.
- **Captures LinkedIn / bookmarklet.** Par candidat (navigateur et jeton propres). Voir question ouverte n° 1.
- **Mots de passe.** Hachés ; limitation des essais ; réinitialisation par lien manuel au départ.
- **Dérive des schémas Postgres / SQLite.** Évitée en utilisant Postgres partout.
- **Risque principal** : la phase 2 touche presque tous les écrans et les tests ; elle est découpée en migrations réversibles et validée par comparaison des chiffres de Vladimir avant/après.

## 12. Questions ouvertes (réponses recommandées par défaut)

1. **Captures partagées.** Une offre capturée via le bookmarklet LinkedIn d'un candidat doit-elle devenir visible de tous ? *Recommandation : rester privée à ce candidat.* **Tranché (défaut retenu, construit en phase 2).**
2. **Alpha avant l'onboarding.** D'accord pour commencer avec 3 à 5 amis dont les profils sont créés à la main ? *Recommandation : oui.* **Dépassée en pratique** : l'onboarding est construit avant le déploiement ; reste à confirmer l'alpha avec 3 à 5 amis (décidé le 9 octobre : après les phases 7a et 7).
3. **Insights.** La page d'apprentissage (basée sur les rejets) est personnelle : la garder par candidat dès le départ ou la mettre de côté jusqu'après le lancement ? *Recommandation : par candidat, mais sans prioriser.* **Déjà par candidat dans le code (phases 2 et 3)** ; la page reste dans le menu candidat, sans travail supplémentaire prévu avant la phase 10.
4. **Nom et style.** L'appli candidat garde-t-elle le nom Saxobeat et le style actuel, ou le désencombrement inclut-il un rafraîchissement visuel ? *Recommandation : garder le nom, rafraîchir seulement ce qui est nécessaire pour l'épure.* **Tranché le 9 octobre 2026 : nom gardé, refonte visuelle complète en thème sombre avec trois palettes (voir §9).**

## 13. Indicateurs de réussite

- 5 amis actifs (au moins une connexion par semaine) un mois après l'alpha.
- Temps d'onboarding d'un nouveau candidat inférieur à 10 minutes (après la phase 5).
- Zéro fuite entre candidats (tests automatisés sur chaque vue).
- Coût mensuel d'hébergement inférieur à 15 $.
- Aucun blocage d'IP lié aux sources approuvées.

## 14. Références dans le dépôt

- Adaptateurs de sources : `jobs/sources/` ; exécution : `jobs/services/runner.py` ; ingestion : `jobs/services/ingest.py` ; filtres durs : `jobs/services/filters.py` ; scoring : `jobs/services/scoring.py`.
- Langues : `jobs/language.py` (choix de la langue), `jobs/reasons.py` (motifs en codes), `jobs/i18n_tools.py` et `manage.py i18n` (catalogue), `locale/fr/`.
- Modèles : `jobs/models.py` (`Candidate`, `CandidateJob`, `Config`, `Job`, `JobSource`, `Score`, `StatusChange`, `Source`, `Run`, `Invitation`, `FailedLogin`, `CandidateCV`, `Interview`, `CheatSheet`, `Company`).
- Rôles : `jobs/access.py`, `jobs/middleware.py` ; comptes : `jobs/accounts.py`, `jobs/views_accounts.py` ; onboarding : `jobs/cvfile.py`, `jobs/cvhealth.py`, `jobs/cvprofile.py`, `jobs/views_cv.py` ; sources proposées : `jobs/services/proposals.py` ; scoring par candidat : `jobs/services/matching.py`.
- Hébergement : `Dockerfile`, `render.yaml`, `scripts/pc_runner.ps1`, [DEPLOY.md](DEPLOY.md).
- Étude de marché et fonctions à venir : [COMPETITION.md](COMPETITION.md), [PRD_competitive_features.md](PRD_competitive_features.md).
- Liste des employeurs non supportés : `docs/unsupported_employers.csv`.
