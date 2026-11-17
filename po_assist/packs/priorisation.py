"""Pack « priorisation » (bloc B, ARBITRER) : une tâche par besoin ouvert (issue du backlog ou NEW:<slug>).

L'agent estime Impact, Confiance, Effort et propose MoSCoW avec une justification sourcée.
Le Reach et le score sont calculés par le code (po_assist/scoring.py), jamais par le LLM.
"""
from __future__ import annotations

from .base import enum_error

IMPACTS = [3, 2, 1, 0.5, 0.25]
CONFIDENCES = [1.0, 0.8, 0.5]
FIBONACCI = [1, 2, 3, 5, 8, 13]
MOSCOW = ["must", "should", "could", "wont"]
OPEN_STATES = ("Backlog", "Todo", "À créer")

INSTRUCTIONS = """\
Pack « priorisation » : pour chaque besoin (issue ouverte du backlog ou besoin nouveau « NEW: » issu des feedbacks),
donne au PO les estimations qui lui manquent pour arbitrer. Le Reach (personnes touchées) et le score RICE sont calculés
par l'application à partir des données : ne les recalcule pas, appuie-toi sur eux.

Pour chaque tâche :
1. impact : l'effet pour chaque personne touchée, sur l'échelle RICE : 3 massif, 2 fort, 1 moyen, 0.5 faible, 0.25
   minimal. Tiens compte de la gravité (bloquant ou confort), de l'argent en jeu (ARR Business à risque, abonnés Plus)
   et de l'alignement avec les objectifs du trimestre (context.okrs).
2. confidence : ta confiance dans ces estimations : 1.0 (preuves nombreuses et convergentes), 0.8 (preuves
   correctes), 0.5 (une ou deux mentions, besoin flou).
3. effort_points : l'effort en points Fibonacci (1, 2, 3, 5, 8, 13). Si l'issue a déjà une estimation de l'équipe,
   reprends-la sauf raison explicite (dis-la dans rationale).
4. moscow : must, should, could ou wont, pour le trimestre en cours (jusqu'au 30 juin 2027). « must » est réservé à ce
   qui bloque un objectif, fait perdre des clients ou casse le produit.
5. okr : l'identifiant de l'objectif du trimestre servi en premier (context.okrs), ou null.
6. rationale : 2 à 4 phrases pour le PO, qui citent les preuves de l'entrée (nombre de clients, segments, ARR, tendance,
   une citation) : c'est la justification que le PO présentera à l'équipe.
7. risks : un risque ou une dépendance à connaître (technique, juridique, produit), ou null.
"""

OUTPUT_FORMAT = {
    "description": "Un objet par tâche, dans le champ output du fichier de résultats.",
    "fields": {
        "impact": f"une valeur parmi {IMPACTS}",
        "confidence": f"une valeur parmi {CONFIDENCES}",
        "effort_points": f"une valeur parmi {FIBONACCI}",
        "moscow": f"une valeur parmi {MOSCOW}",
        "okr": "identifiant d'objectif de context.okrs, ou null",
        "rationale": "chaîne, 2 à 4 phrases",
        "risks": "chaîne ou null",
    },
    "example": {
        "impact": 2, "confidence": 0.8, "effort_points": 8, "moscow": "must", "okr": "ini_b2b",
        "rationale": "Réclamé par 4 comptes Business (190 sièges), dont Cap Rebond (36 k€) qui conditionne son renouvellement de mai à ce tableau. C'est le prérequis de l'objectif O3.",
        "risks": "Confidentialité : certains candidats ne veulent pas que leur conseiller voie toutes leurs candidatures.",
    },
}


OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "impact": {"type": "number", "enum": IMPACTS},
        "confidence": {"type": "number", "enum": CONFIDENCES},
        "effort_points": {"type": "integer", "enum": FIBONACCI},
        "moscow": {"type": "string", "enum": MOSCOW},
        "okr": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "rationale": {"type": "string"},
        "risks": {"anyOf": [{"type": "string"}, {"type": "null"}]},
    },
    "required": ["impact", "confidence", "effort_points", "moscow", "okr", "rationale", "risks"],
    "additionalProperties": False,
}


class PriorisationPack:
    name = "priorisation"
    kind = "prioritization"
    version = 1
    instructions = INSTRUCTIONS
    output_format = OUTPUT_FORMAT
    output_schema = OUTPUT_SCHEMA
    batch_size = 20

    def _demands(self, linear, store):
        from .. import insights
        return insights.demands(insights.load(linear, store))

    def items(self, linear, store) -> list[dict]:
        if not store.results("feedback_analysis"):
            return []  # prioriser sans les preuves des feedbacks n'a pas de sens : l'analyse vient d'abord
        done = store.subjects_done(self.kind)
        demand = {d["target"]: d for d in self._demands(linear, store)}
        items = []
        for b in linear.backlog_issues():
            if b["state_name"] in OPEN_STATES and b["identifier"] not in done:
                items.append(self._item(b["identifier"], demand.get(b["identifier"]), b))
        for tgt, d in demand.items():
            if d["is_new"] and tgt not in done:
                items.append(self._item(tgt, d, None))
        return items

    @staticmethod
    def _item(target, d, b) -> dict:
        ev = {k: (d or {}).get(k, 0) for k in ("mentions", "historic_requests", "customers", "b2c", "b2b", "plus", "reach",
                                               "arr_b2b_eur", "churn_customers", "arr_at_risk_eur", "recent_4w")}
        quotes = [q["quote"] for q in (d or {}).get("quotes", [])[:4]]
        return {"subject": target, "input": {
            "target": target,
            "title": b["title"] if b else d["title"],
            "description": b["description"][:600] if b else " / ".join(sorted(set(d["summaries"]))[:4]),
            "state": b["state_name"] if b else "À créer",
            "current_priority": b["priority"] if b else None,
            "team_estimate": b["estimate"] if b else None,
            "project": b["project_name"] if b else None,
            "evidence": ev,
            "quotes": quotes,
        }}

    def context(self, linear, store) -> dict:
        meta = linear.meta()
        return {
            "product": meta.get("product"),
            "reference_date": meta.get("reference_date"),
            "okrs": [{"id": i["id"], "name": i["name"], "description": i["description"]} for i in linear.initiatives()],
            "projects": [{"name": p["name"], "initiative": p["initiative_name"], "description": p["description"]} for p in linear.projects()],
            "capacity_points_per_cycle": meta.get("team_capacity_points_per_cycle"),
            "velocity_last_cycles": meta.get("velocity_last_cycles"),
            "metrics": meta.get("metrics_snapshot"),
            "reach_definition": "Personnes touchées : 1 par candidat qui a exprimé le besoin, le nombre de sièges pour un compte Business.",
        }

    def validation_context(self, linear, store) -> dict:
        return {"okrs": {i["id"] for i in linear.initiatives()}}

    def validate(self, out: dict, subject: str, ctx: dict) -> list[str]:
        errs = []
        errs += enum_error("impact", out.get("impact"), IMPACTS)
        errs += enum_error("confidence", out.get("confidence"), CONFIDENCES)
        errs += enum_error("effort_points", out.get("effort_points"), FIBONACCI)
        errs += enum_error("moscow", out.get("moscow"), MOSCOW)
        if out.get("okr") is not None and out.get("okr") not in ctx["okrs"]:
            errs.append(f"okr inconnu : {out.get('okr')!r}")
        if not isinstance(out.get("rationale"), str) or len(out["rationale"].strip()) < 20:
            errs.append("rationale manquante ou trop courte")
        if out.get("risks") is not None and not isinstance(out.get("risks"), str):
            errs.append("risks doit être une chaîne ou null")
        return errs
