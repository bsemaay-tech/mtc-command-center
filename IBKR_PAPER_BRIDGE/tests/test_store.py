from __future__ import annotations

import asyncio
import inspect
import multiprocessing
from datetime import UTC, datetime, timedelta

import pytest

from bridge.store.db import (
    KillConflictError,
    Store,
    compute_kill_action_cloid,
    compute_kill_action_id,
)
from bridge.store.db import DURABLE_EVENT_COLUMN_TYPES, DURABLE_EVENT_ROWS
from bridge.store.db import DurableRowFault


def test_store_roundtrip_decision_chain_and_schema_version(tmp_path):
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()

    assert store.get_meta("schema_version") == "4"

    run_id = "run-test"
    decision_uid = "decision-001"
    now = datetime(2026, 7, 6, 12, 0, tzinfo=UTC)

    store.create_run(run_id, mode="dry_run", network="testnet", config={"coin": "BTC"})
    store.insert_bar("BTC", "1h", now, 100.0, 105.0, 99.0, 104.0, 123.0)
    store.insert_decision(run_id, decision_uid, now, "BTC", "SIGNAL", {"direction": "LONG"})
    store.insert_decision(run_id, decision_uid, now, "BTC", "RISK_PASS", {"qty": 0.1})

    trade_id = store.create_trade(
        run_id=run_id,
        coin="BTC",
        direction="LONG",
        qty=0.1,
        entry_decision_uid=decision_uid,
        signal_ts=now,
        decision_ts=now,
        expected_px=104.0,
        risk_dollars=10.0,
        risk_pct=0.005,
        leverage=1,
        sl_initial=100.0,
        tp_initial=None,
        llm_directive_id=None,
    )
    store.insert_order(
        cloid="0xentry",
        oid=101,
        group_id="g1",
        order_ref=f"{decision_uid}:ENTRY",
        order_json={"type": "market"},
        decision_uid=decision_uid,
        trade_id=trade_id,
        role="ENTRY",
        status="SUBMITTED",
        qty=0.1,
    )
    store.update_order_status("0xentry", "FILLED", filled_qty=0.1, avg_fill_px=104.5, ts_last=now)
    store.insert_fill("fill-1", "0xentry", decision_uid, now, 0.1, 104.5, fee=0.01, funding=0.0)
    store.update_trade_exit(trade_id, exit_px=108.0, exit_ts=now, exit_reason="TP", pnl=0.35)
    store.insert_equity(run_id, now, equity=1000.0, cash=999.0, unrealized=1.0, realized_today=0.35)
    store.upsert_risk_day("2026-07-06", 1000.0, 0.35, 0.35, 0.01, 1, 0)
    store.insert_event(run_id, now, "INFO", "TEST_EVENT", "ok")

    chain = store.get_decision_chain(decision_uid)
    assert [row["stage"] for row in chain] == ["SIGNAL", "RISK_PASS"]
    assert chain[0]["payload"]["direction"] == "LONG"

    snapshot = store.get_snapshot()
    assert snapshot["runs"][0]["run_id"] == run_id
    assert snapshot["trades"][0]["trade_id"] == trade_id
    assert snapshot["orders"][0]["status"] == "FILLED"
    assert snapshot["fills"][0]["fill_id"] == "fill-1"
    assert snapshot["events"][0]["code"] == "TEST_EVENT"
    assert snapshot["bars"][0]["close"] == 104.0


# ===========================================================================
# TS-P1-009 — opt-in v9 kill evidence ledger (RED-first contract)
# ===========================================================================


def _v8_store_for_kill(tmp_path):
    store = Store(tmp_path / "kill-v9.db")
    store.initialize(target_schema_version=8)
    store.create_run("kill-run", "dry_run", "testnet", {})
    return store


def _repair4_stale_bind_worker(
    db_path, checkpoint_id, ready, release, results
):
    from bridge.store.db import Store

    store = Store(db_path)
    store.initialize()
    request, epoch = store.open_kill_epoch(
        run_id="kill-run",
        symbol="BTC",
        flatten_requested=True,
        policy_version="policy-v1",
        process_uid="repair4-process-old",
        opened_ts_monotonic=10.0,
    )
    store.mark_kill_request_state(
        epoch=epoch,
        state="SAFE_FLAT",
        reason_code="DIRECT_SAFE_FLAT_PROOF",
    )
    results.put(("old-open", epoch.as_payload()))
    ready.set()
    if not release.wait(15):
        results.put(("old-error", "release-timeout"))
        store.close()
        return
    try:
        store.bind_kill_terminal_proof(
            epoch=epoch,
            terminal_state="SAFE_FLAT",
            reason_code="DIRECT_SAFE_FLAT_PROOF",
            checkpoint_id=checkpoint_id,
            proof={"symbol": "BTC", "position_lots": 0},
        )
    except Exception as exc:  # noqa: BLE001 - report safe class/code only
        results.put((
            "old-stale",
            type(exc).__name__,
            str(getattr(exc, "reason_code", "")),
        ))
    else:
        results.put(("old-bound", request["episode_id"]))
    finally:
        store.close()


def _repair4_new_epoch_worker(db_path, results):
    from bridge.store.db import Store

    store = Store(db_path)
    store.initialize()
    _request, epoch = store.open_kill_epoch(
        run_id="kill-run",
        symbol="BTC",
        flatten_requested=True,
        policy_version="policy-v1",
        process_uid="repair4-process-new",
        opened_ts_monotonic=20.0,
    )
    results.put(("new-open", epoch.as_payload()))
    store.close()


def _repair4_join(process):
    process.join(15)
    if process.is_alive():
        process.terminate()
        process.join(5)
        pytest.fail("repair4 subprocess did not terminate")
    assert process.exitcode == 0


def _repair4_accepted_checkpoint(store):
    from bridge.broker.mock import MockBroker
    from bridge.engine.reconcile import FullReconciler
    from bridge.engine.risk import RiskEngine

    risk = RiskEngine()
    result = asyncio.run(
        FullReconciler(
            store=store,
            broker=MockBroker(bars=[]),
            run_id="kill-run",
            risk_policy=risk.policy,
            exposure_policy=risk.exposure_policy,
        ).run_cycle()
    )
    assert result.accepted is True
    checkpoint = store.latest_accepted_reconcile_checkpoint()
    assert checkpoint is not None
    return str(checkpoint["checkpoint_id"])


def test_v9_is_opt_in_and_creates_only_the_four_kill_objects(tmp_path):
    default = Store(tmp_path / "default.db")
    default.initialize()
    assert default.get_meta("schema_version") == "4"
    assert default.conn.execute(
        "SELECT name FROM sqlite_master WHERE name LIKE 'kill_%'"
    ).fetchall() == []

    upgraded = _v8_store_for_kill(tmp_path)
    upgraded.initialize(target_schema_version=9)

    assert upgraded.get_meta("schema_version") == "9"
    objects = {
        str(row["name"])
        for row in upgraded.conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name LIKE 'kill_%'"
        ).fetchall()
    }
    assert objects == {
        "kill_requests",
        "kill_attempts",
        "kill_actions",
        "kill_action_events",
    }
    assert upgraded.get_meta("kill_request_active") is None


def test_repair4_a7_cross_process_stale_bind_is_rejected_and_recorded(tmp_path):
    assert hasattr(Store, "open_kill_epoch"), "durable epoch OPEN seam is missing"
    db_path = tmp_path / "repair4-cross-process.db"
    store = Store(db_path)
    store.initialize(target_schema_version=8)
    store.create_run("kill-run", "dry_run", "testnet", {})
    store.initialize(target_schema_version=9)
    checkpoint_id = _repair4_accepted_checkpoint(store)
    store.close()

    context = multiprocessing.get_context("spawn")
    ready = context.Event()
    release = context.Event()
    results = context.Queue()
    older = context.Process(
        target=_repair4_stale_bind_worker,
        args=(db_path, checkpoint_id, ready, release, results),
    )
    older.start()
    assert ready.wait(15), "older recovery never opened attempt 1"
    old_open = results.get(timeout=5)
    assert old_open[0] == "old-open"

    newer = context.Process(
        target=_repair4_new_epoch_worker, args=(db_path, results)
    )
    newer.start()
    _repair4_join(newer)
    new_open = results.get(timeout=5)
    assert new_open[0] == "new-open"
    assert new_open[1]["attempt_no"] == old_open[1]["attempt_no"] + 1

    release.set()
    _repair4_join(older)
    stale = results.get(timeout=5)
    assert stale[:2] == ("old-stale", "KillConflictError")
    assert stale[2] == "KILL_EPOCH_STALE_WRITE"

    third = Store(db_path)
    third.initialize()
    with pytest.raises(Exception, match="KILL_NOT_SAFE|KILL_EPOCH"):
        third.acknowledge_kill_evidence(
            now=datetime.now(UTC), max_age_s=900.0
        )
    assert "KILL_EPOCH_STALE_WRITE_REJECTED" in {
        str(row["code"]) for row in third.get_events()
    }
    assert third.get_meta("kill_epoch_active") is not None
    third.close()


def test_repair4_a6_epoch_is_required_and_active_token_cannot_be_adopted(
    tmp_path,
):
    for operation in ("BIND_PROOF", "CLOSE_EPOCH"):
        path = tmp_path / f"repair4-owner-{operation.lower()}.db"
        older = Store(path)
        older.initialize(target_schema_version=8)
        older.create_run("kill-run", "dry_run", "testnet", {})
        older.initialize(target_schema_version=9)
        checkpoint_id = _repair4_accepted_checkpoint(older)
        _request, _epoch1 = older.open_kill_epoch(
            run_id="kill-run",
            symbol="BTC",
            flatten_requested=True,
            policy_version="policy-v1",
            process_uid="repair4-owner-old",
            opened_ts_monotonic=10.0,
        )
        newer = Store(path)
        newer.initialize()
        _request2, epoch2 = newer.open_kill_epoch(
            run_id="kill-run",
            symbol="BTC",
            flatten_requested=True,
            policy_version="policy-v1",
            process_uid="repair4-owner-new",
            opened_ts_monotonic=20.0,
        )
        newer.bind_kill_terminal_proof(
            epoch=epoch2,
            terminal_state="SAFE_FLAT",
            reason_code="DIRECT_SAFE_FLAT_PROOF",
            checkpoint_id=checkpoint_id,
            proof={"symbol": "BTC", "position_lots": 0},
        )
        adopted, state = older._parse_kill_epoch_token(
            older.get_meta("kill_epoch_active")
        )
        assert adopted == epoch2
        assert state == "OPEN"

        with pytest.raises(KillConflictError, match="KILL_EPOCH_STALE_WRITE"):
            if operation == "BIND_PROOF":
                older.bind_kill_terminal_proof(
                    epoch=adopted,
                    terminal_state="SAFE_FLAT",
                    reason_code="DIRECT_SAFE_FLAT_PROOF",
                    checkpoint_id=checkpoint_id,
                    proof={"symbol": "BTC", "position_lots": 0},
                )
            else:
                older.close_kill_epoch(epoch=adopted)
        newer.close()
        older.close()

    for method_name in (
        "mark_kill_request_state",
        "reserve_kill_action",
        "_append_kill_action_event_in_tx",
        "record_kill_action_event",
        "observe_kill_action_clock",
        "bind_kill_terminal_proof",
    ):
        parameter = inspect.signature(getattr(Store, method_name)).parameters[
            "epoch"
        ]
        assert parameter.default is inspect.Parameter.empty, method_name


def test_repair4_a8_stale_rejection_append_failure_is_observable(
    tmp_path, monkeypatch
):
    store = _v8_store_for_kill(tmp_path)
    store.initialize(target_schema_version=9)
    request, epoch1 = store.open_kill_epoch(
        run_id="kill-run",
        symbol="BTC",
        flatten_requested=True,
        policy_version="policy-v1",
        process_uid="repair4-stale-old",
        opened_ts_monotonic=10.0,
    )
    store.open_kill_epoch(
        run_id="kill-run",
        symbol="BTC",
        flatten_requested=True,
        policy_version="policy-v1",
        process_uid="repair4-stale-new",
        opened_ts_monotonic=20.0,
    )

    def fail_stale_append(*_args, **_kwargs):
        raise RuntimeError("injected stale rejection append failure")

    monkeypatch.setattr(store, "_insert_event_in_tx", fail_stale_append)

    with pytest.raises(KillConflictError) as failure:
        store.mark_kill_request_state(
            epoch=epoch1,
            episode_id=request["episode_id"],
            state="UNKNOWN",
            reason_code="STALE_ATTEMPT",
        )
    assert failure.value.reason_code == "KILL_STALE_EVIDENCE_RECORD_FAILED"
    assert failure.value.cause_reason_code == "KILL_EPOCH_STALE_WRITE"
    assert "caused_by=KILL_EPOCH_STALE_WRITE" in str(failure.value)


def test_repair4_a9_replay_appends_immutable_attempt_history(tmp_path):
    store = _v8_store_for_kill(tmp_path)
    store.initialize(target_schema_version=9)
    checkpoint_id = _repair4_accepted_checkpoint(store)
    request, epoch1 = store.open_kill_epoch(
        run_id="kill-run",
        symbol="BTC",
        flatten_requested=True,
        policy_version="policy-v1",
        process_uid="repair4-history-old",
        opened_ts_monotonic=10.0,
    )
    first = store.bind_kill_terminal_proof(
        epoch=epoch1,
        terminal_state="SAFE_FLAT",
        reason_code="DIRECT_SAFE_FLAT_PROOF",
        checkpoint_id=checkpoint_id,
        proof={"symbol": "BTC", "position_lots": 0},
    )
    first_digest = first["proof_digest"]

    _request2, epoch2 = store.open_kill_epoch(
        run_id="kill-run",
        symbol="BTC",
        flatten_requested=True,
        policy_version="policy-v1",
        process_uid="repair4-history-new",
        opened_ts_monotonic=20.0,
    )

    attempts = [
        dict(row)
        for row in store.conn.execute(
            "SELECT * FROM kill_attempts WHERE episode_id=? ORDER BY attempt_no",
            (request["episode_id"],),
        ).fetchall()
    ]
    assert [row["attempt_no"] for row in attempts] == [1, 2]
    assert attempts[0]["terminal_state"] == "SAFE_FLAT"
    assert attempts[0]["proof_digest"] == first_digest
    assert attempts[1]["terminal_state"] == "IN_PROGRESS"
    assert attempts[1]["proof_digest"] is None
    assert epoch2.attempt_no == 2
    with pytest.raises(Exception, match="immutable prior kill attempt"):
        store.conn.execute(
            """UPDATE kill_attempts SET terminal_reason='REWRITTEN'
               WHERE episode_id=? AND attempt_no=1""",
            (request["episode_id"],),
        )


@pytest.mark.parametrize("target", [4, 5, 6, 7, 8])
def test_legacy_v4_through_v8_initialize_never_activates_kill_schema(
    tmp_path, target
):
    store = Store(tmp_path / f"legacy-{target}.db")
    store.initialize(target_schema_version=target)
    assert store.get_meta("schema_version") == str(target)
    assert store.conn.execute(
        "SELECT name FROM sqlite_master WHERE name LIKE 'kill_%'"
    ).fetchall() == []
    assert store.get_meta("kill_request_active") is None


@pytest.mark.parametrize("target", [4, 5, 6, 7, 8])
def test_repair4_a12_legacy_reopen_stays_predecessor_and_epoch_inactive(
    tmp_path, target
):
    path = tmp_path / f"repair4-legacy-{target}.db"
    store = Store(path)
    store.initialize(target_schema_version=target)
    before = store.get_snapshot()
    store.close()

    reopened = Store(path)
    reopened.initialize(target_schema_version=target)
    assert reopened.get_meta("schema_version") == str(target)
    assert reopened.get_snapshot() == before
    assert reopened.get_meta("kill_request_active") is None
    assert reopened.get_meta("kill_epoch_active") is None
    assert hasattr(reopened, "open_kill_epoch"), "epoch seam is missing"
    with pytest.raises(Exception, match="KILL_SCHEMA_INACTIVE"):
        reopened.open_kill_epoch(
            run_id="unused",
            symbol="BTC",
            flatten_requested=False,
            policy_version="policy-v1",
            process_uid="repair4-legacy",
            opened_ts_monotonic=1.0,
        )
    reopened.close()


def test_v9_reopen_is_idempotent_and_future_target_is_rejected(tmp_path):
    path = tmp_path / "kill-v9.db"
    store = _v8_store_for_kill(tmp_path)
    store.initialize(target_schema_version=9)
    store.close()

    reopened = Store(path)
    reopened.initialize()
    assert reopened.get_meta("schema_version") == "9"

    with pytest.raises(RuntimeError, match="Unsupported target_schema_version"):
        reopened.initialize(target_schema_version=10)
    assert reopened.get_meta("schema_version") == "9"


