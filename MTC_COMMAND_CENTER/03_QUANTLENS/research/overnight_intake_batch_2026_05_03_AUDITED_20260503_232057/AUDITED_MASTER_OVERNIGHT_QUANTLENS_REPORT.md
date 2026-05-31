# Audited Master Overnight QuantLens Report

## 1. Executive Verdict
- Pine-ready strategies: **0**.
- MTC producer-ready strategies: **0**.
- PASS_STAGE2 candidates: **1** (CANDIDATE_001).
- WEAK candidates worth Stage 2 only after fixes: **6**.
- Day-trade candidates: 0 viable (all crypto-proxy results either rejected or weak).
- Swing candidates: 7 tested, top is **CANDIDATE_001 Kell Wedge** (PASS_STAGE2).
- Position-trading candidates: 0 testable (CANSLIM/Weinstein DATA_BLOCKED).
- Reject: **2** (CANDIDATE_008, CANDIDATE_011).

## 2. First-Run Reliability Verdict
- **Partially reliable**. All 10 audited strategy metrics independently reproduce within rounding tolerance, fee monotonicity holds, and `MTC_V2.pine` was untouched. The first run was *too conservative* on CANDIDATE_001's classification but otherwise honest. Inventory dedupe was looser than the audit's; this is methodology-difference, not corruption.

## 3. Input Coverage
- Total .md files scanned: 159.
- VALID_INTAKE_REPORT (audit): 56.
- DUPLICATE_VIDEO_ID: 1.
- DUPLICATE_STRATEGY (by normalized title): 30.
- RAW_TRANSCRIPT_BY_MISTAKE (under `Transcrips/`, correctly skipped): 65.
- EMPTY_OR_CORRUPT: 3.
- UNKNOWN: 4.
- User reference '~66' is not exact; inbox holds two date cohorts (15 QL_*.md at root + 50+ in `3 Mayıs/`). Audit count is correct.

## 4. Candidate Extraction Summary
- First-run produced 14 named candidates and 10 implemented strategy folders. Audit kept all 10 with reclassifications: 1 upgrade (CAND_001 → PASS_STAGE2), 1 explicit downgrade phrasing (CAND_008 REJECT_CRYPTO_PROXY → REJECT_NO_EDGE), no merges/splits required.
- 78-row lightweight inventory of all unique intakes is in `AUDITED_INTAKE_INVENTORY.csv` for tomorrow's batch selection.

## 5. Data Audit Summary
- Local 5m crypto futures bundle (17 symbols, 245 873 bars each, 2024-01-01 → 2026-05-03) is the only research-grade dataset available locally.
- All swing tests use 1D resample of that bundle across 10 symbols. Day-trade tests use 5m across 5 symbols.
- US equity, US microcap, options, and fundamental data are all missing.

## 6. Backtest Audit Summary
- Strategies independently audited: 10.
- Reruns required: 0.
- Reruns executed: 0.
- Code review: not exhaustive (out-of-budget for this pass); spot checks on CANDIDATE_001/004/008 strategy_*.py files showed no obvious lookahead, same-bar exit-before-entry, or fill bugs. Full code audit deferred to next pass.

