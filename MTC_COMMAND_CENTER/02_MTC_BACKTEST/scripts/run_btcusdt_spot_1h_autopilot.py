from __future__ import annotations

import argparse
import csv
import json
import math
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPO_ROOT = PROJECT_ROOT.parent

DEFAULT_BASE_CASE = PROJECT_ROOT / "configs" / "cases" / "supertrend_1h_btcusdt_spot_overnight_20260312_202657.json"
DEFAULT_DATASET = REPO_ROOT / "110_" / "data" / "processed" / "binance" / "BTCUSDT" / "1h.parquet"
DEFAULT_SIGNAL_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_signal_broad_20260310.json"
DEFAULT_FILTERS_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_1h_filters_broad_20260312.json"
DEFAULT_TRADE_TIME_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_1h_trade_time_session_20260312.json"
DEFAULT_CONFIRM_GUARDS_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_1h_confirmation_guards_20260312.json"
DEFAULT_SL_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_sl_joint_20260310.json"
DEFAULT_TP_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_tp_joint_20260310.json"
DEFAULT_MULTI_TP_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_multi_tp_20260311.json"
DEFAULT_BE_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_be_20260310.json"
DEFAULT_TRAIL_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_trailing_20260310.json"
DEFAULT_MONEY_RISK_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_1h_money_risk_refine_20260312.json"

DEFAULT_EVAL_START = "2018-07-01T00:00:00"
DEFAULT_EVAL_END = "2025-01-01T00:00:00"
DEFAULT_HOLDOUT_START = "2025-01-01T00:00:00"
DEFAULT_HOLDOUT_END = "2026-03-12T18:00:00"

BASELINE_TEMPLATE_CASES = [
    PROJECT_ROOT / "configs" / "cases" / "supertrend_current_best_candidate_20260308.json",
    PROJECT_ROOT / "configs" / "cases" / "supertrend_sl_risk_current_best_candidate_20260309.json",
    PROJECT_ROOT / "configs" / "cases" / "supertrend_sl_risk_tp_current_best_candidate_20260309.json",
    PROJECT_ROOT / "configs" / "cases" / "supertrend_sl_risk_tp_be_current_best_candidate_20260309.json",
]

LEADERBOARD_COLUMNS = [
    "rank",
    "stage",
    "label",
    "selection_score",
    "full_net_profit",
    "full_net_profit_pct",
    "full_max_drawdown",
    "full_profit_factor",
    "full_total_trades",
    "holdout_net_profit",
    "holdout_net_profit_pct",
    "holdout_max_drawdown",
    "holdout_profit_factor",
    "holdout_total_trades",
    "walk_forward_net_sum",
    "walk_forward_profit_splits",
    "walk_forward_splits",
    "case_path",
    "source_artifact",
]

ROLLING_SPLITS = [
    {
        "label": "split01",
        "train_start": "2018-07-01T00:00:00",
        "train_end_exclusive": "2021-07-01T00:00:00",
        "test1_start": "2021-07-01T00:00:00",
        "test1_end_exclusive": "2022-01-01T00:00:00",
        "test2_start": "2022-01-01T00:00:00",
        "test2_end_exclusive": "2022-07-01T00:00:00",
    },
    {
        "label": "split02",
        "train_start": "2019-07-01T00:00:00",
        "train_end_exclusive": "2022-07-01T00:00:00",
        "test1_start": "2022-07-01T00:00:00",
        "test1_end_exclusive": "2023-01-01T00:00:00",
        "test2_start": "2023-01-01T00:00:00",
        "test2_end_exclusive": "2023-07-01T00:00:00",
    },
    {
        "label": "split03",
        "train_start": "2020-07-01T00:00:00",
        "train_end_exclusive": "2023-07-01T00:00:00",
        "test1_start": "2023-07-01T00:00:00",
        "test1_end_exclusive": "2024-01-01T00:00:00",
        "test2_start": "2024-01-01T00:00:00",
        "test2_end_exclusive": "2024-07-01T00:00:00",
    },
    {
        "label": "split04",
        "train_start": "2021-07-01T00:00:00",
        "train_end_exclusive": "2024-07-01T00:00:00",
        "test1_start": "2024-07-01T00:00:00",
        "test1_end_exclusive": "2025-01-01T00:00:00",
        "test2_start": "2025-01-01T00:00:00",
        "test2_end_exclusive": "2025-07-01T00:00:00",
    },
    {
        "label": "split05",
        "train_start": "2022-07-01T00:00:00",
        "train_end_exclusive": "2025-07-01T00:00:00",
        "test1_start": "2025-07-01T00:00:00",
        "test1_end_exclusive": "2026-01-01T00:00:00",
        "test2_start": "2026-01-01T00:00:00",
        "test2_end_exclusive": "2026-03-12T18:00:01",
    },
]


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path: str | Path, payload: dict[str, Any]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _append_line(path: str | Path, line: str) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as fh:
        fh.write(line.rstrip() + "\n")


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    if math.isnan(out) or math.isinf(out):
        return default
    return out


