#!/usr/bin/env python3
"""
score_gate1b.py — SP-004 Phase 3 Gate-1B MTC-Feasibility scorer.

Read-only consumer: reads MTC-feasibility fields (status-enveloped under the
artifact's `feasibility.*` block) and computes the Gate 1B /100 score (PASS≥75)
per the rubric §"Gate 1B".  Until a feasibility-artifact writer emits those
fields, every gate is INCOMPLETE (correct honest status).  NOT a backtest;
NO Pine/parity/MTC/trading change.  NEVER git/commit.

Usage:
  python score_gate1b.py --in-dir <dir_of_artifact.json> --out-dir <dir>

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
# 1.  RUBRIC DEFINITION  (Gate-1B  / 100)
# ---------------------------------------------------------------------------
# KIND-DRIVEN: all criteria under 'feasibility' section, kind='bool'
# ---------------------------------------------------------------------------

RUBRIC_CRITERIA: List[Dict[str, Any]] = [
    {
        "criterion": "signal_reducible",
        "points_max": 20,
        "source_metric": "feasibility.signal_reducible",
        "section": "1B",
        "kind": "bool",
        "note": "",
    },
    {
        "criterion": "entry_vs_full_clear",
        "points_max": 16,
        "source_metric": "feasibility.entry_vs_full_clear",
        "section": "1B",
        "kind": "bool",
        "note": "",
    },
    {
        "criterion": "no_risk_engine_conflict",
        "points_max": 20,
        "source_metric": "feasibility.no_risk_engine_conflict",
        "section": "1B",
        "kind": "bool",
        "note": "",
    },
    {
        "criterion": "alert_convertible",
        "points_max": 16,
        "source_metric": "feasibility.alert_convertible",
        "section": "1B",
        "kind": "bool",
        "note": "",
    },
    {
        "criterion": "state_machine_definable",
        "points_max": 16,
        "source_metric": "feasibility.state_machine_definable",
        "section": "1B",
        "kind": "bool",
        "note": "",
    },
    {
        "criterion": "mtc_param_mappable",
        "points_max": 12,
        "source_metric": "feasibility.mtc_param_mappable",
        "section": "1B",
        "kind": "bool",
        "note": "",
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
    points_max = crit["points_max"]
    try:
        if kind == "bool":
            result["points_awarded"] = points_max if value else 0.0
        elif kind == "linear":
            result["points_awarded"] = _linear_score(value, crit["low"], crit["high"], points_max)
        elif kind == "linear_desc":
            result["points_awarded"] = _linear_score_desc(value, crit["high"], crit["low"], points_max)
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

def score_gate1b(artifact: dict) -> dict:
    """
    Compute the Gate-1B /100 score from an evaluation_artifact_v1 dict.

    Returns a scorecard-style block with gate1B.
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

    # Verdict (D1 bands)
    verdict = None
    if score is not None:
        if score >= 75:
            verdict = "PASS"
        elif score >= 60:
            verdict = "CONDITIONAL"
            if gate_status == "OK":
                notes.append("Gate 1B CONDITIONAL (60-74): fix spec gaps before backtest")
        else:
            verdict = "FAIL"
    # REJECT_REPAINT hard-fail overrides the band verdict (gate is killed).
    if (artifact.get("hard_flags") or {}).get("repaint_status") == "REJECT_REPAINT":
        verdict = "FAIL"

    return {
        "strategy_id": strategy_id,
        "gate1B": {
            "score": score,
            "max": 100,
            "sub_scores": sub_scores,
            "status": gate_status,
            "pass": gate_pass,
            "verdict": verdict,
        },
        "flags": {
            "parity_status": parity_status,
        },
        "notes": notes,
        "gate1": {"status": "N_A"},
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
        description="SP-004 Phase 3: Gate-1B scorer — reads .eval.json, writes .scorecard.json"
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
        print("[score_gate1b] WARNING: No .eval.json files found in %s" % in_dir)
        return

    counts = {"OK": 0, "INCOMPLETE": 0, "FAIL": 0, "pass": 0}
    for fpath in artifacts:
        try:
            with open(fpath, "r", encoding="utf-8") as fh:
                artifact = json.load(fh)
        except (json.JSONDecodeError, IOError) as exc:
            print("[score_gate1b] SKIP %s: %s" % (os.path.basename(fpath), exc))
            continue

        result = score_gate1b(artifact)

        sid = result.get("strategy_id", "unknown")
        safe = _sanitize_filename(sid)
        out_path = os.path.join(out_dir, safe + ".scorecard.json")

        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2, default=str)

        g1b = result["gate1B"]
        status = g1b["status"]
        passed = g1b["pass"]

        counts[status] = counts.get(status, 0) + 1
        if passed:
            counts["pass"] = counts.get("pass", 0) + 1

        print(
            "[score_gate1b] %s  status=%-11s  score=%s  pass=%s  → %s"
            % (
                sid,
                status,
                str(g1b["score"]) if g1b["score"] is not None else "N/A",
                str(passed),
                os.path.basename(out_path),
            )
        )

    print(
        "\n[score_gate1b] SUMMARY — OK=%d  INCOMPLETE=%d  FAIL=%d  pass=%d  (of %d artifacts)"
        % (counts["OK"], counts["INCOMPLETE"], counts["FAIL"], counts["pass"], len(artifacts))
    )


if __name__ == "__main__":
    main()
