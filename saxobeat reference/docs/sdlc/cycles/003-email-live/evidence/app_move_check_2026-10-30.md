# Slice 7b: first check of the move to `app.saxobeat.fr` (2026-10-30, about 17:30 UTC)

Read-only lookups and requests from the owner's PC, after the owner said "Both added" (the IONOS CNAME and the Render custom domain). Nothing was changed. Decision: decisions.md D4.

| What | Result | Reading |
|---|---|---|
| `app.saxobeat.fr` CNAME, default resolver and `8.8.8.8` | `app.saxobeat.fr -> saxobeat.onrender.com` on both | **DNS is right**, and points at the same Render service as `jobs.stoyan.ovh` (`saxobeat.onrender.com`) |
| Certificate served for `app.saxobeat.fr` (TLS 1.3, `openssl s_client`) | subject `CN=app.saxobeat.fr`, issuer Google Trust Services `WE1`, valid 2026-10-30 16:26 GMT to 2027-01-28 | **Certificate is issued and valid** |
| `https://app.saxobeat.fr/` and `/login/` (`curl`) | HTTP **400**, body Django's own page "Bad Request (400)" (the empty `<p></p>` template) | The request reaches the app over TLS and the app refuses the host name. This is what Django does when the host is not in `ALLOWED_HOSTS`. **The setting is not live yet** |
| `https://saxobeat.onrender.com/` | HTTP 302 to `/login/?next=/` | The service itself is up; its own name is always allowed |
| `https://jobs.stoyan.ovh/` | **TLS handshake failure** on TLS 1.2 and 1.3 (`SSL alert number 40`; `curl` error 35), repeated three times | Render no longer serves a certificate for this name. At 2026-10-30 14:31 UTC it answered 302 with a valid certificate (see intent.md facts). **Something changed on Render since then** |

**What is not known (only the owner can see it):** whether `jobs.stoyan.ovh` was removed, replaced or is re-verifying under Render's *Custom Domains*; whether `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` were saved with the new host and the deploy finished; whether `SAXOBEAT_PUBLIC_URL` is changed.

**How a 400 here differs from the other failures:** a wrong `DJANGO_ALLOWED_HOSTS` gives the 400 seen here; a wrong `DJANGO_CSRF_TRUSTED_ORIGINS` is not visible on a plain page load: pages open and every form (sign-in included) then fails with a 403. Criterion 19 therefore needs a real sign-in, not only a page load.

## Second check, 2026-10-30 17:35 UTC (owner: "should be done now")

| What | Result |
|---|---|
| `https://app.saxobeat.fr/` | **HTTP 302** to `https://app.saxobeat.fr/login/?next=/` (was 400): the host is now allowed on the running service |
| `https://app.saxobeat.fr/login/` | **HTTP 200** |
| Certificate for `app.saxobeat.fr` | unchanged: `CN=app.saxobeat.fr`, Google Trust Services `WE1`, valid to 2027-01-28 |
| `https://saxobeat.onrender.com/` | HTTP 302 to sign-in (still fine) |
| `https://jobs.stoyan.ovh/` | still **HTTP 000** (no certificate, `openssl` cannot read one): not fixed |

**Proven:** the new address resolves, has a valid certificate, reaches the app and is allowed by `DJANGO_ALLOWED_HOSTS`. **Not proven:** that a form works there (`DJANGO_CSRF_TRUSTED_ORIGINS`: it shows only as a 403 when the sign-in form is submitted), that `SAXOBEAT_PUBLIC_URL` is changed (the E-mails page line), and anything about the old address coming back.

**The old address:** D4 says `jobs.stoyan.ovh` stays attached. As of this check it does not answer. No e-mail with a link on it has been sent (only a test e-mail), so nobody is locked out; but it is a departure from D4 and the owner decides whether to re-add it.
