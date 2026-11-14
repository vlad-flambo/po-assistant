# Spec: presume an application rejected after a month of silence

| | |
|---|---|
| **Cycle** | 019 |
| **Stage** | Spec (approved 2026-11-03) |
| **Intent** | [intent.md](intent.md) |

## Behaviour when finished
- A job that has been **Applied** for longer than the delay without any answer is moved to **Rejected** by the app. "Without any answer" means: no interview stage, no move by the candidate since it became Applied (a follow-up the candidate sent is not an answer and does not reset the month), and not a focus job.
- The delay is **one global number of days in the operator console** (default 30, 0 switches the feature off). Candidates cannot change it.
- The candidate can always see that the app did it. The job carries an **"Auto-rejected" tag** on the pipeline card and the job page. The job page shows an **info box** saying the app moved it on a date because there was no answer for N days, with a **"Put back to Applied"** button. The status history shows the line "no answer after N days (automatic)".
- Putting it back restarts the month, so the job is not rejected again the next day. Any other change of status also removes the tag.
- **Insights** keep these jobs apart: they appear as "no answer", and are not counted as rejections or in the delay to a rejection.
- The first time the sweep runs it also moves the applications already older than the delay (same tag, same undo); the pipeline page shows a notice with the count.

## Acceptance criteria
Each one must be checkable in `verify.md`.

**The rule**
1. [ ] With delay N > 0, a job that is Applied, whose `status_changed_at` is more than N days old, with no interview stage and not a focus job, is set to Rejected by the sweep: one `StatusChange` (applied to rejected, note "auto: no answer after N days"), `auto_rejected_at` set, `follow_up_at` cleared. Test with a job at N-1, N and N+1 days.
2. [ ] A job is left alone when it is: newer than N days; in any status other than Applied; Applied with an interview stage; a focus job. A "followed up" entry does not reset the clock (a job with three follow-ups and an old `status_changed_at` is still moved).
3. [ ] The status is checked inside the UPDATE (the cycle 014 rule): when a candidate moves the job between the sweep's read and its write (`_between_read_and_write` test hook), the job is left as the candidate set it and has no history line from the sweep.
4. [ ] A second sweep right after the first changes 0 rows and writes 0 history lines.
5. [ ] Delay 0 moves nothing; tags already on jobs stay.

**The console**
6. [ ] The operator console has a field for the delay: whole number of days, 0 to 365, default 30, saved on a one-row table (migration; new row created on first read like `AiSettings.get()`). A non-number or out-of-range value is refused with a message and nothing is saved. A non-operator gets a refusal on that page.
7. [ ] Changing the delay in the console changes the next sweep (test: 30 then 45 on the same job).

**What the candidate sees**
8. [ ] The job page of an auto-rejected job shows the tag and the info box with the date and N days, in English and in French, with the "Put back to Applied" button. A job rejected by hand (or by the existing "no reply" button) shows neither.
9. [ ] "Put back to Applied" sets the status to Applied, clears the tag, sets a new `status_changed_at` (the month restarts), writes a history line, keeps `applied_at`, sets the follow-up date as when applying. The next sweep leaves it alone until a new delay has passed.
10. [ ] Any other change of status (pipeline drag, status menu, undo of a history entry, interview marked as rejected) clears `auto_rejected_at`.
11. [ ] The pipeline card of an auto-rejected job shows the tag, in English and French, without reading the status history (the tag comes from the field).
12. [ ] The history list on the job page shows the automatic line translated, with the number of days.
13. [ ] When a sweep has moved at least one of a candidate's jobs in the last 7 days, the pipeline page shows a notice with the count and a link to those jobs; it disappears by itself after 7 days (no new column for "seen"; see Design, option rejected 3).

**Insights**
14. [ ] A job whose current status is Rejected with `auto_rejected_at` set is not counted in the rejected total, the delay to a rejection, or the "rejected" end of the diagram; it is counted as "no answer" and shown with that name. A job put back or moved on stops being counted as "no answer". "Still waiting" is unchanged for jobs that are still Applied.

