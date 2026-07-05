# Parity Summary (case_103 - case_162)

- Generated: 2026-04-14 14:40:47 UTC
- Present cases: 58
- Missing exports: case_160, case_161
- Settings clean: 17/58
- Target change observed: 35/58
- Effect observed: 54/58
- TW=PineTS strict pass: 33/58
- TW=Python strict pass: 27/58
- PineTS=Python strict pass: 50/58
- Overall classification pass (strict+soft): 50/58

## case_103
- Setting: `use_candle_pattern_gate` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `-9` | net pnl pct delta `-1.547559` | pf delta `-0.006745`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=7 | PineTS=7 | Python=7
- Report: `reports\manual_tw_futures_case_103.json`

## case_104
- Setting: `use_level_proximity_gate` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 2
- Effect: `YES` | trade delta `+9` | net pnl pct delta `+26.702101` | pf delta `+1.312365`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=16 | PineTS=16 | Python=16
- Report: `reports\manual_tw_futures_case_104.json`

## case_105
- Setting: `level_proximity_threshold_pct` | expected `0.25` | prev `2` | actual `3`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 2
- Effect: `YES` | trade delta `+44` | net pnl pct delta `-13.574499` | pf delta `-2.104827`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=60 | PineTS=60 | Python=60
- Report: `reports\manual_tw_futures_case_105.json`

## case_106
- Setting: `level_proximity_lookback` | expected `30` | prev `50` | actual `30`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 2
- Effect: `YES` | trade delta `-36` | net pnl pct delta `+19.171402` | pf delta `+1.566458`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=24 | PineTS=24 | Python=24
- Report: `reports\manual_tw_futures_case_106.json`

## case_107
- Setting: `use_time_stop` | expected `True` | prev `False` | actual `True`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `YES` | mismatches: 0
- Effect: `YES` | trade delta `+122` | net pnl pct delta `-42.274282` | pf delta `-2.094518`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=146 | PineTS=146 | Python=146
- Report: `reports\manual_tw_futures_case_107.json`

## case_108
- Setting: `time_stop_bars` | expected `20` | prev `50` | actual `20`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `YES` | mismatches: 0
- Effect: `YES` | trade delta `+0` | net pnl pct delta `-2.446303` | pf delta `-0.246571`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=146 | PineTS=146 | Python=146
- Report: `reports\manual_tw_futures_case_108.json`

## case_109
- Setting: `time_stop_condition` | expected `Profit Only` | prev `Always` | actual `Profit Only`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `-15` | net pnl pct delta `-1.388424` | pf delta `+0.380221`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=131 | PineTS=131 | Python=131
- Report: `reports\manual_tw_futures_case_109.json`

## case_110
- Setting: `time_stop_eod` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `+11` | net pnl pct delta `-11.526319` | pf delta `-0.226518`
- Parity: `FAIL` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`FAIL`
- Trades: TW=142 | PineTS=142 | Python=142
- Report: `reports\manual_tw_futures_case_110.json`

## case_111
- Setting: `time_stop_eow` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `-6` | net pnl pct delta `+16.977986` | pf delta `+0.276476`
- Parity: `FAIL` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`FAIL`
- Trades: TW=136 | PineTS=136 | Python=136
- Report: `reports\manual_tw_futures_case_111.json`

## case_112
- Setting: `use_daily_loss_limit` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `-8` | net pnl pct delta `+1.362439` | pf delta `+0.014050`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=128 | PineTS=128 | Python=128
- Report: `reports\manual_tw_futures_case_112.json`

## case_113
- Setting: `max_daily_loss_pct` | expected `1` | prev `2` | actual `1`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `-20` | net pnl pct delta `+2.137643` | pf delta `+0.020973`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=108 | PineTS=108 | Python=108
- Report: `reports\manual_tw_futures_case_113.json`

## case_114
- Setting: `use_max_trades_per_day` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `+23` | net pnl pct delta `-2.244669` | pf delta `-0.021856`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=131 | PineTS=131 | Python=131
- Report: `reports\manual_tw_futures_case_114.json`

