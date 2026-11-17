"""PO Assist : l'interface du Product Owner.

    uv run streamlit run app.py

L'IA ne tourne pas ici : l'application exporte des lots de travail (packs), le skill Claude Code « po-agent »
les traite, l'application importe les résultats après vérification. Tout le reste (comptes, scores, plan) est calculé.
En mode démo (par défaut), le résultat d'un vrai passage du skill, calculé à l'avance, remplace l'attente du skill.
"""
from __future__ import annotations

import time
from pathlib import Path

import pandas as pd
import streamlit as st

from po_assist import actions, api_agent, config, demo, evaluate, handoff, insights, scoring, settings
from po_assist.linear import LinearClient
from po_assist.packs.analyse import THEMES
from po_assist.scoring import CRITERIA, DEFAULT_WEIGHTS, REACH_MODES
from po_assist.store import Store

st.set_page_config(page_title="PO Assist", page_icon="🧭", layout="wide")

TYPE_FR = {"bug": "Bug", "feature_request": "Demande", "improvement": "Amélioration", "question": "Question",
           "praise": "Éloge", "noise": "Bruit"}
CHANNEL_FR = {"support_ticket": "Ticket", "email": "E-mail", "feedback_chat": "Chat"}
SENT_FR = {"negative": "😟", "neutral": "😐", "positive": "🙂"}
MOSCOW_FR = {"must": "Must", "should": "Should", "could": "Could", "wont": "Won't"}
PACK_FR = {"analyse": "1 · Analyse des feedbacks", "priorisation": "2 · Priorisation", "redaction": "3 · Rédaction des stories"}


def clients() -> tuple[LinearClient, Store]:
    return LinearClient(), Store()


def eur(x) -> str:
    return f"{int(x or 0):,} €".replace(",", " ")


# ------------------------------------------------------------------ barre latérale
linear, store = clients()
meta = linear.meta()
cyc = linear.current_cycle() or {}
st.sidebar.title("🧭 PO Assist")
st.sidebar.caption(f"saxobeat · Linear (simulé) · {meta.get('reference_date')} · {cyc.get('name', '')}")
PAGES = ["🤖 Agent", "🏠 Tableau de bord", "📥 Feedbacks", "🧩 Demandes", "⚖️ Priorisation", "✍️ User stories",
         "🎯 Qualité de l'agent", "⚙️ Réglages", "❓ Guide"]
cfg = settings.load()
DEMO = cfg["demo_mode"]
ENGINE = "demo" if DEMO else cfg["engine"]  # le mode démo prime : aucun appel d'API tant qu'il est activé
MODEL = cfg["api_model"]
page = st.sidebar.radio("Navigation", PAGES, index=1 if store.results("feedback_analysis") else 0, label_visibility="collapsed")
stt = handoff.status(linear=linear, store=store)
st.sidebar.divider()
for name, s in stt["packs"].items():
    st.sidebar.caption(f"{PACK_FR[name]} : {s['done']} faits · {s['exported']} chez l'agent · {s['to_do']} à exporter")
if st.sidebar.button("Réinitialiser (état initial)", width="stretch",
                     help="Repart d'un espace Linear neuf, sans aucun résultat importé. Les réglages sont conservés."):
    config.reset_workspace()
    st.session_state.pop("last_results", None)
    st.rerun()
ENGINE_FR = {"demo": "mode démo : résultats d'un vrai passage du skill, calculés à l'avance",
             "skill": "agent : skill Claude Code (échange de fichiers)",
             "api": f"agent : API Claude ({api_agent.MODELS.get(MODEL, MODEL)})"}
st.sidebar.caption("Données fictives · " + ENGINE_FR[ENGINE])
if DEMO:
    st.info("**Mode démo.** Chaque fois que vous lancez l'agent, il reçoit le résultat d'un **vrai passage du skill "
            "po-agent, calculé à l'avance**, au lieu d'attendre plusieurs minutes. Vérification et import restent réels. "
            "Désactivable dans ⚙️ Réglages.", icon="🎬")


def launch_label(name: str, subjects: list[str] | None = None) -> str:
    if ENGINE == "demo":
        return "Lancer l'agent"
    if ENGINE == "api":
        est = api_agent.estimate(name, linear=linear, store=store, subjects=subjects, model=MODEL)
        return f"Lancer l'agent (API, ≈ {est['usd']:.2f} $)".replace(".", ",")
    return "Exporter"