**Safety and cost**
15. [ ] The sweep can be run as a dry run that prints, per candidate, how many jobs it would move and writes nothing. On a local copy of real data, the dry-run count equals the number the real sweep then moves, and equals an independent SQL count of the same rule.
16. [ ] The sweep costs one read query (candidates' Applied rows past the delay, no job texts) and one conditional UPDATE per chunk; measured on a local copy and stated in `verify.md`. No job text is read.
17. [ ] The migration applies on SQLite and on Postgres; the full test suite passes on both.
18. [ ] `manage.py i18n missing` reports no untranslated string for the new texts (tag, info box, button, history line, console labels, notice).

## Design in brief
- **A flag on the candidate's view, `CandidateJob.auto_rejected_at` (nullable datetime).** Set by the sweep together with the status; cleared by `set_status` for any other change and by `remove_change`. It makes the tag, the pipeline card, the notice and Insights cheap and exact, with no reads of the history. The history line (note "auto: no answer after N days", translated by `reasons.note_text` with a pattern like the "bulk: score below" one) is the record and carries N.
- **A one-row settings model** (new, e.g. `PipelineSettings.auto_reject_days`, `get()` with `get_or_create(pk=1)` like `AiSettings` and `MailSettings`) edited on a small operator-console form that follows `ai_settings` in `views_ops.py`.
- **The sweep** is a function in a service (`services/followup.py` or a new `services/auto_reject.py`) and a management command with `--dry-run`. It is written like `matching.expire`: read the ids, then `UPDATE ... WHERE id IN (...) AND status = 'applied' AND status_changed_at < cutoff`, then write the history lines for the rows that update changed. The trigger (PC runner pass, the scheduler call to `cron_run`, or the web app when a candidate opens it) is chosen in the plan; the spec requires only that it needs no new infrastructure and runs at least daily.
- **Insights:** `pipeline_stats.standing_of` and the `ends` bucket read the flag; `to_rejection` skips an automatic rejection. A "no answer" row is added where rejections are listed.
- **Options rejected**
  1. A per-candidate delay (owner, Q2): the delay is global.
  2. Detecting the automatic rejection from the history note only: needs a history read for every pipeline card and every Insights count (the Neon read budget, cycles 001 and 002).
  3. A "seen" column for the one-time notice: another migration for a short-lived banner; a 7-day banner is simpler. **This differs from "one-time notice" in the intent (Q4): the owner approves or changes it with this spec.**
  4. A new status "no answer": the owner asked for Rejected plus a tag; a new status would touch every status list, the pipeline columns and the Insights.
  5. Resetting the clock on a follow-up: a message we sent is not an answer (Q1).

## Interfaces and data
- Migration: `CandidateJob.auto_rejected_at` (nullable) and the one-row settings model; no data migration. On the hosted database it is a metadata-only column add plus one tiny table; applied by the entrypoint on deploy, after a Neon snapshot taken by the owner.
- Console: one new field on one page. Command: `manage.py auto_reject [--dry-run]`.
- Texts: tag, info box, button, history line, notice, console label (English and French, `locale/`, `.po` and `.mo` via `manage.py i18n extract|compile`).
- Docs touched in Learn: `docs/PRD_competitive_features.md` (follow-up section says the app only suggests "no reply"), Insights wording, DEPLOY.md if the sweep is added to the runner.

## Constraints
- **Neon:** the sweep and the new column must not raise reads or storage noticeably (criterion 16); no job text is read.
- **No hosted write by me:** I never run the sweep, the migration or a console change on the hosted database; the owner does, after a snapshot. The first real sweep on the hosted database is preceded by the dry-run count (criterion 15).
- **Reversible:** one tap undoes it, and the feature switches off with 0 in the console.
- **Postgres rehearsal:** the migration and the sweep are rehearsed on a scratch Postgres copy before the owner applies them (SQLite does not enforce lengths and hides some bugs, cycle 013).
- **Local runs:** `SAXOBEAT_MAIL` is set explicitly in my local runs (the PC's `.env` has a live mail key).

## Out of scope
- A per-candidate delay, a setting in Settings, a new status.
- E-mail or push about an auto-rejection (cycle 009).
- Changing the 10-day quiet to-do, the follow-up delays or the "no reply" button.
- Auto-moving any status other than Applied.
- Counting the delay from the last follow-up or any other activity.

## Gate
- [x] Owner approved this spec (2026-11-03: "Approve, write the plan"; includes the 7-day banner in place of a one-time notice)
