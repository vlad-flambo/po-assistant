# Intent: guide utilisateur

| | |
|---|---|
| **Cycle** | 011 |
| **Stage** | Intent |
| **Date** | 2026-11-17 |
| **Owner** | Vlad |
| **Importance** | 4/5 (claude, 2026-11-17): le critère « Expérience utilisateur » (15 %) demande qu'un PO se serve de l'outil sans friction ; utile aussi au jury qui voudra l'essayer seul |

## The request, in your words
> new intent. rédiges un guide utilisateur pour l'outil.
> Détaille étape par étape comment l'utiliser

## Why now / the pain
- Le README s'adresse à un développeur : installation, architecture, tests. Rien n'explique à un PO comment se servir de l'outil, écran par écran.
- L'interface s'est enrichie (mode démo, trois moteurs, réglages) et les captures existantes (`docs/captures/`, 2026-11-16) ne montrent plus l'interface actuelle.

## Goal
Un PO qui n'a jamais vu PO Assist va du double-clic sur le lanceur jusqu'à une user story envoyée dans Linear en suivant uniquement le guide. Il sait aussi passer en mode réel (skill ou API) et lire les résultats.

## Success measure
1. Chaque étape du guide nomme exactement ce que l'écran affiche (pages, boutons, champs) : un test vérifie que chaque libellé cité existe dans l'application.
2. En suivant le guide à la lettre dans un navigateur (Playwright), on obtient une story envoyée dans Linear.
3. Le guide est accessible depuis l'application et depuis le README.

## Not doing (this cycle)
- Changer l'interface pour la simplifier (sauf l'accès au guide).
- Une vidéo ou un tutoriel interactif.

## What we already know (facts, with where they came from)
- **8 pages** : 🤖 Agent, 🏠 Tableau de bord, 📥 Feedbacks, 🧩 Demandes, ⚖️ Priorisation, ✍️ User stories, 🎯 Qualité de l'agent, ⚙️ Réglages. Une trentaine de commandes : boutons, filtres, curseurs, éditeur (`app.py`, inventaire du 2026-11-17).
- **Trois moteurs** : mode démo (par défaut), skill Claude Code, API Claude. Plus le lanceur Mac et la ligne de commande (`po_assist status | export | run | import`).
- **Préférence de Vlad** : livrables en Markdown par défaut.
- Le parcours démo complet a été joué dans un navigateur le 2026-11-17 (cycle 009) : il peut servir de colonne vertébrale au guide et de vérification.

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Format et emplacement ? | `docs/guide-utilisateur.md` (Markdown), lié depuis le README, et affiché dans l'application par une page « ❓ Guide » qui lit ce même fichier (une seule source) | Oui : « je valide les recommandations, go » (Vlad, 2026-11-17) | answered |
| Q2 | À qui s'adresse-t-il ? | Au PO, sans jargon technique. Une annexe pour l'installation, la ligne de commande et la clé API | Oui : « je valide les recommandations, go » (Vlad, 2026-11-17) | answered |
| Q3 | Plan ? | 1. Démarrer · 2. Vue d'ensemble (3 étapes, le PO valide entre chacune) · 3. Parcours pas à pas en mode démo, écran par écran · 4. Passer en mode réel : skill Claude Code, puis API · 5. Lire les résultats (score RICE, MoSCoW, citations, alertes) · 6. Réglages et remise à zéro · 7. Dépannage · 8. Glossaire | Oui : « je valide les recommandations, go » (Vlad, 2026-11-17) | answered |
| Q4 | Captures d'écran ? | Oui : une dizaine de captures neuves de l'interface actuelle, prises en suivant le parcours (`docs/guide/`) | Oui : « je valide les recommandations, go » (Vlad, 2026-11-17) | answered |
| Q5 | Langue ? | Français | Oui : « je valide les recommandations, go » (Vlad, 2026-11-17) | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- **Dérive** : le guide se périme dès que l'interface change. Le test des libellés le signalera.
- **Taille des captures** : une dizaine d'images PNG versionnées (quelques Mo).

## Gate
- [x] All open questions answered or parked
- [x] Goal and success measure confirmed by the owner (« je valide les recommandations, go », Vlad, 2026-11-17)
