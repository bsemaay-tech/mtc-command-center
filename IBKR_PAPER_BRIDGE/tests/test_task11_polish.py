from __future__ import annotations

import asyncio

from fastapi.testclient import TestClient

from bridge.app import create_app
from bridge.engine.notify import TelegramNotifier


def test_dry_run_app_snapshot_has_bars_and_trade_data():
    client = TestClient(create_app(dry_run=True))

    snapshot = client.get("/api/snapshot").json()
    bars = client.get("/api/bars?n=5").json()

    assert snapshot["status"]["mode"] == "dry_run"
    assert snapshot["trades"]
    assert bars["bars"]


def test_notifier_disabled_and_stubbed_send_never_raises():
    disabled = TelegramNotifier(enabled=False)
    asyncio.run(disabled.send("WARN", "noop"))

    sent = []
    notifier = TelegramNotifier(enabled=True, sender=lambda payload: sent.append(payload))
    asyncio.run(notifier.send("WARN", "hello"))
    assert sent[0]["text"] == "[WARN] hello"
