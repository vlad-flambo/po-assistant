# Decisions: Moteur API Mistral

## 013-D1 Mistral par défaut, Claude au choix (2026-11-22)
- **Context:** la seule clé API disponible chez Vlad est une clé Mistral ; le moteur API par défaut (012-D1) n'avait jamais tourné en réel.
- **Decision:** le modèle par défaut devient `mistral-large-latest` ; le fournisseur se déduit du modèle ; les modèles Claude restent choisissables. Complète 012-D1 (API par défaut, skill en repli), qui reste valable.
- **Decided by:** Vlad (« Default to Mistral »).
- **Consequences:** le récit devient « API par défaut, Mistral ou Claude au choix du PO, skill en repli » ; tarifs Mistral affichés comme estimations jusqu'à l'essai réel.
