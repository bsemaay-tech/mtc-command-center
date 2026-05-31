# CANDIDATE_012 — EMA20/50 Two-Retest Baseline

## Source
- Source intake file: `06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs\QUANTLENS_EMA20_50_RETEST_CRITICAL_INTAKE_REPORT.md`
- Source URL: https://youtu.be/RHlsVNSM8Aw?si=g54Kry_ryc8pYWPK
- YouTube ID: RHlsVNSM8Aw

## Candidate Card
- One-sentence thesis: Generic EMA20/50 cross plus two retests baseline.
- Strategy family: baseline_trend
- Asset class: crypto_transferable
- Native timeframe: 1h/4h/1D
- Required data: OHLCV
- Entry logic: Cross then two successful retests.
- Exit logic: Opposite cross/EMA50/ATR.
- Initial SL logic: Retest swing or ATR.
- TP / trailing / partial logic: 2R/3R variants.
- Position sizing notes: 1x equity research sizing.
- MTC relevance: BASELINE_ONLY
- Testability: TEST_NOW_LOCAL_DATA
- Priority tier: A
- Total score: 18

## Conservative Python Formalization
The first-pass prototype uses only OHLCV-derived rules, fixed research sizing, conservative fee/slippage, and no discretionary chart interpretation.

## Ambiguities
- Intake reports are normalized reports, not raw source videos.
- If the source strategy depends on discretionary chart reading, this card uses the most conservative mechanical proxy.

## Critical Caveats
- This is not Pine-ready.
- This is not production MTC integration.
- Crypto proxy results do not prove equity/session-native edge.
