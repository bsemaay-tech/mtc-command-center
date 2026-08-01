from __future__ import annotations

import asyncio
import hashlib
import inspect
import json
import math
import sqlite3
import threading
from contextlib import asynccontextmanager
from dataclasses import replace
from pathlib import Path
from datetime import UTC, datetime, timedelta

import pytest

from bridge.broker.mock import MockBroker
from bridge.engine.engine import BridgeEngine
from bridge.engine.orders import OrderManager
from bridge.engine.orders import KILL_LIFECYCLE_BINDING_FAULT_REASONS
from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from bridge.engine.types import (
    Bar,
    FillEvent,
    OrderUpdateEvent,
    OrderPlan,
    Position,
    ReconcileComponentKind,
    Signal,
)
from bridge.broker.base import SubmissionRejectedError
from bridge.store.db import DurableRowFault, KillConflictError, Store
from bridge.store.db import DURABLE_EVENT_COLUMN_TYPES

FIXTURES = Path(__file__).parent / "fixtures"


def _public_store_apis_reaching(target: str) -> tuple[str, ...]:
    """Derive public Store entrypoints that transitively call one method."""
    methods = dict(inspect.getmembers(Store, predicate=inspect.isfunction))
    reachable = {target}
    changed = True
    while changed:
        changed = False
        for caller, function in methods.items():
            if caller in reachable:
                continue
            source = inspect.getsource(function)
            if any(f"self.{callee}(" in source for callee in reachable):
                reachable.add(caller)
                changed = True
    return tuple(sorted(name for name in reachable if not name.startswith("_")))


_S3T_KILL_CLOSURE_PUBLIC_APIS = _public_store_apis_reaching(
    "_assert_kill_flatten_closure_in_tx"
)


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


def test_kill_uses_full_writer_then_symbol_lock_order(tmp_path, monkeypatch):
    async def run() -> None:
        store = Store(tmp_path / "kill-lock-order.db")
        try:
            store.initialize(target_schema_version=9)
        except RuntimeError:
            store.initialize(target_schema_version=8)
        store.create_run("kill-lock-order", "dry_run", "testnet", {})
        store.set_meta("app_state", "ARMED")
        broker = MockBroker(bars=[])
        broker.orders.append({
            "cloid": "owned-entry", "oid": 1, "role": "ENTRY",
            "status": "OPEN", "qty": 0.1, "reduce_only": False,
            "symbol": "BTC", "direction": "LONG",
        })
        broker.full_open_orders = [{
            "cloid": "owned-entry", "oid": 1, "coin": "BTC", "side": "BUY",
            "size": 0.1, "role": "ENTRY", "reduce_only": False,
        }]
        store.insert_order(
            cloid="owned-entry", oid=1, group_id="request",
            order_ref="request:ENTRY",
            order_json={"symbol": "BTC", "role": "ENTRY"},
            decision_uid="owned", trade_id=None, role="ENTRY",
            status="OPEN", qty=0.1,
        )
        engine = BridgeEngine(
            run_id="kill-lock-order", broker=broker, store=store,
            strategy=KeltnerTrailEma8(), risk_engine=RiskEngine(RiskConfig()),
            state="ARMED",
        )
        writer_held = False
        observations = []
        from bridge.engine import reconcile as reconcile_module

        original_guard = reconcile_module.full_writer_guard

        @asynccontextmanager
        async def tracked_guard(target_store):
            nonlocal writer_held
            async with original_guard(target_store):
                writer_held = True
                try:
                    yield
                finally:
                    writer_held = False

        original_snapshot = broker.symbol_snapshot

        async def checked_snapshot(symbol):
            observations.append(
                (writer_held, engine.order_manager.symbol_locks.is_held(symbol))
            )
            return await original_snapshot(symbol)

        monkeypatch.setattr(reconcile_module, "full_writer_guard", tracked_guard)
        monkeypatch.setattr(broker, "symbol_snapshot", checked_snapshot)

        await engine.kill(flatten=False)

        assert observations
        assert all(full and symbol for full, symbol in observations)

    asyncio.run(run())


def _repair4_kill_engine(tmp_path, *, foreign_substitution: bool = False):
    run_id = "repair4-kill"
    store = Store(tmp_path / "repair4-kill.db")
    store.initialize(target_schema_version=9)
    store.create_run(run_id, "dry_run", "testnet", {})
    store.set_meta("app_state", "ARMED")
    entry_ts = datetime.now(UTC) - timedelta(seconds=2)
    store.conn.execute(
        "UPDATE runs SET started_ts=? WHERE run_id=?",
        ((entry_ts - timedelta(seconds=1)).isoformat(), run_id),
    )
    store.conn.commit()
    decision_uid = "repair4-owned-entry"
    store.insert_decision(
        run_id, decision_uid, entry_ts, "BTC", "SIGNAL", {"direction": "LONG"}
    )
    trade_id = store.create_trade(
        run_id=run_id,
        coin="BTC",
        direction="LONG",
        qty=1.0,
        entry_decision_uid=decision_uid,
        signal_ts=entry_ts,
        decision_ts=entry_ts,
        expected_px=100.0,
        risk_dollars=10.0,
        risk_pct=0.01,
        leverage=1,
        sl_initial=90.0,
        tp_initial=None,
        llm_directive_id=None,
    )
    store.insert_order(
        cloid="repair4-entry",
        oid=101,
        group_id=decision_uid,
        order_ref="repair4-entry-ref",
        order_json={"symbol": "BTC", "role": "ENTRY", "direction": "LONG"},
        decision_uid=decision_uid,
        trade_id=trade_id,
        role="ENTRY",
        status="FILLED",
        qty=1.0,
        filled_qty=1.0,
        ts_submit=entry_ts,
        ts_last=entry_ts,
    )
    store.insert_fill(
        "repair4-owned-fill",
        "repair4-entry",
        decision_uid,
        entry_ts,
        1.0,
        100.0,
        0.0,
        0.0,
    )
    store.insert_order(
        cloid="repair4-sl",
        oid=102,
        group_id=decision_uid,
        order_ref="repair4-sl-ref",
        order_json={
            "symbol": "BTC",
            "role": "SL",
            "side": "SELL",
            "reduce_only": True,
        },
        decision_uid=decision_uid,
        trade_id=trade_id,
        role="SL",
        status="OPEN",
        qty=1.0,
        filled_qty=0.0,
        ts_submit=entry_ts,
        ts_last=entry_ts,
    )

    broker = MockBroker(bars=[])
    broker.position = Position(symbol="BTC", size=1.0, entry_px=100.0)
    broker.orders = [{
        "cloid": "repair4-sl",
        "oid": 102,
        "role": "SL",
        "status": "OPEN",
        "qty": 1.0,
        "filled_qty": 0.0,
        "reduce_only": True,
        "symbol": "BTC",
        "direction": "LONG",
        "trigger_px": 90.0,
    }]
    broker.full_positions = [{"symbol": "BTC", "size": 1.0}]
    broker.full_open_orders = [{
        "cloid": "repair4-sl",
        "oid": 102,
        "coin": "BTC",
        "side": "SELL",
        "sz": 1.0,
        "role": "SL",
        "reduceOnly": True,
        "status": "OPEN",
    }]
    base_ms = int(entry_ts.timestamp() * 1000)
    broker.full_fill_history = [{
        "fill_id": "repair4-owned-fill",
        "oid": 101,
        "coin": "BTC",
        "side": "BUY",
        "sz": 1.0,
        "px": 100.0,
        "time": base_ms,
    }]
    if foreign_substitution:
        broker.full_fill_history.extend([
            {
                "fill_id": "repair4-foreign-sell",
                "oid": 901,
                "coin": "BTC",
                "side": "SELL",
                "sz": 1.0,
                "px": 100.0,
                "time": base_ms + 250,
            },
            {
                "fill_id": "repair4-foreign-buy",
                "oid": 902,
                "coin": "BTC",
                "side": "BUY",
                "sz": 1.0,
                "px": 100.0,
                "time": base_ms + 500,
            },
        ])
    engine = BridgeEngine(
        run_id=run_id,
        broker=broker,
        store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
        state="ARMED",
    )
    return store, broker, engine


def test_repair4_a1_same_net_foreign_substitution_is_ambiguous(tmp_path):
    store, broker, engine = _repair4_kill_engine(
        tmp_path, foreign_substitution=True
    )

    asyncio.run(engine.kill(flatten=True))

    request = store.active_kill_request()
    assert request is not None
    assert request["terminal_state"] == "AMBIGUOUS"
    assert request["terminal_reason"] == "OWNERSHIP_AMBIGUOUS"
    assert broker.broker_mutations == []
    assert next(
        row for row in broker.orders if row["cloid"] == "repair4-sl"
    )["status"] == "OPEN"


def test_repair4_a2_capture_failure_is_query_only(tmp_path):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    broker.full_component_failures[ReconcileComponentKind.FILLS.value] = "RAISE"

    asyncio.run(engine.kill(flatten=True))

    request = store.active_kill_request()
    assert engine.state == "KILLED"
    assert engine.order_manager.kill_latched is True
    assert broker.broker_mutations == []
    assert request is not None
    assert request["terminal_state"] == "UNKNOWN"
    assert request["terminal_reason"] == "KILL_CAPTURE_FILLS_UNAVAILABLE"


def test_repair4_a3_clock_underbound_cannot_hide_foreign_replacement(tmp_path):
    store, broker, engine = _repair4_kill_engine(
        tmp_path, foreign_substitution=True
    )
    future_ms = int((datetime.now(UTC) + timedelta(seconds=60)).timestamp() * 1000)
    broker.full_fill_history[-2]["time"] = future_ms
    broker.full_fill_history[-1]["time"] = future_ms + 1
    engine.clock = lambda: datetime.now(UTC) - timedelta(seconds=60)
    original_capture = broker.capture_kill_evidence

    async def server_filtered_capture(*, epoch, symbol, start_ms, end_ms):
        complete_history = broker.full_fill_history
        broker.full_fill_history = [
            row
            for row in complete_history
            if int(row.get("time", row.get("time_ms", 0))) <= int(end_ms)
        ]
        try:
            return await original_capture(
                epoch=epoch,
                symbol=symbol,
                start_ms=start_ms,
                end_ms=end_ms,
            )
        finally:
            broker.full_fill_history = complete_history

    broker.capture_kill_evidence = server_filtered_capture

    asyncio.run(engine.kill(flatten=True))

    request = store.active_kill_request()
    assert request is not None
    assert broker.broker_mutations == []
    assert request["terminal_state"] == "AMBIGUOUS", request
    assert request["terminal_reason"] == "OWNERSHIP_AMBIGUOUS"


@pytest.mark.parametrize(
    ("inject_at_capture", "expected_state", "expected_reason", "expected_mutations"),
    [
        (2, "AMBIGUOUS", "OWNERSHIP_AMBIGUOUS", []),
        (3, "UNKNOWN", "FLATTEN_POSITION_NOT_FLAT", ["flatten_reduce_only"]),
    ],
)
def test_repair4_a4_flatten_and_residual_cancel_each_use_fresh_capture(
    tmp_path,
    inject_at_capture,
    expected_state,
    expected_reason,
    expected_mutations,
):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    capture_count = 0
    original_capture = broker.capture_kill_evidence
    base_ms = int(datetime.now(UTC).timestamp() * 1000)

    async def capture_with_interphase_foreign_fill(**kwargs):
        nonlocal capture_count
        capture_count += 1
        if capture_count == inject_at_capture:
            broker.full_fill_history.extend(
                [
                    {
                        "fill_id": f"repair4-phase-{inject_at_capture}-foreign-sell",
                        "oid": 910 + inject_at_capture,
                        "coin": "BTC",
                        "side": "SELL",
                        "sz": 1.0,
                        "px": 100.0,
                        "time": base_ms,
                    },
                    {
                        "fill_id": f"repair4-phase-{inject_at_capture}-foreign-buy",
                        "oid": 920 + inject_at_capture,
                        "coin": "BTC",
                        "side": "BUY",
                        "sz": 1.0,
                        "px": 100.0,
                        "time": base_ms + 1,
                    },
                ]
            )
        return await original_capture(**kwargs)

    broker.capture_kill_evidence = capture_with_interphase_foreign_fill

    asyncio.run(engine.kill(flatten=True))

    request = store.active_kill_request()
    assert request is not None
    assert request["terminal_state"] == expected_state
    assert request["terminal_reason"] == expected_reason
    assert [kind for kind, _cloid in broker.broker_mutations] == expected_mutations
    assert next(
        row for row in broker.orders if row["cloid"] == "repair4-sl"
    )["status"] == "OPEN"


def test_repair4_a10_epoch_open_failure_retains_kill_latch(
    tmp_path, monkeypatch
):
    store, broker, engine = _repair4_kill_engine(tmp_path)

    def fail_open(*args, **kwargs):
        raise sqlite3.OperationalError("injected epoch open fault")

    monkeypatch.setattr(store, "open_kill_epoch", fail_open, raising=False)

    with pytest.raises(sqlite3.OperationalError, match="epoch open fault"):
        asyncio.run(engine.kill(flatten=True))

    assert engine.state == "KILLED"
    assert engine.order_manager.kill_latched is True
    assert store.get_meta("app_state") == "KILLED"
    assert engine._app_state() == "KILLED"
    assert broker.broker_mutations == []
    assert store.active_kill_request() is None
    assert store.get_meta("kill_epoch_active") is None
    assert store.conn.execute(
        "SELECT COUNT(*) FROM kill_requests WHERE terminal_state IN "
        "('SAFE_FLAT','SAFE_RETAINED')"
    ).fetchone()[0] == 0


