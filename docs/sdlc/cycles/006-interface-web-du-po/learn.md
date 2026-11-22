# Learn: interface web du PO

| | |
|---|---|
| **Cycle** | 006 |
| **Stage** | Learn |
| **Date** | 2026-11-22 |

## What happened vs what we expected
- Les 3 critères passent : 7 pages (9 depuis : Réglages et Guide), démo rejouable sur un espace neuf, aucune erreur de rendu (AppTest).

## What we learned
- **Tester l'interface sans navigateur** (AppTest) a couvert le rendu ; le test navigateur du cycle 009 a quand même trouvé un défaut d'enchaînement (priorisation possible avant l'analyse).
- **Streamlit est proportionné** à un test : une seule langue, zéro front à maintenir.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| Choix de Streamlit | `docs/demarche.md` §5, Q&A de `docs/presentation.md` | [x] |

## Process feedback
- Garder au moins un parcours navigateur par cycle d'interface : les tests unitaires ne voient pas les enchaînements.

## Next cycle candidates
- Aucun.
