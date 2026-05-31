# Candidate Card — CAND_074

- **Source intake:** `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_intake.md`
- **Source URL:** https://youtu.be/Gr2VDAOPRoc?si=cqu6XcRmWZlekz0M
- **Video ID:** Gr2VDAOPRoc
- **Title:** UNKNOWN_TITLE - 8 EMA purple line Amazon trade
- **Existing candidate id (if any):** QL_2026
- **Codex status (intake):** READY_FOR_PYTHON_PROTOTYPE

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** US_EQUITY
- **Native timeframe:** 10m
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
_(see source intake)_

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
