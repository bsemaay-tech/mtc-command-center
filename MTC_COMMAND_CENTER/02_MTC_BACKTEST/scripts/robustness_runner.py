#!/usr/bin/env python
"""
Robustness validation runner.

Runs deterministic robustness checks around a candidate:
1) Optional walk-forward workflow (delegates to scripts/walk_forward_validate.py)
2) Regime split evaluation on full-run trades (auto-labeled or manual windows)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner
from src.workflow.artifacts import (
    build_manifest,
    ensure_dir,
    render_simple_report,
    sha256_file,
    write_manifest,
    write_report,
    write_results,
)


def _parse_dt(raw: str) -> datetime:
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        dt = datetime.strptime(raw, "%Y-%m-%d")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt


def _load_case(case_path: Path) -> tuple[dict[str, Any], MTCConfig]:
    payload = json.loads(case_path.read_text(encoding="utf-8"))
    cfg = MTCConfig.model_validate(payload.get("config", {}))
    return payload, cfg


def _load_dataset(dataset_name: str) -> pd.DataFrame:
    ds = (PROJECT_ROOT / "data" / dataset_name).resolve()
    if ds.suffix == ".parquet":
        df = pd.read_parquet(ds)
    else:
        df = pd.read_csv(ds)
    if pd.api.types.is_numeric_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    else:
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    else:
        df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")
    return df


def _apply_dot_params(base_cfg: MTCConfig, params: dict[str, Any]) -> MTCConfig:
    # Use alias keys so optimizer/exported param paths such as
    # `break_even.use_break_even` or `stop_loss.use_sl` resolve correctly.
    d = base_cfg.model_dump(by_alias=True)
    for key, val in params.items():
        node = d
        parts = key.split(".")
        for part in parts[:-1]:
            if part not in node or not isinstance(node[part], dict):
                raise KeyError(f"Invalid param path: {key}")
            node = node[part]
        node[parts[-1]] = val
    return MTCConfig.model_validate(d)


def _run_backtest(case_payload: dict[str, Any], cfg: MTCConfig) -> tuple[dict[str, Any], pd.DataFrame]:
    df = _load_dataset(case_payload["dataset"])
    start_dt = _parse_dt(str(case_payload["start_date"]))
    end_dt = _parse_dt(str(case_payload["end_date"]))
    preroll_days = int(case_payload.get("preroll_days", 90))
    warmup_bars = int(case_payload.get("warmup_bars", 200))

    filter_start = start_dt - pd.Timedelta(days=preroll_days) if preroll_days > 0 else start_dt
    df_filtered = df[(df["timestamp"] >= filter_start) & (df["timestamp"] <= end_dt)].copy().reset_index(drop=True)

    runner = MTCRunner(cfg)
    results = runner.run(
        df_filtered,
        warmup_bars=warmup_bars,
        eval_start=start_dt if preroll_days > 0 else None,
        eval_end=end_dt,
    )

    df_eval = df[(df["timestamp"] >= start_dt) & (df["timestamp"] <= end_dt)].copy().reset_index(drop=True)
    return results, df_eval


def _auto_label_regimes(df_eval: pd.DataFrame) -> pd.DataFrame:
    out = df_eval[["timestamp", "close"]].copy()
    out["ret_abs"] = out["close"].pct_change().abs().fillna(0.0)
    out["vol"] = out["ret_abs"].rolling(48, min_periods=12).mean().fillna(0.0)
    out["ma"] = out["close"].rolling(48, min_periods=12).mean()
    out["trend_strength"] = (out["ma"].diff().abs() / out["close"]).fillna(0.0)

    vol_q = float(out["vol"].quantile(0.67))
    trend_q = float(out["trend_strength"].quantile(0.67))

    labels = []
    for _, row in out.iterrows():
        if row["vol"] >= vol_q:
            labels.append("HIGH_VOL")
        elif row["trend_strength"] >= trend_q:
            labels.append("TREND")
        else:
            labels.append("RANGE")
    out["regime"] = labels
    return out[["timestamp", "regime"]]


def _manual_label_regimes(df_eval: pd.DataFrame, regime_file: Path) -> pd.DataFrame:
    payload = json.loads(regime_file.read_text(encoding="utf-8"))
    windows = payload.get("windows", [])
    if not windows:
        raise ValueError("Regime file must contain windows[]")

    out = df_eval[["timestamp"]].copy()
    out["regime"] = "UNLABELED"
    for w in windows:
        s = _parse_dt(str(w["start"]))
        e = _parse_dt(str(w["end"]))
        label = str(w["label"])
        mask = (out["timestamp"] >= s) & (out["timestamp"] <= e)
        out.loc[mask, "regime"] = label
    return out


def _regime_eval(trades: list[Any], labels_df: pd.DataFrame) -> pd.DataFrame:
    label_map = pd.Series(labels_df["regime"].values, index=labels_df["timestamp"]).to_dict()

    agg: dict[str, dict[str, float]] = defaultdict(lambda: {"trades": 0, "wins": 0, "net_profit": 0.0})
    for t in trades:
        et = getattr(t, "entry_time", None)
        pnl = float(getattr(t, "pnl", 0.0))
        if et is None:
            regime = "UNLABELED"
        else:
            regime = label_map.get(et, "UNLABELED")
        agg[regime]["trades"] += 1
        agg[regime]["wins"] += 1 if pnl > 0 else 0
        agg[regime]["net_profit"] += pnl

    rows = []
    for regime, vals in sorted(agg.items()):
        trades_n = int(vals["trades"])
        win_rate = (100.0 * vals["wins"] / trades_n) if trades_n > 0 else 0.0
        rows.append(
            {
                "regime": regime,
                "trades": trades_n,
                "win_rate": round(win_rate, 4),
                "net_profit": round(float(vals["net_profit"]), 6),
            }
        )
    return pd.DataFrame(rows)


def _maybe_run_walkforward(args: argparse.Namespace, outdir: Path) -> dict[str, Any]:
    if not args.run_walkforward:
        return {"enabled": False}

    if not (args.train_case and args.target_case_1 and args.target_case_2):
        raise ValueError("--run-walkforward requires --train-case, --target-case-1, --target-case-2")

    wf_dir = ensure_dir(outdir / "walkforward")
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "walk_forward_validate.py"),
        "--train-case",
        str(args.train_case),
        "--target-case-1",
        str(args.target_case_1),
        "--target-case-2",
        str(args.target_case_2),
        "--iters",
        str(args.wf_iters),
        "--seed",
        str(args.seed),
        "--workers",
        str(args.workers),
        "--outdir",
        str(wf_dir),
    ]
    p = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True)
    return {
        "enabled": True,
        "status": "PASS" if p.returncode == 0 else "FAIL",
        "return_code": p.returncode,
        "stdout": p.stdout,
        "stderr": p.stderr,
        "outdir": str(wf_dir),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Run robustness validation bundle.")
    ap.add_argument("--case", required=True, help="Base case JSON")
    ap.add_argument("--candidate", required=True, help="Candidate JSON with params")
    ap.add_argument("--outdir", required=True, help="Output directory")
    ap.add_argument("--regime-file", default="", help="Optional manual regime windows JSON")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--workers", type=int, default=1)

    ap.add_argument("--run-walkforward", action="store_true")
    ap.add_argument("--train-case", default="")
    ap.add_argument("--target-case-1", default="")
    ap.add_argument("--target-case-2", default="")
    ap.add_argument("--wf-iters", type=int, default=200)
    args = ap.parse_args()

    case_path = (PROJECT_ROOT / args.case).resolve() if not Path(args.case).is_absolute() else Path(args.case).resolve()
    candidate_path = (PROJECT_ROOT / args.candidate).resolve() if not Path(args.candidate).is_absolute() else Path(args.candidate).resolve()
    outdir = ensure_dir(Path(args.outdir).resolve())

    case_payload, base_cfg = _load_case(case_path)
    cand_payload = json.loads(candidate_path.read_text(encoding="utf-8"))
    params = cand_payload.get("params", {})
    merged_cfg = _apply_dot_params(base_cfg, params)

    results, df_eval = _run_backtest(case_payload, merged_cfg)

    if args.regime_file:
        regime_path = (PROJECT_ROOT / args.regime_file).resolve() if not Path(args.regime_file).is_absolute() else Path(args.regime_file).resolve()
        labels_df = _manual_label_regimes(df_eval, regime_path)
        regime_source = "manual"
    else:
        labels_df = _auto_label_regimes(df_eval)
        regime_source = "auto_vol_trend_quantile"

    trades = results.get("trades", [])
    regime_df = _regime_eval(trades, labels_df)
    regime_csv = outdir / "regime_eval.csv"
    regime_df.to_csv(regime_csv, index=False)

    walkforward = _maybe_run_walkforward(args, outdir)

    status = "PASS"
    if walkforward.get("enabled") and walkforward.get("status") != "PASS":
        status = "FAIL"

    run_id = f"robustness_{case_path.stem}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%SZ')}"
    manifest = build_manifest(
        project_root=PROJECT_ROOT,
        run_type="robustness",
        run_id=run_id,
        case_file=case_path,
        dataset_file=(PROJECT_ROOT / "data" / case_payload["dataset"]).resolve(),
        start_date=str(case_payload.get("start_date", "")),
        end_date=str(case_payload.get("end_date", "")),
        config_obj=merged_cfg,
        seed=args.seed,
        workers=args.workers,
        extra={
            "candidate_file": str(candidate_path),
            "candidate_hash": sha256_file(candidate_path),
            "regime_source": regime_source,
        },
    )
    mpath = write_manifest(outdir, manifest)

    payload = {
        "run_id": run_id,
        "run_type": "robustness",
        "status": status,
        "case": str(case_path),
        "candidate": str(candidate_path),
        "metrics": results.get("metrics", {}),
        "regime_source": regime_source,
        "regime_eval_csv": str(regime_csv),
        "walkforward": walkforward,
        "artifacts": {
            "manifest": str(mpath),
            "regime_eval_csv": str(regime_csv),
        },
    }
    rpath = write_results(outdir, payload)

    repath = write_report(
        outdir,
        render_simple_report(
            title="Robustness Validation Report",
            run_id=run_id,
            status=status,
            key_values={
                "case": case_path,
                "candidate": candidate_path,
                "regime_source": regime_source,
                "total_trades": results.get("metrics", {}).get("total_trades", ""),
                "net_profit": results.get("metrics", {}).get("net_profit", ""),
                "max_dd_pct": results.get("metrics", {}).get("max_drawdown", ""),
                "walkforward_status": walkforward.get("status", "DISABLED") if walkforward.get("enabled") else "DISABLED",
            },
            artifact_paths={
                "manifest": str(mpath),
                "results": str(rpath),
                "regime_eval_csv": str(regime_csv),
            },
        ),
    )

    payload["artifacts"]["results"] = str(rpath)
    payload["artifacts"]["report"] = str(repath)
    write_results(outdir, payload)

    print(f"robustness_status={status}")
    print(f"outdir={outdir}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
