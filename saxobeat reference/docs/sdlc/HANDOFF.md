# Handoff: moving from the Windows PC to a Mac (written 2026-11-10)

This note is for the owner and for the Claude session that starts on the Mac. The cycles' own files stay the record of every decision; this note only says **what does not travel through git** and how to start again.

## 1. Where the work stands

Run `uv run python .claude/skills/ai-sdlc/scripts/sdlc_status.py` (or read [BOARD.md](BOARD.md)) for the full picture, and ask Claude "what next?". The items that were moving on 2026-11-10:

| Cycle | State | Next action (also in its `next.md`) |
|---|---|---|
| 025 Environments (prod, pre-prod, testbed) | Intent confirmed by the owner, **spec drafted** (20 criteria, decisions D1 to D5) | The owner reads [spec.md](cycles/025-environments-prod-pre-prod-testbed/spec.md) and approves or changes it; then the plan |
| 026 Cloud runner, 027 Cloud AI step, 028 Cloud dev workspace | Intent drafted, questions open | Wait for 025 (026, 028) and for 025 and 026 (027) |
| **033 Invitation codes for sign-up** | **Live on the host since 2026-11-06** (commits `154897f`, `b1afe41`, pushed); verify written: 16 of 18 criteria pass, 13 partial, 18 pending; learn drafted | The owner signs up through `https://app.saxobeat.fr/signup/?code=Skaleet`, opens *Inviter des amis* on a phone, then says accepted or sent back; decide if 20 sign-ups an hour is too loose (`SIGNUPS_IN_ALL`, one account is about 8 MB); see [033's next.md](cycles/033-referral-codes-for-sign-up/next.md) |
| 029 Keyword edits rescore the inbox | Plan approved, nothing built | Read "Resume here" at the end of its `plan.md`, then build slice 1 |
| Everything else | See BOARD.md | |

The request that started 025 to 028 is quoted verbatim in [025's intent](cycles/025-environments-prod-pre-prod-testbed/intent.md).

## 2. What is not in git (carry it by hand)

| What | Where it is on the PC | Why it matters | How to move it |
|---|---|---|---|
| **`.env`** (secrets: Neon addresses for prod1 and the old project, the Brevo key, the Adzuna key) | the repository folder | nothing hosted can be read or written without it | **Password manager or an encrypted drive. Never e-mail, chat or commit it.** The variable names in it (checked 2026-11-10, no values): `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`, `DATABASE_URL` (the local database), `SAXOBEAT_HOSTED_DATABASE_URL` (prod1), `SAXOBEAT_FALLBACK_DATABASE_URL` (the old project), `SAXOBEAT_MAIL`, `BREVO_API_KEY`, `SAXOBEAT_MAIL_FROM`, `SAXOBEAT_PUBLIC_URL`, `SAXOBEAT_MAIL_REPLY_TO`. `.env.example` is **not** in git (the `.gitignore` pattern `.env.*` hides it) |
| **`data/`** (1.9 GB, gitignored) | the repository folder | see below | copy the parts you need |
| `data/*.csv` (about 340 KB): the employer lists and `employer_coverage*.csv` | `data/` | cycle 013's work (which employers are covered) lives only here | copy; small |
| `data/backups/saxobeat_2026-10-29_100546.dump` (about 65 MB) | `data/backups/` | cycle 029 slices 2 and 9 restore it as a scratch database | copy, or take a fresh backup on the Mac (the owner's call: it reads about 227 MB from Neon) |
| `data/cache/corpus_counts.json.gz` | `data/cache/` | the runner's word-count cache; losing it costs about 17 MB of Neon reads once | optional |
| The older dumps in `data/backups/` | | historical recovery copies (October) | copy only if you want them |
| **Claude's memory** (11 notes) | `C:\Users\Vladimir Stoyanov\.claude\projects\C--Users-Vladimir-Stoyanov-code-saxobeat\memory\` | decisions, gotchas and the owner's rules that are not in the repo | copy the folder to the matching `~/.claude/projects/<mac path of the repo, with / replaced by ->/memory/` on the Mac (start Claude Code once in the repo to see the exact folder name) |
| **User-level skill `house-stack`** | `C:\Users\Vladimir Stoyanov\.claude\skills\house-stack` | the stack, hosting and design reference that `ai-sdlc` points to; **it exists nowhere else** | copy the folder to `~/.claude/skills/house-stack` |
| User-level skill `ai-sdlc` | `C:\Users\Vladimir Stoyanov\.claude\skills\ai-sdlc` | identical to the project copy `.claude/skills/ai-sdlc` in the repo, which travels with git | nothing to do; copy it too if you want it for other projects |
| The AI hand-off folder | `C:\Users\Vladimir Stoyanov\Saxobeat AI` (`to-do` is empty on 2026-11-10; check `problems\` for a held onboarding file) | files that were not imported yet | look in `problems\` and `done\` before leaving; `manage.py ai sync` rewrites whatever is due |
| Docker volume `saxobeat_pg` (local Postgres) | Docker Desktop | stale (last written 2026-10-22); nothing depends on it | nothing |

The two skills `saxobeat-add-employer` and `saxobeat-ai-batch` are in the repo (`.claude/skills/`) and travel with git.

## 3. Setting up the Mac

1. Install `git`, **`uv`** (`brew install uv`) and **Docker Desktop** (the backup and restore tools run `postgres:17` through Docker).
2. `git clone https://github.com/vlad-flambo/saxobeat.git`, then in the folder: `uv sync`.
3. Put `.env` in the repository folder (section 2). Keep the file out of every sync or backup service.
4. Run the tests: `SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q -p no:cacheprovider` (zsh and bash accept an empty variable on the command line; **PowerShell does not**, which is why `docs/sdlc/PROJECT.md` has a rule for it). About 45 seconds; the last full count on Windows was 1,600 or more passing. Run it once before changing anything and write the number in the first cycle note you touch, so a platform difference shows up as a difference.
5. **The runner has a Mac version.** `scripts/pc_runner.sh`, `scripts/ai_sync.sh` and the double-click `saxobeat-runner.command`, `saxobeat-ai.command`, `saxobeat.command` do what the `.ps1` / `.cmd` files do, in the same order (the `.sh` files share `scripts/_env.sh`, which reads the hosted address from `.env` without sourcing it). `scripts/com.saxobeat.runner.plist` is the launchd counterpart of the Task Scheduler entry (install steps in its header). Needs `brew install uv`.

   Before any hosted command, the owner's standing rule applies: read Neon first, follow `docs/sdlc/cycles/001-local-db-replica/evidence/restart_runbook.md`, and check that the command's first line says "a remote server" before a write. Brevo only accepts calls from the addresses on its list, so `mail send` from a new machine answers 401 until its address is added (DEPLOY.md §7 step 2). A cleaner fix is cycle 026 (the cloud runner), which makes the machine irrelevant.
6. The scripts that cycles 013 and 001 mention have Mac versions too: `scripts/seed_hosted_sources.sh` (options `--apply --snapshot-taken --step 1|2|3|all --url-var NAME`) and `scripts/measure_reads.sh` (options `--label --run a,b,c --then --clean ...`; see its header). `measure_reads.sh` was only checked up to its guards (it needs Docker and the dump); run `--label noop` once first, the counter must not move. A Python replacement is part of cycle 025's refresh script (`scripts/refresh_copy.py`), written to run on both systems.
7. Open Claude Code in the repository and say "what next?". The project skill `.claude/skills/ai-sdlc` loads from the repo; copy `house-stack` first (section 2) so the Spec and Plan stages can use it.

## 4. Rules that still apply (they are the owner's, and they are in the memory notes)

- Commit only your own paths; push only when asked. **A push to `main` deploys to prod on Render** until cycle 025 changes that.
- Secrets never go in chat, files in the repository or command lines.
- Read `robots.txt` and the terms before the first request to a new site.
- Hosted writes (restore, deleting a project, enabling a source) only inside an approved plan; the owner performs the ones that need their accounts.

## 5. Git state when this note was written

See the commit that adds this file. Anything pushed is on `origin/main`; anything that was committed here but not pushed must be pushed from the Windows PC (or copied) before the Windows PC is switched off. The closing message of the session that wrote this note says exactly which commits those are.
