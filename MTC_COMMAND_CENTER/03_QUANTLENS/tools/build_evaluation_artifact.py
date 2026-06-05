"""
build_evaluation_artifact.py — SP-004 Phase 1
Pure builder: reads MEGA/CPCV/PBO dicts, writes evaluation-artifact JSON files.
NO backtest reruns, NO Pine/parity/MTC logic, NO git/commit.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Status-envelope helpers
# ---------------------------------------------------------------------------

def _make_envelope(
    value: Any,
    status: str,
    reason: str,
    source_path: str,
) -> Dict[str, Any]:
    """Return a status-envelope dict conforming to status_envelope.schema.json."""
    return {
        "value": value,
        "status": status,
        "reason": reason,
        "source_path": source_path,
    }


def _ok(value: Any, source_path: str) -> Dict[str, Any]:
    return _make_envelope(value, "OK", "", source_path)


def _not_computed(reason: str, source_path: str) -> Dict[str, Any]:
    return _make_envelope(None, "NOT_COMPUTED", reason, source_path)


def _na(reason: str, source_path: str) -> Dict[str, Any]:
    return _make_envelope(None, "N_A", reason, source_path)


# ---------------------------------------------------------------------------
# Cost constant
# ---------------------------------------------------------------------------

COST_BPS_PCT = 0.08  # MEGA COST_BPS=8 bps = 0.08% per trade (round-turn cost already deducted in net_return_pct)


# ---------------------------------------------------------------------------
# Helpers to safely reach into nested dicts
# ---------------------------------------------------------------------------

def _get(mapping: Optional[Dict], *keys: str, default: Any = None) -> Any:
    """Walk nested dicts; return default on any missing step."""
    cur: Any = mapping
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k, default)
    return cur


# ---------------------------------------------------------------------------
# Pure builder — the unit-validated function
# ---------------------------------------------------------------------------

def build_artifact(
    mega_row: Optional[Dict[str, Any]],
    cpcv_row: Optional[Dict[str, Any]],
    pbo: Optional[Dict[str, Any]],
    backtest_run_id: str,
) -> Dict[str, Any]:
    """
    Build a single evaluation-artifact dict from one MEGA row, one CPCV row,
    and the pool-level PBO dict.

    Parameters
    ----------
    mega_row : dict or None
        One row from the MEGA ``results`` list.  Must contain keys like
        strategy, symbol, timeframe, summary{...}, classification, etc.
    cpcv_row : dict or None
        Matching CPCV row (joined on strategy+symbol+timeframe), or None.
    pbo : dict or None
        Pool-level PBO dict with keys pbo, status, splits_used, ….
    backtest_run_id : str
        Typically the MEGA filename stem.

    Returns
    -------
    dict
        Conforms to evaluation_artifact_v1.schema.json (status_envelope refs).
    """
    # ----- guards -----------------------------------------------------------
    if mega_row is None:
        raise ValueError("mega_row is required; cannot be None")

    strategy = mega_row.get("strategy", "UNKNOWN")
    symbol = mega_row.get("symbol", "UNKNOWN")
    timeframe = mega_row.get("timeframe", "UNKNOWN")
    strategy_id = f"{strategy}|{symbol}|{timeframe}"

    summary = mega_row.get("summary") or {}
    lockbox = summary.get("lockbox_oos") or {}

    cpcv_ok = (
        cpcv_row is not None
        and isinstance(cpcv_row, dict)
        and cpcv_row.get("status") == "OK"
    )

    pbo_ok = (
        pbo is not None
        and isinstance(pbo, dict)
        and pbo.get("pbo") is not None
    )

    # ----- metrics (SCHEMA VOCABULARY) --------------------------------------

    metrics: Dict[str, Any] = {}

    # -- Lockbox-derived (OK when present) -----------------------------------

    def _lockbox_ok(lockbox_key: str) -> Dict[str, Any]:
        val = lockbox.get(lockbox_key)
        if val is None:
            return _not_computed(
                f"lockbox_oos field '{lockbox_key}' missing or null",
                f"mega:summary.lockbox_oos.{lockbox_key}",
            )
        return _ok(val, f"mega:summary.lockbox_oos.{lockbox_key}")

    # net_profit_pct
    metrics["net_profit_pct"] = _lockbox_ok("net_return_pct")

    # profit_factor
    metrics["profit_factor"] = _lockbox_ok("profit_factor")

    # expectancy_r
    metrics["expectancy_r"] = _lockbox_ok("expectancy_R")

    # max_drawdown_pct (stored as POSITIVE percent)
    dd_val = lockbox.get("max_drawdown_pct")
    if dd_val is None:
        metrics["max_drawdown_pct"] = _not_computed(
            "lockbox_oos field 'max_drawdown_pct' missing or null",
            "mega:summary.lockbox_oos.max_drawdown_pct",
        )
    else:
        metrics["max_drawdown_pct"] = _ok(
            abs(dd_val), "mega:summary.lockbox_oos.max_drawdown_pct"
        )

    # trades
    metrics["trades"] = _lockbox_ok("num_trades")

    # -- Summary-derived -----------------------------------------------------

    def _summary_ok(key: str) -> Dict[str, Any]:
        val = summary.get(key)
        if val is None:
            return _not_computed(
                f"mega summary field '{key}' missing or null",
                f"mega:summary.{key}",
            )
        return _ok(val, f"mega:summary.{key}")

    # oos_return_pct ← avg_fold_test_return_pct
    metrics["oos_return_pct"] = _summary_ok("avg_fold_test_return_pct")

    # wfo_pass: OK when both folds_positive and n_folds present
    fp_val = summary.get("folds_positive")
    nf_val = summary.get("n_folds")
    if fp_val is not None and nf_val is not None and nf_val > 0:
        threshold = int(math.ceil(nf_val / 2.0))
        wfo_ok_val = bool(fp_val >= threshold)
        metrics["wfo_pass"] = _ok(wfo_ok_val, "mega:summary")
    else:
        metrics["wfo_pass"] = _na(
            "folds_positive and/or n_folds missing from MEGA summary",
            "mega:summary",
        )

    # ret_dd_ratio: derived from net_profit_pct / abs(max_drawdown_pct)
    np_env = metrics["net_profit_pct"]
    dd_env = metrics["max_drawdown_pct"]
    if np_env["status"] == "OK" and dd_env["status"] == "OK" and dd_env["value"] != 0:
        ratio_val = np_env["value"] / dd_env["value"]
        metrics["ret_dd_ratio"] = _ok(ratio_val, "mega:derived")
    else:
        metrics["ret_dd_ratio"] = _na(
            "net_profit_pct and/or max_drawdown_pct unavailable or zero",
            "mega:derived",
        )

    # -- Schema metrics — per-metric derivation from MEGA data ---------------

    # 1. return_pct_compound: lockbox net_return_pct
    if lockbox.get("net_return_pct") is not None:
        metrics["return_pct_compound"] = _ok(
            lockbox["net_return_pct"], "mega:summary.lockbox_oos.net_return_pct"
        )
    else:
        metrics["return_pct_compound"] = _not_computed(
            "lockbox_oos field 'net_return_pct' missing or null",
            "mega:summary.lockbox_oos.net_return_pct",
        )

    # 2. recovery_factor: net_return_pct / abs(max_drawdown_pct)
    np_env = metrics["net_profit_pct"]
    dd_env = metrics["max_drawdown_pct"]
    if np_env["status"] == "OK" and dd_env["status"] == "OK" and dd_env["value"] != 0:
        metrics["recovery_factor"] = _ok(
            round(np_env["value"] / dd_env["value"], 4), "mega:derived"
        )
    else:
        metrics["recovery_factor"] = _na(
            "net/max_dd unavailable or zero", "mega:derived"
        )

    # 3. calendar_days: parse data_start / data_end ISO strings
    data_start = mega_row.get("data_start")
    data_end = mega_row.get("data_end")
    try:
        if data_start and data_end:
            dt_start = datetime.fromisoformat(data_start)
            dt_end = datetime.fromisoformat(data_end)
            days = (dt_end - dt_start).days
            metrics["calendar_days"] = _ok(
                days, "mega:derived(data_end-data_start)"
            )
        else:
            metrics["calendar_days"] = _na(
                "data_start/data_end missing or unparseable", "mega:data_range"
            )
    except Exception:
        metrics["calendar_days"] = _na(
            "data_start/data_end missing or unparseable", "mega:data_range"
        )

    # 4. multi_window_pass: folds_positive == n_folds
    fp_val = summary.get("folds_positive")
    nf_val = summary.get("n_folds")
    if fp_val is not None and nf_val is not None and nf_val > 0:
        metrics["multi_window_pass"] = _ok(
            bool(fp_val == nf_val), "mega:derived(folds_positive==n_folds)"
        )
    else:
        metrics["multi_window_pass"] = _na(
            "folds_positive/n_folds missing", "mega:summary"
        )

    # 5. net_after_fees_pct: lockbox net_return_pct (already net of COST_BPS)
    if lockbox.get("net_return_pct") is not None:
        metrics["net_after_fees_pct"] = _ok(
            lockbox["net_return_pct"],
            "mega:summary.lockbox_oos.net_return_pct",
        )
        metrics["net_after_fees_pct"]["reason"] = (
            "net_return_pct already includes COST_BPS round-turn cost"
        )
    else:
        metrics["net_after_fees_pct"] = _not_computed(
            "lockbox_oos field 'net_return_pct' missing or null",
            "mega:summary.lockbox_oos.net_return_pct",
        )

    # 6. avg_trade_vs_cost: (net_return_pct / num_trades) / COST_BPS_PCT
    nrp = lockbox.get("net_return_pct")
    nt = lockbox.get("num_trades")
    if nrp is not None and nt is not None and nt > 0:
        avg_trade_pct = nrp / nt
        metrics["avg_trade_vs_cost"] = _ok(
            round(avg_trade_pct / COST_BPS_PCT, 3),
            "mega:derived(avg_trade_pct/COST_BPS_PCT)",
        )
    else:
        metrics["avg_trade_vs_cost"] = _na(
            "net_return_pct and/or num_trades missing or zero",
            "mega:derived",
        )

    # 7. param_stability_score: N_A (trial sharpe dispersion ≠ parameter stability)
    metrics["param_stability_score"] = _na(
        "trial sharpe dispersion is across trials, not the fold-level parameter stability the rubric scores; left N_A to avoid misrepresentation",
        "mega:n/a",
    )

    # 8. sharpe: N_A (MEGA lockbox sharpe is t-stat-like per-trade scaled, not annualized)
    metrics["sharpe"] = _na(
        "MEGA lockbox sharpe is a t-stat-like per-trade scaled value, NOT the annualized Sharpe the rubric scores; left N_A to avoid misrepresentation",
        "mega:n/a",
    )

    # 9. sortino: passthrough from lockbox
    sortino_val = lockbox.get("sortino")
    if sortino_val is not None:
        metrics["sortino"] = _ok(sortino_val, "mega:summary.lockbox_oos.sortino")
    else:
        metrics["sortino"] = _na(
            "engine does not yet emit a sortino; left N_A",
            "mega:summary.lockbox_oos.sortino",
        )

    # 10. equity_curve_health: passthrough from lockbox
    ech_val = lockbox.get("equity_curve_health")
    if ech_val is not None:
        metrics["equity_curve_health"] = _ok(
            ech_val, "mega:summary.lockbox_oos.equity_curve_health"
        )
    else:
        metrics["equity_curve_health"] = _na(
            "engine does not yet emit equity_curve_health",
            "mega:summary.lockbox_oos.equity_curve_health",
        )

    # 11. max_consecutive_losses: passthrough from lockbox
    mcl_val = lockbox.get("max_consecutive_losses")
    if mcl_val is not None:
        metrics["max_consecutive_losses"] = _ok(
            mcl_val, "mega:summary.lockbox_oos.max_consecutive_losses"
        )
    else:
        metrics["max_consecutive_losses"] = _na(
            "engine does not yet emit max_consecutive_losses",
            "mega:summary.lockbox_oos.max_consecutive_losses",
        )

    # 12. top_trade_concentration: passthrough from lockbox
    ttc_val = lockbox.get("top_trade_concentration")
    if ttc_val is not None:
        metrics["top_trade_concentration"] = _ok(
            ttc_val, "mega:summary.lockbox_oos.top_trade_concentration"
        )
    else:
        metrics["top_trade_concentration"] = _na(
            "engine does not yet emit top_trade_concentration",
            "mega:summary.lockbox_oos.top_trade_concentration",
        )

    # 13. worst_window_drawdown_pct: primary source = mega summary (Gate-2 enriched);
    # backward-compatible fallback to lockbox (pre-Gate-2) only when summary field missing.
    wwd_val = summary.get("worst_window_drawdown_pct")
    if wwd_val is not None:
        metrics["worst_window_drawdown_pct"] = _ok(
            float(wwd_val), "mega:summary.worst_window_drawdown_pct"
        )
    else:
        lb_wwd = lockbox.get("worst_window_drawdown_pct")
        if lb_wwd is not None:
            metrics["worst_window_drawdown_pct"] = _ok(
                abs(lb_wwd), "mega:summary.lockbox_oos.worst_window_drawdown_pct"
            )
        else:
            metrics["worst_window_drawdown_pct"] = _na(
                "engine does not yet emit worst_window_drawdown_pct",
                "mega:summary.worst_window_drawdown_pct",
            )

    # 14. regime_coverage_count: N_A (no regime stage in MEGA)
    metrics["regime_coverage_count"] = _na(
        "no regime stage in MEGA", "mega:n/a"
    )

    # 15. long_short_ratio: N_A (MEGA runs one direction per strategy)
    metrics["long_short_ratio"] = _na(
        "MEGA runs one direction per strategy; long/short ratio not defined",
        "mega:n/a",
    )

    # 16. net_after_slippage_pct: N_A (MEGA cost model is fees only)
    metrics["net_after_slippage_pct"] = _na(
        "MEGA cost model is fees only (COST_BPS); no separate slippage model",
        "mega:n/a",
    )

    # -- CPCV (optional) -----------------------------------------------------
    if cpcv_ok:
        metrics["cpcv_pass_ratio"] = _ok(
            cpcv_row["pass_rate"], "cpcv:pass_rate"
        )
    else:
        metrics["cpcv_pass_ratio"] = _na(
            "CPCV row absent or status != 'OK'", "cpcv:pass_rate"
        )

    # -- PBO (pool-level, optional) ------------------------------------------
    if pbo_ok:
        metrics["pbo"] = _ok(pbo["pbo"], "pbo:pbo")
    else:
        metrics["pbo"] = _not_computed(
            "PBO dict absent or pbo value is null", "pbo:pbo"
        )

    # -- Extra (additionalProperties allows) ---------------------------------
    def _mega_ok(key: str, path: str) -> Dict[str, Any]:
        val = mega_row.get(key)
        if val is None:
            return _not_computed(f"mega field '{key}' missing or null", f"mega:{path}")
        return _ok(val, f"mega:{path}")

    metrics["dsr_p_value"] = _mega_ok("dsr_p_value", "dsr_p_value")
    metrics["boot_p_value"] = _mega_ok("boot_p_value", "boot_p_value")

    # ----- benchmark --------------------------------------------------------
    benchmark: Dict[str, Any] = {}

    # Read buy_hold_lockbox if present (SP-004 Gate 2)
    bh_lockbox = summary.get("buy_hold_lockbox") or {}
    bh_return = bh_lockbox.get("buy_hold_return_pct")
    bh_ratio = bh_lockbox.get("buy_hold_ret_dd_ratio")

    # excess_alpha_pct: strategy lockbox net_return_pct - buy_hold_return_pct
    strat_return = lockbox.get("net_return_pct")
    excess_val = None
    if strat_return is not None and bh_return is not None:
        excess_val = round(strat_return - bh_return, 3)
        benchmark["excess_alpha_pct"] = _ok(
            excess_val,
            "mega:derived(net_return_pct - buy_hold_return_pct)",
        )
    else:
        benchmark["excess_alpha_pct"] = _not_computed(
            "strategy net_return_pct or buy_hold_return_pct missing",
            "mega:derived",
        )

    # beats_bh_risk_adjusted: strategy ret_dd_ratio > buy_hold_ret_dd_ratio
    # AND excess_alpha_pct >= 0
    strat_ret_dd_env = metrics.get("ret_dd_ratio")
    if (
        strat_ret_dd_env is not None
        and strat_ret_dd_env.get("status") == "OK"
        and bh_ratio is not None
        and excess_val is not None
    ):
        beats = bool(
            strat_ret_dd_env["value"] > bh_ratio and excess_val >= 0
        )
        benchmark["beats_bh_risk_adjusted"] = _ok(
            beats,
            "mega:derived(ret_dd_ratio > buy_hold_ret_dd_ratio AND excess_alpha_pct >= 0)",
        )
    else:
        missing_parts = []
        if strat_ret_dd_env is None or strat_ret_dd_env.get("status") != "OK":
            missing_parts.append("strategy ret_dd_ratio")
        if bh_ratio is None:
            missing_parts.append("buy_hold_ret_dd_ratio")
        if excess_val is None:
            missing_parts.append("excess_alpha_pct")
        benchmark["beats_bh_risk_adjusted"] = _not_computed(
            f"missing inputs: {', '.join(missing_parts)}",
            "mega:derived",
        )

    benchmark["beats_ema_benchmark"] = _na(
        "not produced by MEGA pipeline", "mega:n/a"
    )

    # ----- regime -----------------------------------------------------------
    regime: Dict[str, Any] = {}
    for _rname in (
        "regime_breakdown_present",
        "weak_regime_identified",
        "worst_regime_return_pct",
    ):
        regime[_rname] = _na("not produced by MEGA pipeline", "mega:n/a")

    # ----- hard_flags -------------------------------------------------------
    # FIX 2: hard_flags values are BARE (string|null / boolean|null),
    # NOT status envelopes. Schema: repaint_status ∈ enum|null,
    # overfit_suspect ∈ boolean|null.
    hard_flags: Dict[str, Any] = {}

    # repaint_status: bare string or null from enum — no repaint stage in MEGA
    hard_flags["repaint_status"] = None

    # overfit_suspect: True when pool pbo >= 0.5, else False; null when absent
    if pbo_ok:
        hard_flags["overfit_suspect"] = bool(pbo["pbo"] >= 0.5)
    else:
        hard_flags["overfit_suspect"] = None

    # ----- flags (advisory) -------------------------------------------------
    # FIX 2: flags values are BARE, not status envelopes.
    # parity_status ∈ {PASS, WARN, N_A, null}.
    flags: Dict[str, Any] = {}
    flags["parity_status"] = "N_A"

    # ----- completeness -----------------------------------------------------
    n_folds_val = summary.get("n_folds", 0) or 0
    missing: List[str] = []
    if not cpcv_ok:
        missing.append("cpcv")
    if not pbo_ok:
        missing.append("pbo")
    # benchmark is complete only when both excess_alpha_pct and beats_bh_risk_adjusted are OK
    has_bench = (
        benchmark["excess_alpha_pct"]["status"] == "OK"
        and benchmark["beats_bh_risk_adjusted"]["status"] == "OK"
    )
    if not has_bench:
        missing.append("benchmark")
    missing.append("regime")  # no regime stage in MEGA

    completeness: Dict[str, Any] = {
        "has_cpcv": cpcv_ok,
        "has_wfo": bool(n_folds_val > 0),
        "has_benchmark": has_bench,
        "missing": missing,
    }

    # ----- assemble ---------------------------------------------------------
    generated_at = datetime.now(timezone.utc).isoformat()

    artifact: Dict[str, Any] = {
        "strategy_id": strategy_id,
        "backtest_run_id": backtest_run_id,
        "evaluation_artifact_version": "v1",
        "generated_at": generated_at,
        "symbol": symbol,
        "timeframe": timeframe,
        "strategy_type": mega_row.get("strategy_type"),
        "metrics": metrics,
        "benchmark": benchmark,
        "regime": regime,
        "hard_flags": hard_flags,
        "flags": flags,
        "completeness": completeness,
    }

    return artifact


# ---------------------------------------------------------------------------
# CLI / file I/O (NOT part of the pure function; file I/O lives here)
# ---------------------------------------------------------------------------

def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _sanitize_filename_component(s: str) -> str:
    """Replace characters unsafe for filenames."""
    for ch in r'<>:"/\|?*':
        s = s.replace(ch, "_")
    return s


def main(argv: Optional[List[str]] = None) -> None:
    ap = argparse.ArgumentParser(
        description="SP-004 Phase 1: build evaluation artifacts from MEGA/CPCV/PBO"
    )
    ap.add_argument("--mega", required=True, help="Path to MEGA results JSON")
    ap.add_argument("--cpcv", default=None, help="Path to CPCV results JSON (optional)")
    ap.add_argument("--pbo", default=None, help="Path to PBO summary JSON (optional)")
    ap.add_argument(
        "--out-dir", required=True, help="Directory to write .eval.json files"
    )
    args = ap.parse_args(argv)

    # ---- load --------------------------------------------------------------
    mega_wrapper = _load_json(args.mega)
    mega_rows: List[Dict[str, Any]] = mega_wrapper.get("results", [])

    cpcv_index: Dict[str, Dict[str, Any]] = {}
    if args.cpcv:
        cpcv_wrapper = _load_json(args.cpcv)
        for row in cpcv_wrapper.get("results", []):
            key = f"{row.get('strategy','')}|{row.get('symbol','')}|{row.get('timeframe','')}"
            cpcv_index[key] = row

    pbo: Optional[Dict[str, Any]] = None
    if args.pbo:
        pbo = _load_json(args.pbo)  # single dict, not wrapped

    backtest_run_id = os.path.splitext(os.path.basename(args.mega))[0]

    os.makedirs(args.out_dir, exist_ok=True)

    # ---- process rows ------------------------------------------------------
    written = 0
    for row in mega_rows:
        classification = row.get("classification", "")
        if classification not in {"PASS", "STRONG_PASS"}:
            continue

        strategy = row.get("strategy", "UNKNOWN")
        symbol = row.get("symbol", "UNKNOWN")
        timeframe = row.get("timeframe", "UNKNOWN")
        key = f"{strategy}|{symbol}|{timeframe}"
        cpcv_row = cpcv_index.get(key)

        artifact = build_artifact(row, cpcv_row, pbo, backtest_run_id)

        fname = (
            f"{_sanitize_filename_component(strategy)}__"
            f"{_sanitize_filename_component(symbol)}__"
            f"{_sanitize_filename_component(timeframe)}.eval.json"
        )
        out_path = os.path.join(args.out_dir, fname)
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(artifact, fh, indent=2, default=str)

        written += 1

    print(f"Wrote {written} evaluation artifacts to {args.out_dir}")


if __name__ == "__main__":
    main()
