from __future__ import annotations

import asyncio
import json
import sqlite3
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest

from bridge.broker.base import (
    BrokerOutcomeUnknown,
    BrokerPreSendFailure,
    EvidenceStatus,
    RecoveryQueryEvidence,
    SubmissionDisposition,
    SubmissionOutcome,
    SubmissionRecoveryEvidence,
    SubmissionRejectedError,
    UnknownSubmissionError,
)
from bridge.engine.engine import BridgeEngine
from bridge.engine.orders import OrderManager
from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.types import AccountSnapshot, Bar, BrokerOrder, OrderPlan, Signal
from bridge.broker.hyperliquid import HyperliquidBroker, HyperliquidOrderError
from bridge.store.db import Store


BASE_TS = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)


class Clock:
    def __init__(self, value: datetime = BASE_TS) -> None:
        self.value = value

    def __call__(self) -> datetime:
        return self.value


def plan(ts: datetime = BASE_TS, take_profit: float | None = 110.0) -> OrderPlan:
    signal = Signal(
        ts=ts,
        symbol="BTC",
        direction="LONG",
        reason="unknown-submission-test",
        ref_price=100.0,
        stop_loss=95.0,
        take_profit=take_profit,
    )
    return OrderPlan(
        signal=signal,
        qty=0.1,
        entry_type="MKT",
        stop_loss=95.0,
        take_profit=take_profit,
        leverage=1,
        risk_dollars=0.5,
        risk_pct=0.001,
    )


class ScriptedBroker:
    def __init__(self, behavior: object | None = None) -> None:
        self.behavior = behavior
        self.write_count = 0
        self.recovery_scripts: list[object] = []
        self.connected = True

    def planned_cloids(self, order_plan: OrderPlan) -> dict[str, str]:
        seed = str(order_plan.decision_uid)
        result = {"ENTRY": f"{seed}:ENTRY", "SL": f"{seed}:SL"}
        if order_plan.take_profit is not None:
            result["TP"] = f"{seed}:TP"
        return result

    def success(self, order_plan: OrderPlan) -> SubmissionOutcome:
        rows: dict[str, dict] = {}
        for role, cloid in self.planned_cloids(order_plan).items():
            rows[role.lower()] = {
                "cloid": cloid,
                "oid": len(rows) + 1,
                "role": role,
                "status": "FILLED" if role == "ENTRY" else "OPEN",
                "qty": order_plan.qty,
                "avg_fill_px": 100.0 if role == "ENTRY" else None,
            }
        return SubmissionOutcome(
            SubmissionDisposition.VERIFIED_SUCCESS,
            rows,
            "FAKE_VERIFIED_SUCCESS",
        )

    async def place_bracket(self, order_plan: OrderPlan):
        self.write_count += 1
        behavior = self.behavior
        if behavior is None:
            return self.success(order_plan)
        if callable(behavior):
            behavior = behavior(order_plan, self)
        if isinstance(behavior, BaseException):
            raise behavior
        return behavior

    async def submission_recovery_evidence(self, request):
        if not self.recovery_scripts:
            return unavailable_cycle(request, EvidenceStatus.UNAVAILABLE)
        script = self.recovery_scripts.pop(0)
        return script(request) if callable(script) else script

    async def connect(self) -> None:
        self.connected = True

    async def account(self) -> AccountSnapshot:
        return AccountSnapshot(equity=100_000.0, available_margin=100_000.0)

    async def positions(self) -> list:
        return []

    async def open_orders(self) -> list:
        return []

    async def historical_bars(self, coin: str, tf: str, lookback: int) -> list:
        return []

    def subscribe_bars(self, coin: str, tf: str, on_bar_closed) -> None:
        return None

    def subscribe_user_events(self, callback) -> None:
        return None

    async def modify_stop(self, cloid: str, new_stop: float) -> None:
        return None

    async def cancel(self, cloid: str) -> None:
        return None

    async def cancel_all(self) -> None:
        return None

    async def flatten(self, coin: str) -> None:
        return None

    async def reprotect_position(self, *args, **kwargs):
        return None


def store_and_manager(tmp_path, broker=None, clock=None):
    store = Store(tmp_path / "bridge.db", clock=clock)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})
    broker = broker or ScriptedBroker()
    return store, broker, OrderManager(store, broker, "run-1")


