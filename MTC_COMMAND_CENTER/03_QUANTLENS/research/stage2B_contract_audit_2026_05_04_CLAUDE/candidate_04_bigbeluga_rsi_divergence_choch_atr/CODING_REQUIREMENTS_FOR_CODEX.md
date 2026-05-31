# CODING_REQUIREMENTS_FOR_CODEX — BigBeluga

## Required full rewrite
1. **Open the BigBeluga Pine source** referenced in intake §4 — replicate the exact pivot, divergence and CHoCH logic.
2. **Pivots:** `pivothigh(10, 10)` and `pivotlow(10, 10)` confirmed `msLen` bars after the pivot bar. In Python: `rolling(2*N+1).max() == series.shift(N)` then shift entire result by N to defer to confirmation bar. NEVER use `center=True` followed by partial shift.
3. **Divergence:** detect via *previous-confirmed-pivot vs current-confirmed-pivot* on price and on RSI(14). Bull div = lower price-pivot-low + higher RSI-pivot-low (within validity window e.g. 30 bars between pivots).
4. **State machine:** maintain `direction ∈ {bull, bear}`. CHoCH events flip direction. Latch — no re-fire while direction unchanged.
5. **Entry:** next bar open after CHoCH. Optionally require recent divergence in same direction (sweep both modes).
6. **Initial stop:** divergence-extreme (swing low for bull entry).
7. **Trailing stop:** chandelier-style: `trail_long = max_high_since_entry − ATR(14)*4`. Update each bar; exit when close < trail_long.
8. **Ladder TPs:** TP1, TP2, TP3 at `entry + ATR_at_entry × {2, 4, 6}` for longs (mirror for shorts). Optional partial-exit equal thirds.
9. **Exit on opposite CHoCH:** force-flat on direction flip.

## Variants to grid (within contract envelope)
- ms_len: [8, 10, 13]
- divergence required: [yes, no]
- trailing ATR mult: [3.0, 4.0, 5.0]
- TP ladder mults: [{2,4,6}, {1.5,3,5}, none]
- Anti-whipsaw bars between flips: [0, 5, 10]

## Hard rules
- Zero look-ahead. Verify by replaying bar-by-bar and checking that no signal at bar t depends on data at t+1..t+N.
- Direction must persist (no re-fire).

## Forbidden short-cuts
- Do NOT replace pivot logic with rolling extremes.
- Do NOT replace divergence with rolling-min/max comparison.
- Do NOT use `rolling(..., center=True)`.
- Do NOT skip the trailing stop — without trail, the strategy isn't BigBeluga.

## Output
- Per-trade log: which CHoCH triggered, divergence flag at trigger, pivot index used, all four exit reasons (trail / opp-CHoCH / TP1/2/3 / time stop).
- Walk-forward: prove ms_len 10 and trail mult 4 either work as defaults or fail honestly.
