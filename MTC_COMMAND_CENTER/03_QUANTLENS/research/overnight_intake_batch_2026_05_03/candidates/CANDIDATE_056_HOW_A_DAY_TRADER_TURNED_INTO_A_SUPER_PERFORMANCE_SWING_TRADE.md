# Candidate Card — CAND_056

- **Source intake:** `3 Mayıs/QL_INTAKE_004_Nq_p7Bu1YT0_ariel_rs_leadergroup_swing.md`
- **Source URL:** https://youtu.be/Nq-p7Bu1YT0?si=jA26J6RGZtMXyY4v
- **Video ID:** Nq-p7Bu1YT0
- **Title:** How A Day Trader Turned into a Super-Performance Swing Trader - Real Simple Ariel
- **Existing candidate id (if any):** QL_CAND_004_Nq
- **Codex status (intake):** n

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** US_EQUITY
- **Native timeframe:** swing
- **MTC relevance:** PRODUCER_CANDIDATE
- **Testability:** TEST_WITH_1D_CRYPTO_PROXY

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
### Entry Gates

```text
GATE_MARKET_FOLLOW_THROUGH
GATE_RELATIVE_STRENGTH
GATE_LEADING_GROUP
GATE_ABOVE_200SMA_OR_RECLAIM
GATE_VOLUME_EXPANSION
GATE_ADR_POSITION_CAP
GATE_NO_ACTIVE_MARKET_BREAKDOWN
```

## Exit logic (raw extract)
### Exits

Candidate-specific exits:

```text
LOW_OF_DAY_STOP
PRIOR_DAY_LOW_STOP
FAILED_BREAKOUT_CLOSE_EXIT
BREAKEVEN_AFTER_FAST_MOVE
PARTIAL_PROFIT_FAST_MOVE
MA_TRAIL_10_20_50
GROUP_LEADERSHIP_BREAK_EXIT_OPTIONAL
```

---

## Stop logic (raw extract)
_(see source intake)_

## Sizing (raw extract)
### Position Sizing

Use MTC position sizing but add candidate-specific constraints:

```text
account_risk_pct <= 0.50
position size derived from technical stop distance
max_position_pct reduced by ADR
starter sizing after drawdown or first signal after correction
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