def launch(name: str, subjects: list[str] | None = None) -> None:
    """Lance l'agent sur un pack : démo (résultat pré-calculé), API (appel réel) ou skill (export à traiter)."""
    if ENGINE == "api":
        bar = st.progress(0.0, text=f"Envoi à l'API ({MODEL})…")
        try:
            run = api_agent.run(name, subjects=subjects, model=MODEL, linear=linear, store=store,
                                on_progress=lambda k, n: bar.progress(k / n, text=f"API : paquet {k}/{n} traité"))
        except api_agent.ApiAgentError as e:
            st.error(str(e))
            return
        if run is None:
            st.warning("Rien à traiter : tout est déjà fait ou déjà chez l'agent.")
            return
        st.session_state["last_results"] = run["results"].name
        u = run["usage"]
        st.success(f"Résultats prêts : `{run['results'].name}` ({run['batches']} requête(s)). Coût réel : "
                   f"**{str(round(run['usd'], 2)).replace('.', ',')} $** ({u['input_tokens'] + u['cache_creation_input_tokens'] + u['cache_read_input_tokens']} "
                   f"jetons d'entrée dont {u['cache_read_input_tokens']} lus en cache, {u['output_tokens']} de sortie). "
                   "Vérifiez-les et importez-les dans 🤖 Agent.")
        for prob in run["problems"]:
            st.warning(prob)
        return
    if DEMO:
        run = demo.run(name, subjects=subjects, linear=linear, store=store)
        if run is None:
            st.warning("Rien à traiter : tout est déjà fait ou déjà chez l'agent.")
            return
        bar = st.progress(0.0, text=f"Le skill po-agent traite {run['tasks']} tâche(s)…")
        steps = 20
        for k in range(1, steps + 1):
            time.sleep(run["seconds"] / steps)
            bar.progress(k / steps, text=f"Le skill po-agent traite {run['tasks']} tâche(s)… "
                                         f"{round(run['tasks'] * k / steps)}/{run['tasks']}")
        st.session_state["last_results"] = run["results"].name
        msg = f"Résultats prêts : `{run['results'].name}`. Vérifiez-les et importez-les dans 🤖 Agent."
        if run["missing"]:
            msg += f" {len(run['missing'])} sujet(s) sans résultat pré-calculé : ils reviennent « ignorés »."
        st.success(msg)
    else:
        path = handoff.export(name, linear=linear, store=store, subjects=subjects)
        if path is None:
            st.warning("Rien à exporter : tout est déjà fait ou déjà chez l'agent.")
            return
        st.success(f"Pack écrit : `handoff/to-do/{path.name}`. Dans Claude Code, dites « traite les packs » "
                   "(skill po-agent), puis importez le résultat dans 🤖 Agent.")


def need_analysis() -> bool:
    if not store.results("feedback_analysis"):
        st.info("Aucune analyse importée. Étape 1 dans 🤖 Agent : lancer l'agent sur l'analyse des feedbacks, "
                "puis vérifier et importer le résultat.")
        return True
    return False


