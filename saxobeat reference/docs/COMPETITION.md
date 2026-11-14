# Competitive landscape — Saxobeat

| | |
|---|---|
| **Status** | First version. Research done 9 October 2026 |
| **Date** | 9 October 2026 |
| **Author** | Vladimir (product), written with Claude |
| **Scope** | Tools that help a candidate find and win jobs, as of October 2026, seen from Saxobeat's market: senior profiles in Paris / Île-de-France (fintech, banking, SaaS) |

**How reliable this is.**
- Prices were checked on the vendors' own pages where they are public: Useful Apply, LoopCV (from its price API, called from France), NextRaise, AIJobmatch, Huntr, Careerflow, LazyApply, Kickresume, Jobea, Mon Copilote Carrière.
- Jobright, Simplify, Teal and Jobscan show prices only inside the app or behind a login. Their figures come from 2026 reviews, many written by competing vendors, and are marked **(3P)**.
- **(?)** marks anything that could not be verified.
- Prices are kept in the currency the vendor shows; USD and EUR are not converted.

---

## 1. Summary

1. **Nobody covers Paris the way Saxobeat does.**
   - **Where the others get their jobs:** Jobright lists US jobs only. Useful Apply (formerly KarKo AI) buys Google Jobs results. LoopCV and NextRaise reuse big job boards. AIJobmatch reads US venture-capital portfolio boards. Welcome to the Jungle shows only employers who pay it.
   - **The gap:** no competitor reads French employers' own career pages (Workday, Taleo, SuccessFactors, Talentsoft, Greenhouse, Lever…) and deduplicates them. This is Saxobeat's clearest advantage, and the hardest to copy.
2. **The market has turned against applying on the user's behalf.**
   - **Pushback:** Greenhouse's CEO talks of an AI "doom loop" (254 applicants per job; applications per recruiter up 412%). Greenhouse added identity checks. LinkedIn restricts accounts that use automation.
   - **The best new products now advertise "you click send":** Useful Apply ("we prepare, you send"), NextRaise, Simplify.
   - **For Saxobeat:** its deliberate refusal to auto-apply is now the mainstream position, not a weakness. It is not a differentiator on its own either.
3. **Every competitor scores jobs with an AI model whose reasoning you cannot see.**
   - Saxobeat's rule-based score (keywords + TF-IDF + seniority) can be explained line by line and costs nothing per job.
   - Showing *why* a job scored what it did is the second differentiator. The others need paid credits for it.
4. **The free incumbents are moving in.**
   - **LinkedIn Job Match** launched in French in September 2026, with the best part behind Premium.
   - **HelloWork Coach Emploi** (May 2026), **France Travail MatchFT**, and **Welcome to the Jungle's free AI Candidate Coach**.
   - All are tied to their own job ads. None looks across sources.
   - Indeed Career Scout is not in France yet; it is the main thing to watch.
5. **Prices cluster at $20–40 a month.**
   - **Billing:** the discount usually comes from paying for three months at a time; annual plans are rare, because users leave when they are hired.
   - **Credits:** tools that write applications sell them, at about $0.40–0.80 per application.
   - **French reference points:** LinkedIn Premium about €15–40 a month; French copilots €20–94 a month; outplacement €3,000–25,000.
6. **Ideas worth copying first:**
   - **Score breakdown:** what matches, what's missing, and a verdict on every score.
   - **Fresh / reposted / closed badges.**
   - **A "Strict / Balanced / Broad" dial** that also widens Paris to La Défense, Boulogne and Issy.
   - **A "gone quiet" flag** after 7–10 days, with a follow-up nudge.
   - **A limited "focus" flag,** after Greenhouse's "dream job" feature: those applicants are hired about 5× more often.
   - **Contacts at each company,** from the user's own LinkedIn export.

---

## 2. Who we compare against

| Product | Type | Status (Oct 2026) |
|---|---|---|
| **Useful Apply** (usefulapply.com) | Daily job feed + tailored application kit; never sends for you | Live. **Same company as KarKo AI**, renamed 31 Aug 2026 (karkoai.com redirects) |
| **LoopCV** | Saved searches that apply for you automatically and email recruiters | Live |
| **NextRaise** | Score, CV tailoring, form autofill, finds the hiring team | Live |
| **AIJobmatch** | Pay-per-search ranked job list | Live, anonymous operator |
| **KarKo AI** | — | See Useful Apply |
| **Hired** | Reverse marketplace (companies apply to candidates) | **Gone.** Adecco bought it in a 2020 rescue sale and folded it into LHH on 14 June 2024; hired.com redirects to lhh.com |
| **Jobright.ai** | Ranked job feed with an AI assistant (Orion) and auto-apply | Live, **US only** |
| **Welcome to the Jungle** | Paris job board built on employer branding | Live, now moving towards selling to employers |
| Teal, Huntr, Careerflow, Jobscan | Tracker, job saver, CV keyword checker | Live; the user brings the jobs |
| Simplify | Free form autofill + job feed | Live; feed covers 10 countries **including France** |
| JobCopilot, AIApply, LazyApply, Massive | Volume auto-apply | Live |
| LinkedIn, Indeed, HelloWork, APEC, France Travail | Big boards and public services with free AI | Live |
| Jobea, Mon Copilote Carrière, Talya | French AI startups | Live, small, self-funded |

