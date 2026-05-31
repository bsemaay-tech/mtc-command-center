# Candidate Card — CAND_034

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_ElocJ-b_NTs_oliver_kell_10_principles.md`
- **Source URL:** https://youtu.be/ElocJ-b_NTs?si=5HoHV7QnhLAqXNM1
- **Video ID:** ElocJ-b_NTs
- **Title:** The 10 Principles of Trading with Investing Champion Oliver Kell
- **Existing candidate id (if any):** suggestion
- **Codex status (intake):** n

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** US_EQUITY
- **Native timeframe:** daily
- **MTC relevance:** PRODUCER_CANDIDATE
- **Testability:** TEST_WITH_1D_CRYPTO_PROXY

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
### Entry Logic Draft

```text
long_setup =
    market_regime in ["EARLY", "CONFIRMED"]
    and stock_close > ema20
    and stock_close > ema50
    and ema10 >= ema20
    and recent_pullback_to_ema_zone
    and tight_range_last_3_to_10_bars
    and breakout_above_pullback_high_or_trendline
    and stop_distance_pct <= max_stop_pct
    and not_extended_from_ema20
```

## Exit logic (raw extract)
### Exit Logic Draft

```text
initial_stop = min(recent_swing_low, ema20_buffer)
take_partial_if_R >= 1.5
raise_stop_to_breakeven_after_partial
sell_into_strength_if_extension_signal
exit_if_close_below_structure_stop
avoid_holding_full_size_into_earnings
```

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
