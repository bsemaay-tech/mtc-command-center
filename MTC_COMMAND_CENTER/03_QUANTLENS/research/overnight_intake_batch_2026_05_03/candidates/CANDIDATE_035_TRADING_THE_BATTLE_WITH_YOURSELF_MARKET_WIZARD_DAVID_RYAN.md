# Candidate Card — CAND_035

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_eWtY7uoJL_0_david_ryan_price_volume_discipline.md`
- **Source URL:** https://youtu.be/eWtY7uoJL_0?si=9_3CvT5T5e5HyILo
- **Video ID:** eWtY7uoJL_0
- **Title:** Trading The Battle With Yourself | Market Wizard David Ryan
- **Existing candidate id (if any):** suggestion
- **Codex status (intake):** n

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
### Setup Conditions

```text
prior_uptrend = close > sma50 and sma50 > sma200
base_duration >= min_base_bars
base_depth_pct <= max_base_depth
recent_tightness_pct <= tightness_threshold
pivot = highest_high(base_window)
price_near_pivot = close >= pivot * (1 - near_pivot_pct)
volume_dryup = avg_volume(recent_tight_window) < avg_volume(base_window) * dryup_ratio
```

## Exit logic (raw extract)
### Exit Conditions

```text
downside_volume_spike = close < open and volume > volume_ma * spike_mult
weak_rally = close > close[1] and volume < volume_ma and close < recent_high
trendline_break = close < rising_trendline_proxy
ma_break = close < sma20 or close < sma50

character_change_score =
    downside_volume_spike_count
    + weak_rally_count
    + ma_break_score
    + gap_down_score
    + failed_breakout_score

exit_or_reduce = character_change_score >= threshold
```

## Stop logic (raw extract)
### Stop Logic

```text
initial_stop = min(low_of_tight_area, entry_price * (1 - max_stop_pct))
```

Ryan’ın yaklaşımında tight area’dan alındığında stop çoğu zaman 3–4% gibi yakın olur. Maksimum kayıp 8% üstüne taşınmamalıdır.

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
