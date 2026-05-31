"""
Evaluate the current best Supertrend candidate across regime-lock / entry-mode /
Heikin Ashi / wicks toggle combinations.

Outputs:
- full 16-combo matrix on train/target1/target2 windows
- stepwise greedy path in the requested order:
  regime_lock -> entry_mode -> use_ha -> use_wicks
"""
from __future__ import annotations

import argparse
import json
import time
from copy import deepcopy
from datetime import datetime, timezone, timedelta
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

import sys

sys.path.insert(0, str(PROJECT_ROOT))

from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner
from src.optimizer_v0.replay_candidates import _parse_dt

TOGGLE_ORDER = ["use_regime_lock", "entry_mode", "use_ha", "use_wicks"]
ENTRY_MODES = ["Edge", "Signal"]


def _load_case(case_path: Path) -> tuple[dict, MTCConfig]:
    payload = json.loads(case_path.read_text(encoding="utf-8"))
    cfg = MTCConfig.model_validate(payload["config"])
    return payload, cfg


def _load_window_specs(case_paths: dict[str, Path]) -> dict[str, tuple[datetime, datetime, int]]:
    out: dict[str, tuple[datetime, datetime, int]] = {}
    for name, path in case_paths.items():
        payload = json.loads(path.read_text(encoding="utf-8"))
        start = _parse_dt(payload["start_date"], as_end=False)
        end = _parse_dt(payload["end_date"], as_end=True)
        preroll_days = int(payload.get("preroll_days", 365))
        out[name] = (start, end, preroll_days)
    return out


def _load_data(dataset_name: str) -> pd.DataFrame:
    data_path = PROJECT_ROOT / "data" / dataset_name
    print(f"Loading data: {data_path}")
    df = pd.read_parquet(data_path)
    if "timestamp" not in df.columns:
        df = df.reset_index()
        if "timestamp" not in df.columns:
            df = df.rename(columns={df.columns[0]: "timestamp"})
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    print(f"  Rows: {len(df):,}  |  Range: {df['timestamp'].min()} -- {df['timestamp'].max()}")
    return df


def _set_toggle(cfg: MTCConfig, *, use_regime_lock: bool, entry_mode: str, use_ha: bool, use_wicks: bool) -> MTCConfig:
    cfg = deepcopy(cfg)
    cfg.trade.use_regime_lock = bool(use_regime_lock)
    cfg.trade.entry_mode = str(entry_mode)
    cfg.supertrend.use_ha = bool(use_ha)
    cfg.supertrend.use_wicks = bool(use_wicks)
    return cfg


def _slice_window(df: pd.DataFrame, *, start: datetime, end: datetime, preroll_days: int) -> pd.DataFrame:
    filter_start = start - timedelta(days=preroll_days) if preroll_days > 0 else start
    mask = (df["timestamp"] >= filter_start) & (df["timestamp"] <= end)
    return df.loc[mask].copy().reset_index(drop=True)


def _window_metrics(df_window: pd.DataFrame, cfg: MTCConfig, *, start: datetime, end: datetime, warmup_bars: int) -> dict[str, float]:
    runner = MTCRunner(cfg)
    t0 = time.time()
    results = runner.run(df_window, warmup_bars=warmup_bars, eval_start=start, eval_end=end)
    metrics = results["metrics"]
    dd_pct = abs(float(metrics.get("max_drawdown_pct", metrics.get("max_drawdown", 0.0))))
    return {
        "net_profit": float(metrics.get("net_profit", 0.0)),
        "max_dd_pct": dd_pct,
        "total_trades": int(metrics.get("total_trades", 0)),
        "win_rate": float(metrics.get("win_rate", 0.0)),
        "profit_factor": float(metrics.get("profit_factor", 0.0)),
        "profit_dd_ratio": float(metrics.get("profit_dd_ratio", 0.0)),
        "runtime_s": round(time.time() - t0, 2),
    }


def _evaluate_combo(
    window_data: dict[str, pd.DataFrame],
    window_specs: dict[str, tuple[datetime, datetime, int]],
    base_cfg: MTCConfig,
    *,
    warmup_bars: int,
    use_regime_lock: bool,
    entry_mode: str,
    use_ha: bool,
    use_wicks: bool,
) -> dict[str, object]:
    cfg = _set_toggle(
        base_cfg,
        use_regime_lock=use_regime_lock,
        entry_mode=entry_mode,
        use_ha=use_ha,
        use_wicks=use_wicks,
    )
    row: dict[str, object] = {
        "use_regime_lock": bool(use_regime_lock),
        "entry_mode": str(entry_mode),
        "use_ha": bool(use_ha),
        "use_wicks": bool(use_wicks),
        "combo_key": (
            f"regime={int(bool(use_regime_lock))}|"
            f"mode={entry_mode}|ha={int(bool(use_ha))}|wicks={int(bool(use_wicks))}"
        ),
    }
    for name, (start, end, _) in window_specs.items():
        metrics = _window_metrics(window_data[name], cfg, start=start, end=end, warmup_bars=warmup_bars)
        for key, value in metrics.items():
            row[f"{name}_{key}"] = value

    row["oos_net_sum"] = float(row["target1_net_profit"]) + float(row["target2_net_profit"])
    row["oos_dd_max"] = max(float(row["target1_max_dd_pct"]), float(row["target2_max_dd_pct"]))
    row["oos_trades_sum"] = int(row["target1_total_trades"]) + int(row["target2_total_trades"])
    row["all_net_sum"] = float(row["train_net_profit"]) + float(row["oos_net_sum"])
    row["oos_score"] = float(row["oos_net_sum"]) if float(row["oos_dd_max"]) == 0 else float(row["oos_net_sum"]) / float(row["oos_dd_max"])
    return row


