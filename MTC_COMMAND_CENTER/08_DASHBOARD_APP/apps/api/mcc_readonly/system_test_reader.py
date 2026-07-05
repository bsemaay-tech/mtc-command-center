from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import canonicalize, default_mcc_root, default_quantlens_root

# The literal firewall contract stamped into every system-test artifact. The page
# renders this verbatim so fake-money plumbing can never be mistaken for paper /
# testnet / live trading.
FIREWALL_BANNER = "SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY"

# Vertical-slice gate ladder is a fixed reference model (no live writer). V1.1 is
# CLOSED; the outward legs are deliberately un-opened and each is Barış-gated.
GATE_LADDER = [
    {"leg": "V1.1", "label": "Local core slice (emitter/receiver/reconciler)", "state": "CLOSED"},
    {"leg": "V2", "label": "TradingView alerts", "state": "NOT_OPENED"},
    {"leg": "V3", "label": "WunderTrading demo", "state": "NOT_OPENED"},
    {"leg": "V4", "label": "Exchange testnet", "state": "NOT_OPENED"},
    {"leg": "V5", "label": "Day-30 review", "state": "DUE_2026-08-01"},
]

NEXT_APPROVED_ACTION = (
    "Slice V1.1 CLOSED — clean pause point. Legs V2-V4 are gated and deliberately not opened "
    "(no robust strategy justifies them; robust_final=0 library-wide). Gate V5 day-30 review "
    "due 2026-08-01. No server, broker, exchange, testnet, TradingView, or paper path without "
    "separate explicit Barış approval."
)


def build_system_test_status(mcc_root: str | Path | None = None) -> dict[str, Any]:
    """Read-only view of fake-money / systems-plumbing benchmark replay runs.

    Scans ``03_QUANTLENS/system_test/<run>/`` (git-ignored runtime output). Displays
    reconciliation plumbing evidence only — never P&L, never a trading action. Honest
    empty state when no run exists; never fabricates counts or status.
    """
    root = canonicalize(mcc_root or default_mcc_root())
    quantlens_root = default_quantlens_root(root)
    system_test_root = quantlens_root / "system_test"

    runs: list[dict[str, Any]] = []
    if system_test_root.exists():
        for run_dir in sorted(
            (p for p in system_test_root.iterdir() if p.is_dir()),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        ):
            runs.append(_read_run(run_dir, root))

    return {
        "schema_version": "1.0",
        "mode": "read_only",
        "firewall_banner": FIREWALL_BANNER,
        "generated_at": _latest_timestamp(runs),
        "source": str(system_test_root),
        "gate_ladder": GATE_LADDER,
        "next_approved_action": NEXT_APPROVED_ACTION,
        "summary": _summary(runs),
        "runs": runs,
    }


def _read_run(run_dir: Path, root: Path) -> dict[str, Any]:
    manifest = _read_json(run_dir / "emitter_manifest.json")
    recon = _read_json(run_dir / "reconciliation_summary.json")

    run: dict[str, Any] = {
        "run_id": run_dir.name,
        "relative_path": _relative_to_root(run_dir, root),
        "updated_at": _timestamp(run_dir.stat().st_mtime),
        "firewall_banner": FIREWALL_BANNER,
        "benchmark": _benchmark(manifest),
        "reconciliation": _reconciliation(recon),
        "promotion_blockers": _promotion_blockers(manifest),
        "artifacts": _artifacts(run_dir, root),
        "report_path": _rel_if_exists(run_dir / "reconciliation_report.md", root),
        "status": _run_status(manifest, recon),
    }
    return run


def _benchmark(manifest: dict[str, Any] | None) -> dict[str, Any]:
    if not manifest:
        return {"available": False}
    return {
        "available": True,
        "candidate_id": manifest.get("candidate_id"),
        "engine_strategy_id": manifest.get("engine_strategy_id"),
        "symbol": manifest.get("symbol"),
        "timeframe": manifest.get("timeframe"),
        "benchmark_role": manifest.get("benchmark_role"),
        "strategy_approval_status": manifest.get("strategy_approval_status"),
        "promotable": manifest.get("promotable") is True,
        "expected_payload_count": manifest.get("expected_payload_count"),
    }


def _reconciliation(recon: dict[str, Any] | None) -> dict[str, Any]:
    if not recon:
        return {"available": False}
    filled = _as_int(recon.get("filled_count"))
    round_trips = filled // 2 if filled is not None else None
    return {
        "available": True,
        "status": recon.get("status"),
        "expected_count": _as_int(recon.get("expected_count")),
        "received_count": _as_int(recon.get("received_count")),
        "filled_count": filled,
        "rejected_count": _as_int(recon.get("rejected_count")),
        "duplicates_dropped": _as_int(recon.get("duplicates_dropped")),
        "unexplained_count": _as_int(recon.get("unexplained_count")),
        "round_trips_approx": round_trips,
        "expected_not_received": _as_list(recon.get("expected_not_received")),
        "received_not_expected": _as_list(recon.get("received_not_expected")),
        "received_not_filled": _as_list(recon.get("received_not_filled")),
    }


def _promotion_blockers(manifest: dict[str, Any] | None) -> dict[str, Any]:
    manifest = manifest or {}
    return {
        "promotable": manifest.get("promotable") is True,
        "strategy_approval_status": manifest.get("strategy_approval_status"),
        "benchmark_role": manifest.get("benchmark_role"),
        "robustness_note": manifest.get("robustness_note"),
    }


def _run_status(manifest: dict[str, Any] | None, recon: dict[str, Any] | None) -> str:
    if recon is None:
        return "INCOMPLETE" if manifest is not None else "INVALID"
    unexplained = _as_int(recon.get("unexplained_count")) or 0
    diff_lists = (
        _as_list(recon.get("expected_not_received"))
        + _as_list(recon.get("received_not_expected"))
        + _as_list(recon.get("received_not_filled"))
    )
    if unexplained == 0 and not diff_lists and str(recon.get("status", "")).upper() == "OK":
        return "OK"
    return "MISMATCH"


def _artifacts(run_dir: Path, root: Path) -> list[dict[str, Any]]:
    items = []
    for path in sorted(run_dir.iterdir()):
        if not path.is_file():
            continue
        try:
            size = path.stat().st_size
        except OSError:
            size = None
        items.append(
            {
                "name": path.name,
                "size_bytes": size,
                "relative_path": _relative_to_root(path, root),
            }
        )
    return items


def _summary(runs: list[dict[str, Any]]) -> dict[str, Any]:
    ok_runs = sum(1 for run in runs if run.get("status") == "OK")
    return {
        "run_count": len(runs),
        "ok_runs": ok_runs,
        "mismatch_runs": sum(1 for run in runs if run.get("status") == "MISMATCH"),
        "latest_run_id": runs[0]["run_id"] if runs else None,
        "all_reconciled_clean": bool(runs) and ok_runs == len(runs),
        "any_promotable": any(
            (run.get("benchmark") or {}).get("promotable") for run in runs
        ),
    }


# ---- helpers ----

def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return raw if isinstance(raw, dict) else None


def _as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return None


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path)


def _rel_if_exists(path: Path, root: Path) -> str | None:
    return _relative_to_root(path, root) if path.exists() else None


def _latest_timestamp(runs: list[dict[str, Any]]) -> str | None:
    timestamps = [run.get("updated_at") for run in runs if run.get("updated_at")]
    return max(timestamps) if timestamps else None


def _timestamp(epoch_seconds: float) -> str:
    return datetime.fromtimestamp(epoch_seconds, timezone.utc).isoformat()
