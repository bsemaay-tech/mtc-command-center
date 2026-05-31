# MTC V2 - Input UI Order Specification

Kaynak dokuman: `MTC_V2_ARCHITECTURE.md`

Amaç: TradingView Pine Script input panelinin grup sirasini, alt-grup yerlesimini, input order'ini ve
parent/child active kurallarini tek kaynak olarak dondurmek.

Kapsam:
- Bu dokuman yalniz Pine input paneli icindir.
- Runtime architecture owner'ligini degistirmez.
- Yeni feature tasarlamaz.
- Mevcut config surface disina cikmaz.

---

# 1. Executive Summary

- TradingView input paneli pipeline'a yakin ama birebir runtime sirasi olmayan su ust seviye duzende
  dondurulmalidir:
  1. Global
  2. Signal Producer
  3. Signal Transform
  4. Entry Gates
  5. Position Sizing / Capital / Broker Model
  6. Exit Rules
  7. Integrations
  8. Visualization / Performance
- UI'da gorunmesi gereken seyler yalniz kullanicinin gercekten ayarladigi strategy behavior alanlaridir:
  direction/policy, signal family, transform toggles, filters/guards, sizing, exit rules, integration payload
  alanlari ve tek `Performance Mode`.
- UI'ya cikmamasi gerekenler internal runtime/state/parity alanlaridir:
  working-exit internals, lifecycle metadata, broker normalization, artifact metadata, internal counters,
  indicator/HTF/cache internals.
- Parent-child iliskilerinde esas kontrat `active` state'tir.
  Pine tarafinda hard-hide her durumda mumkun olmayabilir; bu durumda child field ayni parent altinda
  kalmali ve `active = false` ile etkisizlestirilmelidir.

---

# 2. Top-Level Input Group Order

1. Global
2. Signal Producer
3. Signal Transform
4. Entry Gates
5. Position Sizing / Capital / Broker Model
6. Exit Rules
7. Integrations
8. Visualization / Performance

Notlar:
- `PositionManager` ayarlari ayri ana grup acmaz; `Global` icinde kalir.
- `Broker / Cost Model` ayri ana grup acmaz; sizing ile ayni ust grupta kalir.
- `Debug / Diagnostic` ayri standart kullanici grubu acmaz.
- `WunderTrading`, `Integrations` altinda kalir.

---

# 3. Detailed Group / Subgroup Layout

## Global

### Alt grup: Direction & Entry Policy
1. `enable_long`
2. `enable_short`
3. `allow_flip`
4. `regime_lock`
5. `max_entries`
6. `cooldown_bars`

Parent/child active iliskisi:
- Parent yok.

UI gorunurluk kurali:
- Her zaman gorunur.

### Alt grup: Warmup
1. `warmup_bars_override`

Parent/child active iliskisi:
- Parent yok.

UI gorunurluk kurali:
- Her zaman gorunur.

## Signal Producer

### Alt grup: Producer Selection
1. `signal_mode`

Parent/child active iliskisi:
- Tum producer alt gruplari `signal_mode` secimine baglidir.

UI gorunurluk kurali:
- Her zaman gorunur.

### Alt grup: Supertrend
1. `st_atr_len`
2. `st_factor`
3. `st_use_wicks`
4. `st_use_ha`

Parent/child active iliskisi:
- `signal_mode = "Supertrend"` ise aktif.

UI gorunurluk kurali:
- Yalniz `signal_mode = "Supertrend"` ise aktif/gorunur.

### Alt grup: RangeFilterHybrid
1. `rf_adx_trend_threshold`
2. `rf_adx_range_threshold`
3. `rf_chop_trend_threshold`
4. `rf_chop_range_threshold`
5. `rf_rsi_len`
6. `rf_rsi_oversold`
7. `rf_rsi_overbought`
8. `rf_bb_len`
9. `rf_bb_mult`
10. `rf_use_bb_filter`