def _sort_results(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(
        ["oos_net_sum", "oos_dd_max", "target2_net_profit", "combo_key"],
        ascending=[False, True, False, True],
    ).reset_index(drop=True)


def _pick_best(df: pd.DataFrame) -> pd.Series:
    return _sort_results(df).iloc[0]


def _run_stepwise(results_df: pd.DataFrame, base_state: dict[str, object]) -> pd.DataFrame:
    state = dict(base_state)
    steps: list[dict[str, object]] = []

    for step in TOGGLE_ORDER:
        candidate_values = ENTRY_MODES if step == "entry_mode" else [False, True]
        subset = results_df.copy()
        for key, value in state.items():
            if key == step:
                continue
            subset = subset[subset[key] == value]
        subset = subset[subset[step].isin(candidate_values)]
        best = _pick_best(subset)
        state[step] = best[step]
        steps.append(
            {
                "step": step,
                "selected_value": best[step],
                "use_regime_lock": bool(best["use_regime_lock"]),
                "entry_mode": str(best["entry_mode"]),
                "use_ha": bool(best["use_ha"]),
                "use_wicks": bool(best["use_wicks"]),
                "oos_net_sum": float(best["oos_net_sum"]),
                "oos_dd_max": float(best["oos_dd_max"]),
                "target1_net_profit": float(best["target1_net_profit"]),
                "target2_net_profit": float(best["target2_net_profit"]),
            }
        )

    return pd.DataFrame(steps)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sweep regime-lock/entry/HA/wicks combinations on the current best Supertrend candidate.")
    parser.add_argument(
        "--case",
        default="configs/cases/supertrend_current_best_candidate_20260308.json",
        help="Base candidate case JSON.",
    )
    parser.add_argument("--train-case", default="configs/cases/supertrend_wf_train_20260308.json")
    parser.add_argument("--target1-case", default="configs/cases/supertrend_wf_target1_20260308.json")
    parser.add_argument("--target2-case", default="configs/cases/supertrend_wf_target2_20260308.json")
    args = parser.parse_args()

    case_path = (PROJECT_ROOT / args.case).resolve()
    case_payload, base_cfg = _load_case(case_path)
    df = _load_data(case_payload["dataset"])
    warmup_bars = int(case_payload.get("warmup_bars", 200))
    case_paths = {
        "train": (PROJECT_ROOT / args.train_case).resolve(),
        "target1": (PROJECT_ROOT / args.target1_case).resolve(),
        "target2": (PROJECT_ROOT / args.target2_case).resolve(),
    }
    window_specs = _load_window_specs(case_paths)
    window_data = {
        name: _slice_window(df, start=start, end=end, preroll_days=preroll_days)
        for name, (start, end, preroll_days) in window_specs.items()
    }

    print("\n-- Toggle Sweep Setup --")
    print(f"  Case           : {case_path}")
    print(f"  ATR Length     : {base_cfg.supertrend.atr_len}")
    print(f"  Factor         : {base_cfg.supertrend.factor}")
    print(f"  Toggle Order   : {', '.join(TOGGLE_ORDER)}")
    print(f"  Total Combos   : 16")

    rows: list[dict[str, object]] = []
    combo_index = 0
    for use_regime_lock in [False, True]:
        for entry_mode in ENTRY_MODES:
            for use_ha in [False, True]:
                for use_wicks in [False, True]:
                    combo_index += 1
                    print(
                        f"  [{combo_index:02d}/16] "
                        f"regime_lock={use_regime_lock} "
                        f"entry_mode={entry_mode} "
                        f"use_ha={use_ha} "
                        f"use_wicks={use_wicks}"
                    )
                    rows.append(
                        _evaluate_combo(
                            window_data,
                            window_specs,
                            base_cfg,
                            warmup_bars=warmup_bars,
                            use_regime_lock=use_regime_lock,
                            entry_mode=entry_mode,
                            use_ha=use_ha,
                            use_wicks=use_wicks,
                        )
                    )

    results_df = _sort_results(pd.DataFrame(rows))
    results_df.insert(0, "rank_oos", range(1, len(results_df) + 1))

    base_state = {
        "use_regime_lock": bool(base_cfg.trade.use_regime_lock),
        "entry_mode": str(base_cfg.trade.entry_mode),
        "use_ha": bool(base_cfg.supertrend.use_ha),
        "use_wicks": bool(base_cfg.supertrend.use_wicks),
    }
    stepwise_df = _run_stepwise(results_df, base_state=base_state)

    out_dir = PROJECT_ROOT / "optimize_results"
    out_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    out_csv = out_dir / f"supertrend_candidate_toggle_sweep_{timestamp}.csv"
    out_xlsx = out_csv.with_suffix(".xlsx")

    results_df.to_csv(out_csv, index=False)
    with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:
        results_df.to_excel(writer, index=False, sheet_name="all_combos")
        stepwise_df.to_excel(writer, index=False, sheet_name="stepwise")

    print("\nToggle sweep complete")
    print(f"CSV : {out_csv}")
    print(f"XLSX: {out_xlsx}")
    print("\nTop OOS combinations:")
    print(
        results_df[
            [
                "rank_oos",
                "use_regime_lock",
                "entry_mode",
                "use_ha",
                "use_wicks",
                "oos_net_sum",
                "oos_dd_max",
                "target1_net_profit",
                "target2_net_profit",
                "all_net_sum",
            ]
        ].head(10).to_string(index=False)
    )
    print("\nStepwise path:")
    print(stepwise_df.to_string(index=False))


if __name__ == "__main__":
    main()
