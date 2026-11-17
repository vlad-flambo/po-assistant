# Spec: API par défaut, skill en repli

| | |
|---|---|
| **Cycle** | 012 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |
| **Date** | 2026-11-17 |

## Acceptance criteria
1. [x] Sans réglage enregistré, le moteur est `api` ; `skill` reste choisissable dans ⚙️ Réglages (« Skill Claude Code, en local (repli) »).
2. [x] Sans identifiants, ou si l'API refuse la requête dès le premier paquet, le lancement se replie sur le skill : pack exporté, raison affichée (bandeau ↩️), aucune erreur bloquante.
3. [x] En mode démo : bouton « Lancer l'agent (API, ≈ x $) », progression « API : paquet k/n traité », message final avec « Coût simulé … rien n'est facturé » ; provenance indiquée dans le fichier de résultats.
4. [x] La logique du choix de moteur vit dans `po_assist/runner.py`, testable sans interface ; la ligne de commande `run` suit les réglages.
5. [x] README, guide (texte et captures), document de démarche, script de présentation, PROJECT.md et slides décrivent « API par défaut, skill en repli, démo = API simulée ».
6. [x] Tests verts, dont repli sans clé, repli sur clé refusée, API sans repli, démo paquet par paquet, bandeau de repli dans l'interface.

## Design in brief
- `runner.resolve(cfg)` donne le moteur effectif avant lancement (utile pour les libellés et le bandeau) ; `runner.run(...)` lance et gère le repli à l'exécution.
- Le mode démo réutilise le découpage et l'estimation du moteur API (`api_agent.batches`, `api_agent.estimate`), pour que la démo soit le même flux, sans appel.

## Gate
- [x] Owner approved this spec (demande directive de Vlad, 2026-11-17 ; choix Q1 à Q4 à relire)
