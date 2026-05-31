# Supertrend Optimization - Execution Summary

**Date**: 2026-03-04
**Status**: ✓ Ready for Phase 1 Execution
**Parity Baseline**: 99.54% (437/439 cases PASS)

---

## What Has Been Prepared

### 📋 Documentation
1. **`SUPERTREND_OPTIMIZATION_GUIDE.md`** (NEW)
   - Complete 3-phase optimization strategy
   - Detailed execution steps with commands
   - Decision tree for parameter selection
   - Expected outcomes and success criteria

2. **`CURRENT_STATUS_HANDOFF_20260303.md`** (UPDATED)
   - Added optimization framework section
   - Quick-start Phase 1 command
   - Timeline and constraints

### 🛠️ Tools & Scripts
1. **`supertrend_optimizer.py`** (NEW)
   - Grid search automation for parameter combinations
   - Batch backtest runner
   - Result aggregation and reporting

2. **`generate_supertrend_test_cases.py`** (NEW)
   - Generates test case JSON files from baseline
   - Supports arbitrary parameter combinations
   - Ready for manual case creation

### 📊 Framework
- **Baseline Locked**: Case 001 (TV=241, Python=241) - NO REGRESSIONS
- **Optimization Range**: ATR 14-28, Factor 3.0-5.0
- **Parity Guard**: Must maintain ≥95% match on baseline
- **Validation**: Multi-case testing on confirmation cluster

---

## Quick Start: Phase 1 Sensitivity

### Option A: Manual Test Cases (Recommended for first run)

```bash
# Step 1: Generate 9 test cases (ATR 14/21/28 × Factor 3.0/4.0/5.0)
python mtc_backtest/parity_suite_350/scripts/generate_supertrend_test_cases.py \
  --suite-root mtc_backtest/parity_suite_350 \
  --baseline-case parity_core_005_enable_long_trades_v01 \
  --atr-lengths 14 21 28 \
  --factors 3.0 4.0 5.0

# Step 2: Run backtest on baseline case only (quick test)
python mtc_backtest/parity_suite_350/scripts/audit_case_range_manual.py \
  --suite-root mtc_backtest/parity_suite_350 \
  --manifest manifests/cases_manifest_all.csv \
  --run-order-start 5 \
  --run-order-end 5 \
  --output-prefix opt_phase1_sensitivity \
  --use-tv-trading-range

# Step 3: Check results
cat mtc_backtest/parity_suite_350/compare_runs/opt_phase1_sensitivity_compare.csv
```

**Expected Time**: 5-10 minutes
**Output**: CSV with trade counts and parity metrics for each parameter combination

---

### Option B: Automated Grid Search

```bash
# Run full grid search (more time-intensive)
python mtc_backtest/parity_suite_350/scripts/supertrend_optimizer.py \
  --suite-root mtc_backtest/parity_suite_350 \
  --atr-range 14 28 \
  --factor-range 3.0 5.0 \
  --baseline-case 005 \
  --output-prefix phase1_auto

# Check results
cat mtc_backtest/parity_suite_350/optimize/phase1_auto/phase1_auto_results.csv
```

---

## Expected Phase 1 Results

### Hypothesis
- **ATR=14**: More entries (higher factor), more responsive to volatility
- **ATR=21**: Baseline balance
- **ATR=28**: Fewer entries, noise filtering

### Success Criteria
- ✓ All 9 combinations complete without error
- ✓ Parity match % ≥ 99% (maintain baseline alignment)
- ✓ Identify 3 candidates: conservative, balanced, aggressive

### Example Top Performers
```
Rank  ATR   Factor  Status    Match%   Python  TV
────────────────────────────────────────────────────
 1    28    4.5     PASS      99.9%    239     241
 2    21    4.0     PASS      100.0%   241     241   ← Current baseline
 3    14    3.0     PASS      98.5%    248     241
```

---

## Full Workflow: Phases 1-3

### Phase 1: Sensitivity Analysis ✓ (Ready)
- **Input**: 9 parameter combinations on baseline case (001/005)
- **Output**: phase1_sensitivity_results.csv + metrics
- **Time**: 5-10 minutes
- **Decision**: Pick top 3 candidates

### Phase 2: Multi-Case Validation (After Phase 1)
- **Input**: Top 3 parameters × 7 confirmation cases (209-215)
- **Output**: phase2_confirmation_results.csv
- **Time**: 20-30 minutes
- **Decision**: Check for confirmation layer regressions

### Phase 3: Regression Testing (After Phase 2)
- **Input**: Optimal parameters × 9 known PASS cases (001, 236, 281, 395, 398, 401, 409, 412, 422)
- **Output**: phase3_regression_results.csv
- **Time**: 15-20 minutes
- **Decision**: Ensure no closed wins degraded

