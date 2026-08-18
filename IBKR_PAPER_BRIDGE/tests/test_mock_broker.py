from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from pathlib import Path

from bridge.broker.mock import MockBroker
from bridge.engine.types import Bar, OrderPlan, Signal


def test_mock_broker_market_fill_and_sl_priority(tmp_path):
    asyncio.run(_run_market_fill_and_sl_priority())


async def _run_market_fill_and_sl_priority():
    bars = [
        Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=101, low=99, close=100, volume=1),
        Bar(ts=datetime(2026, 7, 6, 1, tzinfo=UTC), open=101, high=110, low=94, close=105, volume=1),
    ]
    broker = MockBroker(bars=bars, starting_equity=1000)
    await broker.connect()

    signal = Signal(
        ts=bars[0].ts,
        symbol="BTC",
        direction="LONG",
        reason="test",
        ref_price=100,
    )
    plan = OrderPlan(
        signal=signal,
        qty=0.1,
        entry_type="MKT",
        stop_loss=95,
        take_profit=108,
        leverage=1,
        risk_dollars=0.5,
        risk_pct=0.001,
    )

    ids = await broker.place_bracket(plan)
    assert ids["entry"]["status"] == "OPEN"

    broker.process_bar(bars[1])

    assert ids["entry"]["avg_fill_px"] == 101
    assert ids["sl"]["status"] == "FILLED"
    assert ids["sl"]["role"] == "SL"
    assert ids["sl"]["avg_fill_px"] == 95
    assert await broker.positions() == []


def test_mock_broker_loads_fixture():
    broker = MockBroker.from_csv(Path(__file__).parent / "fixtures" / "BTC_1h.csv")

    assert len(broker.bars) >= 2000
    assert broker.coin == "BTC"


# ===========================================================================
# TS-P1-004 typed partial-recovery surface + fault injection contract
# ===========================================================================

import pytest  # noqa: E402

from bridge.broker.mock import ScriptedOutcome  # noqa: E402
from bridge.engine.types import (  # noqa: E402
    ActionOutcome,
    LotUnit,
    Position,
    SymbolSnapshot,
)


def _broker_with_position() -> MockBroker:
    broker = MockBroker(bars=[], starting_equity=1000.0)
    broker.orders.append({
        "cloid": "entry-1", "oid": 1, "role": "ENTRY", "status": "OPEN",
        "qty": 2.0, "avg_fill_px": 100.0, "reduce_only": False,
        "symbol": "BTC", "direction": "LONG",
    })
    broker.position = Position(symbol="BTC", size=1.0, entry_px=100.0)
    return broker


def test_mock_exposes_the_full_partial_recovery_surface():
    broker = MockBroker(bars=[])
    for name in (
        "lot_unit", "symbol_snapshot", "query_order", "cancel_order_by_cloid",
        "place_protective_stop", "flatten_reduce_only",
    ):
        assert callable(getattr(broker, name))


def test_mock_lot_unit_is_fixture_driven_and_fail_closed():
    broker = MockBroker(bars=[])
    assert broker.lot_unit("BTC") == LotUnit(3)
    broker.partial_size_decimals = None
    assert broker.lot_unit("BTC") is None


def test_mock_snapshot_reports_position_and_live_orders():
    broker = _broker_with_position()
    snapshot = asyncio.run(broker.symbol_snapshot("BTC"))
    assert isinstance(snapshot, SymbolSnapshot)
    assert snapshot.exact is True
    assert snapshot.net_size == 1.0
    assert [o.cloid for o in snapshot.open_orders] == ["entry-1"]


def test_mock_snapshot_is_inexact_when_unavailable_or_quantum_missing():
    broker = _broker_with_position()
    broker.partial_snapshot_available = False
    assert asyncio.run(broker.symbol_snapshot("BTC")).exact is False

    broker.partial_snapshot_available = True
    broker.partial_size_decimals = None
    snapshot = asyncio.run(broker.symbol_snapshot("BTC"))
    assert snapshot.exact is False and snapshot.lot is None


