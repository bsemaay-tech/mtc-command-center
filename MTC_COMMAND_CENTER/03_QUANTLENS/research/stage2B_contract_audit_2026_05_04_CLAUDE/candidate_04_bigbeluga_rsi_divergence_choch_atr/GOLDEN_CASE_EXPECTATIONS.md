# GOLDEN_CASE_EXPECTATIONS — BigBeluga

## Golden VALID case (bullish)
- 30 bars ago: confirmed swing low at 100.0, RSI pivot-low = 25.
- 12 bars ago: confirmed swing low at 95.0, RSI pivot-low = 35 → bullish divergence valid.
- Current direction = bear; last confirmed pivot high = 110.
- Bar t closes at 111 → crossover triggers bullish CHoCH.
- Entry next bar open. Initial stop at 95.0 (latest swing low). TPs at entry+ATR×{2,4,6}. Trail = max_high_since_entry − ATR×4.

## Golden INVALID case (LLM degradation trap)
- Same crossover above prior pivot high but no divergence formed in last 30 bars and divergence is hard-required → REJECT.
- Same crossover but already in bull direction (latched) → REJECT (no re-fire).
- Pivot computed using `rolling(11, center=True)` → INVALID implementation; reject the implementation, not the trade.

## Edge cases
- **Two consecutive CHoCHs within 5 bars (whipsaw)**: anti-whipsaw guard required.
- **Gap through trail stop**: fill at next open with realistic slippage.
- **Same-bar CHoCH and TP1**: enter then exit same bar; account for in trade log explicitly.
- **No volume / illiquid**: optional liquidity gate.
- **Wrong timeframe**: lower timeframes increase false CHoCHs proportionally; expect noise.

## Acceptance criteria
- Sensitivity to ms_len should be smooth (not knife-edge).
- Removing the trailing stop should worsen risk-adjusted returns vs keeping it (otherwise the trail is decorative — questionable).
- Long+short symmetric edge should hold across multi-year regimes; if asymmetric, document why.
