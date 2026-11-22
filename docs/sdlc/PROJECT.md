# Project profile: PO Assist

What the ai-sdlc skill needs to know about this repository. Everything in the skill that depends on the project lives here, so the skill itself stays the same from project to project. Keep it short and true; fix a line when you find it wrong.

| | |
|---|---|
| **Owner** | Vlad (VP Customer Operations), decides at every gate |
| **Run Python / scripts with** | `uv run python` for project code (uv 0.11 installed); `python3` (3.13) for the ai-sdlc scripts |
| **Shell** | zsh on macOS (Vlad's Mac, since the 2026-11-21 account migration) or bash in a Linux cloud container (Claude Code sessions; no access to `api.mistral.ai` there) |
| **Tests** | `uv run pytest` (71 tests verts au 2026-11-22) |
| **Secrets live in** | `MISTRAL_API_KEY` (modèle par défaut, décision 013-D1) ou `ANTHROPIC_API_KEY` dans un `.env` non versionné à la racine (chargé par le lanceur Mac). Jamais dans le dépôt ni affichée par l'application. Moteur par défaut : l'API (décision 012-D1, 2026-11-17), le skill Claude Code en repli |
| **Hosts and irreversible actions** | No hosted service. The GitHub repo `vlad-flambo/po-assistant` is **public**: nothing personal or confidential goes in it (saxobeat internal docs removed 2026-11-22). Cloud sessions push to their own `claude/…` branch, merged into `main` by Vlad. No real Linear API call, ever (the integration is simulated) |
| **Project memory / status note** | `docs/sdlc/BOARD.md` + `docs/journal.md` (process log for the jury, see cycle 007) |
| **Stack** | not on house-stack (no house-stack skill in this environment). Python, SQLite (tier 1, file committed to the repo), API par défaut : Mistral (HTTP direct, httpx2) ou Claude (SDK anthropic) selon le modèle, skill Claude Code en repli via échange de fichiers, interface Streamlit |
| **Product docs that a cycle updates** | `README.md`, `docs/guide-utilisateur.md`, `docs/demarche.md` (technical choices), `docs/presentation.md` (+ `docs/presentation/` deck), `docs/journal.md` |
| **Board data folder** | `docs/sdlc/board-data` (gitignored) |
| **Live board** | none yet: `BOARD.md` is the board until one is created |
| **Commit / push rules** | commit only our own paths; `main` is the reference branch (Vlad, 2026-11-16); cloud sessions work on their assigned branch and Vlad merges |

## Notes for this project

- **Context:** technical test "Construire un agent IA au service d'un Product Owner" (brief: `docs/brief/brief.md`). Delivery deadline: **Monday 2026-11-16 evening** (delivered; presentation date to be confirmed by Vlad).
- **Working assumptions (owner, 2026-11-14):**
  - The PO's backlog tool is **Linear**. Every channel (emails, support tickets, comments) is assumed to flow into Linear.
  - There is **no real Linear integration**: the agent behaves as if it were connected to Linear, but reads and writes a **local SQLite database** shaped like Linear's data.
  - All data is **synthetic**. The SQLite database **is committed to GitHub** for simplicity (owner decision; acceptable because nothing is real).
  - The synthetic dataset is **based on the owner's GitHub project `Vlad-Flambo/saxobeat`** (not reachable from this session on 2026-11-14, see cycle 001).
- **Decisions already taken (owner, 2026-11-14):** web app interface, French first (some English feedbacks), RICE + MoSCoW (WSJF optional), no real Jira/Linear integration (Markdown/CSV export), project run as ai-sdlc cycles.
- **AI use must be traceable:** the brief scores the process (20 %). Every piece of work delegated to an AI assistant is logged with how it was checked.
- **Account migration (2026-11-21):** the project moved from another Claude and GitHub account to this Mac (git identity `vlad-flambo`). `origin` is now `vlad-flambo/po-assistant` (public). The ported `.venv` pointed to the old user's Python: recreate it with `uv sync`. The slide deck lived only as an artifact on the old Claude account and was lost; rebuilt on 2026-11-22 (see `docs/presentation.md`).