def complete_absence_cycle(request) -> SubmissionRecoveryEvidence:
    not_found = RecoveryQueryEvidence(
        EvidenceStatus.NOT_FOUND, (), "FAKE_COMPLETE_NOT_FOUND"
    )
    return SubmissionRecoveryEvidence(
        request_id=request.request_id,
        planned_cloids=dict(request.planned_cloids),
        direct_lookup={
            str(cloid): not_found for cloid in request.planned_cloids.values()
        },
        open_orders=not_found,
        historical_orders=not_found,
        fills=not_found,
        position=not_found,
    )


def unavailable_cycle(request, status: EvidenceStatus) -> SubmissionRecoveryEvidence:
    query = RecoveryQueryEvidence(status, (), f"FAKE_{status.value}")
    return SubmissionRecoveryEvidence(
        request_id=request.request_id,
        planned_cloids=dict(request.planned_cloids),
        direct_lookup={
            str(cloid): query for cloid in request.planned_cloids.values()
        },
        open_orders=query,
        historical_orders=query,
        fills=query,
        position=query,
    )


def presence_cycle(request, source: str) -> SubmissionRecoveryEvidence:
    cycle = complete_absence_cycle(request)
    found_cloid = next(iter(request.planned_cloids.values()))
    found = RecoveryQueryEvidence(
        EvidenceStatus.FOUND, (found_cloid,), f"FAKE_{source.upper()}_FOUND"
    )
    direct = dict(cycle.direct_lookup)
    kwargs = {
        "request_id": cycle.request_id,
        "planned_cloids": cycle.planned_cloids,
        "direct_lookup": direct,
        "open_orders": cycle.open_orders,
        "historical_orders": cycle.historical_orders,
        "fills": cycle.fills,
        "position": cycle.position,
    }
    if source == "direct":
        direct[found_cloid] = found
    elif source == "history":
        kwargs["historical_orders"] = found
    elif source == "fills":
        kwargs["fills"] = found
    else:
        kwargs["open_orders"] = found
    return SubmissionRecoveryEvidence(**kwargs)


def make_unknown_attempt(tmp_path, clock=None):
    broker = ScriptedBroker(
        SubmissionOutcome(
            SubmissionDisposition.OUTCOME_UNKNOWN, {}, "FAKE_OUTCOME_UNKNOWN"
        )
    )
    store, broker, manager = store_and_manager(tmp_path, broker, clock)
    with pytest.raises(UnknownSubmissionError):
        asyncio.run(manager.submit_plan("decision-1", plan()))
    attempt = store.get_snapshot()["submission_attempts"][0]
    assert attempt["state"] == "UNKNOWN_SUBMISSION"
    return store, broker, manager, attempt


def test_proven_pre_send_failure_and_definitive_rejection_are_terminal(tmp_path):
    pre = ScriptedBroker(BrokerPreSendFailure("FAKE_PRE_SEND"))
    store, _, manager = store_and_manager(tmp_path / "pre", pre)
    with pytest.raises(SubmissionRejectedError, match="PRE_SEND_FAILURE"):
        asyncio.run(manager.submit_plan("pre", plan()))
    assert store.get_snapshot()["submission_attempts"][0]["state"] == "PRE_SEND_FAILURE"
    assert store.get_snapshot()["trades"] == []

    rejected = ScriptedBroker(
        SubmissionOutcome(
            SubmissionDisposition.DEFINITIVE_REJECTION,
            {},
            "FAKE_ALL_REJECTED",
        )
    )
    store2, _, manager2 = store_and_manager(tmp_path / "reject", rejected)
    with pytest.raises(SubmissionRejectedError, match="DEFINITIVE_REJECTION"):
        asyncio.run(manager2.submit_plan("reject", plan()))
    assert store2.get_snapshot()["submission_attempts"][0]["state"] == "DEFINITIVE_REJECTION"


