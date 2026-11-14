# Browser drill, 2026-11-04 (slice 4)

Where: the in-app browser, desktop viewport 1024x768 (not a phone; not a touch device), `http://localhost:8766`, a scratch SQLite file in the session scratchpad
(one test user in power mode, two jobs; never the owner's `data/saxobeat.db`, never Neon). The page was served the new script
(`fetch("/static/jobs/ui.js")` contained `if (!tour.hidden) remember(); show(tour.hidden);`). Reads below are `localStorage["saxobeat.byo"]`,
`#byo-tour.hidden` and the ⓘ button's `aria-expanded`, read from the page after each step.

| Step | flag | tutorial hidden | aria-expanded | Criterion |
|------|------|-----------------|---------------|-----------|
| Clean storage, first job page (/job/2/) | null | false (open) | true | 1 |
| Real click on ⓘ to close it | "1" | true | false | 2 (the new behaviour) |
| Another job page (/job/3/) | "1" | true (closed) | false | 2 |
| Click ⓘ on that page to open it by hand | "1" | false | true | 4 |
| Load /job/3/ again | "1" | true (closed) | - | 4 |
| Clear the flag, load /job/3/ | null | false (open) | - | 1 |
| Click the Cheat sheet button, then load /job/2/ | "1" | true (closed) | - | 3 |

Not exercised in the browser: storage blocked (criterion 5, covered by `tests/js/byo_tour_test.js` cases 5a and 5b), hover popover (6, by diff only), a touch device.
