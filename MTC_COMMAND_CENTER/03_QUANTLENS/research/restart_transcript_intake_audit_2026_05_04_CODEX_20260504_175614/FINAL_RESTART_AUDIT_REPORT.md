# Final Restart Audit Report

## 1. Executive summary
Restart audit completed from local transcript and intake files. No strategy was backtested, promoted to Pine, or claimed profitable.

## 2. Transcript count
70

## 3. Intake count
74

## 4. Match success/failure
- Matched rows: 66
- Transcript without intake: 5
- Intake without transcript: 8

## 5. Corrected intake count
17

## 6. Major intake errors found
|video_id|title|intake_faithfulness|missing_fields|
|---|---|---|---|
|9ZJK8175drM|2026-05-03_9ZJK8175drM_quantlens_canslim_detailed_intake|WRONG_SOURCE_MATCH|source transcript|
|c7ZSb2wNcOc|2026-05-03_c7ZSb2wNcOc_quantlens_detailed_intake|WRONG_SOURCE_MATCH|source transcript|
|fYxSQvuwOQc|2026-05-03_fYxSQvuwOQc_quantlens_oliver_kell_cycle_intake|WRONG_SOURCE_MATCH|source transcript|
|Ne3X-l6W4CQ|"Process adherence, overtrading and behavior analytics playbook"|WRONG_SOURCE_MATCH|source transcript|
|Tm0dkf8_giA|+50% in 20 Days - How to Trade Breakouts with The Volatility Contraction Pattern (VCP|PARTIAL_MISSING_IMPORTANT_WISDOM|warnings_caveats|
|XNZ4f-b3ED8|2026-05-03_XNZ4f-b3ED8_quantlens_intake_indicator_audit|WRONG_SOURCE_MATCH|source transcript|
|6aOnCK1gv2w|+1300% Return in 2 Years The Setups Rules Hard Won Lessons Behind Chris Flander's Edge|PARTIAL_MISSING_IMPORTANT_WISDOM|warnings_caveats|
|6tnREqUJ1WY|Trading Backtests Are Misleading - Here's what to do instead|PARTIAL_MISSING_IMPORTANT_WISDOM|warnings_caveats|
|lTiR1pc82EE|5 Simple & Effective Trading Setups of Market Wizards|PARTIAL_MISSING_IMPORTANT_WISDOM|warnings_caveats; trader_wisdom|
|R215f4fj7V8|The Simple Trading Setup That Made Lance Breitstein Millions|PARTIAL_MISSING_IMPORTANT_WISDOM|trader_wisdom|
|RTHRh_GLwH8|100% Trading Returns - How to become a Super Trade with Mark Ritchie|PARTIAL_MISSING_IMPORTANT_WISDOM|warnings_caveats|
|UMgJ0P8fe0s|Swing Trading Vs|PARTIAL_MISSING_IMPORTANT_WISDOM|market_asset_class; trader_wisdom|
|zw96qkUn9_g|How Clement Ang Achieved 150%+ Returns in the US Investing Championship|PARTIAL_MISSING_IMPORTANT_WISDOM|warnings_caveats|
|JS4_6gv0PpI|33,500% RETURN - Mark Minervini's VCP Setup that made him Millions|PARTIAL_MISSING_IMPORTANT_WISDOM|warnings_caveats|
|Yb5lMegA5Hs|QUANTLENS_DAILY_EXTENSION_ANTI_CHASE_CRITICAL_REPORT|WRONG_SOURCE_MATCH|source transcript|
|RHlsVNSM8Aw|QUANTLENS_EMA20_50_RETEST_CRITICAL_INTAKE_REPORT|WRONG_SOURCE_MATCH|source transcript|
|bRXO6F_vGjM|QUANTLENS_TY_RAJNUS_MICROCAP_SHORT_INTAKE_REPORT|WRONG_SOURCE_MATCH|source transcript|


## 7. Wisdom recovered
280 wisdom rows routed to Trader Wiki.

## 8. Wiki files created
Trader Wiki import: `06_QUANTLENS_LAB\11_TRADER_WIKI\2026_05_04_restart_import_20260504_175618`

## 9. LLM wiki files created
LLM Wiki import: `06_QUANTLENS_LAB\12_LLM_WIKI\2026_05_04_restart_import_20260504_175618`

## 10. Classification summary
{'DAY_TRADE_STRATEGY': 60, 'DATA_BLOCKED': 7, 'SWING_TRADE_STRATEGY': 2, 'POSITION_TRADING_STRATEGY': 1, 'FILTER_MODULE': 1, 'REJECT_LOW_QUALITY': 1, 'DUPLICATE_OR_MERGED': 2}

## 11. Day trade candidates summary
60 candidates; manual visual review only.

## 12. Swing trade candidates summary
2 candidates; manual visual review only.

## 13. Position trading candidates summary
1 candidates; manual visual review only.

## 14. Filters/exits/sizing modules
1 module candidates.

## 15. Rejected/data blocked items
10 rejected, blocked, or duplicate/merged items.

## 16. Excel workbook path
`06_QUANTLENS_LAB\research\restart_transcript_intake_audit_2026_05_04_CODEX_20260504_175614\QUANTLENS_RESTART_CLASSIFICATION_WORKBOOK.xlsx`

## 17. Manual visual test queue
`06_QUANTLENS_LAB\research\restart_transcript_intake_audit_2026_05_04_CODEX_20260504_175614\MANUAL_VISUAL_TEST_QUEUE.csv`

## 18. MTC sandbox architecture decision
`06_QUANTLENS_LAB\research\restart_transcript_intake_audit_2026_05_04_CODEX_20260504_175614\MTC_SANDBOX_ARCHITECTURE_DECISION.md`

## 19. What Antigravity must audit next
Review corrected intakes against transcripts manually, resolve no-transcript intakes, choose one sandbox candidate, and verify source-specific data availability before any backtest.

## 20. Validation
See `VALIDATION_REPORT.md`.

## 21. Exact files created
See `FILES_CREATED.txt`.

## 22. Next prompt for Antigravity
Audit `06_QUANTLENS_LAB\research\restart_transcript_intake_audit_2026_05_04_CODEX_20260504_175614`. Verify corrected intakes against source transcripts, resolve DATA_BLOCKED rows, and select exactly one candidate for a standalone visual-review sandbox. Do not modify MTC_V2.pine or production runners.
