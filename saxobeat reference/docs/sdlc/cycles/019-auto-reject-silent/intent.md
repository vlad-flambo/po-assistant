# Intent: presume an application rejected after a month of silence

| | |
|---|---|
| **Cycle** | 019 |
| **Stage** | Intent (started 2026-11-03; facts gathered; approved 2026-11-03: all 6 questions answered, goal and success measure confirmed) |
| **Date** | 2026-11-03 |
| **Owner** | Vlad |
| **Importance** | 3/5 (claude, 2026-11-03): every candidate who applies is concerned and the list of silent applications only grows, but nothing breaks without it, a manual "no reply" button and a 10-day to-do already exist, and no user feedback asks for it yet |

## The request, in your words
> new feature
> if a job remains on the "applied" stage without an answer for over a month, presume it rejected.
> The status itself can be changed to rejected, but there should be a tag and/or info box showing/explaining that it has been moved automatically because of lack of response.

## Why now / the pain
Many employers never answer. Today such an application stays "Applied" for ever: it sits in the pipeline, keeps showing as "waiting for an answer" in Insights, and is only flagged as quiet after 10 days (a to-do the candidate must clear by hand, or by pressing "no reply" after two follow-ups). No number yet on how many applications are older than a month (to be counted, see Q-measure below).

## Goal
An application that has had no answer for a month is moved to Rejected by the app, and the candidate can always see that the app did it, why, and undo it in one tap.

## Success measure
- A job that stays Applied with no answer for the delay is Rejected by the app, once, with a history entry that says so (checked in tests and on a local copy of the data).
- On the job page and on the pipeline card the candidate sees a tag and an explanation ("moved automatically: no answer after 30 days"), in English and French.
- A job that is not silent (an interview stage, an offer, a move by hand, a focus job) is never touched; a job the candidate puts back is not rejected again by the app the next day.
- The delay is one value in the operator console (default 30, 0 = off).
- Insights keep automatic rejections apart ("no answer"): the rejection count and the delay to rejection do not include them.
- The number of applications older than the delay today on the hosted database, counted read-only before the build, and the number the first sweep moves, match.

## Not doing (this cycle)
- Changing the 10-day "quiet" to-do or the follow-up delays (they stay as they are).
- Auto-moving any other status (shortlisted, interviewing...) or auto-withdrawing.
- Sending an e-mail about it (cycle 009 owns reminders and alerts).
- Counting these jobs in Insights as real rejections (Q5: they are shown apart as "no answer"; the exact wording and places go in the spec).
- A per-candidate delay in Settings (owner, Q2): the delay is one global value in the console.

