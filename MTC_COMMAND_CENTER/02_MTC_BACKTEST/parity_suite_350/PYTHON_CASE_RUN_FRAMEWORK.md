# Python Case Run Automation Framework

## 1. Overview

The Python case run framework automates the execution of parity test cases, comparing MTC Python implementation against TradingView manual results. The framework handles batch execution, result collection, and preliminary validation.

## 2. Architecture

### 2.1 Component Diagram
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Case Loader   │───▶│  Batch Runner   │───▶│  Result Writer  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Config Parser  │    │   Executor      │    │   Report Gen    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 2.2 Key Components

1. **Case Loader** - Loads case configurations from JSON files
2. **Config Parser** - Validates and parses configuration
3. **Batch Runner** - Manages parallel execution of cases
4. **Executor** - Executes individual case using MTC engine
5. **Result Writer** - Saves execution results
6. **Report Generator** - Creates summary reports

## 3. Execution Workflow

### 3.1 Step-by-Step Process

```
1. Load case configurations
   ↓
2. Validate dependencies and constraints
   ↓
3. Group cases by package (core/boundary/pairwise)
   ↓
4. Execute cases in parallel batches
   ↓
5. Collect trade data and metrics
   ↓
6. Save results to structured format
   ↓
7. Generate execution summary
   ↓
8. Prepare for TV comparison
```

### 3.2 Parallel Execution Strategy

- **Core Package**: Sequential execution (establish baseline)
- **Boundary Package**: 4 parallel workers
- **Pairwise Package**: 8 parallel workers (more independent cases)
- **Resource Management**: Monitor memory and CPU usage

## 4. Case Execution Details

### 4.1 Input Requirements

Each case requires:
- `case_config.json` - Case configuration
- Dataset file (specified in config)
- MTC engine with all required indicators

### 4.2 Output Generation

For each case, generate:
- `parity_report.json` - Complete execution results
- `trade_log.csv` - Detailed trade-by-trade data
- `equity_curve.csv` - Equity curve over time
- `metrics_summary.json` - Key performance metrics

### 4.3 Key Metrics Collected

```python
metrics = {
    "total_trades": int,
    "long_trades": int,
    "short_trades": int,
    "winning_trades": int,
    "losing_trades": int,
    "win_rate": float,
    "profit_factor": float,
    "total_net_profit": float,
    "max_drawdown": float,
    "sharpe_ratio": float,
    "calmar_ratio": float,
    "avg_trade": float,
    "avg_win": float,
    "avg_loss": float,
    "largest_win": float,
    "largest_loss": float,
    "total_fees": float,
    "total_slippage": float,
    "first_trade_date": str,
    "last_trade_date": str,
    "total_bars": int,
    "bars_in_trade": int,
    "percent_time_in_market": float
}
```

## 5. Batch Execution Script

### 5.1 Main Script: `run_parity_batch.py`

```python
#!/usr/bin/env python3
"""
Parity Suite 350 - Batch Execution Script
Executes all cases in the parity suite and collects results.
"""

import argparse
import json
import logging
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List, Any

from case_loader import load_cases, validate_case
from case_executor import execute_case
from result_writer import save_results
from report_generator import generate_summary

def setup_logging():
    """Configure logging for batch execution."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('parity_batch.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def execute_batch(cases: List[Dict], max_workers: int = 4) -> Dict[str, Any]:
    """Execute a batch of cases in parallel."""
    logger = logging.getLogger(__name__)
    results = {}
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_case = {
            executor.submit(execute_case, case): case 
            for case in cases
        }
        
        for future in as_completed(future_to_case):
            case = future_to_case[future]
            case_id = case['case_id']
            
            try:
                result = future.result(timeout=300)  # 5 minute timeout
                results[case_id] = result
                logger.info(f"Completed case: {case_id}")
            except Exception as e:
                logger.error(f"Failed case {case_id}: {e}")
                results[case_id] = {
                    "status": "failed",
                    "error": str(e),
                    "case_id": case_id
                }
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Execute parity test cases')
    parser.add_argument('--package', choices=['core', 'boundary', 'pairwise', 'all'],
                       default='all', help='Package to execute')
    parser.add_argument('--workers', type=int, default=4,
                       help='Number of parallel workers')
    parser.add_argument('--cases-dir', type=Path, default=Path('cases'),
                       help='Directory containing case configurations')
    parser.add_argument('--output-dir', type=Path, default=Path('results/raw_outputs'),
                       help='Directory for output results')
    parser.add_argument('--skip-existing', action='store_true',
                       help='Skip cases that already have results')
    
    args = parser.parse_args()
    logger = setup_logging()
    
    # Load cases based on package selection
    cases = load_cases(args.cases_dir, args.package)
    logger.info(f"Loaded {len(cases)} cases for package: {args.package}")
    
    # Validate cases
    valid_cases = []
    for case in cases:
        if validate_case(case):
            valid_cases.append(case)
        else:
            logger.warning(f"Invalid case skipped: {case.get('case_id', 'unknown')}")
    
    logger.info(f"Valid cases: {len(valid_cases)}")
    
    # Execute batch
    results = execute_batch(valid_cases, args.workers)
    
    # Save results
    save_results(results, args.output_dir)
    
    # Generate summary report
    generate_summary(results, args.output_dir / 'summary')
    
    logger.info("Batch execution completed")

if __name__ == '__main__':
    main()
```

