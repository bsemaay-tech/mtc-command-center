#!/usr/bin/env python3
"""
Parameter Sweep for No-Effect Cases.

For each no-effect parameter, runs Python backtests with various values
to find which values actually change the trade count.
Only sweeps parameters that exist in the Python config model.

Output: compare_runs/sweep_results.csv
"""

import sys, io, json, csv, copy, time as _time
from pathlib import Path
from datetime import datetime, timezone, timedelta, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Project paths
BASE = Path(r"C:\LAB\tradingview-lab\mtc_backtest")
SUITE = BASE / "parity_suite_350"
CASES_DIR = SUITE / "cases"
OUT_CSV = SUITE / "compare_runs" / "sweep_results.csv"

# Ensure imports
sys.path.insert(0, str(BASE))

import pandas as pd
from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner

# =====================================================================
# DATASET CACHE (load once, reuse for all runs)
# =====================================================================
_df_cache = {}


def load_dataset(filename: str) -> pd.DataFrame:
    if filename in _df_cache:
        return _df_cache[filename]
    filepath = BASE / "data" / filename
    if filepath.suffix == ".parquet":
        df = pd.read_parquet(filepath)
    else:
        df = pd.read_csv(filepath)
    if "timestamp" in df.columns:
        if pd.api.types.is_numeric_dtype(df["timestamp"]):
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        else:
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    else:
        df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")
    _df_cache[filename] = df
    return df


def _parse_dt(raw: str) -> datetime:
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        dt = datetime.strptime(raw, "%Y-%m-%d")
    if dt.hour == 0 and dt.minute == 0 and dt.second == 0 and "T" not in raw:
        dt = datetime.combine(dt.date(), time.min)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def run_backtest(case: dict, config_overrides: dict = None) -> int:
    """Run backtest with optional overrides, return trade count."""
    cfg_dict = copy.deepcopy(case.get("config", {}))

    # Apply overrides (deep merge)
    if config_overrides:
        for section, params in config_overrides.items():
            if section not in cfg_dict:
                cfg_dict[section] = {}
            if isinstance(params, dict):
                cfg_dict[section].update(params)
            else:
                cfg_dict[section] = params

    # Disable debug CSV export for speed
    if "parity" in cfg_dict:
        cfg_dict["parity"]["export_debug_csv"] = False

    config = MTCConfig.model_validate(cfg_dict)

    df = load_dataset(case["dataset"])
    start_dt = _parse_dt(case["start_date"])
    end_dt = _parse_dt(case["end_date"])
    preroll_days = case.get("preroll_days", 90)
    filter_start = start_dt - timedelta(days=preroll_days) if preroll_days > 0 else start_dt
    mask = (df["timestamp"] >= filter_start) & (df["timestamp"] <= end_dt)
    df_filtered = df.loc[mask].copy().reset_index(drop=True)
    warmup_bars = case.get("warmup_bars", 200)

    runner = MTCRunner(config)
    results = runner.run(
        df_filtered,
        warmup_bars=warmup_bars,
        eval_start=start_dt if preroll_days > 0 else None,
        eval_end=end_dt,
    )
    return results["metrics"]["total_trades"]


# =====================================================================
# SWEEP DEFINITIONS
# Each entry: (seq, case_file, tv_input_name, config_section, config_key, sweep_values)
# =====================================================================
SWEEPS = [
    # === RF Sub-params (signal_mode = "Range Filter Hybrid (ADX+Chop+BB)") ===
    (33, "parity_core_033_rf_rsi_length_v01.json",
     "[RF] RSI Length", "range_filter", "rsi_len",
     [5, 7, 10, 14, 21, 30, 40, 50]),

    (34, "parity_core_034_rf_use_bb_filter_range_mode_v01.json",
     "[RF] Use BB Filter", "range_filter", "use_bb_filter",
     [True, False]),

    (38, "parity_core_038_rf_adx_range_threshold_v01.json",
     "[RF] ADX Range Threshold", "range_filter", "adx_range_threshold",
     [10, 15, 20, 25, 30]),

    (40, "parity_core_040_rf_chop_range_threshold_v01.json",
     "[RF] Chop Range Threshold", "range_filter", "chop_range_threshold",
     [50, 55, 62, 70, 80]),

    (41, "parity_core_041_rf_rsi_oversold_v01.json",
     "[RF] RSI Oversold", "range_filter", "rsi_oversold",
     [10, 20, 30, 35, 40]),

    (42, "parity_core_042_rf_rsi_overbought_v01.json",
     "[RF] RSI Overbought", "range_filter", "rsi_overbought",
     [60, 65, 70, 80, 90]),

    (43, "parity_core_043_rf_bb_length_v01.json",
     "[RF] BB Length", "range_filter", "bb_len",
     [10, 15, 20, 25, 30, 40, 50]),

    (44, "parity_core_044_rf_bb_multiplier_v01.json",
     "[RF] BB Multiplier", "range_filter", "bb_mult",
     [1.0, 1.5, 2.0, 2.5, 3.0]),

    # === MACD Sub-params (use_macd_filter = true) ===
    (194, "parity_core_194_mode_v01.json",
     "MACD Mode", "filters", "macd_gate_mode",
     ["Regime", "Cross-State", "Histogram", "Distance", "HTF Bias", "STANDARD", "PPO_NORM"]),

    (198, "parity_bnd_198_signal_v02.json",
     "MACD Signal", "filters", "macd_signal_len",
     [1, 3, 5, 9, 15, 20, 30]),

    (204, "parity_core_204_min_distance_0_no_effect_v01.json",
     "MACD Min Distance", "filters", "macd_distance_pct",
     [0.0, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]),

    # === McGinley (use_mcginley_filter = true) ===
    (94, "parity_core_094_mcginley_length_v01.json",
     "[McGinley] Length", "filters", "mcginley_len",
     [3, 5, 10, 20, 50, 100, 200]),

    # === TP ATR Length ===
    (71, "parity_core_071_tp_atr_length_v01.json",
     "TP ATR Length", "take_profit", "atr_len",
     [3, 7, 14, 21, 30, 50]),

    # === Max MAE % (use_mae_guard = true parent) ===
    (131, "parity_core_131_max_mae_v01.json",
     "Max MAE %", "guards", "mae_max_pct",
     [0.1, 0.5, 1.0, 2.0, 4.0, 8.0, 15.0]),
]


