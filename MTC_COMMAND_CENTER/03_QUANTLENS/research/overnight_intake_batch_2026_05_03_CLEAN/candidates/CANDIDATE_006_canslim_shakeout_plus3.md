# CANDIDATE_006 — CANSLIM Shakeout +3

## Source
- Source intake file: `06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs\2026-05-03_9ZJK8175drM_quantlens_canslim_detailed_intake.md`
- Source URL: https://youtu.be/9ZJK8175drM?si=QcTE0mdW00UzcL_B
- YouTube ID: 9ZJK8175drM

## Candidate Card
- One-sentence thesis: Equity-specific double-bottom shakeout buy point.
- Strategy family: position_breakout
- Asset class: US_equity_native
- Native timeframe: 1D
- Required data: US equities OHLCV plus RS/fundamental context
- Entry logic: Second low undercuts first low; buy point L1+3 or percentage equivalent.
- Exit logic: Fixed target variants.
- Initial SL logic: 7% stop.
- TP / trailing / partial logic: 20%/25% target.
- Position sizing notes: Position-trading sizing only.
- MTC relevance: PRODUCER_CANDIDATE
- Testability: NEEDS_US_EQUITY_DATA
- Priority tier: C
- Total score: 8

## Conservative Python Formalization
The first-pass prototype uses only OHLCV-derived rules, fixed research sizing, conservative fee/slippage, and no discretionary chart interpretation.

## Ambiguities
- Intake reports are normalized reports, not raw source videos.
- If the source strategy depends on discretionary chart reading, this card uses the most conservative mechanical proxy.

## Critical Caveats
- This is not Pine-ready.
- This is not production MTC integration.
- Crypto proxy results do not prove equity/session-native edge.