def test_v8_to_v9_fault_rolls_back_and_retains_secret_safe_failure_evidence(
    tmp_path, monkeypatch
):
    store = _v8_store_for_kill(tmp_path)
    before = {
        str(row["name"])
        for row in store.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    original = getattr(Store, "_create_kill_evidence_tables_v9", None)
    assert original is not None

    def fail_after_ddl(self):
        original(self)
        raise RuntimeError("secret injected migration detail")

    monkeypatch.setattr(Store, "_create_kill_evidence_tables_v9", fail_after_ddl)
    with pytest.raises(Exception):
        store.initialize(target_schema_version=9)

    assert store.get_meta("schema_version") == "8"
    after = {
        str(row["name"])
        for row in store.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    assert after == before
    failure = store.get_meta("kill_evidence_migration_failure")
    assert failure is not None
    assert failure.startswith("KILL_EVIDENCE_MIGRATION_FAILED:")
    assert "secret" not in failure and "injected" not in failure

    store.close()
    reopened = Store(tmp_path / "kill-v9.db")
    reopened.initialize(target_schema_version=8)
    assert reopened.get_meta("schema_version") == "8"


def test_repair4_a13_epoch_topology_fault_rolls_back_to_reopenable_v8(
    tmp_path, monkeypatch
):
    store = _v8_store_for_kill(tmp_path)
    original = Store._create_kill_evidence_tables_v9

    def fail_after_epoch_ddl(self):
        original(self)
        columns = {
            str(row["name"])
            for row in self.conn.execute(
                "PRAGMA table_info(kill_requests)"
            ).fetchall()
        }
        if "epoch_token" not in columns:
            raise AssertionError("epoch_token column missing")
        raise RuntimeError("injected epoch topology fault")

    monkeypatch.setattr(
        Store, "_create_kill_evidence_tables_v9", fail_after_epoch_ddl
    )
    with pytest.raises(RuntimeError, match="epoch topology fault"):
        store.initialize(target_schema_version=9)

    assert store.get_meta("schema_version") == "8"
    assert store.get_meta("kill_epoch_active") is None
    assert store.conn.execute(
        "SELECT name FROM sqlite_master WHERE name LIKE 'kill_%'"
    ).fetchall() == []
    failure = store.get_meta("kill_evidence_migration_failure")
    # Reason codes fold the raw exception class name, matching the established
    # RISK_CONTROLS_MIGRATION_FAILED / EXPOSURE_CONTROLS_MIGRATION_FAILED
    # convention from TS-P1-007/008. Do not uppercase it here.
    assert failure == "KILL_EVIDENCE_MIGRATION_FAILED:RuntimeError"
    store.close()

    reopened = Store(tmp_path / "kill-v9.db")
    reopened.initialize(target_schema_version=8)
    assert reopened.get_meta("schema_version") == "8"
    reopened.close()


def test_v9_migration_rejects_noncanonical_residue_without_partial_topology(tmp_path):
    store = _v8_store_for_kill(tmp_path)
    store.conn.execute("CREATE TABLE kill_actions(bogus TEXT)")
    store.conn.commit()

    with pytest.raises(Exception, match="pre-existing object|topology"):
        store.initialize(target_schema_version=9)

    assert store.get_meta("schema_version") == "8"
    assert store.conn.execute(
        "SELECT name FROM sqlite_master WHERE name='kill_requests'"
    ).fetchone() is None
    assert store.conn.execute(
        "PRAGMA table_info(kill_actions)"
    ).fetchall()[0]["name"] == "bogus"


def test_v9_migration_meta_failure_rolls_back_to_reopenable_v8(tmp_path):
    store = _v8_store_for_kill(tmp_path)
    store.conn.execute(
        """CREATE TRIGGER fail_v9_meta BEFORE UPDATE ON meta
           WHEN NEW.key='schema_version' AND NEW.value='9'
           BEGIN SELECT RAISE(ABORT, 'injected meta failure'); END"""
    )
    store.conn.commit()

    with pytest.raises(Exception):
        store.initialize(target_schema_version=9)

    assert store.get_meta("schema_version") == "8"
    assert store.conn.execute(
        "SELECT name FROM sqlite_master WHERE name IN "
        "('kill_requests','kill_attempts','kill_actions','kill_action_events')"
    ).fetchall() == []


def test_v9_migration_rejects_dangling_active_pointer_before_ddl(tmp_path):
    store = _v8_store_for_kill(tmp_path)
    store.set_meta("kill_request_active", "kill-v1:" + "f" * 64)

    with pytest.raises(Exception, match="pointer|residual"):
        store.initialize(target_schema_version=9)

    assert store.get_meta("schema_version") == "8"
    assert store.get_meta("kill_request_active") == "kill-v1:" + "f" * 64
    assert store.conn.execute(
        "SELECT name FROM sqlite_master WHERE name='kill_requests'"
    ).fetchone() is None


def test_v9_migration_retains_legacy_killed_without_inventing_an_episode(tmp_path):
    store = _v8_store_for_kill(tmp_path)
    store.set_meta("app_state", "KILLED")

    store.initialize(target_schema_version=9)

    assert store.get_meta("app_state") == "KILLED"
    assert store.get_meta("kill_request_active") is None
    assert store.conn.execute("SELECT COUNT(*) FROM kill_requests").fetchone()[0] == 0


def test_kill_request_action_event_and_pointer_survive_reopen(tmp_path):
    store = _v8_store_for_kill(tmp_path)
    store.initialize(target_schema_version=9)
    episode, epoch = store.open_kill_epoch(
        run_id="kill-run",
        symbol="BTC",
        flatten_requested=True,
        policy_version="policy-v1",
        process_uid="store-roundtrip",
        opened_ts_monotonic=1.0,
    )
    flatten_action_id = compute_kill_action_id(
        episode_id=episode["episode_id"],
        kind="FLATTEN",
        target="BTC",
        qty_lots=125,
    )
    is_replay, action = store.reserve_kill_action(
        epoch=epoch,
        episode_id=episode["episode_id"],
        kind="FLATTEN",
        target="BTC",
        qty_lots=125,
        cloid=compute_kill_action_cloid(flatten_action_id),
        deadline_ts=datetime.now(UTC) + timedelta(seconds=5),
        exit_side="SELL",
    )
    assert is_replay is False
    store.record_kill_action_event(
        epoch=epoch,
        action_id=action["action_id"],
        status="UNKNOWN",
        reason_code="TRANSPORT_TIMEOUT",
        evidence_source="BROKER",
        evidence={"digest": "f" * 64},
    )
    episode_id = str(episode["episode_id"])
    action_id = str(action["action_id"])
    store.close()

    reopened = Store(tmp_path / "kill-v9.db")
    reopened.initialize()
    assert reopened.get_meta("app_state") == "KILLED"
    assert reopened.get_meta("kill_request_active") == episode_id
    assert reopened.active_kill_request()["episode_id"] == episode_id
    assert reopened.get_kill_action(action_id)["current_outcome"] == "UNKNOWN"
    assert [row["status"] for row in reopened.kill_action_events(action_id)] == [
        "RESERVED",
        "UNKNOWN",
    ]


def test_repair4_a11_restart_does_not_reset_unknown_action_deadline(tmp_path):
    assert hasattr(Store, "open_kill_epoch"), "durable epoch OPEN seam is missing"
    path = tmp_path / "repair4-deadline.db"
    store = Store(path)
    store.initialize(target_schema_version=8)
    store.create_run("kill-run", "dry_run", "testnet", {})
    store.initialize(target_schema_version=9)
    request, epoch1 = store.open_kill_epoch(
        run_id="kill-run",
        symbol="BTC",
        flatten_requested=True,
        policy_version="policy-v1",
        process_uid="repair4-before-restart",
        opened_ts_monotonic=100.0,
    )
    action_id = compute_kill_action_id(
        episode_id=request["episode_id"],
        kind="FLATTEN",
        target="BTC",
        qty_lots=1000,
    )
    original_deadline = datetime.now(UTC) + timedelta(seconds=5)
    replay, action = store.reserve_kill_action(
        epoch=epoch1,
        episode_id=request["episode_id"],
        kind="FLATTEN",
        target="BTC",
        qty_lots=1000,
        cloid=compute_kill_action_cloid(action_id),
        deadline_ts=original_deadline,
        action_id=action_id,
        exit_side="SELL",
    )
    assert replay is False
    store.record_kill_action_event(
        epoch=epoch1,
        action_id=action_id,
        status="UNKNOWN",
        reason_code="TRANSPORT_TIMEOUT",
    )
    persisted_deadline = action["deadline_ts"]
    store.close()

    reopened = Store(path)
    reopened.initialize()
    request2, epoch2 = reopened.open_kill_epoch(
        run_id="kill-run",
        symbol="BTC",
        flatten_requested=True,
        policy_version="policy-v1",
        process_uid="repair4-after-restart",
        opened_ts_monotonic=1.0,
    )
    replay, after = reopened.reserve_kill_action(
        epoch=epoch2,
        episode_id=request2["episode_id"],
        kind="FLATTEN",
        target="BTC",
        qty_lots=1000,
        cloid=compute_kill_action_cloid(action_id),
        deadline_ts=datetime.now(UTC) + timedelta(minutes=5),
        action_id=action_id,
        exit_side="SELL",
    )
    assert replay is True
    assert after["deadline_ts"] == persisted_deadline
    assert after["current_outcome"] == "UNKNOWN"
    assert [
        row["status"] for row in reopened.kill_action_events(action_id)
    ] == ["RESERVED", "UNKNOWN"]
    reopened.close()


def test_kill_action_identity_collision_fails_closed(tmp_path):
    store = _v8_store_for_kill(tmp_path)
    store.initialize(target_schema_version=9)
    episode, epoch = store.open_kill_epoch(
        run_id="kill-run",
        symbol="BTC",
        flatten_requested=False,
        policy_version="policy-v1",
        process_uid="store-collision",
        opened_ts_monotonic=1.0,
    )
    deadline = datetime.now(UTC) + timedelta(seconds=5)
    _, first = store.reserve_kill_action(
        epoch=epoch,
        episode_id=episode["episode_id"],
        kind="CANCEL",
        target="owned-entry",
        qty_lots=None,
        cloid="owned-entry",
        deadline_ts=deadline,
    )
    replay, same = store.reserve_kill_action(
        epoch=epoch,
        episode_id=episode["episode_id"],
        kind="CANCEL",
        target="owned-entry",
        qty_lots=None,
        cloid="owned-entry",
        deadline_ts=deadline + timedelta(seconds=30),
    )
    assert replay is True
    assert same["action_id"] == first["action_id"]
    assert same["deadline_ts"] == first["deadline_ts"]

    with pytest.raises(Exception, match="IDENTITY|CONFLICT"):
        store.reserve_kill_action(
            epoch=epoch,
            episode_id=episode["episode_id"],
            kind="CANCEL",
            target="different-entry",
            qty_lots=None,
            cloid="different-entry",
            deadline_ts=deadline,
            action_id=first["action_id"],
        )


# ===========================================================================
# TS-P1-004 — schema v5 partial-fill recovery ledger
# ===========================================================================

import sqlite3

import pytest

from bridge.store.db import (
    MigrationError,
    PartialRecoveryConflictError,
    compute_partial_action_cloid,
    compute_partial_action_id,
    compute_partial_recovery_id,
)

_REQUEST_ID = "request-v1:" + "c" * 64


def _v4_with_trade(tmp_path, *, target=4):
    store = Store(tmp_path / "bridge.db")
    store.initialize(target_schema_version=target)
    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store.create_run("run", mode="dry_run", network="testnet", config={})
    trade_id = store.create_trade(
        run_id="run", coin="BTC", direction="LONG", qty=2.0,
        entry_decision_uid="d1", signal_ts=now, decision_ts=now,
        expected_px=100.0, risk_dollars=1.0, risk_pct=0.001, leverage=1,
        sl_initial=95.0, tp_initial=None, llm_directive_id=None,
    )
    store.insert_order(
        cloid="entry-1", oid=1, group_id=_REQUEST_ID,
        order_ref=f"{_REQUEST_ID}:ENTRY", order_json={"symbol": "BTC"},
        decision_uid="d1", trade_id=trade_id, role="ENTRY", status="OPEN", qty=2.0,
    )
    return store, int(trade_id), now


@pytest.mark.parametrize(
    ("table", "column", "expected_type"),
    [
        pytest.param(table, column, expected_type, id=f"{table}.{column}")
        for (table, column), expected_type in DURABLE_EVENT_COLUMN_TYPES.items()
    ],
)
def test_s3t_a_registry_accepts_valid_typed_values(table, column, expected_type):
    value = 7 if expected_type == "INT64" else 7.25
    assert DURABLE_EVENT_ROWS.read(table, column, value) == value


@pytest.mark.parametrize(
    ("table", "column"),
    [
        pytest.param(table, column, id=f"{table}.{column}")
        for table, column in DURABLE_EVENT_COLUMN_TYPES
    ],
)
@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_s3t_a_registry_rejects_each_raw_non_finite_value(table, column, value):
    with pytest.raises(
        DurableRowFault,
        match=f"DURABLE_{table}_{column}_NON_FINITE".upper(),
    ):
        DURABLE_EVENT_ROWS.read(table, column, value)


def test_s3t_d_active_epoch_two_store_binding_break_rolls_back_and_records(
    tmp_path,
):
    store, trade_id, now = _v4_with_trade(tmp_path, target=9)
    request, epoch = store.open_kill_epoch(
        run_id="run",
        symbol="BTC",
        flatten_requested=True,
        policy_version="policy-v1",
        process_uid="s3t-binding-owner",
        opened_ts_monotonic=10.0,
    )
    store.insert_order(
        cloid="kill-flatten-1",
        oid=201,
        group_id=request["episode_id"],
        order_ref="kill-flatten-1:KILL_FLATTEN",
        order_json={"symbol": "BTC", "role": "KILL_FLATTEN"},
        decision_uid="d1",
        trade_id=trade_id,
        role="KILL_FLATTEN",
        status="FILLED",
        qty=2.0,
        filled_qty=2.0,
        ts_submit=now,
        ts_last=now,
    )
    competitor = Store(store.db_path)
    competitor.initialize(target_schema_version=9)

    # Store 1 has validated and owns the active epoch. Store 2 breaks only the
    # order-to-episode binding before Store 1 begins its close transaction.
    assert store.get_order("kill-flatten-1")["group_id"] == request["episode_id"]
    competitor.conn.execute(
        "UPDATE orders SET group_id=NULL WHERE cloid='kill-flatten-1'"
    )
    competitor.conn.commit()

    with pytest.raises(
        KillConflictError, match="KILL_LIFECYCLE_IDENTITY_MISSING"
    ) as rejected:
        store.close_trade_once_with_decision(
            trade_id=trade_id,
            run_id="run",
            decision_uid="d1",
            coin="BTC",
            exit_px=101.0,
            exit_ts=now,
            exit_reason="KILL_FLATTEN",
            pnl=2.0,
            payload={"exit_reason": "KILL_FLATTEN"},
            epoch=epoch,
        )

    assert rejected.value.reason_code == "KILL_LIFECYCLE_IDENTITY_MISSING"
    assert store.conn.in_transaction is False
    assert competitor.get_trade(trade_id)["exit_ts"] is None
    assert [
        row
        for row in competitor.get_decision_chain("d1")
        if row["stage"] == "TRADE_CLOSED"
    ] == []
    identity_events = [
        row
        for row in competitor.get_events()
        if row["code"] == "KILL_LIFECYCLE_IDENTITY_MISSING"
    ]
    assert len(identity_events) == 1
    assert f"trade_id={trade_id}" in identity_events[0]["detail"]
    competitor.close()
    store.close()


def test_lifecycle_close_requires_a_clean_connection_with_runtime_guard(tmp_path):
    store, trade_id, now = _v4_with_trade(tmp_path)
    store.conn.execute("BEGIN IMMEDIATE")
    try:
        with pytest.raises(RuntimeError, match="clean connection"):
            store.close_trade_once_with_decision(
                trade_id=trade_id,
                run_id="run",
                decision_uid="d1",
                coin="BTC",
                exit_px=101.0,
                exit_ts=now,
                exit_reason="CLOSE",
                pnl=2.0,
                payload={"exit_reason": "CLOSE"},
            )
        assert store.conn.in_transaction is True
    finally:
        store.conn.rollback()
        store.close()


def test_default_initialize_stays_on_schema_v4(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    assert store.get_meta("schema_version") == "4"
    assert store.partial_protection_enabled() is False
    residue = store.conn.execute(
        "SELECT name FROM sqlite_master WHERE name LIKE 'partial_fill_%'"
    ).fetchall()
    assert residue == []


def test_opt_in_v5_migration_is_additive_and_preserves_v4_rows(tmp_path):
    store, trade_id, _now = _v4_with_trade(tmp_path)
    orders = store.conn.execute("SELECT * FROM orders").fetchall()
    trades = store.conn.execute("SELECT * FROM trades").fetchall()
    store.close()

    upgraded = Store(tmp_path / "bridge.db")
    upgraded.initialize(target_schema_version=5)

    assert upgraded.get_meta("schema_version") == "5"
    assert upgraded.partial_protection_enabled() is True
    assert [dict(r) for r in upgraded.conn.execute("SELECT * FROM orders")] == [
        dict(r) for r in orders
    ]
    assert [dict(r) for r in upgraded.conn.execute("SELECT * FROM trades")] == [
        dict(r) for r in trades
    ]
    # no speculative backfill
    assert upgraded.list_partial_recoveries() == []


def test_v5_migration_rolls_back_completely_on_failure(tmp_path):
    class FailingStore(Store):
        def _validate_partial_fill_schema_v5(self):
            raise MigrationError("injected")

    store, _trade_id, _now = _v4_with_trade(tmp_path)
    store.close()

    failing = FailingStore(tmp_path / "bridge.db")
    with pytest.raises(MigrationError):
        failing.initialize(target_schema_version=5)

    assert failing.get_meta("schema_version") == "4"
    assert failing.conn.execute(
        "SELECT name FROM sqlite_master WHERE name LIKE 'partial_fill_%'"
    ).fetchall() == []
    assert failing.conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 1
    assert failing.conn.execute("SELECT COUNT(*) FROM trades").fetchone()[0] == 1


def test_v5_reopen_is_idempotent(tmp_path):
    store, _trade_id, _now = _v4_with_trade(tmp_path, target=5)
    store.close()
    for _ in range(3):
        reopened = Store(tmp_path / "bridge.db")
        reopened.initialize(target_schema_version=5)
        assert reopened.get_meta("schema_version") == "5"
        reopened.close()


def test_partial_recovery_and_action_identities_are_deterministic():
    first = compute_partial_recovery_id(trade_id=1, entry_cloid="e", generation=0)
    assert first == compute_partial_recovery_id(
        trade_id=1, entry_cloid="e", generation=0
    )
    assert first != compute_partial_recovery_id(
        trade_id=1, entry_cloid="e", generation=1
    )
    cancel = compute_partial_action_id(
        kind="CANCEL_ENTRY", trade_id=1, entry_cloid="e", entry_request_id=_REQUEST_ID
    )
    assert cancel.startswith("pfa-v1:")
    assert compute_partial_action_cloid(cancel).startswith("0x")
    assert len(compute_partial_action_cloid(cancel)) == 34


def test_reservation_transition_and_append_only_evidence(tmp_path):
    store, trade_id, now = _v4_with_trade(tmp_path, target=5)
    recovery = store.open_partial_recovery(
        run_id="run", symbol="BTC", trade_id=trade_id, entry_cloid="entry-1",
        entry_decision_uid="d1", entry_request_id=_REQUEST_ID,
        first_observed_ts=now, protect_deadline_ts=now + timedelta(seconds=10),
    )
    assert recovery["state"] == "PARTIAL_DETECTED"

    # idempotent open: the deadline is never rewritten
    again = store.open_partial_recovery(
        run_id="run", symbol="BTC", trade_id=trade_id, entry_cloid="entry-1",
        entry_decision_uid="d1", entry_request_id=_REQUEST_ID,
        first_observed_ts=now + timedelta(seconds=99),
        protect_deadline_ts=now + timedelta(seconds=999),
    )
    assert again["protect_deadline_ts"] == recovery["protect_deadline_ts"]

    action_id = compute_partial_action_id(
        kind="INSTALL_STOP", trade_id=trade_id, entry_cloid="entry-1",
        entry_request_id=_REQUEST_ID, generation=0, qty_lots=1000,
    )
    is_replay, row = store.reserve_partial_action(
        recovery_id=str(recovery["recovery_id"]), action_id=action_id,
        kind="INSTALL_STOP", target_cloid=compute_partial_action_cloid(action_id),
        expected_state="PARTIAL_DETECTED", next_state="PROTECTION_PENDING",
        reason_code="PROTECTION_RESERVED", generation=0, qty_lots=1000,
    )
    assert is_replay is False and row["qty_lots"] == 1000
    # the state transition is committed in the same transaction as the reservation
    assert store.get_partial_recovery(str(recovery["recovery_id"]))["state"] == (
        "PROTECTION_PENDING"
    )
    assert [e["status"] for e in store.partial_action_events(action_id)] == ["RESERVED"]

    store.record_partial_action_event(
        action_id=action_id, status="SENT", reason_code="PROTECTION_SENT"
    )
    store.record_partial_action_event(
        action_id=action_id, status="APPLIED", reason_code="MOCK_OK"
    )
    assert [e["seq"] for e in store.partial_action_events(action_id)] == [1, 2, 3]
    assert store.resolve_partial_action(action_id) == "APPLIED"

    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            "UPDATE partial_fill_action_events SET status='NOT_APPLIED'"
        )
    store.conn.rollback()


def test_reservation_identity_conflict_is_refused(tmp_path):
    store, trade_id, now = _v4_with_trade(tmp_path, target=5)
    recovery = store.open_partial_recovery(
        run_id="run", symbol="BTC", trade_id=trade_id, entry_cloid="entry-1",
        entry_decision_uid="d1", entry_request_id=_REQUEST_ID,
        first_observed_ts=now, protect_deadline_ts=now + timedelta(seconds=10),
    )
    action_id = compute_partial_action_id(
        kind="INSTALL_STOP", trade_id=trade_id, entry_cloid="entry-1",
        entry_request_id=_REQUEST_ID, generation=0, qty_lots=1000,
    )
    common = dict(
        recovery_id=str(recovery["recovery_id"]), action_id=action_id,
        kind="INSTALL_STOP", target_cloid=compute_partial_action_cloid(action_id),
        expected_state="PARTIAL_DETECTED", next_state="PROTECTION_PENDING",
        reason_code="PROTECTION_RESERVED", generation=0,
    )
    store.reserve_partial_action(qty_lots=1000, **common)
    common["expected_state"] = "PROTECTION_PENDING"
    with pytest.raises(PartialRecoveryConflictError) as exc:
        store.reserve_partial_action(qty_lots=1500, **common)
    assert exc.value.code == "PARTIAL_ACTION_IDENTITY_CONFLICT"


def test_generation_bump_preserves_deadline_and_first_observation(tmp_path):
    store, trade_id, now = _v4_with_trade(tmp_path, target=5)
    recovery = store.open_partial_recovery(
        run_id="run", symbol="BTC", trade_id=trade_id, entry_cloid="entry-1",
        entry_decision_uid="d1", entry_request_id=_REQUEST_ID,
        first_observed_ts=now, protect_deadline_ts=now + timedelta(seconds=10),
    )
    store.transition_partial_recovery(
        str(recovery["recovery_id"]), expected="PARTIAL_DETECTED",
        target="PROTECTION_PENDING", reason_code="X",
    )
    bumped = store.open_partial_generation(
        recovery_id=str(recovery["recovery_id"]), reason_code="LATE_FILL_REQUANTIFY",
        position_lots=1500,
    )
    assert bumped["generation"] == 1
    assert bumped["state"] == "PARTIAL_DETECTED"
    assert bumped["protect_deadline_ts"] == recovery["protect_deadline_ts"]
    assert bumped["first_observed_ts"] == recovery["first_observed_ts"]
    assert bumped["position_lots"] == 1500


def test_legacy_partial_entry_candidates_is_a_pure_local_query(tmp_path):
    store, trade_id, now = _v4_with_trade(tmp_path, target=5)
    assert store.legacy_partial_entry_candidates() == []

    store.insert_fill("f1", "entry-1", "d1", now, 1.0, 100.0, fee=0.0, funding=0.0)
    candidates = store.legacy_partial_entry_candidates()
    assert [c["cloid"] for c in candidates] == ["entry-1"]
    assert candidates[0]["ordered_qty"] == 2.0
    assert candidates[0]["filled_qty"] == 1.0

    # a fully filled entry is not a partial
    store.insert_fill("f2", "entry-1", "d1", now, 1.0, 100.0, fee=0.0, funding=0.0)
    assert store.legacy_partial_entry_candidates() == []


def test_blocking_and_rearm_queries(tmp_path):
    store, trade_id, now = _v4_with_trade(tmp_path, target=5)
    assert store.partial_recovery_blocks_new_risk() is False

    recovery = store.open_partial_recovery(
        run_id="run", symbol="BTC", trade_id=trade_id, entry_cloid="entry-1",
        entry_decision_uid="d1", entry_request_id=_REQUEST_ID,
        first_observed_ts=now, protect_deadline_ts=now + timedelta(seconds=10),
    )
    assert store.partial_recovery_blocks_new_risk() is True

    store.transition_partial_recovery(
        str(recovery["recovery_id"]), expected="PARTIAL_DETECTED",
        target="PROTECTION_PENDING", reason_code="X",
    )
    store.transition_partial_recovery(
        str(recovery["recovery_id"]), expected="PROTECTION_PENDING",
        target="PROTECTION_VERIFIED", reason_code="X",
    )
    store.transition_partial_recovery(
        str(recovery["recovery_id"]), expected="PROTECTION_VERIFIED",
        target="CANCEL_PENDING", reason_code="X",
    )
    store.transition_partial_recovery(
        str(recovery["recovery_id"]), expected="CANCEL_PENDING",
        target="PROTECTED_PARTIAL", reason_code="PROTECTED_PARTIAL",
    )
    assert store.partial_recovery_blocks_new_risk() is False
    assert [r["recovery_id"] for r in store.partial_recoveries_awaiting_rearm()] == [
        recovery["recovery_id"]
    ]

    store.transition_partial_recovery(
        str(recovery["recovery_id"]), expected="PROTECTED_PARTIAL",
        target="PROTECTED_PARTIAL", reason_code="REARM_ARCHIVED",
    )
    assert store.partial_recoveries_awaiting_rearm() == []


def test_unprotected_abort_is_a_sticky_latch(tmp_path):
    store, trade_id, now = _v4_with_trade(tmp_path, target=5)
    recovery = store.open_partial_recovery(
        run_id="run", symbol="BTC", trade_id=trade_id, entry_cloid="entry-1",
        entry_decision_uid="d1", entry_request_id=_REQUEST_ID,
        first_observed_ts=now, protect_deadline_ts=now + timedelta(seconds=10),
    )
    store.transition_partial_recovery(
        str(recovery["recovery_id"]), expected="PARTIAL_DETECTED",
        target="UNPROTECTED_ABORT", reason_code="MIXED_PROVENANCE",
    )
    assert store.partial_recovery_abort_active("BTC") is True
    assert store.partial_recovery_blocks_new_risk() is True
    assert store.active_partial_recovery_for_symbol("BTC") is None


# ---------------------------------------------------------------------------
# TS-P1-005 schema v6 (opt-in; default target stays v4)
# ---------------------------------------------------------------------------

_V6_OBJECTS = (
    "reconcile_attempts",
    "reconcile_components",
    "reconcile_diffs",
    "reconcile_checkpoints",
    "funding_events",
)


def _existing_objects(store) -> set[str]:
    rows = store.conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    ).fetchall()
    return {str(row["name"]) for row in rows}


def test_v6_capable_build_opened_with_default_target_stays_v4(tmp_path):
    """The operational baseline is untouched by TS-P1-005."""
    from bridge.store.db import SCHEMA_VERSION_FULL_RECONCILE, Store

    assert SCHEMA_VERSION_FULL_RECONCILE == 6
    store = Store(tmp_path / "bridge.db")
    store.initialize()

    assert store.get_meta("schema_version") == "4"
    assert store.full_reconcile_enabled() is False
    assert not (_existing_objects(store) & set(_V6_OBJECTS))
    assert store.latest_accepted_reconcile_checkpoint() is None
    store.close()


def test_v4_chain_can_reach_v6_and_keeps_v5_ledger(tmp_path):
    from bridge.store.db import Store

    store = Store(tmp_path / "bridge.db")
    store.initialize(target_schema_version=6)

    assert store.get_meta("schema_version") == "6"
    assert set(_V6_OBJECTS) <= _existing_objects(store)
    # v6 is strictly additive: the v5 recovery ledger is still present and
    # still authoritative, so partial-fill gating cannot silently switch off.
    assert {"partial_fill_recoveries", "partial_fill_actions"} <= _existing_objects(store)
    assert store.partial_protection_enabled() is True
    assert store.full_reconcile_enabled() is True
    store.close()


def test_v6_database_reopened_with_default_target_is_never_downgraded(tmp_path):
    from bridge.store.db import Store

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    store.close()

    reopened = Store(path)
    reopened.initialize()
    assert reopened.get_meta("schema_version") == "6"
    assert reopened.full_reconcile_enabled() is True
    reopened.close()


def test_v6_migration_aborts_on_a_preexisting_object_and_rolls_back(tmp_path):
    from bridge.store.db import MigrationError, Store

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=5)
    # Non-canonical residue squatting on a v6 name.
    store.conn.execute("CREATE TABLE funding_events (bogus TEXT)")
    store.conn.commit()

    with pytest.raises(MigrationError):
        store._migrate_v5_to_v6()

    assert store.get_meta("schema_version") == "5"
    remaining = _existing_objects(store)
    assert "reconcile_attempts" not in remaining
    assert "reconcile_checkpoints" not in remaining
    store.close()


