import csv

csv_file = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\05_PARITY\MTC_V2_PARITY_CASES.csv"

# New columns to add
new_columns = [
    "exit_on_filter_block",
    "use_time_stop",
    "time_stop_bars",
    "time_stop_condition",
    "use_eod_exit",
    "use_eow_exit",
    "use_daily_loss_limit",
    "daily_loss_limit_pct",
    "use_max_trades_day",
    "max_trades_per_day",
    "use_max_drawdown_guard",
    "max_drawdown_pct",
    "use_consec_loss_guard",
    "max_consec_losses",
    "use_equity_curve_guard",
    "equity_curve_ma_len",
    "use_confirm_transform",
    "confirm_bars",
    "confirm_close_crosses",
    "use_candle_pattern_gate",
    "use_level_proximity_gate",
    "level_proximity_threshold_pct",
    "exit_on_candle_pattern_block",
    "exit_on_level_prox_block",
    "require_raw_still_true",
    "refresh_on_new_raw",
    "use_level_retest",
    "retest_timeout_bars",
    "retest_buffer_pct"
]

default_values = {
    "exit_on_filter_block": "False",
    "use_time_stop": "False",
    "time_stop_bars": "10",
    "time_stop_condition": "Always",
    "use_eod_exit": "False",
    "use_eow_exit": "False",
    "use_daily_loss_limit": "False",
    "daily_loss_limit_pct": "2.0",
    "use_max_trades_day": "False",
    "max_trades_per_day": "3",
    "use_max_drawdown_guard": "False",
    "max_drawdown_pct": "10.0",
    "use_consec_loss_guard": "False",
    "max_consec_losses": "3",
    "use_equity_curve_guard": "False",
    "equity_curve_ma_len": "20",
    "use_confirm_transform": "False",
    "confirm_bars": "1",
    "confirm_close_crosses": "True",
    "use_candle_pattern_gate": "False",
    "use_level_proximity_gate": "False",
    "level_proximity_threshold_pct": "0.5",
    "exit_on_candle_pattern_block": "False",
    "exit_on_level_prox_block": "False",
    "require_raw_still_true": "False",
    "refresh_on_new_raw": "False",
    "use_level_retest": "False",
    "retest_timeout_bars": "50",
    "retest_buffer_pct": "0.1",
}

