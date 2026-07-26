from __future__ import annotations

from datetime import UTC, datetime

from bridge.store.db import Store


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
