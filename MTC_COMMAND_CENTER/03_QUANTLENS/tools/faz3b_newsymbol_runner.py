#!/usr/bin/env python
"""FAZ 3B Stage-2 new-symbol confirmation runner (zero engine edit).

Injects the FROZEN Stage-1 winner as the ONLY GEN_KELTNER_BREAKOUT config, then
hands off to mega_walk_forward.main(). Implements the hard assertions required by
`00_AGENT_PROTOCOLS/FAZ3B_STAGE2_NEWSYMBOL_CONFIRM_PREREG_2026-07-15.md` §9.1 so a
mis-scoped run cannot start.

APPROVAL-GATED. Importing this module patches nothing and runs nothing. `main()`
refuses to start unless --i-have-approval is passed, which a human may only do
AFTER the pre-registration has passed Gate-5 and Barış has approved it in writing.
Nothing here authorises a download, a run, or a promotion.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

import mega_walk_forward as mw  # noqa: E402

STRATEGY = "GEN_KELTNER_BREAKOUT"
TIMEFRAME = "1h"
# FROZEN Stage-1 winner — the ONLY configuration that decides (pre-reg §3).
FROZEN_CONFIG = {"ema_len": 50, "atr_len": 10, "mult": 2.0}
# Diagnostic-only star neighbours (pre-reg §3): they never decide; the gauntlet
# uses them for neighbourhood stability + the PBO config matrix.
STAR_CONFIGS = [
    {"ema_len": 20, "atr_len": 10, "mult": 2.0},
    {"ema_len": 50, "atr_len": 20, "mult": 2.0},
    {"ema_len": 50, "atr_len": 10, "mult": 1.5},
    {"ema_len": 50, "atr_len": 10, "mult": 2.5},
]
EXIT_MODES = ["fixed_2R", "trail_ema8"]  # ordered; twin + candidate
# Frozen symbol universe, 4 diversity groups (pre-reg §4). Verified 2026-07-15
# absent from every GEN_KELTNER_BREAKOUT row in 05_BACKTEST_RESULTS/ + research/.
SYMBOL_GROUPS = {
    "G1_us_nontech": ["JPM", "XOM", "JNJ", "PG"],
    "G2_international": ["EWJ", "EWG", "INDA", "EWZ"],
    "G3_broad_factor": ["RSP", "QUAL", "MTUM", "USMV"],
    "G4_sector_theme": ["SMH", "XBI", "KRE", "XOP"],
}
SYMBOLS = [s for g in SYMBOL_GROUPS.values() for s in g]
EXPECTED_ROWS = len(SYMBOLS) * len(EXIT_MODES)  # 32


def frozen_grid() -> list[dict]:
    """The injected grid: exactly ONE config. No selection happens on new data."""
    return [dict(FROZEN_CONFIG)]


def assert_scope(argv: list[str], manifest_path: str, out_dir: Path, symbols=None) -> None:
    """Pre-reg §9.1 hard assertions — refuse to start a mis-scoped run."""
    symbols = symbols or SYMBOLS
    if len(symbols) != len(set(symbols)):
        raise SystemExit("ABORT: duplicate symbol in the frozen universe")
    if len(frozen_grid()) != 1 or frozen_grid()[0] != FROZEN_CONFIG:
        raise SystemExit("ABORT: the decision grid must be exactly the frozen winner")
    if os.environ.get("MEGA_GRID_STRIDE"):
        raise SystemExit("ABORT: MEGA_GRID_STRIDE must be unset (stride 1)")
    modes = os.environ.get("MEGA_EXIT_MODES", "")
    if modes.split(",") != EXIT_MODES:
        raise SystemExit(f"ABORT: MEGA_EXIT_MODES must be exactly {','.join(EXIT_MODES)}, got {modes!r}")
    if not manifest_path or not Path(manifest_path).exists():
        raise SystemExit("ABORT: MEGA_BUNDLE_MANIFEST must resolve to an existing manifest")
    if out_dir.exists() and any(out_dir.iterdir()):
        raise SystemExit(f"ABORT: output dir {out_dir} must be empty/new")
    for tf_flag in ("--tf", "--timeframe"):
        if tf_flag in argv:
            got = argv[argv.index(tf_flag) + 1]
            if got != TIMEFRAME:
                raise SystemExit(f"ABORT: timeframe must be {TIMEFRAME}, got {got!r}")
    # engine worktree must be clean at the approved commit
    try:
        dirty = subprocess.run(["git", "status", "--porcelain", "--", str(TOOLS_DIR / "mega_walk_forward.py")],
                               capture_output=True, text=True, cwd=str(TOOLS_DIR)).stdout.strip()
        if dirty:
            raise SystemExit("ABORT: engine mega_walk_forward.py is dirty — commit or restore before a run")
    except FileNotFoundError:
        pass  # git unavailable; the caller must verify manually


def manifest_digest(manifest_path: str) -> str:
    return hashlib.sha256(Path(manifest_path).read_bytes()).hexdigest()


def apply() -> None:
    """Inject the frozen config as the ONLY grid for the strategy (zero engine edit)."""
    mw.GRIDS[STRATEGY] = frozen_grid()


def main() -> int:  # pragma: no cover - approval-gated real-data entrypoint
    if "--i-have-approval" not in sys.argv:
        raise SystemExit(
            "REFUSED: this runner is approval-gated. It may only run after "
            "FAZ3B_STAGE2_NEWSYMBOL_CONFIRM_PREREG_2026-07-15.md passes Gate-5 AND Barış "
            "approves it in writing. Nothing about importing or reading this file authorises a run."
        )
    sys.argv.remove("--i-have-approval")
    manifest_path = os.environ.get("MEGA_BUNDLE_MANIFEST", "")
    out_dir = Path(os.environ.get("MEGA_OUTPUT_DIR", TOOLS_DIR / "faz3b_newsymbol_out"))
    assert_scope(sys.argv, manifest_path, out_dir)
    apply()
    print(f"[faz3b-newsymbol] frozen config={FROZEN_CONFIG} | symbols={len(SYMBOLS)} "
          f"| exits={EXIT_MODES} | expected rows={EXPECTED_ROWS} "
          f"| manifest_sha256={manifest_digest(manifest_path)[:16]}", flush=True)
    if "--symbol" not in sys.argv:
        for s in SYMBOLS:
            sys.argv += ["--symbol", s]
    if "--strategy" not in sys.argv:
        sys.argv += ["--strategy", STRATEGY]
    if "--tf" not in sys.argv:
        sys.argv += ["--tf", TIMEFRAME]
    return mw.main()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
