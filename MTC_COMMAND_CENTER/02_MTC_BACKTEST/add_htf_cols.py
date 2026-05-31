import csv, io
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
csv_path = REPO_ROOT / 'MTC_COMMAND_CENTER/01_MTC_PROJECT/05_PARITY/MTC_V2_PARITY_CASES.csv'

with open(csv_path, encoding='utf-8', newline='') as f:
    content = f.read()

reader = csv.DictReader(io.StringIO(content))
rows = list(reader)
old_fieldnames = list(reader.fieldnames)

# New columns to add (before 'category')
new_cols = [
    'mcginley_use_higher_timeframe',
    'mcginley_htf_timeframe',
    'adx_use_higher_timeframe',
    'adx_htf_timeframe',
    'chop_use_higher_timeframe',
    'chop_htf_timeframe',
]

# Find insert position: before 'category'
insert_before = 'category'
idx = old_fieldnames.index(insert_before)
new_fieldnames = old_fieldnames[:idx] + new_cols + old_fieldnames[idx:]

# Template row (use AUTO_001 defaults)
template = dict(rows[0])  # AUTO_001 row

# Get last run_order
last_run_order = 0
for r in rows:
    try:
        v = int(r.get('run_order', 0) or 0)
        if v > last_run_order:
            last_run_order = v
    except (ValueError, TypeError):
        pass

def make_base(case_id, run_order, case_package, primary_change, description, row_num):
    r = {k: '' for k in new_fieldnames}
    # Copy template defaults for standard fields
    for k in [
        'layer', 'symbol', 'timeframe', 'bars', 'data_source',
        'enable_long', 'enable_short', 'allow_flip', 'regime_lock', 'max_entries', 'cooldown_bars',
        'signal_mode', 'st_atr_len', 'st_factor', 'st_use_wicks', 'st_use_ha',
        'equity_source', 'use_notional_assert',
        'use_ma_filter', 'ma_type', 'ma_length', 'use_ma_slope_filter', 'ma_slope_len', 'ma_slope_min_pct',
        'risk_per_long_pct', 'risk_per_short_pct', 'fallback_size_pct', 'max_leverage_cap',
        'sl_mode', 'sl_atr_len', 'sl_atr_mult',
        'use_volume_filter', 'vol_sma_length', 'vol_sma_mult',
        'use_adx_filter', 'adx_length', 'adx_threshold',
        'use_chop_filter', 'chop_length', 'chop_threshold',
        'use_atr_vol_floor', 'atr_vol_floor_fast_len', 'atr_vol_floor_baseline_len', 'atr_vol_floor_mult',
        'use_macd_regime_filter', 'use_macd_cross_filter', 'use_macd_hist_filter', 'macd_hist_mode',
        'use_macd_zero_dist_filter', 'macd_zero_dist_min', 'macd_fast_len', 'macd_slow_len', 'macd_sig_len',
        'macd_source', 'macd_htf_timeframe', 'use_macd_htf_bias',
        'use_sl', 'exit_on_ma_block', 'exit_on_ma_slope_block', 'exit_on_mcginley_block',
        'exit_on_htf_trend_block', 'exit_on_vol_block', 'exit_on_atr_vol_block', 'exit_on_range_block',
        'use_time_stop', 'time_stop_bars', 'time_stop_condition', 'time_stop_eod', 'time_stop_eow',
        'use_daily_loss_limit', 'max_daily_loss_pct', 'use_max_trades_per_day', 'max_trades_per_day',
        'use_max_drawdown_guard', 'max_drawdown_pct', 'use_consecutive_loss_halt', 'max_consecutive_losses',
        'use_equity_curve_filter', 'equity_ma_length', 'use_mae_guard', 'max_mae_pct',
        'use_guard_recovery', 'guard_recovery_mode', 'guard_recovery_bars', 'guard_recovery_signals',
        'use_confirm_transform', 'confirm_bars', 'confirm_close_crosses',
        'use_candle_pattern_gate', 'use_level_proximity_gate', 'level_proximity_threshold_pct',
        'exit_on_candle_pattern_block', 'exit_on_level_prox_block',
        'require_raw_still_true', 'refresh_on_new_raw',
        'use_level_retest', 'retest_timeout_bars', 'retest_buffer_pct',
        'use_break_even', 'be_trigger_r', 'be_buffer_r',
        'use_trailing', 'trail_start_r', 'trail_distance_atr_mult',
        'tp1_r_multiple', 'tp1_close_pct', 'tp2_r_multiple', 'tp_percent',
        'exit_on_opposite_signal', 'level_proximity_lookback',
        'use_htf_trend_filter', 'htf_trend_timeframe', 'htf_trend_ma_type', 'htf_trend_ma_len', 'htf_trend_buffer_pct',
        'use_ma_mtf', 'ma_htf_timeframe',
        'use_momentum_filter', 'momentum_mode', 'momentum_atr_len', 'momentum_atr_mult', 'momentum_roc_min_pct',
        'use_session_filter', 'session_name', 'session_custom_string',
    ]:
        r[k] = template.get(k, '')
    r['layer'] = 'L12'
    r['pine_preset_name'] = 'AUTO_050'
    r['run_order'] = str(run_order)
    r['case_package'] = case_package
    r['case_id'] = case_id
    r['case_type'] = 'AUTO_ACTIVE'
    r['status'] = 'PENDING'
    r['depends_on'] = ''
    r['primary_change'] = primary_change
    r['expected_trade_behavior'] = 'Trades with HTF-sourced filter'
    r['llm_agent'] = 'Claude'
    r['category'] = 'L12'
    r['case_status'] = 'PENDING'
    r['expected_result'] = 'PASS'
    r['tracker_agent'] = 'Claude'
    r['row'] = str(row_num)
    r['description'] = description
    # HTF defaults (all off)
    r['mcginley_use_higher_timeframe'] = 'False'
    r['mcginley_htf_timeframe'] = '240'
    r['adx_use_higher_timeframe'] = 'False'
    r['adx_htf_timeframe'] = '240'
    r['chop_use_higher_timeframe'] = 'False'
    r['chop_htf_timeframe'] = '240'
    return r

