import pandas as pd

excel_path = 'parity_suite_350/CASE_SETUP_GUIDE_tagged_v6_conflict_candidates.xlsx'
df = pd.read_excel(excel_path, sheet_name='Retest Candidates')

print('=== ANALYSIS OF RETEST CANDIDATES SHEET ===')
print(f'Total rows: {len(df)}')
print()

# Show distribution of categories
print('=== CATEGORY DISTRIBUTION ===')
category_counts = df['category'].value_counts(dropna=False)
print(category_counts)
print()

# Show relationship between category and action_needed
print('=== ACTION_NEEDED BY CATEGORY ===')
for category in df['category'].unique():
    if pd.isna(category):
        continue
    cat_df = df[df['category'] == category]
    print(f'\nCategory: {category} ({len(cat_df)} cases)')
    action_counts = cat_df['action_needed'].value_counts(dropna=False)
    for action, count in action_counts.items():
        print(f'  {action}: {count}')
print()

# Show details about SKIP cases
print('=== DETAILED ANALYSIS OF SKIP CASES ===')
skip_cases = df[df['action_needed'].astype(str).str.contains('SKIP', case=False, na=False)]
print(f'Total SKIP cases: {len(skip_cases)}')

skip_types = skip_cases['action_needed'].value_counts()
print('\nBreakdown of SKIP types:')
for skip_type, count in skip_types.items():
    print(f'  {skip_type}: {count}')
    
    # Show sample cases for each skip type
    sample_cases = skip_cases[skip_cases['action_needed'] == skip_type].head(3)
    for _, row in sample_cases.iterrows():
        print(f'    - Case {row["case_id"]}: {row["primary_change"]} | {row["expected_trade_behavior"]}')
print()

# Show non-SKIP cases
print('=== NON-SKIP CASES (Requiring Action) ===')
non_skip = df[~df['action_needed'].astype(str).str.contains('SKIP', case=False, na=False)]
print(f'Total non-SKIP cases: {len(non_skip)}')

action_types = non_skip['action_needed'].value_counts()
print('\nBreakdown of action types:')
for action_type, count in action_types.items():
    print(f'  {action_type}: {count}')
    
    # Show what needs to be done
    sample_cases = non_skip[non_skip['action_needed'] == action_type].head(3)
    for _, row in sample_cases.iterrows():
        print(f'    - Case {row["case_id"]}: {row["primary_change"]}')
        if pd.notna(row.get('suggested_tv_value')):
            print(f'      Suggested TV value: {row["suggested_tv_value"]}')
print()

# Check parity status
print('=== PARITY STATUS FOR SKIP CASES ===')
print('Based on project context, SKIP cases fall into these groups:')
print('1. SKIP: Structurally no effect (18 cases) - Parameter changes that have no effect on trades')
print('2. SKIP: Expected behavior (14 cases) - Position sizing changes only (no parity impact)')
print('3. SKIP: Too few trades (9 cases) - Cases with only 2 TV trades (statistically insignificant)')
print()
print('These SKIP cases will NOT have parity verification because:')
print('- Structurally no effect: No trades change, so parity is automatically maintained')
print('- Expected behavior: Only position sizing changes, which Python already handles correctly')
print('- Too few trades: Not enough data for meaningful comparison')
print()
print('The 18 "Virtual Trade" SKIP cases mentioned in project files are DIFFERENT')
print('These are FP-08 (Guard Recovery Virtual Trade) features not yet implemented in Python')