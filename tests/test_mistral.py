"""Cycle 013 : moteur API Mistral, testé avec un client simulé (aucun appel réseau, aucune clé, aucune dépense)."""
from __future__ import annotations

import json

import pytest

from po_assist import api_agent, handoff, runner, settings
from tests.test_handoff import perfect_output

MODEL = "mistral-large-latest"


def _tasks(payload) -> list[dict]:
    text = payload["messages"][-1]["content"]
    return json.loads(text[text.index("\n\n") + 2:])


class FakeMistral:
    """Imite MistralClient.chat(payload) ; `behaviour(k, payload)` décide de la réponse du k-ième appel."""

    def __init__(self, behaviour=None):
        self.calls = []
        self.behaviour = behaviour or (lambda k, p: "ok")

    def chat(self, payload):
        self.calls.append(payload)
        what = self.behaviour(len(self.calls), payload)
        if isinstance(what, Exception):
            raise what
        results = [{"task": t["task"], "kind": t["kind"],
                    "output": perfect_output(t["input"]["identifier"], t["input"]["text"])} for t in _tasks(payload)]
        text = "pas du JSON" if what == "garbage" else json.dumps({"results": results}, ensure_ascii=False)
        return {"choices": [{"message": {"role": "assistant", "content": text},
                             "finish_reason": "length" if what == "truncated" else "stop"}],
                "usage": {"prompt_tokens": 12000, "completion_tokens": 15000, "total_tokens": 27000}}


def test_default_model_is_mistral_and_both_providers_are_offered(env):
    assert settings.load()["api_model"] == MODEL == api_agent.DEFAULT_MODEL
    assert api_agent.provider_of(MODEL) == "mistral" and api_agent.provider_of("claude-opus-5-5") == "anthropic"
    assert {api_agent.provider_of(m) for m in api_agent.MODELS} == {"mistral", "anthropic"}
    assert set(api_agent.MODELS) == set(api_agent.PRICES)


def test_mistral_run_batches_constrains_and_imports(env):
    client = FakeMistral()
    run = api_agent.run("analyse", model=MODEL, client=client)
    assert run["batches"] == 4 and len(client.calls) == 4
    first = client.calls[0]
    assert first["model"] == MODEL
    assert [m["role"] for m in first["messages"]] == ["system", "user"]
    assert all(c["messages"][0] == first["messages"][0] for c in client.calls), "instructions identiques d'un paquet à l'autre"
    rf = first["response_format"]
    assert rf["type"] == "json_schema" and rf["json_schema"]["strict"] is True
    assert rf["json_schema"]["schema"]["required"] == ["results"]
    doc = json.loads(run["results"].read_text())
    assert doc["agent"] == f"api / {MODEL}"
    pv, _ = handoff.import_file(run["results"])
    assert len(pv.accepted) == 80 and not pv.refused  # même vérification qu'avec Claude ou le skill
    assert run["usage"]["input_tokens"] == 48000 and run["usage"]["output_tokens"] == 60000
    assert run["usd"] == api_agent.cost_usd(MODEL, run["usage"]) > 0


def test_rejected_schema_is_retried_once_in_json_mode(env):
    def behaviour(k, payload):
        return api_agent.MistralHTTPError(422, "schema") if payload["response_format"]["type"] == "json_schema" else "ok"
    client = FakeMistral(behaviour)
    run = api_agent.run("analyse", model=MODEL, client=client)
    assert len(client.calls) == 8  # 4 paquets, chacun repris une fois
    retry = client.calls[1]
    assert retry["response_format"] == {"type": "json_object"} and "Schéma JSON imposé" in retry["messages"][0]["content"]
    assert len(handoff.check(run["results"]).accepted) == 80


@pytest.mark.parametrize("status", [401, 403, 404])
def test_refused_key_on_first_batch_stops_cleanly_and_runner_falls_back(env, status):
    refuse = lambda k, p: api_agent.MistralHTTPError(status)  # noqa: E731
    with pytest.raises(api_agent.ApiAgentError, match="Mistral refuse la requête"):
        api_agent.run("analyse", model=MODEL, client=FakeMistral(refuse))
    assert handoff.status()["packs"]["analyse"] == {"to_do": 80, "exported": 0, "done": 0}
    assert not list((env / "handoff" / "to-do").glob("*.json"))
    out = runner.run("analyse", cfg={**settings.DEFAULTS, "demo_mode": False}, client=FakeMistral(refuse))
    assert out["engine"] == "skill" and "Repli sur le skill" in out["fallback_reason"]


