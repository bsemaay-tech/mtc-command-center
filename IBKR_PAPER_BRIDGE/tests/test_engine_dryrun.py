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


def test_v4_engine_arm_is_unaffected_by_full_reconciliation(tmp_path):
    """A default (v4) store keeps exactly the predecessor ARM behavior."""
    asyncio.run(_v4_engine_arm_unaffected(tmp_path))


async def _v4_engine_arm_unaffected(tmp_path):
    store = Store(tmp_path / "v4-arm.db")
    store.initialize()
    store.create_run("v4-arm", "paper", "testnet", {})
    engine = BridgeEngine(
        run_id="v4-arm",
        broker=MockBroker([], starting_equity=1000),
        store=store,
        strategy=NoSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig()),
        state="DISARMED",
    )
    assert store.full_reconcile_enabled() is False
    assert engine.full_reconciler is None
    assert engine.full_reconcile_ready() is False

    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC)
    await engine.arm()
    assert store.get_meta("app_state") == "ARMED"
    assert engine.status()["full_reconcile_ready"] is False


def test_v6_engine_requires_both_reconcile_gates_to_arm(tmp_path):
    asyncio.run(_v6_engine_requires_both_gates(tmp_path))


async def _v6_engine_requires_both_gates(tmp_path):
    store = Store(tmp_path / "v6-arm.db")
    store.initialize(target_schema_version=6)
    store.create_run("v6-arm", "paper", "testnet", {})
    broker = MockBroker([], starting_equity=1000)
    broker.full_account = {
        "equity": 1000.0,
        "withdrawable": 1000.0,
        "margin_used": 0.0,
        "available_margin": 1000.0,
    }
    engine = BridgeEngine(
        run_id="v6-arm",
        broker=broker,
        store=store,
        strategy=NoSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig()),
        state="DISARMED",
    )
    assert engine.full_reconciler is not None

    # Light reconcile alone is fresh and successful — and still not enough.
    await engine.order_manager.reconcile()
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC)
    assert engine.full_reconcile_ready() is False
    with pytest.raises(RuntimeError, match="full reconciliation incomplete"):
        await engine.arm()
    assert store.get_meta("app_state") == "DISARMED"

    result = await engine.run_full_reconcile()
    assert result.accepted is True, result.reason_code
    assert engine.full_reconcile_ready() is True
    await engine.arm()
    assert store.get_meta("app_state") == "ARMED"
    assert engine.status()["full_reconcile_ready"] is True
    assert engine.status()["full_reconcile_attempt_id"] == result.attempt_id


def test_v6_engine_blocked_capture_keeps_arm_closed(tmp_path):
    asyncio.run(_v6_engine_blocked_capture(tmp_path))


async def _v6_engine_blocked_capture(tmp_path):
    from bridge.engine.types import ReconcileComponentKind

    store = Store(tmp_path / "v6-blocked.db")
    store.initialize(target_schema_version=6)
    store.create_run("v6-blocked", "paper", "testnet", {})
    broker = MockBroker([], starting_equity=1000)
    broker.full_component_failures = {ReconcileComponentKind.FILLS.value: "RAISE"}
    engine = BridgeEngine(
        run_id="v6-blocked",
        broker=broker,
        store=store,
        strategy=NoSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig()),
        state="DISARMED",
    )
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC)

    result = await engine.run_full_reconcile()
    assert result.accepted is False
    assert engine.full_reconcile_error == result.reason_code
    assert "FULL_RECONCILE_BLOCKED" in [row["code"] for row in store.get_events()]

    with pytest.raises(RuntimeError, match="full reconciliation incomplete"):
        await engine.arm()
    assert store.get_meta("app_state") == "DISARMED"


def test_v6_engine_marks_an_interrupted_capture_on_restart(tmp_path):
    asyncio.run(_v6_engine_marks_interrupted_capture(tmp_path))


