# Deterministic Spec — Ty Rajnus Microcap Liquidity Reversion Short (QL_TY_MICROCAP_LIQUIDITY_REVERSION_SHORT_v0)

> Source: Ty Rajnus microcap short intake. Research-only batch 2026-05-03.
> **BLOCKED_DATA**: requires US microcap 1m OHLCV, premarket/afterhours, borrow/locate,
> dilution flags, halt data.

## Universe
- US microcap equities (market cap < $300M), 1m bars.
- Requires: borrow availability, share dilution data, halt flags, pre/aftermarket data.

## Concept
Microcap stocks that spike intraday on low float or dilution news exhibit strong mean-reversion
patterns by end of day. Short into the spike when key technical conditions align; cover into the fade.

## Expected signal logic (not implemented — blocked)
```
# Spike detection
intraday_spike = (high / open - 1) >= 0.30    # >= 30% intraday spike from open

# Technical overextension
rsi_1m = RSI(close, 14) > 80                  # overbought on 1m
price_vs_avwap = close / AVWAP > 1.15         # > 15% above session VWAP

# Fundamental flags (not available in repo data)
low_float = True                               # float < 10M shares (unavailable)
no_halt_risk = True                            # not in active halt (unavailable)
borrow_available = True                        # locate confirmed (unavailable)

long_entry  = False                            # this is a short-only strategy
short_entry = intraday_spike AND rsi_1m AND price_vs_avwap  # plus fundamental flags
stop_short  = today_high + ATR × 0.5
target_cover = AVWAP OR gap_fill OR EOD
```

## Data requirements (not met in current repo)
- US microcap 1m OHLCV (pre-market and intraday)
- Float, market cap, dilution announcement feed
- Borrow/locate availability
- Halt flag / circuit breaker data

## Research classification
**BLOCKED_DATA** — Cannot be tested without the required dataset.

## Known risks
- Short squeezes on low-float stocks can cause unlimited losses without hard stops.
- Borrow unavailability blocks the trade regardless of the signal.
- Halts can lock positions; size management is critical.
- This strategy requires direct-access broker with real-time locate system.

## Disposition
Blocked. This strategy operates in a specialized niche (OTC/microcap short-selling) that
requires infrastructure not available in the repo. Not suitable for systematic backtesting
without the full data stack.
