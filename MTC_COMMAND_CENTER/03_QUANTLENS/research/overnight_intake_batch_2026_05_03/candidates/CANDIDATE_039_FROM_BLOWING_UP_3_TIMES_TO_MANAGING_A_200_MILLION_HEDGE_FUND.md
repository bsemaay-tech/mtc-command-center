# Candidate Card — CAND_039

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_jLioqyVlRkE_jim_roppel_200m_hedge_fund.md`
- **Source URL:** https://youtu.be/jLioqyVlRkE?si=HMyJ3lenMmbzZ0Tz`
- **Video ID:** jLioqyVlRkE
- **Title:** From Blowing Up 3 Times to Managing a $200 Million Hedge Fund — Exclusive Interview with Jim Roppel
- **Existing candidate id (if any):** YT_jLioqyVlRkE_20260503_A
- **Codex status (intake):** i

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** US_EQUITY
- **Native timeframe:** weekly
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
### Risk / Position Management

1. `three_five_seven_stop_guard_v1`
2. `monster_winner_management_v1`
3. `position_size_liquidity_cap_v1`
4. `correlated_growth_exposure_guard_v1`
5. `equity_feedback_size_modulator_v1`

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
