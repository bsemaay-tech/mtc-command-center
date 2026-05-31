# DATA_REQUIREMENTS — Crabel

## Status
- **NEEDS_SESSION_GAP_DATA** (intraday OHLC anchored to RTH open)
- **CURRENT_CRYPTO_DATA_NOT_FAIR** for canonical Crabel
- **CURRENT_CRYPTO_DATA_ENOUGH_FOR_PROXY** only if explicitly relabelled and "session=00:00 UTC" assumed

## Minimum viable
- ES, NQ futures session OHLC (or 1m/5m bars) — at least 5 years.
- Or US large-cap equities intraday + RTH session boundaries.

## Crypto-adapted variant (acceptable as a separate candidate)
- BTCUSDT, ETHUSDT 1h or 5m bars with daily session boundaries 00:00–23:59 UTC.
- Must report explicitly that this is "Crabel-adapted", not Crabel.
- Likely lower edge because crypto has no real session-open auction dynamic.

## Why crypto-daily fails
- "Open" of a daily crypto bar = arbitrary midnight tick = no auction-driven price discovery.
- Stretch on daily bars ≠ Crabel's Stretch.
- The whole "first decisive move out of session open" mechanism cannot exist on a 24/7 daily bar.

## Decision rule
- Reject any verdict on Crabel that uses crypto-daily results as evidence.
