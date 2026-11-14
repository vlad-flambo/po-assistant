# Project profile: Saxobeat

What the ai-sdlc skill needs to know about this repository. Everything in the skill that depends on the project lives here, so the skill itself stays the same from project to project. Keep it short and true; fix a line when you find it wrong.

| | |
|---|---|
| **Owner** | Vladimir Stoyanov (Vlad) |
| **Run Python / scripts with** | `uv run python` (there is no bare `python` on this machine) |
| **Shell** | PowerShell on Windows (Windows PowerShell 5.1: no `&&`); Git Bash is also available for POSIX scripts |
| **Tests** | `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider` (SQLite, about 45 s; never leave `SAXOBEAT_MAIL` unset, the PC's `.env` has a live Brevo key; **run it from Git Bash**: in PowerShell `$env:DATABASE_URL=''` deletes the variable and pytest then tries the `.env` Postgres, 2026-11-06); more in the project memory note "Running tests" |
| **Secrets live in** | `.env` (untracked). Hosted database: `SAXOBEAT_HOSTED_DATABASE_URL`; fallback: `SAXOBEAT_FALLBACK_DATABASE_URL`. Use `scripts/db_counts.py` to compare databases without exposing an address |
| **Hosts and irreversible actions** | Django app on Render, Postgres on Neon (hosted and fallback projects), a PC runner. Restoring into a hosted database, changing a production setting, deleting a Neon project, pushing and deploying are irreversible: only inside an approved plan, after a guard check, and the owner performs the ones that need their accounts |
| **Project memory / status note** | Claude project memory `project-sdlc-cycles`: update it when a cycle moves stage or closes |
| **Stack** | house-stack (deviations: none recorded yet). Reference: `~/.claude/skills/house-stack`. Database tier: 2 (Postgres on Neon in production, SQLite for the everyday test suite; the suite should also run once on Postgres before a data-touching release). Known drift: `config/settings.py` still mentions Koyeb; `jobs/static/jobs/app.css` is the source of the skill's design assets, not a copy of them |
| **Product docs that a cycle updates** | `docs/PRD*.md` (product source of truth), `docs/DEPLOY.md` (what is live on the host) |
| **Board data folder** | `data/sdlc_board` (gitignored through `data/`); new projects use `docs/sdlc/board-data` |
| **Live board** | https://claude.ai/artifact/NVff2m66eVpfzbUdr1AmpJ (private artifact of the Dashboard type); `docs/sdlc/BOARD.md` is the same facts as a table |
| **Commit / push rules** | commit only your own paths (`git add <paths>`) when the owner agrees; the working tree often holds other in-progress work; push only when asked |

## Notes for this project

- The app is Saxobeat (a job-search tool: Django, Postgres on Neon, web on Render, a PC runner). Neon's free allowance resets on the 1st of the month; a reading that costs allowance is said out loud first.
- Rehearse anything that writes to Neon on a local copy first (scripts in `scripts/`).
- Many cycles share one working tree: stage only the paths of the cycle you are working on.

## Picking the work up on another computer

The Windows PC to Mac move (2026-11-10) is described in [HANDOFF.md](HANDOFF.md) (a second note, PICKUP.md, written by another session the same day, was merged into it and removed). This file's Python, shell and test rows describe the Windows PC; on a Mac use zsh and `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider`.
