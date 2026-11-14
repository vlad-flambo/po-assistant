-- Cycle 031, slice 6: what would the 30-day rule hide on the 29 Oct 2026 dump? READ ONLY (selects, plus EXPLAIN ANALYZE of a select) on a scratch database.
\set ON_ERROR_STOP on
\pset pager off
select current_database() as database, (current_database() = 'scratch031') as is_the_scratch_copy \gset
\if :is_the_scratch_copy
\else
  \echo 'REFUSED: not the scratch database'
  \quit
\endif
-- "as of": the dump's own time, so the numbers read as of 29 Oct 10:06 (the dump is 8 days older than today)
select timestamptz '2026-10-29 10:06+01' as asof \gset

\echo '== 1. stored limits per candidate (jobs_config.filters.max_age_days), visible new views, and the views the NEW rule (30 days) would hide'
with v as (
  select cj.candidate_id, j.posted_at, j.first_seen_at
  from jobs_candidatejob cj join jobs_job j on j.id = cj.job_id
  where cj.status = 'new' and cj.hidden_reason = '' and not cj.keep_visible
)
select c.id as candidate, c.name,
       (select filters->>'max_age_days' from jobs_config where candidate_id = c.id) as stored_limit,
       count(v.*) as visible_new,
       count(*) filter (where v.posted_at is not null and v.posted_at < :'asof'::timestamptz - interval '30 days') as dated_older_than_30,
       count(*) filter (where v.posted_at is null and v.first_seen_at < :'asof'::timestamptz - interval '30 days') as undated_imported_over_30_days_ago,
       count(*) filter (where v.posted_at is null) as undated_total
from jobs_candidate c left join v on v.candidate_id = c.id
group by c.id, c.name order by c.id;

\echo '== 2. the same, visible views that carry a score (what the inbox shows and the AI could pick)'
select cj.candidate_id as candidate,
       count(*) as scored_visible_new,
       count(*) filter (where (j.posted_at is not null and j.posted_at < :'asof'::timestamptz - interval '30 days')
                           or (j.posted_at is null and j.first_seen_at < :'asof'::timestamptz - interval '30 days')) as scored_and_past_30_days
from jobs_candidatejob cj join jobs_job j on j.id = cj.job_id join jobs_score s on s.job_id = cj.id
where cj.status = 'new' and cj.hidden_reason = '' and not cj.keep_visible
group by cj.candidate_id order by cj.candidate_id;

\echo '== 3. all jobs in the database: how many have no posting date at all, and the age of their import date'
select count(*) as jobs, count(*) filter (where posted_at is null) as undated,
       count(*) filter (where posted_at is null and first_seen_at < :'asof'::timestamptz - interval '30 days') as undated_over_30_days,
       count(*) filter (where posted_at is null and first_seen_at < :'asof'::timestamptz - interval '60 days') as undated_over_60_days
from jobs_job;

\echo '== 4. the new nightly age-out, as a SELECT with EXPLAIN ANALYZE for the candidate with most views (nothing is updated)'
select candidate_id as biggest from jobs_candidatejob group by candidate_id order by count(*) desc limit 1 \gset
explain (analyze, buffers off, timing on)
select cj.id from jobs_candidatejob cj join jobs_job j on j.id = cj.job_id
where cj.candidate_id = :biggest and cj.status = 'new' and cj.hidden_reason = '' and not cj.keep_visible
  and (j.posted_at < :'asof'::timestamptz - interval '30 days' or (j.posted_at is null and j.first_seen_at < :'asof'::timestamptz - interval '30 days'));
\echo '   ... and the old one (dated only), for comparison'
explain (analyze, buffers off, timing on)
select cj.id from jobs_candidatejob cj join jobs_job j on j.id = cj.job_id
where cj.candidate_id = :biggest and cj.status = 'new' and cj.hidden_reason = '' and not cj.keep_visible
  and j.posted_at < :'asof'::timestamptz - interval '30 days';
