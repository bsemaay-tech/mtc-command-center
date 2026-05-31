# CANDIDATE_010 — Ty Rajnus Microcap Liquidity Reversion Short

## Source
- Source intake file: `06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs\QUANTLENS_TY_RAJNUS_MICROCAP_SHORT_INTAKE_REPORT.md`
- Source URL: https://youtu.be/bRXO6F_vGjM?si=N4P30T_3_i-IHPP4
- YouTube ID: bRXO6F_vGjM

## Candidate Card
- One-sentence thesis: US microcap premarket overextension short with borrow/halt constraints.
- Strategy family: microcap_short
- Asset class: US_microcap_native
- Native timeframe: 1m/premarket
- Required data: US microcap 1m, premarket, borrow/locate, dilution, halt flags
- Entry logic: Short overextended microcap near open.
- Exit logic: No overnight, cover near close.
- Initial SL logic: Wide adverse stop and halt rules.
- TP / trailing / partial logic: Intraday reversion.
- Position sizing notes: Borrow-aware short sizing.
- MTC relevance: DATA_BLOCKED
- Testability: NEEDS_US_MICROCAP_DATA
- Priority tier: C
- Total score: -1

## Conservative Python Formalization
The first-pass prototype uses only OHLCV-derived rules, fixed research sizing, conservative fee/slippage, and no discretionary chart interpretation.

## Ambiguities
- Intake reports are normalized reports, not raw source videos.
- If the source strategy depends on discretionary chart reading, this card uses the most conservative mechanical proxy.

## Critical Caveats
- This is not Pine-ready.
- This is not production MTC integration.
- Crypto proxy results do not prove equity/session-native edge.
