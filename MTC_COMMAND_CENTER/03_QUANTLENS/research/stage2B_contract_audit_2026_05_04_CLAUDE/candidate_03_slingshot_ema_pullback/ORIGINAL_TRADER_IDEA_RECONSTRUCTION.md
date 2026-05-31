# ORIGINAL_TRADER_IDEA_RECONSTRUCTION — Slingshot

## Plain English
EMA(high, 4) tracks the recent ceiling of the swing. In an uptrend, price spends most time above this line. When price *closes below* it for one or more bars, that's a controlled pullback — a small loss of upside momentum without a trend break. When price then **reclaims** EMA(high, 4) by closing back above it, the slingshot resumes: trapped pullback shorts cover, sidelined money re-enters, and the prior trend tends to extend.

## Decomposition
- **Core edge:** clean reclaim of a tight upper-bound EMA after a brief pullback inside an established uptrend → trapped-trader and trend-resumption flow.
- **Setup context:** prior strength is mandatory (close > SMA50/200, OR 20d return strongly positive, OR near recent 20/60-day high). Without this, "above EMA(high,4)" is meaningless.
- **Trigger:** today close > EMA(high,4) AND yesterday close ≤ EMA(high,4).
- **Pullback validity:** at least one bar in the recent 3–8 bars closed below EMA(high,4); pullback drawdown not catastrophic (e.g. ≤ 15%).
- **Invalidation:** close back below EMA(high,4) after entry; or break of pullback low.
- **Exit:** close below EMA(high,4) (default), ATR trail, fixed R (2R/3R), or time stop.
- **Risk:** stop = pullback low or trigger-bar low or ATR×2; size by 1R risk.
- **Universe:** equities with prior strength; selectively crypto majors (with explicit exploratory caveat).
- **Discretionary:** "obvious resistance overhead", choice of pullback window, choice of exit mode (close-below / ATR trail / R-target).
- **Non-essential commentary:** specific stock examples in the source video.

## What an honest mechanical proxy must include
A. EMA(high, 4) — exactly: EMA of the high series, length 4.
B. Prior-strength gate (configurable but required).
C. Pullback gate: ≥1 close < EMA(high,4) within last 3–8 bars.
D. Pullback-depth cap (≤ 10–15%).
E. Trigger as a *fresh* cross-up.
F. Entry next bar open; stop at pullback low or ATR.

## What proxy must NOT do
- Trigger on every cross-up regardless of pullback depth or prior strength.
- Use SMA(close,4) instead of EMA(high,4) (different magnitude and meaning).
- Skip the "yesterday ≤ EMA(high,4)" freshness check (would over-trigger).
