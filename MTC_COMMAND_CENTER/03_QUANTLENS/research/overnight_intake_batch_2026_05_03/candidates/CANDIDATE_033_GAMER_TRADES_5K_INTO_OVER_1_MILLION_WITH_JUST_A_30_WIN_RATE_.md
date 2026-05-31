# Candidate Card — CAND_033

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_DPA35Gug3Y4_brian_lee_smallcap_mean_reversion_progressive_exposure.md`
- **Source URL:** https://youtu.be/DPA35Gug3Y4?si=tgHSwpjijUJECVZU`
- **Video ID:** DPA35Gug3Y4
- **Title:** Gamer Trades $5k into over $1 Million with just a 30% Win Rate - Brian Lee Trades
- **Existing candidate id (if any):** -
- **Codex status (intake):** n

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** US_MICROCAP
- **Native timeframe:** daily
- **MTC relevance:** DATA_BLOCKED
- **Testability:** NEEDS_US_MICROCAP_DATA

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
### Entry Gates

Potential gates:

```text
liquidity_gate
borrow_availability_gate
news_quality_gate
fundamental_short_gate
cycle_heat_gate
halt_risk_gate
spread_slippage_gate
session_time_gate
```

## Exit logic (raw extract)
### Exit Rules

Potential exit stack:

```text
protective_stop
partial_cover_R
prior_close_target
gap_fill_target
moving_average_target
time_stop
structure_reclaim_exit
```

---

## Stop logic (raw extract)
_(see source intake)_

## Sizing (raw extract)
### Position Sizing

Use R-based sizing:

```text
risk_pct
max_ticker_R
max_daily_R
equity_trailing_risk_base
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
