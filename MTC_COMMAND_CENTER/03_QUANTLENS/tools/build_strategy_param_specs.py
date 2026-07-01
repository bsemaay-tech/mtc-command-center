#!/usr/bin/env python3
"""
build_strategy_param_specs.py  (Faz 1 — read-only)

Emit a declarative per-strategy PARAMETER SPEC registry so that:
  - the OPTIMIZABLE search grid of every strategy is visible (name, values, count, type),
  - the case-count arithmetic (grid x cells x folds) is explicit,
  - the HARDCODED (fixed, not swept) knobs are documented with rationale,
  - candidate MISSING knobs (Faz-3 new-logic) are flagged.

SINGLE SOURCE OF TRUTH:
  - optimizable grids            -> introspected from CODE: mega_walk_forward.GRIDS
  - global execution model       -> introspected from CODE: mega_walk_forward constants
  - rationale / fixed / missing  -> curated overlay: 05_REGISTRY/STRATEGY_PARAM_SPEC_ANNOTATIONS.json

This script READS ONLY. It never changes engine behavior, never runs a backtest,
never touches Pine/MTC_V2/parity. Re-run it whenever GRIDS or the overlay changes.

Usage:
  python build_strategy_param_specs.py            # writes 05_REGISTRY/STRATEGY_PARAM_SPECS.json
  python build_strategy_param_specs.py --check     # print summary, do not write
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                      # .../03_QUANTLENS/tools
QUANTLENS = HERE.parent                                     # .../03_QUANTLENS
MCC_ROOT = QUANTLENS.parent                                 # .../MTC_COMMAND_CENTER
REGISTRY = MCC_ROOT / "05_REGISTRY"
ANNOTATIONS_PATH = REGISTRY / "STRATEGY_PARAM_SPEC_ANNOTATIONS.json"
OUT_PATH = REGISTRY / "STRATEGY_PARAM_SPECS.json"
PRIMARY_BUNDLE = QUANTLENS / "data" / "native_multiasset_alpaca_2026-06-28"
PRIMARY_MANIFEST = PRIMARY_BUNDLE / "manifests" / "dataset_manifest.json"

# R-multiple profit target is a literal in simulate_slice (mega_walk_forward.py:544/558),
# not a module constant, so it is referenced explicitly here.
PROFIT_TARGET_R = 2.0
WARMUP_BARS = 20  # simulate_slice starts at s_idx + 20


def _infer_type(values):
    if all(isinstance(v, bool) for v in values):
        return "bool"
    if all(isinstance(v, int) and not isinstance(v, bool) for v in values):
        return "int"
    if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values):
        return "float"
    return "str"


def introspect_grid(grid: list[dict]) -> dict:
    """grid = list of param-dicts -> {param: {values, count, min, max, type}}."""
    params: dict[str, dict] = {}
    keys: list[str] = []
    for combo in grid:
        for k in combo:
            if k not in keys:
                keys.append(k)
    for k in keys:
        raw = [c[k] for c in grid if k in c]
        distinct = sorted(set(raw), key=lambda x: (str(type(x)), x))
        entry = {"values": distinct, "count": len(distinct), "type": _infer_type(distinct)}
        nums = [v for v in distinct if isinstance(v, (int, float)) and not isinstance(v, bool)]
        if nums:
            entry["min"] = min(nums)
            entry["max"] = max(nums)
        params[k] = entry
    return params


def load_universe() -> dict:
    """Read the primary bundle manifest -> symbols / timeframes / cells."""
    try:
        d = json.loads(PRIMARY_MANIFEST.read_text(encoding="utf-8"))
        ds = d.get("datasets") or []
        syms = sorted({x.get("symbol") for x in ds if x.get("symbol")})
        tfs = sorted({x.get("timeframe_normalized") for x in ds if x.get("timeframe_normalized")})
        return {
            "bundle": PRIMARY_BUNDLE.name,
            "symbols": len(syms),
            "timeframes": len(tfs),
            "timeframe_list": tfs,
            "cells": len(ds),
            "manifest_found": True,
        }
    except Exception as e:  # pragma: no cover - tolerant
        return {"bundle": PRIMARY_BUNDLE.name, "symbols": None, "timeframes": None,
                "cells": None, "manifest_found": False, "reason": f"{type(e).__name__}: {e}"}


def build() -> dict:
    sys.path.insert(0, str(HERE))
    import mega_walk_forward as mw  # noqa: E402  (grids + constants live here)

    grids = mw.GRIDS
    folds = int(getattr(mw, "NUM_ROLLING_FOLDS", 3))
    universe = load_universe()
    cells = universe.get("cells")

    ann_doc = {}
    ann_meta = {}
    if ANNOTATIONS_PATH.exists():
        ann_raw = json.loads(ANNOTATIONS_PATH.read_text(encoding="utf-8"))
        ann_doc = ann_raw.get("strategies", {})
        ann_meta = {k: ann_raw[k] for k in ("schema_version", "phase_legend") if k in ann_raw}

    execution_model = {
        "entry": "next bar open (fill at open[t+1] after signal at t)",
        "profit_target_R": PROFIT_TARGET_R,
        "holding_bar_limit": int(getattr(mw, "HOLDING_BAR_LIMIT", 96)),
        "cost_bps": float(getattr(mw, "COST_BPS", 8.0)),
        "warmup_bars": WARMUP_BARS,
        "default_direction": "long",
        "rolling_folds": folds,
        "fold_train_fraction": float(getattr(mw, "FOLD_TRAIN_FRACTION", 0.60)),
        "fold_test_fraction": float(getattr(mw, "FOLD_TEST_FRACTION", 0.20)),
        "lockbox_fraction": float(getattr(mw, "LOCKBOX_FRACTION", 0.25)),
        "min_bars_required": int(getattr(mw, "MIN_BARS_REQUIRED", 1500)),
        "min_trades_for_pass": int(getattr(mw, "MIN_TRADES_FOR_PASS", 30)),
        "note": "These apply to ALL strategies and are NOT optimized. Changing any of them is new logic (Faz 3), not tuning.",
    }

    strategies = []
    sum_grid = 0
    total_cases = 0
    for sid, grid in grids.items():
        gsize = len(grid)
        sum_grid += gsize
        cases = (gsize * cells * folds) if cells else None
        if cases:
            total_cases += cases
        a = ann_doc.get(sid, {})
        strategies.append({
            "strategy_id": sid,
            "grid_size": gsize,
            "optimizable": introspect_grid(grid),
            "cases_full_universe": cases,
            "cases_formula": "grid_size x cells x rolling_folds",
            "annotation_status": a.get("annotation_status", "todo"),
            "grid_rationale": a.get("grid_rationale", ""),
            "fixed_knobs": a.get("fixed_knobs", []),
            "missing_knobs": a.get("missing_knobs", []),
            "mtc_v2_parity": a.get("mtc_v2_parity", {"status": "not_mapped", "phase": "2-parity"}),
        })

    return {
        "schema_version": ann_meta.get("schema_version", "1.0"),
        "generated_utc": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "03_QUANTLENS/tools/build_strategy_param_specs.py",
        "source_of_truth": "mega_walk_forward.GRIDS (code) + STRATEGY_PARAM_SPEC_ANNOTATIONS.json (curated overlay)",
        "read_only": True,
        "phase_legend": ann_meta.get("phase_legend", {}),
        "universe": universe,
        "execution_model": execution_model,
        "library_totals": {
            "strategies": len(grids),
            "sum_grid_size": sum_grid,
            "cells": cells,
            "rolling_folds": folds,
            "total_cases_full_universe": total_cases or None,
        },
        "strategies": strategies,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="print summary, do not write")
    args = ap.parse_args()

    spec = build()
    lt = spec["library_totals"]
    print(f"[param-specs] strategies={lt['strategies']} sum_grid={lt['sum_grid_size']} "
          f"cells={lt['cells']} folds={lt['rolling_folds']} total_cases={lt['total_cases_full_universe']}")
    documented = sum(1 for s in spec["strategies"] if s["annotation_status"] == "documented")
    print(f"[param-specs] annotated: {documented}/{len(spec['strategies'])}")

    if args.check:
        print("[param-specs] --check: not writing.")
        return
    OUT_PATH.write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[param-specs] wrote {OUT_PATH.relative_to(MCC_ROOT)}")


if __name__ == "__main__":
    main()
