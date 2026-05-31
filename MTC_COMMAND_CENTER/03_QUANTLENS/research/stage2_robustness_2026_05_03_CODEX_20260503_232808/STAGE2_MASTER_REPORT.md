# Stage-2 Master Report

## Executive Verdict
No strategy is Pine-ready or MTC producer-ready. No `PASS_STAGE3` was earned under strict drawdown/OOS/baseline gates. Several swing candidates remain `WEAK_STAGE3_CANDIDATE`; day-trade crypto proxy remains weak or rejected; position-trading candidates need real equity/microcap data.

## What Previous Agents Claimed
- CLEAN/AUDITED: no Pine/MTC candidate; weak swing list.
- Antigravity: LBR Coil/IDNR4 selected for Stage 2.
- Late session warnings: derivative artifacts may be overwritten and asset_class detection can be unreliable.

## Which Claims Were Confirmed
- No Pine/MTC-ready candidate confirmed.
- 8AM ORB remains rejected.
- HighBeta remains proxy/data-needing.
- LBR Coil was tested; it is not promoted without stronger OOS/baseline evidence.

## Which Files Were Trusted
Audited folders with trade exports, fee monotonic evidence, and validation reports were weighted highest. This run regenerated independent Stage-2 outputs under this folder.

## Candidate List
|candidate_id|name|horizon|eligible|data_status|
|---|---|---|---|---|
|KELL_WEDGE|Kell Wedge Pop / EMA Crossback|SWING|True|available_crypto_daily|
|SLINGSHOT|Slingshot EMA(high,4) Pullback|SWING|True|available_crypto_daily|
|CRABEL|Crabel Range Expansion|SWING|True|available_crypto_daily|
|BIGBELUGA|BigBeluga RSI Divergence + CHoCH + ATR|SWING|True|available_crypto_daily|
|LINDA_5SMA|Linda 5SMA RS Pullback|SWING|True|available_crypto_daily_rs_proxy|
|MARTIN_LUKE|Martin Luke Pullback / AVWAP|SWING|True|available_crypto_daily_proxy|
|LBR_COIL|LBR Coil Breakout / IDNR4|DAY|True|available_crypto_5m|
|HIGHBETA_PROXY|HighBeta Opening Bar Gap-and-Go|DAY|True|available_crypto_5m_proxy|
|ORB_8AM|8AM Opening Range Breakout|DAY|True|available_crypto_5m_proxy|
|ANTI_CHASE|Daily Extension Anti-Chase|FILTER|True|available_crypto_daily|
|CANSLIM|CANSLIM Shakeout +3|POSITION|False|blocked_no_equity_fundamental_rs|
|WEINSTEIN|Stan Weinstein Stage Analysis|POSITION|False|blocked_no_equity_universe_rs|
|CHARLES_50DMA|Charles Harris 50DMA Pullback|POSITION|False|blocked_no_equity_data|
|TY_MICROCAP|Ty Rajnus Microcap Liquidity Reversion Short|DAY|False|blocked_no_microcap_borrow_halt|

## Data Used
Local crypto futures daily bundle and existing 5m research data. No external/broker/live data used.

## Baseline Results
See `BASELINE_RESULTS.csv` and `BASELINE_REPORT.md`.

