# iCloud test e-mail: landed in spam (2026-11-03)

Source: **the owner, in chat, 2026-11-03.** Claude has not seen the message or its headers.

| What | Result |
|---|---|
| Test e-mail from the console to an `icloud.com` address | Arrived, **in the spam folder**; "well received otherwise" (owner's words) |
| E-mails page the same morning | "0 of 300 sent today · provider brevo · from Saxobeat <no-reply@mail.saxobeat.fr> · links to https://app.saxobeat.fr. Last 7 days: 5 sent, 1 failed, 0 waiting." |
| Header lines (SPF, DKIM, DMARC) | **Not seen.** Asked for, not given |
| Which address the console was opened on when the test was sent | Not said (matters for criterion 19: a form that worked on `app.saxobeat.fr`) |

**Reading:** the message is delivered, not refused, so Brevo's side and the authentication are good enough for Apple to accept it. Spam placement is the usual first result for a days-old sending domain with no history; it is not shown to be an authentication fault until the headers say so. Not proven either way.

**The counts changed:** on 2026-11-02 the page read 5 sent, 0 failed, 1 waiting; on 2026-11-03 it reads 5 sent, 1 failed, 0 waiting. The waiting e-mail was retried and gave up (an e-mail is kept and retried up to three times, then *failed*). Its kind, address and error text are **not known** (asked 2026-11-02 and 2026-11-03). The iCloud test is not visible as an extra *sent* row in these figures; unexplained.
