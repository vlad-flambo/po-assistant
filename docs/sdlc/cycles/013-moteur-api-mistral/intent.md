# Intent: Moteur API Mistral

| | |
|---|---|
| **Cycle** | 013 |
| **Stage** | Verify |
| **Date** | 2026-11-22 |
| **Owner** | Vlad |
| **Importance** | 4/5 (claude, 2026-11-22): seule clé disponible chez le PO ; sans elle, le moteur API par défaut (012-D1) n'a jamais tourné en réel |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
> I can run the API with a mistral api key. Make sure the app supports their api. Start a new SDLC cycle if mistral is not supported at the moment

## Why now / the pain
- Le moteur API par défaut (décision 012-D1) n'a **jamais tourné en réel** : la seule clé disponible chez Vlad est une clé Mistral, et l'application ne parle qu'à l'API Claude (SDK `anthropic`).
- Le jury peut demander « l'avez-vous vraiment appelée ? » : aujourd'hui la réponse est non (critère 10 du cycle 010 toujours ouvert).

## Goal
Avec une clé Mistral, « Lancer l'agent » traite le pack par l'API Mistral, avec le même pack, la même vérification et le même import qu'avec Claude ; le repli sur le skill reste automatique quand la clé manque ou est refusée.

## Success measure
1. Vlad lance `uv run python -m po_assist run analyse --engine api --model mistral-large-latest --limit 5` avec sa clé : 5 résultats écrits, importés sans refus (ou refus expliqués par la vérification), coût affiché.
2. Le même chemin est testé sans réseau avec un client simulé (succès, clé refusée, erreur de paquet, réponse illisible, tronquée).
3. Sans `MISTRAL_API_KEY`, un modèle Mistral choisi se replie sur le skill avec un message qui nomme la bonne variable.
4. Les tests existants restent verts ; le moteur Claude n'est pas modifié dans son comportement.

## Not doing (this cycle)
- Changer le format des packs, la vérification ou l'import.
- D'autres fournisseurs (OpenAI, etc.) ; une couche d'abstraction générique au-delà de deux fournisseurs.
- Le cache de prompt côté Mistral (non vérifié ; l'estimation de coût le suppose absent).

## What we already know (facts, with where they came from)
- **Moteur API actuel** : `po_assist/api_agent.py`, SDK `anthropic`, `client.beta.messages.stream`, sortie structurée `output_config.format` (json_schema), système mis en cache, paquets de `pack.batch_size` tâches ; testé avec un faux client (`tests/test_api.py`, 13 tests). Choix du modèle dans ⚙️ Réglages (`api_agent.MODELS`), clé lue par `has_credentials()` (`ANTHROPIC_API_KEY`).
- **Repli** : `po_assist/runner.py` se replie sur le skill sans identifiants ou sur `ApiAgentError` au premier paquet.
- **API Mistral** (recherche web du 2026-11-22, pages officielles non lisibles depuis la session : `docs.mistral.ai`, `mistral.ai` et `api.mistral.ai` refusés par le proxy) :
  - chat completions, `POST https://api.mistral.ai/v1/chat/completions`, clé en `Authorization: Bearer` (*à vérifier*, forme standard) ;
  - sortie structurée : `response_format = {"type": "json_schema", "json_schema": {"name", "schema", "strict": true}}` ; mode JSON simple `{"type": "json_object"}` (docs.mistral.ai, « Custom Structured Outputs », d'après l'extrait de recherche) ;
  - tarifs (agrégateurs, non officiels, *à vérifier*) : Large 3 ≈ 0,50 / 1,50 $ ; Medium 3.5 ≈ 1,50 / 7,50 $ ; Small 4 ≈ 0,15 / 0,60 $ par million de jetons (entrée / sortie) ;
  - alias `mistral-large-latest`, `mistral-medium-latest`, `mistral-small-latest` : de mémoire, *à vérifier* par l'essai réel.
- **Réseau** : la session cloud ne peut pas joindre l'API Mistral ; l'essai réel se fait sur le Mac de Vlad.

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Comment choisir Mistral ? | Ajouter les modèles Mistral à la liste « Modèle (mode API) » de ⚙️ Réglages et à `--model` ; le fournisseur se déduit du modèle (`claude-*` → Anthropic, `mistral-*` → Mistral) | Accepté (Vlad, 2026-11-22) | answered |
| Q2 | Modèle par défaut ? | Rester sur Claude Opus 5.5 (récit du jury inchangé) ; Vlad choisit `mistral-large-latest` une fois dans les Réglages pour son essai | **Mistral Large (`mistral-large-latest`) par défaut**, la seule clé disponible (Vlad, 2026-11-22, « Default to Mistral ») ; Claude reste choisissable | answered |
| Q3 | Transport ? | Appel HTTP direct avec `httpx` (déjà installé avec `anthropic`), sans SDK `mistralai` : zéro dépendance nouvelle, faux client simple en test | Accepté (Vlad, 2026-11-22) | answered |
| Q4 | Sortie structurée ? | `json_schema` strict ; si Mistral refuse le schéma (400/422), une seule reprise en mode `json_object` avec le schéma dans le message. La vérification à l'import reste le garde-fou | Accepté (Vlad, 2026-11-22) | answered |
| Q5 | Récit pour le jury ? | « API par défaut (Claude ou Mistral, au choix du PO), skill en repli » ; dire que l'essai réel a été fait avec Mistral | Accepté (Vlad, 2026-11-22) ; Mistral est le modèle par défaut, voir Q2 | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- **Faits Mistral non vérifiés** (pages officielles inaccessibles) : forme exacte des erreurs, prise en charge de `anyOf` en mode strict, prix. Repli `json_object` et vérification à l'import couvrent le premier risque ; l'essai réel tranche le reste.
- **Clé** : `MISTRAL_API_KEY` dans le `.env` non versionné, jamais affichée ni écrite ; l'application dit seulement « détectée / absente ».
- **Coût de l'essai** : 5 feedbacks, quelques centimes au plus d'après les tarifs ci-dessus (*estimation*).

## Gate
- [x] All open questions answered or parked
- [x] Goal and success measure confirmed by the owner (Vlad, 2026-11-22 : réponses recommandées acceptées, Mistral par défaut, construction approuvée d'un seul tenant)
