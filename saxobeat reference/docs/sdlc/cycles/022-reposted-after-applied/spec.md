# Spec: reposted after applied

| | |
|---|---|
| **Cycle** | 022 |
| **Stage** | Spec |
| **Intent** | [intent.md](intent.md) |

## Behaviour when finished
When the employer lists again a role the candidate already applied to (a **repost**, as the app already detects it), the candidate sees it in three places:

- **On the repost's page** (36143): a banner says the role was listed before and that they applied to it, with the date, the status of that application (Applied, Interviewing, Rejected, ...) and a link to the earlier job (31673). It replaces the generic "You applied to <employer> before" line for that job, and the warning "recruiters may see both applications" is no longer shown for it, because it is the same role and not a second one.
- **On the repost's inbox row**: a tag "↺ same role, applied <date>" next to the existing badges. The row stays where it is; nothing is hidden by itself.
- **On the earlier job's page** (31673): a line says the employer listed the role again, with the date, a link to the newer posting and whether it is open or closed.

A new filter next to "Hide reposts" leaves out reposts of roles the candidate applied to. There is no new status, no merge and no change to the shared job rows. A candidate who did not apply sees nothing new.

"Applied" means what it already means in `employer_history.py`: the view has an `applied_at`, or its status is Applied, Interviewing, Offer or Accepted. A job that was applied to and then Rejected (by the employer, by the candidate or by the app's silent-month rule) or Withdrawn still counts, because `applied_at` stays. A job that went from Shortlisted straight to Rejected without an application does not.

## Acceptance criteria
Each one must be checkable in `verify.md`.
1. [ ] **Banner on a repost.** For a candidate whose view of another job of the same repost chain is "applied" (as defined above), the repost's page shows a banner with the application's date, its status label and a link to that job. Checked in tests for each of Applied, Interviewing, Offer, Accepted, Rejected, an auto-rejected one, and Withdrawn, and for a repost in the New, Shortlisted and Dismissed states.
2. [ ] **The chain, not just the parent.** The match uses the whole chain (the first posting and every later one). A role listed three times, applied to on the middle posting, shows the banner on the first and the third.
3. [ ] **The warning is about other roles only.** "You applied here on <date>, less than six months ago: the recruiters may see both applications" is not shown when the only recent application is to the same role; it still is when the candidate also applied to a different role of the same employer within six months. The generic list "You applied to <employer> before: ..." no longer repeats the same-role job (it lists the others).
4. [ ] **Inbox row tag.** The repost's row carries the same-role tag (date in the tag, the earlier job's title and status in its tooltip), distinct from the existing employer tag "↺ applied <date>", and the row is still listed in the New inbox.
5. [ ] **Pointer on the earlier job.** On a job the candidate applied to, when a later posting of the chain exists, a line names the newest one, links to it and says open or closed. It does not show when no later posting exists, nor when the candidate has not applied to the job.
6. [ ] **Filter.** A checkbox next to "Hide reposts" (and its chip, and its place in the URL) leaves out the jobs of a chain the candidate applied to elsewhere. A view that is itself in the pipeline (applied or beyond) stays. The filter is off by default.
7. [ ] **Nobody else is affected.** A second candidate who did not apply sees no banner, no tag and no pointer for the same jobs; a candidate who applied sees only their own application (never another candidate's).
8. [ ] **Nothing stored.** No migration, no new column or table, no write when a page is only viewed. `manage.py makemigrations --check` reports no change; the pages read from the existing `repost_of` and `CandidateJob`.
9. [ ] **Speed.** The inbox page runs the same number of queries for 5 rows and for 50 rows (the same-role lookup comes from the one history query per page that already exists); the job page adds at most one query (the pointer).
10. [ ] **French.** Every new string is translated in `locale/fr` and compiled.
11. [ ] **Tests.** New tests cover criteria 1 to 9; the SQLite suite passes with no new failure (the count is stated in `verify.md`).
12. [ ] **The real case, on the host (after the owner deploys).** On app.saxobeat.fr, 36143 shows the banner with a link to 31673 and its status; 31673 shows the pointer to 36143; the row of 36143 in the inbox shows the tag. Read by me in the in-app browser, or by the owner, and said which.
13. [ ] **Phone width.** The banner and the tag read without horizontal scroll at 375 px (one check in the in-app browser).
14. [ ] **The filter at the host's size** (added 2026-11-04 after the host hung on the first design, decisions.md D2). The inbox with `reapplied=hide` answers in under a second on a candidate with about 29,000 views (the local copy of 22 Oct): count and top 30 by score each timed against the same page without the filter, and the query holds no correlated subquery. Checked on the local Postgres copy, then on the host once, after the fix is deployed.

## Design in brief
- **Read the chain, per candidate.** The repost chain already exists on every job: `repost_of` points at the first posting (or is empty on the first itself), so a chain is "all jobs with the same root", the root being `repost_of_id` or the job's own id. The candidate's history book (`employer_history.Book`) already loads the candidate's engaged views once per page; it gains the root of each (one more column in the same query), and a new `same_role(job)` returns the applied entries of the same chain. The three screens and the filter are fed by that.
- **Wording is factual, not certain.** "This role was listed before: you applied to it on <date> (job N, <status>)". The app's repost rule is the same cleaned employer and the same normalised title; an exact guarantee of "same role" is not claimed.
- **The pointer** is one query on the job page, only when the view is an application: the newest job of the chain after this one.
- **The filter** reads the set of chain roots the candidate applied to (a few dozen ids), and leaves out views whose job has one of those roots and is not itself an applied view. It is applied in the inbox query, not in Python.

**Options rejected** (reasons in the intent's questions 1 and 4, no separate decisions file needed):
- A **"Reposted" status**: a new column and state on every screen and report, and it would hide the application that is the real record.
- **Merging the two jobs** (one row, two postings): jobs are shared by every candidate; the merge would change what others see.
- **Hiding the repost by itself**: it can bury a different opening that has the same title.
- **A stored link** between the candidate's two views: it duplicates what the chain already says and can drift (for example after a purge).

## Interfaces and data
- Changed: `jobs/services/employer_history.py` (the root on each entry; `same_role`; the recent-application test can skip the same role), `jobs/views.py` (`job_detail`: the same-role entries and the pointer; the inbox list: the new filter and chip; the warning rule), `jobs/templatetags/jobs_extras.py` and `jobs/templates/jobs/_employer_note.html` (the tag), `jobs/templates/jobs/detail.html` (banner, pointer, the generic line), `jobs/templates/jobs/_filters.html` (the checkbox), `locale/fr/LC_MESSAGES/django.po` and `.mo`.
- New parameter in the inbox URL: `reapplied=hide` (name to settle in the plan).
- No migration, no setting, no environment variable, nothing written to the hosted database; deploy is the usual push, which is the owner's step.

## Constraints
- Reading per candidate only; shared job rows are never edited.
- The existing six-month employer warning stays for other roles; the "applied" tag for other roles of the employer stays as it is.
- Inbox query cost: no query per row.
- Writes to the hosted database: none, so no rehearsal on a copy is needed. Tests run on SQLite with `SAXOBEAT_MAIL=console DATABASE_URL=` (PROJECT.md).

## Risks
- **A wrong chain** (same title at one large employer for different teams) would show "listed before" for a different role. Detection is unchanged and already marks such jobs "reposted ×N"; the wording stays factual and the link lets the person judge. Accepted, as today.
- **A repost the detection misses** (the title changed slightly, or two postings overlap in time: the app needs 7 days between them and the earlier one closed or unlisted for 2) gets no banner. Out of scope; the generic employer line still shows. Note: 31673 and 36143 both say "Published 27 Oct 2026" yet 36143 is detected, so the app's own first-seen dates are what counts.
- **The page's existing sections** (`detail.html` has a section plan per status) must not move; the banner goes in the block of the existing employer history.

## Out of scope
- Changing how reposts are detected, or backfilling reposts.
- A new status, a merge, a stored link, automatic hiding.
- The pipeline board, Insights, the digest e-mails, the AI screening and the follow-up reminders (a follow-up on 31673 keeps running as today).
- Several applications to different roles of one employer (already covered by the employer line and the six-month warning).

## Gate
- [x] Owner approved this spec
