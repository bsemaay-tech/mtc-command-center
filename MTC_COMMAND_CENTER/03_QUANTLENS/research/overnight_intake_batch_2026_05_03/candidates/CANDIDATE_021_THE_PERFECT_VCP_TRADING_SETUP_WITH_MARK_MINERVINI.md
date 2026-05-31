# Candidate Card — CAND_021

- **Source intake:** `3 Mayıs/INTAKE_004_M_tD6X0CSOI_the_perfect_vcp_trading_setup_mark_minervini.md`
- **Source URL:** https://youtu.be/M_tD6X0CSOI?si=7w03YALv0bHJJJUE`
- **Video ID:** M_tD6X0CSOI
- **Title:** The Perfect VCP Trading Setup with Mark Minervini
- **Existing candidate id (if any):** CAND_20260503_MINERVINI_VCP_CORRECTION_LEADERS_M_tD6X0CSOI
- **Codex status (intake):** i

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** CRYPTO
- **Native timeframe:** UNKNOWN
- **MTC relevance:** PROCESS_ONLY
- **Testability:** REJECT_NOT_TESTABLE_AS_PRODUCER

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
### Entry

```text
entry = close on confirmed breakout bar
OR next_open after confirmed breakout
```

For parity-first research, use bar-close confirmed entry first. Intraday entry tactics can be later mapped from 002.

## Exit logic (raw extract)
### Exit / Partial Sell Into Strength

Transcript gives discretionary sell-into-strength guidance but not enough for strict first prototype. For now:

```text
phase_1_exit = initial_stop only + optional 2R/3R diagnostic labels
phase_2_exit = partial sell into strength after extension from MA / R multiple
```

Do not overfit exits in first implementation.

---

## Stop logic (raw extract)
### Stop Ideas

```text
initial_stop = min(last_contraction_low, short_range_low) - buffer
risk_pct = (entry_price - initial_stop) / entry_price
valid_risk = risk_pct <= max_risk_pct
```

Recommended initial research max risk:

```text
max_risk_pct = 2% to 6% depending on timeframe and stock volatility
```

---

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
