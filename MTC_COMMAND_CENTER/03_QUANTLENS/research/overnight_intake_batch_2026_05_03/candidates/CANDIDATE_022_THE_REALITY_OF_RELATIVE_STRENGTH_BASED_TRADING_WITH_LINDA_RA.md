# Candidate Card — CAND_022

- **Source intake:** `3 Mayıs/INTAKE_005_jD4nynuWfEU_raschke_relative_strength_janus_factor.md`
- **Source URL:** https://www.youtube.com/watch?v=jD4nynuWfEU`
- **Video ID:** jD4nynuWfEU
- **Title:** The Reality of Relative Strength Based Trading with Linda Raschke
- **Existing candidate id (if any):** CAND_20260503_RASCHKE_RS_JANUS_REGIME_jD4nynuWfEU
- **Codex status (intake):** i

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** CRYPTO
- **Native timeframe:** UNKNOWN
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
### Risk

Transcriptte choppy / range ortamında çok sayıda false signal uyarısı var. Bu yüzden bu detector tek başına producer olmamalı; regime filter ile kullanılmalı.

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
