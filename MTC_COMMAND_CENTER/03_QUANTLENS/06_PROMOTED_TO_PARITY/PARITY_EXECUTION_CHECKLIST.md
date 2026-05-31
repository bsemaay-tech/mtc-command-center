# Parity Execution Checklist (REVIEW_ONLY → Parity Candidate)

Shared procedure for verifying a promoted candidate's Pine v6 review wrapper against the
Python reference. **No production `MTC_V2.pine` change. No live alerts/orders.**

## Artifacts now available (per parity candidate)
- `producer_spec.json` — verified params + signal definition.
- `<id>_signals.csv` — full-history bar-level reference (long_entry, stop, indicators).
- `<id>_trades.csv` — realized reference trade list (entry/exit/return/reason).
- `PARITY_REFERENCE_METRICS.md` — engine-vs-recorded verification (all currently VERIFIED).
- `<NAME>_REVIEW.pine` — REVIEW_ONLY Pine v6 wrapper to validate in TradingView.

Generate/refresh the CSVs with: `python tools/reference_producer.py <CANDIDATE_FOLDER|ALL>`

## Step-by-step
1. **Compile** the `*_REVIEW.pine` in TradingView (Pine v6). Resolve any compile errors only inside the review file.
2. **Set chart** to the exact symbol/timeframe in `producer_spec.json` (LINK 1h / ADA 1h). Use a Binance-futures-equivalent feed to match the data bundle as closely as possible.
3. **Set Strategy properties:** commission 0.04% per side (~8 bps round-trip), slippage 0, `calc_on_every_tick = false`, order fill on next bar open.
4. **Producer-signal parity (primary):** compare the Pine `longSig` plot/markers against `<id>_signals.csv` `long_entry`. Require ≥ 99% bar agreement.
5. **Indicator parity:** spot-check `ema8`/`atr14` (LINK) or `highBreak`/`pos` (ADA) vs the CSV columns within relative tolerance 1e-4.
6. **Trade-list parity:** export the Strategy Tester trade list; compare entry/exit bars and direction to `<id>_trades.csv` (≤ 1-bar tolerance; investigate any extra/missing trade).
7. **No-repaint check:** re-run on bar replay; confirm signals do not move after bar close. No `request.security`/HTF is used in these candidates.
8. **Record result** in the candidate's `PINE_PARITY_PLAN.md` acceptance section.

## Acceptance → status change
- Pass steps 4–7 → mark candidate parity-validated (still NOT live, still NOT `APPROVED_FOR_MTC_V2_INTEGRATION`).
- Any divergence → keep `PROMOTE_TO_PARITY_CANDIDATE` and log the mismatch.

## Known caveats
- Data-feed differences (TradingView feed vs Binance-futures bundle) can cause small trade-count deltas; judge parity on signal logic, not exact PnL.
- Engine rejects entries where `stop >= next-bar entry open`; the Pine proxy checks `stopCalc < close` at the signal bar — minor edge-case mismatches are expected and acceptable.
- LTC RSI Oversold parity is **deferred** (weak fold consistency); no Pine wrapper generated yet by design.