def test_repair4_f5_prior_state_read_failure_precommits_killed(
    tmp_path, monkeypatch
):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    observer = Store(store.db_path)
    observer.initialize(target_schema_version=9)
    original_get_meta = store.get_meta

    def fail_prior_state_read(key):
        if key == "app_state":
            raise sqlite3.OperationalError("injected prior state read fault")
        return original_get_meta(key)

    monkeypatch.setattr(store, "get_meta", fail_prior_state_read)

    with pytest.raises(sqlite3.OperationalError, match="prior state read fault"):
        asyncio.run(engine.kill(flatten=True))

    assert engine.state == "KILLED"
    assert engine.order_manager.kill_latched is True
    assert observer.get_meta("app_state") == "KILLED"
    assert broker.broker_mutations == []
    assert observer.active_kill_request() is None
    assert observer.get_meta("kill_request_active") is None
    assert observer.get_meta("kill_epoch_active") is None
    assert observer.conn.execute(
        "SELECT COUNT(*) FROM kill_requests WHERE terminal_state IN "
        "('SAFE_FLAT','SAFE_RETAINED')"
    ).fetchone()[0] == 0
    observer.close()


def test_repair4_f1_legacy_killed_without_evidence_is_rejected_by_kill(tmp_path):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    store.set_meta("app_state", "KILLED")
    assert store.conn.execute("SELECT COUNT(*) FROM kill_requests").fetchone()[0] == 0

    with pytest.raises(
        KillConflictError, match="LEGACY_KILLED_EVIDENCE_MISSING"
    ) as failure:
        asyncio.run(engine.kill(flatten=True))

    assert failure.value.reason_code == "LEGACY_KILLED_EVIDENCE_MISSING"
    assert store.get_meta("app_state") == "KILLED"
    assert store.conn.execute("SELECT COUNT(*) FROM kill_requests").fetchone()[0] == 0
    assert broker.broker_mutations == []


def test_repair4_f4_worker_rejection_is_recorded_on_event_loop(
    tmp_path, monkeypatch
):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    observer = Store(store.db_path)
    observer.initialize(target_schema_version=9)
    event_loop_thread = threading.get_ident()
    record_threads: list[int] = []
    original_record = store._record_stale_epoch_rejection

    def tracked_record(epoch, operation):
        record_threads.append(threading.get_ident())
        return original_record(epoch, operation)

    async def reject_at_worker_boundary(
        *,
        symbol,
        cloid,
        size,
        exit_side,
        epoch,
        epoch_guard,
        worker_epoch_guard=None,
    ):
        epoch_guard(epoch)
        store._owned_kill_epoch = None
        worker_guard = worker_epoch_guard or getattr(
            epoch_guard, "in_memory_only"
        )
        worker_guard(epoch)
        raise AssertionError("worker guard must reject")

    monkeypatch.setattr(
        store, "_record_stale_epoch_rejection", tracked_record
    )
    monkeypatch.setattr(
        broker, "kill_flatten_reduce_only", reject_at_worker_boundary
    )

    with pytest.raises(KillConflictError, match="KILL_EPOCH_STALE_WRITE"):
        asyncio.run(engine.kill(flatten=True))

    stale_events = [
        row
        for row in observer.get_events()
        if row["code"] == "KILL_EPOCH_STALE_WRITE_REJECTED"
    ]
    assert len(stale_events) == 1
    assert record_threads == [event_loop_thread]
    assert observer.get_meta("kill_epoch_active") is not None
    observer.close()


def test_s2_a4_cancel_discovered_entry_fill_persists_immutable_evidence_and_ownership(
    tmp_path,
):
    run_id = "s2-a4-cancel-fill"
    now = datetime.now(UTC)
    store = Store(tmp_path / "s2-a4-cancel-fill.db")
    store.initialize(target_schema_version=9)
    store.create_run(run_id, "dry_run", "testnet", {})
    store.set_meta("app_state", "ARMED")
    store.conn.execute(
        "UPDATE runs SET started_ts=? WHERE run_id=?",
        ((now - timedelta(seconds=1)).isoformat(), run_id),
    )
    store.conn.commit()
    decision_uid = "s2-a4-owned-entry"
    store.insert_decision(
        run_id, decision_uid, now, "BTC", "SIGNAL", {"direction": "LONG"}
    )
    trade_id = store.create_trade(
        run_id=run_id,
        coin="BTC",
        direction="LONG",
        qty=0.25,
        entry_decision_uid=decision_uid,
        signal_ts=now,
        decision_ts=now,
        expected_px=101.0,
        risk_dollars=1.0,
        risk_pct=0.001,
        leverage=1,
        sl_initial=95.0,
        tp_initial=None,
        llm_directive_id=None,
    )
    store.insert_order(
        cloid="s2-a4-entry",
        oid=701,
        group_id=decision_uid,
        order_ref="s2-a4-entry-ref",
        order_json={
            "symbol": "BTC",
            "role": "ENTRY",
            "direction": "LONG",
            "side": "BUY",
            "reduce_only": False,
        },
        decision_uid=decision_uid,
        trade_id=trade_id,
        role="ENTRY",
        status="OPEN",
        qty=0.25,
        ts_submit=now,
        ts_last=now,
    )
    broker = MockBroker(
        bars=[
            Bar(
                ts=now,
                open=101.0,
                high=101.0,
                low=101.0,
                close=101.0,
                volume=1.0,
            )
        ]
    )
    broker.orders = [
        {
            "cloid": "s2-a4-entry",
            "oid": 701,
            "role": "ENTRY",
            "status": "OPEN",
            "qty": 0.25,
            "filled_qty": 0.0,
            "reduce_only": False,
            "symbol": "BTC",
            "direction": "LONG",
        }
    ]
    broker.full_open_orders = [
        {
            "cloid": "s2-a4-entry",
            "oid": 701,
            "coin": "BTC",
            "side": "BUY",
            "size": 0.25,
            "role": "ENTRY",
            "reduce_only": False,
            "status": "OPEN",
        }
    ]
    engine = BridgeEngine(
        run_id=run_id,
        broker=broker,
        store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
        state="ARMED",
    )
    broker._user_callbacks.clear()
    broker.late_entry_fill_on_cancel = 0.25
    original_cancel = broker.cancel_order_by_cloid

    async def cancel_with_authoritative_position(cloid, symbol):
        result = await original_cancel(cloid, symbol)
        assert broker.position is not None
        broker.full_positions = [
            {"symbol": symbol, "size": float(broker.position.size)}
        ]
        return result

    broker.cancel_order_by_cloid = cancel_with_authoritative_position

    asyncio.run(engine.kill(flatten=False))

    terminal_query = asyncio.run(broker.query_order("s2-a4-entry", "BTC"))
    assert terminal_query.terminal is True
    assert terminal_query.filled_size == 0.25
    assert terminal_query.oid == 701
    assert terminal_query.cloid == "s2-a4-entry"
    assert terminal_query.symbol == "BTC"
    observed_fill = broker.fills[-1]
    durable_fills = store.list_fills_for_order("s2-a4-entry")
    durable_totals = store.trade_fill_totals(trade_id)
    local_order = store.get_order("s2-a4-entry")
    request = store.active_kill_request()
    assert local_order is not None
    assert request is not None
    assert {
        "fills": [
            {
                "fill_id": row["fill_id"],
                "cloid": row["cloid"],
                "decision_uid": row["decision_uid"],
                "qty": row["qty"],
                "px": row["px"],
                "fee": row["fee"],
                "funding": row["funding"],
            }
            for row in durable_fills
        ],
        "order_status": local_order["status"],
        "order_filled_qty": local_order["filled_qty"],
        "durable_owned_qty": (
            durable_totals["entry_qty"] - durable_totals["exit_qty"]
        ),
        "observed_position_qty": float(broker.position.size),
        "safe_from_stale_ownership": request["terminal_state"]
        in {"SAFE_FLAT", "SAFE_RETAINED"},
    } == {
        "fills": [
            {
                "fill_id": observed_fill["fill_id"],
                "cloid": "s2-a4-entry",
                "decision_uid": decision_uid,
                "qty": 0.25,
                "px": 101.0,
                "fee": 0.0,
                "funding": 0.0,
            }
        ],
        "order_status": "FILLED",
        "order_filled_qty": 0.25,
        "durable_owned_qty": 0.25,
        "observed_position_qty": 0.25,
        "safe_from_stale_ownership": False,
    }


def test_s2_a5_kill_flatten_closes_trade_lifecycle_once_before_ack(tmp_path):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    open_trade = store.get_open_trade_for_coin("repair4-kill", "BTC")
    assert open_trade is not None
    trade_id = int(open_trade["trade_id"])
    decision_uid = str(open_trade["entry_decision_uid"])
    assert store.list_fills_for_order("repair4-entry")

    asyncio.run(engine.kill(flatten=True))

    request = store.active_kill_request()
    assert request is not None
    assert request["terminal_state"] == "SAFE_FLAT"
    flatten_action = store.kill_actions_for_episode(
        request["episode_id"], kind="FLATTEN"
    )[0]
    durable_flatten_fills = store.list_fills_for_order(flatten_action["cloid"])
    assert len(durable_flatten_fills) == 1

    asyncio.run(engine.acknowledge_kill())

    acknowledged = store.get_kill_request(request["episode_id"])
    assert acknowledged is not None
    assert acknowledged["ack_state"] == "ACKNOWLEDGED"
    assert engine.state == "DISARMED"
    closed_trade = store.get_trade(trade_id)
    assert closed_trade is not None
    closed_lifecycle = {
        key: closed_trade[key]
        for key in ("exit_ts", "exit_px", "exit_reason", "pnl")
    }
    assert all(closed_lifecycle[key] is not None for key in closed_lifecycle)
    assert closed_lifecycle["exit_reason"] == "KILL_FLATTEN"
    assert store.get_open_trade_for_coin("repair4-kill", "BTC") is None

    durable_fill = durable_flatten_fills[0]
    replay = OrderManager(store=store, broker=broker, run_id="repair4-kill")
    replay_event = FillEvent(
        fill_id=durable_fill["fill_id"],
        cloid=durable_fill["cloid"],
        coin="BTC",
        qty=durable_fill["qty"],
        px=durable_fill["px"],
        ts=datetime.fromisoformat(durable_fill["fill_ts"]),
        role="CLOSE",
    )
    assert replay._ingest_fill(replay_event) is True
    assert replay._ingest_fill(replay_event) is True
    replayed_trade = store.get_trade(trade_id)
    assert replayed_trade is not None
    assert {
        key: replayed_trade[key]
        for key in ("exit_ts", "exit_px", "exit_reason", "pnl")
    } == closed_lifecycle
    assert store.get_open_trade_for_coin("repair4-kill", "BTC") is None
    assert len(
        [
            row
            for row in store.get_decision_chain(decision_uid)
            if row["stage"] == "TRADE_CLOSED"
        ]
    ) == 1


@pytest.mark.parametrize(
    ("mutation_name", "mutated_qty"),
    [
        ("boolean", True),
        ("numeric_string", "1.0"),
        ("sub_tolerance", 1.0 + 5e-13),
    ],
    ids=["boolean", "numeric-string", "sub-tolerance"],
)
def test_s2_r3_ack_rejects_noncanonical_close_payload_number(
    tmp_path, mutation_name, mutated_qty
):
    store, _broker, engine = _repair4_kill_engine(tmp_path)

    asyncio.run(engine.kill(flatten=True))

    request = store.active_kill_request()
    assert request is not None
    assert request["terminal_state"] == "SAFE_FLAT"
    decisions = store.conn.execute(
        """SELECT id,payload_json FROM decisions
           WHERE stage='TRADE_CLOSED'
           ORDER BY id"""
    ).fetchall()
    assert len(decisions) == 1
    payload = json.loads(str(decisions[0]["payload_json"]))
    assert type(payload["qty"]) is float
    assert payload["qty"] == 1.0
    if mutation_name == "sub_tolerance":
        assert mutated_qty != payload["qty"]
        assert 0.0 < abs(mutated_qty - payload["qty"]) < 1e-12
    payload["qty"] = mutated_qty
    store.conn.execute(
        "UPDATE decisions SET payload_json=? WHERE id=?",
        (
            json.dumps(payload, sort_keys=True, separators=(",", ":")),
            decisions[0]["id"],
        ),
    )
    store.conn.commit()

    with pytest.raises(
        RuntimeError, match="KILL_FLATTEN_LIFECYCLE_CONFLICT"
    ):
        asyncio.run(engine.acknowledge_kill())

    rejected = store.get_kill_request(request["episode_id"])
    assert rejected is not None
    assert rejected["ack_state"] == "PENDING"
    assert store.get_meta("app_state") == "KILLED"
    assert engine.state == "KILLED"