def test_refusal_after_paid_batches_keeps_their_results(env):
    run = api_agent.run("analyse", model=MODEL,
                        client=FakeMistral(lambda k, p: api_agent.MistralHTTPError(401) if k == 3 else "ok"))
    pv = handoff.check(run["results"])
    assert len(pv.accepted) == 60 and len(pv.skipped) == 20 and run["problems"]


@pytest.mark.parametrize("what,reason", [(api_agent.MistralHTTPError(429), "HTTP 429"),
                                         (api_agent.MistralHTTPError(0, "ConnectError"), "ConnectError"),
                                         ("truncated", "tronquée"), ("garbage", "illisible")])
def test_one_bad_batch_skips_only_that_batch(env, what, reason):
    run = api_agent.run("analyse", model=MODEL, client=FakeMistral(lambda k, p: what if k == 2 else "ok"))
    pv = handoff.check(run["results"])
    assert len(pv.accepted) == 60 and len(pv.skipped) == 20
    assert all(reason in s["reason"] for s in pv.skipped)


class _Resp:
    def __init__(self, status, body=None):
        self.status_code, self._body, self.text = status, body or {}, json.dumps(body or {"message": "x"})

    def json(self):
        return self._body


def test_client_retries_rate_limits_then_succeeds_and_never_leaks_the_key(monkeypatch):
    import httpx2
    seen, waits = [], []
    answers = [_Resp(429), _Resp(503), _Resp(200, {"choices": []})]
    monkeypatch.setattr(httpx2, "post", lambda url, **kw: seen.append(kw) or answers.pop(0))
    client = api_agent.MistralClient(api_key="cle-factice", sleep=waits.append)
    assert client.chat({"model": MODEL}) == {"choices": []}
    assert len(seen) == 3 and waits == [2.0, 4.0]
    assert seen[0]["headers"]["Authorization"] == "Bearer cle-factice"
    monkeypatch.setattr(httpx2, "post", lambda url, **kw: _Resp(401))
    with pytest.raises(api_agent.MistralHTTPError) as e:
        api_agent.MistralClient(api_key="cle-factice", sleep=waits.append).chat({})
    assert e.value.status == 401 and "cle-factice" not in str(e.value) + e.value.detail


def test_no_mistral_key_falls_back_with_the_right_variable_name(env, monkeypatch):
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "factice")  # une clé Claude ne suffit pas pour un modèle Mistral
    assert api_agent.has_credentials(MODEL) is False
    r = runner.resolve({**settings.DEFAULTS, "demo_mode": False})
    assert r["engine"] == "skill" and "MISTRAL_API_KEY" in r["fallback_reason"]
    with pytest.raises(api_agent.ApiAgentError, match="MISTRAL_API_KEY"):
        api_agent.run("analyse", model=MODEL)
    monkeypatch.setenv("MISTRAL_API_KEY", "factice")
    assert api_agent.has_credentials(MODEL) and runner.resolve({**settings.DEFAULTS, "demo_mode": False})["engine"] == "api"


def test_mistral_estimate_has_no_cache_discount(env):
    est = api_agent.estimate("analyse", model=MODEL)
    assert est["tasks"] == 80 and est["batches"] == 4 and est["usd"] > 0
    assert api_agent.estimate("analyse", model="mistral-small-latest")["usd"] < est["usd"]


def test_settings_page_names_the_mistral_key(env, monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest
    from tests.test_api import ROOT
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
    settings.save(demo_mode=False)
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.run()
    at.sidebar.radio[0].set_value("⚙️ Réglages").run()
    assert not at.exception, [e.value for e in at.exception]
    text = " ".join(m.value for m in at.markdown)
    assert "Clé API Mistral : **absente**" in text and "MISTRAL_API_KEY" in text
