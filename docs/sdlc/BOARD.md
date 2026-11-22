# Cycle board

Generated 2026-11-22 15:41 by the ai-sdlc skill from `cycles/*/`. Do not edit by hand: change the cycle's files and run the script again.

Stages: `x` done, `o` in progress, `-` up next, `.` later, `~` dismissed.

## What next?

**Your move**

- 002 Socle agent : hand-off par fichiers et faux connecteur Linear: Accepter la vérification (verify.md) (due 2026-11-16)
- 007 Restitution documentation et démo: Répéter la démo avec docs/presentation.md (Réinitialiser, puis jouer le parcours en mode démo : Lancer l'agent → Importer, étape par étape) (due 2026-11-16)
- 007 Restitution documentation et démo: Confirmer le but et la mesure de succès du cycle 007 (due 2026-11-16)
- 003 Bloc A comprendre les feedbacks: Accepter la vérification (verify.md) (due 2026-11-16)
- 004 Bloc B arbitrer la priorisation: Accepter la vérification (verify.md) (due 2026-11-16)
- 005 Bloc C formaliser les user stories: Accepter la vérification (verify.md) (due 2026-11-16)
- 006 Interface web du PO: Accepter la vérification (verify.md) (due 2026-11-16)
- 009 Mode démo: Accepter la vérification (verify.md) après un essai du parcours démo (due 2026-11-17)
- 011 Guide utilisateur: Relire docs/guide-utilisateur.md (ou la page ❓ Guide) et accepter la vérification (due 2026-11-17)
- 008 Lanceur Mac (port 8007): Après `git pull` : double-cliquer sur « PO Assist.command » sur le Mac et me dire ce qui s'affiche (critère 8) (due 2026-11-17)
- 007 Restitution documentation et démo: Relire les diapositives reconstruites, puis les partager avec le jury (menu Partager) ou les exporter en PDF
- 009 Mode démo: Relire les choix Q1 à Q6 de l'intent
- 012 API par défaut, skill en repli: Relire les choix Q1 à Q4 de l'intent et accepter verify.md
- 013 Moteur API Mistral: Sur le Mac : `git pull`, `uv sync`, ajouter `MISTRAL_API_KEY=...` dans `.env`, puis `uv run python -m po_assist run analyse --engine api --limit 5` et `uv run python -m po_assist import` ; me dire la sortie (critère 8)
- 013 Moteur API Mistral: Accepter verify.md après l'essai
- 010 Option API: Relire les choix Q1 à Q6 de l'intent
- 010 Option API: Accepter verify.md une fois l'essai du cycle 013 fait

**My move (the agent)**

- 007 Restitution documentation et démo: Tenir docs/journal.md à jour à chaque étape (registre de l'usage de l'IA inclus)
- 007 Restitution documentation et démo: Après la présentation : verify.md (répétition, partage) et learn.md
- 013 Moteur API Mistral: Après l'essai : noter le coût réel et le comportement du mode strict dans verify.md, puis learn.md

## Cycles

| # | Cycle | Imp. | Now | Intent | Spec | Plan | Build | Verify | Learn | Criteria | Touched |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 001 | Jeu de données synthétique | 5/5 | Closed | x | x | x | x | x | x | 12/12 | 2026-11-22 |
| 002 | Socle agent : hand-off par fichiers et faux connecteur Linear | 5/5 | Verify | x | x | x | x | o | . | 7/7 | 2026-11-21 |
| 003 | Bloc A comprendre les feedbacks | 4/5 | Verify | x | x | x | x | o | . | 5/5 | 2026-11-21 |
| 004 | Bloc B arbitrer la priorisation | 4/5 | Verify | x | x | x | x | o | . | 4/4 | 2026-11-21 |
| 005 | Bloc C formaliser les user stories | 4/5 | Verify | x | x | x | x | o | . | 4/4 | 2026-11-21 |
| 006 | Interface web du PO | 4/5 | Verify | x | x | x | x | o | . | 3/3 | 2026-11-21 |
| 007 | Restitution documentation et démo | 5/5 | Intent | o | . | . | . | . | . |  | 2026-11-22 |
| 008 | Lanceur Mac (port 8007) | 3/5 | Verify | x | x | x | x | o | . | 7/8 | 2026-11-21 |
| 009 | Mode démo | 4/5 | Verify | x | x | x | x | o | . | 8/8 | 2026-11-21 |
| 010 | Option API | 3/5 | Verify | x | x | x | x | o | . | 8/10 | 2026-11-22 |
| 011 | Guide utilisateur | 4/5 | Verify | x | x | x | x | o | . | 6/6 | 2026-11-21 |
| 012 | API par défaut, skill en repli | 4/5 | Verify | x | x | x | x | o | . | 6/6 | 2026-11-22 |
| 013 | Moteur API Mistral | 4/5 | Verify | x | x | x | x | o | . | 7/8 | 2026-11-22 |
