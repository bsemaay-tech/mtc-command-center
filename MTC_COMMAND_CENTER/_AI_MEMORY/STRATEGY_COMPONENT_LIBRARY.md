# Strategy & Component Library (human-readable index)

Concise map of what exists for strategy research. The **machine-readable source
of truth** is the registries in `05_REGISTRY/`; this file is the quick read.
Counts below are a snapshot — regenerate with
`python 03_QUANTLENS/tools/build_strategy_research_registry.py` and view live in
the **Strategy Research Lab** dashboard tab.

## Inventory snapshot
- **46 strategies** in `03_QUANTLENS/strategies/STGxxx/` (each its own folder).
  Category: day_trading 16, swing_trading 4, **review_needed 26** (mostly 1d
  strategies awaiting confirmation).
- **23 indicators**, **78 reusable components**, controlled-vocab + harvested tags.

## Strategies by method (heuristic)
- trend_following (7), pullback_continuation (7), breakout (7)
- reversal (4), volatility_expansion (3), hybrid (3)
- momentum (2), support_resistance (2), mean_reversion (1)
- **review_needed (18)** — confirm before relying on the method tag.

## Most-used indicators
EMA (7), AVWAP (5), SMA (5), RSI (4), CANDLESTICK (3), GAP (3), OPENING_RANGE (3),
VCP (3), SUPPORT_RESISTANCE (2), RELATIVE_STRENGTH (2). Full list in
`05_REGISTRY/INDICATOR_REGISTRY.json`.

## Reusable components (by type)
confirmation_filter (21), entry_signal (18), exit_signal (15), trailing_module (12),
regime_filter (10), plus ATR stop-loss and fixed-R take-profit modules. See
`05_REGISTRY/COMPONENT_REGISTRY.json`.

## Combination guidance (start here)
**Good candidates to combine:**
- Trend filter (EMA/SMA) + pullback entry (RSI / AVWAP reclaim) + ATR stop + fixed-R TP.
- Regime filter (volatility / RS) gating a breakout entry (OPENING_RANGE / VCP).
- Signal-scoring ensemble across momentum (RSI/MACD/QQE) + structure (SR/Fib).

**Risky / likely redundant:**
- Stacking multiple momentum oscillators (RSI + QQE + MACD) — correlated, false confidence.
- Two trend filters (EMA + SMA) — redundant; pick one.

**Combine only with care:**
- MARKET_STRUCTURE / CHART_PATTERN / DIVERGENCE entries — **high repaint risk**;
  validate on closed bars before trusting backtests.
- AVWAP / VWAP anchored components — anchor choice changes results materially.

## Known risks
- **Repaint**: MARKET_STRUCTURE (CHoCH), CHART_PATTERN (wedge/flag), DIVERGENCE.
- **Lookahead**: any rolling high/low must shift `[1]`; HTF values only post-close.
- **TV mismatch**: RMA/Wilder vs SMA smoothing; session/timezone for intraday.
- See `STRATEGY_CODE_REVIEW_CHECKLIST.md`.

## Recommended starting points
1. `breakout_pullback_hybrid` on the day_trading set (OPENING_RANGE + AVWAP + ATR).
2. `signal_scoring_ensemble` on swing 1h set (EMA trend + RSI pullback + SR).
3. First resolve the 26 `review_needed` categories (see NEXT_STEPS) to widen the pool.

## Next read
`STRATEGY_RESEARCH_WORKFLOW.md` → the step-by-step research process.
