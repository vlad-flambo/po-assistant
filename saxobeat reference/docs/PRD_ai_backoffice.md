# PRD — Instant results now, AI within 24 hours: onboarding, the AI hand-off and the operator console

| | |
|---|---|
| **Status** | **Built, phases A0 to A6 (23 October 2026)**: see "What was built" under §12 for how it differs from the plan. Not yet run on the hosted app or with a real agent. **All decisions in §13 are settled (23 October 2026):** the operator accepted every recommendation, with three changes: D4 (a beta note on the 24 h promise), D9 (cap of 5, and nothing is sent twice) and D13 (company profiles are generic, with nothing specific to a candidate). |
| **Revisions (23 Oct)** | (1) The operator alone runs the AI back office for every candidate in the alpha; work is grouped into **packs** (one file per pack, many candidates); each file carries the full agent instructions, so no skill or setup is needed on the agent side; job screening is selected by global settings (top N % by score). (2) Onboarding gets a short **conversation** (roles, turn-ons, turn-offs) whose answers feed the onboarding pack, which writes each candidate's **screening brief** and **balanced, calibrated keyword weights** (score 50 should mean the same for everyone). Application help becomes **bring your own AI** on the candidate side. A **local runner** fetches the pack files and imports the results automatically. Later work is kept in a **register** (§18). |
| **Date** | 23 October 2026 |
| **Author** | Vladimir (product), written with Claude |
| **Builds on** | [PRD_multi_user.md](PRD_multi_user.md) (candidates, operator space; §3 had put "AI reviews per candidate" out of scope: this PRD brings them in), [PRD_competitive_features.md](PRD_competitive_features.md) (the agent files for application answers, cheat sheets, follow-ups, company reports), [PRD_mobile.md](PRD_mobile.md) (the phone-first candidate interface the new screens must fit), [DEPLOY.md](DEPLOY.md) (the PC runner that writes to the hosted database) |
| **Scope** | (1) What a candidate gets **instantly** (rules, no AI) and how the **AI layer** is promised and delivered (within 24 h); (2) a smoother **onboarding** with a short conversation; (3) one **hand-off** format out to the operator's agents and one **import** back, moved by a **local runner**; (4) a separate **operator console**; (5) **bring-your-own-AI** application help for candidates. |
| **In one line** | Everything a rule can compute is shown at once; everything that needs judgement is queued, handed to the operator's agents as a file, and lands within 24 hours, with the candidate told so at every step. |

---

## Outstanding work (moved to SDLC cycles on 2026-10-29)

What this PRD still asks for is now tracked as cycles in `docs/sdlc/` ([the audit](sdlc/cycles/006-stale-docs/evidence/prd_audit_2026-10-29.md)). This PRD stays the product-level reference; the cycles carry the work.

- Run on the hosted app with a real agent: [004](sdlc/cycles/004-hosted-checks/intent.md)
- Bring-your-own-AI copy and share on real devices: [005](sdlc/cycles/005-real-devices/intent.md)
- Keyword chips, per-candidate AI weight, the tab dot: [011](sdlc/cycles/011-settings-polish/intent.md)
- R1 calibration loop, R2 brief drift: [008](sdlc/cycles/008-calibration-loop/intent.md)
- R4 notifications (push): [009](sdlc/cycles/009-reminders-alerts/intent.md)
- §16 success measures: [007](sdlc/cycles/007-success-measures/intent.md)
- R3 scheduled agent, R5 company freshness, R6 keeping what was sent: [the backlog](sdlc/backlog.md)

---

## 1. Problem

Saxobeat now has friends on the hosted app, but the AI side was built for one person: the operator reviewing his own jobs.

**What happens today (read in the code on 23 October 2026)**

| Area | Today | What goes wrong for 10–30 people |
|---|---|---|
| **AI job reviews** | Operator-only page `/review/` exports a JSON batch (`saxobeat.review.v1`), a Claude session with the `saxobeat-review` skill writes `saxobeat.scores.v2`, the operator uploads or pastes it back (`jobs/services/handoff.py`). | The page works on `request.candidate`, i.e. **the operator's own jobs only**. A friend's jobs can only be reviewed from the command line (`export_review --candidate`). Nothing tells the friend a review is coming or when. The review instructions are the same for everyone: they know the CV, not what the person wants. |
| **Other agent files** | Five more hand-offs, all candidate do-it-yourself: screening answers, cheat sheet, follow-up message (per job), company report (per company), each a Markdown download (`jobs/services/briefing.py`). The result is pasted back by hand into a different place each time, or not at all. | The buttons are there but nothing explains what to do with the file, and a download is the wrong move on a phone. |
| **Re-reviews** | A "rerun round" exists for job reviews only (`Config.rerun_cutoff`). | Changing any other instruction has no way to redo past outputs. |
| **Import** | Paste or upload on `/review/`; the command line imports the newest file in `data/`. No preview, no batch identity: importing the same file twice silently "replaces" every review. | With several people and several kinds of output, one wrong file can overwrite the wrong things with no way to see it first. |
| **Onboarding** | 3 steps (`jobs/views_cv.py`): upload CV; then the CV health check **and** a draft profile to edit as a 200-px text box plus a keyword list typed as `term: weight`; then cities and roles. It ends with "jobs get their scores in a minute or two" and drops the person in the inbox. | Step 2 asks a newcomer to tune a scoring engine before they have seen a single job. Nobody is asked what they actually want or refuse. AI is never mentioned. |
| **Scores across people** | Keyword weights come from rules on each CV, then from whatever the candidate types. | A score of 50 can mean "worth a look" for one person and "noise" for another: a CV with many matching words inflates every score. The job screening line (top N %, minimum 50) is only fair if 50 means roughly the same for everyone. |
| **Operator pages** | An "Operator" dropdown in the candidate top bar (desktop only) and a section on *More*; operator crumbs inside candidate pages: "Refresh now", failing-source banners, platform tags on cards, the AI weight in Settings. | The operator never sees the app the way friends do, and the back office has no home of its own: no queue, no due dates, no overview across people. |

## 2. Goals

1. **Instant value, every time.** Every candidate action that can be answered by rules is answered in seconds: CV health (ATS) score, keyword signals, target-role fit, job score and breakdown.
2. **An honest AI promise.** Wherever an AI result will follow, the candidate sees what it will be and when: *"In-depth AI analysis · ready within 24 h"*. When it lands, they are told. If it is late or paused, they are told that too.
3. **One hand-off, one import.** The operator selects candidates and exports in one go: one file per **pack** (onboarding, job screening, company research), each covering every selected candidate. One results format comes back, validated and previewed before anything is written.
4. **Any agent, no setup.** Each exported file is self-contained: the full agent brief, the instructions per task kind, the output format and its checks. Claude, another assistant, a chat window or a coding agent can all process it; nothing has to be installed or ported.
5. **A personal job screening for each candidate,** written once by the onboarding agent from their CV and their own answers, and a score scale that means the same thing for everyone.
6. **Files move by themselves.** A local runner on the operator's PC writes the due pack files into a folder and imports the results it finds there. The operator only runs the agents.
7. **A single operator console** (`/ops/`) where the operator alone pilots the back office on behalf of every candidate. The operator's own candidate space becomes exactly what friends see.
8. **Onboarding in 2 steps and under 4 minutes** to a sorted inbox: the instant CV results, then a short conversation about what they want.
9. **Application help with your own AI, in two taps,** explained right where the button is.
10. **The app still never calls a model.** No API key, no paid credits. If the operator stops, nothing breaks; candidates keep every instant result.