# ------------------------------------------------------------------ 🤖 Agent
def page_agent():
    st.header("🤖 Agent")
    if ENGINE == "api":
        st.markdown(f"**Lancez l'agent** : le pack est envoyé à l'**API Claude** ({MODEL}) par paquets, le coût estimé "
                    "est indiqué sur le bouton → l'application **vérifie puis importe** le résultat.")
    elif DEMO:
        st.markdown("**Lancez l'agent** sur une étape → le skill `po-agent` « travaille » (résultat réel, calculé à "
                    "l'avance) → l'application **vérifie puis importe** le résultat. Vous validez entre chaque étape.")
    else:
        st.markdown("L'application **exporte** un lot de travail → dans Claude Code, dites **« traite les packs »** "
                    "(skill `po-agent`) → l'application **vérifie puis importe** le résultat. Vous validez entre chaque étape.")
    cols = st.columns(3)
    for col, (name, s) in zip(cols, stt["packs"].items()):
        with col.container(border=True):
            st.subheader(PACK_FR[name])
            st.metric("Faits", s["done"], help="Résultats importés")
            st.caption(f"{s['exported']} en cours chez l'agent · {s['to_do']} à exporter")
            if name == "redaction":
                st.caption("Les stories se choisissent dans ⚖️ Priorisation.")
            elif name == "priorisation" and not store.results("feedback_analysis"):
                st.caption("Disponible après l'import de l'analyse des feedbacks.")
            elif st.button(launch_label(name) if s["to_do"] else ("Lancer l'agent" if ENGINE != "skill" else "Exporter"),
                           key=f"exp_{name}", disabled=s["to_do"] == 0,
                           width="stretch", type="primary" if s["to_do"] else "secondary"):
                launch(name)
    st.divider()
    st.subheader("Importer des résultats")
    todo = config.handoff_dir() / "to-do"
    files = sorted(todo.glob("*.results.json")) if todo.exists() else []
    up = st.file_uploader("…ou déposer un fichier de résultats (JSON, ou bloc collé depuis un chat)", type=["json", "txt", "md"])
    if up is not None:
        todo.mkdir(parents=True, exist_ok=True)
        target = todo / up.name
        target.write_bytes(up.getvalue())
        files = sorted(set(files) | {target})
    if not files:
        st.caption("Aucun fichier de résultats dans `handoff/to-do/`.")
        return
    last = st.session_state.get("last_results")
    default = next((k for k, p in enumerate(files) if p.name == last), len(files) - 1)
    f = st.selectbox("Fichier", files, index=default, format_func=lambda p: p.name)
    pv = handoff.check(f, linear=linear, store=store)
    if pv.fatal or pv.already_imported:
        st.warning(pv.summary())
        return
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Prêts", len(pv.accepted))
    c2.metric("Refusés", len(pv.refused))
    c3.metric("Ignorés par l'agent", len(pv.skipped))
    c4.metric("Sans résultat", len(pv.missing))
    if pv.refused:
        st.error("Refusés (rien ne sera écrit pour eux ; ils repartiront au prochain export) :")
        st.dataframe(pd.DataFrame([{"Tâche": r["task"], "Sujet": r["subject"], "Raisons": "; ".join(r["reasons"])}
                                   for r in pv.refused]), hide_index=True, width="stretch")
    strict = st.checkbox("Mode strict (un seul refus bloque tout le fichier)")
    if st.button(f"Importer {len(pv.accepted)} résultat(s)", type="primary", disabled=not pv.accepted):
        msg = handoff.apply(pv, store=store, strict=strict)
        handoff._file_away(pv)
        st.success(msg)
        st.rerun()


# ------------------------------------------------------------------ 🏠 Tableau de bord
def page_dashboard():
    st.header("🏠 Tableau de bord")
    if need_analysis():
        return
    data = insights.load(linear, store)
    dem = insights.demands(data)
    al = insights.alerts(data)
    ov = insights.overview(data)
    at_risk = {a["customer_id"]: a["arr_eur"] for a in al["churn"] if a["status"] != "churned" and a["segment"] == "b2b"}
    c = st.columns(5)
    c[0].metric("Feedbacks analysés", f"{ov['analysed']} / {ov['feedbacks']}")
    c[1].metric("Besoins distincts", len(dem), help="Issues du backlog ou besoins nouveaux, demandés au moins une fois")
    c[2].metric("Besoins nouveaux", sum(d["is_new"] for d in dem), help="Absents du backlog : à créer")
    c[3].metric("ARR Business à risque", eur(sum(at_risk.values())), help=f"{len(at_risk)} compte(s) Business ont signalé un risque de départ")
    c[4].metric("Bugs signalés", ov["types"].get("bug", 0))

    left, right = st.columns([3, 2])
    with left:
        st.subheader("Thèmes et tendances")
        th = insights.themes(data)
        st.dataframe(pd.DataFrame([{"Thème": f"{t['theme']} · {t['label']}", "Feedbacks": t["count"],
                                    "Négatifs": t["negative"], "Tendance": t["weekly"],
                                    "Évolution": f"{'↗' if t['trend'] > 0 else '↘' if t['trend'] < 0 else '→'} {t['trend']:+d}"}
                                   for t in th if t["count"]]),
                     column_config={"Tendance": st.column_config.LineChartColumn("Par semaine (fév. → avr.)")},
                     hide_index=True, width="stretch")
        st.subheader("Besoins les plus demandés")
        st.dataframe(pd.DataFrame([{"Besoin": d["target"], "Titre": d["title"], "État": d["state"], "Clients": d["customers"],
                                    "Business": d["b2b"], "4 dern. sem.": d["recent_4w"], "ARR à risque": eur(d["arr_at_risk_eur"])}
                                   for d in dem[:10]]), hide_index=True, width="stretch")
    with right:
        st.subheader("🚨 Risques de départ")
        for a in al["churn"]:
            st.markdown(f"**{a['customer']}** ({a['segment'].upper()} · {a['plan']}"
                        f"{' · ' + eur(a['arr_eur']) if a['segment'] == 'b2b' else ''}) · {a['date']} · `{a['feedback']}`  \n{a['summary']}")
        st.subheader("↩️ Déjà décidé : informer le client")
        for a in al["already_decided"]:
            st.markdown(f"`{a['feedback']}` → **{a['target']}** ({a['state']}) {a['title']}  \n{a.get('note') or ''}")
        st.subheader("❓ À clarifier avec le client")
        for a in al["follow_up"]:
            st.markdown(f"`{a['feedback']}` {a['customer']} : *{a['question']}*")