def test_schema_version_claiming_v6_without_v6_objects_fails_closed(tmp_path):
    """A meta row alone is not proof of a version."""
    from bridge.store.db import Store

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize()
    store.conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '6')"
    )
    store.conn.commit()
    store.close()

    reopened = Store(path)
    with pytest.raises(RuntimeError, match="Unsupported schema_version"):
        reopened.initialize(target_schema_version=6)
    reopened.close()


def test_v6_reopen_rejects_a_tampered_topology(tmp_path):
    from bridge.store.db import MigrationError, Store

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    store.conn.execute("DROP TABLE funding_events")
    store.conn.commit()
    store.close()

    reopened = Store(path)
    with pytest.raises(MigrationError):
        reopened.initialize(target_schema_version=6)
    reopened.close()


def test_v6_checkpoint_pointer_must_resolve_on_reopen(tmp_path):
    from bridge.store.db import (
        RECONCILE_CHECKPOINT_POINTER_KEY,
        MigrationError,
        Store,
    )

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    store.set_meta(RECONCILE_CHECKPOINT_POINTER_KEY, "ckpt-v1:" + "0" * 64)
    store.close()

    reopened = Store(path)
    with pytest.raises(MigrationError):
        reopened.initialize(target_schema_version=6)
    reopened.close()


def test_reconcile_attempt_cannot_be_accepted_without_a_complete_state(tmp_path):
    from bridge.engine.types import ReconcileAttemptState
    from bridge.store.db import ReconcileConflictError, Store

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = Store(tmp_path / "bridge.db")
    store.initialize(target_schema_version=6)
    attempt_id = store.reserve_reconcile_attempt(
        run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
    )

    with pytest.raises(ReconcileConflictError):
        store.finalize_reconcile_attempt(
            attempt_id=attempt_id,
            state=ReconcileAttemptState.INCOMPLETE,
            ended_ts=now,
            duration_ms=1,
            canonical_hash="a" * 64,
            reason_code="BOGUS",
            accepted=True,
            fresh=True,
        )
    # The attempt is still open and no checkpoint exists.
    assert store.get_reconcile_attempt(attempt_id)["state"] == "COLLECTING"
    assert store.count_accepted_reconcile_checkpoints() == 0

    store.finalize_reconcile_attempt(
        attempt_id=attempt_id,
        state=ReconcileAttemptState.INCOMPLETE,
        ended_ts=now,
        duration_ms=1,
        canonical_hash=None,
        reason_code="TESTED",
        accepted=False,
        fresh=False,
    )
    with pytest.raises(ReconcileConflictError):
        store.finalize_reconcile_attempt(
            attempt_id=attempt_id,
            state=ReconcileAttemptState.COMPLETE,
            ended_ts=now,
            duration_ms=1,
            canonical_hash="b" * 64,
            reason_code="RETRY",
            accepted=True,
            fresh=True,
        )
    store.close()


def test_reconcile_ledger_methods_refuse_a_v4_store(tmp_path):
    from bridge.store.db import ReconcileConflictError, Store

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = Store(tmp_path / "bridge.db")
    store.initialize()

    with pytest.raises(ReconcileConflictError):
        store.reserve_reconcile_attempt(
            run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
        )
    assert store.latest_accepted_reconcile_checkpoint() is None
    assert store.count_accepted_reconcile_checkpoints() == 0
    assert store.list_funding_events() == []
    assert store.full_reconcile_ready(now=now, max_age_s=900.0) is False
    store.close()


def test_funding_event_identity_conflict_is_refused(tmp_path):
    from bridge.engine.types import (
        FundingAttribution,
        FundingEventRecord,
        ReconcileAttemptState,
    )
    from bridge.store.db import ReconcileConflictError, Store

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = Store(tmp_path / "bridge.db")
    store.initialize(target_schema_version=6)

    def record(amount: float) -> FundingEventRecord:
        return FundingEventRecord(
            event_id="0xhash",
            symbol="BTC",
            amount_usdc=amount,
            effective_ts=now,
            attribution=FundingAttribution.ATTRIBUTED,
        )

    def finalize(events):
        attempt_id = store.reserve_reconcile_attempt(
            run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
        )
        store.finalize_reconcile_attempt(
            attempt_id=attempt_id,
            state=ReconcileAttemptState.INCOMPLETE,
            ended_ts=now,
            duration_ms=1,
            canonical_hash=None,
            reason_code="TESTED",
            funding_events=events,
            accepted=False,
            fresh=False,
        )
        return attempt_id

    finalize([record(-1.0)])
    assert len(store.list_funding_events()) == 1
    # Exact replay is idempotent.
    finalize([record(-1.0)])
    assert len(store.list_funding_events()) == 1
    # A conflicting redefinition of the same identity is refused.
    with pytest.raises(ReconcileConflictError):
        finalize([record(-9.0)])
    assert len(store.list_funding_events()) == 1
    assert store.funding_total(symbol="BTC") == -1.0
    store.close()