def test_s2_r3_ack_accepts_untouched_canonical_close_payload_numbers(tmp_path):
    store, _broker, engine = _repair4_kill_engine(tmp_path)

    asyncio.run(engine.kill(flatten=True))

    request = store.active_kill_request()
    assert request is not None
    assert request["terminal_state"] == "SAFE_FLAT"
    decisions = store.conn.execute(
        """SELECT payload_json FROM decisions
           WHERE stage='TRADE_CLOSED'
           ORDER BY id"""
    ).fetchall()
    assert len(decisions) == 1
    payload = json.loads(str(decisions[0]["payload_json"]))
    assert all(
        type(payload[key]) is float
        for key in (
            "pnl",
            "pnl_gross",
            "costs",
            "entry_basis_px",
            "exit_vwap",
            "qty",
        )
    )

    asyncio.run(engine.acknowledge_kill())

    acknowledged = store.get_kill_request(request["episode_id"])
    assert acknowledged is not None
    assert acknowledged["ack_state"] == "ACKNOWLEDGED"
    assert store.get_meta("app_state") == "DISARMED"
    assert engine.state == "DISARMED"


@pytest.mark.parametrize("column", ["exit_px", "pnl"])
def test_s2_closure_ack_rejects_any_representable_trade_row_tamper(
    tmp_path, column
):
    store, _broker, engine = _repair4_kill_engine(tmp_path)

    asyncio.run(engine.kill(flatten=True))

    request = store.active_kill_request()
    assert request is not None
    assert request["terminal_state"] == "SAFE_FLAT"
    trade = store.get_open_trade_for_coin("repair4-kill", "BTC")
    assert trade is None
    closed_trade = store.conn.execute(
        "SELECT trade_id,exit_px,pnl FROM trades WHERE run_id=? AND coin=?",
        ("repair4-kill", "BTC"),
    ).fetchone()
    assert closed_trade is not None
    original = float(closed_trade[column])
    tampered = math.nextafter(original, math.inf)
    assert tampered != original
    assert 0.0 < abs(tampered - original) < 1e-12
    store.conn.execute(
        f"UPDATE trades SET {column}=? WHERE trade_id=?",
        (tampered, closed_trade["trade_id"]),
    )
    store.conn.commit()
    persisted = store.conn.execute(
        f"SELECT {column} FROM trades WHERE trade_id=?",
        (closed_trade["trade_id"],),
    ).fetchone()
    assert persisted is not None
    assert float(persisted[column]) == tampered

    with pytest.raises(
        KillConflictError, match="KILL_FLATTEN_LIFECYCLE_CONFLICT"
    ) as failure:
        store.validate_applied_kill_flatten_lifecycle_closures(
            episode_id=str(request["episode_id"]),
            run_id="repair4-kill",
            symbol="BTC",
        )
    assert failure.value.reason_code == "KILL_FLATTEN_LIFECYCLE_CONFLICT"

    with pytest.raises(
        RuntimeError, match="KILL_FLATTEN_LIFECYCLE_CONFLICT"
    ):
        asyncio.run(engine.acknowledge_kill())

    rejected = store.get_kill_request(request["episode_id"])
    assert rejected is not None
    assert rejected["ack_state"] == "PENDING"
    assert store.get_meta("app_state") == "KILLED"
    assert engine.state == "KILLED"


def test_s3t_a_kill_closure_public_api_enumeration_is_generated():
    assert _S3T_KILL_CLOSURE_PUBLIC_APIS
    assert all(not name.startswith("_") for name in _S3T_KILL_CLOSURE_PUBLIC_APIS)


@pytest.mark.parametrize("api_name", _S3T_KILL_CLOSURE_PUBLIC_APIS)
@pytest.mark.parametrize(
    ("column", "contract"),
    [
        pytest.param(column, contract, id=column)
        for (table, column), contract in DURABLE_EVENT_COLUMN_TYPES.items()
        if table == "fills" and not contract.nullable
    ],
)
@pytest.mark.parametrize(
    "corrupt_value",
    [
        pytest.param(None, id="null"),
        pytest.param("not-a-number", id="non-numeric-text"),
    ],
)
def test_s3t_a_generated_kill_public_store_api_fault_containment(
    tmp_path, api_name, column, contract, corrupt_value
):
    """No public kill-closure API leaks the typed conversion fault."""
    del contract
    store, _broker, engine = _repair4_kill_engine(tmp_path)
    asyncio.run(engine.kill(flatten=True))
    request = store.active_kill_request()
    assert request is not None
    entry_fill = store.list_fills_for_order("repair4-entry")[0]
    store.conn.execute(
        f"UPDATE fills SET {column}=? WHERE fill_id=?",
        (corrupt_value, entry_fill["fill_id"]),
    )
    store.conn.commit()

    available_arguments = {
        "episode_id": str(request["episode_id"]),
        "run_id": "repair4-kill",
        "symbol": "BTC",
        "now": engine.clock(),
        "max_age_s": engine.full_reconcile_max_age_s(),
    }
    public_api = getattr(store, api_name)
    arguments = {
        name: available_arguments[name]
        for name in inspect.signature(public_api).parameters
    }
    with pytest.raises(KillConflictError) as failure:
        public_api(**arguments)

    assert not isinstance(failure.value, DurableRowFault)
    assert failure.value.reason_code == "KILL_FLATTEN_LIFECYCLE_CONFLICT"
    assert store.conn.in_transaction is False
    assert store.get_kill_request(str(request["episode_id"]))["ack_state"] == "PENDING"
    store.close()


def test_s2_a5_crash_restart_recovers_kill_flatten_before_safe_flat(tmp_path, monkeypatch):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    db_path = store.db_path
    open_trade = store.get_open_trade_for_coin("repair4-kill", "BTC")
    assert open_trade is not None
    trade_id = int(open_trade["trade_id"])
    decision_uid = str(open_trade["entry_decision_uid"])

    def crash_after_coupled_flatten_commit(_fill):
        request = store.active_kill_request()
        assert request is not None
        action = store.kill_actions_for_episode(
            request["episode_id"], kind="FLATTEN"
        )[0]
        assert action["current_outcome"] == "APPLIED"
        durable_fills = store.list_fills_for_order(action["cloid"])
        assert len(durable_fills) == 1
        assert [
            event["status"]
            for event in store.kill_action_events(action["action_id"])
            if event["status"] == "APPLIED"
        ] == ["APPLIED"]
        stranded = store.get_trade(trade_id)
        assert stranded is not None
        assert stranded["exit_ts"] is None
        raise RuntimeError("INJECTED_AFTER_APPLIED_FLATTEN_COMMIT")

    monkeypatch.setattr(
        engine.order_manager, "_ingest_fill", crash_after_coupled_flatten_commit
    )
    with pytest.raises(
        RuntimeError, match="INJECTED_AFTER_APPLIED_FLATTEN_COMMIT"
    ):
        asyncio.run(engine.kill(flatten=True))

    request = store.active_kill_request()
    assert request is not None
    flatten_action = store.kill_actions_for_episode(
        request["episode_id"], kind="FLATTEN"
    )[0]
    durable_flatten_fills = store.list_fills_for_order(flatten_action["cloid"])
    assert flatten_action["current_outcome"] == "APPLIED"
    assert len(durable_flatten_fills) == 1
    assert broker.position is None
    assert store.get_trade(trade_id)["exit_ts"] is None

    broker._user_callbacks.clear()
    store.close()
    restarted_store = Store(db_path)
    restarted_store.initialize(target_schema_version=9)
    restarted_engine = BridgeEngine(
        run_id="repair4-kill",
        broker=broker,
        store=restarted_store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
        state="KILLED",
    )

    asyncio.run(restarted_engine.kill(flatten=True))

    recovered_request = restarted_store.active_kill_request()
    assert recovered_request is not None
    assert recovered_request["episode_id"] == request["episode_id"]
    assert recovered_request["terminal_state"] == "SAFE_FLAT"
    recovered_trade = restarted_store.get_trade(trade_id)
    assert recovered_trade is not None
    durable_fill = durable_flatten_fills[0]
    recovered_lifecycle = {
        key: recovered_trade[key]
        for key in ("exit_ts", "exit_px", "exit_reason", "pnl")
    }
    assert recovered_lifecycle == {
        "exit_ts": durable_fill["fill_ts"],
        "exit_px": durable_fill["px"],
        "exit_reason": "KILL_FLATTEN",
        "pnl": pytest.approx(0.0),
    }
    assert restarted_store.get_open_trade_for_coin("repair4-kill", "BTC") is None
    assert len(
        [
            row
            for row in restarted_store.get_decision_chain(decision_uid)
            if row["stage"] == "TRADE_CLOSED"
        ]
    ) == 1

    asyncio.run(restarted_engine.kill(flatten=True))

    replayed_trade = restarted_store.get_trade(trade_id)
    assert replayed_trade is not None
    assert {
        key: replayed_trade[key]
        for key in ("exit_ts", "exit_px", "exit_reason", "pnl")
    } == recovered_lifecycle
    assert len(
        [
            row
            for row in restarted_store.get_decision_chain(decision_uid)
            if row["stage"] == "TRADE_CLOSED"
        ]
    ) == 1

    asyncio.run(restarted_engine.acknowledge_kill())
    acknowledged = restarted_store.get_kill_request(request["episode_id"])
    assert acknowledged is not None
    assert acknowledged["ack_state"] == "ACKNOWLEDGED"
    assert restarted_engine.state == "DISARMED"


def test_s2_r2_startup_drain_defers_kill_flatten_without_epoch(
    tmp_path, monkeypatch
):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    db_path = store.db_path
    trade = store.get_open_trade_for_coin("repair4-kill", "BTC")
    assert trade is not None
    trade_id = int(trade["trade_id"])
    decision_uid = str(trade["entry_decision_uid"])

    def crash_after_coupled_flatten_commit(_fill):
        raise RuntimeError("INJECTED_AFTER_APPLIED_FLATTEN_COMMIT")

    monkeypatch.setattr(
        engine.order_manager, "_ingest_fill", crash_after_coupled_flatten_commit
    )
    with pytest.raises(
        RuntimeError, match="INJECTED_AFTER_APPLIED_FLATTEN_COMMIT"
    ):
        asyncio.run(engine.kill(flatten=True))

    request = store.active_kill_request()
    assert request is not None
    flatten_action = store.kill_actions_for_episode(
        request["episode_id"], kind="FLATTEN"
    )[0]
    durable_fill = store.list_fills_for_order(flatten_action["cloid"])[0]
    assert store.get_trade(trade_id)["exit_ts"] is None

    broker._user_callbacks.clear()
    store.close()
    restarted_store = Store(db_path)
    restarted_store.initialize(target_schema_version=9)
    restarted_engine = BridgeEngine(
        run_id="repair4-kill",
        broker=broker,
        store=restarted_store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
        state="KILLED",
    )
    redelivered = FillEvent(
        fill_id=str(durable_fill["fill_id"]),
        cloid=str(durable_fill["cloid"]),
        coin="BTC",
        qty=float(durable_fill["qty"]),
        px=float(durable_fill["px"]),
        ts=datetime.fromisoformat(str(durable_fill["fill_ts"])),
        role="UNKNOWN",
    )
    restarted_engine.order_manager._queue_event(redelivered)
    assert restarted_engine.order_manager._active_kill_epoch is None

    consumed = asyncio.run(restarted_engine.order_manager.drain_queued_events())

    assert consumed == 0
    assert restarted_engine.order_manager._queued_events == [redelivered]
    deferred_trade = restarted_store.get_trade(trade_id)
    assert deferred_trade is not None
    assert deferred_trade["exit_ts"] is None
    assert [
        row
        for row in restarted_store.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ] == []
    with pytest.raises(KillConflictError, match="KILL_EPOCH_REQUIRED") as unowned:
        restarted_store.close_trade_once_with_decision(
            trade_id=trade_id,
            run_id="repair4-kill",
            decision_uid=decision_uid,
            coin="BTC",
            exit_px=float(durable_fill["px"]),
            exit_ts=str(durable_fill["fill_ts"]),
            exit_reason="KILL_FLATTEN",
            pnl=0.0,
            payload={},
        )
    assert unowned.value.reason_code == "KILL_EPOCH_REQUIRED"
    assert restarted_store.conn.in_transaction is False

    # This is the same drain entrypoint used by startup reconciliation. It must
    # return normally while retaining the deferred event for kill recovery.
    asyncio.run(restarted_engine.order_manager.sync_broker_state())
    assert restarted_engine.order_manager._queued_events == [redelivered]

    asyncio.run(restarted_engine.kill(flatten=True))

    recovered_trade = restarted_store.get_trade(trade_id)
    assert recovered_trade is not None
    assert recovered_trade["exit_reason"] == "KILL_FLATTEN"
    assert restarted_engine.order_manager._queued_events == []


