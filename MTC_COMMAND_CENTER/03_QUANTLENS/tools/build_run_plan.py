"""build_run_plan.py

Generate a DRAFT, REVIEW-ONLY run_plan.json (+ artifact_index.json + run_plan.md)
for a single strategy so the dashboard can display a real backtest plan instead of
"Pending run_plan.json".

This tool does NOT run backtests, does NOT trigger execution, does NOT touch Pine /
MTC_V2 / the backtest engine / brokers, and adds no write API. It only emits planning
artifacts that the read-only dashboard reader (`night_artifacts_reader.py`) discovers
under 03_QUANTLENS/05_BACKTEST_RESULTS/<run_id>/.
Default behavior is no-write. Writing review artifacts requires explicit `--apply`,
is limited to 03_QUANTLENS/05_BACKTEST_RESULTS, and refuses overwrite unless
`--force` is supplied.

Generated run_plan is always marked:
    status = "draft_pending_approval"
    approval.human_review_required = true
    approval.approved = false
    approval.execution_allowed = false

No backtest KPIs and no profile-separated performance results are produced.

Usage:
    python 03_QUANTLENS/tools/build_run_plan.py --strategy-id QL_... [--apply] [--force]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

MCC_ROOT = Path(__file__).resolve().parents[2]
BACKTEST_ROOT = MCC_ROOT / "03_QUANTLENS" / "05_BACKTEST_RESULTS"
REGISTRY_FILE = MCC_ROOT / "05_REGISTRY" / "STRATEGY_REGISTRY.json"
SCHEMA_DIR = MCC_ROOT / "06_SCHEMAS"

# Reuse the dashboard's read-only schema validator (no execution code imported).
sys.path.insert(0, str(MCC_ROOT / "08_DASHBOARD_APP" / "apps" / "api"))
try:
    from mcc_readonly.schema import validate_json_schema  # type: ignore
except Exception:  # pragma: no cover - validator optional
    validate_json_schema = None  # type: ignore

OFFICIAL_PROFILES = ["SOURCE_NAKED", "RISK_NORMALIZED", "MTC_LIGHT", "FULL_MTC_CANDIDATE"]
DEFAULT_TIMEFRAMES = ["15m", "1h", "4h", "1D"]

# Expected night-run output artifacts (planning contract; none produced here).
EXPECTED_OUTPUTS = [
    ("run_status.json", "status", "run_status.schema.json", "Backtest Runs"),
    ("progress.json", "status", None, "Backtest Runs"),
    ("heartbeat.json", "status", None, "Backtest Runs"),
    ("backtest_profile_result.json", "result", "backtest_profile_result.schema.json", "Backtest Result Explorer"),
    ("top_results.json", "result", "top_results.schema.json", "Strategy Leaderboard"),
    ("leaderboard_delta.json", "leaderboard", None, "Strategy Leaderboard"),
    ("benchmark_update_candidate.json", "leaderboard", None, "Strategy Leaderboard"),
    ("morning_report.md", "report", None, "Reports"),
]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_registry_entry(strategy_id: str) -> dict | None:
    if not REGISTRY_FILE.exists():
        return None
    try:
        data = _read_json(REGISTRY_FILE)
    except Exception as exc:  # pragma: no cover
        print(f"[WARN] could not parse registry: {exc}")
        return None
    entries = []
    for key in ("candidates", "strategies"):
        if isinstance(data.get(key), list):
            entries.extend(data[key])
    base = strategy_id.split("|")[0]
    for e in entries:
        eid = e.get("id") or e.get("candidate_id") or e.get("strategy_id")
        if str(eid) == strategy_id or str(eid).split("|")[0] == base:
            return e
    # Fallback: the built (read-only) registry resolves more candidates than the raw file.
    try:
        from mcc_readonly.registry_reader import build_strategy_registry  # type: ignore
        built = build_strategy_registry(MCC_ROOT)
        for key in ("candidates", "strategies"):
            for e in (built.get(key) or []):
                eid = e.get("id") or e.get("candidate_id") or e.get("strategy_id")
                if str(eid) == strategy_id or str(eid).split("|")[0] == base:
                    return e
    except Exception as exc:  # pragma: no cover
        print(f"[WARN] built-registry fallback failed: {exc}")
    return None


def short_id(strategy_id: str) -> str:
    base = strategy_id.split("|")[0]
    return base[-40:] if len(base) > 40 else base


def build_parameter_space(entry: dict | None) -> dict:
    """Draft parameter space. Unfrozen rules are explicitly NEEDS_FREEZE, never faked
    into numeric sweeps."""
    return {
        "state": "draft",
        "note": "Draft only. Numeric sweeps require source rule-freeze before any run.",
        "params": {
            "primary_length": {"values": [], "state": "needs_freeze", "source": "strategy_source"},
            "entry_threshold": {"values": [], "state": "needs_freeze", "source": "strategy_source"},
            "stop_loss": {"values": [], "state": "needs_freeze", "source": "missing"},
            "take_profit_r": {"values": [], "state": "needs_freeze", "source": "strategy_source"},
        },
    }


def estimate_case_count(param_space: dict, symbols: list[str], timeframes: list[str], profiles: list[str], max_cases: int) -> dict:
    resolved = 1
    unresolved = 0
    for spec in param_space.get("params", {}).values():
        vals = spec.get("values") or []
        if vals:
            resolved *= len(vals)
        else:
            unresolved += 1
    grid = resolved * max(len(symbols), 1) * max(len(timeframes), 1) * max(len(profiles), 1)
    capped = grid > max_cases
    return {
        "estimate": min(grid, max_cases),
        "raw_estimate": grid,
        "capped": capped,
        "max_cases": max_cases,
        "unresolved_params": unresolved,
        "note": "Estimate excludes unresolved (needs_freeze) params; real count pending rule-freeze.",
    }


def build_universe(symbols: list[str], symbol_source: str) -> dict:
    """Explicit universe state. Never invents a symbol. Unresolved universe is allowed
    but must be flagged needs_freeze so approval is blocked until symbols are frozen."""
    if symbols:
        return {
            "status": "draft",
            "source": symbol_source,
            "reason": "Symbol universe resolved (draft); freeze and validate before approval.",
        }
    return {
        "status": "needs_freeze",
        "source": "unresolved",
        "reason": "No validated symbol universe found in registry/source metadata. Provide --symbols before approval.",
    }


def build_run_plan(strategy_id: str, entry: dict | None, profiles: list[str], symbols: list[str],
                   timeframes: list[str], max_cases: int, run_id: str, symbol_source: str = "unknown") -> dict:
    display_name = None
    source_artifacts: list[dict] = []
    if entry:
        display_name = entry.get("strategy_display_name") or entry.get("title") or entry.get("name")
        if entry.get("source_url"):
            source_artifacts.append({"type": "source_url", "ref": entry["source_url"]})
        if entry.get("transcript_path"):
            source_artifacts.append({"type": "transcript", "ref": entry["transcript_path"]})

    param_space = build_parameter_space(entry)
    case_count = estimate_case_count(param_space, symbols, timeframes, profiles, max_cases)
    universe = build_universe(symbols, symbol_source)

    return {
        "schema_version": "1.0",
        "run_id": run_id,
        "created_at": _now_iso(),
        "created_by": "build_run_plan.py (draft tool)",
        "read_only": True,
        "status": "draft_pending_approval",
        "strategy_id": strategy_id,
        "strategy_ids": [strategy_id],
        "strategy_display_name": display_name,
        "source_artifacts": source_artifacts,
        "profiles": profiles,
        "symbols": symbols,
        "universe": universe,
        "timeframes": timeframes,
        "parameter_space": param_space,
        "case_count": case_count["estimate"],
        "case_count_detail": case_count,
        "cost_scenarios": [
            {"name": "baseline", "state": "draft", "note": "Slippage/fees model pending."},
        ],
        "walk_forward": {"state": "draft", "note": "Walk-forward windows pending rule-freeze."},
        "smoke_test": {"required": True, "state": "draft", "note": "Smoke test must pass before any real run."},
        "risk_assumptions": {
            "state": "draft",
            "position_sizing": "NOT_DEFINED",
            "leverage": "NOT_DEFINED",
            "max_risk_per_trade": "NOT_DEFINED",
            "note": "Risk model not validated; do not infer as real.",
        },
        "missing_assumptions": [
            "stop_loss rule not extracted from source",
            "position sizing / leverage undefined",
            "numeric parameter ranges not frozen",
        ] + ([] if symbols else ["symbol universe unresolved (needs_freeze)"]),
        "rule_freeze_requirements": [
            "Freeze entry trigger numeric thresholds",
            "Freeze exit logic and stop placement",
            "Freeze risk/sizing model",
        ],
        "same_bucket_rule": "Compare results only within identical profile + timeframe + symbol universe + score method.",
        "no_execution": True,
        "no_execution_declaration": "This plan is review-only. It does not trigger any backtest, worker, broker, or trade.",
        "approval_required": True,
        "approval_state": "PENDING",
        "approval": {
            "human_review_required": True,
            "approved": False,
            "execution_allowed": False,
        },
        "expected_artifacts": [name for name, *_ in EXPECTED_OUTPUTS],
        "output_dir": f"03_QUANTLENS/05_BACKTEST_RESULTS/{run_id}",
    }


def build_artifact_index(run_id: str, run_dir: Path) -> dict:
    artifacts = [
        {
            "type": "run_plan",
            "path": f"03_QUANTLENS/05_BACKTEST_RESULTS/{run_id}/run_plan.json",
            "exists": True,
            "schema": "run_plan.schema.json",
            "consumed_by": ["Backtest Planner", "Strategy Intelligence", "Advanced Artifacts"],
            "required": True,
        },
        {
            "type": "artifact_index",
            "path": f"03_QUANTLENS/05_BACKTEST_RESULTS/{run_id}/artifact_index.json",
            "exists": True,
            "schema": "artifact_index.schema.json",
            "consumed_by": ["Advanced Artifacts", "Backtest Result Explorer"],
            "required": True,
        },
        {
            "type": "run_plan_md",
            "path": f"03_QUANTLENS/05_BACKTEST_RESULTS/{run_id}/run_plan.md",
            "exists": (run_dir / "run_plan.md").exists(),
            "schema": None,
            "consumed_by": ["Backtest Planner", "Reports"],
            "required": False,
        },
    ]
    consumer_map = {
        "status": "Backtest Runs", "result": "Backtest Result Explorer",
        "leaderboard": "Strategy Leaderboard", "report": "Reports",
    }
    for name, atype, schema, consumer in EXPECTED_OUTPUTS:
        artifacts.append({
            "type": name.replace(".json", "").replace(".md", ""),
            "path": f"03_QUANTLENS/05_BACKTEST_RESULTS/{run_id}/{name}",
            "exists": False,
            "schema": schema,
            "consumed_by": [consumer_map.get(atype, "Advanced Artifacts")],
            "required": False,
        })
    return {
        "schema_version": "1.0",
        "run_id": run_id,
        "root_dir": f"03_QUANTLENS/05_BACKTEST_RESULTS/{run_id}",
        "generated_at": _now_iso(),
        "read_only": True,
        "artifacts": artifacts,
    }


def build_run_plan_md(plan: dict) -> str:
    cc = plan["case_count_detail"]
    return f"""# Run Plan (DRAFT — review only) — {plan['run_id']}

