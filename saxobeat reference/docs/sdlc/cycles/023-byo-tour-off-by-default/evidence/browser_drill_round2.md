# Browser drill, round 2, 2026-11-04 (slice 8)

Where: the in-app browser with the **mobile preset** (375x812, Android user agent, touch points on), `http://localhost:8766`, the same scratch SQLite file and test user as round 1
(never `data/saxobeat.db`, never Neon). The script served was the round 2 `ui.js` from disk. Every step starts from "no tap": page 1 is only loaded, never touched.

| Step | flag | tutorial hidden | aria-expanded | Criterion |
|------|------|-----------------|---------------|-----------|
| Flag cleared, load /job/2/ (page 1), **no tap** | "1" (set at once) | false (open) | true | 1 |
| Load /job/3/ (page 2), no tap | "1" | true (closed) | false | 2 |
| Load /job/2/ again (page 3), no tap | "1" | true (closed) | - | 2 |
| ⓘ activated: opens | "1" | false | true | 4 |
| ⓘ activated again: closes | "1" | true | false | 4 |
| ⓘ activated: opens, then reload /job/2/ | "1" | true (closed) | - | 4 |

The screenshot of page 1 on the phone preset showed the box lying over the page, which is what the owner saw.

Limits: a pointer click on ⓘ failed twice because the pane did not draw (screenshot timeout), so the ⓘ steps above were done with `element.click()` from the page (the same `click` event the handler listens to), not a touch gesture. Button taps (criterion 3) were not repeated in the browser: since the flag is now set when the box opens, a tap cannot change the outcome; the Node cases 3 cover them. Storage blocked (5) and the hover popover (6) were not tried in the browser.
