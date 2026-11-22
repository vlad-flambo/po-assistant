"""Cycle 010 : moteur API Claude, testé avec un client simulé (aucun appel réseau, aucune clé, aucune dépense).

Depuis le cycle 013, le modèle par défaut est Mistral : ces tests choisissent un modèle Claude explicitement
(le moteur Mistral a les siens, tests/test_mistral.py)."""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import anthropic
import httpx2
import pytest

from po_assist import api_agent, handoff, settings
from po_assist.packs import PACKS
from po_assist.store import Store
from tests.test_handoff import perfect_output

ROOT = Path(__file__).resolve().parent.parent
CLAUDE = "claude-opus-5-5"


def _tasks_of(kwargs) -> list[dict]:
    text = kwargs["messages"][0]["content"]
    return json.loads(text[text.index("\n\n") + 2:])


class FakeClient:
    """Imite client.beta.messages.stream(...) ; `behaviour(k, kwargs)` décide de la réponse du k-ième appel."""

    def __init__(self, behaviour=None):
        self.calls = []
        self.behaviour = behaviour or (lambda k, kw: "ok")
        self.beta = SimpleNamespace(messages=self)

    def stream(self, **kwargs):
        self.calls.append(kwargs)
        k = len(self.calls)
        what = self.behaviour(k, kwargs)
        if isinstance(what, Exception):
            raise what
        tasks = _tasks_of(kwargs)
        results = [{"task": t["task"], "kind": t["kind"], "output": perfect_output(t["input"]["identifier"], t["input"]["text"])}
                   for t in tasks]
        msg = SimpleNamespace(
            content=[SimpleNamespace(type="text", text=json.dumps({"results": results}, ensure_ascii=False))],
            stop_reason="refusal" if what == "refusal" else "end_turn",
            stop_details=SimpleNamespace(category="cyber") if what == "refusal" else None,
            usage=SimpleNamespace(input_tokens=2000, cache_creation_input_tokens=9000 if k == 1 else 0,
                                  cache_read_input_tokens=0 if k == 1 else 9000, output_tokens=15000))

        class _Stream:
            def __enter__(self_inner):
                return self_inner

            def __exit__(self_inner, *a):
                return False

            def get_final_message(self_inner):
                return msg
        return _Stream()


def _auth_error():
    return anthropic.AuthenticationError("invalid x-api-key", body=None,
                                         response=httpx2.Response(401, request=httpx2.Request("POST", "https://api.example")))


def test_api_run_batches_caches_constrains_and_imports(env):
    client = FakeClient()
    run = api_agent.run("analyse", model=CLAUDE, client=client)
    assert run["batches"] == 4 and len(client.calls) == 4
    systems = [c["system"] for c in client.calls]
    assert all(s == systems[0] for s in systems), "le préfixe mis en cache doit être identique d'un paquet à l'autre"
    assert systems[0][0]["cache_control"] == {"type": "ephemeral"}
    first = client.calls[0]
    assert first["model"] == "claude-opus-5-5" and first["fallbacks"] == "default"
    assert first["output_config"]["format"]["type"] == "json_schema" and first["output_config"]["effort"] == "high"
    assert "server-side-fallback-2026-07-01" in first["betas"]
    doc = json.loads(run["results"].read_text())
    assert doc["agent"] == "api / claude-opus-5-5"
    pv, _ = handoff.import_file(run["results"])
    assert len(pv.accepted) == 80 and not pv.refused  # même vérification qu'avec le skill
    assert run["usage"]["cache_read_input_tokens"] == 27000 and run["usd"] == api_agent.cost_usd("claude-opus-5-5", run["usage"])


def test_refusal_on_one_batch_skips_only_that_batch(env):
    run = api_agent.run("analyse", model=CLAUDE, client=FakeClient(lambda k, kw: "refusal" if k == 2 else "ok"))
    pv = handoff.check(run["results"])
    assert len(pv.accepted) == 60 and len(pv.skipped) == 20
    assert all("refus du modèle sur le paquet 2 (cyber)" in s["reason"] for s in pv.skipped)


def test_invalid_key_on_first_batch_stops_everything_cleanly(env):
    with pytest.raises(api_agent.ApiAgentError, match="vérifiez la clé"):
        api_agent.run("analyse", model=CLAUDE, client=FakeClient(lambda k, kw: _auth_error()))
    assert handoff.status()["packs"]["analyse"] == {"to_do": 80, "exported": 0, "done": 0}
    assert not list((env / "handoff" / "to-do").glob("*.json"))


def test_error_after_paid_batches_keeps_their_results(env):
    run = api_agent.run("analyse", model=CLAUDE, client=FakeClient(lambda k, kw: _auth_error() if k == 3 else "ok"))
    pv = handoff.check(run["results"])
    assert len(pv.accepted) == 60 and len(pv.skipped) == 20 and run["problems"]


