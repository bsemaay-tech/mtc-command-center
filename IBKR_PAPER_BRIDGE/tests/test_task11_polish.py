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
        # Poll instead of a fixed sleep — the streamed replay races a fixed
        # 0.4 s under machine load (flake seen while the paper instance ran).
        deadline = time.time() + 10
        snapshot = client.get("/api/snapshot").json()
        while time.time() < deadline and not (snapshot.get("decisions") and snapshot.get("trades")):
            time.sleep(0.2)
            snapshot = client.get("/api/snapshot").json()
        bars = client.get("/api/bars?n=5").json()["bars"]
        trades = client.get("/api/trades").json()
        decisions = client.get("/api/decisions").json()
        assert snapshot["decisions"]

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


def test_build_notifier_disabled_without_creds(monkeypatch):
    """B5: missing creds => silently disabled, never raises."""
    import bridge.engine.notify as notify_mod

    monkeypatch.setattr(notify_mod, "resolve_telegram_credentials", lambda: ("", ""))
    notifier = notify_mod.build_notifier()
    assert notifier.enabled is False
    asyncio.run(notifier.send("WARN", "should be a no-op"))


def test_build_notifier_enabled_sends_via_http_sender(monkeypatch):
    import bridge.engine.notify as notify_mod

    sent: list[dict] = []

    def fake_sender(token, chat_id):
        async def send(payload):
            sent.append({"chat_id": chat_id, **payload})
        return send

    monkeypatch.setattr(notify_mod, "resolve_telegram_credentials", lambda: ("tok", "42"))
    monkeypatch.setattr(notify_mod, "_http_sender", fake_sender)
    notifier = notify_mod.build_notifier()
    assert notifier.enabled is True
    asyncio.run(notifier.send("INFO", "hello"))
    assert sent == [{"chat_id": "42", "text": "[INFO] hello"}]


def test_notifier_send_failure_never_raises():
    from bridge.engine.notify import TelegramNotifier

    async def exploding_sender(payload):
        raise RuntimeError("boom")

    notifier = TelegramNotifier(enabled=True, sender=exploding_sender)
    asyncio.run(notifier.send("ERROR", "x"))  # must not raise
