---
name: ai-sdlc
description: Run work in any repository as AI-native SDLC cycles in docs/sdlc (intent, spec, plan, build, verify, learn), one folder per cycle, with human gates, grill-me questioning, evidence for every claim, importance ranking, and a maintained cycle board with a "what next?". Sets docs/sdlc up in a repo that has none. Use this whenever the user starts or continues a cycle, says "new cycle", "next cycle", "set up the SDLC here", "grill me", "what next?", "where are we", "update the board", "close the cycle", "dismiss this intent", "how important is it", "rank the cycles", asks for a spec, plan, verification or learn step, or wants a non-trivial change, migration or investigation handled in a structured, reviewable way, even if they do not say "SDLC".
---

# AI-native SDLC cycles

A **cycle** is one small outcome taken through six stages. Every stage leaves a file in `docs/sdlc/cycles/NNN-name/`, so the next session (or agent) starts from the files, not from the chat. The human decides at each gate; the agent does the legwork between gates.

```
intent -> spec -> plan -> build -> verify -> learn
```

The reason for the structure: long chats lose decisions and drift into "it works, I think". Files make decisions durable, gates keep the owner in control of irreversible steps, and a recorded measure of success stops the work from quietly changing its goal.

This skill is project-independent. Everything that depends on the repository (how to run Python, where secrets live, what is irreversible, the board link) lives in **`docs/sdlc/PROJECT.md`** in that repository, never in this file.

## Start every session here

1. Does `docs/sdlc/` exist in this repository (look from the repository root)?
   - **No**: offer to set it up (see "Setting up a repository"), then continue. Do not start a cycle without it.
   - **Yes**: read `docs/sdlc/PROJECT.md` (the project profile) and the status table in `docs/sdlc/README.md`. Follow what PROJECT.md says about the Python command, the shell, secrets, irreversible actions and the memory note. If PROJECT.md still has `<placeholders>`, fill what you can find out yourself and ask the owner only for the rest.
2. If PROJECT.md's **Stack** row names `house-stack`, that user-level skill is the reference for tech stack, hosting, design system, conventions and gotchas. Do not re-decide those choices: at the Spec and Plan stages read the file it points to for the question at hand (`stack.md`, `hosting.md`, `design-system.md`, `conventions.md`, `gotchas.md`), and record any deviation as a decision. A project with no Stack row is treated as "not yet on the house stack": offer to add the row.
3. Run the status script (below) to know where every cycle is before you answer or act.

`S` below is this skill's `scripts/` folder (the base directory shown when the skill loads). `<python>` is the command PROJECT.md names (`python`, `python3`, `uv run python`, ...). Run the scripts from anywhere inside the repository.

## Where things live

```
docs/sdlc/
  README.md                 the method for humans, and the status table
  PROJECT.md                this project's profile (run commands, secrets, hosts, board link)
  BOARD.md                  generated: the board as a table (never edited by hand)
  templates/                one template per stage (intent, spec, plan, verify, learn, decisions, next)
  cycles/NNN-short-name/
    intent.md  spec.md  plan.md  verify.md  learn.md    one per stage, created when the stage starts
                            (intent.md's header table also carries the cycle's Importance and, if dismissed, its Status)
    next.md                 what happens next, one line per action (feeds the board)
    decisions.md            optional: decisions with reasons, never edited, only superseded
    evidence/               counts, outputs, measurements that back a claim in verify.md
<this skill>/
  scripts/sdlc_status.py    derives every cycle's state, importance and dismissal from those files (JSON, markdown board, board datasets)
  scripts/sdlc_init.py      sets up docs/sdlc, creates the next cycle, builds the live board's page
  templates/                the files init copies into a repository
  board/index.html          the live board's page
  reference/board.md        how to create and refresh the board
```

The project's product docs (PRDs, READMEs, runbooks) stay the product-level source of truth. A cycle's `spec.md` is the small per-outcome version; when a cycle changes product behaviour, `learn.md` names the doc that gets the update.

## Setting up a repository

1. `<python> S/sdlc_init.py init --project "<Project name>"` creates `docs/sdlc/` with README, PROJECT, templates and `cycles/`, and gitignores `docs/sdlc/board-data/`. It never overwrites a file.
2. Fill `docs/sdlc/PROJECT.md`: look in the repository first (package files, `README`, CI config, `.env.example`, existing docs) for the Python command, tests, hosts and secrets; ask the owner only what the repository cannot tell you. Variable names only, never secret values.
3. Add a one-line mention to the repository's `CLAUDE.md` or README if one exists ("work runs as ai-sdlc cycles, see docs/sdlc"), so other agents find the method.
4. Generate the first board: `<python> S/sdlc_status.py --markdown docs/sdlc/BOARD.md`.
5. Commit only these paths when the owner agrees.

## The stages and their gates

