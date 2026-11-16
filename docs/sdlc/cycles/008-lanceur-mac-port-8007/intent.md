# Intent: lanceur Mac (port 8007)

| | |
|---|---|
| **Cycle** | 008 |
| **Stage** | Intent |
| **Date** | 2026-11-16 |
| **Owner** | Vlad |
| **Importance** | 3/5 (claude, 2026-11-16): utile pour la répétition et la démo du soir sur le Mac de Vlad ; rien ne casse sans (la commande uv fonctionne déjà) |

## The request, in your words
> prépares moi un fichier command qui lance l'app sur mon mac.
> je veux un canal différent du par défaut. 8007 par exemple
> passe par le process ai-sdlc

## Why now / the pain
- Lancer l'application demande aujourd'hui un terminal, `uv sync` puis `uv run streamlit run app.py`, sur le port 8501 par défaut de Streamlit.
- Le jour de la présentation, un double-clic est plus sûr qu'une commande tapée sous stress.
- Le port 8501 est souvent déjà pris par une autre application Streamlit.

## Goal
Un double-clic sur un fichier du dépôt ouvre PO Assist dans le navigateur du Mac, sur le port 8007.

## Success measure
1. Double-cliquer sur le fichier ouvre l'application sur `http://localhost:8007`, sans rien taper.
2. Si l'application tourne déjà sur ce port, le fichier ouvre simplement le navigateur, sans erreur.
3. S'il manque un prérequis (uv) ou si le port est pris par autre chose, le message dit quoi faire.

## Not doing (this cycle)
- Une application Mac empaquetée (.app) ou un lanceur pour Windows ou Linux.
- L'installation automatique de uv ou de Python.

## What we already know (facts, with where they came from)
- Vlad travaille sur Mac : `.DS_Store` à la racine du dépôt et dans `.claude/`, et la configuration saxobeat de `.claude/launch.json` lance déjà `uv run python …` (2026-11-16).
- Un fichier `.command` exécutable s'ouvre dans Terminal au double-clic sur macOS. *(Connaissance générale, à vérifier sur le Mac de Vlad.)*
- Git conserve le droit d'exécution (`core.fileMode = true` dans ce dépôt). Un clone garde donc le fichier exécutable ; une archive zip téléchargée depuis GitHub peut le perdre. *(À vérifier.)*
- Aucune configuration Streamlit dans le dépôt : le port est 8501 par défaut (Streamlit 1.67.0, `pyproject.toml`).
- Dépendances : Python ≥ 3.12 et streamlit, installées par `uv sync` (`pyproject.toml`, `uv.lock`).

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Nom et emplacement du fichier ? | `PO Assist.command` à la racine du dépôt, visible et parlant | | open |
| Q2 | Le port 8007 vaut-il aussi pour `uv run streamlit run app.py` ? | Oui : `.streamlit/config.toml` fixe le port 8007, une seule source de vérité, et le README ne cite plus qu'un port | | open |
| Q3 | Si uv manque ? | Afficher la commande d'installation officielle et s'arrêter, sans rien installer à la place de Vlad | | open |
| Q4 | Si le port 8007 est déjà pris ? | PO Assist y répond déjà : ouvrir le navigateur. Autre chose : le dire, avec le processus en cause, et s'arrêter | | open |
| Q5 | Ouvrir le navigateur automatiquement ? | Oui, dès que l'application répond | | open |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- **Gatekeeper** : un fichier téléchargé peut être bloqué au premier lancement (clic droit › Ouvrir). Le risque est faible pour un fichier obtenu par `git pull`.
- **Pas de Mac dans cet environnement** : le script est testé sous Linux (bash, port, page servie), et le double-clic n'est vérifié que par Vlad.

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
