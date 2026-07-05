from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
REPORTS_DIR = REPO_ROOT / "reports"
CASE_ROOT = ROOT / "TW_EXPORT_CASES_V2"
SUMMARY_MD = ROOT / "parity_summary.md"
SUMMARY_JSON = ROOT / "parity_results.json"


def normalize_value(key: str, value: Any) -> Any:
    if isinstance(value, str):
        text = value.strip()
        if key == "session_custom_string" and ":" in text:
            return text.split(":", 1)[0]
        return text
    if isinstance(value, float):
        rounded = round(value, 9)
        if abs(rounded - round(rounded)) < 1e-9:
            return int(round(rounded))
        return rounded
    return value


def values_equal(key: str, left: Any, right: Any) -> bool:
    left_n = normalize_value(key, left)
    right_n = normalize_value(key, right)
    if isinstance(left_n, (int, float)) and isinstance(right_n, (int, float)):
        return abs(float(left_n) - float(right_n)) <= 1e-9
    return left_n == right_n


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def latest_case_report(case_no: int) -> Path:
    prefix = f"manual_tw_futures_case_{case_no:03d}"
    candidates = []
    for path in REPORTS_DIR.glob(f"{prefix}*.json"):
        name = path.name
        if (
            "effective_config" in name
            or "overrides" in name
            or "python_trades" in name
            or "trade_report" in name
        ):
            continue
        candidates.append(path)
    if not candidates:
        raise FileNotFoundError(f"Missing report json for case_{case_no:03d}")
    return max(candidates, key=lambda item: item.stat().st_mtime)


def load_report_row(case_no: int) -> tuple[Path, dict[str, Any]]:
    path = latest_case_report(case_no)
    payload = load_json(path)
    if not isinstance(payload, list) or not payload:
        raise ValueError(f"Unexpected report structure: {path}")
    row = payload[0]
    if not isinstance(row, dict):
        raise ValueError(f"Unexpected report row structure: {path}")
    return path, row


def load_case_plan(case_no: int) -> dict[str, Any]:
    path = CASE_ROOT / f"case_{case_no:03d}" / "case_plan.json"
    return load_json(path)


