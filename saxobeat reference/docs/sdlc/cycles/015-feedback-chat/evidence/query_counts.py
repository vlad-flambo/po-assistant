"""Cycle 015, criterion 2: how many database queries each candidate page costs, so the feedback button can be shown to cost none.

Not part of the test suite (the name does not start with test_). Run it by path, on SQLite, never against the hosted database:

    $env:DATABASE_URL = ""; $env:QC_LABEL = "before"
    uv run pytest docs/sdlc/cycles/015-feedback-chat/evidence/query_counts.py -q -p no:cacheprovider -s

It writes query_counts_<QC_LABEL>.json next to itself: for each page and each mode, the query count of three requests in a row (the first one
is the cold one) and the status code. Slice 1 runs it with QC_LABEL=before, slice 4 with QC_LABEL=after; the two files are compared.
"""

import json
import os
import pathlib
import sys

import pytest
from django.contrib.auth import get_user_model
from django.db import connection
from django.test import Client
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from jobs.models import Candidate, Score  # noqa: E402
from tests.helpers import make_job  # noqa: E402

pytestmark = pytest.mark.django_db
OUT = pathlib.Path(__file__).with_name(f"query_counts_{os.environ.get('QC_LABEL', 'before')}.json")


@pytest.fixture(autouse=True)
def _like_the_suite(settings):
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    settings.AUTO_BACKFILL = False


def build(mode):
    user = get_user_model().objects.create_user(f"qc-{mode}", password="pw-for-tests")
    me = Candidate.objects.create(user=user, name=f"qc-{mode}", mode=mode, onboarded_at=timezone.now())
    views = []
    for i in range(12):
        status = ["new", "new", "new", "applied", "interviewing", "new"][i % 6]
        view = make_job(candidate=me, canonical_key=f"qc-{mode}-{i}", title=f"Role {i}", company=f"Acme {i % 4}", location="Paris", status=status)
        Score.objects.create(job=view, final_score=40 + i * 4, deterministic_score=40 + i * 4)
        views.append(view)
    client = Client()
    assert client.login(username=f"qc-{mode}", password="pw-for-tests")
    return client, views


@pytest.mark.parametrize("mode", ["power", "standard"])
def test_count_queries(mode):
    client, views = build(mode)
    pages = {"inbox": "/?min_score=0", "pipeline": "/pipeline/", "job": f"/job/{views[0].job_id}/", "settings": "/settings/"}
    result = {}
    for name, path in pages.items():
        counts, status = [], None
        for _ in range(3):
            with CaptureQueriesContext(connection) as ctx:
                response = client.get(path)
            counts.append(len(ctx))
            status = response.status_code
        result[name] = {"path": path, "status": status, "queries": counts}
        assert status == 200, f"{name} ({path}) answered {status}"
    data = json.loads(OUT.read_text()) if OUT.exists() else {}
    data[mode] = result
    OUT.write_text(json.dumps(data, indent=1, sort_keys=True))
    print(mode, {k: v["queries"] for k, v in result.items()})
