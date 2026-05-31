# Candidate Rules - QLR_R215f4fj7V8

## Source-Faithful Core

Lance Breitstein's source idea is to trade with trend, avoid fighting VWAP/trend, avoid range-bound "no man's land", and wait for the right side of the V before attempting mean-reversion longs after panic.

This sandbox implements only an OHLCV visual-review proxy:

- Long continuation pulse: above VWAP, VWAP not falling, not compressed/range-bound, positive slope, breakout above recent range.
- Long right-side-of-V pulse: recent downside capitulation proxy, then confirmed break of prior bar high.
- Short logic is symmetrical and exists only for visual inspection.
- Initial stop uses trigger/prior bar extreme.
- Debug trailing stop uses prior-bar low/high.

## What To Visually Verify

- Long markers should not appear while price is steadily below VWAP unless a capitulation/reversal pattern exists.
- Short markers should not appear while price is steadily above VWAP unless upside capitulation exists.
- Range-bound compression zones should show "no trade" behavior.
- Right-side-of-V markers should happen after panic and after a turn starts, not while price is still falling cleanly.
- Debug exits should follow prior-bar stop behavior.

## Not Implemented

- News/catalyst feed.
- Halt logic.
- Tape-reading.
- Discretionary A/B/C setup scoring.
- Real position sizing decisions.
- Optimization or profitability testing.
