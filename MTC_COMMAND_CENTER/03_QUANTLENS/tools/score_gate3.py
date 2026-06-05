#!/usr/bin/env python3
"""
score_gate3.py — SP-004 Phase 3 Gate-3 MTC Production-Readiness scorer.

Read-only consumer: reads production_readiness_artifact_v1 JSONs and computes the
Gate 3 /100 score per the rubric.  NOT a backtest; NO Pine/parity/MTC/trading
change.  NEVER git/commit.

Usage:
  python score_gate3.py --in-dir <dir_of_.readiness.json> --out-dir <dir>

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
# 1.  RUBRIC DEFINITION  (Gate-3  / 100)
# ---------------------------------------------------------------------------
# Each entry: (criterion_label, points_max, source_metric_path, section, kind)
#
# source_metric_path is a dotted path into the production_readiness_artifact_v1
#   e.g. "signal_contract.emits_long_short_close_flat"
#
# All Gate-3 criteria are kind='bool' (points_max if value else 0.0).
# ---------------------------------------------------------------------------

RUBRIC_CRITERIA: List[Dict[str, Any]] = [
    # 6.1 signal_contract /25
    {
        "criterion": "emits_long_short_close_flat",
        "points_max": 5,
        "source_metric": "signal_contract.emits_long_short_close_flat",
        "section": "6.1",
        "kind": "bool",
        "note": "Emits long/short/close/flat signals.",
    },
    {
        "criterion": "signal_timing_defined",
        "points_max": 5,
        "source_metric": "signal_contract.signal_timing_defined",
        "section": "6.1",
        "kind": "bool",
        "note": "Signal timing defined.",
    },
    {
        "criterion": "same_bar_collision_defined",
        "points_max": 4,
        "source_metric": "signal_contract.same_bar_collision_defined",
        "section": "6.1",
        "kind": "bool",
        "note": "Same-bar collision handling defined.",
    },
    {
        "criterion": "signal_uniquely_identifiable",
        "points_max": 4,
        "source_metric": "signal_contract.signal_uniquely_identifiable",
        "section": "6.1",
        "kind": "bool",
        "note": "Signals uniquely identifiable.",
    },
    {
        "criterion": "entry_logical_exit_separable",
        "points_max": 4,
        "source_metric": "signal_contract.entry_logical_exit_separable",
        "section": "6.1",
        "kind": "bool",
        "note": "Entry and logical exit separable.",
    },
    {
        "criterion": "metadata_emittable",
        "points_max": 3,
        "source_metric": "signal_contract.metadata_emittable",
        "section": "6.1",
        "kind": "bool",
        "note": "Metadata emittable with signals.",
    },

    # 6.2 alert_adapter /20
    {
        "criterion": "tv_alert_json_convertible",
        "points_max": 4,
        "source_metric": "alert_adapter.tv_alert_json_convertible",
        "section": "6.2",
        "kind": "bool",
        "note": "TV alert JSON convertible.",
    },
    {
        "criterion": "entry_exit_reduceonly_distinguishable",
        "points_max": 4,
        "source_metric": "alert_adapter.entry_exit_reduceonly_distinguishable",
        "section": "6.2",
        "kind": "bool",
        "note": "Entry/exit/reduce-only distinguishable.",
    },
    {
        "criterion": "duplicate_alert_guarded",
        "points_max": 4,
        "source_metric": "alert_adapter.duplicate_alert_guarded",
        "section": "6.2",
        "kind": "bool",
        "note": "Duplicate alerts guarded.",
    },
    {
        "criterion": "order_type_derivable",
        "points_max": 3,
        "source_metric": "alert_adapter.order_type_derivable",
        "section": "6.2",
        "kind": "bool",
        "note": "Order type derivable.",
    },
    {
        "criterion": "partial_fill_handled",
        "points_max": 2,
        "source_metric": "alert_adapter.partial_fill_handled",
        "section": "6.2",
        "kind": "bool",
        "note": "Partial fills handled.",
    },
    {
        "criterion": "alert_deterministic_parseable",
        "points_max": 3,
        "source_metric": "alert_adapter.alert_deterministic_parseable",
        "section": "6.2",
        "kind": "bool",
        "note": "Alerts deterministically parseable.",
    },

    # 6.3 state_sync /15
    {
        "criterion": "strategy_vs_broker_state_comparable",
        "points_max": 4,
        "source_metric": "state_sync.strategy_vs_broker_state_comparable",
        "section": "6.3",
        "kind": "bool",
        "note": "Strategy vs broker state comparable.",
    },
    {
        "criterion": "flat_long_short_trackable",
        "points_max": 3,
        "source_metric": "state_sync.flat_long_short_trackable",
        "section": "6.3",
        "kind": "bool",
        "note": "Flat/long/short state trackable.",
    },
    {
        "criterion": "resync_after_missed_alert",
        "points_max": 3,
        "source_metric": "state_sync.resync_after_missed_alert",
        "section": "6.3",
        "kind": "bool",
        "note": "Resync after missed alert possible.",
    },
    {
        "criterion": "multi_position_logic_explicit",
        "points_max": 2,
        "source_metric": "state_sync.multi_position_logic_explicit",
        "section": "6.3",
        "kind": "bool",
        "note": "Multi-position logic explicit.",
    },
    {
        "criterion": "recomputable_after_restart",
        "points_max": 3,
        "source_metric": "state_sync.recomputable_after_restart",
        "section": "6.3",
        "kind": "bool",
        "note": "Recomputable after restart.",
    },

    # 6.4 risk_engine_compat /15
    {
        "criterion": "works_with_mtc_default_sl_tp_trail",
        "points_max": 4,
        "source_metric": "risk_engine_compat.works_with_mtc_default_sl_tp_trail",
        "section": "6.4",
        "kind": "bool",
        "note": "Works with MTC default SL/TP/trail.",
    },
    {
        "criterion": "custom_stop_explicit_if_needed",
        "points_max": 3,
        "source_metric": "risk_engine_compat.custom_stop_explicit_if_needed",
        "section": "6.4",
        "kind": "bool",
        "note": "Custom stop explicit if needed.",
    },
    {
        "criterion": "reverse_reentry_cooldown_mappable",
        "points_max": 3,
        "source_metric": "risk_engine_compat.reverse_reentry_cooldown_mappable",
        "section": "6.4",
        "kind": "bool",
        "note": "Reverse/re-entry/cooldown mappable.",
    },
    {
        "criterion": "pyramiding_intent_explicit",
        "points_max": 2,
        "source_metric": "risk_engine_compat.pyramiding_intent_explicit",
        "section": "6.4",
        "kind": "bool",
        "note": "Pyramiding intent explicit.",
    },
    {
        "criterion": "no_conflicting_order_logic",
        "points_max": 3,
        "source_metric": "risk_engine_compat.no_conflicting_order_logic",
        "section": "6.4",
        "kind": "bool",
        "note": "No conflicting order logic.",
    },

    # 6.5 monitoring /10
    {
        "criterion": "signal_reason_loggable",
        "points_max": 2,
        "source_metric": "monitoring.signal_reason_loggable",
        "section": "6.5",
        "kind": "bool",
        "note": "Signal reason loggable.",
    },
    {
        "criterion": "params_loggable",
        "points_max": 2,
        "source_metric": "monitoring.params_loggable",
        "section": "6.5",
        "kind": "bool",
        "note": "Params loggable.",
    },
    {
        "criterion": "backtest_to_live_matchable",
        "points_max": 2,
        "source_metric": "monitoring.backtest_to_live_matchable",
        "section": "6.5",
        "kind": "bool",
        "note": "Backtest-to-live matchable.",
    },
    {
        "criterion": "debug_metadata_sufficient",
        "points_max": 2,
        "source_metric": "monitoring.debug_metadata_sufficient",
        "section": "6.5",
        "kind": "bool",
        "note": "Debug metadata sufficient.",
    },
    {
        "criterion": "carries_version",
        "points_max": 2,
        "source_metric": "monitoring.carries_version",
        "section": "6.5",
        "kind": "bool",
        "note": "Carries version metadata.",
    },

    # 6.6 fail_safe /10
    {
        "criterion": "circuit_breaker_compatible",
        "points_max": 2,
        "source_metric": "fail_safe.circuit_breaker_compatible",
        "section": "6.6",
        "kind": "bool",
        "note": "Circuit breaker compatible.",
    },
    {
        "criterion": "max_daily_loss_compatible",
        "points_max": 2,
        "source_metric": "fail_safe.max_daily_loss_compatible",
        "section": "6.6",
        "kind": "bool",
        "note": "Max daily loss compatible.",
    },
    {
        "criterion": "manual_override_behavior_defined",
        "points_max": 2,
        "source_metric": "fail_safe.manual_override_behavior_defined",
        "section": "6.6",
        "kind": "bool",
        "note": "Manual override behavior defined.",
    },
    {
        "criterion": "safe_on_exchange_bot_error",
        "points_max": 2,
        "source_metric": "fail_safe.safe_on_exchange_bot_error",
        "section": "6.6",
        "kind": "bool",
        "note": "Safe on exchange/bot error.",
    },
    {
        "criterion": "no_trade_on_unexpected_signal",
        "points_max": 2,
        "source_metric": "fail_safe.no_trade_on_unexpected_signal",
        "section": "6.6",
        "kind": "bool",
        "note": "No trade on unexpected signal.",
    },

    # 6.7 reproducibility /5
    {
        "criterion": "version_pinned",
        "points_max": 1,
        "source_metric": "reproducibility.version_pinned",
        "section": "6.7",
        "kind": "bool",
        "note": "Version pinned.",
    },
    {
        "criterion": "param_set_saved",
        "points_max": 1,
        "source_metric": "reproducibility.param_set_saved",
        "section": "6.7",
        "kind": "bool",
        "note": "Param set saved.",
    },
    {
        "criterion": "dataset_window_saved",
        "points_max": 1,
        "source_metric": "reproducibility.dataset_window_saved",
        "section": "6.7",
        "kind": "bool",
        "note": "Dataset window saved.",
    },
    {
        "criterion": "cost_assumptions_saved",
        "points_max": 1,
        "source_metric": "reproducibility.cost_assumptions_saved",
        "section": "6.7",
        "kind": "bool",
        "note": "Cost assumptions saved.",
    },
    {
        "criterion": "rerun_reproducible",
        "points_max": 1,
        "source_metric": "reproducibility.rerun_reproducible",
        "section": "6.7",
        "kind": "bool",
        "note": "Rerun reproducible.",
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

    if status != "OK":
        result["points_awarded"] = None
        result["note"] += " [NOT SCORED: metric status=%s]" % status
        return result

    kind = crit.get("kind", "bool")
    try:
        if kind == "bool":
            result["points_awarded"] = crit["points_max"] if value else 0.0
        elif kind == "linear":
            # placeholder support (not used in Gate-3)
            result["points_awarded"] = crit["points_max"] if value else 0.0
        elif kind == "linear_desc":
            result["points_awarded"] = crit["points_max"] if value else 0.0
        else:
            result["points_awarded"] = None
            result["note"] += " [UNKNOWN kind — cannot score]"
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

def score_gate3(artifact: dict) -> dict:
    """
    Compute the Gate-3 /100 score from a production_readiness_artifact_v1 dict.

    Returns a scorecard-style block:
      {
        strategy_id,
        gate3: {
          score: float|None,
          max: 100,
          sub_scores: [...],
          status: 'OK'|'INCOMPLETE'|'FAIL',
          pass: bool,
        },
        flags: {parity_status},
        notes: [...],
        gate1: {status:'N_A'},
        gate1B: {status:'N_A'},
        gate2: {status:'N_A'},
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
        "gate3": {
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
        "gate1": {"status": "N_A"},
        "gate1B": {"status": "N_A"},
        "gate2": {"status": "N_A"},
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
        description="SP-004 Phase 3: Gate-3 scorer — reads .readiness.json, writes .scorecard.json"
    )
    ap.add_argument("--in-dir", required=True, help="Directory containing *.readiness.json artifacts")
    ap.add_argument("--out-dir", required=True, help="Directory to write *.scorecard.json")
    args = ap.parse_args(argv)

    in_dir = os.path.abspath(args.in_dir)
    out_dir = os.path.abspath(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)

    artifacts: List[str] = []
    for fname in sorted(os.listdir(in_dir)):
        if fname.endswith(".readiness.json") or fname.endswith(".json"):
            artifacts.append(os.path.join(in_dir, fname))

    if not artifacts:
        print("[score_gate3] WARNING: No .readiness.json files found in %s" % in_dir)
        return

    counts = {"OK": 0, "INCOMPLETE": 0, "FAIL": 0, "pass": 0}
    for fpath in artifacts:
        try:
            with open(fpath, "r", encoding="utf-8") as fh:
                artifact = json.load(fh)
        except (json.JSONDecodeError, IOError) as exc:
            print("[score_gate3] SKIP %s: %s" % (os.path.basename(fpath), exc))
            continue

        result = score_gate3(artifact)

        sid = result.get("strategy_id", "unknown")
        safe = _sanitize_filename(sid)
        out_path = os.path.join(out_dir, safe + ".scorecard.json")

        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2, default=str)

        g3 = result["gate3"]
        status = g3["status"]
        passed = g3["pass"]

        counts[status] = counts.get(status, 0) + 1
        if passed:
            counts["pass"] = counts.get("pass", 0) + 1

        print(
            "[score_gate3] %s  status=%-11s  score=%s  pass=%s  → %s"
            % (
                sid,
                status,
                str(g3["score"]) if g3["score"] is not None else "N/A",
                str(passed),
                os.path.basename(out_path),
            )
        )

    print(
        "\n[score_gate3] SUMMARY — OK=%d  INCOMPLETE=%d  FAIL=%d  pass=%d  (of %d artifacts)"
        % (counts["OK"], counts["INCOMPLETE"], counts["FAIL"], counts["pass"], len(artifacts))
    )


if __name__ == "__main__":
    main()
