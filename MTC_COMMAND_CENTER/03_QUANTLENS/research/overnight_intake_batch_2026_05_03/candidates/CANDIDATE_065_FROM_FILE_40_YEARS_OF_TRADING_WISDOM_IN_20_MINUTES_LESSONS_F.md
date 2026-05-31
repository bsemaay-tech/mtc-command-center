# Candidate Card — CAND_065

- **Source intake:** `3 Mayıs/YT_Eb9FkLNJLzs_Intake_Report_2026-05-03.md`
- **Source URL:** https://youtu.be/Eb9FkLNJLzs?si=0aQgV5pBPJoFFund
- **Video ID:** Eb9FkLNJLzs
- **Title:** From File:** `40 Years of Trading Wisdom in 20 Minutes - Lessons from Jim Roppel, Hedge Fund Manager
- **Existing candidate id (if any):** -
- **Codex status (intake):** n

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** US_EQUITY
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
## Riskli veya Supheli Iddialar

- 20–22% position sizing yeni traderlar için agresiftir; doğrudan öneri olarak alınmamalıdır.
- “Big money's in the sitting” mottosu doğru liderlerde işe yarayabilir, fakat otomatik sistemlerde drawdown ve trend-top detection olmadan büyük geri verme riski yaratır.
- Breakaway gaps yüksek slippage ve gap-fade riski taşır; intraday fill varsayımları dikkatli modellenmelidir.
- Quickfire format nedeniyle setup detayları eksiktir; doğrudan backtest sistemi yazmak overfit veya yanlış temsil riski taşır.

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
