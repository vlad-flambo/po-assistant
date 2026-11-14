# Decisions: reposted after applied

One entry per decision, newest last. Do not edit old entries: add a new one that supersedes.

## D1. On a phone card, "already applied" is the first of the two chips
- **Date:** 2026-11-04
- **Context:** Slice 8 (the look at 375 px on a throwaway database) showed that the phone inbox card keeps only two chips and hides the whole detail line (`.jc-detail`, display none under 900 px), where the badges "new", "reposted ×1" and the same-role tag live. The spec's criterion 4 (a tag on the inbox row) was therefore invisible on a phone, which is the main way the candidate interface is used (PRD_mobile, two-chip rule).
- **Options considered:** (a) leave the tag on the desktop row only; (b) show the full same-role tag as a chip ("↺ same role, applied 27 Oct", long for a card); (c) a short chip "↺ already applied", placed first.
- **Decision:** (c), in `card_chips`: the chip is `chip warn` with the text "↺ already applied" (French "↺ déjà postulé"), before the AI's verdict. The date, status and link stay on the job page and in the desktop tag's tooltip.
- **Why:** it is the one thing a person needs to know before opening a repost of a role they applied to; the rule of two chips still holds (a third becomes "+n").
- **Consequences:** criterion 4 now reads "desktop row tag, phone card chip"; `docs/PRD_mobile.md` (the list of chips on a card) gets the new first chip at the Learn stage. Two tests pin the chip and the two-chip rule. The owner approved the spec before this was found; it is a small addition in the spirit of the goal, and is reported to the owner in the build summary.

## D2. The filter reads the candidate's applications first, then cuts with two `IN` lists (supersedes the last design bullet of spec.md)
- **Date:** 2026-11-04
- **Context:** Pushed as `0455313`, the filter `reapplied=hide` used one correlated `EXISTS` per row. On the host two requests to it did not answer and the site then went down for some minutes (probably, see evidence/host_read_2026-11-04.md). On the local copy (29,000 views per candidate) the count took more than 20 s; the same inbox without the filter takes 0.011 s.
- **Options considered:** (a) keep the `EXISTS` and add an index on an expression; (b) read the candidate's applications first (a few dozen rows, the same rules as the book) and exclude with two `IN` lists on indexed columns (`job_id`, `repost_of_id`); (c) remove the filter.
- **Decision:** (b). The set of roots and of applied job ids is read once per request that asks for the filter; the list is then cut with `IN`.
- **Why:** an expression index is a migration on the shared table for one filter; (c) loses a part of the owner's feature without need; (b) measured 0.010 to 0.039 s on the same data.
- **Consequences:** `without_reposts_of_applied(jobs, candidate)` takes the candidate (`f["candidate"]` from `_read_filters`); one more small query when the filter is on, none otherwise; a test pins "no EXISTS, no COALESCE". New acceptance criterion 14 (spec): the filter answers in under a second on a candidate with about 29,000 views. **Process lesson** (for learn.md): any query that runs over a candidate's whole list of views must be timed on the local copy (57,643 views), not only tested on a few rows; the slice list had a query-count check but no timing check.