def _now_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _parse_iso(value: str) -> datetime:
    dt = datetime.fromisoformat(str(value).strip())
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _iso_no_tz(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds")


def _end_inclusive(end_exclusive: str) -> str:
    return _iso_no_tz(_parse_iso(end_exclusive) - timedelta(seconds=1))


def _slug(text: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in text)
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned.strip("_")


def _selection_sort_key(record: dict[str, Any]) -> tuple[int, float, int, float, float, float, float, float]:
    holdout = record.get("holdout_metrics") or {}
    wf = record.get("wf_summary") or {}
    full = record.get("full_metrics") or {}
    holdout_net = _safe_float(holdout.get("net_profit"), default=-1.0e18)
    wf_net = _safe_float(wf.get("net_sum"), default=-1.0e18)
    dd = _safe_float(
        holdout.get("max_drawdown"),
        default=_safe_float(holdout.get("max_drawdown_pct"), default=_safe_float(full.get("max_drawdown"), default=1.0e18)),
    )
    pf = _safe_float(holdout.get("profit_factor"), default=_safe_float(full.get("profit_factor"), default=0.0))
    trades = _safe_float(holdout.get("total_trades"), default=_safe_float(full.get("total_trades"), default=0.0))
    full_net = _safe_float(full.get("net_profit"), default=-1.0e18)
    return (
        1 if holdout_net > 0 else 0,
        holdout_net,
        1 if wf_net > 0 else 0,
        wf_net,
        -dd,
        pf,
        trades,
        full_net,
    )


def _selection_score(record: dict[str, Any]) -> float:
    holdout = record.get("holdout_metrics") or {}
    wf = record.get("wf_summary") or {}
    full = record.get("full_metrics") or {}
    holdout_net = _safe_float(holdout.get("net_profit"))
    wf_net = _safe_float(wf.get("net_sum"))
    dd = _safe_float(
        holdout.get("max_drawdown"),
        default=_safe_float(holdout.get("max_drawdown_pct"), default=_safe_float(full.get("max_drawdown"), default=100.0)),
    )
    pf = _safe_float(holdout.get("profit_factor"), default=_safe_float(full.get("profit_factor"), default=0.0))
    trades = _safe_float(holdout.get("total_trades"), default=_safe_float(full.get("total_trades"), default=0.0))
    bonus = 100000.0 if holdout_net > 0 else 0.0
    bonus += 10000.0 if wf_net > 0 else 0.0
    return round(bonus + holdout_net + wf_net - (dd * 20.0) + (pf * 100.0) + (trades * 0.1), 6)


def _metrics_from_results(results: dict[str, Any] | None) -> dict[str, Any] | None:
    if not results:
        return None
    metrics = results.get("metrics", {})
    if not isinstance(metrics, dict):
        return None
    return {
        "net_profit": metrics.get("net_profit"),
        "net_profit_pct": metrics.get("net_profit_pct"),
        "max_drawdown": metrics.get("max_drawdown"),
        "profit_factor": metrics.get("profit_factor"),
        "win_rate": metrics.get("win_rate"),
        "total_trades": metrics.get("total_trades"),
    }


def _load_case(path: str | Path) -> dict[str, Any]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid case payload: {path}")
    return payload


def _write_case(path: str | Path, payload: dict[str, Any]) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def _clone_case(
    *,
    source_case: Path,
    out_case: Path,
    dataset: str,
    start_date: str,
    end_date: str,
    comment: str,
) -> Path:
    case = _load_case(source_case)
    case["_comment"] = comment
    case["dataset"] = dataset.replace("\\", "/")
    case["start_date"] = start_date
    case["end_date"] = end_date
    meta = case.setdefault("_autopilot", {})
    meta["cloned_from_case"] = str(source_case.resolve()).replace("\\", "/")
    meta["cloned_at_utc"] = _now_utc()
    return _write_case(out_case, case)


def _run(
    cmd: list[str],
    *,
    cwd: Path,
    commands_log: Path,
    step: str,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    _append_line(commands_log, f"{_now_utc()} [{step}] {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=str(cwd), check=False, capture_output=capture, text=True)


def _run_checked(
    cmd: list[str],
    *,
    cwd: Path,
    commands_log: Path,
    step: str,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    result = _run(cmd, cwd=cwd, commands_log=commands_log, step=step, capture=capture)
    if result.returncode != 0:
        raise RuntimeError(
            f"{step} failed with exit code {result.returncode}: {' '.join(cmd)}\n"
            f"{result.stdout[-4000:]}\n{result.stderr[-4000:]}"
        )
    return result


def _materialize(
    *,
    base_case: Path,
    candidate: Path,
    out_case: Path,
    tag: str,
    commands_log: Path,
) -> Path:
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "materialize_candidate_case.py"),
        "--base-case",
        str(base_case),
        "--candidate",
        str(candidate),
        "--out-case",
        str(out_case),
        "--tag",
        tag,
    ]
    _run_checked(cmd, cwd=PROJECT_ROOT, commands_log=commands_log, step=f"materialize_{tag}")
    return out_case


def _backtest_case(
    *,
    case_path: Path,
    artifacts_dir: Path,
    commands_log: Path,
    step: str,
) -> dict[str, Any]:
    results_path = artifacts_dir / "results.json"
    if results_path.exists():
        return _read_json(results_path)
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "run_case.py"),
        str(case_path),
        "--artifacts-dir",
        str(artifacts_dir),
    ]
    _run_checked(cmd, cwd=PROJECT_ROOT, commands_log=commands_log, step=step)
    return _read_json(results_path)


def _window_optimize(
    *,
    base_case: Path,
    space_file: Path,
    mode: str,
    iters: int,
    seed: int,
    workers: int,
    min_trades_per_window: int,
    min_total_trades: int,
    min_profitable_windows: int,
    max_dd: float,
    top_k: int,
    outdir: Path,
    dataset: str,
    eval_start: str,
    eval_end: str,
    holdout_start: str,
    holdout_end: str,
    commands_log: Path,
    step: str,
) -> dict[str, Any]:
    summary_path = outdir / "summary.json"
    if summary_path.exists():
        summary = _read_json(summary_path)
        if summary.get("status") == "PASS":
            return summary
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "run_supertrend_windowed_optimization.py"),
        "--base-case",
        str(base_case),
        "--space-file",
        str(space_file),
        "--dataset",
        dataset,
        "--eval-start",
        eval_start,
        "--eval-end",
        eval_end,
        "--window-months",
        "6",
        "--require-full-windows",
        "--holdout-start",
        holdout_start,
        "--holdout-end",
        holdout_end,
        "--mode",
        mode,
        "--iters",
        str(iters),
        "--seed",
        str(seed),
        "--workers",
        str(workers),
        "--min-trades-per-window",
        str(min_trades_per_window),
        "--min-total-trades",
        str(min_total_trades),
        "--min-profitable-windows",
        str(min_profitable_windows),
        "--max-dd",
        str(max_dd),
        "--top-k",
        str(top_k),
        "--outdir",
        str(outdir),
    ]
    _run_checked(cmd, cwd=PROJECT_ROOT, commands_log=commands_log, step=step)
    return _read_json(summary_path)