# ------------------------------------------------------------------ 📥 Feedbacks
def page_feedbacks():
    st.header("📥 Feedbacks (file Triage)")
    if need_analysis():
        return
    data = insights.load(linear, store)
    rows = []
    for ident, fb in sorted(data["feedbacks"].items()):
        a = data["analyses"].get(ident, {}).get("output")
        c = data["customers"].get(fb["customer_id"], {})
        rows.append({"Id": ident, "Date": fb["created_at"][:10], "Canal": CHANNEL_FR.get(fb["source_type"], fb["source_type"]),
                     "Client": f"{c.get('name')} ({c.get('segment', '').upper()} · {c.get('plan')})", "Titre": fb["title"],
                     "Type": TYPE_FR.get(a["type"], "") if a else "—", "Thèmes": ", ".join(a["themes"]) if a else "",
                     "Sentiment": SENT_FR.get(a["sentiment"], "") if a else "", "Churn": "⚠️" if a and a["churn_risk"] else "",
                     "Besoins": ", ".join(r["target"] for r in a["requests"]) if a else "", "État Linear": fb["state_name"]})
    df = pd.DataFrame(rows)
    f1, f2, f3, f4 = st.columns(4)
    canal = f1.multiselect("Canal", sorted(df["Canal"].unique()))
    typ = f2.multiselect("Type", [v for v in TYPE_FR.values() if v in set(df["Type"])])
    theme = f3.selectbox("Thème", ["(tous)"] + [f"{k} · {v}" for k, v in THEMES.items()])
    churn_only = f4.checkbox("Risque de départ uniquement")
    if canal:
        df = df[df["Canal"].isin(canal)]
    if typ:
        df = df[df["Type"].isin(typ)]
    if theme != "(tous)":
        df = df[df["Thèmes"].str.contains(theme.split(" ·")[0] + r"\b", regex=True)]
    if churn_only:
        df = df[df["Churn"] != ""]
    st.caption(f"{len(df)} feedback(s)")
    st.dataframe(df, hide_index=True, width="stretch", height=360)
    ident = st.selectbox("Détail", df["Id"].tolist())
    if not ident:
        return
    fb, a = data["feedbacks"][ident], data["analyses"].get(ident, {}).get("output")
    left, right = st.columns(2)
    with left.container(border=True):
        st.markdown(f"**{fb['title']}**")
        st.markdown(fb["description"])
    with right.container(border=True):
        if not a:
            st.caption("Pas encore analysé.")
            return
        st.markdown(f"**{TYPE_FR[a['type']]}** · {', '.join(f'{t} {THEMES[t]}' for t in a['themes'])} · {SENT_FR[a['sentiment']]}"
                    f"{' · ⚠️ risque de départ' if a['churn_risk'] else ''}")
        st.markdown(a["summary"])
        for k, r in enumerate(a["requests"]):
            b = data["backlog"].get(r["target"])
            st.markdown(f"- **{r['target']}** {('(' + b['state_name'] + ') ' + b['title']) if b else '(besoin nouveau)'}  \n"
                        f"  {r['summary']}  \n  > « {r['quote']} »" + (f"  \n  ↩️ {r['target_status_note']}" if r.get("target_status_note") else ""))
            if b and fb["state_type"] == "triage" and st.button(f"Rattacher dans Linear à {r['target']}", key=f"link_{ident}_{k}"):
                linear.link_feedback(ident, r["target"])
                st.success(f"{ident} rattaché à {r['target']} (demande client ajoutée, feedback marqué Duplicate).")
                st.rerun()
        if a.get("follow_up_question"):
            st.info(f"Question à poser : {a['follow_up_question']}")