Parent/child active iliskisi:
- `signal_mode = "RangeFilterHybrid"` ise aktif.

UI gorunurluk kurali:
- Yalniz `signal_mode = "RangeFilterHybrid"` ise aktif/gorunur.

### Alt grup: CandlePattern

Input sirasi:
- Base V2 scope'ta producer-specific ek input yok.

Parent/child active iliskisi:
- `signal_mode = "CandlePattern"` secildiginde bu alt grup bos kalir.

UI gorunurluk kurali:
- Bu producer icin base scope'ta ekstra field acilmaz.

## Signal Transform

### Alt grup: Confirmation
1. `use_confirmation`
2. `conf_left_bars`
3. `conf_right_bars`
4. `conf_require_close_beyond`
5. `conf_timeout_bars`
6. `conf_min_wait_bars`
7. `conf_gate_only_when_flat`

Parent/child active iliskisi:
- `use_confirmation = true` ise child field'lar aktif olur.

UI gorunurluk kurali:
- `use_confirmation` her zaman gorunur.
- Diger alanlar yalniz `use_confirmation = true` iken aktif/gorunur.

### Alt grup: Level Retest
1. `use_level_retest`
2. `retest_timeout_bars`
3. `retest_buffer_pct`

Parent/child active iliskisi:
- `use_level_retest = true` ise child field'lar aktif olur.

UI gorunurluk kurali:
- `use_level_retest` her zaman gorunur.
- Diger alanlar yalniz `use_level_retest = true` iken aktif/gorunur.

## Entry Gates

### Alt grup: Filters - MA & Trend
1. `use_ma_filter`
2. `ma_type`
3. `ma_length`
4. `use_ma_mtf`
5. `ma_htf_timeframe`
6. `use_ma_slope_filter`
7. `ma_slope_len`
8. `ma_slope_min_pct`
9. `use_mcginley_filter`
10. `mcginley_length`
11. `mcginley_use_higher_timeframe`
12. `mcginley_htf_timeframe`
13. `use_htf_trend_filter`
14. `htf_trend_timeframe`
15. `htf_trend_ma_type`
16. `htf_trend_ma_len`
17. `htf_trend_buffer_pct`

Parent/child active iliskisi:
- `ma_*` alanlari `use_ma_filter` ile baglidir.
- `ma_htf_timeframe` yalniz `use_ma_filter` ve `use_ma_mtf` iken aktif olur.
- `ma_slope_*` alanlari `use_ma_slope_filter` ile baglidir.
- `mcginley_*` alanlari `use_mcginley_filter` ile baglidir.
- `mcginley_htf_timeframe` yalniz `use_mcginley_filter` ve `mcginley_use_higher_timeframe` iken aktiftir.
- `htf_trend_*` alanlari `use_htf_trend_filter` ile baglidir.

UI gorunurluk kurali:
- Her parent toggle her zaman gorunur.
- Child alanlar yalniz parent acikken aktif/gorunur.

### Alt grup: Filters - MACD
1. `use_macd_regime_line`
2. `use_macd_cross_state`
3. `use_macd_histogram`
4. `use_macd_zero_distance`
5. `use_macd_htf_bias`
6. `macd_fast`
7. `macd_slow`
8. `macd_signal`
9. `macd_source`
10. `macd_hist_mode`
11. `macd_min_distance`
12. `macd_htf_timeframe`

Parent/child active iliskisi:
- `macd_fast`, `macd_slow`, `macd_signal`, `macd_source`:
  en az bir MACD toggle aciksa aktiftir.
- `macd_hist_mode`:
  yalniz `use_macd_histogram = true` iken aktiftir.
- `macd_min_distance`:
  yalniz `use_macd_zero_distance = true` iken aktiftir.
- `macd_htf_timeframe`:
  yalniz `use_macd_htf_bias = true` iken aktiftir.