## case_115
- Setting: `max_trades_per_day` | expected `2` | prev `3` | actual `1`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 2
- Effect: `YES` | trade delta `-48` | net pnl pct delta `-7.909126` | pf delta `-0.104896`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=83 | PineTS=83 | Python=83
- Report: `reports\manual_tw_futures_case_115.json`

## case_116
- Setting: `use_max_drawdown_guard` | expected `True` | prev `False` | actual `True`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `YES` | mismatches: 0
- Effect: `YES` | trade delta `+63` | net pnl pct delta `+2.620016` | pf delta `-0.190845`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=146 | PineTS=146 | Python=146
- Report: `reports\manual_tw_futures_case_116.json`

## case_117
- Setting: `max_drawdown_pct` | expected `5` | prev `10` | actual `5`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `-132` | net pnl pct delta `+4.163790` | pf delta `+0.110821`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=14 | PineTS=14 | Python=14
- Report: `reports\manual_tw_futures_case_117.json`

## case_118
- Setting: `use_consecutive_loss_halt` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `-7` | net pnl pct delta `+0.356953` | pf delta `-0.063870`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=7 | PineTS=7 | Python=7
- Report: `reports\manual_tw_futures_case_118.json`

## case_119
- Setting: `max_consecutive_losses` | expected `2` | prev `3` | actual `2`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `-4` | net pnl pct delta `+1.724628` | pf delta `+0.271547`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=3 | PineTS=3 | Python=3
- Report: `reports\manual_tw_futures_case_119.json`

## case_120
- Setting: `use_equity_curve_filter` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `+30` | net pnl pct delta `+4.668312` | pf delta `+0.193707`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=33 | PineTS=33 | Python=33
- Report: `reports\manual_tw_futures_case_120.json`

## case_121
- Setting: `equity_ma_length` | expected `10` | prev `20` | actual `10`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `-20` | net pnl pct delta `-5.656721` | pf delta `-0.309210`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=13 | PineTS=13 | Python=13
- Report: `reports\manual_tw_futures_case_121.json`

## case_122
- Setting: `use_mae_guard` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `-8` | net pnl pct delta `+1.510823` | pf delta `+0.225259`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=5 | PineTS=5 | Python=5
- Report: `reports\manual_tw_futures_case_122.json`

## case_123
- Setting: `max_mae_pct` | expected `1` | prev `2` | actual `1`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `-3` | net pnl pct delta `+0.098368` | pf delta `+0.635326`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=2 | PineTS=2 | Python=2
- Report: `reports\manual_tw_futures_case_123.json`

## case_124
- Setting: `use_guard_recovery` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 2
- Effect: `YES` | trade delta `+31` | net pnl pct delta `+4.047530` | pf delta `-0.551375`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=33 | PineTS=33 | Python=33
- Report: `reports\manual_tw_futures_case_124.json`

## case_125
- Setting: `guard_recovery_mode` | expected `Signals` | prev `Bars` | actual `Signals`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 2
- Effect: `NO` | trade delta `+0` | net pnl pct delta `+0.000000` | pf delta `+0.000000`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=33 | PineTS=33 | Python=33
- Report: `reports\manual_tw_futures_case_125.json`

## case_126
- Setting: `guard_recovery_bars` | expected `10` | prev `20` | actual `10`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `+98` | net pnl pct delta `-5.624573` | pf delta `-0.216464`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=131 | PineTS=131 | Python=131
- Report: `reports\manual_tw_futures_case_126.json`

## case_127
- Setting: `guard_recovery_signals` | expected `1` | prev `2` | actual `1`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 2
- Effect: `NO` | trade delta `+0` | net pnl pct delta `+0.000000` | pf delta `+0.000000`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=131 | PineTS=131 | Python=131
- Report: `reports\manual_tw_futures_case_127.json`

## case_128
- Setting: `use_trade_cooldown` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `-41` | net pnl pct delta `-14.013388` | pf delta `-0.180898`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=90 | PineTS=90 | Python=90
- Report: `reports\manual_tw_futures_case_128.json`

## case_129
- Setting: `cooldown_bars_after_exit` | expected `3` | prev `5` | actual `3`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `+4` | net pnl pct delta `-3.637544` | pf delta `-0.039181`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=94 | PineTS=94 | Python=94
- Report: `reports\manual_tw_futures_case_129.json`

