#!/usr/bin/env python3
"""
overnight_archetypes_20260703.py — run the 5 NEW research archetypes across the full
multi-asset universe (genuinely-new logic). A23 fix (universe override) + __main__ guard.
Targets ONLY the new archetype ids. Promotes nothing.
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
import research_archetypes_20260703 as arch  # noqa: E402
arch.apply()

try:
    _m = json.loads(Path(mw.BUNDLE_MANIFEST).read_text(encoding="utf-8"))
    _ds = _m.get("datasets", [])
    _syms = sorted({d["symbol"] for d in _ds if d.get("symbol")})
    _tfs = sorted({d["timeframe_normalized"] for d in _ds if d.get("timeframe_normalized")})
    if _syms:
        mw.SYMBOLS = _syms
    if _tfs:
        mw.TIMEFRAMES = _tfs
    # Deeper walk-forward for the confirmation-grade discovery (6 rolling folds vs default 3):
    # more OOS rigor + more genuinely-new compute. Overridable via MEGA_FOLDS env.
    import os as _os
    mw.NUM_ROLLING_FOLDS = int(_os.environ.get("MEGA_FOLDS", "6"))
    print(f"[archetypes-run] universe: {len(_syms)}x{len(_tfs)}; folds={mw.NUM_ROLLING_FOLDS}; "
          f"archetypes: {list(arch.NEW_GRIDS)}", flush=True)
except Exception as _e:  # pragma: no cover
    print(f"[archetypes-run] WARNING: universe override failed: {_e}", flush=True)

if __name__ == "__main__":
    if "--strategy" not in sys.argv:
        for sid in arch.NEW_GRIDS:
            sys.argv += ["--strategy", sid]
    mw.main()
