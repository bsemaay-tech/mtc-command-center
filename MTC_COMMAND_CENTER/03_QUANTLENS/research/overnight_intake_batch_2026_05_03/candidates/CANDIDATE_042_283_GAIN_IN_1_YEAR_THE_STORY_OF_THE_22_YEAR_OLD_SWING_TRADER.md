# Candidate Card — CAND_042

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_lS9zbnLi1Gg_martin_luke_283_gain_swing_trader.md`
- **Source URL:** https://youtu.be/lS9zbnLi1Gg?si=vmGqb0X_iM3tCvw9`
- **Video ID:** lS9zbnLi1Gg
- **Title:** 283% Gain in 1 Year - The Story of the 22-Year-Old Swing Trader
- **Existing candidate id (if any):** YT_lS9zbnLi1Gg_20260503_A
- **Codex status (intake):** i

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** US_EQUITY
- **Native timeframe:** swing
- **MTC relevance:** PROCESS_ONLY
- **Testability:** REJECT_NOT_TESTABLE_AS_PRODUCER

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
### Setup Universe

```yaml
universe_filters:
  market: "US equities"
  min_price: [3, 5, 10]
  min_dollar_volume_20d: [10_000_000, 20_000_000, 50_000_000]
  min_ADR_pct_20d: [4, 5, 6, 8]
  avoid_low_liquidity: true
  small_micro_cap_position_cap: true
```

## Exit logic (raw extract)
### Exit Logic

```yaml
exit:
  trailing_ema_default: 9
  trailing_ema_runner_options: [21, 50]
  sell_into_strength:
    trim_size_pct: [10, 15]
    trigger_R: [3, 6, 8, 12]
    trigger_extended_from_ema9: true
    trigger_euphoria_manual_proxy: "parabolic_extension"
  weakness_exit:
    close_below_ema9: true
    break_swing_low: true
    break_bar_low: true
```

**MTC_V2 Bağlantısı:**

- `SIGNAL PRODUCER`: Tight Range Breakout producer
- `ENTRY GATES`: ADR, dollar volume, EMA stack, weekly context
- `POSITION SIZING`: tight-stop risk sizing + microcap cap
- `EXIT RULES`: 9 EMA / 21 EMA / swing low trailing; partial sells into strength

**Prototype Priority:** `VERY_HIGH`

## Stop logic (raw extract)
### Stop Logic

```yaml
stop:
  preferred_stop: "low_of_day"
  if_low_of_day_too_wide:
    use: "5m_entry_candle_low"
  max_stop_pct: [3, 4, 5]
  max_stop_as_ADR_fraction: [0.33, 0.50, 0.67]
  hard_stop_required: true
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