@pytest.mark.parametrize(
    "behavior,reason",
    [
        (
            SubmissionOutcome(
                SubmissionDisposition.OUTCOME_UNKNOWN, {}, "FAKE_MIXED_RESULT"
            ),
            "FAKE_MIXED_RESULT",
        ),
        (BrokerOutcomeUnknown("FAKE_TIMEOUT_AFTER_ACCEPT"), "FAKE_TIMEOUT_AFTER_ACCEPT"),
        (ConnectionResetError("wallet-secret-do-not-persist"), "UNTYPED_BROKER_EXCEPTION"),
    ],
)
def test_post_send_mixed_timeout_reset_are_unknown(tmp_path, behavior, reason):
    broker = ScriptedBroker(behavior)
    store, broker, manager = store_and_manager(tmp_path, broker)
    with pytest.raises(UnknownSubmissionError, match=reason):
        asyncio.run(manager.submit_plan("decision", plan()))
    attempt = store.get_snapshot()["submission_attempts"][0]
    assert attempt["state"] == "UNKNOWN_SUBMISSION"
    assert broker.write_count == 1
    assert store.get_snapshot()["trades"] == []
    assert "wallet-secret-do-not-persist" not in json.dumps(store.get_snapshot())


def test_hostile_typed_reason_code_is_replaced_before_engine_or_store_use(tmp_path):
    secret = "wallet secret api_key=do-not-persist"
    broker = ScriptedBroker(BrokerOutcomeUnknown(secret))
    store, _, manager = store_and_manager(tmp_path, broker)
    with pytest.raises(UnknownSubmissionError) as exc_info:
        asyncio.run(manager.submit_plan("decision", plan()))
    assert exc_info.value.reason_code == "OUTCOME_UNKNOWN"
    assert secret not in json.dumps(store.get_snapshot())


def malformed_outcome(kind: str):
    def build(order_plan: OrderPlan, broker: ScriptedBroker):
        outcome = broker.success(order_plan)
        rows = {key: dict(value) for key, value in outcome.orders.items()}
        if kind == "empty":
            rows = {}
        elif kind == "partial":
            rows.pop("sl")
        elif kind == "wrong_cloid":
            rows["entry"]["cloid"] = "wrong"
        elif kind == "missing_cloid":
            rows["entry"].pop("cloid")
        elif kind == "duplicate_cloid":
            rows["sl"]["cloid"] = rows["entry"]["cloid"]
        elif kind == "extra_role":
            rows["extra"] = dict(rows["entry"], role="EXTRA", cloid="extra")
        elif kind == "wrong_role":
            rows["entry"]["role"] = "SL"
        elif kind == "rejected_status":
            rows["entry"]["status"] = "REJECTED"
        elif kind == "malformed":
            rows["entry"] = ["not-a-row"]
        return SubmissionOutcome(
            SubmissionDisposition.VERIFIED_SUCCESS, rows, "FAKE_BAD_SUCCESS"
        )

    return build


@pytest.mark.parametrize(
    "kind",
    [
        "empty",
        "partial",
        "wrong_cloid",
        "missing_cloid",
        "duplicate_cloid",
        "extra_role",
        "wrong_role",
        "rejected_status",
        "malformed",
    ],
)
def test_invalid_success_coverage_is_unknown(tmp_path, kind):
    broker = ScriptedBroker(malformed_outcome(kind))
    store, _, manager = store_and_manager(tmp_path, broker)
    with pytest.raises(UnknownSubmissionError, match="BROKER_RESULT_COVERAGE_INVALID"):
        asyncio.run(manager.submit_plan("decision", plan()))
    assert store.get_snapshot()["submission_attempts"][0]["state"] == "UNKNOWN_SUBMISSION"
    assert store.get_snapshot()["orders"] == []


def test_normal_complete_success_finalizes_attempt_trade_and_orders_atomically(tmp_path):
    store, broker, manager = store_and_manager(tmp_path)
    result = asyncio.run(manager.submit_plan("decision", plan()))
    assert result is not None
    snapshot = store.get_snapshot()
    assert snapshot["submission_attempts"][0]["state"] == "FINALIZED"
    assert len(snapshot["trades"]) == 1
    assert {row["role"] for row in snapshot["orders"]} == {"ENTRY", "SL", "TP"}
    assert broker.write_count == 1