## case_130
- Setting: `use_confirm_transform` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `+37` | net pnl pct delta `+17.650932` | pf delta `+0.220079`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=131 | PineTS=131 | Python=131
- Report: `reports\manual_tw_futures_case_130.json`

## case_131
- Setting: `confirm_bars` | expected `2` | prev `1` | actual `2`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `-131` | net pnl pct delta `+0.935148` | pf delta `-0.991645`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=0 | PineTS=0 | Python=0
- Report: `reports\manual_tw_futures_case_131.json`

## case_132
- Setting: `confirm_close_crosses` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `+131` | net pnl pct delta `-0.935148` | pf delta `+0.991645`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=131 | PineTS=131 | Python=131
- Report: `reports\manual_tw_futures_case_132.json`

## case_133
- Setting: `require_raw_still_true` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `NO` | trade delta `+0` | net pnl pct delta `+0.000000` | pf delta `+0.000000`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=131 | PineTS=131 | Python=131
- Report: `reports\manual_tw_futures_case_133.json`

## case_134
- Setting: `refresh_on_new_raw` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 1
- Effect: `YES` | trade delta `-131` | net pnl pct delta `+0.935148` | pf delta `-0.991645`
- Parity: `FAIL` | TW/PineTS=`PASS` | TW/Python=`FAIL` | PineTS/Python=`FAIL`
- Trades: TW=0 | PineTS=0 | Python=131
- Report: `reports\manual_tw_futures_case_134.json`

## case_135
- Setting: `use_level_retest` | expected `True` | prev `False` | actual `True`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 2
- Effect: `YES` | trade delta `+1` | net pnl pct delta `-0.459671` | pf delta `+0.000000`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=1 | PineTS=1 | Python=1
- Report: `reports\manual_tw_futures_case_135.json`

## case_136
- Setting: `retest_timeout_bars` | expected `20` | prev `50` | actual `20`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 2
- Effect: `NO` | trade delta `+0` | net pnl pct delta `+0.000000` | pf delta `+0.000000`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=1 | PineTS=1 | Python=1
- Report: `reports\manual_tw_futures_case_136.json`

## case_137
- Setting: `retest_buffer_pct` | expected `0.2` | prev `0.1` | actual `0.2`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `YES` | mismatches: 3
- Effect: `YES` | trade delta `+130` | net pnl pct delta `-0.475477` | pf delta `+0.991645`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=131 | PineTS=131 | Python=131
- Report: `reports\manual_tw_futures_case_137.json`

## case_138
- Setting: `pair_sl_atr_be` | expected `None` | prev `None` | actual `None`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `NO` | mismatches: 0
- Effect: `YES` | trade delta `-6` | net pnl pct delta `-17.138475` | pf delta `-0.197980`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=125 | PineTS=125 | Python=125
- Report: `reports\manual_tw_futures_case_138.json`

## case_139
- Setting: `pair_sl_atr_trail` | expected `None` | prev `None` | actual `None`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `NO` | mismatches: 0
- Effect: `YES` | trade delta `+9` | net pnl pct delta `+8.095397` | pf delta `+0.109340`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=134 | PineTS=134 | Python=134
- Report: `reports\manual_tw_futures_case_139.json`

## case_140
- Setting: `pair_sl_atr_tp_atr` | expected `None` | prev `None` | actual `None`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `NO` | mismatches: 0
- Effect: `YES` | trade delta `+0` | net pnl pct delta `+2.892662` | pf delta `+0.026553`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=134 | PineTS=134 | Python=134
- Report: `reports\manual_tw_futures_case_140.json`

## case_141
- Setting: `pair_sl_atr_tp_r` | expected `None` | prev `None` | actual `None`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `NO` | mismatches: 0
- Effect: `YES` | trade delta `+0` | net pnl pct delta `+1.786183` | pf delta `+0.020636`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=134 | PineTS=134 | Python=134
- Report: `reports\manual_tw_futures_case_141.json`

