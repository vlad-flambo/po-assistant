# Intent: international destinations chosen individually (narrowed: edit the cities in Settings in standard mode)

| | |
|---|---|
| **Cycle** | 030 |
| **Stage** | Intent |
| **Date** | 2026-11-06 |
| **Owner** | Vlad |
| **Importance** | 5/5 (owner, 2026-11-06): "high priority feature, 5/5"; claude's first read: reach is every standard-mode candidate, who cannot change their places from Settings |

<!-- Importance, 1 to 5: 5 critical (data, hosting, or nothing works without it), 4 high (blocks other work or a core flow), 3 useful, 2 minor, 1 marginal. Claude assesses it first; the owner overrules it by writing "(owner, date)". To dismiss the cycle, add a row "| **Status** | Dismissed YYYY-MM-DD by the owner: <reason> |" to the table above (see the skill). -->

## The request, in your words
First message (2026-11-06):
> high priority feature, 5/5, new intent
> when new candidates are onboarded, they are only asked if they are considering international options.
> however, this is too wide a definition, and impossible to change afterwards.
> In case of open to international. candidate should be given the currently supported destinations: paris/idf/hk/sg to be ticked individually, with paris/idf ticked by default
> afterwards, candidate should be able to edit in setting, same as a power user

Second message, narrowing it:
> mea culpa, it's already done.
> add just the editability of the cities to standard same as power mode

## Why now / the pain
- The onboarding choice of places already works (owner, 2026-11-06). What is missing is changing it afterwards from Settings: standard mode shows no Settings form at all, so the only way back is the guided "What I'm looking for" questions (`jobs/templates/jobs/settings.html:6,21`).
- No count of affected candidates yet.

## Goal
A standard-mode candidate can see and change their cities and the three remote options (remote anywhere in France; extra cities for remote roles only; remote only) from the Settings page, the same boxes a power user has, and what they save is what the inbox filters on.

## Success measure
(Proposed; to be confirmed by the owner.)
1. In standard mode, Settings shows the Cities ticks (the registry's cities, the candidate's current ones ticked), "Accept remote roles anywhere in France", the extra remote-role cities ticks and "Remote only". Saving changes `filters["cities"]`, `["remote_france"]`, `["remote_cities"]` and `["remote_only"]` and the inbox follows (drill on a local copy: a job outside the new places is hidden with the reason shown, one inside comes back; a remote role in France shows or hides with the tick; an on-site posting is dropped with "Remote only" on and returns when it is off).
2. Saving touches nothing else: keywords, blocked words, minimum score, maximum age, languages, salary floor and the other filters a standard user never sees are unchanged (the reason the whole form is hidden today, `jobs/views.py:1009-1010`).
3. The power-mode Cities box and the guided "Where?" answer stay in step with it (one stored list, no two that disagree).
4. A candidate who saves with nothing ticked is told that means no location limit (same wording as the power box).

## Not doing (this cycle)
- The onboarding choice itself (done, owner).
- Showing the rest of the power settings to standard mode.
- Adding destinations; changing how a job's location is matched to a city.
- Anything on the hosted database before the owner approves a plan.

## What we already know (facts, with where they came from)
- The city registry: `paris`, `ile_de_france`, `london`, `hong_kong`, `singapore`; default `["paris"]` (`jobs/cities.py:23-60`, read 2026-11-06). The guided "Where?" question already lists them all as chips (`jobs/templates/jobs/ask.html:27`). I did not find in the code a separate "international" yes/no; the chosen answer is stored as `filters["cities"]`.
- Power mode's Cities box is `settings.html:72-73`; its save writes `cities` and `remote_cities` together with every other field in one form (`jobs/views.py:1018-1031`), and standard mode's POST to Settings is refused so an old page cannot blank unseen fields (`views.py:1009-1010`).
- "Ticked by default" today: `ask.html` pre-ticks the saved cities, else `["paris"]` only, not Île-de-France (`jobs/views_cv.py:203`). Not part of this cycle unless the owner says so.
- Correction (2026-11-06): the plain power-form save starts **no** recompute; it says "Use the buttons below to apply them" (`views.py:1047`). Only the Search-breadth dial calls `recompute_in_background` (`views.py:1053`). Standard mode has none of the apply buttons, so the new save must start the recompute itself (see spec).
- The guided "Where?" question pre-ticks `candidate.preferences["cities"]` before the Config's cities (`jobs/views_cv.py:203`), so a Settings save must update both or the two pages disagree.

## Open questions (grilled one at a time)
| # | Question | Recommended answer | Answer | Status |
|---|----------|--------------------|--------|--------|
| 1 | "Same as power mode": only the Cities ticks, or also the remote options? | Only the Cities ticks | **Also the remote options** (owner, 2026-11-06). Read as: "Accept remote roles anywhere in France" and "Also accept these cities, for remote roles only". "Remote only" (drop on-site/hybrid postings) is not named; see Q3 | answered |
| 2 | Where on the page: a small card of its own with its own Save, above the AI and language cards? | Yes, its own card and Save, so it never touches the power form | **Yes, its own card** (owner, 2026-11-06) | answered |
| 3 | Does "remote options" also include the "Remote only" tick (drops postings explicitly on-site or hybrid)? | No: it is a filter on the kind of job, not a place; keep it power-only | **Yes, include it** (owner, 2026-11-06). So standard mode gets all four place and remote ticks of the power form | answered |

Status: `open`, `answered`, `parked` (deliberately left for later).

## Constraints and risks
- A changed city list hides or shows jobs at once through the filter; the save must refilter and recompute like the power save does.
- Mobile first and the house design system (house-stack): chips, one blue theme.
- Viewing as a candidate: the operator must not be able to change someone's places by accident (the page already disables other buttons in that case).

## Gate
- [x] All open questions answered or parked
- [x] Goal and success measure confirmed by the owner (2026-11-06)