async def _v6_engine_marks_interrupted_capture(tmp_path):
    path = tmp_path / "v6-restart.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    store.create_run("v6-restart", "paper", "testnet", {})
    dangling = store.reserve_reconcile_attempt(
        run_id="v6-restart",
        started_ts=datetime.now(UTC),
        deadline_s=5.0,
        max_skew_s=5.0,
    )
    store.close()

    reopened = Store(path)
    reopened.initialize(target_schema_version=6)
    reopened.create_run("v6-restart-2", "paper", "testnet", {})
    engine = BridgeEngine(
        run_id="v6-restart-2",
        broker=MockBroker([], starting_equity=1000),
        store=reopened,
        strategy=NoSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig()),
        state="DISARMED",
    )
    assert engine.full_reconcile_error == "RESTART_INTERRUPTED"
    assert reopened.get_reconcile_attempt(dangling)["state"] == "INCOMPLETE"
    assert reopened.latest_accepted_reconcile_checkpoint() is None
    assert engine.full_reconcile_ready() is False
    reopened.close()


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


# ---------------------------------------------------------------------------
# TS-P1-005 R2 / R3 — readiness recency, and two independent failure budgets
# ---------------------------------------------------------------------------


def _v6_engine(tmp_path, name: str, run_id: str, broker=None):
    store = Store(tmp_path / name)
    store.initialize(target_schema_version=6)
    store.create_run(run_id, "paper", "testnet", {})
    broker = broker if broker is not None else MockBroker([], starting_equity=1000)
    broker.full_account = {
        "equity": 1000.0,
        "withdrawable": 1000.0,
        "margin_used": 0.0,
        "available_margin": 1000.0,
    }
    engine = BridgeEngine(
        run_id=run_id,
        broker=broker,
        store=store,
        strategy=NoSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig()),
        state="DISARMED",
    )
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC)
    return store, broker, engine


def test_full_reconcile_freshness_bound_is_derived_from_the_cadence(tmp_path):
    asyncio.run(_full_reconcile_freshness_bound(tmp_path))


async def _full_reconcile_freshness_bound(tmp_path):
    from bridge.engine.types import ReconcileComponentKind

    store, _broker, engine = _v6_engine(tmp_path, "v6-fresh.db", "v6-fresh")

    # Exactly the accepted light formula, re-evaluated at call time.
    for interval, expected in ((60.0, 180.0), (5.0, 30.0), (600.0, 1800.0)):
        engine.reconcile_interval_s = interval
        assert engine.full_reconcile_max_age_s() == expected
        assert expected == max(engine.reconcile_interval_s * 3, 30.0)

    engine.reconcile_interval_s = 60.0
    result = await engine.run_full_reconcile()
    assert result.accepted is True, result.reason_code

    seen: list[float] = []
    real_ready = store.full_reconcile_ready

    def spy(*, now, max_age_s):
        seen.append(max_age_s)
        return real_ready(now=now, max_age_s=max_age_s)

    store.full_reconcile_ready = spy
    assert engine.full_reconcile_ready() is True
    engine.reconcile_interval_s = 600.0
    engine.full_reconcile_ready()
    assert seen == [180.0, 1800.0]

    # The bound is a real bound: an old checkpoint is not ready.
    store.full_reconcile_ready = real_ready
    engine.reconcile_interval_s = 60.0
    stale_now = datetime.now(UTC) + timedelta(seconds=181)
    assert engine.full_reconcile_ready(stale_now) is False
    assert ReconcileComponentKind.FILLS.value  # vocabulary is still importable
    store.close()


def test_a_later_failed_capture_blocks_arm_even_with_a_young_checkpoint(tmp_path):
    asyncio.run(_later_failure_blocks_arm(tmp_path))


def test_v6_arm_requires_a_risk_readable_snapshot_not_only_metadata_readiness(tmp_path):
    asyncio.run(_v6_arm_requires_risk_snapshot(tmp_path))