## What we already know (facts, with where they came from)
| Fact | Source |
|---|---|
| Statuses: new, shortlisted, applied, interviewing, offer, accepted, rejected, withdrawn, dismissed, expired; a change goes through `CandidateJob.set_status`, which writes a `StatusChange` (from, to, when, note, who) | `jobs/models.py:27`, `:342` |
| A job gets `status_changed_at` when it becomes Applied; `applied_at` (a date) and `follow_up_at` (+7 days by default) are set at the same time | `jobs/models.py:342-360`, `jobs/services/followup.py:19` |
| "Followed up" is recorded as a history line from applied to applied: it does not touch `status_changed_at` | `jobs/views.py:625-633` |
| Existing "quiet" rule: Applied, no change for `quiet_days` (default 10, 0 = off) and no interview stage; it is a to-do, not a status change | `jobs/services/followup.py:19-96` |
| Existing manual path: after two follow-ups the job page offers "no reply", which sets Rejected with the note "no reply" | `jobs/views.py:632-637`, `reasons.py:122` |
| The app already changes a status by itself in one place: `matching.expire` sets Expired with the note "posting removed from source", with the status checked inside the UPDATE so a candidate's click in between wins; `_reopen` undoes it | `jobs/services/matching.py:157-171`, `:146` |
| Notes the app writes are translated for display through `reasons.note_text` (a new note needs an entry there and in the locale files) | `jobs/reasons.py:110-130` |
| A job set to Rejected also marks its latest interview stage as rejected (`sync_interview`) | `jobs/models.py:361-364` |
| Insights count Rejected as an answer: rejections, the delay to rejection and "waiting for an answer" all read the history; an automatic rejection at day 30 would count as a rejection after 30 days, which it is not | `jobs/services/pipeline_stats.py:151-185` |
| Precedent for a global operator value: `AiSettings` and `MailSettings` are one-row tables (`get_or_create(pk=1)`) edited in the operator console (`views_ops.py`); a new field or row needs a migration | `jobs/models.py:732`, `:793`, `jobs/views_ops.py:32` |
| A rejected job loses its place as a focus job (only live jobs can be focus jobs) | `jobs/services/focus.py:5` |
| The hosted web service has no scheduler of its own: sources are read from the operator's PC, an external scheduler calls `cron_run`, and the mail digest runs at 8:00 Paris | `render.yaml`, `jobs/views.py:864-875`, `jobs/mail.py:10`. *To be verified:* which of these is the right place for a daily sweep |
| Writes by the runner to a candidate's rows must be conditional (status checked in the UPDATE): the lesson of cycle 014's six overwrite windows | `matching.py:39-41`, cycle 014 |
| On a scratch copy of the 29 Oct dump, read 2026-11-03: 60 Applied jobs (one candidate), none older than 30 days on 29 Oct, **17 as of 3 Nov**, none with interviews, focus or follow-ups; the 17 have no history line (put in Applied by migration or import on 29 Sep to 2 Oct) | `evidence/applied_counts.md` |
| Neon's read and storage allowances are tight; a sweep must be one cheap query per candidate | cycles 001 and 002 |

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| Q1 | When does the month start, and what stops the clock? | From the day the job became Applied (`status_changed_at`); a follow-up we sent is not an answer, so it does not reset it; a job with an interview stage, or any move by the candidate, is not silent and is left alone | Yes, as recommended (owner, 2026-11-03) | answered |
| Q2 | Is the delay fixed at 30 days or a setting? | A per-candidate setting next to "quiet days", default 30, 0 switches it off | **Changed by the owner, 2026-11-03: one global value for everybody, set in the operator console, not a candidate setting.** Default 30 days, 0 switches the whole feature off | answered |
| Q3 | What exactly does the candidate see? | Status Rejected, a history entry "no answer after 30 days (automatic)", a small tag "Auto-rejected" on the pipeline card and job page, and an info box on the job page that says why, with a "Put back to Applied" button | Accepted as recommended (owner, 2026-11-03). Putting it back sets a new `status_changed_at`, so the clock starts again and the app does not reject it the next day; moving it any other way also removes the tag | answered |
| Q4 | What happens to the applications already older than the delay on the day it goes live? | The first sweep treats them like any other, with the same tag and one-tap undo, and the pipeline shows a one-time notice with the count | Accepted as recommended (owner, 2026-11-03) | answered |
| Q5 | Do automatic rejections count as rejections in Insights? | No: show them apart as "no answer", so the rejection rate and the delay to rejection are not distorted | Accepted as recommended (owner, 2026-11-03) | answered |
| Q6 | Are focus jobs exempt, and where does the sweep run (PC runner, scheduler call, or when the candidate opens the app)? | Focus jobs exempt (the candidate gives them full attention); sweep decided in the plan from the facts above | Accepted as recommended (owner, 2026-11-03): focus jobs exempt; where the sweep runs is parked to the plan | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- A wrong rejection hides a live application: it must be visible, reversible in one tap, and never repeated on a job the candidate put back.
- Race with the candidate (cycle 014): the status is checked inside the UPDATE.
- A new history note and tag text need French translations (the app is bilingual).
- Product docs to update after the build: `docs/PRD_competitive_features.md` §follow-up (it says the app only suggests "no reply"), and the Insights wording.

## Gate
- [x] All open questions answered or parked
- [x] Goal and success measure confirmed by the owner (2026-11-03: "Confirm, write the spec")
