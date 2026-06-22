"""Tests for the shared provider layer (provider.py).

The provider layer is the single source of truth for AI-provider routing,
shared by the existing ds_agent editor harness and the new read-only board_runner.
No network calls: chat() takes an injected client (dependency injection).
"""
import pytest

import provider


def test_providers_map_has_expected_slugs():
    for slug in ("deepseek", "xai", "grok", "openrouter", "openai", "ollama"):
        assert slug in provider.PROVIDERS
        base, key_env = provider.PROVIDERS[slug]
        assert base.startswith("http")
        assert key_env.endswith("_API_KEY") or key_env == "OLLAMA_API_KEY"


def test_resolve_provider_defaults_to_deepseek(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-deepseek")
    prov, base, key = provider.resolve_provider({})
    assert prov == "deepseek"
    assert base == "https://api.deepseek.com"
    assert key == "sk-deepseek"


def test_resolve_provider_picks_xai(monkeypatch):
    monkeypatch.setenv("XAI_API_KEY", "sk-xai")
    prov, base, key = provider.resolve_provider({"provider": "xai"})
    assert prov == "xai"
    assert base == "https://api.x.ai/v1"
    assert key == "sk-xai"


def test_resolve_provider_missing_key_raises(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("OLLAMA_API_KEY", raising=False)
    with pytest.raises(SystemExit):
        provider.resolve_provider({"provider": "deepseek"})


class _FakeMessage:
    def __init__(self, content):
        self.content = content


class _FakeChoice:
    def __init__(self, content):
        self.message = _FakeMessage(content)


class _FakeCompletion:
    def __init__(self, content):
        self.choices = [_FakeChoice(content)]


class _FakeCompletions:
    def __init__(self, content):
        self._content = content
        self.last_kwargs = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        return _FakeCompletion(self._content)


class _FakeChat:
    def __init__(self, content):
        self.completions = _FakeCompletions(content)


class _FakeClient:
    """Stands in for openai.OpenAI — no network."""
    def __init__(self, content="HELLO FROM FAKE"):
        self.chat = _FakeChat(content)


def test_chat_uses_injected_client_and_returns_text():
    fake = _FakeClient("PONG")
    out = provider.chat(
        [{"role": "user", "content": "ping"}],
        prov="deepseek",
        model="deepseek-chat",
        client=fake,
    )
    assert out == "PONG"
    # one-shot completion: no tools wired, deterministic temperature
    assert fake.chat.completions.last_kwargs["model"] == "deepseek-chat"
    assert fake.chat.completions.last_kwargs["temperature"] == 0
    assert "tools" not in fake.chat.completions.last_kwargs


def test_chat_returns_empty_string_when_no_content():
    fake = _FakeClient(None)
    out = provider.chat([{"role": "user", "content": "x"}], client=fake)
    assert out == ""
