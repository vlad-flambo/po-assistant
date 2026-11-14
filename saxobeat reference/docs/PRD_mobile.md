# PRD — The candidate interface on a phone

| | |
|---|---|
| **Status** | Agreed 23 October 2026: all ten decisions in §13 confirmed, D3 changed (one theme only) |
| **Date** | 23 October 2026 |
| **Author** | Vladimir (product), written with Claude |
| **Builds on** | [PRD_multi_user.md](PRD_multi_user.md) (accounts, candidate space), [PRD_competitive_features.md](PRD_competitive_features.md) (the features that crowd the screens today), [DEPLOY.md](DEPLOY.md) (the app is now hosted, so friends open it on their phones) |
| **Scope** | Every page a **candidate** uses, redesigned phone-first (320–430 px wide), still good on a laptop. The operator's pages are out of scope: they stay desktop tools, but must not get worse. |
| **Progress (23 Oct 2026)** | **M0 to M5 are built** (notes under §12). To check on a real phone: installing the app, and the swipe with a finger (both were tested by simulation: see §12). |
| **In one line** | One thing per screen, the next action under the thumb, and words only where they help a decision. |

---

## Outstanding work (moved to SDLC cycles on 2026-10-29)

What this PRD still asks for is now tracked as cycles in `docs/sdlc/` ([the audit](sdlc/cycles/006-stale-docs/evidence/prd_audit_2026-10-29.md)). This PRD stays the product-level reference; the cycles carry the work.

- Real-phone checks (install, swipe, share target), Playwright (D6), 360 and 390 px: [005](sdlc/cycles/005-real-devices/intent.md)
- Long-press quick sheet, pipeline swipe and Move to…, one-tap to-dos, contacts search: [010](sdlc/cycles/010-phone-gestures/intent.md)
- §16 success measures: [007](sdlc/cycles/007-success-measures/intent.md)
- Stale notes (stack tables, 'Waking up'): [006](sdlc/cycles/006-stale-docs/intent.md)
- D2 'buttons on cards', D10 French copy review: [the backlog](sdlc/backlog.md)

---

## 1. Problem

The interface was built at a desk, for one person who knows every control. Opened on a phone it is cluttered and wordy. Measured on 23 October 2026 with real data, at 375 × 812 px (candidate view, French and English share the same layout):

| Page | What a phone user gets |
|---|---|
| **Every page** | The menu is 6 links, 3 colour swatches (three palettes), a language switch and "Log out" in one bar. At 375 px it wraps to **3 lines (about 150 px) before any content**. |
| **Inbox** | The job table is **537 px wide in a 375 px screen: the page scrolls sideways.** The first job starts **946 px down** (more than one screen) under 6 blocks of controls: Export CSV, the archive button, the breadth switch, a filter bar with 10 controls, keyboard shortcuts (j/k/s/d/o: useless on a touch screen), the bookmarklet (cannot be used on a phone), "add a job by link" and "clear the noise". Each job row is **173 px tall**. The page holds 200 jobs: **536 KB of HTML, 52,783 px tall.** |
| **Job page** | **8,202 px tall (about 10 screens)**, 12 sections, 28 buttons, about 1,450 words. The primary action ("Open apply link") is above the fold but scrolls away; the status, notes and interviews are far below. |
| **Pipeline** | Four-plus columns side by side: one and a half are visible, and each scrolls inside itself. Moving a card is "drag it to another column" (mouse drag: it is very likely not possible by touch, to verify in M3). |
| **Insights** | A Sankey diagram designed for 860 px, and 17 explanatory paragraphs on one page. |
| **Words** | Every screen explains itself: "Jobs scoring below 35 are kept out of this list: they are in Filtered out & archive, under Low score. Type 0 in Min score to see them here." Help text is on the page, not behind a tap. |

The cause is structural, not cosmetic: pages are **tables and side-by-side columns with a single `@media (max-width:640px)` rule** (the whole stylesheet is 14.7 KB), and every feature added since phase 1 put its controls and its explanation on the main screen.

**Why now:** friends are about to use the hosted app, and most job hunting happens on the phone: reading a job on the train, answering "did you apply there?", checking the next interview.

## 2. Goals

