# Candidate Card — CAND_025

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_4-IjRmw7SZI_tqqq_key_strategies.md`
- **Source URL:** https://www.youtube.com/watch?v=4-IjRmw7SZI
- **Video ID:** 4-IjRmw7SZI
- **Title:** The Reality of Trading TQQQ and Key Strategies
- **Existing candidate id (if any):** -
- **Codex status (intake):** READY_FOR_PYTHON_PROTOTYPE

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** US_EQUITY
- **Native timeframe:** 1m
- **MTC relevance:** PROCESS_ONLY
- **Testability:** REJECT_NOT_TESTABLE_AS_PRODUCER

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
## Entry Rule

```text
If TQQQ 3-month return > defensive ETF 3-month return:
    enter/hold TQQQ
else:
    enter/hold defensive ETF/cash proxy
```

## Exit logic (raw extract)
## Exit Rule

```text
Exit TQQQ when its 3-month relative strength falls below defensive ETF at month-end.
```

## Stop logic (raw extract)
## Risks

- TQQQ path dependency and daily-reset decay.
- Monthly rebalance can react slowly during crash windows.
- Backtest may be overly sensitive to lookback period.
- Defensive ETF choice can materially change results.
- Speaker’s backtest references need independent verification.

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
