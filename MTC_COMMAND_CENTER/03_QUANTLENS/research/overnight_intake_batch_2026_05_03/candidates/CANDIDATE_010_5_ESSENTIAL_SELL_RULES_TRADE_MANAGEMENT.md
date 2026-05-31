# Candidate Card — CAND_010

- **Source intake:** `3 Mayıs/2026-05-03_kTqKRi-j9kM_quantlens_linda_raschke_sell_rules_trade_management_intake.md`
- **Source URL:** https://youtu.be/kTqKRi-j9kM?si=99GgO3p0M-b25wBA
- **Video ID:** kTqKRi-j9kM
- **Title:** QUANTLENS TRANSCRIPT INTAKE REPORT — Linda Bradford Raschke / 5 Essential Sell Rules & Trade Management
- **Existing candidate id (if any):** -
- **Codex status (intake):** -

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** CRYPTO
- **Native timeframe:** daily
- **MTC relevance:** PRODUCER_CANDIDATE
- **Testability:** TEST_WITH_1D_CRYPTO_PROXY

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
_(see source intake)_

## Exit logic (raw extract)
### Sell Rule 1 — Fix execution mistakes immediately

```yaml
rule_id: LBR_SELL_RULE_01_FLATTEN_MISTAKES
type: execution_risk_rule
trigger:
  - unintended_position
  - wrong_symbol
  - wrong_side
  - wrong_size
  - trade_not_matching_plan
action:
  - flatten_immediately
  - do_not_check_profit_or_loss_first
```

Interpretation:

If the position is not the intended trade, exit immediately. Do not rationalize. Do not convert an execution error into a discretionary gamble.

## Stop logic (raw extract)
_(see source intake)_

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