def _s3_stranded_kill_restart(tmp_path, monkeypatch):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    db_path = store.db_path
    trade = store.get_open_trade_for_coin("repair4-kill", "BTC")
    assert trade is not None
    trade_id = int(trade["trade_id"])
    decision_uid = str(trade["entry_decision_uid"])

    def crash_after_coupled_flatten_commit(_fill):
        raise RuntimeError("INJECTED_AFTER_APPLIED_FLATTEN_COMMIT")

    monkeypatch.setattr(
        engine.order_manager, "_ingest_fill", crash_after_coupled_flatten_commit
    )
    with pytest.raises(
        RuntimeError, match="INJECTED_AFTER_APPLIED_FLATTEN_COMMIT"
    ):
        asyncio.run(engine.kill(flatten=True))

    request = store.active_kill_request()
    assert request is not None
    flatten_action = store.kill_actions_for_episode(
        request["episode_id"], kind="FLATTEN"
    )[0]
    durable_fill = store.list_fills_for_order(flatten_action["cloid"])[0]
    assert store.get_trade(trade_id)["exit_ts"] is None

    broker._user_callbacks.clear()
    store.close()
    restarted_store = Store(db_path)
    restarted_store.initialize(target_schema_version=9)
    restarted_engine = BridgeEngine(
        run_id="repair4-kill",
        broker=broker,
        store=restarted_store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
        state="KILLED",
    )
    redelivered = FillEvent(
        fill_id=str(durable_fill["fill_id"]),
        cloid=str(durable_fill["cloid"]),
        coin="BTC",
        qty=float(durable_fill["qty"]),
        px=float(durable_fill["px"]),
        ts=datetime.fromisoformat(str(durable_fill["fill_ts"])),
        role="UNKNOWN",
    )
    return (
        restarted_store,
        broker,
        restarted_engine,
        request,
        redelivered,
        trade_id,
        decision_uid,
    )


def _s3_open_epoch(store, request, *, process_uid, opened_ts_monotonic):
    return store.open_kill_epoch(
        run_id=str(request["run_id"]),
        symbol=str(request["symbol"]),
        flatten_requested=bool(request["flatten_requested"]),
        policy_version=str(request["policy_version"]),
        process_uid=process_uid,
        opened_ts_monotonic=opened_ts_monotonic,
    )[1]


def test_s3_deferral_event_is_durable_secret_safe_and_idempotent(
    tmp_path, monkeypatch
):
    (
        store,
        broker,
        engine,
        request,
        redelivered,
        trade_id,
        _decision_uid,
    ) = _s3_stranded_kill_restart(tmp_path, monkeypatch)
    observer = Store(store.db_path)
    observer.initialize(target_schema_version=9)
    assert observer is not store
    engine.order_manager._queue_event(redelivered)

    assert asyncio.run(engine.order_manager.drain_queued_events()) == 0
    assert asyncio.run(engine.order_manager.drain_queued_events()) == 0

    second_store = Store(store.db_path)
    second_store.initialize(target_schema_version=9)
    assert second_store is not store
    second_manager = OrderManager(
        store=second_store, broker=broker, run_id="repair4-kill"
    )
    second_manager._queue_event(FillEvent(**redelivered.model_dump()))
    assert asyncio.run(second_manager.drain_queued_events()) == 0

    deferred = [
        row
        for row in observer.get_events()
        if row["code"] == "KILL_EPOCH_LIFECYCLE_DEFERRED"
    ]
    assert len(deferred) == 1
    detail = str(deferred[0]["detail"])
    assert detail == (
        "episode_sha256="
        + hashlib.sha256(str(request["episode_id"]).encode("utf-8")).hexdigest()
        + f";trade_id={trade_id};fill_sha256="
        + hashlib.sha256(redelivered.fill_id.encode("utf-8")).hexdigest()
        + ";reason=KILL_EPOCH_REQUIRED"
    )
    assert str(request["episode_id"]) not in detail
    assert redelivered.fill_id not in detail
    assert engine.order_manager._queued_events == [redelivered]
    assert second_manager._queued_events == [redelivered]
    second_store.close()
    observer.close()
    store.close()


def test_s3_status_exposes_open_lifecycle_and_deferred_queue_depth(
    tmp_path, monkeypatch
):
    store, _broker, engine, _request, redelivered, _trade_id, _decision_uid = (
        _s3_stranded_kill_restart(tmp_path, monkeypatch)
    )
    engine.order_manager._queue_event(redelivered)

    status = engine.status()

    assert status["kill_episode"] is not None
    assert status["kill_episode"]["lifecycle_state"] == "AWAITING_EPOCH_RECOVERY"
    assert status["deferred_event_queue_depth"] == 1
    store.close()


def test_s3_status_distinguishes_ack_eligible_lifecycle(tmp_path):
    store, _broker, engine = _repair4_kill_engine(tmp_path)

    asyncio.run(engine.kill(flatten=True))
    status = engine.status()

    assert status["kill_episode"] is not None
    assert status["kill_episode"]["lifecycle_state"] == "AWAITING_ACK"
    assert status["deferred_event_queue_depth"] == 0
    store.close()


def test_s3_exact_fill_redelivery_is_coalesced_but_conflict_is_retained(
    tmp_path, monkeypatch
):
    store, _broker, engine, _request, redelivered, _trade_id, _decision_uid = (
        _s3_stranded_kill_restart(tmp_path, monkeypatch)
    )
    engine.order_manager._queue_event(redelivered)
    assert asyncio.run(engine.order_manager.drain_queued_events()) == 0

    exact_redelivery = FillEvent(**redelivered.model_dump())
    engine.order_manager._queue_event(exact_redelivery)
    assert engine.order_manager._queued_events == [exact_redelivery]

    conflicting_payload = redelivered.model_copy(
        update={"px": redelivered.px + 1.0}
    )
    engine.order_manager._queue_event(conflicting_payload)
    assert engine.order_manager._queued_events == [
        exact_redelivery,
        conflicting_payload,
    ]
    assert asyncio.run(engine.order_manager.drain_queued_events()) == 1
    assert engine.order_manager._queued_events == [exact_redelivery]
    assert "FILL_ID_CONFLICT" in {
        row["code"] for row in store.get_events()
    }
    assert asyncio.run(engine.order_manager.drain_queued_events()) == 0
    assert engine.order_manager._queued_events == [exact_redelivery]
    store.close()


def test_s3_stale_epoch_startup_drain_defers_but_store_caller_still_sees_fence(
    tmp_path, monkeypatch
):
    (
        stale_store,
        _broker,
        stale_engine,
        request,
        redelivered,
        trade_id,
        decision_uid,
    ) = _s3_stranded_kill_restart(tmp_path, monkeypatch)
    _request, stale_epoch = stale_store.open_kill_epoch(
        run_id=str(request["run_id"]),
        symbol=str(request["symbol"]),
        flatten_requested=bool(request["flatten_requested"]),
        policy_version=str(request["policy_version"]),
        process_uid="s3-stale-drain-owner",
        opened_ts_monotonic=10.0,
    )
    stale_engine.order_manager._active_kill_epoch = stale_epoch
    competitor = Store(stale_store.db_path)
    competitor.initialize(target_schema_version=9)
    assert competitor is not stale_store
    _request, newer_epoch = competitor.open_kill_epoch(
        run_id=str(request["run_id"]),
        symbol=str(request["symbol"]),
        flatten_requested=bool(request["flatten_requested"]),
        policy_version=str(request["policy_version"]),
        process_uid="s3-newer-drain-owner",
        opened_ts_monotonic=11.0,
    )
    assert newer_epoch.attempt_no == stale_epoch.attempt_no + 1

    with pytest.raises(KillConflictError, match="KILL_EPOCH_STALE_WRITE") as stale:
        stale_store.close_trade_once_with_decision(
            trade_id=trade_id,
            run_id="repair4-kill",
            decision_uid=decision_uid,
            coin="BTC",
            exit_px=redelivered.px,
            exit_ts=redelivered.ts,
            exit_reason="KILL_FLATTEN",
            pnl=0.0,
            payload={},
            epoch=stale_epoch,
        )
    assert stale.value.reason_code == "KILL_EPOCH_STALE_WRITE"
    assert stale_store.conn.in_transaction is False
    assert competitor.get_trade(trade_id)["exit_ts"] is None
    assert [
        row
        for row in competitor.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ] == []
    stale_events_before_start = [
        row
        for row in competitor.get_events()
        if row["code"] == "KILL_EPOCH_STALE_WRITE_REJECTED"
    ]
    assert len(stale_events_before_start) == 1

    stale_engine.order_manager._queue_event(redelivered)

    async def drain_same_symbol():
        async with stale_engine.order_manager.symbol_locks.hold("BTC"):
            stale_engine.order_manager._drain_queued_events_locked("BTC")

    asyncio.run(drain_same_symbol())
    assert stale_engine.order_manager._queued_events == [redelivered]

    async def start_and_stop():
        await stale_engine.start(lookback=0)
        await stale_engine.stop()

    asyncio.run(start_and_stop())

    assert stale_engine.reconcile_ready is True
    assert stale_engine.order_manager._queued_events == [redelivered]
    assert competitor.get_trade(trade_id)["exit_ts"] is None
    assert [
        row
        for row in competitor.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ] == []
    assert len(
        [
            row
            for row in competitor.get_events()
            if row["code"] == "KILL_EPOCH_STALE_WRITE_REJECTED"
        ]
    ) == 2
    assert len(
        [
            row
            for row in competitor.get_events()
            if row["code"] == "KILL_EPOCH_LIFECYCLE_DEFERRED"
        ]
    ) == 1
    competitor.close()
    stale_store.close()


def test_s3_drain_propagates_non_kill_conflict_failures(tmp_path, monkeypatch):
    store, _broker, engine = _repair4_kill_engine(tmp_path)
    event = FillEvent(
        fill_id="s3-non-kill-error",
        cloid="repair4-entry",
        coin="BTC",
        qty=1.0,
        px=100.0,
        ts=datetime.now(UTC),
        role="ENTRY",
    )
    engine.order_manager._queue_event(event)

    def fail_unexpectedly(_event):
        raise RuntimeError("UNRELATED_DRAIN_FAILURE")

    monkeypatch.setattr(engine.order_manager, "_ingest_event", fail_unexpectedly)
    with pytest.raises(RuntimeError, match="UNRELATED_DRAIN_FAILURE"):
        asyncio.run(engine.order_manager.drain_queued_events())
    assert engine.order_manager._queued_events == [event]
    store.close()


def test_s3_r2_durable_close_invalidates_unchanged_deferral_suppression(
    tmp_path, monkeypatch
):
    (
        stale_store,
        broker,
        stale_engine,
        request,
        redelivered,
        trade_id,
        _decision_uid,
    ) = _s3_stranded_kill_restart(tmp_path, monkeypatch)
    stale_epoch = _s3_open_epoch(
        stale_store,
        request,
        process_uid="s3-r2-f1-stale",
        opened_ts_monotonic=10.0,
    )
    stale_engine.order_manager._active_kill_epoch = stale_epoch

    winner_store = Store(stale_store.db_path)
    winner_store.initialize(target_schema_version=9)
    assert winner_store is not stale_store
    winner_epoch = _s3_open_epoch(
        winner_store,
        request,
        process_uid="s3-r2-f1-winner",
        opened_ts_monotonic=11.0,
    )
    winner_manager = OrderManager(
        store=winner_store, broker=broker, run_id="repair4-kill"
    )
    winner_manager._active_kill_epoch = winner_epoch

    stale_engine.order_manager._queue_event(redelivered)
    assert asyncio.run(stale_engine.order_manager.drain_queued_events()) == 0
    assert stale_engine.order_manager._queued_events == [redelivered]

    winner_manager._queue_event(FillEvent(**redelivered.model_dump()))
    assert asyncio.run(winner_manager.drain_queued_events()) == 1
    assert winner_store.get_trade(trade_id)["exit_ts"] is not None

    assert asyncio.run(stale_engine.order_manager.drain_queued_events()) == 1
    assert stale_engine.order_manager._queued_events == []
    assert stale_engine.order_manager._deferred_kill_fills == {}
    winner_store.close()
    stale_store.close()


def test_s3_r2_ep4_append_failure_is_not_converted_to_deferral(
    tmp_path, monkeypatch
):
    (
        stale_store,
        _broker,
        stale_engine,
        request,
        redelivered,
        _trade_id,
        _decision_uid,
    ) = _s3_stranded_kill_restart(tmp_path, monkeypatch)
    stale_epoch = _s3_open_epoch(
        stale_store,
        request,
        process_uid="s3-r2-f2-stale",
        opened_ts_monotonic=10.0,
    )
    stale_engine.order_manager._active_kill_epoch = stale_epoch
    observer = Store(stale_store.db_path)
    observer.initialize(target_schema_version=9)
    assert observer is not stale_store
    _s3_open_epoch(
        observer,
        request,
        process_uid="s3-r2-f2-winner",
        opened_ts_monotonic=11.0,
    )

    original_insert = stale_store._insert_event_in_tx

    def fail_only_ep4(run_id, ts, severity, code, detail):
        if code == "KILL_EPOCH_STALE_WRITE_REJECTED":
            raise RuntimeError("injected EP-4 append failure")
        return original_insert(run_id, ts, severity, code, detail)

    monkeypatch.setattr(stale_store, "_insert_event_in_tx", fail_only_ep4)
    stale_engine.order_manager._queue_event(redelivered)
    consumed = None
    raised_reason = None
    try:
        consumed = asyncio.run(stale_engine.order_manager.drain_queued_events())
    except KillConflictError as exc:
        raised_reason = exc.reason_code

    events = observer.get_events()
    actual = (
        raised_reason,
        consumed,
        len([row for row in events if row["code"] == "KILL_EPOCH_STALE_WRITE_REJECTED"]),
        [
            str(row["detail"]).rsplit(";reason=", 1)[-1]
            for row in events
            if row["code"] == "KILL_EPOCH_LIFECYCLE_DEFERRED"
        ],
    )
    assert actual == ("KILL_STALE_EVIDENCE_RECORD_FAILED", None, 0, [])
    assert stale_engine.order_manager._queued_events == [redelivered]
    observer.close()
    stale_store.close()


