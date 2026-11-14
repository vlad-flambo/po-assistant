# Browser check, 2026-11-04 (criterion 10)

Local server (`scripts/dev_server.py`, port 8791) on a throwaway SQLite database made for this check (an operator, one candidate, a failed source run, a source proposal, one new feedback, two AI tasks, a runner report), `SAXOBEAT_MAIL=console`, `SAXOBEAT_RUN_SOURCES=0`. No hosted database or mail provider was touched. Signed in as the throwaway operator in the Browser pane.

Measured in the page with JavaScript, per page, at **800 px** (all 15 console pages) and **1280 px** (E-mails; bar height):

| Check | Result |
|---|---|
| Horizontal overflow of the page (`scrollWidth - clientWidth`) | 0 on all 15 pages at 800 px, 0 at 1280 px |
| Exactly one `h1` and a `p.purpose` | yes on all 15 |
| Area marked in the bar | Today, Candidates, Sources (Sources and Jungle), Runs, Feedback, AI (Export, Import, Queue, Settings, Instructions), More (E-mails, Exports, Auto-reject, Data) as in the spec |
| Second row | 4 tabs on AI and More, 2 on Sources, none on the other four; the right tab marked (Instructions marks Settings) |
| AI status strip | on the five AI pages, absent elsewhere |
| Bar height | one row (55 px) at 1280 px; at 800 px the right side ("← Candidate app", "Log out") wraps to a second row (about 96 px): the 7 areas need about 690 px and the whole bar about 905 px |

Screenshots: `today-1024.jpg`, `ai-export-800.jpg` (shows the wrapped right side and the strip), `more-emails-1280.jpg`.

Not seen or not traced:
- The browser console shows repeated "An unknown error occurred when fetching the script" on every page and one X-Frame-Options refusal from my own first (abandoned) iframe measurement. The dev server log shows no 5xx and no traceback, only a 404 for `/favicon.ico`; the script error was not traced to a request, and was not compared with the old Console.
- The Export page's candidate table is wider than its card at 800 px (it clips inside the card). That is the page as it was before this cycle, not caused by it.
- The live site was not visible (it needs a login); the owner checks it after deploy (slice 8).