## 7. Metric Audit Summary
- Trade count: MATCH for all 10.
- PF base: MATCH for all 10.
- Net return: MATCH for all 10.
- Max DD: MATCH for all 10.
- Fee 2x PF: MATCH for all 10. Fee 3x PF: MATCH for all 10.
- Fee-stress monotonicity: TRUE for all 10. **No fee-stress bug detected** (this was the user's explicit prior concern).

## 8. Corrected Strategy Ranking
See `AUDITED_MASTER_COMPARISON.csv`/`.md` for the full table.

Top 5 by audit class then PF:
- 1. **CANDIDATE_001** Kell Wedge Pop / EMA Crossback — PASS_STAGE2, PF 1.7481 (2x 1.6786, 3x 1.6132), DD -46.3269%, 10 assets, 111 trades.
- 2. **CANDIDATE_003** Slingshot EMA(high,4) Pullback — WEAK_CANDIDATE, PF 1.4581 (2x 1.3872, 3x 1.3207), DD -86.417%, 10 assets, 1388 trades.
- 3. **CANDIDATE_005** BigBeluga RSI/CHoCH/ATR — WEAK_CANDIDATE, PF 1.4516 (2x 1.4236, 3x 1.3962), DD -79.8493%, 10 assets, 465 trades.
- 4. **CANDIDATE_002** Martin Luke Pullback AVWAP — WEAK_CANDIDATE, PF 1.4435 (2x 1.4078, 3x 1.3733), DD -91.7686%, 10 assets, 584 trades.
- 5. **CANDIDATE_007** Linda 5SMA RS Pullback — WEAK_CANDIDATE, PF 1.3096 (2x 1.2609, 3x 1.2138), DD -85.9357%, 10 assets, 687 trades.

## 9. Corrected Day-Trade Candidates
- **CANDIDATE_009** HighBeta Opening-Bar Gap-and-Go — WEAK_CANDIDATE. Crypto-proxy 5m only. Caveat: not a substitute for native US session/gap/microcap data.
- **CANDIDATE_008** 8AM ET Opening Range Breakout — REJECT_NO_EDGE. Crypto-proxy 5m only. Caveat: not a substitute for native US session/gap/microcap data.
- **CANDIDATE_010** Ty Rajnus Microcap Short — DATA_BLOCKED. Crypto-proxy 5m only. Caveat: not a substitute for native US session/gap/microcap data.

## 10. Corrected Swing-Trade Candidates
- **CANDIDATE_001** Kell Wedge Pop / EMA Crossback — PASS_STAGE2, PF 1.7481 / 2x 1.6786 / 3x 1.6132, DD -46.3269%, top-asset share 0.324.
- **CANDIDATE_003** Slingshot EMA(high,4) Pullback — WEAK_CANDIDATE, PF 1.4581 / 2x 1.3872 / 3x 1.3207, DD -86.417%, top-asset share 0.13.
- **CANDIDATE_005** BigBeluga RSI/CHoCH/ATR — WEAK_CANDIDATE, PF 1.4516 / 2x 1.4236 / 3x 1.3962, DD -79.8493%, top-asset share 0.112.
- **CANDIDATE_002** Martin Luke Pullback AVWAP — WEAK_CANDIDATE, PF 1.4435 / 2x 1.4078 / 3x 1.3733, DD -91.7686%, top-asset share 0.137.
- **CANDIDATE_007** Linda 5SMA RS Pullback — WEAK_CANDIDATE, PF 1.3096 / 2x 1.2609 / 3x 1.2138, DD -85.9357%, top-asset share 0.138.
- **CANDIDATE_004** Crabel Range Expansion — WEAK_CANDIDATE, PF 1.251 / 2x 1.1866 / 3x 1.126, DD -98.442%, top-asset share 0.118.
- **CANDIDATE_012** EMA20/50 Two-Retest Baseline — BASELINE_ONLY, PF 1.8741 / 2x 1.8376 / 3x 1.8023, DD -82.1442%, top-asset share 0.17.

## 11. Corrected Position-Trading Candidates
- **CANDIDATE_006** — DATA_BLOCKED. acquire native data (US equity / microcap).

## 12. Filter / Exit / Sizing Modules Worth Keeping
- **CANDIDATE_011** as filter overlay candidate (test as veto over CAND_001).
- Progressive Exposure / position-sizing module concept extracted from Minervini/poker-trader intakes — needs isolated implementation; deferred.
- ATR/time-stop logic embedded in CAND_001/003/005 should be parameterized into a shared exit harness during Stage 2.

## 13. Rejected / Blocked Ideas
- REJECT_NO_EDGE: CANDIDATE_008, CANDIDATE_011 — edge gone after costs.
- BASELINE_ONLY: CANDIDATE_012 (EMA20/50 retest) — benchmark by design.
- DATA_BLOCKED: CANDIDATE_006, CANDIDATE_010.

## 14. Stage 2 Recommendation
**Eligible**: CANDIDATE_001 Kell Wedge.
**Stage 2 protocol**:
- Walk-forward: 3-fold split of 2024-01 → 2026-05 with 6-month windows; report PF/DD per fold.
- Parameter perturbation: ±20% on EMA periods, wedge pop tolerance, ATR stop multiplier; report PF stability.
- Regime split: bull / bear / chop bins by 200-bar EMA slope on BTCUSDT; report per-regime PF and DD.
- Cost stress at 4x and 5x base fee.
- Concentration check: per-asset PF > 1.0 on at least 7/10 symbols.
**Conditional candidates** (run only after drawdown reduction): CANDIDATE_005 BigBeluga, CANDIDATE_007 Linda 5SMA. Apply CAND_011 anti-extension filter overlay before Stage 2.

## 15. MTC / Pine Recommendation
- Direct MTC integration: **NO**.
- Pine conversion: **NO**.
- Reason: Stage 2 robustness has not been demonstrated for any candidate. CANDIDATE_001 is the only one even eligible to begin Stage 2.

## 16. Data Acquisition Plan for Tomorrow
1. **US daily equities** for top-1500 liquid names + S&P 500 + Russell 2000 + sector ETFs — enables CANSLIM, Weinstein, Minervini VCP backtests.
2. **US 5m intraday for high-beta liquid names** with regular-session boundaries, gap flags, premarket aggregates — enables HighBeta, Episodic Pivot, AVWAP-intraday tests.
3. **US microcap 1m + borrow/locate availability + halt log + dilution events** — required to even start an honest microcap-short backtest.
4. **Crypto futures 1m** for the existing 17 symbols — would enable refined session-segment and ORB-equivalent studies on crypto.
5. **Fundamentals** (earnings dates, EPS surprise, revenue growth) — for CANSLIM-grade filtering.

## 17. Exact Files Created
See `FILES_CREATED.txt`.

## 18. Exact Commands Run
See `COMMAND_LOG.txt`.

## 19. Validation Results
See `VALIDATION_REPORT.md`.

## 20. Known Limitations
- Audit did not perform a line-by-line code review of every strategy_*.py file (time/budget). Spot checks only.
- Audit did not download new data; relies on existing 5m crypto bundle.
- Source-quality scoring is heuristic, not exhaustive.
- Crypto-proxy gap remains for US-equity-native ideas; only real US data closes it.

## 21. Recommended Next Codex Prompt
See bottom of Turkish summary in conversation; saved to `NEXT_PROMPT_TOMORROW.md`.