# Intent: reposted after applied

| | |
|---|---|
| **Cycle** | 022 |
| **Stage** | Intent |
| **Date** | 2026-11-04 |
| **Owner** | Vladimir Stoyanov |
| **Importance** | 2/5 (claude, 2026-11-04): one real case from the owner (jobs 31673 and 36143); the local copy of 2026-10-22 has 278 reposts in 30,093 jobs and 0 of 556 candidate views of reposts still New or Shortlisted after the candidate applied to the same role; the existing six-month employer warning already partly covers it |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
> I already applied to a job https://app.saxobeat.fr/job/31673/
> It has since been reposted by the employer https://app.saxobeat.fr/job/36143/
> it feels like there should be a way to treat this specific case. either a dedicated status, or a way to merge it to the other job post

## Why now / the pain
The owner applied to job 31673. The employer later listed the same role again as job 36143. The app stores it as a second, separate job, so the new posting reaches the inbox as an unapplied job (status New) and nothing ties it to the application that already exists. The risk is applying twice, or losing track of which posting the application belongs to. Numbers: see "What we already know"; the case is real but, on the data I can read, rare.

## Goal
When an employer re-lists a role the candidate already applied to, the candidate sees at once that it is the same role and what happened to their application, and the new posting does not pose as an open opportunity.

