# Candidate Card — CAND_018

- **Source intake:** `3 Mayıs/INTAKE_001_Lot25-2fb-4_433_return_poker_player_full_time_trader.md`
- **Source URL:** https://youtu.be/Lot25-2fb-4?si=YHKVb3kJfybusO5o`
- **Video ID:** Lot25-2fb-4
- **Title:** 433% Return in 1 Year From Poker Player to Full Time Trader
- **Existing candidate id (if any):** CAND_20260503_EP_PROGRESSIVE_EXPOSURE_Lot25_2fb_4
- **Codex status (intake):** i

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** CRYPTO
- **Native timeframe:** 1m
- **MTC relevance:** PROCESS_ONLY
- **Testability:** REJECT_NOT_TESTABLE_AS_PRODUCER

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
#### Entry Rule Draft

```text
LONG if:
  regular_session_open is active
  AND gap_up_pct >= gap_threshold
  AND opening_volume_zscore >= volume_threshold
  AND price breaks above opening_range_high
  AND stock is near all-time high or recent 52-week high
  AND market regime is supportive
```

## Exit logic (raw extract)
### Exit Rules

MTC_V2 can reuse:

- initial SL
- BE
- trailing stop
- time stop
- partial exit logic if available

## Stop logic (raw extract)
#### Initial Stop Draft

```text
initial_stop = opening_range_low
risk_per_share = entry_price - initial_stop
```

## Sizing (raw extract)
### Position Sizing Draft

```text
base_risk_pct = 0.25% to 0.50%
normal_risk_pct = 0.50% to 1.00%
A_plus_risk_pct = 1.00% to 2.00%

if rolling_drawdown > dd_limit:
    risk_pct = min_risk_pct
elif recent_loss_streak >= loss_streak_limit:
    risk_pct = min_risk_pct
elif month_pnl_pct > cushion_threshold and setup_quality == A_PLUS:
    risk_pct = A_plus_risk_pct
else:
    risk_pct = base_or_normal_risk_pct
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