def test_mock_foreign_orders_appear_in_the_snapshot():
    broker = _broker_with_position()
    broker.partial_foreign_orders.append({
        "cloid": "manual", "role": "SL", "status": "OPEN", "qty": 1.0,
        "symbol": "BTC", "direction": "LONG", "reduce_only": True,
    })
    snapshot = asyncio.run(broker.symbol_snapshot("BTC"))
    assert "manual" in {o.cloid for o in snapshot.open_orders}


def test_mock_query_order_is_unknown_when_unavailable():
    broker = _broker_with_position()
    broker.partial_query_available = False
    result = asyncio.run(broker.query_order("entry-1", "BTC"))
    assert result.known is False


def test_mock_query_order_reports_live_then_terminal():
    broker = _broker_with_position()
    live = asyncio.run(broker.query_order("entry-1", "BTC"))
    assert live.known and live.found and not live.terminal

    asyncio.run(broker.cancel_order_by_cloid("entry-1", "BTC"))
    dead = asyncio.run(broker.query_order("entry-1", "BTC"))
    assert dead.known and not dead.found and dead.terminal


def test_mock_cancel_of_absent_or_terminal_order_is_proven_not_applied():
    broker = _broker_with_position()
    absent = asyncio.run(broker.cancel_order_by_cloid("nope", "BTC"))
    assert absent.outcome is ActionOutcome.NOT_APPLIED

    asyncio.run(broker.cancel_order_by_cloid("entry-1", "BTC"))
    again = asyncio.run(broker.cancel_order_by_cloid("entry-1", "BTC"))
    assert again.outcome is ActionOutcome.NOT_APPLIED


@pytest.mark.parametrize("applied", [True, False])
def test_mock_scripted_outcome_separates_report_from_effect(applied):
    broker = _broker_with_position()
    broker.scripted_place.append(
        ScriptedOutcome(ActionOutcome.UNKNOWN, applied=applied)
    )
    result = asyncio.run(
        broker.place_protective_stop(
            symbol="BTC", cloid="0xstop", exit_side="SELL", size=1.0, trigger_px=95.0
        )
    )
    assert result.outcome is ActionOutcome.UNKNOWN
    installed = [o for o in broker.orders if o["cloid"] == "0xstop"]
    assert bool(installed) is applied


def test_mock_installed_stop_is_reduce_only_and_opposite_side():
    broker = _broker_with_position()
    asyncio.run(
        broker.place_protective_stop(
            symbol="BTC", cloid="0xstop", exit_side="SELL", size=1.0, trigger_px=95.0
        )
    )
    snapshot = asyncio.run(broker.symbol_snapshot("BTC"))
    stop = next(o for o in snapshot.open_orders if o.cloid == "0xstop")
    assert stop.role == "SL" and stop.reduce_only is True and stop.side == "SELL"


def test_mock_flatten_reduces_only_the_requested_size():
    broker = _broker_with_position()
    broker.position = Position(symbol="BTC", size=2.0, entry_px=100.0)
    asyncio.run(broker.flatten_reduce_only(symbol="BTC", cloid="0xflat", size=1.0))
    assert broker.position.size == 1.0
    asyncio.run(broker.flatten_reduce_only(symbol="BTC", cloid="0xflat2", size=1.0))
    assert broker.position is None


def test_mock_late_fill_on_cancel_changes_the_position():
    broker = _broker_with_position()
    broker.late_entry_fill_on_cancel = 0.5
    asyncio.run(broker.cancel_order_by_cloid("entry-1", "BTC"))
    assert broker.position.size == 1.5
    assert broker.late_entry_fill_on_cancel == 0.0


def test_mock_records_only_mutating_calls_in_broker_mutations():
    broker = _broker_with_position()
    asyncio.run(broker.symbol_snapshot("BTC"))
    asyncio.run(broker.query_order("entry-1", "BTC"))
    assert broker.broker_mutations == []
    asyncio.run(broker.cancel_order_by_cloid("entry-1", "BTC"))
    assert broker.broker_mutations == [("cancel_order_by_cloid", "entry-1")]


def test_mock_legacy_surface_is_unchanged():
    broker = _broker_with_position()
    assert callable(broker.cancel)
    assert callable(broker.flatten)
    assert callable(broker.reprotect_position)
    asyncio.run(broker.flatten("BTC"))
    assert broker.position is None
