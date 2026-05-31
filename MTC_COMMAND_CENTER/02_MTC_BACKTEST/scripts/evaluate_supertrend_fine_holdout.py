"""
Evaluate the top fine-grid Supertrend ATR/Factor candidates on an unseen holdout.

Reads the latest fine-grid combined CSV, selects the top-N in-sample candidates by
score, then reruns them on the pre-optimization holdout window using the corrected
BTCUSDT.P parity contract and terminal MANUAL close.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner


def _load_data() -> pd.DataFrame:
    data_path = PROJECT_ROOT / "data" / "BTCUSDT_PERP_15m_20240101_20260101_long.parquet"
    print(f"Loading data: {data_path}")
    df = pd.read_parquet(data_path)
    if "timestamp" not in df.columns:
        df = df.reset_index()
        if "timestamp" not in df.columns:
            df = df.rename(columns={df.columns[0]: "timestamp"})
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    print(f"  Rows: {len(df):,}  |  Range: {df['timestamp'].min()} -- {df['timestamp'].max()}")
    return df


def _load_base_config() -> MTCConfig:
    config_path = PROJECT_ROOT / "configs" / "cases" / "supertrend_atr_factor_optimize.json"
    with open(config_path, encoding="utf-8") as f:
        cfg_dict = json.load(f)
    cfg_dict.pop("_meta", None)
    base_config = MTCConfig.model_validate(cfg_dict)
    base_config.parity.enabled = True
    base_config.parity.force_terminal_manual_close = True
    return base_config


def _apply_dot_params(base_cfg: MTCConfig, params: dict[str, float]) -> MTCConfig:
    cfg_dict = base_cfg.model_dump(by_alias=True)
    for key, value in params.items():
        node = cfg_dict
        parts = key.split(".")
        for part in parts[:-1]:
            node = node[part]
        node[parts[-1]] = value
    return MTCConfig.model_validate(cfg_dict)


def _latest_fine_csv() -> Path:
    files = sorted((PROJECT_ROOT / "optimize_results").glob("supertrend_atr_factor_fine_combined_*.csv"))
    if not files:
        raise FileNotFoundError("No fine-grid combined CSV found under optimize_results/")
    return files[-1]


def _load_candidates(csv_path: Path, top_n: int) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df[df["status"] == "OK"].copy()
    df = df.sort_values("score", ascending=False).head(top_n).reset_index(drop=True)
    df.insert(0, "in_sample_rank", range(1, len(df) + 1))
    return df


def _evaluate_candidate(
    *,
    df: pd.DataFrame,
    base_config: MTCConfig,
    atr_len: int,
    factor: float,
    eval_start: datetime,
    eval_end: datetime,
) -> dict[str, float]:
    params = {
        "supertrend.atr_len": int(atr_len),
        "supertrend.factor": float(factor),
    }
    cfg = _apply_dot_params(deepcopy(base_config), params)
    runner = MTCRunner(cfg)
    t0 = time.time()
    results = runner.run(
        df,
        warmup_bars=200,
        eval_start=eval_start,
        eval_end=eval_end,
    )
    metrics = results["metrics"]
    net_profit = float(metrics.get("net_profit", 0.0))
    max_drawdown = abs(
        float(metrics.get("max_drawdown_pct", metrics.get("max_drawdown", 0.0)))
    )
    holdout_score = net_profit if max_drawdown == 0 else net_profit / max_drawdown
    return {
        "holdout_score": holdout_score,
        "holdout_net_profit": net_profit,
        "holdout_max_dd_pct": max_drawdown,
        "holdout_total_trades": int(metrics.get("total_trades", 0)),
        "holdout_win_rate": float(metrics.get("win_rate", 0.0)),
        "holdout_profit_factor": float(metrics.get("profit_factor", 0.0)),
        "holdout_runtime_s": round(time.time() - t0, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate top fine-grid candidates on a holdout window.")
    parser.add_argument("--input", type=Path, default=None, help="Fine-grid combined CSV path. Defaults to latest.")
    parser.add_argument("--top-n", type=int, default=10, help="Number of in-sample candidates to evaluate.")
    args = parser.parse_args()

    input_csv = args.input.resolve() if args.input else _latest_fine_csv()
    top_n = max(1, int(args.top_n))
    df = _load_data()
    base_config = _load_base_config()
    holdout_start = datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc)
    holdout_end = datetime(2025, 6, 29, 23, 45, tzinfo=timezone.utc)
    candidates = _load_candidates(input_csv, top_n=top_n)

    print("\n-- Holdout Evaluation Setup --")
    print(f"  Input CSV       : {input_csv}")
    print(f"  Candidate Count : {len(candidates)}")
    print(f"  Holdout Window  : {holdout_start} -- {holdout_end}")
    print(f"  Parity Mode     : {base_config.parity.enabled}")
    print(f"  Terminal Close  : {base_config.parity.force_terminal_manual_close}")

    rows: list[dict[str, float | int | str]] = []
    for _, row in candidates.iterrows():
        atr_len = int(row["supertrend.atr_len"])
        factor = float(row["supertrend.factor"])
        print(
            f"  -> rank {int(row['in_sample_rank'])}: "
            f"ATR {atr_len} / F {factor:.1f}"
        )
        holdout = _evaluate_candidate(
            df=df,
            base_config=base_config,
            atr_len=atr_len,
            factor=factor,
            eval_start=holdout_start,
            eval_end=holdout_end,
        )
        out_row = {
            "in_sample_rank": int(row["in_sample_rank"]),
            "cluster": row["cluster"],
            "supertrend.atr_len": atr_len,
            "supertrend.factor": factor,
            "in_sample_score": float(row["score"]),
            "in_sample_net_profit": float(row["net_profit"]),
            "in_sample_max_dd_pct": float(row["max_dd_pct"]),
            "in_sample_total_trades": int(row["total_trades"]),
            "in_sample_win_rate": float(row["win_rate"]),
            "in_sample_profit_factor": float(row["profit_factor"]),
        }
        out_row.update(holdout)
        rows.append(out_row)

    out_dir = PROJECT_ROOT / "optimize_results"
    out_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    out_csv = out_dir / f"supertrend_atr_factor_fine_holdout_top{len(rows)}_{timestamp}.csv"
    out_xlsx = out_csv.with_suffix(".xlsx")

    out_df = pd.DataFrame(rows)
    out_df = out_df.sort_values(
        ["holdout_score", "holdout_net_profit", "holdout_profit_factor"],
        ascending=[False, False, False],
    ).reset_index(drop=True)
    out_df.insert(0, "holdout_rank", range(1, len(out_df) + 1))

    out_df.to_csv(out_csv, index=False)
    with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:
        out_df.to_excel(writer, index=False, sheet_name="holdout")

    print("\nHoldout evaluation complete")
    print(f"CSV : {out_csv}")
    print(f"XLSX: {out_xlsx}")
    print("\nTop holdout rows:")
    print(
        out_df[
            [
                "holdout_rank",
                "in_sample_rank",
                "cluster",
                "supertrend.atr_len",
                "supertrend.factor",
                "holdout_score",
                "holdout_net_profit",
                "holdout_max_dd_pct",
                "holdout_total_trades",
                "holdout_profit_factor",
            ]
        ].head(10).to_string(index=False)
    )


if __name__ == "__main__":
    main()
