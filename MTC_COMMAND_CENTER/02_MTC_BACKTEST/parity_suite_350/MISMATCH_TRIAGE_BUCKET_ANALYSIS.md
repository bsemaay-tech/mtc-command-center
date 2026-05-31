# Mismatch Triage and Bucket Analysis System

## 1. Overview

When TV vs Python comparisons reveal discrepancies, this system provides a structured approach to triage, categorize, and analyze mismatches. The goal is to efficiently identify root causes and prioritize fixes.

## 2. Mismatch Triage Process

### 2.1 Triage Workflow

```
1. Detect Mismatch
   ↓
2. Initial Classification
   ↓
3. Severity Assessment
   ↓
4. Bucket Assignment
   ↓
5. Root Cause Analysis
   ↓
6. Priority Assignment
   ↓
7. Action Planning
```

### 2.2 Triage Decision Tree

```
Is trade count different?
├── Yes → Check if TV or Python has zero trades
│   ├── TV zero, Python non-zero → Bucket: "False Positive Trades"
│   ├── TV non-zero, Python zero → Bucket: "Missing Trades"  
│   └── Both non-zero, counts differ → Bucket: "Partial Match"
│
└── No → Check trade-by-trade matching
    ├── Match rate < 95% → Bucket: "Low Match Rate"
    ├── Systematic timing offset → Bucket: "Timing Alignment"
    ├── Price differences > tolerance → Bucket: "Price Calculation"
    └── Profit differences > tolerance → Bucket: "Profit Calculation"
```

## 3. Mismatch Bucket Categories

### 3.1 Primary Buckets

#### Bucket 1: Trade Count Mismatches
- **Description**: Different number of trades between TV and Python
- **Sub-categories**:
  - `1A`: TV has trades, Python has none
  - `1B`: Python has trades, TV has none  
  - `1C`: Both have trades but counts differ
- **Common Causes**: Signal detection differences, filter logic errors, entry/exit condition mismatches

#### Bucket 2: Timing Alignment Issues
- **Description**: Trades match but at different times
- **Sub-categories**:
  - `2A`: Systematic offset (all trades shifted)
  - `2B`: Random timing differences
  - `2C`: Bar alignment issues
- **Common Causes**: Timezone handling, bar open/close logic, data alignment

#### Bucket 3: Price Calculation Differences
- **Description**: Entry/exit price differences beyond tolerance
- **Sub-categories**:
  - `3A`: Entry price differences
  - `3B`: Exit price differences  
  - `3C`: Both entry and exit differences
- **Common Causes**: Slippage calculation, commission handling, price rounding

#### Bucket 4: Filter/Logic Implementation Gaps
- **Description**: Specific feature implementations differ
- **Sub-categories**:
  - `4A`: Filter conditions not matching
  - `4B`: Stop loss/take profit logic differences
  - `4C`: Position management discrepancies
  - `4D`: Risk management implementation gaps
- **Common Causes**: Feature parity issues, configuration mapping errors

#### Bucket 5: Data/Indicator Calculation
- **Description**: Underlying indicator values differ
- **Sub-categories**:
  - `5A`: Indicator calculation differences
  - `5B`: Data quality issues
  - `5C`: Warm-up period handling
- **Common Causes**: Calculation algorithms, precision differences, data preprocessing

#### Bucket 6: Configuration/Setup Errors
- **Description**: Incorrect test setup
- **Sub-categories**:
  - `6A`: Configuration mapping errors
  - `6B`: Dependency violations
  - `6C`: Test case generation errors
- **Common Causes**: Human error in test setup, automation bugs

### 3.2 Severity Levels

| Level | Criteria | Impact | Response Time |
|-------|----------|---------|---------------|
| Critical | Core feature broken, multiple cases affected | Blocks entire suite | Immediate (24h) |
| High | Key feature mismatch, affects many cases | Blocks feature validation | 48 hours |
| Medium | Minor feature issue, limited impact | Needs investigation | 1 week |
| Low | Cosmetic differences, tolerance edge cases | Documentation update | 2 weeks |

## 4. Root Cause Analysis Framework

### 4.1 Analysis Steps

1. **Isolate the Issue**
   - Identify specific trades with mismatches
   - Extract relevant time periods
   - Gather indicator values at mismatch points

2. **Compare Configurations**
   - Verify TV settings match Python configuration
   - Check dependency compliance
   - Validate parameter mappings

