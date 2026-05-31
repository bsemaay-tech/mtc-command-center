# TV vs Python Comparison Methodology

## 1. Overview

This document outlines the methodology for comparing TradingView (TV) manual results with Python MTC engine results. The comparison ensures parity between the two implementations and identifies any discrepancies that need investigation.

## 2. Comparison Levels

### 2.1 Three-Tier Comparison Approach

#### Level 1: High-Level Metrics Comparison
- Compare aggregate metrics (trade count, net profit, win rate)
- Quick pass/fail determination
- Identify gross mismatches

#### Level 2: Trade-by-Trade Comparison  
- Match individual trades between TV and Python
- Compare entry/exit prices, timestamps, direction
- Identify missing or extra trades

#### Level 3: Detailed Analysis
- Analyze timing differences (bar alignment)
- Compare indicator values at trade points
- Investigate root causes of discrepancies

### 2.2 Comparison Dimensions

| Dimension | TV Source | Python Source | Comparison Method |
|-----------|-----------|---------------|-------------------|
| Trade Count | Strategy Report | `parity_report.json` | Exact match |
| Entry Time | Trade List | Trade log | Timestamp alignment |
| Entry Price | Trade List | Trade log | Price tolerance |
| Exit Time | Trade List | Trade log | Timestamp alignment |
| Exit Price | Trade List | Trade log | Price tolerance |
| Direction | Trade List | Trade log | Exact match |
| Profit/Loss | Strategy Report | Trade log | Tolerance-based |
| Equity Curve | Chart export | `equity_curve.csv` | Visual/statistical |

## 3. Data Extraction from TV

### 3.1 TV Strategy Report Structure

The TV Excel export contains:
- **Summary Sheet**: Aggregate metrics
- **Trades Sheet**: Detailed trade list
- **Settings Sheet**: Strategy configuration
- **Performance Sheet**: Additional metrics

### 3.2 Key Data Points to Extract

```python
tv_data = {
    "summary": {
        "total_trades": int,
        "net_profit": float,
        "win_rate": float,
        "profit_factor": float,
        "max_drawdown": float,
        "sharpe_ratio": float
    },
    "trades": [
        {
            "entry_time": "YYYY-MM-DD HH:MM:SS",
            "entry_price": float,
            "exit_time": "YYYY-MM-DD HH:MM:SS",
            "exit_price": float,
            "direction": "long" | "short",
            "profit": float,
            "profit_pct": float,
            "bars_held": int
        }
    ],
    "settings": {
        "signal_mode": str,
        "entry_mode": str,
        "stoploss_mode": str,
        # ... all strategy settings
    }
}
```

### 3.3 TV Data Parsing Script

```python
def parse_tv_excel(file_path):
    """Parse TV strategy report Excel file."""
    import pandas as pd
    
    # Read summary sheet
    summary_df = pd.read_excel(file_path, sheet_name='Summary')
    
    # Read trades sheet
    trades_df = pd.read_excel(file_path, sheet_name='Trades List')
    
    # Read settings sheet
    settings_df = pd.read_excel(file_path, sheet_name='Inputs')
    
    # Extract key metrics
    tv_metrics = {
        'total_trades': int(summary_df.loc[summary_df['Metric'] == 'Total Trades', 'Value'].iloc[0]),
        'net_profit': float(summary_df.loc[summary_df['Metric'] == 'Net Profit', 'Value'].iloc[0]),
        'win_rate': float(summary_df.loc[summary_df['Metric'] == 'Win Rate %', 'Value'].iloc[0]) / 100,
        'profit_factor': float(summary_df.loc[summary_df['Metric'] == 'Profit Factor', 'Value'].iloc[0]),
        'max_drawdown': float(summary_df.loc[summary_df['Metric'] == 'Max Drawdown %', 'Value'].iloc[0]) / 100
    }
    
    # Parse trades
    trades = []
    for _, row in trades_df.iterrows():
        trade = {
            'entry_time': pd.to_datetime(row['Entry Bar Time']),
            'entry_price': float(row['Entry Price']),
            'exit_time': pd.to_datetime(row['Exit Bar Time']),
            'exit_price': float(row['Exit Price']),
            'direction': 'long' if row['Direction'] == 'Buy' else 'short',
            'profit': float(row['Profit']),
            'profit_pct': float(row['Profit %']),
            'bars_held': int(row['Bars Held'])
        }
        trades.append(trade)
    
    # Parse settings
    settings = {}
    for _, row in settings_df.iterrows():
        key = row['Input']
        value = row['Value']
        # Convert value types appropriately
        if isinstance(value, str):
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif value.replace('.', '', 1).isdigit():
                value = float(value) if '.' in value else int(value)
        settings[key] = value
    
    return {
        'metrics': tv_metrics,
        'trades': trades,
        'settings': settings
    }
```