# ---------------------------------------------------------------------------
# TS-P1-005 R1 — the live durable status set is derived, never hand-listed
# ---------------------------------------------------------------------------

_LIVE_STATUS_CASES = (
    "OPEN",
    "RESTING",
    "WAITING_CHILD",
    "SUBMITTED",
    "PARTIALLY_FILLED",
    "PENDING_CANCEL",
)

_TERMINAL_STATUS_CASES = ("FILLED", "CANCELED", "CANCELLED", "REJECTED", "EXPIRED")


def _seed_status_order(store, *, cloid: str, status: str, symbol: str = "BTC") -> None:
    store.insert_order(
        cloid=cloid,
        oid=1,
        group_id="g",
        order_ref=f"ref-{cloid}",
        order_json={"symbol": symbol},
        decision_uid=f"decision-{cloid}",
        trade_id=1,
        role="ENTRY",
        status=status,
        qty=0.1,
    )


@pytest.mark.parametrize("status", _LIVE_STATUS_CASES)
def test_live_local_orders_include_every_derived_live_status(tmp_path, status):
    """Present: a durable row in any live spelling is visible to reconciliation."""
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    _seed_status_order(store, cloid="0xlive", status=status)

    assert [row["cloid"] for row in store.live_local_orders()] == ["0xlive"]
    # A live status is a *known* status, so it never doubles as unknown state.
    assert store.local_orders_with_unknown_status() == []
    store.close()


@pytest.mark.parametrize("status", _TERMINAL_STATUS_CASES)
def test_live_local_orders_exclude_every_terminal_status(tmp_path, status):
    """Absent: a provably finished order is neither live nor unknown."""
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    _seed_status_order(store, cloid="0xdone", status=status)

    assert store.live_local_orders() == []
    assert store.local_orders_with_unknown_status() == []
    store.close()


def test_unknown_durable_status_is_never_silently_dropped(tmp_path):
    """A status outside the closed space is surfaced, not filtered away."""
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    _seed_status_order(store, cloid="0xweird", status="TRIGGER_PENDING")

    assert store.live_local_orders() == []
    unknown = store.local_orders_with_unknown_status()
    assert [row["cloid"] for row in unknown] == ["0xweird"]
    assert unknown[0]["status"] == "TRIGGER_PENDING"
    assert unknown[0]["symbol"] == "BTC"
    store.close()


def test_durable_status_space_is_derived_from_the_order_state_contract():
    """The set follows OrderState/aliases; it cannot silently fall behind."""
    from bridge.engine.types import (
        KNOWN_DURABLE_ORDER_STATUSES,
        LEGACY_LIVE_ORDER_STATUS_SPELLINGS,
        LIVE_DURABLE_ORDER_STATUSES,
        RAW_ORDER_STATUS_ALIASES,
        TERMINAL_DURABLE_ORDER_STATUSES,
        TERMINAL_ORDER_STATES,
        OrderState,
    )

    for state in OrderState:
        target = (
            TERMINAL_DURABLE_ORDER_STATUSES
            if state in TERMINAL_ORDER_STATES
            else LIVE_DURABLE_ORDER_STATUSES
        )
        assert state.value in target, state
    for raw, state in RAW_ORDER_STATUS_ALIASES.items():
        target = (
            TERMINAL_DURABLE_ORDER_STATUSES
            if state in TERMINAL_ORDER_STATES
            else LIVE_DURABLE_ORDER_STATUSES
        )
        assert raw in target, raw
    assert {"RESTING", "WAITING_CHILD"} <= LEGACY_LIVE_ORDER_STATUS_SPELLINGS
    assert LEGACY_LIVE_ORDER_STATUS_SPELLINGS <= LIVE_DURABLE_ORDER_STATUSES
    assert not (LIVE_DURABLE_ORDER_STATUSES & TERMINAL_DURABLE_ORDER_STATUSES)
    assert KNOWN_DURABLE_ORDER_STATUSES == (
        LIVE_DURABLE_ORDER_STATUSES | TERMINAL_DURABLE_ORDER_STATUSES
    )
    # The predecessor hand-written list is a strict subset of the derived one.
    assert {
        "OPEN", "SUBMITTED", "PENDING", "PENDING_NEW", "ACCEPTED",
        "PARTIALLY_FILLED", "PENDING_CANCEL",
    } <= LIVE_DURABLE_ORDER_STATUSES


# ---------------------------------------------------------------------------
# TS-P1-005 R2 / R5 — readiness recency and durable coverage continuity
# ---------------------------------------------------------------------------


def _v6_store(tmp_path, name: str = "bridge.db"):
    store = Store(tmp_path / name)
    store.initialize(target_schema_version=6)
    return store


def _ms(value):
    return int(value.timestamp() * 1000)


def _accept(
    store,
    *,
    now,
    coverage_ms: int,
    seq_hash: str = "a",
    diffs=(),
    duration_ms: int = 1,
    observed_ts=None,
    coverage_start_ms: int = 0,
    funding_rows=(),
    funding_events=(),
):
    from bridge.engine.types import (
        REQUIRED_RECONCILE_COMPONENTS,
        ComponentEvidence,
        ReconcileAttemptState,
        ReconcileComponentStatus,
        reconcile_digest,
    )

    attempt_id = store.reserve_reconcile_attempt(
        run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
    )
    components = tuple(
        ComponentEvidence(
            kind=kind,
            source="TEST",
            status=ReconcileComponentStatus.COMPLETE,
            observed_ts=observed_ts or now,
            rows=tuple(funding_rows) if kind.value == "FUNDING" else (),
            exact=True,
            complete=True,
            reason_code="TEST_COMPLETE",
            cursor_start_ms=coverage_start_ms if kind.value in {"FILLS", "FUNDING"} else None,
            cursor_end_ms=coverage_ms if kind.value in {"FILLS", "FUNDING"} else None,
        )
        for kind in REQUIRED_RECONCILE_COMPONENTS
    )
    payload = {
        "version": "test",
        "components": {
            component.kind.value: {
                "digest": component.digest,
                "cursor_start_ms": component.cursor_start_ms,
                "cursor_end_ms": component.cursor_end_ms,
            }
            for component in components
        },
        "diffs": [diff.canonical() for diff in diffs],
        "funding_event_ids": sorted(event.event_id for event in funding_events),
        "funding_event_digests": {
            event.event_id: event.digest for event in funding_events
        },
    }
    canonical_hash = reconcile_digest({
        "version": payload["version"],
        "components": {
            component.kind.value: component.digest for component in components
        },
        "diffs": [diff.canonical() for diff in diffs],
    })
    store.finalize_reconcile_attempt(
        attempt_id=attempt_id,
        state=ReconcileAttemptState.COMPLETE,
        ended_ts=now,
        duration_ms=duration_ms,
        canonical_hash=canonical_hash,
        reason_code="ACCEPTED",
        diffs=diffs,
        accepted=True,
        fresh=True,
        components=components,
        funding_events=funding_events,
        snapshot_payload=payload,
        coverage_upper_bound_ms=coverage_ms,
    )
    return attempt_id


def _fail_attempt(store, *, now, reason: str = "TESTED"):
    from bridge.engine.types import ReconcileAttemptState

    attempt_id = store.reserve_reconcile_attempt(
        run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
    )
    store.finalize_reconcile_attempt(
        attempt_id=attempt_id,
        state=ReconcileAttemptState.INCOMPLETE,
        ended_ts=now,
        duration_ms=1,
        canonical_hash=None,
        reason_code=reason,
        accepted=False,
        fresh=False,
    )
    return attempt_id


def test_a_later_failed_attempt_makes_a_young_checkpoint_not_ready(tmp_path):
    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = _v6_store(tmp_path)
    accepted = _accept(store, now=now, coverage_ms=_ms(now))

    assert store.latest_resolved_reconcile_attempt_id() == accepted
    assert store.full_reconcile_ready(now=now, max_age_s=900.0) is True

    _fail_attempt(store, now=now + timedelta(seconds=30))
    # The checkpoint is still young and still the accepted pointer - and it is
    # no longer the most recent word on the account, so it is not ready.
    assert store.latest_accepted_reconcile_checkpoint()["attempt_id"] == accepted
    assert (
        store.full_reconcile_ready(now=now + timedelta(seconds=31), max_age_s=900.0)
        is False
    )

    # Only a fresh accept restores readiness.
    later = now + timedelta(seconds=60)
    _accept(store, now=later, coverage_ms=_ms(later), seq_hash="b")
    assert (
        store.full_reconcile_ready(now=now + timedelta(seconds=61), max_age_s=900.0)
        is True
    )
    store.close()


def test_a_restart_interrupted_attempt_makes_readiness_false(tmp_path):
    path = tmp_path / "bridge.db"
    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = Store(path)
    store.initialize(target_schema_version=6)
    _accept(store, now=now, coverage_ms=_ms(now))
    # A capture that never resolved (crash/kill).
    store.reserve_reconcile_attempt(
        run_id="run",
        started_ts=now + timedelta(seconds=30),
        deadline_s=5.0,
        max_skew_s=5.0,
    )
    store.close()

    reopened = Store(path)
    reopened.initialize(target_schema_version=6)
    assert reopened.full_reconcile_ready(now=now, max_age_s=900.0) is True
    assert (
        reopened.resolve_interrupted_reconcile_attempts(
            observed_ts=now + timedelta(seconds=40)
        )
        == 1
    )
    assert (
        reopened.full_reconcile_ready(now=now + timedelta(seconds=41), max_age_s=900.0)
        is False
    )
    reopened.close()


def test_interrupted_attempt_order_is_wall_clock_rollback_proof(tmp_path):
    path = tmp_path / "bridge.db"
    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = Store(path)
    store.initialize(target_schema_version=6)
    accepted = _accept(store, now=now, coverage_ms=_ms(now))
    interrupted = store.reserve_reconcile_attempt(
        run_id="run",
        started_ts=now + timedelta(seconds=30),
        deadline_s=5.0,
        max_skew_s=5.0,
    )
    store.close()

    reopened = Store(path)
    reopened.initialize(target_schema_version=6)
    reopened.resolve_interrupted_reconcile_attempts(
        observed_ts=now - timedelta(minutes=5)
    )
    assert reopened.latest_resolved_reconcile_attempt_id() == interrupted
    assert reopened.latest_resolved_reconcile_attempt_id() != accepted
    assert reopened.full_reconcile_ready(now=now, max_age_s=900.0) is False
    reopened.close()


def test_store_cannot_publish_incomplete_or_nonfresh_checkpoint(tmp_path):
    from bridge.engine.types import ReconcileAttemptState
    from bridge.store.db import ReconcileConflictError

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = _v6_store(tmp_path)
    for fresh in (False, True):
        attempt_id = store.reserve_reconcile_attempt(
            run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
        )
        with pytest.raises(ReconcileConflictError):
            store.finalize_reconcile_attempt(
                attempt_id=attempt_id,
                state=ReconcileAttemptState.COMPLETE,
                ended_ts=now,
                duration_ms=1,
                canonical_hash="a" * 64,
                reason_code="ACCEPTED",
                components=(),
                accepted=True,
                fresh=fresh,
                snapshot_payload={"version": "test", "components": {}, "diffs": []},
                coverage_upper_bound_ms=1_000,
            )
    assert store.count_accepted_reconcile_checkpoints() == 0
    assert store.full_reconcile_ready(now=now, max_age_s=900.0) is False
    store.close()


def test_store_rejects_blocking_diff_and_over_deadline_acceptance(tmp_path):
    from bridge.engine.types import (
        ReconcileDiffKind,
        ReconcileDiffRecord,
        ReconcileOwnership,
    )
    from bridge.store.db import ReconcileConflictError

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = _v6_store(tmp_path)
    blocking = ReconcileDiffRecord(
        kind=ReconcileDiffKind.ORDER,
        subject="probe",
        reason_code="PROBE_BLOCK",
        ownership=ReconcileOwnership.UNKNOWN_OWNERSHIP,
        blocking=True,
    )
    with pytest.raises(ReconcileConflictError, match="RECONCILE_ACCEPT_BLOCKING_DIFF"):
        _accept(store, now=now, coverage_ms=_ms(now), diffs=(blocking,))
    with pytest.raises(ReconcileConflictError, match="RECONCILE_ACCEPT_ENVELOPE_INVALID"):
        _accept(
            store,
            now=now + timedelta(seconds=1),
            coverage_ms=_ms(now + timedelta(seconds=1)),
            duration_ms=5_001,
        )
    stale_now = now + timedelta(seconds=2)
    with pytest.raises(ReconcileConflictError, match="RECONCILE_ACCEPT_COMPONENT_STALE"):
        _accept(
            store,
            now=stale_now,
            coverage_ms=_ms(stale_now),
            observed_ts=stale_now - timedelta(seconds=6),
        )
    assert store.count_accepted_reconcile_checkpoints() == 0
    store.close()


def test_accepted_attempt_requires_and_derives_immutable_coverage(tmp_path):
    from bridge.engine.types import ReconcileAttemptState
    from bridge.store.db import ReconcileConflictError

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = _v6_store(tmp_path)
    assert store.reconcile_coverage_upper_bound_ms() is None

    attempt_id = store.reserve_reconcile_attempt(
        run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
    )
    with pytest.raises(ReconcileConflictError):
        store.finalize_reconcile_attempt(
            attempt_id=attempt_id,
            state=ReconcileAttemptState.COMPLETE,
            ended_ts=now,
            duration_ms=1,
            canonical_hash="a" * 64,
            reason_code="ACCEPTED",
            accepted=True,
            fresh=True,
            snapshot_payload={"version": "test"},
        )
    assert store.get_reconcile_attempt(attempt_id)["state"] == "COLLECTING"
    assert store.reconcile_coverage_upper_bound_ms() is None

    # A fully proven checkpoint derives coverage from its immutable components.
    store.finalize_reconcile_attempt(
        attempt_id=attempt_id,
        state=ReconcileAttemptState.INCOMPLETE,
        ended_ts=now,
        duration_ms=1,
        canonical_hash=None,
        reason_code="TESTED",
        accepted=False,
        fresh=False,
    )
    first_accept = now + timedelta(seconds=1)
    first_bound = _ms(first_accept)
    _accept(store, now=first_accept, coverage_ms=first_bound)
    assert store.reconcile_coverage_upper_bound_ms() == first_bound
    assert store.get_meta("reconcile_coverage_upper_bound_ms") is None

    # A failed attempt never moves coverage.
    _fail_attempt(store, now=now + timedelta(seconds=10))
    assert store.reconcile_coverage_upper_bound_ms() == first_bound

    # Coverage is monotonic: a backwards bound is refused and rolls back whole.
    with pytest.raises(ReconcileConflictError):
        rollback = now - timedelta(seconds=20)
        _accept(store, now=rollback, coverage_ms=_ms(rollback))
    assert store.reconcile_coverage_upper_bound_ms() == first_bound
    assert store.count_accepted_reconcile_checkpoints() == 1
    store.close()


def test_store_rejects_discontinuous_accepted_coverage(tmp_path):
    from bridge.store.db import ReconcileConflictError

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = _v6_store(tmp_path)
    _accept(store, now=now, coverage_ms=_ms(now))
    later = now + timedelta(seconds=10)
    with pytest.raises(ReconcileConflictError, match="RECONCILE_ACCEPT_COVERAGE_GAP"):
        _accept(
            store,
            now=later,
            coverage_start_ms=_ms(now) + 1,
            coverage_ms=_ms(later),
        )


def test_store_rejects_funding_component_without_ledger_event(tmp_path):
    from bridge.store.db import ReconcileConflictError

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = _v6_store(tmp_path)
    funding_row = {
        "event_id": "0xfund",
        "symbol": "BTC",
        "amount_usdc": -1.0,
        "effective_ts_ms": _ms(now),
        "source": "TEST",
    }
    with pytest.raises(
        ReconcileConflictError, match="RECONCILE_ACCEPT_FUNDING_LEDGER_MISMATCH"
    ):
        _accept(
            store,
            now=now,
            coverage_ms=_ms(now),
            funding_rows=(funding_row,),
            funding_events=(),
        )
    store.close()


