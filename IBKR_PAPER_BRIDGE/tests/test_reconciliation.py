"""TS-P1-005 full reconciliation — adversarial suite.

Every test here is written against the *contract*, not the implementation:
an incomplete, ambiguous, stale or unverifiable collection must never be
presented as a complete reconciliation, and only a complete internally valid
attempt may advance the accepted checkpoint.
"""

from __future__ import annotations

import asyncio
import json
import time
from datetime import UTC, datetime, timedelta

import pytest

from bridge.broker.mock import MockBroker
from bridge.engine.reconcile import FullReconciler
from bridge.engine.risk import RiskEngine
from bridge.engine.types import (
    DIFF_EXCHANGE_IDENTITY_CONFLICT,
    ReconcileAttemptState,
    ReconcileComponentKind,
)
from bridge.store.db import (
    SCHEMA_VERSION_EXPOSURE_CONTROLS,
    SCHEMA_VERSION_FULL_RECONCILE,
    Store,
)


def test_v8_checkpoint_policy_hash_accepts_and_reopens(tmp_path):
    db_path = tmp_path / "v8-policy-hash.db"
    store = Store(db_path)
    store.initialize(target_schema_version=SCHEMA_VERSION_EXPOSURE_CONTROLS)
    store.create_run("v8-hash", "dry_run", "testnet", {})
    risk = RiskEngine()
    result = asyncio.run(
        FullReconciler(
            store=store,
            broker=MockBroker(bars=[]),
            run_id="v8-hash",
            risk_policy=risk.policy,
            exposure_policy=risk.exposure_policy,
        ).run_cycle()
    )
    assert result.accepted is True
    pointer = store.get_meta("reconcile_checkpoint_latest")
    assert pointer
    store.close()

    reopened = Store(db_path)
    reopened.initialize(target_schema_version=SCHEMA_VERSION_EXPOSURE_CONTROLS)
    snapshot = reopened.load_authoritative_risk_snapshot(
        now=result.ended_ts, max_age_s=60.0
    )
    assert snapshot.checkpoint_id == pointer
    assert snapshot.exposure_policy_version == risk.exposure_policy.version
    reopened.close()

BASE_TS = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
# The run's durable start is the very first fills/funding coverage lower bound
# (there is no fixed lookback), so it is pinned to the deterministic clock
# instead of the wall clock `create_run()` records.
RUN_STARTED_TS = BASE_TS - timedelta(hours=1)


class FrozenClock:
    """Deterministic UTC clock plus an independent monotonic source."""

    def __init__(self, start: datetime = BASE_TS, mono: float = 1_000.0) -> None:
        self.utc = start
        self.mono = mono

    def now(self) -> datetime:
        return self.utc

    def monotonic(self) -> float:
        return self.mono

    def advance(self, seconds: float) -> None:
        self.utc = self.utc + timedelta(seconds=seconds)
        self.mono += seconds


def open_store(path, *, version: int = SCHEMA_VERSION_FULL_RECONCILE) -> Store:
    store = Store(path)
    store.initialize(target_schema_version=version)
    return store


def seed_owned_order(
    store: Store,
    *,
    run_id: str = "run-recon",
    cloid: str = "0xowned0001",
    symbol: str = "BTC",
    qty: float = 0.100,
    status: str = "OPEN",
    filled_qty: float = 0.0,
    oid: int = 1,
    role: str = "ENTRY",
) -> int:
    """One durable owned entry order with its trade lineage."""
    if store.get_meta(f"seeded:{run_id}") is None:
        store.create_run(run_id, mode="dry_run", network="testnet", config={})
        store.conn.execute(
            "UPDATE runs SET started_ts = ? WHERE run_id = ?",
            (RUN_STARTED_TS.isoformat(), run_id),
        )
        store.conn.commit()
        store.set_meta(f"seeded:{run_id}", "1")
    decision_uid = f"decision-{cloid}"
    store.insert_decision(run_id, decision_uid, BASE_TS, symbol, "SIGNAL", {})
    trade_id = store.create_trade(
        run_id=run_id,
        coin=symbol,
        direction="LONG",
        qty=qty,
        entry_decision_uid=decision_uid,
        signal_ts=BASE_TS,
        decision_ts=BASE_TS,
        expected_px=100.0,
        risk_dollars=10.0,
        risk_pct=0.01,
        leverage=1,
        sl_initial=90.0,
        tp_initial=None,
        llm_directive_id=None,
    )
    store.insert_order(
        cloid=cloid,
        oid=oid,
        group_id=decision_uid,
        order_ref=f"ref-{cloid}",
        order_json={"symbol": symbol, "qty": qty},
        decision_uid=decision_uid,
        trade_id=trade_id,
        role=role,
        status=status,
        qty=qty,
        filled_qty=filled_qty,
        ts_submit=BASE_TS,
        ts_last=BASE_TS,
    )
    return trade_id


def healthy_broker(*, cloid: str = "0xowned0001", symbol: str = "BTC") -> MockBroker:
    broker = MockBroker(bars=[], coin=symbol)
    broker.full_open_orders = [
        {
            "cloid": cloid,
            "oid": 1,
            "coin": symbol,
            "side": "BUY",
            "sz": 0.100,
            "role": "ENTRY",
            "reduceOnly": False,
            "status": "OPEN",
        }
    ]
    broker.full_positions = []
    broker.full_account = {
        "equity": 10_000.0,
        "withdrawable": 9_000.0,
        "margin_used": 1_000.0,
        "available_margin": 9_000.0,
    }
    broker.full_fill_history = []
    broker.full_funding_history = []
    return broker


def build_reconciler(store: Store, broker: MockBroker, clock: FrozenClock) -> FullReconciler:
    # The fake exchange shares the deterministic clock: source timestamps are
    # then explicit test inputs rather than wall-clock noise.
    broker.full_clock = clock.now
    return FullReconciler(
        store=store,
        broker=broker,
        run_id="run-recon",
        clock=clock.now,
        monotonic=clock.monotonic,
    )


def test_repair4_a14_in_epoch_capture_is_additive_to_full_reconcile(tmp_path):
    assert hasattr(
        FullReconciler, "capture_kill_evidence"
    ), "in-epoch capture seam is missing"
    store = open_store(
        tmp_path / "repair4-additive-capture.db",
        version=SCHEMA_VERSION_EXPOSURE_CONTROLS,
    )
    seed_owned_order(store)
    store.initialize(target_schema_version=9)
    broker = healthy_broker()
    clock = FrozenClock()
    reconciler = build_reconciler(store, broker, clock)
    request, epoch = store.open_kill_epoch(
        run_id="run-recon",
        symbol="BTC",
        flatten_requested=False,
        policy_version="policy-v1",
        process_uid="repair4-capture",
        opened_ts_monotonic=clock.monotonic(),
    )
    assert request["episode_id"] == epoch.episode_id
    before_count = store.count_accepted_reconcile_checkpoints()
    before_deadline = reconciler.deadline_s

    capture = asyncio.run(
        reconciler.capture_kill_evidence(
            epoch=epoch,
            symbol="BTC",
            start_ms=int(RUN_STARTED_TS.timestamp() * 1000),
            end_ms=int(clock.now().timestamp() * 1000),
        )
    )

    assert capture.epoch == epoch
    assert capture.accepted is True
    assert store.count_accepted_reconcile_checkpoints() == before_count
    assert reconciler.deadline_s == before_deadline

    result = run_cycle(store, broker, clock)
    assert result.accepted is True
    assert store.count_accepted_reconcile_checkpoints() == before_count + 1
    assert store.full_reconcile_ready(now=clock.now(), max_age_s=30.0) is True


