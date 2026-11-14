# Decisions: Revolut People source

One entry per decision, newest last. Do not edit old entries: add a new one that supersedes.

## D1. Read the Revolut People API although robots.txt disallows it, for tenants the owner opts in
- **Date:** 2026-11-03
- **Context:** `revolutpeople.com/robots.txt` and `people-jobs.com/robots.txt` say `Disallow: /` (only `/public/careers`, terms and privacy allowed). The project's rule for a site's own interface is to obey robots.txt (Capgemini, Phenom, Jibe adapters). The adapter followed it and refused (verify.md). The API is the one the public career page itself calls for every visitor; no login, no key.
- **Options considered:** (a) leave the source inert, (b) remove the code, (c) override the rule.
- **Decision:** (c), by the owner ("Override the rule", 2026-11-03), against my recommendation (a).
- **Why:** the owner's call: it is their project and their job search; the data is public job ads, five requests per run, honest user agent, no login or access control bypassed.
- **Consequences:** the override is **per source, explicit and visible**: the adapter obeys robots.txt unless the source's config has `"ignore_robots": true`; Worklife is seeded with it, so the default for any other tenant stays "obey". The override is written in the adapter's docstring, the seed comment and here. Not changed: the shared `robots.allowed` check and every other adapter. The source stays **switched off** until the owner enables it (and the terms of use are still unread: owner). If revolutpeople.com asks us to stop, or robots.txt/terms change, remove the flag or the source. Rate: no more than the current 5 requests per run with a 0.5 s pause.
