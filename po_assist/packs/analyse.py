"""Pack « analyse » (bloc A, COMPRENDRE) : une tâche par feedback en Triage."""
from __future__ import annotations

from .base import NEW_TARGET, enum_error, normalize

TYPES = ["bug", "feature_request", "improvement", "question", "praise", "noise"]
SENTIMENTS = ["negative", "neutral", "positive"]

# Catalogue de thèmes du produit, tenu par le PO (pas dérivé de la vérité terrain : c'est la taxonomie de l'équipe).
THEMES = {
    "T1": "Pertinence et explication du score",
    "T2": "Couverture des sources (employeurs, agrégateurs, alertes)",
    "T3": "Irritants d'interface, fonctions difficiles à trouver",
    "T4": "Mode standard en retard sur le mode power",
    "T5": "Suivi des candidatures (relances, republications, agenda, trajets)",
    "T6": "Mobile (téléphone, gestes, mise en page)",
    "T7": "Fiabilité et performance (bugs, lenteurs, doublons, e-mails non reçus)",
    "T8": "Notifications et e-mails (rappels, résumés, préférences)",
    "T9": "Délai et transparence de l'analyse IA",
    "T10": "Besoins Business (cabinets d'outplacement, écoles, coachs : console, invitations, reporting)",
    "T11": "Conversion Free → Plus, compréhension de l'offre",
    "T12": "Facturation et compte",
}

INSTRUCTIONS = """\
Pack « analyse » : pour chaque feedback (ticket de support, e-mail ou message du feedback chat), produis une analyse
structurée qui aide le PO à comprendre ce que veulent les clients et à le relier au backlog.

Pour chaque tâche :
1. type : bug (le produit ne fait pas ce qu'il est censé faire), feature_request (une capacité nouvelle),
   improvement (changer une capacité existante), question (le client demande comment ou pourquoi, y compris quand il
   prend une limite de son offre pour un bug), praise (éloge sans demande), noise (hors sujet : réponse automatique,
   désabonnement, spam). Classe selon la réalité décrite, pas selon les mots du client : « pouvez-vous ajouter X » pour
   une fonction qui existe mais plante est un bug ; « bug : je ne vois que 20 offres » sur l'offre Free est une question.
2. themes : 1 à 3 thèmes du catalogue (context.themes), du plus au moins important. Liste vide pour praise et noise
   si aucun thème ne s'applique.
3. sentiment : negative, neutral ou positive.
4. churn_risk : true si le client annonce ou laisse clairement entendre qu'il pourrait partir, résilier ou ne pas
   renouveler. Regarde aussi context et l'entrée customer (statut, ARR) pour juger de la gravité dans "summary".
5. summary : une phrase en français, du point de vue du PO (« Le client … »).
6. requests : une entrée par besoin distinct exprimé (un e-mail peut en contenir plusieurs ; un éloge ou un message
   vague n'en contient aucun). Pour chacune :
   - summary : le besoin en une phrase, formulé comme un besoin utilisateur, en français ;
   - target : l'identifiant de l'issue du backlog (context.backlog) qui couvre ce besoin, même si elle est Done ou
     Canceled ; sinon "NEW:<slug>" (kebab-case, sans accents) pour proposer une nouvelle issue. Réutilise exactement le
     même slug pour le même besoin d'un feedback à l'autre : c'est ainsi que l'application compte les demandes ;
   - target_status_note : si la cible est Done ou Canceled, une phrase pour le PO (déjà livré : informer le client ;
     refusé : rappeler la décision) ; sinon null ;
   - quote : un extrait copié mot pour mot du texte du feedback (5 à 25 mots) qui justifie la demande.
7. follow_up_question : si le feedback est trop vague pour en tirer une demande, la question à poser au client ;
   sinon null.
"""

OUTPUT_FORMAT = {
    "description": "Un objet par tâche, dans le champ output du fichier de résultats.",
    "fields": {
        "type": f"une valeur parmi {TYPES}",
        "themes": "liste de 0 à 3 identifiants de context.themes (ex. [\"T1\", \"T6\"])",
        "sentiment": f"une valeur parmi {SENTIMENTS}",
        "churn_risk": "booléen",
        "summary": "chaîne, une phrase",
        "requests": "liste d'objets {summary, target, target_status_note, quote}",
        "follow_up_question": "chaîne ou null",
    },
    "example": {
        "type": "feature_request",
        "themes": ["T2"],
        "sentiment": "negative",
        "churn_risk": False,
        "summary": "La cliente recopie chaque matin ses alertes LinkedIn à la main et voudrait les retrouver dans l'Inbox.",
        "requests": [{
            "summary": "Importer automatiquement les offres des alertes LinkedIn dans l'Inbox",
            "target": "SAX-110",
            "target_status_note": None,
            "quote": "je recopie tout a la main chaque matin",
        }],
        "follow_up_question": None,
    },
}


