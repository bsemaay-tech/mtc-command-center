"""Shared AI-provider layer for the MTC delegation tooling.

Single source of truth for provider routing (base URL + API-key env var) and a
one-shot, no-tools `chat()` helper. Imported by both the ds_agent editor harness
and the read-only board_runner, so there is exactly one provider client layer
(no duplicate harness).

Design notes:
  - resolve_provider() mirrors the original ds_agent semantics exactly.
  - chat() takes an optional injected `client` (dependency injection) so the
    board layer is unit-testable without any network call.
"""
from __future__ import annotations

import os

# Multi-provider table. Pick with task["provider"] (default deepseek).
# Each entry = (base_url, key_env). All are OpenAI-compatible REST endpoints.
PROVIDERS: dict[str, tuple[str, str]] = {
    "deepseek":   ("https://api.deepseek.com",      "DEEPSEEK_API_KEY"),
    "xai":        ("https://api.x.ai/v1",            "XAI_API_KEY"),
    "grok":       ("https://api.x.ai/v1",            "XAI_API_KEY"),
    "openrouter": ("https://openrouter.ai/api/v1",   "OPENROUTER_API_KEY"),
    "openai":     ("https://api.openai.com/v1",       "OPENAI_API_KEY"),
    "ollama":     ("http://localhost:11434/v1",       "OLLAMA_API_KEY"),
}

DEFAULT_MODEL = "deepseek-chat"


def resolve_provider(task: dict) -> tuple[str, str, str]:
    """Return (provider, base_url, api_key) for a task dict.

    Reads the key from the provider's env var. Raises SystemExit if missing
    (same behaviour as the original ds_agent harness).
    """
    prov = (task.get("provider") or "deepseek").lower()
    base, key_env = PROVIDERS.get(prov, PROVIDERS["deepseek"])
    key = os.environ.get(key_env) or os.environ.get(
        "OLLAMA_API_KEY", "ollama" if prov == "ollama" else "")
    if not key:
        raise SystemExit(f"missing env {key_env} for provider '{prov}'")
    return prov, base, key


def make_client(prov: str = "deepseek"):
    """Build an OpenAI-compatible client for a provider. Network-free until used."""
    from openai import OpenAI  # local import so tests can run without the package wired

    _prov, base, key = resolve_provider({"provider": prov})
    return OpenAI(api_key=key, base_url=base)


def chat(
    messages: list[dict],
    *,
    prov: str = "deepseek",
    model: str | None = None,
    client=None,
    temperature: float = 0,
) -> str:
    """One-shot completion (no tools). Returns the assistant text, or "".

    Pass `client` to inject a fake/real OpenAI-compatible client. When omitted,
    a real client is built from `prov`.
    """
    if client is None:
        client = make_client(prov)
    resp = client.chat.completions.create(
        model=model or DEFAULT_MODEL,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message.content or ""