UI gorunurluk kurali:
- Bes MACD toggle her zaman gorunur.
- Shared MACD parametreleri yalniz en az bir MACD gate acikken aktif/gorunur.

### Alt grup: Filters - Activity & Regime
1. `use_volume_filter`
2. `vol_sma_len`
3. `vol_min_sma`
4. `use_adx_filter`
5. `adx_length`
6. `adx_threshold`
7. `adx_use_higher_timeframe`
8. `adx_htf_timeframe`
9. `use_chop_filter`
10. `chop_length`
11. `chop_threshold`
12. `chop_use_higher_timeframe`
13. `chop_htf_timeframe`
14. `use_atr_vol_filter`
15. `atr_vol_len`
16. `atr_vol_smooth_len`
17. `atr_vol_floor_mult`
18. `use_momentum_filter`
19. `momentum_mode`
20. `momentum_atr_len`
21. `momentum_atr_mult`
22. `momentum_roc_min_pct`

Parent/child active iliskisi:
- `vol_*` alanlari `use_volume_filter` ile baglidir.
- `adx_*` alanlari `use_adx_filter` ile baglidir.
- `adx_htf_timeframe` yalniz `use_adx_filter` ve `adx_use_higher_timeframe` iken aktiftir.
- `chop_*` alanlari `use_chop_filter` ile baglidir.
- `chop_htf_timeframe` yalniz `use_chop_filter` ve `chop_use_higher_timeframe` iken aktiftir.
- `atr_vol_*` alanlari `use_atr_vol_filter` ile baglidir.
- `momentum_*` alanlari `use_momentum_filter` ile baglidir.
- `momentum_atr_len` ve `momentum_atr_mult` yalniz `momentum_mode = "ATR_BODY"` iken aktiftir.
- `momentum_roc_min_pct` yalniz `momentum_mode = "ROC"` iken aktiftir.

UI gorunurluk kurali:
- Parent toggle her zaman gorunur.
- Child alanlar yalniz ilgili parent acikken aktif/gorunur.

### Alt grup: Filters - Pattern / Level / Session
1. `use_candle_pattern_gate`
2. `use_level_proximity_gate`
3. `level_proximity_threshold_pct`
4. `use_session_filter`
5. `session_name`
6. `session_custom_start`
7. `session_custom_end`
8. `session_custom_timezone`

Parent/child active iliskisi:
- `level_proximity_threshold_pct` yalniz `use_level_proximity_gate = true` iken aktiftir.
- `session_name` yalniz `use_session_filter = true` iken aktiftir.
- `session_custom_*` alanlari yalniz `use_session_filter = true` ve `session_name = "Custom"` iken aktiftir.

UI gorunurluk kurali:
- `use_candle_pattern_gate`, `use_level_proximity_gate`, `use_session_filter` her zaman gorunur.
- Session custom alanlari yalniz Custom session secildiginde aktif/gorunur.

### Alt grup: Guards - Hard Limits
1. `use_daily_loss_limit`
2. `max_daily_loss_pct`
3. `use_max_trades_per_day`
4. `max_trades_per_day`
5. `use_max_drawdown_guard`
6. `max_drawdown_pct`
7. `use_consecutive_loss_halt`
8. `max_consecutive_losses`

Parent/child active iliskisi:
- Her threshold alaninin parent toggle'i kendi ustundedir.

UI gorunurluk kurali:
- Parent toggle her zaman gorunur.
- Child alanlar yalniz parent acikken aktif/gorunur.

### Alt grup: Guards - Cooldown / Equity / MAE
1. `use_trade_cooldown`
2. `cooldown_bars_after_exit`
3. `use_equity_curve_filter`
4. `equity_ma_length`
5. `use_mae_guard`
6. `max_mae_pct`

Parent/child active iliskisi:
- Her child field kendi parent toggle'i ile baglidir.

UI gorunurluk kurali:
- Parent toggle her zaman gorunur.
- Child alanlar yalniz parent acikken aktif/gorunur.

