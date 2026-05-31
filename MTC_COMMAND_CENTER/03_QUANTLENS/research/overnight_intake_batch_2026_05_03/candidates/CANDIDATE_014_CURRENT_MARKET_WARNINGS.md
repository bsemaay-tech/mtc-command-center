# Candidate Card — CAND_014

- **Source intake:** `3 Mayıs/2026-05-03_O0GpSPtmCuM_quantlens_stan_weinstein_stage_analysis_intake.md`
- **Source URL:** https://youtu.be/O0GpSPtmCuM?si=Ra7X5w149KdMksmj
- **Video ID:** O0GpSPtmCuM
- **Title:** QUANTLENS TRANSCRIPT INTAKE REPORT — Stan Weinstein Stage Analysis / Current Market Warnings
- **Existing candidate id (if any):** -
- **Codex status (intake):** -

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** CRYPTO
- **Native timeframe:** weekly
- **MTC relevance:** PRODUCER_CANDIDATE
- **Testability:** TEST_WITH_1D_CRYPTO_PROXY

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
_(see source intake)_

## Exit logic (raw extract)
### Exit / stop

```yaml
initial_stop:
  - below_breakout_day_low
  - below_recent_swing_low
  - below_200d_if_nearby
  - below_gap_low_if_gap_breakout
risk_rule:
  reject_if_stop_distance_pct > [8, 10, 12]
```

---

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
