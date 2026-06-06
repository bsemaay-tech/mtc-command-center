# Deterministic Spec — BigBeluga RSI Divergence + CHoCH + ATR (QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0)

> Source: BigBeluga indicator intake. Research-only Python batch 2026-05-03.
> Signal logic from `run_batch.py::signal_bigbeluga()`. No Pine, no MTC production integration.

## Universe
- Crypto (BTC, ETH, SOL, BNB, XRP), 4h and 1D bars.

## Concept
RSI bullish/bearish divergence + Change of Character (CHoCH): price makes new extreme but RSI
does not confirm. Then price breaks the prior swing structure — this is the CHoCH entry trigger.

## Indicators
```
atr  = ATR(14)
rsi  = RSI(close, 14)

# Swing high/low using pivot detection (centered rolling window)
swing_high = high == highest(high, 2×pivot+1, center=True)
swing_low  = low == lowest(low, 2×pivot+1, center=True)

# Confirmed pivot prices (shifted by pivot bars to avoid lookahead)
confirmed_high = high where swing_high, shifted pivot bars, forward-filled
confirmed_low  = low where swing_low, shifted pivot bars, forward-filled
```

## Signal definition

### Bullish (long entry)
```
bull_div = (low < lowest(low, 50)[1])          # price lower low
         AND (rsi > lowest(rsi, 50)[1])         # RSI higher low (divergence)

# CHoCH entry: divergence in prior 20 bars, then break above confirmed swing high
long_entry = any(bull_div in last 20 bars)
           AND (close > confirmed_high[1])      # break of prior swing high (CHoCH)
```

### Bearish (short entry)
```
bear_div = (high > highest(high, 50)[1])        # price higher high
         AND (rsi < highest(rsi, 50)[1])         # RSI lower high (divergence)

short_entry = any(bear_div in last 20 bars)
            AND (close < confirmed_low[1])       # break of prior swing low
```

## Stop and target
```
stop   = close - atr_mult × ATR    (long); close + atr_mult × ATR    (short)
target = close + atr_mult × ATR    (long); close - atr_mult × ATR    (short)
```
Default `atr_mult = 3.0`.

## Key caveat: centered rolling window
`swing_high/low` uses `center=True` rolling — this is a **lookahead in real-time**.
In backtest with confirmed pivot (shifted by `pivot` bars), this is OK.
In live trading, swing detection must use a confirmation delay of at least `pivot` bars.

## Research classification
**WEAK_CANDIDATE** — LOW_SAMPLE: too few trades for promotion.

## Backtesting risks
- Centered pivot detection requires `pivot`-bar delay in live; not built-in to naive implementations.
- Very low trade count on 1D — insufficient for statistical inference.
- ATR stop = ATR target gives 1:1 R:R by default; not favorable unless win rate > 50%.

## Disposition
Research-only. WEAK_CANDIDATE. The divergence + CHoCH concept is sound (well-known signal
class) but the implementation requires careful lookahead handling. Revisit with proper
pivot detection delay and tighter R:R structure.
