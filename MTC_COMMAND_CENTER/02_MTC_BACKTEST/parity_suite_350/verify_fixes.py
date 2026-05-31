#!/usr/bin/env python3
"""
Verify that dependency fixes resolved all issues.
"""

import json
import csv
from pathlib import Path
from typing import Dict, Any

def get_nested_value(data: Dict, path: str, default=None) -> Any:
    """Get value from nested dictionary using dot notation."""
    keys = path.split('.')
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def verify_case(case_path: Path, case_id: str) -> Dict[str, Any]:
    """Verify a fixed case has no dependency issues."""
    with open(case_path, 'r', encoding='utf-8') as f:
        case_data = json.load(f)
    
    config = case_data.get('config', {})
    
    issues = []
    
    # 1. Check exit_on_filter_block dependencies
    exit_on_filter_block = get_nested_value(config, 'trade.exit_on_filter_block', False)
    if exit_on_filter_block:
        # Check if any filter is enabled
        filter_paths = [
            'filters.use_ma_filter',
            'filters.use_ma_slope_filter', 
            'filters.use_mcginley_filter',
            'filters.use_htf_trend_filter',
            'filters.use_volume_filter',
            'filters.use_atr_vol_filter',
        ]
        
        any_filter_enabled = False
        for filter_path in filter_paths:
            if get_nested_value(config, filter_path, False):
                any_filter_enabled = True
                # Check if corresponding block exit is enabled
                if filter_path == 'filters.use_ma_filter':
                    exit_on_ma_block = get_nested_value(config, 'exit_filter_block.exit_on_ma_block', False)
                    if not exit_on_ma_block:
                        issues.append(f"MA filter enabled but exit_on_ma_block=false")
                break
        
        if not any_filter_enabled:
            issues.append("exit_on_filter_block=true but no filters enabled (inert)")
    
    # 2. Check MA slope filter dependency
    use_ma_slope_filter = get_nested_value(config, 'filters.use_ma_slope_filter', False)
    if use_ma_slope_filter:
        use_ma_filter = get_nested_value(config, 'filters.use_ma_filter', False)
        if not use_ma_filter:
            issues.append("use_ma_slope_filter=true but use_ma_filter=false")
    
    # 3. Check risk limit dependencies
    # Daily loss limit
    max_daily_loss = get_nested_value(config, 'risk.max_daily_loss_percent', 0)
    if max_daily_loss > 0:
        use_daily_loss_limit = get_nested_value(config, 'risk.use_daily_loss_limit', False)
        if not use_daily_loss_limit:
            issues.append("max_daily_loss_percent set but use_daily_loss_limit=false")
    
    # Max trades per day
    max_trades = get_nested_value(config, 'risk.max_trades_per_day', 0)
    if max_trades > 0:
        use_max_trades = get_nested_value(config, 'risk.use_max_trades_per_day', False)
        if not use_max_trades:
            issues.append("max_trades_per_day set but use_max_trades_per_day=false")
    
    # 4. Check signal mode dependencies (should be cleaned)
    signal_mode = get_nested_value(config, 'signal_mode', '').lower()
    
    # Supertrend settings when not supertrend
    if signal_mode != 'supertrend':
        supertrend_paths = ['supertrend.atr_len', 'supertrend.factor', 'supertrend.use_wicks', 'supertrend.use_ha']
        for path in supertrend_paths:
            if get_nested_value(config, path, None) is not None:
                issues.append(f"Supertrend setting {path} present but signal_mode={signal_mode}")
    
    # Range filter settings when not range
    if 'range' not in signal_mode:
        range_paths = ['range_filter.atr_len', 'range_filter.smoothing', 'range_filter.multiplier']
        for path in range_paths:
            if get_nested_value(config, path, None) is not None:
                issues.append(f"Range filter setting {path} present but signal_mode={signal_mode}")
    
    # 5. Check SL/TP dependencies
    # Stop loss
    sl_mode = get_nested_value(config, 'stop_loss.mode', '')
    if sl_mode:
        use_sl = get_nested_value(config, 'stop_loss.use_sl', False)
        if not use_sl:
            issues.append(f"SL mode={sl_mode} but use_sl=false")
    
    # Take profit
    tp_mode = get_nested_value(config, 'take_profit.mode', '')
    if tp_mode:
        use_tp = get_nested_value(config, 'take_profit.use_tp', False)
        if not use_tp:
            issues.append(f"TP mode={tp_mode} but use_tp=false")
    
    # 6. Check time stop dependencies
    time_stop_enabled = get_nested_value(config, 'time_stop.enabled', False)
    if not time_stop_enabled:
        time_stop_bars = get_nested_value(config, 'time_stop.bars', 0)
        time_stop_eod = get_nested_value(config, 'time_stop.exit_at_end_of_day', False)
        time_stop_eow = get_nested_value(config, 'time_stop.exit_at_end_of_week', False)
        
        if time_stop_bars > 0:
            issues.append("time_stop.bars set but time_stop.enabled=false")
        if time_stop_eod:
            issues.append("exit_at_end_of_day=true but time_stop.enabled=false")
        if time_stop_eow:
            issues.append("exit_at_end_of_week=true but time_stop.enabled=false")
    
    return {
        'case_id': case_id,
        'issues': issues,
        'issue_count': len(issues),
        'has_fix_notes': '_fix_notes' in case_data
    }

