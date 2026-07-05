#!/usr/bin/env python3
"""
overnight_v2_multiasset_20260702.py

Runs the FULL 43-strategy set (20 mega + 23 v2 monkey-patch) across the multi-asset
universe. The 23 v2 strategies were designed 2026-05-30 for the crypto-era data and
have NEVER been swept on native_multiasset_alpaca_2026-06-28 (the 06-29 run was mega's
20 only) -> genuinely-NEW compute, not a deterministic re-run (A19/A22 compliant).

Fixes A23 (LESSONS_2026-07-01): mega's SYMBOLS/TIMEFRAMES are hardcoded LEGACY and the
manifest binds DATA only, so the universe must be overridden from the manifest.

Importing overnight_v2_runner applies its GRIDS/build_signals patch WITHOUT running
main (its main is __name__-guarded). Promotes nothing.
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
import overnight_v2_runner as v2  # noqa: E402  (module-level import patches 43 strategies; main is guarded)

# A23 fix: override the hardcoded legacy universe with the manifest-derived one.
try:
    _m = json.loads(Path(mw.BUNDLE_MANIFEST).read_text(encoding="utf-8"))
    _ds = _m.get("datasets", [])
    _syms = sorted({d["symbol"] for d in _ds if d.get("symbol")})
    _tfs = sorted({d["timeframe_normalized"] for d in _ds if d.get("timeframe_normalized")})
    if _syms:
        mw.SYMBOLS = _syms
    if _tfs:
        mw.TIMEFRAMES = _tfs
    print(f"[v2-multiasset] universe: {len(_syms)} symbols x {len(_tfs)} tfs; "
          f"GRIDS={len(mw.GRIDS)} strategies", flush=True)
except Exception as _e:  # pragma: no cover
    print(f"[v2-multiasset] WARNING: universe override failed: {_e}", flush=True)

if __name__ == "__main__":
    # Run ONLY the 23 v2 strategies (never swept on multiasset). Do NOT re-run mega's
    # 20 — those were swept 06-29 and re-running is deterministic (A22 violation).
    if "--strategy" not in sys.argv:
        for sid in v2.NEW_GRIDS:
            sys.argv += ["--strategy", sid]
        print(f"[v2-multiasset] targeting {len(v2.NEW_GRIDS)} v2-only strategies (mega's 20 excluded — already done 06-29)", flush=True)
    mw.main()
