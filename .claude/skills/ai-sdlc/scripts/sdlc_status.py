"""Where is each cycle? Reads docs/sdlc/cycles/* and prints one JSON document (stages, open gates, criteria, next actions).

    <python> sdlc_status.py [--root docs/sdlc] [--out status.json]
    <python> sdlc_status.py --markdown docs/sdlc/BOARD.md       (the board as a table, readable anywhere)
    <python> sdlc_status.py --datasets docs/sdlc/board-data     (the two files the live cycle board shows)

<python> is whatever runs Python in the project (python, python3, uv run python; see docs/sdlc/PROJECT.md).
Run it from anywhere inside the repository: the sdlc folder is found by walking up from the current folder.

Nothing is stored: the state is derived from the files each stage leaves behind (see SKILL.md), so it cannot drift from them.
The one thing that cannot be derived is "what next?": each cycle keeps it in next.md, one line per action:

    - [ ] [owner] 2026-10-30 Read the sum of all projects in Neon and tell me
    - [ ] [claude] Record criterion 9 and commit
    - [x] [owner] An action that is done

`[owner]`, `[claude]` or `[both]`; the date is optional.

Two more things are read from the header table of each intent.md (they are judgments, so they are typed, not derived):

    | **Status** | Dismissed 2026-10-30 by the owner: <reason> |      a dismissed cycle leaves the "what next?" list and shows as Dismissed
    | **Importance** | 4/5 (claude, 2026-10-30): <reason> |          1 to 5, the first digit counts; the owner can overwrite it ("owner")

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

STAGES = [
    ("intent", "Intent"),
    ("spec", "Spec"),
    ("plan", "Plan"),
    ("build", "Build"),
    ("verify", "Verify"),
    ("learn", "Learn"),
]
HEADER_ROW = re.compile(r"^\|\s*\*\*(Status|Importance)\*\*\s*\|\s*(.*?)\s*\|?\s*$", re.I)
CHECK = re.compile(r"^\s*[-*]\s*\[( |x|X)\]\s*(.+?)\s*$")
NEXT = re.compile(r"^\s*-\s*\[( |x|X)\]\s*\[(owner|claude|both)\]\s*(?:(\d{4}-\d{2}-\d{2})\s+)?(\S.*?)\s*$")


def find_root(start: Path) -> Path:
    """docs/sdlc (with a cycles/ folder) in this folder or the nearest parent that has one; docs/sdlc under start if none."""
    for base in [start, *start.resolve().parents]:
        if (base / "docs" / "sdlc" / "cycles").is_dir():
            return base / "docs" / "sdlc"
    return start / "docs" / "sdlc"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig") if path.exists() else ""


def section(text: str, heading: str) -> str:
    """The lines under '## <heading>' up to the next '## ' heading."""
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith(heading.lower())
            continue
        if inside:
            out.append(line)
    return "\n".join(out)


def checks(text: str) -> list[tuple[bool, str]]:
    return [(m.group(1).lower() == "x", m.group(2)) for m in map(CHECK.match, text.splitlines()) if m]


def table_checks(text: str) -> list[tuple[bool, str]]:
    """Checkboxes inside table cells ('| [ ] |' / '| [x] |'), labelled with the row's first cell."""
    found = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        for cell in cells[1:]:
            m = re.match(r"^\[( |x|X)\]\s*(.*)$", cell)
            if m:
                found.append((m.group(1).lower() == "x", (cells[0] + (" (" + m.group(2) + ")" if m.group(2) else "")).strip()))
    return found


def criteria(verify: str) -> dict:
    counts = {"pass": 0, "accepted": 0, "pending": 0, "fail": 0, "total": 0}
    for line in verify.splitlines():
        if not re.match(r"^\|\s*\d+\s*\|", line):
            continue
        cells = line.split("|")
        if len(cells) < 5:
            continue
        result = cells[3].lower()
        counts["total"] += 1
        if "accepted" in result:
            counts["accepted"] += 1
        elif "pending" in result or "partial" in result or "not checked" in result:
            counts["pending"] += 1
        elif "fail" in result:
            counts["fail"] += 1
        elif "pass" in result:
            counts["pass"] += 1
    return counts


