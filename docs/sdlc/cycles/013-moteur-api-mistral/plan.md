# Plan: Moteur API Mistral

| | |
|---|---|
| **Cycle** | 013 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

## Slices
| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | Fournisseur déduit du modèle, envoi Mistral, reprise `json_object`, essais | `po_assist/api_agent.py`, `pyproject.toml` | Tests avec faux client Mistral | 2 à 5 | done |
| 2 | Défaut Mistral, repli et message par fournisseur, interface et CLI | `settings.py`, `runner.py`, `app.py` | Tests du repli, AppTest Réglages | 1, 6 | done |
| 3 | Tests Claude réglés explicitement, suite complète | `tests/test_api.py`, `tests/test_mistral.py` | `uv run pytest` | 7 | done |
| 4 | Documentation (README, guide, démarche, présentation, PROJECT.md) | `docs/`, `README.md` | Test des libellés du guide | 1, 6 | done |
| 5 | Essai réel (Vlad, sur son Mac) | aucun fichier | 5 analyses importées | 8 | todo |

Rollback : un seul commit de code ; le remettre à l'état précédent rend le moteur Claude seul.

## Gate
- [x] Owner approved the slices (Vlad, 2026-11-22)

## As run
| Date | Slice | What happened |
|---|---|---|
| 2026-11-22 | 1 | `api_agent.py` : `provider_of`, `_send_anthropic` (logique Claude déplacée telle quelle), `_send_mistral`, `MistralClient` (httpx2, 3 essais sur 429/5xx). `httpx2` déclaré dans `pyproject.toml` (il n'arrivait que par `anthropic`) |
| 2026-11-22 | 2 | Défaut `mistral-large-latest` ; message de repli et indication de clé par fournisseur ; libellés Agent, Réglages, barre latérale ; `--model` documenté. Barre d'outils Streamlit réduite (plus de bouton « Deploy » en démo) |
| 2026-11-22 | 3 | 9 tests Claude cassés par le nouveau défaut, attendu : modèle Claude fixé explicitement. 15 tests Mistral ajoutés. Suite : 71 verts |
| 2026-11-22 | 4 | README, guide (texte + captures 01 et 11 refaites), présentation. Pages officielles Mistral inaccessibles depuis la session (proxy) : tarifs marqués « estimation » |