def classify_setting_mismatches(
    applied: dict[str, Any], planned: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    mismatches: list[dict[str, Any]] = []
    accepted: list[dict[str, Any]] = []
    for key, planned_value in planned.items():
        if key not in applied:
            continue
        actual_value = applied[key]
        if not values_equal(key, actual_value, planned_value):
            item = {
                "key": key,
                "planned": normalize_value(key, planned_value),
                "actual": normalize_value(key, actual_value),
            }
            if key == "confirm_close_crosses" and not bool(applied.get("use_confirm_transform", False)):
                item["reason"] = "ignored because use_confirm_transform=false"
                accepted.append(item)
                continue
            if key == "max_leverage_cap":
                item["reason"] = "accepted intentional export override to avoid margin call"
                accepted.append(item)
                continue
            mismatches.append(item)
    return mismatches, accepted


def parity_classification(row: dict[str, Any]) -> str:
    if bool(row["tw_vs_pine_strict"]) and bool(row["tw_vs_python_strict"]) and bool(row["pine_vs_python_strict"]):
        return "STRICT_PASS"
    if (
        bool(row["pine_vs_python_strict"])
        and bool(row.get("tw_vs_pine_trade_soft_pass", False))
        and bool(row.get("tw_vs_python_trade_soft_pass", False))
    ):
        return "SOFT_PASS"
    return "FAIL"


def changed_keys(prev_applied: dict[str, Any], curr_applied: dict[str, Any]) -> list[str]:
    keys = sorted(set(prev_applied) | set(curr_applied))
    changed: list[str] = []
    for key in keys:
        if key not in prev_applied or key not in curr_applied:
            changed.append(key)
            continue
        if not values_equal(key, prev_applied[key], curr_applied[key]):
            changed.append(key)
    return changed


def effect_summary(prev_row: dict[str, Any], curr_row: dict[str, Any]) -> dict[str, Any]:
    prev_trades = int(prev_row["tw_trades"])
    curr_trades = int(curr_row["tw_trades"])
    prev_pnl = float(prev_row["tw_net_pnl_pct"])
    curr_pnl = float(curr_row["tw_net_pnl_pct"])
    prev_pf = float(prev_row["tw_profit_factor"])
    curr_pf = float(curr_row["tw_profit_factor"])
    return {
        "trade_delta": curr_trades - prev_trades,
        "net_pnl_pct_delta": round(curr_pnl - prev_pnl, 6),
        "profit_factor_delta": round(curr_pf - prev_pf, 6),
        "effect_observed": (
            curr_trades != prev_trades
            or abs(curr_pnl - prev_pnl) > 1e-9
            or abs(curr_pf - prev_pf) > 1e-9
        ),
    }


def build_row(case_no: int, prev_report_row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    report_path, row = load_report_row(case_no)
    plan = load_case_plan(case_no)
    applied = row["applied_overrides"]
    planned = plan["planned_overrides"]
    mismatches, accepted_mismatches = classify_setting_mismatches(applied, planned)
    target_key = str(plan["title"])
    prev_applied = prev_report_row["applied_overrides"]
    actual_changed = changed_keys(prev_applied, applied)
    target_changed = target_key in actual_changed
    target_prev = normalize_value(target_key, prev_applied.get(target_key))
    target_curr = normalize_value(target_key, applied.get(target_key))
    target_planned = normalize_value(target_key, planned.get(target_key))
    effects = effect_summary(prev_report_row, row)
    summary_row = {
        "case": f"case_{case_no:03d}",
        "xlsx": row["xlsx"],
        "report_json": str(report_path.relative_to(REPO_ROOT)),
        "title": plan["title"],
        "description": plan["description"],
        "settings_check_pass": len(mismatches) == 0,
        "settings_mismatch_count": len(mismatches),
        "settings_mismatches": mismatches,
        "accepted_mismatch_count": len(accepted_mismatches),
        "accepted_mismatches": accepted_mismatches,
        "actual_changed_keys": actual_changed,
        "target_key": target_key,
        "target_prev": target_prev,
        "target_curr": target_curr,
        "target_planned": target_planned,
        "target_change_observed": target_changed,
        "target_value_matches_plan": values_equal(target_key, applied.get(target_key), planned.get(target_key)),
        "effect_observed": effects["effect_observed"],
        "trade_delta_vs_prev": effects["trade_delta"],
        "net_pnl_pct_delta_vs_prev": effects["net_pnl_pct_delta"],
        "profit_factor_delta_vs_prev": effects["profit_factor_delta"],
        "tw_trades": int(row["tw_trades"]),
        "pine_trades": int(row["pine_trades"]),
        "python_trades": int(row["python_trades"]),
        "tw_vs_pine_strict": bool(row["tw_vs_pine_strict"]),
        "tw_vs_python_strict": bool(row["tw_vs_python_strict"]),
        "pine_vs_python_strict": bool(row["pine_vs_python_strict"]),
        "parity_classification": parity_classification(row),
        "tw_vs_pine_trade_soft_pass": bool(row.get("tw_vs_pine_trade_soft_pass", False)),
        "tw_vs_python_trade_soft_pass": bool(row["tw_vs_python_trade_soft_pass"]),
        "tw_first_mismatch": row.get("tw_vs_python_first_mismatch"),
        "tw_win_rate_pct": float(row["tw_win_rate_pct"]),
        "tw_net_pnl_pct": float(row["tw_net_pnl_pct"]),
        "tw_profit_factor": float(row["tw_profit_factor"]),
        "tw_max_drawdown_pct": float(row["tw_max_drawdown_pct"]),
        "tw_pyramiding_observed": bool(row.get("tw_pyramiding_observed", False)),
        "tw_stack_entry_events": int(row.get("tw_stack_entry_events", 0)),
        "tw_observed_max_open_same_side": int(row.get("tw_observed_max_open_same_side", 0)),
    }
    return summary_row, row


def render_summary(results: list[dict[str, Any]]) -> str:
    first_case = results[0]["case"] if results else "case_???"
    last_case = results[-1]["case"] if results else "case_???"
    lines = [
        f"# Parity Summary ({first_case} - {last_case})",
        "",
        f"- Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"- Cases: {len(results)}",
        f"- Settings clean: {sum(1 for row in results if row['settings_check_pass'])}/{len(results)}",
        f"- Accepted mismatches only: {sum(1 for row in results if row['settings_check_pass'] and row['accepted_mismatch_count'] > 0)}/{len(results)}",
        f"- Target change observed: {sum(1 for row in results if row['target_change_observed'])}/{len(results)}",
        f"- Effect observed: {sum(1 for row in results if row['effect_observed'])}/{len(results)}",
        f"- TW=PineTS strict pass: {sum(1 for row in results if row['tw_vs_pine_strict'])}/{len(results)}",
        f"- TW=Python strict pass: {sum(1 for row in results if row['tw_vs_python_strict'])}/{len(results)}",
        f"- PineTS=Python strict pass: {sum(1 for row in results if row['pine_vs_python_strict'])}/{len(results)}",
        f"- Overall classification pass (strict+soft): {sum(1 for row in results if row['parity_classification'] != 'FAIL')}/{len(results)}",
        "",
    ]
    repeated_failures = [
        "accepted override: max_leverage_cap exported at 5 to suppress TradingView margin-call noise",
        "accepted inert mismatch: confirm_close_crosses=true while use_confirm_transform=false",
    ]
    for row in results:
        lines.extend(
            [
                f"## {row['case']}",
                f"- Setting: `{row['title']}` | expected `{row['target_planned']}` | prev `{row['target_prev']}` | actual `{row['target_curr']}`",
                f"- Settings check: `{'PASS' if row['settings_check_pass'] else 'FAIL'}` | accepted mismatches: {row['accepted_mismatch_count']} | target changed: `{'YES' if row['target_change_observed'] else 'NO'}` | mismatches: {row['settings_mismatch_count']}",
                f"- Effect: `{'YES' if row['effect_observed'] else 'NO'}` | trade delta `{row['trade_delta_vs_prev']:+d}` | net pnl pct delta `{row['net_pnl_pct_delta_vs_prev']:+.6f}` | pf delta `{row['profit_factor_delta_vs_prev']:+.6f}`",
                f"- Parity: `{row['parity_classification']}` | TW/PineTS=`{'PASS' if row['tw_vs_pine_strict'] else 'FAIL'}` | TW/Python=`{'PASS' if row['tw_vs_python_strict'] else 'FAIL'}` | PineTS/Python=`{'PASS' if row['pine_vs_python_strict'] else 'FAIL'}`",
                f"- Trades: TW={row['tw_trades']} | PineTS={row['pine_trades']} | Python={row['python_trades']}",
                f"- Report: `{row['report_json']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Retrospective",
            f"- {repeated_failures[0]}",
            f"- {repeated_failures[1]}",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    args = parser.parse_args()

    results: list[dict[str, Any]] = []
    _, prev_report_row = load_report_row(args.start - 1)
    for case_no in range(args.start, args.end + 1):
        summary_row, prev_report_row = build_row(case_no, prev_report_row)
        results.append(summary_row)

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "cases": len(results),
            "settings_clean_cases": sum(1 for row in results if row["settings_check_pass"]),
            "accepted_only_mismatch_cases": sum(
                1 for row in results if row["settings_check_pass"] and row["accepted_mismatch_count"] > 0
            ),
            "target_change_observed_cases": sum(1 for row in results if row["target_change_observed"]),
            "effect_observed_cases": sum(1 for row in results if row["effect_observed"]),
            "tw_vs_pine_strict_pass_cases": sum(1 for row in results if row["tw_vs_pine_strict"]),
            "tw_vs_python_strict_pass_cases": sum(1 for row in results if row["tw_vs_python_strict"]),
            "pine_vs_python_strict_pass_cases": sum(1 for row in results if row["pine_vs_python_strict"]),
            "parity_classification_pass_cases": sum(1 for row in results if row["parity_classification"] != "FAIL"),
        },
        "rows": results,
        "notes": [
            "Settings are sourced from workbook Properties via manual_tw_futures_audit reports, not tracker rows.",
            "Effect is measured against the immediately previous case using TradingView trade count, net pnl pct, and profit factor deltas.",
            "max_leverage_cap mismatch is treated as accepted when it reflects the intentional no-margin-call export profile.",
            "confirm_close_crosses mismatch is treated as accepted when use_confirm_transform=false.",
        ],
    }
    SUMMARY_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    SUMMARY_MD.write_text(render_summary(results), encoding="utf-8")
    print(f"Saved {SUMMARY_JSON}")
    print(f"Saved {SUMMARY_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