def test_s3_r2_canonical_then_conflicting_fill_reaches_quarantine(
    tmp_path, monkeypatch
):
    store, _broker, engine, request, redelivered, _trade_id, _decision_uid = (
        _s3_stranded_kill_restart(tmp_path, monkeypatch)
    )
    engine.order_manager._queue_event(redelivered)
    assert asyncio.run(engine.order_manager.drain_queued_events()) == 0
    epoch = _s3_open_epoch(
        store,
        request,
        process_uid="s3-r2-f3-owner",
        opened_ts_monotonic=10.0,
    )
    engine.order_manager._active_kill_epoch = epoch
    conflicting = redelivered.model_copy(update={"px": redelivered.px + 1.0})
    engine.order_manager._queue_event(conflicting)
    assert engine.order_manager._queued_events == [redelivered, conflicting]

    assert asyncio.run(engine.order_manager.drain_queued_events()) == 2
    assert engine.order_manager._queued_events == []
    conflicts = [
        row for row in store.get_events() if row["code"] == "FILL_ID_CONFLICT"
    ]
    assert len(conflicts) == 1
    store.close()


@pytest.mark.parametrize("missing_column", ["group_id", "trade_id"])
def test_s3_r2_incomplete_kill_identity_is_contained_at_startup(
    tmp_path, monkeypatch, missing_column
):
    store, _broker, engine, _request, redelivered, trade_id, decision_uid = (
        _s3_stranded_kill_restart(tmp_path, monkeypatch)
    )
    store.conn.execute(
        f"UPDATE orders SET {missing_column}=NULL WHERE cloid=?",
        (redelivered.cloid,),
    )
    store.conn.commit()
    observer = Store(store.db_path)
    observer.initialize(target_schema_version=9)
    assert observer is not store
    engine.order_manager._queue_event(redelivered)

    async def start_and_stop():
        await engine.start(lookback=0)
        await engine.stop()

    asyncio.run(start_and_stop())

    assert engine.reconcile_ready is True
    assert engine.order_manager._queued_events == []
    assert observer.get_trade(trade_id)["exit_ts"] is None
    assert [
        row
        for row in observer.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ] == []
    identity_faults = [
        row
        for row in observer.get_events()
        if row["code"] == "KILL_LIFECYCLE_IDENTITY_MISSING"
    ]
    assert len(identity_faults) == 1
    assert f"missing={missing_column}" in str(identity_faults[0]["detail"])
    assert observer.get_meta("app_state") in {"DISARMED", "KILLED"}
    observer.close()
    store.close()


def test_s3_r2_consumed_quantity_fault_clears_deferred_fill_cache(
    tmp_path, monkeypatch
):
    store, _broker, engine, request, redelivered, _trade_id, _decision_uid = (
        _s3_stranded_kill_restart(tmp_path, monkeypatch)
    )
    observer = Store(store.db_path)
    observer.initialize(target_schema_version=9)
    assert observer is not store
    engine.order_manager._queue_event(redelivered)
    assert asyncio.run(engine.order_manager.drain_queued_events()) == 0
    assert redelivered.fill_id in engine.order_manager._deferred_kill_fills

    epoch = _s3_open_epoch(
        store,
        request,
        process_uid="s3-r2-f5-owner",
        opened_ts_monotonic=10.0,
    )
    engine.order_manager._active_kill_epoch = epoch
    monkeypatch.setattr(engine.order_manager, "_broker_lot_unit", lambda _coin: None)

    assert asyncio.run(engine.order_manager.drain_queued_events()) == 1
    assert engine.order_manager._queued_events == []
    assert engine.order_manager._deferred_kill_fills == {}
    assert "FILL_QUANTITY_INTEGRITY" in {
        row["code"] for row in observer.get_events()
    }
    observer.close()
    store.close()


@pytest.mark.parametrize(
    ("column", "value", "missing_identity"),
    [
        ("group_id", "dangling-episode", "episode"),
        ("trade_id", "not-an-integer", "trade_id"),
    ],
)
def test_s3_r3_invalid_durable_kill_identity_is_consumed_at_startup(
    tmp_path, monkeypatch, column, value, missing_identity
):
    store, _broker, engine, _request, redelivered, trade_id, decision_uid = (
        _s3_stranded_kill_restart(tmp_path, monkeypatch)
    )
    store.conn.execute(
        f"UPDATE orders SET {column}=? WHERE cloid=?",
        (value, redelivered.cloid),
    )
    store.conn.commit()
    observer = Store(store.db_path)
    observer.initialize(target_schema_version=9)
    assert observer is not store
    engine.order_manager._queue_event(redelivered)

    async def start_probe_and_stop():
        await engine.start(lookback=0)
        status = engine.status()
        with pytest.raises(RuntimeError, match="KILLED requires operator acknowledgement"):
            await engine.arm()
        with pytest.raises(RuntimeError, match="KILL_"):
            await engine.acknowledge_kill()
        await engine.stop()
        return status

    status = asyncio.run(start_probe_and_stop())

    assert engine.reconcile_ready is True
    assert engine.order_manager._queued_events == []
    assert engine.order_manager._deferred_kill_fills == {}
    assert engine.order_manager._synced_fills[redelivered.fill_id] == (
        engine.order_manager._fill_delivery_identity(redelivered)
    )
    assert observer.get_trade(trade_id)["exit_ts"] is None
    assert [
        row
        for row in observer.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ] == []
    identity_faults = [
        row
        for row in observer.get_events()
        if row["code"] == "KILL_LIFECYCLE_IDENTITY_MISSING"
    ]
    assert len(identity_faults) == 1
    assert f"missing={missing_identity}" in str(identity_faults[0]["detail"])
    assert not [
        row
        for row in observer.get_events()
        if row["code"] == "KILL_EPOCH_LIFECYCLE_DEFERRED"
    ]
    assert status["state"] == "KILLED"
    assert status["deferred_event_queue_depth"] == 0
    assert observer.get_meta("app_state") == "KILLED"
    observer.close()
    store.close()


def _s3_schema_admitted_kill_fill(tmp_path, target_schema_version):
    run_id = f"s3-r3-schema-v{target_schema_version}"
    store = Store(tmp_path / f"schema-v{target_schema_version}.db")
    store.initialize(target_schema_version=target_schema_version)
    store.create_run(run_id, "dry_run", "testnet", {})
    store.set_meta("app_state", "ARMED")
    entry_ts = datetime.now(UTC) - timedelta(seconds=2)
    decision_uid = f"s3-r3-entry-v{target_schema_version}"
    store.insert_decision(
        run_id, decision_uid, entry_ts, "BTC", "SIGNAL", {"direction": "LONG"}
    )
    trade_id = store.create_trade(
        run_id=run_id,
        coin="BTC",
        direction="LONG",
        qty=1.0,
        entry_decision_uid=decision_uid,
        signal_ts=entry_ts,
        decision_ts=entry_ts,
        expected_px=100.0,
        risk_dollars=10.0,
        risk_pct=0.01,
        leverage=1,
        sl_initial=90.0,
        tp_initial=None,
        llm_directive_id=None,
    )
    entry_cloid = f"s3-r3-entry-v{target_schema_version}"
    store.insert_order(
        cloid=entry_cloid,
        oid=1,
        group_id=decision_uid,
        order_ref=f"{entry_cloid}:ENTRY",
        order_json={"symbol": "BTC", "role": "ENTRY"},
        decision_uid=decision_uid,
        trade_id=trade_id,
        role="ENTRY",
        status="FILLED",
        qty=1.0,
        filled_qty=1.0,
        ts_submit=entry_ts,
        ts_last=entry_ts,
    )
    store.insert_fill(
        f"s3-r3-entry-fill-v{target_schema_version}",
        entry_cloid,
        decision_uid,
        entry_ts,
        1.0,
        100.0,
        0.0,
        0.0,
    )
    kill_cloid = f"s3-r3-kill-v{target_schema_version}"
    store.insert_order(
        cloid=kill_cloid,
        oid=2,
        group_id=f"s3-r3-episode-v{target_schema_version}",
        order_ref=f"{kill_cloid}:KILL_FLATTEN",
        order_json={"symbol": "BTC", "role": "KILL_FLATTEN"},
        decision_uid=decision_uid,
        trade_id=trade_id,
        role="KILL_FLATTEN",
        status="SUBMITTED",
        qty=1.0,
        filled_qty=0.0,
        ts_submit=entry_ts,
        ts_last=entry_ts,
    )
    broker = MockBroker(bars=[])
    engine = BridgeEngine(
        run_id=run_id,
        broker=broker,
        store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
        state="ARMED",
    )
    redelivered = FillEvent(
        fill_id=f"s3-r3-kill-fill-v{target_schema_version}",
        cloid=kill_cloid,
        coin="BTC",
        qty=1.0,
        px=99.0,
        ts=datetime.now(UTC),
        role="UNKNOWN",
    )
    return store, engine, redelivered, trade_id, decision_uid


@pytest.mark.parametrize(
    (
        "target_schema_version",
        "migrate_to_v9",
        "expected_missing",
        "expected_ack_failure",
    ),
    [
        (4, False, "kill_schema", "KILL_SCHEMA_INACTIVE"),
        (8, False, "kill_schema", "KILL_SCHEMA_INACTIVE"),
        (8, True, "episode", "KILL_EVIDENCE_MISSING"),
    ],
)
def test_s3_r3_schema_capability_and_preserved_v8_order_are_contained(
    tmp_path,
    target_schema_version,
    migrate_to_v9,
    expected_missing,
    expected_ack_failure,
):
    store, engine, redelivered, trade_id, decision_uid = (
        _s3_schema_admitted_kill_fill(tmp_path, target_schema_version)
    )
    if migrate_to_v9:
        store.initialize(target_schema_version=9)
        assert store.conn.execute("SELECT COUNT(*) FROM kill_requests").fetchone()[0] == 0
    observer = Store(store.db_path)
    observer.initialize(
        target_schema_version=9 if migrate_to_v9 else target_schema_version
    )
    assert observer is not store
    engine.order_manager._queue_event(redelivered)

    async def start_probe_and_stop():
        await engine.start(lookback=0)
        status = engine.status()
        with pytest.raises(RuntimeError, match="KILLED requires operator acknowledgement"):
            await engine.arm()
        with pytest.raises(RuntimeError, match=expected_ack_failure):
            await engine.acknowledge_kill()
        await engine.stop()
        return status

    status = asyncio.run(start_probe_and_stop())

    assert engine.order_manager._queued_events == []
    assert engine.order_manager._deferred_kill_fills == {}
    assert redelivered.fill_id in engine.order_manager._synced_fills
    assert observer.get_trade(trade_id)["exit_ts"] is None
    assert [
        row
        for row in observer.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ] == []
    identity_faults = [
        row
        for row in observer.get_events()
        if row["code"] == "KILL_LIFECYCLE_IDENTITY_MISSING"
    ]
    assert len(identity_faults) == 1
    assert f"missing={expected_missing}" in str(identity_faults[0]["detail"])
    assert status["state"] == "KILLED"
    assert status["kill_episode"] is None
    assert status["deferred_event_queue_depth"] == 0
    assert observer.get_meta("app_state") == "KILLED"
    observer.close()
    store.close()


def test_s3_r3_deferred_suppression_revalidates_identity_without_raising(
    tmp_path, monkeypatch
):
    store, _broker, engine, _request, redelivered, trade_id, decision_uid = (
        _s3_stranded_kill_restart(tmp_path, monkeypatch)
    )
    competitor = Store(store.db_path)
    competitor.initialize(target_schema_version=9)
    assert competitor is not store
    engine.order_manager._queue_event(redelivered)
    assert asyncio.run(engine.order_manager.drain_queued_events()) == 0
    assert redelivered.fill_id in engine.order_manager._deferred_kill_fills

    competitor.conn.execute(
        "UPDATE orders SET trade_id=? WHERE cloid=?",
        ("not-an-integer", redelivered.cloid),
    )
    competitor.conn.commit()

    async def start_and_stop():
        await engine.start(lookback=0)
        await engine.stop()

    asyncio.run(start_and_stop())

    assert engine.order_manager._queued_events == []
    assert engine.order_manager._deferred_kill_fills == {}
    assert redelivered.fill_id in engine.order_manager._synced_fills
    assert competitor.get_trade(trade_id)["exit_ts"] is None
    assert [
        row
        for row in competitor.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ] == []
    identity_faults = [
        row
        for row in competitor.get_events()
        if row["code"] == "KILL_LIFECYCLE_IDENTITY_MISSING"
    ]
    assert len(identity_faults) == 1
    assert "missing=trade_id" in str(identity_faults[0]["detail"])
    competitor.close()
    store.close()