### Alt grup: Guards - Recovery
1. `use_guard_recovery`
2. `guard_recovery_mode`
3. `guard_recovery_bars`
4. `guard_recovery_signals`

Parent/child active iliskisi:
- `guard_recovery_mode` yalniz `use_guard_recovery = true` iken aktiftir.
- `guard_recovery_bars` yalniz `use_guard_recovery = true` ve `guard_recovery_mode = "Bars"` iken aktiftir.
- `guard_recovery_signals` yalniz `use_guard_recovery = true` ve `guard_recovery_mode = "Signals"` iken aktiftir.

UI gorunurluk kurali:
- `use_guard_recovery` yalniz en az bir recoverable guard aciksa aktif/gorunur olmali.
- `capital_exhaustion_guard` recovery kapsaminda gosterilmez.

## Position Sizing / Capital / Broker Model

### Alt grup: Risk Sizing
1. `risk_per_long_pct`
2. `risk_per_short_pct`
3. `fallback_size_pct`
4. `max_leverage_cap`
5. `equity_source`

Parent/child active iliskisi:
- Parent yok.

UI gorunurluk kurali:
- Her zaman gorunur.
- `fallback_size_pct`, `use_sl = false` durumunda devreye girse de UI'da her zaman gorunur;
  cunku sizing grubu exit grubundan once gelir.

### Alt grup: Broker / Cost Model
1. `commission_pct`
2. `slippage_ticks`
3. `spread_ticks`
4. `funding_bps_per_8h`

Parent/child active iliskisi:
- Parent yok.

UI gorunurluk kurali:
- Her zaman gorunur.

### Alt grup: Capital Safeguard
1. `use_capital_exhaustion_guard`
2. `capital_exhaustion_floor_pct`

Parent/child active iliskisi:
- `capital_exhaustion_floor_pct` yalniz `use_capital_exhaustion_guard = true` iken aktiftir.

UI gorunurluk kurali:
- Parent her zaman gorunur.
- Child alan yalniz parent acikken aktif/gorunur.

Not:
- UI'da bu grup altinda gorunse de runtime owner `broker_model / capital policy` katmanidir.

## Exit Rules

### Alt grup: Stop Loss
1. `use_sl`
2. `use_sl_atr`
3. `use_sl_percent`
4. `use_sl_swing_atr`
5. `sl_atr_len`
6. `sl_atr_mult`
7. `sl_percent`
8. `sl_swing_basis`
9. `sl_swing_lookback`
10. `sl_swing_atr_len`
11. `sl_swing_atr_mult`

Parent/child active iliskisi:
- `use_sl_*` secimleri yalniz `use_sl = true` iken aktiftir.
- Bu uc alan radio mantigiyla sirali gorunur:
  `use_sl_percent`, `use_sl_atr` secili degilken aktif olur;
  `use_sl_swing_atr`, onceki iki mod secili degilken aktif olur.
- Parametreler yalniz secili SL moduna gore aktif olur.

UI gorunurluk kurali:
- `use_sl` her zaman gorunur.
- `use_sl_*` alanlari parent acikken gorunur/aktif olur.
- Mode parametreleri yalniz secilen mode icin gorunur/aktif olur.

### Alt grup: Take Profit
1. `use_tp`
2. `use_tp_single_atr`
3. `use_tp_single_pct`
4. `use_tp_single_r`
5. `use_tp_multi`
6. `tp_atr_len`
7. `tp_atr_mult`
8. `tp_percent`
9. `tp_r_multiple`
10. `tp1_r_multiple`
11. `tp1_close_pct`
12. `tp2_r_multiple`

