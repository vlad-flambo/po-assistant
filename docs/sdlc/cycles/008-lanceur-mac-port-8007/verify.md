# Verify: lanceur Mac (port 8007)

| | |
|---|---|
| **Cycle** | 008 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |
| **Date** | 2026-11-17 |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence (command and output, measurement, screenshot, link) |
|---|-----------|--------|-------------------------------------------------------------|
| 1 | Exécutable versionné, compatible bash 3.2 | pass | `git ls-files -s` : `100755 PO Assist.command` ; `bash -n` sans erreur ; aucune syntaxe bash 4 ([evidence](evidence/tests_lanceur_2026-11-17.md)) |
| 2 | Démarrage normal : l'application répond sur 8007, le navigateur s'ouvre | pass | Scénario A : `/_stcore/health` répond ; `open` reçoit `http://localhost:8007` |
| 3 | Déjà lancé : navigateur ouvert, code 0 | pass | Scénario B : code 0, message « tourne déjà », `open` appelé |
| 4 | Port pris par un autre programme : il est nommé, code 1, rien n'est lancé | pass | Scénario C : code 1, `lsof` nomme `python3`, aucun Streamlit lancé, navigateur non ouvert |
| 5 | uv introuvable : commandes d'installation, code 1 | pass | Scénario D (HOME vide, PATH sans uv) : code 1, message et commande `astral.sh` |
| 6 | `.streamlit/config.toml` : port 8007, pas de statistiques | pass | `uv run streamlit run app.py` sans option : santé « ok » sur 8007 |
| 7 | README et script de démo à jour | pass | `README.md` (« Démarrer »), `docs/presentation.md` (liste d'avant démo) |
| 8 | Double-clic sur le Mac de Vlad | pending | À faire par Vlad |

## Tests
- Suite complète : `uv run pytest` : 30 passed (la configuration Streamlit ne change rien aux tests).

## Not verified
- **Le comportement propre à macOS** : le double-clic depuis le Finder, `open`, `lsof` et le bash 3.2 de macOS, Gatekeeper au premier lancement. Les tests ont tourné sous Linux avec bash 5.2 et une fausse commande `open`. C'est le critère 8.
- **Le PATH d'une fenêtre ouverte depuis le Finder** : la recherche de uv dans `~/.local/bin`, `~/.cargo/bin` et Homebrew couvre les installations habituelles, sans avoir été vérifiée sur le Mac.

## Verdict
- [ ] Accepted by owner
- [ ] Sent back (what, to which stage)
