from __future__ import annotations

import asyncio
from pathlib import Path
from datetime import UTC, datetime, timedelta

import pytest

from bridge.broker.mock import MockBroker
from bridge.engine.engine import BridgeEngine
from bridge.engine.orders import OrderManager
from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from bridge.engine.types import Bar, Position, Signal
from bridge.store.db import Store

FIXTURES = Path(__file__).parent / "fixtures"


def test_dryrun_replay_creates_trade_and_decision_chain(tmp_path):
    asyncio.run(_run_dryrun_replay(tmp_path))


def test_engine_uses_broker_protocol_not_mockbroker_bars(tmp_path):
    asyncio.run(_run_protocol_broker_replay(tmp_path))


def test_strategy_drives_stop(tmp_path):
    asyncio.run(_run_strategy_stop(tmp_path))


def test_position_blocks_entry(tmp_path):
    asyncio.run(_run_position_blocks_entry(tmp_path))


def test_disarm_mid_await_no_submit(tmp_path):
    asyncio.run(_run_disarm_mid_await_no_submit(tmp_path))


def test_decision_chain_records_trade_closed(tmp_path):
    asyncio.run(_run_decision_chain_records_trade_closed(tmp_path))


def test_reconciler_tolerates_two_failures_then_disarms_on_third(tmp_path):
    asyncio.run(_reconciler_tolerates_two_failures_then_disarms_on_third(tmp_path))


def test_reconciler_success_resets_consecutive_failure_budget(tmp_path):
    asyncio.run(_reconciler_success_resets_consecutive_failure_budget(tmp_path))


def test_arm_requires_fresh_reconcile_evidence(tmp_path):
    asyncio.run(_arm_requires_fresh_reconcile_evidence(tmp_path))


