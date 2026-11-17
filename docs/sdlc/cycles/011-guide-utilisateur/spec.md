# Spec: guide utilisateur

| | |
|---|---|
| **Cycle** | 011 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |
| **Date** | 2026-11-17 |

## Behaviour when finished
- `docs/guide-utilisateur.md` : le guide, en français, pour un PO. Les libellés de l'interface y sont cités en gras entre guillemets (**« Lancer l'agent »**), exactement comme à l'écran.
- `docs/guide/*.jpg` : une dizaine de captures de l'interface actuelle, prises en suivant le parcours.
- Une page **❓ Guide** dans l'application affiche ce même fichier, captures comprises. Le README pointe vers le guide.

## Acceptance criteria
1. [ ] Le guide suit le plan validé (Q3) : démarrer, vue d'ensemble, parcours pas à pas en mode démo, mode réel (skill puis API), lire les résultats, réglages et remise à zéro, dépannage, glossaire, annexe technique.
2. [ ] Chaque libellé cité en gras entre guillemets existe dans l'application (`app.py`), vérifié par un test.
3. [ ] Chaque image citée existe, vérifié par un test.
4. [ ] Les captures montrent l'interface actuelle (mode démo, bandeau, 9 pages).
5. [ ] En suivant le parcours du guide dans un navigateur (Playwright), on va de « Réinitialiser » à une story envoyée dans Linear.
6. [ ] La page ❓ Guide s'affiche sans erreur, images comprises ; le README y renvoie.

## Design in brief
- Une seule source (le Markdown) pour le dépôt et pour l'application : la page ❓ Guide découpe le fichier aux lignes d'image, affiche le texte avec `st.markdown` et les images avec `st.image`.
- Écarté : un guide dans l'application seulement (illisible depuis GitHub) ; un PDF (format plus lourd, contraire à la préférence de Vlad).

## Out of scope
- Simplifier l'interface ; vidéo ; traduction.

## Gate
- [x] Owner approved this spec (approbation préalable : « je valide les recommandations, go », Vlad, 2026-11-17)
