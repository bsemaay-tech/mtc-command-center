# GOLDEN_CASE_EXPECTATIONS — Slingshot

## Golden VALID
- Asset: liquid uptrending stock; close > SMA50; close ≥ 95% of 20-day high.
- 6 bars ago, close was below EMA(high,4); next 5 bars contained at least one more close below EMA(high,4); rolling-5 pullback depth = 8%.
- Today: close > EMA(high,4); yesterday close ≤ EMA(high,4)[1]. Volume ≥ SMA(vol,20).
- Expected: enter next bar open. Stop at min(rolling-5 low, trigger bar low). Default exit on close < EMA(high,4).

## Golden INVALID
- Same fresh cross-up but no close below EMA(high,4) in last 13 bars (no real pullback) → contract REJECTS. (Codex's current code with N=5 may also reject — verify.)
- Pullback depth = 35% (deep correction, broken trend) → REJECTS.
- Prior strength absent (close < SMA50, 20d return = −5%) → REJECTS.

## Edge cases
- **Gap up through stop level**: fill at open; recompute R.
- **Same-bar close-below-EMAH4 again** (whipsaw): exit immediately.
- **Missing volume**: skip volume confirmation only; do not skip trade.
- **Wrong timeframe**: scale EMA(high,4) into native; expect different statistics.
- **Earnings inside pullback window** (equities): allow but flag.

## Acceptance
- Variant grid must show monotone behaviour over (N, depth) — not knife-edge peaks.
- Equity basket Sharpe > random basket of equal long-only buy-and-hold.
- Crypto basket result is informative, not decisive.