def test_success_payload_does_not_persist_or_return_hostile_extra_fields(tmp_path):
    secret = "wallet-secret-never-persist"

    def hostile_success(order_plan, broker):
        outcome = broker.success(order_plan)
        rows = {role: dict(row) for role, row in outcome.orders.items()}
        rows["entry"]["api_key"] = secret
        rows["sl"]["pending_reason"] = secret
        return SubmissionOutcome(
            SubmissionDisposition.VERIFIED_SUCCESS,
            rows,
            "FAKE_VERIFIED_SUCCESS",
        )

    store, _, manager = store_and_manager(
        tmp_path, ScriptedBroker(hostile_success)
    )
    result = asyncio.run(manager.submit_plan("decision", plan()))
    assert secret not in json.dumps(result)
    assert secret not in json.dumps(store.get_snapshot())


def test_local_finalization_failure_after_success_becomes_unknown(tmp_path):
    store, broker, manager = store_and_manager(tmp_path)
    order_plan = plan()
    order_plan.decision_uid = None
    from bridge.store.db import compute_intent_identity, compute_request_identity

    intent_id, _, _ = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG", BASE_TS
    )
    request_id, _, _ = compute_request_identity(
        intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1
    )
    store.insert_order(
        cloid=f"{request_id}:ENTRY",
        oid=999,
        group_id="foreign",
        order_ref="foreign:ENTRY",
        order_json={},
        decision_uid="foreign",
        trade_id=None,
        role="ENTRY",
        status="OPEN",
        qty=1.0,
    )
    with pytest.raises(UnknownSubmissionError, match="LOCAL_FINALIZATION_FAILED"):
        asyncio.run(manager.submit_plan("decision", order_plan))
    snapshot = store.get_snapshot()
    assert snapshot["submission_attempts"][0]["state"] == "UNKNOWN_SUBMISSION"
    assert snapshot["trades"] == []


def test_definitive_rejection_transition_failure_leaves_submitting_quarantined(
    tmp_path, monkeypatch
):
    broker = ScriptedBroker(
        SubmissionOutcome(
            SubmissionDisposition.DEFINITIVE_REJECTION,
            {},
            "FAKE_ALL_REJECTED",
        )
    )
    store, _, manager = store_and_manager(tmp_path, broker)

    def fail_transition(*args, **kwargs):
        raise sqlite3.OperationalError("secret-transition-failure")

    monkeypatch.setattr(store, "transition_submission_attempt", fail_transition)
    with pytest.raises(
        UnknownSubmissionError,
        match="DEFINITIVE_REJECTION_FINALIZATION_FAILED",
    ):
        asyncio.run(manager.submit_plan("decision", plan()))
    snapshot = store.get_snapshot()
    assert snapshot["submission_attempts"][0]["state"] == "SUBMITTING"
    assert "secret-transition-failure" not in json.dumps(snapshot)


class SignalStrategy:
    id = "unknown_engine_strategy"
    warmup_bars = 0

    def on_bar(self, bars, position):
        return Signal(
            ts=bars[-1].ts,
            symbol="BTC",
            direction="LONG",
            reason="engine-test",
            ref_price=bars[-1].close,
            stop_loss=95.0,
        )

    def trail_level(self, bars, position):
        return None


def test_unknown_immediately_disarms_and_restart_arm_replay_write_zero(tmp_path):
    broker = ScriptedBroker(BrokerOutcomeUnknown("FAKE_TIMEOUT"))
    store, _, manager = store_and_manager(tmp_path, broker)
    store.set_meta("app_state", "ARMED")
    engine = BridgeEngine(
        run_id="run-1",
        broker=broker,
        store=store,
        strategy=SignalStrategy(),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        order_manager=manager,
        state="ARMED",
    )
    bar = Bar(
        ts=BASE_TS, open=100.0, high=101.0, low=99.0, close=100.0, volume=1.0
    )
    asyncio.run(engine.on_bar(bar))
    assert engine.state == "DISARMED"
    assert engine._consecutive_order_rejects == 0
    assert any(
        row["stage"] == "UNKNOWN_SUBMISSION" for row in store.get_decisions()
    )
    writes = broker.write_count
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime.now(UTC)
    with pytest.raises(RuntimeError, match="quarantine"):
        asyncio.run(engine.arm())
    asyncio.run(engine.run_replay(max_bars=1))
    assert broker.write_count == writes

    restarted = BridgeEngine(
        run_id="run-2",
        broker=broker,
        store=store,
        strategy=SignalStrategy(),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        state="ARMED",
    )
    assert restarted.state == "DISARMED"
    asyncio.run(restarted.run_replay(max_bars=1))
    assert broker.write_count == writes


