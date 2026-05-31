# Candidate Card — CAND_029

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_a4uJ3rHhbfA_anish_sikri_position_sizing.md`
- **Source URL:** https://youtu.be/a4uJ3rHhbfA?si=hD9z9rji3O6XbMnj
- **Video ID:** a4uJ3rHhbfA
- **Title:** The Art of Position Sizing with Anish Sikri | US Investing Championship Top Contender
- **Existing candidate id (if any):** -
- **Codex status (intake):** n

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
### Trigger Mantığı

Başlangıçta veya kötü feedback dönemlerinde:

```text
if no_profit_cushion or loss_streak_active:
    size_mode = MICRO_PROBE or HALF_BLOCK
```

Traction geldikçe:

```text
if recent_trades_profitable and equity_above_recent_high:
    size_mode = HALF_BLOCK -> FULL_BLOCK
```

---

## Exit logic (raw extract)
_(see source intake)_

## Stop logic (raw extract)
### Risk Management

- Stop below 50-day area / prior technical level
- Tight stop, around 2–5% zone
- Fast gain captured; 20% in two days example

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
