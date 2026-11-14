"""Delete drill for cycle 032: build one realistic account, delete it with accounts.delete_account, report time, SQL statements and rows left.

Run from Git Bash in the repository root:
    SAXOBEAT_DB="$TEMP/drill32.db" uv run python docs/sdlc/cycles/032-*/evidence/drill_delete.py 36271 5000
(args: job views, then private jobs; default 36271 0). For Postgres, set DATABASE_URL to the localhost database made for the drill.

Refuses to run on anything but a temporary SQLite file or a Postgres on localhost, and never prints an address."""
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.getcwd())
os.environ.setdefault("SAXOBEAT_MAIL", "console")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django  # noqa: E402

django.setup()
from django.conf import settings  # noqa: E402
from django.contrib.auth.models import User  # noqa: E402
from django.core.management import call_command  # noqa: E402
from django.db import connection  # noqa: E402

db = settings.DATABASES["default"]
if db["ENGINE"].endswith("sqlite3"):
    if Path(str(db["NAME"])).resolve().parent != Path(os.environ.get("TEMP", "/tmp")).resolve():
        sys.exit("refused: the SQLite file is not in the temp folder")
    kind = "sqlite (temp file)"
elif db["ENGINE"].endswith("postgresql"):
    if db.get("HOST") not in ("localhost", "127.0.0.1", "::1"):
        sys.exit("refused: Postgres is not on localhost")
    kind = "postgres (localhost)"
else:
    sys.exit("refused: unknown database engine")
print("database:", kind)

from jobs import accounts  # noqa: E402
from jobs.models import (AiTask, ApplicationPacket, Candidate, CandidateJob, CheatSheet, Interview, Job, JobSource, Score, Source,  # noqa: E402
                         StatusChange)

call_command("migrate", verbosity=0)
VIEWS = int(sys.argv[1]) if len(sys.argv) > 1 else 36271
PRIVATE = int(sys.argv[2]) if len(sys.argv) > 2 else 0
B = 500

other_user = User.objects.create_user("other@example.com", "other@example.com", "pw-pw-pw-pw-1")
other = Candidate.objects.create(user=other_user)
user = User.objects.create_user("drill@example.com", "drill@example.com", "pw-pw-pw-pw-1")
cand = Candidate.objects.create(user=user)

shared = Job.objects.bulk_create([Job(canonical_key=f"s{i}", title=f"shared {i}") for i in range(VIEWS)], batch_size=B)
shared = list(Job.objects.filter(canonical_key__startswith="s"))
CandidateJob.objects.bulk_create([CandidateJob(candidate=cand, job=j) for j in shared], batch_size=B)
CandidateJob.objects.bulk_create([CandidateJob(candidate=other, job=j) for j in shared[:1000]], batch_size=B)  # a second person on the same jobs
mine = list(CandidateJob.objects.filter(candidate=cand))
Score.objects.bulk_create([Score(job=c, final_score=50, matched_keywords=["a", "b"], summary="x" * 300) for c in mine], batch_size=B)
StatusChange.objects.bulk_create([StatusChange(job=c, to_status="new") for c in mine], batch_size=B)
tenth = mine[::10]
Interview.objects.bulk_create([Interview(job=c) for c in tenth], batch_size=B)
CheatSheet.objects.bulk_create([CheatSheet(job=c, content="y" * 500) for c in tenth], batch_size=B)
ApplicationPacket.objects.bulk_create([ApplicationPacket(job=c, letter="z" * 500) for c in tenth], batch_size=B)
from django.utils import timezone  # noqa: E402

AiTask.objects.bulk_create([AiTask(candidate=cand, job=c, kind="screen", pack="p", due_at=timezone.now()) for c in mine[::2]], batch_size=B)
if PRIVATE:
    src = Source.objects.create(type="x", name="drill")
    own = Job.objects.bulk_create([Job(canonical_key=f"p{i}", title=f"private {i}", owner=cand) for i in range(PRIVATE)], batch_size=B)
    own = list(Job.objects.filter(owner=cand))
    JobSource.objects.bulk_create([JobSource(job=j, source=src, external_id=f"e{j.pk}") for j in own], batch_size=B)
    CandidateJob.objects.bulk_create([CandidateJob(candidate=cand, job=j) for j in own], batch_size=B)
    mine2 = list(CandidateJob.objects.filter(candidate=cand, job__owner=cand))
    Score.objects.bulk_create([Score(job=c, final_score=40) for c in mine2], batch_size=B)
print(f"built: {VIEWS} views (+{PRIVATE} private jobs), scores {Score.objects.filter(job__candidate=cand).count()}, tasks {AiTask.objects.filter(candidate=cand).count()}")

t = time.time()
count = [0]


def counter(execute, sql, params, many, context):
    count[0] += 1
    return execute(sql, params, many, context)


with connection.execute_wrapper(counter):
    gone = accounts.delete_account(user)
seconds = time.time() - t
print(f"RESULT seconds={seconds:.1f} statements={count[0]} returned={gone}")
print("left of theirs: views", CandidateJob.objects.filter(candidate=cand).count() if Candidate.objects.filter(pk=cand.pk).exists() else 0,
      "| candidate", Candidate.objects.filter(pk=cand.pk).count(), "| user", User.objects.filter(pk=user.pk).count(),
      "| private jobs", Job.objects.filter(canonical_key__startswith="p").count(), "| tasks", AiTask.objects.filter(candidate_id=cand.pk).count())
print("kept: shared jobs", Job.objects.filter(canonical_key__startswith="s").count(), "| other person's views", CandidateJob.objects.filter(candidate=other).count(),
      "| other's user", User.objects.filter(pk=other_user.pk).count())
