# Intent: option API

| | |
|---|---|
| **Cycle** | 010 |
| **Stage** | Closed 2026-11-22 |
| **Date** | 2026-11-17 |
| **Owner** | Vlad |
| **Importance** | 3/5 (claude, 2026-11-17): rend l'agent utilisable sans geste manuel ; alternative au skill local, au choix dans les réglages |

## The request, in your words
> Deuxième intent séparé, ajouter l'option API également. A choisir entre mode skills en local ou via API dans les settings

## Why now / the pain
- En mode skill, le PO doit exporter, aller dans Claude Code, dire « traite les packs », puis revenir importer. Ce sont trois gestes manuels par étape.
- La décision du 2026-11-16 (002-D1, « pas d'API ») visait le délai et la simplicité ; l'API redevient une option, pas un remplacement.

## Goal
Dans ⚙️ Réglages, le PO choisit le moteur de l'agent : **skill Claude Code en local** (échange de fichiers, comme aujourd'hui) ou **API Claude**. En mode API, « Lancer l'agent » envoie le même pack à l'API et récupère les résultats dans le même format. Ils passent ensuite par la même vérification et le même import.

## Success measure
1. Le choix du moteur se fait dans ⚙️ Réglages et survit à « Réinitialiser ».
2. En mode API, un pack de 80 feedbacks est traité sans geste manuel entre « Lancer l'agent » et l'aperçu d'import.
3. Le coût de chaque lancement (jetons et dollars) est affiché, et une estimation est donnée avant de dépenser.
4. Sans clé ou en cas d'erreur de l'API, le message dit quoi faire, et rien n'est importé à moitié sans le dire.

## Not doing (this cycle)
- Remplacer le skill : il reste le moteur par défaut.
- L'API des lots asynchrones (Message Batches) ou les Managed Agents : une requête par paquet de tâches suffit.
- Saisir et stocker une clé API dans l'application.

## What we already know (facts, with where they came from)
- **Référence officielle** (skill `claude-api`, cache du 2026-11-03) :
  - modèle par défaut `claude-opus-5-5` (4 $ / 20 $ par million de jetons), alternatives `claude-sonnet-5-5` (2 $ / 10 $) et `claude-haiku-5-5` (0,10 $ / 0,50 $) ;
  - sorties structurées via `output_config.format` (`json_schema`, `additionalProperties: false` obligatoire, sans contraintes numériques ni de longueur) ;
  - mise en cache des instructions communes (`cache_control`) ;
  - réponses de refus (`stop_reason: "refusal"`), avec repli côté serveur en option (`fallbacks: "default"`, bêta `server-side-fallback-2026-07-01`) ;
  - streaming conseillé pour les sorties longues ;
  - erreurs typées du SDK (`RateLimitError`, `APIStatusError`…) et 2 nouvelles tentatives automatiques.
- **Identifiants** : le SDK lit `ANTHROPIC_API_KEY`, ou un profil `ant auth login`. Dans ce conteneur, aucune clé n'est définie et `ant` n'est pas installé : **aucun appel réel ne peut être testé ici**.
- **Le format des packs ne change pas** : brief, instructions, format de sortie, contexte, tâches (`po_assist/handoff.py`). Seul le transport change ; la vérification à l'import reste le garde-fou.
- **Le lanceur Mac** (cycle 008) peut charger un fichier `.env` local, non versionné, pour fournir la clé sans la saisir dans l'application.

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Modèle par défaut ? | `claude-opus-5-5`, le défaut recommandé ; Sonnet 5.5 et Haiku 5.5 au choix dans les réglages | Décidé par Claude (consigne « enchaîner si tout est clair »), à relire | answered |
| Q2 | Où vit la clé ? | Dans l'environnement : `ANTHROPIC_API_KEY`, un profil `ant auth login`, ou un `.env` à la racine chargé par le lanceur Mac (`.env` est ignoré par git). L'application ne stocke jamais de clé et affiche seulement « clé détectée / absente » | Idem | answered |
| Q3 | Taille des paquets ? | 20 tâches par requête (10 pour la rédaction, aux sorties longues), avec les instructions et le contexte mis en cache entre les requêtes | Idem | answered |
| Q4 | Garde-fou sur la dépense ? | Estimation du coût affichée avant l'envoi ; le PO confirme d'un clic ; coût réel affiché après | Idem | answered |
| Q5 | Refus de sécurité du modèle ? | Repli côté serveur activé par défaut (`fallbacks: "default"`), sinon la tâche revient « ignorée » avec la raison | Idem | answered |
| Q6 | Mode démo et mode API ? | Le mode démo prime : tant qu'il est activé, aucun appel n'est fait. Le choix du moteur s'applique quand il est désactivé | Idem | answered |

## Constraints and risks
- **Dépense réelle** : chaque lancement en mode API coûte de l'argent sur le compte du PO. Aucun appel n'est fait sans clic de confirmation, et aucun dans les tests.
- **Non testable ici** : les appels réels ne peuvent être vérifiés que par Vlad avec sa clé. Les tests utilisent un client simulé.

## Gate
- [x] All open questions answered or parked
- [x] Goal and success measure confirmed by the owner (consigne de Vlad, 2026-11-17 : « A enchainer directement si tout est clair » ; choix Q1 à Q6 à relire)
