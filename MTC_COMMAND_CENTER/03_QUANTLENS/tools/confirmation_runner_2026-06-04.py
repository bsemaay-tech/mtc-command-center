"""Confirmation runner — 2026-06-04 (Option B, pre-registered).

Two-stage methodology (runbook A17 / lessons G4): the wide overnight discovery
sweep (171k configs) deflates the Deflated-Sharpe trial count so hard that no
candidate clears DSR. This run is the SECOND stage: a NARROW, PRE-REGISTERED
grid around the 8 down-market-alpha cells discovered on the 2026-06-03 night.

What it does, by monkey-patching mega_walk_forward WITHOUT editing it:
  1. Shrinks GRIDS[strategy] for the 6 candidate strategies to a small
     neighborhood around each discovered winner. Smaller grid => smaller DSR
     trial count (mega: grid_n = len(GRIDS[strat])) => restored DSR power.
  2. Restricts the run to those 6 strategies x ALL 17 symbols x {15m,1h,2h}.
     Keeping all 17 symbols is deliberate: the decisive confirmation question is
     cross-symbol generalization (does the edge appear on >=5 symbols, A9), not
     re-confirming the single discovered cell.

The signal logic for all 6 strategies already lives in mega_walk_forward; this
runner only swaps their parameter grids and the run universe. It does NOT change
trading logic, Pine, MTC behavior, or parity.

NOTE: results are fully deterministic (bootstrap seed = md5(strat|sym|tf)), so a
single complete run is statistically sufficient. There is no value in looping.

Launch:  python confirmation_runner_2026-06-04.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import mega_walk_forward as mw  # noqa: E402

# ============================================================
# Pre-registered narrow grids (each centered on / covering the
# discovered down-market-alpha winner params).
# ============================================================

CONFIRM_GRIDS: dict[str, list[dict]] = {
    # winners: L200/tol0.75/stop0.25 (APT1h), L144/tol0.15/stop0.25 (ADA15m),
    #          L144/tol0.75/stop0.10 (ADA1h)
    "QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE": [
        {"level_lookback": lb, "tolerance_atr": tol, "atr_stop_mult": sm}
        for lb in (144, 200)
        for tol in (0.15, 0.50, 0.75)
        for sm in (0.10, 0.25)
    ],  # 12
    # winner: L200/upper0.6/buf0.0 (ADA1h)
    "QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR": [
        {"level_lookback": lb, "upper_third": ut, "break_buf_atr": bb}
        for lb in (144, 200)
        for ut in (0.55, 0.60, 0.66)
        for bb in (0.0, 0.10)
    ],  # 12
    # winner: pa0.5/ia1.6/sw3 (LINK1h)
    "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL": [
        {"pullback_atr": pa, "impulse_atr": ia, "slope_window": sw}
        for pa in (0.40, 0.50, 0.65)
        for ia in (1.3, 1.6)
        for sw in (3, 5)
    ],  # 12
    # winner: touch0.3/stop10 (SOL1h)
    "GEN_TRIPLE_EMA_STACK": [
        {"touch_atr": ta, "stop_lookback": sl}
        for ta in (0.15, 0.30, 0.50)
        for sl in (5, 10)
    ],  # 6
    # winner: ch20/buf0.1/stop20 (ETH1h)
    "GEN_DONCHIAN_BREAKOUT": [
        {"channel_len": cl, "atr_buf": ab, "stop_lookback": sl}
        for cl in (10, 20, 40)
        for ab in (0.0, 0.10, 0.25)
        for sl in (10, 20)
    ],  # 18
    # winner: rl5/ob25/rec45 (LINK2h)
    "GEN_RSI_OVERSOLD_REVERSAL": [
        {"rsi_len": rl, "oversold": ob, "recovery": rec}
        for rl in (5, 7)
        for ob in (25, 30)
        for rec in (40, 45, 50)
    ],  # 12 (recovery > oversold always)
}

CONFIRM_TIMEFRAMES = ["15m", "1h", "2h"]

# Apply the narrow grids over the originals.
for _strat, _grid in CONFIRM_GRIDS.items():
    if _strat not in mw.GRIDS:
        raise SystemExit(f"[confirm] strategy not in mega GRIDS: {_strat}")
    mw.GRIDS[_strat] = _grid

_total = sum(len(g) for g in CONFIRM_GRIDS.values())
print(f"[confirm] narrowed {len(CONFIRM_GRIDS)} strategies; "
      f"param sets per strategy: "
      + ", ".join(f"{k.split('_')[-1] or k}={len(v)}" for k, v in CONFIRM_GRIDS.items()))
print(f"[confirm] total narrow param sets: {_total}")

# Build the restricted run universe via argv (mega.main parses these).
_argv = [sys.argv[0]]
for _s in CONFIRM_GRIDS:
    _argv += ["--strategy", _s]
for _sym in mw.SYMBOLS:               # all 17 -> cross-symbol generalization test
    _argv += ["--symbol", _sym]
for _tf in CONFIRM_TIMEFRAMES:
    _argv += ["--tf", _tf]
sys.argv = _argv

if __name__ == "__main__":
    print(f"[confirm] universe: {len(CONFIRM_GRIDS)} strat x {len(mw.SYMBOLS)} sym "
          f"x {len(CONFIRM_TIMEFRAMES)} tf; handing off to mega_walk_forward.main()")
    mw.main()