## 4. Python Results Structure

### 4.1 Expected Python Output

```python
python_data = {
    "case_id": "parity_core_001_baseline_touch",
    "metrics": {
        "total_trades": 142,
        "net_profit": 1250.75,
        "win_rate": 0.524,
        # ... other metrics
    },
    "trades": [
        {
            "entry_bar": 150,
            "entry_time": "2025-07-01 10:30:00",
            "entry_price": 51250.25,
            "exit_bar": 155,
            "exit_time": "2025-07-01 13:45:00",
            "exit_price": 51320.50,
            "direction": "long",
            "profit": 70.25,
            "profit_pct": 0.137,
            "bars_held": 5
        }
    ],
    "equity_curve": [
        {"time": "2025-07-01 10:30:00", "equity": 10000.00},
        # ... more points
    ]
}
```

## 5. Comparison Algorithms

### 5.1 High-Level Metrics Comparison

```python
def compare_metrics(tv_metrics, python_metrics, tolerances):
    """Compare high-level metrics with tolerances."""
    results = {}
    
    for key in ['total_trades', 'net_profit', 'win_rate', 'profit_factor']:
        tv_val = tv_metrics.get(key)
        py_val = python_metrics.get(key)
        
        if key == 'total_trades':
            # Trade count must match exactly
            match = tv_val == py_val
            tolerance = 0
        else:
            # Other metrics have percentage tolerance
            if tv_val == 0 and py_val == 0:
                match = True
            elif tv_val == 0 or py_val == 0:
                match = False
            else:
                diff_pct = abs(tv_val - py_val) / abs(tv_val) * 100
                match = diff_pct <= tolerances.get(key, 1.0)  # 1% default
        
        results[key] = {
            'tv': tv_val,
            'python': py_val,
            'match': match,
            'diff': tv_val - py_val if isinstance(tv_val, (int, float)) else None,
            'diff_pct': diff_pct if 'diff_pct' in locals() else None
        }
    
    return results
```

### 5.2 Trade-by-Trade Matching