# ------------------------------------------------------------------ 🧩 Demandes
def page_demands():
    st.header("🧩 Demandes : chaque besoin, avec ses preuves")
    if need_analysis():
        return
    data = insights.load(linear, store)
    dem = insights.demands(data)
    df = pd.DataFrame([{"Besoin": d["target"], "Titre": d["title"], "État": d["state"], "Feedbacks": d["mentions"],
                        "Demandes antérieures": d["historic_requests"], "Clients": d["customers"], "B2C": d["b2c"],
                        "Business": d["b2b"], "Personnes touchées": d["reach"], "ARR à risque": d["arr_at_risk_eur"],
                        "4 dern. sem.": d["recent_4w"]} for d in dem])
    only_new = st.toggle("Besoins nouveaux uniquement (absents du backlog)")
    if only_new:
        df = df[df["État"] == "À créer"]
    st.dataframe(df, hide_index=True, width="stretch", height=380,
                 column_config={"ARR à risque": st.column_config.NumberColumn(format="%d €")})
    tgt = st.selectbox("Preuves pour", df["Besoin"].tolist(), format_func=lambda t: f"{t} · {next(d['title'] for d in dem if d['target'] == t)}")
    d = next((d for d in dem if d["target"] == tgt), None)
    if d:
        for q in d["quotes"]:
            c = data["customers"].get(q["customer_id"], {})
            st.markdown(f"> « {q['quote']} »  \n> — {c.get('name')} ({c.get('segment', '').upper()} · {c.get('plan')}), `{q['feedback']}`")


