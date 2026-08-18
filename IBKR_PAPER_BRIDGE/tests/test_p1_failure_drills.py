from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

from bridge.broker.base import SubmissionDisposition, SubmissionOutcome
from bridge.broker.mock import MockBroker
from bridge.engine.bars import BarFeed
from bridge.engine.engine import BridgeEngine
from bridge.engine.llm_gate import LLMGate
from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.types import Bar, Signal
from bridge.store.db import Store


def test_drill_disconnect_reconnect_dedupes_to_one_order(tmp_path):
    asyncio.run(_disconnect_reconnect_dedupes_to_one_order(tmp_path))


def test_drill_duplicate_candle_creates_one_decision_and_order(tmp_path):
    asyncio.run(_duplicate_candle_creates_one_decision_and_order(tmp_path))


def test_new_run_can_replay_bar_timestamp_from_prior_run(tmp_path):
    asyncio.run(_new_run_can_replay_bar_timestamp_from_prior_run(tmp_path))


def test_drill_three_order_rejects_auto_disarm(tmp_path):
    asyncio.run(_three_order_rejects_auto_disarm(tmp_path))


def test_drill_llm_timeout_skips_and_loop_proceeds(tmp_path):
    asyncio.run(_llm_timeout_skips_and_loop_proceeds(tmp_path))


def test_drill_kill_mid_await_preempts_submit(tmp_path):
    asyncio.run(_kill_mid_await_preempts_submit(tmp_path))


def test_drill_data_stale_auto_disarms(tmp_path):
    asyncio.run(_data_stale_auto_disarms(tmp_path))


async def _disconnect_reconnect_dedupes_to_one_order(tmp_path) -> None:
    bars = _bars(2)
    broker = MockBroker(bars=bars, starting_equity=100000, streaming=True)
    engine = _engine(tmp_path, broker, AlwaysSignalStrategy(), run_id="disconnect")
    await broker.connect()
    feed = BarFeed(broker, "BTC", "1h", engine.on_bar, poll_seconds=100)
    await feed.start(lookback=0)

    broker.emit_bar(bars[0])
    await asyncio.sleep(0.02)
    assert await feed.reconnect(attempts=1, base_delay=0)
    broker.emit_bar(bars[0])
    await asyncio.sleep(0.02)
    await feed.stop()

    orders = engine.store.get_snapshot()["orders"]
    assert len([order for order in orders if order["role"] == "ENTRY"]) == 1
    assert broker.resubscribe_count == 1


async def _duplicate_candle_creates_one_decision_and_order(tmp_path) -> None:
    bars = _bars(2)
    broker = MockBroker(bars=bars, starting_equity=100000)
    engine = _engine(tmp_path, broker, AlwaysSignalStrategy(), run_id="duplicate")
    await broker.connect()

    await engine.on_bar(bars[0])
    await engine.on_bar(bars[0])

    decisions = engine.store.get_decisions()
    assert len([row for row in decisions if row["stage"] == "SIGNAL"]) == 1
    assert len([row for row in engine.store.get_snapshot()["orders"] if row["role"] == "ENTRY"]) == 1


async def _new_run_can_replay_bar_timestamp_from_prior_run(tmp_path) -> None:
    bars = _bars(2)
    broker = MockBroker(bars=bars, starting_equity=100000)
    first = _engine(tmp_path, broker, AlwaysSignalStrategy(), run_id="replay-one")
    await broker.connect()
    await first.on_bar(bars[0])

    store = Store(tmp_path / "replay-one.db")
    store.initialize()
    store.create_run("replay-two", "dry_run", "testnet", {})
    second = BridgeEngine(
        run_id="replay-two",
        broker=broker,
        store=store,
        strategy=AlwaysSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        state="ARMED",
    )
    store.set_meta("app_state", "ARMED")
    await second.on_bar(bars[0])

    # Durable cross-run identity blocks the second broker submission:
    # same intent (strategy + symbol + direction + signal_ts) → BLOCKED
    entries = [row for row in store.get_snapshot()["orders"] if row["role"] == "ENTRY"]
    assert len(entries) == 1


