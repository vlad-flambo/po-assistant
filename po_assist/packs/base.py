from __future__ import annotations

import re
import unicodedata

NEW_TARGET = re.compile(r"^NEW:[a-z0-9]+(?:-[a-z0-9]+)*$")


def normalize(text: str) -> str:
    """Pour comparer une citation au texte source : casse, accents, guillemets et espaces neutralisés."""
    t = unicodedata.normalize("NFKD", text or "")
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("«", '"').replace("»", '"')
    t = re.sub(r"[*_`>#]", " ", t)  # la mise en forme Markdown des transcriptions de chat
    return re.sub(r"\s+", " ", t).strip()


def enum_error(name: str, value, allowed) -> list[str]:
    return [] if value in allowed else [f"{name} invalide : {value!r} (attendu : {', '.join(map(str, allowed))})"]
