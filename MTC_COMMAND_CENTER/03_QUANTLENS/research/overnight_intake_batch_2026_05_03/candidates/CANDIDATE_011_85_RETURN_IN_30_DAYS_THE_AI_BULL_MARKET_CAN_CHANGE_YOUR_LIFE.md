# Candidate Card — CAND_011

- **Source intake:** `3 Mayıs/2026-05-03_MnXQOt7_ZP0_quantlens_jim_roppel_ai_bull_market_intake_report.md`
- **Source URL:** https://youtu.be/MnXQOt7_ZP0?si=OdvX4hI-qnjYMKZp
- **Video ID:** MnXQOt7_ZP0
- **Title:** +85% Return in 30 Days The AI Bull Market Can Change your Life Hedge Fund Manager
- **Existing candidate id (if any):** -
- **Codex status (intake):** -

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** US_EQUITY
- **Native timeframe:** position
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
### Risk

```yaml
stop_variants:
  - below_tight_range_low
  - below_sma50_minus_atr_buffer
  - 3_5_7_scaleout
exit_variants:
  - break_sma50_confirmed
  - close_below_sma50_2_days
  - fixed_R_multiple
  - trailing_ema21_or_sma50
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