3. **Analyze Trade Logic**
   - Recreate trade decision at mismatch point
   - Compare indicator values between implementations
   - Step through decision logic

4. **Identify Root Cause**
   - Determine if issue is in: data, indicators, logic, or configuration
   - Document findings with evidence

### 4.2 Diagnostic Tools

```python
class MismatchDiagnostic:
    """Tool for diagnosing mismatch root causes."""
    
    def __init__(self, case_id, tv_data, python_data):
        self.case_id = case_id
        self.tv_data = tv_data
        self.python_data = python_data
        self.mismatches = []
    
    def analyze_trade_count_mismatch(self):
        """Analyze why trade counts differ."""
        tv_count = len(self.tv_data['trades'])
        py_count = len(self.python_data['trades'])
        
        if tv_count == 0 and py_count > 0:
            return self._analyze_false_positives()
        elif tv_count > 0 and py_count == 0:
            return self._analyze_missing_trades()
        else:
            return self._analyze_partial_match()
    
    def _analyze_false_positives(self):
        """Python has trades that TV doesn't."""
        analysis = {
            'type': 'false_positives',
            'python_trades': self.python_data['trades'],
            'potential_causes': []
        }
        
        # Check each Python trade against TV data
        for trade in self.python_data['trades']:
            # Analyze why TV didn't take this trade
            cause = self._analyze_single_trade_mismatch(trade, None)
            analysis['potential_causes'].append(cause)
        
        return analysis
    
    def generate_diagnostic_report(self):
        """Generate comprehensive diagnostic report."""
        report = {
            'case_id': self.case_id,
            'analysis_timestamp': datetime.now().isoformat(),
            'trade_count_analysis': self.analyze_trade_count_mismatch(),
            'timing_analysis': self.analyze_timing_issues(),
            'price_analysis': self.analyze_price_differences(),
            'indicator_analysis': self.analyze_indicator_values(),
            'configuration_validation': self.validate_configurations(),
            'root_cause_hypotheses': self.generate_hypotheses(),
            'recommended_actions': self.recommend_actions()
        }
        
        return report
```

## 5. Bucket Analysis Dashboard

### 5.1 Dashboard Metrics

```python
bucket_metrics = {
    "total_cases": 350,
    "passed_cases": 280,
    "failed_cases": 70,
    "bucket_distribution": {
        "bucket_1": {"count": 15, "percent": 21.4},
        "bucket_2": {"count": 10, "percent": 14.3},
        "bucket_3": {"count": 8, "percent": 11.4},
        "bucket_4": {"count": 25, "percent": 35.7},
        "bucket_5": {"count": 7, "percent": 10.0},
        "bucket_6": {"count": 5, "percent": 7.1}
    },
    "severity_distribution": {
        "critical": {"count": 5, "percent": 7.1},
        "high": {"count": 20, "percent": 28.6},
        "medium": {"count": 30, "percent": 42.9},
        "low": {"count": 15, "percent": 21.4}
    },
    "feature_impact": {
        "supertrend": {"cases": 12, "bucket": "4A"},
        "stoploss": {"cases": 8, "bucket": "4B"},
        "filters": {"cases": 18, "bucket": "4A"},
        "timing": {"cases": 10, "bucket": "2A"}
    }
}
```

### 5.2 Visualization Requirements

1. **Bucket Distribution Chart** - Pie/bar chart of mismatch buckets
2. **Severity Heatmap** - Cases by severity and bucket
3. **Trend Analysis** - Mismatches over time/progress
4. **Feature Impact Matrix** - Which features cause most issues
5. **Case Correlation Map** - Related mismatches across cases

## 6. Prioritization Matrix

### 6.1 Priority Calculation

```
Priority Score = (Severity Weight × 3) + (Impact Weight × 2) + (Frequency Weight × 1)

Where:
- Severity Weight: Critical=4, High=3, Medium=2, Low=1
- Impact Weight: Core feature=3, Boundary feature=2, Pairwise feature=1  
- Frequency Weight: Multiple cases=3, Few cases=2, Single case=1
```

### 6.2 Priority Tiers

| Tier | Score Range | Description | Response |
|------|-------------|-------------|----------|
| P0 | 15-18 | Critical issues blocking suite | Immediate fix |
| P1 | 10-14 | High impact, frequent issues | Next sprint |
| P2 | 6-9 | Medium impact issues | Schedule fix |
| P3 | 3-5 | Low impact, isolated issues | Backlog |
| P4 | 0-2 | Cosmetic/minor issues | Document only |

