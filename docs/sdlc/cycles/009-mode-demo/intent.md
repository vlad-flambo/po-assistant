# Intent: mode démo

| | |
|---|---|
| **Cycle** | 009 |
| **Stage** | Closed 2026-11-22 |
| **Date** | 2026-11-17 |
| **Owner** | Vlad |
| **Importance** | 4/5 (claude, 2026-11-17): la démo devant le jury doit montrer le parcours réel du PO sans attendre le skill (3 à 4 min pour 80 feedbacks) ni tout révéler d'un coup |

## The request, in your words
> nouveau intent. A enchainer directement si tout est clair.
>
> Je veux créer un mode démo, activé par défaut.
> Dans ce mode de démo, j'aurais pré-compute et pré-importé toutes les étapes de l'assistant, avec une véritable execution de l'IA via le skill pertinent.
> Ces données pre-computés seront cahcés, et révélé uniquement lorsque le parcours utilisateur aura été fait dans l'interface. Comme si j'executais les étapes avec les skills dans le background.

## Why now / the pain
- Aujourd'hui, le bouton « Charger les résultats pré-calculés » révèle les 3 étapes d'un coup : le jury ne voit pas le parcours (lancer l'agent, vérifier, importer, arbitrer, choisir les stories).
- Sans lui, il faut attendre le skill en direct : 3 à 4 minutes pour 80 feedbacks, incompatible avec 10 minutes de démonstration.
- Seules 5 stories sont pré-calculées : choisir un autre besoin en démo ne donnerait rien.

## Goal
En mode démo (activé par défaut), le PO suit le vrai parcours dans l'interface. Chaque fois qu'il lance l'agent, le résultat d'un vrai passage du skill, calculé à l'avance et tenu caché, « arrive » comme si le skill tournait en arrière-plan. Il passe ensuite par la même vérification et le même import que d'habitude.

## Success measure
1. Au premier lancement, rien n'est visible tant que le PO n'a pas lancé l'agent.
2. Analyse, priorisation et rédaction se jouent chacune en moins de 15 secondes, avec une progression visible.
3. N'importe quelle sélection de besoins à formaliser reçoit une story (couverture de 30 besoins sur 30).
4. Les résultats affichés sont ceux d'un vrai passage du skill, sans retouche, et le mode est signalé à l'écran.

## Not doing (this cycle)
- Rejouer le skill à chaque démo, ou faire varier les résultats.
- L'option API (cycle 010).

## What we already know (facts, with where they came from)
- **Résultats réels du skill déjà versionnés** (`handoff/demo/`, 2026-11-16) : analyse 80/80, priorisation 30/30, rédaction 5 (SAX-123, SAX-124, NEW:delivrabilite-emails, SAX-126, SAX-115).
- **30 besoins priorisés au total** (`scoring.table()` sur ces résultats), donc 25 stories manquantes. Pack exporté le 2026-11-17 et confié au skill en arrière-plan (`E-20261117-110405-redaction`).
- **Le parcours existe déjà** : export → fichier de résultats → `check()` (aperçu, refus) → `apply()` (`po_assist/handoff.py`). Le mode démo ne remplace que l'étape « le skill traite le pack ».
- **La réinitialisation** (`config.reset_workspace`) supprime `data/workspace/po_assist.db` : un réglage stocké là serait perdu à chaque remise à zéro.

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Compléter les stories pré-calculées ? | Oui : faire rédiger les 25 manquantes par le skill, pour couvrir toute sélection | Décidé par Claude (consigne « enchaîner si tout est clair »), à relire par Vlad | answered |
| Q2 | Durée simulée ? | Proportionnelle au nombre de tâches (environ 0,1 s par tâche, entre 3 et 10 s), avec une barre de progression | Idem | answered |
| Q3 | Garder l'aperçu et le bouton Importer ? | Oui : ce sont les garde-fous à montrer au jury | Idem | answered |
| Q4 | Que devient « Charger les résultats pré-calculés » ? | Supprimé : il révèle tout d'un coup, ce que la demande exclut. « Réinitialiser » reste | Idem | answered |
| Q5 | Le mode démo est-il signalé ? | Oui, en permanence : bandeau « Mode démo : résultats d'un vrai passage du skill, calculés à l'avance ». Honnêteté envers le jury | Idem | answered |
| Q6 | Où ranger le réglage ? | `data/workspace/settings.json`, qui survit à « Réinitialiser » ; page ⚙️ Réglages (reprise par le cycle 010) | Idem | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- **Transparence** : la démo ne doit jamais laisser croire que l'IA tourne en direct ; le bandeau et le nom de l'agent (« pré-calculé ») le disent.
- **Cohérence** : les besoins nouveaux (`NEW:`) de la priorisation viennent de l'analyse pré-calculée. Si le PO réimporte une autre analyse, certains sujets n'auront plus de résultat en cache. Ils reviennent alors « ignorés », sans être inventés.

## Gate
- [x] All open questions answered or parked
- [x] Goal and success measure confirmed by the owner (consigne de Vlad, 2026-11-17 : « A enchainer directement si tout est clair » ; choix Q1 à Q6 à relire)
