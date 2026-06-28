# US-Equities 10m — 8EMA-Pullback Full Param Sweep

**Date:** 2026-06-28
**Author:** Claude Opus 4.8
**Classification:** RESEARCH ONLY / NOT PROMOTABLE
**Strategy:** `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`
**Data:** native TradingView bundle `03_QUANTLENS/data/native_us_equities_10m_us3_tradingview_2026-06-28/` (SPY/QQQ/AAPL, 20,094 10m RTH bars each, 2024-06-03 → 2026-06-26)
**Method:** evaluated **all 75** grid configs (`grid_ema8_family`: pullback_atr × impulse_atr × slope_window) per symbol over (a) the full period and (b) the lockbox OOS (last 25%). Engine code reused unmodified (imported `build_signals`/`simulate_slice`); nothing written to `05_BACKTEST_RESULTS`.

## Goal

Before spending compute on a full soak (or touching protected engine session-gating), answer: **does ANY 8EMA config survive on native US-equities 10m?**

## Result

| Symbol | Buy&hold (full) | Configs net-positive full (of 75) | Positive & ≥30 trades | Beat B&H | Best full-period config | Best lockbox-OOS |
|---|---|---|---|---|---|---|
| SPY | +42.0% | **0** | 0 | 0 | pa0.3/ia1.6/sw3 → **−3.04%** (86 tr, PF 0.79) | −0.71% (10 tr) |
| QQQ | +57.2% | **0** | 0 | 0 | pa0.2/ia1.6/sw3 → **−3.33%** (36 tr, PF 0.47) | −1.93% (11 tr) |
| AAPL | +46.8% | **1** | 1 | 0 | pa0.2/ia1.6/sw3 → **+0.15%** (54 tr, PF 1.02) | +0.93% (16 tr, PF 1.45) |

### Survivors (full net>0 AND lockbox net>0 AND ≥30 trades)

Only **one**, and it is noise:

- `AAPL pa0.2/ia1.6/sw3`: full **+0.15%** over 2 years (PF 1.02 ≈ breakeven), lockbox +0.93% on **16** OOS trades (below the 30 floor). Buy&hold AAPL over the same window = **+46.8%**. The "edge" is ~300× smaller than just holding.

## Conclusion

**The 8EMA-pullback strategy does not work on SPY/QQQ/AAPL 10m over this window.**
- 149 of 150 symbol×config in-sample evaluations are net-negative.
- Zero configs beat buy&hold on any symbol.
- The lone positive config is statistically indistinguishable from breakeven and under-traded.

**Recommendation: do NOT run a full native soak with this strategy, and do NOT configure protected-scope equity-session gating for it yet.** The infrastructure (data → bundle → engine → OOS metrics) is proven working on native US-equities 10m; the *strategy itself* is the blocker now, not the pipeline.

### Options for Barış

1. **Shelve this strategy on US equities** — crypto-proxy already showed no robust edge; native 10m confirms it.
2. **Test a different strategy** on the same native bundle (the other `QL_2026-05-01_US_EQUITIES_INTRADAY_*` families, or a fresh idea) — reuse the bundle as-is.
3. **Change the window/regime** — e.g. open-only / first-N-bars sessions, different date slice — but in-sample is already fully negative, so low expected value.
4. If you still want a recorded native soak for documentation, it can be run — but it will record a NEGATIVE / non-robust result, not a promotable one.

No `backtest_profile_result.json` / `top_results.json` generated (no qualifying rows).
