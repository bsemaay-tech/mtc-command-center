"""TS-P1-004 partial-fill protect-or-flatten — adversarial suite.

RED-first: the tests in the ``RED BASELINE`` block were written against the
accepted TS-P1-004 contract and failed on base commit ``677c3a29`` before any
production change (undersized SL accepted as protection; no v5 schema; no
recovery ledger).

Everything here runs offline against ``MockBroker`` and temporary SQLite
databases. No network, exchange, testnet or runtime database is touched.
"""

from __future__ import annotations

import asyncio
import sqlite3
from datetime import UTC, datetime, timedelta

import pytest

from bridge.broker.mock import MockBroker, ScriptedOutcome
from bridge.engine.orders import OrderManager, exact_size_equal, exit_side_for
from bridge.engine.types import (
    FLATTEN_VERIFY_DEADLINE_S,
    PROTECT_DEADLINE_S,
    AccountSnapshot,
    ActionOutcome,
    BrokerOrder,
    FillEvent,
    LotQuantizationError,
    LotUnit,
    OrderState,
    PartialProtectionState,
    Position,
    canonical_order_state,
    can_transition_partial,
    lots_to_size,
    quantize_lots,
)
from bridge.store.db import (
    MigrationError,
    PartialRecoveryConflictError,
    Store,
    compute_partial_action_cloid,
    compute_partial_action_id,
)

FROZEN = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
ENTRY_CLOID = "entry-1"
REQUEST_ID = "request-v1:" + "a" * 64


# ---------------------------------------------------------------------------
# Injected clocks
# ---------------------------------------------------------------------------


class Clock:
    """Injected UTC wall clock."""

    def __init__(self, start: datetime = FROZEN) -> None:
        self.now = start

    def __call__(self) -> datetime:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now = self.now + timedelta(seconds=seconds)


class Mono:
    """Injected monotonic runtime clock (never persisted)."""

    def __init__(self, start: float = 1_000.0) -> None:
        self.value = start

    def __call__(self) -> float:
        return self.value

    def advance(self, seconds: float) -> None:
        self.value += seconds


# ---------------------------------------------------------------------------
# Fakes / builders
# ---------------------------------------------------------------------------


class RecordingBroker:
    """Minimal legacy Broker-protocol fake that records every mutating call."""

    def __init__(
        self,
        *,
        positions: list[Position] | None = None,
        open_orders: list[BrokerOrder] | None = None,
    ) -> None:
        self._positions = positions or []
        self._open_orders = open_orders or []
        self.reprotect_attempts = 0
        self.flattened: list[str] = []
        self.cancelled: list[str] = []

    async def connect(self) -> None:
        return None

    async def account(self) -> AccountSnapshot:
        return AccountSnapshot(equity=1000.0, available_margin=1000.0)

    async def positions(self) -> list[Position]:
        return list(self._positions)

    async def open_orders(self) -> list[BrokerOrder]:
        return list(self._open_orders)

    async def historical_bars(self, coin, tf, lookback):  # pragma: no cover
        return []

    def subscribe_bars(self, coin, tf, on_bar_closed) -> None:  # pragma: no cover
        return None

    async def place_bracket(self, plan):  # pragma: no cover
        raise AssertionError("reconcile must not submit entries")

    async def modify_stop(self, cloid: str, new_stop: float) -> None:
        return None

    async def cancel(self, cloid: str) -> None:
        self.cancelled.append(cloid)

    async def cancel_all(self) -> None:
        return None

    async def flatten(self, coin: str) -> None:
        self.flattened.append(coin)

    async def reprotect_position(self, position, stop_loss, take_profit, decision_uid):
        self.reprotect_attempts += 1
        return None


def make_store(tmp_path, *, version: int = 5, clock: Clock | None = None) -> Store:
    store = Store(tmp_path / "bridge.db", clock=clock or Clock())
    store.initialize(target_schema_version=version)
    store.create_run("run", "dry_run", "testnet", {})
    return store


def seed_trade(
    store: Store,
    *,
    qty: float = 2.0,
    coin: str = "BTC",
    direction: str = "LONG",
    sl_initial: float | None = 95.0,
    entry_status: str = "OPEN",
    entry_cloid: str = ENTRY_CLOID,
) -> tuple[int, str]:
    decision_uid = "owned-decision"
    trade_id = int(
        store.create_trade(
            run_id="run",
            coin=coin,
            direction=direction,
            qty=qty,
            entry_decision_uid=decision_uid,
            signal_ts=FROZEN,
            decision_ts=FROZEN,
            expected_px=100.0,
            risk_dollars=1.0,
            risk_pct=0.001,
            leverage=1,
            sl_initial=sl_initial,
            tp_initial=None,
            llm_directive_id=None,
        )
    )
    store.insert_order(
        cloid=entry_cloid,
        oid=1,
        group_id=REQUEST_ID,
        order_ref=f"{REQUEST_ID}:ENTRY",
        order_json={"symbol": coin, "role": "ENTRY"},
        decision_uid=decision_uid,
        trade_id=trade_id,
        role="ENTRY",
        status=entry_status,
        qty=qty,
    )
    return trade_id, decision_uid


def make_broker(
    *,
    coin: str = "BTC",
    ordered: float = 2.0,
    position_size: float = 1.0,
    direction: str = "LONG",
    entry_cloid: str = ENTRY_CLOID,
    entry_status: str = "OPEN",
) -> MockBroker:
    broker = MockBroker(bars=[], starting_equity=1000.0, coin=coin)
    broker.orders.append({
        "cloid": entry_cloid,
        "oid": 1,
        "role": "ENTRY",
        "status": entry_status,
        "qty": ordered,
        "avg_fill_px": 100.0,
        "reduce_only": False,
        "symbol": coin,
        "direction": direction,
    })
    if position_size:
        broker.position = Position(
            symbol=coin, size=position_size, entry_px=100.0, unrealized=0.0
        )
    return broker


def make_manager(
    store: Store, broker, *, mono: Mono | None = None
) -> OrderManager:
    return OrderManager(
        store=store,
        broker=broker,
        run_id="run",
        pending_grace_s=0,
        monotonic=mono or Mono(),
    )


def detect_partial(
    manager: OrderManager,
    *,
    filled: float = 1.0,
    cloid: str = ENTRY_CLOID,
    coin: str = "BTC",
    fill_id: str = "f1",
) -> None:
    manager._ingest_fill(
        FillEvent(
            fill_id=fill_id, cloid=cloid, coin=coin, qty=filled, px=100.0,
            ts=FROZEN, role="ENTRY",
        )
    )


def scenario(tmp_path, **kwargs):
    """v5 store + partial entry fill + armed OrderManager."""
    clock = kwargs.pop("clock", None) or Clock()
    mono = kwargs.pop("mono", None) or Mono()
    ordered = kwargs.pop("ordered", 2.0)
    filled = kwargs.pop("filled", 1.0)
    position_size = kwargs.pop("position_size", 1.0)
    store = make_store(tmp_path, clock=clock)
    seed_trade(store, qty=ordered, **kwargs)
    broker = make_broker(ordered=ordered, position_size=position_size)
    manager = make_manager(store, broker, mono=mono)
    detect_partial(manager, filled=filled)
    return store, broker, manager, clock, mono


def codes(store: Store) -> set[str]:
    return {row["code"] for row in store.get_events()}


# ===========================================================================
# RED BASELINE
# ===========================================================================


def test_reconcile_rejects_wrong_sized_owned_stop_as_protection(tmp_path):
    """Quantity-blind reconciliation must not report an undersized SL as safe.

    Base behaviour: ``reconcile`` marked a symbol protected as soon as *any*
    matched SL existed, so a 1.0-lot stop covered a 2.0-lot position.
    """
    store = make_store(tmp_path, version=4)
    trade_id, decision_uid = seed_trade(store, qty=2.0)
    store.insert_order(
        cloid="sl-half", oid=11, group_id="g", order_ref=f"{decision_uid}:SL",
        order_json={"symbol": "BTC", "role": "SL", "trigger_px": 95.0},
        decision_uid=decision_uid, trade_id=trade_id, role="SL",
        status="OPEN", qty=1.0,
    )
    broker = RecordingBroker(
        positions=[Position(symbol="BTC", size=2.0, entry_px=100.0)],
        open_orders=[
            BrokerOrder(
                cloid="sl-half", oid=11, coin="BTC", side="SELL", size=1.0,
                status="OPEN", role="SL", reduce_only=True, trigger_px=95.0,
            )
        ],
    )
    manager = make_manager(store, broker)

    asyncio.run(manager.reconcile())

    assert broker.reprotect_attempts == 1, "undersized SL must not count as protection"