def test_store_rejects_semantically_different_funding_record(tmp_path):
    from bridge.engine.types import FundingEventRecord
    from bridge.store.db import ReconcileConflictError

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = _v6_store(tmp_path)
    component_row = {
        "event_id": "0xfund-semantic",
        "symbol": "BTC",
        "amount_usdc": -1.0,
        "effective_ts_ms": _ms(now),
        "source": "TEST",
        "funding_rate": None,
        "position_szi": None,
        "n_samples": None,
    }
    different = FundingEventRecord(
        event_id="0xfund-semantic",
        symbol="BTC",
        amount_usdc=-9.0,
        effective_ts=now,
        source="TEST",
    )
    with pytest.raises(
        ReconcileConflictError, match="RECONCILE_ACCEPT_FUNDING_LEDGER_MISMATCH"
    ):
        _accept(
            store,
            now=now,
            coverage_ms=_ms(now),
            funding_rows=(component_row,),
            funding_events=(different,),
        )
    assert store.count_accepted_reconcile_checkpoints() == 0
    store.close()


def test_unauthorized_coverage_pointer_fails_closed_on_reopen(tmp_path):
    from bridge.store.db import MigrationError, Store

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    store.set_meta("reconcile_coverage_upper_bound_ms", "1234")
    store.close()

    reopened = Store(path)
    with pytest.raises(MigrationError):
        reopened.initialize(target_schema_version=6)
    reopened.close()


# ===========================================================================
# TS-P1-006 - authoritative risk-input snapshot loader
#
# Written against docs/27_AUTHORITATIVE_RISK_SNAPSHOT_CONTRACT.md, not against
# the implementation: an incomplete, superseded, legacy, tampered, stale or
# unverifiable checkpoint must never be presented to risk as a portfolio view,
# and there is no "empty snapshot" a caller could mistake for "no exposure".
# ===========================================================================


DEFAULT_RISK_ROWS = {
    "POSITIONS": [],
    "BALANCES": [{"equity": 10_000.0, "withdrawable": 9_000.0}],
    "MARGIN": [{"margin_used": 1_000.0, "available_margin": 9_000.0}],
}

NOW = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)


def _accept_v2(
    store,
    *,
    now,
    coverage_ms: int,
    risk_rows=None,
    payload_version: str | None = None,
    tamper_rows=None,
    bypass_accept_validation: bool = False,
    diffs=(),
    coverage_start_ms: int = 0,
    run_id: str = "run",
    risk_policy=None,
    funding_rows=(),
    funding_events=(),
):
    """Accept one checkpoint whose payload carries canonical risk rows.

    ``tamper_rows`` writes *different* row content into the payload while the
    persisted component provenance (row_count, digest, cursor bounds) still
    describes the honest rows - the semantic-tamper attack.

    ``bypass_accept_validation`` disables only the *write-side* v2 check, so a
    test can put evidence on disk that the current writer would have refused:
    a checkpoint produced by a rollback-era build, a foreign writer, or direct
    database manipulation. The loader must still refuse it on its own, without
    relying on the write-side guard having ever run.
    """
    from bridge.engine.types import (
        REQUIRED_RECONCILE_COMPONENTS,
        RISK_SNAPSHOT_COMPONENTS,
        SNAPSHOT_PAYLOAD_VERSION_V2,
        ComponentEvidence,
        ReconcileAttemptState,
        ReconcileComponentStatus,
        reconcile_digest,
    )

    rows = {**DEFAULT_RISK_ROWS, **(risk_rows or {})}
    if funding_rows:
        rows = {**rows, "FUNDING": list(funding_rows)}
    version = payload_version or SNAPSHOT_PAYLOAD_VERSION_V2
    attempt_id = store.reserve_reconcile_attempt(
        run_id=run_id, started_ts=now, deadline_s=5.0, max_skew_s=5.0
    )
    components = tuple(
        ComponentEvidence(
            kind=kind,
            source="TEST",
            status=ReconcileComponentStatus.COMPLETE,
            observed_ts=now,
            rows=tuple(rows.get(kind.value, ())),
            exact=True,
            complete=True,
            reason_code="TEST_COMPLETE",
            cursor_start_ms=(
                coverage_start_ms if kind.value in {"FILLS", "FUNDING"} else None
            ),
            cursor_end_ms=coverage_ms if kind.value in {"FILLS", "FUNDING"} else None,
        )
        for kind in REQUIRED_RECONCILE_COMPONENTS
    )
    by_kind = {component.kind.value: component for component in components}
    payload = {
        "version": version,
        "run_id": run_id,
        "risk_rows": {
            kind.value: by_kind[kind.value].canonical_rows()
            for kind in RISK_SNAPSHOT_COMPONENTS
        },
        "risk_row_digests": {
            kind.value: by_kind[kind.value].digest for kind in RISK_SNAPSHOT_COMPONENTS
        },
        "components": {
            component.kind.value: {
                "digest": component.digest,
                "cursor_start_ms": component.cursor_start_ms,
                "cursor_end_ms": component.cursor_end_ms,
            }
            for component in components
        },
        "diffs": [diff.canonical() for diff in diffs],
        "funding_event_ids": sorted(event.event_id for event in funding_events),
        "funding_event_digests": {
            event.event_id: event.digest for event in funding_events
        },
    }
    canonical_hash = reconcile_digest({
        "version": version,
        "components": {
            component.kind.value: component.digest for component in components
        },
        "diffs": [diff.canonical() for diff in diffs],
    })
    if tamper_rows is not None:
        # The rows change; row_count, digests, cursor bounds and the canonical
        # hash all keep describing the honest evidence.
        payload["risk_rows"] = {**payload["risk_rows"], **tamper_rows}
    finalize = lambda: store.finalize_reconcile_attempt(  # noqa: E731
        attempt_id=attempt_id,
        state=ReconcileAttemptState.COMPLETE,
        ended_ts=now,
        duration_ms=1,
        canonical_hash=canonical_hash,
        reason_code="ACCEPTED",
        diffs=diffs,
        accepted=True,
        fresh=True,
        components=components,
        funding_events=funding_events,
        snapshot_payload=payload,
        coverage_upper_bound_ms=coverage_ms,
        **({} if risk_policy is None else {"risk_policy": risk_policy}),
    )
    if bypass_accept_validation:
        # Keep the descriptor itself so the restore cannot silently turn a
        # staticmethod into a bound method and leak into later tests.
        original = Store.__dict__["_validate_v2_risk_rows"]
        Store._validate_v2_risk_rows = staticmethod(lambda payload, components: None)
        try:
            finalize()
        finally:
            Store._validate_v2_risk_rows = original
    else:
        finalize()
    return attempt_id


def _accept_v1_legacy(store, *, now, coverage_ms: int, coverage_start_ms: int = 0):
    """Exactly the accepted TS-P1-005 payload: digests and counts, no rows."""
    from bridge.engine.types import (
        REQUIRED_RECONCILE_COMPONENTS,
        SNAPSHOT_PAYLOAD_VERSION_V1,
        ComponentEvidence,
        ReconcileAttemptState,
        ReconcileComponentStatus,
        reconcile_digest,
    )

    attempt_id = store.reserve_reconcile_attempt(
        run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
    )
    components = tuple(
        ComponentEvidence(
            kind=kind,
            source="TEST",
            status=ReconcileComponentStatus.COMPLETE,
            observed_ts=now,
            rows=tuple(DEFAULT_RISK_ROWS.get(kind.value, ())),
            exact=True,
            complete=True,
            reason_code="TEST_COMPLETE",
            cursor_start_ms=(
                coverage_start_ms if kind.value in {"FILLS", "FUNDING"} else None
            ),
            cursor_end_ms=coverage_ms if kind.value in {"FILLS", "FUNDING"} else None,
        )
        for kind in REQUIRED_RECONCILE_COMPONENTS
    )
    payload = {
        "version": SNAPSHOT_PAYLOAD_VERSION_V1,
        "run_id": "run",
        "components": {
            component.kind.value: {
                "digest": component.digest,
                "row_count": len(component.rows),
                "cursor_start_ms": component.cursor_start_ms,
                "cursor_end_ms": component.cursor_end_ms,
            }
            for component in components
        },
        "diffs": [],
        "funding_event_ids": [],
        "funding_event_digests": {},
    }
    canonical_hash = reconcile_digest({
        "version": SNAPSHOT_PAYLOAD_VERSION_V1,
        "components": {
            component.kind.value: component.digest for component in components
        },
        "diffs": [],
    })
    store.finalize_reconcile_attempt(
        attempt_id=attempt_id,
        state=ReconcileAttemptState.COMPLETE,
        ended_ts=now,
        duration_ms=1,
        canonical_hash=canonical_hash,
        reason_code="ACCEPTED",
        diffs=(),
        accepted=True,
        fresh=True,
        components=components,
        funding_events=(),
        snapshot_payload=payload,
        coverage_upper_bound_ms=coverage_ms,
    )
    return attempt_id


def _load(store, *, now, max_age_s: float = 900.0):
    return store.load_authoritative_risk_snapshot(now=now, max_age_s=max_age_s)


def _veto(store, *, now, max_age_s: float = 900.0) -> str:
    """Assert the load fails closed and return its stable reason code."""
    from bridge.engine.types import RiskSnapshotUnavailable

    with pytest.raises(RiskSnapshotUnavailable) as excinfo:
        _load(store, now=now, max_age_s=max_age_s)
    return excinfo.value.reason_code


def test_v2_checkpoint_loads_as_one_immutable_typed_snapshot(tmp_path):
    from bridge.engine.types import (
        SNAPSHOT_PAYLOAD_VERSION_V2,
        AuthoritativeRiskSnapshot,
    )

    store = _v6_store(tmp_path)
    attempt = _accept_v2(
        store,
        now=NOW,
        coverage_ms=_ms(NOW),
        risk_rows={"POSITIONS": [{"symbol": "BTC", "size": 0.0}]},
    )

    snapshot = _load(store, now=NOW + timedelta(seconds=5))
    assert isinstance(snapshot, AuthoritativeRiskSnapshot)
    assert snapshot.payload_version == SNAPSHOT_PAYLOAD_VERSION_V2
    assert snapshot.attempt_id == attempt
    assert snapshot.run_id == "run"
    checkpoint = store.latest_accepted_reconcile_checkpoint()
    assert snapshot.checkpoint_id == checkpoint["checkpoint_id"]
    assert snapshot.canonical_hash == checkpoint["canonical_hash"]
    assert snapshot.equity == 10_000.0
    assert snapshot.withdrawable == 9_000.0
    assert snapshot.margin_used == 1_000.0
    assert snapshot.available_margin == 9_000.0
    assert tuple(snapshot.positions[0]) == ("BTC", 0.0)
    assert snapshot.has_open_position is False
    assert snapshot.age_s == 5.0
    assert snapshot.accepted_ts == NOW
    assert snapshot.observed_from_ts == NOW and snapshot.observed_to_ts == NOW
    assert snapshot.coverage_end_ms == _ms(NOW)
    # The account view handed to the gates is derived, never re-read.
    account = snapshot.account()
    assert (account.equity, account.available_margin, account.withdrawable) == (
        10_000.0,
        9_000.0,
        9_000.0,
    )
    store.close()


def test_snapshot_is_deeply_immutable_with_no_writable_holder(tmp_path):
    """A frozen dataclass would still expose a writable __dict__ here."""
    import gc

    store = _v6_store(tmp_path)
    _accept_v2(
        store,
        now=NOW,
        coverage_ms=_ms(NOW),
        risk_rows={"POSITIONS": [{"symbol": "BTC", "size": 2.0}]},
    )
    snapshot = _load(store, now=NOW)

    for target, name in ((snapshot, "equity"), (snapshot.positions[0], "size")):
        with pytest.raises(AttributeError):
            setattr(target, name, 1.0)
        with pytest.raises(AttributeError):
            object.__setattr__(target, name, 1.0)
        with pytest.raises(AttributeError):
            object.__setattr__(target, "__class__", tuple)
        with pytest.raises(AttributeError):
            object.__setattr__(target, "smuggled", 1.0)

    seen: set[int] = set()
    stack = [snapshot]
    mutable: list[str] = []
    while stack:
        item = stack.pop()
        if id(item) in seen:
            continue
        seen.add(id(item))
        if isinstance(item, (dict, list, set, bytearray)):
            mutable.append(type(item).__name__)
        for referent in gc.get_referents(item):
            if isinstance(referent, type):
                continue
            stack.append(referent)
    assert mutable == [], f"mutable containers reachable from the snapshot: {mutable}"
    assert snapshot.equity == 10_000.0
    assert snapshot.positions[0].size == 2.0
    store.close()


def test_canonical_rows_and_hash_are_row_order_independent(tmp_path):
    """Permuting the wire order changes neither the hash nor the loaded view."""
    forward = [
        {"symbol": "AAA", "size": 1.0},
        {"symbol": "BBB", "size": -2.0},
        {"symbol": "CCC", "size": 0.0},
    ]
    loaded = []
    hashes = []
    for index, rows in enumerate((forward, list(reversed(forward)))):
        store = _v6_store(tmp_path, name=f"perm-{index}.db")
        _accept_v2(store, now=NOW, coverage_ms=_ms(NOW), risk_rows={"POSITIONS": rows})
        hashes.append(store.latest_accepted_reconcile_checkpoint()["canonical_hash"])
        loaded.append(_load(store, now=NOW).positions)
        store.close()

    assert hashes[0] == hashes[1], "canonical hash must not depend on row order"
    assert loaded[0] == loaded[1]
    # Canonical order is the accepted TS-P1-005 order: the sorted canonical JSON
    # of the whole row, not the symbol. Both permutations resolve to it exactly.
    assert [row.symbol for row in loaded[0]] == ["BBB", "CCC", "AAA"]
    assert [row.size for row in loaded[0]] == [-2.0, 0.0, 1.0]


def test_legacy_v1_checkpoint_is_retained_reopenable_and_never_risk_readable(tmp_path):
    import json

    from bridge.engine.types import (
        RISK_SNAPSHOT_LEGACY_PAYLOAD,
        SNAPSHOT_PAYLOAD_VERSION_V1,
    )

    path = tmp_path / "legacy.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    attempt = _accept_v1_legacy(store, now=NOW, coverage_ms=_ms(NOW))
    original = dict(store.latest_accepted_reconcile_checkpoint())
    assert _veto(store, now=NOW) == RISK_SNAPSHOT_LEGACY_PAYLOAD
    store.close()

    reopened = Store(path)
    reopened.initialize(target_schema_version=6)
    # The predecessor evidence is byte-for-byte retained and still reopenable...
    survivor = reopened.latest_accepted_reconcile_checkpoint()
    assert survivor == original
    assert survivor["attempt_id"] == attempt
    assert json.loads(survivor["snapshot_json"])["version"] == (
        SNAPSHOT_PAYLOAD_VERSION_V1
    )
    # ...and the predecessor readiness gate still accepts it, which is exactly
    # why risk needs its own, stricter authority.
    assert reopened.full_reconcile_ready(now=NOW, max_age_s=900.0) is True
    assert _veto(reopened, now=NOW) == RISK_SNAPSHOT_LEGACY_PAYLOAD

    # Only a fresh real v2 capture restores risk authority.
    later = NOW + timedelta(seconds=60)
    _accept_v2(reopened, now=later, coverage_ms=_ms(later), coverage_start_ms=_ms(NOW))
    assert _load(reopened, now=later).equity == 10_000.0
    # The old evidence was not rewritten or deleted.
    assert reopened.get_reconcile_attempt(attempt)["reason_code"] == "ACCEPTED"
    assert reopened.count_accepted_reconcile_checkpoints() == 2
    reopened.close()


def test_unknown_payload_version_fails_closed(tmp_path):
    from bridge.engine.types import RISK_SNAPSHOT_PAYLOAD_VERSION_UNSUPPORTED

    store = _v6_store(tmp_path)
    _accept_v2(store, now=NOW, coverage_ms=_ms(NOW), payload_version="ts-p9-future")
    assert _veto(store, now=NOW) == RISK_SNAPSHOT_PAYLOAD_VERSION_UNSUPPORTED
    store.close()


def test_stale_and_future_checkpoints_fail_closed(tmp_path):
    from bridge.engine.types import RISK_SNAPSHOT_FUTURE_CLOCK, RISK_SNAPSHOT_STALE

    store = _v6_store(tmp_path)
    _accept_v2(store, now=NOW, coverage_ms=_ms(NOW))

    # Exactly on the bound is still authoritative.
    assert _load(store, now=NOW + timedelta(seconds=180), max_age_s=180.0).equity
    assert (
        _veto(store, now=NOW + timedelta(seconds=181), max_age_s=180.0)
        == RISK_SNAPSHOT_STALE
    )
    # A checkpoint accepted in the future is a clock failure, not a fresh one.
    assert (
        _veto(store, now=NOW - timedelta(seconds=1), max_age_s=180.0)
        == RISK_SNAPSHOT_FUTURE_CLOCK
    )
    store.close()


def test_a_later_failed_attempt_supersedes_a_young_checkpoint_for_risk(tmp_path):
    from bridge.engine.types import RISK_SNAPSHOT_SUPERSEDED

    store = _v6_store(tmp_path)
    _accept_v2(store, now=NOW, coverage_ms=_ms(NOW))
    assert _load(store, now=NOW).equity == 10_000.0

    _fail_attempt(store, now=NOW + timedelta(seconds=30))
    assert _veto(store, now=NOW + timedelta(seconds=31)) == RISK_SNAPSHOT_SUPERSEDED

    later = NOW + timedelta(seconds=60)
    _accept_v2(store, now=later, coverage_ms=_ms(later), coverage_start_ms=_ms(NOW))
    assert _load(store, now=later).equity == 10_000.0
    store.close()


