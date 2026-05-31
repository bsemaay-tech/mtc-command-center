# Candidate Card — CAND_020

- **Source intake:** `3 Mayıs/INTAKE_003_NwgJQyoUAaI_pro_swing_trading_setups_ep2.md`
- **Source URL:** https://youtu.be/NwgJQyoUAaI?si=IuOBlOwf_231Oftz`
- **Video ID:** NwgJQyoUAaI
- **Title:** Pro Swing Trading Setups For Consistent Gains Ultimate Trading Guide Ep 2
- **Existing candidate id (if any):** CAND_20260503_SETUP_FRAMEWORK_NwgJQyoUAaI
- **Codex status (intake):** i

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** CRYPTO
- **Native timeframe:** swing
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
### Initial Stop Ideas

```text
stop = min(recent_swing_low, ma_cluster_low - buffer)
```

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
