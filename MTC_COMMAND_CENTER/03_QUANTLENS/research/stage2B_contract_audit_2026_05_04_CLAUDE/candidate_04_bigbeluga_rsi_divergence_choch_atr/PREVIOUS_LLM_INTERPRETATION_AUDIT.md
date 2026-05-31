# PREVIOUS_LLM_INTERPRETATION_AUDIT — BigBeluga

## What Codex coded (`signal_bigbeluga`)
```
pivot=5, atr_mult=3.0
swing_high = high.rolling(11, center=True).max() == high   # uses future bars (look-ahead)
swing_low  = low.rolling(11, center=True).min() == low
confirmed_high = high.where(swing_high).shift(pivot).ffill()
confirmed_low  = low.where(swing_low).shift(pivot).ffill()
bull_div = (low < low.rolling(50).min().shift(1)) & (rs > rs.rolling(50).min().shift(1))   # NOT divergence
bear_div = (high > high.rolling(50).max().shift(1)) & (rs < rs.rolling(50).max().shift(1)) # NOT divergence
long_entry = bull_div.shift(1).rolling(20).max().fillna(False).astype(bool) & (close > confirmed_high.shift(1))
short_entry = analogous
stop = ATR_3 from close
target = ATR_3 from close (1:1 RR)
```

## Comparison to indicator

| Indicator requirement | Coded? | Notes |
|---|---|---|
| `msLen = 10` pivot left/right | NO (`pivot=5`) | Halved the structural window |
| Pivot confirmation lag (right-side) | PARTIAL | `center=True` means *future bars used*; `.shift(pivot)` only restores 5-bar lag, not 10 |
| Real divergence (swing-pivot vs swing-pivot of RSI) | NO | Replaced with rolling-50 min/max comparison; this fires on any new 50-bar low/high regardless of swing structure |
| CHoCH = crossover(close, last confirmed pivot) | PARTIAL | Uses `close > confirmed_high.shift(1)` but never latches `direction` state, so a flip can re-fire on every bar |
| `atrMult = 4` trailing stop | NO (`atr_mult = 3.0`, not trailing) | Static stop at entry; no trail |
| ATR ladder targets (`targetStepMult=2`) | NO | Single target at ATR_mult from close (1:1 RR) |
| Direction latching | NO | Stateless re-evaluation each bar |

## Identified errors
- **Look-ahead bias (severe):** `rolling(11, center=True).max() == high` reads 5 bars into the future. `.shift(pivot)` recovers 5 bars but the *pivot itself* was computed using future data first; this is leak unless the entire pivot expression is shifted. The implementation is borderline-broken and likely flatters historical metrics.
- **Wrong divergence definition:** comparing today's price low vs rolling-50-min and today's RSI vs rolling-50-min RSI is *not* divergence. Real divergence: lower price-pivot-low + higher RSI-pivot-low (bullish), formed in confirmed swings.
- **Pivot length wrong:** indicator default 10, code default 5.
- **No latching of direction:** signal can re-fire bar after bar.
- **No trailing stop:** the indicator's whole exit logic is missing.
- **No ATR ladder targets:** missing.
- **Wrong RR:** entry uses 1:1 ATR target not ATR ladder.

## Classification
**MATERIAL_MISINTERPRETATION** — the producer that ran is structurally a *different* strategy (rolling-min breakout with RSI confluence and centered-pivot leak) wearing BigBeluga's name.

## Was the previous backtest fair?
**NO.** Even ignoring look-ahead, the divergence definition is wrong, the pivot length is wrong, and the exit framework is missing.

## Additional finding
- Provenance: AUDITED card cited Tito Adhikary's video; CLEAN card cited Nick Schmidt's video. Neither contains BigBeluga. Only the `XNZ4f-b3ED8` indicator-audit intake actually documents BigBeluga. The other two attributions are LLM hallucinations / transcription errors that the AUDITED step did not catch.