def test_an_interrupted_capture_supersedes_the_snapshot_after_restart(tmp_path):
    """Crash/restart may never expose a partial or pre-crash-authoritative view."""
    from bridge.engine.types import RISK_SNAPSHOT_SUPERSEDED

    path = tmp_path / "crash.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    _accept_v2(store, now=NOW, coverage_ms=_ms(NOW))
    dangling = store.reserve_reconcile_attempt(
        run_id="run",
        started_ts=NOW + timedelta(seconds=30),
        deadline_s=5.0,
        max_skew_s=5.0,
    )
    store.close()

    reopened = Store(path)
    reopened.initialize(target_schema_version=6)
    # The half-finished capture never published anything.
    assert reopened.count_accepted_reconcile_checkpoints() == 1
    assert reopened.get_reconcile_attempt(dangling)["state"] == "COLLECTING"
    reopened.resolve_interrupted_reconcile_attempts(
        observed_ts=NOW + timedelta(seconds=35)
    )
    assert reopened.get_reconcile_attempt(dangling)["state"] == "INCOMPLETE"
    assert _veto(reopened, now=NOW + timedelta(seconds=40)) == RISK_SNAPSHOT_SUPERSEDED
    reopened.close()


def test_missing_pointer_dangling_pointer_and_v4_store_fail_closed(tmp_path):
    from bridge.engine.types import (
        RISK_SNAPSHOT_NO_CHECKPOINT,
        RISK_SNAPSHOT_POINTER_DANGLING,
        RISK_SNAPSHOT_SCHEMA_INACTIVE,
    )
    from bridge.store.db import RECONCILE_CHECKPOINT_POINTER_KEY

    v4 = Store(tmp_path / "v4.db")
    v4.initialize()
    assert _veto(v4, now=NOW) == RISK_SNAPSHOT_SCHEMA_INACTIVE
    v4.close()

    store = _v6_store(tmp_path, name="pointer.db")
    assert _veto(store, now=NOW) == RISK_SNAPSHOT_NO_CHECKPOINT
    _accept_v2(store, now=NOW, coverage_ms=_ms(NOW))
    store.set_meta(RECONCILE_CHECKPOINT_POINTER_KEY, "ckpt-v1:" + "0" * 64)
    assert _veto(store, now=NOW) == RISK_SNAPSHOT_POINTER_DANGLING
    store.close()


def test_semantically_tampered_rows_are_rejected_despite_intact_metadata(tmp_path):
    """row_count, digests and cursor bounds all still describe the honest rows.

    The evidence is planted with the write-side guard disabled, so this proves
    the *loader* recomputes semantics rather than trusting stored metadata or
    the fact that some earlier writer validated it.
    """
    from bridge.engine.types import RISK_SNAPSHOT_ROW_DIGEST_MISMATCH

    store = _v6_store(tmp_path)
    _accept_v2(
        store,
        now=NOW,
        coverage_ms=_ms(NOW),
        risk_rows={"POSITIONS": [{"symbol": "BTC", "size": 3.0}]},
        # Same row count, same stored digest, different exposure.
        tamper_rows={"POSITIONS": [{"symbol": "BTC", "size": 0.0}]},
        bypass_accept_validation=True,
    )
    assert _veto(store, now=NOW) == RISK_SNAPSHOT_ROW_DIGEST_MISMATCH
    store.close()

    inflated = _v6_store(tmp_path, name="inflate.db")
    _accept_v2(
        inflated,
        now=NOW,
        coverage_ms=_ms(NOW),
        tamper_rows={"BALANCES": [{"equity": 10_000_000.0, "withdrawable": 9_000.0}]},
        bypass_accept_validation=True,
    )
    assert _veto(inflated, now=NOW) == RISK_SNAPSHOT_ROW_DIGEST_MISMATCH
    inflated.close()


def test_non_canonical_row_order_in_a_stored_payload_is_rejected(tmp_path):
    """Canonical order is part of the digested evidence, not a presentation detail."""
    from bridge.engine.types import RISK_SNAPSHOT_ROW_DIGEST_MISMATCH

    rows = [{"symbol": "AAA", "size": 1.0}, {"symbol": "BBB", "size": 2.0}]
    store = _v6_store(tmp_path)
    _accept_v2(
        store,
        now=NOW,
        coverage_ms=_ms(NOW),
        risk_rows={"POSITIONS": rows},
        tamper_rows={"POSITIONS": list(reversed(rows))},
        bypass_accept_validation=True,
    )
    assert _veto(store, now=NOW) == RISK_SNAPSHOT_ROW_DIGEST_MISMATCH
    store.close()


@pytest.mark.parametrize(
    "label, rows, expected",
    [
        (
            "duplicate",
            {"POSITIONS": [{"symbol": "BTC", "size": 1.0}, {"symbol": "BTC", "size": 2.0}]},
            "RISK_SNAPSHOT_POSITION_DUPLICATE",
        ),
        ("blank-symbol", {"POSITIONS": [{"symbol": "", "size": 1.0}]},
         "RISK_SNAPSHOT_POSITION_MALFORMED"),
        ("string-size", {"POSITIONS": [{"symbol": "BTC", "size": "1.0"}]},
         "RISK_SNAPSHOT_POSITION_MALFORMED"),
        ("bool-size", {"POSITIONS": [{"symbol": "BTC", "size": True}]},
         "RISK_SNAPSHOT_POSITION_MALFORMED"),
        ("missing-size", {"POSITIONS": [{"symbol": "BTC"}]},
         "RISK_SNAPSHOT_POSITION_MALFORMED"),
        ("extra-key", {"POSITIONS": [{"symbol": "BTC", "size": 1.0, "extra": 1}]},
         "RISK_SNAPSHOT_POSITION_MALFORMED"),
        ("no-balance-row", {"BALANCES": []}, "RISK_SNAPSHOT_ACCOUNT_MALFORMED"),
        (
            "two-margin-rows",
            {
                "MARGIN": [
                    {"margin_used": 1_000.0, "available_margin": 9_000.0},
                    {"margin_used": 2_000.0, "available_margin": 8_000.0},
                ]
            },
            "RISK_SNAPSHOT_ACCOUNT_MALFORMED",
        ),
        (
            "string-money",
            {"BALANCES": [{"equity": 10_000.0, "withdrawable": "9000"}]},
            "RISK_SNAPSHOT_ACCOUNT_MALFORMED",
        ),
        (
            "negative-equity",
            {
                "BALANCES": [{"equity": -1.0, "withdrawable": 0.0}],
                "MARGIN": [{"margin_used": 0.0, "available_margin": 0.0}],
            },
            "RISK_SNAPSHOT_ACCOUNT_NEGATIVE",
        ),
        (
            "identity-broken",
            {
                "BALANCES": [{"equity": 10_000.0, "withdrawable": 9_000.0}],
                "MARGIN": [{"margin_used": 1_000.0, "available_margin": 8_000.0}],
            },
            "RISK_SNAPSHOT_ACCOUNT_INCONSISTENT",
        ),
        (
            "withdrawable-exceeds-equity",
            {
                "BALANCES": [{"equity": 1_000.0, "withdrawable": 2_000.0}],
                "MARGIN": [{"margin_used": 0.0, "available_margin": 1_000.0}],
            },
            "RISK_SNAPSHOT_ACCOUNT_INCONSISTENT",
        ),
    ],
)
def test_malformed_risk_rows_fail_closed_with_a_stable_reason(
    tmp_path, label, rows, expected
):
    store = _v6_store(tmp_path, name=f"malformed-{label}.db")
    _accept_v2(store, now=NOW, coverage_ms=_ms(NOW), risk_rows=rows)
    assert _veto(store, now=NOW) == expected
    store.close()


def test_non_finite_money_and_size_never_reach_risk(tmp_path):
    """NaN/Inf cannot survive canonical JSON, so they are refused at write time."""
    from bridge.engine.types import RISK_SNAPSHOT_NO_CHECKPOINT

    store = _v6_store(tmp_path)
    for rows in (
        {"POSITIONS": [{"symbol": "BTC", "size": float("nan")}]},
        {"BALANCES": [{"equity": float("inf"), "withdrawable": 0.0}]},
    ):
        with pytest.raises(ValueError):
            _accept_v2(store, now=NOW, coverage_ms=_ms(NOW), risk_rows=rows)
    assert store.count_accepted_reconcile_checkpoints() == 0
    assert _veto(store, now=NOW) == RISK_SNAPSHOT_NO_CHECKPOINT
    store.close()


def test_a_v2_payload_that_disagrees_with_its_components_is_never_accepted(tmp_path):
    from bridge.store.db import ReconcileConflictError

    store = _v6_store(tmp_path)
    with pytest.raises(
        ReconcileConflictError, match="RECONCILE_ACCEPT_RISK_ROWS_INVALID"
    ):
        _accept_v2(
            store,
            now=NOW,
            coverage_ms=_ms(NOW),
            risk_rows={"POSITIONS": [{"symbol": "BTC", "size": 1.0}]},
            # A payload cannot claim rows the capture did not observe.
            tamper_rows={"POSITIONS": [{"symbol": "BTC", "size": 9.0}]},
        )
    assert store.count_accepted_reconcile_checkpoints() == 0
    store.close()


def test_a_read_failure_vetoes_and_never_returns_a_partial_snapshot(tmp_path):
    import sqlite3

    from bridge.engine.types import RiskSnapshotUnavailable

    store = _v6_store(tmp_path)
    _accept_v2(store, now=NOW, coverage_ms=_ms(NOW))
    assert _load(store, now=NOW).equity == 10_000.0

    original = store._risk_component_rows_locked

    def exploding(attempt_id):
        raise sqlite3.OperationalError("component ledger unavailable")

    store._risk_component_rows_locked = exploding
    with pytest.raises(RiskSnapshotUnavailable) as excinfo:
        _load(store, now=NOW)
    assert excinfo.value.reason_code.startswith("RISK_SNAPSHOT_READ_FAILED")
    assert "OPERATIONALERROR" in excinfo.value.reason_code
    # The failed read left no open transaction behind.
    assert store.conn.in_transaction is False

    store._risk_component_rows_locked = original
    assert _load(store, now=NOW).equity == 10_000.0
    store.close()


def test_a_concurrent_capture_cannot_mix_two_epochs_into_one_snapshot(tmp_path):
    """The load pins one epoch; a capture committing mid-read is the next one."""
    path = tmp_path / "epoch.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    first = _accept_v2(
        store,
        now=NOW,
        coverage_ms=_ms(NOW),
        risk_rows={
            "POSITIONS": [{"symbol": "BTC", "size": 1.0}],
            "BALANCES": [{"equity": 1_000.0, "withdrawable": 1_000.0}],
            "MARGIN": [{"margin_used": 0.0, "available_margin": 1_000.0}],
        },
    )

    later = NOW + timedelta(seconds=30)
    competitor = Store(path)
    interleaved: list[str] = []
    original = store._risk_component_rows_locked

    def racing(attempt_id):
        # A whole second capture is accepted on another connection *between*
        # this load's pointer read and its component read.
        if not interleaved:
            interleaved.append(
                _accept_v2(
                    competitor,
                    now=later,
                    coverage_ms=_ms(later),
                    coverage_start_ms=_ms(NOW),
                    risk_rows={
                        "POSITIONS": [{"symbol": "BTC", "size": 7.0}],
                        "BALANCES": [{"equity": 9_999.0, "withdrawable": 9_999.0}],
                        "MARGIN": [{"margin_used": 0.0, "available_margin": 9_999.0}],
                    },
                )
            )
        return original(attempt_id)

    store._risk_component_rows_locked = racing
    snapshot = _load(store, now=later)
    store._risk_component_rows_locked = original

    assert interleaved, "the competing capture must really have committed"
    # One coherent epoch: never epoch A's identity with epoch B's rows.
    assert snapshot.attempt_id == first
    assert snapshot.equity == 1_000.0
    assert [(p.symbol, p.size) for p in snapshot.positions] == [("BTC", 1.0)]
    assert snapshot.canonical_hash == (
        store.get_reconcile_attempt(first)["canonical_hash"]
    )
    store.close()

    # A fresh load sees the new epoch, whole.
    reader = Store(path)
    fresh = _load(reader, now=later)
    assert fresh.attempt_id == interleaved[0]
    assert fresh.equity == 9_999.0
    assert [(p.symbol, p.size) for p in fresh.positions] == [("BTC", 7.0)]
    reader.close()
    competitor.close()


# ---------------------------------------------------------------------------
# TS-P1-007 — durable daily-risk state, exact thresholds and control latches
#
# Owner policy (TS_P1_007_GATE1_FINAL.md §11, ratified 2026-07-27):
#   D1=A whole-account authoritative equity change from the accepted checkpoint
#   D2=A UTC day; baseline = last accepted checkpoint at/before 00:00 UTC
#   D3A=2% daily loss, D3B=5% intraday drawdown, D3C=500 USDC equity floor
#   D4=A sticky latches with human-gated reset/supersession
#   D5=A opt-in additive schema v7; the default schema stays v4
#
# Every assertion below drives real persisted evidence through the production
# accept path; nothing injects a daily-risk number straight into a gate.
# ---------------------------------------------------------------------------

D3A_DAILY_LOSS_PCT = 0.02
D3B_MAX_DRAWDOWN_PCT = 0.05
D3C_EQUITY_FLOOR_USDC = 500.0

DAY = datetime(2026, 7, 26, 0, 0, tzinfo=UTC)


def _policy(**overrides):
    from bridge.engine.types import DurableRiskPolicy

    values = {
        "policy_id": "ts-p1-007-v1",
        "max_daily_loss_pct": D3A_DAILY_LOSS_PCT,
        "max_intraday_drawdown_pct": D3B_MAX_DRAWDOWN_PCT,
        "equity_floor_usdc": D3C_EQUITY_FLOOR_USDC,
    }
    values.update(overrides)
    return DurableRiskPolicy.create(**values)


def _v7_store(tmp_path, name="risk.db", *, run_id="run", mode="paper", network="testnet"):
    store = Store(tmp_path / name)
    store.initialize(target_schema_version=7)
    store.create_run(run_id, mode, network, {})
    return store


def _equity_rows(equity, *, margin_used=0.0):
    """Risk rows that satisfy the TS-P1-005 account identity for one equity."""
    equity = float(equity)
    margin_used = float(margin_used)
    return {
        "POSITIONS": [],
        "BALANCES": [{"equity": equity, "withdrawable": equity - margin_used}],
        "MARGIN": [
            {"margin_used": margin_used, "available_margin": equity - margin_used}
        ],
    }


def _accept_equity(store, *, now, equity, policy, run_id="run", **kwargs):
    """One accepted v2 checkpoint whose BALANCES row carries ``equity``."""
    return _accept_v2(
        store,
        now=now,
        coverage_ms=_ms(now),
        risk_rows=_equity_rows(equity),
        run_id=run_id,
        risk_policy=policy,
        **kwargs,
    )


def _day_rows(store):
    return store.list_risk_day_checkpoints()


def _latch_rows(store):
    return store.list_risk_control_latches()


# --- D5=A: the opt-in migration itself --------------------------------------


def test_v7_is_opt_in_and_the_default_target_still_lands_on_v4(tmp_path):
    from bridge.store.db import SCHEMA_VERSION_DURABLE_RISK, Store

    assert SCHEMA_VERSION_DURABLE_RISK == 7
    store = Store(tmp_path / "bridge.db")
    store.initialize()

    assert store.get_meta("schema_version") == "4"
    assert store.durable_risk_controls_enabled() is False
    assert store.full_reconcile_enabled() is False
    assert store.conn.execute(
        "SELECT name FROM sqlite_master WHERE name IN "
        "('risk_day_checkpoints', 'risk_control_latches')"
    ).fetchall() == []
    store.close()


def test_v4_chain_reaches_v7_and_keeps_every_predecessor_ledger(tmp_path):
    store, trade_id, _now = _v4_with_trade(tmp_path)
    orders = [dict(r) for r in store.conn.execute("SELECT * FROM orders")]
    trades = [dict(r) for r in store.conn.execute("SELECT * FROM trades")]
    store.close()

    upgraded = Store(tmp_path / "bridge.db")
    upgraded.initialize(target_schema_version=7)

    assert upgraded.get_meta("schema_version") == "7"
    objects = _existing_objects(upgraded)
    assert {"risk_day_checkpoints", "risk_control_latches"} <= objects
    assert set(_V6_OBJECTS) <= objects
    assert {"partial_fill_recoveries", "partial_fill_actions"} <= objects
    # v6 capability must survive the bump, or TS-P1-006 risk silently switches
    # off the moment TS-P1-007 is enabled.
    assert upgraded.full_reconcile_enabled() is True
    assert upgraded.partial_protection_enabled() is True
    assert upgraded.durable_risk_controls_enabled() is True
    # Strictly additive: no pre-existing evidence row is touched, no backfill.
    assert [dict(r) for r in upgraded.conn.execute("SELECT * FROM orders")] == orders
    assert [dict(r) for r in upgraded.conn.execute("SELECT * FROM trades")] == trades
    assert _day_rows(upgraded) == []
    assert _latch_rows(upgraded) == []
    assert int(trade_id) > 0
    upgraded.close()