### 5.2 Case Executor: `case_executor.py`

```python
"""
Individual case execution logic.
"""

import pandas as pd
from datetime import datetime
from typing import Dict, Any
from mtc_engine import MTCEngine  # Assuming MTC engine interface

def execute_case(case_config: Dict) -> Dict[str, Any]:
    """Execute a single case using MTC engine."""
    
    # Load dataset
    dataset_path = case_config.get('dataset')
    df = pd.read_parquet(dataset_path)
    
    # Initialize MTC engine with case configuration
    engine = MTCEngine(config=case_config['config'])
    
    # Run backtest
    results = engine.run_backtest(df)
    
    # Extract metrics
    metrics = extract_metrics(results, case_config)
    
    # Prepare comprehensive result
    result = {
        "case_id": case_config["case_id"],
        "package": case_config.get("package", "unknown"),
        "status": "completed",
        "execution_time": datetime.now().isoformat(),
        "config": case_config["config"],
        "metrics": metrics,
        "trades": results.get("trades", []),
        "equity_curve": results.get("equity_curve", []),
        "signals": results.get("signals", []),
        "warnings": results.get("warnings", []),
        "errors": results.get("errors", [])
    }
    
    return result

def extract_metrics(results: Dict, case_config: Dict) -> Dict:
    """Extract key metrics from backtest results."""
    trades = results.get("trades", [])
    
    if not trades:
        return {
            "total_trades": 0,
            "total_net_profit": 0,
            "status": "no_trades"
        }
    
    # Calculate basic metrics
    total_trades = len(trades)
    long_trades = sum(1 for t in trades if t.get('direction') == 'long')
    short_trades = total_trades - long_trades
    
    winning_trades = sum(1 for t in trades if t.get('profit', 0) > 0)
    losing_trades = total_trades - winning_trades
    
    total_profit = sum(t.get('profit', 0) for t in trades)
    winning_profit = sum(t.get('profit', 0) for t in trades if t.get('profit', 0) > 0)
    losing_profit = sum(t.get('profit', 0) for t in trades if t.get('profit', 0) < 0)
    
    win_rate = winning_trades / total_trades if total_trades > 0 else 0
    profit_factor = abs(winning_profit / losing_profit) if losing_profit != 0 else float('inf')
    
    # Calculate drawdown from equity curve
    equity_curve = results.get("equity_curve", [])
    if equity_curve:
        equity_values = [e['equity'] for e in equity_curve]
        peak = equity_values[0]
        max_dd = 0
        for value in equity_values:
            if value > peak:
                peak = value
            dd = (peak - value) / peak * 100
            if dd > max_dd:
                max_dd = dd
    else:
        max_dd = 0
    
    return {
        "total_trades": total_trades,
        "long_trades": long_trades,
        "short_trades": short_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "win_rate": round(win_rate, 4),
        "profit_factor": round(profit_factor, 2),
        "total_net_profit": round(total_profit, 2),
        "max_drawdown": round(max_dd, 2),
        "avg_trade": round(total_profit / total_trades, 2) if total_trades > 0 else 0,
        "avg_win": round(winning_profit / winning_trades, 2) if winning_trades > 0 else 0,
        "avg_loss": round(losing_profit / losing_trades, 2) if losing_trades > 0 else 0,
        "largest_win": round(max(t.get('profit', 0) for t in trades), 2) if trades else 0,
        "largest_loss": round(min(t.get('profit', 0) for t in trades), 2) if trades else 0,
        "total_fees": round(sum(t.get('fee', 0) for t in trades), 2),
        "total_slippage": round(sum(t.get('slippage', 0) for t in trades), 2)
    }
```

