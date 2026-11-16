"""Pack « rédaction » (bloc C, FORMALISER) : une user story par besoin priorisé choisi par le PO."""
from __future__ import annotations

from .base import enum_error
from .priorisation import FIBONACCI

INVEST = ["independent", "negotiable", "valuable", "estimable", "small", "testable"]
DEFAULT_TOP = 5

INSTRUCTIONS = """\
Pack « rédaction » : pour chaque besoin priorisé, rédige une user story prête à être discutée en affinage puis
poussée dans Linear. Écris en français, pour une équipe produit (PO, développeurs, designer).

Pour chaque tâche :
1. title : un titre d'issue Linear court, orienté résultat (moins de 80 caractères).
2. user_story : {as_a, i_want, so_that}. Le persona est précis et vient des preuves (ex. « conseiller d'un cabinet
   d'outplacement », « candidat en offre Free sur téléphone »), pas « utilisateur ».
3. context : 2 à 4 phrases qui expliquent pourquoi maintenant, en citant les preuves de l'entrée (nombre de clients,
   segments, ARR, citation). C'est ce qui relie la story aux feedbacks.
4. acceptance_criteria : 3 à 7 critères au format Gherkin {title, given, when, then}, testables, couvrant le cas
   nominal, au moins un cas limite ou d'erreur, et le mobile si l'usage est mobile.
5. non_functional : exigences non fonctionnelles pertinentes (performance, confidentialité, accessibilité,
   compatibilité) ; liste vide si aucune.
6. out_of_scope : ce que la story ne fait pas (évite le glissement de périmètre).
7. invest : pour chacun de independent, negotiable, valuable, estimable, small, testable : {ok: booléen, note}.
8. estimate_points : estimation relative en points Fibonacci (1, 2, 3, 5, 8, 13), et estimate_rationale : ce qui
   pèse dans l'estimation (complexité, inconnues, dépendances). Si l'équipe a déjà estimé, explique tout écart.
9. split_proposal : si estimate_points ≥ 8 ou si « small » n'est pas respecté, 2 à 4 stories plus petites
   (titres) livrables séparément ; sinon liste vide.
10. open_questions : les questions à trancher avec le PO ou les clients avant le développement.
N'invente pas de faits qui ne sont pas dans l'entrée : pour une hypothèse, formule-la en question ouverte.
"""

OUTPUT_FORMAT = {
    "description": "Un objet par tâche, dans le champ output du fichier de résultats.",
    "fields": {
        "title": "chaîne (< 80 caractères)",
        "user_story": "{as_a, i_want, so_that} : chaînes",
        "context": "chaîne",
        "acceptance_criteria": "liste de 3 à 7 objets {title, given, when, then}",
        "non_functional": "liste de chaînes",
        "out_of_scope": "liste de chaînes",
        "invest": f"objet avec les clés {INVEST}, chacune {{ok: booléen, note: chaîne}}",
        "estimate_points": f"une valeur parmi {FIBONACCI}",
        "estimate_rationale": "chaîne",
        "split_proposal": "liste de chaînes (titres), vide si inutile",
        "open_questions": "liste de chaînes",
    },
    "example": {
        "title": "Rappel e-mail quand une relance de candidature est due",
        "user_story": {"as_a": "candidat abonné Plus qui suit plusieurs candidatures",
                       "i_want": "recevoir un e-mail le jour où une relance est due",
                       "so_that": "je ne laisse plus une candidature s'endormir faute d'y avoir pensé"},
        "context": "5 clients l'ont demandé depuis février, dont un abonné Plus qui a résilié le 1er avril faute de rappels (« je retourne à mon tableur »).",
        "acceptance_criteria": [
            {"title": "Rappel envoyé à échéance", "given": "une candidature au statut Postulé avec une date de relance au 15/04",
             "when": "le 15/04 à 8 h", "then": "le candidat reçoit un e-mail qui nomme l'offre et l'employeur, avec un lien vers la candidature"},
            {"title": "Pas de rappel si déjà relancé", "given": "la candidature est passée en Entretien avant l'échéance",
             "when": "la date de relance arrive", "then": "aucun e-mail n'est envoyé"},
            {"title": "Désactivation", "given": "le candidat a coupé les rappels dans Réglages", "when": "une relance est due",
             "then": "aucun e-mail n'est envoyé et le rappel reste visible dans le Pipeline"},
        ],
        "non_functional": ["E-mail authentifié (SPF/DKIM) pour ne pas finir en spam"],
        "out_of_scope": ["Résumé hebdomadaire (story séparée)"],
        "invest": {k: {"ok": True, "note": ""} for k in INVEST},
        "estimate_points": 5,
        "estimate_rationale": "Planificateur existant ; modèle d'e-mail et préférence à créer.",
        "split_proposal": [],
        "open_questions": ["Heure d'envoi fixe ou selon le fuseau du candidat ?"],
    },
}


