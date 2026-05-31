from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "00_PYTHON"))

from mtc_v2.signals.supertrend import SupertrendSignal

from parity_oracles.common.io_utils import ROOT, git_code_hash, read_json, sha256_file, sha256_json, write_csv, write_json
from parity_oracles.engines.pinets_runner import _build_case_bars, _plot_values, _truthy_plot, _write_input_json


COMPARE_FIELDS = ["supertrend_line", "direction", "long_raw", "short_raw"]


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number):
        return None
    return number


def _same_value(field: str, left: Any, right: Any) -> bool:
    if field in {"long_raw", "short_raw", "direction"}:
        return str(left) == str(right)
    left_number = _optional_float(left)
    right_number = _optional_float(right)
    if left_number is None and right_number is None:
        return True
    if left_number is None or right_number is None:
        return False
    return math.isclose(left_number, right_number, abs_tol=1e-8, rel_tol=1e-6)


def _pine_bool(value: bool) -> str:
    return "true" if value else "false"


def _build_supertrend_pine(out_dir: Path, config: dict[str, Any]) -> Path:
    atr_len = int(config.get("st_atr_len", 21))
    factor = float(config.get("st_factor", 4.0))
    use_wicks = bool(config.get("st_use_wicks", False))
    pine = f"""//@version=6
indicator("MTC V2 Supertrend Isolation", overlay=false)
int st_atr_len = {atr_len}
float st_factor = {factor}
bool st_use_wicks = {_pine_bool(use_wicks)}
var float st_prev_close_state = na
var float st_prev_atr_state = na
var float st_prev_upper_band_state = na
var float st_prev_lower_band_state = na
var int st_prev_direction_state = na
var int st_tr_count = 0
var float st_tr_sum = 0.0

bool st_bar_valid = not na(open) and not na(high) and not na(low) and not na(close) and high >= low and open >= low and open <= high and close >= low and close <= high
float st_line = na
int st_direction = na
bool long_raw = false
bool short_raw = false

if not st_bar_valid
    st_line := st_prev_direction_state > 0 ? st_prev_lower_band_state : st_prev_upper_band_state
    st_direction := st_prev_direction_state
else
    float st_prev_close_for_tr = na(st_prev_close_state) ? close : st_prev_close_state
    float st_tr = math.max(high - low, math.max(math.abs(high - st_prev_close_for_tr), math.abs(low - st_prev_close_for_tr)))
    float st_atr = na
    if st_tr_count < st_atr_len
        st_tr_count += 1
        st_tr_sum += st_tr
        if st_tr_count == st_atr_len
            st_atr := st_tr_sum / st_atr_len
    else
        float st_prev_atr_for_calc = na(st_prev_atr_state) ? st_tr : st_prev_atr_state
        st_atr := ((st_prev_atr_for_calc * (st_atr_len - 1)) + st_tr) / st_atr_len

    if na(st_atr)
        st_prev_close_state := close
    else
        float st_basis = (high + low) / 2.0
        float st_basic_upper = st_basis + (st_factor * st_atr)
        float st_basic_lower = st_basis - (st_factor * st_atr)
        float st_next_upper = st_basic_upper
        if not na(st_prev_upper_band_state)
            st_next_upper := st_basic_upper < st_prev_upper_band_state or st_prev_close_state > st_prev_upper_band_state ? st_basic_upper : st_prev_upper_band_state
        float st_next_lower = st_basic_lower
        if not na(st_prev_lower_band_state)
            st_next_lower := st_basic_lower > st_prev_lower_band_state or st_prev_close_state < st_prev_lower_band_state ? st_basic_lower : st_prev_lower_band_state
        float st_high_eff = st_use_wicks ? high : close
        float st_low_eff = st_use_wicks ? low : close
        if na(st_prev_direction_state)
            st_direction := 1
        else if st_prev_direction_state < 0 and not na(st_prev_upper_band_state) and st_high_eff > st_prev_upper_band_state
            st_direction := 1
            long_raw := true
        else if st_prev_direction_state > 0 and not na(st_prev_lower_band_state) and st_low_eff < st_prev_lower_band_state
            st_direction := -1
            short_raw := true
        else
            st_direction := st_prev_direction_state
        st_line := st_direction > 0 ? st_next_lower : st_next_upper
        st_prev_atr_state := st_atr
        st_prev_upper_band_state := st_next_upper
        st_prev_lower_band_state := st_next_lower
        st_prev_direction_state := st_direction
        st_prev_close_state := close

plot(st_line, title="supertrend_line")
plot(float(st_direction), title="direction")
plot(long_raw ? 1.0 : 0.0, title="long_raw")
plot(short_raw ? 1.0 : 0.0, title="short_raw")
"""
    path = out_dir / "supertrend_only_adapter.pine"
    path.write_text(pine, encoding="utf-8")
    return path


