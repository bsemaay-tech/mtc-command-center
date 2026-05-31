# Risks And Unknowns

## Risks
- Performance claims are anecdotal and promotional.
- "As close as possible to EMA" is discretionary without a numeric threshold.
- HOD/LOD exits can accidentally introduce lookahead if not implemented bar-by-bar.
- Options returns are not equivalent to underlying price returns.
- Trend days may perform differently from choppy sessions.
- EMA-only systems can overtrade in sideways regimes.

## Unknowns
- Exact video title and channel name were not provided.
- Exact option contract selection rules are absent.
- Exact session definition is absent.
- Partial profit percentages are not specified.
- Runner sizing is described by examples but not formalized.
- "EMA break" needs a precise close-through, wick-through, or confirmation rule.

## Required Clarifications Before Backtest
- Which market universe should be tested first.
- Whether shorts mean underlying shorts or put options only.
- Whether entries are at touch, close, next open, or limit near EMA.
- Whether stops are hard intrabar stops or close-based invalidations.