## 6. Configuration Management

### 6.1 Case Configuration Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["case_id", "config"],
  "properties": {
    "case_id": {
      "type": "string",
      "pattern": "^parity_(core|bnd|pw)_\\d{3}_[a-z_]+$"
    },
    "package": {
      "type": "string",
      "enum": ["core", "boundary", "pairwise"]
    },
    "dependencies": {
      "type": "array",
      "items": {"type": "string"}
    },
    "config": {
      "type": "object",
      "properties": {
        "signal_mode": {"type": "string"},
        "trade": {"type": "object"},
        "strategy": {"type": "object"},
        "risk": {"type": "object"},
        "filters": {"type": "object"},
        "stoploss": {"type": "object"},
        "takeprofit": {"type": "object"}
      }
    }
  }
}
```

### 6.2 Validation Rules

1. **Dependency Validation**: Ensure all required features are enabled
2. **Parameter Range Validation**: Check numeric parameters within valid ranges
3. **Compatibility Validation**: Ensure no conflicting settings
4. **Dataset Validation**: Verify dataset exists and matches date range

## 7. Error Handling and Recovery

### 7.1 Error Categories

1. **Configuration Errors** - Invalid case configuration
2. **Execution Errors** - Runtime errors during backtest
3. **Data Errors** - Missing or corrupt dataset
4. **Resource Errors** - Memory or CPU constraints

### 7.2 Recovery Strategies

- **Retry Logic**: Retry failed cases with exponential backoff
- **Checkpointing**: Save intermediate results periodically
- **Fallback Execution**: Run failed cases sequentially after batch
- **Partial Results**: Save whatever results were obtained before failure

### 7.3 Monitoring and Alerting

- **Progress Tracking**: Real-time progress updates
- **Performance Metrics**: Execution time, memory usage
- **Error Reporting**: Detailed error logs with context
- **Completion Notifications**: Email/Slack notifications on batch completion

## 8. Quality Assurance

### 8.1 Pre-execution Checks

1. Validate all case configurations
2. Verify dataset availability
3. Check MTC engine compatibility
4. Ensure sufficient disk space

### 8.2 During Execution

1. Monitor resource usage
2. Log detailed execution traces
3. Capture warnings and anomalies
4. Validate intermediate results

### 8.3 Post-execution Validation

1. Verify all cases completed
2. Check result file integrity
3. Validate metric calculations
4. Generate quality report

## 9. Performance Optimization

### 9.1 Caching Strategies

- **Dataset Caching**: Cache loaded datasets in memory
- **Indicator Caching**: Cache calculated indicators
- **Result Caching**: Cache results for identical configurations

### 9.2 Parallelization Techniques

- **Case-level Parallelism**: Independent cases in parallel
- **Feature-level Parallelism**: Parallel indicator calculation
- **Data-level Parallelism**: Chunk-based processing

### 9.3 Memory Management

- **Streaming Processing**: Process data in chunks
- **Garbage Collection**: Explicit memory cleanup
- **Resource Limits**: Enforce memory and CPU limits

## 10. Integration with Overall Workflow

### 10.1 Input from Previous Phase
- Case configurations from generation phase
- TV manual inputs (for comparison)

### 10.2 Output to Next Phase
- Parity reports for each case
- Trade logs for detailed analysis
- Summary metrics for comparison

### 10.3 Integration Points
1. **Case Generation** → Load case configurations
2. **TV Collection** → Compare with Python results
3. **Mismatch Analysis** → Provide detailed trade data
4. **Correction Loop** → Re-execute after fixes

## 11. Implementation Roadmap

### Phase 1: Basic Framework
- Implement case loader and executor
- Add basic error handling
- Create simple reporting

### Phase 2: Advanced Features
- Add parallel execution
- Implement caching
- Add comprehensive monitoring

### Phase 3: Optimization
- Performance tuning
- Memory optimization
- Advanced error recovery

## 12. Next Steps

1. Create case loader implementation
2. Implement basic executor
3. Add result writer
4. Create integration tests
5. Set up monitoring and logging