Parent/child active iliskisi:
- `use_tp_*` secimleri yalniz `use_tp = true` iken aktiftir.
- Bu dort alan radio mantigiyla sirali gorunur.
- `use_tp_single_r` ve `use_tp_multi`, `use_sl = true` degilse aktif olmamalidir.
- `tp_atr_*` yalniz `use_tp_single_atr = true` iken aktiftir.
- `tp_percent` yalniz `use_tp_single_pct = true` iken aktiftir.
- `tp_r_multiple` yalniz `use_tp_single_r = true` ve `use_sl = true` iken aktiftir.
- `tp1_r_multiple`, `tp1_close_pct`, `tp2_r_multiple`
  yalniz `use_tp_multi = true` ve `use_sl = true` iken aktiftir.

UI gorunurluk kurali:
- `use_tp` her zaman gorunur.
- `use_tp_*` alanlari parent acikken gorunur/aktif olur.
- Mode parametreleri yalniz secilen TP moduna gore gorunur/aktif olur.

### Alt grup: Break Even
1. `use_break_even`
2. `be_trigger_r`
3. `be_buffer_r`

Parent/child active iliskisi:
- `use_break_even` yalniz `use_sl = true` iken aktif olmalidir.
- `be_*` alanlari yalniz `use_break_even = true` iken aktiftir.

UI gorunurluk kurali:
- Parent alan gorunur, `use_sl = false` iken inactive olur.
- Child alanlar yalniz parent acikken aktif/gorunur.

### Alt grup: Trailing
1. `use_trailing`
2. `trail_atr_len`
3. `trail_start_r`
4. `trail_distance_atr_mult`

Parent/child active iliskisi:
- `use_trailing` yalniz `use_sl = true` iken aktif olmalidir.
- `trail_*` alanlari yalniz `use_trailing = true` iken aktiftir.

UI gorunurluk kurali:
- Parent alan gorunur, `use_sl = false` iken inactive olur.
- Child alanlar yalniz parent acikken aktif/gorunur.

### Alt grup: Time Exits
1. `use_time_stop`
2. `time_stop_bars`
3. `time_stop_eod`
4. `time_stop_eow`
5. `time_stop_condition`

Parent/child active iliskisi:
- `time_stop_bars` yalniz `use_time_stop = true` iken aktiftir.
- `time_stop_condition`, `use_time_stop = true` veya `time_stop_eod = true` veya `time_stop_eow = true`
  ise aktif olmalidir.

UI gorunurluk kurali:
- Uc parent toggle her zaman gorunur.
- Condition field yalniz en az bir time-exit family aktifse gorunur/aktif olur.

### Alt grup: Signal / Filter Exits
1. `exit_on_opposite_signal`
2. `exit_on_filter_block`
3. `exit_on_ma_block`
4. `exit_on_ma_slope_block`
5. `exit_on_mcginley_block`
6. `exit_on_htf_trend_block`
7. `exit_on_vol_block`
8. `exit_on_atr_vol_block`
9. `exit_on_range_block`

Parent/child active iliskisi:
- `exit_on_opposite_signal` parent yok.
- Per-filter exit toggle'lari yalniz `exit_on_filter_block = true` iken aktiftir.
- Ayrica her biri ancak ilgili entry filter'i aciksa aktif olmalidir.
- `exit_on_range_block`, ancak `use_adx_filter = true` veya `use_chop_filter = true` iken aktif olmalidir.

UI gorunurluk kurali:
- `exit_on_opposite_signal` ve `exit_on_filter_block` her zaman gorunur.
- Per-filter exit toggle'lari yalniz master acikken ve ilgili filter mevcutken aktif/gorunur.

## Integrations

### Alt grup: WunderTrading
1. `wt_enter_long_code`
2. `wt_exit_long_code`
3. `wt_enter_short_code`
4. `wt_exit_short_code`
5. `wt_exit_all_code`
6. `wt_order_type`
7. `wt_amount_type`
8. `wt_amount`
9. `wt_leverage`
10. `wt_use_tp`
11. `wt_use_sl`
12. `wt_reduce_only`
13. `wt_place_cond_orders`

