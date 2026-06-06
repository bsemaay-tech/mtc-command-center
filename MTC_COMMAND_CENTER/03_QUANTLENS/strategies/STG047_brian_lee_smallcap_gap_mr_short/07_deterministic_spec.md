# Deterministic Spec — Brian Lee Small-cap Gap Mean-Reversion Short

> Source: YouTube `DPA35Gug3Y4` (Brian Lee). Re-triaged 2026-06-04 from
> `11_TRIAGE/strategies/stg083.md`. **Discretionary strategy** — this spec
> captures the systematizable core; flagged fields require human judgment in the
> original method.

## Universe
- US small-cap equities, liquid (big movers trade ~300-500M shares on the day).
- Pre-market gap scanner: stocks **gapping up >= 20%** (top of list = bigger gap = higher quality).
- Volume filter in pre-market and intraday.

## Bias / regime
- Short-only. Small-caps are typically **downtrending** and gap up **into prior
  resistance**; gaps have a statistical tendency to (partially) fill and to
  **close red by end of day**.

## Entry (short)
- Stock is extended/parabolic into a daily/HTF prior resistance level.
- Extension confirmed on **higher timeframes** (15m/30m/1h/daily RSI extension —
  NOT 1-minute RSI).
- Trigger: short on the **momentum turn / snap** after extension (discretionary
  timing). Method allows a **pilot position** then add as momentum fails.

## Stop / risk
- Tight, **risk-based position sizing**: fixed dollar/R risk per trade that
  **trails the account balance** (risk more after winning, less after losing).
- Stop above the extension high / invalidation of the fade.

## Exit / target (cover)
- Mean reversion = capture the **fade**, not top-to-bottom: cover into partial
  **gap fill** / loss of downside momentum / by end of day.
- ~30% win rate by design; edge is **high reward-to-risk** (avg winner >> avg loser).

## Known risks for backtesting
- **Front-side squeeze**: shorting into momentum can blow out before the fade.
- **Discretion ~50%**: news/PR/filings (dilution, bankruptcy, M&A) and market
  psychology drive entries — not fully mechanizable.
- **Repaint/lookahead**: resistance levels and "extension" must be defined on
  closed bars; gap% from prior close only.
- **Borrow/short availability** and small-cap halts are real-world frictions.

## Minimal systematizable variant (for first prototype)
`gap_up_pct >= 20` AND `price near prior_daily_resistance` AND
`HTF_RSI extended` -> short on first lower-high after the high; cover at
`0.5 * gap_fill` or EOD; stop at `extension_high`. Risk = fixed R trailing equity.

## Disposition
CANDIDATE (partial / discretionary). Not yet prototyped, not promoted, not for live trading.