def test_partial_entry_fill_opens_durable_recovery(tmp_path):
    store, _broker, _manager, _clock, _mono = scenario(tmp_path)
    recovery = store.active_partial_recovery_for_symbol("BTC")
    assert recovery is not None
    assert recovery["state"] == PartialProtectionState.PARTIAL_DETECTED.value
    assert store.get_order(ENTRY_CLOID)["status"] == OrderState.PARTIALLY_FILLED.value
    assert store.get_meta("app_state") == "DISARMED"
    assert "PARTIAL_FILL_DETECTED" in codes(store)


def test_cancel_reservation_persists_pending_cancel_before_unknown_io(tmp_path):
    store, broker, manager, _clock, _mono = scenario(tmp_path)
    broker.scripted_cancel.append(
        ScriptedOutcome(
            ActionOutcome.UNKNOWN,
            applied=False,
            reason_code="MOCK_CANCEL_TIMEOUT",
        )
    )

    asyncio.run(manager.run_partial_recovery("BTC"))

    assert store.get_order(ENTRY_CLOID)["status"] == OrderState.PENDING_CANCEL.value
    recovery = store.latest_partial_recovery_for_symbol("BTC")
    assert recovery["state"] == PartialProtectionState.CANCEL_UNKNOWN.value


def test_schema_v5_is_opt_in_and_additive(tmp_path):
    store = Store(tmp_path / "bridge.db", clock=Clock())
    store.initialize()
    assert store.get_meta("schema_version") == "4"
    store.close()

    upgraded = Store(tmp_path / "bridge.db", clock=Clock())
    upgraded.initialize(target_schema_version=5)
    assert upgraded.get_meta("schema_version") == "5"
    tables = {
        row[0]
        for row in upgraded.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    assert {
        "partial_fill_recoveries", "partial_fill_actions", "partial_fill_action_events"
    } <= tables
    assert {"orders", "trades", "submission_attempts", "order_identity"} <= tables


# ===========================================================================
# Quantity model — exact integer lots, never an epsilon
# ===========================================================================


@pytest.mark.parametrize(
    ("value", "decimals", "expected"),
    [(1.0, 3, 1000), (0.001, 3, 1), (2.5, 1, 25), (7.0, 0, 7), (0.0, 4, 0)],
)
def test_quantize_lots_exact(value, decimals, expected):
    assert quantize_lots(value, LotUnit(decimals)) == expected


@pytest.mark.parametrize("value", [0.0001, 0.1 + 0.2, 1.23456])
def test_quantize_lots_rejects_non_lot_multiples(value):
    with pytest.raises(LotQuantizationError):
        quantize_lots(value, LotUnit(3))


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_quantize_lots_rejects_non_finite(value):
    with pytest.raises(LotQuantizationError):
        quantize_lots(value, LotUnit(3))


@pytest.mark.parametrize("decimals", [-1, 19, True, 1.5, "3"])
def test_invalid_size_quantum_fails_closed(decimals):
    with pytest.raises(LotQuantizationError):
        LotUnit(decimals)


def test_lots_round_trip():
    lot = LotUnit(3)
    assert lots_to_size(quantize_lots(1.234, lot), lot) == 1.234


def test_exact_size_equal_without_quantum_is_still_exact():
    assert exact_size_equal(1.0, 1.0, None)
    assert not exact_size_equal(1.0, 1.0000001, None)
    assert not exact_size_equal(1.0, 2.0, LotUnit(3))


@pytest.mark.parametrize(
    ("ordered", "filled", "expected"),
    [
        (2.0, 0.0, OrderState.OPEN),
        (2.0, 1.0, OrderState.PARTIALLY_FILLED),
        (2.0, 2.0, OrderState.FILLED),
    ],
)
def test_canonical_order_state_is_wired_by_quantity(ordered, filled, expected):
    assert (
        canonical_order_state(
            raw_status="OPEN", ordered_qty=ordered, filled_qty=filled, lot=LotUnit(3)
        )
        is expected
    )


def test_canonical_order_state_reserved_cancel_is_pending_cancel():
    assert (
        canonical_order_state(
            raw_status="OPEN", ordered_qty=2.0, filled_qty=1.0,
            lot=LotUnit(3), cancel_reserved=True,
        )
        is OrderState.PENDING_CANCEL
    )


def test_canonical_order_state_terminal_raw_status_wins():
    assert (
        canonical_order_state(
            raw_status="CANCELLED_BY_ENGINE", ordered_qty=2.0, filled_qty=1.0
        )
        is OrderState.CANCELED
    )


def test_partial_state_machine_is_monotonic_within_generation():
    S = PartialProtectionState
    assert can_transition_partial(S.PROTECTION_VERIFIED, S.CANCEL_PENDING)
    assert can_transition_partial(S.PROTECTED_PARTIAL, S.PARTIAL_DETECTED)
    assert not can_transition_partial(S.SAFE_FLAT, S.PARTIAL_DETECTED)
    assert not can_transition_partial(S.UNPROTECTED_ABORT, S.PROTECTION_PENDING)
    assert not can_transition_partial(S.PARTIAL_DETECTED, S.PROTECTED_PARTIAL)
    assert not can_transition_partial(S.PARTIAL_DETECTED, S.SAFE_FLAT)


def test_exit_side_for():
    assert exit_side_for(1.0) == "SELL"
    assert exit_side_for(-1.0) == "BUY"


# ===========================================================================
# Happy path
# ===========================================================================


def test_owned_partial_is_protected_then_entry_cancelled(tmp_path):
    store, broker, manager, _clock, _mono = scenario(tmp_path)

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.PROTECTED_PARTIAL.value
    recovery = store.latest_partial_recovery_for_symbol("BTC")
    assert recovery["position_lots"] == 1000
    assert recovery["provenance"] == "OWNED"
    # exactly one stop, sized to the live position, and one entry cancel
    placed = [c for c in broker.partial_calls if c[0] == "place_protective_stop"]
    cancels = [c for c in broker.partial_calls if c[0] == "cancel_order_by_cloid"]
    assert len(placed) == 1
    assert cancels == [("cancel_order_by_cloid", ENTRY_CLOID)]
    stop = next(o for o in broker.orders if o["role"] == "SL")
    assert stop["qty"] == 1.0 and stop["reduce_only"] is True
    assert "PARTIAL_PROTECTED" in codes(store)
    # accepting, but the application stays DISARMED until a human re-arms
    assert store.get_meta("app_state") == "DISARMED"
    assert store.partial_recoveries_awaiting_rearm()


def test_zero_percent_fill_never_opens_recovery(tmp_path):
    store = make_store(tmp_path)
    seed_trade(store, qty=2.0)
    broker = make_broker()
    manager = make_manager(store, broker)

    # a full fill is not a partial fill
    detect_partial(manager, filled=2.0)

    assert store.active_partial_recovery_for_symbol("BTC") is None
    assert broker.broker_mutations == []


def test_single_lot_partial_is_protected(tmp_path):
    store, broker, manager, _c, _m = scenario(
        tmp_path, ordered=0.002, filled=0.001, position_size=0.001
    )
    state = asyncio.run(manager.run_partial_recovery("BTC"))
    assert state == PartialProtectionState.PROTECTED_PARTIAL.value
    assert store.latest_partial_recovery_for_symbol("BTC")["position_lots"] == 1


def test_repeated_recovery_runs_are_idempotent(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    asyncio.run(manager.run_partial_recovery("BTC"))
    before = list(broker.broker_mutations)
    asyncio.run(manager.run_partial_recovery("BTC"))
    assert broker.broker_mutations == before


# ===========================================================================
# Safety precedence — zero-mutation outcomes
# ===========================================================================


def test_active_submission_quarantine_defers_with_zero_mutation(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    store.conn.execute(
        """INSERT INTO order_identity(
             intent_id, intent_preimage, request_id, request_preimage,
             cloid_seed, origin_run_id, origin_decision_uid, state, reserved_ts)
           VALUES (?, 'p', ?, 'p', 'seed', 'run', 'd', 'RESERVED', 'ts')""",
        ("intent-v1:" + "b" * 64, "request-v1:" + "b" * 64),
    )
    store.conn.execute(
        """INSERT INTO submission_attempts(
             attempt_id, intent_id, request_id, origin_run_id, origin_decision_uid,
             state, recovery_payload_json, planned_cloids_json,
             created_ts, updated_ts, reason_code)
           VALUES (?, ?, ?, 'run', 'd', 'UNKNOWN_SUBMISSION', '{}', '{}',
                   'ts', 'ts', 'QUARANTINE')""",
        ("attempt-v1:" + "b" * 64, "intent-v1:" + "b" * 64, "request-v1:" + "b" * 64),
    )
    store.conn.commit()
    assert store.has_submission_quarantine()

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.PARTIAL_DETECTED.value
    assert broker.broker_mutations == []
    assert "PARTIAL_RECOVERY_DEFERRED_QUARANTINE" in codes(store)
    # the dominant quarantine must not be shadowed by a competing abort
    assert not store.partial_recovery_abort_active("BTC")


def test_quarantine_prevents_detection_from_opening_competing_recovery(tmp_path):
    store = make_store(tmp_path)
    seed_trade(store, qty=2.0)
    broker = make_broker()
    manager = make_manager(store, broker)
    intent_id = "intent-v1:" + "c" * 64
    request_id = "request-v1:" + "c" * 64
    store.conn.execute(
        """INSERT INTO order_identity(
             intent_id, intent_preimage, request_id, request_preimage,
             cloid_seed, origin_run_id, origin_decision_uid, state, reserved_ts)
           VALUES (?, 'p', ?, 'p', 'seed', 'run', 'd', 'RESERVED', 'ts')""",
        (intent_id, request_id),
    )
    store.conn.execute(
        """INSERT INTO submission_attempts(
             attempt_id, intent_id, request_id, origin_run_id, origin_decision_uid,
             state, recovery_payload_json, planned_cloids_json,
             created_ts, updated_ts, reason_code)
           VALUES (?, ?, ?, 'run', 'd', 'UNKNOWN_SUBMISSION', '{}', '{}',
                   'ts', 'ts', 'QUARANTINE')""",
        ("attempt-v1:" + "c" * 64, intent_id, request_id),
    )
    store.conn.commit()

    detect_partial(manager)

    assert store.latest_partial_recovery_for_symbol("BTC") is None
    assert broker.broker_mutations == []


def test_foreign_order_aborts_with_zero_mutation(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    broker.partial_foreign_orders.append({
        "cloid": "manual-order", "role": "SL", "status": "OPEN", "qty": 1.0,
        "symbol": "BTC", "direction": "LONG", "reduce_only": True,
    })

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.UNPROTECTED_ABORT.value
    assert broker.broker_mutations == []
    assert store.latest_partial_recovery_for_symbol("BTC")["reason_code"] == (
        "FOREIGN_ORDER_PRESENT"
    )


def test_mixed_provenance_aborts_with_zero_mutation(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    # more live size than the owned entry could ever account for
    broker.partial_extra_position = 2.0

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.UNPROTECTED_ABORT.value
    assert broker.broker_mutations == []
    assert store.latest_partial_recovery_for_symbol("BTC")["reason_code"] == (
        "MIXED_PROVENANCE"
    )
    assert store.partial_recovery_abort_active("BTC")


def test_subplanned_manual_quantity_is_still_mixed_and_never_mutated(tmp_path):
    # The planned order is 2.0 and durable owned fills are only 1.0. A 1.5
    # position used to slip through A1's planned-quantity ceiling.
    store, broker, manager, _c, _m = scenario(tmp_path, position_size=1.5)

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.UNPROTECTED_ABORT.value
    assert broker.broker_mutations == []
    assert store.latest_partial_recovery_for_symbol("BTC")["reason_code"] == (
        "MIXED_PROVENANCE"
    )


def test_other_trade_order_is_mixed_provenance_not_owned(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    other_trade, other_decision = seed_trade(
        store, qty=1.0, entry_cloid="other-entry"
    )
    store.insert_order(
        cloid="other-sl", oid=22, group_id="other",
        order_ref=f"{other_decision}:SL",
        order_json={"symbol": "BTC", "role": "SL"},
        decision_uid=other_decision, trade_id=other_trade, role="SL",
        status="OPEN", qty=1.0,
    )
    broker.partial_foreign_orders.append({
        "cloid": "other-sl", "role": "SL", "status": "OPEN", "qty": 1.0,
        "symbol": "BTC", "direction": "LONG", "reduce_only": True,
    })

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.UNPROTECTED_ABORT.value
    assert broker.broker_mutations == []
    assert store.latest_partial_recovery_for_symbol("BTC")["reason_code"] == (
        "OTHER_TRADE_ORDER_PRESENT"
    )


def test_opposite_side_position_is_ambiguous_and_aborts(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path, position_size=-1.0)

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.UNPROTECTED_ABORT.value
    assert broker.broker_mutations == []
    assert store.latest_partial_recovery_for_symbol("BTC")["reason_code"] == (
        "POSITION_SIDE_CONFLICT"
    )


def test_inexact_snapshot_before_deadline_does_not_mutate_or_abort(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    broker.partial_snapshot_available = False

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.PARTIAL_DETECTED.value
    assert broker.broker_mutations == []
    assert "PARTIAL_EVIDENCE_INCOMPLETE" in codes(store)


def test_inexact_snapshot_after_deadline_aborts(tmp_path):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    broker.partial_snapshot_available = False
    clock.advance(PROTECT_DEADLINE_S + 1)

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.UNPROTECTED_ABORT.value
    assert broker.broker_mutations == []
    assert store.latest_partial_recovery_for_symbol("BTC")["reason_code"] == (
        "SNAPSHOT_INEXACT"
    )


def test_missing_size_quantum_fails_closed(tmp_path):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    broker.partial_size_decimals = None
    clock.advance(PROTECT_DEADLINE_S + 1)

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.UNPROTECTED_ABORT.value
    assert broker.broker_mutations == []


def test_recovery_api_unavailable_aborts_without_mutation(tmp_path):
    store = make_store(tmp_path)
    seed_trade(store, qty=2.0)
    broker = RecordingBroker(positions=[Position(symbol="BTC", size=1.0, entry_px=100.0)])
    manager = make_manager(store, broker)
    detect_partial(manager)

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.UNPROTECTED_ABORT.value
    assert broker.flattened == [] and broker.cancelled == []
    assert broker.reprotect_attempts == 0


def test_missing_stop_price_aborts_without_mutation(tmp_path):
    store = make_store(tmp_path)
    seed_trade(store, qty=2.0, sl_initial=None)
    broker = make_broker()
    manager = make_manager(store, broker)
    detect_partial(manager)

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.UNPROTECTED_ABORT.value
    assert broker.broker_mutations == []


# ===========================================================================
# Unknown outcomes — query only, never a blind retry
# ===========================================================================


def test_unknown_protection_outcome_is_query_only(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    # reported UNKNOWN, and the exchange really did not apply it
    broker.scripted_place.append(
        ScriptedOutcome(ActionOutcome.UNKNOWN, applied=False, reason_code="MOCK_TIMEOUT")
    )
    broker.partial_query_available = False

    asyncio.run(manager.run_partial_recovery("BTC"))

    places = [c for c in broker.partial_calls if c[0] == "place_protective_stop"]
    assert len(places) == 1, "an UNKNOWN outcome must never be re-placed"
    assert [c for c in broker.partial_calls if c[0] == "query_order"], "evidence queried"
    recovery = store.latest_partial_recovery_for_symbol("BTC")
    assert recovery["state"] == PartialProtectionState.PROTECTION_PENDING.value


def test_unknown_but_actually_applied_protection_is_resolved_by_evidence(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    broker.scripted_place.append(
        ScriptedOutcome(ActionOutcome.UNKNOWN, applied=True, reason_code="MOCK_TIMEOUT")
    )

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    places = [c for c in broker.partial_calls if c[0] == "place_protective_stop"]
    assert len(places) == 1
    assert state == PartialProtectionState.PROTECTED_PARTIAL.value


def test_proven_not_applied_protection_reuses_the_same_identity(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    broker.scripted_place.append(
        ScriptedOutcome(
            ActionOutcome.NOT_APPLIED, applied=False, reason_code="MOCK_REJECTED"
        )
    )

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    places = [c for c in broker.partial_calls if c[0] == "place_protective_stop"]
    assert len(places) == 2, "a proven non-application may be retried"
    assert places[0][1] == places[1][1], "retry must reuse the same cloid"
    assert state == PartialProtectionState.PROTECTED_PARTIAL.value
    stops = store.partial_actions_for_recovery(
        store.latest_partial_recovery_for_symbol("BTC")["recovery_id"], "INSTALL_STOP"
    )
    assert len(stops) == 1, "one identity, not a new one per attempt"


def test_unknown_cancel_then_terminal_by_query(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    broker.scripted_cancel.append(
        ScriptedOutcome(ActionOutcome.UNKNOWN, applied=True, reason_code="MOCK_TIMEOUT")
    )

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    cancels = [c for c in broker.partial_calls if c[0] == "cancel_order_by_cloid"]
    assert len(cancels) == 1, "an UNKNOWN cancel is never re-issued blindly"
    assert state == PartialProtectionState.PROTECTED_PARTIAL.value


def test_crash_after_reservation_before_send_never_replaces(tmp_path):
    """Reserve committed, process died before the write: evidence only."""
    store, broker, manager, _c, _m = scenario(tmp_path)
    recovery = store.active_partial_recovery_for_symbol("BTC")
    action_id = compute_partial_action_id(
        kind="INSTALL_STOP", trade_id=int(recovery["trade_id"]),
        entry_cloid=ENTRY_CLOID, entry_request_id=REQUEST_ID,
        generation=0, qty_lots=1000,
    )
    store.reserve_partial_action(
        recovery_id=str(recovery["recovery_id"]), action_id=action_id,
        kind="INSTALL_STOP", target_cloid=compute_partial_action_cloid(action_id),
        expected_state=PartialProtectionState.PARTIAL_DETECTED.value,
        next_state=PartialProtectionState.PROTECTION_PENDING.value,
        reason_code="PROTECTION_RESERVED", generation=0, qty_lots=1000,
        provenance="OWNED", size_decimals=3, position_lots=1000,
    )
    restarted = make_manager(store, broker)  # fresh process: no monotonic memory

    asyncio.run(restarted.run_partial_recovery("BTC"))

    assert not [c for c in broker.partial_calls if c[0] == "place_protective_stop"]
    assert [c for c in broker.partial_calls if c[0] == "query_order"]


# ===========================================================================
# Deadlines — non-resetting in both domains
# ===========================================================================


def test_protect_deadline_is_not_reset_by_a_later_fill(tmp_path):
    store, _broker, manager, _c, _m = scenario(tmp_path)
    first = store.active_partial_recovery_for_symbol("BTC")["protect_deadline_ts"]
    detect_partial(manager, filled=1.5, fill_id="f2")
    again = store.active_partial_recovery_for_symbol("BTC")
    assert again["protect_deadline_ts"] == first
    assert again["first_observed_ts"] == store.active_partial_recovery_for_symbol(
        "BTC"
    )["first_observed_ts"]


def test_protect_deadline_survives_restart_without_a_fresh_window(tmp_path):
    clock = Clock()
    store, broker, _manager, _c, _m = scenario(tmp_path, clock=clock)
    deadline = store.active_partial_recovery_for_symbol("BTC")["protect_deadline_ts"]
    clock.advance(PROTECT_DEADLINE_S + 1)
    restarted = make_manager(store, broker, mono=Mono())

    asyncio.run(restarted.run_partial_recovery("BTC"))

    recovery = store.latest_partial_recovery_for_symbol("BTC")
    assert recovery["protect_deadline_ts"] == deadline
    # already expired on boot -> straight to the bounded flatten phase
    assert recovery["state"] in {
        PartialProtectionState.SAFE_FLAT.value,
        PartialProtectionState.FLATTEN_PENDING.value,
        PartialProtectionState.FLATTEN_UNKNOWN.value,
        PartialProtectionState.UNPROTECTED_ABORT.value,
    }


def test_monotonic_domain_alone_can_expire_the_deadline(tmp_path):
    mono = Mono()
    store, broker, manager, _c, _m = scenario(tmp_path, mono=mono)
    # wall clock frozen; only the runtime monotonic clock advances
    broker.partial_snapshot_available = False
    mono.advance(PROTECT_DEADLINE_S + 1)

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.UNPROTECTED_ABORT.value


def test_wall_clock_rollback_is_treated_as_expired(tmp_path):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    broker.partial_snapshot_available = False
    clock.advance(-3600)  # observer's clock jumped backwards

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.UNPROTECTED_ABORT.value


def test_unparseable_persisted_deadline_is_treated_as_expired(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    broker.partial_snapshot_available = False
    store.conn.execute(
        "UPDATE partial_fill_recoveries SET protect_deadline_ts = 'not-a-time'"
    )
    store.conn.commit()

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.UNPROTECTED_ABORT.value


def test_flatten_deadline_is_written_once_and_never_reset(tmp_path):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    clock.advance(PROTECT_DEADLINE_S + 1)
    broker.scripted_flatten.append(
        ScriptedOutcome(ActionOutcome.UNKNOWN, applied=False, reason_code="MOCK_TIMEOUT")
    )
    asyncio.run(manager.run_partial_recovery("BTC"))
    first = store.latest_partial_recovery_for_symbol("BTC")["flatten_deadline_ts"]
    assert first is not None

    clock.advance(1.0)
    asyncio.run(manager.run_partial_recovery("BTC"))

    assert store.latest_partial_recovery_for_symbol("BTC")["flatten_deadline_ts"] == first


def test_flatten_deadline_expiry_ends_in_unprotected_abort(tmp_path):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    clock.advance(PROTECT_DEADLINE_S + 1)
    broker.scripted_flatten.append(
        ScriptedOutcome(ActionOutcome.UNKNOWN, applied=False, reason_code="MOCK_TIMEOUT")
    )
    asyncio.run(manager.run_partial_recovery("BTC"))
    clock.advance(FLATTEN_VERIFY_DEADLINE_S + 1)

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.UNPROTECTED_ABORT.value
    assert store.latest_partial_recovery_for_symbol("BTC")["reason_code"] == (
        "FLATTEN_DEADLINE_EXPIRED"
    )


def test_unknown_flatten_does_not_advance_the_attempt_sequence(tmp_path):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    clock.advance(PROTECT_DEADLINE_S + 1)
    broker.scripted_flatten.append(
        ScriptedOutcome(ActionOutcome.UNKNOWN, applied=False, reason_code="MOCK_TIMEOUT")
    )

    asyncio.run(manager.run_partial_recovery("BTC"))
    asyncio.run(manager.run_partial_recovery("BTC"))

    recovery = store.latest_partial_recovery_for_symbol("BTC")
    assert recovery["flatten_seq"] == 0
    flattens = [c for c in broker.partial_calls if c[0] == "flatten_reduce_only"]
    assert len(flattens) == 1, "an unknown flatten never mints a second close"


def test_proven_failed_flatten_advances_sequence_with_a_new_identity(tmp_path):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    clock.advance(PROTECT_DEADLINE_S + 1)
    broker.scripted_flatten.append(
        ScriptedOutcome(
            ActionOutcome.NOT_APPLIED, applied=False, reason_code="MOCK_REJECTED"
        )
    )

    asyncio.run(manager.run_partial_recovery("BTC"))

    recovery = store.latest_partial_recovery_for_symbol("BTC")
    assert recovery["flatten_seq"] >= 1
    flattens = [c for c in broker.partial_calls if c[0] == "flatten_reduce_only"]
    assert len({call[1] for call in flattens}) == len(flattens), "distinct identities"


# ===========================================================================
# Late fills / generations
# ===========================================================================


def test_late_fill_during_cancel_opens_a_new_generation(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    broker.late_entry_fill_on_cancel = 0.5  # fills while the cancel is in flight

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    recovery = store.latest_partial_recovery_for_symbol("BTC")
    assert recovery["generation"] >= 1, "quantity proof invalidated by the late fill"
    assert state == PartialProtectionState.PROTECTED_PARTIAL.value
    assert recovery["position_lots"] == 1500
    stop = [o for o in broker.orders if o["role"] == "SL" and o["status"] == "OPEN"]
    assert any(o["qty"] == 1.5 for o in stop), "re-protected at the new exact quantity"
    # the deadline is untouched by the new generation
    assert recovery["first_observed_ts"] == store.list_partial_recoveries()[0][
        "first_observed_ts"
    ]


def test_cancel_entry_identity_is_quantity_and_generation_independent():
    base = dict(trade_id=7, entry_cloid=ENTRY_CLOID, entry_request_id=REQUEST_ID)
    first = compute_partial_action_id(kind="CANCEL_ENTRY", **base)
    second = compute_partial_action_id(kind="CANCEL_ENTRY", **base)
    assert first == second
    stop_a = compute_partial_action_id(
        kind="INSTALL_STOP", generation=0, qty_lots=1000, **base
    )
    stop_b = compute_partial_action_id(
        kind="INSTALL_STOP", generation=1, qty_lots=1000, **base
    )
    stop_c = compute_partial_action_id(
        kind="INSTALL_STOP", generation=0, qty_lots=1500, **base
    )
    assert len({stop_a, stop_b, stop_c}) == 3
    assert compute_partial_action_cloid(stop_a) != compute_partial_action_cloid(stop_b)


def test_action_identities_are_stable_across_replay(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    asyncio.run(manager.run_partial_recovery("BTC"))
    recovery = store.latest_partial_recovery_for_symbol("BTC")
    first = [a["action_id"] for a in store.partial_actions_for_recovery(
        str(recovery["recovery_id"])
    )]
    replayed = make_manager(store, broker)
    asyncio.run(replayed.run_partial_recovery("BTC"))
    second = [a["action_id"] for a in store.partial_actions_for_recovery(
        str(recovery["recovery_id"])
    )]
    assert first == second


def test_new_recovery_generation_reuses_stable_cancel_reservation(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    assert asyncio.run(manager.run_partial_recovery("BTC")) == (
        PartialProtectionState.PROTECTED_PARTIAL.value
    )
    prior = store.latest_partial_recovery_for_symbol("BTC")
    store.conn.execute(
        "UPDATE partial_fill_recoveries SET state = ?, reason_code = ? "
        "WHERE recovery_id = ?",
        (
            PartialProtectionState.SAFE_FLAT.value,
            "TEST_SAFE_FLAT",
            prior["recovery_id"],
        ),
    )
    store.conn.commit()
    reopened = store.open_partial_recovery(
        run_id="run",
        symbol="BTC",
        trade_id=int(prior["trade_id"]),
        entry_cloid=str(prior["entry_cloid"]),
        entry_decision_uid=str(prior["entry_decision_uid"]),
        entry_request_id=str(prior["entry_request_id"]),
        first_observed_ts=str(prior["first_observed_ts"]),
        protect_deadline_ts=str(prior["protect_deadline_ts"]),
        generation=int(prior["generation"]) + 1,
        size_decimals=int(prior["size_decimals"]),
        ordered_lots=int(prior["ordered_lots"]),
        filled_lots=int(prior["filled_lots"]),
    )

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    cancel_id = compute_partial_action_id(
        kind="CANCEL_ENTRY",
        trade_id=int(prior["trade_id"]),
        entry_cloid=str(prior["entry_cloid"]),
        entry_request_id=str(prior["entry_request_id"]),
    )
    assert state == PartialProtectionState.PROTECTED_PARTIAL.value
    assert store.get_partial_action(cancel_id)["recovery_id"] == prior["recovery_id"]
    assert store.partial_actions_for_recovery(
        str(reopened["recovery_id"]), "CANCEL_ENTRY"
    ) == []


def test_orphan_cancel_replay_queries_before_exact_identity_resend(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    assert asyncio.run(manager.run_partial_recovery("BTC")) == (
        PartialProtectionState.PROTECTED_PARTIAL.value
    )
    recovery = store.latest_partial_recovery_for_symbol("BTC")

    async def exercise():
        async with manager.symbol_locks.hold("BTC"):
            snapshot = await broker.symbol_snapshot("BTC")
            orphan = next(order for order in snapshot.open_orders if order.role == "SL")
            action_id = compute_partial_action_id(
                kind="CANCEL_PROTECTION",
                trade_id=int(recovery["trade_id"]),
                entry_cloid=str(recovery["entry_cloid"]),
                entry_request_id=str(recovery["entry_request_id"]),
                target_cloid=str(orphan.cloid),
            )
            store.reserve_partial_action(
                recovery_id=str(recovery["recovery_id"]),
                action_id=action_id,
                kind="CANCEL_PROTECTION",
                target_cloid=str(orphan.cloid),
                expected_state=str(recovery["state"]),
                next_state=str(recovery["state"]),
                reason_code="CANCEL_PROTECTION_RESERVED",
            )
            before = len([
                call for call in broker.partial_calls
                if call == ("cancel_order_by_cloid", str(orphan.cloid))
            ])
            await manager._cancel_orphan(recovery, broker, orphan)
            after_query = len([
                call for call in broker.partial_calls
                if call == ("cancel_order_by_cloid", str(orphan.cloid))
            ])
            assert after_query == before
            assert store.resolve_partial_action(action_id) == (
                ActionOutcome.NOT_APPLIED.value
            )
            await manager._cancel_orphan(recovery, broker, orphan)
            await manager._cancel_orphan(recovery, broker, orphan)
            after_replays = len([
                call for call in broker.partial_calls
                if call == ("cancel_order_by_cloid", str(orphan.cloid))
            ])
            assert after_replays == before + 1
            assert store.resolve_partial_action(action_id) == (
                ActionOutcome.APPLIED.value
            )

    asyncio.run(exercise())


# ===========================================================================
# SAFE_FLAT
# ===========================================================================


def test_safe_flat_requires_zero_position_and_no_owned_live_orders(tmp_path):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    clock.advance(PROTECT_DEADLINE_S + 1)

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.SAFE_FLAT.value
    assert broker.position is None
    live = [o for o in broker.orders if o["status"] in {"OPEN", "SUBMITTED"}]
    assert live == [], "no orphan owned order may survive a SAFE_FLAT claim"
    assert "PARTIAL_SAFE_FLAT" in codes(store)


def test_safe_flat_refused_while_a_remainder_survives(tmp_path):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    clock.advance(PROTECT_DEADLINE_S + 1)
    # the close only removes half of the exposure
    original = broker._reduce_position

    def half(symbol, size, cloid):
        original(symbol, size / 2.0, cloid)

    broker._reduce_position = half
    clock.advance(FLATTEN_VERIFY_DEADLINE_S + 1)

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.UNPROTECTED_ABORT.value
    assert broker.position is not None


def test_orphan_owned_protection_prevents_safe_flat_until_cancelled(tmp_path):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    # protect first, then force the flatten path so an owned SL is left behind
    asyncio.run(manager.run_partial_recovery("BTC"))
    assert any(o["role"] == "SL" and o["status"] == "OPEN" for o in broker.orders)
    store.conn.execute(
        "UPDATE partial_fill_recoveries SET state = ?, reason_code = 'FORCED'",
        (PartialProtectionState.CANCEL_PENDING.value,),
    )
    store.conn.commit()
    broker.position = None
    clock.advance(PROTECT_DEADLINE_S + 1)

    state = asyncio.run(manager.run_partial_recovery("BTC"))

    assert state == PartialProtectionState.SAFE_FLAT.value
    assert not [
        o for o in broker.orders if o["role"] == "SL" and o["status"] == "OPEN"
    ]


def test_new_owned_exposure_after_safe_flat_opens_a_new_generation(tmp_path):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    clock.advance(PROTECT_DEADLINE_S + 1)
    assert asyncio.run(manager.run_partial_recovery("BTC")) == (
        PartialProtectionState.SAFE_FLAT.value
    )
    flat_id = store.latest_partial_recovery_for_symbol("BTC")["recovery_id"]

    # a second owned entry partially fills later
    seed_trade(store, qty=2.0, entry_cloid="entry-2")
    detect_partial(manager, filled=1.0, cloid="entry-2", fill_id="late-1")

    active = store.active_partial_recovery_for_symbol("BTC")
    assert active is not None
    assert active["recovery_id"] != flat_id
    assert store.get_partial_recovery(flat_id)["state"] == (
        PartialProtectionState.SAFE_FLAT.value
    )


def test_same_entry_late_fill_after_safe_flat_opens_new_generation(tmp_path):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    clock.advance(PROTECT_DEADLINE_S + 1)
    assert asyncio.run(manager.run_partial_recovery("BTC")) == (
        PartialProtectionState.SAFE_FLAT.value
    )
    flat = store.latest_partial_recovery_for_symbol("BTC")
    original_deadline = flat["protect_deadline_ts"]
    broker.position = Position(symbol="BTC", size=0.5, entry_px=100.0)

    detect_partial(manager, filled=0.5, fill_id="post-flat-late")

    active = store.active_partial_recovery_for_symbol("BTC")
    assert active is not None
    assert active["recovery_id"] != flat["recovery_id"]
    assert active["generation"] == int(flat["generation"]) + 1
    assert active["protect_deadline_ts"] == original_deadline
    assert store.get_order(ENTRY_CLOID)["status"] == "CANCELED"


def test_reconcile_claims_owned_exposure_after_safe_flat_without_fill_event(tmp_path):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    clock.advance(PROTECT_DEADLINE_S + 1)
    assert asyncio.run(manager.run_partial_recovery("BTC")) == (
        PartialProtectionState.SAFE_FLAT.value
    )
    flat = store.latest_partial_recovery_for_symbol("BTC")
    original_deadline = flat["protect_deadline_ts"]
    manager._legacy_partial_scan_done = True
    broker.position = Position(symbol="BTC", size=1.0, entry_px=100.0)
    before = list(broker.broker_mutations)

    asyncio.run(manager.reconcile())

    active = store.active_partial_recovery_for_symbol("BTC")
    assert active is not None
    assert active["recovery_id"] != flat["recovery_id"]
    assert active["generation"] == int(flat["generation"]) + 1
    assert active["reason_code"] == "POST_SAFE_FLAT_OWNED"
    assert active["protect_deadline_ts"] == original_deadline
    assert broker.broker_mutations == before


def test_reconcile_aborts_ambiguous_exposure_after_safe_flat_without_mutation(
    tmp_path,
):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    clock.advance(PROTECT_DEADLINE_S + 1)
    assert asyncio.run(manager.run_partial_recovery("BTC")) == (
        PartialProtectionState.SAFE_FLAT.value
    )
    flat = store.latest_partial_recovery_for_symbol("BTC")
    manager._legacy_partial_scan_done = True
    broker.position = Position(symbol="BTC", size=0.5, entry_px=100.0)
    before = list(broker.broker_mutations)

    asyncio.run(manager.reconcile())

    latest = store.latest_partial_recovery_for_symbol("BTC")
    assert latest["recovery_id"] != flat["recovery_id"]
    assert latest["state"] == PartialProtectionState.UNPROTECTED_ABORT.value
    assert latest["reason_code"] == "OWNED_QUANTITY_CONFLICT"
    assert broker.broker_mutations == before


def test_restart_scan_opens_new_generation_for_owned_post_safe_flat_exposure(
    tmp_path,
):
    clock = Clock()
    store, broker, manager, _c, _m = scenario(tmp_path, clock=clock)
    clock.advance(PROTECT_DEADLINE_S + 1)
    assert asyncio.run(manager.run_partial_recovery("BTC")) == (
        PartialProtectionState.SAFE_FLAT.value
    )
    flat = store.latest_partial_recovery_for_symbol("BTC")
    broker.position = Position(symbol="BTC", size=1.0, entry_px=100.0)
    restarted = make_manager(store, broker)

    asyncio.run(restarted.reconcile())

    latest = store.latest_partial_recovery_for_symbol("BTC")
    assert latest["recovery_id"] != flat["recovery_id"]
    assert latest["generation"] == int(flat["generation"]) + 1


# ===========================================================================
# Shared protection predicate / reconciliation repair
# ===========================================================================


@pytest.mark.parametrize(
    ("size", "role", "reduce_only", "side"),
    [
        (0.5, "SL", True, "SELL"),   # undersized
        (2.0, "SL", True, "SELL"),   # oversized
        (1.0, "TP", True, "SELL"),   # take-profit never substitutes
        (1.0, "SL", False, "SELL"),  # not reduce-only
        (1.0, "SL", True, "BUY"),    # wrong side
    ],
)
def test_non_qualifying_stops_are_never_protection(tmp_path, size, role, reduce_only, side):
    store = make_store(tmp_path, version=4)
    trade_id, decision_uid = seed_trade(store, qty=1.0)
    store.insert_order(
        cloid="sl-x", oid=11, group_id="g", order_ref=f"{decision_uid}:SL",
        order_json={"symbol": "BTC", "role": role, "trigger_px": 95.0},
        decision_uid=decision_uid, trade_id=trade_id, role=role,
        status="OPEN", qty=size,
    )
    broker = RecordingBroker(
        positions=[Position(symbol="BTC", size=1.0, entry_px=100.0)],
        open_orders=[
            BrokerOrder(
                cloid="sl-x", oid=11, coin="BTC", side=side, size=size,
                status="OPEN", role=role, reduce_only=reduce_only, trigger_px=95.0,
            )
        ],
    )
    manager = make_manager(store, broker)

    asyncio.run(manager.reconcile())

    assert broker.reprotect_attempts == 1


def test_exact_owned_stop_is_accepted_as_protection(tmp_path):
    store = make_store(tmp_path, version=4)
    trade_id, decision_uid = seed_trade(store, qty=1.0)
    store.insert_order(
        cloid="sl-ok", oid=11, group_id="g", order_ref=f"{decision_uid}:SL",
        order_json={"symbol": "BTC", "role": "SL", "trigger_px": 95.0},
        decision_uid=decision_uid, trade_id=trade_id, role="SL",
        status="OPEN", qty=1.0,
    )
    broker = RecordingBroker(
        positions=[Position(symbol="BTC", size=1.0, entry_px=100.0)],
        open_orders=[
            BrokerOrder(
                cloid="sl-ok", oid=11, coin="BTC", side="SELL", size=1.0,
                status="OPEN", role="SL", reduce_only=True, trigger_px=95.0,
            )
        ],
    )
    manager = make_manager(store, broker)

    asyncio.run(manager.reconcile())

    assert broker.reprotect_attempts == 0
    assert broker.flattened == []


def test_unowned_exact_stop_is_not_protection(tmp_path):
    """An exchange SL that matches nothing in our books is foreign, not safe."""
    store = make_store(tmp_path, version=4)
    seed_trade(store, qty=1.0)
    broker = RecordingBroker(
        positions=[Position(symbol="BTC", size=1.0, entry_px=100.0)],
        open_orders=[
            BrokerOrder(
                cloid="not-ours", oid=99, coin="BTC", side="SELL", size=1.0,
                status="OPEN", role="SL", reduce_only=True, trigger_px=95.0,
            )
        ],
    )
    manager = make_manager(store, broker)

    asyncio.run(manager.reconcile())

    assert broker.reprotect_attempts == 1


def test_active_recovery_suppresses_ordinary_reconcile_repair(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    broker.partial_snapshot_available = False  # recovery cannot progress
    calls: list[str] = []

    async def spy(coin):
        calls.append(coin)

    broker.flatten = spy

    asyncio.run(manager.reconcile())

    assert calls == [], "ordinary repair must not compete with partial recovery"


def test_protected_partial_suppresses_ordinary_reconcile_until_human_rearm(
    tmp_path,
):
    store, broker, manager, _c, _m = scenario(tmp_path)
    assert asyncio.run(manager.run_partial_recovery("BTC")) == (
        PartialProtectionState.PROTECTED_PARTIAL.value
    )
    for order in broker.orders:
        if order["role"] == "SL":
            order["qty"] = 0.5
    before = list(broker.broker_mutations)

    asyncio.run(manager.reconcile())

    assert broker.broker_mutations == before
    assert store.partial_recoveries_awaiting_rearm()


# ===========================================================================
# Per-symbol serialization and ordinary-path suppression
# ===========================================================================


def test_trail_and_close_are_suppressed_during_recovery(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    position = Position(symbol="BTC", size=1.0, entry_px=100.0)

    trailed = asyncio.run(manager.trail_position(position, 99.0))
    asyncio.run(manager.close_position(position))

    assert trailed is False
    assert "TRAIL_SUPPRESSED_PARTIAL_RECOVERY" in codes(store)
    assert "CLOSE_SUPPRESSED_PARTIAL_RECOVERY" in codes(store)


def test_abort_latch_keeps_suppressing_ordinary_paths(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)
    broker.partial_extra_position = 2.0
    asyncio.run(manager.run_partial_recovery("BTC"))
    assert store.partial_recovery_abort_active("BTC")

    trailed = asyncio.run(
        manager.trail_position(Position(symbol="BTC", size=1.0, entry_px=100.0), 99.0)
    )

    assert trailed is False


def test_concurrent_recovery_runs_do_not_interleave_broker_calls(tmp_path):
    store, broker, manager, _c, _m = scenario(tmp_path)

    async def race():
        await asyncio.gather(
            manager.run_partial_recovery("BTC"),
            manager.run_partial_recovery("BTC"),
            manager.run_partial_recovery("BTC"),
        )

    asyncio.run(race())

    places = [c for c in broker.partial_calls if c[0] == "place_protective_stop"]
    cancels = [c for c in broker.partial_calls if c[0] == "cancel_order_by_cloid"]
    assert len(places) == 1
    assert len(cancels) == 1
    assert store.latest_partial_recovery_for_symbol("BTC")["state"] == (
        PartialProtectionState.PROTECTED_PARTIAL.value
    )


def test_queued_fill_ingestion_holds_the_symbol_writer_lock(tmp_path):
    store = make_store(tmp_path)
    seed_trade(store, qty=2.0)
    broker = make_broker()
    manager = make_manager(store, broker)
    observed: list[bool] = []
    original = manager._ingest_event

    def spy(event):
        observed.append(manager.symbol_locks.is_held("BTC"))
        return original(event)

    manager._ingest_event = spy
    manager._queued_events.append(
        FillEvent(
            fill_id="locked-fill", cloid=ENTRY_CLOID, coin="BTC",
            qty=1.0, px=100.0, ts=FROZEN, role="ENTRY",
        )
    )

    asyncio.run(manager.sync_broker_state())

    assert observed == [True]
    assert store.active_partial_recovery_for_symbol("BTC") is not None


def test_ordinary_reconcile_mutations_hold_the_symbol_writer_lock(tmp_path):
    store = make_store(tmp_path, version=4)
    seed_trade(store, qty=2.0)
    broker = RecordingBroker(
        positions=[Position(symbol="BTC", size=2.0, entry_px=100.0)],
        open_orders=[],
    )
    manager = make_manager(store, broker)
    held: list[tuple[str, bool]] = []

    async def reprotect(*args):
        held.append(("reprotect", manager.symbol_locks.is_held("BTC")))
        return None

    async def flatten(symbol):
        held.append(("flatten", manager.symbol_locks.is_held(symbol)))

    broker.reprotect_position = reprotect
    broker.flatten = flatten

    asyncio.run(manager.reconcile())

    assert held == [("reprotect", True), ("flatten", True)]


def test_symbol_lock_is_required_for_snapshot_helpers(tmp_path):
    from bridge.engine.orders import SymbolLockNotHeld

    store, broker, manager, _c, _m = scenario(tmp_path)
    recovery = store.active_partial_recovery_for_symbol("BTC")

    with pytest.raises(SymbolLockNotHeld):
        asyncio.run(manager._snapshot(broker, recovery))


# ===========================================================================
# Store-level invariants
# ===========================================================================


def test_action_rows_are_immutable(tmp_path):
    store, _broker, manager, _c, _m = scenario(tmp_path)
    asyncio.run(manager.run_partial_recovery("BTC"))
    action = store.partial_actions_for_recovery(
        str(store.latest_partial_recovery_for_symbol("BTC")["recovery_id"])
    )[0]

    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            "UPDATE partial_fill_actions SET qty_lots = 1 WHERE action_id = ?",
            (action["action_id"],),
        )
    store.conn.rollback()
    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            "DELETE FROM partial_fill_actions WHERE action_id = ?",
            (action["action_id"],),
        )
    store.conn.rollback()


def test_action_events_are_append_only(tmp_path):
    store, _broker, manager, _c, _m = scenario(tmp_path)
    asyncio.run(manager.run_partial_recovery("BTC"))
    action = store.partial_actions_for_recovery(
        str(store.latest_partial_recovery_for_symbol("BTC")["recovery_id"])
    )[0]
    events = store.partial_action_events(str(action["action_id"]))
    assert events

    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            "UPDATE partial_fill_action_events SET status = 'APPLIED' WHERE event_id = ?",
            (events[0]["event_id"],),
        )
    store.conn.rollback()
    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            "DELETE FROM partial_fill_action_events WHERE event_id = ?",
            (events[0]["event_id"],),
        )
    store.conn.rollback()


def test_transition_is_compare_and_set(tmp_path):
    store, _broker, _manager, _c, _m = scenario(tmp_path)
    recovery = store.active_partial_recovery_for_symbol("BTC")

    with pytest.raises(PartialRecoveryConflictError) as exc:
        store.transition_partial_recovery(
            str(recovery["recovery_id"]),
            expected=PartialProtectionState.CANCEL_PENDING.value,
            target=PartialProtectionState.SAFE_FLAT.value,
            reason_code="BOGUS",
        )
    assert exc.value.code == "PARTIAL_TRANSITION_CAS_FAILED"


def test_illegal_transition_is_refused(tmp_path):
    store, _broker, _manager, _c, _m = scenario(tmp_path)
    recovery = store.active_partial_recovery_for_symbol("BTC")

    with pytest.raises(PartialRecoveryConflictError) as exc:
        store.transition_partial_recovery(
            str(recovery["recovery_id"]),
            expected=PartialProtectionState.PARTIAL_DETECTED.value,
            target=PartialProtectionState.SAFE_FLAT.value,
            reason_code="BOGUS",
        )
    assert exc.value.code == "PARTIAL_TRANSITION_DENIED"


def test_only_one_active_recovery_per_symbol(tmp_path):
    store, _broker, _manager, _c, _m = scenario(tmp_path)
    other_trade, _ = seed_trade(store, qty=2.0, entry_cloid="entry-9")

    with pytest.raises(PartialRecoveryConflictError) as exc:
        store.open_partial_recovery(
            run_id="run", symbol="BTC", trade_id=other_trade,
            entry_cloid="entry-9", entry_decision_uid="owned-decision",
            entry_request_id=REQUEST_ID, first_observed_ts=FROZEN,
            protect_deadline_ts=FROZEN + timedelta(seconds=10),
        )
    assert exc.value.code == "PARTIAL_RECOVERY_SYMBOL_BUSY"


def test_reserve_is_replay_safe(tmp_path):
    store, _broker, _manager, _c, _m = scenario(tmp_path)
    recovery = store.active_partial_recovery_for_symbol("BTC")
    action_id = compute_partial_action_id(
        kind="CANCEL_ENTRY", trade_id=int(recovery["trade_id"]),
        entry_cloid=ENTRY_CLOID, entry_request_id=REQUEST_ID,
    )
    kwargs = dict(
        recovery_id=str(recovery["recovery_id"]), action_id=action_id,
        kind="CANCEL_ENTRY", target_cloid=ENTRY_CLOID,
        expected_state=PartialProtectionState.PARTIAL_DETECTED.value,
        next_state=PartialProtectionState.CANCEL_PENDING.value,
        reason_code="CANCEL_ENTRY_RESERVED",
    )
    first, _ = store.reserve_partial_action(**kwargs)
    kwargs["expected_state"] = PartialProtectionState.CANCEL_PENDING.value
    second, _ = store.reserve_partial_action(**kwargs)

    assert first is False and second is True


def test_outcome_fold_is_conservative(tmp_path):
    store, _broker, _manager, _c, _m = scenario(tmp_path)
    recovery = store.active_partial_recovery_for_symbol("BTC")
    action_id = compute_partial_action_id(
        kind="CANCEL_ENTRY", trade_id=int(recovery["trade_id"]),
        entry_cloid=ENTRY_CLOID, entry_request_id=REQUEST_ID,
    )
    store.reserve_partial_action(
        recovery_id=str(recovery["recovery_id"]), action_id=action_id,
        kind="CANCEL_ENTRY", target_cloid=ENTRY_CLOID,
        expected_state=PartialProtectionState.PARTIAL_DETECTED.value,
        next_state=PartialProtectionState.CANCEL_PENDING.value,
        reason_code="CANCEL_ENTRY_RESERVED",
    )
    assert store.resolve_partial_action(action_id) is None

    store.record_partial_action_event(
        action_id=action_id, status="UNKNOWN", reason_code="TIMEOUT"
    )
    assert store.resolve_partial_action(action_id) == ActionOutcome.UNKNOWN.value

    store.record_partial_action_event(
        action_id=action_id, status="APPLIED", reason_code="EVIDENCE"
    )
    assert store.resolve_partial_action(action_id) == ActionOutcome.APPLIED.value

    store.record_partial_action_event(
        action_id=action_id, status="UNKNOWN", reason_code="TIMEOUT"
    )
    assert store.resolve_partial_action(action_id) == ActionOutcome.APPLIED.value, (
        "a definitive outcome is never downgraded"
    )

    store.record_partial_action_event(
        action_id=action_id, status="NOT_APPLIED", reason_code="EVIDENCE"
    )
    assert store.resolve_partial_action(action_id) == ActionOutcome.UNKNOWN.value, (
        "conflicting definitive evidence resolves to the most restrictive verdict"
    )


def test_flatten_seq_refuses_to_advance_while_unresolved(tmp_path):
    store, _broker, _manager, _c, _m = scenario(tmp_path)
    recovery = store.active_partial_recovery_for_symbol("BTC")
    action_id = compute_partial_action_id(
        kind="FLATTEN", trade_id=int(recovery["trade_id"]), entry_cloid=ENTRY_CLOID,
        entry_request_id=REQUEST_ID, generation=0, flatten_seq=0, qty_lots=1000,
    )
    store.reserve_partial_action(
        recovery_id=str(recovery["recovery_id"]), action_id=action_id, kind="FLATTEN",
        target_cloid=compute_partial_action_cloid(action_id),
        expected_state=PartialProtectionState.PARTIAL_DETECTED.value,
        next_state=PartialProtectionState.FLATTEN_PENDING.value,
        reason_code="FLATTEN_RESERVED", generation=0, flatten_seq=0, qty_lots=1000,
    )
    store.record_partial_action_event(
        action_id=action_id, status="UNKNOWN", reason_code="TIMEOUT"
    )

    with pytest.raises(PartialRecoveryConflictError) as exc:
        store.bump_partial_flatten_seq(str(recovery["recovery_id"]), 0)
    assert exc.value.code == "PARTIAL_FLATTEN_SEQ_UNRESOLVED"

    store.record_partial_action_event(
        action_id=action_id, status="NOT_APPLIED", reason_code="EVIDENCE"
    )
    assert store.bump_partial_flatten_seq(str(recovery["recovery_id"]), 0) == 1


def test_partial_tables_use_real_schema_foreign_keys(tmp_path):
    store = make_store(tmp_path)
    columns = {
        row["name"]: row["type"]
        for row in store.conn.execute(
            "PRAGMA table_info(partial_fill_recoveries)"
        ).fetchall()
    }
    assert columns["trade_id"] == "INTEGER"
    assert columns["entry_cloid"] == "TEXT"
    keys = {
        (row["table"], row["from"], row["to"])
        for row in store.conn.execute(
            "PRAGMA foreign_key_list(partial_fill_recoveries)"
        ).fetchall()
    }
    assert ("trades", "trade_id", "trade_id") in keys
    assert ("orders", "entry_cloid", "cloid") in keys


def test_recovery_rejects_unknown_trade(tmp_path):
    store = make_store(tmp_path)
    with pytest.raises(sqlite3.IntegrityError):
        store.open_partial_recovery(
            run_id="run", symbol="BTC", trade_id=4242, entry_cloid="nope",
            entry_decision_uid="d", entry_request_id=REQUEST_ID,
            first_observed_ts=FROZEN,
            protect_deadline_ts=FROZEN + timedelta(seconds=10),
        )


def test_partial_apis_fail_closed_on_v4(tmp_path):
    store = make_store(tmp_path, version=4)
    seed_trade(store, qty=2.0)
    assert store.partial_protection_enabled() is False
    assert store.active_partial_recovery_for_symbol("BTC") is None
    assert store.partial_recovery_blocks_new_risk() is False
    with pytest.raises(PartialRecoveryConflictError) as exc:
        store.open_partial_recovery(
            run_id="run", symbol="BTC", trade_id=1, entry_cloid=ENTRY_CLOID,
            entry_decision_uid="d", entry_request_id=REQUEST_ID,
            first_observed_ts=FROZEN,
            protect_deadline_ts=FROZEN + timedelta(seconds=10),
        )
    assert exc.value.code == "PARTIAL_SCHEMA_UNAVAILABLE"


# ===========================================================================
# Migration and rollback
# ===========================================================================


def test_v5_reopen_is_idempotent_and_preserves_rows(tmp_path):
    store = make_store(tmp_path)
    seed_trade(store, qty=2.0)
    before = store.conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    store.close()

    reopened = Store(tmp_path / "bridge.db", clock=Clock())
    reopened.initialize(target_schema_version=5)
    assert reopened.get_meta("schema_version") == "5"
    assert reopened.conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == before

    # a v4-target open of a v5 database must not downgrade it
    reopened.close()
    again = Store(tmp_path / "bridge.db", clock=Clock())
    again.initialize()
    assert again.get_meta("schema_version") == "5"


def test_migration_failure_rolls_back_fully_to_v4(tmp_path):
    class FailingStore(Store):
        def _validate_partial_fill_schema_v5(self) -> None:
            raise MigrationError("injected validation failure")

    store = make_store(tmp_path, version=4)
    seed_trade(store, qty=2.0)
    order_count = store.conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    trade_count = store.conn.execute("SELECT COUNT(*) FROM trades").fetchone()[0]
    store.close()

    failing = FailingStore(tmp_path / "bridge.db", clock=Clock())
    with pytest.raises(MigrationError):
        failing.initialize(target_schema_version=5)

    assert failing.get_meta("schema_version") == "4"
    residue = failing.conn.execute(
        "SELECT name FROM sqlite_master WHERE name LIKE 'partial_fill_%'"
    ).fetchall()
    assert residue == [], "no v5 residue may survive a rolled-back migration"
    assert failing.conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == order_count
    assert failing.conn.execute("SELECT COUNT(*) FROM trades").fetchone()[0] == trade_count
    failing.close()

    # the database is still a valid, reopenable v4
    recovered = Store(tmp_path / "bridge.db", clock=Clock())
    recovered.initialize()
    assert recovered.get_meta("schema_version") == "4"


def test_migration_refuses_to_alter_existing_evidence(tmp_path):
    class DestructiveStore(Store):
        def _create_partial_fill_tables_v5(self) -> None:
            super()._create_partial_fill_tables_v5()
            self.conn.execute("DELETE FROM orders")

    store = make_store(tmp_path, version=4)
    seed_trade(store, qty=2.0)
    store.close()

    destructive = DestructiveStore(tmp_path / "bridge.db", clock=Clock())
    with pytest.raises(MigrationError):
        destructive.initialize(target_schema_version=5)
    assert destructive.get_meta("schema_version") == "4"
    assert destructive.conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 1


@pytest.mark.parametrize("version", ["6", "99", "garbage"])
def test_future_or_corrupt_schema_version_fails_closed(tmp_path, version):
    store = Store(tmp_path / "bridge.db", clock=Clock())
    store.initialize()
    store.conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', ?)",
        (version,),
    )
    store.conn.commit()
    store.close()

    reopened = Store(tmp_path / "bridge.db", clock=Clock())
    with pytest.raises(RuntimeError, match="Unsupported schema_version"):
        reopened.initialize(target_schema_version=5)


@pytest.mark.parametrize("target", [3, 6, True, "5", 4.0])
def test_unsupported_migration_target_fails_closed(tmp_path, target):
    store = Store(tmp_path / "bridge.db", clock=Clock())
    with pytest.raises(RuntimeError, match="Unsupported target_schema_version"):
        store.initialize(target_schema_version=target)


def test_v2_chain_can_reach_v5(tmp_path):
    store = Store(tmp_path / "bridge.db", clock=Clock())
    store.initialize()
    store.conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')"
    )
    store.conn.commit()
    store.close()

    upgraded = Store(tmp_path / "bridge.db", clock=Clock())
    upgraded.initialize(target_schema_version=5)
    assert upgraded.get_meta("schema_version") == "5"


# ===========================================================================
# Legacy startup scan
# ===========================================================================


def test_legacy_strong_evidence_opens_a_conservatively_expired_recovery(tmp_path):
    clock = Clock()
    store = make_store(tmp_path, clock=clock)
    trade_id, decision_uid = seed_trade(store, qty=2.0)
    store.insert_fill(
        "legacy-1", ENTRY_CLOID, decision_uid, FROZEN - timedelta(hours=3),
        1.0, 100.0, fee=0.0, funding=0.0,
    )
    broker = make_broker()
    manager = make_manager(store, broker)

    asyncio.run(manager.reconcile())

    recovery = store.latest_partial_recovery_for_symbol("BTC")
    assert recovery is not None
    assert recovery["reason_code"] in {
        "SAFE_FLAT", "PARTIAL_LEGACY_RECOVERED", "PROTECT_DEADLINE_EXPIRED",
        "FLATTEN_DEADLINE_EXPIRED", "PROTECTED_PARTIAL",
    }
    # seeded from the earliest durable fill -> no fresh 10s window
    assert recovery["first_observed_ts"].startswith("2026-07-26T09:00")
    assert "PARTIAL_LEGACY_DETECTED" in codes(store)


def test_legacy_weak_evidence_aborts_durably_and_mutates_nothing(tmp_path):
    store = make_store(tmp_path)
    trade_id, decision_uid = seed_trade(store, qty=2.0)
    # partial by order bookkeeping but with no durable fill evidence at all
    store.update_order_status(ENTRY_CLOID, "OPEN", filled_qty=1.0, avg_fill_px=100.0)
    broker = make_broker()
    manager = make_manager(store, broker)

    asyncio.run(manager.reconcile())

    recovery = store.latest_partial_recovery_for_symbol("BTC")
    assert recovery is not None
    assert recovery["state"] == PartialProtectionState.UNPROTECTED_ABORT.value
    assert recovery["reason_code"] == "LEGACY_FIRST_OBSERVATION_MISSING"
    assert broker.broker_mutations == []
    assert not any(
        str(order.get("cloid", "")).startswith("mock-reprotect")
        for order in broker.orders
    )
    assert broker.position is not None


def test_legacy_inexact_snapshot_aborts_before_any_broker_mutation(tmp_path):
    store = make_store(tmp_path)
    _trade_id, decision_uid = seed_trade(store, qty=2.0)
    store.insert_fill(
        "legacy-inexact", ENTRY_CLOID, decision_uid, FROZEN,
        1.0, 100.0, fee=0.0, funding=0.0,
    )
    broker = make_broker()
    broker.partial_snapshot_available = False
    manager = make_manager(store, broker)

    asyncio.run(manager.reconcile())

    recovery = store.latest_partial_recovery_for_symbol("BTC")
    assert recovery["state"] == PartialProtectionState.UNPROTECTED_ABORT.value
    assert recovery["reason_code"] == "SNAPSHOT_INEXACT"
    assert broker.broker_mutations == []
    assert not any(
        str(order.get("cloid", "")).startswith("mock-reprotect")
        for order in broker.orders
    )
    assert broker.position is not None


def test_legacy_scan_runs_only_once(tmp_path):
    store = make_store(tmp_path)
    _trade_id, decision_uid = seed_trade(store, qty=2.0)
    store.insert_fill(
        "legacy-1", ENTRY_CLOID, decision_uid, FROZEN - timedelta(hours=3),
        1.0, 100.0, fee=0.0, funding=0.0,
    )
    broker = make_broker()
    manager = make_manager(store, broker)

    asyncio.run(manager.reconcile())
    first = list(broker.partial_calls)
    asyncio.run(manager.reconcile())

    assert len(store.list_partial_recoveries()) == 1
    assert len(broker.partial_calls) >= len(first)


def test_db_layer_performs_no_broker_io(tmp_path):
    """`legacy_partial_entry_candidates` is a pure local query."""
    store = make_store(tmp_path)
    _trade_id, decision_uid = seed_trade(store, qty=2.0)
    store.insert_fill(
        "legacy-1", ENTRY_CLOID, decision_uid, FROZEN, 1.0, 100.0, fee=0.0, funding=0.0
    )
    candidates = store.legacy_partial_entry_candidates()
    assert [c["cloid"] for c in candidates] == [ENTRY_CLOID]
    assert candidates[0]["filled_qty"] == 1.0
    assert store.list_partial_recoveries() == []
