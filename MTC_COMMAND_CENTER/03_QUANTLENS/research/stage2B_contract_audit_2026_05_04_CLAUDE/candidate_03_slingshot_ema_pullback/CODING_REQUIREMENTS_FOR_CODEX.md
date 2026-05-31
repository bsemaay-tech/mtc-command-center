# CODING_REQUIREMENTS_FOR_CODEX — Slingshot

## Required adjustments to existing prototype
1. **Expand prior-strength gate** to true OR over the four intake-quoted alternatives (currently only `close > SMA50`).
2. **Sweep pullback lookback** N ∈ {3, 5, 8, 13}.
3. **Sweep pullback depth cap** ∈ {10, 15, 25}.
4. **Sweep exit mode** as separate runs: `{close_below_EMAH4, ATR_2_trail, R_multiple_2, R_multiple_3, time_stop_8}`.
5. **Add macro gate** option: SPY > SPY_EMA200 (or BTC > BTC_EMA200 for crypto-exploratory).
6. **Add equity-data run**: at minimum a top-50 US growth basket; report equity vs crypto separately.

## Hard rules
- Trigger must remain "fresh cross-up" (close > EMA(high,4) AND close[1] ≤ EMA(high,4)[1]).
- No look-ahead in pullback flag (use `.shift(1)` on the rolling sum).

## Forbidden short-cuts
- Do NOT replace EMA(high,4) with SMA(close,4) or EMA(close,4).
- Do NOT mark a candidate "killed" using crypto-only results.

## Output
- Per-asset, per-year, per-variant equity curve and metric grid.
- Side-by-side equity-basket vs crypto-basket comparison.
- Sensitivity heatmap over (N, depth, exit_mode).
