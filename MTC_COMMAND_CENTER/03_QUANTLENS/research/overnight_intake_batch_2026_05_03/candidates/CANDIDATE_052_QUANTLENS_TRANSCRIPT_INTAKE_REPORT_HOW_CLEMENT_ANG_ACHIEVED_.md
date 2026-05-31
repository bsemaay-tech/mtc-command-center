# Candidate Card — CAND_052

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_zw96qkUn9_g_clement_ang_150pct_returns.md`
- **Source URL:** https://www.youtube.com/watch?v=zw96qkUn9_g`
- **Video ID:** zw96qkUn9_g
- **Title:** QuantLens Transcript Intake Report — How Clement Ang Achieved 150%+ Returns in the US Investing Championship
- **Existing candidate id (if any):** QL_20260503_ZW96QKUN9_G_CLEMENT_ANG_VCP_EP_RISK
- **Codex status (intake):** i

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** US_EQUITY
- **Native timeframe:** UNKNOWN
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
### Risk Notu

Short setup'lar gap, borrow, squeeze ve haber riskine çok açık. Bu yüzden ilk prototipte:

- Lower risk_pct
- Max daily aggregate risk
- No overnight short opsiyonu
- Gap-risk penalty
- Borrow/slippage placeholder

kullanılmalı.

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