def test_v7_migration_rolls_back_to_a_reopenable_v6_and_keeps_failure_evidence(tmp_path):
    from bridge.store.db import (
        RISK_CONTROLS_MIGRATION_FAILURE_KEY,
        MigrationError,
        Store,
    )

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    store.create_run("run", "paper", "testnet", {})
    accepted = _accept_v2(store, now=NOW, coverage_ms=_ms(NOW))
    before = {
        table: int(store.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
        for table in _V6_OBJECTS
    }
    store.close()

    class FailingStore(Store):
        def _validate_durable_risk_schema_v7(self):
            raise MigrationError("injected v7 validation failure")

    failing = FailingStore(path)
    with pytest.raises(MigrationError):
        failing.initialize(target_schema_version=7)

    assert failing.get_meta("schema_version") == "6"
    assert not (
        _existing_objects(failing) & {"risk_day_checkpoints", "risk_control_latches"}
    )
    assert {
        table: int(failing.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
        for table in _V6_OBJECTS
    } == before
    # A secret-safe failure record survives outside the rolled-back transaction.
    failure = failing.get_meta(RISK_CONTROLS_MIGRATION_FAILURE_KEY)
    assert failure is not None and "injected" not in failure
    assert failure.startswith("RISK_CONTROLS_MIGRATION_FAILED")
    failing.close()

    # The predecessor is still a valid, reopenable v6 with its checkpoint intact.
    reopened = Store(path)
    reopened.initialize(target_schema_version=6)
    assert reopened.get_meta("schema_version") == "6"
    assert reopened.latest_accepted_reconcile_checkpoint()["attempt_id"] == accepted
    assert reopened.durable_risk_controls_enabled() is False
    reopened.close()


def test_v7_migration_aborts_on_a_preexisting_object_and_rolls_back(tmp_path):
    from bridge.store.db import MigrationError, Store

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    store.conn.execute("CREATE TABLE risk_control_latches (bogus TEXT)")
    store.conn.commit()

    with pytest.raises(MigrationError):
        store._migrate_v6_to_v7()

    assert store.get_meta("schema_version") == "6"
    assert "risk_day_checkpoints" not in _existing_objects(store)
    store.close()


def test_schema_version_claiming_v7_without_v7_objects_fails_closed(tmp_path):
    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    store.conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '7')"
    )
    store.conn.commit()
    store.close()

    reopened = Store(path)
    with pytest.raises(RuntimeError, match="Unsupported schema_version"):
        reopened.initialize(target_schema_version=7)
    reopened.close()


def test_v7_reopen_rejects_a_tampered_topology(tmp_path):
    from bridge.store.db import MigrationError, Store

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=7)
    store.conn.execute("DROP TABLE risk_control_latches")
    store.conn.commit()
    store.close()

    reopened = Store(path)
    with pytest.raises(MigrationError):
        reopened.initialize(target_schema_version=7)
    reopened.close()


def test_v7_reopen_rejects_same_named_trigger_with_wrong_semantics(tmp_path):
    from bridge.store.db import MigrationError, Store

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=7)
    store.conn.execute("DROP TRIGGER risk_day_checkpoints_immutable_update")
    store.conn.execute(
        """CREATE TRIGGER risk_day_checkpoints_immutable_update
           BEFORE INSERT ON risk_day_checkpoints BEGIN SELECT 1; END"""
    )
    store.conn.commit()
    store.close()

    reopened = Store(path)
    with pytest.raises(MigrationError):
        reopened.initialize(target_schema_version=7)
    reopened.close()


def test_v7_database_reopened_with_the_default_target_is_never_downgraded(tmp_path):
    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=7)
    store.close()

    reopened = Store(path)
    reopened.initialize()
    assert reopened.get_meta("schema_version") == "7"
    assert reopened.durable_risk_controls_enabled() is True
    reopened.close()


# --- D2=A: the UTC day baseline ---------------------------------------------


def test_first_v7_day_has_no_baseline_and_risk_blocks_instead_of_inventing_one(tmp_path):
    from bridge.engine.types import RISK_DAY_BASELINE_MISSING, RiskSnapshotUnavailable

    policy = _policy()
    store = _v7_store(tmp_path)
    noon = DAY + timedelta(hours=12)
    _accept_equity(store, now=noon, equity=10_000.0, policy=policy)

    rows = _day_rows(store)
    assert len(rows) == 1
    assert rows[0]["trading_date"] == "2026-07-26"
    assert rows[0]["equity"] == 10_000.0
    assert rows[0]["baseline_source"] == "MISSING"
    assert rows[0]["baseline_equity"] is None
    assert rows[0]["daily_pnl"] is None
    assert rows[0]["mode"] == "paper" and rows[0]["network"] == "testnet"

    with pytest.raises(RiskSnapshotUnavailable) as excinfo:
        store.load_durable_risk_view(
            now=noon + timedelta(seconds=5),
            max_age_s=900.0,
            policy_version=policy.version,
        )
    assert excinfo.value.reason_code == RISK_DAY_BASELINE_MISSING
    store.close()


def test_baseline_is_the_last_accepted_checkpoint_at_or_before_utc_midnight(tmp_path):
    policy = _policy()
    store = _v7_store(tmp_path)

    # Yesterday: two observations; the later one is the day-start authority.
    _accept_equity(store, now=DAY - timedelta(hours=6), equity=9_000.0, policy=policy)
    _accept_equity(store, now=DAY - timedelta(minutes=1), equity=10_000.0, policy=policy)
    # Exactly 00:00:00Z belongs to the new day *and* is at/before midnight, so it
    # is the strongest possible baseline for it.
    midnight = _accept_equity(store, now=DAY, equity=10_500.0, policy=policy)
    noon = DAY + timedelta(hours=12)
    _accept_equity(store, now=noon, equity=10_300.0, policy=policy)

    today = [row for row in _day_rows(store) if row["trading_date"] == "2026-07-26"]
    assert len(today) == 2
    for row in today:
        assert row["baseline_source"] == "CHECKPOINT_AT_OR_BEFORE_UTC_MIDNIGHT"
        assert row["baseline_equity"] == 10_500.0
        assert row["baseline_ts"].startswith("2026-07-26T00:00:00")

    snapshot, daily = store.load_durable_risk_view(
        now=noon + timedelta(seconds=5), max_age_s=900.0, policy_version=policy.version
    )
    assert daily.baseline_equity == 10_500.0
    assert daily.equity == 10_300.0 == snapshot.equity
    # D1=A: whole-account equity change, not a local PnL ledger.
    assert daily.daily_pnl == -200.0
    assert daily.checkpoint_id == snapshot.checkpoint_id
    assert store.get_reconcile_attempt(midnight)["reason_code"] == "ACCEPTED"
    store.close()


def test_a_new_utc_day_blocks_until_a_fresh_checkpoint_establishes_it(tmp_path):
    from bridge.engine.types import RISK_DAY_DATE_MISMATCH, RiskSnapshotUnavailable

    policy = _policy()
    store = _v7_store(tmp_path)
    _accept_equity(store, now=DAY - timedelta(hours=1), equity=10_000.0, policy=policy)
    _accept_equity(
        store, now=DAY - timedelta(seconds=1), equity=10_000.0, policy=policy
    )

    # One second later it is a different UTC day and the newest durable day row
    # still describes yesterday: D2=A blocks rather than reusing it.
    with pytest.raises(RiskSnapshotUnavailable) as excinfo:
        store.load_durable_risk_view(
            now=DAY, max_age_s=900.0, policy_version=policy.version
        )
    assert excinfo.value.reason_code == RISK_DAY_DATE_MISMATCH

    _accept_equity(store, now=DAY + timedelta(minutes=1), equity=9_900.0, policy=policy)
    _snapshot, daily = store.load_durable_risk_view(
        now=DAY + timedelta(minutes=2), max_age_s=900.0, policy_version=policy.version
    )
    assert daily.trading_date == "2026-07-26"
    assert daily.baseline_equity == 10_000.0
    assert daily.daily_pnl == -100.0
    store.close()


def test_clock_rollback_between_accepted_checkpoints_fails_closed(tmp_path):
    from bridge.store.db import ReconcileConflictError

    policy = _policy()
    store = _v7_store(tmp_path)
    _accept_equity(store, now=DAY + timedelta(hours=12), equity=10_000.0, policy=policy)

    with pytest.raises(ReconcileConflictError) as excinfo:
        _accept_equity(
            store, now=DAY + timedelta(hours=11), equity=9_000.0, policy=policy
        )
    assert excinfo.value.code == "RISK_DAY_CLOCK_ROLLBACK"
    # The refused accept left one day row and no partial evidence.
    assert len(_day_rows(store)) == 1
    store.close()


# --- D3/D4: exact boundaries, exactly-once latches --------------------------


def test_daily_loss_latches_exactly_once_at_the_exact_boundary(tmp_path):
    from bridge.engine.types import RISK_CONTROL_DAILY_LOSS

    policy = _policy()
    store = _v7_store(tmp_path)
    _accept_equity(
        store, now=DAY - timedelta(minutes=1), equity=10_000.0, policy=policy
    )

    # One unit inside the boundary: -1.99% is not a breach.
    _accept_equity(store, now=DAY + timedelta(hours=1), equity=9_801.0, policy=policy)
    assert _latch_rows(store) == []

    # Exactly -2.00% of the *day-start* equity blocks.
    _accept_equity(store, now=DAY + timedelta(hours=2), equity=9_800.0, policy=policy)
    latches = _latch_rows(store)
    assert len(latches) == 1
    assert latches[0]["control"] == RISK_CONTROL_DAILY_LOSS
    assert latches[0]["record_kind"] == "LATCH"
    assert latches[0]["scope_key"] == "2026-07-26"
    assert latches[0]["observed_value"] == -200.0
    assert latches[0]["threshold_value"] == -200.0
    assert latches[0]["policy_version"] == policy.version
    assert latches[0]["equity"] == 9_800.0

    # A further loss cannot duplicate DAILY_LOSS, but an independently crossed
    # drawdown control must retain its own evidence.
    _accept_equity(store, now=DAY + timedelta(hours=3), equity=9_000.0, policy=policy)
    assert [row["control"] for row in _latch_rows(store)] == [
        "DAILY_LOSS",
        "MAX_DRAWDOWN",
    ]

    _snapshot, daily = store.load_durable_risk_view(
        now=DAY + timedelta(hours=3, seconds=5),
        max_age_s=900.0,
        policy_version=policy.version,
    )
    assert daily.latched_controls == (
        RISK_CONTROL_DAILY_LOSS,
        "MAX_DRAWDOWN",
    )
    store.close()


def test_daily_loss_denominator_is_day_start_equity_not_current_equity(tmp_path):
    """The interim gate divided by current equity; the full gate must not.

    A 199 USDC loss is inside the 2% day-start budget (200) but outside the 2%
    budget the interim gate would compute from current equity (2% of 9,801 =
    196.02), so the two rules disagree on exactly this evidence.
    """
    policy = _policy()
    store = _v7_store(tmp_path)
    _accept_equity(
        store, now=DAY - timedelta(minutes=1), equity=10_000.0, policy=policy
    )
    _accept_equity(store, now=DAY + timedelta(hours=1), equity=9_801.0, policy=policy)

    assert _latch_rows(store) == []
    _snapshot, daily = store.load_durable_risk_view(
        now=DAY + timedelta(hours=1, seconds=5),
        max_age_s=900.0,
        policy_version=policy.version,
    )
    assert daily.baseline_equity == 10_000.0
    assert daily.equity == 9_801.0
    assert daily.daily_pnl == -199.0
    assert daily.daily_loss_pct == 0.0199
    assert -daily.daily_pnl < policy.max_daily_loss_pct * daily.baseline_equity
    assert -daily.daily_pnl > policy.max_daily_loss_pct * daily.equity
    store.close()


def test_peak_equity_is_monotonic_within_the_day_and_max_drawdown_is_exact(tmp_path):
    from bridge.engine.types import RISK_CONTROL_MAX_DRAWDOWN

    policy = _policy()
    store = _v7_store(tmp_path)
    _accept_equity(
        store, now=DAY - timedelta(minutes=1), equity=10_000.0, policy=policy
    )
    _accept_equity(store, now=DAY + timedelta(hours=1), equity=12_000.0, policy=policy)
    # Peak rises, then equity falls - the peak must not follow it down.
    _accept_equity(store, now=DAY + timedelta(hours=2), equity=11_401.0, policy=policy)
    today = [row for row in _day_rows(store) if row["trading_date"] == "2026-07-26"]
    assert [row["peak_equity"] for row in today] == [12_000.0, 12_000.0]
    assert _latch_rows(store) == []

    # Exactly 5% below the peak blocks.
    _accept_equity(store, now=DAY + timedelta(hours=3), equity=11_400.0, policy=policy)
    latches = _latch_rows(store)
    assert len(latches) == 1
    assert latches[0]["control"] == RISK_CONTROL_MAX_DRAWDOWN
    assert latches[0]["observed_value"] == 600.0
    assert latches[0]["threshold_value"] == 600.0
    assert latches[0]["peak_equity"] == 12_000.0
    store.close()


def test_peak_and_latch_are_reconstructed_identically_after_reopen(tmp_path):
    policy = _policy()
    path = tmp_path / "restart.db"
    store = Store(path)
    store.initialize(target_schema_version=7)
    store.create_run("run", "paper", "testnet", {})
    _accept_equity(
        store, now=DAY - timedelta(minutes=1), equity=10_000.0, policy=policy
    )
    _accept_equity(store, now=DAY + timedelta(hours=1), equity=12_000.0, policy=policy)
    _accept_equity(store, now=DAY + timedelta(hours=2), equity=11_400.0, policy=policy)
    before_days = _day_rows(store)
    before_latches = _latch_rows(store)
    store.close()

    reopened = Store(path)
    reopened.initialize(target_schema_version=7)
    assert _day_rows(reopened) == before_days
    assert _latch_rows(reopened) == before_latches
    assert len(before_latches) == 1
    active = reopened.active_risk_control_latches(
        run_id="run", now=DAY + timedelta(hours=2, seconds=5)
    )
    assert [latch.control for latch in active] == ["MAX_DRAWDOWN"]
    reopened.close()


def test_equity_floor_latches_and_a_new_utc_day_never_clears_it(tmp_path):
    from bridge.engine.types import RISK_CONTROL_EQUITY_STOP, RISK_LATCH_ACCOUNT_SCOPE

    policy = _policy()
    store = _v7_store(tmp_path)
    _accept_equity(
        store, now=DAY - timedelta(minutes=1), equity=505.0, policy=policy
    )
    # One unit above the floor is not a breach.
    _accept_equity(store, now=DAY + timedelta(hours=1), equity=501.0, policy=policy)
    assert _latch_rows(store) == []
    # Exactly at the 500 USDC floor blocks.
    _accept_equity(store, now=DAY + timedelta(hours=2), equity=500.0, policy=policy)
    latches = _latch_rows(store)
    assert len(latches) == 1
    assert latches[0]["control"] == RISK_CONTROL_EQUITY_STOP
    assert latches[0]["scope_key"] == RISK_LATCH_ACCOUNT_SCOPE
    assert latches[0]["observed_value"] == 500.0
    assert latches[0]["threshold_value"] == 500.0

    # A whole new UTC day, and recovered equity, cannot clear an equity stop.
    next_day = DAY + timedelta(days=1, hours=2)
    _accept_equity(store, now=next_day, equity=20_000.0, policy=policy)
    active = store.active_risk_control_latches(
        run_id="run", now=next_day + timedelta(seconds=5)
    )
    assert [latch.control for latch in active] == [RISK_CONTROL_EQUITY_STOP]
    store.close()


def test_a_daily_latch_stays_active_on_a_new_day_until_human_supersession(tmp_path):
    policy = _policy()
    store = _v7_store(tmp_path)
    _accept_equity(
        store, now=DAY - timedelta(minutes=1), equity=10_000.0, policy=policy
    )
    _accept_equity(store, now=DAY + timedelta(hours=2), equity=9_800.0, policy=policy)
    assert len(_latch_rows(store)) == 1

    next_day = DAY + timedelta(days=1)
    _accept_equity(
        store, now=next_day + timedelta(hours=1), equity=9_800.0, policy=policy
    )
    # UTC rollover alone never clears durable evidence.
    assert len(_latch_rows(store)) == 1
    active = store.active_risk_control_latches(
        run_id="run", now=next_day + timedelta(hours=1, seconds=5)
    )
    assert [latch.control for latch in active] == ["DAILY_LOSS"]
    store.close()


