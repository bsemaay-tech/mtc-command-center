from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from parity_oracles.common.io_utils import NORMALIZED_FILES, ROOT, read_json, result_payload, utc_now, write_csv, write_json
from parity_oracles.engines.runner_base import parser_for, raw_normalize_result, unavailable_result


KNOWN_ENTRYPOINTS = [
    "05_PARITY/manual_tw_futures_audit.py",
    "05_PARITY/validate_export_parity.py",
    "05_PARITY/run_close_only_canonical.py",
    "00_PYTHON/mtc_v2/core/runner.py",
]


def _load_export_module():
    sys.path.insert(0, str(ROOT / "05_PARITY"))
    sys.path.insert(0, str(ROOT / "00_PYTHON"))
    import validate_export_parity

    return validate_export_parity


def _case_payload(case_plan_path: Path) -> dict[str, object]:
    plan = read_json(case_plan_path)
    overrides = plan.get("planned_overrides", {})
    return {
        "case_id": str(plan.get("case_name") or f"case_{plan.get('case_no', 'unknown')}"),
        "symbol": "BTCUSDT.P",
        "timeframe": "60",
        "start_time": "",
        "end_time": "",
        "exchange": "BINANCE",
        "data_file": "05_PARITY/01_TW_CHART_DATA/BINANCE_BTCUSDT.P, 60_consolidated_stable.csv",
        "mtc_config": overrides if isinstance(overrides, dict) else {},
        "warmup_bars": int(overrides.get("warmup_bars", 0)) if isinstance(overrides, dict) else 0,
        "commission": 0.0,
        "slippage": 0.0,
        "initial_capital": 10000.0,
        "sizing": {"mode": "case_plan"},
        "expected_reference_source": str(plan.get("baseline_reference_xlsx", "")),
        "case_plan": str(case_plan_path),
    }


def _as_number(value: object) -> object:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    return value


def _config_from_case_plan_overrides(export_config: dict[str, object], plan: dict[str, object]) -> dict[str, object]:
    from mtc_v2.core.config import DEFAULT_CONFIG

    overrides = plan.get("planned_overrides", {})
    if not isinstance(overrides, dict):
        return export_config
    config = dict(export_config)
    for key, value in overrides.items():
        if key in DEFAULT_CONFIG:
            config[key] = value
    sl_mode = str(overrides.get("sl_mode", ""))
    if sl_mode:
        config["use_sl"] = sl_mode != "None"
        config["use_sl_atr"] = sl_mode == "ATR"
        config["use_sl_percent"] = sl_mode == "Percent"
        config["use_sl_swing_atr"] = sl_mode in {"Swing", "Swing+ATR"}
    tp_mode = str(overrides.get("tp_mode", ""))
    if tp_mode:
        config["tp_mode"] = tp_mode
    return config


