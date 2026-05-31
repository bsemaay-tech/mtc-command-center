# Candidate Card — CAND_064

- **Source intake:** `3 Mayıs/YT_DLlNDuOTUfQ_Intake_Report_2026-05-03.md`
- **Source URL:** https://youtu.be/DLlNDuOTUfQ?si=_eUc_moFLJqb-qm-`
- **Video ID:** DLlNDuOTUfQ
- **Title:** Secrets to Profitable Trading from Market Legend Stan Weinstein
- **Existing candidate id (if any):** -
- **Codex status (intake):** READY_FOR_PYTHON_PROTOTYPE

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** US_EQUITY
- **Native timeframe:** UNKNOWN
- **MTC relevance:** PROCESS_ONLY
- **Testability:** REJECT_NOT_TESTABLE_AS_PRODUCER

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
#### Entry A — MA Reclaim Stage 2A

```text
enter_long when:
    close > SMA150
    AND close > SMA200
    AND close > base_high
    AND volume_confirmed
    AND group_strength_ok
```

## Exit logic (raw extract)
### Exit Rules

Potential exits:

```text
EXIT_MA50_BREAK
EXIT_KEY_REVERSAL_TRIM
EXIT_EXHAUSTION_GAP_TRIM
EXIT_GAP_FILL_FAIL
EXIT_STAGE3_DISTRIBUTION
```

Important: initial Python research can model trim as full exit first, then add partials later.

---

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
