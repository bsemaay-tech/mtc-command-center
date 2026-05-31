# Supertrend Parameter Optimization Guide

**Date**: 2026-03-04
**Status**: Ready for execution at 98% parity baseline
**Objective**: Optimize Supertrend ATR length and factor to improve trade quality and reduce drawdown

---

## Current Baseline

**Supertrend Default Parameters** (mtc_backtest/src/config/defaults.py):
- `atr_len`: 21 (lookback period for ATR volatility calculation)
- `factor`: 4.0 (multiplier applied to ATR for band width)
- `use_wicks`: True (use High/Low instead of Close)
- `use_ha`: True (use Heikin Ashi candles)

**Current Performance** (Case 001 baseline):
- TV Trades: 241
- Python Trades: 241
- Status: PASS (100% parity)

---

## Optimization Strategy

### Phase 1: Sensitivity Analysis (Narrow Grid)

Test parameter combinations to identify:
- How sensitive trade count is to ATR changes
- How sensitive trade count is to Factor changes
- Which combinations maintain parity while improving quality

**Recommended Test Points**:

| ATR Length | Factor | Rationale |
|-----------|--------|-----------|
| 14 | 3.0 | Shorter ATR, tighter bands (more entries) |
| 14 | 4.0 | Shorter ATR, baseline factor |
| 14 | 5.0 | Shorter ATR, wider bands |
| 21 | 3.0 | Baseline ATR, tighter bands |
| **21** | **4.0** | **CURRENT BASELINE** |
| 21 | 5.0 | Baseline ATR, wider bands |
| 28 | 3.0 | Longer ATR, tighter bands |
| 28 | 4.0 | Longer ATR, baseline factor |
| 28 | 5.0 | Longer ATR, wider bands (fewer entries) |

**Expected Impact**:
- **Lower ATR (14)**: Faster volatility response → More entries, potentially more whipsaws
- **Higher ATR (28)**: Slower volatility response → Fewer entries, potentially better quality
- **Lower Factor (3.0)**: Tighter bands → More signal changes, more trades
- **Higher Factor (5.0)**: Wider bands → Fewer signals, fewer trades

### Phase 2: Quality Metrics

For each parameter combination, evaluate:

1. **Parity Alignment**:
   - Match % vs TV reference
   - Trade count delta

2. **Risk Metrics**:
   - Maximum drawdown
   - Consecutive losing trades
   - Win rate

3. **Efficiency Metrics**:
   - Average trade duration
   - Profit factor
   - Sharpe ratio (if available)

### Phase 3: Multi-Case Validation

Once Phase 1 identifies promising parameters:
- Test on confirmation cases (210-215 cluster)
- Test on MACD filter cases (193-200 cluster)
- Verify no regression in closed parity wins (001, 236, 281, 395, 398, 401, 409, 412, 422)

---

## Test Case Creation

### Quick Setup (Manual)

Create test cases by modifying baseline case JSON. Example for ATR=14, Factor=3.0:

```json
{
  "_case_id": "opt_001_atr14_factor3",
  "_generated": {
    "description": "Baseline with Supertrend ATR=14, Factor=3.0",
    "supertrend_atr_len": 14,
    "supertrend_factor": 3.0
  },
  "signals": {
    "supertrend": {
      "atr_len": 14,
      "factor": 3.0,
      "use_wicks": true,
      "use_ha": true
    }
  },
  // ... rest of baseline config
}
```

### Batch Generation Script

Location: `mtc_backtest/parity_suite_350/scripts/supertrend_optimizer.py`

**Usage**:
```bash
python mtc_backtest/parity_suite_350/scripts/supertrend_optimizer.py \
  --suite-root mtc_backtest/parity_suite_350 \
  --atr-range 14 28 \
  --factor-range 3.0 5.0 \
  --baseline-case 001 \
  --output-prefix phase1_sensitivity
```

**Outputs**:
- `mtc_backtest/parity_suite_350/optimize/phase1_sensitivity/phase1_sensitivity_results.csv`
- `mtc_backtest/parity_suite_350/optimize/phase1_sensitivity/phase1_sensitivity_report.md`

---

## Execution Steps

### Step 1: Run Sensitivity Analysis

```bash
# Phase 1: Test 9 combinations (ATR: 14/21/28, Factor: 3.0/4.0/5.0)
python mtc_backtest/parity_suite_350/scripts/audit_case_range_manual.py \
  --suite-root mtc_backtest/parity_suite_350 \
  --manifest manifests/cases_manifest_all.csv \
  --run-order-start 1 \
  --run-order-end 1 \
  --output-prefix opt_phase1_baseline \
  --use-tv-trading-range
```

**Expected time**: ~5-10 minutes (single baseline case with 9 parameter combinations)

### Step 2: Analyze Results

- Compare parity metrics
- Identify top 3 parameter sets
- Check drawdown/risk metrics

### Step 3: Multi-Case Validation