## 7. Action Planning

### 7.1 Action Types

#### Type A: Code Fixes
- Fix implementation bugs in MTC engine
- Update indicator calculations
- Correct logic errors

#### Type B: Configuration Updates
- Fix configuration mappings
- Update dependency rules
- Correct test case generation

#### Type C: Data Corrections
- Fix data alignment issues
- Update timezone handling
- Correct data preprocessing

#### Type D: Documentation
- Update tolerance settings
- Document known differences
- Add workarounds

#### Type E: Test Suite Updates
- Update test expectations
- Add new test cases
- Improve validation rules

### 7.2 Action Tracking

```python
action_item = {
    "id": "ACT-001",
    "case_id": "parity_core_001_baseline_touch",
    "bucket": "1A",
    "severity": "high",
    "priority": "P1",
    "description": "Python generating false positive trades",
    "root_cause": "Entry signal detection logic differs from TV",
    "assigned_to": "engineer@example.com",
    "due_date": "2026-03-01",
    "status": "investigating",  # investigating, fixing, testing, verified
    "fix_type": "A",  # Code fix
    "test_cases": ["parity_core_001", "parity_core_002"],
    "verification_plan": "Re-run affected cases after fix",
    "notes": "Need to check SuperTrend calculation at bar close"
}
```

## 8. Verification and Closure

### 8.1 Fix Verification Process

1. **Implement Fix** - Apply code/config changes
2. **Re-run Affected Cases** - Execute Python for impacted cases
3. **Re-compare with TV** - Run comparison again
4. **Verify Resolution** - Confirm mismatches resolved
5. **Update Documentation** - Document fix and lessons learned

### 8.2 Closure Criteria

A mismatch can be closed when:
1. Root cause identified and documented
2. Fix implemented and verified
3. All affected cases pass comparison
4. No regression introduced in other cases
5. Documentation updated

## 9. Reporting and Communication

### 9.1 Daily Status Report

```
Mismatch Triage Status - 2026-02-25
====================================

Summary:
- Total cases: 350
- Passed: 280 (80%)
- Failed: 70 (20%)
- In progress: 15
- Resolved today: 5

Top Issues:
1. Bucket 4A (Filter conditions) - 10 cases (P1)
2. Bucket 2A (Timing alignment) - 8 cases (P1)  
3. Bucket 1C (Partial match) - 6 cases (P2)

Critical Issues:
- None currently

Actions Required:
- Engineer A: Investigate SuperTrend filter mismatches (3 cases)
- Engineer B: Fix timezone alignment issue (2 cases)

Next Steps:
- Complete investigation of 5 remaining P1 issues
- Begin fixing highest priority items
```

### 9.2 Stakeholder Communication

- **Daily**: Team standup with mismatch status
- **Weekly**: Detailed analysis report to stakeholders
- **Milestone**: Comprehensive summary at package completion
- **Ad-hoc**: Immediate notification for critical issues

## 10. Continuous Improvement

### 10.1 Lessons Learned Process

After each mismatch resolution:
1. Document root cause and solution
2. Identify process improvements
3. Update prevention measures
4. Share knowledge with team

### 10.2 Prevention Measures

1. **Proactive Validation** - Validate configurations before execution
2. **Early Detection** - Compare sample cases early in process
3. **Automated Checks** - Add validation rules to case generation
4. **Knowledge Base** - Maintain database of known issues and solutions

## 11. Implementation Roadmap

### Phase 1: Basic Triage
- Implement bucket classification
- Create basic diagnostic tools
- Set up tracking spreadsheet

### Phase 2: Advanced Analysis
- Implement automated root cause analysis
- Create dashboard visualizations
- Add prioritization algorithms

### Phase 3: Integration
- Integrate with existing test frameworks
- Automate action tracking
- Implement continuous improvement loop

## 12. Success Metrics

1. **Time to Triage** - Average time from detection to bucket assignment
2. **Time to Resolution** - Average time from detection to fix verification
3. **First-Pass Accuracy** - Percentage of correct bucket assignments
4. **Recurrence Rate** - Percentage of issues that reoccur
5. **Stakeholder Satisfaction** - Feedback on communication and resolution

This system ensures mismatches are handled systematically, efficiently, and with clear accountability, leading to faster parity achievement and higher quality MTC implementation.