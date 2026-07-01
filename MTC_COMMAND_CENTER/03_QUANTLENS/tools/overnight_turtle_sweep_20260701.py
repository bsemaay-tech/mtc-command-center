#!/usr/bin/env python3
"""
overnight_turtle_sweep_2026-07-01.py  (Faz-3 validation, genuinely-NEW)

Runs the NEW GEN_DONCHIAN_TURTLE variant through the canonical walk-forward engine
across the full universe. This is genuinely-new compute (the variant was created
2026-07-01 and has never been backtested) — NOT a deterministic re-run of the base
sweep (A19/A22 compliant).

Pattern mirrors overnight_v2_runner.py: import mega, apply the variant monkey-patch,
then hand off to mega_walk_forward.main(). All mega CLI args pass through, so the
orchestrator can add --symbol/--tf/--resume/--checkpoint-every and env
(MEGA_WORKERS / MEGA_OUTPUT_DIR / MEGA_BUNDLE_MANIFEST).

NOTHING promotable. Promotion still requires robust_final downstream.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# Bulletproof the data binding BEFORE importing mega (mega reads the env at import).
# mega's default SYMBOLS/TIMEFRAMES are a hardcoded LEGACY crypto universe, and the
# manifest only supplies data — so we must also override the sweep universe below.
_DEFAULT_MANIFEST = (
    r"C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\data"
    r"\native_multiasset_alpaca_2026-06-28\manifests\dataset_manifest.json"
)
os.environ.setdefault("MEGA_BUNDLE_MANIFEST", _DEFAULT_MANIFEST)

import mega_walk_forward as mw  # noqa: E402
import variant_missing_knobs as variant  # noqa: E402

# Override the hardcoded legacy universe with the FULL multi-asset universe from the
# bound manifest (mega:81/87 SYMBOLS/TIMEFRAMES are legacy 17-crypto x 5-TF; the sweep
# iterates these unless --symbol/--tf are passed). Derived from the manifest = correct data.
try:
    _m = json.loads(Path(mw.BUNDLE_MANIFEST).read_text(encoding="utf-8"))
    _ds = _m.get("datasets", [])
    _syms = sorted({d["symbol"] for d in _ds if d.get("symbol")})
    _tfs = sorted({d["timeframe_normalized"] for d in _ds if d.get("timeframe_normalized")})
    if _syms:
        mw.SYMBOLS = _syms
    if _tfs:
        mw.TIMEFRAMES = _tfs
    print(f"[turtle-runner] universe from manifest: {len(_syms)} symbols x {len(_tfs)} tfs {_tfs}", flush=True)
except Exception as _e:  # pragma: no cover
    print(f"[turtle-runner] WARNING: could not derive universe from manifest: {_e}", flush=True)

# Apply at MODULE level (not under __main__): on Windows spawn, worker processes
# re-import this module by name and must also get the variant patch into their mega.
variant.apply()  # registers GEN_DONCHIAN_TURTLE in mw.GRIDS + wraps build_signals

if __name__ == "__main__":
    # Default: limit the sweep to the variant only (genuinely-new). Callers may append
    # more mega args; if no --strategy is supplied we inject the variant id.
    if "--strategy" not in sys.argv:
        sys.argv += ["--strategy", "GEN_DONCHIAN_TURTLE"]
    print(f"[turtle-runner] GRIDS={len(mw.GRIDS)} strategies; running "
          f"{sys.argv[sys.argv.index('--strategy') + 1:]}", flush=True)
    mw.main()
