# Candidate Card — CAND_048

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_RTHRh_GLwH8_mark_ritchie_low_risk_breakout_pyramid.md`
- **Source URL:** https://youtu.be/RTHRh_GLwH8?si=NyxT_vvKDrHwMv64
- **Video ID:** RTHRh_GLwH8
- **Title:** 100% Trading Returns - How to become a Super Trade with Mark Ritchie
- **Existing candidate id (if any):** QC_2026
- **Codex status (intake):** READY_FOR_PYTHON_PROTOTYPE

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** CRYPTO
- **Native timeframe:** swing
- **MTC relevance:** PRODUCER_CANDIDATE
- **Testability:** TEST_WITH_1D_CRYPTO_PROXY

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
### Entry Gates

- MA trend gate
- MA slope gate
- ATR volatility floor
- Volume gate
- Momentum / relative strength gate
- Level proximity / pivot gate
- Session gate, crypto için opsiyonel.

## Exit logic (raw extract)
### Exit Rules

Mevcut MTC_V2 exit altyapısına çok uygun:

- INITIAL_SL
- PARTIAL_TP
- BREAK_EVEN
- TRAIL
- TIME_STOP
- FILTER_BLOCK veya regime exit.

## Stop logic (raw extract)
_(see source intake)_

## Sizing (raw extract)
### Position Sizing

MTC_V2'nin mevcut risk_pct, max_leverage_cap, notional check ve fallback sizing katmanları kullanılmalı.

Eklenmesi önerilen araştırma-only state:

- `adaptive_risk_multiplier`
- `consecutive_losses`
- `recent_R_window`
- `equity_near_high`
- `risk_after_add`.

## Ambiguities
- Crypto-proxy applicability for US-equity-native setups (catalyst, gap, session).
- Discretionary "support/resistance" or "candle confirmation" rules require deterministic formalization before backtest.

## Conservative formalization for Python prototype
- Replace any discretionary subjective check with a single deterministic rule.
- If the strategy depends on US session, gap, or earnings catalyst, mark DATA_BLOCKED unless an explicit numeric proxy is documented in this card.

## Critical caveats
- Tonight's run is Python-only research; no Pine, no parity, no live alerts.
- A weak or rejected result is acceptable if evidence-based.