@pytest.mark.parametrize(
    ("mutation", "expected_missing"),
    [("group_id", "group_id"), ("trade_row", "trade_row")],
)
def test_s3_r3_two_store_identity_invalidation_is_quarantined_not_raised(
    tmp_path, monkeypatch, mutation, expected_missing
):
    store, _broker, engine, _request, redelivered, trade_id, decision_uid = (
        _s3_stranded_kill_restart(tmp_path, monkeypatch)
    )
    competitor = Store(store.db_path)
    competitor.initialize(target_schema_version=9)
    assert competitor is not store
    original_totals = store.trade_fill_totals
    interleaved = []

    def invalidate_binding_after_initial_validation(target_trade_id):
        totals = original_totals(target_trade_id)
        if not interleaved:
            if mutation == "group_id":
                competitor.conn.execute(
                    "UPDATE orders SET group_id=NULL WHERE cloid=?",
                    (redelivered.cloid,),
                )
            else:
                competitor.conn.execute(
                    "DELETE FROM trades WHERE trade_id=?", (trade_id,)
                )
            competitor.conn.commit()
            interleaved.append(True)
        return totals

    monkeypatch.setattr(
        store, "trade_fill_totals", invalidate_binding_after_initial_validation
    )
    engine.order_manager._queue_event(redelivered)

    async def start_probe_and_stop():
        await engine.start(lookback=0)
        status = engine.status()
        with pytest.raises(RuntimeError, match="KILLED requires operator acknowledgement"):
            await engine.arm()
        with pytest.raises(RuntimeError, match="KILL_"):
            await engine.acknowledge_kill()
        await engine.stop()
        return status

    status = asyncio.run(start_probe_and_stop())

    assert interleaved, "the second Store must invalidate the binding after validation"
    assert engine.order_manager._queued_events == []
    assert engine.order_manager._deferred_kill_fills == {}
    assert redelivered.fill_id in engine.order_manager._synced_fills
    durable_trade = competitor.get_trade(trade_id)
    assert durable_trade is None or durable_trade["exit_ts"] is None
    assert [
        row
        for row in competitor.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ] == []
    identity_faults = [
        row
        for row in competitor.get_events()
        if row["code"] == "KILL_LIFECYCLE_IDENTITY_MISSING"
    ]
    assert len(identity_faults) == 1
    assert f"missing={expected_missing}" in str(identity_faults[0]["detail"])
    assert not [
        row
        for row in competitor.get_events()
        if row["code"] == "KILL_EPOCH_LIFECYCLE_DEFERRED"
    ]
    assert status["state"] == "KILLED"
    assert status["deferred_event_queue_depth"] == 0
    competitor.close()
    store.close()


@pytest.mark.parametrize(
    ("binding_element", "expected_fault"),
    [
        pytest.param(binding_element, expected_fault, id=binding_element)
        for binding_element, expected_fault in (
            KILL_LIFECYCLE_BINDING_FAULT_REASONS.items()
        )
    ],
)
def test_s3t_d_active_epoch_binding_mutation_matrix_is_quarantined(
    tmp_path, monkeypatch, binding_element, expected_fault
):
    """Each well-formed post-validation binding mutation is startup-contained."""
    store, _broker, engine, request, redelivered, trade_id, decision_uid = (
        _s3_stranded_kill_restart(tmp_path, monkeypatch)
    )
    epoch = _s3_open_epoch(
        store,
        request,
        process_uid=f"s3t-binding-{binding_element}",
        opened_ts_monotonic=10.0,
    )
    engine.order_manager._active_kill_epoch = epoch
    competitor = Store(store.db_path)
    competitor.initialize(target_schema_version=9)
    assert competitor is not store
    original_close = store.close_trade_once_with_decision
    interleaved: list[str] = []

    def invalidate_binding_before_close(**kwargs):
        if not interleaved:
            if binding_element == "orders.role":
                competitor.conn.execute(
                    "UPDATE orders SET role='CLOSE' WHERE cloid=?",
                    (redelivered.cloid,),
                )
            elif binding_element == "orders.group_id":
                competitor.conn.execute(
                    "UPDATE orders SET group_id=? WHERE cloid=?",
                    (f"{request['episode_id']}-other", redelivered.cloid),
                )
            elif binding_element == "orders.trade_id":
                competitor.conn.execute(
                    "UPDATE orders SET trade_id=? WHERE cloid=?",
                    (trade_id + 1000, redelivered.cloid),
                )
            elif binding_element == "orders.row":
                competitor.conn.execute(
                    "DELETE FROM orders WHERE cloid=?", (redelivered.cloid,)
                )
            else:  # pragma: no cover - registry growth must add a mutation above
                raise AssertionError(f"unhandled binding element: {binding_element}")
            competitor.conn.commit()
            interleaved.append(binding_element)
        return original_close(**kwargs)

    monkeypatch.setattr(
        store, "close_trade_once_with_decision", invalidate_binding_before_close
    )
    engine.order_manager._queue_event(redelivered)

    async def start_probe_and_stop():
        await engine.start(lookback=0)
        status = engine.status()
        with pytest.raises(
            RuntimeError, match="KILLED requires operator acknowledgement"
        ):
            await engine.arm()
        with pytest.raises(RuntimeError, match="KILL_"):
            await engine.acknowledge_kill()
        await engine.stop()
        return status

    status = asyncio.run(start_probe_and_stop())

    assert interleaved == [binding_element]
    assert engine.reconcile_ready is True
    evidence = [
        row
        for row in competitor.get_events()
        if row["code"] == "KILL_LIFECYCLE_IDENTITY_MISSING"
    ]
    assert any(expected_fault in str(row["detail"]) for row in evidence)
    assert status["state"] == "KILLED"
    assert competitor.get_meta("app_state") == "KILLED"
    assert competitor.get_trade(trade_id)["exit_ts"] is None
    assert [
        row
        for row in competitor.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ] == []
    assert engine.order_manager._queued_events == []
    assert engine.order_manager._deferred_kill_fills == {}
    assert redelivered.fill_id in engine.order_manager._synced_fills
    competitor.close()
    store.close()


_S3T_D_ACTIVE_EPOCH_EDGE_CASES = (
    pytest.param("stale_episode", id="stale-a-epoch-b-order"),
    pytest.param("aba_restore_after_veto", id="aba-restore-after-veto"),
)


@pytest.mark.parametrize("edge_case", _S3T_D_ACTIVE_EPOCH_EDGE_CASES)
def test_s3t_d_active_epoch_edge_case_matrix(tmp_path, monkeypatch, edge_case):
    store, _broker, engine, request, redelivered, trade_id, decision_uid = (
        _s3_stranded_kill_restart(tmp_path, monkeypatch)
    )
    manager = engine.order_manager
    original_episode = str(request["episode_id"])

    if edge_case == "stale_episode":
        # Retire only the old pointer so a real generation-A epoch can become
        # active while the well-formed generation-B order/request remain.
        store.conn.execute(
            "UPDATE kill_requests SET ack_state='ACKNOWLEDGED',ack_ts=? "
            "WHERE episode_id=?",
            (datetime.now(UTC).isoformat(), original_episode),
        )
        store.conn.execute(
            "DELETE FROM meta WHERE key IN ('kill_request_active','kill_epoch_active')"
        )
        store.conn.commit()
        active_request, active_epoch = store.open_kill_epoch(
            run_id=str(request["run_id"]),
            symbol=str(request["symbol"]),
            flatten_requested=bool(request["flatten_requested"]),
            policy_version=str(request["policy_version"]),
            process_uid="s3t-active-a-stale-b",
            opened_ts_monotonic=30.0,
            app_state_precommitted=True,
        )
        assert str(active_request["episode_id"]) != original_episode
        manager._active_kill_epoch = active_epoch

        assert manager._ingest_fill(redelivered) is True

        evidence = store.get_events()
        assert any(
            row["code"] == "KILL_LIFECYCLE_IDENTITY_MISSING"
            and "KILL_LIFECYCLE_GROUP_ID_CHANGED" in str(row["detail"])
            for row in evidence
        )
        assert not any(
            row["code"] == "KILL_EPOCH_LIFECYCLE_DEFERRED" for row in evidence
        )
        assert manager._deferred_kill_fills == {}
        assert redelivered.fill_id in manager._synced_fills
    else:
        assert edge_case == "aba_restore_after_veto"
        active_epoch = _s3_open_epoch(
            store,
            request,
            process_uid="s3t-active-aba-owner",
            opened_ts_monotonic=30.0,
        )
        manager._active_kill_epoch = active_epoch
        competitor = Store(store.db_path)
        competitor.initialize(target_schema_version=9)
        original_close = store.close_trade_once_with_decision
        transitions: list[str] = []

        def veto_then_restore_binding(**kwargs):
            competitor.conn.execute(
                "UPDATE orders SET group_id=? WHERE cloid=?",
                (f"{original_episode}-aba", redelivered.cloid),
            )
            competitor.conn.commit()
            transitions.append("changed")
            try:
                return original_close(**kwargs)
            except KillConflictError as exc:
                assert exc.reason_code == "KILL_LIFECYCLE_IDENTITY_MISSING"
                competitor.conn.execute(
                    "UPDATE orders SET group_id=? WHERE cloid=?",
                    (original_episode, redelivered.cloid),
                )
                competitor.conn.commit()
                transitions.append("restored")
                raise

        monkeypatch.setattr(
            store, "close_trade_once_with_decision", veto_then_restore_binding
        )

        assert manager._ingest_fill(redelivered) is False

        assert transitions == ["changed", "restored"]
        assert competitor.get_order(redelivered.cloid)["group_id"] == original_episode
        assert redelivered.fill_id in manager._deferred_kill_fills
        assert redelivered.fill_id not in manager._synced_fills
        deferred = [
            row
            for row in competitor.get_events()
            if row["code"] == "KILL_EPOCH_LIFECYCLE_DEFERRED"
        ]
        assert len(deferred) == 1
        assert "reason=KILL_LIFECYCLE_IDENTITY_MISSING" in str(
            deferred[0]["detail"]
        )
        competitor.close()

    durable_trade = store.get_trade(trade_id)
    assert durable_trade is not None
    assert durable_trade["exit_ts"] is None
    assert [
        row
        for row in store.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ] == []
    assert store.get_meta("app_state") == "KILLED"
    store.close()


def test_s3_r3_deferral_evidence_store_failure_still_propagates(
    tmp_path, monkeypatch
):
    store, _broker, engine, _request, redelivered, _trade_id, _decision_uid = (
        _s3_stranded_kill_restart(tmp_path, monkeypatch)
    )
    original_insert = store._insert_event_in_tx

    def fail_deferral_append(run_id, ts, severity, code, detail):
        if code == "KILL_EPOCH_LIFECYCLE_DEFERRED":
            raise RuntimeError("injected deferral evidence-store failure")
        return original_insert(run_id, ts, severity, code, detail)

    monkeypatch.setattr(store, "_insert_event_in_tx", fail_deferral_append)
    engine.order_manager._queue_event(redelivered)

    with pytest.raises(KillConflictError) as failure:
        asyncio.run(engine.start(lookback=0))

    assert failure.value.reason_code == "KILL_LIFECYCLE_DEFERRAL_RECORD_FAILED"
    assert engine.order_manager._queued_events == [redelivered]
    assert engine.order_manager._deferred_kill_fills == {}
    assert redelivered.fill_id not in engine.order_manager._synced_fills
    assert store.get_meta("app_state") == "KILLED"
    store.close()


_S3T_D_CORRUPTION_CASES = (
    pytest.param(None, "NULL", id="null"),
    pytest.param("not-a-number", "NON_NUMERIC_TEXT", id="non_numeric_text"),
    pytest.param(sqlite3.Binary(b"wrong-storage"), "STORAGE_CLASS", id="blob"),
    pytest.param(str(-(2**64)), "INT64_RANGE", id="int64_underflow"),
    pytest.param(str(2**64), "INT64_RANGE", id="int64_overflow"),
    # Python's sqlite3 adapter normalizes NaN to SQL NULL; the boundary must
    # still contain the schema-observed value rather than letting it escape.
    pytest.param(float("nan"), "NULL", id="nan_normalized_to_null"),
    pytest.param(float("inf"), "NON_FINITE", id="positive_infinity"),
    pytest.param(float("-inf"), "NON_FINITE", id="negative_infinity"),
)