@pytest.mark.parametrize("source", ["direct", "history", "fills"])
def test_direct_history_or_fill_presence_confirms_present(tmp_path, source):
    store, broker, manager, attempt = make_unknown_attempt(tmp_path)
    broker.recovery_scripts = [lambda request: presence_cycle(request, source)]
    asyncio.run(manager.recover_unknown_submissions())
    resolved = store.get_submission_attempt(attempt["attempt_id"])
    assert resolved["state"] == "CONFIRMED_PRESENT"
    assert store.submission_quarantine_count() == 1


def test_delayed_fill_presence_resets_absence_candidate(tmp_path):
    clock = Clock()
    store, broker, manager, attempt = make_unknown_attempt(tmp_path, clock)
    broker.recovery_scripts = [
        complete_absence_cycle,
        lambda request: presence_cycle(request, "fills"),
    ]
    asyncio.run(manager.recover_unknown_submissions())
    assert store.get_submission_attempt(attempt["attempt_id"])["absence_count"] == 1
    clock.value += timedelta(seconds=130)
    asyncio.run(manager.recover_unknown_submissions())
    resolved = store.get_submission_attempt(attempt["attempt_id"])
    assert resolved["state"] == "CONFIRMED_PRESENT"
    assert resolved["absence_count"] == 0


@pytest.mark.parametrize(
    "offsets,expected_state,expected_count",
    [
        ([0], "UNKNOWN_SUBMISSION", 1),
        ([0, 60], "UNKNOWN_SUBMISSION", 2),
        ([0, 30, 119], "UNKNOWN_SUBMISSION", 3),
        ([0, 60, 120], "CONFIRMED_ABSENT", 3),
    ],
)
def test_absence_requires_three_cycles_spanning_120_seconds(
    tmp_path, offsets, expected_state, expected_count
):
    clock = Clock()
    store, broker, manager, attempt = make_unknown_attempt(tmp_path, clock)
    broker.recovery_scripts = [complete_absence_cycle for _ in offsets]
    for offset in offsets:
        clock.value = BASE_TS + timedelta(seconds=offset)
        asyncio.run(manager.recover_unknown_submissions())
    resolved = store.get_submission_attempt(attempt["attempt_id"])
    assert resolved["state"] == expected_state
    assert resolved["absence_count"] == expected_count
    assert len(store.get_submission_evidence(attempt["attempt_id"])) == len(offsets)
    if expected_state == "CONFIRMED_ABSENT":
        writes = broker.write_count
        broker.behavior = None
        assert asyncio.run(manager.submit_plan("replay", plan())) is None
        assert broker.write_count == writes


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.QUERY_FAILED,
        EvidenceStatus.UNAVAILABLE,
        EvidenceStatus.TRUNCATED,
        EvidenceStatus.STALE,
    ],
)
def test_incomplete_coverage_never_proves_absence_and_resets(tmp_path, status):
    clock = Clock()
    store, broker, manager, attempt = make_unknown_attempt(tmp_path, clock)
    broker.recovery_scripts = [
        complete_absence_cycle,
        lambda request: unavailable_cycle(request, status),
    ]
    asyncio.run(manager.recover_unknown_submissions())
    clock.value += timedelta(seconds=130)
    asyncio.run(manager.recover_unknown_submissions())
    resolved = store.get_submission_attempt(attempt["attempt_id"])
    assert resolved["state"] == "UNKNOWN_SUBMISSION"
    assert resolved["absence_count"] == 0


