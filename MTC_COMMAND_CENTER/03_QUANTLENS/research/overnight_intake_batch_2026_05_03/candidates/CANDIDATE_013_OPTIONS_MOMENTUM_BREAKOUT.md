# Candidate Card — CAND_013

- **Source intake:** `3 Mayıs/2026-05-03_NGyE4YIgGpU_quantlens_tito_adhikary_options_momentum_intake_report.md`
- **Source URL:** https://youtu.be/NGyE4YIgGpU?si=gj_6ZcIyjUFAEGhk"
- **Video ID:** NGyE4YIgGpU
- **Title:** QuantLens Intake Report — Tito Adhikary / Options Momentum Breakout
- **Existing candidate id (if any):** -
- **Codex status (intake):** -

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** OPTIONS
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
### Risk Throttle Rules v0

```yaml
base_risk_pct:
  A_plus_setup_strong_market: 1.00
  normal_setup_good_market: 0.50
  choppy_market: 0.25
  weak_market: 0.00

drawdown_throttle:
  if_monthly_dd_pct <= -10:
    risk_multiplier: 0.50
    frequency_multiplier: 0.50
  if_monthly_dd_pct <= -15:
    risk_multiplier: 0.25
    frequency_multiplier: 0.25
  if_daily_loss_limit_hit:
    trade_allowed: false

weekly_cushion_logic:
  if_weekly_pnl_positive:
    allow_fraction_of_weekly_profit_as_risk: true
  if_weekly_pnl_negative:
    reduce_risk: true

mental_equity_proxy:
  after_large_loss:
    cooldown_trades_or_days: configurable
    reduce_size_until_new_equity_high_or_recovery_threshold: true
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