1. **Triage 20 jobs in under a minute** on a phone: one gesture or tap per job.
2. **Read a job and act on it in three taps:** open it, open the posting, mark it applied.
3. **Know where I stand in five seconds:** what to follow up, the next interview, what is waiting.
4. **Say less.** A screen shows what is needed for the decision in front of the user; everything else is one tap away, never on the page by default.
5. **No sideways scrolling, no tiny targets, no zoom on any candidate page** at 320–430 px.
6. **Same app, same data, same French and English.** No separate mobile site. The laptop experience keeps its keyboard shortcuts and its density.

## 3. Out of scope

- A native iOS or Android app. (An installable web app, §9, gets most of the benefit.)
- The operator's pages (people, sources, runs, radar, AI review, data & backups).
- New features: this PRD changes how things are shown and reached, not what the app can do. (Two small additions serve the phone itself: add a job by sharing a link to the app, and paging the inbox.)
- Offline use. Job data is personal and changes daily; the app needs the network.
- Redesigning the scoring, the filters' logic or the Insights numbers.

## 4. Users and what they do on a phone

| Moment | The job to be done | Where it lives today |
|---|---|---|
| On the move, 2 minutes | Sweep the new jobs: keep a few, drop the rest | Inbox |
| Interested in one | Understand it fast: score, why, pay, remote, who I know there | Job page |
| Decided | Apply, then log it | Job page: apply link, "Applied" |
| After applying | See what needs a nudge | Pipeline, "To do" |
| A recruiter calls | Note the stage and the date | Job page → Interviews |
| Before an interview | Prepare: cheat sheet, company profile, what I sent | Job page, cheat sheet |
| Once in a while | Check how the search is going | Insights |
| Rarely | CV, search breadth, language, account | Settings |

**Phone first for the first six rows. Insights and Settings must work on a phone but may be less rich.** Long forms (CV upload review, contacts import) stay possible, and are allowed to be a little longer.

## 5. Principles

1. **One screen, one question.** The inbox asks "keep or drop?", the job page asks "apply?", the pipeline asks "what next?".
2. **The thumb decides the layout.** The main action sits at the bottom of the screen, in the thumb's reach: a bottom tab bar, a fixed action bar. The top holds only the title and one or two icons.
3. **Show the decision, hide the explanation.** Numbers, short labels and icons on the screen. The "why" is behind a tap (a bottom sheet), and the same sheet is reused everywhere.
4. **Two chips at most** on a list card. Everything else belongs to the job page.
5. **Gestures are shortcuts, never the only way.** Every swipe has a visible equivalent.
6. **Lists are lists, not tables.** Cards that reflow, one column on a phone, columns on a laptop.
7. **Heavy things load later.** Pages of 30 items, not 200; nothing the first screen does not need.
8. **Desktop does not regress.** At 1024 px and above, the keyboard flow (j/k/s/d/o) and the information density stay.

## 6. Navigation

**Phone (under 900 px): a top bar and a bottom tab bar.**

```
┌──────────────────────────┐
│ Inbox · 142        🔍  ⚙ │   top bar: title + count, search, filters
├──────────────────────────┤
│                          │
│       (the screen)       │
│                          │
├──────────────────────────┤
│ Inbox  Pipeline  Talks  ⋯│   bottom tabs, 56 px + safe area
└──────────────────────────┘
```

| Tab | Content | Badge |
|---|---|---|
| **Inbox** | new jobs | new today |
| **Pipeline** | shortlisted, applied, interviewing, offer, closed; the "To do" card | follow-ups due |
| **Interviews** | next first, then waiting for feedback, then past | upcoming |
| **More** | Companies, Contacts, Insights, Settings, Filtered out & archive, language, log out | none |

- **The colour swatches disappear: there is one theme (§8).** The FR / EN switch moves into **More** (and into Settings on a laptop): it is changed once, not on every page.
- **Laptop (900 px and above):** the current top navigation, unchanged in content (Inbox, Pipeline, Interviews, Companies, Insights, Settings), with the language switch folded into a small menu next to Log out.
- A visible **back** arrow on every detail screen; the browser's back button keeps working (real URLs, no single-page trickery).

## 7. Screens

### 7.1 Inbox