class RedactionPack:
    name = "redaction"
    kind = "user_story"
    version = 1
    instructions = INSTRUCTIONS
    output_format = OUTPUT_FORMAT

    def items(self, linear, store, subjects: list[str] | None = None) -> list[dict]:
        from .. import insights, scoring
        done = store.subjects_done(self.kind)
        rows = scoring.table(linear, store)
        if not subjects:
            rows = [r for r in rows if r["moscow"] in ("must", "should")][:DEFAULT_TOP]
        data = insights.load(linear, store)
        demand = {d["target"]: d for d in insights.demands(data)}
        by = {r["target"]: r for r in scoring.table(linear, store)}
        out = []
        for r in rows if not subjects else [by[s] for s in subjects if s in by]:
            if r["target"] in done:
                continue
            d = demand.get(r["target"], {})
            b = data["backlog"].get(r["target"])
            segs = sorted({data["customers"][q["customer_id"]]["segment"] + "/" + data["customers"][q["customer_id"]]["plan"]
                           for q in d.get("quotes", []) if q.get("customer_id") in data["customers"]})
            out.append({"subject": r["target"], "input": {
                "target": r["target"], "title": r["title"], "state": r["state"],
                "description": b["description"] if b else " / ".join(sorted(set(d.get("summaries", [])))),
                "project": r["project"],
                "prioritization": {k: r[k] for k in ("rice", "reach", "impact", "confidence", "effort", "moscow", "okr", "rationale", "risks")},
                "evidence": {k: d.get(k, 0) for k in ("mentions", "customers", "b2c", "b2b", "plus", "arr_b2b_eur", "arr_at_risk_eur")},
                "customer_segments": segs,
                "quotes": [q["quote"] for q in d.get("quotes", [])][:6],
                "team_estimate": b["estimate"] if b else None,
            }})
        return out

    def context(self, linear, store) -> dict:
        meta = linear.meta()
        return {
            "product": meta.get("product"),
            "plans": meta.get("plans"),
            "estimate_scale": meta.get("estimate_scale"),
            "okrs": [{"id": i["id"], "name": i["name"]} for i in linear.initiatives()],
            "backlog_titles": [{"identifier": b["identifier"], "title": b["title"], "state": b["state_name"]} for b in linear.backlog_issues()],
        }

    def validation_context(self, linear, store) -> dict:
        return {}

    def validate(self, out: dict, subject: str, ctx: dict) -> list[str]:
        errs = []
        if not isinstance(out.get("title"), str) or not (5 <= len(out["title"]) <= 100):
            errs.append("title manquant ou trop long")
        us = out.get("user_story")
        if not isinstance(us, dict) or not all(isinstance(us.get(k), str) and us[k].strip() for k in ("as_a", "i_want", "so_that")):
            errs.append("user_story incomplète (as_a, i_want, so_that)")
        if not isinstance(out.get("context"), str) or not out["context"].strip():
            errs.append("context manquant")
        ac = out.get("acceptance_criteria")
        if not isinstance(ac, list) or not 3 <= len(ac) <= 7:
            errs.append("acceptance_criteria : 3 à 7 critères attendus")
        else:
            for k, c in enumerate(ac, 1):
                if not isinstance(c, dict) or not all(isinstance(c.get(f), str) and c[f].strip() for f in ("title", "given", "when", "then")):
                    errs.append(f"acceptance_criteria[{k}] incomplet (title, given, when, then)")
        for f in ("non_functional", "out_of_scope", "split_proposal", "open_questions"):
            if not isinstance(out.get(f), list) or not all(isinstance(x, str) for x in out[f]):
                errs.append(f"{f} doit être une liste de chaînes")
        inv = out.get("invest")
        if not isinstance(inv, dict) or set(inv) != set(INVEST) or not all(isinstance(v, dict) and isinstance(v.get("ok"), bool) for v in inv.values()):
            errs.append(f"invest doit contenir {INVEST} avec ok booléen")
        errs += enum_error("estimate_points", out.get("estimate_points"), FIBONACCI)
        if not isinstance(out.get("estimate_rationale"), str) or not out["estimate_rationale"].strip():
            errs.append("estimate_rationale manquante")
        if out.get("estimate_points", 0) >= 8 and isinstance(out.get("split_proposal"), list) and not out["split_proposal"]:
            errs.append("split_proposal attendu pour une estimation ≥ 8")
        return errs