def stage_states(folder: Path) -> list[dict]:
    files = {key: folder / f"{key}.md" for key, _ in STAGES if key != "build"}
    text = {key: read(path) for key, path in files.items()}
    states = []
    done_before = True  # every earlier stage is done
    for key, label in STAGES:
        open_items: list[str] = []
        total = 0
        if key == "build":
            has_file = files["verify"].exists()
            state = "done" if has_file else ("active" if done_before else "todo")
            note = "work happens in commits and the plan's log"
            file = "plan.md"
        else:
            file = files[key].name
            has_file = files[key].exists()
            if key in ("intent", "spec", "plan"):
                items = checks(section(text[key], "Gate"))
            elif key == "verify":
                items = [c for c in checks(section(text[key], "Verdict")) if "sent back" not in c[1].lower()]
            else:
                items = table_checks(section(text[key], "What moves where"))
            total = len(items)
            open_items = [name for ok, name in items if not ok]
            if not has_file:
                state = "todo" if not done_before else "next"
            elif open_items or (total == 0 and key != "learn"):
                state = "active"
            else:
                state = "done"
            if key == "learn" and has_file and not open_items and not done_before:
                state = "active"
            note = ""
        states.append({"key": key, "label": label, "state": state, "file": file, "exists": has_file, "gate_total": total, "gate_open": open_items, "note": note})
        done_before = done_before and state == "done"
    return states


def title_of(folder: Path) -> str:
    first = read(folder / "intent.md").splitlines()[:1]
    if first and first[0].startswith("#"):
        name = re.sub(r"^#\s*(Intent:\s*)?", "", first[0]).strip()
        return name[:1].upper() + name[1:]
    return folder.name


def header(folder: Path) -> dict:
    """The Status and Importance rows of intent.md's header table: status ('open' or 'dismissed'), dismissed_on, importance (1 to 5 or None), importance_note, importance_by."""
    rows = {}
    for line in read(folder / "intent.md").splitlines():
        m = HEADER_ROW.match(line)
        if m:
            rows[m.group(1).lower()] = m.group(2)
    status = rows.get("status", "")
    dismissed = status.lower().startswith("dismissed")
    on = re.search(r"\d{4}-\d{2}-\d{2}", status)
    imp = rows.get("importance", "")
    score = re.match(r"\s*([1-5])(?!\d)", imp)
    by = re.search(r"\((owner|claude)\b", imp, re.I)
    note = imp.split("):", 1)[1].strip() if "):" in imp else ""
    return {
        "status": "dismissed" if dismissed else "open",
        "dismissed_on": (on.group(0) if on and dismissed else ""),
        "importance": int(score.group(1)) if score else None,
        "importance_by": by.group(1).lower() if by else "",
        "importance_note": note,
    }


def next_actions(folder: Path) -> list[dict]:
    out = []
    for line in read(folder / "next.md").splitlines():
        m = NEXT.match(line)
        if m:
            out.append({"done": m.group(1).lower() == "x", "who": m.group(2), "due": m.group(3), "text": m.group(4)})
    return out


def current_stage(states: list[dict]) -> dict:
    for s in states:
        if s["state"] != "done":
            return s
    return {"key": "closed", "label": "Closed", "state": "done", "gate_open": []}


def cycle(folder: Path) -> dict:
    states = stage_states(folder)
    now = current_stage(states)
    head = header(folder)
    if head["status"] == "dismissed":  # stages never reached are shown as dismissed, not as "later"
        for st in states:
            if st["state"] != "done":
                st["state"] = "dismissed"
        now = {"key": "dismissed", "label": "Dismissed", "state": "dismissed", "gate_open": []}
    stamp = max((p.stat().st_mtime for p in folder.rglob("*") if p.is_file()), default=0)
    return {
        "id": folder.name.split("-")[0],
        "folder": folder.name,
        "title": title_of(folder),
        "current": now["key"],
        "current_label": now["label"],
        "stages": states,
        **head,
        "open_gate": now.get("gate_open", []),
        "criteria": criteria(read(folder / "verify.md")),
        "next": [] if head["status"] == "dismissed" else next_actions(folder),
        "last_touched": datetime.fromtimestamp(stamp).date().isoformat() if stamp else None,
    }


def board(root: Path) -> dict:
    cycles = [cycle(f) for f in sorted((root / "cycles").glob("[0-9]*-*")) if f.is_dir()]
    todo = [(c, n) for c in cycles for n in c["next"] if not n["done"]]
    todo.sort(key=lambda cn: (cn[1]["due"] or "9999-99-99", -(cn[0]["importance"] or 0), cn[0]["id"]))  # earliest date, then the more important cycle
    flat = [{"cycle": c["id"], "title": c["title"], "importance": c["importance"], **n} for c, n in todo]
    return {
        "generated": datetime.now().isoformat(timespec="minutes"),
        "today": date.today().isoformat(),
        "cycles": cycles,
        "your_move": [n for n in flat if n["who"] in ("owner", "both")],
        "my_move": [n for n in flat if n["who"] in ("claude", "both")],
    }