async def _v6_arm_requires_risk_snapshot(tmp_path):
    from bridge.engine.types import (
        RISK_SNAPSHOT_LEGACY_PAYLOAD,
        RiskSnapshotUnavailable,
    )

    store, _broker, engine = _v6_engine(
        tmp_path, "v6-risk-arm.db", "v6-risk-arm"
    )
    accepted = await engine.run_full_reconcile()
    assert accepted.accepted is True
    assert engine.full_reconcile_ready() is True

    def legacy_only(*, now, max_age_s):
        raise RiskSnapshotUnavailable(RISK_SNAPSHOT_LEGACY_PAYLOAD)

    store.load_authoritative_risk_snapshot = legacy_only
    with pytest.raises(
        RuntimeError,
        match=f"authoritative risk snapshot unavailable: {RISK_SNAPSHOT_LEGACY_PAYLOAD}",
    ):
        await engine.arm()
    assert engine.state == "DISARMED"
    assert store.get_meta("app_state") == "DISARMED"
    assert engine.risk_snapshot_error == RISK_SNAPSHOT_LEGACY_PAYLOAD
    assert engine.risk_input_error is not None
    store.close()


def test_v6_signal_risk_never_reads_a_point_account(tmp_path):
    asyncio.run(_v6_signal_never_reads_point_account(tmp_path))


async def _v6_signal_never_reads_point_account(tmp_path):
    store, broker, engine = _v6_engine(
        tmp_path, "v6-no-point-account.db", "v6-no-point-account"
    )
    accepted = await engine.run_full_reconcile()
    assert accepted.accepted is True
    await engine.arm()
    engine.strategy = FixedSignalStrategy(stop_loss=90.0)

    async def forbidden_account():
        raise AssertionError("v6 risk must not call broker.account()")

    broker.account = forbidden_account
    await engine.on_bar(
        Bar(
            ts=datetime.now(UTC),
            open=100,
            high=101,
            low=99,
            close=100,
            volume=1,
        )
    )
    stages = [row["stage"] for row in store.get_snapshot()["decisions"]]
    assert "RISK_PASS" in stages
    assert engine.risk_snapshot_error is None
    store.close()


def test_failed_full_gate_blocks_new_entry_while_persisted_armed(tmp_path):
    asyncio.run(_failed_full_gate_blocks_new_entry(tmp_path))


async def _failed_full_gate_blocks_new_entry(tmp_path):
    from bridge.engine.types import ReconcileComponentKind

    store, broker, engine = _v6_engine(tmp_path, "v6-entry-gate.db", "v6-entry-gate")
    accepted = await engine.run_full_reconcile()
    assert accepted.accepted is True
    await engine.arm()
    assert store.get_meta("app_state") == "ARMED"

    broker.full_component_failures = {ReconcileComponentKind.FILLS.value: "RAISE"}
    failed = await engine.run_full_reconcile()
    assert failed.accepted is False
    assert engine.full_reconcile_ready() is False

    class CountingStrategy(NoSignalStrategy):
        def __init__(self):
            self.calls = 0

        def on_bar(self, bars, position):
            self.calls += 1
            return None

    strategy = CountingStrategy()
    engine.strategy = strategy
    bar = Bar(
        ts=datetime.now(UTC),
        open=100,
        high=101,
        low=99,
        close=100,
        volume=1,
    )
    await engine.on_bar(bar)
    assert strategy.calls == 0
    assert store.get_meta("app_state") == "ARMED"
    store.close()


def test_on_bar_waits_for_the_full_reconcile_epoch_guard(tmp_path):
    asyncio.run(_on_bar_waits_for_full_guard(tmp_path))


async def _on_bar_waits_for_full_guard(tmp_path):
    from bridge.engine.reconcile import full_writer_guard

    store, _, engine = _v6_engine(tmp_path, "v6-bar-guard.db", "v6-bar-guard")
    guard = full_writer_guard(store)
    await guard.acquire()
    task = asyncio.create_task(engine.on_bar(Bar(
        ts=datetime.now(UTC),
        open=100,
        high=101,
        low=99,
        close=100,
        volume=1,
    )))
    await asyncio.sleep(0)
    await asyncio.sleep(0)
    assert task.done() is False
    guard.release()
    await task
    store.close()