## case_142
- Setting: `pair_sl_atr_tp_multi` | expected `None` | prev `None` | actual `None`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `NO` | mismatches: 0
- Effect: `YES` | trade delta `+27` | net pnl pct delta `-0.042160` | pf delta `+0.001147`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=161 | PineTS=161 | Python=161
- Report: `reports\manual_tw_futures_case_142.json`

## case_143
- Setting: `pair_sl_percent_tp_percent` | expected `None` | prev `None` | actual `None`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `NO` | mismatches: 0
- Effect: `YES` | trade delta `-19` | net pnl pct delta `-23.046052` | pf delta `-0.188179`
- Parity: `SOFT_PASS` | TW/PineTS=`FAIL` | TW/Python=`FAIL` | PineTS/Python=`PASS`
- Trades: TW=142 | PineTS=142 | Python=142
- Report: `reports\manual_tw_futures_case_143.json`

## case_144
- Setting: `pair_ma_exit` | expected `None` | prev `None` | actual `None`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `NO` | mismatches: 0
- Effect: `YES` | trade delta `-46` | net pnl pct delta `+22.536090` | pf delta `-0.241682`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=96 | PineTS=96 | Python=96
- Report: `reports\manual_tw_futures_case_144.json`

## case_145
- Setting: `pair_ma_slope_exit` | expected `None` | prev `None` | actual `None`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `NO` | mismatches: 1
- Effect: `YES` | trade delta `-24` | net pnl pct delta `+1.818366` | pf delta `+0.038446`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=72 | PineTS=72 | Python=72
- Report: `reports\manual_tw_futures_case_145.json`

## case_146
- Setting: `pair_mcginley_exit` | expected `None` | prev `None` | actual `None`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `NO` | mismatches: 1
- Effect: `YES` | trade delta `+6` | net pnl pct delta `-0.191815` | pf delta `+0.063187`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=78 | PineTS=78 | Python=78
- Report: `reports\manual_tw_futures_case_146.json`

## case_147
- Setting: `pair_htf_trend_exit` | expected `None` | prev `None` | actual `None`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `NO` | mismatches: 1
- Effect: `YES` | trade delta `+46` | net pnl pct delta `-1.676672` | pf delta `-0.051854`
- Parity: `FAIL` | TW/PineTS=`PASS` | TW/Python=`FAIL` | PineTS/Python=`FAIL`
- Trades: TW=124 | PineTS=124 | Python=126
- Report: `reports\manual_tw_futures_case_147.json`

## case_148
- Setting: `pair_volume_exit` | expected `None` | prev `None` | actual `None`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `NO` | mismatches: 1
- Effect: `YES` | trade delta `-1` | net pnl pct delta `+5.149511` | pf delta `+0.259315`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=123 | PineTS=123 | Python=123
- Report: `reports\manual_tw_futures_case_148.json`

## case_149
- Setting: `pair_atr_floor_exit` | expected `None` | prev `None` | actual `None`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `NO` | mismatches: 1
- Effect: `YES` | trade delta `+20` | net pnl pct delta `-4.785147` | pf delta `-0.115855`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=143 | PineTS=143 | Python=143
- Report: `reports\manual_tw_futures_case_149.json`

## case_150
- Setting: `pair_candle_exit` | expected `None` | prev `None` | actual `None`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `NO` | mismatches: 1
- Effect: `YES` | trade delta `-136` | net pnl pct delta `+5.589423` | pf delta `+0.896053`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=7 | PineTS=7 | Python=7
- Report: `reports\manual_tw_futures_case_150.json`

## case_151
- Setting: `pair_level_exit` | expected `None` | prev `None` | actual `None`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `NO` | mismatches: 2
- Effect: `YES` | trade delta `+56` | net pnl pct delta `-0.403360` | pf delta `-0.686414`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=63 | PineTS=63 | Python=63
- Report: `reports\manual_tw_futures_case_151.json`

## case_152
- Setting: `pair_confirm_require_raw` | expected `None` | prev `None` | actual `None`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `NO` | mismatches: 0
- Effect: `YES` | trade delta `+83` | net pnl pct delta `-5.873061` | pf delta `-0.228454`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=146 | PineTS=146 | Python=146
- Report: `reports\manual_tw_futures_case_152.json`