class AnalysePack:
    name = "analyse"
    kind = "feedback_analysis"
    version = 1
    instructions = INSTRUCTIONS
    output_format = OUTPUT_FORMAT

    @staticmethod
    def _customer(c: dict | None) -> dict | None:
        if not c:
            return None
        out = {"id": c["id"], "segment": c["segment"], "plan": c["plan"], "status": c["status"]}
        if c["segment"] == "b2b":
            out |= {"arr_eur": c["revenue_eur"], "seats": c["size"]}
        return out

    def items(self, linear, store) -> list[dict]:
        done = store.subjects_done(self.kind)
        customers = linear.customers()
        items = []
        for i in linear.triage_issues():
            if i["identifier"] in done:
                continue
            md = i["source_metadata"]
            details = {k: md[k] for k in ("path", "page", "device", "mode", "subject", "via") if md.get(k)}
            items.append({"subject": i["identifier"], "input": {
                "identifier": i["identifier"],
                "channel": i["source_type"],
                "received_at": i["created_at"],
                "language": md.get("language"),
                "customer": self._customer(customers.get(i["customer_id"])),
                "title": i["title"],
                "text": i["description"],
                "details": details,
            }})
        return items

    def context(self, linear, store) -> dict:
        meta = linear.meta()
        needs = {}
        for n in linear.customer_needs():
            needs[n["issue_identifier"]] = needs.get(n["issue_identifier"], 0) + 1
        return {
            "product": meta.get("product"),
            "plans": meta.get("plans"),
            "reference_date": meta.get("reference_date"),
            "themes": THEMES,
            "backlog": [{
                "identifier": b["identifier"], "title": b["title"], "state": b["state_name"],
                "project": b["project_name"], "labels": b["labels"],
                "description": b["description"][:400], "customer_requests": needs.get(b["identifier"], 0),
            } for b in linear.backlog_issues()],
        }

    def validation_context(self, linear, store) -> dict:
        return {"backlog": {b["identifier"] for b in linear.backlog_issues()},
                "texts": {i["identifier"]: normalize(i["title"] + "\n" + i["description"]) for i in linear.triage_issues()}}

    def validate(self, out: dict, subject: str, ctx: dict) -> list[str]:
        errs = []
        errs += enum_error("type", out.get("type"), TYPES)
        errs += enum_error("sentiment", out.get("sentiment"), SENTIMENTS)
        if not isinstance(out.get("churn_risk"), bool):
            errs.append("churn_risk doit être un booléen")
        themes = out.get("themes")
        if not isinstance(themes, list) or len(themes) > 3 or any(t not in THEMES for t in themes):
            errs.append(f"themes invalide : {themes!r} (0 à 3 identifiants du catalogue)")
        if not isinstance(out.get("summary"), str) or not out["summary"].strip():
            errs.append("summary manquant")
        fq = out.get("follow_up_question")
        if fq is not None and not isinstance(fq, str):
            errs.append("follow_up_question doit être une chaîne ou null")
        reqs = out.get("requests")
        if not isinstance(reqs, list):
            return errs + ["requests doit être une liste"]
        text = ctx["texts"].get(subject)
        if text is None:
            errs.append("feedback introuvable ou déjà sorti de Triage")
        for k, r in enumerate(reqs, 1):
            if not isinstance(r, dict):
                errs.append(f"requests[{k}] n'est pas un objet")
                continue
            if not isinstance(r.get("summary"), str) or not r["summary"].strip():
                errs.append(f"requests[{k}].summary manquant")
            tgt = r.get("target")
            if not (tgt in ctx["backlog"] or (isinstance(tgt, str) and NEW_TARGET.match(tgt))):
                errs.append(f"requests[{k}].target inconnu : {tgt!r} (issue du backlog ou NEW:<slug>)")
            q = r.get("quote")
            if not isinstance(q, str) or len(normalize(q)) < 5:
                errs.append(f"requests[{k}].quote manquante")
            elif text is not None and normalize(q) not in text:
                errs.append(f"requests[{k}].quote absente du feedback : {q[:60]!r}")
        return errs