async def _run_dryrun_replay(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    broker = MockBroker.from_csv(FIXTURES / "BTC_1h.csv", starting_equity=100000)
    risk = RiskEngine(RiskConfig(max_position_notional_pct=0.5))
    engine = BridgeEngine(
        run_id="dryrun-test",
        broker=broker,
        store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=risk,
        state="ARMED",
    )

    await engine.run_replay(max_bars=60)

    snapshot = store.get_snapshot()
    assert snapshot["trades"]
    chain = store.get_decision_chain(snapshot["trades"][0]["entry_decision_uid"])
    stages = [row["stage"] for row in chain]
    assert stages[:3] == ["SIGNAL", "RISK_PASS", "LLM_SKIPPED"]
    assert "SUBMITTED" in stages
    assert snapshot["orders"]


async def _run_protocol_broker_replay(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    broker = ProtocolOnlyBroker(
        bars=[
            Bar(
                ts=datetime(2026, 7, 6, 0, tzinfo=UTC),
                open=100,
                high=101,
                low=99,
                close=100,
                volume=1,
            )
        ]
    )
    engine = BridgeEngine(
        run_id="protocol-broker",
        broker=broker,
        store=store,
        strategy=NoSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        state="ARMED",
    )

    await engine.run_replay(max_bars=1)

    snapshot = store.get_snapshot()
    assert len(snapshot["bars"]) == 1
    assert broker.connected is True


async def _run_strategy_stop(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    bar = Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=102, low=99, close=100, volume=1)
    broker = RecordingBroker([bar])
    engine = BridgeEngine(
        run_id="strategy-stop",
        broker=broker,
        store=store,
        strategy=FixedSignalStrategy(stop_loss=90.0, take_profit=115.0),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        state="ARMED",
    )

    await engine.run_replay(max_bars=1)

    trade = store.get_snapshot()["trades"][0]
    assert trade["sl_initial"] == 90.0
    assert trade["tp_initial"] == 115.0


async def _run_position_blocks_entry(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    bar = Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=102, low=99, close=100, volume=1)
    broker = RecordingBroker(
        [bar],
        positions=[
            Position(
                symbol="BTC",
                size=0.5,
                entry_px=95.0,
                unrealized=1.0,
            )
        ],
    )
    engine = BridgeEngine(
        run_id="position-block",
        broker=broker,
        store=store,
        strategy=FixedSignalStrategy(stop_loss=90.0, take_profit=115.0),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        state="ARMED",
    )

    await engine.run_replay(max_bars=1)

    assert store.get_snapshot()["trades"] == []
    assert broker.submitted == []


async def _run_disarm_mid_await_no_submit(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    store.set_meta("app_state", "ARMED")
    bar = Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=102, low=99, close=100, volume=1)
    broker = RecordingBroker([bar])
    engine = BridgeEngine(
        run_id="mid-await-disarm",
        broker=broker,
        store=store,
        strategy=FixedSignalStrategy(stop_loss=90.0, take_profit=115.0),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        llm_gate=DisarmingGate(store),
        state="ARMED",
    )

    await engine.run_replay(max_bars=1)

    assert store.get_meta("app_state") == "DISARMED"
    assert broker.submitted == []
    assert store.get_snapshot()["trades"] == []


async def _run_decision_chain_records_trade_closed(tmp_path):
    bars = [
        Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=101, low=99, close=100, volume=1),
        Bar(ts=datetime(2026, 7, 6, 1, tzinfo=UTC), open=101, high=104, low=100, close=103, volume=1),
        Bar(ts=datetime(2026, 7, 6, 2, tzinfo=UTC), open=103, high=104, low=94, close=96, volume=1),
    ]
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    broker = MockBroker(bars=bars, starting_equity=100000)
    engine = BridgeEngine(
        run_id="closed-chain",
        broker=broker,
        store=store,
        strategy=FixedSignalStrategy(stop_loss=95.0, take_profit=None),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        state="ARMED",
    )

    await engine.run_replay(max_bars=3)

    trade = store.get_snapshot()["trades"][0]
    stages = [row["stage"] for row in store.get_decision_chain(trade["entry_decision_uid"])]
    assert "TRADE_CLOSED" in stages
    assert trade["exit_reason"] == "SL"


async def _reconciler_tolerates_two_failures_then_disarms_on_third(tmp_path):
    store = Store(tmp_path / "reconciler.db")
    store.initialize()
    store.create_run("reconciler", "paper", "testnet", {})
    store.set_meta("app_state", "ARMED")
    broker = MockBroker([], starting_equity=1000)
    manager = ScriptedOrderManager([RuntimeError("one"), RuntimeError("two"), RuntimeError("three")])
    engine = BridgeEngine(
        run_id="reconciler",
        broker=broker,
        store=store,
        strategy=NoSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig()),
        order_manager=manager,
        state="ARMED",
    )
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC)

    for expected_count in (1, 2):
        assert await engine._run_reconcile_cycle() is False
        assert engine._app_state() == "ARMED"
        assert engine.reconcile_ready is False
        assert engine.reconcile_error == "RuntimeError"
        tolerated = [
            row for row in store.get_events() if row["code"] == "RECONCILE_FAILED_TOLERATED"
        ]
        assert tolerated[0]["severity"] == "WARN"
        assert tolerated[0]["detail"] == f"consecutive={expected_count}/3; error=RuntimeError"

    assert await engine._run_reconcile_cycle() is False
    assert engine._app_state() == "DISARMED"
    failed = [row for row in store.get_events() if row["code"] == "RECONCILE_FAILED"]
    assert len(failed) == 1
    assert failed[0]["severity"] == "ERROR"
    assert failed[0]["detail"].startswith("consecutive=3/3; error=RuntimeError; stack=")


