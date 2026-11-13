# The cycle board: how to create it and keep it current

The board answers "where is each cycle, and what happens next?" at a glance. It is **derived, never typed**: `scripts/sdlc_status.py` reads `docs/sdlc/cycles/*/` and the board only displays what it prints. So a board that is out of date is always fixable by running the script again.

There are two levels. Level 1 is mandatory and works in any repository with any agent; level 2 is optional and needs the Artifact tool (a Dashboard artifact).

| Level | What | Where | Needs |
|---|---|---|---|
| 1 | `docs/sdlc/BOARD.md`: the cycles as a table plus "what next?" | committed with the repo, shows in any viewer | Python only |
| 2 | A live dashboard: sortable table, five importance pips, dismissed chips, recommended next step | a private artifact; its link is in `docs/sdlc/PROJECT.md` | Artifact and ArtifactData tools |

`<python>` below is the command in `docs/sdlc/PROJECT.md` (python, python3, uv run python). `S` is this skill's `scripts/` folder.

## What "refresh the board" means (after every step that moves a cycle)

1. Level 1, always: `<python> S/sdlc_status.py --markdown docs/sdlc/BOARD.md`. Include `BOARD.md` in the commit that documents the step.
2. Level 2, when PROJECT.md has a live-board link and the Artifact tool is available:
   1. `<python> S/sdlc_status.py --datasets docs/sdlc/board-data` writes `cycles.json` (one row per cycle: `id, title, current, status, dismissed_on, importance, importance_by, importance_note, last_touched`, the six stages as columns with `done|active|next|todo|dismissed`, `pass, accepted, pending, fail, total`, `open_gate`) and `actions.json` (one row per open action of a non-dismissed cycle: `key, cycle, title, who, due, text`; row 0 is the recommended next step). That folder is gitignored; if the working directory does not allow writing there, write to the scratchpad instead.
   2. Upload each file to the board with the Artifact tool: `url` = the board, `asset: true`, `file_path` = the file (a JSON file goes in a call of its own). Each reply gives a new `/_blob/<id>` url.
   3. Read `datasets/cycles` and `datasets/actions` with ArtifactData (to get their `version`), then `batch` two `update`s pinned with `if_version`: `source.url` = the new `/_blob/...` url, `updated` = `{at: <now, ISO>, by: "Claude"}`. The page redraws by itself; the page file does not change for a data refresh. Other sessions may refresh the board too: pin to the versions you just read and, if a pin fails, re-read and redo.
   4. Delete the two superseded assets (Artifact `action: "delete"`, `url` + `path` = the old asset id) so the store does not fill up. The old ids are in the `source.url` you read in step 3.
3. Say in the reply that the board is refreshed (or that level 2 was skipped, and why).

If the Artifact tool is not available (another agent, offline), do level 1 only and add a line to `next.md`: `- [ ] [claude] Refresh the live board`, so the next session with the tool does it.

## Creating the live board (once per project)

Do it when the project has two or more cycles, or when the owner asks. The board is a private artifact; publishing it is the owner's call, so ask once, then record the link.

1. Artifact `action: "quickstart"` with `intent: "other"` (a dashboard that shows data) tells you the exact current way to start from the Dashboard type; follow it. In short: publish with the type's `type_url`, `title` = "<Project> cycle board", `auto_open: "after_first_write"`, no files.
2. Write the dashboard's documents with ArtifactData, one `batch`:
   - `dash/meta` = `{"title": "<Project> cycle board"}`
   - `datasets/cycles` = `{"title": "Cycles", "description": "One row per cycle: its title, importance (1 to 5), status (open or dismissed), the state of each of the six stages, criteria counts and the last change. Read from docs/sdlc by the ai-sdlc skill's sdlc_status.py.", "source": {"kind": "file", "format": "json", "name": "cycles.json", "url": "<the /_blob url from the upload>"}, "updated": {"at": "<now>", "by": "Claude"}}`
   - `datasets/actions` = the same shape, `title` "Open actions", `description` "One row per open action from every cycle's next.md, owner actions first, earliest date first; the first row is the recommended next step.", `name` "actions.json".
   - `files/index.html` = `{"text": <the page>}`: run `<python> S/sdlc_init.py board-page --project "<Project>" --out <file.json>` and send that file with `file_path` (the page is `S/../board/index.html` with the project name filled in).
   Upload the two data files first (step "Upload" above) to get their urls.
3. Read the type's own instructions that the publish result returns (the page rules: marks, `data-source`, `dash.draw`, the check read of `data/users/me` doc `check`) and follow them: they may have changed since this file was written. Fix what the check reports, at most twice.
4. Put the link in `docs/sdlc/PROJECT.md` ("Live board") and in `docs/sdlc/README.md` ("The board and what next?"). Commit.
5. Tell the owner the board is private, and that anyone who can open it can read the cycle titles and actions it shows.

## Changing the page itself (a column, a control)

Read the stored `files/index.html` again first (a person may have saved edits), and read `artifact-type/reference/one-writer.md` on the board artifact (fixed text goes in the HTML; a script writes only inside `dash.draw`). Write the whole page to a file, wrap it as `{"text": ...}` JSON, and `update` `files/index.html` with `file_path`, pinned with `if_version`. Keep `board/index.html` in this skill in step with what you published, so the next project gets the improvement; replace the project name with `__PROJECT__` there.

The page's columns are: #, Cycle, Importance (five pips, the reason on hover), Now (stage, or the Dismissed chip with its date), the six stage squares (a dismissed cycle's unreached stages are crossed out), Criteria, Touched. "Sort by Number / Importance" re-draws the table, dismissed cycles last. "What next?" shows row 0 of `actions` and the full list below.

## If the board is missing or its link is dead

Recreate it as above; the data comes from the files, so nothing is lost. Never treat the board as a source of truth: if the board and the files disagree, the files win.