async def _later_failure_blocks_arm(tmp_path):
    from bridge.engine.types import ReconcileComponentKind

    store, broker, engine = _v6_engine(tmp_path, "v6-later.db", "v6-later")

    accepted = await engine.run_full_reconcile()
    assert accepted.accepted is True, accepted.reason_code
    assert engine.full_reconcile_ready() is True

    broker.full_component_failures = {ReconcileComponentKind.FILLS.value: "RAISE"}
    failed = await engine.run_full_reconcile()
    assert failed.accepted is False

    # The accepted checkpoint is still young and still the pointer...
    checkpoint = store.latest_accepted_reconcile_checkpoint()
    assert checkpoint["attempt_id"] == accepted.attempt_id
    # ...and it is no longer the latest word, so neither gate is open.
    assert store.full_reconcile_ready(
        now=datetime.now(UTC), max_age_s=engine.full_reconcile_max_age_s()
    ) is False
    assert engine.full_reconcile_error == failed.reason_code
    assert engine.full_reconcile_ready() is False
    with pytest.raises(RuntimeError, match="full reconciliation incomplete"):
        await engine.arm()
    assert store.get_meta("app_state") == "DISARMED"

    # Only a fresh accept clears the latch.
    broker.full_component_failures = {}
    recovered = await engine.run_full_reconcile()
    assert recovered.accepted is True, recovered.reason_code
    assert engine.full_reconcile_error is None
    assert engine.full_reconcile_ready() is True
    await engine.arm()
    assert store.get_meta("app_state") == "ARMED"
    store.close()


def test_a_dangling_capture_resolved_on_reopen_blocks_arm(tmp_path):
    asyncio.run(_dangling_capture_blocks_arm(tmp_path))


async def _dangling_capture_blocks_arm(tmp_path):
    path = tmp_path / "v6-dangling.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    store.create_run("v6-dangling", "paper", "testnet", {})
    broker = MockBroker([], starting_equity=1000)
    broker.full_account = {
        "equity": 1000.0,
        "withdrawable": 1000.0,
        "margin_used": 0.0,
        "available_margin": 1000.0,
    }
    engine = BridgeEngine(
        run_id="v6-dangling",
        broker=broker,
        store=store,
        strategy=NoSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig()),
        state="DISARMED",
    )
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC)
    accepted = await engine.run_full_reconcile()
    assert accepted.accepted is True, accepted.reason_code
    assert engine.full_reconcile_ready() is True

    # A capture that is killed before it can resolve.
    dangling = store.reserve_reconcile_attempt(
        run_id="v6-dangling",
        started_ts=datetime.now(UTC),
        deadline_s=5.0,
        max_skew_s=5.0,
    )
    store.close()

    reopened = Store(path)
    reopened.initialize(target_schema_version=6)
    restarted = BridgeEngine(
        run_id="v6-dangling",
        broker=broker,
        store=reopened,
        strategy=NoSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig()),
        state="DISARMED",
    )
    restarted.reconcile_ready = True
    restarted.last_reconcile_ts = datetime.now(UTC)

    assert reopened.get_reconcile_attempt(dangling)["state"] == "INCOMPLETE"
    assert restarted.full_reconcile_error == "RESTART_INTERRUPTED"
    # The pre-crash checkpoint is retained but is no longer the latest word.
    assert (
        reopened.latest_accepted_reconcile_checkpoint()["attempt_id"]
        == accepted.attempt_id
    )
    assert reopened.full_reconcile_ready(
        now=datetime.now(UTC), max_age_s=restarted.full_reconcile_max_age_s()
    ) is False
    assert restarted.full_reconcile_ready() is False
    with pytest.raises(RuntimeError, match="full reconciliation incomplete"):
        await restarted.arm()
    assert reopened.get_meta("app_state") == "DISARMED"
    reopened.close()