Parent/child active iliskisi:
- `wt_use_tp` yalniz `use_tp = true` iken aktif olmalidir.
- `wt_use_sl` yalniz `use_sl = true` iken aktif olmalidir.

UI gorunurluk kurali:
- Pine tarafinda her zaman gorunur.
- Bos code alanlari "unused" anlamina gelir; ayri enable toggle eklenmez.

## Visualization / Performance

### Alt grup: Performance
1. `performance_mode`

Parent/child active iliskisi:
- Parent yok.

UI gorunurluk kurali:
- Her zaman gorunur.

### Alt grup: Auto-Plotted Elements

Input sirasi:
- Base V2 scope'ta ayri input yok.

Parent/child active iliskisi:
- Yok.

UI gorunurluk kurali:
- Asagidaki elemanlar ilgili feature aktifse otomatik cizilir, ayri toggle almaz:
  `SL`, `SL Base`, `TP/TP1/TP2`, `Trail`, `Supertrend line/fill`, `BB bands`, `MA`, `McGinley`,
  `BUY/SELL`, `ENTRY`, `PYRAMID` marker'lari.

---

# 4. Recommended Active/Visibility Rules

- Her zaman gorunen alanlar:
  - `enable_long`, `enable_short`, `allow_flip`, `regime_lock`, `max_entries`, `cooldown_bars`,
    `warmup_bars_override`, `signal_mode`, parent filter/guard toggles, sizing alanlari,
    `use_sl`, `use_tp`, `use_break_even`, `use_trailing`, `exit_on_opposite_signal`,
    `exit_on_filter_block`, WT alanlari, `performance_mode`
- Parent toggle acikken aktif olacak alanlar:
  - tum `use_*` child parametreleri
  - `session_custom_*`
  - `guard_recovery_*`
  - `capital_exhaustion_floor_pct`
  - WT `tp/sl` dispatch flag'lari
- Radio secimine bagli aktif olacak alanlar:
  - `use_sl_atr | use_sl_percent | use_sl_swing_atr`
  - `use_tp_single_atr | use_tp_single_pct | use_tp_single_r | use_tp_multi`
- SL radio mantigi:
  - `use_sl = false` ise tum `use_sl_*` alanlari inactive olmali
  - `use_sl = true` ise yalniz tek mode secilebilir
  - yalniz secilen mode'un parametreleri aktif olmali
- TP radio mantigi:
  - `use_tp = false` ise tum `use_tp_*` alanlari inactive olmali
  - `use_tp = true` ise yalniz tek mode secilebilir
  - yalniz secilen mode'un parametreleri aktif olmali
  - `Single R` ve `Multi-TP`, `use_sl = true` degilse secilebilir olmamali
- Multi-TP gorunurlugu:
  - `tp1_r_multiple`, `tp1_close_pct`, `tp2_r_multiple`
    yalniz `use_tp_multi = true` ve `use_sl = true` iken aktif/gorunur
- BE / Trailing dependency:
  - `use_break_even` ve `use_trailing`, `use_sl = false` iken inactive olmali
  - child alanlar yalniz parent acikken aktif olmali
- Session custom alanlari:
  - `session_custom_start`, `session_custom_end`, `session_custom_timezone`
    yalniz `use_session_filter = true` ve `session_name = "Custom"` iken aktif/gorunur
- MACD alt parametre gorunurlugu:
  - shared MACD parametreleri yalniz en az bir MACD gate acikken aktif olmali
  - `macd_hist_mode` yalniz histogram gate icin
  - `macd_min_distance` yalniz zero-distance gate icin
  - `macd_htf_timeframe` yalniz HTF bias gate icin
- Guard recovery gorunurlugu:
  - `use_guard_recovery` yalniz recoverable guard ailelerinden en az biri aciksa aktif olmali
  - Bars/Signals child alanlari yalniz secili recovery mode'a gore aktif olmali
- Cross-group dependency:
  - `allow_flip`, `exit_on_opposite_signal = true` degilse aktif olmamali