---

## 3. Geography and data sources

| Product | Head office | Job markets | France / Paris depth | Where jobs come from |
|---|---|---|---|---|
| **Saxobeat** | Paris | Paris / Île-de-France (+ London remote) | **Deep**: ~325 sources, about 20 types of recruiting system | Employers' own career pages, read directly (Greenhouse, Lever, Ashby, Workday, SuccessFactors, Talentsoft, Oracle HCM, SmartRecruiters, Teamtailor, Workable, Phenom, Eightfold…), plus Adzuna, eFinancialCareers and manual saves |
| Useful Apply | Delaware, USA (founder came from a job search in Germany) | 22 countries: US, CA, UK, IE, DE, NL, FR, ES, IT, CH, AT, BE, DK, SE, NO, FI, PL, AU, NZ, IN, SG, UAE | Shallow: Paris, Lyon and Toulouse only; "built first for the US" | **Google Jobs via SerpAPI** (its privacy policy), plus links the user pastes |
| LoopCV | Thessaloniki, Greece | Global, leaning Europe | Only through global boards (LinkedIn, Indeed, Glassdoor, Jooble, CareerJet, Adzuna); French interface; no French board named | 30+ boards; a career-page option on the higher plans |
| NextRaise | Bengaluru, India (says "built in SF") | India first; US, UK, CA, SG, AU, DE | Not listed (?) | "100+ portals and career pages in 20+ countries" |
| AIJobmatch | Unknown | Unstated; US tech | Incidental only | Scrapes 16 sources per search: LinkedIn, Wellfound, Built In, 13 VC portfolio boards (a16z, Accel, Index, Sequoia…) |
| Hired (historic) | San Francisco | US, UK, Paris from 2016 (bought Breaz) … | Was real (BlaBlaCar, Algolia, Aircall) | Screened candidate profiles; employers paid |
| Jobright | Santa Clara, USA | **US only** (says so in its App Store listing) | None: cannot search Paris | 8M+ jobs, 400K new a day from LinkedIn, Indeed, career pages |
| Welcome to the Jungle | Paris | FR, UK (Otta brand retired), US. Czech office closed Jan 2025 | Strong for startups, scale-ups, SaaS; **only paying employers** | Employer subscriptions; jobs synced from the employer's recruiting system |
| Simplify | San Francisco | Feed in 10 countries incl. FR | Some (?) | Jobs scraped from the web, ~20K companies |
| JobCopilot | Not disclosed | "Worldwide", French interface | Unknown | Claims 500K+ career pages |
| LinkedIn | USA | Global | Strong | Its own ads |
| Indeed | USA | Global (Career Scout: US, AU, IN only) | Strong volume; AI not in France | Ads + crawled career pages |
| APEC / France Travail / HelloWork | France | France | Strong | Their own ads |
| Talya | France | France | Good | 15+ boards (France Travail, Indeed, LinkedIn, WTTJ), ~2,400 jobs/day |
| Jobea | France | France | Good, different angle | The French company register (SIRENE) + hiring signals; unsolicited applications, no job ads |

**Reading:** the global tools rely on aggregators, so French banks and corporates are missing from them unless those employers post on LinkedIn or Indeed. The French tools cover their own ads. The gap Saxobeat fills is **"all the employers I care about, straight from their own sites, deduplicated, scored for me"**.

---

## 4. Product profiles and USPs

### The products named in the brief

**Useful Apply (formerly KarKo AI)** — *closest to Saxobeat in philosophy.*
- **Who:** Karko AI Inc. (Delaware); founder Wasim Jalali; started 2026. Runs on Claude on AWS. No published user numbers; 2 Trustpilot reviews.
- **What:**
  - Daily feed, run by hand once a day, showing up to 25 "strong/good fit" jobs.
  - Settings: up to 2–4 job titles × 2–4 countries, salary floor, work permit, languages, and a **Strict / Balanced / Broad** dial (Broad adds related titles and nearby cities).
  - Fit check (score, strengths, gaps, apply or skip).
  - An application kit in about 90 seconds: tailored CV, cover letter, application email, follow-up email, screening answers.
  - Tracker flags applications that have **gone quiet**.
- **USP:**
  - It never sends anything for you: "not today, not ever".
  - **Zero fabrication:** skills and figures are first taken from the CV and used as hard limits, so a bullet with no number gets no number.
- **Weak points:** Google Jobs data only; France is an afterthought; the score comes from an AI model with no visible reasoning; no interview prep or company research; Max plan costs $80.

