from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import canonicalize, default_mcc_root, load_path_config, resolve_configured_path


def build_liveops_status(mcc_root: str | Path | None = None) -> dict[str, Any]:
    root = canonicalize(mcc_root or default_mcc_root())
    status = _read_status_file(root / "03_STATUS" / "LIVEOPS_STATUS.json")
    path_config = load_path_config(root)
    mtc_v2_root = resolve_configured_path(path_config.config, "mtc_v2_root")
    paper_plans = _paper_trade_plans(mtc_v2_root) if mtc_v2_root and mtc_v2_root.exists() else []
    safety_gates = _safety_gates(status)

    return {
        "schema_version": "1.0",
        "generated_at": _latest_timestamp(status, paper_plans),
        "source": str(root / "03_STATUS" / "LIVEOPS_STATUS.json"),
        "mode": status.get("mode", "disabled"),
        "dry_run": status.get("dry_run") is True,
        "live_trading_enabled": status.get("live_trading_enabled") is True,
        "summary": _summary(status, paper_plans, safety_gates),
        "safety_gates": safety_gates,
        "paper_trade_plans": paper_plans,
        "events": _events(status),
    }


def _read_status_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "schema_version": "1.0",
            "generated_at": None,
            "mode": "missing_status_file",
            "dry_run": True,
            "live_trading_enabled": False,
            "events": [],
        }
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "schema_version": "1.0",
            "generated_at": None,
            "mode": "invalid_status_file",
            "dry_run": True,
            "live_trading_enabled": False,
            "events": [],
            "error": str(exc),
        }
    return raw if isinstance(raw, dict) else {}


def _paper_trade_plans(mtc_v2_root: Path) -> list[dict[str, Any]]:
    promoted_root = mtc_v2_root / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY"
    if not promoted_root.exists():
        return []

    plans = []
    for path in sorted(promoted_root.glob("*/FORWARD_PAPER_TRADE_PLAN.md")):
        stat = path.stat()
        plans.append(
            {
                "candidate_id": path.parent.name,
                "status": "PAPER_PLAN_ONLY",
                "live_orders_enabled": False,
                "webhook_enabled": False,
                "title": _markdown_title(path),
                "source_path": str(path),
                "relative_path": _relative_to_mtc(path, mtc_v2_root),
                "updated_at": _timestamp(stat.st_mtime),
            }
        )
    return plans


def _safety_gates(status: dict[str, Any]) -> dict[str, bool]:
    live_trading_enabled = status.get("live_trading_enabled") is True
    webhook_sending_enabled = status.get("webhook_sending_enabled") is True or status.get("webhook_enabled") is True
    broker_integration_enabled = status.get("broker_integration_enabled") is True or status.get("broker_enabled") is True
    events = _events(status)
    dry_run = status.get("dry_run") is True
    mode = str(status.get("mode", "disabled")).lower()
    return {
        "dry_run_enabled": dry_run,
        "live_trading_disabled": not live_trading_enabled,
        "webhook_sending_disabled": not webhook_sending_enabled and _webhook_send_count(events) == 0,
        "broker_integration_disabled": not broker_integration_enabled and _live_order_count(events) == 0,
        "mode_is_safe": mode in {"disabled", "dry_run", "sandbox", "missing_status_file", "invalid_status_file"},
    }


def _summary(status: dict[str, Any], paper_plans: list[dict[str, Any]], safety_gates: dict[str, bool]) -> dict[str, Any]:
    events = _events(status)
    return {
        "mode": status.get("mode", "disabled"),
        "dry_run": status.get("dry_run") is True,
        "live_trading_enabled": status.get("live_trading_enabled") is True,
        "event_count": len(events),
        "paper_trade_plan_count": len(paper_plans),
        "simulated_signal_count": sum(1 for event in events if event.get("event_type") == "SIMULATED_SIGNAL"),
        "live_order_count": _live_order_count(events),
        "webhook_send_count": _webhook_send_count(events),
        "all_safety_gates_ok": all(safety_gates.values()),
    }


def _events(status: dict[str, Any]) -> list[dict[str, Any]]:
    raw_events = status.get("events")
    if not isinstance(raw_events, list):
        return []
    return [event for event in raw_events if isinstance(event, dict)]


def _live_order_count(events: list[dict[str, Any]]) -> int:
    live_order_types = {"LIVE_ORDER", "LIVE_ORDER_SENT", "ORDER_SENT"}
    return sum(1 for event in events if str(event.get("event_type", "")).upper() in live_order_types)


def _webhook_send_count(events: list[dict[str, Any]]) -> int:
    webhook_types = {"WEBHOOK_SEND", "WEBHOOK_SENT"}
    return sum(1 for event in events if str(event.get("event_type", "")).upper() in webhook_types)


def _markdown_title(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip() or path.stem
            if stripped:
                return stripped[:120]
    except Exception:
        pass
    return path.stem


def _latest_timestamp(status: dict[str, Any], paper_plans: list[dict[str, Any]]) -> str | None:
    timestamps = [str(status.get("generated_at"))] if status.get("generated_at") else []
    timestamps.extend(plan.get("updated_at") for plan in paper_plans if plan.get("updated_at"))
    return max(timestamps) if timestamps else None


def _relative_to_mtc(path: Path, mtc_v2_root: Path) -> str:
    try:
        return str(path.relative_to(mtc_v2_root))
    except ValueError:
        return str(path)


def _timestamp(epoch_seconds: float) -> str:
    return datetime.fromtimestamp(epoch_seconds, timezone.utc).isoformat()
