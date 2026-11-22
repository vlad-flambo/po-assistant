# Close-out plan (2026-11-22)

Goal: every cycle 002–013 closed (verify accepted by Vlad, learn written), the work on `main`, and the deck and demo ready for the jury. Cycle 007 closes after the presentation.

## Where we are

| Cycle | Blocking item | Who |
|---|---|---|
| 002–006, 009, 011, 012 | All criteria pass; only the owner's "Accepted" box is open; no learn.md | Vlad accepts, Claude writes learn.md |
| 008 Mac launcher | Criterion 8: double-click on the Mac | Vlad |
| 010 Claude API option | Criterion 10: real Claude run. No Claude key, so the real-run check moves to 013 (decision needed) | Vlad decides |
| 013 Mistral engine | Criterion 8: real Mistral run with Vlad's key | Vlad |
| 007 Presentation | Goal not confirmed; verify and learn only possible after the presentation | Vlad, then Claude |

## Steps

### 1. Get the work onto `main` (Vlad, 2 min)
- [x] On the Mac, merge the session branch into `main` and push:
  `git fetch origin && git checkout main && git merge origin/claude/ecstatic-albattani-xad8g6 && git push`
  (Done 2026-11-22 via vlad-flambo/po-assistant#1.)

### 2. Real-world checks on the Mac (Vlad, about 30 min, one sitting)
- [x] `uv sync` (rebuilds the `.venv` ported from the old machine).
- [x] **008:** (« works, tested successfully », 2026-11-22) double-click `PO Assist.command` in Finder. Note what the Terminal window says and whether the browser opens on localhost:8007.
- [ ] **013:** add `MISTRAL_API_KEY=...` to `.env` at the repo root, then:
  `uv run python -m po_assist run analyse --engine api --limit 5` and `uv run python -m po_assist import`.
  Keep the full terminal output (cost, accepted, refused, ignored).
- [ ] **013, recommended:** measure Mistral's quality. In the app: Réinitialiser, Réglages › demo mode off, Agent › Lancer l'agent (≈ 0,35 $ for 80 feedbacks), Importer, then 🎯 Qualité. A screenshot of that page lets the deck say "measured on Mistral" next to the skill's 84 / 96 / 98 %.
- [ ] Réinitialiser and switch demo mode back on afterwards.
- [ ] **009 / 007:** rehearse the demo once with a timer, following `docs/presentation.md`.
- [ ] **011:** skim `docs/guide-utilisateur.md` (or the ❓ Guide page).
- [ ] **007:** page through the rebuilt deck: https://claude.ai/artifact/SnLtghS49Mfa2x2hSKPSxD

### 3. Send the results to Claude (Vlad, 2 min)
Paste in one message: the launcher output, the Mistral run output, the Qualité numbers (or screenshot), the rehearsal time, and anything that looked wrong in the deck or the guide.

### 4. Record the evidence (Claude)
- [ ] 008, 013 (and 010 if decided in step 5): results and dated evidence files in `verify.md`. Anything that failed goes back to its cycle's build stage instead.
- [ ] Mistral cost and quality written into the deck (slides 5 and 11), `docs/demarche.md` §6 and the README.
- [x] Refresh `docs/captures/6-agent.png` (also guide captures 02 and 03, 2026-11-22) (it still shows "API Claude"); it's the fallback if the app does not start.

### 5. Owner decisions (Vlad, one message)
- [x] Accept verify for 002, 003, 004, 005, 006, 009, 011, 012 (« I accept », 2026-11-22).
- [ ] Accept verify for 008 and 013 (after step 4).
- [ ] 010 criterion 10 (Vlad: « skipping this », 2026-11-22; recorded as not checked, cycle left open until you say close): accept as "covered by 013's real Mistral run" (recommended), or keep it open until a Claude key exists.
- [ ] 007: confirm the goal and success measure in its `intent.md` (the four measures listed there).

Claude ticks these boxes only on your words, quoting them with the date.

### 6. Close the cycles (Claude)
- [x] (2026-11-22, 002–006, 008, 009, 011, 012; 010 and 013 still open) One `learn.md` per cycle 002–006 and 008–013: outcome against the success measure, findings, and where each one moves (README, guide, démarche, journal), every row ticked.
- [ ] README status table: each cycle set to Closed; `next.md` lines all ticked or moved.
- [ ] Board regenerated, one commit, push.

### 7. Before the presentation (Vlad)
- [ ] Deck: Share › Export as PDF; keep a copy offline. Share the link with the jury if they should have it.
- [ ] App: Réinitialiser, demo mode on, the Mac awake, the launcher tested the same day.

### 8. After the presentation (Vlad, then Claude)
- [ ] Tell Claude how it went (questions asked, what worked, what didn't).
- [ ] Claude writes 007's verify and learn, closes it, and refreshes the board.
