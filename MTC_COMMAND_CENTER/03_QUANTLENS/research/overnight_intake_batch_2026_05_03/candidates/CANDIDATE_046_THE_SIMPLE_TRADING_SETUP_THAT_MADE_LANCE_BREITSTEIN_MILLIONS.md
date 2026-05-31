# Candidate Card — CAND_046

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_R215f4fj7V8_lance_breitstein_trend_trading.md`
- **Source URL:** https://youtu.be/R215f4fj7V8?si=L3wGYRC2vMT5Bjb_
- **Video ID:** R215f4fj7V8
- **Title:** The Simple Trading Setup That Made Lance Breitstein Millions
- **Existing candidate id (if any):** suggestion
- **Codex status (intake):** n

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** US_EQUITY
- **Native timeframe:** 5m
- **MTC relevance:** PROCESS_ONLY
- **Testability:** REJECT_NOT_TESTABLE_AS_PRODUCER

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
### Setup Context

```text
prior_down_capitulation =
    intraday_downtrend_clean
    and price_extension_down >= min_extension
    and volume_spike >= 2x prior_bar_or_volume_ma
    and broad_market_or_symbol_panic
```

## Exit logic (raw extract)
### Exit

- Prior 2m/5m bar low kırılırsa çık.
- Euphoric upside capitulation olursa partial veya full exit.
- VWAP rejection varsa çık.
- Trendline break aşağıysa çık.

## Stop logic (raw extract)
### Stop

```text
initial_stop = recent_pivot_low
or low_of_trigger_bar
or prior_bar_low_trailing
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