def _write_real_case_outputs(case_plan_path: Path, out_dir: Path, config_source: str) -> tuple[dict[str, str], dict[str, object]]:
    export = _load_export_module()
    from mtc_v2.core.config import SIGNAL_MODE_RANGE_FILTER
    from mtc_v2.signals.range_filter import RangeFilterSignal
    from mtc_v2.signals.supertrend import SupertrendSignal

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
    export_config = export.build_config(props)
    runner_config = export_config if config_source == "export_workbook" else _config_from_case_plan_overrides(export_config, plan)
    runner = export.Runner(runner_config)
    raw_signal_producer = None
    if config_source == "case_plan_overrides":
        raw_signal_producer = (
            RangeFilterSignal(runner_config)
            if str(runner_config.get("signal_mode")) == SIGNAL_MODE_RANGE_FILTER
            else SupertrendSignal(runner_config)
        )

    data_rows: list[dict[str, object]] = []
    indicator_rows: list[dict[str, object]] = []
    signal_rows: list[dict[str, object]] = []
    decision_rows: list[dict[str, object]] = []
    trade_rows: list[dict[str, object]] = []
    trade_id = 1

    for bar in bars:
        position_before = runner.state.position.side if runner.state.position is not None else "flat"
        raw_signal = raw_signal_producer.calculate(bar) if raw_signal_producer is not None else None
        signals = runner.run([bar])
        signal = signals[-1]
        normalized_signal = raw_signal or signal
        snapshot = runner.state.indicator_snapshot
        position_after = runner.state.position.side if runner.state.position is not None else "flat"
        data_rows.append({
            "timestamp": bar.timestamp.isoformat(),
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume,
        })
        for name, value in [
            ("supertrend_line", snapshot.supertrend.line),
            ("supertrend_direction", snapshot.supertrend.direction),
        ]:
            if value is not None:
                indicator_rows.append({"timestamp": bar.timestamp.isoformat(), "indicator_name": name, "value": _as_number(value)})
        signal_rows.append({
            "timestamp": bar.timestamp.isoformat(),
            "bar_index": bar.bar_index,
            "raw_long": int(bool(normalized_signal.long)),
            "raw_short": int(bool(normalized_signal.short)),
            "final_long": int(bool(normalized_signal.long)),
            "final_short": int(bool(normalized_signal.short)),
            "reason_code": normalized_signal.reason or "",
        })
        side = "long" if signal.long else "short" if signal.short else ""
        if side or runner.state.opened_this_bar_reason or runner.state.closed_this_bar_reason:
            decision_rows.append({
                "timestamp": bar.timestamp.isoformat(),
                "bar_index": bar.bar_index,
                "side": side,
                "entry_allowed": int(bool(runner.state.opened_this_bar_reason)),
                "blocked_reason": "" if runner.state.opened_this_bar_reason else runner.state.closed_this_bar_reason or "",
                "position_before": position_before,
                "position_after": position_after,
            })
        if runner.state.opened_this_bar_reason and runner.state.position is not None:
            pos = runner.state.position
            trade_rows.append({
                "trade_id": trade_id,
                "timestamp": bar.timestamp.isoformat(),
                "bar_index": bar.bar_index,
                "event_type": "ENTRY",
                "side": pos.side,
                "qty": pos.qty,
                "price": pos.entry_price,
                "reason": runner.state.opened_this_bar_reason,
                "sl": _as_number(pos.active_stop_price),
                "tp": _as_number(pos.active_tp_price),
                "commission": 0,
                "equity_after": runner.state.equity,
            })
            trade_id += 1
        for event in runner.state.exit_events_this_bar:
            trade_rows.append({
                "trade_id": trade_id,
                "timestamp": bar.timestamp.isoformat(),
                "bar_index": bar.bar_index,
                "event_type": "EXIT",
                "side": position_before,
                "qty": event.exit_qty,
                "price": event.exit_price,
                "reason": event.exit_reason,
                "sl": "",
                "tp": "",
                "commission": 0,
                "equity_after": runner.state.equity,
            })
            trade_id += 1

    outputs: dict[str, str] = {}
    for key, rows_for_file in [
        ("data", data_rows),
        ("indicators", indicator_rows),
        ("signals", signal_rows),
        ("decisions", decision_rows),
        ("trades", trade_rows),
    ]:
        filename, fields = NORMALIZED_FILES[key]
        target = out_dir / filename
        write_csv(target, fields, rows_for_file)
        outputs[key] = str(target)
    stats = {
        "bar_count": len(data_rows),
        "indicator_row_count": len(indicator_rows),
        "signal_row_count": len(signal_rows),
        "trade_event_count": len(trade_rows),
        "net_profit": runner.state.equity - runner.state.initial_capital,
        "initial_capital": runner.state.initial_capital,
        "final_equity": runner.state.equity,
    }
    stats_path = out_dir / "normalized_stats.json"
    write_json(stats_path, stats)
    outputs["stats"] = str(stats_path)
    return outputs, runner.config


def main() -> int:
    parser = parser_for("python_engine")
    parser.add_argument("--config-source", choices=["export_workbook", "case_plan_overrides"], default="export_workbook")
    args = parser.parse_args()
    case_ref = args.case_plan or args.case
    if case_ref is None:
        parser.error("--case or --case-plan is required")
    command = (
        f"python parity_oracles/engines/python_engine_runner.py --case-plan {case_ref} "
        f"--out-dir {args.out_dir} --config-source {args.config_source}"
    )
    if args.case_plan:
        started = utc_now()
        case = _case_payload(args.case_plan)
        outputs, runner_config = _write_real_case_outputs(args.case_plan, args.out_dir, args.config_source)
        case["mtc_config"] = runner_config
        case["sizing"] = {"mode": args.config_source}
        result = result_payload("python_engine", command, "success", case, outputs, started)
        result["case"] = case
        result["config_source"] = args.config_source
        write_json(args.out_dir / "result.json", result)
        return 0
    if args.raw:
        return raw_normalize_result("python_engine", case_ref, args.out_dir, command, args.raw)
    detected = [entry for entry in KNOWN_ENTRYPOINTS if (ROOT / entry).exists()]
    if detected:
        note = "Detected candidate MTC engine entrypoints: " + ", ".join(detected) + ". Wrapper is a documentation stub until a single CLI contract is selected."
        return raw_normalize_result("python_engine", case_ref, args.out_dir, command, None, warnings=[note])
    return unavailable_result("python_engine", case_ref, args.out_dir, command, "No obvious MTC Python engine entrypoint detected.")


if __name__ == "__main__":
    raise SystemExit(main())