**LoopCV** — *the European auto-apply tool.*
- **Who:** Greece, founded 2019. Claims 1.5M jobs collected a day and 25K people hired. Trustpilot 3.9 from 131 reviews, 20% one-star.
- **What:**
  - "Loops" (saved searches) that apply automatically, or email the recruiter from your own address.
  - Required and excluded keywords, excluded companies.
  - A **"Rejected matches" view** showing what was filtered out.
  - Never applies to the same company twice within 6 months.
  - Also: email open and reply tracking, CV A/B tests, screening answers, mock interviews, an **MCP connector** so Claude or ChatGPT can drive it, and a white-label B2B offer.
- **USP:** volume across 30+ sources plus recruiter emails.
- **Weak points:** failed applications, weak matches, emails landing in spam; complaints of sending to the wrong company; confusing pricing.

**NextRaise** — *the most detailed score breakdown.*
- **Who:** ThreeDots Inc., Bengaluru, founded 2024. Claims 500K users, but a search snippet of its Chrome Web Store listing showed only about 5K extension users (unverified).
- **What:**
  - 0–100 score labelled Strong / Good / Fair, broken down into qualifications, responsibilities, skills (e.g. "22 of 31"), title fit, years of experience and a location gate, with the **top gaps** and next steps.
  - CV keyword check with one-click fixes; CV tailored per job.
  - Autofill on Workday, Greenhouse and Lever.
  - **Find HR:** paste a job link from a recruiting system and get the recruiters and hiring managers, with the evidence for each.
  - **Super Apply:** emails 2–4 people on the hiring team from your Gmail, after you approve.
  - Referral finder.
- **USP:** "see which jobs you'll be shortlisted for" and reach the hiring team directly.
- **Weak points:** India first; contradictory claims; heavy "74% off" anchors; no refunds; people-data lookups with no mention of GDPR.

**AIJobmatch** — *pay per search.*
- **What:** a free profile built from the CV, plus a chat to refine it. Each $5 search scrapes 16 sources live, takes 15–30 minutes, and returns jobs ranked by match % with **Key matches / Areas for growth / Recommendations**. Results export to Excel or Word.
- **USP:** no subscription, and access to "hidden" jobs on VC portfolio boards.
- **Weak points:** nobody stands behind it publicly, and there are no reviews. It is aimed at US tech. Its pricing is inconsistent: the homepage advertises a monthly plan that is switched off in the code.

**Hired** — *the cautionary tale.*
- **Model:**
  - Screened candidates (5–10% accepted) published a profile with salary expectations, and companies sent interview requests with pay stated up front.
  - Free for candidates. Employers paid 15% of first-year salary (12% in France in 2016), or 1% a month for 24 months, or later a subscription.
- **What happened:** raised about $130M; after cash ran short it was sold cheaply to Adecco's Vettery in 2020, then folded into LHH in 2024.
- **Lessons:**
  - A two-sided marketplace lives or dies with employers' hiring budgets, and human screening does not scale.
  - Candidates loved the salary transparency and the inbound interest. In 2024 users on Blind were still asking someone to "build another Hired".

### Head-to-head focus

