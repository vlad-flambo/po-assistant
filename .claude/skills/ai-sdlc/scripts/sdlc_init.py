"""Set up, and grow, docs/sdlc in any repository. Standard library only.

    <python> sdlc_init.py init [--project NAME]          create docs/sdlc (README, PROJECT, templates, cycles/); never overwrites
    <python> sdlc_init.py new "short name" [--importance N --reason "..." --owner NAME]
                                                         create the next cycle folder (intent.md, next.md) and its row in README.md
    <python> sdlc_init.py board-page --project NAME --out page.json
                                                         the live board's page as {"text": ...} JSON, ready for the dashboard store

Run from anywhere inside the repository: the repository root is the nearest parent holding .git (or the current folder).
<python> is whatever runs Python in the project (python, python3, uv run python).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL / "templates"
BOARD_DATA = "docs/sdlc/board-data/"


def repo_root(start: Path) -> Path:
    for base in [start, *start.resolve().parents]:
        if (base / ".git").exists() or (base / "docs" / "sdlc").is_dir():
            return base
    return start


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:40] or "cycle"


def write_new(path: Path, text: str) -> bool:
    if path.exists():
        print(f"kept    {path} (already there)")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"created {path}")
    return True


def init(root: Path, project: str) -> None:
    sdlc = root / "docs" / "sdlc"
    for t in sorted(TEMPLATES.glob("[a-z]*.md")):
        write_new(sdlc / "templates" / t.name, t.read_text(encoding="utf-8"))
    write_new(sdlc / "README.md", (TEMPLATES / "_README.md").read_text(encoding="utf-8"))
    write_new(sdlc / "PROJECT.md", (TEMPLATES / "_PROJECT.md").read_text(encoding="utf-8").replace("<project name>", project))
    (sdlc / "cycles").mkdir(parents=True, exist_ok=True)
    keep = sdlc / "cycles" / ".gitkeep"
    if not any((sdlc / "cycles").iterdir()):
        keep.write_text("", encoding="utf-8")
    gitignore = root / ".gitignore"
    lines = gitignore.read_text(encoding="utf-8").splitlines() if gitignore.exists() else []
    if BOARD_DATA.rstrip("/") not in [ln.strip().rstrip("/") for ln in lines]:
        gitignore.write_text("\n".join(lines + ["", "# ai-sdlc: the live board's data files (regenerated from docs/sdlc)", BOARD_DATA]) + "\n", encoding="utf-8")
        print(f"updated {gitignore} (ignores {BOARD_DATA})")
    print("\nNext: fill docs/sdlc/PROJECT.md, then start the first cycle with the `new` command.")


def new_cycle(root: Path, name: str, importance: int | None, reason: str, owner: str) -> None:
    sdlc = root / "docs" / "sdlc"
    if not (sdlc / "templates" / "intent.md").exists():
        sys.exit("docs/sdlc is not set up here: run the `init` command first.")
    numbers = [int(m.group(1)) for f in (sdlc / "cycles").glob("[0-9]*-*") if (m := re.match(r"(\d+)-", f.name))]
    nnn = f"{max(numbers, default=0) + 1:03d}"
    folder = sdlc / "cycles" / f"{nnn}-{slug(name)}"
    today = date.today().isoformat()
    intent = (sdlc / "templates" / "intent.md").read_text(encoding="utf-8")
    intent = intent.replace("# Intent: <short name>", f"# Intent: {name}").replace("| **Cycle** | NNN |", f"| **Cycle** | {nnn} |").replace("YYYY-MM-DD |", f"{today} |", 1)
    intent = intent.replace("| **Owner** | |", f"| **Owner** | {owner} |")
    if importance:
        imp = f"{importance}/5 (claude, {today}): {reason or 'no evidence yet'}"
        intent = re.sub(r"\| \*\*Importance\*\* \|.*\|", lambda _: f"| **Importance** | {imp} |", intent, count=1)
    nxt = (sdlc / "templates" / "next.md").read_text(encoding="utf-8").replace("# Next: <cycle name>", f"# Next: {name}")
    nxt = re.sub(r"- \[ \] \[owner\] YYYY-MM-DD ?\n", "- [ ] [owner] Say your request in your own words (it goes in intent.md, unedited)\n", nxt)
    nxt = re.sub(r"- \[ \] \[claude\] *\n?", "- [ ] [claude] Gather the facts (code, docs, files), draft the open questions in intent.md and grill the owner one at a time\n", nxt)
    write_new(folder / "intent.md", intent)
    write_new(folder / "next.md", nxt)
    readme = sdlc / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        row = f"| {nnn} | {importance or ''} | {name} | Intent: started {today} |"
        readme.write_text(text.rstrip("\n") + "\n" + row + "\n", encoding="utf-8")
        print(f"added   row {nnn} to {readme}")
    print(f"\nCycle {nnn} ready: {folder}. Next: grill the owner, fill intent.md, then refresh the board.")


def board_page(project: str, out: Path) -> None:
    html = (SKILL / "board" / "index.html").read_text(encoding="utf-8").replace("__PROJECT__", project)
    out.write_text(json.dumps({"text": html}, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out} ({len(html)} characters; the store refuses a file over 256 KB).")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_init = sub.add_parser("init", help="create docs/sdlc in this repository")
    p_init.add_argument("--project", help="project name for PROJECT.md (default: the repository folder's name)")
    p_new = sub.add_parser("new", help="create the next cycle")
    p_new.add_argument("name", help="short name, e.g. 'Faster search'")
    p_new.add_argument("--importance", type=int, choices=range(1, 6), help="1 to 5, as assessed by the agent")
    p_new.add_argument("--reason", default="", help="one line of evidence for the importance")
    p_new.add_argument("--owner", default="", help="who decides at the gates")
    p_page = sub.add_parser("board-page", help="the live board's page as JSON for the dashboard store")
    p_page.add_argument("--project", default="", help="project name shown in the title")
    p_page.add_argument("--out", required=True, help="file to write")
    args = parser.parse_args()
    root = repo_root(Path.cwd())
    if args.cmd == "board-page":
        board_page(args.project or root.resolve().name, Path(args.out))
    elif args.cmd == "init":
        init(root, args.project or root.resolve().name)
    else:
        new_cycle(root, args.name, args.importance, args.reason, args.owner)
    return 0


if __name__ == "__main__":
    sys.exit(main())
