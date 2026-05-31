# Candidate Card — CAND_051

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_UMgJ0P8fe0s_swing_vs_position_matt_petrolia.md`
- **Source URL:** https://www.youtube.com/watch?v=UMgJ0P8fe0s
- **Video ID:** UMgJ0P8fe0s
- **Title:** Swing Trading Vs. Position Trading
- **Existing candidate id (if any):** -
- **Codex status (intake):** SALVAGE_ONLY

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** UNKNOWN
- **Native timeframe:** daily
- **MTC relevance:** PRODUCER_CANDIDATE
- **Testability:** TEST_WITH_5M_CRYPTO_PROXY

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
_(see source intake)_

## Exit logic (raw extract)
_(see source intake)_

## Stop logic (raw extract)
## Risk and Parity Notes

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