### Phase 4: Commit & Lock (After Phase 3)
- Update `mtc_backtest/src/config/defaults.py` with optimal atr_len/factor
- Tag commit as optimization checkpoint
- Update `CURRENT_STATUS_HANDOFF` with final results

**Total Time for All Phases**: ~1-2 hours

---

## Critical Rules

### 🔒 Parity Lock
- Must maintain ≥95% parity on baseline case
- If Phase 1 shows <95% on any combo, investigate before proceeding
- Current baseline (ATR=21, Factor=4.0) is locked reference

### 📍 No-Repaint Guarantee
- All Supertrend calculations use bar-close gating
- Verified in [src/modules/signals/supertrend.py:110-116](../../src/modules/signals/supertrend.py#L110)
- Heikin Ashi candles use completed bars only
- Parameter changes cannot affect this guarantee

### 🎯 Confirmation Compatibility
- Confirmation layer timing must not degrade
- Phase 2 tests cases 209-215 (confirmation cluster)
- If confirmation cases show <95% parity in Phase 2, revert to baseline

### 🔗 HTF Bias Independence
- MACD filter HTF Bias already aligned (completed 2026-03-04)
- Supertrend optimization is independent
- No interaction between filters

---

## How to Analyze Results

### Key Metrics to Check
```csv
atr_len,factor,status,match_pct,py_trades,tv_trades,delta
14,3.0,PASS,98.5,248,241,+7
21,4.0,PASS,100.0,241,241,0
28,4.5,PASS,99.9,239,241,-2
```

### Selection Criteria
1. **Conservative** (Lower risk, drawdown focus):
   - Highest match %
   - Lowest trade count (fewer whipsaws)
   - Likely: ATR=28, Factor=4.5

2. **Balanced** (Moderate risk/reward):
   - Current baseline or very close
   - Good match % with slight quality improvement
   - Likely: ATR=21, Factor=4.0 (current) or ATR=21, Factor=4.5

3. **Aggressive** (Higher win rate focus):
   - Still ≥95% match %
   - More trades (better signal responsiveness)
   - Likely: ATR=14, Factor=3.0

---

## Files to Check During Optimization

### Live Results
```
mtc_backtest/parity_suite_350/
├── compare_runs/
│   ├── opt_phase1_sensitivity_compare.csv      ← Phase 1 results
│   ├── opt_phase2_confirmation_compare.csv     ← Phase 2 results
│   └── opt_phase3_regression_compare.csv       ← Phase 3 results
└── optimize/
    ├── phase1_sensitivity_results.csv          ← Aggregated Phase 1
    ├── phase1_sensitivity_report.md            ← Phase 1 analysis
    └── ...
```

### Debug Data (If Needed)
```
debug/parity_suite_350/
└── parity_opt_001_atr{N:02d}_factor{F:.1f}/
    ├── debug_python_trades_*.csv
    ├── debug_python_signals_*.csv
    └── ...
```

---

## Fallback Plans

### If Phase 1 Shows Poor Results
1. Check if baseline case parameters in JSON are correct
2. Verify test case generation succeeded
3. Review `debug_python_signals_*.csv` for Supertrend line/direction
4. Compare ATR calculations between Python and expected

### If Phase 2 Shows Confirmation Regressions
1. Revert to Phase 1 candidate with best balance
2. Investigate confirmation timing (swing break, momentum)
3. Consider candidate with factor closer to 4.0 baseline

### If Phase 3 Shows Closed Wins Degraded
1. Lock baseline (ATR=21, Factor=4.0)
2. Document which case degraded and by how much
3. Report as acceptable risk (if <2% parity loss) or revert

---

## Documentation References

- **SUPERTREND_OPTIMIZATION_GUIDE.md** - Full 3-phase plan with decision tree
- **CURRENT_STATUS_HANDOFF_20260303.md** - Status overview + quick commands
- **src/modules/signals/supertrend.py** - Supertrend implementation + param space
- **src/config/defaults.py** - Current default parameters
- **scripts/audit_case_range_manual.py** - Audit runner (existing)

---

## Next Step

**Execute Phase 1** with Option A (manual test cases) to:
1. Generate 9 test cases
2. Run backtest on baseline case only
3. Compare results
4. Identify top 3 candidates

**Estimated Time**: 5-10 minutes
**Expected Decision**: Select candidate for Phase 2 validation

**Command to Run**:
```bash
python mtc_backtest/parity_suite_350/scripts/generate_supertrend_test_cases.py \
  --suite-root mtc_backtest/parity_suite_350 \
  --baseline-case parity_core_005_enable_long_trades_v01 \
  --atr-lengths 14 21 28 \
  --factors 3.0 4.0 5.0
```

---

**Ready to execute?** Start with Phase 1 above. Check back after 5-10 minutes for results analysis.
