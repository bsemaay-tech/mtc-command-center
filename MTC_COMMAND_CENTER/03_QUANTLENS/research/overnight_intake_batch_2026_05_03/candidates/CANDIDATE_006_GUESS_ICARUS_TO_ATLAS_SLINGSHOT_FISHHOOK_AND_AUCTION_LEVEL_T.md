# Candidate Card — CAND_006

- **Source intake:** `3 Mayıs/2026-05-03_c7ZSb2wNcOc_quantlens_detailed_intake.md`
- **Source URL:** https://youtu.be/c7ZSb2wNcOc?si=qdou6ffSbBNhJw63
- **Video ID:** c7ZSb2wNcOc
- **Title:** _guess: "Icarus to Atlas — Slingshot, Fishhook and Auction-Level Trading"
- **Existing candidate id (if any):** -
- **Codex status (intake):** -

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
_(see source intake)_

## Exit logic (raw extract)
_(see source intake)_

## Stop logic (raw extract)
### Risk / limitations

- Main examples are equities and earnings-gap stocks, not crypto.
- Fishhook depends heavily on earnings/catalyst logic, so it does not directly transfer to crypto.
- Icarus/Atlas pivot drawing is partly discretionary; codification requires approximations.
- Many examples rely on visual support/resistance and intraday chart reading.
- No full backtest table is provided in the transcript.
- Several claims are experience-based, not statistically proven inside the transcript.

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
