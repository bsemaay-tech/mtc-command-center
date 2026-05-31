# ORIGINAL_TRADER_IDEA_RECONSTRUCTION — BigBeluga

## Plain English
The "trader's idea" is actually an **indicator's idea**. BigBeluga's "Market Structure Trend Matrix" detects:
1. A swing high/low pivot (10 bars left, 10 bars right) — this is the structure reference.
2. A break of that confirmed pivot (close crossover phigh = bullish CHoCH; close crossunder plow = bearish CHoCH) — this is a market-structure flip.
3. RSI divergence between price extreme and RSI extreme is used as an **early warning** (visual cue) before the CHoCH.
4. After CHoCH, ATR×4 trails the position; ATR×2 spaced ladder marks targets.

## Decomposition
- **Core edge (claimed):** trade only when momentum (RSI) and structure (pivot break) agree on the reversal/continuation.
- **Setup context:** confirmed pivot exists; recent RSI divergence flagged.
- **Trigger:** crossover/crossunder of confirmed pivot price — i.e. CHoCH.
- **Invalidation:** ATR×4 trailing stop OR opposite CHoCH.
- **Exit:** ATR-ladder targets and/or trailing stop.
- **Risk logic:** ATR-based trail; initial stop at divergence-pattern extreme.
- **Universe:** asset-agnostic per indicator design.
- **Discretionary:** what counts as "RSI divergence" — pivot-vs-pivot? rolling-min vs rolling-min? In the published Pine the divergence detection uses pivot pairs with conditions on RSI value direction.
- **Non-essential:** speaker's promotional commentary about "best indicator I've seen".

## What an honest mechanical proxy must include
A. **Confirmed pivot** logic with 10-bar right-confirmation lag (use `pivot_high(N,N).shift(N)` to avoid look-ahead).
B. CHoCH detection as `crossover(close, last_confirmed_phigh)` and inverse for shorts.
C. RSI divergence using **swing-vs-swing pivot** comparison, not rolling-min/rolling-max.
D. Latching state (trend direction) so a single CHoCH flips and persists.
E. ATR×4 trailing stop replicated exactly.

## What proxy must NOT do
- Use centered rolling max (`rolling(11, center=True)`) for pivots — leaks future data.
- Use rolling-N min/max as proxy for "RSI divergence" — that is not divergence.
- Skip the pivot confirmation lag.
- Treat divergence as the entry trigger directly without CHoCH.
