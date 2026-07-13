from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(autouse=True)
def _no_real_telegram(monkeypatch):
    """Monkeypatch resolve_telegram_credentials at both import sites so tests
    cannot fall through to real HKCU Telegram credentials."""
    monkeypatch.setattr(
        "bridge.settings.resolve_telegram_credentials", lambda: ("", "")
    )
    monkeypatch.setattr(
        "bridge.engine.notify.resolve_telegram_credentials", lambda: ("", "")
    )
