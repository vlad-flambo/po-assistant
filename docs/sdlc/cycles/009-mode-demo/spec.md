# Spec: mode démo

| | |
|---|---|
| **Cycle** | 009 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |
| **Date** | 2026-11-17 |

## Behaviour when finished
- **Réglages** (nouvelle page ⚙️) : « Mode démo », activé par défaut, enregistré dans `data/workspace/settings.json`.
- **Mode démo activé** : un bandeau le signale. La page 🤖 Agent propose « Lancer l'agent » pour chaque étape. Le clic exporte le vrai pack, affiche une progression (« le skill po-agent traite 80 tâches… »), puis dépose le fichier de résultats, construit à partir des résultats réels pré-calculés pour exactement les sujets exportés. Le PO voit l'aperçu et importe.
- **Mode démo désactivé** : comportement actuel (export, skill lancé à la main, import).

## Acceptance criteria
1. [ ] Sans `settings.json`, le mode démo est actif ; le réglage se modifie dans ⚙️ Réglages et survit à « Réinitialiser ».
2. [ ] Au démarrage et après « Réinitialiser », aucune analyse, estimation ni story n'est importée. Le bouton « Charger les résultats pré-calculés » n'existe plus.
3. [ ] « Lancer l'agent » (démo) écrit un vrai pack, puis un fichier de résultats `po-assist.results.v1` dont l'agent porte la mention « pré-calculé ». Il contient une entrée par tâche, avec la sortie réelle du skill pour ce sujet, ou `skipped` si le cache n'en a pas.
4. [ ] La progression est visible et la durée simulée reste entre 3 et 10 secondes.
5. [ ] Le cache couvre 80 analyses, 30 estimations et 30 stories. Toute sélection de stories parmi les 30 besoins est servie.
6. [ ] Les résultats du cache passent la vérification en mode strict (0 refus).
7. [ ] Un bandeau signale le mode démo sur toutes les pages.
8. [ ] Tests : parcours démo complet (analyse → priorisation → rédaction) sur une base vierge, réglage par défaut, sujet absent du cache renvoyé `skipped`, rendu de toutes les pages dans les deux modes.

## Design in brief
- `po_assist/settings.py` : lecture et écriture de `settings.json`, avec les valeurs par défaut.
- `po_assist/demo.py` : index du cache (type de tâche + sujet → sortie réelle, depuis `handoff/demo/*.results.json` et leurs packs) et `run(pack)`, qui exporte puis écrit le fichier de résultats.
- Le reste du parcours est inchangé : vérification, aperçu, import (`handoff.check/apply`).
- Écarté : pré-importer en base et masquer à l'affichage. Le parcours réel (export, vérification, import) ne serait plus joué.

## Out of scope
- L'option API (cycle 010).

## Gate
- [x] Owner approved this spec (consigne « A enchainer directement si tout est clair », Vlad, 2026-11-17)
