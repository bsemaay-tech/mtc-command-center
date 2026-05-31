# Candidate Card — CAND_038

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_GHZBv1W4-II_larry_williams.md`
- **Source URL:** https://youtu.be/GHZBv1W4-II?si=de5dq3ybVKbtFD-b
- **Video ID:** GHZBv1W4-II
- **Title:** 11,300% Return in One Year Interview with Larry Williams
- **Existing candidate id (if any):** QL_CAND_20260503_GHZBV1W4II_VOL_BREAKOUT_OPEN
- **Codex status (intake):** i

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** US_EQUITY
- **Native timeframe:** daily
- **MTC relevance:** PROCESS_ONLY
- **Testability:** REJECT_NOT_TESTABLE_AS_PRODUCER

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
### Entry Concepts

- Opening price breakout bracket.
- Prior day low/high reclaim reversal.
- Same-family comparative strength confirmation.
- Weekly setup alignment, daily trigger execution.
- Trendline break / recent high breakout / higher-low confirmation.

## Exit logic (raw extract)
### Exit Concepts

- Protective stop placed at technical invalidation area.
- If target reached, take profit.
- If target not reached, trail protective stop.
- Big trend = give trade time; trend function is time.
- Stop must be in the market before walking away.

## Stop logic (raw extract)
### Risk Concepts

- Bet small, catch large moves.
- Fixed percent of equity per trade.
- Position size derives from stop distance.
- Do not average down.
- Avoid oversized illiquid trades because liquidity affects both execution and psychology.
- Trade platform/order entry mistakes are a real operational risk; double-check orders.

## Sizing (raw extract)
_(see source intake)_

## Ambiguities
- Crypto-proxy applicability for US-equity-native setups (catalyst, gap, session).
- Discretionary "support/resistance" or "candle confirmation" rules require deterministic formalization before backtest.

## Conservative formalization for Python prototype
- Replace any discretionary subjective check with a single deterministic rule.
- If the strategy depends on US session, gap, or earnings catalyst, mark DATA_BLOCKED unless an explicit numeric proxy is documented in this card.

## Critical caveats
- Tonight's run is Python-only research; no Pine, no parity, no live alerts.
- A weak or rejected result is acceptable if evidence-based.
