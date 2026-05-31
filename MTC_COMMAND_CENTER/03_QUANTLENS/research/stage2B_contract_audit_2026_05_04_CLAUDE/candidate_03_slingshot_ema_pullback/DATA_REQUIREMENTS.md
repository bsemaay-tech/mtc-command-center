# DATA_REQUIREMENTS — Slingshot

## Status
- **CURRENT_CRYPTO_DATA_ENOUGH_FOR_PROXY** (exploratory only, per intake).
- **NEEDS_US_EQUITY_DAILY** (for primary verdict).

## Minimum viable
- Daily OHLC of target universe; 5+ years.

## Why crypto can be used (with caveat)
- Strategy is timeframe- and indicator-light; the math (EMA of highs) works on any liquid OHLC.
- BUT speaker designed for equities; pullback dynamics on crypto majors are different (more noise, no earnings-driven flushes).

## Decision rule
- Acceptable to keep crypto-only Stage-2 numbers as exploratory.
- Final verdict requires equity-basket run to confirm or reject the edge in native context.
