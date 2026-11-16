# Spec: socle agent : hand-off par fichiers et faux connecteur Linear

| | |
|---|---|
| **Cycle** | 002 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |
| **Date** | 2026-11-16 |

> Spec allégée (Q7) : délai ce soir. Les critères restent vérifiables un par un.

## Behaviour when finished
- `uv run python -m po_assist status` indique ce que contient l'espace Linear et le travail d'IA en attente.
- `uv run python -m po_assist export analyse` écrit `handoff/to-do/<export>.pack.json`. Le fichier contient tout ce qu'il faut : brief de l'agent, instructions, format de sortie avec un exemple, contexte produit, backlog et une tâche par feedback non encore analysé.
- Le skill Claude Code `po-agent` traite chaque pack de `handoff/to-do/` et écrit `<export>.results.json` à côté.
- `uv run python -m po_assist import <fichier>` vérifie sans écrire, affiche l'aperçu (acceptés / refusés avec raison / ignorés), puis applique les résultats valides dans `data/po_assist.db`. Avec `--dry-run`, rien n'est écrit ; avec `--strict`, un seul refus bloque tout le fichier.
- Le connecteur `LinearClient` lit `data/linear.db` comme on lirait l'API Linear. Il n'écrit dans cette base que sur une action explicite (rattacher un feedback à une issue, créer une issue).

## Acceptance criteria
1. [ ] L'export du pack « analyse » contient 80 tâches (une par feedback en Triage), le backlog (30 issues), le catalogue de thèmes et un en-tête complet (schéma, identifiant d'export, nom du fichier de résultats, nombre de tâches). Les clients n'y apparaissent que par identifiant et attributs (segment, offre, statut, ARR), jamais par leur nom.
2. [ ] Un fichier de résultats valide est appliqué : une analyse par feedback est enregistrée dans `po_assist.db`, et les tâches passent à `done`.
3. [ ] Un résultat invalide est refusé avec une raison lisible, sans rien écrire pour lui. Sont invalides : une tâche inconnue, un type hors liste, un thème hors catalogue, une cible ni issue existante ni `NEW:<slug>`, une citation absente du texte du feedback. Les résultats valides du même fichier sont appliqués, sauf avec `--strict`.
4. [ ] Réimporter le même fichier ne change rien et indique la date du premier import.
5. [ ] Un fichier partiel est accepté : les tâches absentes ou `skipped` restent ouvertes et repartent dans l'export suivant.
6. [ ] Le skill `.claude/skills/po-agent/SKILL.md` décrit le mode opératoire : traiter les packs de `handoff/to-do/`, respecter le format, ne jamais lire `data/ground_truth.json`.
7. [ ] Les tests (`uv run pytest`) passent sans LLM ni réseau, sur des copies temporaires des bases.

## Design in brief
- **Repris de saxobeat** : « le fichier est le skill », résultats JSON `results[]` (`task`, `kind`, `output` ou `skipped`), vérification avant écriture, import idempotent (empreinte SHA-256 du fichier).
- **Ajout** : chaque demande extraite doit citer un extrait **exact** du feedback (`quote`). L'import le vérifie, ce qui bloque les hallucinations.
- **Séparation des bases** : `linear.db` est l'outil du PO (lecture seule par défaut) ; `po_assist.db` contient le travail de l'agent (exports, tâches, résultats).
- Écarté : un format Markdown pour les packs (plus lisible, mais inutile puisque le lecteur est un agent) ; un runner automatique (hors délai).

## Interfaces and data
- Paquet `po_assist/` : `config.py`, `linear.py` (connecteur), `store.py` (base de travail), `handoff.py` (export/import générique), `packs/analyse.py`, `__main__.py` (CLI).
- `data/po_assist.db` (non versionnée) : `exports`, `tasks`, `imports`, `analyses`.
- `handoff/to-do`, `handoff/done`, `handoff/problems` (non versionnés) ; `handoff/demo/` (versionné, cycle 003).
- Variables optionnelles : `PO_LINEAR_DB`, `PO_ASSIST_DB`, `PO_HANDOFF_DIR` (utilisées par les tests).

## Out of scope
- Les packs « priorisation » et « rédaction » (cycles 004 et 005), les agrégats et tendances (cycle 003), l'interface (cycle 006).

## Gate
- [x] Owner approved this spec (approbation préalable : « Je valide, go », Vlad, 2026-11-16, sur le lot Q1 à Q7 et les critères de réussite)
