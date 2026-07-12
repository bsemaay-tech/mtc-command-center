from __future__ import annotations

import asyncio
import time
from pathlib import Path

from fastapi.testclient import TestClient

from bridge.app import create_app
from bridge.broker.mock import MockBroker
from bridge.engine.notify import TelegramNotifier


def test_dry_run_app_snapshot_has_bars_and_trade_data(tmp_path):
    fixture = Path(__file__).parent / "fixtures" / "BTC_1h.csv"
    broker = MockBroker.from_csv(fixture, starting_equity=100000)
    broker.streaming = True
    broker.stream_delay_s = 0.001
    app = create_app(
        dry_run=True,
        start_runtime=True,
        store_path=tmp_path / "bridge.db",
        broker=broker,
    )

    with TestClient(app) as client:
        status = client.get("/api/status").json()
        assert status["reconcile_ready"] is True
        client.post("/api/arm", headers={"X-Confirm": str(status["state_version"])})
        time.sleep(0.4)
        snapshot = client.get("/api/snapshot").json()
        bars = client.get("/api/bars?n=5").json()["bars"]
        trades = client.get("/api/trades").json()
        decisions = client.get("/api/decisions").json()

    assert app.state.bridge_status["mode"] == "dry_run"
    assert snapshot["trades"]
    assert snapshot["bars"]["bars"]
    assert bars
    assert trades
    assert decisions


def test_notifier_disabled_and_stubbed_send_never_raises():
    disabled = TelegramNotifier(enabled=False)
    asyncio.run(disabled.send("WARN", "noop"))

    sent = []
    notifier = TelegramNotifier(enabled=True, sender=lambda payload: sent.append(payload))
    asyncio.run(notifier.send("WARN", "hello"))
    assert sent[0]["text"] == "[WARN] hello"