```python
def match_trades(tv_trades, python_trades, time_tolerance='5min', price_tolerance=0.001):
    """Match individual trades between TV and Python."""
    
    matched = []
    tv_unmatched = tv_trades.copy()
    py_unmatched = python_trades.copy()
    
    # Convert to DataFrames for easier manipulation
    tv_df = pd.DataFrame(tv_trades)
    py_df = pd.DataFrame(python_trades)
    
    # Add time windows for matching
    tv_df['entry_time_window_start'] = tv_df['entry_time'] - pd.Timedelta(time_tolerance)
    tv_df['entry_time_window_end'] = tv_df['entry_time'] + pd.Timedelta(time_tolerance)
    
    # Match trades
    for _, tv_trade in tv_df.iterrows():
        # Find Python trades in the same time window with same direction
        mask = (
            (py_df['entry_time'] >= tv_trade['entry_time_window_start']) &
            (py_df['entry_time'] <= tv_trade['entry_time_window_end']) &
            (py_df['direction'] == tv_trade['direction'])
        )
        
        candidates = py_df[mask]
        
        if len(candidates) > 0:
            # Find best match by price proximity
            candidates['price_diff'] = abs(candidates['entry_price'] - tv_trade['entry_price'])
            best_match = candidates.loc[candidates['price_diff'].idxmin()]
            
            # Check if within price tolerance
            price_diff_pct = abs(best_match['entry_price'] - tv_trade['entry_price']) / tv_trade['entry_price']
            
            if price_diff_pct <= price_tolerance:
                matched.append({
                    'tv_trade': tv_trade.to_dict(),
                    'python_trade': best_match.to_dict(),
                    'entry_time_diff': (best_match['entry_time'] - tv_trade['entry_time']).total_seconds(),
                    'entry_price_diff_pct': price_diff_pct * 100,
                    'profit_diff': best_match['profit'] - tv_trade['profit']
                })
                
                # Remove matched trades
                py_df = py_df.drop(best_match.name)
                tv_unmatched = [t for t in tv_unmatched if t['entry_time'] != tv_trade['entry_time']]
    
    return {
        'matched_trades': matched,
        'tv_unmatched': tv_unmatched,
        'python_unmatched': py_df.to_dict('records'),
        'match_rate': len(matched) / len(tv_trades) if tv_trades else 0
    }
```

### 5.3 Timing Alignment Analysis

```python
def analyze_timing_differences(matched_trades):
    """Analyze systematic timing differences."""
    if not matched_trades:
        return {}
    
    entry_diffs = [t['entry_time_diff'] for t in matched_trades]
    exit_diffs = [t.get('exit_time_diff', 0) for t in matched_trades]
    
    return {
        'entry_time_stats': {
            'mean': np.mean(entry_diffs),
            'std': np.std(entry_diffs),
            'min': np.min(entry_diffs),
            'max': np.max(entry_diffs),
            'median': np.median(entry_diffs)
        },
        'exit_time_stats': {
            'mean': np.mean(exit_diffs),
            'std': np.std(exit_diffs),
            'min': np.min(exit_diffs),
            'max': np.max(exit_diffs),
            'median': np.median(exit_diffs)
        },
        'systematic_offset': np.median(entry_diffs) > 300,  # >5 minutes
        'consistent_direction': all(d > 0 for d in entry_diffs) or all(d < 0 for d in entry_diffs)
    }
```

## 6. Comparison Report Generation

### 6.1 Report Structure

```python
comparison_report = {
    "case_id": "parity_core_001_baseline_touch",
    "comparison_date": "2026-02-25T14:44:47Z",
    "summary": {
        "status": "PASS" | "FAIL" | "PARTIAL",
        "metrics_match": True/False,
        "trades_match": True/False,
        "overall_match_percentage": 95.5
    },
    "metrics_comparison": {
        "total_trades": {"tv": 142, "python": 142, "match": True},
        "net_profit": {"tv": 1250.75, "python": 1248.50, "match": True, "diff_pct": 0.18},
        # ... other metrics
    },
    "trade_matching": {
        "total_tv_trades": 142,
        "total_python_trades": 142,
        "matched_trades": 140,
        "tv_unmatched": 2,
        "python_unmatched": 2,
        "match_rate": 98.6,
        "match_details": [
            {
                "trade_index": 1,
                "tv_entry": "2025-07-01 10:30:00",
                "python_entry": "2025-07-01 10:30:00",
                "entry_time_diff_seconds": 0,
                "profit_diff": 0.25
            }
        ]
    },
    "timing_analysis": {
        "systematic_offset": False,
        "mean_entry_time_diff": 12.5,
        "entry_time_std": 45.2
    },
    "discrepancies": [
        {
            "type": "missing_trade",
            "trade_details": {...},
            "possible_causes": ["bar alignment", "indicator calculation", "filter condition"],
            "severity": "high" | "medium" | "low"
        }
    ],
    "recommendations": [
        "Check bar alignment for trades around 2025-08-15",
        "Verify indicator calculation for SuperTrend on 2025-09-01"
    ]
}
```