# ---------------------------------------------------------------------------
# Predecessor RED 1 — complete deterministic capture
# ---------------------------------------------------------------------------


def test_red1_complete_capture_is_order_independent_and_survives_reopen(tmp_path):
    """Same evidence in different row order → byte-stable hash, one checkpoint."""
    hashes: list[str] = []
    checkpoints: list[str] = []

    for index, reversed_rows in enumerate((False, True)):
        db_path = tmp_path / f"bridge-{index}.db"
        store = open_store(db_path)
        seed_owned_order(store)
        broker = healthy_broker()
        broker.full_row_order_reversed = reversed_rows
        broker.full_open_orders = list(broker.full_open_orders) + [
            {
                "cloid": "0xowned0002",
                "oid": 2,
                "coin": "BTC",
                "side": "SELL",
                "sz": 0.100,
                "role": "SL",
                "reduceOnly": True,
                "status": "OPEN",
            }
        ]
        seed_owned_order(store, cloid="0xowned0002", oid=2, role="SL")
        clock = FrozenClock()
        result = asyncio.run(build_reconciler(store, broker, clock).run_cycle())

        assert result.state is ReconcileAttemptState.COMPLETE, result.reason_code
        assert result.accepted is True
        hashes.append(result.canonical_hash)

        accepted = store.latest_accepted_reconcile_checkpoint()
        assert accepted is not None
        assert accepted["canonical_hash"] == result.canonical_hash
        assert (
            store.count_accepted_reconcile_checkpoints() == 1
        ), "exactly one accepted checkpoint per complete cycle"

        store.close()
        reopened = open_store(db_path)
        reopened_checkpoint = reopened.latest_accepted_reconcile_checkpoint()
        assert reopened_checkpoint is not None
        assert reopened_checkpoint["canonical_hash"] == result.canonical_hash
        checkpoints.append(reopened_checkpoint["canonical_hash"])
        reopened.close()

    assert hashes[0] == hashes[1], "canonical hash must not depend on row order"
    assert checkpoints[0] == checkpoints[1]


# ---------------------------------------------------------------------------
# Predecessor RED 2 — missing component
# ---------------------------------------------------------------------------


def test_red2_missing_fills_component_blocks_and_retains_prior_checkpoint(tmp_path):
    """Orders succeed, fills endpoint fails → INCOMPLETE, prior pointer kept."""
    db_path = tmp_path / "bridge.db"
    store = open_store(db_path)
    seed_owned_order(store)
    clock = FrozenClock()

    good = healthy_broker()
    accepted_result = asyncio.run(build_reconciler(store, good, clock).run_cycle())
    assert accepted_result.accepted is True
    baseline = store.latest_accepted_reconcile_checkpoint()
    assert baseline is not None

    clock.advance(30.0)
    broken = healthy_broker()
    broken.full_component_failures = {ReconcileComponentKind.FILLS.value: "RAISE"}
    failed = asyncio.run(build_reconciler(store, broken, clock).run_cycle())

    assert failed.state is ReconcileAttemptState.INCOMPLETE
    assert failed.accepted is False
    assert failed.reason_code != "NONE"

    still = store.latest_accepted_reconcile_checkpoint()
    assert still is not None
    assert still["attempt_id"] == baseline["attempt_id"]
    assert still["canonical_hash"] == baseline["canonical_hash"]

    store.close()
    reopened = open_store(db_path)
    attempt = reopened.get_reconcile_attempt(failed.attempt_id)
    assert attempt is not None
    assert attempt["state"] == ReconcileAttemptState.INCOMPLETE.value
    components = {
        row["component"]: row
        for row in reopened.get_reconcile_components(failed.attempt_id)
    }
    assert ReconcileComponentKind.FILLS.value in components
    assert components[ReconcileComponentKind.FILLS.value]["status"] != "COMPLETE"
    assert (
        reopened.latest_accepted_reconcile_checkpoint()["attempt_id"]
        == baseline["attempt_id"]
    )
    reopened.close()


# ---------------------------------------------------------------------------
# Predecessor RED 3 — partial failure / crash boundary
# ---------------------------------------------------------------------------


def test_red3_crash_after_reserve_leaves_no_partial_checkpoint(tmp_path):
    """A crash mid-collection may never publish a half-current snapshot."""
    db_path = tmp_path / "bridge.db"
    store = open_store(db_path)
    seed_owned_order(store)
    clock = FrozenClock()

    good = healthy_broker()
    baseline_result = asyncio.run(build_reconciler(store, good, clock).run_cycle())
    assert baseline_result.accepted is True
    baseline = store.latest_accepted_reconcile_checkpoint()
    assert baseline is not None

    clock.advance(30.0)
    crashing = healthy_broker()
    # BaseException — a real process kill, not a handled adapter failure.
    crashing.full_component_failures = {
        ReconcileComponentKind.POSITIONS.value: "CRASH"
    }
    with pytest.raises(KeyboardInterrupt):
        asyncio.run(build_reconciler(store, crashing, clock).run_cycle())

    store.close()
    reopened = open_store(db_path)
    resolved = reopened.resolve_interrupted_reconcile_attempts(
        observed_ts=clock.now() + timedelta(seconds=1)
    )
    assert resolved == 1
    interrupted = [
        row
        for row in reopened.list_reconcile_attempts()
        if row["attempt_id"] != baseline["attempt_id"]
    ]
    assert interrupted, "the reserved attempt must remain visible"
    assert all(
        row["state"] == ReconcileAttemptState.INCOMPLETE.value for row in interrupted
    )
    pointer = reopened.latest_accepted_reconcile_checkpoint()
    assert pointer["attempt_id"] == baseline["attempt_id"]
    assert pointer["canonical_hash"] == baseline["canonical_hash"]
    assert reopened.count_accepted_reconcile_checkpoints() == 1
    reopened.close()


# ---------------------------------------------------------------------------
# Shared adversarial helpers
# ---------------------------------------------------------------------------


def run_cycle(store: Store, broker: MockBroker, clock: FrozenClock):
    return asyncio.run(build_reconciler(store, broker, clock).run_cycle())


def diff_codes(result) -> set[str]:
    return {diff.reason_code for diff in result.diffs}


def blocking_codes(result) -> set[str]:
    return {diff.reason_code for diff in result.blocking_diffs}