> **NOT EXECUTED.** This is a read-only planning artifact. No backtest, worker, broker,
> or trade is triggered by this file. `execution_allowed = false`.

## Selected strategy
- **ID:** `{plan['strategy_id']}`
- **Display name:** {plan.get('strategy_display_name') or '(not extracted)'}
- **Status:** {plan['status']}

## Why selected
Manually selected via `build_run_plan.py` to seed the first real run-plan artifact for
dashboard verification. Selection is operator-driven, not a performance claim.

## Planned profiles
{', '.join(plan['profiles'])}

## Universe / timeframes
- Symbols: {', '.join(plan['symbols']) if plan['symbols'] else '(unresolved)'}
- Universe state: **{plan['universe']['status']}** — {plan['universe']['reason']}
- Timeframes: {', '.join(plan['timeframes'])}
{'' if plan['symbols'] else chr(10) + '> **Symbol universe is unresolved and must be frozen before execution approval.** No default symbol was injected.'}

## Estimated case count
- Estimate: **{cc['estimate']}** (raw {cc['raw_estimate']}, capped={cc['capped']}, max={cc['max_cases']})
- {cc['note']}

## Missing rule-freeze assumptions
{chr(10).join('- ' + x for x in plan['missing_assumptions'])}

## Required before a real backtest can run
{chr(10).join('- ' + x for x in plan['rule_freeze_requirements'])}
- Human review + approval (`approved` is currently false)
- Smoke test pass