async def _reconciler_success_resets_consecutive_failure_budget(tmp_path):
    store = Store(tmp_path / "reconciler-reset.db")
    store.initialize()
    store.create_run("reconciler-reset", "paper", "testnet", {})
    store.set_meta("app_state", "ARMED")
    broker = MockBroker([], starting_equity=1000)
    manager = ScriptedOrderManager(
        [RuntimeError("one"), RuntimeError("two"), None, RuntimeError("three"), RuntimeError("four")]
    )
    engine = BridgeEngine(
        run_id="reconciler-reset",
        broker=broker,
        store=store,
        strategy=NoSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig()),
        order_manager=manager,
        state="ARMED",
    )
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC)

    assert await engine._run_reconcile_cycle() is False
    assert await engine._run_reconcile_cycle() is False
    assert await engine._run_reconcile_cycle() is True
    assert engine._consecutive_reconcile_failures == 0
    assert await engine._run_reconcile_cycle() is False
    assert await engine._run_reconcile_cycle() is False

    assert engine._app_state() == "ARMED"
    assert engine._consecutive_reconcile_failures == 2
    events = store.get_events()
    assert sum(row["code"] == "RECONCILE_FAILED_TOLERATED" for row in events) == 4
    assert not any(row["code"] == "RECONCILE_FAILED" for row in events)
    assert any(row["code"] == "RECONCILE_RECOVERED" for row in events)


async def _arm_requires_fresh_reconcile_evidence(tmp_path):
    store = Store(tmp_path / "arm-freshness.db")
    store.initialize()
    store.create_run("arm-freshness", "paper", "testnet", {})
    broker = MockBroker([], starting_equity=1000)
    engine = BridgeEngine(
        run_id="arm-freshness",
        broker=broker,
        store=store,
        strategy=NoSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig()),
        state="DISARMED",
    )
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC) - timedelta(minutes=10)

    with pytest.raises(RuntimeError, match="reconcile evidence stale"):
        await engine.arm()
    assert store.get_meta("app_state") == "DISARMED"

    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC)
    await engine.arm()
    assert store.get_meta("app_state") == "ARMED"
    codes = [row["code"] for row in store.get_events()]
    assert codes.count("ARM_REQUEST") == 2
    assert "STATE_TRANSITION" in codes


def test_order_manager_duplicate_and_disarmed_guards(tmp_path):
    asyncio.run(_run_order_manager_guards(tmp_path))