# AUTO_058: McGinley HTF
r058 = make_base('AUTO_058', last_run_order + 1, 'auto_058_mcginley_htf',
                 'McGinley filter on 240m HTF close',
                 'McGinley HTF: mcginley_use_higher_timeframe=True, HTF TF=240',
                 105)
r058['use_mcginley_filter'] = 'True'
r058['mcginley_length'] = '50'
r058['mcginley_use_higher_timeframe'] = 'True'
r058['mcginley_htf_timeframe'] = '240'
r058['use_adx_filter'] = 'False'
r058['use_chop_filter'] = 'False'

# AUTO_059: ADX HTF
r059 = make_base('AUTO_059', last_run_order + 2, 'auto_059_adx_htf',
                 'ADX filter on 240m HTF h/l/c',
                 'ADX HTF: adx_use_higher_timeframe=True, HTF TF=240',
                 106)
r059['use_mcginley_filter'] = 'False'
r059['use_adx_filter'] = 'True'
r059['adx_length'] = '14'
r059['adx_threshold'] = '25.0'
r059['adx_use_higher_timeframe'] = 'True'
r059['adx_htf_timeframe'] = '240'
r059['use_chop_filter'] = 'False'

# AUTO_060: Chop HTF
r060 = make_base('AUTO_060', last_run_order + 3, 'auto_060_chop_htf',
                 'Chop filter on 240m HTF h/l/c',
                 'Chop HTF: chop_use_higher_timeframe=True, HTF TF=240',
                 107)
r060['use_mcginley_filter'] = 'False'
r060['use_adx_filter'] = 'False'
r060['use_chop_filter'] = 'True'
r060['chop_length'] = '14'
r060['chop_threshold'] = '61.8'
r060['chop_use_higher_timeframe'] = 'True'
r060['chop_htf_timeframe'] = '240'

# Patch existing rows with empty values for new columns
for r in rows:
    for c in new_cols:
        if c not in r:
            r[c] = ''

# Write new CSV
out = io.StringIO()
writer = csv.DictWriter(out, fieldnames=new_fieldnames, lineterminator='\n')
writer.writeheader()
writer.writerows(rows)
writer.writerows([r058, r059, r060])

with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    f.write(out.getvalue())

print(f'Written. Total rows: {len(rows) + 3}, Total cols: {len(new_fieldnames)}')
print(f'Last run_order was: {last_run_order}, new rows: {last_run_order+1}, {last_run_order+2}, {last_run_order+3}')