| Stage | File | The question | Gate (lines in the file's `## Gate` or `## Verdict` section) |
|---|---|---|---|
| Intent | `intent.md` | Why, for whom, what does "done" look like, what are we not doing? | goal and success measure confirmed; all questions answered or parked |
| Spec | `spec.md` | What will be true when finished? Acceptance criteria, constraints, out of scope | owner approved |
| Plan | `plan.md` | Which thin slices, in what order, with which check and rollback each? | owner approved |
| Build | commits, plan's "As run" log | One slice at a time | per-slice check |
| Verify | `verify.md` | Evidence per acceptance criterion | verdict: accepted by owner (or sent back) |
| Learn | `learn.md` | What changed in our understanding, docs and memory? | every row of "What moves where" ticked |

Gates are markdown checkboxes (`- [ ]` / `- [x]`). The status script reads them, so tick them for real and only when the owner has said so. Never tick an owner's gate on their behalf.

## Starting a cycle

1. Gather facts yourself before asking anything: read the code, the docs, the files on disk, look things up. Mark anything from memory as "to be verified".
2. Assess its **importance** (next section) from those facts: a score and one line of evidence.
3. `<python> S/sdlc_init.py new "short name" --importance N --reason "evidence" --owner "<name>"` picks the next number, creates `cycles/NNN-name/` with `intent.md` (importance already in its header table) and `next.md` from the templates, and adds the row to the README status table. (By hand: copy the templates; same result.)
4. Fill in the owner's words verbatim under "The request, in your words", and each fact from step 1 in "What we already know" with its source.
5. Refresh the board (below), then start grilling.

## Importance: ranking the cycles

Every cycle carries one **importance from 1 to 5** so the owner can rank them (the live board has a "Sort by importance" button). It is a judgment, so it is typed, not derived, in the header table of `intent.md`:

```
| **Importance** | 4/5 (claude, 2026-10-30): nothing is e-mailed yet; invitations depend on passing links by hand |
```

- The first digit is the score; `(claude, date)` says who set it; the text after `):` is the reason, one short line that names the evidence (the board shows it on hover).
- **Scale:** 5 critical (data loss or wrong data, a hosting or cost cap, or nothing works without it) · 4 high (blocks other cycles, or a core flow for every user) · 3 useful (a clear gap or gain for most users; nothing breaks without it) · 2 minor (polish, small gaps, or few users) · 1 marginal (cosmetic, hardly anyone affected).
- **How to assess:** reach (how many users, how often), pain (how much it hurts, what the owner or a user said, a feedback count if there is one), what it unlocks (other cycles that wait on it), and the risk of not doing it. Use facts you have found, not taste; if you have none, say "no evidence yet" in the reason and lean low.
- **You make the first assessment** when a cycle starts, and again when facts change (a result in Verify, a new feedback). **The owner overrules it**: when they give a number, write it as `(owner, date)` with their reason, and never lower or raise an `owner` score yourself.
- Importance ranks cycles; it does not order the steps inside one. In "what next?" it only breaks ties (see below).

## Dismissing a cycle

The owner can drop a cycle at any stage ("dismiss this intent", "this does not affect most users"). Dismissing is a decision, not a deletion:

1. In `intent.md`: add `| **Status** | Dismissed YYYY-MM-DD by the owner: <their reason> |` to the header table, and a short "Decision: dismissed" section at the top saying what was not done and what would reopen it. Leave the open questions and the gate as they are: nothing was confirmed, so nothing is ticked.
2. Tick every line of `next.md` (say "dismissed" in one of them); a dismissed cycle has no actions.
3. In the README status table: "Dismissed YYYY-MM-DD at the <stage> stage, <reason>; reopen if ...".
4. Keep the folder and its facts: they are the record, and a reopening starts from them (remove the Status row, add a line to the Decision section saying when and why, update the board).
5. Refresh the board. The script then shows the cycle as **Dismissed** with the date, its unreached stages crossed out, and removes its actions from "what next?".

If the cycle was born from an item in an outside system (a feedback form, a ticket, an issue), say in the reply that the item itself is still open there; changing it is a write outside the repository, so only do it when the owner asks.

## Grill-me protocol (the Intent stage, and any time a decision is open)

- Ask **one question at a time**, with your **recommended answer** and the reason. The owner can accept in one word.
- **Never ask what you can find out.** Read the repo, run a read-only check, or search the docs first; ask only what only the owner knows or decides.
- Record the answer in the file **the moment it is given**, in the open-questions table (question, recommendation, answer, status). A decision that lives only in chat is lost.
- Group low-stakes questions that have a sensible default into one "accept my recommended answers to Q3, Q4 and Q7?".
- Treat the owner's guesses as hypotheses worth a cheap check ("probably resets on the 22nd" is a note marked *unverified*, not a fact). Say so, and say what would confirm it.
- A question the evidence overturns is worth saying out loud: when a result contradicts an earlier assumption (or the docs), correct the record and tell the owner.
- Close the stage by listing what is decided, what is parked, what is still open, and asking for approval to move on.

## Running the other stages

- **Spec**: acceptance criteria are numbered and each one must be checkable in `verify.md`. Include a "Not doing" list, constraints, risks and the rejected options with one line on why.
- **Plan**: slices are thin and ordered so everything that changes nothing in production comes first and the one irreversible step is a single, rollback-able edit. Each slice names who does it (owner or agent), what it touches, its check and its rollback.
- **Build**: one slice at a time, stop at its check. Keep an "As run" log in `plan.md`: what was done, what failed, what was learned, with times. Failures belong in the log, not in silence.
- **Verify**: one row per criterion with the evidence (command and output, measurement, file in `evidence/`). The table's rows start with the criterion number and the Result column holds `pass`, `fail`, `accepted`, `pending`, `partial` or `not checked` (the script counts these). A criterion that is partly met says so, and an accepted risk is marked as accepted by the owner with the date. List what was **not** verified.
- **Learn**: compare the outcome with the success measure; list the findings; give each a destination (docs, README, memory, a rule, or **house-stack** when it will bite another project too: a gotcha, a design asset, a dated provider fact) and tick it when moved. End with next-cycle candidates and process feedback for this playbook.

## Evidence over assertion

- **Prove, don't observe.** A health check proving "ok" is not proof the new backend is in use. Find the signal that can only be true if the change took effect (for example a login timestamp in the new database and not in the old one). Prefer a signal whose absence would contradict you.
- **Rehearse on a local copy** anything that writes to a hosted service, before touching it. Measure first, then change.
- **Say what is not verified**, and what a weaker proxy was used instead.
- **Numbers carry their source and time** ("4.76 GB, owner, sum of all projects, 2026-10-29").

## Safety rules that apply to every cycle

- **Secrets** (connection strings, keys, tokens) are never pasted in chat, written to a file in the repo, or put on a command line. They live where PROJECT.md says (an untracked env file, a vault, CI secrets), travel in environment variables set for one process, and tools print yes/no or counts, never the value. Check an env file's structure by printing only variable names and flags.
- **Outward or irreversible actions** (restoring into a hosted database, changing a production setting, deleting a project, pushing, publishing, sending messages) happen only inside an approved plan, after a guard check (for example "refuse if the target is not empty"), and the owner performs the ones that need their accounts. Ask before anything not in the plan. PROJECT.md lists what counts as irreversible here.
- **Do not widen the blast radius for a measurement.** If a reading would spend a scarce allowance (an API quota, a billing cap, production load), say what it costs before taking it, or take it on a local copy.
- **Commit only your own paths** (`git add <paths>`), with a message that says what changed and why; never commit env files, dumps or data. Commit when the owner agrees; do not push unless asked.

## next.md and the board

`next.md` is the one thing that cannot be derived from the files: judgment about what happens next. One line per action:

```
- [ ] [owner] 2026-10-30 Read the sum of all projects in the hosting dashboard and tell me
- [ ] [claude] Record criterion 9 and commit
- [x] [owner] An action that is done
```

`[owner]`, `[claude]` or `[both]`; the date is optional. After **every step that moves a cycle** (an answer recorded, a stage approved, a slice done), do these four things:

1. Tick the gate or checkbox that moved; update the cycle's row in `docs/sdlc/README.md`.
2. Update `next.md`: tick what is done, add what is now next, say who owes it and by when.
3. Run `<python> S/sdlc_status.py` (add `--out file.json` to save it). It derives every cycle's stage, open gate items, criteria counts and the "your move / my move" lists from the files, so the board cannot drift.
4. **Refresh the cycle board**, both levels as `reference/board.md` describes: always `<python> S/sdlc_status.py --markdown docs/sdlc/BOARD.md`; and, when PROJECT.md names a live board and the Artifact tool is available, refresh its datasets. That file also says how to create the live board when a project has none, how to change its page, and what to do when its link is dead. **Read it the first time you touch the board in a session.**
5. If PROJECT.md names a memory or status note, update it when a cycle moves stage or closes.

The board is a view, not a record: when it disagrees with the files, the files win and the board is regenerated.

## Answering "what next?"

Run the status script and answer from its output: the owner's open actions first (earliest date first; among the same date, the cycle with the higher importance first), then yours, with **one recommended next step** and the reason. Dismissed cycles never appear. If a cycle is blocked on a reading or a decision only the owner can give, say exactly what to read or decide and in what form. If nothing is due, propose the most useful free action (often a measurement that costs nothing) and say why. Never invent a next step that is not in `next.md` or a gate; if you think one is missing, propose it and add it once the owner agrees.

## Closing a cycle

Verdict in `verify.md`, every "What moves where" row ticked or explicitly deferred with a date in `learn.md`, the cycle's row in the README status table set to closed, all `next.md` lines ticked or moved to the next cycle, the board refreshed, and one commit with the documentation. Do not delete the fallback, the evidence or the log: they are the record.

## Improving this skill

When a cycle's "Process feedback" says the method itself slowed the work down, propose the edit to this skill to the owner. The skill is shared by every project: change it for all of them or not at all, and keep project facts in PROJECT.md. If the skill is installed in more than one place (a project copy and a user-level copy), edit both or say which one is canonical.
