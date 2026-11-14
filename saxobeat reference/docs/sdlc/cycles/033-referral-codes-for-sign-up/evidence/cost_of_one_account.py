"""Cycle 033, criterion 16: what does one new account cost? Sign a fresh candidate up the way /join/ does, run the first backfill
(what the web server does at the person's first request), and count rows and bytes before and after.

Run from Git Bash in the repository root, against a LOCAL Postgres holding a restored dump:
    DATABASE_URL=postgres://saxobeat:saxobeat@localhost:5432/scratch033 SAXOBEAT_MAIL=console \
        uv run python docs/sdlc/cycles/033-*/evidence/cost_of_one_account.py [accounts]
(accounts: how many fresh candidates to add one after the other, default 1; each is measured separately)

Refuses to run on anything but a Postgres on localhost, and never prints an address."""
import os
import sys
import time

sys.path.insert(0, os.getcwd())
os.environ.setdefault("SAXOBEAT_MAIL", "console")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django  # noqa: E402

django.setup()
from django.conf import settings  # noqa: E402
from django.core.management import call_command  # noqa: E402
from django.db import connection  # noqa: E402

db = settings.DATABASES["default"]
if not db["ENGINE"].endswith("postgresql") or db.get("HOST") not in ("localhost", "127.0.0.1", "::1"):
    sys.exit("refused: this drill runs on a Postgres on localhost only")
print("database: postgres (localhost), name:", db["NAME"])

from jobs import accounts  # noqa: E402
from jobs.models import Candidate  # noqa: E402
from jobs.services import matching  # noqa: E402

call_command("migrate", verbosity=0)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1


def snapshot():
    """Rows and total bytes (table + indexes + toast) of every table of the app."""
    with connection.cursor() as cur:
        cur.execute("select relname, pg_total_relation_size(c.oid) from pg_class c join pg_namespace n on n.oid=c.relnamespace "
                    "where n.nspname='public' and c.relkind='r' and relname like 'jobs\\_%' or relname in ('auth_user')")
        sizes = dict(cur.fetchall())
        rows = {}
        for table in sizes:
            cur.execute(f'select count(*) from "{table}"')  # table names come from pg_class, not from input
            rows[table] = cur.fetchone()[0]
    return rows, sizes


for n in range(N):
    before_rows, before_size = snapshot()
    with connection.cursor() as cur:
        cur.execute("select pg_database_size(current_database())")
        db_before = cur.fetchone()[0]
    invite = accounts.create_invitation(None, note=f"cost drill {n}")
    started = time.time()
    user = accounts.sign_up(invite, f"cost-drill-{n}@example.com", "a-long-drill-password-1", "a-long-drill-password-1", "Cost Drill")
    signup_seconds = time.time() - started
    candidate = Candidate.for_user(user)
    started = time.time()
    made = matching.backfill(candidate)
    backfill_seconds = time.time() - started
    after_rows, after_size = snapshot()
    with connection.cursor() as cur:
        cur.execute("select pg_database_size(current_database())")
        db_after = cur.fetchone()[0]
    print(f"\naccount {n + 1}: sign-up {signup_seconds:.2f} s, backfill {backfill_seconds:.1f} s, views made {made}")
    print("  table                          rows added   bytes added")
    for table in sorted(after_rows):
        rows = after_rows[table] - before_rows.get(table, 0)
        size = after_size[table] - before_size.get(table, 0)
        if rows or size > 8192:
            print(f"  {table:<30} {rows:>10} {size:>13,}")
    total = sum(after_size.values()) - sum(before_size.values())
    print(f"  tables + indexes total: {total / 1e6:.2f} MB; whole database: {(db_after - db_before) / 1e6:.2f} MB")
