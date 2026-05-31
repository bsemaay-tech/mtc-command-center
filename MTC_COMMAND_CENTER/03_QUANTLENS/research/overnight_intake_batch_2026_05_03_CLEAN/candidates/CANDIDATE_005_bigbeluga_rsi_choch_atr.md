# CANDIDATE_005 — BigBeluga RSI Divergence + CHoCH + ATR

## Source
- Source intake file: `06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs\2026-05-03_-JyH5PAJ4-Y_quantlens_nick_schmidt_weekly_character_change_intake.md`
- Source URL: https://youtu.be/-JyH5PAJ4-Y?si=BqaSaOarsfJIutKk
- YouTube ID: -JyH5PAJ4-Y

## Candidate Card
- One-sentence thesis: RSI divergence confirmed by market structure shift with ATR management.
- Strategy family: reversal_structure
- Asset class: crypto_transferable
- Native timeframe: 4h/1D
- Required data: OHLCV with pivot confirmation
- Entry logic: Confirmed divergence plus CHoCH, next bar open.
- Exit logic: ATR trail or opposite CHoCH.
- Initial SL logic: ATR stop.
- TP / trailing / partial logic: ATR target ladder.
- Position sizing notes: 1x equity research sizing.
- MTC relevance: PRODUCER_CANDIDATE
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