## 3. Out of scope

- The app calling an LLM API, or candidates bringing an API key.
- Running the agent automatically. The runner moves files (§8.8); starting the agent on them stays a manual step (register R3).
- E-mail or push notifications to candidates. In-app only (badge, "ready" strip). *E-mail is brought in on 28 October 2026 by [PRD_users_and_emails.md](PRD_users_and_emails.md), which also lets the operator view and act as a candidate (changing §9's rule).*
- Paid tiers, quotas tied to payment.
- The calibration **feedback loop** (adjusting weights from outcomes over time): register R1. This PRD only calibrates once, at onboarding.
- Changes to scraping, sources or the score formula itself (except the new instant *target-role fit*, §6.2).

## 4. Users

| Who | What they need from this PRD |
|---|---|
| **Candidate** (friend, early user) | Something useful within a minute of signing up; to say in their own words what they want and refuse; to know which results are instant and which are coming from AI, and when; to prepare an application with the AI assistant they already use, without having to learn anything. |
| **Operator** (Vladimir) | During the alpha, the **only** person who runs AI, on behalf of every candidate. Pack files waiting in a folder when he sits down; results imported as soon as an agent writes them; one place that says what is due for whom and by when; global settings for how much is sent; confidence that a result never lands on the wrong person and that scores are comparable across people. Target: **under 10 minutes of hands-on time per day** for 30 candidates. |

## 5. Principles

1. **Two speeds, always labelled.** *Instant* = computed by rules in the app, now. *AI* = prepared by an AI agent, run by the operator, within 24 h. Every result says which it is; an AI result never silently replaces an instant one: both stay visible.
2. **The promise is a date, not a vibe.** Each AI request has a due time (requested + 24 h). The candidate sees "ready by Fri 10:30" as a *latest* time, with the beta note that AI is not instant; the operator sees the same clock.
3. **Instant first, AI second, never AI only.** No screen waits for AI to be useful.
4. **Scoring changes are visible and undoable.** When the AI changes how a candidate's jobs are scored (keywords, target roles), the operator sees the effect before it is applied, and the candidate is told what changed and can undo it with one tap.
5. **One format, self-contained.** Each exported file carries the full agent brief, the instructions per kind, the output schema and the versions, so any agent on any platform can process it with no skill installed, and the importer can check what comes back.
6. **No result without a home.** Every task belongs to exactly one candidate and one object (their profile, a job, a company); the importer refuses anything else.
7. **Minimum personal data out.** Exported files carry what the task needs and no more: e-mail addresses and phone numbers are removed from CV text, candidates appear by a reference, not their name or login.
8. **The operator eats the same food.** The operator's candidate space shows no machinery; the machinery lives in the console.
9. **Ask, don't make people configure.** Candidates answer plain questions with taps; the app and the agent turn the answers into weights and filters.

## 6. The two speeds, feature by feature

### 6.1 What is instant and what follows

| Moment | Instant (rules, seconds) | AI (operator's agent, within 24 h) | How it starts |
|---|---|---|---|
| **CV uploaded and conversation answered** (onboarding, or later from *My CV* / *What I'm looking for*) | **CV health (ATS) score /100** with each check explained (`jobs/cvhealth.py`); detected titles, skills, languages, years of experience; **keyword signals** (`jobs/cvprofile.py`); **target-role fit** (§6.2); the answers that map to a rule applied at once (§7.2). | **In-depth CV analysis**: strengths, weaknesses an ATS rule cannot see, section-by-section rewrite suggestions, a positioning line. **Tuned search**: balanced and calibrated keyword weights, exclusions, target titles. **Personal job screening brief** used for every later job review (§8.4). | Automatically, once per CV version or change of answers (onboarding pack). |
| **New jobs matched** (daily) | Score, breakdown, missing keywords, signals (salary, remote, English), freshness, employer history. | **Job review** following the candidate's screening brief: score, apply / don't apply, two-sentence analysis, requirement scorecard, CV tweaks. | Automatically: the jobs that pass the job screening settings (top N % by score, §8.3). |
| **Interview coming** | The cheat sheet skeleton built from the posting and profile. | **Company profile** (one generic profile per company, common to every candidate; never researched twice). | On request, and automatically on the first interview at a company (D7). |
| **Preparing an application, interview or follow-up** | CV ↔ job match; built-in follow-up message (FR/EN); cheat sheet skeleton. | **Bring your own AI** (§6.4): application answers, cheat sheet, follow-up, prepared in the candidate's own assistant. | The candidate, whenever they want. Not part of the operator's back office. |

### 6.2 New instant result: target-role fit

The multi-user PRD defined the ATS score as "CV health first, then match to a target role". The second half exists only per job today (`cv_match`). New: for each of the candidate's target roles, take the catalogue's recent postings for that role (title match, last 90 days, Paris/IdF), find the requirement words that recur in them, and show how many the CV covers: *"Head of Customer Success: your CV covers 14 of the 20 words these postings use most. Missing: churn, NRR, Gainsight…"*. Rules only, computed on upload and when target roles change; cached per CV version.

### 6.3 How a pending AI result looks (one component, everywhere)

```
┌───────────────────────────────────────────────┐
│ ✦ In-depth AI analysis                        │
│ Ready by Fri 24 Oct, 10:30                    │
│ Strengths, gaps an ATS can't see, and         │
│ rewrite suggestions for each section.         │
└───────────────────────────────────────────────┘
```

| State | English | French |
|---|---|---|
| Queued / with the agent | ✦ In-depth AI analysis · ready by Fri 10:30 | ✦ Analyse IA approfondie · prête vendredi 10 h 30 |
| Ready (unseen) | ✦ Your AI analysis is ready · New | ✦ Votre analyse IA est prête · Nouveau |
| Late (past due) | ✦ Taking longer than planned: today, we're on it. | ✦ Un peu plus long que prévu : aujourd'hui, c'est en cours. |
| Paused by the operator | ✦ AI analyses are paused until Mon 27 Oct. Your instant results are complete. | ✦ Analyses IA en pause jusqu'au lundi 27 oct. Vos résultats instantanés sont complets. |
| Candidate opted out | (component hidden) | (component hidden) |

**Beta note (D4).** The component always carries one standing line, until the beta ends: *"During the beta, AI is not instant: you'll get it within 24 h at the latest. Check back soon."* / *"Pendant la bêta, l'IA n'est pas instantanée : vous la recevrez sous 24 h au plus tard. Revenez bientôt."* The same line sits under "Done" at the end of onboarding and in the first-run tour. "Ready by …" is therefore a latest time, not an estimate; most results land earlier.

When an AI result lands: a dot on the relevant tab (Inbox for job reviews, More → My CV for the CV analysis), and a one-line "ready" strip on top of the inbox, dismissible. The instant result stays on screen next to it, labelled *Instant*. When the tuned search lands: *"Your search was tuned: 6 keywords added, 2 removed, 3 exclusions. [See what changed] [Undo]"*.

### 6.4 Bring your own AI: application help

Application answers, cheat sheets and follow-ups are prepared by the candidate in **their own AI assistant** (ChatGPT, Claude, Gemini, Copilot, Le Chat…). They are personal, urgent and iterative (the candidate wants to edit and ask again), so a 24-hour queue is the wrong tool. The app's job is to hand over a perfect prompt in one tap, and to say how, right there.

On the job page, in the *Prepare* section, one row:

```
Prepare with your AI   ⓘ
[ Application answers ]  [ Cheat sheet ]  [ Follow-up ]
```

- **One tap = the prompt is ready.** On a laptop it is copied to the clipboard (*"Copied. Paste it into your AI."*). On a phone it opens the share sheet, so it goes straight into the ChatGPT, Claude or Gemini app; "Copy" is offered there too. "Download as a file" stays as a small link for long prompts or assistants that prefer attachments. The prompt is what `briefing.py` builds today: instructions, the posting, the profile, the app's fit analysis, the candidate's notes.
- **Application answers** first opens a box: *"Paste the employer's questions (optional)"*; they are included in the prompt.
- **The tutorial is where the button is.** Hover on a laptop, tap ⓘ on a phone, and the first time automatically:
  > **① Tap a button** — your job, your profile and our instructions are copied.
  > **② Paste into your AI** — ChatGPT, Claude, Gemini or any other.
  > **③ Use the answer** — paste it into the application. For the cheat sheet, paste it back here to keep it.
  
  Three lines, one picture each, French and English. Nothing else to read.
- **Paste back where it is worth keeping:** the cheat sheet has a "Paste the AI's version" box (with keep-mine / replace if they had edited it); answers and follow-ups are used directly, with an optional "Save to my notes".
- No AI consent is needed: the candidate sends their own data to their own assistant. A one-line note says so in the tutorial's footer.

## 7. Onboarding, reworked

**Today:** 3 steps, a form to tune the score in the middle, nobody asks what the person wants, no reward until the inbox.
**Target:** 2 steps: the instant CV results, then a short conversation. The inbox is sorted with both when they land, and the AI follows within 24 h.

### 7.1 The two steps

1. **Your CV.** Upload (PDF, DOCX, Markdown; from a phone's files too) or paste text, or skip. On the same step, one explicit tick: *"Let an AI agent run by Saxobeat analyse my CV and jobs (you can turn this off any time)"* (D10).
   → **Instant results screen** (not a form):
   - the **ATS score** as a big number with its level and the **3 fixes that would gain the most points** (the rest folded);
   - **keyword signals** as chips grouped strong / medium / light, each removable with a tap (no `term: weight` typing);
   - detected titles, years of experience, languages, as chips;
   - the **AI card**: *In-depth AI analysis · ready by …* (or nothing if they did not tick).
2. **What you're looking for: a short conversation** (§7.2).
   → **Done.** *"Sorting the jobs for you"* with a live count, then the inbox. The first page of matches is computed first, the rest in the background. If they ticked AI: *"Within 24 h, an AI agent tunes your search and sets up your personal job screening."*

**What moves out of onboarding:** the full profile text and the keyword weights. They live in Settings (*Profile and keywords*) as chips with a weight control. The conversation can be reopened any time from Settings (*What I'm looking for*); changing an answer re-queues the onboarding pack.

### 7.2 The conversation

A chat-style screen, **scripted, not AI**: the app asks, the candidate answers with chips or a few words. Five questions, about a minute, phone-first, each skippable, with "back" always available.

| # | The app asks | Answers | Applied instantly (rules) | Sent to the onboarding agent |
|---|---|---|---|---|
| 1 | Which roles are you after? | Chips prefilled from the CV titles and target-role suggestions; add your own. | Target roles (keywords at weight 4, as today), target-role fit shown under each. | Yes |
| 2 | What gets you excited about a job? (*turn-ons*) | Chips: remote or hybrid · international team · scale-up · large company · leading a team · customer-facing · product / tech · fintech / banking · mission-driven · better pay; plus free text. | Light boosts where a word list exists (an industry, "international"). | Yes, all of it, including free text |
| 3 | What makes you skip a job straight away? (*turn-offs*) | Chips: 5 days on site · consulting / ESN · lots of travel · sales targets · junior scope · early-stage startup · an industry I avoid; plus free text. | Where a rule exists: exclusion words (consulting, ESN…), hide junior roles, remote filter from the work-mode signal (F10), excluded industries as words. | Yes |
| 4 | Anything non-negotiable? | Minimum salary, contract (permanent only / freelance OK), languages you work in. | Salary and language filters (signals F10, posting language). | Yes |
| 5 | Where? | Cities as chips (Paris preselected), "remote in France too". | City filters, breadth. | Yes |

The last bubble recaps the answers in one block with "Change" links, then *Done*. Every new string exists in French and English.

**Success:** median time from "join" to a sorted inbox under 4 minutes; at least 80 % of people who start the CV step finish onboarding; nobody types a weight; at least 70 % answer the turn-ons and turn-offs questions.

## 8. The AI hand-off, reworked

During the alpha **the operator does all the back-office AI work, for every candidate**. Candidates never handle a pack file: they get instant results, and AI results appear in their space. (Application help is the exception by design: the candidate's own AI, §6.4.)

### 8.1 Tasks

Every piece of back-office AI work is an **AI task**: one candidate (or a company shared by several), one kind, one subject, one due time.

| Kind | Pack | Subject | Created | Output lands in |
|---|---|---|---|---|
| `profile_analysis` | Onboarding | candidate (per CV version and set of answers) | after the conversation (or a later change), if AI consent | *AI analysis* block on *My CV*; tuned keywords, exclusions and target roles (§8.4, applied after the operator's check, undoable); the candidate's **screening brief** |
| `job_review` | Job screening | candidate × job | when a job passes the job screening settings (§8.3) | `Score` AI fields, as today |
| `company_report` | Company research | company (one generic profile, shared by every candidate; nothing in it is specific to a candidate) | on request, or first interview at that company (D7), **only if the company has no profile yet** (D9) | the shared company profile, shown on every candidate's company page next to their own notes |

**Lifecycle:** `queued` → `exported` (in export *E*) → `done` | `failed` (output refused: back to `queued`) | `cancelled` (no longer needed: job dismissed or expired before export, CV replaced, candidate opted out or deleted). One open task per kind and subject: asking twice does nothing. A task exported more than 24 h ago with no result is offered again in the next export.

**Order of work:** a candidate's job screening uses their screening brief once it exists. Until then, their jobs are reviewed with the generic instructions plus their conversation answers, so nobody waits.

**Instruction versions** replace the rerun round: each kind has an instructions version. Bumping it (in the console) offers to re-queue the outputs made with older versions, filtered as today (for job reviews: by verdict).

### 8.2 Packs: one file per category of work

| Pack | Kinds inside | Why together | Rhythm | What the agent needs |
|---|---|---|---|---|
| **Onboarding** | `profile_analysis` (CV analysis, tuned search and screening brief, in one output) | One input (CV + answers + calibration data), one careful pass per person. | When people join or change their answers | Text only |
| **Job screening** | `job_review` | The volume pack: same instructions for hundreds of jobs, each candidate with their own brief, best first. | Daily | Text only |
| **Company research** | `company_report` | One generic profile per company, researched **once** for everyone (D13). The file holds no candidate data at all. | A few per week | Web browsing strongly recommended |

Why separate files: the rhythms differ, only company research needs the web, and the large job screening pack would bury the small onboarding one, which is the most important for a newcomer's first impression.

### 8.3 Export: select candidates, set, export

The console's **Export** page, in one screen (the runner uses the same settings, §8.8):

1. **Candidates**: a checklist of every candidate, ticked by default when they have something due, with their due count per pack. Candidates without AI consent are greyed out; a candidate can be excluded from automatic exports.
2. **Packs**: ticked by default when they hold something due.
3. **Job screening settings** (global, saved; can be changed for one export before clicking):

| Setting | Default | Meaning |
|---|---|---|
| **Top share** | 10 % | Of each candidate's jobs waiting for a review, the best N % by score. |
| **Minimum score** | 50 | Never send a job below this score, whatever the share. Meaningful only if 50 means the same for everyone (§8.4, register R1). |
| **Per candidate: at least / at most** | 3 / 25 | Bounds, so a candidate with few jobs still gets some and one with many does not swamp the file. |
| **Freshness** | first seen in the last 14 days | Older jobs are not worth a review. |
| **Pool** | per candidate | The N % is taken within each candidate, never across all of them: one candidate's high scores cannot take everyone's share. |
| **Re-reviews** | off | Also send jobs reviewed with an older instructions version. |

"Jobs waiting for a review" are the candidate's jobs in the inbox (past their filters and minimum score), still *new* (not dismissed, applied, or archived), and with no AI review. The same rule runs after every matching run, so the jobs that qualify show *"AI review · ready by …"* to the candidate as soon as they qualify. Tightening the settings at export time only postpones jobs (they stay queued); it never takes back a promise.

4. **Format**: Markdown (default) or JSON. **File size**: at most 150 tasks per file (setting); a larger pack is split into self-contained parts (`part 1 of 2`).
5. **Live preview** before export: *"Onboarding: 2 candidates · Job screening: 214 jobs for 9 candidates (≈ 1.3 MB, 2 parts) · Company research: 3 companies"*.
6. **Export** → one zip with one file per pack (and part), or each file on its own.

### 8.4 The onboarding agent: tuned search, calibrated scores, a personal screening brief

The onboarding pack is the most important one: it decides how every later job is scored and reviewed for that person. For each candidate it receives:

- the CV (contact details removed), the instant results (health checks, detected titles, skills, years), the **conversation answers** (chips and free text);
- the **current keyword weights** and **calibration data**, computed by the app with those weights on the candidate's own matches: how many jobs fall in each score band (under 35, 35–50, 50–70, 70+), the share at 50 or more, and about 15 sample jobs around the line (title, company, score, matched keywords), spread from 35 to 70.

And returns, in one output:

1. **CV analysis** (for the candidate): strengths, gaps an ATS rule cannot see, section-by-section rewrite suggestions (truthful only), a positioning line.
2. **Tuned search** (for the scoring):
   - include keywords with weights 1–5, **balanced**: between 15 and 40 keywords; at most 5 at weight 5; French and English equivalents together; no generic words that match everything ("management", "projet", "client"); the candidate's target titles at the top; turn-ons as light weights;
   - exclude keywords from the turn-offs;
   - target titles;
   - **calibrated** so that a score of 50 means *"worth a look for this person"*: looking at the sample jobs, the agent says which should land above and below 50 and sets the weights so they do, aiming for a share of matched jobs at 50 or more inside the target band (D15, default 6–12 % since 30 Oct 2026; it was 8–15 %).
3. **Screening brief** (for the job screening agent): at most 200 words, written for an AI reviewer: what a strong fit is for this person, must-haves, deal-breakers (from the turn-offs), what earns extra points (from the turn-ons), how to treat adjacent roles, and the seniority line. It is included in that candidate's block of every job screening file from then on, and shown to the candidate in Settings as *"What we look for for you"*, in plain words, with *"Change my answers"*.

**Checked by the app at import, before anything is applied** (rules, no AI): the weight rules above (counts, range, no duplicates); then the app **recomputes the candidate's score bands with the proposed weights** and shows the operator the effect: *"C-07: at 50 or more 31 % → 11 % (target 8–15 %) ✓ · 4 of 5 'should be above' samples above ✓"*. Out of band is flagged, not blocked: the operator decides. Applied, the candidate sees *"Your search was tuned"* with *See what changed* and *Undo* (§6.3).

**The applied-jobs benchmark (added 23 October 2026, after the first real tuning).** A tuning built from the CV alone let through only 77 % of the jobs the operator had applied to: a person's CV headline is not what they apply to. Every job a candidate applied to is by their own judgement good enough, so it must pass. The onboarding file therefore carries the candidate's applied jobs (the 60 most recent titles, with how today's weights do on all of them), and the import tests the proposed weights on them in memory: **at least 90 % (a console setting) of the applied jobs that the candidate's own filters do not hide must reach the inbox**, or the result is held for the operator (runner) or flagged "would miss good jobs" with the missed titles (console). With fewer than 10 applied jobs there is no benchmark and nothing is held. The instructions to the agent are version 2.

This calibrates each person **once**, at onboarding. Keeping 50 consistent over time (from AI review verdicts and what candidates do with their jobs) is the feedback loop of register R1.

### 8.5 What a file contains: everything the agent needs

Each file is the skill. No skill, plugin, project or prompt has to exist on the agent's side: any assistant that can read a text file (Claude, ChatGPT, Gemini, a coding agent, a chat window with an attachment) can do the work.

In order:

1. **Header**: schema `saxobeat.pack.v1`, export id, pack, part, instructions version per kind, exported at, task count, and **the exact name of the results file to write**.
2. **Agent brief** (platform-neutral, the playbook that lives in `skills/saxobeat-review/SKILL.md` today, generalised): what Saxobeat is and what the file is; work through the tasks in order, best first, in chunks of about 20, never skip one; never invent facts, experience or figures; if the session is about to end, write the results done so far (partial files are imported, the rest is sent again); write the results as one JSON file **next to this file**, or, if the agent cannot write files, print it as a single code block for the operator to paste; the checks to run before finishing; what to tell the operator at the end (counts, problems).
3. **Instructions for each kind in the pack**, with their version.
4. **Output format**: the JSON shape in words and one filled example per kind.
5. **Candidates and tasks**, grouped by candidate: the candidate reference (`C-07`, never a name or e-mail), output language, **their profile once** (CV text with e-mail addresses and phone numbers removed), **their screening brief** (job screening) or **their answers and calibration data** (onboarding), then each task: task id, kind, context. Company research files have no candidate section: each company appears once, with its name, the postings seen there and any links the operator already holds, and the profile asked for is the same for everyone.
6. **The checklist again** at the end, because long files are read top to bottom.

Markdown and JSON carry exactly the same content. The file is generated on the fly and **not stored on the server**: the console keeps only its id, pack, part, candidates, task ids, the settings used, size and a checksum. The texts of the brief and of each kind are kept in code (`jobs/ai/`), versioned, and shown on the console's *Instructions* page.

### 8.6 The results (back)

One JSON object per file processed, whatever the pack, consolidated across candidates:

```json
{"schema": "saxobeat.results.v1", "export": "E-20261024-093000", "pack": "job_screening", "part": 1,
 "agent": "claude-code / opus",
 "results": [
   {"task": "T-1842", "kind": "job_review", "output": { ...today's review fields... }},
   {"task": "T-1843", "kind": "job_review", "skipped": "posting text missing"}
 ]}
```

Onboarding returns `{"cv_analysis": "<markdown>", "keywords": {"include": {...}, "exclude": {...}}, "target_titles": [...], "calibration_note": "...", "screening_brief": "<markdown>"}` per candidate. Company research returns `{"report": "<markdown>", "sources": [...]}` per company: one generic profile, no per-candidate part. The importer still accepts today's `saxobeat.scores.v1/v2` files during the transition and maps them to `job_review` tasks of the operator's candidate.

### 8.7 Import

One drop zone in the console, for one or several files at once (or a pasted JSON block, with any code fence around it removed); the runner uses the same import (§8.8).

1. **Check, write nothing:** schema; export known; every task id belongs to that export and is still open; each output valid for its kind (and, for onboarding, the weight rules and the recomputed score bands of §8.4). **Preview, by candidate and pack:** *"Job screening part 1: 112 results for 6 candidates ready, 1 skipped by the agent, 1 refused: score missing (T-1871)"*. Results whose input changed since export (CV replaced) are flagged *stale*.
2. **Import** applies the valid ones, marks tasks `done`, and the candidates see "ready". Refused ones go back to `queued` with the reason.
3. **Partial and repeated files are fine:** a partial file imports what it has; the same file imported twice changes nothing the second time ("already imported on 24 Oct 10:12").

### 8.8 The local runner: files fetched and results imported automatically

The PC runner already runs every 3 hours from Task Scheduler (`scripts/pc_runner.ps1`, one-click `saxobeat-runner.cmd`) and writes **directly into the hosted database**. It gains an AI step, `manage.py ai sync`, so no new API, token or server endpoint is needed. A second one-click file, `saxobeat-ai.cmd`, runs only that step ("sync now", in seconds).

One folder on the PC (setting `SAXOBEAT_AI_DIR`, default `%USERPROFILE%\Saxobeat AI\`, outside the repository and outside any cloud-synced folder):

```
Saxobeat AI\
  to-do\        pack files waiting for an agent (the agent writes its results next to them)
  done\         packs and results already imported (kept 7 days, then deleted)
  problems\     result files that failed a check, each with a short .txt saying why
  STATUS.txt    what is waiting, what was imported, what is late — rewritten at every sync
```

At every sync:

1. **Fetch.** For each pack with something due, write a file into `to-do\` using the saved settings and every consenting candidate not excluded from automatic exports. **At most one open file per pack** (or per part): a new one is written only when the previous one's results are imported or it is more than 24 h old, so the folder never fills with overlapping files. The export is recorded as made by the runner and appears on the console's *Exports* page.
2. **Import.** Every `*_results.json` found in the folder is checked (§8.7). If every result passes, it is imported automatically and the pack and its results move to `done\`. If anything is refused, nothing from that file is imported: it moves to `problems\` with the reason, and the console's *Today* shows it for the operator to review and import from the preview (D16). Onboarding results with a calibration out of band always wait for the operator's preview.
3. **Report.** One line in the runner's output and in `STATUS.txt`: *"AI: 2 files to do (onboarding, job screening), 1 imported (112 results), 0 problems, 3 tasks late"*.

The operator's part is then only: open the `to-do\` folder, point any agent at it ("process every file in this folder") or hand the files over one by one, and close the session. The next sync (or `saxobeat-ai.cmd`) imports the results.

### 8.9 Command line, same thing

`manage.py ai status` (what is due), `manage.py ai export [--candidates all|C-07,C-12] [--packs ...] [--format md|json] [--out DIR]`, `manage.py ai import <file>... [--dry-run]`, `manage.py ai sync` (§8.8). `export_review` and `import_review` become aliases, then go; `skills/saxobeat-review` is retired once the packs replace it (nothing replaces it: the file is the skill).

## 9. The operator console

One AI back office, for the operator only: a separate interface at `/ops/`, with its own desktop-first layout, its own menu, English only. Candidates get "not found" on every `/ops/` URL (the existing rule in `jobs/access.py`). The candidate top bar loses the Operator dropdown; the operator gets a single "Console" link in *More*.

**How the console is laid out (cycle 024, 2026-11-04).** The top bar has seven areas: **Today · Candidates · Sources · Runs · Feedback · AI · More**. A second row of tabs appears under three of them: **AI** = Export · Import · Queue · Settings (the Instructions page is reached from Settings and highlights it); **Sources** = Sources · Jungle radar; **More** = E-mails · Exports · Auto-reject · Data & backups. Every page keeps its own address, and every page opens with a one-line purpose under its title. Every AI page shows a one-line status strip (what is waiting, with an agent and late, the on-time rate, the runner's last sync, any pause). The table below describes the pages; "AI queue" is the AI area's Queue tab, "AI settings" its Settings tab, and Exports sits under More.

| Page | What it shows and does |
|---|---|
| **Today** (home) | What needs the operator today, in this order, empty blocks left out ("Nothing needs you today." when all are): failing sources, source proposals to decide, new feedback, candidates who joined in the last 7 days, the last source run with *Refresh now*, then one AI line (to export, with an agent, late; paused). The pack cards, the runner folder and the on-time rate moved to the AI pages (the status strip and *Import*), cycle 024. |
| **Export** | §8.3: pick candidates and packs, adjust the job screening settings for this export, see the preview, download the zip or each file. |
| **Import** | §8.7: the drop zone (files or pasted JSON), the preview by candidate and pack (with the calibration effect for onboarding), the import history (manual and runner). |
| **AI queue** | Every task, filterable by pack, kind, candidate, state, due; cancel; re-queue; open a task to see its context and its output. |
| **Exports** | Past exports (console or runner): settings used, candidates, files and parts; how many results came back, how many are outstanding; "send the outstanding ones again". |
| **AI settings** | The job screening defaults (§8.3), calibration target band (D15), file size, runner behaviour (automatic exports on/off, automatic import on/off), the AI weight in the final score (per candidate, with a default), the pause switch. |
| **Instructions** | The agent brief and each kind's instructions: current version, the text, a changelog note; "bump version and re-queue…". |
| **Candidates** | Today's *People* page, plus per person: onboarding stage, CV health score, AI consent, conversation answers, screening brief, current score bands (share at 50 or more), open and late tasks, last seen, "exclude from automatic exports". Invite, reset link, deactivate. The console never lets the operator act inside a candidate's space. |
| **Sources, Proposals, Runs, Jungle, Data** | The existing operator pages, moved under `/ops/` unchanged. |

Things that leave the candidate pages: "Refresh now", failing-source banners, platform tags on job cards, the AI weight in Settings (it moves to *AI settings*).

**Daily routine this is designed for** (target under 10 minutes hands-on):

1. The runner has already put today's files in `Saxobeat AI\to-do\` (and `STATUS.txt` says what they are).
2. Point an agent at the folder, or hand it each file: no skill, no setup. Onboarding first (newcomers' first impression), job screening last (large). Company research in an agent that can browse.
3. Nothing else: the next sync imports the results. Glance at *Today* for anything in *problems* or out-of-band calibrations to confirm.

## 10. Data model (sketch)

- **`AiTask`**: candidate, kind, subject (job, company or none), state, requested_at, due_at, exported_at, export (and part), input_hash (to spot stale results), instructions_version, output (JSON), finished_at, error, seen_at (for the "new" dot), requested_by (system / candidate). Company research: one task per company, with the candidate who asked recorded only for the weekly cap; the profile it produces belongs to the company, not to a candidate. **`CompanyProfile`** (new, shared): normalised company key (the same cleaning as `employers.clean_name`), report, sources, researched_at, instructions_version. Each candidate's own `Company` page (their notes, dream flag, red flags) keeps working and shows the shared profile above it; a candidate's own written report is never shared with other candidates.
- **`AiExport`**: id, created_at, origin (console / runner), candidates, packs, format, the job screening settings used (snapshot), and per file: pack, part, task ids, size, checksum, imported_at.
- **`AiSettings`** (one row): job screening defaults (top share, minimum score, per-candidate bounds, freshness, pool, re-reviews), calibration target band, max tasks per file, runner automatic export / import, default AI weight, paused until. Instruction versions per kind live in code next to the texts.
- **Per candidate** (`Candidate` / `Config`): `ai_consent` (+ when), `auto_export` (default on), `preferences` (the conversation: roles, turn-ons, turn-offs, non-negotiables, places, free text, answered_at), `screening_brief` (+ version and the task it came from), the previous keyword set kept for *Undo*. `CvAnalysis` (or the output kept on the task and shown from there).
- `Config.rerun_cutoff` retires once job reviews run through instruction versions.

Code layout: `jobs/ai/` with `brief.py` (the agent brief), `kinds.py` (one entry per kind: build context, instructions and version, output check, apply), `packs.py`, `selection.py` (the job screening rule), `calibration.py` (score bands, sample jobs, weight rules, recompute with proposed weights), `queue.py` (create, de-duplicate, cancel, due), `export.py` (Markdown/JSON/zip, parts), `results.py` (check, preview, apply), `sync.py` (the runner's folder); `jobs/conversation.py` (the questions, chips and their rule mappings); `jobs/views_ops.py` and `jobs/templates/jobs/ops/`. `handoff.py` becomes the `job_review` kind; `briefing.py` stays as the bring-your-own-AI prompt builder and gives its company instructions to `company_report`.

## 11. Privacy and safety

- **Consent:** back-office AI processing only for people who ticked it; turning it off cancels their open tasks and hides every AI component. The privacy note says what leaves the app (CV text without contact details, conversation answers, the jobs), to whom (the operator's AI provider), and that nothing is kept by Saxobeat outside its database. Bring-your-own-AI is the candidate's own action and needs no consent from Saxobeat; the tutorial says so in one line.
- **Minimum data:** e-mails and phone numbers stripped from CV text in exported files; candidates by reference; files not stored server-side; the runner's folder lives outside the repository and cloud-synced folders, and imported files are deleted after 7 days.
- **No cross-candidate leaks:** a result only applies to the task's own candidate and subject; tests import a crafted file that points a task at another candidate's job and expect refusal.
- **AI can be wrong:** AI outputs are labelled as such, the instant result stays visible, tuned searches are previewed by the operator and undoable by the candidate.

## 12. Phases

| # | Phase | Size | Result |
|---|---|---|---|
| **A0** | **Console shell** | S | `/ops/` layout and menu; existing operator pages moved there; operator crumbs removed from candidate pages; *Today* page with what exists now (sources, proposals, runs). |
| **A1** | **Tasks, export and import, with the job screening pack** | M | `AiTask`, `AiExport`, `AiSettings`; the agent brief inside every file; the **job screening** pack for every selected candidate, selected by the global settings (top N %); Export page (candidates, packs, preview, parts, zip), Import page (preview, partial, idempotent); `manage.py ai export/import/status`; legacy scores files still accepted. |
| **A2** | **The local runner** | S | `manage.py ai sync`, the `Saxobeat AI` folder, automatic fetch (one open file per pack) and import (all-or-problems), `STATUS.txt`, the step in `pc_runner.ps1`, `saxobeat-ai.cmd`, runner exports on *Exports*. |
| **A3** | **Onboarding: CV results and the conversation** | M | §7: instant results screen, chips instead of text boxes, the five-question conversation with its instant rule mappings, AI consent, the pending/ready component (FR/EN), first page of matches first, target-role fit; profile and weights moved to Settings; *What I'm looking for* in Settings. |
| **A4** | **The onboarding pack** | M | `profile_analysis`: CV analysis, balanced and calibrated keywords (calibration data out, weight rules and recomputed score bands at import, operator preview, candidate *Undo*), screening brief included in job screening files; *What we look for for you* in Settings. |
| **A5** | **Company research pack and bring-your-own-AI help** | M | `company_report` (one generic `CompanyProfile` per company, never researched twice, on request and at the first interview; the shared profile shown on every candidate's company page); the *Prepare with your AI* row on the job page: copy / share sheet / download, the questions box, the hover/tap tutorial, paste-back for the cheat sheet. |
| **A6** | **Running it well** | S | Instruction versions and re-queue (retires the rerun round); pause switch with candidate copy; on-time metrics on *Today*; old commands and the `saxobeat-review` skill removed. |

**What was built (23 October 2026, all six phases, 1,109 tests on SQLite).** Where the code differs from the plan above:

- **Tasks are made when the queue is refreshed**, not at the moment a job qualifies: `jobs/ai/queue.refresh()` runs on `manage.py ai status/export/sync` and on the Export page. Candidates see "ready by ..." from the first refresh after a job qualifies; the PC runner refreshes at every sync.
- **Conversation and onboarding:** the draft profile is applied the moment the CV is read (the results screen shows the keywords as chips to drop), not on a form. The profile text and the keyword weights are still edited in Settings as text boxes: **the chips with a weight control (§7) are not built.**
- **Calibration** scores up to 3,000 of the candidate's most recent visible jobs again, in memory, with the proposed weights (`jobs/ai/calibration.py`). The "samples" the agent classifies are used to count how many land on the chosen side; that count is shown, but only the share at 50 or more decides whether a file is held.
- **Held results:** the runner holds a whole file when any result is refused or an onboarding result lands out of its band; the console import shows the same as a flag ("look first") and leaves the decision to the operator.
- **Applying a tuned search** scores the person's jobs again: in the background on the web server, to the end in the PC runner (a flag on the candidate, `rescore_pending`, carries it between the two).
- **AI weight:** one setting for everybody (`AiSettings.default_ai_weight`). Changing it rewrites every candidate's weight and every blended score; it is no longer in a candidate's Settings.
- **Bring your own AI:** the three buttons are on the job page (not on the company page). Copy and share were exercised in the browser pane up to the clipboard, which that pane refuses: **to check on a real laptop and a real phone**, together with the share sheet.
- **Retired:** the AI review page, `export_review`, `import_review`, the rerun round (`Config.rerun_cutoff`, dropped) and the `skills/saxobeat-review` skill. Older scores files still import on the Import page.
- **AI reviews never remove a job (added the same day):** visibility reads the rules score, the blend only ranks and labels; a one-tap filter hides the "don't apply" jobs on request (`jobs/services/visibility.py`).
- **Not built / left for later:** per-candidate AI weight, the tab dot for a ready result (the card and the inbox strip say it), `Candidate`-level "exclude from automatic exports" is built (People page), push notifications (R4), a scheduled agent (R3), the calibration feedback loop (R1).

**Order:** A0 → A1 → A2 → A3 → A4 → A5 → A6. If onboarding is the most urgent, A3 can come right after A0 (the conversation and instant results need no AI plumbing), and A4 follows A1. The bring-your-own-AI half of A5 needs nothing from the others and can be built at any time.

## 13. Decisions

| # | Question | Decision (the recommendation, where it was accepted as written) |
|---|---|---|
| D1 | Console: same app under `/ops/` with its own layout, or a separate site/subdomain? | **Accepted 23 Oct.** `/ops/` in the same app: one deploy, one login, the existing operator gate. |
| D2 | How to group the work into files? | **Decided 23 Oct:** one file per pack, each covering every selected candidate. Packs: onboarding, job screening, company research (§8.2). |
| D3 | Files out in Markdown by default, results back always as JSON? | Yes. **Decided 23 Oct:** every file carries the full agent brief, so no skill or setup is needed on any platform. |
| D4 | The promise: "within 24 h" as a firm due time shown to the candidate ("ready by Fri 10:30")? | **Decided 23 Oct:** yes, with the late and paused messages of §6.3, plus a standing beta note: *during the beta, AI is not instant; you'll get it within 24 h at the latest; check back soon* (§6.3). |
| D5 | AI keyword changes: applied automatically or offered to the candidate? | **Accepted 23 Oct.** *Changed from the first draft* (calibration needs consistent weights): applied after the **operator's** import preview, then the candidate is told and can **undo** with one tap. Candidates no longer accept keywords one by one. |
| D6 | Job screening defaults? | **Accepted 23 Oct.** Top 10 % of each candidate's jobs waiting for review, score 50 or more, at least 3 and at most 25 per candidate, first seen in the last 14 days, pooled per candidate (§8.3). All global settings, changeable per export. |
| D7 | Company report also automatic on the first interview at a company? | Yes (accepted): it is the moment it matters most, and it is rare. Skipped when the company already has a profile (D9). |
| D8 | Application help: operator back office or the candidate's own AI? | **Decided 23 Oct:** bring your own AI, visible on the job page with a hover / tap tutorial (§6.4). Not in the operator's packs. |
| D9 | Cap on company research requests per candidate? | **Decided 23 Oct:** 5 per week; the operator can lift it per person. **A company that already has a profile is never sent again:** the candidate gets the existing profile at once, no task is created, and the request does not count against the cap. (No cap for application help: it costs the operator nothing.) |
| D10 | AI consent: explicit tick at onboarding (not pre-ticked)? | **Accepted 23 Oct.** Yes. Existing users are asked once with the same tick on their next visit; until they answer, no tasks are queued for them. |
| D11 | Output language? | **Accepted 23 Oct.** Analyses (CV, job review, screening brief shown to the candidate) in the candidate's interface language; the bring-your-own-AI prompts for texts meant for an employer ask for the posting's language, as already decided for the agent files. |
| D12 | How does the operator learn something is due? | **Accepted 23 Oct.** The runner's output and `STATUS.txt`, the console's *Today* page. Push notifications later. |
| D13 | Company research: shared per company, with a short angle per candidate? | **Decided 23 Oct, changed:** one **generic** profile per company, common to all candidates; **no per-candidate angle**. The research file therefore carries no candidate data. |
| D14 | Largest file: split a pack into parts above how many tasks? | **Accepted 23 Oct.** 150 tasks per part (setting). Each part is self-contained and imports on its own. |
| D15 | Calibration target: what share of a candidate's matched jobs should score 50 or more? | **Accepted 23 Oct.** 8–15 % to start, a console setting. Revisit with real data (register R1). **Changed 30 Oct 2026 (owner): 6–12 %**, after the first real onboarding result scored 7.7 % and was held for being just under 8; the default is now 6–12 (migration 0042) and the console value is edited on the AI settings page. |
| D16 | Runner import: automatic, or always through the operator? | **Decided 23 Oct:** a local runner fetches files and imports results. Recommended rule: import automatically when every result in the file passes; otherwise hold the whole file in `problems\`. Onboarding results out of the calibration band always wait for the operator. |
| D17 | The conversation: scripted questions with chips, no AI? | **Decided 23 Oct** (a short conversation about roles, turn-ons and turn-offs). Recommended: scripted, five questions, chips plus free text; the free text goes to the onboarding agent. |
| D18 | Bring-your-own-AI handover: copy / share sheet first, file download second? | **Accepted 23 Oct.** Yes: on a phone a download is a dead end; the share sheet goes straight into the AI app. |

## 14. Acceptance

- A company that already has a profile is never sent for research again: asking for it shows the existing profile at once and creates no task; a research file contains no candidate data.
- Every AI card carries the beta note (AI is not instant; within 24 h at the latest).
- A new candidate goes from the invitation to a sorted inbox in **under 4 minutes**, never types a keyword weight, sees their ATS score, keyword signals and target-role fit **before** the conversation, and their conversation answers that map to rules change their inbox at once.
- Every AI component shows one of the five states of §6.3; no AI output appears without its label; the instant result is still visible next to it.
- The onboarding agent's output is refused if the weight rules fail; the import preview shows each candidate's share at 50 or more before and after; an applied tuning can be undone by the candidate and restores the previous weights exactly.
- A job screening file contains each candidate's screening brief (or their answers, if no brief yet).
- The operator exports every pack for the selected candidates in **one click** (with the saved settings) and imports any number of result files in **one drop + one confirm**.
- With the runner scheduled, pack files appear in `to-do\` without the operator opening the console, a valid results file is imported at the next sync, and an invalid one lands in `problems\` with a reason and changes nothing.
- The same exported file is processed by **two different assistants** (for example Claude and another vendor's) with nothing installed or configured on either, and both results import cleanly.
- Job screening sends, per candidate, exactly the jobs the settings select, and the preview count matches the file.
- Importing a file twice changes nothing; a result pointing at another candidate's job is refused; a malformed result is refused alone (console) or holds its file (runner).
- *Prepare with your AI*: one tap puts a complete prompt on the clipboard (laptop) or in the share sheet (phone); the tutorial shows on hover / tap and the first time; a first-time user gets an answer from their own assistant without any other help.
- No `/ops/` URL answers a candidate; no operator word ("source", "run", "platform", "batch", "pack") appears in candidate pages, including for the operator.
- With AI turned off for a candidate, no task is created for them and every screen still works.
- All candidate strings exist in French and English.

## 15. Risks

| Risk | Mitigation |
|---|---|
| The 24-hour promise is missed (operator away, ill, busy). | Files are fetched and imported without the operator; pause switch with an end date and honest candidate copy; late message; on-time rate on *Today*. |
| Volume outgrows a manual routine (30 people × up to 25 reviews = 750 a day). | The job screening settings (top share, per-candidate maximum), parts of 150 tasks, best-first ordering inside files, the runner removing every file chore; a scheduled agent later (R3). |
| An agent handles a long file badly (skips tasks, drifts from the format). | Best-first order, chunks of 20 in the brief, the checklist at both ends of the file, strict import checks, outstanding tasks re-sent automatically. |
| Calibration is wrong for someone (too many or too few jobs above 50). | Recomputed score bands at import, operator preview, candidate undo, the band visible per candidate in the console; the feedback loop R1 later. |
| The conversation feels like a form. | Five questions, chips first, every question skippable, one minute; measured by the answer rate (§16). |
| Bring-your-own-AI is not understood. | One row, three buttons, a three-line tutorial shown the first time; measured by copies per active candidate. |
| An exported file with many CVs is leaked from the operator's disk. | Contact details stripped, references instead of names, the runner's folder outside synced folders, imported files deleted after 7 days, nothing kept server-side. |
| AI output is wrong or invented. | Instructions forbid invention (as today); scoring changes previewed and undoable; the instant result stays visible; the candidate can dismiss an AI output. |
| Scores jump when AI reviews land (the final score blends both). | The job card says "AI reviewed" and shows both numbers on the job page, as today; the blend weight is a console setting. |

## 16. Success measures

- Onboarding completion ≥ 80 %; median time to sorted inbox < 4 min; ≥ 70 % answer the turn-ons and turn-offs questions.
- ≥ 95 % of AI tasks delivered before their due time over a month.
- Operator hands-on time ≤ 10 min/day (self-reported, plus export-to-import time from the export records).
- After onboarding calibration, every candidate's share of matched jobs at 50 or more sits inside the target band.
- At least half of active candidates open an AI result within 2 days of it landing; at least a third use *Prepare with your AI* in their first month.

## 17. References in the repository

- Today's hand-off: `jobs/services/handoff.py`, `jobs/management/commands/export_review.py`, `import_review.py`, `skills/saxobeat-review/SKILL.md`, `/review/` in `jobs/views.py`.
- Bring-your-own-AI prompts: `jobs/services/briefing.py` (application answers, cheat sheet, follow-up, company report), served by `job_briefing` and `company_briefing`.
- Onboarding: `jobs/views_cv.py`, `jobs/templates/jobs/welcome*.html`, `jobs/cvfile.py`, `jobs/cvhealth.py`, `jobs/cvprofile.py`, `jobs/cv.py`; filters and breadth: `jobs/services/filters.py`, `jobs/services/breadth.py`; signals: `jobs/services/signals.py`.
- Scores: `Score` in `jobs/models.py`; blend in `jobs/services/scoring.py`; per-candidate matching: `jobs/services/matching.py`.
- Runner: `scripts/pc_runner.ps1`, `saxobeat-runner.cmd`, [DEPLOY.md](DEPLOY.md).
- Roles and the operator gate: `jobs/access.py`; operator menu in `jobs/templates/jobs/base.html` and `more.html`.

## 18. Register: issues to tackle later

| # | Issue | Why it matters | First idea |
|---|---|---|---|
| **R1** | **Score calibration feedback loop.** Keep "50" meaning the same across candidates over time, not only at onboarding. | The job screening line (top N %, minimum 50) and every comparison across people depend on it. Catalogue changes, new keywords and new CVs drift the scale. | Track per candidate: share at 50 or more, AI review verdicts against the rule score near the line (AI "apply" below 50, "don't apply" above 70), dismiss and apply rates by score band. Then a periodic *recalibration* task in the onboarding pack, or a per-candidate offset. |
| R2 | Screening brief drift | Turn-ons and turn-offs change as a search goes on. | Re-queue the onboarding pack after N dismissals of jobs the AI said to apply to, or every month. |
| R3 | Running the agent automatically | The last manual step of the routine. | A scheduled agent (e.g. a command-line agent started by the runner) processes `to-do\`; needs a cost and consent check first. |
| R4 | Notifications | "Ready" is only seen when the candidate opens the app. | Web push for the installed app (M5 made it installable). |
| R5 | Company profile freshness | A profile is never sent twice (D9), so it ages. | Re-research after 3 months or on a flagged change; a "report outdated" button for the operator. |
| R6 | Keeping what was sent | Bring-your-own-AI answers are used outside the app. | "Save to my application packet" with a paste box (F8 packet). |
