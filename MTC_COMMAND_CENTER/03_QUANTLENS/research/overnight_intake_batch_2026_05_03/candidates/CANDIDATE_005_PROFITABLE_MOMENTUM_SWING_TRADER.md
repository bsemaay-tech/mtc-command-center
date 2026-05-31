# Candidate Card — CAND_005

- **Source intake:** `3 Mayıs/2026-05-03__QewlGLBaeA_quantlens_anthony_shi_cycle_aware_momentum_intake.md`
- **Source URL:** https://youtu.be/_QewlGLBaeA?si=ZoVcYdRIch1Lx_Df
- **Video ID:** _QewlGLBaeA
- **Title:** QUANTLENS TRANSCRIPT INTAKE REPORT — Anthony Shi / Profitable Momentum Swing Trader
- **Existing candidate id (if any):** -
- **Codex status (intake):** -

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** CRYPTO
- **Native timeframe:** 1d
- **MTC relevance:** PRODUCER_CANDIDATE
- **Testability:** TEST_WITH_1D_CRYPTO_PROXY

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
### Entry permission

```yaml
entry_filter:
  allow_long_if:
    - symbol_RS_rank_high
    - theme_RS_rank_high
    - market_health_not_bad
  block_or_reduce_if:
    - random_stock_no_theme
    - theme_is_late_and_euphoric
    - more_breakdowns_than_breakouts
```

This is highly relevant to MTC as a gate.

---

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