def test_full_ledger_failure_never_consumes_the_light_failure_budget(tmp_path):
    asyncio.run(_full_failure_keeps_light_budget(tmp_path))


async def _full_failure_keeps_light_budget(tmp_path):
    import sqlite3

    store, _broker, engine = _v6_engine(tmp_path, "v6-budget.db", "v6-budget")

    accepted = await engine.run_full_reconcile()
    assert accepted.accepted is True, accepted.reason_code
    await engine.arm()
    assert store.get_meta("app_state") == "ARMED"

    def exploding_reserve(**_kwargs):
        raise sqlite3.OperationalError("reconcile ledger unavailable")

    store.reserve_reconcile_attempt = exploding_reserve

    limit = engine.reconcile_max_consecutive_failures
    assert limit <= 3, "3 cycles must be enough to exhaust the light budget"
    for _ in range(3):
        assert await engine._run_reconcile_cycle() is True

    # The light gate is untouched: budget, flags, cadence and ARMED state.
    assert engine._consecutive_reconcile_failures == 0
    assert engine.reconcile_ready is True
    assert engine.reconcile_error is None
    assert engine.state == "ARMED"
    assert store.get_meta("app_state") == "ARMED"

    # The full gate carries the whole outcome by itself.
    assert engine.full_reconcile_error is not None
    assert engine.full_reconcile_error.startswith("FULL_RECONCILE_CYCLE_FAILED")
    assert "OPERATIONALERROR" in engine.full_reconcile_error
    assert engine.full_reconcile_ready() is False
    assert engine.status()["full_reconcile_ready"] is False
    codes = [row["code"] for row in store.get_events()]
    assert codes.count("FULL_RECONCILE_BLOCKED") == 3
    assert "RECONCILE_FAILED" not in codes
    assert "RECONCILE_FAILED_TOLERATED" not in codes
    store.close()


# ---------------------------------------------------------------------------
# TS-P1-007 — durable risk controls on the engine path (opt-in v7)
#
# The engine clock, the store clock and the mock adapter's observation clock are
# one frozen domain, so UTC-day boundaries and freshness are deterministic.
# Nothing below injects a daily-risk number: every value is derived by a real
# accepted capture.
# ---------------------------------------------------------------------------

V7_DAY = datetime(2026, 7, 26, 0, 0, tzinfo=UTC)


def _v7_risk_config():
    return RiskConfig(
        max_position_notional_pct=0.5,
        max_daily_loss_pct=0.02,
        max_intraday_drawdown_pct=0.05,
        equity_floor_usdc=500.0,
    )


def _set_equity(broker, equity: float) -> None:
    equity = float(equity)
    broker.full_account = {
        "equity": equity,
        "withdrawable": equity,
        "margin_used": 0.0,
        "available_margin": equity,
    }


class _MovableClock:
    def __init__(self, start: datetime) -> None:
        self.value = start

    def __call__(self) -> datetime:
        return self.value


def _v7_engine(tmp_path, name, run_id, *, store_cls=Store, equity=10_000.0):
    """A v7 engine whose whole clock domain starts two hours before the day."""
    clock = _MovableClock(V7_DAY - timedelta(hours=2))
    store = store_cls(tmp_path / name, clock=clock)
    store.initialize(target_schema_version=7)
    store.create_run(run_id, "paper", "testnet", {})
    broker = MockBroker([], starting_equity=equity)
    broker.full_clock = clock
    _set_equity(broker, equity)
    engine = BridgeEngine(
        run_id=run_id,
        broker=broker,
        store=store,
        strategy=NoSignalStrategy(),
        risk_engine=RiskEngine(_v7_risk_config()),
        state="DISARMED",
        clock=clock,
    )
    engine.reconcile_ready = True
    engine.last_reconcile_ts = clock.value
    return store, broker, engine, clock


async def _capture_at(engine, broker, clock, when, equity):
    """One full capture observed at ``when`` with ``equity`` on the account."""
    clock.value = when
    _set_equity(broker, equity)
    engine.last_reconcile_ts = when
    return await engine.run_full_reconcile()