def test_paper_and_dry_run_on_the_same_utc_date_never_collide(tmp_path):
    policy = _policy()
    store = _v7_store(tmp_path, run_id="paper-run", mode="paper", network="testnet")
    store.create_run("dry-run", "dry_run", "testnet", {})

    _accept_equity(
        store,
        now=DAY - timedelta(minutes=2),
        equity=10_000.0,
        policy=policy,
        run_id="paper-run",
    )
    _accept_equity(
        store,
        now=DAY - timedelta(minutes=1),
        equity=10_000.0,
        policy=policy,
        run_id="dry-run",
    )
    # Only the dry-run environment breaches.
    _accept_equity(
        store,
        now=DAY + timedelta(hours=1),
        equity=9_800.0,
        policy=policy,
        run_id="dry-run",
    )
    assert [row["mode"] for row in _latch_rows(store)] == ["dry_run"]
    when = DAY + timedelta(hours=1, seconds=5)
    assert store.active_risk_control_latches(run_id="paper-run", now=when) == ()
    assert len(store.active_risk_control_latches(run_id="dry-run", now=when)) == 1
    store.close()


def test_risk_day_rows_and_latches_are_append_only(tmp_path):
    policy = _policy()
    store = _v7_store(tmp_path)
    _accept_equity(
        store, now=DAY - timedelta(minutes=1), equity=10_000.0, policy=policy
    )
    _accept_equity(store, now=DAY + timedelta(hours=2), equity=9_800.0, policy=policy)
    assert len(_latch_rows(store)) == 1

    for sql in (
        "UPDATE risk_day_checkpoints SET equity = 1.0",
        "DELETE FROM risk_day_checkpoints",
        "UPDATE risk_control_latches SET observed_value = 0.0",
        "DELETE FROM risk_control_latches",
    ):
        with pytest.raises(sqlite3.IntegrityError):
            store.conn.execute(sql)
        store.conn.rollback()
    assert len(_day_rows(store)) == 2
    assert len(_latch_rows(store)) == 1
    store.close()


# --- D4=A: human-gated reset ------------------------------------------------


def test_daily_latch_reset_requires_a_human_and_a_new_utc_day_baseline(tmp_path):
    from bridge.engine.types import risk_control_reset_token
    from bridge.store.db import RiskControlConflictError

    policy = _policy()
    store = _v7_store(tmp_path)
    _accept_equity(
        store, now=DAY - timedelta(minutes=1), equity=10_000.0, policy=policy
    )
    _accept_equity(store, now=DAY + timedelta(hours=2), equity=9_800.0, policy=policy)
    latch = _latch_rows(store)[0]
    token = risk_control_reset_token("DAILY_LOSS", "2026-07-26")

    # Same day: no new baseline exists, so no human may clear it.
    with pytest.raises(RiskControlConflictError) as excinfo:
        store.record_risk_control_reset(
            latch_row_id=latch["latch_row_id"],
            actor="baris",
            acknowledgement=token,
            policy=policy,
            now=DAY + timedelta(hours=3),
            max_age_s=7200.0,
        )
    assert excinfo.value.code == "RISK_RESET_REQUIRES_NEW_DAY"

    next_day = DAY + timedelta(days=1)
    _accept_equity(
        store, now=next_day + timedelta(hours=1), equity=9_900.0, policy=policy
    )

    # A wrong or automated acknowledgement is refused.
    with pytest.raises(RiskControlConflictError) as excinfo:
        store.record_risk_control_reset(
            latch_row_id=latch["latch_row_id"],
            actor="baris",
            acknowledgement="yes",
            policy=policy,
            now=next_day + timedelta(hours=2),
            max_age_s=7200.0,
        )
    assert excinfo.value.code == "RISK_RESET_ACKNOWLEDGEMENT_INVALID"

    store.record_risk_control_reset(
        latch_row_id=latch["latch_row_id"],
        actor="baris",
        acknowledgement=token,
        policy=policy,
        now=next_day + timedelta(hours=2),
        max_age_s=7200.0,
    )
    rows = _latch_rows(store)
    assert [row["record_kind"] for row in rows] == ["LATCH", "RESET"]
    assert rows[1]["supersedes_row_id"] == latch["latch_row_id"]
    assert rows[1]["actor"] == "baris"
    # Exactly once: the same latch cannot be reset twice.
    with pytest.raises(RiskControlConflictError):
        store.record_risk_control_reset(
            latch_row_id=latch["latch_row_id"],
            actor="baris",
            acknowledgement=token,
            policy=policy,
            now=next_day + timedelta(hours=3),
            max_age_s=7200.0,
        )
    store.close()


def test_equity_stop_reset_requires_a_fresh_safe_checkpoint(tmp_path):
    from bridge.engine.types import RISK_LATCH_ACCOUNT_SCOPE, risk_control_reset_token
    from bridge.store.db import RiskControlConflictError

    policy = _policy(max_daily_loss_pct=0.9, max_intraday_drawdown_pct=0.9)
    store = _v7_store(tmp_path)
    _accept_equity(
        store, now=DAY - timedelta(minutes=1), equity=505.0, policy=policy
    )
    _accept_equity(store, now=DAY + timedelta(hours=1), equity=400.0, policy=policy)
    latch = _latch_rows(store)[0]
    token = risk_control_reset_token("EQUITY_STOP", RISK_LATCH_ACCOUNT_SCOPE)

    # Still below the floor: acknowledgement alone is not enough.
    with pytest.raises(RiskControlConflictError) as excinfo:
        store.record_risk_control_reset(
            latch_row_id=latch["latch_row_id"],
            actor="baris",
            acknowledgement=token,
            policy=policy,
            now=DAY + timedelta(hours=2),
            max_age_s=7200.0,
        )
    assert excinfo.value.code == "RISK_RESET_REQUIRES_SAFE_CHECKPOINT"

    _accept_equity(store, now=DAY + timedelta(hours=3), equity=20_000.0, policy=policy)
    store.record_risk_control_reset(
        latch_row_id=latch["latch_row_id"],
        actor="baris",
        acknowledgement=token,
        policy=policy,
        now=DAY + timedelta(hours=4),
        max_age_s=7200.0,
    )
    assert store.active_risk_control_latches(
        run_id="run", now=DAY + timedelta(hours=4)
    ) == ()

    # A later breach can latch again; the first latch row is never rewritten.
    _accept_equity(store, now=DAY + timedelta(hours=5), equity=100.0, policy=policy)
    rows = _latch_rows(store)
    assert [row["record_kind"] for row in rows] == [
        "LATCH",
        "RESET",
        "LATCH",
        "LATCH",
    ]
    assert [row["control"] for row in rows[2:]] == [
        "EQUITY_STOP",
        "MAX_DRAWDOWN",
    ]
    assert rows[0]["generation"] == 1 and rows[2]["generation"] == 2
    store.close()


def test_equity_stop_reset_rejects_substituted_policy_and_stale_evidence(tmp_path):
    from bridge.engine.types import RISK_LATCH_ACCOUNT_SCOPE, risk_control_reset_token
    from bridge.store.db import RiskControlConflictError

    policy = _policy(max_daily_loss_pct=0.9, max_intraday_drawdown_pct=0.9)
    store = _v7_store(tmp_path)
    _accept_equity(
        store, now=DAY - timedelta(minutes=1), equity=505.0, policy=policy
    )
    _accept_equity(store, now=DAY + timedelta(hours=1), equity=400.0, policy=policy)
    latch = _latch_rows(store)[0]
    token = risk_control_reset_token("EQUITY_STOP", RISK_LATCH_ACCOUNT_SCOPE)
    substituted = _policy(
        policy_id="unsafe-substitute",
        max_daily_loss_pct=0.9,
        max_intraday_drawdown_pct=0.9,
        equity_floor_usdc=0.0,
    )
    with pytest.raises(RiskControlConflictError) as excinfo:
        store.record_risk_control_reset(
            latch_row_id=latch["latch_row_id"],
            actor="baris",
            acknowledgement=token,
            policy=substituted,
            now=DAY + timedelta(hours=1, minutes=1),
            max_age_s=900.0,
        )
    assert excinfo.value.code == "RISK_RESET_POLICY_MISMATCH"

    _accept_equity(store, now=DAY + timedelta(hours=2), equity=1_000.0, policy=policy)
    with pytest.raises(RiskControlConflictError) as excinfo:
        store.record_risk_control_reset(
            latch_row_id=latch["latch_row_id"],
            actor="baris",
            acknowledgement=token,
            policy=policy,
            now=DAY + timedelta(days=1),
            max_age_s=900.0,
        )
    assert excinfo.value.code == "RISK_RESET_REQUIRES_SAFE_CHECKPOINT"
    assert [row["record_kind"] for row in _latch_rows(store)] == ["LATCH"]
    store.close()


# --- fail-closed loading ----------------------------------------------------


def test_durable_view_binds_one_checkpoint_and_refuses_a_policy_change(tmp_path):
    from bridge.engine.types import RISK_DAY_POLICY_MISMATCH, RiskSnapshotUnavailable

    policy = _policy()
    store = _v7_store(tmp_path)
    _accept_equity(
        store, now=DAY - timedelta(minutes=1), equity=10_000.0, policy=policy
    )
    _accept_equity(store, now=DAY + timedelta(hours=1), equity=9_900.0, policy=policy)
    now = DAY + timedelta(hours=1, seconds=5)

    snapshot, daily = store.load_durable_risk_view(
        now=now, max_age_s=900.0, policy_version=policy.version
    )
    assert daily.checkpoint_id == snapshot.checkpoint_id
    assert daily.attempt_id == snapshot.attempt_id
    assert daily.equity == snapshot.equity
    assert daily.policy_version == policy.version

    changed = _policy(max_intraday_drawdown_pct=0.10)
    assert changed.version != policy.version
    with pytest.raises(RiskSnapshotUnavailable) as excinfo:
        store.load_durable_risk_view(
            now=now, max_age_s=900.0, policy_version=changed.version
        )
    assert excinfo.value.reason_code == RISK_DAY_POLICY_MISMATCH
    store.close()


def test_durable_view_pins_snapshot_day_state_and_latches_to_one_read_epoch(tmp_path):
    from bridge.store.db import Store

    policy = _policy()
    reader = _v7_store(tmp_path, name="epoch.db")
    _accept_equity(
        reader, now=DAY - timedelta(minutes=1), equity=10_000.0, policy=policy
    )
    first = _accept_equity(
        reader, now=DAY + timedelta(hours=1), equity=10_000.0, policy=policy
    )
    writer = Store(tmp_path / "epoch.db")
    writer.initialize(target_schema_version=7)
    original = reader._load_risk_snapshot_locked
    second: list[str] = []

    def interleave(**kwargs):
        snapshot = original(**kwargs)
        second.append(
            _accept_equity(
                writer,
                now=DAY + timedelta(hours=2),
                equity=9_900.0,
                policy=policy,
            )
        )
        return snapshot

    reader._load_risk_snapshot_locked = interleave
    snapshot, daily = reader.load_durable_risk_view(
        now=DAY + timedelta(hours=2, seconds=5),
        max_age_s=7200.0,
        policy_version=policy.version,
    )
    reader._load_risk_snapshot_locked = original
    assert snapshot.attempt_id == first
    assert daily.checkpoint_id == snapshot.checkpoint_id
    assert daily.equity == snapshot.equity == 10_000.0
    latest = reader.load_authoritative_risk_snapshot(
        now=DAY + timedelta(hours=2, seconds=5), max_age_s=7200.0
    )
    assert latest.attempt_id == second[0]
    assert latest.equity == 9_900.0
    reader.close()
    writer.close()


def test_durable_view_is_deeply_immutable_and_has_no_writable_holder(tmp_path):
    policy = _policy()
    store = _v7_store(tmp_path)
    _accept_equity(
        store, now=DAY - timedelta(minutes=1), equity=10_000.0, policy=policy
    )
    _accept_equity(store, now=DAY + timedelta(hours=2), equity=9_800.0, policy=policy)
    _snapshot, daily = store.load_durable_risk_view(
        now=DAY + timedelta(hours=2, seconds=5),
        max_age_s=900.0,
        policy_version=policy.version,
    )
    assert not hasattr(daily, "__dict__")
    for attribute in ("baseline_equity", "peak_equity", "equity"):
        with pytest.raises((AttributeError, TypeError)):
            object.__setattr__(daily, attribute, 1.0)
    with pytest.raises((AttributeError, TypeError)):
        daily.active_latches = ()
    store.close()


def test_a_v6_store_has_no_durable_risk_state_and_says_so(tmp_path):
    from bridge.engine.types import RISK_DAY_SCHEMA_INACTIVE, RiskSnapshotUnavailable

    store = _v6_store(tmp_path)
    _accept_v2(store, now=NOW, coverage_ms=_ms(NOW))
    # TS-P1-006 behaviour is completely unchanged on v6.
    assert _load(store, now=NOW + timedelta(seconds=5)).equity == 10_000.0
    assert store.durable_risk_controls_enabled() is False
    with pytest.raises(RiskSnapshotUnavailable) as excinfo:
        store.load_durable_risk_view(
            now=NOW + timedelta(seconds=5),
            max_age_s=900.0,
            policy_version=_policy().version,
        )
    assert excinfo.value.reason_code == RISK_DAY_SCHEMA_INACTIVE
    store.close()


def _accept_v1_legacy_with_policy(store, *, now, policy):
    """A v1 metadata-only checkpoint offered to a v7 store."""
    original = Store.finalize_reconcile_attempt

    def finalize(self, **kwargs):
        kwargs.setdefault("risk_policy", policy)
        return original(self, **kwargs)

    Store.finalize_reconcile_attempt = finalize
    try:
        return _accept_v1_legacy(store, now=now, coverage_ms=_ms(now))
    finally:
        Store.finalize_reconcile_attempt = original


def test_v7_accept_requires_a_policy_and_refuses_a_legacy_payload(tmp_path):
    from bridge.store.db import ReconcileConflictError

    store = _v7_store(tmp_path)
    with pytest.raises(ReconcileConflictError) as excinfo:
        _accept_v2(store, now=NOW, coverage_ms=_ms(NOW))
    assert excinfo.value.code == "RISK_POLICY_REQUIRED"
    assert _day_rows(store) == []

    with pytest.raises(ReconcileConflictError) as excinfo:
        _accept_v1_legacy_with_policy(store, now=NOW, policy=_policy())
    assert excinfo.value.code == "RISK_DAY_REQUIRES_V2_PAYLOAD"
    assert _day_rows(store) == []
    store.close()


def _funding_row(event_id, when, amount=-25.0):
    return {
        "event_id": event_id,
        "symbol": "BTC",
        "amount_usdc": amount,
        "effective_ts_ms": _ms(when),
        "source": "HL_USER_FUNDING",
    }


def test_unattributed_funding_inside_the_day_fails_closed(tmp_path):
    from bridge.engine.types import (
        RISK_DAY_UNEXPLAINED_CASHFLOW,
        FundingAttribution,
        FundingEventRecord,
        RiskSnapshotUnavailable,
    )

    policy = _policy()
    store = _v7_store(tmp_path)
    _accept_equity(
        store, now=DAY - timedelta(minutes=1), equity=10_000.0, policy=policy
    )

    noon = DAY + timedelta(hours=12)
    effective = noon - timedelta(minutes=5)
    event = FundingEventRecord(
        event_id="0xdead",
        symbol="BTC",
        amount_usdc=-25.0,
        effective_ts=effective,
        source="HL_USER_FUNDING",
        attribution=FundingAttribution.UNATTRIBUTED,
    )
    _accept_v2(
        store,
        now=noon,
        coverage_ms=_ms(noon),
        risk_rows=_equity_rows(9_950.0),
        risk_policy=policy,
        funding_rows=[_funding_row("0xdead", effective)],
        funding_events=(event,),
    )
    with pytest.raises(RiskSnapshotUnavailable) as excinfo:
        store.load_durable_risk_view(
            now=noon + timedelta(seconds=5),
            max_age_s=900.0,
            policy_version=policy.version,
        )
    assert excinfo.value.reason_code == RISK_DAY_UNEXPLAINED_CASHFLOW
    store.close()


def test_funding_is_never_subtracted_twice_from_the_equity_change(tmp_path):
    from bridge.engine.types import FundingAttribution, FundingEventRecord

    policy = _policy()
    store = _v7_store(tmp_path)
    _accept_equity(
        store, now=DAY - timedelta(minutes=1), equity=10_000.0, policy=policy
    )

    noon = DAY + timedelta(hours=12)
    effective = noon - timedelta(minutes=5)
    event = FundingEventRecord(
        event_id="0xfeed",
        symbol="BTC",
        amount_usdc=-25.0,
        effective_ts=effective,
        source="HL_USER_FUNDING",
        attribution=FundingAttribution.ATTRIBUTED,
    )
    _accept_v2(
        store,
        now=noon,
        coverage_ms=_ms(noon),
        risk_rows=_equity_rows(9_950.0),
        risk_policy=policy,
        funding_rows=[_funding_row("0xfeed", effective)],
        funding_events=(event,),
    )
    _snapshot, daily = store.load_durable_risk_view(
        now=noon + timedelta(seconds=5), max_age_s=900.0, policy_version=policy.version
    )
    # D1=A: funding is already inside the authoritative equity move. The ledger
    # value is retained as a diagnostic column and is NOT subtracted again.
    assert daily.daily_pnl == -50.0
    assert daily.funding_attributed_usdc == -25.0
    store.close()