**Jobright.ai** — *the global benchmark.*
- **Who:** Santa Clara, founded 2023, about $3–8M raised (Indeed's venture arm among investors). Claims 3M+ users; iOS app rated 4.8.
- **What:**
  - 0–100 match % from a mix of AI models (OpenAI, Anthropic, Google, fine-tuned Llama), with no published weights.
  - **Orion**, a chat assistant for fit analysis, interview tips, company insight and CV revisions.
  - **Insider Connections**: alumni, ex-colleagues and hiring managers at the company, with message templates.
  - H-1B sponsorship filter; CV tailoring; autofill (Workday, Greenhouse, Lever, Taleo, iCIMS); tracker.
  - **Jobright Agent** auto-apply (paid plan only; it skips sites that block bots).
- **USP:** matching plus referrals in one feed; it claims to filter out fake jobs.
- **Weak points:** US only; AI-tailored CVs can invent figures; prices are hidden and keep rising.

**Welcome to the Jungle** — *the Paris reference board.*
- **Who:** Paris; about €40M annual recurring revenue; 4,500 paying employers (target 15,000 by 2029).
- **Pivot:** in April 2026 it pivoted to an **AI hiring suite sold to employers**. Co-founder Jérémy Clédat stepped down as CEO in July 2026.
- **What candidates get:**
  - Polished company pages with photos, videos and team.
  - Job suggestions from Otta's matching ("Matchez !"), but **no match score shown to candidates**.
  - Alerts, saved jobs, a kanban tracker, and recruiters contacting you.
  - A free **AI Candidate Coach**: CV checked against a job, cover letter, interview practice, profile audit.
  - Applies either through its own form or by redirecting to the employer's recruiting system. English-only iOS app.
- **USP:** company culture content and reach among startups and scale-ups.
- **Weak points for our users:** only paying employers, so banks and corporates are thin. Investment now goes to the employer side, and candidates are becoming a pool for recruiters to source from.
- **Scraping:** its terms (section 10) **ban automated extraction**; no public API.

### Others worth knowing

| Product | One line | Worth noting |
|---|---|---|
| Teal | Tracker + job saver + keyword match | Best-loved job saver (4.9★, ~200K users). No autofill, no auto-apply |
| Huntr | Kanban tracker | **Map view**, contacts CRM, "application packets" (the CV and letter sent, kept with the job) |
| Simplify | Free autofill "Copilot" | "Copilot, not bot": the user clicks Submit. French feed |
| Jobscan | Original CV-vs-ad match rate | 30+ checks; aims for a 75–80% match |
| Careerflow | Tracker + LinkedIn optimiser + networking CRM | Job-search funnel analytics |
| JobCopilot / AIApply / LazyApply / Massive | Mass auto-apply | LazyApply rated 2.3–2.5 on Trustpilot; Sonara shut down in 2024 and users lost their history |
| LinkedIn | Job Match (FR, Sept 2026), AI search in French | Free gap analysis; "Top Applicant" badge on Premium only |
| HelloWork | Coach Emploi (May 2026) | CV-vs-job check, voice interview simulator |
| APEC | "Le Matching", free consultants | Free match rate on APEC ads; free 1-hour advice sessions |
| France Travail | CoachFT, MatchFT (built on Mistral), La Bonne Boîte | **Free licensed job-ad API** |
| Talya (FR) | Daily scored feed + tailoring | Closest French analogue to Saxobeat's inbox; prices not published |
| Jobea (FR) | Unsolicited applications to companies likely to hire | Uses the SIRENE register + hiring signals |
| Jack & Jill (UK) | Voice-interview AI agent, intros to hiring managers | ~$60M raised; not in France yet |

---

## 5. Head-to-head: Saxobeat vs Jobright vs Welcome to the Jungle

| | **Saxobeat** (today) | **Jobright.ai** | **Welcome to the Jungle** |
|---|---|---|---|
| Market | Paris / Île-de-France, senior | US only | FR, UK, US |
| Who it serves | The candidate | The candidate | Mainly the employer (who pays) |
| Job supply | Employers' own career pages, read directly, plus a few aggregators | 8M aggregated jobs (LinkedIn, Indeed, career pages) | Paying employers only |
| Banks and corporates in Paris | **Yes** (Workday, SuccessFactors, Oracle, Talentsoft…) | n/a | Thin unless they pay |
| Duplicates across sources | Merged | Claims to merge | n/a (one source) |
| Freshness | First seen / last seen per job and source | "400K new a day", early alerts | Publication date |
| Match score | Rule-based, free to compute; matched keywords shown | 0–100 from AI models, method not published | **None shown to candidates** |
| Why it matched | Matched keywords; gaps partly shown (in full with the AI review) | % plus a fit analysis in Orion | No |
| Hard filters | Yes: language, seniority, cities, salary, words | Yes, incl. H-1B sponsorship | Basic search filters |
| Learns from your decisions | **Insights** suggests what to block or boost | Learns from interactions (?) | Otta matching learns from interactions |
| Triage | Inbox with keyboard shortcuts, bulk dismiss | Feed + like/dismiss | Suggestions + saved jobs |
| Pipeline | Kanban with follow-ups that turn red | Tracker | Kanban (jobs applied elsewhere added by hand) |
| Interviews | Stages, calendar export (.ics), cheat sheet per job | Orion tips | AI coach: interview practice |
| Company research | Company profile + report written with an agent | "Company insights" in Orion | **Best in class**: photos, videos, team |
| CV check | CV health + match to a target role (onboarding) | Strengths and gaps, tailored CV | AI coach CV check |
| Writing help | Exports for an agent (cheat sheet, company report) | Tailored CV, cover letters | Cover letter |
| Referrals / contacts | — | **Insider Connections** | — |
| Recruiters reach you | — | — | **Yes** ("Opportunities") |
| Auto-apply | **No, by design** | Yes (Agent, paid plan) | No (own form or redirect) |
| Saving jobs from other sites | Bookmarklet (LinkedIn, career pages) | Extension (autofill) | — |
| Mobile | Web pages; cheat sheet reads on a phone | iOS app 4.8★ | iOS app (English) |
| Price to the candidate | Free, by invitation | Free (2 AI credits a day); paid plan $39.99/mo, $89.99/quarter **(3P)** | Free |
| Business model | None yet | Candidate subscriptions | Employer subscriptions and job-ad packs |

**What this says.**
- Jobright is the product standard Saxobeat's experience will be judged against: one feed, a match %, referrals and an assistant. But it cannot serve a Paris user at all.
- Welcome to the Jungle is where Paris candidates already go for culture and startups. But it is a shop window for paying employers with no candidate-side score, and it is putting its money into the employer side.
- Saxobeat's place is between them: Jobright's discipline (score everything, triage fast, follow the process) on the Paris supply that neither covers fully.

---

## 6. Pricing analysis

### 6.1 Plans of the products in the brief, plus the two in focus

| Product | Free tier | Paid plans | Effective per month | Unit of value | Annual plan | Refunds |
|---|---|---|---|---|---|---|
| **Useful Apply** | 2 applications or 8 fit checks a month; top 5 jobs a day | Plus **$19.99/mo** (25 applications, top 25 a day, 2 titles × 2 countries); Max **$79.99/mo** (100 applications, 4×4) | Same (monthly only) | Credits: fit check 0.5, application 2 (1.5 after a fit check). Top-up: 50 credits $19.99 | No | Generally none |
| **LoopCV** (EUR, price API from France) | 1 loop, 10 applications a month | Standard **€14.99/mo** or €36 per 3 months; Premium **€24.99** or €60; Done For You **€87.99** or €197.97 | Standard €12, Premium €20, Done For You €65.99 on 3-month billing | Applications per month (100 / 300) | No | Within 7 days if ≤10% of quota used |
| LoopCV (USD, 3P) | — | $19.99 / $59.99 / $89.99 | — | — | — | — |
| **NextRaise** (USD outside India) | 2 tailored CVs, 5 CV checks, 10 match checks, 1 alert a day | **$12.99 a week; $24.99 a month; $48.99 for 3 months; $58.99 for 5 months** | $24.99 / $16.33 / **$11.80** | Credits for Super Apply / Find HR (3 / 10 / 25 / 40); packs: 10 for $12.99 … 50 for $44.99 | No | None |
| NextRaise (India) | — | ₹499 a week … ₹2,999 for 5 months, one-off payments | ₹600–1,099 | — | — | — |
| **AIJobmatch** | Profile and CV analysis | **$5 per search**; "Unlimited" $20/mo announced but switched off | — | Searches | No | "100% money back" |
| **Hired** (historic) | Free for candidates | Employer: 15% of first-year salary (12% in France), or 1% a month × 24, or a subscription | — | Hires | — | — |
| **Jobright** (3P) | 2 AI credits a day; feed, scores, tracker | Paid plan **$17.99 a week, $39.99 a month, $89.99 a quarter** (Oct 2026; was $14.99 / $29.99 / $69.99 earlier in 2026) | ~$30 on quarterly | AI credits | ~$20/mo per one review (?) | — |
| **Welcome to the Jungle** | Everything, free | Employers only: quote-based hiring suite, job-ad packs, content studio | — | — | — | — |

### 6.2 The wider market, as an effective monthly price

| Product | Weekly | Monthly | Quarterly (per month) | Longer (per month) | Source |
|---|---|---|---|---|---|
| Teal | $13 | $29 | $26.33 | — | 3P |
| Simplify+ | $19.99 | $39.99 | ~$30 | — | 3P |
| Huntr Pro | — | $40 | $30 | $26.66 (6 months) | Official |
| Jobscan | — | $49.95 | $29.98 | — | 3P |
| Careerflow Premium / Plus | $8.99 / $19.99 | $23.99 / $44.99 | $18.33 / $39.99 | $14.41 / $24.99 (annual) | Official |
| JobCopilot | ~$8.90–12.90 | ~$28–39 | Offered | — | Official per-day teaser + 3P |
| AIApply | — | ~$29 + auto-apply $49 (100) or $99 (250) | $199 / 3 months (auto-apply) | — | 3P |
| LazyApply | — | — | — | $99 / $149 / $999 a year | Official |
| Kickresume (EUR) | — | €24 | €18 | €8 (annual) | Official |
| LinkedIn Premium Career (EUR) | — | €29.74–39.99 | — | €14.87–19.99 (annual) | 3P |
| Jobea (FR) | — | €29 / €39.90 / €94 | −25% on quarterly | — | Official |
| Mon Copilote Carrière (FR) | — | €19.99 / €29.99 / €49.99 | — | — | Official |
| Indeed, HelloWork, APEC, France Travail, WTTJ | Free | | | | |

### 6.3 Patterns

- **Monthly price points cluster at $20–40** (LoopCV in euros is the cheapest at €15–25; Max at Useful Apply and "Done For You" at LoopCV sit at €80–90 for power users).
- **Short billing periods.** A job search ends, so annual plans are rare: Teal, Simplify, Jobscan, Jobright, Useful Apply, LoopCV and NextRaise have none. The **quarterly plan is the main discount** (about 20–35% off). NextRaise even sells a 5-month plan.
- **Weekly plans for urgent searchers** at $9–20, i.e. $40–85 a month if kept: a high-margin impulse plan.
- **Anything the AI writes is metered.** Matching, feeds and trackers are mostly free; tailored CVs, letters and auto-applications cost credits. That reflects the cost of the AI calls. Unit prices: about **$0.40–0.50 per auto-application**, about **$0.80 per tailored application** (Useful Apply), **$5 per search** (AIJobmatch).
- **Free tiers are capped by counts:** 2 applications, 5 checks, 10 a month, 100 tracked jobs, 5 jobs a day.
- **The trust problems repeat everywhere:** prices hidden until signup, fake "74% off" anchors, no refunds, auto-renewal complaints. An honest, readable price page is a cheap way to stand out.
- **Regional pricing exists but is rare:** NextRaise (INR one-off vs USD subscription), LoopCV (EUR vs USD).

### 6.4 What French senior candidates already pay

| Reference | Price |
|---|---|
| APEC consultants, CEP career advice, France Travail tools, LinkedIn Job Match basics | Free |
| LinkedIn Premium Career | ~€15–20/mo on annual billing, €30–40 monthly |
| French AI copilots (Jobea, Mon Copilote Carrière) | €20–94/mo |
| Career coaching | €70–120 an hour outside Paris; executive €200–800 an hour |
| Individual outplacement (usually paid by the employer) | €3,000–25,000 |

### 6.5 What this means for Saxobeat (if it ever charges)

Charging is out of scope for the current phase (PRD §3); these are notes for later, not decisions.
- **Saxobeat's costs are mostly fixed.** Rule-based scoring and reading sources cost the same for 1 or 30 users. Competitors pay per AI call, which is why they meter. Saxobeat can offer **unlimited scoring and triage** where others count credits.
- **A credible price sits under LinkedIn Premium:** about **€9–15 a month**, or **€29–39 per quarter** to match how searches end, with no weekly plan and no fake discounts. A short free period (a month, or the first N jobs shortlisted) fits better than permanent feature caps.
- **If AI writing comes back** (reviews, letters, tailored CVs), sell it as an add-on or per use, as the market does. The current "export for an agent" approach, where the user runs their own Claude, is already a zero-cost version of this.
- **Do not monetise through employers.** That is Hired's and Welcome to the Jungle's model: revenue follows hiring budgets, and the product drifts towards serving recruiters.

---

## 7. Features worth copying

Sorted by fit with Saxobeat (direct career pages, rule-based scoring, Paris, no auto-apply). "Have" means Saxobeat already has part of it.

| # | Feature | Seen at | Why it fits | Saxobeat today | Effort |
|---|---|---|---|---|---|
| 1 | **Score breakdown: matches / gaps / verdict** (e.g. "skills 22 of 31, title fits, seniority fits, missing: X, Y") | NextRaise, AIJobmatch, Useful Apply, LinkedIn Job Match, Jobscan | Rule-based scoring can explain itself exactly, and no rival's AI score can. Makes the score trustworthy | Have: matched keywords; gaps only with the AI review | S |
| 2 | **Fresh / reposted / closed badges** ("on Workday, 3 days old", "reposted 4×", "closed") | Jobright (claims to filter fakes), Useful Apply (drops old reposts) | Direct career pages give real dates and closures, which aggregators cannot. Answers the "ghost job" complaint | Have: first seen / last seen data | S |
| 3 | **Strict / Balanced / Broad dial**: threshold + related titles + nearby areas (Paris → La Défense, Boulogne, Issy, Saint-Denis) | Useful Apply, LoopCV | One control instead of many filters; fits Île-de-France geography | Have: thresholds and city list as separate settings | S |
| 4 | **"Gone quiet" flag + follow-up draft** at 7–10 days after applying | Useful Apply, Huntr, Careerflow | Extends the pipeline's follow-up dates | Have: follow-up dates turn red | S |
| 5 | **"Rejected matches" view**: what the hard filters hid and why | LoopCV | Lets a user check the rule-based filter; builds trust | Have: Filtered & archive | S |
| 6 | **Same-company cooldown warning** ("you applied to X 2 months ago") | LoopCV (6-month rule) | Avoids awkward duplicates in a small Paris market | — | S |
| 7 | **Focus flag with a cap** (e.g. 3 a week) that triggers cheat sheet, company report and contact search | Greenhouse "My Dream Job" (hired ~5× more) | Puts the quality-over-volume stance into the product | Have: shortlist | S–M |
| 8 | **Contacts at the company** from the user's own LinkedIn export (Connections.csv), shown in triage and on company profiles, with a referral-request draft | Jobright Insider Connections, NextRaise referrals | Referrals produced about 25% of cadre hires (APEC 2025). Uses the user's own export, so no scraping | — | M |
| 9 | **Salary and work-mode extraction**: pay range, remote days, English-speaking, visa-friendly, shown on cards and company pages | Jobright (H-1B filter), LinkedIn / Indeed salary insights, Hired (salary up front) | EU pay-transparency rules should put more salary ranges in ads (France's transposition status unverified) | Have: salary fields and minimum-salary filter | M |
| 10 | **Funnel analytics**: conversion by stage, source, score band, company size | Teal, Careerflow | Tells each user whether high scores really convert, and tunes the weights | Have: Insights (decisions), not outcomes | M |
| 11 | **Application packet**: keep the exact CV and letter sent with the pipeline card | Huntr | The cheat sheet can then refer to what was actually sent | — | S |
| 12 | **Required / excluded keywords and excluded companies** as simple lists | LoopCV | Plain, predictable controls | Have: keyword weights and word blocks | — |
| 13 | **VC portfolio job boards as sources** (Index, Accel, Partech, Eurazeo… usually Getro / Consider) | AIJobmatch | Cheap new connector type covering many Paris startups at once | — | M |
| 14 | **Grounding rule for any AI writing**: take skills and figures from the CV first, never invent | Useful Apply "zero fabrication" | Good guardrail for the agent exports and any future AI review | Partly (agent prompts) | S |
| 15 | **MCP connector**: let Claude read the inbox, pipeline and company profiles | LoopCV | Replaces the export/import of files for AI reviews and cheat sheets | Have: file exports for an agent | M |
| 16 | **Commute / map view** from home by RER and metro | Huntr (map view) | Very relevant in Île-de-France | — | M |
| 17 | **Interview question list** per stage from the ad and the company profile | Careerflow, Jobright Orion, HelloWork | Natural addition to the cheat sheet | Have: questions to ask | S |
| 18 | **Assisted autofill, user clicks Submit** | Simplify, NextRaise | Most-loved free feature in the category, and consistent with "no auto-apply". Costly to build across Workday etc. | — | L, later |

**Not worth copying:**
- Auto-apply and mass emails to recruiters (LoopCV, NextRaise Super Apply).
- People-data lookups of recruiters' emails: a GDPR risk in France.
- Anything that automates inside LinkedIn.
- Employer-paid models.
- Fake discount anchors and hidden prices.

---

## 8. Where Saxobeat stands

**Strengths.**
- **Supply nobody else has for Paris:** employers' own career pages, read directly, across about 20 kinds of recruiting system, deduplicated. That includes banks and corporates missing from Welcome to the Jungle and only partly on aggregators.
- **A score you can explain**, with no cost per job and no credits.
- **The whole process in one place:** triage, pipeline, interviews, company profiles, cheat sheets. Most rivals stop at the application.
- A stance against auto-apply that matches where the market is going.

**Gaps compared with the best.**
- No full "why it matched / what's missing" view without the AI review (items 1 and 5 in §7).
- No contacts or referral features (item 8).
- Saved jobs, freshness and salary data exist but are not yet shown as user-facing signals (items 2 and 9).
- No mobile app and no extension (the bookmarklet covers the essentials).
- Small scale: one operator, sources read from one PC.

**Threats.**
- **LinkedIn Job Match** in French (Sept 2026): free, on the biggest network. Its limit: LinkedIn ads only.
- **Indeed Career Scout** if it comes to France: free, on the largest aggregator, which also crawls career pages.
- **HelloWork, APEC and France Travail** making free AI matching standard for cadres.
- **Talya** if it moves upmarket to senior roles.
- **Hired's lesson** for any future paid offer: stay on the candidate side.

**Positioning in one line:**
> *Every Paris job that fits you — straight from employers' own sites, scored in a way you can read, and followed through to the interview. No spam, no auto-apply.*

---

## 9. Legal and regulatory context (France / EU)

Confidence: unless marked, these come from secondary sources (law-firm notes, press). The AI Act guidelines are still a draft.

| Topic | What applies | What it means for Saxobeat |
|---|---|---|
| **EU AI Act** | Recruitment and selection AI is high-risk (Annex III 4(a)). The Commission's draft guidelines (19 May 2026) list a *candidate-run job-recommendation tool* and a *candidate-controlled CV-tailoring assistant* as **not** high-risk. The Digital Omnibus (Reg. 2026/1744) pushed high-risk obligations to 2 Dec 2027; Art. 50 transparency applies from 2 Aug 2026. | Saxobeat's model (candidate-side scoring, no auto-apply, no ranking of candidates for employers) sits on the safe side. Anything that serves employers (ranking candidates, deciding who sees vacancies) would pull it back into scope. If AI reviews return, tell users when they are reading AI output. |
| **GDPR / CNIL** | The CNIL made recruitment a 2026 priority inspection theme (automated decisions, information, retention); the targets are employers and agencies. Its HR retention guide was updated in January 2026. | Saxobeat is controller for each candidate's CV under contract. Keep EU hosting, data minimisation, a clear retention policy (the PRD's ~90-day rule helps) and account deletion. |
| **Scraping** | CNIL scraping guidance (June 2025): respect robots.txt and ToS objections, only data reachable without login, avoid personal data. *CV-Online Latvia v Melons* (CJEU C-762/19, 2021): a job-ad **metasearch that links back** infringes database rights only if it harms the maker's ability to recoup its investment. | Reading employers' own career pages and linking back is the strong position. Bulk-copying a board's database (Indeed, APEC, WTTJ) carries more risk. The France Travail *Offres d'emploi* API is a free, licensed route (dedup and redirect conditions). |
| **Welcome to the Jungle ToS** | Its French terms (section 10) ban robots and scripts for automated extraction, and job ads are licensed for personal use only. robots.txt blocks search and query URLs but publishes a sitemap. | Saxobeat reads only the published sitemap, for the employer radar, and keeps those jobs out of the inbox. That is the cautious end, but the terms are broad: keep the radar operator-only, never show the ad content to candidates, and stop if WTTJ objects. |
| **LinkedIn ToS** | §8.2 bans bots and scrapers, including on public data. LinkedIn sued Proxycurl (Jan 2025, permanent injunction, shut down) and ProAPIs (Oct 2025). | Confirms the current choice: LinkedIn jobs only as manual captures, private to the person who captured them. Never automate inside LinkedIn. A contacts feature must use the user's own data export. |

---

## 10. Sources

Main sources, by product. Full notes are in the research of 9 October 2026.

- **Useful Apply / KarKo AI:** https://usefulapply.com/ · /pricing · /privacy · /imprint · /blog/karko-ai-job-application-agent · /blog/smart-job-feed-ai-curated-daily-jobs · /ai-job-application/zero-fabrication · https://www.trustpilot.com/review/karkoai.com
- **LoopCV:** https://www.loopcv.pro/ · /about · /job-board-api/ · https://api.loopcv.com/prices · https://loopcv.freshdesk.com/support/solutions/articles/103000399849-knowledge-base · https://www.trustpilot.com/review/loopcv.pro
- **NextRaise:** https://nextraise.ai/ · /about · /features/job-match · /features/find-hr
- **AIJobmatch:** https://aijobmatch.io/ · /features · /pricing · /about
- **Hired:** https://www.staffingindustry.com/news/global-daily-news/adecco-incorporating-hired-lhh-business · https://www.recruitingnewsnetwork.com/posts/youre-not-hired-vettery-acquires-a-deeply-troubled-hired · https://techcrunch.com/2020/11/23/vettery-acquires-hired/amp/ · https://www.frenchweb.fr/hired-leve-40-millions-de-dollars-et-rachete-la-start-up-francaise-breaz/227326 · https://techcrunch.com/2015/11/12/hired-the-jobs-marketplace-now-includes-freelance-workers
- **Jobright:** https://jobright.ai/ · https://apps.apple.com/app/id6738236788 · https://www.theregister.com/2025/06/24/ai_may_take_jobs_but/ · https://resumehog.com/blog/posts/jobright-ai-review-2026-is-this-job-search-copilot-worth-it.html (3P)
- **Welcome to the Jungle:** https://about.welcometothejungle.com/ · https://help.welcometothejungle.com/understanding-your-candidate-space-%EF%B8%8F · https://contact.welcometothejungle.com/candidate-coach · https://solutions.welcometothejungle.com/notre-offre · https://www.welcometothejungle.com/fr/pages/terms · https://www.maddyness.com/2026/04/15/welcome-to-the-jungle-change-de-braquet-pour-se-reinventer-sur-un-marche-du-recrutement-bouleverse-par-lia/ · https://www.maddyness.com/2026/05/28/jeremy-cledat-va-lacher-les-commandes-de-welcome-to-the-jungle/
- **Other global tools:** https://huntr.co/pricing · https://www.careerflow.ai/premium · https://lazyapply.com/pricing · https://jobcopilot.com/pricing · https://www.kickresume.com/en/pricing/ · https://help.simplify.jobs/en/help/articles/6895855-supported-countries-and-regions · https://toolradar.com/tools/teal-hq/pricing (3P) · https://careery.pro/blog/is-jobscan-worth-it-2026 (3P)
- **France:** https://jobea.fr/ · https://moncopilotecarriere.fr/tarifs · https://app.talya.app/ · https://gensdinternet.fr/2026/09/10/job-match-de-linkedin-est-lance-en-france-voici-pourquoi/amp/ · https://www.lejournaldesentreprises.com/breve/hellowork-lance-un-agent-ia-pour-accompagner-les-candidats-2143603 · https://www.francetravail.fr/actualites/a-laffiche/2026/candidats-ce-que-l-ia-change-vra.html · https://derrick-app.com/fr/linkedin/profile/prix-linkedin-premium (3P) · https://www.je-change-de-metier.com/outplacement-et-reconversion
- **Market and backlash:** https://fortune.com/2026/07/27/greenhouse-ceo-daniel-chait-ai-doom-loop-job-seekers-spam-interview-applications-unemployment/ · https://www.greenhouse.com/blog/introducing-greenhouse-real-talent · https://www.linkedin.com/help/linkedin/answer/90586 · APEC studies, May 2026 (cadres and AI; recruitment practices) via banquedesterritoires.fr
- **Legal:** https://www.faegredrinker.com/en/insights/publications/2026/6/draft-commission-guidelines-on-high-risk-ai-implications-for-the-workplace · https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/ · https://cnil.fr/fr/controles-prioritaires-2026 · https://cnil.fr/fr/recommandations-developpement-ia-interet-legitime · https://www.twobirds.com/en/insights/2021/uk/cv-online-latvia-cjeu-complicates-the-enforcement-of-database-rights · https://news.linkedin.com/2025/linkedin-takes-legal-action-to-defend-member-privacy

**Not verified:**
- Jobright's exact current price (shown only in its app).
- Simplify, Teal and Jobscan prices.
- Talya's paid tiers.
- Whether Indeed Career Scout will come to France.
- Whether major French banks use Workday.
- France's transposition of the EU pay-transparency directive.
- Welcome to the Jungle job counts for Paris.
