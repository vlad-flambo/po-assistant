# Learn: lanceur Mac (port 8007)

| | |
|---|---|
| **Cycle** | 008 |
| **Stage** | Learn |
| **Date** | 2026-11-22 |

## What happened vs what we expected
- Les 8 critères passent, dont le double-clic sur le Mac de Vlad (« works, tested successfully », 2026-11-22, après la migration de compte).

## What we learned
- **Tester le shell de macOS ailleurs a suffi** : les 4 scénarios rejoués sous Linux (bash 5) avec une fausse commande `open` ont prédit le comportement sur le Mac (bash 3.2).
- **Un lanceur double-cliquable** retire une étape de la démo et du guide.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| Démarrage par double-clic | `README.md` (« Démarrer »), guide §1, `docs/presentation.md` (avant la démo) | [x] |

## Process feedback
- Le critère « sur le Mac de Vlad » est resté ouvert 5 jours : les vérifications qui demandent la machine du PO gagnent à être groupées en une seule séance (fait ainsi dans le plan de clôture).

## Next cycle candidates
- Aucun.
