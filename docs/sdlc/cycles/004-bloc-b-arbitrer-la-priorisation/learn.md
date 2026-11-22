# Learn: bloc B arbitrer la priorisation

| | |
|---|---|
| **Cycle** | 004 |
| **Stage** | Learn |
| **Date** | 2026-11-22 |

## What happened vs what we expected
- Les 4 critères passent : 30 estimations importées (8 Must, 9 Should, 12 Could, 1 Won't), scores calculés par le code, corrections du PO appliquées, proposition de sprint dans la capacité (9,5 points disponibles sur 20).

## What we learned
- **L'IA estime, le code calcule** : Reach, RICE et score pondéré sont exacts et rejouables ; l'IA ne donne que des jugements justifiés et corrigibles.
- **Le Reach cache un choix produit** : en sièges, les comptes Business écrasent le B2C ; la bascule « personnes / clients » rend l'arbitrage visible au lieu de le trancher dans le code.
- **Pas de vérité terrain pour la priorisation** : la qualité se juge sur pièces.

## What moves where
| Finding | Goes to | Done |
|---------|---------|------|
| « L'IA estime, le code calcule » | `docs/demarche.md` §5, diapositive 10 | [x] |
| Biais du Reach et bascule | `docs/demarche.md` §3 et §6, diapositives 7 et 13 | [x] |

## Process feedback
- Le biais du Reach a été découvert à l'usage, pas en spec : une démo jouée tôt est un bon test de conception.

## Next cycle candidates
- Vérité terrain de priorisation à partir des décisions passées du PO.
- Pondération par segment fixée en équipe.
