# Learn: guide utilisateur

| | |
|---|---|
| **Cycle** | 011 |
| **Stage** | Learn |
| **Date** | 2026-11-22 |

## What happened vs what we expected
- Les 6 critères passent : 45 libellés cités tous présents dans l'interface, 12 captures, parcours suivi jusqu'à une story dans Linear, page ❓ Guide et lien README.

## What we learned
- **Un test qui lit le guide** empêche qu'il se périme en silence : il a cassé dès le cycle 013 sur « API Claude (recommandé) », ce qui a forcé la mise à jour.
- **Les captures ne sont pas testées** : deux ont dû être refaites au cycle 013 (coût et libellés).

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| Guide, une seule source (dépôt et application) | `docs/guide-utilisateur.md`, page ❓ | [x] |

## Process feedback
- Les captures restent le point faible : un script de reprise des captures éviterait les retouches à la main.

## Next cycle candidates
- Script qui reprend toutes les captures du guide en une commande.
