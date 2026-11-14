# DNS check for the new sending domain (2026-10-30, about 16:30 Paris time)

Read-only lookups from the owner's PC (`Resolve-DnsName -DnsOnly`), after the owner said the Brevo account was set up with `mail.saxobeat.fr` (decisions.md D1). Nothing was changed. The DKIM public keys are public and left out here.

| Name | Type | Answer | What it is |
|---|---|---|---|
| `saxobeat.fr` | NS | `ns1103.ui-dns.biz`, `ns1050.ui-dns.org`, `ns1069.ui-dns.com`, `ns1056.ui-dns.de` | The DNS is hosted at IONOS |
| `saxobeat.fr` | MX | `10 mx00.ionos.fr`, `10 mx01.ionos.fr` | The owner's own mailbox on the root domain, at IONOS |
| `saxobeat.fr` | TXT | `v=spf1 include:_spf-eu.ionos.com ~all` | SPF of the IONOS mailbox (not touched) |
| `saxobeat.fr` | TXT | `brevo-code:ab5e3d5a7ad47a4bf7b28605f75d9b4a` | Brevo's ownership code for the domain (a public verification value, not a secret) |
| `mail.saxobeat.fr` | CNAME | `mail-saxobeat-fr.brand.brevosend.com` | The sending subdomain, handed to Brevo |
| `mail-saxobeat-fr.brand.brevosend.com` | TXT | `v=spf1 include:spf.brevo.com -all` | The SPF the CNAME brings with it |
| `mail.saxobeat.fr` | MX (through the CNAME) | `10 return-path.mx.brevosend.com` | Where bounces go: to Brevo |
| `brevo1._domainkey.saxobeat.fr` | CNAME | `b1.saxobeat-fr.dkim.brevo.com` → `brevo9.dkim.brevo.com` (TXT `k=rsa;p=…`) | First DKIM key |
| `brevo2._domainkey.saxobeat.fr` | CNAME | `b2.saxobeat-fr.dkim.brevo.com` → `brevo10.dkim.brevo.com` (TXT `k=rsa;p=…`) | Second DKIM key |
| `_dmarc.saxobeat.fr` | TXT | `v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com` | DMARC on the root; it covers `mail.saxobeat.fr` by inheritance (no `sp=`), policy `none`, reports go to Brevo |
| `_dmarc.mail.saxobeat.fr` | TXT | none | No own record for the subdomain |
| `brevo1._domainkey.mail.saxobeat.fr`, `mail._domainkey…` and similar | CNAME, TXT | none | The DKIM names are under `saxobeat.fr`, not under the subdomain |
| `jobs.saxobeat.fr` | CNAME | none | The app has not been moved (as the owner said) |

**What this shows:** Brevo's records for the sending domain are all in place and resolve (CNAME for SPF and return-path, two DKIM CNAMEs, the ownership code, a DMARC `p=none`).

**What it does not show:** that Brevo itself says "Authenticated" (only the owner can see that); that a message is signed and passes at Gmail and Outlook (slices 8 and 9); the plan's limits.

**What it implies (to be confirmed by the first test's headers):** the DKIM keys are named under `saxobeat.fr`, so Brevo probably signs with `d=saxobeat.fr`. DMARC then passes by relaxed alignment with the sender `mail.saxobeat.fr` (same organisational domain). The spec no longer expects `header.d=mail…`.

**A choice the owner has to make (decisions.md D2, open):** the DMARC record sits on the root and its reports go to Brevo, not to the owner (Q3 had said "reports to the owner"). It also applies to the owner's own IONOS mailbox, which is harmless at `p=none` but matters if the policy is tightened later.
