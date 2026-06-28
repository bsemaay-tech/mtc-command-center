"""Read-only aggregator for the Strategy Validation Terminal dashboard tab.

Derives a validation overview (funnel, survivors, graveyard, family survival,
killed-by-filter gauntlet, IS/OOS scatter, cross-asset consistency) purely from
the already-discovered profile-result rows in the night-artifacts snapshot.

Design contract:
  * Pure in-memory aggregation over ``night_artifacts["profile_results"]`` —
    never re-reads disk, never writes files, never triggers runs.
  * Invents no metrics. Every classification is derived from real fields
    (``robustness.bh_fdr_survivor``, ``metrics.buy_hold_alpha``, etc.).
  * Empty-safe: absent/empty inputs yield empty panels, never an exception.
  * Reuses existing MCC vocabulary (classification + promotion_status); adds no
    new verdict enum.

Funnel stages (each strictly narrows the previous):
  total_variants -> completed_runs -> positive_oos -> beats_buy_hold
  -> robust_passed -> survivors
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

# Ordered gate checks. The first failing gate is a row's ``primary_failure``.
# (key, human label) — order matters and mirrors 07_BACKTEST_AND_OPTIMIZATION_RULES.
_GATE_ORDER = (
    ("completed_run", "no_completed_run"),
    ("positive_oos", "negative_oos"),
    ("beats_buy_hold", "did_not_beat_buy_hold"),
    ("robust_final", "not_robust"),
    ("dsr_robust", "dsr_not_robust"),
    ("bh_fdr_survivor", "bh_fdr_not_survivor"),
)


def _num(value: Any) -> float | None:
    """Coerce to float, treating bools/None/garbage as missing."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _metrics(row: dict[str, Any]) -> dict[str, Any]:
    m = row.get("metrics")
    return m if isinstance(m, dict) else {}


def _robustness(row: dict[str, Any]) -> dict[str, Any]:
    r = row.get("robustness")
    return r if isinstance(r, dict) else {}


def _family_of(row: dict[str, Any]) -> str:
    """Best-effort family label without coupling to pipeline_reader.

    Uses the trailing tokens of the strategy_id (e.g. QL_..._8EMA_PULLBACK ->
    "8EMA_PULLBACK"). Falls back to the raw strategy_id, then "UNKNOWN".
    """
    sid = row.get("strategy_id")
    if not isinstance(sid, str) or not sid.strip():
        return "UNKNOWN"
    parts = sid.split("_")
    # Drop a leading "QL" + date + universe/timeframe boilerplate when present.
    tail = parts[-2:] if len(parts) >= 2 else parts
    label = "_".join(tail).strip("_")
    return label or sid


def _gate_flags(row: dict[str, Any]) -> dict[str, bool]:
    """Evaluate each ordered gate to a strict boolean from real fields only.

    A gate whose evidence is missing is treated as *not passed* so unfinished or
    underspecified rows fall into the graveyard rather than silently surviving.
    """
    m = _metrics(row)
    r = _robustness(row)

    completed = bool(m)  # any metrics block at all means the run produced output

    oos = _num(r.get("avg_fold_test_return_pct"))
    positive_oos = oos is not None and oos > 0

    alpha = _num(m.get("buy_hold_alpha"))
    if alpha is not None:
        beats_bh = alpha > 0
    else:
        net = _num(m.get("net_profit"))
        bh = _num(m.get("buy_hold_return"))
        beats_bh = net is not None and bh is not None and net > bh

    return {
        "completed_run": completed,
        "positive_oos": positive_oos,
        "beats_buy_hold": beats_bh,
        "robust_final": bool(r.get("robust_final")),
        "dsr_robust": bool(r.get("dsr_robust")),
        "bh_fdr_survivor": bool(r.get("bh_fdr_survivor")),
    }


def _primary_failure(flags: dict[str, bool], row: dict[str, Any]) -> str | None:
    """First failing gate. None when the row survived every gate."""
    r = _robustness(row)
    for key, label in _GATE_ORDER:
        if not flags.get(key):
            # Prefer an explicit engine classification when the robustness gate fails.
            if key == "robust_final":
                cls = r.get("classification")
                if isinstance(cls, str) and cls and cls.upper() != "PASS":
                    return cls.upper()
            return label
    return None


def _cross_asset_scores(rows: list[dict[str, Any]]) -> dict[str, int]:
    """0–4 consistency score per strategy_id from real survivor evidence.

    Counts distinct symbols where a strategy both survived BH-FDR and beat
    buy & hold, then buckets. Timeframe/window breadth nudges the top bucket.
    """
    by_strategy: dict[str, dict[str, set]] = defaultdict(
        lambda: {"symbols": set(), "timeframes": set()}
    )
    for row in rows:
        flags = _gate_flags(row)
        if not (flags["bh_fdr_survivor"] and flags["beats_buy_hold"]):
            continue
        sid = row.get("strategy_id") or "UNKNOWN"
        sym = row.get("symbol")
        tf = row.get("timeframe")
        if sym:
            by_strategy[sid]["symbols"].add(sym)
        if tf:
            by_strategy[sid]["timeframes"].add(tf)

    scores: dict[str, int] = {}
    for sid, agg in by_strategy.items():
        n = len(agg["symbols"])
        if n <= 1:
            score = 0
        elif n <= 3:
            score = 1
        elif n <= 5:
            score = 2
        else:
            score = 3
        if score >= 3 and len(agg["timeframes"]) >= 2:
            score = 4
        scores[sid] = score
    return scores