async def _run_order_manager_guards(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    store.create_run("run", "dry_run", "testnet", {})
    broker = MockBroker.from_csv(FIXTURES / "BTC_1h.csv", starting_equity=100000)
    await broker.connect()
    manager = OrderManager(store=store, broker=broker, run_id="run")

    engine = BridgeEngine(
        run_id="run",
        broker=broker,
        store=store,
        strategy=KeltnerTrailEma8(),
        order_manager=manager,
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        state="ARMED",
    )
    await engine.run_replay(max_bars=25)
    first_order_count = len(store.get_snapshot()["orders"])
    await engine.run_replay(max_bars=25)
    assert len(store.get_snapshot()["orders"]) == first_order_count

    engine.disarm()
    await engine.run_replay(max_bars=60)
    assert engine.state == "DISARMED"


class NoSignalStrategy:
    id = "no_signal"
    warmup_bars = 0

    def on_bar(self, bars, position):
        return None

    def trail_level(self, bars, position):
        return None


class ScriptedOrderManager:
    def __init__(self, outcomes: list[Exception | None]) -> None:
        self.outcomes = list(outcomes)

    async def reconcile(self) -> None:
        outcome = self.outcomes.pop(0)
        if outcome is not None:
            raise outcome


class ProtocolOnlyBroker:
    coin = "BTC"

    def __init__(self, bars: list[Bar]) -> None:
        self._replay = bars
        self.connected = False

    async def connect(self) -> None:
        self.connected = True

    async def account(self) -> dict:
        return {"equity": 100000.0, "available_margin": 100000.0}

    async def positions(self) -> list:
        return []

    async def open_orders(self) -> list:
        return []

    async def historical_bars(self, coin: str, tf: str, lookback: int) -> list[Bar]:
        return self._replay[-lookback:]

    def subscribe_bars(self, coin: str, tf: str, on_bar_closed) -> None:
        for bar in self._replay:
            on_bar_closed(bar)

    async def place_bracket(self, plan) -> dict:
        raise AssertionError("no signal should be submitted")

    async def modify_stop(self, cloid: str, new_stop: float) -> None:
        raise AssertionError("no stop should be modified")

    async def cancel(self, cloid: str) -> None:
        return None

    async def cancel_all(self) -> None:
        return None

    async def flatten(self, coin: str) -> None:
        return None


class FixedSignalStrategy:
    id = "fixed_signal"
    warmup_bars = 0
    symbol = "BTC"

    def __init__(self, stop_loss: float, take_profit: float | None = None, direction: str = "LONG") -> None:
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.direction = direction

    def on_bar(self, bars, position):
        return Signal(
            ts=bars[-1].ts,
            symbol=self.symbol,
            direction=self.direction,
            reason="fixed",
            ref_price=bars[-1].close,
            stop_loss=self.stop_loss,
            take_profit=self.take_profit,
        )

    def trail_level(self, bars, position):
        return None


class RecordingBroker(ProtocolOnlyBroker):
    def __init__(self, bars: list[Bar], positions: list[Position] | None = None) -> None:
        super().__init__(bars)
        self._positions = positions or []
        self.submitted: list = []

    async def positions(self) -> list[Position]:
        return list(self._positions)

    async def place_bracket(self, plan) -> dict:
        self.submitted.append(plan)
        return {
            "entry": {
                "cloid": f"{plan.signal.ts.timestamp()}:entry",
                "oid": 1,
                "role": "ENTRY",
                "status": "FILLED",
                "qty": plan.qty,
                "avg_fill_px": plan.signal.ref_price,
            }
        }


class DisarmingGate:
    def __init__(self, store: Store) -> None:
        self.store = store

    async def check(self, plan):
        self.store.set_meta("app_state", "DISARMED")

        class Result:
            reason = "test disarm"

        return Result()


# ===========================================================================
# TS-P1-004 — engine participation: pre-ARM suppression and the re-ARM gate
# ===========================================================================

from bridge.engine.types import FillEvent, PartialProtectionState, Position  # noqa: E402


def _partial_engine(tmp_path, *, position_size: float = 1.0):
    """v5 store + a partially filled owned entry + a wired engine."""
    store = Store(tmp_path / "bridge.db")
    store.initialize(target_schema_version=5)
    store.create_run("run", "dry_run", "testnet", {})
    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    request_id = "request-v1:" + "d" * 64
    trade_id = int(
        store.create_trade(
            run_id="run", coin="BTC", direction="LONG", qty=2.0,
            entry_decision_uid="d1", signal_ts=now, decision_ts=now,
            expected_px=100.0, risk_dollars=1.0, risk_pct=0.001, leverage=1,
            sl_initial=95.0, tp_initial=None, llm_directive_id=None,
        )
    )
    store.insert_order(
        cloid="entry-1", oid=1, group_id=request_id,
        order_ref=f"{request_id}:ENTRY", order_json={"symbol": "BTC"},
        decision_uid="d1", trade_id=trade_id, role="ENTRY", status="OPEN", qty=2.0,
    )
    broker = MockBroker(bars=[], starting_equity=1000.0)
    broker.orders.append({
        "cloid": "entry-1", "oid": 1, "role": "ENTRY", "status": "OPEN",
        "qty": 2.0, "avg_fill_px": 100.0, "reduce_only": False,
        "symbol": "BTC", "direction": "LONG",
    })
    broker.position = Position(symbol="BTC", size=position_size, entry_px=100.0)
    manager = OrderManager(store, broker, "run", pending_grace_s=0)
    engine = BridgeEngine(
        run_id="run", broker=broker, store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        order_manager=manager,
    )
    manager._ingest_fill(
        FillEvent(
            fill_id="f1", cloid="entry-1", coin="BTC", qty=1.0, px=100.0,
            ts=now, role="ENTRY",
        )
    )
    return store, broker, manager, engine


def test_partial_recovery_latches_the_engine_disarmed(tmp_path):
    store, _broker, _manager, engine = _partial_engine(tmp_path)
    store.set_meta("app_state", "ARMED")

    assert engine._app_state() == "DISARMED"
    assert store.get_meta("app_state") == "DISARMED"
    assert engine.status()["partial_recovery_blocking"] is True


def test_arm_is_refused_while_a_recovery_is_active(tmp_path):
    store, _broker, _manager, engine = _partial_engine(tmp_path)
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC)

    with pytest.raises(RuntimeError, match="partial-fill recovery blocks ARM"):
        asyncio.run(engine.arm())
    assert store.get_meta("app_state") == "DISARMED"


