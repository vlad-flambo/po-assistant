# Verify: guide utilisateur

| | |
|---|---|
| **Cycle** | 011 |
| **Stage** | Verify |
| **Spec** | [spec.md](spec.md) |
| **Date** | 2026-11-17 |

## Evidence per acceptance criterion
| # | Criterion | Result | Evidence (command and output, measurement, screenshot, link) |
|---|-----------|--------|-------------------------------------------------------------|
| 1 | Plan validé (Q3) | pass | `test_guide_follows_the_validated_outline` : 9 sections, de « Démarrer » à l'annexe technique |
| 2 | Libellés cités = libellés de l'interface | pass | `test_every_cited_label_exists_in_the_app` : 53 libellés en gras entre guillemets, tous trouvés dans `app.py` (y compris les libellés dynamiques comme « Importer N résultat(s) ») |
| 3 | Images présentes | pass | `test_every_image_exists` : 12 images |
| 4 | Captures de l'interface actuelle | pass | Prises le 2026-11-17 en mode démo (bandeau, 9 pages) ; 3 relues à l'œil (aperçu d'import, sprint et rédaction, envoi dans Linear) |
| 5 | Parcours du guide jusqu'à une story dans Linear | pass | [evidence/parcours_guide_2026-11-17.md](evidence/parcours_guide_2026-11-17.md) : « Dans Linear : SAX-301 » |
| 6 | Page ❓ Guide et lien README | pass | `test_guide_page_renders_with_its_images` (12 images rendues) ; `test_readme_links_to_the_guide` |

## Tests
- `uv run pytest` : 51 passed ([evidence/pytest_2026-11-17.txt](evidence/pytest_2026-11-17.txt)).

## Not verified
- **Les sections 4.1 et 4.2 (skill, API) n'ont pas été suivies à la lettre dans un navigateur.** Elles décrivent des parcours vérifiés ailleurs : le skill par trois passages réels (cycles 002 à 005), l'API par un client simulé (cycle 010).
- **La lisibilité pour un PO** qui découvre l'outil : à juger par Vlad, ou mieux, par quelqu'un qui ne l'a jamais vu.
- 9 captures sur 12 n'ont été vérifiées que par le script (pas d'erreur, bonne page), sans relecture à l'œil.

## Verdict
- [ ] Accepted by owner
- [ ] Sent back (what, to which stage)
