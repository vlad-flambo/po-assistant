# Project profile: PO Assist

What the ai-sdlc skill needs to know about this repository. Everything in the skill that depends on the project lives here, so the skill itself stays the same from project to project. Keep it short and true; fix a line when you find it wrong.

| | |
|---|---|
| **Owner** | Vlad (VP Customer Operations), decides at every gate |
| **Run Python / scripts with** | `uv run python` for project code (uv 0.11 installed); `python3` (3.13) for the ai-sdlc scripts |
| **Shell** | bash (Linux cloud container) |
| **Tests** | none yet (to be set by cycle 002: `uv run pytest`) |
| **Secrets live in** | untracked `.env` at the repo root (gitignored). Variable names: `ANTHROPIC_API_KEY`. Not set in this container on 2026-11-14 |
| **Hosts and irreversible actions** | No hosted service. Push to GitHub only on branch `claude/optimistic-brown-avbf17`. No real Linear API call, ever (the integration is simulated) |
| **Project memory / status note** | `docs/sdlc/BOARD.md` + `docs/journal.md` (process log for the jury, see cycle 007) |
| **Stack** | not on house-stack (no house-stack skill in this environment). Python, SQLite (tier 1, file committed to the repo), Claude API, light web UI |
| **Product docs that a cycle updates** | `README.md`, `docs/analyse/`, `docs/adr/` (technical decisions), `docs/journal.md` |
| **Board data folder** | `docs/sdlc/board-data` (gitignored) |
| **Live board** | none yet: `BOARD.md` is the board until one is created |
| **Commit / push rules** | commit only our own paths; push to `claude/optimistic-brown-avbf17` at the end of each step the owner validates |

## Notes for this project

- **Context:** technical test "Construire un agent IA au service d'un Product Owner" (brief: `docs/brief/brief.md`). Delivery deadline: **Monday 2026-11-16 evening**.
- **Working assumptions (owner, 2026-11-14):**
  - The PO's backlog tool is **Linear**. Every channel (emails, support tickets, comments) is assumed to flow into Linear.
  - There is **no real Linear integration**: the agent behaves as if it were connected to Linear, but reads and writes a **local SQLite database** shaped like Linear's data.
  - All data is **synthetic**. The SQLite database **is committed to GitHub** for simplicity (owner decision; acceptable because nothing is real).
  - The synthetic dataset is **based on the owner's GitHub project `Vlad-Flambo/saxobeat`** (not reachable from this session on 2026-11-14, see cycle 001).
- **Decisions already taken (owner, 2026-11-14):** web app interface, French first (some English feedbacks), RICE + MoSCoW (WSJF optional), no real Jira/Linear integration (Markdown/CSV export), project run as ai-sdlc cycles.
- **AI use must be traceable:** the brief scores the process (20 %). Every piece of work delegated to an AI assistant is logged with how it was checked.
