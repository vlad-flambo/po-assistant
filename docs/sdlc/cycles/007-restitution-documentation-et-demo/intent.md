# Intent: restitution documentation et démo

| | |
|---|---|
| **Cycle** | 007 |
| **Stage** | Intent |
| **Date** | 2026-11-16 |
| **Owner** | Vlad |
| **Importance** | 5/5 (claude, 2026-11-14): démarche et présentation pèsent 40 % de la note (brief §04) ; échéance lundi 16/11 au soir |

## The request, in your words
> Cycle issu de l'analyse initiale (`docs/analyse/01-analyse-initiale.md`, WBS §6), validée par Vlad le 2026-11-14.
> « oui, fais les slides » (Vlad, 2026-11-16) ; « oui, fais les deux » (remplir ce cadrage, 2026-11-16).

## Why now / the pain
- Le brief attend 3 livrables : l'agent, une documentation de la démarche et des choix techniques, une présentation de 30 minutes (10 min de démonstration, 5 d'architecture, 5 de démarche, 10 de questions).
- Démarche (20 %) et présentation (20 %) comptent autant que le reste réuni hors compréhension métier.

## Goal
Vlad présente PO Assist en 20 minutes sans accroc, s'appuie sur une démonstration qui fonctionne même sans réseau ni agent en direct, et répond aux questions du jury avec des preuves tirées du dépôt.

## Success measure
1. Les 3 livrables du brief existent et sont cohérents entre eux (mêmes chiffres partout, recoupés avec les données).
2. La démonstration se rejoue en un clic depuis un état initial, et des captures de secours couvrent les 3 blocs.
3. Une répétition minutée tient dans les 10 minutes de démonstration et les 20 minutes de présentation.
4. Les diapositives sont accessibles au jury (partagées ou exportées en PDF).

## Not doing (this cycle)
- Une vidéo de démonstration : remplacée par le rejeu en un clic et les captures de secours.
- Une démonstration en direct du skill sur les 80 feedbacks (3 à 4 minutes) : seulement sur demande du jury, sur un petit pack.

## What we already know (facts, with where they came from)
- **Documentation** : `README.md` (démarrage, architecture, qualité mesurée), `docs/demarche.md` (livrable 2 : problème, hypothèses, chemin, abandons, usage de l'IA, choix techniques, limites), `docs/journal.md` (journal et registre de l'usage de l'IA), `docs/sdlc/` (cycles).
- **Présentation** : `docs/presentation.md` (déroulé, script de démonstration minuté, 10 questions probables) ; 14 diapositives avec notes : https://claude.ai/artifact/Uvou3wJVtTvQHdhBGFSJSk (privées ; perdues à la migration de compte, reconstruites le 2026-11-22 : https://claude.ai/artifact/SnLtghS49Mfa2x2hSKPSxD, source dans `docs/presentation/deck/`).
- **Démonstration** : rejeu des résultats réels de l'agent (`handoff/demo/`), réinitialisation sans toucher aux données versionnées, 7 captures dans `docs/captures/`.
- **Chiffres du script recoupés avec les données** le 2026-11-16 : 3 corrigés (38 besoins, canaux de la délivrabilité, thèmes dominants).

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Support de présentation ? | Diapositives, avec démonstration dans l'application | Diapositives : « oui, fais les slides » (Vlad, 2026-11-16) | answered |
| Q2 | Charte graphique ? | Neutre : le design system par défaut de l'organisation (celui de l'employeur actuel) ne convient pas pour un test destiné à une autre entreprise | Neutre, appliquée par défaut ; Vlad peut demander autre chose | parked |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- **Panne le jour J** (réseau, application) : captures de secours dans les diapositives 5 à 7.
- **Diapositives privées** : le jury ne peut pas les ouvrir tant qu'elles ne sont pas partagées ou exportées.

## Gate
- [x] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
