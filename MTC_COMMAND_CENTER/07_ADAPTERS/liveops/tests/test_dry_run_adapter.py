from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "dry_run_adapter.py"
SPEC = importlib.util.spec_from_file_location("dry_run_adapter", MODULE_PATH)
dry_run_adapter = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(dry_run_adapter)


def _artifact() -> dict:
    return {
        "strategy_id": "QL_FAM_MOMENTUM_CONTINUATION|TRXUSDT|4h",
        "evaluation_artifact_version": "v1",
        "alert_adapter": {
            "tv_alert_json_convertible": {"status": "N_A", "value": None},
            "entry_exit_reduceonly_distinguishable": {"status": "N_A", "value": None},
            "duplicate_alert_guarded": {"status": "N_A", "value": None},
            "order_type_derivable": {"status": "N_A", "value": None},
            "partial_fill_handled": {"status": "N_A", "value": None},
            "alert_deterministic_parseable": {"status": "N_A", "value": None},
        },
        "state_sync": {
            "strategy_vs_broker_state_comparable": {"status": "N_A", "value": None},
            "flat_long_short_trackable": {"status": "N_A", "value": None},
            "resync_after_missed_alert": {"status": "N_A", "value": None},
            "multi_position_logic_explicit": {"status": "N_A", "value": None},
            "recomputable_after_restart": {"status": "N_A", "value": None},
        },
        "risk_engine_compat": {
            "works_with_mtc_default_sl_tp_trail": {"status": "N_A", "value": None},
            "reverse_reentry_cooldown_mappable": {"status": "NOT_COMPUTED", "value": None},
        },
        "monitoring": {
            "backtest_to_live_matchable": {"status": "N_A", "value": None},
        },
        "fail_safe": {
            "circuit_breaker_compatible": {"status": "N_A", "value": None},
            "max_daily_loss_compatible": {"status": "N_A", "value": None},
            "manual_override_behavior_defined": {"status": "N_A", "value": None},
            "safe_on_exchange_bot_error": {"status": "N_A", "value": None},
            "no_trade_on_unexpected_signal": {"status": "N_A", "value": None},
        },
    }


def test_success_lifecycle_is_dry_run_only() -> None:
    signal = dry_run_adapter.representative_signal(_artifact())
    evidence = dry_run_adapter.process_signal(signal)

    assert [s["state"] for s in evidence["state_transitions"]] == dry_run_adapter.LIFECYCLE_STATES
    assert evidence["final_state"] == "final_state_recorded"
    assert evidence["webhook_sent"] is False
    assert evidence["order_placed"] is False
    assert evidence["broker_client_created"] is False


def test_fail_safe_cases_skip_execution() -> None:
    signal = dry_run_adapter.representative_signal(_artifact())

    cases = [
        dry_run_adapter.process_signal("bad"),
        dry_run_adapter.process_signal({"strategy": "ONLY"}),
        dry_run_adapter.process_signal(signal | {"entry_price": 2_000_000.0}),
        dry_run_adapter.process_signal(signal, {"mode": "live", "dry_run": False, "live_trading_enabled": True}),
    ]

    assert [case["final_state"] for case in cases] == [
        "invalid_payload",
        "missing_field",
        "rejected_risk",
        "disabled_trading",
    ]
    for case in cases:
        assert case["webhook_sent"] is False
        assert case["order_placed"] is False
        assert case["broker_client_created"] is False


def test_readiness_overlay_uses_gate3_schema_names_and_keeps_live_gaps_non_ok() -> None:
    base = _artifact()
    signal = dry_run_adapter.representative_signal(base)
    evidence = dry_run_adapter.process_signal(signal)
    readiness = dry_run_adapter.overlay_readiness(base, evidence, "evidence.json")

    assert all(v["status"] == "OK" for v in readiness["alert_adapter"].values())
    assert all(v["status"] == "OK" for v in readiness["state_sync"].values())
    assert all(v["status"] == "OK" for v in readiness["fail_safe"].values())
    assert readiness["risk_engine_compat"]["works_with_mtc_default_sl_tp_trail"]["status"] != "OK"
    assert readiness["risk_engine_compat"]["reverse_reentry_cooldown_mappable"]["status"] != "OK"
    assert readiness["monitoring"]["backtest_to_live_matchable"]["status"] != "OK"


def test_cli_writes_evidence_readiness_and_safe_status() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        artifact_path = root / "artifact.json"
        out_dir = root / "out"
        status_path = root / "LIVEOPS_STATUS.json"
        artifact_path.write_text(json.dumps(_artifact()), encoding="utf-8")

        result = dry_run_adapter.main(
            ["--artifact-in", str(artifact_path), "--out-dir", str(out_dir), "--status-out", str(status_path)]
        )

        assert result == 0
        evidence_files = list(out_dir.glob("*.dry_run_evidence.json"))
        readiness_files = list(out_dir.glob("*.readiness.json"))
        assert len(evidence_files) == 1
        assert len(readiness_files) == 1

        evidence = json.loads(evidence_files[0].read_text(encoding="utf-8"))
        status = json.loads(status_path.read_text(encoding="utf-8"))
        assert evidence["final_state"] == "final_state_recorded"
        assert status["dry_run"] is True
        assert status["live_trading_enabled"] is False
        assert status["webhook_sending_enabled"] is False
        assert status["broker_integration_enabled"] is False
        assert status["events"][0]["event_type"] == "SIMULATED_SIGNAL"