# ------------------------------------------------------------------ ⚖️ Priorisation
def page_prioritization():
    st.header("⚖️ Priorisation")
    if need_analysis():
        return
    if not store.results("prioritization"):
        st.info("Aucune estimation importée. Étape 2 dans 🤖 Agent : exporter le pack « priorisation », le faire traiter, importer.")
        return
    c1, c2 = st.columns([1, 2])
    reach_mode = c1.radio("Reach compté en", list(REACH_MODES), format_func=lambda m: REACH_MODES[m])
    with c2.expander("Score pondéré : régler les poids (simulation « et si »)"):
        weights = {k: st.slider(CRITERIA[k], 0.0, 1.0, float(v), 0.05, key=f"w_{k}") for k, v in DEFAULT_WEIGHTS.items()}
    sort_by = c1.radio("Classer par", ["RICE", "Score pondéré"], horizontal=True)
    base = scoring.table(linear, store, reach_mode=reach_mode, weights=weights)
    st.caption("Reach : calculé. Impact, Confiance, Effort, MoSCoW : estimés par l'agent, **modifiables ici** "
               "(les scores et le plan se recalculent).")
    edit_df = pd.DataFrame([{"Besoin": r["target"], "Titre": r["title"], "Impact": r["impact"], "Confiance": r["confidence"],
                             "Effort": r["effort"], "MoSCoW": r["moscow"]} for r in base])
    edited = st.data_editor(edit_df, hide_index=True, width="stretch", key=f"ed_{reach_mode}",
                            disabled=["Besoin", "Titre"],
                            column_config={"Impact": st.column_config.SelectboxColumn(options=[3, 2, 1, 0.5, 0.25]),
                                           "Confiance": st.column_config.SelectboxColumn(options=[1.0, 0.8, 0.5]),
                                           "Effort": st.column_config.SelectboxColumn(options=[1, 2, 3, 5, 8, 13]),
                                           "MoSCoW": st.column_config.SelectboxColumn(options=["must", "should", "could", "wont"])})
    overrides = {}
    for (_, e), r in zip(edited.iterrows(), base):
        o = {k2: e[k1] for k1, k2 in [("Impact", "impact"), ("Confiance", "confidence"), ("Effort", "effort_points"), ("MoSCoW", "moscow")]
             if e[k1] != r[{"impact": "impact", "confidence": "confidence", "effort_points": "effort", "moscow": "moscow"}[k2]]}
        if o:
            overrides[r["target"]] = o
    rows = scoring.table(linear, store, reach_mode=reach_mode, weights=weights, overrides=overrides)
    key = "rice" if sort_by == "RICE" else "weighted"
    rows.sort(key=lambda r: -r[key])
    st.subheader("Classement")
    st.dataframe(pd.DataFrame([{"#": k, "Besoin": r["target"], "Titre": r["title"], "État": r["state"], "Reach": r["reach"],
                                "Impact": r["impact"], "Conf.": r["confidence"], "Effort": r["effort"], "RICE": r["rice"],
                                "Pondéré": r["weighted"], "MoSCoW": MOSCOW_FR[r["moscow"]], "OKR": r["okr"] or "",
                                "Modifié": "✏️" if r["overridden"] else "", "Justification": r["rationale"]}
                               for k, r in enumerate(rows, 1)]), hide_index=True, width="stretch", height=420)
    plan = scoring.cycle_proposal(rows, linear, key=key)
    st.subheader(f"Proposition pour le {plan['cycle']['name'] if plan['cycle'] else 'cycle en cours'}")
    p1, p2, p3 = st.columns(3)
    p1.metric("Capacité", f"{plan['capacity']} pts")
    p2.metric("Reste à faire sur les issues en cours", f"{plan['capacity'] - plan['capacity_left']:.0f} pts")
    p3.metric("Engagé par la proposition", f"{plan['points_picked']} / {plan['capacity_left']:.0f} pts")
    st.markdown("**À prendre :** " + " · ".join(f"`{r['target']}` {r['title']} ({MOSCOW_FR[r['moscow']]}, {r['effort']} pts)" for r in plan["picked"]))
    if plan["dropped_from_plan"]:
        st.warning("Déjà planifiés en Todo dans ce cycle mais non retenus à cette capacité : " + ", ".join(plan["dropped_from_plan"]))
    st.divider()
    st.subheader("Rédiger les user stories")
    default = [r["target"] for r in rows if r["moscow"] in ("must", "should")][:5]
    chosen = st.multiselect("Besoins à formaliser", [r["target"] for r in rows], default=default,
                            format_func=lambda t: f"{t} · {next(r['title'] for r in rows if r['target'] == t)}")
    label = {"demo": "Lancer la rédaction (agent)", "skill": "Exporter le pack « rédaction »"}.get(ENGINE)
    if ENGINE == "api":
        label = launch_label("redaction", chosen).replace("Lancer l'agent", "Lancer la rédaction") if chosen else "Lancer la rédaction"
    if st.button(label, type="primary", disabled=not chosen):
        launch("redaction", chosen)


# ------------------------------------------------------------------ ✍️ User stories
def page_stories():
    st.header("✍️ User stories")
    stories = store.results("user_story")
    if not stories:
        st.info("Aucune story importée. Choisissez les besoins dans ⚖️ Priorisation, exportez le pack « rédaction », "
                "faites-le traiter, importez-le dans 🤖 Agent.")
        return
    prio = {r["target"]: r for r in scoring.table(linear, store)} if store.results("prioritization") else {}
    pushed = {}
    try:
        pushed = {r[0]: r[1] for r in store.conn.execute("SELECT target, issue FROM pushes")}
    except Exception:
        pass
    d1, d2 = st.columns(2)
    d1.download_button("Télécharger (Markdown)", actions.stories_markdown(store, list(prio.values())), "user_stories.md")
    d2.download_button("Télécharger (CSV pour import Linear)", actions.stories_csv(store, list(prio.values())), "user_stories.csv")
    for target, res in stories.items():
        s = res["output"]
        with st.expander(f"{s['title']} · {target} · {s['estimate_points']} pts", expanded=len(stories) <= 2):
            st.markdown(actions.story_markdown(target, s, prio.get(target)))
            if target in pushed:
                st.success(f"Dans Linear : {pushed[target]}")
            elif st.button("Envoyer vers Linear", key=f"push_{target}", type="primary"):
                ident = actions.push_story(target, linear=linear, store=store, prio=prio.get(target))
                st.success(f"{'Issue créée' if target.startswith('NEW:') else 'Story ajoutée en commentaire'} : {ident}. "
                           "Les feedbacks sources y sont rattachés.")
                st.rerun()


