#!/usr/bin/env python3
"""
score_gate2.py — SP-004 Phase 2 Gate-2 Backtest Scorer.

Read-only consumer: reads evaluation_artifact_v1 JSONs and computes the
Gate 2 /100 score per the rubric.  NOT a backtest; NO Pine/parity/MTC/trading
change.  NEVER git/commit.

Usage:
  python score_gate2.py --in-dir <dir_of_.eval.json> --out-dir <dir>

Output per artifact: <strategy_id_sanitized>.scorecard.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# 1.  RUBRIC DEFINITION  (Gate-2  / 100)
# ---------------------------------------------------------------------------
# Each entry: (criterion_label, points_max, source_metric_path, rubric_note)
#
# source_metric_path is a dotted path into the artifact, e.g.
#   "metrics.sharpe"  or  "benchmark.beats_bh_risk_adjusted"
#
# The rubric categories follow the evaluation_artifact_v1 schema sections
# §5.1–§5.7.  Point totals:
#   §5.1  Performance         20 pts
#   §5.2  Risk / Drawdown     20 pts
#   §5.3  Sample Quality      10 pts
#   §5.4  Robustness          25 pts
#   §5.5  Cost                 5 pts
#   §5.6  Benchmark           10 pts
#   §5.7  Regime              10 pts  (raised 5→10 per schema)
#                           ---------
#                            100 pts
# ---------------------------------------------------------------------------

RUBRIC_CRITERIA: List[Dict[str, Any]] = [
    # ----- §5.1  Performance (risk-adjusted)  20 pts -----
    {
        "criterion": "sharpe_ratio",
        "points_max": 5,
        "source_metric": "metrics.sharpe",
        "section": "5.1",
        "note": "Sharpe ratio (risk-adjusted return).  Threshold ≥ 0.5 scores full.",
    },
    {
        "criterion": "sortino_ratio",
        "points_max": 4,
        "source_metric": "metrics.sortino",
        "section": "5.1",
        "note": "Sortino ratio (downside-only risk).  Threshold ≥ 0.5 scores full.",
    },
    {
        "criterion": "profit_factor",
        "points_max": 4,
        "source_metric": "metrics.profit_factor",
        "section": "5.1",
        "note": "Gross profit / gross loss.  Threshold ≥ 1.2 scores full.",
    },
    {
        "criterion": "expectancy_r",
        "points_max": 3,
        "source_metric": "metrics.expectancy_r",
        "section": "5.1",
        "note": "Average R-multiple per trade.  Threshold ≥ 0.15 scores full.",
    },
    {
        "criterion": "net_profit",
        "points_max": 4,
        "source_metric": "metrics.net_profit_pct",
        "section": "5.1",
        "note": "Net profit % over the OOS window.  Threshold ≥ 0 scores full.",
    },

    # ----- §5.2  Risk / Drawdown  20 pts -----
    {
        "criterion": "max_drawdown",
        "points_max": 6,
        "source_metric": "metrics.max_drawdown_pct",
        "section": "5.2",
        "note": "Max drawdown %.  Lower is better; ≤ 25 % scores full.",
    },
    {
        "criterion": "ret_dd_ratio",
        "points_max": 6,
        "source_metric": "metrics.ret_dd_ratio",
        "section": "5.2",
        "note": "Return / drawdown ratio.  ≥ 1.0 scores full.",
    },
    {
        "criterion": "recovery_factor",
        "points_max": 4,
        "source_metric": "metrics.recovery_factor",
        "section": "5.2",
        "note": "Recovery factor.  ≥ 1.0 scores full.",
    },
    {
        "criterion": "worst_window_dd",
        "points_max": 4,
        "source_metric": "metrics.worst_window_drawdown_pct",
        "section": "5.2",
        "note": "Worst single-window drawdown %.  ≤ 30 % scores full.",
    },

    # ----- §5.3  Sample Quality  10 pts -----
    {
        "criterion": "trade_count",
        "points_max": 4,
        "source_metric": "metrics.trades",
        "section": "5.3",
        "note": "Number of trades.  ≥ 30 scores full (scalping/intraday ≥ 50).",
    },
    {
        "criterion": "calendar_duration",
        "points_max": 3,
        "source_metric": "metrics.calendar_days",
        "section": "5.3",
        "note": "Calendar days in OOS window.  ≥ 180 scores full.",
    },
    {
        "criterion": "trade_concentration",
        "points_max": 3,
        "source_metric": "metrics.top_trade_concentration",
        "section": "5.3",
        "note": "Top-trade concentration (lower is more diversified).  ≤ 30 % scores full.",
    },

    # ----- §5.4  Robustness  25 pts -----
    {
        "criterion": "cpcv_pass_rate",
        "points_max": 8,
        "source_metric": "metrics.cpcv_pass_ratio",
        "section": "5.4",
        "note": "Combinatorial purged CV pass ratio.  ≥ 0.7 scores full.",
    },
    {
        "criterion": "pbo_overfit_check",
        "points_max": 5,
        "source_metric": "metrics.pbo",
        "section": "5.4",
        "note": "Probability of backtest overfitting.  ≤ 0.3 scores full; ≥ 0.5 → OVERFIT_SUSPECT.",
    },
    {
        "criterion": "wfo_pass",
        "points_max": 4,
        "source_metric": "metrics.wfo_pass",
        "section": "5.4",
        "note": "Walk-forward optimisation pass (boolean).  True scores full.",
    },
    {
        "criterion": "multi_window_pass",
        "points_max": 4,
        "source_metric": "metrics.multi_window_pass",
        "section": "5.4",
        "note": "Multi-window OOS consistency.  True scores full.",
    },
    {
        "criterion": "param_stability",
        "points_max": 4,
        "source_metric": "metrics.param_stability_score",
        "section": "5.4",
        "note": "Parameter stability across folds.  ≥ 0.6 scores full.",
    },

    # ----- §5.5  Cost sensitivity  5 pts -----
    {
        "criterion": "net_after_fees",
        "points_max": 3,
        "source_metric": "metrics.net_after_fees_pct",
        "section": "5.5",
        "note": "Net return after fees.  ≥ 0 scores full.",
    },
    {
        "criterion": "net_after_slippage",
        "points_max": 2,
        "source_metric": "metrics.net_after_slippage_pct",
        "section": "5.5",
        "note": "Net return after slippage.  ≥ 0 scores full.",
    },

    # ----- §5.6  Benchmark relative  10 pts -----
    {
        "criterion": "beats_bh_risk_adj",
        "points_max": 5,
        "source_metric": "benchmark.beats_bh_risk_adjusted",
        "section": "5.6",
        "note": "Beats buy & hold on a risk-adjusted basis.  True scores full.",
    },
    {
        "criterion": "excess_alpha",
        "points_max": 3,
        "source_metric": "benchmark.excess_alpha_pct",
        "section": "5.6",
        "note": "Excess alpha over benchmark.  ≥ 0 scores full.",
    },
    {
        "criterion": "beats_ema",
        "points_max": 2,
        "source_metric": "benchmark.beats_ema_benchmark",
        "section": "5.6",
        "note": "Beats EMA crossover benchmark.  True scores full.",
    },

    # ----- §5.7  Regime robustness  10 pts (raised 5→10) -----
    {
        "criterion": "regime_breakdown",
        "points_max": 4,
        "source_metric": "regime.regime_breakdown_present",
        "section": "5.7",
        "note": "Regime breakdown present.  True scores full.",
    },
    {
        "criterion": "weak_regime_awareness",
        "points_max": 3,
        "source_metric": "regime.weak_regime_identified",
        "section": "5.7",
        "note": "Weak regime identified.  True/string scores full.",
    },
    {
        "criterion": "worst_regime_return",
        "points_max": 3,
        "source_metric": "regime.worst_regime_return_pct",
        "section": "5.7",
        "note": "Worst-regime return %.  ≥ -10 % scores full.",
    },
]

# Sum-of-maxima guard
_TOTAL_MAX = sum(c["points_max"] for c in RUBRIC_CRITERIA)
assert _TOTAL_MAX == 100, f"Rubric max points must total 100, got {_TOTAL_MAX}"

# ---------------------------------------------------------------------------
# 2.  STATUS ENVELOPE HELPERS
# ---------------------------------------------------------------------------

# Status values that are NOT ok (anything other than 'OK' means the metric
# was not successfully computed).
NON_OK_STATUSES = frozenset({
    "N_A",
    "NOT_COMPUTED",
    "INSUFFICIENT_DATA",
    "INSUFFICIENT_TRADES",
    "INSUFFICIENT_HISTORY",
    "INSUFFICIENT_FOLDS",
    "TOOL_FAILED",
    "TOOL_ERROR",
    "MISSING",
    "SKIPPED",
})


def _resolve_dotted(obj: Dict[str, Any], path: str) -> Any:
    """Walk a dotted path into a nested dict.  Returns None if missing."""
    parts = path.split(".")
    cur: Any = obj
    for p in parts:
        if isinstance(cur, dict):
            cur = cur.get(p)
        else:
            return None
    return cur


def _envelope_status(env: Any) -> str:
    """Return the status string from a status envelope, or 'ABSENT'."""
    if isinstance(env, dict) and "status" in env:
        return str(env.get("status", "ABSENT"))
    if env is None:
        return "ABSENT"
    # If it's not a dict-with-status, treat as raw value → OK (legacy / unwrapped)
    return "OK"


def _envelope_value(env: Any) -> Any:
    """Return the value from a status envelope, or the raw value if unwrapped."""
    if isinstance(env, dict) and "value" in env:
        return env["value"]
    return env


def _is_ok(env: Any) -> bool:
    """True if the envelope status is exactly 'OK'."""
    return _envelope_status(env) == "OK"


# ---------------------------------------------------------------------------
# 3.  PER-CRITERION SCORING FUNCTIONS
# ---------------------------------------------------------------------------

def _score_criterion(
    crit: Dict[str, Any],
    artifact: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Score a single rubric criterion against the artifact.

    Returns a sub_score dict:
      {criterion, points_awarded, points_max, metric_status, source_metric, note}
    """
    path = crit["source_metric"]
    raw = _resolve_dotted(artifact, path)
    status = _envelope_status(raw)
    value = _envelope_value(raw)

    result: Dict[str, Any] = {
        "criterion": crit["criterion"],
        "points_max": crit["points_max"],
        "metric_status": status,
        "source_metric": path,
        "note": crit.get("note", ""),
    }

    # ---- Core status rule: only 'OK' scores ----
    if status != "OK":
        result["points_awarded"] = None  # NOT scored — not zero!
        result["note"] += " [NOT SCORED: metric status=%s]" % status
        return result

    # ---- Hard-flag: REJECT_REPAINT ----
    # repaint is NOT a rubric criterion but may appear in hard_flags.
    # We check it at the gate level, not per criterion.

    # ---- Score based on metric type ----
    cname = crit["criterion"]
    try:
        if cname == "sharpe_ratio":
            result["points_awarded"] = _linear_score(value, 0.0, 0.5, crit["points_max"])
        elif cname == "sortino_ratio":
            result["points_awarded"] = _linear_score(value, 0.0, 0.5, crit["points_max"])
        elif cname == "profit_factor":
            result["points_awarded"] = _linear_score(value, 0.8, 1.2, crit["points_max"])
        elif cname == "expectancy_r":
            result["points_awarded"] = _linear_score(value, 0.0, 0.15, crit["points_max"])
        elif cname == "net_profit":
            result["points_awarded"] = _linear_score(value, -5.0, 0.0, crit["points_max"])
        elif cname == "max_drawdown":
            # Lower is better: ≤25% full, >50% zero
            result["points_awarded"] = _linear_score_desc(value, 50.0, 25.0, crit["points_max"])
        elif cname == "ret_dd_ratio":
            result["points_awarded"] = _linear_score(value, 0.0, 1.0, crit["points_max"])
        elif cname == "recovery_factor":
            result["points_awarded"] = _linear_score(value, 0.5, 1.0, crit["points_max"])
        elif cname == "worst_window_dd":
            result["points_awarded"] = _linear_score_desc(value, 60.0, 30.0, crit["points_max"])
        elif cname == "trade_count":
            result["points_awarded"] = _linear_score(value, 10, 30, crit["points_max"])
        elif cname == "calendar_duration":
            result["points_awarded"] = _linear_score(value, 60, 180, crit["points_max"])
        elif cname == "trade_concentration":
            result["points_awarded"] = _linear_score_desc(value, 60.0, 30.0, crit["points_max"])
        elif cname == "cpcv_pass_rate":
            result["points_awarded"] = _linear_score(value, 0.3, 0.7, crit["points_max"])
        elif cname == "pbo_overfit_check":
            # PBO: lower is better. ≤0.3 full, ≥0.5 zero (and flagged)
            result["points_awarded"] = _linear_score_desc(value, 0.5, 0.3, crit["points_max"])
        elif cname == "wfo_pass":
            result["points_awarded"] = crit["points_max"] if value else 0.0
        elif cname == "multi_window_pass":
            result["points_awarded"] = crit["points_max"] if value else 0.0
        elif cname == "param_stability":
            result["points_awarded"] = _linear_score(value, 0.3, 0.6, crit["points_max"])
        elif cname == "net_after_fees":
            result["points_awarded"] = _linear_score(value, -5.0, 0.0, crit["points_max"])
        elif cname == "net_after_slippage":
            result["points_awarded"] = _linear_score(value, -5.0, 0.0, crit["points_max"])
        elif cname == "beats_bh_risk_adj":
            result["points_awarded"] = crit["points_max"] if value else 0.0
        elif cname == "excess_alpha":
            result["points_awarded"] = _linear_score(value, -5.0, 0.0, crit["points_max"])
        elif cname == "beats_ema":
            result["points_awarded"] = crit["points_max"] if value else 0.0
        elif cname == "regime_breakdown":
            result["points_awarded"] = crit["points_max"] if value else 0.0
        elif cname == "weak_regime_awareness":
            # Could be bool or string
            result["points_awarded"] = crit["points_max"] if value else 0.0
        elif cname == "worst_regime_return":
            result["points_awarded"] = _linear_score(value, -20.0, -10.0, crit["points_max"])
        else:
            result["points_awarded"] = None
            result["note"] += " [UNKNOWN criterion — cannot score]"
    except (TypeError, ValueError):
        result["points_awarded"] = None
        result["note"] += " [SCORING_ERROR: value=%s]" % repr(value)

    return result


