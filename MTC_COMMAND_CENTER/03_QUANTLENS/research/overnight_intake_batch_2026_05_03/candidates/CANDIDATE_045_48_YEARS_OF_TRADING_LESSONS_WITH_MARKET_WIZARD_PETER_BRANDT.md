# Candidate Card — CAND_045

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_R1sNTB2Vh7w_peter_brandt_48_years_trading_lessons.md`
- **Source URL:** https://youtu.be/R1sNTB2Vh7w?si=XnkewkLqMeGAOqVg`
- **Video ID:** R1sNTB2Vh7w
- **Title:** 48 Years of Trading Lessons with Market Wizard Peter Brandt
- **Existing candidate id (if any):** YT_R1sNTB2Vh7w_20260503_A
- **Codex status (intake):** i

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** FUTURES
- **Native timeframe:** swing
- **MTC relevance:** PROCESS_ONLY
- **Testability:** REJECT_NOT_TESTABLE_AS_PRODUCER

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
_(see source intake)_

## Exit logic (raw extract)
### Exit / Trade Management

1. `pattern_height_target_1x_2x_v1`
2. `tranche_exit_policy_v1`
3. `breakeven_after_initial_progress_v1`
4. `early_failure_cut_v1`
5. `winner_room_policy_v1`

## Stop logic (raw extract)
### Risk / Position Management

1. `risk_budget_guard_brandt_v1`
2. `correlated_exposure_guard_v1`
3. `pareto_trade_management_v1`
4. `max_worst_loss_bps_guard_v1`
5. `capital_basis_normalizer_v1`

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
