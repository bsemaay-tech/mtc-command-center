#!/usr/bin/env python
"""
Optimize case set for from-scratch UI coverage.

Input:
- manifests/cases_manifest_all.csv
- case json files in cases/

Output:
- rewritten manifests (all/core/boundary/pairwise) with optimized subset
- manifests/ui_coverage_tokens.csv
- manifests/final_case_set_freeze.json

Method:
1) Build active diffs vs baseline for each case.
2) Build coverage tokens (path/value for categorical fields, path-change for numeric fields).
3) Greedy set cover + redundant-case pruning.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
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


EXCLUDED_PATH_PREFIXES = ("parity.",)
EXCLUDED_EXACT_PATHS = {
    "trade.same_bar_reentry_requires_exit",
    "trade.first_bar_requires_edge",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_int(raw: Any, default: int = 0) -> int:
    try:
        return int(str(raw).strip())
    except Exception:
        return default


def as_bool(raw: Any, default: bool = False) -> bool:
    if raw is None:
        return default
    text = str(raw).strip().lower()
    if text in {"1", "true", "yes", "y"}:
        return True
    if text in {"0", "false", "no", "n"}:
        return False
    return default


def load_csv(path: Path) -> list[dict[str, str]]:
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


def get_path(cfg: dict[str, Any], path: str, default: Any = None) -> Any:
    node: Any = cfg
    for key in path.split("."):
        if not isinstance(node, dict) or key not in node:
            return default
        node = node[key]
    return node


def flatten_leaves(obj: Any, prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            out.update(flatten_leaves(v, p))
        return out
    if isinstance(obj, list):
        out[prefix] = list(obj)
        return out
    out[prefix] = obj
    return out


def normalize_value(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return f"{v:.10g}"
    if v is None:
        return "null"
    return str(v)


def guard_any_enabled(cfg: dict[str, Any]) -> bool:
    keys = [
        "guards.use_dd_guard",
        "guards.use_consec_loss_guard",
        "guards.use_cooldown_guard",
        "guards.use_eq_curve_guard",
        "guards.use_mae_guard",
    ]
    return any(as_bool(get_path(cfg, k, False), False) for k in keys)


def is_path_active(cfg: dict[str, Any], path: str) -> bool:
    if path in EXCLUDED_EXACT_PATHS:
        return False
    if any(path.startswith(prefix) for prefix in EXCLUDED_PATH_PREFIXES):
        return False

    if path == "trade.exit_on_filter_block":
        # Parent is behaviorally meaningful only when at least one selected per-filter
        # exit path is active (Pine uses child toggles, not global fallback).
        if not as_bool(get_path(cfg, "trade.exit_on_filter_block", False), False):
            return True  # OFF value can still be compared as a baseline-side token.
        effective_exit_paths = [
            (
                as_bool(get_path(cfg, "exit_filter_block.exit_on_ma_block", False), False)
                and as_bool(get_path(cfg, "filters.use_ma_filter", False), False)
            ),
            (
                as_bool(get_path(cfg, "exit_filter_block.exit_on_ma_slope_block", False), False)
                and as_bool(get_path(cfg, "filters.use_ma_slope_filter", False), False)
            ),
            (
                as_bool(get_path(cfg, "exit_filter_block.exit_on_mcginley_block", False), False)
                and as_bool(get_path(cfg, "filters.use_mcginley_filter", False), False)
            ),
            (
                as_bool(get_path(cfg, "exit_filter_block.exit_on_htf_trend_block", False), False)
                and as_bool(get_path(cfg, "filters.use_htf_trend_filter", False), False)
            ),
            (
                (
                    as_bool(get_path(cfg, "exit_filter_block.exit_on_vol_block", False), False)
                    or as_bool(get_path(cfg, "exit_filter_block.exit_on_vol_part_block", False), False)
                )
                and as_bool(get_path(cfg, "filters.use_volume_filter", False), False)
            ),
            (
                as_bool(get_path(cfg, "exit_filter_block.exit_on_atr_vol_block", False), False)
                and as_bool(get_path(cfg, "filters.use_atr_vol_filter", False), False)
            ),
            (
                as_bool(get_path(cfg, "exit_filter_block.exit_on_range_block", False), False)
                and
                as_bool(get_path(cfg, "filters.use_range_filters", False), False)
                and as_bool(get_path(cfg, "filters.use_range_regime_filter", False), False)
            ),
        ]
        if not any(effective_exit_paths):
            return False

    signal_mode = str(get_path(cfg, "signal_mode", "")).strip().lower()
    if path.startswith("supertrend.") and signal_mode != "supertrend":
        return False
    if path.startswith("range_filter.") and "range" not in signal_mode:
        return False

    if path == "filters.use_range_regime_filter":
        if not as_bool(get_path(cfg, "filters.use_range_filters", False), False):
            return False
    if path.startswith("filters.range_regime_"):
        if not as_bool(get_path(cfg, "filters.use_range_filters", False), False):
            return False
        if not as_bool(get_path(cfg, "filters.use_range_regime_filter", False), False):
            return False

    if path.startswith("time_stop.") and path != "time_stop.enabled":
        if not as_bool(get_path(cfg, "time_stop.enabled", False), False):
            return False

    if path == "risk.max_daily_loss_percent":
        if not as_bool(get_path(cfg, "risk.use_daily_loss_limit", False), False):
            return False
    if path == "risk.max_trades_per_day":
        if not as_bool(get_path(cfg, "risk.use_max_trades_per_day", False), False):
            return False

    if path.startswith("stop_loss.") and path != "stop_loss.use_sl":
        if not as_bool(get_path(cfg, "stop_loss.use_sl", False), False):
            return False

    if path.startswith("take_profit.") and path != "take_profit.use_tp":
        if not as_bool(get_path(cfg, "take_profit.use_tp", False), False):
            return False

    if path.startswith("multi_tp.") and path != "multi_tp.use_multi_tp":
        if not as_bool(get_path(cfg, "take_profit.use_tp", False), False):
            return False
        if not as_bool(get_path(cfg, "multi_tp.use_multi_tp", False), False):
            return False

    if path.startswith("break_even.") and path != "break_even.use_break_even":
        if not as_bool(get_path(cfg, "break_even.use_break_even", False), False):
            return False

    if path.startswith("trailing.") and path != "trailing.use_trailing":
        if not as_bool(get_path(cfg, "trailing.use_trailing", False), False):
            return False

    # If multi TP on, single TP settings are behaviorally overridden.
    if path in {
        "take_profit.mode",
        "take_profit.atr_len",
        "take_profit.atr_mult",
        "take_profit.percent",
        "take_profit.rr",
    }:
        if as_bool(get_path(cfg, "take_profit.use_tp", False), False) and as_bool(
            get_path(cfg, "multi_tp.use_multi_tp", False), False
        ):
            return False

    if path.startswith("exit_filter_block."):
        if not as_bool(get_path(cfg, "trade.exit_on_filter_block", False), False):
            return False
        exit_dep = {
            "exit_filter_block.exit_on_ma_block": "filters.use_ma_filter",
            "exit_filter_block.exit_on_ma_slope_block": "filters.use_ma_slope_filter",
            "exit_filter_block.exit_on_mcginley_block": "filters.use_mcginley_filter",
            "exit_filter_block.exit_on_htf_trend_block": "filters.use_htf_trend_filter",
            "exit_filter_block.exit_on_vol_block": "filters.use_volume_filter",
            "exit_filter_block.exit_on_vol_part_block": "filters.use_volume_filter",
            "exit_filter_block.exit_on_atr_vol_block": "filters.use_atr_vol_filter",
            "exit_filter_block.exit_on_range_block": "filters.use_range_regime_filter",
        }
        dep = exit_dep.get(path)
        if dep is not None and not as_bool(get_path(cfg, dep, False), False):
            return False
        if path == "exit_filter_block.exit_on_range_block":
            if not as_bool(get_path(cfg, "filters.use_range_filters", False), False):
                return False

    if path.startswith("confirmation.") and path != "confirmation.enabled":
        if not as_bool(get_path(cfg, "confirmation.enabled", False), False):
            return False

    if path.startswith("filters.entry_pause.") and path != "filters.entry_pause.enabled":
        if not as_bool(get_path(cfg, "filters.entry_pause.enabled", False), False):
            return False
        if path == "filters.entry_pause.minimum_pass_count":
            mode = str(get_path(cfg, "filters.entry_pause.logic_mode", "")).strip().upper()
            if mode != "COUNT":
                return False

    if path == "guards.use_guard_recovery":
        if not guard_any_enabled(cfg):
            return False

    if path.startswith("guards.guard_recovery_") or path.startswith("guards.recovery_") or path.startswith("guards.recovery."):
        if not guard_any_enabled(cfg):
            return False
        if not as_bool(get_path(cfg, "guards.use_guard_recovery", False), False):
            return False

    return True


def build_active_diff_map(
    baseline_cfg: dict[str, Any],
    case_cfg: dict[str, Any],
) -> dict[str, tuple[str, str]]:
    bflat = flatten_leaves(baseline_cfg)
    cflat = flatten_leaves(case_cfg)
    keys = sorted(set(bflat.keys()) | set(cflat.keys()))
    diffs: dict[str, tuple[str, str]] = {}
    for path in keys:
        if not is_path_active(case_cfg, path):
            continue
        bval = normalize_value(bflat.get(path, None))
        cval = normalize_value(cflat.get(path, None))
        if bval != cval:
            diffs[path] = (bval, cval)
    return diffs


def is_categorical(path: str, values: set[str]) -> bool:
    if len(values) <= 1:
        return True
    if all(v in {"true", "false"} for v in values):
        return True
    if path.endswith(".mode") or path in {"signal_mode", "trade.entry_mode"}:
        return True
    if path.endswith(".enabled") or path.startswith(
        (
            "trade.exit_",
            "risk.use_",
            "stop_loss.use_",
            "take_profit.use_",
            "multi_tp.use_",
            "break_even.use_",
            "trailing.use_",
            "filters.use_",
            "guards.use_",
        )
    ):
        return True
    if len(values) <= 3:
        # Small finite alternatives can be treated as categorical.
        return True
    return False


def make_token(path: str, value: str, categorical: bool) -> str:
    if categorical:
        return f"{path}=={value}"
    return f"{path}::changed"


def pack_rank(pack: str) -> int:
    pack = (pack or "").strip()
    if pack == "core":
        return 0
    if pack == "boundary":
        return 1
    if pack == "pairwise":
        return 2
    return 3


def compute_hash_for_manifest(config: dict[str, Any]) -> str:
    # Keep this consistent with bootstrap hash style.
    obj = json.dumps(config, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(obj.encode("utf-8")).hexdigest()


def optimize(
    suite_root: Path,
    baseline_case_id: str,
) -> dict[str, Any]:
    manifest_path = suite_root / "manifests" / "cases_manifest_all.csv"
    rows = load_csv(manifest_path)
    enabled_rows = [r for r in rows if as_bool(r.get("enabled", "1"), True)]
    enabled_rows.sort(key=lambda r: parse_int(r.get("run_order", 0), 0))

    if not enabled_rows:
        raise RuntimeError("No enabled rows found in manifest.")

    by_case_id = {r["case_id"]: r for r in enabled_rows}
    if baseline_case_id and baseline_case_id in by_case_id:
        baseline_row = by_case_id[baseline_case_id]
    else:
        baseline_row = enabled_rows[0]
        baseline_case_id = baseline_row["case_id"]

    # Load configs.
    cfg_by_case: dict[str, dict[str, Any]] = {}
    for row in enabled_rows:
        case_id = row["case_id"]
        case_json_path = suite_root / row["case_json"]
        case_obj = load_json(case_json_path)
        cfg = case_obj.get("config", {})
        if not isinstance(cfg, dict):
            cfg = {}
        cfg_by_case[case_id] = cfg

    baseline_cfg = cfg_by_case[baseline_case_id]

    # Build per-case diff map.
    case_diffs: dict[str, dict[str, tuple[str, str]]] = {}
    path_value_map: dict[str, set[str]] = {}
    for case_id, cfg in cfg_by_case.items():
        if case_id == baseline_case_id:
            continue
        diffs = build_active_diff_map(baseline_cfg, cfg)
        if not diffs:
            continue
        case_diffs[case_id] = diffs
        for path, (_, val) in diffs.items():
            path_value_map.setdefault(path, set()).add(val)

    # Build token universe.
    token_kind: dict[str, tuple[str, str, str]] = {}
    # token -> (kind, path, target_value)
    for path, values in sorted(path_value_map.items()):
        categorical = is_categorical(path, values)
        if categorical:
            for v in sorted(values):
                token = make_token(path, v, True)
                token_kind[token] = ("value", path, v)
        else:
            token = make_token(path, "", False)
            token_kind[token] = ("changed", path, "")

    universe = set(token_kind.keys())

    # Candidate coverage map.
    case_tokens: dict[str, set[str]] = {}
    for case_id, diffs in case_diffs.items():
        tokens: set[str] = set()
        for path, (_, val) in diffs.items():
            values = path_value_map.get(path, set())
            categorical = is_categorical(path, values)
            token = make_token(path, val, True) if categorical else make_token(path, "", False)
            if token in universe:
                tokens.add(token)
        if tokens:
            case_tokens[case_id] = tokens

    # Greedy set cover.
    selected: set[str] = {baseline_case_id}
    covered: set[str] = set()
    candidate_order = sorted(
        [r for r in enabled_rows if r["case_id"] in case_tokens],
        key=lambda r: (pack_rank(r.get("pack", "")), parse_int(r.get("run_order", 0), 0)),
    )

    while covered != universe:
        best_case = None
        best_new: set[str] = set()
        for row in candidate_order:
            cid = row["case_id"]
            if cid in selected:
                continue
            new_tokens = case_tokens[cid] - covered
            if len(new_tokens) > len(best_new):
                best_case = cid
                best_new = new_tokens
            elif len(new_tokens) == len(best_new) and len(new_tokens) > 0 and best_case is not None:
                # Tie-break: prefer core, then lower run_order.
                current = by_case_id[cid]
                chosen = by_case_id[best_case]
                cur_key = (pack_rank(current.get("pack", "")), parse_int(current.get("run_order", 0), 0))
                cho_key = (pack_rank(chosen.get("pack", "")), parse_int(chosen.get("run_order", 0), 0))
                if cur_key < cho_key:
                    best_case = cid
                    best_new = new_tokens
        if not best_case or not best_new:
            # Cannot cover remaining tokens with existing candidates.
            break
        selected.add(best_case)
        covered |= best_new

    # Redundant prune (keep baseline always).
    selected_nonbaseline = sorted(
        [cid for cid in selected if cid != baseline_case_id],
        key=lambda cid: (pack_rank(by_case_id[cid].get("pack", "")), parse_int(by_case_id[cid].get("run_order", 0), 0)),
    )
    for cid in selected_nonbaseline:
        trial = selected - {cid}
        trial_covered: set[str] = set()
        for tcid in trial:
            if tcid == baseline_case_id:
                continue
            trial_covered |= case_tokens.get(tcid, set())
        if universe <= trial_covered:
            selected.remove(cid)

    # Build final rows with new run_order.
    selected_rows = [deepcopy(by_case_id[cid]) for cid in selected if cid in by_case_id]
    selected_rows.sort(key=lambda r: (pack_rank(r.get("pack", "")), parse_int(r.get("run_order", 0), 0)))
    for idx, row in enumerate(selected_rows, start=1):
        row["run_order"] = idx
        case_id = row.get("case_id", "")
        # Refresh fingerprints from current config (keep stable with selected set).
        cfg = cfg_by_case.get(case_id, {})
        row["canonical_config_hash"] = compute_hash_for_manifest(cfg)
        primary = row.get("primary_change", case_id)
        row["semantic_fingerprint"] = f"{row.get('pack','')}:{primary}:{row['canonical_config_hash'][:16]}"
        row["enabled"] = 1
        if row.get("tv_preset_name", "").strip() == "":
            row["tv_preset_name"] = case_id
        if row.get("expected_trade_behavior", "").strip() == "":
            mode = str(get_path(cfg, "signal_mode", "")).strip().lower()
            row["expected_trade_behavior"] = "ZERO_TRADE_EXPECTED" if mode == "none" else "NORMAL"
        row["notes"] = (row.get("notes", "").strip() + " | optimized_ui_coverage").strip(" |")

    # Write manifests.
    write_csv(suite_root / "manifests" / "cases_manifest_all.csv", ALL_HEADERS, selected_rows)
    for pack in ("core", "boundary", "pairwise"):
        subset = [r for r in selected_rows if r.get("pack", "") == pack]
        write_csv(suite_root / "manifests" / f"cases_manifest_{pack}.csv", ALL_HEADERS, subset)

    # Coverage report.
    token_headers = [
        "token",
        "kind",
        "path",
        "target_value",
        "covered",
        "covered_by_count",
        "covered_by_cases",
    ]
    coverage_rows: list[dict[str, Any]] = []
    selected_case_tokens = {cid: case_tokens.get(cid, set()) for cid in selected if cid != baseline_case_id}
    for token in sorted(universe):
        kind, path, target = token_kind[token]
        covered_by = sorted([cid for cid, toks in selected_case_tokens.items() if token in toks])
        coverage_rows.append(
            {
                "token": token,
                "kind": kind,
                "path": path,
                "target_value": target,
                "covered": 1 if covered_by else 0,
                "covered_by_count": len(covered_by),
                "covered_by_cases": ";".join(covered_by),
            }
        )
    write_csv(suite_root / "manifests" / "ui_coverage_tokens.csv", token_headers, coverage_rows)

    # Freeze summary.
    freeze = {
        "generated_at_utc": now_utc(),
        "baseline_case_id": baseline_case_id,
        "input_cases_enabled": len(enabled_rows),
        "final_cases_selected": len(selected_rows),
        "selected_by_pack": {
            "core": sum(1 for r in selected_rows if r.get("pack") == "core"),
            "boundary": sum(1 for r in selected_rows if r.get("pack") == "boundary"),
            "pairwise": sum(1 for r in selected_rows if r.get("pack") == "pairwise"),
        },
        "coverage_universe_tokens": len(universe),
        "coverage_tokens_covered": sum(1 for r in coverage_rows if r["covered"] == 1),
        "coverage_rate": (
            (sum(1 for r in coverage_rows if r["covered"] == 1) / len(universe)) if universe else 1.0
        ),
        "selection_method": "greedy_set_cover_plus_redundant_prune",
        "files": {
            "cases_manifest_all": "manifests/cases_manifest_all.csv",
            "cases_manifest_core": "manifests/cases_manifest_core.csv",
            "cases_manifest_boundary": "manifests/cases_manifest_boundary.csv",
            "cases_manifest_pairwise": "manifests/cases_manifest_pairwise.csv",
            "coverage_tokens": "manifests/ui_coverage_tokens.csv",
        },
    }
    freeze_path = suite_root / "manifests" / "final_case_set_freeze.json"
    freeze_path.write_text(json.dumps(freeze, ensure_ascii=True, indent=2), encoding="utf-8")

    md_lines = [
        "# Final Case Set Freeze",
        "",
        f"- generated_at_utc: {freeze['generated_at_utc']}",
        f"- baseline_case_id: {freeze['baseline_case_id']}",
        f"- final_cases_selected: {freeze['final_cases_selected']}",
        f"- selected_core: {freeze['selected_by_pack']['core']}",
        f"- selected_boundary: {freeze['selected_by_pack']['boundary']}",
        f"- selected_pairwise: {freeze['selected_by_pack']['pairwise']}",
        f"- coverage_tokens: {freeze['coverage_tokens_covered']}/{freeze['coverage_universe_tokens']}",
        f"- coverage_rate: {freeze['coverage_rate']:.4f}",
        "",
        "## Files",
        f"- {freeze['files']['cases_manifest_all']}",
        f"- {freeze['files']['cases_manifest_core']}",
        f"- {freeze['files']['cases_manifest_boundary']}",
        f"- {freeze['files']['cases_manifest_pairwise']}",
        f"- {freeze['files']['coverage_tokens']}",
    ]
    (suite_root / "manifests" / "final_case_set_freeze.md").write_text(
        "\n".join(md_lines) + "\n",
        encoding="utf-8",
    )

    return freeze


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Optimize case set for from-scratch UI coverage.")
    ap.add_argument("--suite-root", default="mtc_backtest/parity_suite_350", help="Suite root path")
    ap.add_argument("--baseline-case-id", default="parity_core_001_baseline_touch", help="Baseline case id")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    suite_root = Path(args.suite_root).resolve()
    freeze = optimize(suite_root, args.baseline_case_id)
    print(f"baseline_case_id={freeze['baseline_case_id']}")
    print(f"input_cases_enabled={freeze['input_cases_enabled']}")
    print(f"final_cases_selected={freeze['final_cases_selected']}")
    print(f"selected_core={freeze['selected_by_pack']['core']}")
    print(f"selected_boundary={freeze['selected_by_pack']['boundary']}")
    print(f"selected_pairwise={freeze['selected_by_pack']['pairwise']}")
    print(f"coverage_universe_tokens={freeze['coverage_universe_tokens']}")
    print(f"coverage_tokens_covered={freeze['coverage_tokens_covered']}")
    print(f"coverage_rate={freeze['coverage_rate']:.4f}")
    print(f"freeze_file={Path(args.suite_root) / 'manifests' / 'final_case_set_freeze.json'}")
    print("status=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