with open(csv_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

headers = rows[0]
for c in new_columns:
    if c not in headers:
        headers.append(c)

for i in range(1, len(rows)):
    if not rows[i] or len(rows[i]) == 0:
        continue
    while len(rows[i]) < len(headers):
        col_name = headers[len(rows[i])]
        rows[i].append(default_values.get(col_name, ""))

# Add new tests
def create_test(run_order, layer, pkg, case_id, preset, overrides, primary, expected):
    # start with a copy of AUTO_001
    base = rows[1].copy()
    row_dict = dict(zip(headers, base))
    row_dict["run_order"] = str(run_order)
    row_dict["layer"] = layer
    row_dict["case_package"] = pkg
    row_dict["case_id"] = case_id
    row_dict["status"] = "PENDING_RUN"
    row_dict["pine_preset_name"] = preset
    row_dict["primary_change"] = primary
    row_dict["expected_trade_behavior"] = expected
    row_dict["llm_auto_status"] = ""
    row_dict["llm_last_run_utc"] = ""
    row_dict["llm_agent"] = ""
    row_dict["pine_trades"] = ""
    row_dict["pine_win_rate_pct"] = ""
    row_dict["pine_net_pnl_pct"] = ""
    row_dict["pine_max_dd_pct"] = ""
    row_dict["python_trades"] = ""
    row_dict["python_win_rate_pct"] = ""
    row_dict["python_net_pnl_pct"] = ""
    row_dict["python_max_dd_pct"] = ""
    row_dict["parity_verdict"] = ""
    row_dict["notes"] = ""
    row_dict["artifacts"] = ""
    
    for k, v in overrides.items():
        row_dict[k] = str(v)
    
    return [row_dict[h] for h in headers]

new_rows = []
ro = 47
# AUTO_034: Filter block exit
new_rows.append(create_test(ro, "L14", "EXIT_FILTER_BLOCK", "AUTO_034", "auto_034_filter_block", {
    "use_ma_filter": "True", "ma_type": "EMA", "ma_length": "50", "exit_on_filter_block": "True"
}, "Filter block exit on", "Exits early when MA invalidates direction"))
ro += 1

# AUTO_035: Time Stop
new_rows.append(create_test(ro, "L15", "TIME_EXITS", "AUTO_035", "auto_035_time_stop", {
    "use_time_stop": "True", "time_stop_bars": "12", "time_stop_condition": "Always"
}, "Time stop (12 bars)", "Cuts trade directly at 12th bar"))
ro += 1

# AUTO_036: EOD Exit
new_rows.append(create_test(ro, "L15", "TIME_EXITS", "AUTO_036", "auto_036_eod", {
    "use_eod_exit": "True"
}, "EOD exit on", "No trade holds overnight"))
ro += 1

# AUTO_037: EOW Exit
new_rows.append(create_test(ro, "L15", "TIME_EXITS", "AUTO_037", "auto_037_eow", {
    "use_eow_exit": "True"
}, "EOW exit on", "Closes open trades before weekend"))
ro += 1

# AUTO_038: Daily Loss Limit
new_rows.append(create_test(ro, "L16", "GUARDS", "AUTO_038", "auto_038_daily_loss", {
    "use_daily_loss_limit": "True", "daily_loss_limit_pct": "1.0", "sl_pct": "1.5"
}, "Daily Loss Limit 1%", "Stops trading for the day if drawdown > 1%"))
ro += 1

# AUTO_039: Max Trades/Day
new_rows.append(create_test(ro, "L16", "GUARDS", "AUTO_039", "auto_039_max_trades", {
    "use_max_trades_day": "True", "max_trades_per_day": "1"
}, "Max Trades = 1", "Only 1 trade permitted per timezone day"))
ro += 1

# AUTO_040: Max DD Guard
new_rows.append(create_test(ro, "L16", "GUARDS", "AUTO_040", "auto_040_max_dd", {
    "use_max_drawdown_guard": "True", "max_drawdown_pct": "2.0"
}, "Max Global DD 2%", "Permanently halts trading if from peak we drop 2%"))
ro += 1

# AUTO_041: Consec Loss
new_rows.append(create_test(ro, "L16", "GUARDS", "AUTO_041", "auto_041_consec_loss", {
    "use_consec_loss_guard": "True", "max_consec_losses": "2"
}, "Max consec loss 2", "Blocks entry after 2 losses until win (if ever)"))
ro += 1

# AUTO_042: Equity Curve
new_rows.append(create_test(ro, "L16", "GUARDS", "AUTO_042", "auto_042_equity_curve", {
    "use_equity_curve_guard": "True", "equity_curve_ma_len": "5"
}, "Eq Curve Guard", "Trades only when equity > MA(5)"))
ro += 1

# AUTO_043: L17 Regime/Flip
new_rows.append(create_test(ro, "L17", "POSITION_MGR", "AUTO_043", "auto_043_regime", {
    "regime_lock": "True", "allow_flip": "True", "tp_mode": "Percent", "tp_percent": "0.5"
}, "Regime lock + flip + tp", "Regime blocks immediate reentry same dir, flip works opposite if signal reverses"))
ro += 1

# AUTO_044: L18 Confirm
new_rows.append(create_test(ro, "L18", "CONFIRM", "AUTO_044", "auto_044_confirm", {
    "use_confirm_transform": "True", "confirm_bars": "2"
}, "Confirm 2 bars", "Signal needs 2 consecutive bars of same dir to trigger"))
ro += 1

# AUTO_045: L22 Candle Pattern Gate
new_rows.append(create_test(ro, "L22", "GATES", "AUTO_045", "auto_045_candle_pattern", {
    "use_candle_pattern_gate": "True"
}, "Candle Pattern Gate ON", "Only entries on valid engulfing, hammer or shooting star"))
ro += 1

# AUTO_046: L20 Level Proximity Gate
new_rows.append(create_test(ro, "L20", "GATES", "AUTO_046", "auto_046_level_proximity", {
    "use_level_proximity_gate": "True", "level_proximity_threshold_pct": "1.0"
}, "Level Proximity Gate ON", "Only enters if price near 1% of recent swing highs/lows"))
ro += 1

# AUTO_047: L18b Advanced Confirm (Req Raw)
new_rows.append(create_test(ro, "L18", "CONFIRM", "AUTO_047", "auto_047_confirm_req_raw", {
    "use_confirm_transform": "True", "confirm_bars": "2", "require_raw_still_true": "True"
}, "Confirm 2 req raw", "Requires raw to be active exactly on the confirm bar"))
ro += 1

# AUTO_048: L18b Advanced Confirm (Refresh New Raw)
new_rows.append(create_test(ro, "L18", "CONFIRM", "AUTO_048", "auto_048_confirm_refresh", {
    "use_confirm_transform": "True", "confirm_bars": "2", "refresh_on_new_raw": "True"
}, "Confirm 2 refresh", "Refreshes the counter if a brand new raw pulse arrives before confirmation"))
ro += 1

# AUTO_049: L21 Level Retest
new_rows.append(create_test(ro, "L21", "RETEST", "AUTO_049", "auto_049_level_retest", {
    "use_level_retest": "True", "retest_timeout_bars": "10", "retest_buffer_pct": "1.0"
}, "Retest ON", "Level retest transforms signal on pullback"))
ro += 1

rows.extend(new_rows)

with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Done updating CSV.")
