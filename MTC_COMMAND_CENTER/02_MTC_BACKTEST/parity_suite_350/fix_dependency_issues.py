#!/usr/bin/env python3
"""
Fix dependency issues in the case set and generate corrected manifest.
"""

import json
import csv
import shutil
from pathlib import Path
from typing import Dict, Any, List, Tuple
import hashlib

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

def set_nested_value(data: Dict, path: str, value: Any) -> None:
    """Set value in nested dictionary using dot notation."""
    keys = path.split('.')
    current = data
    for i, key in enumerate(keys[:-1]):
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value

def calculate_config_hash(config: Dict) -> str:
    """Calculate SHA256 hash of configuration for duplicate detection."""
    config_str = json.dumps(config, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(config_str.encode()).hexdigest()

def fix_case_dependencies(case_data: Dict, case_id: str) -> Tuple[Dict, List[str]]:
    """Fix dependency issues in a case and return fixed case with change notes."""
    config = case_data.get('config', {}).copy()
    changes = []
    
    # Make a deep copy to avoid modifying original
    import copy
    fixed_config = copy.deepcopy(config)
    
    # 1. Fix exit_on_filter_block dependencies
    exit_on_filter_block = get_nested_value(fixed_config, 'trade.exit_on_filter_block', False)
    if exit_on_filter_block:
        # Ensure at least one filter is enabled and has block exit enabled
        use_ma_filter = get_nested_value(fixed_config, 'filters.use_ma_filter', False)
        if use_ma_filter:
            # Set exit_on_ma_block to true for global exit to work
            current_exit_on_ma_block = get_nested_value(fixed_config, 'exit_filter_block.exit_on_ma_block', False)
            if not current_exit_on_ma_block:
                set_nested_value(fixed_config, 'exit_filter_block.exit_on_ma_block', True)
                changes.append("Fixed: Set exit_on_ma_block=true for global filter block exit")
    
    # 2. Fix MA slope filter dependency
    use_ma_slope_filter = get_nested_value(fixed_config, 'filters.use_ma_slope_filter', False)
    if use_ma_slope_filter:
        use_ma_filter = get_nested_value(fixed_config, 'filters.use_ma_filter', False)
        if not use_ma_filter:
            # Option 1: Enable MA filter (preferred for testing)
            set_nested_value(fixed_config, 'filters.use_ma_filter', True)
            changes.append("Fixed: Enabled use_ma_filter=true for MA slope filter dependency")
            # Also need to set exit_on_ma_block if exit_on_filter_block is true
            if exit_on_filter_block:
                set_nested_value(fixed_config, 'exit_filter_block.exit_on_ma_block', True)
                changes.append("Fixed: Set exit_on_ma_block=true for MA filter")
    
    # 3. Fix risk limit dependencies
    # Daily loss limit
    max_daily_loss = get_nested_value(fixed_config, 'risk.max_daily_loss_percent', 0)
    if max_daily_loss > 0:
        use_daily_loss_limit = get_nested_value(fixed_config, 'risk.use_daily_loss_limit', False)
        if not use_daily_loss_limit:
            # Option: Enable the parent toggle
            set_nested_value(fixed_config, 'risk.use_daily_loss_limit', True)
            changes.append(f"Fixed: Enabled use_daily_loss_limit=true for max_daily_loss_percent={max_daily_loss}")
    
    # Max trades per day
    max_trades = get_nested_value(fixed_config, 'risk.max_trades_per_day', 0)
    if max_trades > 0:
        use_max_trades = get_nested_value(fixed_config, 'risk.use_max_trades_per_day', False)
        if not use_max_trades:
            set_nested_value(fixed_config, 'risk.use_max_trades_per_day', True)
            changes.append(f"Fixed: Enabled use_max_trades_per_day=true for max_trades_per_day={max_trades}")
    
    # 4. Fix signal mode dependencies
    signal_mode = get_nested_value(fixed_config, 'signal_mode', '').lower()
    
    # Remove supertrend settings if signal mode is not supertrend
    if signal_mode != 'supertrend':
        supertrend_paths = ['supertrend.atr_len', 'supertrend.factor', 'supertrend.use_wicks', 'supertrend.use_ha']
        for path in supertrend_paths:
            if get_nested_value(fixed_config, path, None) is not None:
                # Remove or set to default
                keys = path.split('.')
                parent = fixed_config
                for key in keys[:-1]:
                    parent = parent.get(key, {})
                if keys[-1] in parent:
                    del parent[keys[-1]]
                    changes.append(f"Removed inert setting: {path} (signal_mode={signal_mode})")
    
    # Remove range filter settings if signal mode is not range
    if 'range' not in signal_mode:
        range_paths = ['range_filter.atr_len', 'range_filter.smoothing', 'range_filter.multiplier']
        for path in range_paths:
            if get_nested_value(fixed_config, path, None) is not None:
                keys = path.split('.')
                parent = fixed_config
                for key in keys[:-1]:
                    parent = parent.get(key, {})
                if keys[-1] in parent:
                    del parent[keys[-1]]
                    changes.append(f"Removed inert setting: {path} (signal_mode={signal_mode})")
    
    # 5. Fix SL/TP dependencies
    # Stop loss
    sl_mode = get_nested_value(fixed_config, 'stop_loss.mode', '')
    if sl_mode:
        use_sl = get_nested_value(fixed_config, 'stop_loss.use_sl', False)
        if not use_sl:
            set_nested_value(fixed_config, 'stop_loss.use_sl', True)
            changes.append(f"Fixed: Enabled use_sl=true for SL mode={sl_mode}")
    
    # Take profit
    tp_mode = get_nested_value(fixed_config, 'take_profit.mode', '')
    if tp_mode:
        use_tp = get_nested_value(fixed_config, 'take_profit.use_tp', False)
        if not use_tp:
            set_nested_value(fixed_config, 'take_profit.use_tp', True)
            changes.append(f"Fixed: Enabled use_tp=true for TP mode={tp_mode}")
    
    # 6. Fix time stop dependencies
    time_stop_enabled = get_nested_value(fixed_config, 'time_stop.enabled', False)
    if not time_stop_enabled:
        # Check for time-stop dependent settings
        time_stop_bars = get_nested_value(fixed_config, 'time_stop.bars', 0)
        time_stop_eod = get_nested_value(fixed_config, 'time_stop.exit_at_end_of_day', False)
        time_stop_eow = get_nested_value(fixed_config, 'time_stop.exit_at_end_of_week', False)
        
        if time_stop_bars > 0 or time_stop_eod or time_stop_eow:
            # Enable time stop
            set_nested_value(fixed_config, 'time_stop.enabled', True)
            changes.append("Fixed: Enabled time_stop.enabled=true for time-stop dependent settings")
    
    # Create fixed case data
    fixed_case_data = case_data.copy()
    fixed_case_data['config'] = fixed_config
    
    # Add fix notes
    if '_fix_notes' not in fixed_case_data:
        fixed_case_data['_fix_notes'] = []
    fixed_case_data['_fix_notes'].extend(changes)
    fixed_case_data['_original_hash'] = calculate_config_hash(config)
    fixed_case_data['_fixed_hash'] = calculate_config_hash(fixed_config)
    
    return fixed_case_data, changes

def main():
    suite_root = Path(__file__).parent
    cases_dir = suite_root / 'cases'
    manifests_dir = suite_root / 'manifests'
    
    # Create backup of original cases
    backup_dir = suite_root / 'cases_backup_original'
    if not backup_dir.exists():
        backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created backup directory: {backup_dir}")
    
    # Read manifest
    manifest_path = manifests_dir / 'cases_manifest_all.csv'
    with open(manifest_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        original_cases = list(reader)
    
    print(f"Processing {len(original_cases)} cases...")
    
    fixed_cases = []
    all_changes = []
    cases_with_changes = 0
    
    # Create fixed cases directory
    fixed_cases_dir = suite_root / 'cases_fixed'
    if not fixed_cases_dir.exists():
        fixed_cases_dir.mkdir(parents=True, exist_ok=True)
    
    for case in original_cases:
        case_id = case['case_id']
        case_path = cases_dir / f"{case_id}.json"
        
        if not case_path.exists():
            print(f"Warning: Case file not found: {case_path}")
            continue
        
        # Backup original
        backup_path = backup_dir / f"{case_id}.json"
        if not backup_path.exists():
            shutil.copy2(case_path, backup_path)
        
        # Load and fix case
        with open(case_path, 'r', encoding='utf-8') as f:
            case_data = json.load(f)
        
        fixed_case_data, changes = fix_case_dependencies(case_data, case_id)
        
        if changes:
            cases_with_changes += 1
            print(f"\n{case_id}:")
            for change in changes:
                print(f"  - {change}")
            all_changes.extend([(case_id, change) for change in changes])
            
            # Save fixed case
            fixed_case_path = fixed_cases_dir / f"{case_id}.json"
            with open(fixed_case_path, 'w', encoding='utf-8') as f:
                json.dump(fixed_case_data, f, indent=2)
            
            # Update case info for manifest
            fixed_case = case.copy()
            fixed_case['case_json'] = f"cases_fixed/{case_id}.json"
            fixed_case['notes'] = f"{case.get('notes', '')} | dependency_fixes_applied"
            
            # Recalculate hash
            config_hash = calculate_config_hash(fixed_case_data['config'])
            fixed_case['canonical_config_hash'] = config_hash
            
            fixed_cases.append(fixed_case)
        else:
            # No changes needed
            fixed_cases.append(case)
    
    print("\n" + "=" * 80)
    print(f"Summary:")
    print(f"  Total cases processed: {len(original_cases)}")
    print(f"  Cases with fixes applied: {cases_with_changes}")
    print(f"  Total fixes applied: {len(all_changes)}")
    
    # Generate fixed manifest
    if fixed_cases:
        # Sort by run_order
        fixed_cases.sort(key=lambda x: int(x['run_order']))
        
        # Write fixed manifest
        fixed_manifest_path = manifests_dir / 'cases_manifest_all_fixed.csv'
        fieldnames = original_cases[0].keys() if original_cases else []
        
        with open(fixed_manifest_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(fixed_cases)
        
        print(f"\nFixed manifest saved to: {fixed_manifest_path}")
        
        # Also create package-specific manifests
        for package in ['core', 'boundary', 'pairwise']:
            package_cases = [c for c in fixed_cases if c['pack'] == package]
            if package_cases:
                package_path = manifests_dir / f'cases_manifest_{package}_fixed.csv'
                with open(package_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(package_cases)
                print(f"  {package} manifest: {len(package_cases)} cases")
    
    # Generate fix report
    report_path = suite_root / 'dependency_fixes_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Dependency Fixes Report\n\n")
        f.write(f"**Total cases processed:** {len(original_cases)}\n")
        f.write(f"**Cases with fixes applied:** {cases_with_changes}\n")
        f.write(f"**Total fixes applied:** {len(all_changes)}\n\n")
        
        f.write("## Fix Summary by Case\n\n")
        for case in original_cases:
            case_id = case['case_id']
            case_changes = [change for cid, change in all_changes if cid == case_id]
            if case_changes:
                f.write(f"### {case_id}\n")
                for change in case_changes:
                    f.write(f"- {change}\n")
                f.write("\n")
        
        f.write("## Fix Types Summary\n\n")
        # Group changes by type
        change_types = {}
        for case_id, change in all_changes:
            # Extract change type (first few words before :)
            change_type = change.split(':')[0] if ':' in change else change.split()[0]
            if change_type not in change_types:
                change_types[change_type] = []
            change_types[change_type].append(case_id)
        
        for change_type, case_list in sorted(change_types.items()):
            f.write(f"### {change_type}\n")
            f.write(f"**Count:** {len(case_list)}\n")
            f.write("**Cases:** " + ", ".join(case_list) + "\n\n")
        
        f.write("## Next Steps\n\n")
        f.write("1. Review the fixed cases in `cases_fixed/` directory\n")
        f.write("2. Compare with original cases in `cases_backup_original/`\n")
        f.write("3. Run the optimization script again on fixed cases\n")
        f.write("4. Update TV manual inputs if needed\n")
    
    print(f"\nDetailed report saved to: {report_path}")
    print(f"\nNext steps:")
    print("1. Review fixed cases in 'cases_fixed/' directory")
    print("2. Compare with originals in 'cases_backup_original/'")
    print("3. Consider running optimization script on fixed cases")
    print("4. Update TV manual inputs accordingly")

if __name__ == '__main__':
    main()