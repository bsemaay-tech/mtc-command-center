# Candidate Card — CAND_057

- **Source intake:** `3 Mayıs/QL_INTAKE_005_7UfHg8PpDZk_marios_three_setup_superperformance.md`
- **Source URL:** https://youtu.be/7UfHg8PpDZk?si=0mLL1k1aOKmlfSS4
- **Video ID:** 7UfHg8PpDZk
- **Title:** The 3 Powerful Trading Setups of a Top Super-performance Trader
- **Existing candidate id (if any):** QL_CAND_005_7UfHg8PpDZk
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

Useful MTC_V2 gates:

- MA alignment gate
- Volume / relative volume gate
- ATR / ADR volatility gate
- Momentum / relative strength gate
- Level proximity / pivot gate
- Session gate for intraday prototypes
- HTF trend / market regime gate

## Exit logic (raw extract)
### Exits

Required exit modules:

- low-of-day stop
- same-day failure stop
- no-red-overnight exit
- breakeven stop
- ADR-multiple partial profit
- MA trail exit
- failed add / failed breakout exit
- retry limiter

---

## Stop logic (raw extract)
_(see source intake)_

## Sizing (raw extract)
### Position Sizing

Required sizing module:

```text
risk_pct_per_trade = 0.25% to 0.4%
max_single_position_pct = 25% to 30%
stop_distance = entry_price - stop_price
position_size = risk_budget / stop_distance
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