## Why no execution is triggered
{plan['no_execution_declaration']}

## Same-bucket comparison rule
{plan['same_bucket_rule']}
"""


def validate(doc: dict, schema_name: str) -> list[str]:
    if validate_json_schema is None:
        return ["validator unavailable (jsonschema/mcc_readonly not importable)"]
    schema_path = SCHEMA_DIR / schema_name
    if not schema_path.exists():
        return [f"schema missing: {schema_name}"]
    schema = _read_json(schema_path)
    return [f"{i.path}: {i.message}" for i in validate_json_schema(doc, schema)]


def _resolve_output_root(path: Path) -> Path:
    candidate = path if path.is_absolute() else (Path.cwd() / path)
    candidate = candidate.resolve()
    root = BACKTEST_ROOT.resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"output root must resolve under {root}") from exc
    return candidate


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate a draft review-only run_plan.json for one strategy.")
    p.add_argument("--strategy-id", required=True)
    p.add_argument("--profiles", default=",".join(OFFICIAL_PROFILES))
    p.add_argument("--timeframes", default="")
    p.add_argument("--symbols", default="")
    p.add_argument("--max-cases", type=int, default=5000)
    p.add_argument("--run-id", default=None)
    p.add_argument("--output-root", default=str(BACKTEST_ROOT))
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true", help="write the review artifacts; default is no-write")
    p.add_argument("--force", action="store_true", help="allow overwriting existing run-plan artifacts")
    args = p.parse_args(argv)

    strategy_id = args.strategy_id
    entry = load_registry_entry(strategy_id)
    if entry is None:
        print(f"[WARN] strategy '{strategy_id}' not found in registry; continuing with provided args only.")

    profiles = [x.strip() for x in args.profiles.split(",") if x.strip()]
    invalid = [x for x in profiles if x not in OFFICIAL_PROFILES]
    if invalid:
        print(f"[ERROR] invalid profiles: {invalid}; allowed: {OFFICIAL_PROFILES}")
        return 2

    timeframes = [x.strip() for x in args.timeframes.split(",") if x.strip()]
    if not timeframes:
        tf = (entry or {}).get("timeframe")
        timeframes = [tf] if tf else list(DEFAULT_TIMEFRAMES)

    symbols = [x.strip() for x in args.symbols.split(",") if x.strip()]
    if symbols:
        symbol_source = "cli"
    else:
        # Resolve only from validated metadata. Never silently default (e.g. to BTCUSDT)
        # for a strategy whose universe is unknown or non-crypto (e.g. US_EQUITIES).
        sym = (entry or {}).get("symbol")
        symbols_meta = (entry or {}).get("symbols")
        if isinstance(symbols_meta, list) and symbols_meta:
            symbols = [str(s).strip() for s in symbols_meta if str(s).strip()]
            symbol_source = "registry"
        elif sym:
            symbols = [str(sym).strip()]
            symbol_source = "registry"
        else:
            symbols = []
            symbol_source = "unresolved"

    if not symbols:
        print("[WARN] symbol universe unresolved; run_plan.universe.status=needs_freeze. "
              "Provide --symbols before approval. (no default symbol injected)")

    run_id = args.run_id or f"draft_run_plan_{short_id(strategy_id)}_{datetime.now().strftime('%Y-%m-%d')}"
    try:
        output_root = _resolve_output_root(Path(args.output_root))
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 5
    run_dir = output_root / run_id

    plan = build_run_plan(strategy_id, entry, profiles, symbols, timeframes, args.max_cases, run_id, symbol_source)
    plan_issues = validate(plan, "run_plan.schema.json")
    index = build_artifact_index(run_id, run_dir)
    index_issues = validate(index, "artifact_index.schema.json")

    print(f"run_id            : {run_id}")
    print(f"strategy_id       : {strategy_id}")
    print(f"display_name      : {plan.get('strategy_display_name')}")
    print(f"profiles          : {profiles}")
    print(f"symbols           : {symbols}")
    print(f"timeframes        : {timeframes}")
    print(f"case_count est    : {plan['case_count']}")
    print(f"run_plan valid    : {'YES' if not plan_issues else 'NO -> ' + str(plan_issues)}")
    print(f"artifact_index ok : {'YES' if not index_issues else 'NO -> ' + str(index_issues)}")
    print(f"output_dir        : {run_dir}")

    if plan_issues or index_issues:
        print("[ERROR] schema validation failed; not writing artifacts.")
        return 3

    if args.dry_run:
        print("[DRY-RUN] no files written.")
        return 0
    if not args.apply:
        print("[NO-WRITE] no files written. Re-run with --apply to write review artifacts.")
        return 0

    targets = [run_dir / "run_plan.json", run_dir / "artifact_index.json", run_dir / "run_plan.md"]
    existing = [str(p) for p in targets if p.exists()]
    if existing and not args.force:
        print(f"[ERROR] output exists; not overwriting without --force: {existing}")
        return 5

    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "run_plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
    (run_dir / "artifact_index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    (run_dir / "run_plan.md").write_text(build_run_plan_md(plan), encoding="utf-8")
    print(f"[OK] wrote run_plan.json, artifact_index.json, run_plan.md into {run_dir}")
    print("[NOTE] review-only draft; execution_allowed=false. Refresh /api/snapshot?refresh=1 to surface.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
