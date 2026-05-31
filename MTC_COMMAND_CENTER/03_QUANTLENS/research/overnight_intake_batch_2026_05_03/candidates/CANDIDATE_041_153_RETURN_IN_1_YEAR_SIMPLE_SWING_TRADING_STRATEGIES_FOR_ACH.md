# Candidate Card — CAND_041

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_lpjTNygfnzM_deepak_swing_trading_triple_digit_returns.md`
- **Source URL:** https://www.youtube.com/watch?v=lpjTNygfnzM
- **Video ID:** lpjTNygfnzM
- **Title:** 153% Return in 1 Year - Simple Swing Trading Strategies for Achieving Triple Digit Returns
- **Existing candidate id (if any):** QL
- **Codex status (intake):** i

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** US_EQUITY
- **Native timeframe:** swing
- **MTC relevance:** PROCESS_ONLY
- **Testability:** REJECT_NOT_TESTABLE_AS_PRODUCER

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
#### Entry Trigger

Bir veya birden fazla:

- Downtrend line break.
- Prior-day high breakout.
- Tight flag breakout.
- Shakeout sonrası range reclaim.
- Earnings gap sonrası 6–10 gün sıkışma ve tekrar breakout.
- Strong theme leader rotation.

## Exit logic (raw extract)
#### Exit

- Initial stop: setup low / prior day low / flag low.
- Profit taking:
  - 2R–4R arası partial veya full exit.
  - Hızlı hareketlerde strength'e satış.
  - Market bozulursa risk azalt.
- Earnings öncesi genellikle çık.

## Stop logic (raw extract)
#### Stop

- Half stop: opening low.
- Half stop: most recent intraday higher-low.
- VIX kapanışa doğru tekrar yükselirse lighten up.

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
