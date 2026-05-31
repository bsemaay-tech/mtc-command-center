# CANDIDATE_002 — Martin Luke Pullback AVWAP

## Source
- Source intake file: `06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs\INTAKE_2026-05-03_lS9zbnLi1Gg_martin_luke_283_gain_swing_trader.md`
- Source URL: https://youtu.be/lS9zbnLi1Gg?si=vmGqb0X_iM3tCvw9`
- YouTube ID: lS9zbnLi1Gg

## Candidate Card
- One-sentence thesis: Pullback into EMA/anchored VWAP confluence with reclaim trigger.
- Strategy family: support_reclaim
- Asset class: crypto_proxy/equity_native
- Native timeframe: 1D + 4h/1h
- Required data: OHLCV; true AVWAP improves with intraday volume
- Entry logic: Flush into support confluence, reclaim previous bar high.
- Exit logic: Partial at R targets and EMA trail.
- Initial SL logic: Local low or max stop.
- TP / trailing / partial logic: 3R/5R partials.
- Position sizing notes: R-based research sizing.
- MTC relevance: PRODUCER_CANDIDATE
- Testability: TEST_WITH_1D_CRYPTO_PROXY
- Priority tier: B
- Total score: 16

## Conservative Python Formalization
The first-pass prototype uses only OHLCV-derived rules, fixed research sizing, conservative fee/slippage, and no discretionary chart interpretation.

## Ambiguities
- Intake reports are normalized reports, not raw source videos.
- If the source strategy depends on discretionary chart reading, this card uses the most conservative mechanical proxy.

## Critical Caveats
- This is not Pine-ready.
- This is not production MTC integration.
- Crypto proxy results do not prove equity/session-native edge.
