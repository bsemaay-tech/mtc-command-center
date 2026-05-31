# MTC Parity Suite 350 - Case Classification Plan

## 1. Case Set Classification Strategy

### 1.1 Three-Tier Classification System

Based on dependency analysis and previous experience, we classify cases into three categories:

#### **CORE Cases** 
- Fundamental configurations that must work correctly
- Independent of other features (minimal dependencies)
- Serve as baseline for all other tests
- Examples: Baseline touch/close, basic signal modes

#### **BOUNDARY Cases**
- Test edge cases and boundary conditions  
- Validate dependency relationships
- Ensure feature isolation works correctly
- Examples: Time stop variations, SL/TP boundary values

#### **PAIRWISE Cases**
- Test combinations of features
- Validate feature interactions
- Ensure no conflicts between enabled features
- Examples: Multi-TP with different SL modes, filters with confirmation layers

### 1.2 Dependency Rules (From User Analysis)

Key dependencies that must be respected:

1. **Exit if selected filter blocks** → Requires "While In Position" active
2. **Use Time stop** → Required for "Exit end of day" and "Exit end of week"
3. **Signal mode Super trend** → Super trend settings affect trade count
4. **Signal mode Range Filter hybrid** → Must be selected for RF hybrid settings to affect trade count
5. **Signal mode none** → Should generate zero trades
6. **Use daily Loss limit** → Required for Max daily loss % to affect trade count
7. **Use Max trades per day** → Required for max trade per days to affect trade count
8. **Use Stop Loss** → Required for SL modes to affect trade count
9. **SL mode ATR** → Required for SL ATR and ATR length to affect trade count
10. **Use TP** → Required for TP modes to affect trade count
11. **Multi TP selected** → Single TP should NOT affect trade count
12. **Same logic applies to Trailing Stop and Break Even**
13. **Filters follow same dependency pattern** (MA, MA Slope, McGinley, HTF Trend, Volume participation, ATR Volatility floor, MACD filter HUB)
14. **MACD Filter hub** → Required for MACD filter modes to affect trade count
15. **Confirmation selected** → Required for confirmation settings to affect trade count
16. **Range and Volatility filter (entry Pause)** → Required for range filters to affect trade count
17. **Guard filters** → Any guard filter must be selected for "Use guard recover" to affect trade count
18. **Use Guard recover (auto resume after block)** → Required for guard recovery modes to work

## 2. Case Package Design

### 2.1 Core Package (50 cases)
- Baseline configurations (touch vs close)
- Basic signal modes (Supertrend, Range Filter, None)
- Entry/Exit fundamentals
- Position management basics
- Risk management fundamentals

### 2.2 Boundary Package (150 cases)
- Time stop variations (12 cases)
- SL mode variations (16 cases)
- TP mode variations (12 cases)
- Multi-TP variations (16 cases)
- Break Even/Trailing variations (12 cases)
- Filter boundary values
- Guard filter edge cases
- Daily limit boundaries

### 2.3 Pairwise Package (150 cases)
- Signal mode × SL mode combinations
- SL mode × TP mode combinations  
- Filter × Confirmation combinations
- Guard × Recovery combinations
- Time stop × Daily limit combinations
- Multi-feature interaction tests

## 3. No Repeat Case Guarantee

### 3.1 Case ID System
```
parity_[type]_[seq]_[feature]_[variant]
```
Where:
- `type`: core, bnd (boundary), pw (pairwise)
- `seq`: 3-digit sequence (001, 002, ...)
- `feature`: primary feature being tested
- `variant`: specific variant identifier

### 3.2 Duplicate Prevention
- Central registry of all case configurations
- Hash-based duplicate detection
- Dependency-aware generation
- Reuse mapping for similar configurations

## 4. Dependency-Aware Test Generation

### 4.1 Generation Rules
1. Start with independent features (Core)
2. Add dependent features only when prerequisites are met
3. Validate dependency chains before case creation
4. Generate both enabled and disabled states for each feature
5. Create boundary values for numeric parameters

### 4.2 Validation Matrix
- Create dependency matrix showing feature relationships
- Generate test cases that cover all valid combinations
- Exclude invalid combinations (e.g., TP settings when Use TP = false)
- Ensure comprehensive coverage of dependency edges

## 5. Implementation Approach

### 5.1 Phase 1: Core Package
- Implement all Core cases
- Validate baseline functionality
- Establish parity baseline

### 5.2 Phase 2: Boundary Package  
- Add boundary cases incrementally
- Validate each feature in isolation
- Confirm dependency rules

### 5.3 Phase 3: Pairwise Package
- Add combination tests
- Validate feature interactions
- Complete comprehensive coverage

## 6. Quality Gates

1. **No duplicate cases** in final suite
2. **All dependencies respected** in case generation
3. **Comprehensive coverage** of feature states
4. **Boundary values tested** for all numeric parameters
5. **Invalid combinations excluded** from test suite

## 7. Next Steps

1. Create detailed case specifications for each package
2. Implement case generation scripts
3. Set up validation checks for dependencies
4. Create reuse mapping for efficient execution
5. Establish parity verification workflow