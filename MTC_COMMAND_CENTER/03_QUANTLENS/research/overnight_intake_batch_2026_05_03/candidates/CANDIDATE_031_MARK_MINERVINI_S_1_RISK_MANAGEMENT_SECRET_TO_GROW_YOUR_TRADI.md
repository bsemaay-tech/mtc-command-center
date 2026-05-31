# Candidate Card — CAND_031

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_C9Pvd9UD0jM_mark_minervini_progressive_exposure.md`
- **Source URL:** https://www.youtube.com/watch?v=C9Pvd9UD0jM
- **Video ID:** C9Pvd9UD0jM
- **Title:** Mark Minervini's #1 Risk Management Secret to Grow Your Trading Profit
- **Existing candidate id (if any):** -
- **Codex status (intake):** n

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** CRYPTO
- **Native timeframe:** position
- **MTC relevance:** PRODUCER_CANDIDATE
- **Testability:** TEST_WITH_1D_CRYPTO_PROXY

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
_(see source intake)_

## Exit logic (raw extract)
_(see source intake)_

## Stop logic (raw extract)
## Risky / Suspicious Claims

- The transcript argues that trading cannot be fully captured by spreadsheets, algorithms, or AI. Treat this as a discretionary trading opinion, not as a testable system rule.
- Progressive exposure can amplify gains, but it can also amplify losses if the feedback signal is noisy or delayed.
- The transcript does not provide exact numerical rules for when to move from probe to full exposure.
- The 2-for-1 rule requires multi-position portfolio logic and may not be directly expressible in TradingView Pine for a single-chart strategy.
- If open profits are treated too aggressively as cushion, correlated reversals can cause fast drawdowns.

---

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