def _python_rows(case_plan: Path, bars: list[Any]) -> list[dict[str, Any]]:
    plan = read_json(case_plan)
    config = plan.get("planned_overrides", {})
    signal = SupertrendSignal(config if isinstance(config, dict) else {})
    rows: list[dict[str, Any]] = []
    for bar in bars:
        raw = signal.calculate(bar)
        snapshot = signal.indicator_snapshot().supertrend
        rows.append({
            "timestamp": bar.timestamp.isoformat(),
            "bar_index": bar.bar_index,
            "supertrend_line": snapshot.line,
            "direction": snapshot.direction if snapshot.direction is not None else "",
            "long_raw": int(raw.long),
            "short_raw": int(raw.short),
        })
    return rows


def _pinets_rows(raw_path: Path, bars: list[Any]) -> list[dict[str, Any]]:
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    if raw.get("status") != "success":
        raise RuntimeError(str(raw.get("error", "PineTS Supertrend run failed")))
    values = {field: _plot_values(raw, field) for field in COMPARE_FIELDS}
    rows: list[dict[str, Any]] = []
    for index, bar in enumerate(bars):
        rows.append({
            "timestamp": bar.timestamp.isoformat(),
            "bar_index": bar.bar_index,
            "supertrend_line": values["supertrend_line"][index] if index < len(values["supertrend_line"]) else "",
            "direction": int(float(values["direction"][index])) if index < len(values["direction"]) and values["direction"][index] is not None else "",
            "long_raw": _truthy_plot(values["long_raw"][index]) if index < len(values["long_raw"]) else 0,
            "short_raw": _truthy_plot(values["short_raw"][index]) if index < len(values["short_raw"]) else 0,
        })
    return rows


