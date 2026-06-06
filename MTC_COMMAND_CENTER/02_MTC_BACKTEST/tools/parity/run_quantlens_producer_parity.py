#!/usr/bin/env python3
"""Run QuantLens producer-level Python vs PineTS raw-signal parity."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MCC_ROOT = PROJECT_ROOT.parent
REPO_ROOT = MCC_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.io import load_dataset, validate_dataset
from src.modules.signals.producers import create_producer
from src.workflow.signal_parity import compare_signals


FEATURE_ID = "producer_ql_fam_momentum_continuation_v1"
RAW_LONG_TITLE = f"FEATURE__{FEATURE_ID}__signal__raw_long"
RAW_SHORT_TITLE = f"FEATURE__{FEATURE_ID}__signal__raw_short"
DEFAULT_PINE = MCC_ROOT / "01_MTC_PROJECT" / "parity_oracles" / "feature_adapters" / "pinets" / f"{FEATURE_ID}.pine"
DEFAULT_PINETS_MODULE = PROJECT_ROOT / "node_modules" / "pinets" / "dist" / "pinets.min.es.js"


def _json_file(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8"))


def _timestamp_ms(value: Any) -> int:
    ts = pd.Timestamp(value)
    if ts.tzinfo is None:
        ts = ts.tz_localize("UTC")
    else:
        ts = ts.tz_convert("UTC")
    return int(ts.timestamp() * 1000)


def _write_pinets_input(df: pd.DataFrame, path: Path) -> None:
    candles = []
    for row in df.itertuples(index=False):
        ms = _timestamp_ms(getattr(row, "timestamp"))
        candles.append(
            {
                "open": float(getattr(row, "open")),
                "high": float(getattr(row, "high")),
                "low": float(getattr(row, "low")),
                "close": float(getattr(row, "close")),
                "volume": float(getattr(row, "volume")),
                "time": ms,
                "openTime": ms,
            }
        )
    path.write_text(json.dumps(candles), encoding="utf-8")


def _resolved_pine(source: Path, out_path: Path, params: dict[str, Any]) -> Path:
    text = source.read_text(encoding="utf-8")
    replacements = {
        "Momentum Lookback": int(params.get("mom_lb", 10)),
        "Trend EMA": int(params.get("trend_ema", 50)),
        "Breakout Lookback": int(params.get("breakout_lb", 10)),
    }
    for title, value in replacements.items():
        text = re.sub(
            rf'input\.int\(\d+,\s*"{re.escape(title)}"',
            f'input.int({value}, "{title}"',
            text,
            count=1,
        )
    out_path.write_text(text, encoding="utf-8")
    return out_path


def _plot_values(raw: dict[str, Any], title: str) -> list[Any]:
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
        values.append(item.get("value", "") if isinstance(item, dict) else "")
    return values


def _truthy(value: Any) -> bool:
    try:
        return float(value) > 0.5
    except (TypeError, ValueError):
        return False


def _write_signal_csv(df: pd.DataFrame, raw: dict[str, Any], path: Path) -> tuple[pd.Series, pd.Series]:
    long_values = _plot_values(raw, RAW_LONG_TITLE)
    short_values = _plot_values(raw, RAW_SHORT_TITLE)
    n = min(len(df), len(long_values), len(short_values))
    rows = []
    pine_long = []
    pine_short = []
    for i in range(n):
        long_bool = _truthy(long_values[i])
        short_bool = _truthy(short_values[i])
        pine_long.append(long_bool)
        pine_short.append(short_bool)
        rows.append(
            {
                "timestamp": df["timestamp"].iloc[i],
                "bar_index": i,
                "raw_long": int(long_bool),
                "raw_short": int(short_bool),
                RAW_LONG_TITLE: int(long_bool),
                RAW_SHORT_TITLE: int(short_bool),
            }
        )
    pd.DataFrame(rows).to_csv(path, index=False)
    return pd.Series(pine_long, dtype=bool), pd.Series(pine_short, dtype=bool)


def _report(payload: dict[str, Any]) -> str:
    parity = payload["parity"]
    return "\n".join(
        [
            "# QuantLens Producer Parity Report",
            "",
            f"- status: `{parity['status']}`",
            f"- feature_id: `{FEATURE_ID}`",
            f"- producer: `{payload['producer']}`",
            f"- data: `{payload['data']}`",
            f"- bars: `{parity['bars']}`",
            f"- long_match_rate: `{parity['long_match_rate']:.6f}`",
            f"- short_match_rate: `{parity['short_match_rate']:.6f}`",
            f"- min_match_rate: `{parity['min_match_rate']}`",
            f"- pine_adapter: `{payload['pine_adapter']}`",
            f"- resolved_pine_adapter: `{payload['resolved_pine_adapter']}`",
            f"- pine_signals_csv: `{payload['pine_signals_csv']}`",
            "",
            "## First Mismatches",
            "",
            f"- long: `{parity['long_mismatch_bars'][:20]}`",
            f"- short: `{parity['short_mismatch_bars'][:20]}`",
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare QuantLens producer raw signals between Python and PineTS.")
    parser.add_argument("--data", required=True, help="OHLCV CSV/parquet path")
    parser.add_argument("--producer", default="ql_fam_momentum_continuation")
    parser.add_argument("--producer-params", help="JSON params for the Python producer and resolved Pine adapter")
    parser.add_argument("--pine", default=str(DEFAULT_PINE), help="Standalone PineTS feature adapter")
    parser.add_argument("--pinets-module", default=str(DEFAULT_PINETS_MODULE), help="pinets.min.es.js path")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--min-match-rate", type=float, default=1.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data_path = Path(args.data)
    pine_path = Path(args.pine)
    module_path = Path(args.pinets_module)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not pine_path.exists():
        raise FileNotFoundError(f"Pine adapter not found: {pine_path}")
    if not module_path.exists():
        raise FileNotFoundError(f"PineTS module not found: {module_path}")

    params = _json_file(args.producer_params)
    producer = create_producer(args.producer, params)
    df = load_dataset(data_path)
    ok, messages = validate_dataset(df)
    if not ok:
        raise ValueError("Invalid dataset: " + "; ".join(messages))

    pinets_input = out_dir / "pinets_input_candles.json"
    pinets_raw = out_dir / "pinets_raw.json"
    resolved_pine = _resolved_pine(pine_path, out_dir / f"{FEATURE_ID}.resolved.pine", params)
    _write_pinets_input(df, pinets_input)

    completed = subprocess.run(
        [
            "node",
            str(MCC_ROOT / "01_MTC_PROJECT" / "parity_oracles" / "engines" / "pinets_signal_export.mjs"),
            "--pine",
            str(resolved_pine),
            "--data",
            str(pinets_input),
            "--out",
            str(pinets_raw),
            "--pinets-module",
            str(module_path),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        (out_dir / "pinets_stdout.txt").write_text(completed.stdout, encoding="utf-8")
        (out_dir / "pinets_stderr.txt").write_text(completed.stderr, encoding="utf-8")
        raise RuntimeError(completed.stderr or completed.stdout or "PineTS run failed")

    raw = json.loads(pinets_raw.read_text(encoding="utf-8"))
    if raw.get("status") != "success":
        raise RuntimeError(str(raw.get("error", "PineTS run failed")))

    pine_csv = out_dir / "pine_signals.csv"
    pine_long, pine_short = _write_signal_csv(df, raw, pine_csv)
    py_long, py_short = producer.generate(df)
    parity = compare_signals(py_long, py_short, pine_long, pine_short, min_match_rate=args.min_match_rate)
    payload = {
        "status": parity["status"],
        "producer": producer.name,
        "producer_params": params,
        "feature_id": FEATURE_ID,
        "data": str(data_path),
        "pine_adapter": str(pine_path),
        "resolved_pine_adapter": str(resolved_pine),
        "pinets_module": str(module_path),
        "pine_signals_csv": str(pine_csv),
        "pinets_raw": str(pinets_raw),
        "parity": parity,
    }
    (out_dir / "parity_compare.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (out_dir / "PARITY_REPORT.md").write_text(_report(payload), encoding="utf-8")
    print(json.dumps({"status": parity["status"], "report": str(out_dir / "PARITY_REPORT.md")}, indent=2))
    return 0 if parity["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
