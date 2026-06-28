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

# Bound the payload as night-run history grows. Lists are ranked before capping;
# honest totals stay in source_counts and a `truncated` flag marks any cut list.
_MAX_LIST_ROWS = 500
_MAX_SCATTER_POINTS = 2000

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
        # Strict identity: a malformed truthy string (e.g. "false") must NOT pass.
        "robust_final": r.get("robust_final") is True,
        "dsr_robust": r.get("dsr_robust") is True,
        "bh_fdr_survivor": r.get("bh_fdr_survivor") is True,
    }


def _cumulative_pass(flags: dict[str, bool]) -> dict[str, bool]:
    """Strictly narrowing pass-state per gate, in _GATE_ORDER.

    Gate N is "passed" only if every prior gate also passed, so the funnel can
    never widen and a survivor must have cleared completed-run, positive-OOS,
    beats-buy&hold, robustness, DSR, and BH-FDR — even if a malformed row sets a
    late flag without the earlier evidence.
    """
    out: dict[str, bool] = {}
    ok = True
    for key, _label in _GATE_ORDER:
        ok = ok and bool(flags.get(key))
        out[key] = ok
    return out


def _primary_failure(flags: dict[str, bool], row: dict[str, Any]) -> str | None:
    """First failing gate in _GATE_ORDER. None when every gate passed."""
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


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2.0


def _parameter_sensitivity(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Per-strategy OOS spread across parameter sets — a real robustness signal.

    A wide spread across neighboring parameter sets flags a fragile / overfit
    pocket; a tight, positive spread is a stability signal. Derived only from the
    ``avg_fold_test_return_pct`` already present per row. Strategies with a single
    parameter set are omitted (no spread to report).
    """
    # Aggregate OOS by (strategy, parameter_set_id) so spread is computed only
    # across genuine parameter variants. Rows without a parameter id are not part
    # of a parameter comparison and must not inflate the spread.
    by_strategy: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"family": None, "param_oos": defaultdict(list), "symbols": set()}
    )
    for row in rows:
        pid = row.get("parameter_set_id")
        if pid is None or str(pid) == "":
            continue
        oos = _num(_robustness(row).get("avg_fold_test_return_pct"))
        if oos is None:
            continue
        sid = row.get("strategy_id") or "UNKNOWN"
        agg = by_strategy[sid]
        if agg["family"] is None:
            agg["family"] = _family_of(row)
        agg["param_oos"][str(pid)].append(oos)
        if row.get("symbol"):
            agg["symbols"].add(row.get("symbol"))

    out: list[dict[str, Any]] = []
    for sid, agg in by_strategy.items():
        param_oos = agg["param_oos"]
        if len(param_oos) < 2:
            continue
        # One representative OOS per parameter set (median across its rows).
        oos = [_median(vals) for vals in param_oos.values() if vals]
        oos = [v for v in oos if v is not None]
        if len(oos) < 2:
            continue
        out.append(
            {
                "strategy_id": sid,
                "family": agg["family"],
                "n_param_sets": len(param_oos),
                "n_symbols": len(agg["symbols"]),
                "oos_min": round(min(oos), 4),
                "oos_median": round(_median(oos), 4),
                "oos_max": round(max(oos), 4),
                "oos_spread": round(max(oos) - min(oos), 4),
            }
        )
    out.sort(key=lambda x: x["oos_spread"], reverse=True)
    return out


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
    parameter_sensitivity = _parameter_sensitivity(rows)

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
        cum = _cumulative_pass(flags)
        family = _family_of(row)
        sid = row.get("strategy_id") or "UNKNOWN"
        m = _metrics(row)
        r = _robustness(row)

        # Cumulative (strictly narrowing) funnel — each stage requires all prior gates.
        funnel["total_variants"] += 1
        funnel["completed_runs"] += int(cum["completed_run"])
        funnel["positive_oos"] += int(cum["positive_oos"])
        funnel["beats_buy_hold"] += int(cum["beats_buy_hold"])
        funnel["robust_passed"] += int(cum["robust_final"])
        is_survivor = cum["bh_fdr_survivor"]  # True only if every ordered gate passed
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
                    "dsr_robust": r.get("dsr_robust") is True,
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

    # True totals captured before capping so the dashboard reports honest counts
    # while the payload stays bounded as night-run history grows. Lists are
    # already ranked (best-first / most-killed-first), so caps keep the top slice.
    totals = {
        "profile_result_rows": len(rows),
        "survivors": len(survivors),
        "graveyard": len(graveyard),
        "families": len(family_survival),
        "scatter_points": len(scatter),
        "parameter_sensitivity": len(parameter_sensitivity),
    }
    survivors_out = survivors[:_MAX_LIST_ROWS]
    graveyard_out = graveyard[:_MAX_LIST_ROWS]
    scatter_out = scatter[:_MAX_SCATTER_POINTS]
    param_out = parameter_sensitivity[:_MAX_LIST_ROWS]

    return {
        "schema_version": "1.0",
        "mode": "read_only",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "funnel": funnel,
        "survivors": survivors_out,
        "graveyard": graveyard_out,
        "family_survival": family_survival,
        "gauntlet": gauntlet_list,
        "is_oos_scatter": scatter_out,
        "parameter_sensitivity": param_out,
        "truncated": {
            "survivors": len(survivors) > len(survivors_out),
            "graveyard": len(graveyard) > len(graveyard_out),
            "is_oos_scatter": len(scatter) > len(scatter_out),
            "parameter_sensitivity": len(parameter_sensitivity) > len(param_out),
        },
        "source_counts": totals,
    }