def main():
    suite_root = Path(__file__).parent
    fixed_cases_dir = suite_root / 'cases_fixed'
    manifest_path = suite_root / 'manifests' / 'cases_manifest_all_fixed.csv'
    
    # Read manifest
    with open(manifest_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        cases = list(reader)
    
    print(f"Verifying {len(cases)} fixed cases...")
    print("=" * 80)
    
    all_issues = []
    clean_cases = 0
    
    for case in cases:
        case_id = case['case_id']
        # Try fixed cases dir first, then original
        case_path = fixed_cases_dir / f"{case_id}.json"
        if not case_path.exists():
            case_path = suite_root / 'cases' / f"{case_id}.json"
        
        if not case_path.exists():
            print(f"Warning: Case file not found: {case_path}")
            continue
        
        result = verify_case(case_path, case_id)
        
        if result['issues']:
            print(f"\n[X] {case_id}:")
            for issue in result['issues']:
                print(f"  - {issue}")
            all_issues.extend([(case_id, issue) for issue in result['issues']])
        else:
            clean_cases += 1
            print(f"[OK] {case_id}: Clean")
    
    print("\n" + "=" * 80)
    print(f"Verification Results:")
    print(f"  Total cases: {len(cases)}")
    print(f"  Clean cases: {clean_cases}")
    print(f"  Cases with remaining issues: {len(cases) - clean_cases}")
    print(f"  Total issues found: {len(all_issues)}")
    
    if all_issues:
        print("\nRemaining Issues:")
        for case_id, issue in all_issues:
            print(f"  {case_id}: {issue}")
        
        # Save verification report
        report_path = suite_root / 'fix_verification_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Fix Verification Report\n\n")
            f.write(f"**Total cases verified:** {len(cases)}\n")
            f.write(f"**Clean cases:** {clean_cases}\n")
            f.write(f"**Cases with issues:** {len(cases) - clean_cases}\n")
            f.write(f"**Total issues:** {len(all_issues)}\n\n")
            
            f.write("## Cases with Remaining Issues\n\n")
            for case in cases:
                case_id = case['case_id']
                case_path = fixed_cases_dir / f"{case_id}.json"
                if case_path.exists():
                    result = verify_case(case_path, case_id)
                    if result['issues']:
                        f.write(f"### {case_id}\n")
                        for issue in result['issues']:
                            f.write(f"- {issue}\n")
                        f.write("\n")
            
            f.write("## Recommendations\n\n")
            f.write("1. Manual review needed for cases with remaining issues\n")
            f.write("2. Consider whether these are false positives or need additional fixes\n")
            f.write("3. Run TV parity tests to validate behavior\n")
        
        print(f"\nVerification report saved to: {report_path}")
    else:
        print("\n🎉 SUCCESS: All dependency issues have been resolved!")
        print("\nNext steps:")
        print("1. Update TV manual inputs for the fixed cases")
        print("2. Run parity tests to validate behavior")
        print("3. Consider running optimization script on fixed cases")

if __name__ == '__main__':
    main()