## case_153
- Setting: `pair_confirm_refresh` | expected `None` | prev `None` | actual `None`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `NO` | mismatches: 0
- Effect: `YES` | trade delta `-146` | net pnl pct delta `+6.224258` | pf delta `-0.695904`
- Parity: `FAIL` | TW/PineTS=`PASS` | TW/Python=`FAIL` | PineTS/Python=`FAIL`
- Trades: TW=0 | PineTS=0 | Python=146
- Report: `reports\manual_tw_futures_case_153.json`

## case_154
- Setting: `pair_level_retest_confirm` | expected `None` | prev `None` | actual `None`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `NO` | mismatches: 1
- Effect: `YES` | trade delta `+27` | net pnl pct delta `-0.925017` | pf delta `+0.529895`
- Parity: `FAIL` | TW/PineTS=`PASS` | TW/Python=`FAIL` | PineTS/Python=`FAIL`
- Trades: TW=27 | PineTS=27 | Python=44
- Report: `reports\manual_tw_futures_case_154.json`

## case_155
- Setting: `pair_macd_htf_regime` | expected `None` | prev `None` | actual `None`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `NO` | mismatches: 0
- Effect: `YES` | trade delta `+28` | net pnl pct delta `-1.138405` | pf delta `+0.193097`
- Parity: `FAIL` | TW/PineTS=`PASS` | TW/Python=`FAIL` | PineTS/Python=`FAIL`
- Trades: TW=55 | PineTS=55 | Python=76
- Report: `reports\manual_tw_futures_case_155.json`

## case_156
- Setting: `pair_macd_hist_zero` | expected `None` | prev `None` | actual `None`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `NO` | mismatches: 0
- Effect: `YES` | trade delta `+87` | net pnl pct delta `-3.733205` | pf delta `-0.012061`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=142 | PineTS=142 | Python=142
- Report: `reports\manual_tw_futures_case_156.json`

## case_157
- Setting: `pair_momentum_session` | expected `None` | prev `None` | actual `None`
- Settings check: `FAIL` | accepted mismatches: 1 | target changed: `NO` | mismatches: 1
- Effect: `YES` | trade delta `-82` | net pnl pct delta `+3.694031` | pf delta `+0.052645`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=60 | PineTS=60 | Python=60
- Report: `reports\manual_tw_futures_case_157.json`

## case_158
- Setting: `pair_trade_cooldown_max_trades` | expected `None` | prev `None` | actual `None`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `NO` | mismatches: 0
- Effect: `YES` | trade delta `+13` | net pnl pct delta `-1.335491` | pf delta `-0.089594`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=73 | PineTS=73 | Python=73
- Report: `reports\manual_tw_futures_case_158.json`

## case_159
- Setting: `pair_daily_loss_recovery` | expected `None` | prev `None` | actual `None`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `NO` | mismatches: 0
- Effect: `YES` | trade delta `+73` | net pnl pct delta `-2.786171` | pf delta `+0.021922`
- Parity: `STRICT_PASS` | TW/PineTS=`PASS` | TW/Python=`PASS` | PineTS/Python=`PASS`
- Trades: TW=146 | PineTS=146 | Python=146
- Report: `reports\manual_tw_futures_case_159.json`

## case_162
- Setting: `pair_ma_htf_htf_trend` | expected `None` | prev `None` | actual `None`
- Settings check: `PASS` | accepted mismatches: 1 | target changed: `NO` | mismatches: 0
- Effect: `YES` | trade delta `-50` | net pnl pct delta `+1.735633` | pf delta `-0.003572` | Compared against case_159 because case_160 and case_161 exports are missing locally.
- Parity: `FAIL` | TW/PineTS=`PASS` | TW/Python=`FAIL` | PineTS/Python=`FAIL`
- Trades: TW=96 | PineTS=96 | Python=94
- Report: `reports\manual_tw_futures_case_162.json`

## Missing Exports
- `case_160` not present locally
- `case_161` not present locally

## Retrospective
- accepted override: max_leverage_cap exported at 5 to suppress TradingView margin-call noise
- accepted inert mismatch: confirm_close_crosses=true while use_confirm_transform=false