### 6.2 Visual Comparison Charts

Generate the following visualizations:
1. **Trade Timeline Comparison** - Side-by-side trade timing
2. **Equity Curve Overlay** - TV vs Python equity curves
3. **Profit Distribution Comparison** - Histogram of trade profits
4. **Timing Difference Distribution** - Histogram of entry time differences

## 7. Tolerance Settings

### 7.1 Default Tolerances

```python
DEFAULT_TOLERANCES = {
    # Metric tolerances (percentage)
    'net_profit': 1.0,      # 1% difference allowed
    'win_rate': 2.0,        # 2% difference allowed  
    'profit_factor': 5.0,   # 5% difference allowed
    'max_drawdown': 5.0,    # 5% difference allowed
    
    # Trade matching tolerances
    'entry_time_tolerance': '5min',     # 5 minutes
    'exit_time_tolerance': '5min',      # 5 minutes
    'price_tolerance': 0.001,           # 0.1% price difference
    'profit_tolerance': 0.01,           # 1% profit difference
    
    # Match rate thresholds
    'min_match_rate': 95.0,             # 95% trade match required
    'max_unmatched_trades': 5           # Maximum 5 unmatched trades
}
```

### 7.2 Tolerance Adjustment Rules

1. **Core Package**: Stricter tolerances (0.5% profit, 2 minutes time)
2. **Boundary Package**: Standard tolerances (1% profit, 5 minutes time)  
3. **Pairwise Package**: Relaxed tolerances (2% profit, 10 minutes time)
4. **Signal Mode = None**: Zero tolerance for any trades

## 8. Quality Gates

### 8.1 Pass/Fail Criteria

**PASS Criteria (All must be true):**
1. Trade count matches exactly
2. Match rate ≥ 95%
3. Net profit difference ≤ tolerance
4. No systematic timing offset > 5 minutes
5. All dependencies validated

**PARTIAL PASS Criteria:**
1. Trade count matches exactly
2. Match rate ≥ 80% but < 95%
3. Profit difference ≤ 2× tolerance
4. Minor timing issues identified

**FAIL Criteria (Any one true):**
1. Trade count mismatch
2. Match rate < 80%
3. Profit difference > 2× tolerance
4. Systematic timing offset > 15 minutes
5. Dependency violation detected

### 8.2 Severity Classification

| Severity | Criteria | Action Required |
|----------|----------|-----------------|
| Critical | Trade count mismatch, Match rate < 50% | Immediate investigation, halt suite |
| High | Match rate 50-80%, Profit diff > 5% | Priority investigation, may block release |
| Medium | Match rate 80-95%, Minor timing issues | Investigation needed, document findings |
| Low | Match rate ≥ 95%, Small profit differences | Monitor, may be acceptable variance |

## 9. Automated Comparison Workflow

### 9.1 Comparison Script: `compare_tv_python.py`

```python
#!/usr/bin/env python3
"""
Compare TV manual results with Python execution results.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List

from tv_parser import parse_tv_excel
from comparison_engine import compare_metrics, match_trades
from report_generator import generate_comparison_report

def compare_case(tv_excel_path: Path, python_json_path: Path) -> Dict:
    """Compare a single case."""
    
    # Load TV data
    tv_data = parse_tv_excel(tv_excel_path)
    
    # Load Python data
    with open(python_json_path) as f:
        python_data = json.load(f)
    
    # Compare metrics
    metrics_comparison = compare_metrics(
        tv_data['metrics'],
        python_data['metrics'],
        tolerances=DEFAULT_TOLERANCES
    )
    
    # Match trades
    trade_matching = match_trades(
        tv_data['trades'],
        python_data['trades'],
        time_tolerance=DEFAULT_TOLERANCES['entry_time_tolerance'],
        price_tolerance=DEFAULT_TOLERANCES['price_tolerance']
    )
    
    # Generate report
    report