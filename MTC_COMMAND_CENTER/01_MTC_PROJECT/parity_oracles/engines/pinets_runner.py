from __future__ import annotations

import json
import re
import shutil
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from parity_oracles.common.io_utils import NORMALIZED_FILES, ROOT, empty_normalized_set, read_json, result_payload, utc_now, write_csv, write_json
from parity_oracles.engines.python_engine_runner import _case_payload, _load_export_module
from parity_oracles.engines.runner_base import parser_for, raw_normalize_result, unavailable_result


SIGNAL_PLOTS = {
    "raw_long": "long_raw",
    "raw_short": "short_raw",
    "final_long": "long_gated",
    "final_short": "short_gated",
}


def _plot_values(raw: dict[str, object], title: str) -> list[object]:
    plots = raw.get("plots", {})
    if not isinstance(plots, dict):
        return []
    plot = plots.get(title, {})
    if not isinstance(plot, dict):
        return []
    data = plot.get("data", [])
    if not isinstance(data, list):
        return []
    values = []
    for item in data:
        if isinstance(item, dict):
            values.append(item.get("value", ""))
        else:
            values.append("")
    return values


def _truthy_plot(value: object) -> int:
    try:
        return int(float(value) != 0.0)
    except (TypeError, ValueError):
        return 0


def _build_case_bars(case_plan_path: Path) -> tuple[dict[str, object], list[object]]:
    export = _load_export_module()
    plan = read_json(case_plan_path)
    workbook_path = ROOT / "05_PARITY" / "case_001" / "MTC_V2_BINANCE_BTCUSDT.P_2026-04-03_827c5.xlsx"
    baseline = str(plan.get("baseline_reference_xlsx", ""))
    if baseline:
        candidate = ROOT.parent / baseline
        if candidate.exists():
            workbook_path = candidate
    workbook = export.openpyxl.load_workbook(workbook_path, data_only=True)
    try:
        props = export.export_props(workbook)
    finally:
        workbook.close()
    rows = export.load_all_rows()
    start, end = export.parse_range(str(props["Backtesting range"]))
    bars = export.build_bars(rows, start, end)
    return props, bars


def _write_data_outputs(out_dir: Path, bars: list[object]) -> dict[str, str]:
    outputs = empty_normalized_set(out_dir)
    rows = [
        {
            "timestamp": bar.timestamp.isoformat(),
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume,
        }
        for bar in bars
    ]
    filename, fields = NORMALIZED_FILES["data"]
    target = out_dir / filename
    write_csv(target, fields, rows)
    outputs["data"] = str(target)
    return outputs


def _write_input_json(path: Path, bars: list[object]) -> None:
    candles = [
        {
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume,
            "time": int(bar.timestamp.timestamp() * 1000),
            "openTime": int(bar.timestamp.timestamp() * 1000),
        }
        for bar in bars
    ]
    write_json(path, candles)


def _build_signal_adapter(source_pine: Path, out_dir: Path, config: dict[str, object] | None = None) -> Path:
    text = source_pine.read_text(encoding="utf-8")
    config = config or {}
    if str(config.get("signal_mode", "")) == "Range Filter":
        text = text.replace(
            'input.string("Supertrend", "Signal Mode", options=["Supertrend", "Range Filter"]',
            'input.string("Range Filter", "Signal Mode", options=["Supertrend", "Range Filter"]',
        )
        if "rf_range" in config:
            text = text.replace(
                'input.float(1000.0, "RF Range"',
                f'input.float({float(config["rf_range"])}, "RF Range"',
            )
    text = text.replace("syminfo.mintick", "0.1")
    text = text.replace("syminfo.mincontract", "0.000001")
    text = text.replace("syminfo.pointvalue", "1.0")
    text = text.replace("syminfo.tickerid", '"BINANCE:BTCUSDT.P"')
    text = re.sub(r"request\.security\([^,]+,\s*[^,]+,\s*([^,]+),\s*barmerge\.gaps_off,\s*barmerge\.lookahead_off\)", r"(\1)", text)
    transformed_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("strategy("):
            transformed_lines.append('indicator("MTC V2 PineTS Signal Adapter", overlay=true, max_labels_count=500, max_lines_count=500)')
            continue
        if "strategy.initial_capital" in line:
            line = line.replace("strategy.initial_capital", "10000.0")
        if (
            stripped.startswith("strategy.entry(")
            or stripped.startswith("strategy.exit(")
            or stripped.startswith("strategy.close(")
            or stripped.startswith("strategy.close_all(")
        ):
            indent = line[: len(line) - len(line.lstrip())]
            transformed_lines.append(f"{indent}na")
            continue
        transformed_lines.append(line)
    adapter_path = out_dir / "MTC_V2_PINETS_SIGNAL_ADAPTER.pine"
    adapter_path.write_text("\n".join(transformed_lines) + "\n", encoding="utf-8")
    return adapter_path


