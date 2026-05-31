# MTC Module Mapping

## Candidate Role
- Primary role: none yet
- Salvage roles: confirmation, guard, sl_tp_method

## Possible Future Mapping
- Oscillator confirmation: momentum line and signal line crossing.
- Divergence guard: bullish/bearish divergence detection.
- Price-action confirmation: structure break after divergence.
- Stop method: beyond divergence extreme.

## No Direct Mapping
The oscillator formula is not exact enough for parity-safe local implementation. Any MTC mapping requires script-level audit first.

## No-Touch Notes
- No change to `01_PINE/MTC_V2.pine`.
- No production Python runner change.
- No backtest, optimization, parity run, or TradingView automation.