```bash
# Validate top parameters on confirmation cluster (cases 209-215)
python mtc_backtest/parity_suite_350/scripts/audit_case_range_manual.py \
  --suite-root mtc_backtest/parity_suite_350 \
  --manifest manifests/cases_manifest_all.csv \
  --run-order-start 209 \
  --run-order-end 215 \
  --output-prefix opt_phase2_confirmation \
  --use-tv-trading-range
```

### Step 4: Validate Closed Wins

```bash
# Re-run known PASS cases to ensure no regression
python mtc_backtest/parity_suite_350/scripts/audit_case_range_manual.py \
  --suite-root mtc_backtest/parity_suite_350 \
  --manifest manifests/cases_manifest_all.csv \
  --run-order-start 001,236,281,395,398,401,409,412,422 \
  --output-prefix opt_phase3_regression_check \
  --use-tv-trading-range
```

---

## Expected Outcomes

### Conservative Optimization (Low Risk)

**Goal**: Find parameters that reduce drawdown while maintaining parity

**Success Criteria**:
- ✓ Match % ≥ 99% on baseline
- ✓ No regression on closed wins
- ✓ Measurably lower max drawdown
- ✓ Fewer whipsaws (shorter avg trade duration)

**Likely Candidate**: ATR=28, Factor=4.5
- Reason: Longer ATR filters noise, slightly wider bands reduce overtrading

### Aggressive Optimization (Higher Risk)

**Goal**: Maximize trade quality and win rate

**Success Criteria**:
- ✓ Match % ≥ 95% (acceptable 5% parity tolerance)
- ✓ Measurable improvement in Sharpe ratio
- ✓ Better profit factor

**Likely Candidate**: ATR=14, Factor=3.0 OR ATR=21, Factor=3.0
- Reason: Tighter bands increase responsiveness, catch more reversals

---

## Decision Tree

```
Start: Current baseline (ATR=21, Factor=4.0, PASS)
  │
  ├─ Phase 1: Test 9 combinations
  │   │
  │   ├─ All maintain parity? → Phase 2
  │   │
  │   └─ Some lose parity? → Analyze root causes
  │       ├─ Filter signal differences?
  │       ├─ Confirmation timing?
  │       └─ Adjust range, retest
  │
  ├─ Phase 2: Multi-case validation
  │   │
  │   ├─ Closed wins stable? → Phase 3
  │   │
  │   └─ Regression detected? → Revert and try different range
  │
  └─ Phase 3: Quality assessment
      │
      ├─ Improved metrics? → Lock as new baseline
      │
      └─ No improvement? → Keep current baseline
```

---

## Key Constraints

1. **No-Repaint Rule**: All Supertrend calculations must respect bar-close gating
   - Verified in [supertrend.py:110-116](../../src/modules/signals/supertrend.py#L110)
   - Heikin Ashi candles use completed bars only
   - ATR calculation uses confirmed bars

2. **Parity Lock**: Must maintain ≥ 95% parity on baseline case (001)
   - Hard constraint for any parameter set used in production

3. **Confirmation Compatibility**: Must not degrade confirmation layer timing
   - Test on cases 209-215 (confirmation cluster) as part of Phase 2

4. **HTF Bias Alignment**: Already implemented in MACD filter
   - No interaction with Supertrend parameters
   - Can optimize independently

---

## Historical Parameter Space

From [supertrend.py:147-168](../../src/modules/signals/supertrend.py#L147):

```python
'atr_len': {
    'type': 'int',
    'low': 7,
    'high': 50,
    'step': 1,
},
'factor': {
    'type': 'float',
    'low': 1.0,
    'high': 8.0,
    'step': 0.5,
},
```

Current optimization range is conservative subset: ATR 14-28, Factor 3.0-5.0.
- If needed, can expand to full range in Phase 2.

---

## Next Actions

1. **Immediate**: Run Phase 1 sensitivity analysis (9 combinations)
2. **Review Phase 1 Results**: Identify top 3 candidates
3. **Execute Phase 2**: Multi-case validation
4. **Lock Parameters**: Update defaults.py with optimal values
5. **Commit**: Tag as optimization checkpoint with commit message

**Estimated Total Time**: 1-2 hours for all phases

---

## Output Files

All results will be saved to: `mtc_backtest/parity_suite_350/optimize/`

```
optimize/
├── phase1_sensitivity/
│   ├── phase1_sensitivity_results.csv       # Parameter combinations + metrics
│   └── phase1_sensitivity_report.md         # Analysis and recommendations
├── phase2_confirmation/
│   ├── phase2_confirmation_results.csv      # Multi-case validation
│   └── phase2_confirmation_report.md
└── phase3_regression/
    └── phase3_regression_results.csv        # Closed wins stability check
```

---

## References

- **Supertrend Signal Module**: `mtc_backtest/src/modules/signals/supertrend.py`
- **Default Config**: `mtc_backtest/src/config/defaults.py`
- **Optimization Script**: `mtc_backtest/parity_suite_350/scripts/supertrend_optimizer.py`
- **Audit Runner**: `mtc_backtest/parity_suite_350/scripts/audit_case_range_manual.py`