def test_empty_open_orders_alone_and_unattributable_position_never_absent(tmp_path):
    store, broker, manager, attempt = make_unknown_attempt(tmp_path)

    def empty_open_only(request):
        cycle = unavailable_cycle(request, EvidenceStatus.UNAVAILABLE)
        return SubmissionRecoveryEvidence(
            request_id=cycle.request_id,
            planned_cloids=cycle.planned_cloids,
            direct_lookup=cycle.direct_lookup,
            open_orders=RecoveryQueryEvidence(
                EvidenceStatus.NOT_FOUND, (), "OPEN_EMPTY"
            ),
            historical_orders=cycle.historical_orders,
            fills=cycle.fills,
            position=cycle.position,
        )

    def position_only(request):
        cycle = complete_absence_cycle(request)
        return SubmissionRecoveryEvidence(
            request_id=cycle.request_id,
            planned_cloids=cycle.planned_cloids,
            direct_lookup=cycle.direct_lookup,
            open_orders=cycle.open_orders,
            historical_orders=cycle.historical_orders,
            fills=cycle.fills,
            position=RecoveryQueryEvidence(
                EvidenceStatus.FOUND, (), "UNATTRIBUTABLE_POSITION"
            ),
        )

    broker.recovery_scripts = [empty_open_only, position_only]
    asyncio.run(manager.recover_unknown_submissions())
    asyncio.run(manager.recover_unknown_submissions())
    resolved = store.get_submission_attempt(attempt["attempt_id"])
    assert resolved["state"] == "UNKNOWN_SUBMISSION"
    assert resolved["absence_count"] == 0


def test_forged_linkage_is_rejected_without_evidence_append(tmp_path):
    store, broker, manager, attempt = make_unknown_attempt(tmp_path)

    def forged(request):
        cycle = complete_absence_cycle(request)
        return SubmissionRecoveryEvidence(
            request_id="wrong-request",
            planned_cloids=cycle.planned_cloids,
            direct_lookup=cycle.direct_lookup,
            open_orders=cycle.open_orders,
            historical_orders=cycle.historical_orders,
            fills=cycle.fills,
            position=cycle.position,
        )

    broker.recovery_scripts = [forged]
    asyncio.run(manager.recover_unknown_submissions())
    assert store.get_submission_evidence(attempt["attempt_id"]) == []
    assert store.get_submission_attempt(attempt["attempt_id"])["state"] == "UNKNOWN_SUBMISSION"


def test_recovery_transaction_rollback_preserves_state_and_evidence(tmp_path, monkeypatch):
    store, broker, manager, attempt = make_unknown_attempt(tmp_path)
    broker.recovery_scripts = [lambda request: presence_cycle(request, "direct")]

    def fail_transition(*args, **kwargs):
        raise sqlite3.DatabaseError("forced transition failure")

    monkeypatch.setattr(store, "_transition_attempt_in_tx", fail_transition)
    with pytest.raises(sqlite3.DatabaseError):
        asyncio.run(manager.recover_unknown_submissions())
    assert store.get_submission_evidence(attempt["attempt_id"]) == []
    assert store.get_submission_attempt(attempt["attempt_id"])["state"] == "UNKNOWN_SUBMISSION"


def test_evidence_append_only_and_transition_matrix_resists_attacks(tmp_path):
    store, broker, manager, attempt = make_unknown_attempt(tmp_path)
    broker.recovery_scripts = [unavailable_cycle]
    broker.recovery_scripts = [
        lambda request: unavailable_cycle(request, EvidenceStatus.UNAVAILABLE)
    ]
    asyncio.run(manager.recover_unknown_submissions())
    evidence_id = store.get_submission_evidence(attempt["attempt_id"])[0]["evidence_id"]
    with pytest.raises(sqlite3.IntegrityError, match="APPEND_ONLY"):
        store.conn.execute(
            "UPDATE submission_recovery_evidence SET verdict='PRESENT' WHERE evidence_id=?",
            (evidence_id,),
        )
    store.conn.rollback()
    with pytest.raises(Exception):
        store.transition_submission_attempt(
            attempt["attempt_id"], "SUBMITTING", "CRAFTED_SELF"
        )
    with pytest.raises(sqlite3.IntegrityError, match="TRANSITION_DENIED"):
        store.conn.execute(
            "UPDATE submission_attempts SET state='UNKNOWN_SUBMISSION' WHERE attempt_id=?",
            (attempt["attempt_id"],),
        )
    store.conn.rollback()
    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            "UPDATE submission_attempts SET reason_code=? WHERE attempt_id=?",
            ("wallet secret must not persist", attempt["attempt_id"]),
        )
    store.conn.rollback()


def create_v3_database(path):
    store = Store(path)
    store.conn.execute(
        "CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)"
    )
    store._create_tables_v3()
    store.conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '3')"
    )
    store.conn.commit()
    store.close()


