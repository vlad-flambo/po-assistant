# Decisions: API par défaut, skill en repli

## D1. L'API devient le moteur par défaut ; le skill passe en repli (remplace 002-D1)
- **Date:** 2026-11-17
- **Context:** 002-D1 (2026-11-16) avait écarté l'API pour tenir le délai ; le cycle 010 l'a ajoutée en option.
- **Decision:** « Lancer l'agent » appelle l'API Claude par défaut. Sans identifiants, ou si l'API refuse la requête dès le premier paquet, l'outil se replie sur le skill Claude Code local. La démo simule le flux API.
- **Why:** demande de Vlad ; c'est le comportement attendu d'une intégration en production, sans geste manuel. Le skill garde sa valeur : zéro clé, et un repli quand l'API est indisponible.
- **Consequences:** documentation, guide (et captures) et slides changent de récit : « API par défaut, skill en repli ».
