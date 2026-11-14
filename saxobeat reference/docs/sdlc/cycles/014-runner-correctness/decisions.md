# Decisions: cycle 014

Decisions with their reasons. Never edited, only superseded by a later line.

| # | Date | Decision | Why | Rejected |
|---|------|----------|-----|----------|
| D1 | 2026-10-29 | W6: the final score is blended by the database in the write, from the row's own `ai_score` | It closes the window with no lock and no extra read: the read of the old score before the write is no longer needed, so the runner reads the same from Neon as before | A `select_for_update` re-read in a transaction (one more read per job, and a lock held while scoring) |
