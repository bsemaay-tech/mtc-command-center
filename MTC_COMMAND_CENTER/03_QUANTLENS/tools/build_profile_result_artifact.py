"""build_profile_result_artifact.py

Review/artifact writer: turn EXISTING real deterministic-soak result rows
(`MEGA_results_iter_*_results.json`) into ONE schema-valid
`backtest_profile_result.json` for the dashboard's profile-separated bucket.

This tool does NOT run a backtest, does NOT optimize, does NOT compute performance
from raw data, and NEVER fabricates KPI values. It only re-shapes values that already
exist in a real source file, preserving full provenance. Absent metrics stay null.
Default behavior is no-write. Writing the dashboard artifact requires explicit
`--apply`, is limited to 03_QUANTLENS/05_BACKTEST_RESULTS, and refuses overwrite
unless `--force` is supplied.

Honesty constraints baked in:
  * Only rows whose `strategy` exactly matches --strategy-id are used.
  * Metrics are copied 1:1 from the source `summary.lockbox_oos`; missing -> null.
  * `robust_final` / dsr / fdr flags are copied verbatim; promotion_status reflects them
    (a non-robust PASS becomes RESEARCH_ONLY, never "promoted").
  * A universe mismatch (e.g. strategy id says US_EQUITIES/10M but the soak symbol is
    crypto at another timeframe) is recorded explicitly, not hidden.
  * `profile` is a mapping decision (default SOURCE_NAKED = raw source rules, no MTC
    risk normalization) and is documented in `profile_mapping`.

Usage:
  python 03_QUANTLENS/tools/build_profile_result_artifact.py \
      --strategy-id QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK \
      --source-path 03_QUANTLENS/05_BACKTEST_RESULTS/MEGA_results_iter_1_20260601_054633_results.json \
      [--classification PASS] [--profile SOURCE_NAKED] [--apply] [--force]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

MCC_ROOT = Path(__file__).resolve().parents[2]
BACKTEST_ROOT = MCC_ROOT / "03_QUANTLENS" / "05_BACKTEST_RESULTS"
SCHEMA_DIR = MCC_ROOT / "06_SCHEMAS"

sys.path.insert(0, str(MCC_ROOT / "08_DASHBOARD_APP" / "apps" / "api"))
try:
    from mcc_readonly.schema import validate_json_schema  # type: ignore
except Exception:  # pragma: no cover
    validate_json_schema = None  # type: ignore

OFFICIAL_PROFILES = ["SOURCE_NAKED", "RISK_NORMALIZED", "MTC_LIGHT", "FULL_MTC_CANDIDATE"]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _num(v):
    """Return v only if it is a real finite number, else None. Never coerces/guesses."""
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, (int, float)):
        return v
    return None


def _universe_mismatch(strategy_id: str, symbol: str, timeframe: str) -> str | None:
    sid = strategy_id.upper()
    notes = []
    if "US_EQUITIES" in sid and symbol.upper().endswith(("USDT", "USD", "BTC", "ETH")):
        notes.append(f"strategy id implies US equities universe but soak symbol is {symbol}")
    # detect an embedded timeframe token like 10M / 5M / 1H in the id
    import re
    m = re.search(r"_(\d+)(M|MIN|H|D)_", sid)
    if m:
        implied = m.group(1) + ("m" if m.group(2).startswith("M") else m.group(2).lower())
        if implied.lower() != timeframe.lower():
            notes.append(f"strategy id implies timeframe ~{implied} but soak timeframe is {timeframe}")
    return "; ".join(notes) or None


def map_row(raw: dict, strategy_id: str, profile: str, run_id: str, source_rel: str, cost_bps) -> dict:
    summary = raw.get("summary") or {}
    lb = summary.get("lockbox_oos") or {}
    symbol = str(raw.get("symbol") or "")
    timeframe = str(raw.get("timeframe") or "")

    # Metrics: copied 1:1 from real source; anything absent stays null (never invented).
    metrics = {
        "net_profit": _num(lb.get("net_return_pct")),
        "profit_factor": _num(lb.get("profit_factor")),
        "max_drawdown": _num(lb.get("max_drawdown_pct")),
        "win_rate": _num(lb.get("win_rate")),
        "trade_count": _num(lb.get("num_trades")),
        "sharpe": _num(lb.get("sharpe")),
        # genuinely absent in source -> explicit null, not fabricated:
        "sortino": None,
        "exposure": None,
        "avg_trade": None,
        "buy_hold_return": None,
        "buy_hold_alpha": None,
        "max_loss_streak": None,
    }

    classification = raw.get("classification")
    robust_final = bool(raw.get("robust_final"))
    if robust_final:
        promotion = "ROBUST_CANDIDATE"
    elif classification == "PASS":
        promotion = "RESEARCH_ONLY"  # passed gate thresholds but NOT robustness-survivor
    else:
        promotion = f"NOT_PROMOTED ({classification})" if classification else "NOT_PROMOTED"

    best_params = summary.get("best_params")
    param_set_id = json.dumps(best_params, sort_keys=True, separators=(",", ":")) if isinstance(best_params, dict) else None

    return {
        "run_id": run_id,
        "strategy_id": strategy_id,
        "profile": profile,
        "symbol": symbol,
        "timeframe": timeframe,
        "parameter_set_id": param_set_id,
        "score_method": "deterministic_soak_lockbox_oos_sharpe",
        "score": _num(lb.get("sharpe")),
        "gate_summary": None,  # this is soak evidence, not gate scoring
        "metrics": metrics,
        "benchmark": None,  # no buy&hold in source -> not fabricated
        "robustness": {
            "classification": classification,
            "dsr_p_value": _num(raw.get("dsr_p_value")),
            "dsr_robust": bool(raw.get("dsr_robust")),
            "bh_fdr_survivor": bool(raw.get("bh_fdr_survivor")),
            "robust_final": robust_final,
            "n_folds": summary.get("n_folds"),
            "folds_positive": summary.get("folds_positive"),
            "avg_fold_test_return_pct": _num(summary.get("avg_fold_test_return_pct")),
        },
        "artifacts": {"source_path": source_rel, "source_type": "deterministic_soak_mega_results"},
        "promotion_status": promotion,
        "provenance": {
            "source_path": source_rel,
            "source_type": "deterministic_soak_mega_results",
            "data_start": raw.get("data_start"),
            "data_end": raw.get("data_end"),
            "cost_bps": cost_bps,
            "win_rate_unit": "fraction_0_1",
            "metric_units": "net_profit/max_drawdown = percent; sharpe = OOS lockbox sharpe",
            "universe_mismatch": _universe_mismatch(strategy_id, symbol, timeframe),
            "not_robust_note": None if robust_final else "robust_final=false; research-only evidence, not a promotion claim",
        },
    }


def build_document(source_path: Path, strategy_id: str, profile: str, run_id: str,
                   classification: str | None, symbol: str | None, timeframe: str | None,
                   max_rows: int) -> tuple[dict, list[str]]:
    notes: list[str] = []
    raw_doc = _read_json(source_path)
    if not isinstance(raw_doc, dict) or not isinstance(raw_doc.get("results"), list):
        raise ValueError("source is not a MEGA results document with a 'results' array")
    cfg = raw_doc.get("config") or {}
    cost_bps = cfg.get("cost_bps")
    source_rel = source_path.resolve().relative_to(MCC_ROOT).as_posix() if str(source_path.resolve()).startswith(str(MCC_ROOT)) else str(source_path)

    rows = [r for r in raw_doc["results"] if isinstance(r, dict) and r.get("strategy") == strategy_id]
    if not rows:
        raise ValueError(f"no rows for strategy_id '{strategy_id}' in source")
    if classification and classification.upper() != "ALL":
        rows = [r for r in rows if r.get("classification") == classification]
    if symbol:
        rows = [r for r in rows if str(r.get("symbol")) == symbol]
    if timeframe:
        rows = [r for r in rows if str(r.get("timeframe")) == timeframe]
    # only rows that actually carry real lockbox metrics
    rows = [r for r in rows if (r.get("summary") or {}).get("lockbox_oos")]
    if not rows:
        raise ValueError("no rows with real lockbox_oos metrics after filtering (refusing to emit empty/fake artifact)")

    rows = rows[:max_rows]
    mapped = [map_row(r, strategy_id, profile, run_id, source_rel, cost_bps) for r in rows]

    try:
        smod = datetime.fromtimestamp(source_path.stat().st_mtime, tz=timezone.utc).isoformat()
    except OSError:
        smod = None

    doc = {
        "schema_version": "1.0",
        "run_id": run_id,
        "read_only": True,
        "no_execution": True,
        "generated_by": "build_profile_result_artifact.py (read-only converter)",
        "conversion_timestamp": _now_iso(),
        "provenance": {
            "source_path": source_rel,
            "source_type": "deterministic_soak_mega_results",
            "source_modified_at": smod,
            "source_generated_utc": raw_doc.get("generated_utc"),
            "cost_bps": cost_bps,
            "fold_config": {k: cfg.get(k) for k in ("num_rolling_folds", "fold_train_fraction", "fold_test_fraction", "lockbox_fraction", "min_trades_for_pass")},
        },
        "profile_mapping": {
            "profile": profile,
            "rationale": "Soak ran raw source rules with a parameter sweep and no MTC risk normalization; mapped to SOURCE_NAKED. Override with --profile only with justification.",
            "is_interpretation": True,
        },
        "results": mapped,
    }
    notes.append(f"mapped {len(mapped)} real row(s); classification filter={classification or 'ALL'}")
    mism = [m["provenance"]["universe_mismatch"] for m in mapped if m["provenance"]["universe_mismatch"]]
    if mism:
        notes.append("UNIVERSE MISMATCH recorded: " + mism[0])
    if all(not m["robustness"]["robust_final"] for m in mapped):
        notes.append("all rows robust_final=false -> promotion_status RESEARCH_ONLY/NOT_PROMOTED (no robust claim)")
    return doc, notes


def validate(doc: dict) -> list[str]:
    if validate_json_schema is None:
        return ["validator unavailable"]
    schema_path = SCHEMA_DIR / "backtest_profile_result.schema.json"
    if not schema_path.exists():
        return ["schema missing"]
    return [f"{i.path}: {i.message}" for i in validate_json_schema(doc, _read_json(schema_path))]


def _resolve_under_backtest_root(path: Path) -> Path:
    candidate = path if path.is_absolute() else (Path.cwd() / path)
    candidate = candidate.resolve()
    root = BACKTEST_ROOT.resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"output directory must resolve under {root}") from exc
    return candidate


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Review/artifact writer for one backtest_profile_result.json from real soak data.")
    p.add_argument("--strategy-id", required=True)
    p.add_argument("--source-path", required=True)
    p.add_argument("--run-id", default=None)
    p.add_argument("--profile", default="SOURCE_NAKED")
    p.add_argument("--classification", default="PASS", help="filter by source classification, or ALL")
    p.add_argument("--symbol", default=None)
    p.add_argument("--timeframe", default=None)
    p.add_argument("--max-rows", type=int, default=10)
    p.add_argument("--output-dir", default=None)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true", help="write the artifact; default is no-write")
    p.add_argument("--force", action="store_true", help="allow overwriting an existing backtest_profile_result.json")
    args = p.parse_args(argv)

    if args.profile not in OFFICIAL_PROFILES:
        print(f"[ERROR] invalid profile {args.profile}; allowed {OFFICIAL_PROFILES}")
        return 2

    source_path = Path(args.source_path)
    if not source_path.is_absolute():
        source_path = (MCC_ROOT / args.source_path).resolve()
    if not source_path.is_file():
        print(f"[ERROR] source not found: {source_path}")
        return 2

    run_id = args.run_id or f"profileresult_{source_path.stem}"
    try:
        doc, notes = build_document(source_path, args.strategy_id, args.profile, run_id,
                                    args.classification, args.symbol, args.timeframe, args.max_rows)
    except ValueError as exc:
        print(f"[STOP] {exc}")
        return 4  # insufficient/refused source -> no artifact

    issues = validate(doc)
    print(f"run_id          : {run_id}")
    print(f"strategy_id     : {args.strategy_id}")
    print(f"profile         : {args.profile}")
    print(f"rows mapped     : {len(doc['results'])}")
    for n in notes:
        print(f"note            : {n}")
    print(f"schema valid    : {'YES' if not issues else 'NO -> ' + str(issues)}")

    if issues:
        print("[ERROR] schema validation failed; not writing.")
        return 3

    default_dir = BACKTEST_ROOT / f"pilot_profile_result_{args.strategy_id}_{datetime.now().strftime('%Y-%m-%d')}"
    try:
        out_dir = _resolve_under_backtest_root(Path(args.output_dir) if args.output_dir else default_dir)
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 5
    print(f"output_dir      : {out_dir}")

    if args.dry_run:
        print("[DRY-RUN] no files written.")
        return 0
    if not args.apply:
        print("[NO-WRITE] no files written. Re-run with --apply to write the artifact.")
        return 0

    target = out_dir / "backtest_profile_result.json"
    if target.exists() and not args.force:
        print(f"[ERROR] output exists; not overwriting without --force: {target}")
        return 5
    out_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"[OK] wrote backtest_profile_result.json into {out_dir}")
    print("[NOTE] read-only pilot from real soak data; no backtest run, no fabricated KPIs. Refresh /api/snapshot?refresh=1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