def _linear_score(
    value: float, low: float, high: float, pts_max: float
) -> float:
    """Linear interpolation: value≤low → 0, value≥high → pts_max."""
    if value is None:
        return 0.0
    if value >= high:
        return pts_max
    if value <= low:
        return 0.0
    return round((value - low) / (high - low) * pts_max, 2)


def _linear_score_desc(
    value: float, high: float, low: float, pts_max: float
) -> float:
    """Descending linear: value≥high → 0, value≤low → pts_max."""
    if value is None:
        return 0.0
    if value <= low:
        return pts_max
    if value >= high:
        return 0.0
    return round((high - value) / (high - low) * pts_max, 2)


# ---------------------------------------------------------------------------
# 4.  PURE SCORING FUNCTION
# ---------------------------------------------------------------------------

def score_gate2(artifact: dict) -> dict:
    """
    Compute the Gate-2 /100 score from an evaluation_artifact_v1 dict.

    Returns a scorecard_v2-style block:
      {
        strategy_id,
        gate2: {
          score: float|None,
          max: 100,
          sub_scores: [...],
          status: 'OK'|'INCOMPLETE'|'FAIL',
          pass: bool,
          overfit_suspect: bool|None
        },
        flags: {parity_status},
        notes: [...]
      }
    """
    strategy_id = artifact.get("strategy_id", "UNKNOWN")

    # ----- 4a.  Score every criterion -----
    sub_scores: List[Dict[str, Any]] = []
    incomplete_reasons: List[str] = []
    overfit_suspect: Optional[bool] = None
    total_scored: float = 0.0
    total_possible_scored: int = 0  # sum of points_max for OK criteria only

    for crit in RUBRIC_CRITERIA:
        ss = _score_criterion(crit, artifact)
        sub_scores.append(ss)

        if ss["metric_status"] != "OK":
            # Required metric missing → INCOMPLETE
            incomplete_reasons.append(
                "%s (%s status=%s)" % (ss["criterion"], ss["source_metric"], ss["metric_status"])
            )
            # NOT scored — points_awarded is None, do NOT add to total
        else:
            pts = ss.get("points_awarded")
            if pts is not None:
                total_scored += pts
            total_possible_scored += crit["points_max"]

    # ----- 4b.  Gate-level hard flags -----
    hard_flags = artifact.get("hard_flags") or {}
    repaint = hard_flags.get("repaint_status")

    # ----- 4c.  Overfit suspect (PBO >= 0.5) -----
    pbo_env = _resolve_dotted(artifact, "metrics.pbo")
    if _is_ok(pbo_env):
        pbo_val = _envelope_value(pbo_env)
        if pbo_val is not None and float(pbo_val) >= 0.5:
            overfit_suspect = True
        else:
            overfit_suspect = False

    # ----- 4d.  Determine gate status -----
    # 'OK'    — every required criterion had OK status, and score ≥ 0
    # 'INCOMPLETE' — at least one required metric was non-OK
    # 'FAIL'   — all required metrics OK, but score < 75 OR repaint==REJECT_REPAINT

    notes: List[str] = []

    if repaint == "REJECT_REPAINT":
        # Kill-switch: gate fails regardless
        gate_status = "FAIL"
        notes.append("REJECT_REPAINT hard-flag triggered — gate FAIL")
    elif incomplete_reasons:
        gate_status = "INCOMPLETE"
        notes.append(
            "INCOMPLETE: %d required metric(s) not OK: %s"
            % (len(incomplete_reasons), "; ".join(incomplete_reasons))
        )
    else:
        gate_status = "OK"

    # (OK→FAIL downgrade for low score happens at step 4f after score is computed)

    # ----- 4e.  Compute final score -----
    # If INCOMPLETE, score is partial (sum of OK criteria only), but flagged.
    # If FAIL due to repaint, score can be whatever was computed.
    if total_possible_scored > 0:
        # total_scored is already a sum of points on the /100 scale
        # (each criterion's points_awarded is out of its points_max,
        #  and all points_max sum to 100).
        score = round(total_scored, 2)
    else:
        score = None  # Nothing scorable at all

    # ----- 4f.  FAIL check (score < 75 threshold) -----
    # Only FAIL if all metrics were OK but score fell below min-pass
    if gate_status == "OK" and score is not None and score < 75:
        gate_status = "FAIL"
        notes.append("Score %.2f < 75 min-pass threshold" % score)

    # ----- 4g.  pass boolean -----
    # pass = (status=='OK' and score>=75)
    gate_pass: bool = (gate_status == "OK" and score is not None and score >= 75)

    # ----- 4h.  Parity advisory -----
    flags_block = artifact.get("flags") or {}
    parity_status = flags_block.get("parity_status", "N_A")
    if parity_status == "WARN":
        notes.append("PARITY_WARN: PineTS parity mismatch (advisory only — does NOT block)")

    # ----- 4i.  Overfit note -----
    if overfit_suspect is True:
        notes.append("OVERFIT_SUSPECT: PBO >= 0.5 (advisory — does NOT auto-zero)")

    # ----- 4j.  Assemble output -----
    return {
        "strategy_id": strategy_id,
        "gate2": {
            "score": score,
            "max": 100,
            "sub_scores": sub_scores,
            "status": gate_status,
            "pass": gate_pass,
            "overfit_suspect": overfit_suspect,
        },
        "flags": {
            "parity_status": parity_status,
        },
        "notes": notes,
        # Placeholder gates (not built yet)
        "gate1": {"status": "N_A"},
        "gate1B": {"status": "N_A"},
        "gate3": {"status": "N_A"},
    }


