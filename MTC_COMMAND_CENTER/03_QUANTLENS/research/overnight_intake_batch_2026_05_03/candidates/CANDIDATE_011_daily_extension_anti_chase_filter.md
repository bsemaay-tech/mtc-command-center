# CANDIDATE_011 — Daily Extension Anti-Chase Filter

## Source
- Source intake file: `06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs\QUANTLENS_DAILY_EXTENSION_ANTI_CHASE_CRITICAL_REPORT.md`
- Source URL: https://youtu.be/Yb5lMegA5Hs?si=_zP9cjzTaZN8vh4w
- YouTube ID: Yb5lMegA5Hs

## Candidate Card
- One-sentence thesis: Block late long/short entries after consecutive extended candles.
- Strategy family: filter
- Asset class: crypto_transferable
- Native timeframe: 1D context
- Required data: Daily OHLCV plus target strategy trades
- Entry logic: Not standalone; blocks entries after 3-5 strong candles.
- Exit logic: N/A
- Initial SL logic: N/A
- TP / trailing / partial logic: N/A
- Position sizing notes: Filter score only.
- MTC relevance: FILTER_CANDIDATE
- Testability: TEST_NOW_LOCAL_DATA
- Priority tier: A
- Total score: 23

## Conservative Python Formalization
The first-pass prototype uses only OHLCV-derived rules, fixed research sizing, conservative fee/slippage, and no discretionary chart interpretation.

## Ambiguities
- Intake reports are normalized reports, not raw source videos.
- If the source strategy depends on discretionary chart reading, this card uses the most conservative mechanical proxy.

## Critical Caveats
- This is not Pine-ready.
- This is not production MTC integration.
- Crypto proxy results do not prove equity/session-native edge.
