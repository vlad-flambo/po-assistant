# Plan: guide utilisateur

| | |
|---|---|
| **Cycle** | 011 |
| **Stage** | Plan |
| **Spec** | [spec.md](spec.md) |

## Slices
| # | Slice | Files touched | Check (test / measurement / drill) | Criteria | Status |
|---|-------|---------------|------------------------------------|----------|--------|
| 1 | Page ❓ Guide qui affiche le Markdown et ses images | `app.py` | AppTest | 6 | done |
| 2 | Captures neuves en déroulant le parcours jusqu'à l'envoi dans Linear | `docs/guide/*.jpg` | Le script Playwright suit le guide et aboutit | 4, 5 | done |
| 3 | Rédaction du guide | `docs/guide-utilisateur.md`, `README.md` | Relecture | 1 | done |
| 4 | Test des libellés et des images | `tests/test_guide.py` | `uv run pytest` | 2, 3 | done |

## Rollback
Supprimer la page et les fichiers ; rien d'autre n'est touché.

## Gate
- [x] Owner approved the slices (« je valide les recommandations, go », Vlad, 2026-11-17)

## As run
| Heure | Tranche | Ce qui s'est passé |
|---|---|---|
| 2026-11-17 | 1 | Page ❓ Guide : le Markdown est découpé aux lignes d'image (texte avec `st.markdown`, images avec `st.image`) |
| 2026-11-17 | 2 | 12 captures prises en suivant le parcours jusqu'à l'envoi dans Linear (SAX-301). **Reprise** : la capture de l'aperçu d'import s'arrêtait au titre ; défilement corrigé |
| 2026-11-17 | 3 | Guide rédigé avec 53 libellés cités tels qu'à l'écran ; lien depuis le README |
| 2026-11-17 | 4 | Test des libellés vert du premier coup ; test de rendu corrigé (type d'élément AppTest « image », pas « imgs ») ; 51 tests |
