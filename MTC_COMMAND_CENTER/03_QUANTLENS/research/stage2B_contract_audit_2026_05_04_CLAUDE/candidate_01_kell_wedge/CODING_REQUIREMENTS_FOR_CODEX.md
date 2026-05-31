# CODING_REQUIREMENTS_FOR_CODEX — Kell Wedge Pop

## Repaired Python prototype must include
1. **Pre-flush detector**: rolling window 30 bars, flag bars where `close < EMA20 − 1.5*ATR(20)`. Must store the *flush_low* timestamp+price for later higher-low comparison.
2. **Snapback flag**: after a flush, watch for a bar where `min(|close−EMA10|,|close−EMA20|)/close <= 0.01` within next 15 bars.
3. **Higher-low confirmation**: after snapback, confirm a swing-low pivot (left=2,right=2 minimum, evaluated *only after* the right-side bars print → no look-ahead) whose low > flush_low.
4. **Contraction window**: rolling 5-bar range / close vs 30-bar-median range / close ratio ≤ 0.7. Mini-base length ≥ 3 bars.
5. **Trigger**: close > rolling-N high of mini-base AND close > EMA10 AND close > EMA20. Entry at next bar open.
6. **Universe gate**: relative-strength rank 60d vs SPY (or sector benchmark) in top decile at trigger bar.
7. **Macro gate**: SPY > SPY_EMA200 at trigger bar.
8. **Earnings blackout**: skip if next earnings ≤ 5 trading days away.

## Variants to grid (held inside contract envelope)
- Pre-flush ATR multiple: [1.0, 1.5, 2.0]
- Higher-low pivot left/right: [(1,1), (2,2), (3,3)]
- Mini-base duration: [3, 4, 5]
- Trail MA switch: [always EMA20, always EMA10, switch_after_N_holds with N∈{2,3}]
- Time stop bars: [3, 5, 8, none]

## Hard rules (do NOT sweep these away)
- No look-ahead in pivot detection (`shift(right_bars)` after rolling).
- Universe MUST be US equities OR cleanly defined RS-leader basket. Not raw BTC/ETH/SOL.
- Walk-forward by year; do not optimise on full history.

## Forbidden short-cuts
- Do not collapse to a Donchian-N breakout with EMA20 trend filter.
- Do not call any 5-bar tight range "mini-base" without contraction-vs-context check.
- Do not test on crypto and report as Kell parity.

## Output requirements
- Trade log with all preconditions checked per entry (one column per A–E).
- Per-asset and per-year breakdown.
- Comparison vs **baseline**: same universe with naive Donchian-N + EMA20 (to prove the cycle preconditions add edge over the baseline).