## Success measure
*Proposed, awaiting the owner's confirmation:* all of these hold, each checked in `verify.md`:
1. On 36143 (and in a test for any repost of a role the candidate applied to, whatever the earlier application's status, including Rejected and auto-rejected), the job page shows a banner "You applied to this role on <date> (job 31673, <status>)" with a link to the earlier job; the generic "recruiters may see both applications" warning is not shown for the same role (it stays for other roles of the same employer).
2. The repost's inbox row carries a tag "applied on <date>" (or equivalent) and stays in the New inbox; nothing is hidden by itself.
3. On 31673, the page points to its newer posting 36143.
4. An "already applied" filter next to "Hide reposts" leaves such reposts out of the list.
5. No new status, no change to the shared job rows, no change to the pipeline or Insights.
6. Showing it does not add a query per row in the inbox (one history lookup per page, as today).

## Not doing (this cycle)
- Changing the repost detection itself (Q2: it already works on this pair) (`services/freshness.py`: 7 to 180 days, same cleaned employer and normalised title). Only what is shown for a detected repost.
- Merging the two jobs in the database (Q1: owner chose a link with a banner) (one job row with two source postings is a different, heavier feature; the catalogue's jobs are shared by all candidates).

## What we already know (facts, with where they came from)
- A repost is already detected and stored: `Job.repost_of` (the first job of the chain), `repost_count`, `repost_key` (hash of cleaned employer and normalised title). The first posting must be 7 to 180 days older and closed or not listed for 2 days. Source: `jobs/services/freshness.py`.
- It is only shown as a badge "reposted ×N" (tooltip "first listed <date>"); the badge has no link to the earlier job and does not say what the candidate did with it. Source: `jobs/templates/jobs/_freshness.html`.
- A "Hide reposts" filter hides every repost for everybody, whether or not the candidate applied. Source: `jobs/views.py:184`.
- A separate warning exists on the job page for New or Shortlisted jobs: "You applied here on <date>, less than six months ago: the recruiters may see both applications." It matches the **employer** only, not the role, and it does not name or link the earlier job. Source: `jobs/services/employer_history.py`, `jobs/templates/jobs/detail.html:31`.
- Status lives on the candidate's own view of a job (`CandidateJob`), not on the job; so each candidate has their own status for 31673 and for 36143. Statuses today: new, shortlisted, applied, interviewing, offer, accepted, rejected, withdrawn, dismissed, expired. Source: `jobs/models.py:27`.
- Reach on the data I can read: the local copy is from 2026-10-22 and has 278 reposts in 30,093 jobs (0.9 %); 556 candidate views of those reposts; in none is the repost still New or Shortlisted after that candidate applied to the same role (1 is a Rejected). Source: read-only count on the local Postgres, 2026-11-04. The local copy does not contain jobs 31673 and 36143 (it stops at 2026-10-22).
- **Verified 2026-11-04 on the host (in-app browser, owner signed in; I only read two pages):** job 36143 (Doctolib, Head of Customer Engineering, Nantes) shows the badges "new" and "reposted ×1" (tooltip "first listed 28 Oct 2026"), Status New. So the pair **is detected as a repost today**. Its page already carries two generic lines: "You applied to Doctolib before: Head of Customer Engineering (x/f/m) (applied, 28 Oct 2026) · Senior Manager Customer Engineering - Paris/Nantes (interviewing, 2 Oct 2026)", with each title a link (one goes to /job/31673/), and "You applied here on 28 Oct 2026, less than six months ago: the recruiters may see both applications." Nothing says that the first of these is the **same role**. Job 31673 (Nantes; Paris) is Applied, with a follow-up due 4 Nov, and shows no sign that a newer posting exists. Both say "Published 27 Oct 2026". Source: read of app.saxobeat.fr/job/36143/ and /job/31673/.
- Consequence: the information is there but not recognised. What is missing is (a) saying plainly that 36143 is the same role as the application on 31673 (with its status), instead of the generic employer line and the "recruiters may see both" warning, which is wrong for a repost of the same role; (b) a mark on the inbox row; (c) a pointer on 31673 to its newer posting.

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | What should the repost of a job you applied to be, in the app: a **new status** (a "Reposted" step in the pipeline), a **merge** of the two jobs, or a **link with a banner** on the new posting that points to your application (and keeps 36143 out of the New inbox)? | A link with a banner: no new status, no merge. The application stays on 31673 and stays the record; 36143 says "You applied to this role on <date> (job 31673, <status>)" with a link. A status would add a pipeline column and a state to every screen and report; a merge changes shared catalogue data for everybody. | Link with a banner (owner, 2026-11-04). No new status, no merge. | answered |
| 2 | Does 36143 already show "reposted ×1" today? | Please look; it decides whether the detection also needs work. | Yes: "reposted ×1", first listed 28 Oct 2026 (checked by Claude on the host, 2026-11-04). The detection needs no work for this pair. | answered |
| 3 | Where else should it show: the inbox row (a tag "applied on <date>"), the pipeline, Insights? | Inbox row tag and the job page; not the pipeline or Insights. | Yes, all three (owner, 2026-11-04): the repost's job page, its inbox row (tag), and the older job's page (a pointer to its newer posting). Not the pipeline or Insights. | answered |
| 4 | Should such a repost leave the New inbox by itself? | No: tag and banner only; an "already applied" filter next to "Hide reposts". Hiding by itself risks hiding a new opening that is really different. | Accepted (owner, 2026-11-04): no automatic hiding; tag and banner, plus an "already applied" filter next to "Hide reposts". | answered |
| 5 | If the earlier application was rejected (or auto-rejected), is the repost a second chance worth showing normally? | Yes, show it normally with the banner "You applied on <date>, it ended Rejected", because a repost after a rejection is a signal worth seeing. | Accepted (owner, 2026-11-04): shown normally, with the banner saying how the earlier application ended. | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- Catalogue jobs are shared by all candidates; any change that edits a job row for one candidate's sake is out. Everything is read per candidate (as `employer_history` does).
- The matching must read the whole repost chain (first posting, later ones), not only the direct parent.
- The app is live with other candidates: changes to the inbox query must not slow it (the existing history book loads once per page).
- Writes to the hosted database (a backfill, a migration) are not needed in this proposal; if a later answer needs one, it is rehearsed on a local copy first.

## Gate
- [x] All open questions answered or parked
- [x] Goal and success measure confirmed by the owner
