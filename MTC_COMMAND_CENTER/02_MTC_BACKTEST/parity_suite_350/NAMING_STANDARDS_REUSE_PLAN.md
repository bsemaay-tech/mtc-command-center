# Naming Standards and Reuse Plan

## 1. Naming Conventions

### 1.1 Case ID Format
```
parity_[package]_[sequence]_[feature]_[variant]
```

**Components:**
- `package`: `core`, `bnd` (boundary), `pw` (pairwise)
- `sequence`: 3-digit number (001, 002, ...)
- `feature`: Primary feature being tested (abbreviated)
- `variant`: Specific variant or parameter value

**Examples:**
- `parity_core_001_baseline_touch`
- `parity_bnd_051_time_stop_01` 
- `parity_pw_201_supertrend_sl_atr`

### 1.2 Feature Abbreviations

| Feature Category | Abbreviation | Examples |
|-----------------|--------------|----------|
| Baseline | `baseline` | `touch`, `close` |
| Signal Mode | `signal` | `supertrend`, `range_filter`, `none` |
| Time Stop | `time_stop` | `01`, `02`, `eod`, `eow` |
| Stop Loss | `sl` | `atr`, `fixed`, `trailing` |
| Take Profit | `tp` | `atr`, `fixed`, `multi` |
| Break Even | `be` | `01`, `02`, `trail` |
| Trailing Stop | `trail` | `01`, `02`, `atr` |
| Filters | `filter` | `ma`, `ma_slope`, `mcginley` |
| Confirmation | `confirm` | `rsi`, `macd`, `volume` |
| Guard | `guard` | `mae`, `consec_loss`, `recovery` |
| Daily Limits | `daily` | `loss`, `trades`, `drawdown` |

### 1.3 Folder Naming
```
[3-digit_sequence]_[case_id]/
```
- Sequence numbers are continuous across packages
- Core: 001-050
- Boundary: 051-200  
- Pairwise: 201-350

### 1.4 File Naming
- `case_config.json` - Case configuration
- `tv_strategy_report.xlsx` - TV export (user provided)
- `parity_report.json` - Python execution results
- `comparison_report.md` - TV vs Python comparison
- `mismatch_analysis.md` - Mismatch analysis

## 2. Reuse Plan Strategy

### 2.1 Reuse Principles

1. **Identical Configurations** - Same settings produce same TV output
2. **Independent Features** - Changing one feature doesn't affect others
3. **Parameter Variations** - Only numeric values differ
4. **Boolean Toggles** - On/off states for features

### 2.2 Reuse Categories

#### Category A: Full Reuse
- Identical configuration except for non-trade-affecting parameters
- Examples: Different ATR lengths when Use ATR SL = false
- TV output can be copied directly

#### Category B: Partial Reuse  
- Similar configuration with minor variations
- May affect trade count but pattern is predictable
- Can use as reference but need verification

#### Category C: No Reuse
- Different signal modes
- Different entry/exit logic
- Different filter combinations
- Requires separate TV execution

### 2.3 Reuse Mapping Structure

The `REUSE_MAPPING.csv` will contain:

```csv
source_case_id,target_case_id,reuse_type,confidence,notes
parity_core_001_baseline_touch,parity_core_002_baseline_close,A,100%,"Only entry_mode differs (touch vs close)"
parity_bnd_051_time_stop_01,parity_bnd_057_time_stop_07,B,80%,"Time stop bars differ (1 vs 7)"
parity_core_003_signal_supertrend,parity_pw_201_supertrend_sl_atr,C,0%,"Different SL mode added"
```

### 2.4 Dependency-Based Reuse Rules

Based on user's dependency analysis:

1. **If parent feature disabled → child features irrelevant**
   - Example: `Use Stop Loss = false` → All SL mode variations can reuse same TV output
   
2. **If feature has no trade impact → all variations reusable**
   - Example: `Signal mode = none` → All other settings irrelevant
   
