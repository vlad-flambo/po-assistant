# Learn: Moteur API Mistral

| | |
|---|---|
| **Cycle** | 013 |
| **Stage** | Learn |

## What happened vs what we expected
Les quatre mesures de succès sont atteintes.
1. Essai réel (2026-11-22, Mac de Vlad, sa clé) : 5 analyses écrites par `mistral-large-latest`, importées sans refus (5 prêts, 0 refusés, 0 ignorés), coût réel affiché (0,0312 $). L'essai a tourné dans un espace de test isolé, pas dans l'espace de travail réel, dont les 80 analyses étaient déjà faites.
2. à 4. : tests avec client simulé, repli sans clé, moteur Claude inchangé, 71 tests verts (voir verify.md).

## What we learned
- **Mistral accepte le schéma de résultats en `json_schema` strict**, `anyOf` compris. Le risque principal du cycle ne s'est pas réalisé : la reprise en `json_object` reste un filet, et elle n'a pas servi.
- **Durée** : 1 min 15 s pour un paquet de 5 tâches avec Mistral Large. La sonde renvoie `reasoning_tokens` : le modèle raisonne avant de répondre, ce qui explique le temps. Un lot complet de 80 tâches en 4 paquets, joués l'un après l'autre, peut prendre plusieurs minutes.
- **`run --limit 5` ne trouve rien une fois les 80 analyses faites** : l'analyse saute ce qui est déjà fait, même avec `--subjects`. Pour un essai, il faut un espace jetable (variables `PO_ASSIST_DB`, `PO_SETTINGS_FILE`, `PO_HANDOFF_DIR`) ou une remise à zéro.
- **Le lancement n'enregistre pas si la reprise `json_object` a servi** : il a fallu une sonde à part pour le savoir. Le savoir dans l'en-tête des résultats éviterait ça.
- **Prérequis sur le Mac** après la migration : `uv` absent, `.venv` cassé, lanceur bloqué par la quarantaine macOS (Gatekeeper). Les trois sont réglés.
- Les tarifs Mistral du code restent des estimations : le coût réel affiché est calculé avec eux.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| Essai réel réussi, mode strict accepté, coût et durée | `docs/demarche.md` (limite « pas encore appelé pour de vrai » remplacée) | [x] |
| Essai réel et sa vérification | `docs/journal.md` (tableau et journal) | [x] |
| Réponse « La démo appelle-t-elle vraiment l'API ? » | `docs/presentation.md` | [x] |
| `uv` installé par Homebrew, quarantaine du lanceur levée | `docs/sdlc/PROJECT.md` | [x] |
| Coût et qualité Mistral dans les diapositives 5 et 11 | close-out plan, étape 4 (qualité non mesurée : hors de la demande) | deferred, sans date : la qualité n'est pas mesurée |

## Process feedback
- Le pas à pas de l'essai (`next.md`, close-out plan) supposait des analyses à faire. Un pas d'essai réel devrait dire dans quel état doivent être les données, ou prévoir un espace isolé.

## Next cycle candidates
- Enregistrer dans l'en-tête des résultats le mode de sortie utilisé (`strict` ou `json_object`) et la durée de chaque paquet.
- Mesurer la qualité de Mistral sur les 80 feedbacks (≈ 0,35 $, page 🎯 Qualité), à comparer aux 84 / 96 / 98 % du skill.
