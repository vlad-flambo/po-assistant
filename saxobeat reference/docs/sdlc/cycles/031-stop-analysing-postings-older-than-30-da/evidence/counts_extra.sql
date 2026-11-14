-- Cycle 031 slice 6, extra read-only counts: when were the undated postings imported, so when does the undated rule start to bite?
\set ON_ERROR_STOP on
\pset pager off
select current_database() as database, (current_database() = 'scratch031') as ok \gset
\if :ok
\else
  \quit
\endif
\echo '== undated jobs by week of import (first_seen_at), and how many of them are visible new views of candidate 1 / 3'
select date_trunc('week', j.first_seen_at)::date as week_of_import,
       count(distinct j.id) as undated_jobs,
       count(*) filter (where cj.candidate_id = 1 and cj.status = 'new' and cj.hidden_reason = '' and not cj.keep_visible) as visible_new_c1,
       count(*) filter (where cj.candidate_id = 3 and cj.status = 'new' and cj.hidden_reason = '' and not cj.keep_visible) as visible_new_c3
from jobs_job j left join jobs_candidatejob cj on cj.job_id = j.id
where j.posted_at is null group by 1 order by 1;
\echo '== the oldest and newest import date in the whole database'
select min(first_seen_at) as oldest_import, max(first_seen_at) as newest_import from jobs_job;
\echo '== dated visible new views by how old they are, candidate 1 (days since posted, as of the dump)'
select width_bucket(extract(epoch from (timestamptz '2026-10-29 10:06+01' - j.posted_at))/86400, array[0,7,14,30,45,60,90,180]) as bucket,
       count(*) as views
from jobs_candidatejob cj join jobs_job j on j.id = cj.job_id
where cj.candidate_id = 1 and cj.status = 'new' and cj.hidden_reason = '' and not cj.keep_visible and j.posted_at is not null
group by 1 order by 1;
