# Candidate Card — CAND_028

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03__AAX1ylNbIE_market_wizards_lessons.md`
- **Source URL:** https://youtu.be/_AAX1ylNbIE?si=GS5jQ8yvhFsDIQd1`
- **Video ID:** _AAX1ylNbIE
- **Title:** QuantLens Transcript Intake Report
- **Existing candidate id (if any):** STRAT_2026
- **Codex status (intake):** READY_FOR_PYTHON_PROTOTYPE

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
#### Setup Conditions

Long side draft:

1. HTF trend bullish.
2. Price above or reclaiming 21 EMA.
3. Recent higher low structure exists.
4. Volatility contraction detected:
   - range compression versus prior N bars, or
   - ATR percentile low, or
   - Bollinger Band width percentile low, or
   - custom RMV-like contraction proxy.
5. Breakout trigger:
   - close above local pivot high, or
   - close above tight range high, or
   - gap / impulse through range high with volume confirmation.

Short side:

- Video long-bias momentum / leader framework anlattığı için short taraf doğrudan önerilmez. MTC_V2 parity için ileride simetrik short test edilebilir; ilk prototype long-only olmalı.

## Exit logic (raw extract)
#### Take Profit / Exit

Test variants:

1. Trend exit: two closes below 21 EMA.
2. 50 SMA fail exit for position-trading variant.
3. Partial profit at 2R, runner exits on 21 EMA rule.
4. Time stop if no progress after N bars.
5. Opposite signal ignored in first long-only prototype.

## Stop logic (raw extract)
#### Stop Loss

Initial stop alternatives:

1. Tight range low minus ATR buffer.
2. 21 EMA minus ATR buffer.
3. Last higher low minus ATR buffer.
4. Fixed percent cap, e.g. max 3–5%, only as emergency cap.

Preferred first prototype:

```text
initial_stop = min(tight_range_low, last_swing_low) - ATR(14) * buffer
risk_invalid_if_stop_distance_pct > max_stop_pct
```

## Sizing (raw extract)
#### Position Sizing

- Risk percent per trade: small fixed risk in prototype, e.g. 0.25%–1.0% equity.
- Position notional capped by max leverage / max exposure.
- Reject trade if stop distance too wide.

## Ambiguities
- Crypto-proxy applicability for US-equity-native setups (catalyst, gap, session).
- Discretionary "support/resistance" or "candle confirmation" rules require deterministic formalization before backtest.

## Conservative formalization for Python prototype
- Replace any discretionary subjective check with a single deterministic rule.
- If the strategy depends on US session, gap, or earnings catalyst, mark DATA_BLOCKED unless an explicit numeric proxy is documented in this card.

## Critical caveats
- Tonight's run is Python-only research; no Pine, no parity, no live alerts.
- A weak or rejected result is acceptable if evidence-based.