def _candidate_path(summary: dict[str, Any], step: str) -> Path:
    if summary.get("status") != "PASS" or not summary.get("best_candidate_path"):
        raise RuntimeError(f"{step} did not produce a valid candidate")
    path = Path(str(summary["best_candidate_path"])).resolve()
    if not path.exists():
        raise RuntimeError(f"{step} candidate missing: {path}")
    return path


def _build_signal_refine_space(candidate_file: Path, out_path: Path) -> Path:
    candidate = _read_json(candidate_file)
    params = candidate.get("params", {})
    atr = int(params.get("supertrend.atr_len", 21))
    factor = float(params.get("supertrend.factor", 4.0))
    atr_low = max(5, atr - 5)
    atr_high = atr + 5
    factor_low = max(1.0, round(factor - 0.6, 2))
    factor_high = round(factor + 0.6, 2)
    steps = int(round((factor_high - factor_low) / 0.1))
    payload = {
        "grid": {
            "supertrend.atr_len": {
                "dtype": "int",
                "values": list(range(atr_low, atr_high + 1)),
            },
            "supertrend.factor": {
                "dtype": "float",
                "values": [round(factor_low + i * 0.1, 2) for i in range(steps + 1)],
            },
            "supertrend.use_wicks": {
                "values": [False, True],
            },
            "supertrend.use_ha": {
                "values": [False, True],
            },
        }
    }
    _write_json(out_path, payload)
    return out_path


def _get_dot(payload: dict[str, Any], key: str) -> Any:
    cur: Any = payload
    for part in key.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def _int_choices(key: str, value: int) -> list[int]:
    step = 1
    lowered = key.lower()
    if any(token in lowered for token in ("atr_len", "lookback", "ma_length", "ma_len", "smooth_len", "slope_len")):
        step = max(1, int(round(max(abs(value), 1) * 0.15)))
    elif any(token in lowered for token in ("bars", "timeout", "hold")):
        step = max(1, int(round(max(abs(value), 1) * 0.2)))
    values = {max(1, value - step), value, max(1, value + step)}
    return sorted(values)


def _float_choices(key: str, value: float) -> list[float]:
    lowered = key.lower()
    if "risk_long_percent" in lowered or "risk_short_percent" in lowered:
        step = 0.25
        low = 0.1
    elif "fallback_qty_pct" in lowered or "tp1_pct" in lowered:
        step = 5.0
        low = 1.0
    elif "max_leverage_cap" in lowered:
        step = 1.0
        low = 1.0
    elif any(token in lowered for token in ("percent", "_pct")):
        step = 0.25 if value <= 5 else 1.0
        low = 0.0
    elif any(token in lowered for token in ("factor", "mult", "rr", "buffer", "_k")):
        step = 0.1 if value < 1 else 0.25
        low = 0.0
    else:
        step = max(0.05, round(max(abs(value), 0.5) * 0.15, 2))
        low = 0.0
    values = {
        round(max(low, value - step), 4),
        round(value, 4),
        round(max(low, value + step), 4),
    }
    return sorted(values)


def _is_refinable_key(case: dict[str, Any], key: str) -> bool:
    cfg = case.get("config", {})
    if key.startswith("stop_loss.") and not bool(_get_dot(cfg, "stop_loss.use_sl")):
        return False
    if key.startswith("take_profit.") and not bool(_get_dot(cfg, "take_profit.use_tp")):
        return False
    if key.startswith("multi_tp.") and not bool(_get_dot(cfg, "multi_tp.use_multi_tp")):
        return False
    if key.startswith("break_even.") and not bool(_get_dot(cfg, "break_even.use_break_even")):
        return False
    if key.startswith("trailing.") and not bool(_get_dot(cfg, "trailing.use_trailing")):
        return False
    if key.startswith("filters.ma_") and not bool(_get_dot(cfg, "filters.use_ma_filter")):
        return False
    if key.startswith("filters.ma_slope") and not bool(_get_dot(cfg, "filters.use_ma_slope_filter")):
        return False
    if key.startswith("filters.vol_") and not bool(_get_dot(cfg, "filters.use_volume_filter")):
        return False
    if key.startswith("filters.atr_vol") and not bool(_get_dot(cfg, "filters.use_atr_vol_filter")):
        return False
    if key.startswith("filters.mcginley") and not bool(_get_dot(cfg, "filters.use_mcginley_filter")):
        return False
    if key.startswith("filters.htf_trend") and not bool(_get_dot(cfg, "filters.use_htf_trend_filter")):
        return False
    if key.startswith("filters.macd") and not bool(_get_dot(cfg, "filters.use_macd_filter")):
        return False
    if key.startswith("filters.range_") and not bool(_get_dot(cfg, "filters.use_range_regime_filter")):
        return False
    if key.startswith("confirmation.") and key not in {"confirmation.use_session_filter", "confirmation.session"}:
        if key.startswith("confirmation.use_momentum") or key.startswith("confirmation.momentum_") or key.startswith("confirmation.roc_") or key.startswith("confirmation.atr_"):
            return bool(_get_dot(cfg, "confirmation.enabled")) and bool(_get_dot(cfg, "confirmation.use_momentum"))
        return bool(_get_dot(cfg, "confirmation.enabled"))
    if key.startswith("time_stop.") and not bool(_get_dot(cfg, "time_stop.enabled")):
        return False
    return True