def test_arm_is_refused_after_an_unprotected_abort(tmp_path):
    store, broker, manager, engine = _partial_engine(tmp_path)
    broker.partial_extra_position = 2.0  # mixed provenance
    asyncio.run(manager.run_partial_recovery("BTC"))
    assert store.partial_recovery_abort_active("BTC")
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC)

    with pytest.raises(RuntimeError, match="partial-fill recovery blocks ARM"):
        asyncio.run(engine.arm())


def test_pre_arm_trail_and_close_are_suppressed_during_recovery(tmp_path):
    store, broker, manager, engine = _partial_engine(tmp_path)
    bars = [
        Bar(ts=datetime(2026, 7, 6, h, tzinfo=UTC), open=100, high=101, low=99,
            close=100, volume=1)
        for h in range(3)
    ]
    engine.bars = list(bars[:2])
    before = list(broker.partial_calls)

    asyncio.run(engine.on_bar(bars[2]))

    # neither the ordinary trail/close path nor a new entry may run
    assert broker.partial_calls == before
    assert store.get_meta("app_state") == "DISARMED"
    assert "TRAIL_MODIFIED" not in {row["code"] for row in store.get_events()}


def test_runtime_disarm_does_not_compete_with_partial_recovery(tmp_path):
    _store, broker, manager, engine = _partial_engine(tmp_path)
    calls: list[tuple[str, bool]] = []

    async def cancel_spy(cloid):
        calls.append((str(cloid), manager.symbol_locks.is_held("BTC")))

    broker.cancel = cancel_spy

    asyncio.run(engine.disarm_runtime())

    assert calls == []


def test_kill_does_not_cancel_or_flatten_while_recovery_owns_symbol(tmp_path):
    _store, broker, manager, engine = _partial_engine(tmp_path)
    calls: list[tuple[str, bool]] = []

    async def cancel_all_spy():
        calls.append(("cancel_all", manager.symbol_locks.is_held("BTC")))

    async def flatten_spy(symbol):
        calls.append((f"flatten:{symbol}", manager.symbol_locks.is_held("BTC")))

    broker.cancel_all = cancel_all_spy
    broker.flatten = flatten_spy

    asyncio.run(engine.kill(flatten=True))

    assert calls == []


def test_protected_partial_requires_a_human_rearm_with_fresh_evidence(tmp_path):
    store, broker, manager, engine = _partial_engine(tmp_path)
    state = asyncio.run(manager.run_partial_recovery("BTC"))
    assert state == PartialProtectionState.PROTECTED_PARTIAL.value
    # accepting, yet still DISARMED and still awaiting an explicit re-ARM
    assert store.get_meta("app_state") == "DISARMED"
    assert store.partial_recoveries_awaiting_rearm()

    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC)
    asyncio.run(engine.arm())

    assert store.get_meta("app_state") == "ARMED"
    assert store.partial_recoveries_awaiting_rearm() == []


def test_rearm_is_refused_when_the_fresh_snapshot_cannot_prove_protection(tmp_path):
    store, broker, manager, engine = _partial_engine(tmp_path)
    assert asyncio.run(manager.run_partial_recovery("BTC")) == (
        PartialProtectionState.PROTECTED_PARTIAL.value
    )
    # the protective stop vanished between the proof and the re-ARM request
    for order in broker.orders:
        if order["role"] == "SL":
            order["status"] = "CANCELLED_BY_ENGINE"
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC)

    with pytest.raises(RuntimeError, match="partial-fill re-arm proof failed"):
        asyncio.run(engine.arm())
    assert store.get_meta("app_state") == "DISARMED"


