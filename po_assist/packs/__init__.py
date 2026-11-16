"""Registre des packs (lots de travail d'IA). Chaque pack sait : quoi exporter, avec quelles instructions,
et comment vérifier un résultat avant import."""
from __future__ import annotations

from .analyse import AnalysePack
from .priorisation import PriorisationPack
from .redaction import RedactionPack

PACKS = {p.name: p for p in [AnalysePack(), PriorisationPack(), RedactionPack()]}