def test_no_credentials_means_no_export_and_a_clear_message(env, monkeypatch, tmp_path):
    for var in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "MISTRAL_API_KEY"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    assert api_agent.has_credentials(CLAUDE) is False
    with pytest.raises(api_agent.ApiAgentError, match="Aucune clé API"):
        api_agent.run("analyse", model=CLAUDE)
    assert handoff.status()["packs"]["analyse"]["exported"] == 0


def _walk(schema):
    yield schema
    for v in schema.values():
        if isinstance(v, dict):
            yield from _walk(v)
        elif isinstance(v, list):
            for x in v:
                if isinstance(x, dict):
                    yield from _walk(x)


@pytest.mark.parametrize("pack", list(PACKS))
def test_output_schemas_respect_structured_output_limits(pack):
    schema = api_agent.results_schema(PACKS[pack])
    for node in _walk(schema):
        if node.get("type") == "object":
            assert node.get("additionalProperties") is False and set(node["required"]) == set(node["properties"])
        assert not {"minimum", "maximum", "minLength", "maxLength", "pattern", "minItems", "maxItems"} & set(node)


def test_estimate_and_engine_setting(env):
    est = api_agent.estimate("analyse")
    assert est["tasks"] == 80 and est["batches"] == 4 and est["usd"] > 0
    assert api_agent.estimate("analyse", model="claude-haiku-5-5")["usd"] < est["usd"]
    assert settings.load()["engine"] == "api"  # cycle 012 : l'API est le moteur par défaut
    settings.save(engine="skill", api_model="claude-sonnet-5-5")
    assert settings.load()["engine"] == "skill"
    settings.save(engine="api")
    assert settings.load()["engine"] == "api" and settings.load()["api_model"] == "claude-sonnet-5-5"


def test_ui_in_api_mode_shows_cost_on_the_button(env, monkeypatch):
    from streamlit.testing.v1 import AppTest
    monkeypatch.setenv("MISTRAL_API_KEY", "factice-pour-le-test")  # jamais utilisée : aucun clic de lancement ici
    settings.save(demo_mode=False, engine="api")
    for page in ["🤖 Agent", "⚙️ Réglages"]:
        at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
        at.run()
        at.sidebar.radio[0].set_value(page).run()
        assert not at.exception, [e.value for e in at.exception]
        if page == "🤖 Agent":
            assert any("Lancer l'agent (API, ≈" in b.label for b in at.button)


# ---------------------------------------------------------------- cycle 012 : API par défaut, skill en repli
from po_assist import runner  # noqa: E402


def _cfg(**kw):
    return {**settings.DEFAULTS, "api_model": CLAUDE, **kw}


def test_default_is_api_and_no_key_falls_back_to_skill(env, monkeypatch, tmp_path):
    for var in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "MISTRAL_API_KEY"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    cfg = _cfg(demo_mode=False)
    assert cfg["engine"] == "api"
    r = runner.resolve(cfg)
    assert r["engine"] == "skill" and "repli" in r["fallback_reason"]
    out = runner.run("analyse", cfg=cfg)
    assert out["engine"] == "skill" and out["pack"].exists() and "repli" in out["fallback_reason"]


def test_key_refused_on_first_batch_falls_back_to_skill(env):
    out = runner.run("analyse", cfg=_cfg(demo_mode=False), client=FakeClient(lambda k, kw: _auth_error()))
    assert out["engine"] == "skill" and "Repli sur le skill" in out["fallback_reason"]
    assert out["pack"].exists() and handoff.status()["packs"]["analyse"]["exported"] == 80


def test_api_engine_with_a_working_client_does_not_fall_back(env):
    out = runner.run("analyse", cfg=_cfg(demo_mode=False), client=FakeClient())
    assert out["engine"] == "api" and out["fallback_reason"] is None and out["batches"] == 4


def test_demo_simulates_the_api_flow(env):
    calls = []
    out = runner.run("analyse", cfg=_cfg(demo_mode=True), on_progress=lambda k, n: calls.append((k, n)))
    assert out["engine"] == "demo" and out["simulated"] and out["usd"] > 0
    assert calls == [(1, 4), (2, 4), (3, 4), (4, 4)]  # paquet par paquet, comme l'API
    assert json.loads(out["results"].read_text())["agent"].startswith("api simulée / claude-opus-5-5")
    pv, _ = handoff.import_file(out["results"])
    assert len(pv.accepted) == 80


def test_ui_without_key_shows_the_fallback(env, monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest
    for var in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "MISTRAL_API_KEY"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    settings.save(demo_mode=False)
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.run()
    at.sidebar.radio[0].set_value("🤖 Agent").run()
    assert not at.exception
    assert any("repli" in w.value for w in at.warning)
    assert any(b.label == "Exporter" for b in at.button)
