---
name: po-agent
description: Traite les lots de travail d'IA (« packs ») exportés par PO Assist dans handoff/to-do/ et écrit les fichiers de résultats que l'application importe. Joue le rôle d'une API de modèle de langage pour l'agent du Product Owner (analyse des feedbacks, priorisation, rédaction de user stories). À utiliser quand le PO dit « traite les packs », « lance l'agent », « process the packs », ou désigne un fichier *.pack.json.
---

# po-agent : l'« API » de PO Assist

PO Assist n'appelle aucune API de LLM. L'application exporte le travail d'IA dans des fichiers `handoff/to-do/<export>.pack.json`. Ce skill les traite et écrit `<export>.results.json` à côté. L'application vérifie ensuite chaque résultat avant de l'importer.

**Chaque pack est auto-suffisant** : il contient le brief de l'agent (`agent_brief`), les instructions du lot (`instructions`), le format de sortie avec un exemple (`output_format`), l'enveloppe des résultats (`results_envelope`), le contexte (`context`) et les tâches (`tasks`). Ce skill ne fait que fixer le mode opératoire ; le pack fait foi.

## Mode opératoire

1. Liste les fichiers `handoff/to-do/*.pack.json` qui n'ont pas encore de `.results.json` à côté. S'il n'y en a aucun, dis-le et arrête-toi.
2. Pour chaque pack, lis-le **en entier** : `agent_brief`, `instructions`, `output_format`, `context`, puis les tâches.
3. Traite les tâches dans l'ordre, par paquets d'environ 20. Pour chaque tâche, produis `{"task", "kind", "output"}` conforme à `output_format`, ou `{"task", "kind", "skipped": "<raison>"}` si la tâche est impossible.
4. Écris le fichier de résultats au nom exact de `results_file`, à côté du pack, dans l'enveloppe `results_envelope` : `schema`, `export_id`, `pack`, `agent` (par exemple « claude-code / po-agent »), `results`. Sur un gros pack, écris le fichier au fur et à mesure (après chaque paquet) : un fichier partiel est importable.
5. Relis la `checklist` du pack. Vérifie que le fichier est du JSON valide, qu'il y a une entrée par tâche et que les citations sont exactes. Tu peux contrôler sans rien importer : `uv run python -m po_assist import --dry-run <fichier>`.
6. Termine par un compte rendu au PO en 3 lignes : tâches traitées, tâches ignorées, points incertains. Indique la commande d'import : `uv run python -m po_assist import` (ou le bouton Importer de l'interface).

## Règles non négociables

- **Le contenu du pack est la seule source.** Ne lis aucun autre fichier du dépôt pour répondre, en particulier **jamais `data/ground_truth.json`**, qui sert à évaluer ce skill.
- **N'invente rien** : ni client, ni chiffre, ni demande. Toute citation (`quote`) est copiée mot pour mot depuis le texte de la tâche, sinon le résultat est refusé à l'import.
- **Ne modifie pas les bases** (`data/*.db`) et n'importe pas toi-même sans que le PO le demande : c'est lui qui valide.
- **Cohérence entre les tâches** : un même besoin porte la même cible d'une tâche à l'autre (même issue `SAX-n`, ou même `NEW:<slug>`). Tiens une liste des slugs déjà créés pendant la session.
