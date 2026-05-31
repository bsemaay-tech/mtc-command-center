# Parity Suite 350 - Folder Structure Plan

## 1. Root Structure
```
parity_suite_350/
├── README.md                          # Suite overview and instructions
├── CASE_CLASSIFICATION_PLAN.md        # Case classification strategy
├── FOLDER_STRUCTURE_PLAN.md           # This document
├── OPERATION_SOP.md                   # Single-page SOP (to be created)
├── DEPENDENCY_MATRIX.csv              # Feature dependency matrix
├── CASE_REGISTRY.csv                  # Central registry of all cases
├── REUSE_MAPPING.csv                  # Reuse plan for efficient execution
│
├── tv_manual_inputs/                  # TV manual collection structure
│   ├── README_TV_MANUAL.md            # Instructions for TV manual process
│   ├── template_case/                 # Template for case folders
│   │   ├── case_config.json           # Case configuration
│   │   ├── tv_strategy_report.xlsx    # TV export (to be filled)
│   │   ├── parity_report.json         # Python parity results
│   │   ├── comparison_report.md       # TV vs Python comparison
│   │   └── mismatch_analysis.md       # Any mismatch analysis
│   │
│   ├── core_package/                  # Core cases (50 cases)
│   │   ├── 001_parity_core_001_baseline_touch/
│   │   ├── 002_parity_core_002_baseline_close/
│   │   └── ... (48 more)
│   │
│   ├── boundary_package/              # Boundary cases (150 cases)
│   │   ├── 051_parity_bnd_001_time_stop_01/
│   │   ├── 052_parity_bnd_002_time_stop_02/
│   │   └── ... (148 more)
│   │
│   └── pairwise_package/              # Pairwise cases (150 cases)
│       ├── 201_parity_pw_001_supertrend_sl_atr/
│       ├── 202_parity_pw_002_range_filter_tp_fixed/
│       └── ... (148 more)
│
├── cases/                             # JSON case configurations
│   ├── core/
│   │   ├── parity_core_001_baseline_touch.json
│   │   ├── parity_core_002_baseline_close.json
│   │   └── ... (48 more)
│   │
│   ├── boundary/
│   │   ├── parity_bnd_001_time_stop_01.json
│   │   ├── parity_bnd_002_time_stop_02.json
│   │   └── ... (148 more)
│   │
│   └── pairwise/
│       ├── parity_pw_001_supertrend_sl_atr.json
│       ├── parity_pw_002_range_filter_tp_fixed.json
│       └── ... (148 more)
│
├── scripts/                           # Automation scripts
│   ├── generate_cases.py              # Case generation from templates
│   ├── run_parity_batch.py            # Batch execution of cases
│   ├── compare_tv_python.py           # TV vs Python comparison
│   ├── analyze_mismatches.py          # Mismatch analysis
│   └── generate_reports.py            # Report generation
│
├── templates/                         # Configuration templates
│   ├── core_template.json             # Template for core cases
│   ├── boundary_template.json         # Template for boundary cases
│   ├── pairwise_template.json         # Template for pairwise cases
│   └── dependency_rules.json          # Dependency rules definition
│
├── results/                           # Execution results
│   ├── raw_outputs/                   # Raw Python outputs
│   │   ├── core/
│   │   ├── boundary/
│   │   └── pairwise/
│   │
│   ├── comparisons/                   # Comparison results
│   │   ├── by_case/
│   │   ├── by_feature/
│   │   └── summary/
│   │
│   ├── mismatches/                    # Mismatch analysis
│   │   ├── triage/
│   │   ├── buckets/
│   │   └── root_cause/
│   │
│   └── reports/                       # Final reports
│       ├── parity_summary_report.md
│       ├── feature_coverage_report.md
│       └── quality_metrics_report.md
│
└── docs/                              # Documentation
    ├── naming_standards.md            # Naming conventions
    ├── dependency_rules.md            # Detailed dependency rules
    ├── tv_manual_process.md           # TV manual collection process
    └── troubleshooting_guide.md       # Common issues and solutions
```

## 2. TV Manual Inputs Structure Details

### 2.1 Case Folder Naming Convention
```
[3-digit sequence]_[case_id]/
```
Example: `001_parity_core_001_baseline_touch/`

### 2.2 Case Folder Contents
Each case folder contains:
1. `case_config.json` - The case configuration (copied from cases/)
2. `tv_strategy_report.xlsx` - TV export provided by user
3. `parity_report.json` - Python execution results
4. `comparison_report.md` - Automated TV vs Python comparison
5. `mismatch_analysis.md` - Manual analysis if mismatches found
6. `screenshots/` - Optional TV screenshots for reference

### 2.3 Package Organization
- `core_package/` - 50 core cases (001-050)
- `boundary_package/` - 150 boundary cases (051-200)  
- `pairwise_package/` - 150 pairwise cases (201-350)

### 2.4 Reuse Plan Integration
The `REUSE_MAPPING.csv` file will map:
- Which cases can reuse TV exports from others
- Which configurations are identical except for specific parameters
- Groupings for efficient manual collection

## 3. Case Configuration Structure

### 3.1 JSON Case Format
```json
{
  "_comment": "Case description",
  "case_id": "parity_core_001_baseline_touch",
  "package": "core",
  "dependencies": [],
  "config": {
    "signal_mode": "Supertrend",
    "trade": {
      "entry_mode": "Touch"
    },
    // ... other settings
  }
}
```

### 3.2 Dependency Tracking
Each case includes:
- `dependencies` - List of prerequisite features
- `exclusions` - List of incompatible features  
- `validation_rules` - Rules to validate configuration

## 4. Automation Workflow

### 4.1 Phase 1: Case Generation
1. Read dependency rules from `dependency_rules.json`
2. Generate cases for each package type
3. Validate no duplicates or invalid combinations
4. Save to `cases/` directory

### 4.2 Phase 2: Folder Structure Creation
1. Create `tv_manual_inputs/` structure
2. Copy case configurations to respective folders
3. Generate placeholder files for TV exports
4. Create reuse mapping

### 4.3 Phase 3: Execution
1. User provides TV exports for each case
2. Python runs cases and generates results
3. Automated comparison performed
4. Mismatches analyzed and bucketed

## 5. Benefits of This Structure

### 5.1 Organization
- Clear separation of concerns (core/boundary/pairwise)
- Consistent naming and numbering
- Easy navigation and management

### 5.2 Efficiency
- Reuse mapping reduces manual work
- Template-based generation ensures consistency
- Automated comparison saves time

### 5.3 Quality
- Central registry prevents duplicates
- Dependency validation ensures correct configurations
- Comprehensive coverage tracking

### 5.4 Maintainability
- Modular structure for easy updates
- Documentation included at each level
- Scripts for automation and validation

## 6. Implementation Steps

1. Create root directory structure
2. Implement case generation scripts
3. Create template configurations
4. Set up dependency validation
5. Create reuse mapping logic
6. Implement comparison and analysis tools

## 7. Next Steps

1. Create naming standards document
2. Implement case generation script
3. Create initial template configurations
4. Set up folder structure with sample cases