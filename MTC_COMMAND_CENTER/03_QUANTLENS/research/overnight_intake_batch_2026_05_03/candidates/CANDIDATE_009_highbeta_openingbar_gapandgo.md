# CANDIDATE_009 — HighBeta Opening-Bar Gap-and-Go

## Source
- Source intake file: `06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs\2026-05-03_-JyH5PAJ4-Y_quantlens_nick_schmidt_weekly_character_change_intake.md`
- Source URL: https://youtu.be/-JyH5PAJ4-Y?si=BqaSaOarsfJIutKk
- YouTube ID: -JyH5PAJ4-Y

## Candidate Card
- One-sentence thesis: Strong first 5m bar continuation if low holds.
- Strategy family: intraday_momentum
- Asset class: US_equity_native/crypto_proxy
- Native timeframe: 5m
- Required data: US high-beta intraday with gaps; crypto proxy available
- Entry logic: First bar range extreme, hold low, break high.
- Exit logic: Time/ATR exit.
- Initial SL logic: First bar low.
- TP / trailing / partial logic: First-hour exit.
- Position sizing notes: Intraday strict costs.
- MTC relevance: PRODUCER_CANDIDATE
- Testability: TEST_WITH_5M_CRYPTO_PROXY
- Priority tier: B
- Total score: 15

## Conservative Python Formalization
The first-pass prototype uses only OHLCV-derived rules, fixed research sizing, conservative fee/slippage, and no discretionary chart interpretation.

## Ambiguities
- Intake reports are normalized reports, not raw source videos.
- If the source strategy depends on discretionary chart reading, this card uses the most conservative mechanical proxy.

## Critical Caveats
- This is not Pine-ready.
- This is not production MTC integration.
- Crypto proxy results do not prove equity/session-native edge.