3. **Boolean toggles create reuse groups**
   - All cases with `Use TP = false` can share TV output
   - All cases with `Use daily Loss limit = false` can share TV output

### 2.5 Reuse Group Identification

#### Group 1: Baseline Variations
- `parity_core_001_baseline_touch` (source)
- `parity_core_002_baseline_close` (reuse)

#### Group 2: Time Stop Variations  
- `parity_bnd_051_time_stop_01` (source)
- `parity_bnd_052_time_stop_02` through `parity_bnd_062_time_stop_12` (reuse)

#### Group 3: SL Mode Variations (when Use SL = true)
- `parity_bnd_101_sl_atr_01` (source)
- Other ATR length variations (reuse with caution)

#### Group 4: TP Mode Variations (when Use TP = true)
- `parity_bnd_151_tp_atr_01` (source)
- Other TP variations (reuse with verification)

## 3. Implementation of Reuse Plan

### 3.1 Reuse Detection Algorithm

```python
def can_reuse_tv_output(case1, case2):
    # Check if core configuration identical
    if not same_core_config(case1, case2):
        return False
    
    # Check if differing features are trade-irrelevant
    diff_features = find_differences(case1, case2)
    for feature in diff_features:
        if affects_trade_count(feature):
            return False
    
    return True
```

### 3.2 Trade-Affecting Features

Features that ALWAYS affect trade count:
- Signal mode (Supertrend vs Range Filter vs None)
- Entry mode (Touch vs Close vs Signal)
- Use Stop Loss (true/false) when SL mode active
- Use TP (true/false) when TP mode active
- Filter enable/disable states

Features that MAY affect trade count:
- Numeric parameter variations (ATR length, factor, etc.)
- Time stop bar counts
- Daily limit values

### 3.3 Reuse Confidence Levels

- **100%**: Identical trade-affecting configuration
- **80%**: Minor parameter variations, unlikely to affect trades  
- **50%**: Moderate variations, needs spot checking
- **20%**: Significant variations, partial reference only
- **0%**: Different configuration, no reuse

## 4. Reuse Workflow

### 4.1 Phase 1: Initial TV Collection
1. Execute TV for all source cases (Group representatives)
2. Document exact settings and trade counts
3. Validate configuration matches JSON

### 4.2 Phase 2: Reuse Application
1. For each target case, find best source match
2. Copy TV output with appropriate renaming
3. Add note about what differs

### 4.3 Phase 3: Verification Sampling
1. Select random sample from each reuse group
2. Execute TV for verification
3. Confirm trade counts match expectations
4. Update reuse confidence levels

### 4.4 Phase 4: Gap Filling
1. Identify cases with no suitable reuse source
2. Execute TV for remaining cases
3. Add new sources to reuse mapping

## 5. Benefits of Reuse Plan

### 5.1 Efficiency Gains
- Reduce TV manual executions by 60-70%
- Focus effort on unique configurations
- Faster suite completion

### 5.2 Consistency
- Ensure identical configurations produce identical results
- Detect configuration errors early
- Maintain parity between similar cases

### 5.3 Quality
- Systematic approach to reuse validation
- Confidence levels indicate reliability
- Sampling verification ensures accuracy

## 6. Implementation Steps

### 6.1 Create Reuse Mapping
1. Generate initial reuse mapping based on dependency analysis
2. Identify source cases for each feature group
3. Calculate expected reuse coverage

### 6.2 Implement Reuse Detection
1. Create script to analyze case configurations
2. Implement trade-affecting feature detection
3. Generate reuse recommendations

### 6.3 Create Reuse Workflow
1. Document process for TV collection with reuse
2. Create verification sampling procedure
3. Establish quality gates for reuse acceptance

## 7. Next Steps

1. Create initial reuse mapping for core package
2. Implement reuse detection script
3. Create TV collection workflow document
4. Set up verification sampling procedure