def _build_local_refine_space(
    *,
    case_path: Path,
    candidate_paths: list[Path],
    out_path: Path,
) -> Path | None:
    case = _load_case(case_path)
    cfg = case.get("config", {})
    touched: list[str] = []
    for candidate_path in candidate_paths:
        if not candidate_path.exists():
            continue
        params = _read_json(candidate_path).get("params", {})
        for key in params:
            if key not in touched:
                touched.append(str(key))
    random_space: dict[str, Any] = {}
    for key in touched:
        if not _is_refinable_key(case, key):
            continue
        value = _get_dot(cfg, key)
        if isinstance(value, bool) or isinstance(value, str) or value is None:
            continue
        if isinstance(value, int):
            values = _int_choices(key, value)
        elif isinstance(value, float):
            values = _float_choices(key, value)
        else:
            continue
        if len(values) <= 1:
            continue
        random_space[key] = {
            "dist": "choice",
            "values": values,
        }
    if not random_space:
        return None
    _write_json(out_path, {"random": random_space})
    return out_path


def _case_params_summary(case_path: Path) -> dict[str, Any]:
    case = _load_case(case_path)
    cfg = case.get("config", {})
    return {
        "signal_mode": cfg.get("signal_mode"),
        "supertrend": cfg.get("supertrend", {}),
        "trade": cfg.get("trade", {}),
        "stop_loss": cfg.get("stop_loss", {}),
        "take_profit": cfg.get("take_profit", {}),
        "multi_tp": cfg.get("multi_tp", {}),
        "break_even": cfg.get("break_even", {}),
        "trailing": cfg.get("trailing", {}),
        "risk": cfg.get("risk", {}),
        "filters": cfg.get("filters", {}),
        "confirmation": cfg.get("confirmation", {}),
        "guards": cfg.get("guards", {}),
        "strategy": cfg.get("strategy", {}),
    }


def _record_from_results(
    *,
    category: str,
    stage: str,
    label: str,
    case_path: Path,
    source_artifact: Path,
    full_results: dict[str, Any] | None,
    holdout_results: dict[str, Any] | None,
    window_summary: dict[str, Any] | None = None,
    best_candidate_path: Path | None = None,
    note: str = "",
) -> dict[str, Any]:
    return {
        "category": category,
        "stage": stage,
        "label": label,
        "status": "PASS",
        "case_path": str(case_path.resolve()).replace("\\", "/"),
        "source_artifact": str(source_artifact.resolve()).replace("\\", "/"),
        "full_metrics": _metrics_from_results(full_results),
        "holdout_metrics": _metrics_from_results(holdout_results),
        "window_summary": window_summary,
        "best_candidate_path": str(best_candidate_path.resolve()).replace("\\", "/") if best_candidate_path else None,
        "wf_summary": None,
        "params_summary": _case_params_summary(case_path),
        "note": note,
    }


def _load_dataset_end(dataset_path: Path) -> tuple[str, int]:
    cmd = [
        sys.executable,
        "-c",
        (
            "import pandas as pd, sys; "
            "df = pd.read_parquet(sys.argv[1]); "
            "print(len(df)); "
            "print(pd.Timestamp(df.index.max()).tz_convert('UTC').strftime('%Y-%m-%dT%H:%M:%S'))"
        ),
        str(dataset_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-4000:])
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return lines[-1], int(lines[0])


def _write_leaderboard(path: Path, records: list[dict[str, Any]]) -> None:
    ranked = sorted([record for record in records if record.get("status") == "PASS"], key=_selection_sort_key, reverse=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=LEADERBOARD_COLUMNS)
        writer.writeheader()
        for rank, record in enumerate(ranked, start=1):
            full = record.get("full_metrics") or {}
            holdout = record.get("holdout_metrics") or {}
            wf = record.get("wf_summary") or {}
            writer.writerow(
                {
                    "rank": rank,
                    "stage": record.get("stage"),
                    "label": record.get("label"),
                    "selection_score": _selection_score(record),
                    "full_net_profit": full.get("net_profit"),
                    "full_net_profit_pct": full.get("net_profit_pct"),
                    "full_max_drawdown": full.get("max_drawdown"),
                    "full_profit_factor": full.get("profit_factor"),
                    "full_total_trades": full.get("total_trades"),
                    "holdout_net_profit": holdout.get("net_profit"),
                    "holdout_net_profit_pct": holdout.get("net_profit_pct"),
                    "holdout_max_drawdown": holdout.get("max_drawdown", holdout.get("max_drawdown_pct")),
                    "holdout_profit_factor": holdout.get("profit_factor"),
                    "holdout_total_trades": holdout.get("total_trades"),
                    "walk_forward_net_sum": wf.get("net_sum"),
                    "walk_forward_profit_splits": wf.get("positive_splits"),
                    "walk_forward_splits": wf.get("total_splits"),
                    "case_path": record.get("case_path"),
                    "source_artifact": record.get("source_artifact"),
                }
            )


def _update_state(
    *,
    state_path: Path,
    run_root: Path,
    dataset: str,
    dataset_end: str,
    base_case: Path,
    records: list[dict[str, Any]],
    current_case: Path | None,
    status: str,
    current_step: str,
    selected_seed: str | None,
    error: str = "",
) -> None:
    _write_json(
        state_path,
        {
            "status": status,
            "updated_at": _now_utc(),
            "run_root": str(run_root.resolve()).replace("\\", "/"),
            "dataset": dataset.replace("\\", "/"),
            "dataset_end": dataset_end,
            "base_case": str(base_case.resolve()).replace("\\", "/"),
            "current_case": str(current_case.resolve()).replace("\\", "/") if current_case else None,
            "current_step": current_step,
            "selected_seed": selected_seed,
            "records": records,
            "leaderboard_path": str((run_root / "leaderboard.csv").resolve()).replace("\\", "/"),
            "journal_path": str((run_root / "journal.md").resolve()).replace("\\", "/"),
            "commands_log_path": str((run_root / "commands.log").resolve()).replace("\\", "/"),
            "final_handoff_path": str((run_root / "FINAL_HANDOFF.md").resolve()).replace("\\", "/"),
            "error": error,
        },
    )