# ------------------------------------------------------------------ 🎯 Qualité
def page_quality():
    st.header("🎯 Qualité de l'agent")
    st.markdown("Les analyses importées sont comparées à la **vérité terrain** du jeu de données (`data/ground_truth.json`), "
                "que l'agent ne voit jamais. C'est ainsi qu'on sait si l'on peut lui faire confiance, et où il se trompe.")
    m = evaluate.evaluate(store)
    st.markdown(evaluate.report_markdown(m))


# ------------------------------------------------------------------ ⚙️ Réglages
def page_settings():
    st.header("⚙️ Réglages")
    st.subheader("Mode démo")
    on = st.toggle("Activer le mode démo", value=DEMO,
                   help="L'agent reçoit le résultat d'un vrai passage du skill, calculé à l'avance, au lieu d'attendre.")
    if on != DEMO:
        settings.save(demo_mode=on)
        st.rerun()
    st.subheader("Moteur de l'agent")
    engines = {"skill": "Skill Claude Code (local, échange de fichiers)", "api": "API Claude"}
    eng = st.radio("Quand le mode démo est désactivé, l'agent passe par :", list(engines), format_func=engines.get,
                   index=list(engines).index(cfg["engine"]), disabled=DEMO)
    model = st.selectbox("Modèle (mode API)", list(api_agent.MODELS), format_func=api_agent.MODELS.get,
                         index=list(api_agent.MODELS).index(MODEL) if MODEL in api_agent.MODELS else 0, disabled=DEMO)
    if (eng, model) != (cfg["engine"], MODEL):
        settings.save(engine=eng, api_model=model)
        st.rerun()
    if DEMO:
        st.caption("Le mode démo est activé : il prime, et aucun appel d'API n'est fait.")
    key = api_agent.has_credentials()
    st.markdown(f"Clé API : **{'détectée' if key else 'absente'}** (jamais affichée ni enregistrée par l'application)."
                + ("" if key else " Pour le mode API : définir `ANTHROPIC_API_KEY`, par exemple dans un fichier `.env` à la "
                                  "racine du dépôt (ignoré par git, chargé par le lanceur Mac), ou `ant auth login`."))
    pin, pout = api_agent.PRICES[MODEL] if MODEL in api_agent.PRICES else api_agent.PRICES["claude-opus-5-5"]
    st.caption(f"Tarif {MODEL} : {pin} $ / {pout} $ par million de jetons (entrée / sortie) ; instructions et contexte "
               "mis en cache entre les paquets. Coût estimé affiché sur le bouton avant chaque lancement.")
    st.divider()
    st.subheader("Résultats pré-calculés (mode démo)")
    cov = demo.coverage()
    st.caption(f"Résultats pré-calculés disponibles : {cov.get('feedback_analysis', 0)} analyses, "
               f"{cov.get('prioritization', 0)} estimations, {cov.get('user_story', 0)} user stories "
               f"(`handoff/demo/`, vrais passages du skill po-agent).")


# ------------------------------------------------------------------ ❓ Guide
GUIDE = config.ROOT / "docs" / "guide-utilisateur.md"


def page_guide():
    """Affiche docs/guide-utilisateur.md (une seule source pour le dépôt et l'application), images comprises."""
    import re
    if not GUIDE.exists():
        st.warning("Guide introuvable : docs/guide-utilisateur.md")
        return
    chunk = []
    for line in GUIDE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^!\[(.*?)\]\((.+?)\)\s*$", line.strip())
        if m:
            if chunk:
                st.markdown("\n".join(chunk))
                chunk = []
            img = (GUIDE.parent / m.group(2)).resolve()
            if img.exists():
                st.image(str(img), caption=m.group(1))
        else:
            chunk.append(line)
    if chunk:
        st.markdown("\n".join(chunk))


{"🤖 Agent": page_agent, "🏠 Tableau de bord": page_dashboard, "📥 Feedbacks": page_feedbacks, "🧩 Demandes": page_demands,
 "⚖️ Priorisation": page_prioritization, "✍️ User stories": page_stories, "🎯 Qualité de l'agent": page_quality,
 "⚙️ Réglages": page_settings, "❓ Guide": page_guide}[page]()