def _compare_rows(python_rows: list[dict[str, Any]], pinets_rows: list[dict[str, Any]]) -> dict[str, Any]:
    first_divergence: dict[str, Any] | None = None
    matched = 0
    mismatched = 0
    for left, right in zip(python_rows, pinets_rows):
        diffs = []
        for field in COMPARE_FIELDS:
            if not _same_value(field, left.get(field), right.get(field)):
                diffs.append({"field": field, "python": left.get(field), "pinets": right.get(field)})
        if diffs:
            mismatched += 1
            if first_divergence is None:
                first_divergence = {
                    "timestamp": left["timestamp"],
                    "bar_index": left["bar_index"],
                    "diffs": diffs,
                    "python": left,
                    "pinets": right,
                }
        else:
            matched += 1
    return {
        "matched": matched,
        "mismatched": mismatched,
        "missing_in_pinets": max(0, len(python_rows) - len(pinets_rows)),
        "extra_in_pinets": max(0, len(pinets_rows) - len(python_rows)),
        "first_divergence": first_divergence,
        "passed": mismatched == 0 and len(python_rows) == len(pinets_rows),
    }


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    first = payload.get("first_divergence") or {}
    lines = [
        "# Supertrend PineTS Isolation",
        "",
        f"- Command: `{payload['command']}`",
        f"- Case: `{payload['case_id']}`",
        f"- Data hash: `{payload['data_hash']}`",
        f"- Config hash: `{payload['config_hash']}`",
        f"- Code hash: `{payload['code_hash']}`",
        f"- Verdict: `{payload['verdict']}`",
        "",
        "## Compared Fields",
        "",
        "- `supertrend_line`",
        "- `direction`",
        "- `long_raw`",
        "- `short_raw`",
        "",
        "## Summary",
        "",
        f"- matched: {payload['matched']}",
        f"- mismatched: {payload['mismatched']}",
        f"- missing_in_pinets: {payload['missing_in_pinets']}",
        f"- extra_in_pinets: {payload['extra_in_pinets']}",
        "",
        "## First Divergence",
        "",
    ]
    if first:
        lines.extend([
            f"- timestamp: `{first['timestamp']}`",
            f"- bar_index: `{first['bar_index']}`",
            f"- diffs: `{first['diffs']}`",
            f"- python: `{first['python']}`",
            f"- pinets: `{first['pinets']}`",
        ])
    else:
        lines.append("- None")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-plan", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    plan = read_json(args.case_plan)
    config = plan.get("planned_overrides", {})
    _, bars = _build_case_bars(args.case_plan)
    pine_path = _build_supertrend_pine(args.out_dir, config if isinstance(config, dict) else {})
    input_path = args.out_dir / "supertrend_input_candles.json"
    raw_path = args.out_dir / "supertrend_pinets_raw.json"
    _write_input_json(input_path, bars)
    module_path = ROOT.parent / "node_modules" / "pinets" / "dist" / "pinets.min.es.js"
    command = (
        "python parity_oracles/engines/supertrend_isolation_runner.py "
        f"--case-plan {args.case_plan} --out-dir {args.out_dir}"
    )
    completed = subprocess.run(
        [
            "node",
            "parity_oracles/engines/pinets_signal_export.mjs",
            "--pine",
            str(pine_path),
            "--data",
            str(input_path),
            "--out",
            str(raw_path),
            "--pinets-module",
            str(module_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    python_rows = _python_rows(args.case_plan, bars)
    write_csv(args.out_dir / "python_supertrend.csv", ["timestamp", "bar_index", *COMPARE_FIELDS], python_rows)
    if completed.returncode != 0:
        raw = json.loads(raw_path.read_text(encoding="utf-8")) if raw_path.exists() else {"error": completed.stderr}
        payload = {
            "case_id": str(plan.get("case_name", "case_001")),
            "command": command,
            "compared_fields": COMPARE_FIELDS,
            "data_hash": sha256_file(ROOT / "05_PARITY/01_TW_CHART_DATA/BINANCE_BTCUSDT.P, 60_consolidated_stable.csv"),
            "config_hash": sha256_json(config),
            "code_hash": git_code_hash(),
            "verdict": "PINETS_FAILED",
            "matched": 0,
            "mismatched": len(python_rows),
            "missing_in_pinets": len(python_rows),
            "extra_in_pinets": 0,
            "first_divergence": {"timestamp": "", "bar_index": "", "diffs": [{"field": "pinets", "python": "available", "pinets": raw.get("error", "failed")}]},
        }
        write_json(args.out_dir / "supertrend_isolation.json", payload)
        _write_markdown(args.out_dir / "supertrend_isolation.md", payload)
        return 1

    pinets_rows = _pinets_rows(raw_path, bars)
    write_csv(args.out_dir / "pinets_supertrend.csv", ["timestamp", "bar_index", *COMPARE_FIELDS], pinets_rows)
    comparison = _compare_rows(python_rows, pinets_rows)
    payload = {
        "case_id": str(plan.get("case_name", "case_001")),
        "command": command,
        "compared_fields": COMPARE_FIELDS,
        "data_hash": sha256_file(ROOT / "05_PARITY/01_TW_CHART_DATA/BINANCE_BTCUSDT.P, 60_consolidated_stable.csv"),
        "config_hash": sha256_json(config),
        "code_hash": git_code_hash(),
        "verdict": "PASS" if comparison["passed"] else "FAIL_SUPERTREND",
        **comparison,
    }
    write_json(args.out_dir / "supertrend_isolation.json", payload)
    _write_markdown(args.out_dir / "supertrend_isolation.md", payload)
    return 0 if comparison["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