def test_v7_arm_requires_an_established_utc_day_baseline(tmp_path):
    asyncio.run(_v7_arm_requires_baseline(tmp_path))


async def _v7_arm_requires_baseline(tmp_path):
    from bridge.engine.types import RISK_DAY_BASELINE_MISSING

    store, broker, engine, clock = _v7_engine(tmp_path, "v7-arm.db", "v7-arm")

    # First capture of the very first day: no checkpoint at/before 00:00 UTC.
    first = await _capture_at(
        engine, broker, clock, V7_DAY + timedelta(hours=1), 10_000.0
    )
    assert first.accepted is True, first.reason_code
    assert engine.full_reconcile_ready() is True
    with pytest.raises(RuntimeError, match=RISK_DAY_BASELINE_MISSING):
        await engine.arm()
    assert engine.state == "DISARMED"
    assert engine.risk_snapshot_error == RISK_DAY_BASELINE_MISSING

    # Establish the next day's baseline the approved way: a real accepted
    # checkpoint at/before its 00:00 UTC boundary.
    next_day = V7_DAY + timedelta(days=1)
    await _capture_at(engine, broker, clock, next_day - timedelta(minutes=1), 10_000.0)
    await _capture_at(engine, broker, clock, next_day + timedelta(hours=1), 9_950.0)
    await engine.arm()
    assert store.get_meta("app_state") == "ARMED"
    assert engine.risk_snapshot_error is None
    store.close()


def test_v7_exact_daily_loss_boundary_latches_and_submits_nothing(tmp_path):
    asyncio.run(_v7_daily_loss_boundary(tmp_path))


async def _v7_daily_loss_boundary(tmp_path):
    from bridge.engine.types import RISK_CONTROL_DAILY_LOSS

    store, broker, engine, clock = _v7_engine(tmp_path, "v7-daily.db", "v7-daily")
    await _capture_at(engine, broker, clock, V7_DAY - timedelta(minutes=1), 10_000.0)
    await _capture_at(engine, broker, clock, V7_DAY + timedelta(hours=1), 9_801.0)
    await engine.arm()
    assert store.get_meta("app_state") == "ARMED"
    assert store.list_risk_control_latches() == []

    # Exactly -2.00% of the day-start equity.
    await _capture_at(engine, broker, clock, V7_DAY + timedelta(hours=2), 9_800.0)
    latches = store.list_risk_control_latches()
    assert len(latches) == 1
    assert latches[0]["control"] == RISK_CONTROL_DAILY_LOSS
    # The veto is independent of any strategy signal: the capture alone disarms.
    assert engine.state == "DISARMED"
    assert engine.risk_control_latch == RISK_CONTROL_DAILY_LOSS
    codes = [row["code"] for row in store.get_events()]
    assert codes.count("RISK_CONTROL_LATCHED") == 1

    # Even a forcibly re-armed persisted state cannot get an order out.
    engine.state = "ARMED"
    engine.risk_input_error = None
    engine.risk_snapshot_error = None
    engine.risk_control_latch = None
    store.set_meta("app_state", "ARMED")
    engine.strategy = FixedSignalStrategy(stop_loss=90.0)
    clock.value = V7_DAY + timedelta(hours=2, seconds=5)
    engine.last_reconcile_ts = clock.value
    await engine.on_bar(
        Bar(ts=clock.value, open=100, high=101, low=99, close=100, volume=1)
    )
    decisions = store.get_snapshot()["decisions"]
    stages = [row["stage"] for row in decisions]
    assert "SUBMITTED" not in stages
    assert "RISK_PASS" not in stages
    reject = [row for row in decisions if row["stage"] == "RISK_REJECT"][-1]
    import json as _json

    assert _json.loads(reject["payload_json"])["reason"] == (
        f"RISK_CONTROL_LATCHED:{RISK_CONTROL_DAILY_LOSS}"
    )
    assert engine.state == "DISARMED"
    assert store.get_meta("app_state") == "DISARMED"
    # No second latch row: a crossing latches exactly once.
    assert len(store.list_risk_control_latches()) == 1
    store.close()