def test_v3_to_v4_success_reopen_and_rollback_clean(tmp_path, monkeypatch):
    success_path = tmp_path / "success.db"
    create_v3_database(success_path)
    store = Store(success_path)
    store.initialize()
    assert store.get_meta("schema_version") == "4"
    store.close()
    reopened = Store(success_path)
    reopened.initialize()
    assert reopened.get_meta("schema_version") == "4"
    reopened.close()

    failure_path = tmp_path / "failure.db"
    create_v3_database(failure_path)

    def fail_ledger(self):
        self.conn.execute("CREATE TABLE v4_partial(id INTEGER)")
        raise RuntimeError("forced-v4-failure")

    monkeypatch.setattr(Store, "_create_submission_ledger_v4", fail_ledger)
    failed = Store(failure_path)
    with pytest.raises(RuntimeError, match="forced-v4-failure"):
        failed.initialize()
    assert failed.get_meta("schema_version") == "3"
    residue = failed.conn.execute(
        "SELECT name FROM sqlite_master WHERE name='v4_partial'"
    ).fetchone()
    assert residue is None
    failed.close()


def test_v2_commits_valid_v3_before_later_v4_failure(tmp_path, monkeypatch):
    path = tmp_path / "v2.db"
    seed = Store(path)
    seed.conn.execute(
        "CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT)"
    )
    seed.conn.execute(
        """CREATE TABLE signal_fingerprints(
             run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT,
             PRIMARY KEY(run_id, fingerprint)
           )"""
    )
    seed.conn.execute(
        "INSERT INTO meta(key, value) VALUES ('schema_version', '2')"
    )
    seed.conn.commit()
    seed.close()

    def fail_ledger(self):
        self.conn.execute("CREATE TABLE v4_partial(id INTEGER)")
        raise RuntimeError("forced-v4-failure")

    monkeypatch.setattr(Store, "_create_submission_ledger_v4", fail_ledger)
    failed = Store(path)
    with pytest.raises(RuntimeError, match="forced-v4-failure"):
        failed.initialize()
    assert failed.get_meta("schema_version") == "3"
    identity = failed.conn.execute(
        "SELECT name FROM sqlite_master WHERE name='order_identity'"
    ).fetchone()
    partial = failed.conn.execute(
        "SELECT name FROM sqlite_master WHERE name='v4_partial'"
    ).fetchone()
    assert identity is not None
    assert partial is None
    failed.close()


def test_hyperliquid_complete_rejection_and_mixed_result_are_typed():
    exchange = MagicMock()
    exchange.bulk_orders.return_value = {
        "response": {
            "data": {
                "statuses": [
                    {"error": "entry rejected"},
                    {"error": "sl rejected"},
                    {"error": "tp rejected"},
                ]
            }
        }
    }
    broker = HyperliquidBroker(info_client=object(), exchange_client=exchange)
    result = asyncio.run(broker.place_bracket(plan()))
    assert result.disposition is SubmissionDisposition.DEFINITIVE_REJECTION
    assert dict(result) == {}

    exchange.bulk_orders.return_value = {
        "response": {
            "data": {
                "statuses": [
                    {"resting": {"oid": 1}},
                    {"error": "sl rejected"},
                    {"pending_child": "waitingForFill"},
                ]
            }
        }
    }
    with pytest.raises(HyperliquidOrderError) as exc_info:
        asyncio.run(broker.place_bracket(plan()))
    assert exc_info.value.disposition is SubmissionDisposition.OUTCOME_UNKNOWN
    assert exc_info.value.write_may_have_started is True


@pytest.mark.parametrize("status_count", [0, 1, 2])
def test_hyperliquid_partial_response_remains_unknown_after_open_order_verification(
    status_count,
):
    exchange = MagicMock()
    exchange.bulk_orders.return_value = {
        "response": {
            "data": {
                "statuses": [
                    {"resting": {"oid": index + 1}}
                    for index in range(status_count)
                ]
            }
        }
    }
    request_plan = plan()
    broker = HyperliquidBroker(info_client=object(), exchange_client=exchange)
    planned = broker.planned_cloids(request_plan)
    broker.open_orders = AsyncMock(
        return_value=[
            BrokerOrder(
                cloid=cloid,
                oid=index + 1,
                coin="BTC",
                side="BUY" if role == "ENTRY" else "SELL",
                size=request_plan.qty,
                status="OPEN",
                role=role,
                reduce_only=role != "ENTRY",
            )
            for index, (role, cloid) in enumerate(planned.items())
        ]
    )

    outcome = asyncio.run(broker.place_bracket(request_plan))
    assert outcome.disposition is SubmissionDisposition.OUTCOME_UNKNOWN
    assert outcome.reason_code == "HL_RESULT_CARDINALITY_MISMATCH"
    assert set(outcome) == {"entry", "sl", "tp"}


