# Intent: socle agent : hand-off par fichiers et faux connecteur Linear

| | |
|---|---|
| **Cycle** | 002 |
| **Stage** | Intent |
| **Date** | 2026-11-16 |
| **Owner** | Vlad |
| **Importance** | 5/5 (claude, 2026-11-16): les cycles 003 à 006 reposent sur ce socle ; l'échéance est ce soir |

## The request, in your words
> on ne fera pas d'api ANTHROPIC
> j'utiliserai ici un skill claude code, qui ferait ce job (comme sur saxobeat)
> export des payloads en json ou autre format adequat
> le skill qui traite tout comme si c'était l'API
> puis import de la réponse dans l'app

## Why now / the pain
- Le travail d'IA des 3 blocs (comprendre, arbitrer, formaliser) doit passer par un mécanisme commun. Sans lui, rien ne fonctionne.
- Échéance : lundi 16/11 au soir (aujourd'hui).

## Goal
L'application lit l'espace Linear simulé (`data/linear.db`), exporte le travail d'IA sous forme de fichiers auto-suffisants (« packs »). Un skill Claude Code traite ces fichiers comme le ferait l'API. L'application réimporte les résultats après vérification et aperçu. Aucun appel d'API, aucune clé.

## Success measure
1. Un aller-retour complet export → skill → import fonctionne sur le pack « analyse » avec les 80 feedbacks, sans aucune clé API.
2. Un fichier de résultats invalide (schéma, identifiant inconnu, champ manquant) est refusé avec une raison lisible, sans rien écrire.
3. Importer deux fois le même fichier ne change rien la seconde fois.
4. Les tests passent sans LLM, grâce à des fichiers de résultats de référence.

## Not doing (this cycle)
- Le contenu métier des 3 blocs (cycles 003, 004 et 005). Ce cycle livre le mécanisme et le connecteur, avec le pack « analyse » comme premier usage.
- Un runner automatique : l'export, le lancement du skill et l'import restent des gestes manuels.
- Toute API LLM (Anthropic ou autre).

## What we already know (facts, with where they came from)
- **Pas d'API Anthropic ; un skill Claude Code traite des payloads exportés, puis l'application importe la réponse** : décision de Vlad, 2026-11-16 (chat).
- **Le modèle saxobeat** (`saxobeat reference/docs/PRD_ai_backoffice.md` §8) :
  - le fichier exporté « est le skill » : il contient le brief de l'agent, les instructions par type de tâche, le format de sortie avec un exemple, puis les données ;
  - les résultats reviennent en JSON (`schema`, `export`, `results[]` avec `task`, `kind`, `output` ou `skipped`) ;
  - à l'import : vérification sans écriture, aperçu, puis application ; les fichiers partiels sont acceptés ; un second import du même fichier est sans effet ;
  - dossiers `to-do\`, `done\`, `problems\` et `STATUS.txt`.
  En production sur saxobeat : 257 tâches IA sur 258 revenues traitées, en 8 packs (`saxobeat reference/docs/sdlc/cycles/027-cloud-ai-agent-step/intent.md`, d'après la synthèse du 2026-11-14).
- **Données prêtes** : `data/linear.db` (cycle 001 ; 11 tests verts). La vérité terrain (`data/ground_truth.json`) permet de mesurer la qualité des résultats importés.
- **Conséquence pour l'interface** : sans API, l'interface ne peut pas contenir de chat. La conversation avec l'agent a lieu dans Claude Code ; l'application montre les résultats et laisse le PO décider.

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | Format des payloads ? | Un fichier **JSON** par pack, auto-suffisant comme chez saxobeat : en-tête, brief de l'agent, instructions, schéma de sortie avec un exemple, puis les tâches. Le skill `.claude/skills/po-agent/` contient le mode opératoire commun (traiter tous les packs de `to-do/`, écrire `<pack>.results.json` à côté). Les résultats sont aussi en JSON | | open |
| Q2 | Dossier d'échange ? | `handoff/to-do`, `handoff/done`, `handoff/problems` (contenu non versionné). Des résultats de démo pré-calculés sont versionnés dans `handoff/demo/` pour rejouer la démo sans attendre le skill | | open |
| Q3 | Où stocker l'état de l'agent ? | Une base de travail séparée, `data/po_assist.db` (exports, tâches, résultats, scores, stories), non versionnée et recréable. `linear.db` reste « Linear » et n'est modifiée que sur une action explicite du PO (« Envoyer vers Linear ») | | open |
| Q4 | Interface (cycle 006) ? | **Streamlit** : Python uniquement, le plus rapide à livrer ce soir, suffisant pour des vues, des tableaux et des boutons. Pas de chat (cf. ci-dessus). Écarté : FastAPI + HTMX, plus proche de saxobeat mais trop long pour ce soir | | open |
| Q5 | Déclenchement ? | Boutons Exporter / Importer dans l'interface, et une ligne de commande équivalente (`po status`, `po export <pack>`, `po import <fichier>`) pour les tests et la démo | | open |
| Q6 | Découpage du travail d'IA en packs ? | 3 packs, un par bloc, enchaînés avec le PO entre chaque : **analyse** (classer, regrouper, extraire, rattacher), **priorisation** (estimer Impact, Confiance et Effort avec justification, proposer MoSCoW ; le score RICE est calculé par le code), **rédaction** (story, critères Gherkin, estimation) | | open |
| Q7 | Replanification pour tenir ce soir ? | Ordre : socle + analyse → priorisation → rédaction → interface → documentation et présentation. Un cycle par bloc, avec une documentation allégée (intent et spec fusionnés). Si le temps manque : la démo s'appuie sur les résultats pré-calculés | | open |

## Constraints and risks
- **Délai** : tout doit être livré ce soir, documentation et présentation comprises.
- **Démo en direct** : le traitement des 80 feedbacks par le skill prend plusieurs minutes. Les résultats pré-calculés servent de filet, et la démo en direct se fait sur un petit pack (quelques feedbacks).
- **Qualité non garantie des réponses du skill** : vérification stricte à l'import, et mesure contre la vérité terrain.

## Gate
- [ ] All open questions answered or parked
- [ ] Goal and success measure confirmed by the owner
