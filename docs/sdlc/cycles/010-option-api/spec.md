# Spec: option API

| | |
|---|---|
| **Cycle** | 010 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |
| **Date** | 2026-11-17 |

## Behaviour when finished
- **⚙️ Réglages** : moteur de l'agent, « Skill Claude Code (local) » par défaut ou « API Claude » ; modèle (Opus 5.5 par défaut, Sonnet 5.5, Haiku 5.5) ; état de la clé (« détectée » ou « absente », jamais affichée). Tant que le mode démo est activé, il prime et aucun appel n'est fait.
- **Mode API** : le bouton annonce le coût estimé (« Lancer l'agent (API, ≈ 0,40 $) »). Le clic exporte le pack, l'envoie à l'API par paquets avec une progression, écrit le fichier de résultats habituel, puis affiche le coût réel. Le PO vérifie et importe comme d'habitude.

## Acceptance criteria
1. [ ] Le réglage `engine` (`skill` / `api`) et le modèle se choisissent dans ⚙️ Réglages et survivent à « Réinitialiser ». Le défaut est `skill` + `claude-opus-5-5`.
2. [ ] Chaque pack déclare un schéma JSON de sortie, conforme aux limites des sorties structurées (`additionalProperties: false` partout, pas de contraintes numériques ou de longueur). La réponse de l'API est contrainte par `output_config.format`.
3. [ ] Envoi par paquets (20 tâches, 10 pour la rédaction). Le brief, les instructions, le format et le contexte sont dans un `system` mis en cache (`cache_control`), identique d'un paquet à l'autre.
4. [ ] Le fichier produit est un `po-assist.results.v1` valide, avec l'agent « api / <modèle> ». Il passe par la vérification et l'import habituels.
5. [ ] Refus du modèle, sortie tronquée ou erreur d'un paquet : les tâches concernées reviennent `skipped` avec la raison, et les autres paquets continuent. Une clé absente ou invalide arrête tout avec un message clair, avant toute écriture de résultats.
6. [ ] Coût estimé avant l'envoi, coût réel (jetons d'entrée, de cache et de sortie, en dollars) après, au tarif de la référence du 2026-11-03.
7. [ ] Le repli côté serveur (`fallbacks: "default"`) est activé.
8. [ ] Le lanceur Mac charge un `.env` local s'il existe ; `.env` est ignoré par git.
9. [ ] Tests sans réseau ni clé (client simulé) : découpage, cache, schéma, import, refus, erreur d'authentification, coût, réglages. Aucun test ne fait d'appel réel.
10. [ ] Vérification réelle par Vlad avec sa clé, sur un petit pack (`--limit 5`).

## Design in brief
- `po_assist/api_agent.py` : `run(pack, subjects, model, client)` exporte le pack, découpe les tâches et appelle `client.beta.messages.stream(...)` (avec `get_final_message()`) pour chaque paquet. Il écrit ensuite les résultats et renvoie l'usage et le coût. Il fournit aussi `estimate(...)` et `has_credentials()`.
- Les schémas de sortie vivent avec chaque pack (`output_schema`), à côté de ses règles de validation : l'API contraint la forme, l'import vérifie le fond (cibles, citations exactes).
- Paramètres : `effort: "high"` (jugement), réflexion adaptive par défaut, streaming (`max_tokens` 64 000).
- Ligne de commande : `python -m po_assist run <pack> --engine api [--limit N]`.
- Écarté : l'API des lots asynchrones (moitié prix, mais jusqu'à 24 h d'attente : incompatible avec un PO devant son écran) ; des outils (*tool use*) : les sorties structurées suffisent, il n'y a rien à exécuter.

## Out of scope
- Le stockage d'une clé dans l'application ; Bedrock, Vertex AI, Foundry.

## Gate
- [x] Owner approved this spec (consigne « A enchainer directement si tout est clair », Vlad, 2026-11-17)
