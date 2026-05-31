# Candidate Card — CAND_036

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_FiUGDA7eMyU_canslim_ross_haber.md`
- **Source URL:** https://www.youtube.com/watch?v=FiUGDA7eMyU
- **Video ID:** FiUGDA7eMyU
- **Title:** CANSLIM Trading Strategy: Beat 99% of Investors Using This Simple Strategy
- **Existing candidate id (if any):** -
- **Codex status (intake):** n

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** CRYPTO
- **Native timeframe:** daily
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

- “Beat 99% of investors” is a marketing-style title and should not be treated as a statistically validated claim.
- CANSLIM outperformance depends heavily on correct data, correct market regime interpretation, and disciplined execution.
- Full CANSLIM is not reproducible from OHLCV alone.
- The exact 7–8% stop rule may not fit all markets, instruments, vol regimes, or MTC crypto/futures use cases.
- Follow-through day logic can fail; the transcript explicitly notes not every follow-through day leads to a new bull market.
- Base-stage classification has discretionary elements and must be made objective before backtesting.

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
