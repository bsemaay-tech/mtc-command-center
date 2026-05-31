# PREVIOUS_LLM_INTERPRETATION_AUDIT — Slingshot

## What Codex coded (`signal_slingshot`)
```
eh        = EMA(high, 4)
strength  = close > SMA(close, 50)
pulled    = (close < eh).rolling(5).sum() >= 1     # any of last 5 bars closed under
high_ref  = high.rolling(5).max()
depth_ok  = (high_ref - low.rolling(5).min())/high_ref*100 <= 15
cross     = (close > eh) & (close[1] <= eh[1])
long_entry = strength & pulled.shift(1) & depth_ok & cross
stop      = low.rolling(5).min().shift(1)   # default; ATR2 variant
target    = close + 2 or 3 R
exit_long = close < eh
```

## Comparison to source

| Source requirement | Coded? | Notes |
|---|---|---|
| EMA(high, 4) — exact formula | YES | Correct |
| Prior strength gate | PARTIAL | Only `close > SMA50`. Intake offered SMA50 OR SMA200 OR 20d-return-strong OR near-recent-high. |
| Pullback (≥1 bar < EMA(high,4) in last N) | YES | N=5 hardcoded; intake suggested 3/5/8/13. |
| Pullback depth cap | YES | 15% from rolling-5 high; reasonable. |
| Fresh cross-up | YES | Explicit. |
| Stop at pullback low / ATR | YES | Both modes available. |
| Exit on close < EMA(high,4) | YES | Correct. |
| Universe = equities | NO | Tested on crypto majors only. Intake explicitly warned crypto = exploratory. |

## Identified errors / gaps
- **Faithful core**: kernel logic (EMA(high,4) + pullback + cross-up) is the closest match in the entire batch.
- **Wrong asset class for pass/fail decision**: only crypto tested; no fair equity test. Crypto results are exploratory only — they cannot kill the candidate.
- **Limited prior-strength gate**: only one of intake's four alternatives. Real-world filtering may want OR-conjunction over multiple regime proxies.
- **Hardcoded lookback** at 5; no sweep over [3, 5, 8, 13] as intake recommended.
- **Single exit mode** in the contract; no comparative study of close-below vs ATR-trail vs R-targets.

## Classification
**FAITHFUL** (or borderline FAITHFUL with **PARTIALLY_FAITHFUL** in prior-strength gating and exit variant coverage).

## Was the previous backtest fair?
**PARTIALLY**. Logic is sound; asset class is wrong for verdict. Stage-2 weak crypto numbers do NOT prove the strategy is dead — they prove it doesn't transfer cleanly to crypto majors (which the intake itself warned about).
