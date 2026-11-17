"""Ligne de commande : uv run python -m po_assist <status|export|import> ..."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import handoff


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="po_assist", description="PO Assist : agent IA au service du PO (échange de fichiers).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="ce qui attend dans Linear et dans les packs")
    ex = sub.add_parser("export", help="écrire un pack dans handoff/to-do/")
    ex.add_argument("pack")
    ex.add_argument("--limit", type=int)
    ex.add_argument("--subjects", nargs="*")
    rn = sub.add_parser("run", help="lancer l'agent : exporter, traiter (démo ou API), écrire les résultats")
    rn.add_argument("pack")
    rn.add_argument("--engine", choices=["demo", "api"], required=True)
    rn.add_argument("--model", default="claude-opus-5-5")
    rn.add_argument("--limit", type=int)
    rn.add_argument("--subjects", nargs="*")
    im = sub.add_parser("import", help="vérifier puis importer un ou plusieurs fichiers de résultats")
    im.add_argument("files", nargs="*", type=Path, help="par défaut : tous les *.results.json de handoff/to-do/")
    im.add_argument("--dry-run", action="store_true")
    im.add_argument("--strict", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "status":
        print(json.dumps(handoff.status(), ensure_ascii=False, indent=2))
    elif a.cmd == "export":
        path = handoff.export(a.pack, limit=a.limit, subjects=a.subjects)
        print(f"Pack écrit : {path}" if path else "Rien à exporter.")
    elif a.cmd == "run":
        if a.engine == "demo":
            from . import demo
            r = demo.run(a.pack, subjects=a.subjects)
        else:
            from . import api_agent
            print(f"Estimation : {api_agent.estimate(a.pack, subjects=a.subjects, model=a.model)}")
            r = api_agent.run(a.pack, subjects=a.subjects, model=a.model, limit=a.limit,
                              on_progress=lambda k, n: print(f"  paquet {k}/{n}"))
        if r is None:
            print("Rien à traiter.")
        else:
            extra = f" · coût {r['usd']} $ · {r['usage']}" if "usd" in r else ""
            print(f"Résultats écrits : {r['results']}{extra}")
            print("Vérifier et importer : uv run python -m po_assist import")
    elif a.cmd == "import":
        from . import config
        files = a.files or sorted((config.handoff_dir() / "to-do").glob("*.results.json"))
        if not files:
            print("Aucun fichier de résultats.")
        for f in files:
            pv, msg = handoff.import_file(f, dry_run=a.dry_run, strict=a.strict)
            print(f"{f.name} — {msg}")
            for r in pv.refused:
                print(f"  refusé {r['task']} {r['subject']} : {'; '.join(r['reasons'])}")
            for s in pv.skipped:
                print(f"  ignoré {s['task']} {s['subject']} : {s['reason']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
