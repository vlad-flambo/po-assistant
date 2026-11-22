# Intent: API par défaut, skill en repli

| | |
|---|---|
| **Cycle** | 012 |
| **Stage** | Closed 2026-11-22 |
| **Date** | 2026-11-17 |
| **Owner** | Vlad |
| **Importance** | 4/5 (claude, 2026-11-17): change le comportement par défaut de l'outil, la démo et le discours de restitution (architecture, slides, guide) |

## The request, in your words
> Comportement par défaut devrait être celui d'une intégration API. La version skill le fallback.
> Configure la démo pour suivre un flow simulé par api.
> Refait la documentation et slides si besoin

## Why now / the pain
- Aujourd'hui, le moteur par défaut est le skill local (`settings.py`, cycle 010), et le mode démo imite le skill (« le skill po-agent traite… »).
- Le discours des slides et du guide est « pas d'API : le fichier est le skill » (diapositive 8), ce qui contredit le comportement voulu.

## Goal
Par défaut, PO Assist se comporte comme une intégration API : « Lancer l'agent » appelle l'API Claude. Si l'API est indisponible (pas de clé, clé refusée), l'outil se replie automatiquement sur le skill Claude Code local et le dit. En mode démo, le parcours est celui de l'API, simulé : même bouton avec coût estimé, progression paquet par paquet, coût affiché (simulé, rien n'est facturé). Documentation et slides racontent cette architecture.

## Success measure
1. Sans `settings.json`, le moteur est l'API ; le skill reste choisissable dans ⚙️ Réglages.
2. Sans clé ou avec une clé refusée, « Lancer l'agent » se replie sur le skill (pack exporté, consigne affichée), sans erreur bloquante.
3. En mode démo, le bouton, la progression et le message final sont ceux du mode API, avec la mention « simulé ».
4. README, guide (avec ses captures), document de démarche, script de présentation et slides décrivent « API par défaut, skill en repli, démo = API simulée » ; plus aucune mention de « pas d'API » comme choix actuel.

## Not doing (this cycle)
- Changer le format des packs, la vérification ou l'import.
- Repli automatique tâche par tâche vers le skill après une erreur partielle de l'API (les tâches ignorées repartent au prochain lancement, comme aujourd'hui).

## What we already know (facts, with where they came from)
- **Moteur API** déjà construit et testé avec un client simulé (cycle 010, `po_assist/api_agent.py`) ; aucun appel réel fait (pas de clé ici).
- **Mode démo** (cycle 009, `po_assist/demo.py`) : rejoue de vrais résultats du skill, en une seule « progression », au nom du skill.
- **Décision 002-D1** (2026-11-16, « pas d'API ») : remplacée par celle-ci, à consigner.
- **Slides** : 14 diapositives (https://claude.ai/artifact/Uvou3wJVtTvQHdhBGFSJSk, lien mort depuis la migration du 2026-11-21). À revoir : 8 (architecture), 12 (ce qui a changé), notes de 4 et 9.
- **Guide** : sections 1, 3, 4, 6, 7, 8 et 3 captures de la page Agent ; un test vérifie les libellés cités.

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Qu'est-ce qui déclenche le repli sur le skill ? | Pas d'identifiants détectés, ou l'API refuse la requête dès le premier paquet (clé invalide, modèle inaccessible) : le pack est exporté pour le skill, et un message dit pourquoi et quoi faire | Décidé par Claude (demande directive), à relire | answered |
| Q2 | Le skill reste-t-il choisissable explicitement ? | Oui, dans ⚙️ Réglages (« Skill Claude Code (repli) »), pour qui ne veut pas d'API | Idem | answered |
| Q3 | Que montre la démo ? | Exactement le parcours API : bouton « Lancer l'agent (API, ≈ x $) », progression « paquet k/n », message final avec coût **simulé** (« rien n'est facturé »). Les résultats restent ceux d'un vrai passage de l'agent, et le bandeau 🎬 le dit | Idem | answered |
| Q4 | Provenance affichée dans les résultats de démo ? | « API simulée : résultats d'un vrai passage de l'agent po-agent, calculés à l'avance » : la démo imite le flux API sans prétendre que l'API a produit ces résultats | Idem | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- **Honnêteté envers le jury** : la démo simule le flux API mais ne doit pas laisser croire à un appel réel ; bandeau et mention « simulé » obligatoires.
- **L'API par défaut sans essai réel** : le moteur API n'a jamais été appelé pour de vrai ; le repli sur le skill protège la démo et l'usage si l'appel échoue.

## Gate
- [x] All open questions answered or parked
- [x] Goal and success measure confirmed by the owner (demande directive de Vlad, 2026-11-17 ; choix Q1 à Q4 à relire)
