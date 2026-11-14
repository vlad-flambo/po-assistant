# Revolut People probe, 2026-11-03

What was run (about 25 requests in all, none writing anything; no login, no key, no cookie). Source: claude, 2026-11-03.

## 1. The link is a Revolut People career site

`https://people-jobs.com/worklife/apply/f42653cb-a3e5-4cd0-b273-d7c995f6c998?utm_source=linkedin&utm_campaign=revolut_people`

| Check | Result |
|---|---|
| `people-jobs.com` page source (3.3 KB) | an empty iframe; a script maps host `people-jobs.com` to origin `https://revolutpeople.com` and loads `https://revolutpeople.com/<tenant>/public/careers/<path>`; the tenant is the first path segment (`worklife`) |
| Page `Content-Security-Policy` | names `revolutpeople.com`, `aqueduct.revolut.com`, `revolut.okta.com` |
| Application form footer (read in the browser pane) | "Powered by Revolut People" |
| Page title | "Head of Product (H/F) - 78k€ à 87k€ \| Careers at Worklife" |

So: yes, Revolut People. The employer is **Worklife** (a French employee-benefits platform, office in Paris), a *customer* of the product. The link is not Revolut's own hiring.

## 2. The public API behind it

The page calls these (read in the browser's network log), all `GET`, JSON, no authentication:

| URL (`https://revolutpeople.com/api/<tenant>/external/...`) | Gives |
|---|---|
| `v2/postings` | the list: `id`, `title`, `locations[{name,type,country{name}}]`, `function{name}`, `is_featured` (Worklife: 4 postings) |
| `v2/postings/<id>` | the detail: the same plus `description` (HTML), `creation_date_time` (here `2026-10-01T11:01:03Z`), `type`, `presentation_video_url` |
| `v2/postings/careerPageSettings`, `v1/careersPages`, `v2/postings/applicationFormSettings` | page settings (slogan, logo, form fields) |

- Both `postings` endpoints answer **plain `curl` (HTTP 200, JSON)** too, not only the browser. The HTML pages on `revolutpeople.com` sit behind a Cloudflare challenge (HTTP 403, `Cf-Mitigated: challenge`), the API does not.
- The public address of a posting: `https://people-jobs.com/<tenant>/apply/<id>`.
- An **unknown or private tenant** answers HTTP 403 `{"detail": "Invalid token"}`, the same for `revolut`, `revolutpeople`, `nonexistentzzz` and so on. A real tenant answers 200. So a tenant can be found only by guessing its slug (or reading it from a link such as this one).
- Salary is only in the title text ("78k€ à 87k€"), not a structured field (as seen on 4 postings).
- Not verified: the platform's terms of use, rate limits, other tenants' shapes (only `worklife` was read).

The four Worklife postings, 2026-11-03: RevOps (55-60k€ + variable), Senior Backend Engineer (65-70k€), Customer Success Manager (44-48k€ + variable), Head of Product (78-87k€). All Paris.

## 3. Revolut's own jobs are not behind that API

- `https://revolutpeople.com/api/revolut/external/v2/postings` answers 403 "Invalid token", exactly like a made-up tenant.
- `https://www.revolut.com/careers/` is a separate Next.js site. In a real browser it holds **all 291 open positions in its page data (`__NEXT_DATA__`, 251 KB)**, 7 of them in Paris, each with `id`, `text`, `locations`, `team`. Its network log shows no call to revolutpeople.com.
- Plain HTTP to `revolut.com/careers` gets the Cloudflare challenge ("Just a quick security check", HTTP 403, `Cf-Mitigated: challenge`, checked twice). This matches the existing line in `docs/unsupported_employers.csv` (blocked since 2026-10-08).
- The posting shape (`id` UUID, `locations[{name,type,country}]`) matches Revolut People's, so the back end is probably the same product; there is no public door to it for Revolut itself.

Revolut's Paris openings seen in the browser, 2026-11-03: Head of Business Lending (Credit), Head of Lending (Mortgages) (Credit), Head of Capital Management - Western Europe (Finance), Operations Manager (Banking) (Operations), FX Forwards Product Sales Executive (Italian Market) (Sales), FX Forwards Product Sales Executive (Sales), Product Sales Executive (SMB Field) (Sales).

## 4. How many employers in Saxobeat's lists use it

- `data/*.csv` (250 employers in `employer_careers.csv`, plus the coverage lists): 0 mention `people-jobs` or `revolutpeople`.
- Web search found no customer list. Revolut's launch material says the product is for small and medium businesses with a registered entity in Europe or the UK (third-party summary, date unclear), and that it has a built-in careers portal and LinkedIn posting (Revolut blog post of May 2024).
- Not measurable cheaply: the tenants that exist (a guess-the-slug probe of 250 names would be 250 requests to a third party for a near-certain handful of hits).

## 5. robots.txt (read after the build, 2026-11-03: should have been read first)

`https://revolutpeople.com/robots.txt`: `User-agent: *`, `Allow: /public/careers`, `Allow: /public/terms-and-conditions`, `Allow: /public/privacy-notice`, `Allow: /$`, `Disallow: /`. `https://people-jobs.com/robots.txt`: the same three allows and `Disallow: /`.
The API (`/api/<tenant>/external/...`) and the tenant pages (`/<tenant>/public/careers/...`) are not allowed. Sections 1 to 3 above (about 25 requests) and the 10 requests of the scratch live read were made before this was read. See [../verify.md](../verify.md).