async def _three_order_rejects_auto_disarm(tmp_path) -> None:
    bars = _bars(4)
    broker = RejectingBroker(bars=bars, starting_equity=100000)
    engine = _engine(tmp_path, broker, AlwaysSignalStrategy(), run_id="rejects")
    await broker.connect()

    for idx in range(3):
        await engine.on_bar(bars[idx])
        if idx < 2:
            assert engine.state == "ARMED"

    assert engine.state == "DISARMED"
    assert len([row for row in engine.store.get_decisions() if row["stage"] == "REJECTED"]) == 3
    assert engine.store.get_events()[0]["code"] == "ORDER_REJECT_LIMIT"


async def _llm_timeout_skips_and_loop_proceeds(tmp_path) -> None:
    async def slow_veto(_plan):
        await asyncio.sleep(0.05)
        return {"verdict": "VETO", "reason": "late"}

    bars = _bars(2)
    broker = MockBroker(bars=bars, starting_equity=100000)
    gate = LLMGate(veto_enabled=True, veto_provider=slow_veto, veto_deadline_s=0.001)
    engine = _engine(tmp_path, broker, AlwaysSignalStrategy(), run_id="llm-timeout", llm_gate=gate)
    await broker.connect()

    await asyncio.wait_for(engine.on_bar(bars[0]), timeout=0.1)

    stages = [row["stage"] for row in engine.store.get_decisions()]
    assert "LLM_SKIPPED" in stages
    assert "SUBMITTED" in stages


async def _kill_mid_await_preempts_submit(tmp_path) -> None:
    bars = _bars(2)
    broker = MockBroker(bars=bars, starting_equity=100000)
    engine = _engine(tmp_path, broker, AlwaysSignalStrategy(), run_id="kill-await")
    engine.llm_gate = KillingGate(engine)
    await broker.connect()

    await engine.on_bar(bars[0])

    assert engine.state == "KILLED"
    assert engine.store.get_snapshot()["orders"] == []


async def _data_stale_auto_disarms(tmp_path) -> None:
    bars = _bars(1)
    broker = MockBroker(bars=bars, starting_equity=100000, streaming=True)
    engine = _engine(tmp_path, broker, AlwaysSignalStrategy(), run_id="stale")
    feed = BarFeed(
        broker,
        "BTC",
        "1h",
        engine.on_bar,
        on_event=engine._feed_event,
        on_stale=engine._stale_disarm,
    )
    feed.last_bar_update = bars[0].ts

    await feed.check_once(bars[0].ts + timedelta(hours=2, seconds=1))

    assert engine.state == "DISARMED"
    assert engine.store.get_events()[-1]["code"] == "DATA_STALE"


def _engine(tmp_path, broker, strategy, run_id: str, llm_gate=None) -> BridgeEngine:
    store = Store(tmp_path / f"{run_id}.db")
    store.initialize()
    store.create_run(run_id, "dry_run", "testnet", {})
    return BridgeEngine(
        run_id=run_id,
        broker=broker,
        store=store,
        strategy=strategy,
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        llm_gate=llm_gate,
        state="ARMED",
    )


def _bars(count: int) -> list[Bar]:
    base = datetime(2026, 7, 12, 0, tzinfo=UTC)
    return [
        Bar(
            ts=base + timedelta(hours=idx),
            open=100 + idx,
            high=102 + idx,
            low=98 + idx,
            close=100 + idx,
            volume=1,
        )
        for idx in range(count)
    ]


class AlwaysSignalStrategy:
    symbol = "BTC"
    warmup_bars = 0

    def on_bar(self, bars, position):
        return Signal(
            ts=bars[-1].ts,
            symbol="BTC",
            direction="LONG",
            reason="drill",
            ref_price=bars[-1].close,
            stop_loss=bars[-1].close - 5,
        )

    def trail_level(self, bars, position):
        return None


class RejectingBroker(MockBroker):
    async def place_bracket(self, plan):
        return SubmissionOutcome(
            SubmissionDisposition.DEFINITIVE_REJECTION,
            {},
            "SCRIPTED_DEFINITIVE_REJECTION",
        )


class KillingGate:
    def __init__(self, engine: BridgeEngine) -> None:
        self.engine = engine

    async def check(self, plan):
        await self.engine.kill(flatten=False)

        class Result:
            verdict = "SKIPPED"
            reason = "kill drill"

        return Result()


