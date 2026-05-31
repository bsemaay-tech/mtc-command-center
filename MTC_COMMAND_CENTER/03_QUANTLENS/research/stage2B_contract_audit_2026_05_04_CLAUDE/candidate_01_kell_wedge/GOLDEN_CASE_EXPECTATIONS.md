# GOLDEN_CASE_EXPECTATIONS — Kell Wedge Pop

## Golden VALID case
- Asset: liquid US growth leader, top-decile RS-rank vs SPY.
- Sequence: bar t-25 close was 2.0×ATR below EMA20 (flush). Bars t-20..t-15 snap up to EMA10. Bar t-12 prints swing-low pivot at price > flush low. Bars t-8..t-4 form 5-bar tight range, range/close = 0.6× 30-bar median. Bar t closes above range_high AND > EMA10 AND > EMA20.
- Expected label: **valid_wedge_pop**, entry next bar open, stop at min(mini_base_low, higher_low_pivot − 0.25 ATR).

## Golden INVALID case (LLM degradation trap)
- Asset: same kind. Bars t-30..t-1 in steady uptrend with no pullback, no flush, no higher-low. Bar t closes above 5-bar high.
- Previous Codex `signal_kell` would FIRE this. A faithful contract must REJECT (`pre_flush=false → no entry`).

## Golden EDGE cases
- **Gap up through trigger**: trigger satisfied but next bar opens above stop+target → use realistic open fill, treat as immediate take-profit / partial.
- **Same-bar stop and target**: ambiguous fill order; use conservative stop-first assumption.
- **Missing volume column**: degrade gracefully (skip volume confirmation, log a warning, keep other gates strict).
- **Wrong timeframe (1h instead of 1D)**: scale ATR/EMA windows; expect far fewer valid sequences; do not down-weight strategy purely from this.
- **Earnings inside contraction window**: skip entirely (data leakage proxy for catalyst risk).
- **Trend filter conflict**: SPY < EMA200 → block entry even if all other gates green.

## Acceptance criteria for the Codex retest
- Must produce ≥10 valid signals per 5-year window per asset to count as "tested".
- Must show that adding A→D preconditions strictly reduces trade count vs Donchian baseline AND increases per-trade R-expectancy.
- If the cycle preconditions do NOT improve baseline → strategy is genuinely weak (not just mis-coded).
