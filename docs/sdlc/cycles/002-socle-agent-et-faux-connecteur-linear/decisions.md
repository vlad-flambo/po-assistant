# Decisions: socle agent

One entry per decision, newest last. Do not edit old entries: add a new one that supersedes.

## D1. Pas d'API LLM : l'IA passe par un skill Claude Code et un échange de fichiers
- **Date:** 2026-11-16
- **Context:** l'agent a besoin d'un LLM pour comprendre, estimer et rédiger. Il n'y a pas de clé API dans l'environnement.
- **Options considered:** API Anthropic ; échange de fichiers traités par un skill Claude Code (modèle saxobeat).
- **Decision:** l'application exporte des payloads, un skill Claude Code les traite « comme si c'était l'API », l'application importe la réponse.
- **Why:** décision de Vlad ; architecture déjà éprouvée en production sur saxobeat ; zéro clé, zéro coût par appel ; le PO garde la main à chaque étape (human-in-the-loop par construction).
- **Consequences:** pas de chat dans l'interface. Le temps de traitement n'est pas instantané, d'où les résultats pré-calculés pour la démo. La validation à l'import devient centrale. Remplace l'hypothèse « clé ANTHROPIC_API_KEY pour la démo ».
