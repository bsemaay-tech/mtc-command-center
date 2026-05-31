# FINAL_STRATEGY_CONTRACT — BigBeluga RSI Divergence + CHoCH + ATR

| # | Field | Value |
|---|---|---|
| 1 | Candidate ID | `BIGBELUGA_RSI_DIV_CHOCH_ATR_v1_CONTRACT` |
| 2 | Source file | `2026-05-03_XNZ4f-b3ED8_quantlens_intake_indicator_audit.md` (only authoritative source) |
| 3 | Source URL | https://youtu.be/XNZ4f-b3ED8 |
| 4 | Strategy family | reversal_structure / market_structure_trend_following (indicator-derived) |
| 5 | Native market | Asset-agnostic per indicator design (long+short symmetric) |
| 6 | Native timeframe | Indicator-agnostic; reasonable backtest timeframes 4h, 1D, 1W |
| 7 | Minimum data required | OHLC + RSI computable (close); no special data |
| 8 | Tradable universe | Liquid assets with enough swing structure (avoid ultra-thin) |
| 9 | Setup context | Confirmed pivot high (msLen=10 left & right) and pivot low exist; RSI divergence detected at swing-pivot level (lower price-pivot-low + higher RSI-pivot-low for bull; mirror for bear) |
| 10 | Entry trigger | `crossover(close, last_confirmed_pivot_high)` AND current direction != bull → bullish CHoCH; mirror for bearish |
| 11 | Confirmation | Direction state latched; only one entry per direction-flip |
| 12 | Filters | Optional macro trend gate (close > EMA200 for longs); optional minimum bars between flips (anti-whipsaw) |
| 13 | Initial stop | At divergence-pattern extreme (the swing low for bull entry; swing high for bear) |
| 14 | Profit target | ATR ladder: tp1 = entry + ATR×2; tp2 = entry + ATR×4; tp3 = entry + ATR×6 (`targetStepMult = 2`) |
| 15 | Time stop | Optional 50-bar time stop |
| 16 | Exit rules | ATR×4 trailing stop (chandelier-style from highest-high since entry) AND/OR opposite CHoCH AND/OR ladder TPs |
| 17 | Position sizing | Risk-based 0.5–1% per trade |
| 18 | Do-not-trade | No confirmed pivot in lookback; no divergence; bar count between consecutive flips below threshold |
| 19 | Ambiguities | Exact RSI divergence detection algorithm in BigBeluga Pine (intake notes verbal vs Pine differs); whether RSI divergence is hard prerequisite or visual hint |
| 20 | Mechanical confidence | 4 / 5 (indicator code is the source of truth — replicate exactly) |
| 21 | Data confidence | 4 / 5 (current crypto bundle works) |
| 22 | MTC compatibility | 3 / 5 (FSM with latched direction; ladder TP needs partial-exit support) |
| 23 | Testability | 4 / 5 once look-ahead-clean replication done |
| 24 | Was previous backtest fair? | **NO** |
| 25 | Deserves repaired test? | **YES** — but rebuild from indicator source, not from rolling-min approximation |
