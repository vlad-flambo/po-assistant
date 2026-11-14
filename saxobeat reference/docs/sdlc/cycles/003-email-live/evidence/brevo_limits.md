# Brevo account: what the owner read (2026-10-30)

Source for every line below: **the owner, from the Brevo dashboard, 2026-10-30, in chat.** Claude has not seen the dashboard.

| Item | What was said | Status |
|---|---|---|
| Domain `mail.saxobeat.fr` | "Brevo shows mail.saxobeat.fr as Authenticated" | Confirmed by the owner. Matches the DNS lookup of the same day (`dns_check_2026-10-30_saxobeat_fr.md`) |
| Daily sending limit | "daily 300/day" | Confirmed by the owner. Equals the app's default `SAXOBEAT_MAIL_DAILY_CAP` (300), so that setting needs no change |
| Transactional e-mail through the API | "looks like api is included" | **Partly confirmed:** the owner's reading, not a statement from Brevo's terms. The first test through the API (slice 8) is the real proof |
| Monthly sending limit | not given | Not stated. Not needed at the scale of this cycle (one friend, a few e-mails); the daily limit is the one the app enforces |
| A custom sending domain on the free plan | implied by the Authenticated domain | Evidenced by the domain being authenticated |
| A Brevo footer or logo added to e-mails | not given | **Not known.** It will be visible in the received test e-mail (slice 8): if there is one, it is written here |