# ---------------------------------------------------------------------------
# 5.  CLI  main()
# ---------------------------------------------------------------------------

def _sanitize_filename(name: str) -> str:
    """Replace characters unsafe for filenames."""
    return re.sub(r"[^a-zA-Z0-9_\-.]", "_", name)


def main(argv: Optional[List[str]] = None) -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # avoid cp1254 crash on arrows
    except Exception:
        pass
    ap = argparse.ArgumentParser(
        description="SP-004 Phase 2: Gate-2 scorer — reads .eval.json, writes .scorecard.json"
    )
    ap.add_argument("--in-dir", required=True, help="Directory containing *.eval.json artifacts")
    ap.add_argument("--out-dir", required=True, help="Directory to write *.scorecard.json")
    args = ap.parse_args(argv)

    in_dir = os.path.abspath(args.in_dir)
    out_dir = os.path.abspath(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)

    # Find all .eval.json / .json files
    artifacts: List[str] = []
    for fname in sorted(os.listdir(in_dir)):
        if fname.endswith(".eval.json") or fname.endswith(".json"):
            artifacts.append(os.path.join(in_dir, fname))

    if not artifacts:
        print("[score_gate2] WARNING: No .eval.json files found in %s" % in_dir)
        return

    counts = {"OK": 0, "INCOMPLETE": 0, "FAIL": 0, "pass": 0}
    for fpath in artifacts:
        try:
            with open(fpath, "r", encoding="utf-8") as fh:
                artifact = json.load(fh)
        except (json.JSONDecodeError, IOError) as exc:
            print("[score_gate2] SKIP %s: %s" % (os.path.basename(fpath), exc))
            continue

        result = score_gate2(artifact)

        sid = result.get("strategy_id", "unknown")
        safe = _sanitize_filename(sid)
        out_path = os.path.join(out_dir, safe + ".scorecard.json")

        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2, default=str)

        g2 = result["gate2"]
        status = g2["status"]
        passed = g2["pass"]

        counts[status] = counts.get(status, 0) + 1
        if passed:
            counts["pass"] = counts.get("pass", 0) + 1

        print(
            "[score_gate2] %s  status=%-11s  score=%s  pass=%s  → %s"
            % (
                sid,
                status,
                str(g2["score"]) if g2["score"] is not None else "N/A",
                str(passed),
                os.path.basename(out_path),
            )
        )

    print(
        "\n[score_gate2] SUMMARY — OK=%d  INCOMPLETE=%d  FAIL=%d  pass=%d  (of %d artifacts)"
        % (counts["OK"], counts["INCOMPLETE"], counts["FAIL"], counts["pass"], len(artifacts))
    )


# ---------------------------------------------------------------------------
# 6.  EMBEDDED VALIDATION  (run with: python -c "import score_gate2; ...")
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
