# Deterministic Spec — EMA20/50 Two-Retests Baseline (QL_EMA20_50_TWO_RETEST_BASELINE_v0)

> Source: EMA20/50 retest critical intake. Research-only Python batch 2026-05-03.
> Signal logic from `run_batch.py::signal_ema_retest()`. No Pine, no MTC production integration.
> **BASELINE_ONLY**: not strong enough for producer research.

## Universe
- Crypto (BTC, ETH, SOL, BNB, XRP), 1D, 4h, 1h bars.

## Concept
After EMA20 crosses EMA50 (bullish or bearish), wait for the price to retest EMA20 at least
**twice** before entering. The logic: one retest may be a false cross; two retests confirm
the new regime. Entry triggers on the second retest.

## Indicators
```
e20  = EMA(close, 20)
e50  = EMA(close, 50)
atr  = ATR(14)

cross_up = (e20 > e50) AND (e20[1] <= e50[1])    # bullish cross
cross_dn = (e20 < e50) AND (e20[1] >= e50[1])    # bearish cross

# Track cumulative count within current cross regime
since_up = cumcount of cross_up (resets to 0 at each new cross_dn)
since_dn = cumcount of cross_dn (resets to 0 at each new cross_up)

# Retest conditions
retest_long  = (low <= e20 × (1 + tol)) AND (close > e20)    # touch from below + reclaim
retest_short = (high >= e20 × (1 - tol)) AND (close < e20)   # touch from above + rejection

# Count retests since current cross
long_retest_count  = cumsum(retest_long) within current since_up group
short_retest_count = cumsum(retest_short) within current since_dn group
```

## Signal definition
```
# Entry: exactly when count transitions from <2 to >=2 (second retest event)
long_entry  = (e20 > e50)                            # bullish regime
            AND (long_retest_count >= 2)
            AND (long_retest_count[1] < 2)           # transition on this bar

short_entry = (e20 < e50)                            # bearish regime
            AND (short_retest_count >= 2)
            AND (short_retest_count[1] < 2)
```
Default `tolerance = 0.01` (1% touch zone).

## Stop and target
```
stop   = close - 2 × atr (long); close + 2 × atr (short)
target = close + 3 × atr (long); close - 3 × atr (short)
exit_long  = close < e50    # exit if price drops below e50
exit_short = close > e50
```

## Research classification
**BASELINE_ONLY** — Baseline reference only; fee stress and drawdown not strong enough for
producer research.

## Backtesting risks
- Groupby-based retest counting resets on every cross — this is correct behavior but
  complex to verify in a different backtest framework.
- The "second retest" logic requires careful state tracking; naive implementations may miscount.
- Aggregate PF slightly above 1.0 but fee stress degrades quickly.

## Disposition
Research-only. BASELINE_ONLY. The two-retest concept is a legitimate "confirmation of new regime"
filter. Use as a meta-rule: after a MA cross, wait for two retests before switching strategy
direction, rather than as a standalone entry system.
