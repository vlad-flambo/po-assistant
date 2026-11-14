# Spec: deleting an account takes a handful of statements, not thousands

| | |
|---|---|
| **Cycle** | 032 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |

## Behaviour when finished
- Deleting an account from the People page, or from "delete my account", removes the person and everything that is theirs in a few seconds, however many jobs they follow, and the operator sees the same confirmation as today ("Deleted ... and their data (N job views, M private jobs)").
- What is deleted and what is kept does not change: the person, their settings, CV, views of jobs with scores, status history, interviews, cheat sheets, application packets, AI tasks, companies, contacts, feedback, e-mails, impersonation records, their private jobs and their undecided source suggestions go; shared jobs, other people's views, approved sources and operator accounts stay.
- It is still all or nothing: one transaction. If a step fails, nothing is deleted and the operator is told so on the People page (no hang, no 500).

## Acceptance criteria
Each one must be checkable in `verify.md`.
1. [ ] **Speed.** On a local temporary database, an account with 36,271 job views (each with a score and a status change, plus some interviews, cheat sheets, packets and AI tasks) is deleted in under 10 s and under 50 SQL statements (today: 32 s and 7,700 on the lighter version of that account).
2. [ ] **Same result.** After the delete, no row of that person remains in any table, and a second candidate who follows the same shared jobs keeps all their views, scores and data; shared jobs and approved sources are untouched. The existing test `test_the_operator_deletes_an_account_...` passes unchanged, and a new test covers two candidates on the same jobs.
3. [ ] **Private jobs go fast too.** An account that captured many private jobs (`Job.owner`) has them removed with their views, scores and sources by the same bulk path, within the same limits (a drill with 5,000 private jobs).
4. [ ] **Nothing forgotten, now or later.** A test walks every relation that cascades from Candidate and CandidateJob (including hidden ones such as `Impersonation`, which has `related_name="+"`) and fails, naming the model, if the bulk delete does not cover it. A new model added later cannot silently break account deletion or leave rows behind.
5. [ ] **All or nothing.** A test forces a failure in the last step and shows that the person, their views and their scores are all still there afterwards.
6. [ ] **No hang, no 500 for the operator.** If the delete raises, the People page shows an error message ("Nothing was deleted: ...") and the account is unchanged (test with a forced error).
7. [ ] **Both entry points.** The operator's delete and the person's own `/account/delete/` use the same function; both tests pass. The full suite passes (`SAXOBEAT_MAIL=console DATABASE_URL= uv run pytest -q`, from Git Bash).
8. [ ] **Also right on Postgres.** The speed drill and the new tests are run once on a local Postgres (the docker-compose database), since production is Postgres and `DELETE ... WHERE x IN (SELECT ...)` plans differ from SQLite. If Docker is not available here, this is marked not checked, not passed.
9. [ ] **Hosted.** After the owner deploys, weiersto+0611@gmail.com is deleted from the People page and disappears from it; the page answers without a timeout (owner's observation, with the time it took if noticed). This is the only step that touches the hosted database, and the owner performs it.

## Design in brief
Replace the loop Django does by itself (load every job view, then every score, status change... into memory, then delete in small batches) with **one DELETE statement per table, children before parents, in the same transaction**:

1. Tables that hang off the person's job views, each filtered by `job__candidate=<them>` (they have no children of their own, so Django's `.delete()` already turns each into one DELETE): `Score`, `StatusChange`, `ApplicationPacket`, `Interview`, `CheatSheet`, and `AiTask` (both the ones tied to a job and the ones tied to the person).
2. The person's own tables, one DELETE each: `CandidateJob` (with `_raw_delete`, since Django's `.delete()` would load them all to look for children, which is the problem), `Company`, `Contact`, `Feedback`, `OutgoingEmail`, `CandidateCV`, `Config`, `Impersonation`.
3. Their private jobs (`Job.owner`): the same bulk treatment for what hangs off a job (views of it, scores and so on, `JobSource`), then the jobs.
4. Their pending source suggestions and their e-mails by address: as today. Then `candidate.delete()` and `user.delete()` (now they have nothing left to cascade, so these are two cheap statements).
5. The list of tables is written once, in `accounts.py`, next to the function, and the guard test (criterion 4) compares it with Django's own relation graph.

Rejected:
- **Raise the 120 s timeout or the Render limit**: hides the cost, blocks one of the four threads of the only worker for minutes, and the web app is unreachable for others meanwhile. Rejected.
- **Delete in chunks in a loop**: the same 7,700+ statements, only spread out; and the all-or-nothing rule is lost or needs a long transaction anyway. Rejected.
- **A background job / queue ("deleting...")**: a new moving part, an "in between" state to explain, and not needed if the delete is a few statements (owner chose "just make it fast", 2026-11-06). Parked: reopen if criterion 1 cannot be met.
- **Database-level `ON DELETE CASCADE`**: needs a migration on the hosted database and bypasses Django's rules; larger blast radius than the problem. Rejected.
- **Switching the account off only** (exists today): keeps the data, so it does not answer a request for erasure. Kept as it is, not a fix.

## Interfaces and data
- `jobs/accounts.py`: `delete_account` is rewritten; same name, same return (`{"views": n, "private_jobs": m}`), so both callers are unchanged except the error handling in criterion 6.
- `jobs/views_accounts.py`: the operator's "delete" action catches a failure and shows a message (criterion 6).
- Tests in `tests/test_accounts.py` (or a new `tests/test_account_delete.py`); the drill script lives in `docs/sdlc/cycles/032-.../evidence/` and is rerun for `verify.md`.
- No migration, no setting, no new dependency, no change to what the pages show.

## Constraints
- Production is Postgres on Neon (house-stack tier 2); the everyday suite is SQLite, hence criterion 8.
- Rehearse on a local copy only; the one hosted write is the owner's deletion of one account after deploy (criterion 9). Deploying and pushing stay with the owner, in the plan.
- Never print secrets; the drill uses a temporary database file that is removed afterwards.
- A bulk `_raw_delete` skips Django's signals and the collector: there are no delete signals in the app today (grep, 2026-11-06), and the guard test stands in for the collector's knowledge of relations.

## Out of scope
- A grace period or undo for deleted accounts; an e-mail to the person; a "deleting..." state.
- Making the People page itself faster; changes to what is deleted.
- Cleaning up anything else that is slow on the hosted database.

## Gate
- [x] Owner approved this spec (2026-11-06)
