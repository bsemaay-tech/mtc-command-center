#!/usr/bin/env python3
"""
score_gate1.py — SP-004 Phase 3 Gate-1 Intake Scorer.

Read-only consumer: reads candidate-intake fields (status-enveloped under the
artifact's `intake.*` block) and computes the Gate 1 /100 score per the rubric
§"Gate 1".  Until an intake-artifact writer emits those fields, every gate is
INCOMPLETE (correct honest status).  NOT a backtest; NO Pine/parity/MTC/trading
change.  NEVER git/commit.

Usage:
  python score_gate1.py --in-dir <dir_of_artifact.json> --out-dir <dir>

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
# 1.  RUBRIC DEFINITION  (Gate-1  / 100)
# ---------------------------------------------------------------------------
# Each entry: criterion, points_max, source_metric, section, kind, note
#
# All source_metric paths are under the 'intake' block (status envelopes).
# ---------------------------------------------------------------------------

RUBRIC_CRITERIA: List[Dict[str, Any]] = [
    # §1.1 Rule clarity & determinism (25)
    {
        "criterion": "entry_rule_explicit",
        "points_max": 6,
        "source_metric": "intake.entry_pseudo_present",
        "section": "1.1",
        "kind": "bool",
        "note": "Entry rule pseudo-code or explicit description present.",
    },
    {
        "criterion": "exit_approach_explicit",
        "points_max": 5,
        "source_metric": "intake.exit_pseudo_or_delegated",
        "section": "1.1",
        "kind": "bool",
        "note": "Exit approach or delegation to backtest model stated.",
    },
    {
        "criterion": "direction_defined",
        "points_max": 4,
        "source_metric": "intake.direction_defined",
        "section": "1.1",
        "kind": "bool",
        "note": "Long/short/neutral direction explicitly defined.",
    },
    {
        "criterion": "same_bar_collision_rule",
        "points_max": 4,
        "source_metric": "intake.opposite_signal_behavior_present",
        "section": "1.1",
        "kind": "bool",
        "note": "Same-bar opposite-signal collision rule present.",
    },
    {
        "criterion": "params_explicit",
        "points_max": 3,
        "source_metric": "intake.params_enumerated",
        "section": "1.1",
        "kind": "bool",
        "note": "All tunable parameters enumerated with defaults.",
    },
    {
        "criterion": "no_human_interpretation",
        "points_max": 3,
        "source_metric": "intake.has_deterministic_rules",
        "section": "1.1",
        "kind": "bool",
        "note": "Rules are deterministic (no human interpretation required).",
    },

    # §1.2 Algorithmic codability (20)
    {
        "criterion": "writable_pine_python",
        "points_max": 5,
        "source_metric": "intake.codable",
        "section": "1.2",
        "kind": "bool",
        "note": "Strategy is writable in Pine/Python.",
    },
    {
        "criterion": "no_manual_eyeball",
        "points_max": 5,
        "source_metric": "intake.not_manual_visual",
        "section": "1.2",
        "kind": "bool",
        "note": "No manual eyeball/chart inspection required.",
    },
    {
        "criterion": "inputs_numeric_boolean",
        "points_max": 4,
        "source_metric": "intake.inputs_numeric_boolean",
        "section": "1.2",
        "kind": "bool",
        "note": "Inputs are numeric or boolean (no free-text).",
    },
    {
        "criterion": "state_machine_modelable",
        "points_max": 3,
        "source_metric": "intake.state_machine_definable",
        "section": "1.2",
        "kind": "bool",
        "note": "State machine / position model definable.",
    },
    {
        "criterion": "tv_python_reproducible",
        "points_max": 3,
        "source_metric": "intake.not_closed_source",
        "section": "1.2",
        "kind": "bool",
        "note": "Reproducible in TradingView/Python (not closed-source).",
    },

    # §1.3 Preliminary repaint/lookahead (15)
    {
        "criterion": "signal_closed_bar",
        "points_max": 4,
        "source_metric": "intake.signal_from_closed_bar",
        "section": "1.3",
        "kind": "bool",
        "note": "Signal generated on closed bar only.",
    },
    {
        "criterion": "low_future_bar_risk",
        "points_max": 4,
        "source_metric": "intake.repaint_class",
        "section": "1.3",
        "kind": "repaint",
        "note": "Preliminary repaint class LOW=full/MEDIUM=half/HIGH=0.",
    },
    {
        "criterion": "htf_lookahead_safe",
        "points_max": 3,
        "source_metric": "intake.htf_lookahead_safe",
        "section": "1.3",
        "kind": "bool",
        "note": "Higher-timeframe lookahead safe.",
    },
    {
        "criterion": "no_risky_structure",
        "points_max": 2,
        "source_metric": "intake.no_risky_structure",
        "section": "1.3",
        "kind": "bool",
        "note": "No risky structure (repaint/peek).",
    },
    {
        "criterion": "realtime_eq_backtest",
        "points_max": 2,
        "source_metric": "intake.realtime_eq_backtest",
        "section": "1.3",
        "kind": "bool",
        "note": "Realtime behavior equals backtest.",
    },

    # §1.4 Trade lifecycle (15)
    {
        "criterion": "entry_signal_clear",
        "points_max": 3,
        "source_metric": "intake.entry_signal_clear",
        "section": "1.4",
        "kind": "bool",
        "note": "Entry signal definition clear.",
    },
    {
        "criterion": "exit_or_delegated_clear",
        "points_max": 3,
        "source_metric": "intake.exit_or_delegated_clear",
        "section": "1.4",
        "kind": "bool",
        "note": "Exit or delegated exit model clear.",
    },
    {
        "criterion": "opposite_signal_clear",
        "points_max": 3,
        "source_metric": "intake.opposite_signal_clear",
        "section": "1.4",
        "kind": "bool",
        "note": "Opposite-signal handling clear.",
    },
    {
        "criterion": "reentry_policy_clear",
        "points_max": 2,
        "source_metric": "intake.reentry_policy_clear",
        "section": "1.4",
        "kind": "bool",
        "note": "Re-entry policy clear.",
    },
    {
        "criterion": "state_model_clear",
        "points_max": 2,
        "source_metric": "intake.state_model_clear",
        "section": "1.4",
        "kind": "bool",
        "note": "State/position model clear.",
    },
    {
        "criterion": "backtest_exit_model_chosen",
        "points_max": 2,
        "source_metric": "intake.backtest_exit_model_chosen",
        "section": "1.4",
        "kind": "bool",
        "note": "Backtest exit model chosen.",
    },

    # §1.5 Data & backtest feasibility (10)
    {
        "criterion": "required_data_available",
        "points_max": 3,
        "source_metric": "intake.required_data_available",
        "section": "1.5",
        "kind": "bool",
        "note": "Required data available.",
    },
    {
        "criterion": "granularity_available",
        "points_max": 2,
        "source_metric": "intake.granularity_available",
        "section": "1.5",
        "kind": "bool",
        "note": "Granularity available.",
    },
    {
        "criterion": "indicators_computable",
        "points_max": 2,
        "source_metric": "intake.indicators_computable",
        "section": "1.5",
        "kind": "bool",
        "note": "Indicators computable.",
    },
    {
        "criterion": "cost_model_addable",
        "points_max": 2,
        "source_metric": "intake.cost_model_addable",
        "section": "1.5",
        "kind": "bool",
        "note": "Cost model addable.",
    },
    {
        "criterion": "enough_trade_potential",
        "points_max": 1,
        "source_metric": "intake.enough_trade_potential",
        "section": "1.5",
        "kind": "bool",
        "note": "Enough trade potential.",
    },

    # §1.6 Execution realism (10)
    {
        "criterion": "order_type_clear",
        "points_max": 2,
        "source_metric": "intake.order_type_clear",
        "section": "1.6",
        "kind": "bool",
        "note": "Order type clear.",
    },
    {
        "criterion": "entry_timing_clear",
        "points_max": 2,
        "source_metric": "intake.entry_timing_clear",
        "section": "1.6",
        "kind": "bool",
        "note": "Entry timing clear.",
    },
    {
        "criterion": "spread_slippage_estimable",
        "points_max": 2,
        "source_metric": "intake.spread_slippage_estimable",
        "section": "1.6",
        "kind": "bool",
        "note": "Spread/slippage estimable.",
    },
    {
        "criterion": "no_anti_liquidity",
        "points_max": 1,
        "source_metric": "intake.no_anti_liquidity_assumption",
        "section": "1.6",
        "kind": "bool",
        "note": "No anti-liquidity assumption.",
    },
    {
        "criterion": "intrabar_uncertainty_ok",
        "points_max": 1,
        "source_metric": "intake.intrabar_uncertainty_manageable",
        "section": "1.6",
        "kind": "bool",
        "note": "Intrabar uncertainty manageable.",
    },
    {
        "criterion": "no_extreme_latency",
        "points_max": 2,
        "source_metric": "intake.no_extreme_latency_dependence",
        "section": "1.6",
        "kind": "bool",
        "note": "No extreme latency dependence.",
    },

    # §1.7 Edge hypothesis (5)
    {
        "criterion": "sensible_market_hypothesis",
        "points_max": 3,
        "source_metric": "intake.strategy_thesis_present",
        "section": "1.7",
        "kind": "bool",
        "note": "Sensible market hypothesis present.",
    },
    {
        "criterion": "expected_regime_stated",
        "points_max": 2,
        "source_metric": "intake.expected_regime_present",
        "section": "1.7",
        "kind": "bool",
        "note": "Expected regime stated.",
    },
]

# Sum-of-maxima guard
_TOTAL_MAX = sum(c["points_max"] for c in RUBRIC_CRITERIA)
assert _TOTAL_MAX == 100, f"Rubric max points must total 100, got {_TOTAL_MAX}"

# ---------------------------------------------------------------------------
# 2.  STATUS ENVELOPE HELPERS
# ---------------------------------------------------------------------------

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

def _score_repaint(value: Any, pts_max: float) -> Optional[float]:
    s = str(value).upper().replace("_RISK", "")
    if s in ("LOW",):
        return pts_max
    if s in ("MEDIUM", "MED"):
        return round(pts_max / 2, 2)
    if s in ("HIGH",):
        return 0.0
    return None


def _score_criterion(
    crit: Dict[str, Any],
    artifact: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Score a single rubric criterion against the artifact (kind-driven).

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

    if status != "OK":
        result["points_awarded"] = None
        result["note"] += " [NOT SCORED: metric status=%s]" % status
        return result

    kind = crit.get("kind", "bool")
    try:
        if kind == "bool":
            result["points_awarded"] = crit["points_max"] if value else 0.0
        elif kind == "linear":
            result["points_awarded"] = _linear_score(
                value, crit["low"], crit["high"], crit["points_max"]
            )
        elif kind == "linear_desc":
            result["points_awarded"] = _linear_score_desc(
                value, crit["high"], crit["low"], crit["points_max"]
            )
        elif kind == "repaint":
            result["points_awarded"] = _score_repaint(value, crit["points_max"])
        else:
            result["points_awarded"] = None
            result["note"] += " [UNKNOWN kind]"
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

def score_gate1(artifact: dict) -> dict:
    """
    Compute the Gate-1 /100 score from an evaluation_artifact_v1 dict.

    Returns a scorecard_v2-style block:
      {
        strategy_id,
        gate1: {
          score: float|None,
          max: 100,
          sub_scores: [...],
          status: 'OK'|'INCOMPLETE'|'FAIL',
          pass: bool,
        },
        flags: {parity_status},
        notes: [...],
        gate1B:{status:'N_A'},
        gate2:{status:'N_A'},
        gate3:{status:'N_A'}
      }
    """
    strategy_id = artifact.get("strategy_id", "UNKNOWN")

    sub_scores: List[Dict[str, Any]] = []
    incomplete_reasons: List[str] = []
    total_scored: float = 0.0
    total_possible_scored: int = 0

    for crit in RUBRIC_CRITERIA:
        ss = _score_criterion(crit, artifact)
        sub_scores.append(ss)

        if ss["metric_status"] != "OK":
            incomplete_reasons.append(
                "%s (%s status=%s)" % (ss["criterion"], ss["source_metric"], ss["metric_status"])
            )
        else:
            pts = ss.get("points_awarded")
            if pts is not None:
                total_scored += pts
            total_possible_scored += crit["points_max"]

    hard_flags = artifact.get("hard_flags") or {}
    repaint = hard_flags.get("repaint_status")

    notes: List[str] = []

    if repaint == "REJECT_REPAINT":
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

    if total_possible_scored > 0:
        score = round(total_scored, 2)
    else:
        score = None

    if gate_status == "OK" and score is not None and score < 75:
        gate_status = "FAIL"
        notes.append("Score %.2f < 75 min-pass threshold" % score)

    gate_pass: bool = (gate_status == "OK" and score is not None and score >= 75)

    flags_block = artifact.get("flags") or {}
    parity_status = flags_block.get("parity_status", "N_A")
    if parity_status == "WARN":
        notes.append("PARITY_WARN: PineTS parity mismatch (advisory only — does NOT block)")

    return {
        "strategy_id": strategy_id,
        "gate1": {
            "score": score,
            "max": 100,
            "sub_scores": sub_scores,
            "status": gate_status,
            "pass": gate_pass,
        },
        "flags": {
            "parity_status": parity_status,
        },
        "notes": notes,
        "gate1B": {"status": "N_A"},
        "gate2": {"status": "N_A"},
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
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(
        description="SP-004 Phase 3: Gate-1 scorer — reads .eval.json, writes .scorecard.json"
    )
    ap.add_argument("--in-dir", required=True, help="Directory containing *.eval.json artifacts")
    ap.add_argument("--out-dir", required=True, help="Directory to write *.scorecard.json")
    args = ap.parse_args(argv)

    in_dir = os.path.abspath(args.in_dir)
    out_dir = os.path.abspath(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)

    artifacts: List[str] = []
    for fname in sorted(os.listdir(in_dir)):
        if fname.endswith(".eval.json") or fname.endswith(".json"):
            artifacts.append(os.path.join(in_dir, fname))

    if not artifacts:
        print("[score_gate1] WARNING: No .eval.json files found in %s" % in_dir)
        return

    counts = {"OK": 0, "INCOMPLETE": 0, "FAIL": 0, "pass": 0}
    for fpath in artifacts:
        try:
            with open(fpath, "r", encoding="utf-8") as fh:
                artifact = json.load(fh)
        except (json.JSONDecodeError, IOError) as exc:
            print("[score_gate1] SKIP %s: %s" % (os.path.basename(fpath), exc))
            continue

        result = score_gate1(artifact)

        sid = result.get("strategy_id", "unknown")
        safe = _sanitize_filename(sid)
        out_path = os.path.join(out_dir, safe + ".scorecard.json")

        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2, default=str)

        g1 = result["gate1"]
        status = g1["status"]
        passed = g1["pass"]

        counts[status] = counts.get(status, 0) + 1
        if passed:
            counts["pass"] = counts.get("pass", 0) + 1

        print(
            "[score_gate1] %s  status=%-11s  score=%s  pass=%s  → %s"
            % (
                sid,
                status,
                str(g1["score"]) if g1["score"] is not None else "N/A",
                str(passed),
                os.path.basename(out_path),
            )
        )

    print(
        "\n[score_gate1] SUMMARY — OK=%d  INCOMPLETE=%d  FAIL=%d  pass=%d  (of %d artifacts)"
        % (counts["OK"], counts["INCOMPLETE"], counts["FAIL"], counts["pass"], len(artifacts))
    )


if __name__ == "__main__":
    main()
