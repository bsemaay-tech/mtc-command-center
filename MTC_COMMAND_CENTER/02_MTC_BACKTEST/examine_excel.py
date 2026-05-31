import pandas as pd
import sys

excel_path = 'parity_suite_350/CASE_SETUP_GUIDE_tagged_v6_conflict_candidates.xlsx'

try:
    xl = pd.ExcelFile(excel_path)
    print('Sheets:', xl.sheet_names)
    
    df = pd.read_excel(excel_path, sheet_name='Retest Candidates')
    print('Sheet loaded. Shape:', df.shape)
    
    print('\nColumn names:')
    for i, col in enumerate(df.columns):
        print(f'{i}: {col}')
    
    print('\nLooking for actions_needed column...')
    if 'actions_needed' in df.columns:
        print('Found actions_needed column at index:', df.columns.get_loc('actions_needed'))
        print('Sample values (first 30 rows):')
        print(df['actions_needed'].head(30).tolist())
        
        # Count different values
        print('\nValue counts:')
        print(df['actions_needed'].value_counts(dropna=False).head(20))
    else:
        print('actions_needed not found, checking column V (index 21)...')
        if len(df.columns) > 21:
            print('Column 21 name:', df.columns[21])
            print('Sample values (first 30 rows):')
            print(df.iloc[:30, 21].tolist())
            
            # Check if this column contains SKIP values
            col_name = df.columns[21]
            print(f'\nValue counts for {col_name}:')
            print(df[col_name].value_counts(dropna=False).head(20))
    
    # Also check for any column containing "SKIP"
    print('\n\nSearching for columns containing "SKIP" values...')
    for col in df.columns:
        if df[col].astype(str).str.contains('SKIP', case=False, na=False).any():
            skip_count = df[col].astype(str).str.contains('SKIP', case=False, na=False).sum()
            print(f'Column "{col}" contains {skip_count} SKIP entries')
            print(f'  Sample SKIP values: {df[df[col].astype(str).str.contains("SKIP", case=False, na=False)][col].head(5).tolist()}')
            
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()