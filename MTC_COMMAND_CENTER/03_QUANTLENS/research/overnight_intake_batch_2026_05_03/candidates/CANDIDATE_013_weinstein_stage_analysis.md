# CANDIDATE_013 — Weinstein / Long-Base Stage Analysis

## Source
- Source intake file: `06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs\2026-05-03_O0GpSPtmCuM_quantlens_stan_weinstein_stage_analysis_intake.md`
- Source URL: https://youtu.be/O0GpSPtmCuM?si=Ra7X5w149KdMksmj
- YouTube ID: O0GpSPtmCuM

## Candidate Card
- One-sentence thesis: Position-trading trend stage and base breakout framework.
- Strategy family: position_trend
- Asset class: equity_native/crypto_proxy
- Native timeframe: 1D/1W
- Required data: Long history OHLCV, relative strength preferred
- Entry logic: Stage 2 breakout above base and rising MA.
- Exit logic: Stage deterioration or trailing MA.
- Initial SL logic: Base low.
- TP / trailing / partial logic: Long-term trail.
- Position sizing notes: Portfolio sleeve sizing.
- MTC relevance: PRODUCER_CANDIDATE
- Testability: TEST_WITH_1D_CRYPTO_PROXY
- Priority tier: B
- Total score: 17

## Conservative Python Formalization
The first-pass prototype uses only OHLCV-derived rules, fixed research sizing, conservative fee/slippage, and no discretionary chart interpretation.

## Ambiguities
- Intake reports are normalized reports, not raw source videos.
- If the source strategy depends on discretionary chart reading, this card uses the most conservative mechanical proxy.

## Critical Caveats
- This is not Pine-ready.
- This is not production MTC integration.
- Crypto proxy results do not prove equity/session-native edge.
