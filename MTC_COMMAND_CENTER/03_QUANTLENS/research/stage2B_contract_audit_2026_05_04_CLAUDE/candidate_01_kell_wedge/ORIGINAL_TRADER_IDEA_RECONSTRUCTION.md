# ORIGINAL_TRADER_IDEA_RECONSTRUCTION — Kell Wedge Pop

## In plain English
Kell does not trade "buy when price closes above 10EMA". He waits for a specific multi-stage choreography on a leader stock:

1. The stock *first* has a real downtrend / capitulation flush — a reversal extension where it overshoots below the 10/20EMA (objective proxy: distance-from-EMA20 z-score very negative or close < EMA20*(1-extension_threshold)).
2. Then it snaps back *up to* the 10/20EMA zone (relief rally).
3. It pulls back *again* but this pullback prints a **higher low** vs the original capitulation low. This higher-low is the structural confirmation that selling has dried up.
4. While building the higher low, daily volatility/range contracts: ATR percentile drops, recent N-bar range becomes narrow, a mini-base of >=3 bars forms.
5. Trigger: close breaks above the mini-base swing high, ideally with close > both 10EMA and 20EMA.
6. Entry: next bar open or stop entry above mini-base high.
7. Initial stop: below the mini-base low, OR below the higher-low pivot (whichever is closer/safer).
8. Exit: ride EMA10 or EMA20; first 3–4 holds → switch to faster MA. Sell into obvious blowoff / exhaustion extension.

## Decomposition by category
- **Core edge:** capturing trend resumption *after* sellers have been exhausted (post-flush higher-low contraction). The edge is *not* the EMA cross — it is the structural sequence.
- **Setup context:** must be a leader in an in-play theme; weekly chart in uptrend or in a base; daily already showed reversal extension+snapback.
- **Trigger:** mini-base high break with close above 10EMA & 20EMA.
- **Invalidation:** close below mini-base low; or break below higher-low; or daily closes back through 20EMA after entry.
- **Exit:** primarily MA-ride (10EMA or 20EMA depending on stock's behaviour). Discretionary blowoff / wedge-drop exit on extension extreme.
- **Risk logic:** position sized so mini-base-low stop = 1R; size per Kell's name-size table (NOT per-trade % risk).
- **Universe:** liquid US equity high-beta growth leaders. Theme leadership and relative strength vs index are *prerequisites*, not nice-to-haves.
- **Discretionary judgement:** "leader status", "in-play theme", choice of which MA to trail (10 vs 20), recognising blowoff exhaustion, choice of execution TF (10m vs 30m).
- **Non-essential commentary:** Kell's specific name examples (SMCI etc.) are illustrative; backtest must not overfit to them.

## What an honest mechanical proxy must include
A. Pre-flush detection (close < EMA20*(1-k*ATR%) or zscore<-1.5).
B. Snapback flag (price returns to within tolerance of EMA10/20 after pre-flush).
C. Higher-low pivot confirmed (later swing low > prior capitulation low).
D. Contraction window (ATR percentile dropping; rolling N-bar range below threshold; min 3 bars).
E. Trigger only valid when A→B→C→D all happened in the right order.

## What proxy must NOT do
- Treat any breakout-of-rolling-N-day-high in an uptrend as "Wedge Pop". This is the most common LLM degradation: dropping the cycle prerequisites and reducing the strategy to a Donchian breakout with an EMA20 trend filter.
- Use crypto BTC/ETH/SOL as proof of equity-leader edge.
- Skip the higher-low requirement.
