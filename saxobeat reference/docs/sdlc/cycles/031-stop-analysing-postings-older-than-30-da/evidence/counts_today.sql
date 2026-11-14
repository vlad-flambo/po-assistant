-- Cycle 031 slice 6: the same counts with "now" = 2026-11-06 applied to the 29 Oct data (an estimate: nothing newer is in the dump).
\set ON_ERROR_STOP on
\pset pager off
select current_database() as database, (current_database() = 'scratch031') as ok \gset
\if :ok
\else
  \quit
\endif
select timestamptz '2026-11-06 18:00+01' as asof \gset
select cj.candidate_id as candidate,
       count(*) as visible_new_in_dump,
       count(*) filter (where j.posted_at is not null and j.posted_at < :'asof'::timestamptz - interval '30 days') as dated_over_30_days,
       count(*) filter (where j.posted_at is null and j.first_seen_at < :'asof'::timestamptz - interval '30 days') as undated_imported_over_30_days_ago
from jobs_candidatejob cj join jobs_job j on j.id = cj.job_id
where cj.status = 'new' and cj.hidden_reason = '' and not cj.keep_visible group by 1 order by 1;
