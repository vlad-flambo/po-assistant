"""Mode démo (cycles 009 et 012) : le flux de l'intégration API, simulé.

Le parcours est celui du mode API : export du pack, paquets traités l'un après l'autre (progression), coût estimé,
fichier de résultats, puis vérification et import réels. Aucun appel n'est fait et rien n'est facturé : les sorties
sont celles d'un vrai passage de l'agent (skill po-agent), calculées à l'avance et tenues cachées jusqu'au lancement.
Un sujet absent du cache revient « ignoré » : rien n'est jamais inventé.
"""
from __future__ import annotations

import json
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path

from . import api_agent, config, handoff
from .packs import PACKS
from .linear import LinearClient
from .store import Store

AGENT = "api simulée / {model} (mode démo) : résultats d'un vrai passage de l'agent po-agent, calculés à l'avance"


@lru_cache(maxsize=4)
def _cache(demo_dir: str) -> dict[tuple[str, str], dict]:
    out = {}
    for rf in sorted(Path(demo_dir).glob("*.results.json")):
        pf = rf.with_name(rf.name.replace(".results.json", ".pack.json"))
        if not pf.exists():
            continue
        subject_of = {t["task"]: t["subject"] for t in json.loads(pf.read_text(encoding="utf-8"))["tasks"]}
        doc = json.loads(rf.read_text(encoding="utf-8"))
        for r in doc["results"]:
            if "output" in r and r["task"] in subject_of:
                out[(r["kind"], subject_of[r["task"]])] = {"output": r["output"], "agent": doc.get("agent"), "file": rf.name}
    return out


def cache() -> dict[tuple[str, str], dict]:
    return _cache(str(config.demo_dir()))


def coverage() -> dict[str, int]:
    return dict(Counter(kind for kind, _ in cache()))


def simulated_seconds(task_count: int) -> float:
    """Durée affichée de la « progression » : environ 0,1 s par tâche, entre 3 et 10 s."""
    return max(3.0, min(10.0, 0.1 * task_count))


def run(pack_name: str, *, subjects: list[str] | None = None, linear: LinearClient | None = None,
        store: Store | None = None, model: str = "claude-opus-5-5", pace: float = 0.0,
        on_progress=None) -> dict | None:
    """Simule le mode API : export, paquets traités un à un (`pace` secondes au total), coût estimé, résultats."""
    linear, store = linear or LinearClient(), store or Store()
    est = api_agent.estimate(pack_name, linear=linear, store=store, subjects=subjects, model=model)
    pack_path = handoff.export(pack_name, linear=linear, store=store, subjects=subjects)
    if pack_path is None:
        return None
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    c = cache()
    groups = api_agent.batches(pack["tasks"], PACKS[pack_name].batch_size)
    results, missing = [], []
    for k, group in enumerate(groups, 1):
        for t in group:
            hit = c.get((t["kind"], t["subject"]))
            if hit:
                results.append({"task": t["task"], "kind": t["kind"], "output": hit["output"]})
            else:
                missing.append(t["subject"])
                results.append({"task": t["task"], "kind": t["kind"],
                                "skipped": "pas de résultat pré-calculé pour ce sujet (mode démo)"})
        if pace:
            time.sleep(pace / len(groups))
        if on_progress:
            on_progress(k, len(groups))
    results_path = pack_path.with_name(pack["results_file"])
    results_path.write_text(json.dumps({"schema": handoff.RESULTS_SCHEMA, "export_id": pack["export_id"],
                                        "pack": pack_name, "agent": AGENT.format(model=model), "results": results},
                                       ensure_ascii=False, indent=2), encoding="utf-8")
    return {"pack": pack_path, "results": results_path, "tasks": len(results), "missing": missing,
            "batches": len(groups), "seconds": simulated_seconds(len(results)), "usd": est["usd"],
            "simulated": True, "model": model, "problems": []}
