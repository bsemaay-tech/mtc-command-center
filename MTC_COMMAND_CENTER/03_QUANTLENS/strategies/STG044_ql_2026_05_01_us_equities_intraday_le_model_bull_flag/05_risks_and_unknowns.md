# Risks And Unknowns

## Risks
- The strategy may be regime-dependent and optimized for lockout rallies.
- Marketing claims are anecdotal and not evidence-backed.
- "Good flag" versus "bad flag" is discretionary without numeric thresholds.
- HOD/LOD exits can leak future data if implemented incorrectly.
- Options/0DTE returns can exaggerate underlying edge.
- Lunch/chop avoidance is useful but requires exact session definitions.

## Unknowns
- Channel name and channel ID were not provided.
- Exact chart timeframe is not stated as a single default.
- Exact option contract selection is absent.
- Exact partial profit percentage beyond "sell half" is limited.
- Exact EMA runner stop trigger is not specified.
- Exact bearish mirror examples are described conceptually but not deeply shown.

## Required Clarifications Before Backtest
- Which timeframe to prototype first.
- Which market universe to use beyond SPY.
- Whether pre-market levels are calculated from extended-hours data only.
- Whether entries execute intrabar at touch or on next candle.
- Whether stops are intrabar hard stops or close-based exits.