def test_v7_manual_arm_is_refused_while_a_latch_is_active(tmp_path):
    asyncio.run(_v7_manual_arm_refused(tmp_path))


async def _v7_manual_arm_refused(tmp_path):
    store, broker, engine, clock = _v7_engine(tmp_path, "v7-latch-arm.db", "v7-latch-arm")
    await _capture_at(engine, broker, clock, V7_DAY - timedelta(minutes=1), 10_000.0)
    await _capture_at(engine, broker, clock, V7_DAY + timedelta(hours=1), 400.0)
    assert [row["control"] for row in store.list_risk_control_latches()] == [
        "EQUITY_STOP",
        "DAILY_LOSS",
        "MAX_DRAWDOWN",
    ]

    with pytest.raises(RuntimeError, match="risk control latched"):
        await engine.arm()
    assert engine.state == "DISARMED"
    assert store.get_meta("app_state") == "DISARMED"

    # Recovered equity on a whole new UTC day still cannot arm: an equity stop
    # is account-scoped and needs an explicit owner acknowledgement.
    next_day = V7_DAY + timedelta(days=1)
    await _capture_at(engine, broker, clock, next_day - timedelta(minutes=1), 50_000.0)
    await _capture_at(engine, broker, clock, next_day + timedelta(hours=1), 50_000.0)
    with pytest.raises(RuntimeError, match="risk control latched"):
        await engine.arm()
    store.close()


def test_v7_latch_and_baseline_survive_restart_and_start_disarmed(tmp_path):
    asyncio.run(_v7_latch_survives_restart(tmp_path))


async def _v7_latch_survives_restart(tmp_path):
    from bridge.engine.types import RISK_CONTROL_DAILY_LOSS

    store, broker, engine, clock = _v7_engine(tmp_path, "v7-restart.db", "v7-restart")
    await _capture_at(engine, broker, clock, V7_DAY - timedelta(minutes=1), 10_000.0)
    await _capture_at(engine, broker, clock, V7_DAY + timedelta(hours=1), 9_800.0)
    assert engine.state == "DISARMED"
    days_before = store.list_risk_day_checkpoints()
    latches_before = store.list_risk_control_latches()
    # Worst case: the persisted state lies and claims ARMED.
    store.set_meta("app_state", "ARMED")
    store.close()

    reopened = Store(tmp_path / "v7-restart.db", clock=clock)
    reopened.initialize(target_schema_version=7)
    restarted = BridgeEngine(
        run_id="v7-restart",
        broker=broker,
        store=reopened,
        strategy=NoSignalStrategy(),
        risk_engine=RiskEngine(_v7_risk_config()),
        state="DISARMED",
        clock=clock,
    )
    assert reopened.list_risk_day_checkpoints() == days_before
    assert reopened.list_risk_control_latches() == latches_before
    assert restarted.risk_control_latch == RISK_CONTROL_DAILY_LOSS
    assert restarted._app_state() == "DISARMED"
    assert reopened.get_meta("app_state") == "DISARMED"
    with pytest.raises(RuntimeError, match="risk control latched"):
        await restarted.arm()
    reopened.close()


def test_v7_utc_rollover_blocks_until_a_fresh_checkpoint_establishes_the_day(tmp_path):
    asyncio.run(_v7_utc_rollover_blocks(tmp_path))