@pytest.mark.parametrize(
    ("table", "column", "contract"),
    [
        pytest.param(table, column, contract, id=f"{table}.{column}")
        for (table, column), contract in DURABLE_EVENT_COLUMN_TYPES.items()
    ],
)
@pytest.mark.parametrize(("corrupt_value", "reason_case"), _S3T_D_CORRUPTION_CASES)
def test_s3t_d_registry_generated_durable_corruption_matrix(
    tmp_path,
    monkeypatch,
    table,
    column,
    contract,
    corrupt_value,
    reason_case,
):
    """Every registered queued-event durable read is startup-containable."""
    store, _broker, engine, _request, redelivered, trade_id, decision_uid = (
        _s3_stranded_kill_restart(tmp_path, monkeypatch)
    )
    if table == "trades":
        # Force the legacy durable-trade basis branch instead of the preferred
        # entry-fill aggregate branch so every registered trades column is read.
        store.conn.execute("DELETE FROM fills WHERE cloid='repair4-entry'")
        store.conn.commit()
    identity = {
        "orders": ("cloid", redelivered.cloid),
        "fills": ("fill_id", redelivered.fill_id),
        "trades": ("trade_id", trade_id),
    }[table]
    key_column, key_value = identity
    store.conn.execute(
        f"UPDATE {table} SET {column}=? WHERE {key_column}=?",
        (corrupt_value, key_value),
    )
    store.conn.commit()
    engine.order_manager._queue_event(redelivered)

    async def start_probe_and_stop():
        await engine.start(lookback=0)
        status = engine.status()
        with pytest.raises(
            RuntimeError, match="KILLED requires operator acknowledgement"
        ):
            await engine.arm()
        with pytest.raises(RuntimeError, match="KILL_"):
            await engine.acknowledge_kill()
        await engine.stop()
        return status

    status = asyncio.run(start_probe_and_stop())

    reason_code = f"DURABLE_{table}_{column}_{reason_case}".upper()
    evidence = store.get_events()
    null_is_accepted = contract.nullable and reason_case == "NULL"
    if null_is_accepted:
        assert not any(
            row["code"] == reason_code or reason_code in str(row["detail"])
            for row in evidence
        )
        if (table, column) == ("orders", "trade_id"):
            assert any(
                row["code"] == "KILL_LIFECYCLE_IDENTITY_MISSING"
                and "missing=trade_id" in str(row["detail"])
                for row in evidence
            )
            assert engine.order_manager._queued_events == []
            assert engine.order_manager._deferred_kill_fills == {}
            assert redelivered.fill_id in engine.order_manager._synced_fills
        else:
            assert (table, column) == ("trades", "entry_px")
            assert any(
                row["code"] == "KILL_EPOCH_LIFECYCLE_DEFERRED"
                and "reason=KILL_EPOCH_REQUIRED" in str(row["detail"])
                for row in evidence
            )
            assert engine.order_manager._queued_events == [redelivered]
            assert redelivered.fill_id in engine.order_manager._deferred_kill_fills
            assert redelivered.fill_id not in engine.order_manager._synced_fills
    else:
        assert any(
            row["code"] == reason_code or reason_code in str(row["detail"])
            for row in evidence
        )
        assert engine.order_manager._queued_events == []
        assert engine.order_manager._deferred_kill_fills == {}
        assert redelivered.fill_id in engine.order_manager._synced_fills
    assert status["state"] == "KILLED"
    assert store.get_meta("app_state") == "KILLED"
    assert store.get_trade(trade_id)["exit_ts"] is None
    assert [
        row
        for row in store.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ] == []
    store.close()


def test_s3t_d_nullable_entry_px_uses_expected_px_basis_in_active_epoch(
    tmp_path, monkeypatch
):
    store, _broker, engine, request, redelivered, trade_id, decision_uid = (
        _s3_stranded_kill_restart(tmp_path, monkeypatch)
    )
    contract = DURABLE_EVENT_COLUMN_TYPES[("trades", "entry_px")]
    assert contract.nullable is True
    store.conn.execute("DELETE FROM fills WHERE cloid='repair4-entry'")
    store.conn.commit()
    before = store.get_trade(trade_id)
    assert before is not None
    assert before["entry_px"] is None
    assert before["expected_px"] == 100.0
    epoch = _s3_open_epoch(
        store,
        request,
        process_uid="s3t-nullable-entry-basis",
        opened_ts_monotonic=20.0,
    )
    engine.order_manager._active_kill_epoch = epoch

    assert engine.order_manager._ingest_fill(redelivered) is True

    closed = store.get_trade(trade_id)
    assert closed is not None
    assert closed["exit_reason"] == "KILL_FLATTEN"
    decisions = [
        row
        for row in store.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ]
    assert len(decisions) == 1
    assert decisions[0]["payload"]["entry_basis_px"] == before["expected_px"]
    assert not any(
        row["code"] == "DURABLE_TRADES_ENTRY_PX_NULL"
        for row in store.get_events()
    )
    store.close()


def test_s3t_c_event_symbol_contains_int64_overflow_at_startup(tmp_path):
    store, _broker, engine = _repair4_kill_engine(tmp_path)
    trade = store.get_open_trade_for_coin("repair4-kill", "BTC")
    assert trade is not None
    trade_id = int(trade["trade_id"])
    store.conn.execute(
        "UPDATE orders SET trade_id=? WHERE cloid='repair4-sl'", (str(2**64),)
    )
    store.conn.commit()
    event = OrderUpdateEvent(
        cloid="repair4-sl",
        status="OPEN",
        ts=datetime.now(UTC),
    )
    engine.order_manager._queue_event(event)

    async def start_probe_and_stop():
        await engine.start(lookback=0)
        with pytest.raises(
            RuntimeError, match="KILLED requires operator acknowledgement"
        ):
            await engine.arm()
        with pytest.raises(RuntimeError, match="KILL_"):
            await engine.acknowledge_kill()
        await engine.stop()

    asyncio.run(start_probe_and_stop())

    reason_code = "DURABLE_ORDERS_TRADE_ID_INT64_RANGE"
    evidence = [row for row in store.get_events() if row["code"] == reason_code]
    assert evidence
    assert engine.order_manager._queued_events == []
    assert engine.order_manager._deferred_kill_fills == {}
    assert store.get_meta("app_state") == "KILLED"
    assert store.get_trade(trade_id)["exit_ts"] is None
    store.close()


def test_s2_closure_stale_recovery_cannot_commit_after_epoch_invalidation(
    tmp_path, monkeypatch
):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    db_path = store.db_path
    trade = store.get_open_trade_for_coin("repair4-kill", "BTC")
    assert trade is not None
    trade_id = int(trade["trade_id"])
    decision_uid = str(trade["entry_decision_uid"])

    def crash_after_coupled_flatten_commit(_fill):
        raise RuntimeError("INJECTED_AFTER_APPLIED_FLATTEN_COMMIT")

    monkeypatch.setattr(
        engine.order_manager, "_ingest_fill", crash_after_coupled_flatten_commit
    )
    with pytest.raises(
        RuntimeError, match="INJECTED_AFTER_APPLIED_FLATTEN_COMMIT"
    ):
        asyncio.run(engine.kill(flatten=True))

    request = store.active_kill_request()
    assert request is not None
    flatten_action = store.kill_actions_for_episode(
        request["episode_id"], kind="FLATTEN"
    )[0]
    assert flatten_action["current_outcome"] == "APPLIED"
    assert len(store.list_fills_for_order(flatten_action["cloid"])) == 1
    assert store.get_trade(trade_id)["exit_ts"] is None

    broker._user_callbacks.clear()
    store.close()
    recovery_store = Store(db_path)
    recovery_store.initialize(target_schema_version=9)
    recovery_engine = BridgeEngine(
        run_id="repair4-kill",
        broker=broker,
        store=recovery_store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
        state="KILLED",
    )
    competitor = Store(db_path)
    competitor.initialize(target_schema_version=9)
    assert competitor is not recovery_store
    original_ingest = recovery_engine.order_manager._ingest_fill
    invalidations = []

    def invalidate_epoch_then_ingest(fill):
        active_epoch = recovery_engine.order_manager._active_kill_epoch
        assert active_epoch is not None
        current = competitor.active_kill_request()
        assert current is not None
        _request, newer_epoch = competitor.open_kill_epoch(
            run_id=str(current["run_id"]),
            symbol=str(current["symbol"]),
            flatten_requested=bool(current["flatten_requested"]),
            policy_version=str(current["policy_version"]),
            process_uid="s2-closure-competing-owner",
            opened_ts_monotonic=active_epoch.opened_ts_monotonic + 1.0,
        )
        invalidations.append((active_epoch, newer_epoch))
        return original_ingest(fill)

    monkeypatch.setattr(
        recovery_engine.order_manager,
        "_ingest_fill",
        invalidate_epoch_then_ingest,
    )

    with pytest.raises(KillConflictError, match="KILL_EPOCH_STALE_WRITE"):
        asyncio.run(recovery_engine.kill(flatten=True))

    assert len(invalidations) == 1
    assert invalidations[0][1].attempt_no == invalidations[0][0].attempt_no + 1
    durable_trade = competitor.get_trade(trade_id)
    assert durable_trade is not None
    assert durable_trade["exit_ts"] is None
    assert [
        row
        for row in competitor.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ] == []
    competitor.close()
    recovery_store.close()


def test_s2_closure_live_flatten_cannot_commit_after_epoch_invalidation(
    tmp_path, monkeypatch
):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    trade = store.get_open_trade_for_coin("repair4-kill", "BTC")
    assert trade is not None
    trade_id = int(trade["trade_id"])
    decision_uid = str(trade["entry_decision_uid"])
    competitor = Store(store.db_path)
    competitor.initialize(target_schema_version=9)
    assert competitor is not store
    original_ingest = engine.order_manager._ingest_fill
    invalidations = []

    def invalidate_epoch_then_ingest(fill):
        active_epoch = engine.order_manager._active_kill_epoch
        assert active_epoch is not None
        current = competitor.active_kill_request()
        assert current is not None
        _request, newer_epoch = competitor.open_kill_epoch(
            run_id=str(current["run_id"]),
            symbol=str(current["symbol"]),
            flatten_requested=bool(current["flatten_requested"]),
            policy_version=str(current["policy_version"]),
            process_uid="s2-closure-live-competing-owner",
            opened_ts_monotonic=active_epoch.opened_ts_monotonic + 1.0,
        )
        invalidations.append((active_epoch, newer_epoch))
        return original_ingest(fill)

    monkeypatch.setattr(
        engine.order_manager,
        "_ingest_fill",
        invalidate_epoch_then_ingest,
    )

    with pytest.raises(KillConflictError, match="KILL_EPOCH_STALE_WRITE"):
        asyncio.run(engine.kill(flatten=True))

    assert len(invalidations) == 1
    assert invalidations[0][1].attempt_no == invalidations[0][0].attempt_no + 1
    flatten_action = competitor.kill_actions_for_episode(
        competitor.active_kill_request()["episode_id"], kind="FLATTEN"
    )[0]
    assert flatten_action["current_outcome"] == "APPLIED"
    assert len(competitor.list_fills_for_order(flatten_action["cloid"])) == 1
    durable_trade = competitor.get_trade(trade_id)
    assert durable_trade is not None
    assert durable_trade["exit_ts"] is None
    assert [
        row
        for row in competitor.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ] == []
    competitor.close()
    store.close()


