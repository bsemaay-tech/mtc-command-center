# Candidate Card — CAND_054

- **Source intake:** `3 Mayıs/QL_INTAKE_002_XOul_ECgHyA_sean_ryan_swing_system.md`
- **Source URL:** https://youtu.be/XOul-ECgHyA?si=lGRJSk2sTxtqli3v
- **Video ID:** XOul-ECgHyA
- **Title:** 100% Returns After Losing it all - Developing a Swing Trading System
- **Existing candidate id (if any):** QL_CAND_002_XOul_ECgHyA
- **Codex status (intake):** n

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** US_EQUITY
- **Native timeframe:** swing
- **MTC relevance:** PRODUCER_CANDIDATE
- **Testability:** TEST_WITH_1D_CRYPTO_PROXY

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
### Entry Gates

Recommended MTC_V2 gates:

```text
- HTF Trend Gate
- Momentum Gate / RSI Divergence Gate
- Volume Gate
- ATR Vol Floor
- ADX / Chop filter
- Session filter only if non-crypto
```

## Exit logic (raw extract)
### Exit Rules

```text
1. Protective stop first
2. RSI divergence / reversal-day discretionary exit converted to signal exit
3. Time stop / rotation exit
4. Optional filter-block exit when market regime deteriorates
```

Canonical MTC caution:

```text
Keep exit-first ordering. Do not allow an exhaustion exit and a new same-bar long entry to conflict.
```

---

## Stop logic (raw extract)
_(see source intake)_

## Sizing (raw extract)
### Position Sizing

Directly relevant:

```text
risk_pct = 1.0
stop_distance from chart structure
max_position_pct cap
max_total_exposure_pct cap
```

## Ambiguities
- Crypto-proxy applicability for US-equity-native setups (catalyst, gap, session).
- Discretionary "support/resistance" or "candle confirmation" rules require deterministic formalization before backtest.

## Conservative formalization for Python prototype
- Replace any discretionary subjective check with a single deterministic rule.
- If the strategy depends on US session, gap, or earnings catalyst, mark DATA_BLOCKED unless an explicit numeric proxy is documented in this card.

## Critical caveats
- Tonight's run is Python-only research; no Pine, no parity, no live alerts.
- A weak or rejected result is acceptable if evidence-based.