def datasets(data: dict, folder: Path) -> None:
    """Two flat files for the cycle board: one row per cycle (stages as columns), one row per open action (row 0 is the recommended next step)."""
    folder.mkdir(parents=True, exist_ok=True)
    rows = []
    for c in data["cycles"]:
        row = {"id": c["id"], "title": c["title"], "current": c["current_label"], "status": c["status"], "dismissed_on": c["dismissed_on"], "importance": c["importance"] if c["importance"] is not None else "", "importance_by": c["importance_by"], "importance_note": c["importance_note"], "last_touched": c["last_touched"] or ""}
        row.update({s["key"]: s["state"] for s in c["stages"]})
        row.update({"pass": c["criteria"]["pass"], "accepted": c["criteria"]["accepted"], "pending": c["criteria"]["pending"], "fail": c["criteria"]["fail"], "total": c["criteria"]["total"]})
        row["open_gate"] = "; ".join(c["open_gate"])
        rows.append(row)
    seen: dict[str, dict] = {}
    for n in data["your_move"] + data["my_move"]:
        seen.setdefault(f"{n['cycle']}|{n['text']}", n)
    lane = {"owner": 0, "both": 1, "claude": 2}  # the owner's own actions first: row 0 is what the board recommends
    ordered = sorted(seen.values(), key=lambda n: (lane[n["who"]], n["due"] or "9999-99-99", -(n.get("importance") or 0), n["cycle"]))
    actions = [{"key": f"{n['cycle']}-{i + 1}", "cycle": n["cycle"], "title": n["title"], "who": n["who"], "due": n["due"] or "", "text": n["text"]} for i, n in enumerate(ordered)]
    (folder / "cycles.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    (folder / "actions.json").write_text(json.dumps(actions, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {folder / 'cycles.json'} ({len(rows)} cycle(s)) and {folder / 'actions.json'} ({len(actions)} open action(s)).")


def markdown(data: dict) -> str:
    """The board as plain markdown: the same facts as the live board, readable in any repo viewer."""
    mark = {"done": "x", "active": "o", "next": "-", "todo": ".", "dismissed": "~"}
    out = [
        "# Cycle board",
        "",
        f"Generated {data['generated'].replace('T', ' ')} by the ai-sdlc skill from `cycles/*/`. Do not edit by hand: change the cycle's files and run the script again.",
        "",
        "Stages: `x` done, `o` in progress, `-` up next, `.` later, `~` dismissed.",
        "",
        "## What next?",
        "",
    ]
    moves = [("Your move", data["your_move"]), ("My move (the agent)", [n for n in data["my_move"] if n["who"] == "claude"])]
    if not any(m for _, m in moves):
        out += ["Nothing is open in any `next.md`.", ""]
    for label, items in moves:
        if not items:
            continue
        out += [f"**{label}**", ""]
        out += [f"- {n['cycle']} {n['title']}: {n['text']}" + (f" (due {n['due']})" if n["due"] else "") + (" [both]" if n["who"] == "both" else "") for n in items]
        out.append("")
    out += ["## Cycles", "", "| # | Cycle | Imp. | Now | " + " | ".join(label for _, label in STAGES) + " | Criteria | Touched |", "|---|---|---|---|" + "---|" * len(STAGES) + "---|---|"]
    for c in data["cycles"]:
        crit = c["criteria"]
        done = f"{crit['pass'] + crit['accepted']}/{crit['total']}" if crit["total"] else ""
        now = f"Dismissed {c['dismissed_on']}".strip() if c["status"] == "dismissed" else c["current_label"]
        stages = " | ".join(mark.get(s["state"], "?") for s in c["stages"])
        imp = f"{c['importance']}/5" if c["importance"] else ""
        out.append(f"| {c['id']} | {c['title']} | {imp} | {now} | {stages} | {done} | {c['last_touched'] or ''} |")
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", help="the folder that holds cycles/ (default: docs/sdlc, found by walking up from here)")
    parser.add_argument("--markdown", metavar="FILE", help="write the board as a markdown table to this file ('-' for the screen)")
    parser.add_argument("--out", help="write the JSON to this file instead of the screen")
    parser.add_argument("--datasets", metavar="DIR", help="write cycles.json and actions.json (the cycle board's data) into this folder")
    args = parser.parse_args()
    data = board(Path(args.root) if args.root else find_root(Path.cwd()))
    if args.markdown:
        if args.markdown == "-":
            sys.stdout.reconfigure(encoding="utf-8")
            print(markdown(data), end="")
        else:
            Path(args.markdown).write_text(markdown(data), encoding="utf-8")
            print(f"Wrote {args.markdown} ({len(data['cycles'])} cycle(s)).")
        if not (args.datasets or args.out):
            return 0
    if args.datasets:
        datasets(data, Path(args.datasets))
        return 0
    text = json.dumps(data, indent=1, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Wrote {args.out}: {len(data['cycles'])} cycle(s).")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