def test_s2_a5_multifill_crash_restart_recovers_final_aggregate_once(
    tmp_path, monkeypatch
):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    db_path = store.db_path
    trade = store.get_open_trade_for_coin("repair4-kill", "BTC")
    assert trade is not None
    trade_id = int(trade["trade_id"])
    decision_uid = str(trade["entry_decision_uid"])
    store.conn.execute(
        "UPDATE fills SET fee=?,funding=? WHERE fill_id=?",
        (0.1, 0.05, "repair4-owned-fill"),
    )
    store.conn.commit()

    first_fill_ts = datetime.now(UTC)
    final_fill_ts = first_fill_ts + timedelta(milliseconds=1)

    def split_reduce_position(symbol, size, cloid):
        current = float(broker.position.size)
        close = broker._order(
            "CLOSE",
            "FILLED",
            float(size),
            100.8,
            reduce_only=True,
            symbol=symbol,
            cloid=str(cloid),
            direction="LONG" if current > 0 else "SHORT",
        )
        broker._record_fill(close, 0.4, 99.0, first_fill_ts)
        broker._record_fill(close, 0.6, 102.0, final_fill_ts)
        broker.position = None
        broker.full_positions = []

    monkeypatch.setattr(broker, "_reduce_position", split_reduce_position)
    original_fills_evidence = broker.fills_evidence

    async def fills_evidence_with_costs(*, start_ms, end_ms):
        evidence = await original_fills_evidence(
            start_ms=start_ms, end_ms=end_ms
        )
        rows = []
        for raw in evidence.rows:
            row = dict(raw)
            if row.get("side") == "SELL" and row.get("px") == 99.0:
                row.update(fee=0.2, funding=-0.02)
            elif row.get("side") == "SELL" and row.get("px") == 102.0:
                row.update(fee=0.3, funding=0.04)
            rows.append(row)
        return replace(evidence, rows=tuple(rows))

    monkeypatch.setattr(broker, "fills_evidence", fills_evidence_with_costs)

    def crash_after_coupled_flatten_commit(_fill):
        action = store.kill_actions_for_episode(
            store.active_kill_request()["episode_id"], kind="FLATTEN"
        )[0]
        assert action["current_outcome"] == "APPLIED"
        assert len(store.list_fills_for_order(action["cloid"])) == 2
        assert store.get_trade(trade_id)["exit_ts"] is None
        raise RuntimeError("INJECTED_AFTER_MULTIFILL_APPLIED_COMMIT")

    monkeypatch.setattr(
        engine.order_manager, "_ingest_fill", crash_after_coupled_flatten_commit
    )
    with pytest.raises(
        RuntimeError, match="INJECTED_AFTER_MULTIFILL_APPLIED_COMMIT"
    ):
        asyncio.run(engine.kill(flatten=True))

    request = store.active_kill_request()
    assert request is not None
    flatten_action = store.kill_actions_for_episode(
        request["episode_id"], kind="FLATTEN"
    )[0]
    durable_fills = store.list_fills_for_order(flatten_action["cloid"])
    assert [(row["qty"], row["px"]) for row in durable_fills] == [
        (0.4, 99.0),
        (0.6, 102.0),
    ]
    expected_exit_ts = durable_fills[-1]["fill_ts"]
    expected_costs = 0.1 + 0.05 + 0.2 - 0.02 + 0.3 + 0.04
    expected_gross = (100.8 - 100.0) * 1.0
    expected_pnl = expected_gross - expected_costs

    broker._user_callbacks.clear()
    store.close()
    restarted_store = Store(db_path)
    restarted_store.initialize(target_schema_version=9)
    restarted_engine = BridgeEngine(
        run_id="repair4-kill",
        broker=broker,
        store=restarted_store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
        state="KILLED",
    )

    asyncio.run(restarted_engine.kill(flatten=True))

    recovered_request = restarted_store.active_kill_request()
    recovered_trade = restarted_store.get_trade(trade_id)
    assert recovered_request is not None
    assert recovered_request["terminal_state"] == "SAFE_FLAT"
    assert recovered_trade is not None
    assert recovered_trade["exit_ts"] == expected_exit_ts
    assert recovered_trade["exit_px"] == pytest.approx(100.8)
    assert recovered_trade["exit_reason"] == "KILL_FLATTEN"
    assert recovered_trade["pnl"] == pytest.approx(expected_pnl)
    close_decisions = [
        row
        for row in restarted_store.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ]
    assert len(close_decisions) == 1
    close_decision = close_decisions[0]
    assert close_decision["ts"] == expected_exit_ts
    assert close_decision["run_id"] == "repair4-kill"
    assert close_decision["coin"] == "BTC"
    assert close_decision["trade_id"] == trade_id
    assert close_decision["payload"] == pytest.approx(
        {
            "exit_reason": "KILL_FLATTEN",
            "pnl": expected_pnl,
            "pnl_gross": expected_gross,
            "costs": expected_costs,
            "entry_basis_px": 100.0,
            "exit_vwap": 100.8,
            "qty": 1.0,
        }
    )
    immutable_counts = {
        "actions": len(
            restarted_store.kill_actions_for_episode(request["episode_id"])
        ),
        "action_events": len(
            restarted_store.kill_action_events(flatten_action["action_id"])
        ),
        "fills": len(restarted_store.list_all_fills()),
        "orders": len(restarted_store.get_orders_for_trade(trade_id)),
        "close_decisions": len(close_decisions),
    }

    asyncio.run(restarted_engine.kill(flatten=True))
    assert {
        "actions": len(
            restarted_store.kill_actions_for_episode(request["episode_id"])
        ),
        "action_events": len(
            restarted_store.kill_action_events(flatten_action["action_id"])
        ),
        "fills": len(restarted_store.list_all_fills()),
        "orders": len(restarted_store.get_orders_for_trade(trade_id)),
        "close_decisions": len(
            [
                row
                for row in restarted_store.get_decision_chain(decision_uid)
                if row["stage"] == "TRADE_CLOSED"
            ]
        ),
    } == immutable_counts

    broker._user_callbacks.clear()
    restarted_store.close()
    replay_store = Store(db_path)
    replay_store.initialize(target_schema_version=9)
    replay_engine = BridgeEngine(
        run_id="repair4-kill",
        broker=broker,
        store=replay_store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
        state="KILLED",
    )
    asyncio.run(replay_engine.kill(flatten=True))
    assert {
        "actions": len(replay_store.kill_actions_for_episode(request["episode_id"])),
        "action_events": len(
            replay_store.kill_action_events(flatten_action["action_id"])
        ),
        "fills": len(replay_store.list_all_fills()),
        "orders": len(replay_store.get_orders_for_trade(trade_id)),
        "close_decisions": len(
            [
                row
                for row in replay_store.get_decision_chain(decision_uid)
                if row["stage"] == "TRADE_CLOSED"
            ]
        ),
    } == immutable_counts


def test_s2_a5_ack_rejects_stranded_applied_flatten_open_trade(tmp_path, monkeypatch):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    db_path = store.db_path
    trade = store.get_open_trade_for_coin("repair4-kill", "BTC")
    assert trade is not None
    trade_id = int(trade["trade_id"])

    def crash_after_coupled_flatten_commit(_fill):
        raise RuntimeError("INJECTED_AFTER_APPLIED_FLATTEN_COMMIT")

    monkeypatch.setattr(
        engine.order_manager, "_ingest_fill", crash_after_coupled_flatten_commit
    )
    with pytest.raises(
        RuntimeError, match="INJECTED_AFTER_APPLIED_FLATTEN_COMMIT"
    ):
        asyncio.run(engine.kill(flatten=True))

    broker._user_callbacks.clear()
    store.close()
    stranded_store = Store(db_path)
    stranded_store.initialize(target_schema_version=9)
    stranded_engine = BridgeEngine(
        run_id="repair4-kill",
        broker=broker,
        store=stranded_store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
        state="KILLED",
    )
    monkeypatch.setattr(
        stranded_engine.order_manager,
        "_recover_applied_kill_flatten_lifecycles",
        lambda **_kwargs: None,
        raising=False,
    )

    asyncio.run(stranded_engine.kill(flatten=True))

    request = stranded_store.active_kill_request()
    assert request is not None
    assert request["terminal_state"] == "SAFE_FLAT"
    assert request["safe_checkpoint_id"] is not None
    assert stranded_store.get_trade(trade_id)["exit_ts"] is None
    with pytest.raises(RuntimeError, match="KILL_FLATTEN_TRADE_OPEN"):
        asyncio.run(stranded_engine.acknowledge_kill())
    rejected = stranded_store.get_kill_request(request["episode_id"])
    assert rejected is not None
    assert rejected["ack_state"] == "PENDING"
    assert stranded_store.get_meta("app_state") == "KILLED"


def test_s2_a5_ack_rejects_inconsistent_closed_flatten_lifecycle(
    tmp_path, monkeypatch
):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    db_path = store.db_path
    trade = store.get_open_trade_for_coin("repair4-kill", "BTC")
    assert trade is not None
    trade_id = int(trade["trade_id"])
    decision_uid = str(trade["entry_decision_uid"])

    def crash_after_coupled_flatten_commit(_fill):
        raise RuntimeError("INJECTED_AFTER_APPLIED_FLATTEN_COMMIT")

    monkeypatch.setattr(
        engine.order_manager, "_ingest_fill", crash_after_coupled_flatten_commit
    )
    with pytest.raises(
        RuntimeError, match="INJECTED_AFTER_APPLIED_FLATTEN_COMMIT"
    ):
        asyncio.run(engine.kill(flatten=True))

    broker._user_callbacks.clear()
    store.close()
    inconsistent_store = Store(db_path)
    inconsistent_store.initialize(target_schema_version=9)
    inconsistent_engine = BridgeEngine(
        run_id="repair4-kill",
        broker=broker,
        store=inconsistent_store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
        state="KILLED",
    )
    monkeypatch.setattr(
        inconsistent_engine.order_manager,
        "_recover_applied_kill_flatten_lifecycles",
        lambda **_kwargs: None,
        raising=False,
    )
    asyncio.run(inconsistent_engine.kill(flatten=True))

    request = inconsistent_store.active_kill_request()
    assert request is not None
    assert request["terminal_state"] == "SAFE_FLAT"
    flatten_action = inconsistent_store.kill_actions_for_episode(
        request["episode_id"], kind="FLATTEN"
    )[0]
    durable_fill = inconsistent_store.list_fills_for_order(
        flatten_action["cloid"]
    )[0]
    inconsistent_exit_ts = (
        datetime.fromisoformat(durable_fill["fill_ts"]) + timedelta(seconds=1)
    ).isoformat()
    inconsistent_store.conn.execute(
        """UPDATE trades
           SET exit_ts=?,exit_px=?,exit_reason='KILL_FLATTEN',pnl=?
           WHERE trade_id=?""",
        (inconsistent_exit_ts, 877.0, 123456.0, trade_id),
    )
    inconsistent_store.conn.commit()
    assert [
        row
        for row in inconsistent_store.get_decision_chain(decision_uid)
        if row["stage"] == "TRADE_CLOSED"
    ] == []

    with pytest.raises(RuntimeError, match="KILL_FLATTEN_LIFECYCLE_CONFLICT"):
        asyncio.run(inconsistent_engine.acknowledge_kill())

    rejected = inconsistent_store.get_kill_request(request["episode_id"])
    assert rejected is not None
    assert rejected["ack_state"] == "PENDING"
    assert inconsistent_store.get_meta("app_state") == "KILLED"
    assert inconsistent_engine.state == "KILLED"


@pytest.mark.parametrize(
    ("column", "invalid_value"),
    [("fee", None), ("funding", float("inf"))],
)
def test_s2_a5_restart_types_invalid_durable_flatten_costs_as_fill_conflict(
    tmp_path, monkeypatch, column, invalid_value
):
    store, broker, engine = _repair4_kill_engine(tmp_path)
    db_path = store.db_path

    def crash_after_coupled_flatten_commit(_fill):
        raise RuntimeError("INJECTED_AFTER_APPLIED_FLATTEN_COMMIT")

    monkeypatch.setattr(
        engine.order_manager, "_ingest_fill", crash_after_coupled_flatten_commit
    )
    with pytest.raises(
        RuntimeError, match="INJECTED_AFTER_APPLIED_FLATTEN_COMMIT"
    ):
        asyncio.run(engine.kill(flatten=True))

    request = store.active_kill_request()
    assert request is not None
    flatten_action = store.kill_actions_for_episode(
        request["episode_id"], kind="FLATTEN"
    )[0]
    durable_fill = store.list_fills_for_order(flatten_action["cloid"])[0]
    store.conn.execute(
        f"UPDATE fills SET {column}=? WHERE fill_id=?",
        (invalid_value, durable_fill["fill_id"]),
    )
    store.conn.commit()

    broker._user_callbacks.clear()
    store.close()
    restarted_store = Store(db_path)
    restarted_store.initialize(target_schema_version=9)
    restarted_engine = BridgeEngine(
        run_id="repair4-kill",
        broker=broker,
        store=restarted_store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
        state="KILLED",
    )

    asyncio.run(restarted_engine.kill(flatten=True))

    conflicted = restarted_store.active_kill_request()
    assert conflicted is not None
    assert conflicted["terminal_state"] == "AMBIGUOUS"
    assert conflicted["terminal_reason"] == "KILL_FLATTEN_FILL_CONFLICT"
    assert conflicted["ack_state"] == "PENDING"
    assert restarted_store.get_meta("app_state") == "KILLED"


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


class PausingKillGuardBroker(MockBroker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entered = asyncio.Event()
        self.resume = asyncio.Event()

    async def place_bracket(self, plan, *, pre_send_guard=None):
        self.entered.set()
        await self.resume.wait()
        return await super().place_bracket(plan, pre_send_guard=pre_send_guard)


def test_kill_latch_at_paused_write_boundary_vetoes_new_bracket(tmp_path):
    async def run() -> None:
        store = Store(tmp_path / "kill-write-guard.db")
        store.initialize()
        store.create_run("guard-run", "dry_run", "testnet", {})
        store.set_meta("app_state", "ARMED")
        now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
        bars = [
            Bar(ts=now - timedelta(minutes=1), open=100, high=101, low=99, close=100, volume=1),
            Bar(ts=now, open=100, high=101, low=99, close=100, volume=1),
        ]
        broker = PausingKillGuardBroker(bars=bars)
        broker.connected = True
        manager = OrderManager(store, broker, "guard-run")
        plan = OrderPlan(
            signal=Signal(ts=now, symbol="BTC", direction="LONG", reason="test", ref_price=100),
            qty=0.1, entry_type="MKT", stop_loss=95.0,
        )
        task = asyncio.create_task(manager.submit_plan("guard-decision", plan))
        await broker.entered.wait()
        manager.kill_latched = True
        store.set_meta("app_state", "KILLED")
        broker.resume.set()
        with pytest.raises(SubmissionRejectedError):
            await task
        assert broker.orders == []
        assert store.get_quarantined_submission_attempts() == []
        attempt = store.get_snapshot()["submission_attempts"][0]
        assert attempt["state"] == "PRE_SEND_FAILURE"
        assert attempt["state"] != "UNKNOWN_SUBMISSION"

    asyncio.run(run())


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
