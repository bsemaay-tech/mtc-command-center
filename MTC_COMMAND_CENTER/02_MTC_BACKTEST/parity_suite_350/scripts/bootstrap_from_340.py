#!/usr/bin/env python
"""
Bootstrap parity_suite_350 manifests and case JSONs from parity_suite_340.

Goals:
- start fast from prior suite
- remove disabled cases
- exclude Python-only / non-UI config keys from dedupe hash
- drop semantic duplicates using canonical_config_hash
- produce manifests and per-pack manifest files
- copy selected case JSON files into parity_suite_350/cases
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from copy import deepcopy
from pathlib import Path
from typing import Any


ALL_HEADERS = [
    "run_order",
    "pack",
    "case_id",
    "case_json",
    "tv_preset_name",
    "enabled",
    "expected_trade_behavior",
    "primary_change",
    "ui_actions",
    "depends_on",
    "parent_required",
    "canonical_config_hash",
    "semantic_fingerprint",
    "symbol",
    "timeframe",
    "start_date",
    "end_date",
    "notes",
]


DROP_NON_UI_PATHS = {
    "trade.same_bar_reentry_requires_exit",
    "trade.first_bar_requires_edge",
}


def apply_dependency_repairs(case_id: str, config: dict[str, Any]) -> dict[str, Any]:
    """
    Normalize known dependency-misaligned legacy cases from suite_340
    into behaviorally effective forms for from-scratch UI coverage.
    """
    cfg = deepcopy(config)

    # 020: keep this as pure global toggle only (no child or filter force).
    if case_id == "parity_core_020_exit_filter_block_global_on":
        cfg.setdefault("trade", {})["exit_on_filter_block"] = True

    # 021-027: child exit flags require parent ON + corresponding base filter ON.
    exit_child_map = {
        "parity_core_021_exit_filter_ma_block_on": ("use_ma_filter", "exit_on_ma_block"),
        "parity_core_022_exit_filter_ma_slope_block_on": ("use_ma_slope_filter", "exit_on_ma_slope_block"),
        "parity_core_023_exit_filter_mcginley_block_on": ("use_mcginley_filter", "exit_on_mcginley_block"),
        "parity_core_024_exit_filter_htf_block_on": ("use_htf_trend_filter", "exit_on_htf_trend_block"),
        "parity_core_025_exit_filter_volume_block_on": ("use_volume_filter", "exit_on_vol_block"),
        "parity_core_026_exit_filter_atr_vol_block_on": ("use_atr_vol_filter", "exit_on_atr_vol_block"),
        "parity_core_027_exit_filter_range_block_on": ("use_range_regime_filter", "exit_on_range_block"),
    }
    if case_id in exit_child_map:
        filter_key, child_key = exit_child_map[case_id]
        cfg.setdefault("trade", {})["exit_on_filter_block"] = True
        cfg.setdefault("filters", {})[filter_key] = True
        if filter_key == "use_range_regime_filter":
            cfg.setdefault("filters", {})["use_range_filters"] = True
        efb = cfg.setdefault("exit_filter_block", {})
        for k in (
            "exit_on_ma_block",
            "exit_on_ma_slope_block",
            "exit_on_mcginley_block",
            "exit_on_htf_trend_block",
            "exit_on_vol_block",
            "exit_on_vol_part_block",
            "exit_on_atr_vol_block",
            "exit_on_range_block",
        ):
            if k in efb:
                efb[k] = False
        efb[child_key] = True

    # 062-064: guard recovery requires at least one guard enabled.
    recovery_mode_map = {
        "parity_core_062_guard_recovery_bars": "Bars",
        "parity_core_063_guard_recovery_signals": "Signals",
        "parity_core_064_guard_recovery_virtual_trade": "Virtual Trade",
    }
    if case_id in recovery_mode_map:
        g = cfg.setdefault("guards", {})
        g["use_guard_recovery"] = True
        g["guard_recovery_mode"] = recovery_mode_map[case_id]
        g["use_consec_loss_guard"] = True
        g["consec_loss_max"] = 1

    # Range regime is effective only if range-filter hub parent is ON.
    if case_id == "parity_core_056_filter_range_regime_on":
        f = cfg.setdefault("filters", {})
        f["use_range_filters"] = True
        f["use_range_regime_filter"] = True

    return cfg


def parse_bool(raw: Any, default: bool = False) -> bool:
    if raw is None:
        return default
    text = str(raw).strip().lower()
    if text in {"1", "true", "yes", "y"}:
        return True
    if text in {"0", "false", "no", "n"}:
        return False
    return default


def parse_int(raw: Any, default: int = 0) -> int:
    try:
        return int(str(raw).strip())
    except Exception:
        return default


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, headers: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row.get(h, "") for h in headers})


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_source_case_json(workspace_root: Path, raw_case_file: str) -> Path:
    raw_case_file = (raw_case_file or "").strip()
    candidate_paths = []
    if raw_case_file:
        candidate_paths.append(workspace_root / raw_case_file)
        candidate_paths.append(workspace_root / "mtc_backtest" / raw_case_file)
    for p in candidate_paths:
        if p.exists():
            return p.resolve()
    raise FileNotFoundError(f"case json not found: {raw_case_file}")


def delete_path(obj: dict[str, Any], dotted_path: str) -> None:
    parts = dotted_path.split(".")
    node: Any = obj
    for key in parts[:-1]:
        if not isinstance(node, dict) or key not in node:
            return
        node = node[key]
    if isinstance(node, dict):
        node.pop(parts[-1], None)


def get_path(obj: dict[str, Any], dotted_path: str, default: Any = None) -> Any:
    node: Any = obj
    for key in dotted_path.split("."):
        if not isinstance(node, dict) or key not in node:
            return default
        node = node[key]
    return node


def prune_for_semantics(config: dict[str, Any]) -> dict[str, Any]:
    cfg = deepcopy(config)

    # Always drop Python-only parity internals from semantic parity hash.
    cfg.pop("parity", None)

    # Drop known non-UI fields.
    for path in DROP_NON_UI_PATHS:
        delete_path(cfg, path)

    # Parent-off pruning (conservative).
    if not parse_bool(get_path(cfg, "time_stop.enabled", False), False):
        for p in (
            "time_stop.bars",
            "time_stop.condition",
            "time_stop.exit_end_of_day",
            "time_stop.exit_end_of_week",
        ):
            delete_path(cfg, p)

    if not parse_bool(get_path(cfg, "risk.use_daily_loss_limit", False), False):
        delete_path(cfg, "risk.max_daily_loss_percent")

    if not parse_bool(get_path(cfg, "risk.use_max_trades_per_day", False), False):
        delete_path(cfg, "risk.max_trades_per_day")

    if not parse_bool(get_path(cfg, "stop_loss.use_sl", False), False):
        for p in (
            "stop_loss.mode",
            "stop_loss.atr_len",
            "stop_loss.atr_mult",
            "stop_loss.percent",
            "stop_loss.swing_basis",
            "stop_loss.swing_lookback",
            "stop_loss.swing_atr_len",
            "stop_loss.swing_atr_mult",
        ):
            delete_path(cfg, p)

    if not parse_bool(get_path(cfg, "take_profit.use_tp", False), False):
        for p in (
            "take_profit.mode",
            "take_profit.atr_len",
            "take_profit.atr_mult",
            "take_profit.percent",
            "take_profit.rr",
            "multi_tp.use_multi_tp",
            "multi_tp.tp1_rr",
            "multi_tp.tp1_pct",
            "multi_tp.tp2_rr",
            "break_even.use_break_even",
            "break_even.rr",
            "break_even.buffer_r",
            "trailing.use_trailing",
            "trailing.atr_len",
            "trailing.start_r",
            "trailing.dist_r",
        ):
            delete_path(cfg, p)
    else:
        if parse_bool(get_path(cfg, "multi_tp.use_multi_tp", False), False):
            # Multi TP ON => single TP tuning is usually inert for parity behavior.
            for p in (
                "take_profit.mode",
                "take_profit.atr_len",
                "take_profit.atr_mult",
                "take_profit.percent",
                "take_profit.rr",
            ):
                delete_path(cfg, p)

    if not parse_bool(get_path(cfg, "trade.exit_on_filter_block", False), False):
        # Keep global parent, drop child toggles when parent is OFF.
        filters = get_path(cfg, "filters", {})
        if isinstance(filters, dict):
            for key in list(filters.keys()):
                if str(key).startswith("exit_filter_"):
                    filters.pop(key, None)

    return cfg


def canonical_hash(config: dict[str, Any]) -> str:
    normalized = prune_for_semantics(config)
    raw = json.dumps(normalized, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def extract_primary_change(case_id: str) -> str:
    m = re.match(r"^parity_(?:core|bnd|pw)_\d{3}_(.+)$", case_id)
    tail = m.group(1) if m else case_id
    return tail.replace("_", " ")


def expected_trade_behavior(config: dict[str, Any], case_id: str) -> str:
    signal_mode = str(get_path(config, "signal_mode", "")).strip().lower()
    if signal_mode == "none":
        return "ZERO_TRADE_EXPECTED"
    if "signal_none" in case_id:
        return "ZERO_TRADE_EXPECTED"
    return "NORMAL"


def compose_ui_actions(case_id: str, primary_change: str) -> str:
    return f"Apply only this case change in TV UI: {primary_change}"


def make_semantic_fingerprint(pack: str, primary_change: str, hash_value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", primary_change.lower()).strip("_")
    return f"{pack}:{slug}:{hash_value[:16]}"


def bootstrap(
    workspace_root: Path,
    source_suite: Path,
    target_suite: Path,
) -> dict[str, int]:
    source_manifest = source_suite / "cases_manifest.csv"
    rows = read_csv(source_manifest)
    rows.sort(key=lambda r: parse_int(r.get("run_order", 0), 0))

    target_cases_dir = target_suite / "cases"
    target_cases_dir.mkdir(parents=True, exist_ok=True)

    kept_rows: list[dict[str, Any]] = []
    dropped_rows: list[dict[str, Any]] = []
    seen_hashes: dict[str, str] = {}

    next_run_order = 1
    for row in rows:
        case_id = (row.get("case_id") or "").strip()
        if not case_id:
            continue
        if not parse_bool(row.get("enabled", "1"), True):
            dropped_rows.append(
                {
                    "case_id": case_id,
                    "reason": "disabled_in_source_manifest",
                    "duplicate_of": "",
                }
            )
            continue

        source_case_json = resolve_source_case_json(workspace_root, row.get("case_file", ""))
        case_obj = load_json(source_case_json)
        config = case_obj.get("config", {})
        if not isinstance(config, dict):
            dropped_rows.append(
                {
                    "case_id": case_id,
                    "reason": "invalid_case_config",
                    "duplicate_of": "",
                }
            )
            continue

        repaired_config = apply_dependency_repairs(case_id, config)
        case_obj["config"] = repaired_config

        hash_value = canonical_hash(repaired_config)
        if hash_value in seen_hashes:
            dropped_rows.append(
                {
                    "case_id": case_id,
                    "reason": "duplicate_canonical_config_hash",
                    "duplicate_of": seen_hashes[hash_value],
                }
            )
            continue

        seen_hashes[hash_value] = case_id
        pack = (row.get("pack") or "").strip()
        primary = extract_primary_change(case_id)
        behavior = expected_trade_behavior(repaired_config, case_id)
        sem_fp = make_semantic_fingerprint(pack, primary, hash_value)

        # Copy source case json to target suite cases folder.
        target_case_json = target_cases_dir / f"{case_id}.json"
        target_case_json.write_text(json.dumps(case_obj, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

        suite_rel_json = f"cases/{case_id}.json"
        kept_rows.append(
            {
                "run_order": next_run_order,
                "pack": pack,
                "case_id": case_id,
                "case_json": suite_rel_json,
                "tv_preset_name": case_id,
                "enabled": 1,
                "expected_trade_behavior": behavior,
                "primary_change": primary,
                "ui_actions": compose_ui_actions(case_id, primary),
                "depends_on": "",
                "parent_required": "",
                "canonical_config_hash": hash_value,
                "semantic_fingerprint": sem_fp,
                "symbol": "",
                "timeframe": "",
                "start_date": str(case_obj.get("start_date", "")),
                "end_date": str(case_obj.get("end_date", "")),
                "notes": "bootstrapped_from_parity_suite_340",
            }
        )
        next_run_order += 1

    # Write manifests.
    all_manifest = target_suite / "manifests" / "cases_manifest_all.csv"
    write_csv(all_manifest, ALL_HEADERS, kept_rows)

    for pack in ("core", "boundary", "pairwise"):
        subset = [r for r in kept_rows if str(r.get("pack", "")).strip() == pack]
        pack_manifest = target_suite / "manifests" / f"cases_manifest_{pack}.csv"
        write_csv(pack_manifest, ALL_HEADERS, subset)

    dropped_headers = ["case_id", "reason", "duplicate_of"]
    write_csv(target_suite / "manifests" / "dedup_dropped_cases.csv", dropped_headers, dropped_rows)

    return {
        "source_rows": len(rows),
        "kept_rows": len(kept_rows),
        "dropped_rows": len(dropped_rows),
        "core_rows": sum(1 for r in kept_rows if r["pack"] == "core"),
        "boundary_rows": sum(1 for r in kept_rows if r["pack"] == "boundary"),
        "pairwise_rows": sum(1 for r in kept_rows if r["pack"] == "pairwise"),
    }


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Bootstrap parity_suite_350 manifests from parity_suite_340.")
    ap.add_argument("--workspace-root", default=".", help="Workspace root")
    ap.add_argument("--source-suite", default="mtc_backtest/parity_suite_340", help="Source suite directory")
    ap.add_argument("--target-suite", default="mtc_backtest/parity_suite_350", help="Target suite directory")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    workspace_root = Path(args.workspace_root).resolve()
    source_suite = (workspace_root / args.source_suite).resolve()
    target_suite = (workspace_root / args.target_suite).resolve()

    if not source_suite.exists():
        print(f"ERROR: source suite not found: {source_suite}")
        return 2
    target_suite.mkdir(parents=True, exist_ok=True)
    (target_suite / "manifests").mkdir(parents=True, exist_ok=True)

    stats = bootstrap(workspace_root, source_suite, target_suite)
    for k, v in stats.items():
        print(f"{k}={v}")
    print(f"all_manifest={(target_suite / 'manifests' / 'cases_manifest_all.csv').resolve()}")
    print("status=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
