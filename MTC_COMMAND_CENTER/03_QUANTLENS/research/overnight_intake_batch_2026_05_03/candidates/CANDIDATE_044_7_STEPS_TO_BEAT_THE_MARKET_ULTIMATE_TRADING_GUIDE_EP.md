# Candidate Card — CAND_044

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_QzzKqmPcB3A_ultimate_trading_guide_ep.md`
- **Source URL:** https://youtu.be/QzzKqmPcB3A?si=gJB9Tj18DU75ZM8Y`
- **Video ID:** QzzKqmPcB3A
- **Title:** 7 Steps to Beat the Market - Ultimate Trading Guide Ep
- **Existing candidate id (if any):** YT_QzzKqmPcB3A_20260503_A
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
_(see source intake)_

## Exit logic (raw extract)
_(see source intake)_

## Stop logic (raw extract)
### Risk / Position Management Adayları

1. Stop mesafesi çok genişse trade’i reddet.
2. Base/pivot stop ile ATR stop’u karşılaştır.
3. Breakout sonrası follow-through yoksa erken cut logic.
4. Trade sayısı / overtrading guard.
5. Market cycle negatifse long entry kapatma veya risk azaltma.

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
