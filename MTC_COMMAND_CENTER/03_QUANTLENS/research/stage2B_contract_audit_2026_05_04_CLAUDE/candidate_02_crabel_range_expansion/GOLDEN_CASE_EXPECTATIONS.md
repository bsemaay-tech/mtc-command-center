# GOLDEN_CASE_EXPECTATIONS — Crabel Range Expansion

## Golden VALID case
- Asset: ES futures session.
- Prior day: NR7 (today's range smallest of last 7).
- Stretch_10 = 4.0 points; multiplier = 0.6 → trigger = O ± 2.4.
- Today's open = 4500. Buy stop @ 4502.4, sell stop @ 4497.6.
- 09:35 ET price prints 4502.5 → long fill at 4502.4.
- Sell stop becomes initial SL at 4497.6.
- Session closes 4520. EOD exit at 4520. Net long +17.6.
- Expected label: **valid_long_NR7_breakout**.

## Golden INVALID case (LLM degradation trap)
- Prior day NOT NR4/NR7/ID-NR4. Codex's `signal_crabel` would still place the trigger; faithful contract REJECTS (no NR pattern → no trade today).

## Edge cases
- **Both stops hit same bar**: take direction of first 1-minute breach; if 1-min unavailable, prefer the side aligned with daily EMA200 trend.
- **Gap open beyond a stop**: fill at open price; treat slippage explicitly.
- **Half-day session**: skip.
- **No volume / illiquid open**: skip.
- **Wrong timeframe (daily bars)**: strategy invalid — DO NOT generate trades.
- **Trend filter conflict**: optional; document both with/without.

## Acceptance criteria
- ≥30 sessions with NR-pattern per year per asset.
- NR-filtered version must beat the no-NR baseline on Sharpe AND profit factor; otherwise the NR filter is decorative.
- Stretch sensitivity: small monotonic profile across mult ∈ [0.4..1.0]. Sharp single-peak = overfit.