## Stage-2 Results
|rank|candidate_id|profit_factor|fee_2x_pf|oos_pf|max_drawdown|beats_baseline|final_classification|
|---|---|---|---|---|---|---|---|
|1|CRABEL|1.7727|1.609|1.5286|-90.0656|True|WEAK_STAGE3_CANDIDATE|
|2|SLINGSHOT|1.7495|1.7205|0.7786|-99.9692|True|WEAK_STAGE3_CANDIDATE|
|3|BIGBELUGA|1.7252|1.6919|1.0241|-99.9616|True|WEAK_STAGE3_CANDIDATE|
|4|MARTIN_LUKE|1.5289|1.504|0.7089|-99.3507|True|WEAK_STAGE3_CANDIDATE|
|5|LINDA_5SMA|1.3557|1.3108|1.0382|-98.3383|True|WEAK_STAGE3_CANDIDATE|
|6|ANTI_CHASE|0|0|0|0|False|FILTER_ONLY|
|7|KELL_WEDGE|3.5956|3.3993|3.3326|-7.3131|True|REJECT_NO_EDGE|
|8|HIGHBETA_PROXY|1.4648|1.0183|1.9843|-15.5149|True|NEEDS_REAL_EQUITY_DATA|
|9|LBR_COIL|0.8687|0.5618|0.7842|-100.0|False|REJECT_NO_EDGE|
|10|ORB_8AM|0.7414|0.533|0.6697|-100.0|False|REJECT_NO_EDGE|
|11|CANSLIM|0|0|0|0|False|NEEDS_REAL_EQUITY_DATA|
|12|WEINSTEIN|0|0|0|0|False|NEEDS_REAL_EQUITY_DATA|
|13|CHARLES_50DMA|0|0|0|0|False|NEEDS_REAL_EQUITY_DATA|
|14|TY_MICROCAP|0|0|0|0|False|NEEDS_REAL_MICROCAP_DATA|

## Walk-Forward / Fee / Monte Carlo / Exit Variants
See `walkforward_results.csv`, `fee_stress_results.csv`, `monte_carlo_results.csv`, and per-strategy reports.

## Day-Trade Candidates
|candidate_id|profit_factor|fee_2x_pf|final_classification|
|---|---|---|---|
|HIGHBETA_PROXY|1.4648|1.0183|NEEDS_REAL_EQUITY_DATA|
|LBR_COIL|0.8687|0.5618|REJECT_NO_EDGE|
|ORB_8AM|0.7414|0.533|REJECT_NO_EDGE|
|TY_MICROCAP|0|0|NEEDS_REAL_MICROCAP_DATA|

## Swing-Trade Candidates
|candidate_id|profit_factor|fee_2x_pf|oos_pf|max_drawdown|final_classification|
|---|---|---|---|---|---|
|CRABEL|1.7727|1.609|1.5286|-90.0656|WEAK_STAGE3_CANDIDATE|
|SLINGSHOT|1.7495|1.7205|0.7786|-99.9692|WEAK_STAGE3_CANDIDATE|
|BIGBELUGA|1.7252|1.6919|1.0241|-99.9616|WEAK_STAGE3_CANDIDATE|
|MARTIN_LUKE|1.5289|1.504|0.7089|-99.3507|WEAK_STAGE3_CANDIDATE|
|LINDA_5SMA|1.3557|1.3108|1.0382|-98.3383|WEAK_STAGE3_CANDIDATE|
|KELL_WEDGE|3.5956|3.3993|3.3326|-7.3131|REJECT_NO_EDGE|

## Position-Trading Candidates
|candidate_id|data_status|final_classification|
|---|---|---|
|CANSLIM|blocked_no_equity_fundamental_rs|NEEDS_REAL_EQUITY_DATA|
|WEINSTEIN|blocked_no_equity_universe_rs|NEEDS_REAL_EQUITY_DATA|
|CHARLES_50DMA|blocked_no_equity_data|NEEDS_REAL_EQUITY_DATA|

## Filter / Exit / Sizing Modules
|candidate_id|before_pf|after_pf|before_dd|after_dd|classification|
|---|---|---|---|---|---|
|KELL_WEDGE|3.5956|3.5956|-7.3131|-7.3131|NO_IMPROVEMENT|
|CRABEL|1.7727|1.7324|-90.0656|-90.0656|NO_IMPROVEMENT|
|SLINGSHOT|1.7495|1.7111|-99.9692|-99.9746|NO_IMPROVEMENT|

## Portfolio Combination
|portfolio|candidate_count|net_return|max_drawdown|
|---|---|---|---|
|equal_weight_weak_candidates|5|256288322439.0113|-84.5664|

## MTC Readiness
No integration. See `MTC_V2_STAGE2_READINESS.md`.

## Rejected / Data-Blocked
See `STAGE2_DATA_BLOCKED_REPORT.md`.

## Next Exact Work
Run Stage-3 robustness only on weak candidates and acquire real equity/session/microcap data for blocked ideas.

## Files / Commands / Validation
See `FILES_CREATED.txt`, `COMMAND_LOG.txt`, and `VALIDATION_REPORT.md`.
