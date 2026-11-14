# Intent: operator cannot delete a user, it times out

| | |
|---|---|
| **Cycle** | 032 |
| **Stage** | Intent |
| **Date** | 2026-11-06 |
| **Owner** | Vlad |
| **Importance** | 4/5 (claude, 2026-11-06): an account cannot be erased at all (operator path, and the shared delete_account is also the person's own path); French users have a right to erasure; 1 reported case, no workaround |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
> issue
> https://app.saxobeat.fr/ops/people/
> can't delete a user.
> for weiersto+0611@gmail.com
>  i follow the steps
> confirm the address by re-entering it
> then app thinks for a long while and eventually times out

## Why now / the pain
- The operator cannot remove an account from the People page: the request hangs, then times out. One case reported (weiersto+0611@gmail.com); no workaround other than switching the account off ("their data is kept").
- The same function (`accounts.delete_account`) also serves the person's own "delete my account" page, so a person could be stuck the same way.

## Goal
Deleting an account from the People page finishes, completely (the person, their data, their private jobs, their e-mails), and says so; the same holds for the person's own deletion.

## Success measure
(Proposed; to be confirmed by the owner.)
1. On a local copy with a realistic candidate (thousands of job views with scores, history, interviews and AI tasks), deleting that account finishes well under the 120 s the web server allows (target: under 10 s, measured; the current time is measured first for comparison).
2. Everything of theirs is gone afterwards and nothing shared is touched: shared jobs, other candidates' views, and approved sources stay (the existing test `test_the_operator_deletes_an_account_...` keeps passing).
3. If the delete cannot finish, nothing is half-deleted (it stays one transaction) and the operator sees an error, not a hang.
4. weiersto+0611@gmail.com is actually deleted on the hosted app (owner checks the People page; the owner performs or approves the hosted step).

## Not doing (this cycle)
- Changing what gets deleted (the rules in `delete_account`), or adding a grace period / undo.
- Making the People page itself faster, unless it turns out to be part of the problem.

## What we already know (facts, with where they came from)
- The operator's delete is `views_accounts.py:122-130` (needs the typed address to match); it calls `accounts.delete_account(user)` (`accounts.py:157-172`): one `transaction.atomic()` that deletes their e-mails, their private jobs, their pending source suggestions, then `candidate.delete()` and `user.delete()`. (Read from the code, 2026-11-06.)
- `candidate.delete()` goes through Django's cascade collector, not a single SQL delete. It cascades from the candidate to `CandidateJob` (one row per job they follow, thousands for a real inbox), and from each of those to `Score`, `StatusChange`, `Interview`, `CheatSheet`, `ApplicationPacket` and `AiTask`; also `Config`, `CandidateCV`, `Company`, `Contact`, `Feedback`, `Impersonation`, `OutgoingEmail`. (`jobs/models.py`, FKs with `on_delete=CASCADE`.) Django must load every one of those rows into memory and then deletes them in batches: on a remote Neon database each round trip is slow, so a large account can take minutes. **Measured on a local copy, 2026-11-06 (`evidence/delete-drill-2026-11-06.md`): an account with 36,271 views (the reported account's size), each with a score and a status change, took 32 s on the lighter account and 40.9 s and 72,945 statements on the realistic one (the first count, 7,700, was an undercount; see `evidence/baseline-2026-11-06.md`) to delete on a local file database, before any network cost. With Neon's latency on top, passing 120 s is expected; the hosted time itself is not measured.**
- No delete signals exist in the app (grep for `pre_delete|post_delete`: none), so nothing else adds to the work.
- The web server runs gunicorn with `--timeout 120`, one worker, 4 threads (`scripts/entrypoint.sh:10`, `render.yaml`): a request that runs over 120 s is killed, which matches "thinks for a long while, then times out". (Render's own proxy may cut earlier; to be verified.)
- The account has 36,271 job views, 0 in progress (owner, People page row, 2026-11-06). It is still listed after the timeout, so the transaction rolled back and nothing was half-deleted; the owner has switched the account off since.
- Not yet known: the hosted delete time itself, and the round-trip latency between Render and Neon (not needed to fix the cause: the number of statements and rows is the lever).

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | Is weiersto+0611@gmail.com still listed on the People page after the timeout, and how many jobs does the row show? | Look at the row and tell me the job count (it is already on the page, no cost). | Still listed (so the delete rolled back); the owner has since switched it off. 36,271 jobs, 0 in progress (owner, 2026-11-06). | answered |
| 2 | Is it urgent for this one person (erasure request), or do we fix the cause first? | Fix the cause first; then delete this person with the fixed code. | Accepted (owner, 2026-11-06). | answered |
| 3 | Is an e-mail confirmation or a "deleting..." state wanted, or just make it fast? | Just make it fast; revisit only if the measured time stays over 10 s. | Accepted (owner, 2026-11-06). | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Deleting is irreversible: the fix is rehearsed on a local copy with a realistic account, and the hosted deletion happens only in the approved plan (PROJECT.md lists writes to production as irreversible).
- A timed-out request may leave the hosted account in an unknown state (rolled back, normally; Postgres rolls back a killed transaction). Check before retrying.
- Do not delete another candidate's data or shared jobs while making it faster (a raw SQL delete skips the cascade rules).

## Gate
- [x] All open questions answered or parked
- [x] Goal and success measure confirmed by the owner (2026-11-06)