def test_rearm_is_refused_when_the_snapshot_is_inexact(tmp_path):
    store, broker, manager, engine = _partial_engine(tmp_path)
    assert asyncio.run(manager.run_partial_recovery("BTC")) == (
        PartialProtectionState.PROTECTED_PARTIAL.value
    )
    broker.partial_snapshot_available = False
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC)

    with pytest.raises(RuntimeError, match="partial-fill re-arm proof failed"):
        asyncio.run(engine.arm())


def test_submission_boundary_rechecks_recovery_after_final_position_await(tmp_path):
    asyncio.run(_submission_boundary_recovery_race(tmp_path))


async def _submission_boundary_recovery_race(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize(target_schema_version=5)
    store.create_run("run", "dry_run", "testnet", {})
    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    request_id = "request-v1:" + "e" * 64
    trade_id = int(
        store.create_trade(
            run_id="run",
            coin="BTC",
            direction="LONG",
            qty=2.0,
            entry_decision_uid="prior-decision",
            signal_ts=now - timedelta(minutes=1),
            decision_ts=now - timedelta(minutes=1),
            expected_px=100.0,
            risk_dollars=1.0,
            risk_pct=0.001,
            leverage=1,
            sl_initial=95.0,
            tp_initial=None,
            llm_directive_id=None,
        )
    )
    store.insert_order(
        cloid="prior-entry",
        oid=1,
        group_id=request_id,
        order_ref=f"{request_id}:ENTRY",
        order_json={"symbol": "BTC", "role": "ENTRY"},
        decision_uid="prior-decision",
        trade_id=trade_id,
        role="ENTRY",
        status="OPEN",
        qty=2.0,
    )
    bars = [
        Bar(
            ts=now - timedelta(minutes=1),
            open=100,
            high=101,
            low=99,
            close=100,
            volume=1,
        ),
        Bar(ts=now, open=100, high=102, low=99, close=100, volume=1),
    ]
    broker = MockBroker(bars=bars, starting_equity=1000.0)
    broker.connected = True
    broker.orders.append(
        {
            "cloid": "prior-entry",
            "oid": 1,
            "role": "ENTRY",
            "status": "OPEN",
            "qty": 2.0,
            "avg_fill_px": None,
            "reduce_only": False,
            "symbol": "BTC",
            "direction": "LONG",
        }
    )
    manager = OrderManager(store, broker, "run", pending_grace_s=0)
    position_reads = 0

    async def positions_with_partial_race():
        nonlocal position_reads
        position_reads += 1
        if position_reads == 2:
            stale_response: list[Position] = []
            broker.position = Position(symbol="BTC", size=1.0, entry_px=100.0)
            manager._ingest_fill(
                FillEvent(
                    fill_id="barrier-partial",
                    cloid="prior-entry",
                    coin="BTC",
                    qty=1.0,
                    px=100.0,
                    ts=now,
                    role="ENTRY",
                )
            )
            return stale_response
        return []

    broker.positions = positions_with_partial_race
    engine = BridgeEngine(
        run_id="run",
        broker=broker,
        store=store,
        strategy=FixedSignalStrategy(stop_loss=90.0, take_profit=115.0),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        order_manager=manager,
        state="ARMED",
    )

    await engine.on_bar(bars[-1])

    assert store.active_partial_recovery_for_symbol("BTC") is not None
    assert store.get_meta("app_state") == "DISARMED"
    assert store.conn.execute("SELECT COUNT(*) FROM submission_attempts").fetchone()[0] == 0
    assert [row for row in broker.orders if row["cloid"] != "prior-entry"] == []


def test_engine_start_drives_partial_recovery_through_reconcile(tmp_path):
    store, broker, manager, engine = _partial_engine(tmp_path)

    asyncio.run(manager.reconcile())

    recovery = store.latest_partial_recovery_for_symbol("BTC")
    assert recovery["state"] == PartialProtectionState.PROTECTED_PARTIAL.value