def _pine_bool(value: bool) -> str:
    return "true" if value else "false"


def _build_supertrend_signal_adapter(case_plan_path: Path, out_dir: Path) -> Path:
    plan = read_json(case_plan_path)
    config = plan.get("planned_overrides", {})
    if not isinstance(config, dict):
        config = {}
    atr_len = int(config.get("st_atr_len", 21))
    factor = float(config.get("st_factor", 4.0))
    use_wicks = bool(config.get("st_use_wicks", False))
    pine = f"""//@version=6
indicator("MTC V2 PineTS Supertrend Signal Adapter", overlay=false)
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
    adapter_path = out_dir / "MTC_V2_PINETS_SUPERTREND_SIGNAL_ADAPTER.pine"
    adapter_path.write_text(pine, encoding="utf-8")
    return adapter_path


def _normalize_pinets_raw(raw_path: Path, out_dir: Path, bars: list[object], outputs: dict[str, str]) -> list[str]:
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    warnings: list[str] = []
    if raw.get("status") != "success":
        error_path = out_dir / "pinets_error.txt"
        error_path.write_text(str(raw.get("error", "PineTS run failed")), encoding="utf-8")
        outputs["error"] = str(error_path)
        warnings.append("PineTS raw Pine execution failed; L1/L2 are not comparable until adapter succeeds.")
        return warnings

    signal_columns = {name: _plot_values(raw, plot_title) for name, plot_title in SIGNAL_PLOTS.items()}
    if not signal_columns["final_long"]:
        signal_columns["final_long"] = signal_columns["raw_long"]
        warnings.append("PineTS adapter did not export long_gated; normalized final_long falls back to long_raw.")
    if not signal_columns["final_short"]:
        signal_columns["final_short"] = signal_columns["raw_short"]
        warnings.append("PineTS adapter did not export short_gated; normalized final_short falls back to short_raw.")
    signal_rows = []
    for index, bar in enumerate(bars):
        signal_rows.append({
            "timestamp": bar.timestamp.isoformat(),
            "bar_index": bar.bar_index,
            "raw_long": _truthy_plot(signal_columns["raw_long"][index]) if index < len(signal_columns["raw_long"]) else 0,
            "raw_short": _truthy_plot(signal_columns["raw_short"][index]) if index < len(signal_columns["raw_short"]) else 0,
            "final_long": _truthy_plot(signal_columns["final_long"][index]) if index < len(signal_columns["final_long"]) else 0,
            "final_short": _truthy_plot(signal_columns["final_short"][index]) if index < len(signal_columns["final_short"]) else 0,
            "reason_code": "PINETS_PLOT_EXPORT",
        })
    filename, fields = NORMALIZED_FILES["signals"]
    target = out_dir / filename
    write_csv(target, fields, signal_rows)
    outputs["signals"] = str(target)

    indicator_rows = []
    indicator_map = {
        "supertrend_line": "supertrend_line",
        "direction": "supertrend_direction",
    }
    for plot_name, indicator_name in indicator_map.items():
        values = _plot_values(raw, plot_name)
        for index, value in enumerate(values[: len(bars)]):
            if value not in ("", None):
                indicator_rows.append({
                    "timestamp": bars[index].timestamp.isoformat(),
                    "indicator_name": indicator_name,
                    "value": value,
                })
    filename, fields = NORMALIZED_FILES["indicators"]
    target = out_dir / filename
    write_csv(target, fields, indicator_rows)
    outputs["indicators"] = str(target)
    return warnings


def _run_case_plan(case_plan_path: Path, out_dir: Path, pine: str, adapter_mode: str) -> int:
    started = utc_now()
    case = _case_payload(case_plan_path)
    plan = read_json(case_plan_path)
    config = plan.get("planned_overrides", {})
    if not isinstance(config, dict):
        config = {}
    _, bars = _build_case_bars(case_plan_path)
    outputs = _write_data_outputs(out_dir, bars)
    raw_path = out_dir / "pinets_raw.json"
    input_path = out_dir / "pinets_input_candles.json"
    _write_input_json(input_path, bars)
    if adapter_mode == "supertrend":
        adapter_path = _build_supertrend_signal_adapter(case_plan_path, out_dir)
    else:
        adapter_path = _build_signal_adapter(ROOT / pine, out_dir, config)
    module_path = ROOT.parent / "node_modules" / "pinets" / "dist" / "pinets.min.es.js"
    command = (
        "node parity_oracles/engines/pinets_signal_export.mjs "
        f"--pine {adapter_path} --data {input_path} --out {raw_path} --pinets-module {module_path}"
    )
    if not module_path.exists():
        error_path = out_dir / "pinets_error.txt"
        error_path.write_text(f"PineTS module not found: {module_path}", encoding="utf-8")
        outputs["error"] = str(error_path)
        result = result_payload("pinets", command, "engine_unavailable", case, outputs, started, errors=[error_path.read_text(encoding="utf-8")])
        write_json(out_dir / "result.json", result)
        return 2
    completed = subprocess.run(
        [
            "node",
            "parity_oracles/engines/pinets_signal_export.mjs",
            "--pine",
            str(adapter_path),
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
    outputs["raw"] = str(raw_path)
    outputs["adapter_pine"] = str(adapter_path)
    warnings = _normalize_pinets_raw(raw_path, out_dir, bars, outputs) if raw_path.exists() else []
    status = "success" if completed.returncode == 0 else "failed"
    errors = []
    if completed.returncode != 0:
        errors.append((completed.stderr or completed.stdout or "PineTS execution failed").strip())
    result = result_payload("pinets", command, status, case, outputs, started, errors=errors, warnings=warnings)
    write_json(out_dir / "result.json", result)
    return 0 if completed.returncode == 0 else 2


def main() -> int:
    parser = parser_for("pinets")
    parser.add_argument("--pine", default="01_PINE/MTC_V2.pine")
    parser.add_argument("--data")
    parser.add_argument("--adapter-mode", choices=["supertrend", "full"], default="full")
    args = parser.parse_args()
    case_ref = args.case_plan or args.case
    if case_ref is None:
        parser.error("--case or --case-plan is required")
    command = f"python parity_oracles/engines/pinets_runner.py --case-plan {case_ref} --out-dir {args.out_dir}"
    if args.case_plan:
        return _run_case_plan(args.case_plan, args.out_dir, args.pine, args.adapter_mode)
    if args.raw:
        return raw_normalize_result("pinets", case_ref, args.out_dir, command, args.raw)
    if shutil.which("pinets-cli") is None:
        return unavailable_result(
            "pinets",
            case_ref,
            args.out_dir,
            command,
            "pinets-cli not found. PineTS remains a signal/indicator oracle; provide --raw PineTS JSON/CSV or install local pinets-cli.",
        )
    return unavailable_result("pinets", case_ref, args.out_dir, command, "pinets-cli detected, but project-specific adapter invocation is not configured yet.")


if __name__ == "__main__":
    raise SystemExit(main())