```
┌──────────────────────────┐
│ Inbox · 142       🔍  ⛃2│   ⛃ = filters (2 active)
├──────────────────────────┤
│ [Remote ✕] [Added today ✕]│   active filters, one scrollable line
│ ┌──────────────────────┐ │
│ │ 77  Senior Account…  ♥│ │   score · title (2 lines) · dream heart
│ │     Alma · Paris      │ │   company · city (1 line)
│ │     [apply] [👥 2]    │ │   two chips at most
│ └──────────────────────┘ │
│ ┌──────────────────────┐ │
│ │ 71  Head of Partner…  │ │
│ │ …                     │ │
│ 238 hidden below 35 · Show│   one line, replaces the paragraph
├──────────────────────────┤
│ Inbox  Pipeline  Talks  ⋯│
└──────────────────────────┘
```

**Card (target 88–104 px):**
- Left: the score chip (colour = band). Then the title (2 lines, 16 px bold), then **company · city** (1 line, truncated), then the chips.
- **Chips, in priority order, two shown, "+n" if more:** AI verdict (apply / don't apply), someone I know there (👥 n), remote or days at home, pay stated, "new" or "reposted". Everything else (employer history, English, closed, freshness details, summary) moves to the job page.
- The dream-employer heart sits on the title line.
- **No buttons on the card by default.**

**Triage:**
- **Swipe right = shortlist** (★), **swipe left = dismiss** (✕), with a colour reveal and a threshold, then a **toast with Undo for 5 seconds**: "Dismissed · Undo · Why?". "Why?" opens the reason list (it replaces the per-row "why?" dropdown).
- **Tap = open the job.** **Long-press = quick sheet:** shortlist, dismiss, open the posting, share.
- **Visible equivalent for every swipe:** the quick sheet, the job page's action bar, and (decision D2) an optional "buttons on cards" setting for people who dislike swiping.
- On a laptop the row keeps its ★ / ✕ buttons and the j/k/s/d/o shortcuts (hover and fine-pointer devices only).

**Filters (one bottom sheet, opened from the top bar):**
- Contents in this order: **Breadth** (Strict / Balanced / Broad as a segmented control), **Min score**, **Added** (any / today / 24 h), **Salary stated**, **English-speaking**, **Hide reposts**, **Sort** (best / newest), **Employers** (a searchable list that opens on its own screen).
- Active filters appear as **removable chips under the top bar**, one scrollable line. "Reset" in the sheet. **Apply** is the one button.
- Search is a field that opens from the 🔍 icon, not a permanent block.

**What leaves the phone inbox:**

| Today on the inbox | On a phone |
|---|---|
| Export CSV | Laptop only |
| Bookmarklet ("send jobs from LinkedIn") | Laptop only; replaced on the phone by **sharing a link to the app** (§9) |
| "Add a job by link" | The **+** in the top bar opens a sheet with one field |
| "Clear the noise: dismiss everything below…" | Laptop only |
| Keyboard shortcuts line | Only when a keyboard is detected |
| The "scores below 35 are hidden…" paragraph | One line: "238 hidden below 35 · Show" |
| Breadth switch with its "details" link | Inside the filter sheet |

**Paging:** 30 jobs per page, the next page loads as the end comes into view (an HTMX "revealed" trigger), with a visible "Load more" as the fallback. First page target: **under 100 KB** (today 536 KB).

### 7.2 Job page

```
┌──────────────────────────┐
│ ←  Alma           ♥   ⋯  │
├──────────────────────────┤
│ Senior Strategic           │
│ Partnerships Manager       │
│ Paris · full remote        │
│ [71 why?] [apply] [70–90k] │   chips: tap the score for the explanation
│ Posted 2 weeks ago         │
│                            │
│ ▸ Summary                  │   sections: collapsed, one-line summaries
│ ▸ Why this score  71       │
│ ▸ Description              │
│ ▸ Interviews · none yet    │
│ ▸ Notes · empty            │
│ ▸ History                  │
├──────────────────────────┤
│ [ Open posting ↗ ] [★] [⋯]│   fixed action bar
└──────────────────────────┘
```

- **Header:** back, company (opens the company profile), the dream heart, "⋯".
- **First screen:** title, place and work mode, **three chips at most** (score, verdict, pay), when it was posted. Nothing else.
- **Fixed action bar at the bottom, always visible:** the primary action **changes with the status**:
  - new → **Open posting ↗** · ★ Shortlist
  - shortlisted → **Open posting ↗** · ✓ Applied
  - applied → **Add a stage** (interview) · ⋯
  - interviewing → **Next stage** · Cheat sheet · ⋯
- **"⋯" sheet:** Dismiss (with reason), Not available any more, Focus, Move to… (status), Notes, Download for an agent, "How well does my CV fit?".
- **Sections are accordions**, collapsed, each with a **one-line summary** in its header ("Interviews · 2 stages, next Tue 14:00", "Notes · 3 lines"). The order follows the status: for a new job, Summary → Why this score → Description; once applied or interviewing, Interviews and Notes come first.
- **"Why this score"** is the shared bottom sheet (matches, gaps, verdict), not a long section. **Signals** (pay, days at home, English), **employer history** and **contacts** become one-line rows with a chevron ("Applied here 3 months ago", "2 people you know").
- **Target: the page is at most three screens tall with everything collapsed (about 2,400 px)**, against 8,202 px today.

### 7.3 Pipeline

```
┌──────────────────────────┐
│ Pipeline                 │
├──────────────────────────┤
│ [Shortlisted 4][Applied 52][Interviewing 2][Offer][Closed]   ← scrolls sideways, chips only
│ ┌──────────────────────┐ │
│ │ ▶ To do · 45          │ │   one card, opens the follow-up list
│ └──────────────────────┘ │
│ ★ Focus                  │
│  Company · Role   applied 22 Oct · follow up │
│ …                        │
├──────────────────────────┤
│ Inbox  Pipeline  Talks  ⋯│
└──────────────────────────┘
```

- **One stage at a time**, chosen from a segmented bar with counts. Swiping the list left or right changes stage.
- **Compact cards:** title, company, one status line ("applied 22 Oct · follow up"). Focus jobs are pinned first.
- **"To do"** is a card at the top of Applied, opening a full-screen list of what needs a nudge, with a one-tap "Followed up" and "Not interested".
- **Moving a card:** long-press or "⋯" → **Move to…** (a sheet). **Drag and drop stays on laptops only.**
- On a laptop the board stays as it is (columns, drag and drop).

### 7.4 Interviews

- **Next up first:** a card per upcoming stage with the company, stage, date and time ("Tue 14:00", "in 2 days"), and a **Prepare** button (cheat sheet). Then **Waiting for feedback**, then past stages.
- Adding a stage is two taps from a job; the "How it went" outcome is a segmented control (Waiting / Positive / Negative / Rejected). The existing rule keeps working: Rejected here also rejects the job.

### 7.5 Insights

- Three tiles first (landed, scored above 50, applied) with the **day / week / month** control as chips.
- The Sankey diagrams are drawn for wide screens. **Under 640 px they are replaced by a vertical list of bars** ("Landed 1,970 → Above 50 887 → AI said apply 136 → Applied 64") with the same numbers, the same breakdowns and a tap on a bar to expand its parts. The Sankey stays above 900 px.
- Every explanatory paragraph moves behind an **ⓘ** that opens the shared help sheet.

### 7.6 Companies, contacts, company page

- A search field and a list; the dream heart is a tap target on each row. The company page keeps its pay, history and contacts as one-line rows that open the detail.
- Contacts (the LinkedIn import) is a list with a search field; the import form is a separate screen.

### 7.7 Settings

- **A list of groups that open one by one:** Search (breadth, cities, pay), Profile & CV, Language, Account (download my data, delete my account). No page of ten stacked forms.
- Each screen has one save action at the bottom.

### 7.8 Sign-in, invitation and first run

- Sign-in and "join with an invitation" are single-column, centred, with the keyboard-friendly input types (email, current-password, new-password).
- **First run (CV upload):** at most three steps, one per screen, each with one primary button. The CV is chosen with the phone's file picker.

## 8. Components (the vocabulary)

| Component | Rule |
|---|---|
| **Tap target** | At least 44 × 44 px, 8 px apart. |
| **Text** | 16 px minimum for body and inputs (stops iOS from zooming on focus); 13 px only for secondary lines; no 11 px text. |
| **Spacing** | A 4-px scale: 4, 8, 12, 16, 24. Page side padding 16 px. |
| **Card** | One radius (12 px), one border, no shadow stacking. |
| **Chip** | 24 px high, one line, at most 12 characters; colour carries meaning (good, warn, bad, neutral), never decoration. |
| **Bottom sheet** | The native `<dialog>` element, slides up, closes on tap outside or swipe down; used for filters, quick actions, "Why this score", the reason for dismissing, help, "Move to…". |
| **Toast** | One at a time, 5 s, with Undo, above the tab bar. |
| **Segmented control** | For 2–4 mutually exclusive options (breadth, period, "How it went"); replaces dropdowns. |
| **Accordion** | A header with a one-line summary; only one open at a time is not required. |
| **Safe areas** | `viewport-fit=cover` and `env(safe-area-inset-*)` so the tab bar clears the home indicator. |
| **Motion** | Short and reduced when the user asks for less (the stylesheet already honours it). |
| **Theme** | **One theme: the blue one (today's "midnight", the default).** Graphite (green) and Ember (orange) are removed, with the swatches, the theme script and the stored choice. The colours stay design tokens in `:root`, so a second theme could return later without a rewrite. The print styles stay. |

## 9. Behaviour on the phone

- **Installable web app:** a manifest (name, icons, colours, standalone display) so "Add to Home Screen" opens it full screen, without the browser bar. A minimal service worker caches only the static files (CSS, icons, the htmx script), **never** pages or data.
- **Share a link to the app (Android Chrome):** a Web Share Target, so "Share → Saxobeat" from the LinkedIn or browser app lands on the "add a job" sheet with the link filled in. iOS does not support share targets: there, the "+" sheet with a paste field is the way, and it says so in one short line.
- **Speed:** the first inbox page under 100 KB of HTML; the next page appended in place; htmx **served from the app** (today it is loaded from a CDN, unpkg, on every page, a slow and fragile dependency).
- **Waking up:** the hosted free tier sleeps when idle, so the first visit can take about a minute (DEPLOY.md). The phone shows a short "Waking up…" screen instead of a blank page. A paid plan removes the wait: that is a hosting decision, outside this PRD.
- **Language:** every new string exists in French and English before it ships. Shorter copy (§10) means fewer strings overall.

## 10. Words: copy rules

1. **Labels are 1–3 words.** Buttons are one verb: "Shortlist", "Applied", "Dismiss", "Filter".
2. **Sentences are at most 12 words**, and a screen shows no explanatory paragraph by default. Explanations live behind **ⓘ** in one shared help sheet.
3. **Numbers before words:** "238 hidden below 35", not "Jobs scoring below 35 are kept out of this list".
4. **Do not repeat the page.** No "Inbox" heading under a tab named Inbox, no "Search breadth:" label before a control that says Balanced.
5. **No vocabulary of the machinery on candidate screens** (the existing test keeps operator words out).
6. **Word budgets for the first screen:** Inbox about 40 words, Job page about 60, Pipeline about 40.

| Today | On a phone |
|---|---|
| "Jobs scoring below 35 are kept out of this list: they are in Filtered out & archive, under Low score. Type 0 in Min score to see them here." | "238 hidden below 35 · Show" |
| "Search breadth: Strict / Balanced / Broad · details" | A segmented control inside Filters |
| "Clear the noise: dismiss all new jobs scoring below [35] Dismiss" | Laptop only |
| "j/k move · s shortlist · d dismiss · o open · Enter details" | Shown only with a keyboard |
| "Drag a card to another column to change its status; every change is recorded in the job's history. The board fills the window…" | Nothing (the control is obvious); "Move to…" in the card menu |

## 11. Technical approach

- **One set of templates, responsive.** No separate mobile templates: they would drift. Where the *structure* differs between a phone and a laptop (a table versus cards, columns versus a stage switcher), the markup is the card or list form and the **CSS** makes it a row layout at 900 px and above.
- **Mobile-first CSS.** `app.css` is rebuilt with design tokens (colours, spacing, radius, type), mobile defaults and `min-width` breakpoints at 640 and 900 px, in the same single file (or a base file and a components file), no build step.
- **Server-rendered with HTMX**, as today. Paging, the filter sheet's apply, accordions and "Move to…" are HTMX partials or plain forms; the app works with a normal page load when scripts fail.
- **Bottom sheets** use the native `<dialog>`; **swipe** is a small pointer-events script (about 1–2 KB) with `touch-action: pan-y` and a visible fallback for every action; **paging** is `hx-trigger="revealed"`.
- **Inbox query:** the `[:200]` slice becomes a page parameter (30 per page) with a count that stays exact.
- **The pipeline board and the Sankey stay for laptops;** the phone gets the stage switcher and the bars, built from the same `PipelineStats` and `Intake` data (no second source of numbers).
- **Static files:** htmx is vendored under `jobs/static/`; the manifest, icons and the service worker are served from the root scope.
- **Tests:**
  - Template tests: no `<table>` in a candidate list; the first screen's word budgets; no operator vocabulary on any candidate page (exists).
  - A **mobile check** run in the browser pane at 360, 375, 390 and 430 px on every candidate page: no horizontal scroll (`scrollWidth ≤ innerWidth`), no tap target under 44 px. Whether to automate it with a headless browser as a development-only dependency is decision D6.
  - The existing 965 tests keep passing at each milestone.

## 12. Phases

| Phase | Content | Done when |
|---|---|---|
| **M0 — Foundations and quick wins** | Design tokens and the mobile-first stylesheet; the bottom tab bar and top bar; the More screen (language, log out); remove the Graphite and Ember palettes, the swatches and the theme script; htmx served locally; the shared bottom sheet, toast and chip components; hide keyboard hints, CSV, bookmarklet and "clear the noise" on touch. | Every candidate page shows the new shell at 375 px and nothing scrolls sideways. |
| **M1 — Inbox** | Table to cards; two-chip rule; filters sheet and active-filter chips; swipe with undo; "238 hidden" line; paging by 30; the "+" add sheet. | 20 jobs can be triaged in under a minute; first card within the first screen; first page under 100 KB. |
| **M2 — Job page** | Hero with three chips; the fixed action bar that follows the status; accordions with one-line summaries; the shared "Why this score" sheet; the "⋯" sheet. | Collapsed page at most about 2,400 px; apply and mark applied without scrolling. |
| **M3 — Pipeline and interviews** | Stage switcher; compact cards; the To do card and list; "Move to…"; Interviews as a "next up" list; the "How it went" segmented control. | Every status change possible by touch; the next interview visible on the first screen of Interviews. |
| **M4 — Insights, companies, settings, first run** | Tiles and the bar view under 640 px; ⓘ help sheets; settings as a list of screens; sign-in, invitation and first run tidied. | Every candidate action possible on a phone except the laptop-only list in §7.1. |
| **M5 — Installable and share** | Manifest, icons, minimal service worker, share target (Android), the "Waking up…" screen; a final copy pass (FR and EN). | "Add to Home Screen" works; sharing a link from the LinkedIn app adds the job (Android). |

**M0 built (23 October 2026).** One blue theme (Graphite, Ember, the swatches, the theme script and the stored choice are gone); a top bar and a bottom tab bar (Inbox, Pipeline, Interviews, More) under 900 px, the top navigation from 900 px with the language in a small menu; the **More** page (`/more/`: Companies, Contacts, Insights, Filtered out & archive, Settings, language, log out, and the operator's pages for the operator); htmx served from the app (`htmx.min.js` 2.0.4, checked against htmx's published SRI hash); `ui.js` with the shared **bottom sheet** (`<dialog class="sheet">`, opened by `data-sheet`), **toast** (`toast(message, {action, onAction})`) and menu closing; the **chip** component; touch rules (44 px targets on coarse pointers, 16 px fields on phones, safe areas); the export button, bookmarklet, bulk dismissal and keyboard hints marked for laptops only; wide tables scroll inside themselves. Measured at 375 px on 18 candidate pages with the real data: **none scrolls sideways.** Not in M0, on purpose: the tab badges (new today, follow-ups due, upcoming) come with the screens that own those numbers (M1 and M3); the headless-browser check (D6) is still manual, run in the browser pane.

**M1 built — the inbox.** The table is a list of cards (`_row.html`): score, title with the dream heart, company · city, **two chips at most** (the verdict, people you know, work mode, pay, "new": `card_chips`). Swipe right to shortlist, left to dismiss, with a 5-second **Undo** (it takes the change out of the history as if it never happened: action `undo`) and **"Why?"** (the reason is added to the dismissal afterwards: action `dismiss_reason`). From 900 px the same markup is the row of before, with its buttons and the j / k / s / d / o keys; the buttons now use the same Undo and "Why?" flow, so the per-row "why?" menu is gone. **Filters** are one sheet (Breadth as a segmented control, Min score, Added, Salary stated, English-speaking, Hide reposts, Sort, Employers) with the filters in use as chips that remove themselves; on a laptop the same fields are inline. "238 hidden below 35 · Show" replaces the paragraph. Pages of **30 jobs**, the next page appended as the end comes into view. The **+** opens the "add a job" sheet. The employer list is fetched when its panel opens: it was most of the page's weight. First page: **98 KB** (was 536 KB for 200 rows; 169 KB before the employer list moved), 30 cards in about 4,100 px (was 52,783 px for 200 rows).

**M2 built — the job page.** A hero (title, place, signals, the score, the verdict, when it was posted), a **fixed action bar** whose main button follows the status (new: Open posting · Shortlist; shortlisted: Open posting · Applied; applied: Add a stage; interviewing: Cheat sheet · Add a stage), a "⋯" sheet that is the laptop's inline row of actions, and **sections that fold with a one-line summary** (Follow-up, Summary, Why this score, Description, Interviews, Notes, What I sent, People you know, Status history), ordered and opened by status (`SECTION_ORDER` in the view). Collapsed, the page is **815–1,281 px tall** (was 8,202 px). A laptop opens every section on load.

**M3 built — pipeline and interviews.** The pipeline shows **one stage at a time** (a stage bar with the counts; `?stage=`), cards with a "⋯" that opens **Move to…** (with an Undo), the To do card opening a list with its "Follow up" buttons; dragging stays for laptops. Interviews lists **Coming up first**, and its tables become cards on a phone; the outcome of a stage ("How it went") is a segmented control. The **tab bar's numbers**: new jobs found today (Inbox), what needs a nudge (Pipeline: quiet applications, due follow-ups, interviews within 48 hours), stages still to come (Interviews).

**M4 built — insights, companies, settings, sign-in.** Insights opens on three numbers (landed, above 50, applied) with the period chips; the two diagrams are drawn for 640 px and wider, and a **list of bars** (`sankey.bars`, the same data) takes their place on a phone; every explanation is behind an **ⓘ** that opens a sheet (`_help.html`). Settings is a list of groups that fold (one open at a time on a phone, all open on a laptop, a link to a field such as `#max_age_days` opens its group) with one save button that stays in reach. Companies has a search field and ⓘ help; the company page's tables become cards. Sign-in and join use phone keyboards (`inputmode="email"`, no auto-capitalisation).

**M5 built — installable.** A web **manifest** (`/manifest.webmanifest`: standalone, the blue theme, three icons, the share target), icons drawn by `scripts/make_icons.py` (no library), and a **service worker** (`/sw.js`, scope: the whole site) that stores only static files (network first) and never a page or data. When the host does not answer a page within four seconds it shows **"Waking up…"** (`waking.html`, English or French), which reloads the page as soon as `/healthz` answers. On Android, **sharing a link to the app** (`/share/`) opens the inbox's add sheet with the link filled in; iOS has no share targets, so there the paste field is the way (the sheet says "Paste the link of the posting.").

**What differs from the plan above.** (1) The search field is always on screen, next to the Filters button, rather than opening from a 🔍: one tap less. (2) The score chip opens the "Why this score" **section** of the job page, not a separate sheet. (3) Row buttons on a laptop and the swipe share one flow (Undo and "Why?"). (4) The tab badges and the help sheets were added where the numbers and the text live (M3 and M4). (5) The headless-browser check (D6) is not installed: every phase was measured by hand in the browser pane (overflow, 44 px targets, heights), and the service worker's logic has a Node test (`tests/js/sw_test.js`, run by pytest when Node exists) because the pane cannot register a worker. (6) Contacts, My CV and the first-run screens were already one column: they only got the touch rules.

**Measured at 375 px with the real data (23 October 2026).** No candidate page scrolls sideways (18 pages checked). No button, field or tab under 44 px on the pages checked after the last fix. The first inbox card starts about 123 px under the top bar; a card is 92–112 px; the first page weighs 98 KB. Job pages: 815–1,281 px collapsed. Word budgets (Inbox 40, Job page 60, Pipeline 40) are enforced by tests. 955 strings translated; 1,023 tests pass.

Order matters: M0 and M1 alone remove most of the pain (the sideways scroll, the clutter above the list, the table). Each phase is shippable by itself, and the laptop layout is checked at the end of each one.

## 13. Decisions (confirmed 23 October 2026; D3 changed from the recommendation)

| # | Question | Recommendation |
|---|---|---|
| D1 | Bottom tabs: **Inbox · Pipeline · Interviews · More**? Or fold Interviews into Pipeline? | Keep Interviews as a tab: it is the time-sensitive screen. |
| D2 | Swipe to triage, with an Undo toast and the visible equivalents? Plus a "buttons on cards" setting? | Yes to swipe with Undo; add the setting only if a friend asks for it. |
| D3 | Colour themes? | **Decided: a single theme, the blue one (midnight); Graphite and Ember are removed.** |
| D4 | Pipeline on a phone: stage switcher, no drag and drop? | Yes. |
| D5 | Installable app and Android share target in this PRD (M5)? | Yes, last. iOS keeps the paste field. |
| D6 | A development-only headless browser (Playwright) to automate the no-sideways-scroll and tap-size checks? | Yes: it is the only guard against regressions on 9 pages. It does not ship to Render. |
| D7 | Laptop navigation: keep the top bar as is? | Yes, with the language switch folded into a small menu. |
| D8 | Insights on a phone: bars instead of the Sankey under 640 px? | Yes. |
| D9 | Word budgets (§10) as a rule, with a template test? | Yes, for the three first screens. |
| D10 | Review the French copy myself, screen by screen, before each phase ships? | Yes: the shorter strings are the ones friends read first. |

## 14. Acceptance (the whole PRD)

At 360 × 740 and 390 × 844, with the real data:
1. **No candidate page scrolls sideways**, and no control is under 44 × 44 px.
2. **Inbox:** the first job card begins within 130 px of the top bar; each card is at most about 112 px; the first page is under 100 KB; shortlist and dismiss are one gesture each, with Undo.
3. **Job page:** collapsed, at most about 2,400 px tall; the primary action is always on screen; "Applied" and "Open posting" need no scroll.
4. **Pipeline:** one stage per screen; any job can be moved by touch; the To do list opens in one tap.
5. **Interviews:** the next stage is the first thing on the screen; adding a stage takes two taps from a job.
6. **Insights:** readable without a diagram wider than the screen.
7. **Words:** the first screen of Inbox, Job page and Pipeline stays within the word budgets of §10.
8. **Both languages** complete for every new string; the operator vocabulary stays out of candidate pages.
9. **Laptop (1280 px):** the keyboard shortcuts work; the layout is at least as dense as today; the Sankey and the board are unchanged.
10. All tests pass, and the page weights are as in the targets above.

## 15. Risks

| Risk | Mitigation |
|---|---|
| **A swipe dismisses a job by accident** | A threshold and a colour reveal; the 5-second Undo; a dismissed job is never deleted (it stays in the archive, as today). |
| **The laptop experience gets worse** | Desktop checks at the end of every phase; the row layout, the board, the Sankey and the shortcuts stay at 900 px and above. |
| **A rewrite of nine templates and their tests** | Phased, shippable by phase; M0 and M1 first; the same view code and the same data. |
| **French copy slips** | The existing completeness test blocks a phase until every string is translated; D10. |
| **Hosted cold start looks like a slow app on a phone** | The "Waking up…" screen; the paid plan if friends complain (outside this PRD). |
| **Gestures conflict with the browser** (back swipe on iOS, pull to refresh) | `touch-action`, a swipe threshold away from the screen edge, visible alternatives. |
| **A CDN dependency (htmx) breaks the page** | Vendor the script (M0). |
| **Scope creep into new features** | §3: this PRD changes presentation and reach, not capabilities. |

## 16. Success measures

- **Timed with the owner and two friends:** 20 jobs triaged in under a minute; "shortlist → applied" from a job in under 15 seconds.
- **No friend asks "where is…?"** for the six main actions of §4 within the first session.
- **Page weight and height** at the targets of §14.
- **Phone share of visits** (counted from request logs, no tracker): it rises once the phone experience is good.

## 17. References in the repository

- Navigation and shell: `jobs/templates/jobs/base.html`; styles: `jobs/static/jobs/app.css` (14.7 KB, one media query).
- Inbox: `inbox.html`, `_row.html`, `_filters.html`, `_score.html`, `_ai_badge.html`, `_bookmarklet.html`; the view `inbox` in `jobs/views.py` (slice `[:200]`).
- Job page: `detail.html` and its includes (`_signals.html`, `_employer_note.html`, `_contacts_card.html`, `_interview_card.html`, `packet.html`).
- Pipeline and follow-ups: `pipeline.html`, `followup.html`; Interviews: `interviews.html`, `cheatsheet.html`; Insights: `insights.html`, `_sankey.html`, `services/sankey.py`.
- Settings and first run: `settings.html`, `welcome*.html`, `cv.html`; accounts: `login.html`, `join.html`.
- Measured on 23 October 2026 by rendering the candidate pages with the real data at 375 × 812 px in the browser pane (temporary files, deleted afterwards).
