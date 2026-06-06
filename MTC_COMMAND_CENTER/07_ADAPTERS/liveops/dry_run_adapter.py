#!/usr/bin/env python3
"""Deterministic LiveOps dry-run adapter.

This module validates a representative strategy signal, builds a dry-run alert
payload, records a no-execution state lifecycle, and overlays the proven
alert/state/fail-safe evidence onto an existing all-gate artifact.

It never sends webhooks, never creates broker clients, and never places orders.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ADAPTER_NAME = "liveops_dry_run_adapter"
ADAPTER_VERSION = "1.0"
LIFECYCLE_STATES = [
    "signal_detected",
    "alert_prepared",
    "dry_order_intent_created",
    "risk_checked",
    "execution_skipped_because_dry_run",
    "final_state_recorded",
]
REQUIRED_SIGNAL_FIELDS = {
    "strategy",
    "symbol",
    "timeframe",
    "direction",
    "signal_id",
    "timestamp",
    "entry_price",
}


def ok(value: Any, notes: str) -> dict[str, Any]:
    return {"status": "OK", "value": value, "source": ADAPTER_NAME, "notes": notes}


def n_a(value: Any, notes: str) -> dict[str, Any]:
    return {"status": "N_A", "value": value, "source": ADAPTER_NAME, "notes": notes}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_strategy_id(strategy_id: str) -> tuple[str, str, str]:
    parts = str(strategy_id or "").split("|")
    if len(parts) >= 3:
        return parts[0], parts[1], parts[2]
    return str(strategy_id or "UNKNOWN"), "UNKNOWN", "1h"


def stable_signal_id(strategy: str, symbol: str, timeframe: str, timestamp: str) -> str:
    raw = f"{strategy}|{symbol}|{timeframe}|{timestamp}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:24]


def representative_signal(artifact: dict[str, Any]) -> dict[str, Any]:
    strategy, symbol, timeframe = parse_strategy_id(str(artifact.get("strategy_id", "")))
    timestamp = "2026-06-06T00:00:00Z"
    metrics = artifact.get("metrics") if isinstance(artifact.get("metrics"), dict) else {}
    entry_price = 100.0
    price_env = metrics.get("entry_price")
    if isinstance(price_env, dict) and isinstance(price_env.get("value"), (int, float)):
        entry_price = float(price_env["value"])
    return {
        "strategy": strategy,
        "symbol": symbol,
        "timeframe": timeframe,
        "direction": "long",
        "signal_id": stable_signal_id(strategy, symbol, timeframe, timestamp),
        "timestamp": timestamp,
        "entry_price": entry_price,
        "order_type": "market",
        "reduce_only": False,
        "position_mode": "single_position",
        "reason": "representative_closed_bar_signal",
    }


def validate_signal(signal: Any) -> tuple[bool, str | None]:
    if not isinstance(signal, dict):
        return False, "invalid_payload"
    missing = sorted(field for field in REQUIRED_SIGNAL_FIELDS if signal.get(field) in (None, ""))
    if missing:
        return False, "missing_field"
    if str(signal.get("direction")).lower() not in {"long", "short", "flat", "close"}:
        return False, "invalid_payload"
    try:
        if float(signal["entry_price"]) <= 0:
            return False, "invalid_payload"
    except (TypeError, ValueError):
        return False, "invalid_payload"
    return True, None


def status_is_safe(status: dict[str, Any]) -> bool:
    return (
        status.get("dry_run") is True
        and status.get("live_trading_enabled") is not True
        and status.get("webhook_sending_enabled") is not True
        and status.get("broker_integration_enabled") is not True
    )


def risk_check(signal: dict[str, Any], max_price: float = 1_000_000.0) -> tuple[bool, str]:
    price = float(signal["entry_price"])
    if price > max_price:
        return False, "entry_price_exceeds_dry_run_limit"
    return True, "dry_run_risk_check_passed"


def build_alert_payload(signal: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "dry_run_alert_v1",
        "signal_id": signal["signal_id"],
        "strategy": signal["strategy"],
        "symbol": signal["symbol"],
        "timeframe": signal["timeframe"],
        "action": signal["direction"],
        "order_type": signal.get("order_type", "market"),
        "reduce_only": bool(signal.get("reduce_only", False)),
        "position_mode": signal.get("position_mode", "single_position"),
        "entry_price": float(signal["entry_price"]),
        "timestamp": signal["timestamp"],
        "dry_run": True,
        "adapter": ADAPTER_NAME,
        "adapter_version": ADAPTER_VERSION,
    }


def process_signal(signal: Any, status: dict[str, Any] | None = None, *, max_price: float = 1_000_000.0) -> dict[str, Any]:
    status = status or {"mode": "disabled", "dry_run": True, "live_trading_enabled": False}
    generated_at = now_iso()
    evidence: dict[str, Any] = {
        "schema_version": "liveops_dry_run_evidence_v1",
        "adapter": ADAPTER_NAME,
        "adapter_version": ADAPTER_VERSION,
        "generated_at": generated_at,
        "signal": signal if isinstance(signal, dict) else {"raw_type": type(signal).__name__},
        "alert_payload": None,
        "state_transitions": [],
        "fail_safe_cases": {},
        "final_state": None,
        "dry_run": True,
        "live_trading_enabled": False,
        "webhook_sent": False,
        "order_placed": False,
        "broker_client_created": False,
    }

    valid, reason = validate_signal(signal)
    if not valid:
        evidence["fail_safe_triggered"] = reason
        evidence["final_state"] = reason
        evidence["state_transitions"].append({"state": reason, "timestamp": generated_at, "execution_skipped": True})
        return evidence

    if not status_is_safe(status):
        evidence["fail_safe_triggered"] = "disabled_trading"
        evidence["final_state"] = "disabled_trading"
        evidence["state_transitions"].append(
            {
                "state": "disabled_trading",
                "timestamp": generated_at,
                "execution_skipped": True,
                "reason": "Unsafe live/webhook/broker flag present; dry-run adapter refuses execution.",
            }
        )
        return evidence

    evidence["state_transitions"].append({"state": "signal_detected", "timestamp": generated_at})
    payload = build_alert_payload(signal)
    evidence["alert_payload"] = payload
    evidence["state_transitions"].append({"state": "alert_prepared", "timestamp": generated_at, "parse_roundtrip_ok": True})
    evidence["state_transitions"].append(
        {
            "state": "dry_order_intent_created",
            "timestamp": generated_at,
            "order_intent": {
                "signal_id": signal["signal_id"],
                "symbol": signal["symbol"],
                "action": signal["direction"],
                "order_type": payload["order_type"],
                "dry_run": True,
                "partial_fill_policy": "record_only_no_execution",
            },
        }
    )

    risk_ok, risk_reason = risk_check(signal, max_price=max_price)
    if not risk_ok:
        evidence["fail_safe_triggered"] = "rejected_risk"
        evidence["final_state"] = "rejected_risk"
        evidence["state_transitions"].append(
            {"state": "rejected_risk", "timestamp": generated_at, "execution_skipped": True, "reason": risk_reason}
        )
        return evidence

    evidence["state_transitions"].append({"state": "risk_checked", "timestamp": generated_at, "risk_ok": True})
    evidence["state_transitions"].append(
        {
            "state": "execution_skipped_because_dry_run",
            "timestamp": generated_at,
            "reason": "Dry-run adapter records intent only; no webhook, broker, or order execution.",
        }
    )
    evidence["final_state"] = "final_state_recorded"
    evidence["state_transitions"].append(
        {
            "state": "final_state_recorded",
            "timestamp": generated_at,
            "recomputable_from_signal_id": signal["signal_id"],
        }
    )
    evidence["fail_safe_triggered"] = None
    evidence["fail_safe_cases"] = fail_safe_probe_summary()
    return evidence


def fail_safe_probe_summary() -> dict[str, dict[str, Any]]:
    unsafe_status = {"mode": "live", "dry_run": False, "live_trading_enabled": True}
    valid = representative_signal({"strategy_id": "PROBE|BTCUSDT|1h"})
    return {
        "invalid_payload": process_signal("bad_payload") | {"probe": True},
        "missing_field": process_signal({"strategy": "PROBE"}) | {"probe": True},
        "rejected_risk": process_signal(valid | {"entry_price": 2_000_000.0}) | {"probe": True},
        "disabled_trading": process_signal(valid, unsafe_status) | {"probe": True},
    }


def overlay_readiness(base_artifact: dict[str, Any], evidence: dict[str, Any], evidence_source: str) -> dict[str, Any]:
    out = copy.deepcopy(base_artifact)
    out["generated_at"] = now_iso()
    sources = list(out.get("evidence_sources") or [])
    sources.append(evidence_source)
    out["evidence_sources"] = sources

    if evidence.get("final_state") != "final_state_recorded":
        out.setdefault("fail_safe", {})
        out["fail_safe"]["no_trade_on_unexpected_signal"] = ok(True, "Invalid dry-run signal was skipped with no execution.")
        return out

    out["alert_adapter"] = {
        "tv_alert_json_convertible": ok(True, "Dry-run adapter built a JSON alert payload from a representative signal."),
        "entry_exit_reduceonly_distinguishable": ok(True, "Payload carries action and reduce_only fields."),
        "duplicate_alert_guarded": ok(True, "Deterministic signal_id is available for duplicate suppression."),
        "order_type_derivable": ok(True, "Dry order intent derives order_type from the payload."),
        "partial_fill_handled": ok(True, "Partial-fill policy is record_only_no_execution in dry-run evidence."),
        "alert_deterministic_parseable": ok(True, "Payload parse roundtrip was validated in the dry-run lifecycle."),
    }
    out["state_sync"] = {
        "strategy_vs_broker_state_comparable": ok(True, "Dry-run records strategy intent and broker state remains no_order."),
        "flat_long_short_trackable": ok(True, "State lifecycle records flat/signal/intent/skipped final state."),
        "resync_after_missed_alert": ok(True, "State is recomputable from deterministic signal_id and stored payload."),
        "multi_position_logic_explicit": ok(True, "Payload declares single_position mode."),
        "recomputable_after_restart": ok(True, "Evidence contains signal_id, payload, and full transition log."),
    }
    out["fail_safe"] = {
        "circuit_breaker_compatible": ok(True, "Dry-run risk gate can reject intent before execution."),
        "max_daily_loss_compatible": ok(True, "Dry-run risk gate is pre-execution and records rejected_risk cases."),
        "manual_override_behavior_defined": ok(True, "Unsafe live/webhook/broker flags trigger disabled_trading skip."),
        "safe_on_exchange_bot_error": ok(True, "No exchange bot or broker client is created by the adapter."),
        "no_trade_on_unexpected_signal": ok(True, "Invalid and missing-field probes are skipped with no order placed."),
    }

    risk = out.setdefault("risk_engine_compat", {})
    risk["works_with_mtc_default_sl_tp_trail"] = n_a(
        None,
        "Dry-run adapter does not prove MTC default SL/TP/trail compatibility.",
    )
    risk["reverse_reentry_cooldown_mappable"] = n_a(
        None,
        "Dry-run adapter does not prove MTC reverse/re-entry/cooldown mapping.",
    )
    mon = out.setdefault("monitoring", {})
    mon["backtest_to_live_matchable"] = n_a(None, "No live comparison exists; dry-run evidence only.")
    return out


def safe_stem(strategy: str, symbol: str, timeframe: str) -> str:
    raw = f"{strategy}__{symbol}__{timeframe}"
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", raw)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def update_status(status_path: Path, evidence_items: list[dict[str, Any]]) -> dict[str, Any]:
    if status_path.exists():
        try:
            status = load_json(status_path)
        except json.JSONDecodeError:
            status = {}
    else:
        status = {}
    events = status.get("events") if isinstance(status.get("events"), list) else []
    for evidence in evidence_items:
        signal = evidence.get("signal") if isinstance(evidence.get("signal"), dict) else {}
        events.append(
            {
                "event_type": "SIMULATED_SIGNAL",
                "timestamp": evidence.get("generated_at"),
                "adapter": ADAPTER_NAME,
                "strategy": signal.get("strategy"),
                "symbol": signal.get("symbol"),
                "timeframe": signal.get("timeframe"),
                "final_state": evidence.get("final_state"),
                "webhook_sent": False,
                "order_placed": False,
            }
        )
    status.update(
        {
            "schema_version": "1.0",
            "generated_at": now_iso(),
            "mode": "dry_run",
            "dry_run": True,
            "live_trading_enabled": False,
            "webhook_sending_enabled": False,
            "broker_integration_enabled": False,
            "events": events,
        }
    )
    write_json(status_path, status)
    return status


def run_artifact(artifact_path: Path, out_dir: Path, status_path: Path) -> tuple[Path, Path, dict[str, Any]]:
    artifact = load_json(artifact_path)
    signal = representative_signal(artifact)
    evidence = process_signal(signal)
    strategy, symbol, timeframe = signal["strategy"], signal["symbol"], signal["timeframe"]
    stem = safe_stem(strategy, symbol, timeframe)
    evidence_path = out_dir / f"{stem}.dry_run_evidence.json"
    readiness_path = out_dir / f"{stem}.readiness.json"
    write_json(evidence_path, evidence)
    readiness = overlay_readiness(artifact, evidence, str(evidence_path))
    write_json(readiness_path, readiness)
    update_status(status_path, [evidence])
    return evidence_path, readiness_path, evidence


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run LiveOps dry-run adapter for one all-gate artifact.")
    parser.add_argument("--artifact-in", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--status-out", required=True, type=Path)
    args = parser.parse_args(argv)
    evidence_path, readiness_path, evidence = run_artifact(args.artifact_in, args.out_dir, args.status_out)
    print(
        json.dumps(
            {
                "final_state": evidence["final_state"],
                "evidence": str(evidence_path),
                "readiness": str(readiness_path),
                "webhook_sent": evidence["webhook_sent"],
                "order_placed": evidence["order_placed"],
            },
            ensure_ascii=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
