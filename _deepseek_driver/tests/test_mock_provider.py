"""Tests for mock_provider.py — a network-free OpenAI-compatible fake client.

It plugs into provider.chat(client=...) so the board layer can run with zero
API calls in tests and dry-runs.
"""
import provider
from mock_provider import MockClient


def test_mock_client_returns_default_via_provider_chat():
    client = MockClient(default="MOCK_REPLY")
    out = provider.chat([{"role": "user", "content": "hi"}], client=client)
    assert out == "MOCK_REPLY"


def test_mock_client_responder_sees_model_and_messages():
    seen = {}

    def responder(kwargs):
        seen["model"] = kwargs["model"]
        seen["messages"] = kwargs["messages"]
        return "DYNAMIC"

    client = MockClient(responder=responder)
    out = provider.chat(
        [{"role": "user", "content": "audit this"}],
        model="worker-1",
        client=client,
    )
    assert out == "DYNAMIC"
    assert seen["model"] == "worker-1"
    assert seen["messages"][0]["content"] == "audit this"


def test_mock_client_records_calls():
    client = MockClient(default="x")
    provider.chat([{"role": "user", "content": "a"}], model="m1", client=client)
    provider.chat([{"role": "user", "content": "b"}], model="m2", client=client)
    assert len(client.calls) == 2
    assert [c["model"] for c in client.calls] == ["m1", "m2"]