def test_hyperliquid_recovery_missing_and_failed_apis_are_not_not_found():
    request_plan = plan()
    request_plan.decision_uid = "request-v1:" + "a" * 64
    broker = HyperliquidBroker(info_client=object(), exchange_client=MagicMock())
    request = type("Request", (), {
        "attempt_id": "attempt-v1:" + "b" * 64,
        "request_id": request_plan.decision_uid,
        "planned_cloids": broker.planned_cloids(request_plan),
        "symbol": "BTC",
        "window_start": BASE_TS.isoformat(),
    })()
    evidence = asyncio.run(broker.submission_recovery_evidence(request))
    assert {
        query.status for query in evidence.direct_lookup.values()
    } == {EvidenceStatus.UNAVAILABLE}
    assert evidence.open_orders.status is EvidenceStatus.UNAVAILABLE
    assert evidence.historical_orders.status is EvidenceStatus.UNAVAILABLE
    assert evidence.fills.status is EvidenceStatus.UNAVAILABLE

    class NoneInfo:
        def query_order_by_oid(self, *args):
            return None

    none_broker = HyperliquidBroker(
        info_client=NoneInfo(), exchange_client=MagicMock()
    )
    none_evidence = asyncio.run(
        none_broker.submission_recovery_evidence(request)
    )
    assert {
        query.status for query in none_evidence.direct_lookup.values()
    } == {EvidenceStatus.CONFLICTING}

    class FailingInfo:
        def query_order_by_oid(self, *args):
            raise TimeoutError("secret")

        def open_orders(self, *args):
            raise ConnectionError("secret")

        def historical_orders(self, *args):
            raise ConnectionError("secret")

        def user_fills_by_time(self, *args):
            raise ConnectionError("secret")

        def user_state(self, *args):
            raise ConnectionError("secret")

    failing = HyperliquidBroker(info_client=FailingInfo(), exchange_client=MagicMock())
    failed_evidence = asyncio.run(failing.submission_recovery_evidence(request))
    assert {
        query.status for query in failed_evidence.direct_lookup.values()
    } == {EvidenceStatus.QUERY_FAILED}
    assert failed_evidence.open_orders.status is EvidenceStatus.QUERY_FAILED
    assert failed_evidence.historical_orders.status is EvidenceStatus.QUERY_FAILED
    assert failed_evidence.fills.status is EvidenceStatus.QUERY_FAILED
    assert failed_evidence.position.status is EvidenceStatus.QUERY_FAILED


def test_hyperliquid_complete_recovery_cycle_is_request_specific():
    class CompleteInfo:
        def query_order_by_oid(self, address, cloid):
            return {"status": "unknownOid"}

        def open_orders(self, address):
            return []

        def historical_orders(self, address):
            return []

        def user_fills_by_time(self, address, start_ms, end_ms):
            return []

        def user_state(self, address):
            return {"assetPositions": []}

    request_plan = plan()
    request_plan.decision_uid = "request-v1:" + "c" * 64
    broker = HyperliquidBroker(info_client=CompleteInfo(), exchange_client=MagicMock())
    request = type("Request", (), {
        "attempt_id": "attempt-v1:" + "d" * 64,
        "request_id": request_plan.decision_uid,
        "planned_cloids": broker.planned_cloids(request_plan),
        "symbol": "BTC",
        "window_start": BASE_TS.isoformat(),
    })()
    evidence = asyncio.run(broker.submission_recovery_evidence(request))
    assert all(
        query.status is EvidenceStatus.NOT_FOUND
        for query in evidence.direct_lookup.values()
    )
    assert evidence.open_orders.status is EvidenceStatus.NOT_FOUND
    assert evidence.historical_orders.status is EvidenceStatus.NOT_FOUND
    assert evidence.fills.status is EvidenceStatus.NOT_FOUND
    assert evidence.position.status is EvidenceStatus.NOT_FOUND