def _write_handoff(path: Path, run_root: Path, records: list[dict[str, Any]], dataset_end: str, script_path: Path) -> None:
    ranked = sorted([record for record in records if record.get("status") == "PASS"], key=_selection_sort_key, reverse=True)
    if not ranked:
        path.write_text("# Final Handoff\n\nNo completed candidate yet.\n", encoding="utf-8")
        return
    best = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None
    third = ranked[2] if len(ranked) > 2 else None
    best_full = best.get("full_metrics") or {}
    best_holdout = best.get("holdout_metrics") or {}
    best_wf = best.get("wf_summary") or {}
    rerun_cmd = (
        f"python {script_path} --run-root {run_root} --base-case {DEFAULT_BASE_CASE} "
        f"--dataset {DEFAULT_DATASET} --eval-start {DEFAULT_EVAL_START} --eval-end {DEFAULT_EVAL_END} "
        f"--holdout-start {DEFAULT_HOLDOUT_START} --holdout-end {dataset_end}"
    )
    lines = [
        "# Final Handoff",
        "",
        f"- Recommended case: `{best.get('case_path')}`",
        f"- Source artifact: `{best.get('source_artifact')}`",
        f"- Rerun command: `{rerun_cmd}`",
        "",
        "## Recommended Metrics",
        "",
        f"- Full net profit: `{best_full.get('net_profit')}`",
        f"- Full net pct: `{best_full.get('net_profit_pct')}`",
        f"- Full max drawdown: `{best_full.get('max_drawdown')}`",
        f"- Full profit factor: `{best_full.get('profit_factor')}`",
        f"- Full trades: `{best_full.get('total_trades')}`",
        f"- Holdout net profit: `{best_holdout.get('net_profit')}`",
        f"- Holdout net pct: `{best_holdout.get('net_profit_pct')}`",
        f"- Holdout max drawdown: `{best_holdout.get('max_drawdown')}`",
        f"- Holdout profit factor: `{best_holdout.get('profit_factor')}`",
        f"- Holdout trades: `{best_holdout.get('total_trades')}`",
        "",
        "## Walk-Forward Summary",
        "",
        f"- Net sum: `{best_wf.get('net_sum')}`",
        f"- Positive splits: `{best_wf.get('positive_splits')}` / `{best_wf.get('total_splits')}`",
        f"- Worst test drawdown: `{best_wf.get('worst_test_dd')}`",
        f"- Test trades total: `{best_wf.get('test_total_trades')}`",
        "",
        "## Active Modules / Params",
        "",
        "```json",
        json.dumps(best.get("params_summary") or {}, indent=2, ensure_ascii=False),
        "```",
        "",
        "## Why Selected",
        "",
        "- Ranked first by positive holdout net, then walk-forward net sum, then drawdown / PF / trade count.",
        "",
        "## Alternatives",
        "",
    ]
    for alt in (second, third):
        if alt is None:
            continue
        alt_full = alt.get("full_metrics") or {}
        alt_holdout = alt.get("holdout_metrics") or {}
        alt_wf = alt.get("wf_summary") or {}
        lines.append(
            f"- `{alt.get('label')}` -> case `{alt.get('case_path')}` | holdout `{alt_holdout.get('net_profit')}` | wf `{alt_wf.get('net_sum')}` | full `{alt_full.get('net_profit')}`"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _stage_record_from_summary(
    *,
    stage: str,
    case_path: Path,
    summary: dict[str, Any],
    full_results: dict[str, Any],
) -> dict[str, Any]:
    holdout_metrics = dict((summary.get("holdout_result") or {}).get("metrics") or {})
    if "max_drawdown" not in holdout_metrics and "max_drawdown_pct" in holdout_metrics:
        holdout_metrics["max_drawdown"] = holdout_metrics.get("max_drawdown_pct")
    return {
        "category": "stage",
        "stage": stage,
        "label": stage,
        "status": "PASS",
        "case_path": str(case_path.resolve()).replace("\\", "/"),
        "source_artifact": str((Path(summary["outdir"]).resolve() / "summary.json")).replace("\\", "/"),
        "full_metrics": _metrics_from_results(full_results),
        "holdout_metrics": holdout_metrics,
        "window_summary": {
            "outdir": summary.get("outdir"),
            "best_candidate_path": summary.get("best_candidate_path"),
            "best_score": summary.get("best_score"),
            "best_metrics": summary.get("best_metrics"),
            "windows": summary.get("windows"),
            "ok_trials": summary.get("ok_trials"),
            "scheduled_trials": summary.get("scheduled_trials"),
        },
        "best_candidate_path": summary.get("best_candidate_path"),
        "wf_summary": None,
        "params_summary": _case_params_summary(case_path),
        "note": "",
    }


def _run_baselines(
    *,
    run_root: Path,
    dataset: str,
    full_start: str,
    full_end: str,
    holdout_start: str,
    holdout_end: str,
    commands_log: Path,
    journal_path: Path,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    baseline_dir = run_root / "cases" / "baselines"
    eval_dir = run_root / "evaluations" / "baselines"
    baseline_dir.mkdir(parents=True, exist_ok=True)
    eval_dir.mkdir(parents=True, exist_ok=True)

    spot_base_case = baseline_dir / "spot_base_full.json"
    if not spot_base_case.exists():
        _clone_case(
            source_case=DEFAULT_BASE_CASE,
            out_case=spot_base_case,
            dataset=dataset,
            start_date=full_start,
            end_date=full_end,
            comment="Spot BTCUSDT 1h naked baseline for autopilot.",
        )
    spot_holdout_case = baseline_dir / "spot_base_holdout.json"
    if not spot_holdout_case.exists():
        _clone_case(
            source_case=DEFAULT_BASE_CASE,
            out_case=spot_holdout_case,
            dataset=dataset,
            start_date=holdout_start,
            end_date=holdout_end,
            comment="Spot BTCUSDT 1h naked holdout baseline for autopilot.",
        )
    full_results = _backtest_case(case_path=spot_base_case, artifacts_dir=eval_dir / "spot_base_full", commands_log=commands_log, step="baseline_spot_base_full")
    holdout_results = _backtest_case(case_path=spot_holdout_case, artifacts_dir=eval_dir / "spot_base_holdout", commands_log=commands_log, step="baseline_spot_base_holdout")
    records.append(
        _record_from_results(
            category="baseline",
            stage="baseline",
            label="baseline_spot_base",
            case_path=spot_base_case,
            source_artifact=eval_dir / "spot_base_full" / "results.json",
            full_results=full_results,
            holdout_results=holdout_results,
            note="Spot naked/base case",
        )
    )
    _append_line(journal_path, f"- {_now_utc()} baseline_spot_base completed")

    for template_case in BASELINE_TEMPLATE_CASES:
        label = f"baseline_{template_case.stem}"
        full_case = baseline_dir / f"{template_case.stem}_full.json"
        holdout_case = baseline_dir / f"{template_case.stem}_holdout.json"
        if not full_case.exists():
            _clone_case(
                source_case=template_case,
                out_case=full_case,
                dataset=dataset,
                start_date=full_start,
                end_date=full_end,
                comment=f"Spot clone of {template_case.name} full-period baseline.",
            )
        if not holdout_case.exists():
            _clone_case(
                source_case=template_case,
                out_case=holdout_case,
                dataset=dataset,
                start_date=holdout_start,
                end_date=holdout_end,
                comment=f"Spot clone of {template_case.name} holdout baseline.",
            )
        full_results = _backtest_case(case_path=full_case, artifacts_dir=eval_dir / f"{template_case.stem}_full", commands_log=commands_log, step=f"{label}_full")
        holdout_results = _backtest_case(case_path=holdout_case, artifacts_dir=eval_dir / f"{template_case.stem}_holdout", commands_log=commands_log, step=f"{label}_holdout")
        records.append(
            _record_from_results(
                category="baseline",
                stage="baseline",
                label=label,
                case_path=full_case,
                source_artifact=eval_dir / f"{template_case.stem}_full" / "results.json",
                full_results=full_results,
                holdout_results=holdout_results,
                note=f"Spot clone of {template_case.name}",
            )
        )
        _append_line(journal_path, f"- {_now_utc()} {label} completed")
    return records


def _run_explicit_walk_forward(
    *,
    case_path: Path,
    label: str,
    run_root: Path,
    dataset: str,
    commands_log: Path,
) -> dict[str, Any]:
    wf_root = run_root / "wf" / _slug(label)
    summary_path = wf_root / "summary.json"
    if summary_path.exists():
        return _read_json(summary_path)
    wf_root.mkdir(parents=True, exist_ok=True)
    split_rows: list[dict[str, Any]] = []
    for split in ROLLING_SPLITS:
        split_dir = wf_root / split["label"]
        case_dir = split_dir / "cases"
        eval_dir = split_dir / "eval"
        case_dir.mkdir(parents=True, exist_ok=True)
        eval_dir.mkdir(parents=True, exist_ok=True)
        train_case = _clone_case(source_case=case_path, out_case=case_dir / "train.json", dataset=dataset, start_date=split["train_start"], end_date=_end_inclusive(split["train_end_exclusive"]), comment=f"{label} {split['label']} train replay")
        test1_case = _clone_case(source_case=case_path, out_case=case_dir / "test1.json", dataset=dataset, start_date=split["test1_start"], end_date=_end_inclusive(split["test1_end_exclusive"]), comment=f"{label} {split['label']} test1 replay")
        test2_case = _clone_case(source_case=case_path, out_case=case_dir / "test2.json", dataset=dataset, start_date=split["test2_start"], end_date=_end_inclusive(split["test2_end_exclusive"]), comment=f"{label} {split['label']} test2 replay")
        train_results = _backtest_case(case_path=train_case, artifacts_dir=eval_dir / "train", commands_log=commands_log, step=f"wf_{label}_{split['label']}_train")
        test1_results = _backtest_case(case_path=test1_case, artifacts_dir=eval_dir / "test1", commands_log=commands_log, step=f"wf_{label}_{split['label']}_test1")
        test2_results = _backtest_case(case_path=test2_case, artifacts_dir=eval_dir / "test2", commands_log=commands_log, step=f"wf_{label}_{split['label']}_test2")
        test1_metrics = _metrics_from_results(test1_results) or {}
        test2_metrics = _metrics_from_results(test2_results) or {}
        split_rows.append(
            {
                "label": split["label"],
                "train_metrics": _metrics_from_results(train_results),
                "test1_metrics": test1_metrics,
                "test2_metrics": test2_metrics,
                "test_net_sum": _safe_float(test1_metrics.get("net_profit")) + _safe_float(test2_metrics.get("net_profit")),
                "test_max_dd": max(_safe_float(test1_metrics.get("max_drawdown")), _safe_float(test2_metrics.get("max_drawdown"))),
                "test_trade_sum": int(_safe_float(test1_metrics.get("total_trades")) + _safe_float(test2_metrics.get("total_trades"))),
            }
        )
    net_sum = sum(_safe_float(row.get("test_net_sum")) for row in split_rows)
    positive_splits = sum(1 for row in split_rows if _safe_float(row.get("test_net_sum")) > 0)
    worst_dd = max((_safe_float(row.get("test_max_dd")) for row in split_rows), default=0.0)
    total_trades = sum(int(row.get("test_trade_sum", 0)) for row in split_rows)
    payload = {
        "status": "PASS",
        "label": label,
        "case_path": str(case_path.resolve()).replace("\\", "/"),
        "net_sum": round(net_sum, 6),
        "positive_splits": positive_splits,
        "total_splits": len(split_rows),
        "worst_test_dd": round(worst_dd, 6),
        "test_total_trades": total_trades,
        "splits": split_rows,
    }
    _write_json(summary_path, payload)
    return payload


def main() -> int:
    ap = argparse.ArgumentParser(description="Spot BTCUSDT 1h staged overnight autopilot.")
    ap.add_argument("--run-root", required=True)
    ap.add_argument("--base-case", default=str(DEFAULT_BASE_CASE))
    ap.add_argument("--dataset", default=str(DEFAULT_DATASET))
    ap.add_argument("--eval-start", default=DEFAULT_EVAL_START)
    ap.add_argument("--eval-end", default=DEFAULT_EVAL_END)
    ap.add_argument("--holdout-start", default=DEFAULT_HOLDOUT_START)
    ap.add_argument("--holdout-end", default=DEFAULT_HOLDOUT_END)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) - 2))
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--signal-iters", type=int, default=1400)
    ap.add_argument("--filters-iters", type=int, default=1800)
    ap.add_argument("--trade-time-iters", type=int, default=1200)
    ap.add_argument("--confirm-iters", type=int, default=1600)
    ap.add_argument("--sl-iters", type=int, default=1800)
    ap.add_argument("--tp-iters", type=int, default=1200)
    ap.add_argument("--mtp-iters", type=int, default=800)
    ap.add_argument("--money-iters", type=int, default=1000)
    ap.add_argument("--local-iters", type=int, default=800)
    ap.add_argument("--top-k", type=int, default=48)
    args = ap.parse_args()

    run_root = Path(args.run_root).resolve()
    run_root.mkdir(parents=True, exist_ok=True)
    for subdir in ("cases", "spaces", "runs", "evaluations", "wf"):
        (run_root / subdir).mkdir(parents=True, exist_ok=True)

    state_path = run_root / "state.json"
    leaderboard_path = run_root / "leaderboard.csv"
    journal_path = run_root / "journal.md"
    commands_log = run_root / "commands.log"
    handoff_path = run_root / "FINAL_HANDOFF.md"

    base_case = Path(args.base_case).resolve()
    dataset = str(Path(args.dataset).resolve()).replace("\\", "/")
    dataset_end, dataset_rows = _load_dataset_end(Path(args.dataset))

    records: list[dict[str, Any]] = []
    current_case = base_case
    selected_seed: str | None = None
    stage_candidate_paths: list[Path] = []

    _append_line(journal_path, f"- {_now_utc()} autopilot start | dataset_rows={dataset_rows} | dataset_end={dataset_end}")
    _update_state(state_path=state_path, run_root=run_root, dataset=dataset, dataset_end=dataset_end, base_case=base_case, records=records, current_case=current_case, status="RUNNING", current_step="baselines", selected_seed=selected_seed)

    baseline_records = _run_baselines(run_root=run_root, dataset=dataset, full_start=args.eval_start, full_end=dataset_end, holdout_start=args.holdout_start, holdout_end=args.holdout_end, commands_log=commands_log, journal_path=journal_path)
    records.extend(baseline_records)
    if baseline_records:
        selected_seed = sorted(baseline_records, key=_selection_sort_key, reverse=True)[0]["label"]
    _write_leaderboard(leaderboard_path, records)
    _write_handoff(handoff_path, run_root, records, dataset_end, Path(__file__).resolve())
    _update_state(state_path=state_path, run_root=run_root, dataset=dataset, dataset_end=dataset_end, base_case=base_case, records=records, current_case=current_case, status="RUNNING", current_step="stages", selected_seed=selected_seed)

    stage_specs = [
        {"stage": "signal_broad", "space": DEFAULT_SIGNAL_SPACE, "mode": "random", "iters": args.signal_iters, "seed": args.seed, "thresholds": (3, 150, 6, 65.0)},
        {"stage": "signal_refine", "space": None, "mode": "grid", "iters": 0, "seed": args.seed + 50, "thresholds": (3, 150, 6, 65.0)},
        {"stage": "filters_broad", "space": DEFAULT_FILTERS_SPACE, "mode": "random", "iters": args.filters_iters, "seed": args.seed + 100, "thresholds": (2, 120, 6, 55.0)},
        {"stage": "trade_time_session", "space": DEFAULT_TRADE_TIME_SPACE, "mode": "random", "iters": args.trade_time_iters, "seed": args.seed + 130, "thresholds": (2, 100, 6, 50.0)},
        {"stage": "confirmation_guards", "space": DEFAULT_CONFIRM_GUARDS_SPACE, "mode": "random", "iters": args.confirm_iters, "seed": args.seed + 150, "thresholds": (1, 80, 5, 45.0)},
        {"stage": "sl_joint", "space": DEFAULT_SL_SPACE, "mode": "random", "iters": args.sl_iters, "seed": args.seed + 200, "thresholds": (1, 70, 5, 40.0)},
        {"stage": "tp_joint", "space": DEFAULT_TP_SPACE, "mode": "random", "iters": args.tp_iters, "seed": args.seed + 300, "thresholds": (1, 60, 5, 40.0)},
        {"stage": "multi_tp_joint", "space": DEFAULT_MULTI_TP_SPACE, "mode": "random", "iters": args.mtp_iters, "seed": args.seed + 350, "thresholds": (1, 50, 5, 40.0)},
        {"stage": "be_grid", "space": DEFAULT_BE_SPACE, "mode": "grid", "iters": 0, "seed": args.seed + 400, "thresholds": (1, 50, 5, 40.0)},
        {"stage": "trailing_grid", "space": DEFAULT_TRAIL_SPACE, "mode": "grid", "iters": 0, "seed": args.seed + 500, "thresholds": (1, 50, 5, 40.0)},
        {"stage": "money_risk_refine", "space": DEFAULT_MONEY_RISK_SPACE, "mode": "random", "iters": args.money_iters, "seed": args.seed + 550, "thresholds": (1, 50, 5, 35.0)},
        {"stage": "top_candidate_local_refine", "space": None, "mode": "random", "iters": args.local_iters, "seed": args.seed + 600, "thresholds": (1, 50, 5, 35.0)},
    ]

    signal_candidate_path: Path | None = None
    for spec in stage_specs:
        stage = str(spec["stage"])
        _append_line(journal_path, f"- {_now_utc()} stage_start {stage}")
        _update_state(state_path=state_path, run_root=run_root, dataset=dataset, dataset_end=dataset_end, base_case=base_case, records=records, current_case=current_case, status="RUNNING", current_step=stage, selected_seed=selected_seed)
        try:
            run_dir = run_root / "runs" / stage
            case_out = run_root / "cases" / f"{stage}_full.json"
            eval_out = run_root / "evaluations" / f"{stage}_full"
            if stage == "signal_refine":
                if signal_candidate_path is None:
                    raise RuntimeError("signal_refine requires signal_broad candidate")
                space_file = _build_signal_refine_space(signal_candidate_path, run_root / "spaces" / "signal_refine.json")
            elif stage == "top_candidate_local_refine":
                space_file = _build_local_refine_space(case_path=current_case, candidate_paths=stage_candidate_paths, out_path=run_root / "spaces" / "top_candidate_local_refine.json")
                if space_file is None:
                    _append_line(journal_path, f"- {_now_utc()} stage_skip {stage} no refinable numeric params")
                    continue
            else:
                space_file = Path(spec["space"]).resolve() if spec["space"] is not None else None
            if space_file is None:
                _append_line(journal_path, f"- {_now_utc()} stage_skip {stage} no space")
                continue

            min_window, min_total, min_profitable, max_dd = spec["thresholds"]
            summary = _window_optimize(base_case=current_case, space_file=space_file, mode=str(spec["mode"]), iters=int(spec["iters"]), seed=int(spec["seed"]), workers=args.workers, min_trades_per_window=min_window, min_total_trades=min_total, min_profitable_windows=min_profitable, max_dd=max_dd, top_k=args.top_k, outdir=run_dir, dataset=dataset, eval_start=args.eval_start, eval_end=args.eval_end, holdout_start=args.holdout_start, holdout_end=args.holdout_end, commands_log=commands_log, step=f"window_{stage}")
            if summary.get("status") != "PASS":
                summary = _window_optimize(base_case=current_case, space_file=space_file, mode=str(spec["mode"]), iters=int(spec["iters"]), seed=int(spec["seed"]) + 1, workers=args.workers, min_trades_per_window=max(1, min_window - 1), min_total_trades=max(20, int(min_total * 0.75)), min_profitable_windows=max(3, min_profitable - 1), max_dd=max_dd + 10.0, top_k=args.top_k, outdir=run_root / "runs" / f"{stage}_retry", dataset=dataset, eval_start=args.eval_start, eval_end=args.eval_end, holdout_start=args.holdout_start, holdout_end=args.holdout_end, commands_log=commands_log, step=f"window_{stage}_retry")
            if summary.get("status") != "PASS":
                _append_line(journal_path, f"- {_now_utc()} stage_empty {stage}")
                continue

            candidate_path = _candidate_path(summary, stage)
            if stage == "signal_broad":
                signal_candidate_path = candidate_path
            stage_candidate_paths.append(candidate_path)
            current_case = _materialize(base_case=current_case, candidate=candidate_path, out_case=case_out, tag=stage, commands_log=commands_log)
            full_results = _backtest_case(case_path=current_case, artifacts_dir=eval_out, commands_log=commands_log, step=f"{stage}_full_backtest")
            records.append(_stage_record_from_summary(stage=stage, case_path=current_case, summary=summary, full_results=full_results))
            record = records[-1]
            _append_line(journal_path, f"- {_now_utc()} stage_done {stage} | holdout_net={(record.get('holdout_metrics') or {}).get('net_profit')} | full_net={(record.get('full_metrics') or {}).get('net_profit')}")
            _write_leaderboard(leaderboard_path, records)
            _write_handoff(handoff_path, run_root, records, dataset_end, Path(__file__).resolve())
            _update_state(state_path=state_path, run_root=run_root, dataset=dataset, dataset_end=dataset_end, base_case=base_case, records=records, current_case=current_case, status="RUNNING", current_step=stage, selected_seed=selected_seed)
        except Exception as exc:
            _append_line(journal_path, f"- {_now_utc()} stage_fail {stage} | {exc}")
            _update_state(state_path=state_path, run_root=run_root, dataset=dataset, dataset_end=dataset_end, base_case=base_case, records=records, current_case=current_case, status="RUNNING", current_step=stage, selected_seed=selected_seed, error=str(exc))
            continue

    ranked = sorted([record for record in records if record.get("status") == "PASS"], key=_selection_sort_key, reverse=True)
    for record in ranked[:3]:
        wf_summary = _run_explicit_walk_forward(case_path=Path(str(record["case_path"])), label=str(record["label"]), run_root=run_root, dataset=dataset, commands_log=commands_log)
        record["wf_summary"] = wf_summary
        _append_line(journal_path, f"- {_now_utc()} wf_done {record['label']} | net_sum={wf_summary.get('net_sum')}")

    _write_leaderboard(leaderboard_path, records)
    _write_handoff(handoff_path, run_root, records, dataset_end, Path(__file__).resolve())
    _update_state(state_path=state_path, run_root=run_root, dataset=dataset, dataset_end=dataset_end, base_case=base_case, records=records, current_case=current_case, status="PASS", current_step="complete", selected_seed=selected_seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