class SequenceClock(FrozenClock):
    """UTC clock that replays a fixed sequence, repeating the final value."""

    def __init__(self, values: list[datetime], mono: float = 1_000.0) -> None:
        super().__init__(values[0], mono)
        self._values = list(values)
        self._index = 0

    def now(self) -> datetime:
        value = self._values[min(self._index, len(self._values) - 1)]
        self._index += 1
        return value


class RushingClock(FrozenClock):
    """Monotonic source that burns ten seconds on every observation."""

    def monotonic(self) -> float:
        self.mono += 10.0
        return self.mono


# ---------------------------------------------------------------------------
# Component completeness
# ---------------------------------------------------------------------------


def test_truncated_page_fails_closed_and_publishes_no_checkpoint(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    broker.full_component_failures = {ReconcileComponentKind.FILLS.value: "TRUNCATED"}
    result = run_cycle(store, broker, FrozenClock())

    assert result.state is ReconcileAttemptState.INCOMPLETE
    assert result.reason_code == "FILLS_TRUNCATED"
    assert store.latest_accepted_reconcile_checkpoint() is None
    row = next(
        item
        for item in store.get_reconcile_components(result.attempt_id)
        if item["component"] == ReconcileComponentKind.FILLS.value
    )
    assert row["status"] == "TRUNCATED"
    assert row["complete"] == 0
    store.close()


def test_malformed_component_never_defaults_to_empty(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    broker.full_component_failures = {
        ReconcileComponentKind.POSITIONS.value: "MALFORMED"
    }
    result = run_cycle(store, broker, FrozenClock())

    assert result.accepted is False
    assert result.reason_code == "POSITIONS_MALFORMED"
    assert store.count_accepted_reconcile_checkpoints() == 0
    store.close()


def test_missing_observation_timestamp_blocks(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    broker.full_component_failures = {ReconcileComponentKind.FUNDING.value: "NO_TS"}
    result = run_cycle(store, broker, FrozenClock())

    assert result.accepted is False
    assert result.state is ReconcileAttemptState.INCOMPLETE
    store.close()


# ---------------------------------------------------------------------------
# Deadline / freshness envelope (D2=A)
# ---------------------------------------------------------------------------


def test_deadline_exceeded_fails_closed(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    result = run_cycle(store, healthy_broker(), RushingClock())

    assert result.state is ReconcileAttemptState.STALE
    assert result.reason_code == "FULL_RECONCILE_DEADLINE_EXCEEDED"
    assert store.latest_accepted_reconcile_checkpoint() is None
    store.close()


def test_wall_clock_rollback_fails_closed(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    clock = SequenceClock([BASE_TS, BASE_TS, BASE_TS - timedelta(seconds=60)])
    result = run_cycle(store, healthy_broker(), clock)

    assert result.state is ReconcileAttemptState.STALE
    assert result.reason_code == "FULL_RECONCILE_CLOCK_ROLLBACK"
    store.close()


def test_component_source_skew_beyond_envelope_fails_closed(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    broker.full_observed_offsets_s = {ReconcileComponentKind.FILLS.value: 30.0}
    result = run_cycle(store, broker, FrozenClock())

    assert result.state is ReconcileAttemptState.STALE
    assert result.reason_code == "FULL_RECONCILE_SOURCE_SKEW"
    store.close()


def test_broker_client_rebuild_mid_capture_fails_closed(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)

    class RebuildingBroker(MockBroker):
        async def open_orders_evidence(self):
            evidence = await super().open_orders_evidence()
            # The adapter swapped its SDK clients between two reads.
            self.info = object()
            return evidence

    template = healthy_broker()
    broker = RebuildingBroker(bars=[], coin="BTC")
    broker.info = object()
    broker.exchange = object()
    broker.full_open_orders = [dict(row) for row in template.full_open_orders]
    broker.full_positions = []
    result = run_cycle(store, broker, FrozenClock())

    assert result.state is ReconcileAttemptState.STALE
    assert result.reason_code == "FULL_RECONCILE_CLIENT_REBUILT"
    store.close()


def test_bounded_rest_call_budget_is_four_reads(tmp_path):
    """D2=A offline budget proof: one capture issues four bounded reads."""
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    result = run_cycle(store, broker, FrozenClock())

    assert result.accepted is True
    assert broker.full_calls == [
        "portfolio_evidence",
        "open_orders_evidence",
        "fills_evidence",
        "funding_evidence",
    ]
    total_calls = sum(component.call_count for component in result.components)
    assert total_calls == 4
    store.close()


# ---------------------------------------------------------------------------
# Ownership and divergence (D1=B)
# ---------------------------------------------------------------------------


def test_owned_order_missing_on_exchange_blocks(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    broker.full_open_orders = []
    result = run_cycle(store, broker, FrozenClock())

    assert result.state is ReconcileAttemptState.CONFLICTING
    assert "OWNED_ORDER_MISSING_ON_EXCHANGE" in blocking_codes(result)
    assert store.latest_accepted_reconcile_checkpoint() is None
    store.close()


def test_owned_order_quantity_compared_in_exact_lots(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    broker.full_open_orders[0]["sz"] = 0.101
    result = run_cycle(store, broker, FrozenClock())
    assert "OWNED_ORDER_QTY_MISMATCH" in blocking_codes(result)

    # The same economic size spelled differently is not a mismatch.
    store2 = open_store(tmp_path / "bridge2.db")
    seed_owned_order(store2)
    broker2 = healthy_broker()
    broker2.full_open_orders[0]["sz"] = 0.1000
    result2 = run_cycle(store2, broker2, FrozenClock())
    assert result2.accepted is True, result2.reason_code
    store.close()
    store2.close()


def test_unknown_size_quantum_blocks_affected_classification(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    broker.partial_size_decimals = None
    result = run_cycle(store, broker, FrozenClock())

    assert result.accepted is False
    assert "OWNED_ORDER_SIZE_QUANTUM_UNKNOWN" in blocking_codes(result)
    store.close()


def test_identified_foreign_order_is_observe_only(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    broker.full_open_orders.append({
        "cloid": "0xforeign999",
        "oid": 77,
        "coin": "BTC",
        "side": "BUY",
        "sz": 5.0,
        "role": "UNKNOWN",
        "reduceOnly": False,
        "status": "OPEN",
    })
    before = list(broker.orders)
    result = run_cycle(store, broker, FrozenClock())

    assert result.accepted is True, result.reason_code
    assert "FOREIGN_ORDER_OBSERVED" in diff_codes(result)
    assert not result.blocking_diffs
    # Zero mutation of foreign state.
    assert broker.orders == before
    assert broker.partial_calls == []
    store.close()


def test_order_without_identity_is_unknown_ownership(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    broker.full_open_orders.append({
        "cloid": "",
        "oid": 78,
        "coin": "BTC",
        "side": "BUY",
        "sz": 1.0,
        "reduceOnly": False,
        "status": "OPEN",
    })
    result = run_cycle(store, broker, FrozenClock())

    assert result.accepted is False
    assert result.reason_code == "OPEN_ORDERS_UNAVAILABLE"
    store.close()


def test_unattributable_position_blocks(tmp_path):
    """A position carries no cloid: without lineage it is never 'foreign'."""
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    broker.full_positions = [{"symbol": "ETH", "size": 2.0}]
    result = run_cycle(store, broker, FrozenClock())

    assert result.accepted is False
    assert "UNKNOWN_OWNERSHIP_POSITION" in blocking_codes(result)
    store.close()


def test_position_quantity_mismatch_blocks(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    trade_id = seed_owned_order(store, status="FILLED", filled_qty=0.100)
    broker = healthy_broker()
    broker.full_open_orders = []
    broker.full_positions = [{"symbol": "BTC", "size": 0.050}]
    result = run_cycle(store, broker, FrozenClock())

    assert trade_id > 0
    assert result.accepted is False
    assert "POSITION_QTY_MISMATCH" in blocking_codes(result)
    store.close()


def test_account_arithmetic_conflict_blocks(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    broker.full_account = {
        "equity": 1_000.0,
        "withdrawable": 1_500.0,   # more withdrawable than equity
        "margin_used": 100.0,
        "available_margin": 900.0,
    }
    result = run_cycle(store, broker, FrozenClock())

    assert result.accepted is False
    assert "ACCOUNT_ARITHMETIC_INCONSISTENT" in blocking_codes(result)
    store.close()


# ---------------------------------------------------------------------------
# Human gates keep their authority
# ---------------------------------------------------------------------------


def seed_quarantine(store: Store, *, attempt_id: str = "attempt-v1:" + "a" * 64) -> None:
    intent_id = "intent-v1:" + "b" * 64
    request_id = "request-v1:" + "c" * 64
    store.conn.execute(
        """INSERT INTO order_identity(
             intent_id, intent_preimage, request_id, request_preimage, cloid_seed,
             origin_run_id, origin_decision_uid, state, reserved_ts)
           VALUES (?, 'p', ?, 'p', 'seed', 'run-recon', 'decision-q', 'RESERVED', ?)""",
        (intent_id, request_id, BASE_TS.isoformat()),
    )
    store.conn.execute(
        """INSERT INTO submission_attempts(
             attempt_id, intent_id, request_id, origin_run_id, origin_decision_uid,
             state, recovery_payload_json, planned_cloids_json, created_ts,
             updated_ts, reason_code)
           VALUES (?, ?, ?, 'run-recon', 'decision-q', 'UNKNOWN_SUBMISSION',
                   '{}', '{}', ?, ?, 'UNKNOWN_SUBMISSION')""",
        (attempt_id, intent_id, request_id, BASE_TS.isoformat(), BASE_TS.isoformat()),
    )
    store.conn.commit()


def test_active_quarantine_blocks_and_is_never_cleared(tmp_path):
    db_path = tmp_path / "bridge.db"
    store = open_store(db_path)
    seed_owned_order(store)
    seed_quarantine(store)
    assert store.has_submission_quarantine() is True

    result = run_cycle(store, healthy_broker(), FrozenClock())
    assert result.accepted is False
    assert "PENDING_ACTION_DIVERGENCE" in blocking_codes(result)
    assert store.has_submission_quarantine() is True
    store.close()

    reopened = open_store(db_path)
    assert reopened.has_submission_quarantine() is True
    assert reopened.latest_accepted_reconcile_checkpoint() is None
    reopened.close()


def test_active_partial_recovery_blocks_readiness(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    trade_id = seed_owned_order(store)
    store.open_partial_recovery(
        run_id="run-recon",
        symbol="BTC",
        trade_id=trade_id,
        entry_cloid="0xowned0001",
        entry_decision_uid="decision-0xowned0001",
        entry_request_id="request-v1:" + "d" * 64,
        first_observed_ts=BASE_TS,
        protect_deadline_ts=BASE_TS + timedelta(seconds=60),
    )
    assert store.partial_recovery_blocks_new_risk() is True

    result = run_cycle(store, healthy_broker(), FrozenClock())
    assert result.accepted is False
    assert "PENDING_ACTION_DIVERGENCE" in blocking_codes(result)
    assert store.partial_recovery_blocks_new_risk() is True
    store.close()


# ---------------------------------------------------------------------------
# Funding ledger (D3=A)
# ---------------------------------------------------------------------------


def funding_row(
    *,
    event_hash: str,
    coin: str = "BTC",
    usdc: float = -1.25,
    time_ms: int | None = None,
) -> dict:
    """One authoritative ``userFunding`` record shape."""
    return {
        "hash": event_hash,
        "time": (
            time_ms
            if time_ms is not None
            else int(BASE_TS.timestamp() * 1000) - 1000
        ),
        "delta": {
            "coin": coin,
            "fundingRate": "0.0000125",
            "szi": "0.1",
            "type": "funding",
            "usdc": str(usdc),
            "nSamples": 1,
        },
    }


def healthy_broker_with(source: MockBroker) -> MockBroker:
    fresh = healthy_broker()
    fresh.full_funding_history = list(source.full_funding_history)
    return fresh


def test_funding_events_are_recorded_once_and_replay_is_idempotent(tmp_path):
    db_path = tmp_path / "bridge.db"
    store = open_store(db_path)
    seed_owned_order(store)
    broker = healthy_broker()
    broker.full_funding_history = [
        funding_row(event_hash="0xfund1"),
        funding_row(event_hash="0xfund1"),   # exact duplicate
        funding_row(event_hash="0xfund2", usdc=0.75),
    ]
    clock = FrozenClock()
    first = run_cycle(store, broker, clock)
    assert first.accepted is True, first.reason_code
    assert len(store.list_funding_events()) == 2

    clock.advance(30.0)
    second = run_cycle(store, healthy_broker_with(broker), clock)
    assert second.accepted is True
    assert len(store.list_funding_events()) == 2
    assert store.funding_total(symbol="BTC") == pytest.approx(-0.5)
    store.close()

    reopened = open_store(db_path)
    assert len(reopened.list_funding_events()) == 2
    assert reopened.funding_total(symbol="BTC") == pytest.approx(-0.5)
    reopened.close()


def test_conflicting_funding_identity_blocks(tmp_path):
    db_path = tmp_path / "bridge.db"
    store = open_store(db_path)
    seed_owned_order(store)
    broker = healthy_broker()
    broker.full_funding_history = [
        funding_row(event_hash="0xfund1", usdc=-1.0),
        funding_row(event_hash="0xfund1", usdc=-9.0),  # same identity, new amount
    ]
    result = run_cycle(store, broker, FrozenClock())

    assert result.state is ReconcileAttemptState.CONFLICTING
    assert result.accepted is False
    assert store.list_funding_events() == []
    persisted = store.get_reconcile_diffs(result.attempt_id)
    assert len(persisted) == 1
    conflict_payload = __import__("json").loads(persisted[0]["payload_json"])
    assert len(conflict_payload["exchange"]["observations"]) == 2
    assert len(set(conflict_payload["exchange"]["observation_digests"])) == 2
    store.close()

    reopened = open_store(db_path)
    persisted_after_restart = reopened.get_reconcile_diffs(result.attempt_id)
    assert persisted_after_restart == persisted
    reopened.close()


def test_cross_attempt_funding_identity_drift_retains_both_observations(tmp_path):
    db_path = tmp_path / "bridge.db"
    store = open_store(db_path)
    seed_owned_order(store)
    clock = FrozenClock()
    first_broker = healthy_broker()
    first_broker.full_funding_history = [
        funding_row(
            event_hash="0xcross",
            usdc=-1.0,
            time_ms=int(BASE_TS.timestamp() * 1000),
        )
    ]
    first = run_cycle(store, first_broker, clock)
    assert first.accepted is True

    clock.advance(30)
    second_broker = healthy_broker()
    second_broker.full_funding_history = [
        funding_row(
            event_hash="0xcross",
            usdc=-9.0,
            time_ms=int(BASE_TS.timestamp() * 1000),
        )
    ]
    second = run_cycle(store, second_broker, clock)
    assert second.accepted is False
    assert DIFF_EXCHANGE_IDENTITY_CONFLICT in blocking_codes(second)
    persisted = store.get_reconcile_diffs(second.attempt_id)
    payload = __import__("json").loads(persisted[0]["payload_json"])
    assert payload["local"]["amount_usdc"] == -1.0
    assert payload["exchange"]["amount_usdc"] == -9.0
    assert payload["local"]["payload_digest"] != payload["exchange"]["payload_digest"]
    store.close()

    reopened = open_store(db_path)
    assert reopened.get_reconcile_diffs(second.attempt_id) == persisted
    reopened.close()


def test_fill_reconciliation_blocks_wrong_symbol_and_cumulative_overfill(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store, qty=0.100)
    broker = healthy_broker()
    ts_ms = int(BASE_TS.timestamp() * 1000)
    broker.full_fill_history = [
        {
            "hash": "0xf1",
            "oid": 1,
            "coin": "ETH",
            "side": "B",
            "sz": 0.060,
            "px": 100.0,
            "time": ts_ms,
        },
        {
            "hash": "0xf2",
            "oid": 1,
            "coin": "BTC",
            "side": "B",
            "sz": 0.060,
            "px": 100.0,
            "time": ts_ms,
        },
    ]
    result = run_cycle(store, broker, FrozenClock())
    assert result.accepted is False
    assert DIFF_EXCHANGE_IDENTITY_CONFLICT in blocking_codes(result)
    store.close()


def test_unattributed_funding_blocks_but_is_still_retained(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    broker.full_funding_history = [funding_row(event_hash="0xfundX", coin="SOL")]
    result = run_cycle(store, broker, FrozenClock())

    assert result.accepted is False
    assert "FUNDING_UNATTRIBUTED" in blocking_codes(result)
    # Ambiguous attribution blocks readiness; the evidence is not discarded.
    assert [row["attribution"] for row in store.list_funding_events()] == [
        "UNATTRIBUTED"
    ]
    assert store.funding_total() == 0.0
    store.close()


def test_attribution_change_is_not_a_funding_identity_conflict(tmp_path):
    """The same exchange event, UNATTRIBUTED then ATTRIBUTED, stays one row.

    Attribution is derived from local owned-order lineage, so it must not take
    part in the append-only identity digest. If it did, the very next capture
    after the lineage appeared would reject an *untouched* exchange event as a
    conflicting redefinition of itself and lose the whole evidence write.
    """
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)  # BTC lineage only
    clock = FrozenClock()

    sol_funding = [funding_row(event_hash="0xsolfund", coin="SOL")]
    broker = healthy_broker()
    broker.full_funding_history = list(sol_funding)
    first = run_cycle(store, broker, clock)

    assert first.accepted is False
    assert "FUNDING_UNATTRIBUTED" in blocking_codes(first)
    stored = store.list_funding_events()
    assert [row["attribution"] for row in stored] == ["UNATTRIBUTED"]
    first_digest = stored[0]["payload_digest"]

    # Owned SOL lineage now exists, so the identical event is ATTRIBUTED.
    clock.advance(30.0)
    seed_owned_order(store, cloid="0xowned0sol", symbol="SOL", oid=3)
    later = healthy_broker()
    later.full_open_orders = list(later.full_open_orders) + [
        {
            "cloid": "0xowned0sol",
            "oid": 3,
            "coin": "SOL",
            "side": "BUY",
            "sz": 0.100,
            "role": "ENTRY",
            "reduceOnly": False,
            "status": "OPEN",
        }
    ]
    later.full_funding_history = list(sol_funding)
    second = run_cycle(store, later, clock)

    assert second.accepted is True, second.reason_code
    assert "FUNDING_UNATTRIBUTED" not in blocking_codes(second)
    assert second.reason_code != "FULL_RECONCILE_EVIDENCE_WRITE_FAILED"
    attempt = store.get_reconcile_attempt(second.attempt_id)
    assert attempt["reason_code"] == "ACCEPTED"

    rows = store.list_funding_events()
    assert len(rows) == 1, "one exchange event is exactly one ledger row"
    assert rows[0]["payload_digest"] == first_digest, (
        "the identity digest may only hash exchange-authoritative content"
    )
    # The column keeps the durable first-seen attribution; the digest never
    # carried it, so re-observing the event is a no-op instead of a conflict.
    assert rows[0]["attribution"] == "UNATTRIBUTED"
    store.close()


def test_funding_ledger_does_not_change_the_interim_risk_result(tmp_path):
    """Interim TS-P1-007 gross-minus-fees stays numerically identical (D017)."""
    db_path = tmp_path / "bridge.db"
    store = open_store(db_path)
    seed_owned_order(store)
    store.insert_fill(
        fill_id="fill-1",
        cloid="0xowned0001",
        decision_uid="decision-0xowned0001",
        fill_ts=BASE_TS,
        qty=0.1,
        px=100.0,
        fee=0.25,
        funding=0.0,
    )
    before = store.trade_costs("decision-0xowned0001")

    broker = healthy_broker()
    broker.full_fill_history = [
        {
            "fill_id": "fill-1",
            "oid": 1,
            "coin": "BTC",
            "side": "BUY",
            "sz": 0.1,
            "px": 100.0,
            "time": int(BASE_TS.timestamp() * 1000),
        }
    ]
    broker.full_funding_history = [
        funding_row(event_hash="0xfundA", usdc=-3.5),
        funding_row(event_hash="0xfundB", usdc=-7.5),
    ]
    result = run_cycle(store, broker, FrozenClock())
    assert result.accepted is True, result.reason_code
    assert len(store.list_funding_events()) == 2

    after = store.trade_costs("decision-0xowned0001")
    assert after == before == pytest.approx(0.25)
    store.close()

    reopened = open_store(db_path)
    assert reopened.trade_costs("decision-0xowned0001") == pytest.approx(0.25)
    assert reopened.funding_total(symbol="BTC") == pytest.approx(-11.0)
    reopened.close()


# ---------------------------------------------------------------------------
# Concurrency: one full writer, and light reconcile can never upgrade
# ---------------------------------------------------------------------------


def test_overlapping_full_attempts_are_refused(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)

    class SlowBroker(MockBroker):
        async def portfolio_evidence(self):
            await asyncio.sleep(0)
            await asyncio.sleep(0)
            return await super().portfolio_evidence()

    template = healthy_broker()

    def make() -> MockBroker:
        broker = SlowBroker(bars=[], coin="BTC")
        broker.full_open_orders = [dict(row) for row in template.full_open_orders]
        broker.full_positions = []
        broker.full_account = dict(template.full_account)
        return broker

    clock = FrozenClock()
    first = build_reconciler(store, make(), clock)
    second = build_reconciler(store, make(), clock)

    async def both():
        return await asyncio.gather(first.run_cycle(), second.run_cycle())

    results = asyncio.run(both())
    assert "FULL_RECONCILE_OVERLAP" in {result.reason_code for result in results}
    assert sum(1 for result in results if result.accepted) == 1
    assert store.count_accepted_reconcile_checkpoints() == 1
    # Both outcomes survive as evidence.
    assert len(store.list_reconcile_attempts()) == 2
    store.close()


def test_light_reconcile_alone_never_grants_full_readiness(tmp_path):
    from bridge.engine.orders import OrderManager

    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    manager = OrderManager(store, broker, "run-recon")

    asyncio.run(manager.reconcile())

    assert store.latest_accepted_reconcile_checkpoint() is None
    assert store.full_reconcile_ready(now=BASE_TS, max_age_s=900.0) is False
    store.close()


def test_light_reconcile_cannot_interleave_with_full_epoch_guard(tmp_path):
    from bridge.engine.orders import OrderManager
    from bridge.engine.reconcile import full_writer_guard

    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    manager = OrderManager(store, broker, "run-recon")

    async def prove_exclusion():
        guard = full_writer_guard(store)
        await guard.acquire()
        task = asyncio.create_task(manager.reconcile())
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        assert task.done() is False
        guard.release()
        await task

    asyncio.run(prove_exclusion())
    store.close()


def test_authoritative_fill_without_local_fill_blocks(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store, status="FILLED", filled_qty=0.1)
    broker = healthy_broker()
    broker.full_open_orders = []
    broker.full_positions = [{"symbol": "BTC", "size": 0.1}]
    broker.full_fill_history = [{
        "fill_id": "fill-missing-local",
        "oid": 1,
        "coin": "BTC",
        "side": "BUY",
        "sz": 0.1,
        "px": 100.0,
        "time": int(BASE_TS.timestamp() * 1000),
    }]

    result = run_cycle(store, broker, FrozenClock())

    assert result.accepted is False
    assert DIFF_EXCHANGE_IDENTITY_CONFLICT in blocking_codes(result)
    assert store.conn.execute("SELECT COUNT(*) FROM fills").fetchone()[0] == 0
    store.close()


def test_owned_open_order_identity_mismatch_blocks(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    broker.full_open_orders[0].update({
        "oid": 999,
        "coin": "ETH",
        "side": "SELL",
        "role": "SL",
        "reduceOnly": True,
    })

    result = run_cycle(store, broker, FrozenClock())

    assert result.accepted is False
    assert DIFF_EXCHANGE_IDENTITY_CONFLICT in blocking_codes(result)
    store.close()


def test_owned_order_unknown_adapter_role_is_restart_safe(tmp_path):
    from bridge.engine.types import (
        ComponentEvidence,
        ReconcileComponentStatus,
    )

    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    reconciler = build_reconciler(store, broker, FrozenClock())
    component = ComponentEvidence(
        kind=ReconcileComponentKind.OPEN_ORDERS,
        source="HL_INFO",
        status=ReconcileComponentStatus.COMPLETE,
        observed_ts=BASE_TS,
        rows=({
            "cloid": "0xowned0001",
            "oid": 1,
            "coin": "BTC",
            "side": "BUY",
            "size": 0.1,
            "status": "OPEN",
            "role": "UNKNOWN",
            "reduce_only": False,
        },),
        exact=True,
        complete=True,
        reason_code="HL_OPEN_ORDERS_COMPLETE",
    )
    local = {row["cloid"]: row for row in store.live_local_orders()}
    assert reconciler._order_diffs(component, local) == []
    store.close()


def test_funding_drift_survives_an_unrelated_component_failure(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    clock = FrozenClock()
    broker = healthy_broker()
    event_time = int(BASE_TS.timestamp() * 1000)
    broker.full_funding_history = [
        funding_row(event_hash="0xdrift", usdc=-1.0, time_ms=event_time)
    ]
    assert run_cycle(store, broker, clock).accepted is True

    clock.advance(30.0)
    broker.full_component_failures["OPEN_ORDERS"] = "UNAVAILABLE"
    broker.full_funding_history = [
        funding_row(event_hash="0xdrift", usdc=-9.0, time_ms=event_time)
    ]
    result = run_cycle(store, broker, clock)

    assert result.accepted is False
    persisted = store.get_reconcile_diffs(result.attempt_id)
    assert any(
        row["reason_code"] == DIFF_EXCHANGE_IDENTITY_CONFLICT for row in persisted
    )
    payload = json.loads(next(
        row["payload_json"]
        for row in persisted
        if row["reason_code"] == DIFF_EXCHANGE_IDENTITY_CONFLICT
    ))
    assert payload["local"]["amount_usdc"] == -1.0
    assert payload["exchange"]["amount_usdc"] == -9.0
    store.close()


# ---------------------------------------------------------------------------
# Checkpoint lifecycle and restart
# ---------------------------------------------------------------------------


def test_failed_attempt_between_two_good_checkpoints(tmp_path):
    db_path = tmp_path / "bridge.db"
    store = open_store(db_path)
    seed_owned_order(store)
    clock = FrozenClock()

    good_a = run_cycle(store, healthy_broker(), clock)
    checkpoint_a = store.latest_accepted_reconcile_checkpoint()
    assert good_a.accepted and checkpoint_a is not None

    clock.advance(30.0)
    broken = healthy_broker()
    broken.full_component_failures = {
        ReconcileComponentKind.OPEN_ORDERS.value: "UNAVAILABLE"
    }
    failed_b = run_cycle(store, broken, clock)
    assert failed_b.accepted is False
    assert (
        store.latest_accepted_reconcile_checkpoint()["attempt_id"]
        == checkpoint_a["attempt_id"]
    )

    clock.advance(30.0)
    good_c = run_cycle(store, healthy_broker(), clock)
    assert good_c.accepted is True
    checkpoint_c = store.latest_accepted_reconcile_checkpoint()
    assert checkpoint_c["attempt_id"] == good_c.attempt_id
    assert checkpoint_c["attempt_id"] != checkpoint_a["attempt_id"]
    assert store.count_accepted_reconcile_checkpoints() == 2

    attempts = {row["attempt_id"]: row for row in store.list_reconcile_attempts()}
    assert attempts[good_a.attempt_id]["state"] == "COMPLETE"
    assert attempts[failed_b.attempt_id]["state"] == "INCOMPLETE"
    assert attempts[good_c.attempt_id]["state"] == "COMPLETE"
    store.close()


def test_accepted_checkpoints_and_evidence_are_immutable(tmp_path):
    import sqlite3

    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    broker = healthy_broker()
    # An observe-only foreign row guarantees the diff table is non-empty, so
    # the append-only triggers are actually exercised.
    broker.full_open_orders.append({
        "cloid": "0xforeign111",
        "oid": 91,
        "coin": "BTC",
        "side": "BUY",
        "sz": 1.0,
        "reduceOnly": False,
        "status": "OPEN",
    })
    result = run_cycle(store, broker, FrozenClock())
    assert result.accepted is True
    assert store.get_reconcile_diffs(result.attempt_id)

    for statement in (
        "DELETE FROM reconcile_checkpoints",
        "UPDATE reconcile_components SET status = 'COMPLETE'",
        "DELETE FROM reconcile_diffs",
        "UPDATE reconcile_attempts SET state = 'INCOMPLETE'",
        "DELETE FROM reconcile_attempts",
    ):
        with pytest.raises(sqlite3.IntegrityError):
            store.conn.execute(statement)
        store.conn.rollback()
    store.close()


def test_stale_checkpoint_is_retained_but_not_ready(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    clock = FrozenClock()
    result = run_cycle(store, healthy_broker(), clock)
    assert result.accepted is True

    assert store.full_reconcile_ready(now=clock.now(), max_age_s=900.0) is True
    assert (
        store.full_reconcile_ready(
            now=clock.now() + timedelta(seconds=3_600), max_age_s=900.0
        )
        is False
    )
    # A rolled-back clock is never "fresh" either.
    assert (
        store.full_reconcile_ready(
            now=clock.now() - timedelta(seconds=3_600), max_age_s=900.0
        )
        is False
    )
    assert store.latest_accepted_reconcile_checkpoint() is not None
    store.close()


# ---------------------------------------------------------------------------
# R1 — an unknown durable order status is never dropped from the comparison
# ---------------------------------------------------------------------------


def test_unknown_durable_order_status_blocks_the_capture(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    # Same exchange evidence, plus one durable row whose status is outside the
    # closed status space: it is neither provably live nor provably terminal.
    seed_owned_order(store, cloid="0xweird0002", status="TRIGGER_PENDING")

    result = run_cycle(store, healthy_broker(), FrozenClock())

    assert result.accepted is False
    assert result.state is ReconcileAttemptState.CONFLICTING
    assert "LOCAL_ORDER_STATUS_UNKNOWN" in blocking_codes(result)
    assert store.latest_accepted_reconcile_checkpoint() is None
    store.close()


def test_a_live_legacy_spelling_is_compared_rather_than_ignored(tmp_path):
    """RESTING is a live spelling: a missing exchange row must still block."""
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store, cloid="0xresting01", status="RESTING")
    broker = healthy_broker()
    broker.full_open_orders = []

    result = run_cycle(store, broker, FrozenClock())

    assert result.accepted is False
    assert "OWNED_ORDER_MISSING_ON_EXCHANGE" in blocking_codes(result)
    assert "LOCAL_ORDER_STATUS_UNKNOWN" not in blocking_codes(result)
    store.close()


# ---------------------------------------------------------------------------
# R4 — the 5 s budget is enforced during collection, not only afterwards
# ---------------------------------------------------------------------------


def test_hung_broker_call_fails_closed_within_the_wall_clock_deadline(tmp_path):
    """A genuinely hanging adapter await is cut off, not merely detected late."""
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    clock = FrozenClock()
    broker = healthy_broker()
    broker.full_clock = clock.now
    # Far longer than any deadline: only a real bound can end this capture.
    broker.full_component_delays_s = {ReconcileComponentKind.FILLS.value: 30.0}

    reconciler = FullReconciler(
        store=store,
        broker=broker,
        run_id="run-recon",
        clock=clock.now,
        monotonic=time.monotonic,   # real monotonic: a real budget
        deadline_s=0.25,
    )
    started = time.monotonic()
    result = asyncio.run(reconciler.run_cycle())
    elapsed = time.monotonic() - started

    assert result.state is ReconcileAttemptState.STALE
    assert result.reason_code == "FULL_RECONCILE_DEADLINE_EXCEEDED"
    assert elapsed < 5.0, f"capture was not bounded: {elapsed:.2f}s"
    assert store.latest_accepted_reconcile_checkpoint() is None
    assert store.count_accepted_reconcile_checkpoints() == 0
    assert store.reconcile_coverage_upper_bound_ms() is None
    attempt = store.get_reconcile_attempt(result.attempt_id)
    assert attempt["state"] == ReconcileAttemptState.STALE.value
    store.close()


def test_a_delay_inside_the_budget_still_completes(tmp_path):
    """The bound is a budget, not a ban on slow-but-timely adapters."""
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    clock = FrozenClock()
    broker = healthy_broker()
    broker.full_clock = clock.now
    broker.full_component_delays_s = {ReconcileComponentKind.FILLS.value: 0.05}

    reconciler = FullReconciler(
        store=store,
        broker=broker,
        run_id="run-recon",
        clock=clock.now,
        monotonic=time.monotonic,
        deadline_s=5.0,
    )
    result = asyncio.run(reconciler.run_cycle())

    assert result.accepted is True, result.reason_code
    store.close()


# ---------------------------------------------------------------------------
# R5 — durable coverage continuity (no fixed lookback, no silent gap)
# ---------------------------------------------------------------------------


def component_of(result, kind: ReconcileComponentKind):
    return next(item for item in result.components if item.kind is kind)


def ms(value: datetime) -> int:
    return int(value.timestamp() * 1000)


def test_first_capture_starts_at_the_durable_run_start(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    clock = FrozenClock()

    result = run_cycle(store, healthy_broker(), clock)

    assert result.accepted is True, result.reason_code
    for kind in (ReconcileComponentKind.FILLS, ReconcileComponentKind.FUNDING):
        component = component_of(result, kind)
        assert component.cursor_start_ms == ms(RUN_STARTED_TS)
        assert component.cursor_end_ms == ms(BASE_TS)
    assert store.reconcile_coverage_upper_bound_ms() == ms(BASE_TS)
    store.close()


def test_coverage_is_continuous_across_a_48h_downtime_and_reopen(tmp_path):
    """After 48 h down, the next capture covers the whole interval it missed."""
    db_path = tmp_path / "bridge.db"
    store = open_store(db_path)
    seed_owned_order(store)
    clock = FrozenClock()

    first = run_cycle(store, healthy_broker(), clock)
    assert first.accepted is True, first.reason_code
    assert store.reconcile_coverage_upper_bound_ms() == ms(BASE_TS)
    store.close()

    # Downtime, restart, and a funding event 10 h into the gap. A fixed 24 h
    # lookback from the new capture would start at +24 h and lose it entirely.
    reopened = open_store(db_path)
    clock.advance(48 * 3600)
    gap_event_ms = ms(BASE_TS + timedelta(hours=10))
    broker = healthy_broker()
    broker.full_funding_history = [
        funding_row(event_hash="0xgapfund", time_ms=gap_event_ms)
    ]

    second = run_cycle(reopened, broker, clock)

    assert second.accepted is True, second.reason_code
    for kind in (ReconcileComponentKind.FILLS, ReconcileComponentKind.FUNDING):
        component = component_of(second, kind)
        assert component.cursor_start_ms == ms(BASE_TS), "coverage must not gap"
        assert component.cursor_end_ms == ms(clock.now())
    assert [row["event_id"] for row in reopened.list_funding_events()] == [
        "0xgapfund"
    ]
    assert reopened.reconcile_coverage_upper_bound_ms() == ms(clock.now())
    reopened.close()


def test_coverage_floor_survives_a_restart_before_the_first_accept(tmp_path):
    """Run A failed for 48 h, run B is healthy: the window starts at run A.

    Nothing was ever accepted, so there is no coverage pointer. Trusting only
    the *current* run's durable start would hand run B a lower bound 48 h after
    run A began observing and silently drop everything in between.
    """
    db_path = tmp_path / "bridge.db"
    store = open_store(db_path)
    seed_owned_order(store)  # run-recon, durable start RUN_STARTED_TS
    clock = FrozenClock()

    broken = healthy_broker()
    broken.full_component_failures = {ReconcileComponentKind.FILLS.value: "RAISE"}
    failed = run_cycle(store, broken, clock)
    assert failed.accepted is False
    assert store.reconcile_coverage_upper_bound_ms() is None
    store.close()

    # 48 h down, reopen, and a brand-new run whose durable start is *now*.
    reopened = open_store(db_path)
    clock.advance(48 * 3600)
    reopened.create_run("run-b", mode="dry_run", network="testnet", config={})
    reopened.conn.execute(
        "UPDATE runs SET started_ts = ? WHERE run_id = ?",
        (clock.now().isoformat(), "run-b"),
    )
    reopened.conn.commit()
    assert reopened.earliest_reconcile_attempt_started_ts() == BASE_TS

    gap_event_ms = ms(BASE_TS + timedelta(hours=10))
    broker = healthy_broker()
    broker.full_funding_history = [
        funding_row(event_hash="0xrunafund", time_ms=gap_event_ms)
    ]
    broker.full_clock = clock.now
    result = asyncio.run(
        FullReconciler(
            store=reopened,
            broker=broker,
            run_id="run-b",
            clock=clock.now,
            monotonic=clock.monotonic,
        ).run_cycle()
    )

    assert result.accepted is True, result.reason_code
    for kind in (ReconcileComponentKind.FILLS, ReconcileComponentKind.FUNDING):
        component = component_of(result, kind)
        assert component.cursor_start_ms == ms(BASE_TS), (
            "the floor is run A's first attempt, never run B's start"
        )
        assert component.cursor_end_ms == ms(clock.now())
    assert [row["event_id"] for row in reopened.list_funding_events()] == [
        "0xrunafund"
    ], "funding inside the abandoned run's window is still retained"
    assert reopened.reconcile_coverage_upper_bound_ms() == ms(clock.now())
    reopened.close()


def test_failed_attempts_widen_the_next_window_instead_of_skipping_it(tmp_path):
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    clock = FrozenClock()

    first = run_cycle(store, healthy_broker(), clock)
    assert first.accepted is True, first.reason_code
    covered_to = store.reconcile_coverage_upper_bound_ms()

    # Two failed attempts across an hour: coverage never advances on failure.
    for _ in range(2):
        clock.advance(1_800.0)
        broken = healthy_broker()
        broken.full_component_failures = {
            ReconcileComponentKind.FILLS.value: "RAISE"
        }
        failed = run_cycle(store, broken, clock)
        assert failed.accepted is False
        assert store.reconcile_coverage_upper_bound_ms() == covered_to

    clock.advance(30.0)
    recovered = run_cycle(store, healthy_broker(), clock)
    assert recovered.accepted is True, recovered.reason_code
    fills = component_of(recovered, ReconcileComponentKind.FILLS)
    # The whole hour of failed attempts is inside the recovered window.
    assert fills.cursor_start_ms == covered_to
    assert fills.cursor_end_ms == ms(clock.now())
    store.close()


def test_an_unprovable_interval_fails_closed_and_keeps_coverage(tmp_path):
    """Retention/page/deadline truncation is a gap, so it never advances."""
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    clock = FrozenClock()

    first = run_cycle(store, healthy_broker(), clock)
    assert first.accepted is True, first.reason_code
    covered_to = store.reconcile_coverage_upper_bound_ms()

    clock.advance(48 * 3600)
    truncated = healthy_broker()
    truncated.full_component_failures = {
        ReconcileComponentKind.FUNDING.value: "TRUNCATED"
    }
    result = run_cycle(store, truncated, clock)

    assert result.accepted is False
    assert result.reason_code == "FUNDING_TRUNCATED"
    assert store.reconcile_coverage_upper_bound_ms() == covered_to
    assert (
        store.latest_accepted_reconcile_checkpoint()["attempt_id"]
        == first.attempt_id
    )
    store.close()


def test_a_short_window_component_is_a_coverage_gap(tmp_path):
    """Evidence that silently narrowed its own window can never be accepted."""

    class NarrowingBroker(MockBroker):
        async def funding_evidence(self, *, start_ms: int, end_ms: int):
            # Reports healthy evidence for a *later* window than required.
            return await super().funding_evidence(
                start_ms=start_ms + 60_000, end_ms=end_ms
            )

    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    template = healthy_broker()
    broker = NarrowingBroker(bars=[], coin="BTC")
    broker.full_open_orders = [dict(row) for row in template.full_open_orders]
    broker.full_positions = []
    broker.full_account = dict(template.full_account)

    result = run_cycle(store, broker, FrozenClock())

    assert result.accepted is False
    assert result.reason_code == "FULL_RECONCILE_COVERAGE_GAP"
    assert store.reconcile_coverage_upper_bound_ms() is None
    store.close()


def test_capture_without_durable_run_lineage_fails_closed(tmp_path):
    """No accepted coverage and no run row: a lower bound would be invented."""
    store = open_store(tmp_path / "bridge.db")
    seed_owned_order(store)
    clock = FrozenClock()
    broker = healthy_broker()
    broker.full_clock = clock.now
    reconciler = FullReconciler(
        store=store,
        broker=broker,
        run_id="run-that-was-never-created",
        clock=clock.now,
        monotonic=clock.monotonic,
    )

    result = asyncio.run(reconciler.run_cycle())

    assert result.accepted is False
    assert result.reason_code == "FULL_RECONCILE_COVERAGE_UNPROVABLE"
    assert broker.full_calls == [], "no broker I/O without a provable window"
    assert store.reconcile_coverage_upper_bound_ms() is None
    store.close()
