#!/usr/bin/env python3
"""
overnight_variants_multiasset_20260702.py

Runs the Faz-3 missing-knob VARIANT FAMILY (variant_missing_knobs.NEW_GRIDS) across the
full multi-asset universe. All variants are NEW logic that has never been backtested →
genuinely-new (A19/A22 compliant). Targets ONLY the variant ids (not mega's 20, which
were swept 06-29 → re-running would be a deterministic A22 violation).

A23 fix: overrides mega's hardcoded legacy SYMBOLS/TIMEFRAMES from the manifest.
__main__ guard so Windows-spawn workers inherit the patch without recursing.
Promotes nothing.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

_DEFAULT_MANIFEST = (
    r"C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\data"
    r"\native_multiasset_alpaca_2026-06-28\manifests\dataset_manifest.json"
)
os.environ.setdefault("MEGA_BUNDLE_MANIFEST", _DEFAULT_MANIFEST)

import mega_walk_forward as mw  # noqa: E402
import variant_missing_knobs as variant  # noqa: E402
variant.apply()

try:
    _m = json.loads(Path(mw.BUNDLE_MANIFEST).read_text(encoding="utf-8"))
    _ds = _m.get("datasets", [])
    _syms = sorted({d["symbol"] for d in _ds if d.get("symbol")})
    _tfs = sorted({d["timeframe_normalized"] for d in _ds if d.get("timeframe_normalized")})
    if _syms:
        mw.SYMBOLS = _syms
    if _tfs:
        mw.TIMEFRAMES = _tfs
    print(f"[variants-multiasset] universe: {len(_syms)} symbols x {len(_tfs)} tfs; "
          f"variants: {list(variant.NEW_GRIDS)}", flush=True)
except Exception as _e:  # pragma: no cover
    print(f"[variants-multiasset] WARNING: universe override failed: {_e}", flush=True)

if __name__ == "__main__":
    if "--strategy" not in sys.argv:
        for sid in variant.NEW_GRIDS:
            sys.argv += ["--strategy", sid]
        print(f"[variants-multiasset] targeting {len(variant.NEW_GRIDS)} variant strategies", flush=True)
    mw.main()