async def _v7_utc_rollover_blocks(tmp_path):
    from bridge.engine.types import RISK_DAY_DATE_MISMATCH

    store, broker, engine, clock = _v7_engine(tmp_path, "v7-rollover.db", "v7-rollover")
    # Establish July 25 from a real checkpoint at/before its UTC boundary,
    # then prove rollover blocks July 26 until its own baseline exists.
    await _capture_at(
        engine, broker, clock, V7_DAY - timedelta(days=1, minutes=1), 10_000.0
    )
    await _capture_at(engine, broker, clock, V7_DAY - timedelta(seconds=30), 10_000.0)
    await engine.arm()
    assert store.get_meta("app_state") == "ARMED"

    # One second past midnight the newest durable day row still describes
    # yesterday; D2=A blocks rather than carrying the budget across the boundary.
    clock.value = V7_DAY + timedelta(seconds=1)
    engine.last_reconcile_ts = clock.value
    engine.strategy = FixedSignalStrategy(stop_loss=90.0)
    await engine.on_bar(
        Bar(ts=clock.value, open=100, high=101, low=99, close=100, volume=1)
    )
    assert engine.risk_snapshot_error == RISK_DAY_DATE_MISMATCH
    assert engine.state == "DISARMED"
    stages = [row["stage"] for row in store.get_snapshot()["decisions"]]
    assert "SUBMITTED" not in stages and "RISK_PASS" not in stages
    store.close()


def test_v7_forced_persistence_failure_disarms_and_retains_evidence(tmp_path):
    asyncio.run(_v7_persistence_failure(tmp_path))


async def _v7_persistence_failure(tmp_path):
    import sqlite3

    class BrokenRiskDayStore(Store):
        break_day_state = False

        def _append_risk_day_state_locked(self, **kwargs):
            if self.break_day_state:
                raise sqlite3.OperationalError("risk day ledger unavailable")
            return super()._append_risk_day_state_locked(**kwargs)

    store, broker, engine, clock = _v7_engine(
        tmp_path, "v7-broken.db", "v7-broken", store_cls=BrokenRiskDayStore
    )
    await _capture_at(engine, broker, clock, V7_DAY - timedelta(minutes=1), 10_000.0)
    await _capture_at(
        engine, broker, clock, V7_DAY + timedelta(minutes=30), 10_000.0
    )
    await engine.arm()
    assert engine.state == "ARMED"
    good = store.latest_accepted_reconcile_checkpoint()
    assert good is not None
    days_before = store.list_risk_day_checkpoints()

    store.break_day_state = True
    failed = await _capture_at(
        engine, broker, clock, V7_DAY + timedelta(hours=1), 9_000.0
    )
    assert failed.accepted is False
    # The accept transaction rolled back whole: no new checkpoint, no new day
    # row, and the previous pointer is untouched.
    assert store.latest_accepted_reconcile_checkpoint()["checkpoint_id"] == (
        good["checkpoint_id"]
    )
    assert store.list_risk_day_checkpoints() == days_before
    # The failure itself is retained as durable append-only evidence.
    attempts = store.list_reconcile_attempts("v7-broken")
    assert attempts[-1]["state"] == "INCOMPLETE"
    assert engine.full_reconcile_error is not None
    assert engine.full_reconcile_ready() is False
    assert engine.state == "DISARMED"
    assert store.get_meta("app_state") == "DISARMED"
    with pytest.raises(RuntimeError):
        await engine.arm()
    assert store.get_meta("app_state") == "DISARMED"
    store.close()


def test_v6_engine_risk_path_is_untouched_by_ts_p1_007(tmp_path):
    asyncio.run(_v6_path_untouched(tmp_path))


async def _v6_path_untouched(tmp_path):
    store, _broker, engine = _v6_engine(tmp_path, "v6-untouched.db", "v6-untouched")
    accepted = await engine.run_full_reconcile()
    assert accepted.accepted is True
    assert store.durable_risk_controls_enabled() is False
    await engine.arm()
    engine.strategy = FixedSignalStrategy(stop_loss=90.0)
    await engine.on_bar(
        Bar(ts=datetime.now(UTC), open=100, high=101, low=99, close=100, volume=1)
    )
    stages = [row["stage"] for row in store.get_snapshot()["decisions"]]
    assert "RISK_PASS" in stages
    assert engine.risk_snapshot_error is None
    assert engine.risk_control_latch is None
    store.close()
