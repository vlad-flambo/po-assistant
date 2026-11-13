# Project profile: <project name>

What the ai-sdlc skill needs to know about this repository. Everything in the skill that depends on the project lives here, so the skill itself stays the same from project to project. Keep it short and true; fix a line when you find it wrong.

| | |
|---|---|
| **Owner** | <who decides at the gates> |
| **Run Python / scripts with** | <`python`, `python3`, `uv run python`, ... the command that works here> |
| **Shell** | <bash, PowerShell 5.1 (no `&&`), ...> |
| **Tests** | <the command, and the expected result today> |
| **Secrets live in** | <`.env` / a vault / CI secrets; variable names only, never values> |
| **Hosts and irreversible actions** | <production, hosted databases, deploys, registries: what must be asked before touching> |
| **Project memory / status note** | <the file or tool where live state is kept between sessions, updated when a cycle moves; "none" is fine> |
| **Stack** | house-stack (deviations: none). Reference: `~/.claude/skills/house-stack`. Database tier for this project: <tier 1: SQLite, PC only; or tier 2: Postgres, hosted> |
| **Product docs that a cycle updates** | <PRD, README, runbook, ADRs: where `learn.md` moves findings> |
| **Board data folder** | `docs/sdlc/board-data` (gitignored) |
| **Live board** | <artifact URL, or "none yet": `BOARD.md` is the board until one is created> |
| **Commit / push rules** | commit only your own paths when the owner agrees; push only when asked |

## Notes for this project
<anything else a cycle must respect: cost caps, quirks of the platform, how to rehearse on a local copy, who owns which account>