def build_validation_terminal(
    night_artifacts: dict[str, Any] | None = None,
    scorecards: Any = None,
    candidate_pipeline: Any = None,
) -> dict[str, Any]:
    """Build the validation-terminal snapshot section.

    Args:
        night_artifacts: the snapshot section produced by ``build_night_artifacts``.
            Only ``profile_results`` (a flat list of normalized rows) is consumed.
        scorecards / candidate_pipeline: reserved for later enrichment; unused in
            Phase 1 so the aggregation stays decoupled and crash-proof.
    """
    rows: list[dict[str, Any]] = []
    if isinstance(night_artifacts, dict):
        maybe = night_artifacts.get("profile_results")
        if isinstance(maybe, list):
            rows = [r for r in maybe if isinstance(r, dict)]

    cross_asset = _cross_asset_scores(rows)

    funnel = {
        "total_variants": 0,
        "completed_runs": 0,
        "positive_oos": 0,
        "beats_buy_hold": 0,
        "robust_passed": 0,
        "survivors": 0,
    }
    gauntlet: dict[str, int] = defaultdict(int)
    family_stats: dict[str, dict[str, int]] = defaultdict(
        lambda: {"tested": 0, "survivors": 0}
    )
    survivors: list[dict[str, Any]] = []
    graveyard: list[dict[str, Any]] = []
    scatter: list[dict[str, Any]] = []

    for row in rows:
        flags = _gate_flags(row)
        family = _family_of(row)
        sid = row.get("strategy_id") or "UNKNOWN"
        m = _metrics(row)
        r = _robustness(row)

        funnel["total_variants"] += 1
        funnel["completed_runs"] += int(flags["completed_run"])
        funnel["positive_oos"] += int(flags["completed_run"] and flags["positive_oos"])
        funnel["beats_buy_hold"] += int(
            flags["completed_run"] and flags["positive_oos"] and flags["beats_buy_hold"]
        )
        funnel["robust_passed"] += int(flags["robust_final"])
        is_survivor = flags["bh_fdr_survivor"]
        funnel["survivors"] += int(is_survivor)

        family_stats[family]["tested"] += 1
        family_stats[family]["survivors"] += int(is_survivor)

        # IS/OOS scatter point (only when both axes have real values).
        is_score = _num(row.get("score"))
        oos_score = _num(r.get("avg_fold_test_return_pct"))
        if is_score is not None and oos_score is not None:
            scatter.append(
                {
                    "strategy_id": sid,
                    "symbol": row.get("symbol"),
                    "timeframe": row.get("timeframe"),
                    "family": family,
                    "is_score": is_score,
                    "oos_score": oos_score,
                    "survivor": is_survivor,
                }
            )

        common = {
            "strategy_id": sid,
            "family": family,
            "symbol": row.get("symbol"),
            "timeframe": row.get("timeframe"),
            "profile": row.get("profile"),
            "net_profit": m.get("net_profit"),
            "max_drawdown": m.get("max_drawdown"),
            "buy_hold_return": m.get("buy_hold_return"),
            "buy_hold_alpha": m.get("buy_hold_alpha"),
            "trade_count": m.get("trade_count"),
            "oos_return_pct": r.get("avg_fold_test_return_pct"),
            "classification": r.get("classification"),
            "dsr_p_value": r.get("dsr_p_value"),
            "promotion_status": row.get("promotion_status"),
            "source_rel_path": row.get("source_rel_path"),
        }

        if is_survivor:
            survivors.append(
                {
                    **common,
                    "dsr_robust": bool(r.get("dsr_robust")),
                    "cross_asset_consistency_score": cross_asset.get(sid, 0),
                }
            )
        else:
            failure = _primary_failure(flags, row) or "unconfirmed"
            gauntlet[failure] += 1
            graveyard.append({**common, "primary_failure": failure})

    # Survivor ranking: real components only, no black-box composite.
    survivors.sort(
        key=lambda s: (
            1 if s.get("dsr_robust") else 0,
            s.get("cross_asset_consistency_score") or 0,
            _num(s.get("buy_hold_alpha")) if _num(s.get("buy_hold_alpha")) is not None else -1e18,
        ),
        reverse=True,
    )

    family_survival = sorted(
        (
            {
                "family": fam,
                "tested": st["tested"],
                "survivors": st["survivors"],
                "survival_rate": round(st["survivors"] / st["tested"], 4) if st["tested"] else 0.0,
            }
            for fam, st in family_stats.items()
        ),
        key=lambda f: (f["survival_rate"], f["tested"]),
        reverse=True,
    )

    gauntlet_list = sorted(
        ({"filter": k, "killed": v} for k, v in gauntlet.items()),
        key=lambda g: g["killed"],
        reverse=True,
    )

    return {
        "schema_version": "1.0",
        "mode": "read_only",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "funnel": funnel,
        "survivors": survivors,
        "graveyard": graveyard,
        "family_survival": family_survival,
        "gauntlet": gauntlet_list,
        "is_oos_scatter": scatter,
        "source_counts": {
            "profile_result_rows": len(rows),
            "survivors": len(survivors),
            "graveyard": len(graveyard),
            "families": len(family_survival),
            "scatter_points": len(scatter),
        },
    }
