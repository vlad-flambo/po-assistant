# Essai réel Mistral (critère 8), 2026-11-22

Sur le Mac de Vlad, avec sa clé `MISTRAL_API_KEY` (lue depuis `.env`, jamais affichée), session Claude Code locale, 21:46 UTC.

**Isolement.** Les 80 analyses de l'espace de travail étaient déjà faites, donc `run analyse --limit 5` n'aurait rien trouvé. L'essai tourne dans un espace jetable (`PO_ASSIST_DB`, `PO_SETTINGS_FILE` et `PO_HANDOFF_DIR` pointés vers un dossier temporaire), sur la même base Linear synthétique. L'espace de travail réel n'a pas été modifié.

## 1. Lot de 5 analyses
`uv run python -m po_assist run analyse --engine api --limit 5` (durée : 1 min 15 s)
```
Moteur : api · estimation API : {'tasks': 80, 'batches': 4, 'usd': 0.3525}
  paquet 1/1
Résultats écrits : <espace de test isolé>/handoff/to-do/E-20261122-214642-analyse.results.json · coût réel : 0.0312 $
Vérifier et importer : uv run python -m po_assist import
```
L'estimation affichée (0,3525 $) porte sur les 80 tâches restantes, pas sur le lot de 5.

## 2. Import
`uv run python -m po_assist import`
```
E-20261122-214642-analyse.results.json — Importé : analyse (E-20261122-214642-analyse) : 5 prêts, 0 refusés, 0 ignorés par l'agent, 0 sans résultat
```
Ensuite, `status` indique : analyse 5 faites, 75 à faire.

## 3. Contenu (fichier complet : [mistral-live_2026-11-22.results.json](mistral-live_2026-11-22.results.json))
| Tâche | Feedback | Type | Sentiment | Cible |
|---|---|---|---|---|
| T-001 | SAX-201 | feature_request | negative | SAX-110 |
| T-002 | SAX-203 | feature_request | positive | SAX-122, SAX-123 |
| T-003 | SAX-202 | question | negative | SAX-126 |
| T-004 | SAX-204 | feature_request | positive | SAX-103 |
| T-005 | SAX-205 | bug | negative | NEW:delivrabilite-des-emails-transactionnels |

L'en-tête du fichier indique `"agent": "api / mistral-large-latest"`.

## 4. Mode strict
Le lancement n'enregistre pas si la reprise `json_object` a servi. Une sonde, avec le même schéma de résultats d'analyse en `json_schema` strict et un message de deux mots, tranche :
```
strict json_schema: ACCEPTED (HTTP 200) | model: mistral-large-latest | usage: {'prompt_tokens': 497, 'total_tokens': 547, 'completion_tokens': 50, 'prompt_tokens_details': {'cached_tokens': 0}, 'completion_tokens_details': {'reasoning_tokens': 49}, 'service_tier': 'standard'}
```
Mistral accepte le schéma strict, `anyOf` compris : le lot est passé en mode strict, sans reprise. Coût de la sonde : environ 0,0009 $.
