"""Trades-driven STG002 replay emitter.

ENTRY rows use ``entry_time - 1h`` as a nominal signal-bar reconstruction, not
guaranteed to be an existing bar in the source series.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .constants import (
    BANNER,
    CANDIDATE_ID,
    ENGINE_STRATEGY_ID,
    EXCHANGE,
    QTY_MODEL,
    REPO_ROOT,
    RISK_REF,
    SCHEMA_ID,
    STRATEGY_VERSION,
    SYMBOL,
    SYSTEM_TEST_ROOT,
    TIMEFRAME,
)
from .contracts import canonicalize_timestamp, redact_sensitive_fields, sign_payload
from .local_receiver import LocalReceiver, ReceiverState
from .reconciler import reconcile_ledgers, write_reconciliation_report


def _parse_utc(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    elif text.endswith("+0000"):
        text = text[:-5] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).replace(microsecond=0)


def _iso_z(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def _base_payload(action: str, timestamp_utc: str, bar_time_utc: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA_ID,
        "strategy_id": CANDIDATE_ID,
        "strategy_version": STRATEGY_VERSION,
        "candidate_id": CANDIDATE_ID,
        "engine_strategy_id": ENGINE_STRATEGY_ID,
        "environment": "paper",
        "symbol": SYMBOL,
        "exchange": EXCHANGE,
        "timeframe": TIMEFRAME,
        "timestamp_utc": canonicalize_timestamp(timestamp_utc),
        "bar_time_utc": canonicalize_timestamp(bar_time_utc),
        "side": "LONG",
        "action": action,
        "qty_model": QTY_MODEL,
        "risk_ref": RISK_REF,
    }


def build_expected_payloads_from_trades(
    trades_csv_path: str | Path,
    *,
    auth_token: str,
) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    with Path(trades_csv_path).open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader):
            entry_time = _parse_utc(row["entry_time"])
            exit_time = _parse_utc(row["exit_time"])
            signal_bar = entry_time - timedelta(hours=1)

            entry_payload = _base_payload("ENTRY", _iso_z(entry_time), _iso_z(signal_bar))
            entry_payload.update(
                {
                    "current_position_intent": "FLAT_TO_LONG",
                    "entry_price": float(row["entry"]),
                    "stop_loss": float(row["stop"]),
                    "take_profit": None,
                    "source_trade_index": index,
                }
            )
            payloads.append(sign_payload(entry_payload, auth_token=auth_token))

            exit_payload = _base_payload("EXIT", _iso_z(exit_time), _iso_z(exit_time))
            exit_payload.update(
                {
                    "current_position_intent": "LONG_TO_FLAT",
                    "stop_loss": None,
                    "take_profit": None,
                    "exit_price": float(row["exit"]),
                    "exit_reason": row.get("reason") or None,
                    "source_trade_index": index,
                }
            )
            payloads.append(sign_payload(exit_payload, auth_token=auth_token))
    return payloads


def build_emitter_manifest(
    payload_count: int,
    *,
    trades_csv_path: str | Path,
    signals_csv_path: str | Path | None,
) -> dict[str, Any]:
    return {
        "banner": BANNER,
        "benchmark_role": "SYSTEM_TEST_ONLY",
        "candidate_id": CANDIDATE_ID,
        "engine_strategy_id": ENGINE_STRATEGY_ID,
        "symbol": SYMBOL,
        "timeframe": TIMEFRAME,
        "promotable": False,
        "strategy_approval_status": "NOT_APPROVED",
        "robustness_note": "Current library-wide robust result is robust_final = 0.",
        "expected_payload_count": payload_count,
        "expected_source": "trades.csv",
        "trades_csv_path": str(trades_csv_path),
        "signals_csv_path": str(signals_csv_path) if signals_csv_path else None,
    }


def write_replay_artifacts(
    *,
    trades_csv_path: str | Path,
    signals_csv_path: str | Path | None,
    output_dir: str | Path,
    auth_token: str,
) -> list[dict[str, Any]]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    payloads = build_expected_payloads_from_trades(
        trades_csv_path,
        auth_token=auth_token,
    )

    expected_path = output / "expected_signals.jsonl"
    with expected_path.open("w", encoding="utf-8", newline="\n") as handle:
        for payload in payloads:
            redacted = redact_sensitive_fields(payload)
            handle.write(json.dumps(redacted, sort_keys=True, separators=(",", ":")) + "\n")

    manifest = build_emitter_manifest(
        len(payloads),
        trades_csv_path=trades_csv_path,
        signals_csv_path=signals_csv_path,
    )
    (output / "emitter_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payloads


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def run_local_replay(
    *,
    trades_csv_path: str | Path,
    signals_csv_path: str | Path | None,
    output_dir: str | Path,
    auth_token: str,
) -> dict[str, Any]:
    """Run the local fake-money replay pipeline into an explicit output dir.

    This function is importable test plumbing only. It starts no server, uses no
    network, and never talks to a broker, exchange, TradingView, or WunderTrading.
    """
    output = Path(output_dir)
    resolved_output = output.resolve()
    resolved_repo = REPO_ROOT.resolve()
    resolved_system_test = SYSTEM_TEST_ROOT.resolve()
    if resolved_output.is_relative_to(resolved_repo) and not resolved_output.is_relative_to(
        resolved_system_test
    ):
        raise ValueError(
            "run_local_replay output_dir must be outside the repo or under "
            f"{resolved_system_test}"
        )

    payloads = write_replay_artifacts(
        trades_csv_path=trades_csv_path,
        signals_csv_path=signals_csv_path,
        output_dir=output,
        auth_token=auth_token,
    )

    receiver = LocalReceiver(ReceiverState(expected_auth_token=auth_token))
    for payload in payloads:
        receiver.process(payload)

    _write_jsonl(output / "received_signals.jsonl", receiver.state.received_rows)
    _write_jsonl(output / "simulated_fills.jsonl", receiver.state.fills)

    summary = reconcile_ledgers(
        expected_signals=payloads,
        received_rows=receiver.state.received_rows,
        fills=receiver.state.fills,
    )
    write_reconciliation_report(output, summary)
    return summary
