# CANDIDATE_008 — 8AM ET Opening Range Breakout

## Source
- Source intake file: `06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs\2026-05-03_-JyH5PAJ4-Y_quantlens_nick_schmidt_weekly_character_change_intake.md`
- Source URL: https://youtu.be/-JyH5PAJ4-Y?si=BqaSaOarsfJIutKk
- YouTube ID: -JyH5PAJ4-Y

## Candidate Card
- One-sentence thesis: Session anchored opening range breakout.
- Strategy family: intraday_breakout
- Asset class: futures/session_native
- Native timeframe: 5m
- Required data: 5m session-aware OHLCV
- Entry logic: Break 08:00 ET opening range high/low.
- Exit logic: Time exit or opposite range side.
- Initial SL logic: Opposite OR side/ATR.
- TP / trailing / partial logic: Short holding period.
- Position sizing notes: Intraday strict costs.
- MTC relevance: PRODUCER_CANDIDATE
- Testability: TEST_WITH_5M_CRYPTO_PROXY
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
