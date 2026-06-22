"""Network-free OpenAI-compatible fake client for tests and board dry-runs.

Plugs into provider.chat(client=MockClient(...)) so the Boardroom can run its
full fan-out + judge flow with zero API calls and fully deterministic output.
"""
from __future__ import annotations

from typing import Callable


class _Message:
    def __init__(self, content):
        self.content = content


class _Choice:
    def __init__(self, content):
        self.message = _Message(content)


class _Completion:
    def __init__(self, content):
        self.choices = [_Choice(content)]


class _Completions:
    def __init__(self, client: "MockClient"):
        self._client = client

    def create(self, **kwargs):
        self._client.calls.append(kwargs)
        if self._client.responder is not None:
            content = self._client.responder(kwargs)
        else:
            content = self._client.default
        return _Completion(content)


class _Chat:
    def __init__(self, client: "MockClient"):
        self.completions = _Completions(client)


class MockClient:
    """Mimics openai.OpenAI for chat.completions.create.

    Args:
      responder: optional callable(kwargs) -> str for dynamic replies. Receives
                 the raw create() kwargs (model, messages, temperature, ...).
      default:   static reply text used when no responder is given.
    """

    def __init__(self, responder: Callable[[dict], str] | None = None, default: str = "MOCK"):
        self.responder = responder
        self.default = default
        self.calls: list[dict] = []
        self.chat = _Chat(self)
