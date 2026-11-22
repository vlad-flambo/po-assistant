# Spec: Moteur API Mistral

| | |
|---|---|
| **Cycle** | 013 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |

## Behaviour when finished
Le moteur « API » parle à deux fournisseurs : Mistral (par défaut, `mistral-large-latest`) et Claude. Le fournisseur se déduit du modèle choisi dans ⚙️ Réglages ou passé à `--model`. Le pack, la découpe en paquets, la vérification et l'import sont les mêmes ; sans la clé du fournisseur choisi, ou si elle est refusée dès le premier paquet, l'outil se replie sur le skill comme aujourd'hui.

## Acceptance criteria
1. [x] Sans `settings.json`, le modèle est `mistral-large-latest` ; les trois modèles Mistral et les trois modèles Claude sont choisissables (Réglages, `--model`).
2. [x] Avec un faux client Mistral : 80 feedbacks en 4 paquets, requêtes au format chat completions avec `response_format` json_schema strict, résultats importés sans refus, coût calculé depuis `usage`.
3. [x] Si Mistral rejette le schéma (HTTP 400/422), le paquet est repris une fois en mode `json_object`, le schéma dans le message.
4. [x] Clé refusée (401/403) ou modèle inconnu (404) au premier paquet : arrêt propre, aucun pack orphelin, repli sur le skill ; après des paquets déjà payés : leurs résultats sont gardés.
5. [x] 429 / 5xx / coupure réseau : jusqu'à 3 essais avec attente, puis seul ce paquet est ignoré avec sa raison ; réponse tronquée (`length`) ou illisible : seul ce paquet est ignoré.
6. [x] Sans `MISTRAL_API_KEY`, un modèle Mistral se replie sur le skill avec un message qui nomme `MISTRAL_API_KEY` ; la clé n'est jamais affichée, écrite ni journalisée.
7. [x] Le comportement du moteur Claude est inchangé (ses tests passent, réglés explicitement sur un modèle Claude) ; toute la suite est verte.
8. [ ] Essai réel par Vlad : `uv run python -m po_assist run analyse --engine api --limit 5` puis `uv run python -m po_assist import`, avec sa clé Mistral.

## Design in brief
- `po_assist/api_agent.py` : `provider_of(model)`, un envoi par fournisseur (`_send_anthropic`, `_send_mistral`) qui renvoie texte, usage et raison d'échec dans une forme commune ; la boucle de paquets et l'écriture des résultats restent communes.
- Transport Mistral : `MistralClient`, appel HTTP direct avec `httpx2` (déjà installé par `anthropic`, déclaré explicitement), essais avec attente sur 429 / 5xx.
- Rejeté : SDK `mistralai` (une dépendance de plus pour un seul appel) ; couche d'abstraction multi-fournisseurs générique (deux fournisseurs suffisent).

## Interfaces and data
- Variable d'environnement : `MISTRAL_API_KEY` (dans `.env`, chargé par le lanceur Mac).
- Réglage `api_model` : défaut `mistral-large-latest`.
- Fichier de résultats : `agent` = `api / <modèle>`.

## Constraints
- Faits Mistral non vérifiables depuis la session (pages officielles bloquées) : tarifs affichés comme estimations ; l'essai réel (critère 8) tranche.

## Out of scope
- Cache de prompt Mistral, appels groupés (batch API), autres fournisseurs.

## Gate
- [x] Owner approved this spec (Vlad, 2026-11-22 : construction approuvée d'un seul tenant)
