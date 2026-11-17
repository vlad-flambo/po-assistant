# Spec: lanceur Mac (port 8007)

| | |
|---|---|
| **Cycle** | 008 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |
| **Date** | 2026-11-17 |

## Behaviour when finished
- **Double-clic sur `PO Assist.command`** (racine du dépôt), sur le Mac : Terminal s'ouvre, l'environnement est préparé (`uv sync`), l'application démarre sur le port 8007, et le navigateur s'ouvre sur `http://localhost:8007` dès qu'elle répond. Fermer la fenêtre de Terminal (ou Ctrl+C) arrête l'application.
- **Lancement manuel** : `uv run streamlit run app.py` utilise aussi le port 8007, fixé par `.streamlit/config.toml`.

## Acceptance criteria
1. [ ] `PO Assist.command` est versionné avec le droit d'exécution (mode git `100755`) et compatible avec le bash 3.2 de macOS (aucune syntaxe bash 4).
2. [ ] Lancé dans un état normal, il démarre l'application, qui répond sur `http://localhost:8007/_stcore/health`, et il ouvre le navigateur sur `http://localhost:8007`.
3. [ ] Si PO Assist tourne déjà sur 8007 (processus lancé depuis le dossier du dépôt), il ouvre le navigateur et s'arrête sans erreur (code 0).
4. [ ] Si un autre programme occupe le port 8007, il le nomme, s'arrête (code 1) et ne lance rien.
5. [ ] Si uv est introuvable, y compris dans ses emplacements d'installation habituels (`~/.local/bin`, `~/.cargo/bin`, Homebrew), il affiche les commandes d'installation officielles et s'arrête (code 1) sans rien installer.
6. [ ] `.streamlit/config.toml` fixe le port 8007 et désactive l'envoi de statistiques d'usage.
7. [ ] Le README et le script de démo (`docs/presentation.md`) indiquent le double-clic et le port 8007.
8. [ ] Vlad double-clique sur le fichier sur son Mac et voit l'application.

## Design in brief
- Un script bash unique : il se place dans le dossier du script, cherche uv (PATH, puis les emplacements habituels : une fenêtre ouverte depuis le Finder n'a pas toujours le même PATH qu'un terminal), vérifie le port avec `lsof` (et le dossier de travail du processus, pour reconnaître PO Assist), lance `uv sync` puis Streamlit en mode headless, et ouvre lui-même le navigateur (`open`) quand `/_stcore/health` répond.
- En cas d'erreur, la fenêtre attend Entrée avant de se fermer, pour que le message reste lisible.
- Écarté : une application `.app` (Automator ou Platypus), plus lourde à maintenir et à signer ; laisser Streamlit ouvrir le navigateur (il ne sait pas gérer le cas « déjà lancé »).

## Interfaces and data
- Nouveaux fichiers : `PO Assist.command`, `.streamlit/config.toml`.
- Modifiés : `README.md`, `docs/presentation.md`.

## Constraints
- Pas de Mac dans l'environnement de développement : les critères 1 à 6 sont testés sous Linux (bash, lsof, curl, `open` simulé). Le critère 8 est vérifié par Vlad.

## Out of scope
- Windows, Linux, `.app`, installation automatique de uv.

## Gate
- [x] Owner approved this spec (approbation préalable : recommandations Q1 à Q5, « je valide les recommandations, go », Vlad, 2026-11-17)
