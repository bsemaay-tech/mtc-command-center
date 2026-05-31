# CANDIDATE_001 — Kell Wedge Pop / EMA Crossback

## Source
- Source intake file: `06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs\2026-05-03_fYxSQvuwOQc_quantlens_oliver_kell_cycle_intake.md`
- Source URL: https://youtu.be/fYxSQvuwOQc?si=mZyENAdFJu8x7LKZ
- YouTube ID: fYxSQvuwOQc

## Candidate Card
- One-sentence thesis: Trend continuation after EMA10/20 contraction and reclaim.
- Strategy family: trend_pullback
- Asset class: crypto_transferable
- Native timeframe: 1D/4h/1h
- Required data: OHLCV with daily and intraday bars
- Entry logic: EMA10 above EMA20, recent compression, close reclaims fast EMA.
- Exit logic: Close below EMA20 or ATR/time exit.
- Initial SL logic: Mini-base low or 2 ATR.
- TP / trailing / partial logic: Trail on EMA10/20 ride.
- Position sizing notes: 1x equity research sizing.
- MTC relevance: PRODUCER_CANDIDATE
- Testability: TEST_NOW_LOCAL_DATA
- Priority tier: A
- Total score: 22

## Conservative Python Formalization
The first-pass prototype uses only OHLCV-derived rules, fixed research sizing, conservative fee/slippage, and no discretionary chart interpretation.

## Ambiguities
- Intake reports are normalized reports, not raw source videos.
- If the source strategy depends on discretionary chart reading, this card uses the most conservative mechanical proxy.

## Critical Caveats
- This is not Pine-ready.
- This is not production MTC integration.
- Crypto proxy results do not prove equity/session-native edge.
