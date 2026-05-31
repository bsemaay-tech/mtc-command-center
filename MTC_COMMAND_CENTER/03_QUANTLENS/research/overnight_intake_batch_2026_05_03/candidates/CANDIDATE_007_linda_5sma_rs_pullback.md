# CANDIDATE_007 — Linda 5SMA RS Pullback

## Source
- Source intake file: `06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs\2026-05-03_kTqKRi-j9kM_quantlens_linda_raschke_sell_rules_trade_management_intake.md`
- Source URL: https://youtu.be/kTqKRi-j9kM?si=99GgO3p0M-b25wBA
- YouTube ID: kTqKRi-j9kM

## Candidate Card
- One-sentence thesis: Trend asset pulls below 5SMA and exits on snapback.
- Strategy family: mean_reversion_pullback
- Asset class: crypto_transferable
- Native timeframe: 1D
- Required data: Daily OHLCV
- Entry logic: Above SMA50/200, close dips below SMA5, next open entry.
- Exit logic: Exit when close recovers above SMA5 or ATR stop.
- Initial SL logic: Optional ATR/fixed stop.
- TP / trailing / partial logic: Mean-reversion exit.
- Position sizing notes: 1x equity research sizing.
- MTC relevance: PRODUCER_CANDIDATE
- Testability: TEST_NOW_LOCAL_DATA
- Priority tier: A
- Total score: 24

## Conservative Python Formalization
The first-pass prototype uses only OHLCV-derived rules, fixed research sizing, conservative fee/slippage, and no discretionary chart interpretation.

## Ambiguities
- Intake reports are normalized reports, not raw source videos.
- If the source strategy depends on discretionary chart reading, this card uses the most conservative mechanical proxy.

## Critical Caveats
- This is not Pine-ready.
- This is not production MTC integration.
- Crypto proxy results do not prove equity/session-native edge.