class _WsDeadBroker:
    """B1 stub: broker whose SDK websocket reports dead."""

    def __init__(
        self,
        alive: bool = False,
        reconnect_ok: bool = True,
        failures_before_success: int = 0,
    ) -> None:
        self.alive = alive
        self.reconnect_ok = reconnect_ok
        self.failures_before_success = failures_before_success
        self.connect_calls = 0
        self.resubscribe_calls = 0
        self.last_bar_update = None

    def ws_alive(self) -> bool:
        return self.alive

    async def connect(self) -> None:
        self.connect_calls += 1
        if not self.reconnect_ok or self.connect_calls <= self.failures_before_success:
            raise RuntimeError("socket refused")
        self.alive = True

    async def resubscribe(self) -> None:
        self.resubscribe_calls += 1


def test_drill_ws_death_triggers_auto_reconnect():
    async def run() -> None:
        broker = _WsDeadBroker(alive=False, reconnect_ok=True)
        events: list[tuple[str, str]] = []
        feed = BarFeed(
            broker,
            "BTC",
            "1h",
            on_bar_closed=lambda bar: None,
            on_event=lambda code, detail: events.append((code, detail)),
        )

        await feed.check_once(datetime(2026, 7, 12, tzinfo=UTC))

        assert broker.connect_calls == 1
        assert broker.resubscribe_calls == 1
        codes = [code for code, _ in events]
        assert "DISCONNECT" in codes and "RECONNECT" in codes
        assert "DATA_STALE" not in codes

    asyncio.run(run())


def test_drill_ws_death_survives_three_minute_outage_within_retry_budget(monkeypatch):
    async def run() -> None:
        broker = _WsDeadBroker(alive=False, failures_before_success=6)
        events: list[tuple[str, str]] = []
        stale_calls: list[bool] = []
        scheduled_delays: list[float] = []

        async def record_sleep(delay: float) -> None:
            scheduled_delays.append(delay)

        monkeypatch.setattr("bridge.engine.bars.asyncio.sleep", record_sleep)
        feed = BarFeed(
            broker,
            "BTC",
            "1h",
            on_bar_closed=lambda bar: None,
            on_event=lambda code, detail: events.append((code, detail)),
            on_stale=lambda: stale_calls.append(True),
        )

        await feed.check_once(datetime(2026, 7, 12, tzinfo=UTC))

        assert broker.connect_calls == 7
        assert scheduled_delays == [5.0, 10.0, 20.0, 40.0, 60.0, 60.0]
        assert sum(scheduled_delays) == 195.0
        assert ("RECONNECT", "attempt=7") in events
        assert not any(code == "DATA_STALE" for code, _ in events)
        assert stale_calls == []

    asyncio.run(run())


def test_drill_ws_death_reconnect_failure_goes_stale_after_full_budget(monkeypatch, tmp_path):
    async def run() -> None:
        broker = _WsDeadBroker(alive=False, reconnect_ok=False)
        events: list[tuple[str, str]] = []
        scheduled_delays: list[float] = []
        store = Store(tmp_path / "reconnect-budget.db")
        store.initialize()
        store.create_run("reconnect-budget", "paper", "testnet", {})
        store.set_meta("app_state", "ARMED")
        engine = BridgeEngine(
            run_id="reconnect-budget",
            broker=broker,
            store=store,
            strategy=AlwaysSignalStrategy(),
            risk_engine=RiskEngine(RiskConfig()),
            state="ARMED",
        )

        async def record_sleep(delay: float) -> None:
            scheduled_delays.append(delay)

        monkeypatch.setattr("bridge.engine.bars.asyncio.sleep", record_sleep)
        feed = BarFeed(
            broker,
            "BTC",
            "1h",
            on_bar_closed=lambda bar: None,
            on_event=lambda code, detail: events.append((code, detail)),
            on_stale=engine._stale_disarm,
        )

        await feed.check_once(datetime(2026, 7, 12, tzinfo=UTC))

        assert broker.connect_calls == 9
        assert scheduled_delays == [5.0, 10.0, 20.0, 40.0, 60.0, 60.0, 60.0, 60.0]
        assert sum(scheduled_delays) == 315.0
        codes = [code for code, _ in events]
        assert codes.count("RECONNECT_RETRY") == 9
        assert ("DATA_STALE", "ws_dead_reconnect_failed") in events
        assert engine._app_state() == "DISARMED"

    asyncio.run(run())