- WunderTrading alanlari:
  - ayri master toggle acilmaz
  - kod alanlari her zaman gorunur
  - `wt_use_tp` yalniz TP aciksa, `wt_use_sl` yalniz SL aciksa aktif olur
- Performance Mode:
  - Visualization grubundaki tek standart user-facing toggle budur
  - diger cizimler feature-active ise otomatik olmalidir
- Future extension gelene kadar UI'da yer almamasi gerekenler:
  - advanced confirmation knobs
  - producer arbitration knobs
  - context-exit knobs
  - diagnostics formatting knobs
  - parity/export knobs

---

# 5. Things That Must Stay Out of the UI

- `lifecycle_id`
- `event_seq_in_bar`
- `working_exit_book_version`
- `working_exit_reference_qty`
- `completed_exit_ids`
- `active_stop_owner`
- `active_stop_price`
- `trail_price`
- `initial_risk_per_unit`
- `fill_type`
- `is_pessimistic_sl`
- parity/export metadata
- broker normalization internals
- rounding helper secenekleri
- indicator registry/cache internals
- HTF hub internals
- session definition tables
- `price_tick`, `qty_step`, `min_qty`, `min_notional`, `contract_multiplier`
- guard recovery internal counters
- internal state fields
- debug-only low-level counters
- compile-time fallback gates
- raw marker/debug artifact toggles

---

# 6. Future-Proof Placement Rules

- Yeni direction / run-policy alanlari -> `Global`
- Yeni mutually-exclusive signal family -> `Signal Producer`
- Producer-specific parametreler -> ilgili producer alt grubu
- Stateful pre-entry wait / confirm / retest logic -> `Signal Transform`
- Bar-snapshot tabanli market eligibility -> `Entry Gates > Filters`
- Portfolio halt / cooldown / recovery mantigi -> `Entry Gates > Guards`
- Qty formulu, qty clamp veya leverage/notional limit -> `Position Sizing / Capital / Broker Model`
- Capital floor / broker-owned hard capital safeguard -> `Position Sizing / Capital / Broker Model`
- Pozisyon acikken close ureten yeni aile -> `Exit Rules`
- External execution adapter / webhook / broker payload -> `Integrations`
- Chartta otomatik cizilen yeni eleman -> ayri toggle degil; ilgili feature aktifse implicit plot
- Runtime internal metadata veya parity tooling -> UI disinda kalir

UI grouping kurali:
- UI grubu runtime owner'i degistirmez.
- Kullanici tarafindan ayarlanmayacak internal alan UI'ya cikarilmaz.
- Bir aile mevcut alt gruba dogal sigiyorsa yeni ana grup acilmaz.

---

# 7. Proposed MTC_V2_INPUT_UI_SPEC.md

Kisa freeze taslagi:

- Top-level order:
  `Global -> Signal Producer -> Signal Transform -> Entry Gates -> Position Sizing / Capital / Broker Model -> Exit Rules -> Integrations -> Visualization / Performance`
- Parent-child contract:
  - parent field her zaman gorunur
  - child field yalniz parent acikken aktif olur
  - radio-mode ailelerde yalniz secili mode'un child field'lari aktif olur
- Auto UI kurali:
  - feature-active visual'lar otomatik cizilir
  - `Performance Mode` disinda ekstra visual clutter toggle acilmaz
- Hidden contract:
  - runtime state, parity metadata, broker normalization, working-exit internals ve low-level debug alanlari UI'ya cikmaz

---

# 8. Final Recommendation

`UI ORDER MOSTLY CLEAR, MINOR GAPS`

Minor gaps:
- `performance_mode` Pine-local bir UI field'dir; architecture'da davranisi net, fakat exact field naming implementation'da sabitlenecektir.
- Pine tarafinda dinamik hard-hide yerine bazi alanlar `active = false` ile gosterilebilir; spec bunu kabul eder ama order'i degistirmez.