def main():
    results = []
    total_runs = sum(len(s[5]) for s in SWEEPS)
    run_count = 0

    print(f"Parameter Sweep: {len(SWEEPS)} sequences, {total_runs} total runs")
    print("=" * 70)

    for seq, case_file, tv_name, section, key, values in SWEEPS:
        case_path = CASES_DIR / case_file
        if not case_path.exists():
            print(f"  SKIP seq {seq}: {case_file} not found")
            continue

        with open(case_path, encoding="utf-8") as f:
            case = json.load(f)

        print(f"\nSeq {seq:3d} | {tv_name}")
        print(f"  Case: {case_file}")
        print(f"  Config path: {section}.{key}")
        print(f"  Sweep values: {values}")

        trade_counts = {}
        for val in values:
            run_count += 1
            t0 = _time.time()
            try:
                overrides = {section: {key: val}}

                # For MAE guard: need to enable it
                if section == "guards" and key == "mae_max_pct":
                    overrides["guards"]["use_mae_guard"] = True

                tc = run_backtest(case, overrides)
                elapsed = _time.time() - t0
                trade_counts[str(val)] = tc
                print(f"  [{run_count:3d}/{total_runs}] {key}={val!s:>12s} → {tc:4d} trades  ({elapsed:.1f}s)")
            except Exception as e:
                trade_counts[str(val)] = f"ERROR: {e}"
                print(f"  [{run_count:3d}/{total_runs}] {key}={val!s:>12s} → ERROR: {e}")

        # Check if trade count varies
        numeric_counts = [v for v in trade_counts.values() if isinstance(v, int)]
        unique_counts = set(numeric_counts)
        has_effect = len(unique_counts) > 1

        if has_effect:
            min_tc = min(numeric_counts)
            max_tc = max(numeric_counts)
            print(f"  ✓ PARAMETER HAS EFFECT: {min_tc} - {max_tc} trades (Δ={max_tc-min_tc})")
            # Find best discriminating values
            for val_str, tc in trade_counts.items():
                if isinstance(tc, int) and tc != numeric_counts[0]:
                    print(f"    → Best test value: {key}={val_str} → {tc} trades (vs default {numeric_counts[0]})")
                    break
        else:
            count = numeric_counts[0] if numeric_counts else "N/A"
            print(f"  ✗ NO EFFECT: all values → {count} trades")

        # Store results
        for val_str, tc in trade_counts.items():
            results.append({
                "seq": seq,
                "tv_input_name": tv_name,
                "config_path": f"{section}.{key}",
                "value": val_str,
                "trade_count": tc,
                "has_effect": has_effect,
                "unique_counts": len(unique_counts),
            })

    # Write CSV
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "seq", "tv_input_name", "config_path", "value",
            "trade_count", "has_effect", "unique_counts",
        ])
        w.writeheader()
        w.writerows(results)

    print(f"\n{'='*70}")
    print(f"Results saved to: {OUT_CSV}")

    # Summary
    seqs_with_effect = set()
    seqs_no_effect = set()
    for r in results:
        if r["has_effect"]:
            seqs_with_effect.add(r["seq"])
        else:
            seqs_no_effect.add(r["seq"])

    print(f"\nSUMMARY:")
    print(f"  Parameters WITH effect:  {len(seqs_with_effect)} sequences")
    for s in sorted(seqs_with_effect):
        name = next(r["tv_input_name"] for r in results if r["seq"] == s)
        print(f"    seq {s:3d}: {name}")
    print(f"  Parameters NO effect:    {len(seqs_no_effect)} sequences")
    for s in sorted(seqs_no_effect):
        name = next(r["tv_input_name"] for r in results if r["seq"] == s)
        print(f"    seq {s:3d}: {name}")

    # Report unmapped parameters (can only test in TV)
    print(f"\n{'='*70}")
    print("UNMAPPED PARAMETERS (not in Python config, TV-only test needed):")
    unmapped = [
        ("seq 036", "[RF] Use Strategy TF Source", "No config path"),
        ("seq 096", "[McGinley] HTF Timeframe", "No mcginley HTF in Python"),
        ("seq 102", "Range Aggregation", "No aggregation mode in Python"),
        ("seq 221", "If LONG & SHORT raw same bar", "No confirmation module in Python"),
        ("seq 224", "Break buffer (ticks)", "No confirmation module in Python"),
        ("seq 225", "Max swing distance %", "No confirmation module in Python"),
    ]
    for seq_s, name, reason in unmapped:
        print(f"  {seq_s}: {name} → {reason}")


if __name__ == "__main__":
    main()
