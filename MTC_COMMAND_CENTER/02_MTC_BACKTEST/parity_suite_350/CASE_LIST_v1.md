# MTC Parity Suite 350 — Canonical Case List v1

> **Kural:** Her case, baseline'dan gerçekten farklı trade davranışı üretmeli.
> Inert case (hiçbir şeyi değiştirmeyen) kabul edilmez.
>
> **Baseline:** `parity_core_001_baseline_touch`
> Signal=Supertrend (ATR21 factor4.0 wicks=on ha=on), SL=ATR(14,4.0), TP=ATR(14,3.0),
> BE=on(rr=1.0 buf=0.1), MultiTP=on(tp1@3R 50% tp2@5.5R), Trail=on(start2.5R dist2.0R),
> Tüm filters=off, Tüm guards=off, TimeStop=off, Long+Short enabled

---

## EXIT FILTER BLOCK — Dependency Kuralı (kritik)

Pine kodu (satır 3741-3746):
```pine
if not closeRequestedThisBar and exit_on_filter_block and strategy.position_size != 0
    if exit_on_ma_block and use_ma_filter
```

**Sonuç:** Geçerli bir exit_filter_block case için 3 şart aynı anda aktif olmalı:
1. `trade.exit_on_filter_block = true` (global master)
2. `filters.use_XXX_filter = true` (ilgili filter açık)
3. `exit_filter_block.exit_on_XXX_block = true` (per-filter exit toggle)

Sadece global ON veya sadece filter ON → **inert** → geçersiz case.

---

## CORE PACKAGE (~55 case)

### C01 — Baseline
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C01 | parity_core_001_baseline_touch | Temel referans | — | — | fill_contract=touch |

---

### C02–C06 — Signal Mode
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C02 | core_signal_none | signal_mode=None → sıfır trade | signal_mode=None | — | ZERO_TRADE_EXPECTED |
| C03 | core_signal_rfh | Range Filter Hybrid mode | signal_mode=Range Filter Hybrid | — | Tüm RF parametreler default |
| C04 | core_st_wicks_off | Supertrend wicks=false | st_use_wicks=false | signal_mode=Supertrend | HA hâlâ on |
| C05 | core_st_ha_off | Supertrend ha=false | use_ha_for_supertrend=false | signal_mode=Supertrend | Wicks hâlâ on |
| C06 | core_st_wicks_ha_off | Supertrend wicks=false AND ha=false | st_use_wicks=false, use_ha=false | signal_mode=Supertrend | |

---

### C07 — Confirmation Layer
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C07 | core_confirmation_on | Confirmation layer aktif | confirmation.enabled=true | — | Sub-params default |

---

### C08–C12 — Trade Directions & Entry Controls
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C08 | core_entry_edge | entry_mode=Edge (sadece flip'te giriş) | trade.entry_mode=Edge | — | |
| C09 | core_allow_flip_off | Position flip yok | trade.allow_flip=false | — | |
| C10 | core_exit_opposite_on | Karşı sinyal = çıkış | trade.exit_on_opposite_signal=true | — | |
| C11 | core_long_only | Sadece long trade | trade.enable_short=false | — | |
| C12 | core_short_only | Sadece short trade | trade.enable_long=false | — | |

---

### C13 — Regime Lock
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C13 | core_regime_lock_on | Aynı yönde re-entry yok | trade.use_regime_lock=true | — | |

---

### C14–C18 — Time Stop
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C14 | core_time_stop_bars | Belirli bar sonra çıkış | time_stop.enabled=true, bars=5 | — | eod=false eow=false condition=Always |
| C15 | core_time_stop_eod | Günün sonunda çıkış | time_stop.enabled=true, eod=true | time_stop.enabled=true | bars=999 (büyük değer - EOD önce tetiklenmeli) |
| C16 | core_time_stop_eow | Haftanın sonunda çıkış | time_stop.enabled=true, eow=true | time_stop.enabled=true | bars=999 |
| C17 | core_time_stop_profit_only | Sadece karda çıkış | time_stop.enabled=true, bars=5, condition=Profit Only | time_stop.enabled=true | |
| C18 | core_time_stop_loss_only | Sadece zararda çıkış | time_stop.enabled=true, bars=5, condition=Loss Only | time_stop.enabled=true | |

---

### C19–C21 — Stop Loss Mode
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C19 | core_sl_off | SL tamamen kapalı | stop_loss.use_sl=false | — | fallback_qty_pct devreye girer |
| C20 | core_sl_mode_pct | SL mode=% | stop_loss.mode=%, percent=1.0 | stop_loss.use_sl=true | |
| C21 | core_sl_mode_swing_atr | SL mode=Swing+ATR | stop_loss.mode=Swing+ATR | stop_loss.use_sl=true | swing_basis=Wick, lookback=20 default |

---

### C22–C25 — Take Profit Mode
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C22 | core_tp_off | TP tamamen kapalı | take_profit.use_tp=false, multi_tp.use_multi_tp=false | — | MultiTP da kapatılmalı (parent=TP) |
| C23 | core_tp_mode_pct | Single TP mode=% | take_profit.mode=%, multi_tp.use_multi_tp=false | take_profit.use_tp=true | MultiTP kapalı = single TP path aktif |
| C24 | core_tp_mode_rr | Single TP mode=R | take_profit.mode=R, multi_tp.use_multi_tp=false | take_profit.use_tp=true | MultiTP kapalı = single TP path aktif |
| C25 | core_multi_tp_off | MultiTP kapalı, single TP (ATR) path | multi_tp.use_multi_tp=false | take_profit.use_tp=true | TP mode=ATR kalır (baseline gibi) |

---

### C26–C27 — Break-Even & Trailing
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C26 | core_break_even_off | BE kapalı | break_even.use_break_even=false | — | |
| C27 | core_trailing_off | Trailing stop kapalı | trailing.use_trailing=false | — | |

---

### C28–C35 — Filters (Entry Blocking Only)
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C28 | core_filter_ma_on | MA filter entry'leri kısıtlıyor | filters.use_ma_filter=true | — | exit_on_filter_block=false (sadece entry block) |
| C29 | core_filter_ma_slope_on | MA Slope filter aktif | filters.use_ma_slope_filter=true | — | exit_on_filter_block=false |
| C30 | core_filter_volume_on | Volume filter aktif (Pine default=on, baseline=off) | filters.use_volume_filter=true | — | exit_on_filter_block=false |
| C31 | core_filter_atr_vol_on | ATR volatility floor aktif (Pine default=on, baseline=off) | filters.use_atr_vol_filter=true | — | exit_on_filter_block=false |
| C32 | core_filter_mcginley_on | McGinley filter aktif | filters.use_mcginley_filter=true | — | exit_on_filter_block=false |
| C33 | core_filter_htf_on | HTF Trend filter aktif | filters.use_htf_trend_filter=true | — | exit_on_filter_block=false |
| C34 | core_filter_macd_regime | MACD Hub filter (mode=Regime, default) | filters.use_macd_filter=true, macd_gate_mode=Regime | — | exit_on_filter_block=false |
| C35 | core_filter_range_regime_on | Range Regime (ADX+Chop) filter aktif | filters.use_range_filters=true, filters.use_range_regime_filter=true | — | exit_on_filter_block=false |

---

### C36–C42 — Exit Filter Block (entry + exit block — TÜM 3 KOŞUL aktif)
> Her case: `trade.exit_on_filter_block=true` + ilgili filter ON + per-filter exit toggle ON

| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C36 | core_exit_ma_block | MA filter: hem entry block hem exit trigger | exit_on_filter_block=true, use_ma_filter=true, exit_on_ma_block=true | Üç koşul birlikte | |
| C37 | core_exit_ma_slope_block | MA Slope filter exit trigger | exit_on_filter_block=true, use_ma_slope_filter=true, exit_on_ma_slope_block=true | Üç koşul birlikte | |
| C38 | core_exit_volume_block | Volume filter exit trigger | exit_on_filter_block=true, use_volume_filter=true, exit_on_vol_part_block=true | Üç koşul birlikte | |
| C39 | core_exit_atr_vol_block | ATR Vol filter exit trigger | exit_on_filter_block=true, use_atr_vol_filter=true, exit_on_atr_vol_block=true | Üç koşul birlikte | |
| C40 | core_exit_mcginley_block | McGinley filter exit trigger | exit_on_filter_block=true, use_mcginley_filter=true, exit_on_mcginley_block=true | Üç koşul birlikte | |
| C41 | core_exit_htf_block | HTF Trend filter exit trigger | exit_on_filter_block=true, use_htf_trend_filter=true, exit_on_htf_trend_block=true | Üç koşul birlikte | |
| C42 | core_exit_range_block | Range filter exit trigger | exit_on_filter_block=true, use_range_filters=true, use_range_regime_filter=true, exit_on_range_block=true | Üç koşul birlikte | |

---

### C43–C47 — Guards (Entry Blocking)
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C43 | core_guard_dd_on | Max Drawdown guard aktif | guards.use_dd_guard=true | — | dd_guard_pct=10.0 default |
| C44 | core_guard_consec_loss_on | Consecutive loss guard aktif | guards.use_consec_loss_guard=true | — | consec_loss_max=3 default |
| C45 | core_guard_cooldown_on | Cooldown guard aktif | guards.use_cooldown_guard=true | — | cooldown_bars=5 default |
| C46 | core_guard_eq_curve_on | Equity curve guard aktif (Pine default=on, baseline=off) | guards.use_eq_curve_guard=true | — | eq_curve_ma_len=5 default |
| C47 | core_guard_mae_on | MAE in-trade guard aktif | guards.use_mae_guard=true | — | mae_max_pct=2.0 default |

---

### C48–C50 — Guard Recovery Modes (her mod bir case — guard aktif olmalı)
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C48 | core_guard_recovery_bars | Guard recovery mode=Bars | use_dd_guard=true, use_guard_recovery=true, guard_recovery_mode=Bars | use_dd_guard=true | guard_recovery_bars=3 default |
| C49 | core_guard_recovery_signals | Guard recovery mode=Signals | use_dd_guard=true, use_guard_recovery=true, guard_recovery_mode=Signals | use_dd_guard=true | guard_recovery_signals=2 default |
| C50 | core_guard_recovery_virtual | Guard recovery mode=Virtual Trade | use_consec_loss_guard=true, use_guard_recovery=true, guard_recovery_mode=Virtual Trade | use_consec_loss_guard=true | Virtual Trade requires consec_loss guard |

---

### C51–C52 — Daily Limits
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C51 | core_daily_loss_limit_on | Günlük max kayıp limiti | risk.use_daily_loss_limit=true | — | max_daily_loss_percent=5.0 default |
| C52 | core_max_trades_per_day_on | Günlük max trade limiti | risk.use_max_trades_per_day=true | — | max_trades_per_day=5 default |

---

### C53–C56 — MACD Filter Sub-Modes (use_macd_filter=true zorunlu parent)
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| C53 | core_filter_macd_cross_state | MACD gate mode=Cross-State | use_macd_filter=true, macd_gate_mode=Cross-State | use_macd_filter=true | |
| C54 | core_filter_macd_histogram | MACD gate mode=Histogram | use_macd_filter=true, macd_gate_mode=Histogram | use_macd_filter=true | |
| C55 | core_filter_macd_distance | MACD gate mode=Distance | use_macd_filter=true, macd_gate_mode=Distance | use_macd_filter=true | |
| C56 | core_filter_macd_htf_bias | MACD gate mode=HTF Bias | use_macd_filter=true, macd_gate_mode=HTF Bias | use_macd_filter=true | |

---

**Core toplam: 56 case (C01–C56)**

---

## BOUNDARY PACKAGE (~35 case)

### B01–B06 — Supertrend Parametreleri (signal_mode=Supertrend aktif)
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık |
|---|---------|-------------|-------------------|-----------------|
| B01 | bnd_st_atr_len_7 | ST ATR kısa (daha hassas) | st_atr_len=7 | signal_mode=Supertrend |
| B02 | bnd_st_atr_len_50 | ST ATR uzun (daha yavaş) | st_atr_len=50 | signal_mode=Supertrend |
| B03 | bnd_st_factor_low | ST factor düşük (daha sık sinyal) | st_factor=1.5 | signal_mode=Supertrend |
| B04 | bnd_st_factor_high | ST factor yüksek (daha seyrek) | st_factor=8.0 | signal_mode=Supertrend |
| B05 | bnd_st_signal_max_entries_2 | Signal mode max entries=2 (Pine default) | signal_mode_max_entries=2 | signal_mode=Supertrend |
| B06 | bnd_st_cooldown_bars_1 | Cooldown=1 bar (çok hızlı re-entry) | signal_mode_cooldown_bars=1 | signal_mode=Supertrend |

---

### B07–B11 — SL Parametreleri
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık |
|---|---------|-------------|-------------------|-----------------|
| B07 | bnd_sl_atr_mult_tight | SL ATR mult=1.5 (sıkı stop) | stop_loss.atr_mult=1.5 | use_sl=true, mode=ATR |
| B08 | bnd_sl_atr_mult_wide | SL ATR mult=8.0 (geniş stop) | stop_loss.atr_mult=8.0 | use_sl=true, mode=ATR |
| B09 | bnd_sl_atr_len_7 | SL ATR length=7 | stop_loss.atr_len=7 | use_sl=true, mode=ATR |
| B10 | bnd_sl_pct_tight | SL %=0.5 (sıkı) | stop_loss.mode=%, percent=0.5 | use_sl=true |
| B11 | bnd_sl_swing_body | SL Swing+ATR basis=Body | stop_loss.mode=Swing+ATR, swing_basis=Body | use_sl=true |

---

### B12–B15 — TP Parametreleri (MultiTP kapalı = single TP path)
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık |
|---|---------|-------------|-------------------|-----------------|
| B12 | bnd_tp_atr_mult_tight | TP ATR mult=1.0 (erken çıkış) | take_profit.atr_mult=1.0, multi_tp.use_multi_tp=false | use_tp=true |
| B13 | bnd_tp_atr_mult_wide | TP ATR mult=6.0 (geç çıkış) | take_profit.atr_mult=6.0, multi_tp.use_multi_tp=false | use_tp=true |
| B14 | bnd_tp_mode_pct_tight | TP mode=% at 0.5% | take_profit.mode=%, percent=0.5, multi_tp.use_multi_tp=false | use_tp=true |
| B15 | bnd_tp_mode_rr_low | TP mode=R at 1.0R | take_profit.mode=R, rr=1.0, multi_tp.use_multi_tp=false | use_tp=true |

---

### B16–B19 — Multi-TP Parametreleri (use_multi_tp=true aktif)
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık |
|---|---------|-------------|-------------------|-----------------|
| B16 | bnd_multi_tp_tp1_rr_low | TP1 erken (1.5R) | multi_tp.tp1_rr=1.5 | use_multi_tp=true, use_tp=true |
| B17 | bnd_multi_tp_tp1_pct_low | TP1 az kapat (20%) | multi_tp.tp1_pct=20.0 | use_multi_tp=true, use_tp=true |
| B18 | bnd_multi_tp_tp1_pct_high | TP1 çok kapat (80%) | multi_tp.tp1_pct=80.0 | use_multi_tp=true, use_tp=true |
| B19 | bnd_multi_tp_tp2_rr_high | TP2 çok geç (10R) | multi_tp.tp2_rr=10.0 | use_multi_tp=true, use_tp=true |

---

### B20–B21 — Break-Even Parametreleri (use_break_even=true aktif)
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık |
|---|---------|-------------|-------------------|-----------------|
| B20 | bnd_be_rr_high | BE trigger=3.0R (çok geç) | break_even.rr=3.0 | use_break_even=true |
| B21 | bnd_be_buffer_zero | BE buffer=0.0 (tam BE) | break_even.buffer_r=0.0 | use_break_even=true |

---

### B22–B23 — Trailing Parametreleri (use_trailing=true aktif)
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık |
|---|---------|-------------|-------------------|-----------------|
| B22 | bnd_trail_start_r_low | Trailing erken başlar (0.5R) | trailing.start_r=0.5 | use_trailing=true |
| B23 | bnd_trail_dist_r_tight | Trailing dar mesafe (0.5R) | trailing.dist_r=0.5 | use_trailing=true |

---

### B24–B26 — Time Stop Bars Boundary
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık |
|---|---------|-------------|-------------------|-----------------|
| B24 | bnd_time_stop_bars_1 | 1 bar sonra çıkış (anlık) | time_stop.enabled=true, bars=1 | time_stop.enabled=true |
| B25 | bnd_time_stop_bars_200 | 200 bar sonra çıkış | time_stop.enabled=true, bars=200 | time_stop.enabled=true |
| B26 | bnd_time_stop_eod_eow | Hem EOD hem EOW aktif | time_stop.enabled=true, eod=true, eow=true | time_stop.enabled=true |

---

### B27–B30 — Filter Parametreleri
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık |
|---|---------|-------------|-------------------|-----------------|
| B27 | bnd_filter_ma_sma_type | MA filter type=SMA | use_ma_filter=true, ma_type=SMA | use_ma_filter=true |
| B28 | bnd_filter_ma_len_50 | MA filter kısa (50) | use_ma_filter=true, ma_length=50 | use_ma_filter=true |
| B29 | bnd_filter_htf_tf_60 | HTF filter timeframe=60m | use_htf_trend_filter=true, htf_trend_timeframe=60 | use_htf_trend_filter=true |
| B30 | bnd_filter_vol_mult_high | Volume filter sert (2.0x) | use_volume_filter=true, vol_filter_mult=2.0 | use_volume_filter=true |

---

### B31–B35 — Guard Parametreleri
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık |
|---|---------|-------------|-------------------|-----------------|
| B31 | bnd_guard_dd_pct_tight | DD guard sıkı (%5) | use_dd_guard=true, dd_guard_pct=5.0 | use_dd_guard=true |
| B32 | bnd_guard_consec_loss_max_1 | 1 kayıptan sonra dur | use_consec_loss_guard=true, consec_loss_max=1 | use_consec_loss_guard=true |
| B33 | bnd_guard_consec_reset_off | Günlük reset kapalı | use_consec_loss_guard=true, consec_loss_reset_daily=false | use_consec_loss_guard=true |
| B34 | bnd_guard_cooldown_bars_1 | 1 bar cooldown | use_cooldown_guard=true, cooldown_bars=1 | use_cooldown_guard=true |
| B35 | bnd_guard_mae_pct_tight | MAE sıkı (%0.5) | use_mae_guard=true, mae_max_pct=0.5 | use_mae_guard=true |

---

### B36–B37 — Risk / Daily Limits Boundary
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık |
|---|---------|-------------|-------------------|-----------------|
| B36 | bnd_daily_loss_limit_tight | Günlük limit=%1 (sıkı) | use_daily_loss_limit=true, max_daily_loss_percent=1.0 | use_daily_loss_limit=true |
| B37 | bnd_max_trades_per_day_1 | Günde max 1 trade | use_max_trades_per_day=true, max_trades_per_day=1 | use_max_trades_per_day=true |

---

### B38–B39 — Guard Recovery Boundary
| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık |
|---|---------|-------------|-------------------|-----------------|
| B38 | bnd_guard_recovery_bars_1 | 1 bar sonra recovery | use_dd_guard=true, use_guard_recovery=true, mode=Bars, guard_recovery_bars=1 | use_dd_guard=true |
| B39 | bnd_guard_recovery_signals_1 | 1 sinyal sonra recovery | use_dd_guard=true, use_guard_recovery=true, mode=Signals, guard_recovery_signals=1 | use_dd_guard=true |

---

**Boundary toplam: 39 case (B01–B39)**

---

## PAIRWISE PACKAGE (~10 case)

> Aynı anda iki veya daha fazla feature kombinasyonunu test eder.

| # | case_id | Test niyeti | Baseline'dan fark | Aktif bağımlılık | Not |
|---|---------|-------------|-------------------|-----------------|-----|
| P01 | pw_sl_tp_both_off | Sadece sinyal çıkışı (SL+TP yok) | use_sl=false, use_tp=false, use_multi_tp=false | — | fallback_qty_pct ve trailing hâlâ aktif |
| P02 | pw_filter_ma_entry_and_exit | MA filter hem entry hem exit block | use_ma_filter=true, exit_on_filter_block=true, exit_on_ma_block=true | Üç koşul | Hem entry azalır hem exit artar |
| P03 | pw_filter_multi | MA + Volume filter birlikte | use_ma_filter=true, use_volume_filter=true | — | İki filter AND ile filtreliyor |
| P04 | pw_guard_dd_plus_recovery | DD guard + recovery (bars=10) | use_dd_guard=true, use_guard_recovery=true, mode=Bars, bars=10 | use_dd_guard=true | Recovery aktif: kısa duraklamadan döner |
| P05 | pw_time_stop_plus_max_trades | TimeStop + max trades per day | time_stop.enabled=true, bars=5, use_max_trades_per_day=true, max_trades_per_day=2 | — | İki limit birden |
| P06 | pw_exit_opposite_plus_filter | OPP_SIGNAL + MA filter exit | exit_on_opposite_signal=true, use_ma_filter=true, exit_on_filter_block=true, exit_on_ma_block=true | Üç koşul | Hem sinyal çıkışı hem filter çıkışı aktif |
| P07 | pw_multi_tp_plus_trailing | MultiTP + Trailing (her ikisi açık, baseline gibi ama trailing dar) | trailing.dist_r=0.5 | use_multi_tp=true, use_trailing=true | Erken trailing ile TP2 nadir tetiklenir |
| P08 | pw_rfh_with_range_filter | RFH sinyal + Range regime filter | signal_mode=Range Filter Hybrid, use_range_filters=true, use_range_regime_filter=true | — | RFH sinyal + entry pause combo |
| P09 | pw_all_guards_on | Tüm 5 guard birden | use_dd_guard=true, use_consec_loss_guard=true, use_cooldown_guard=true, use_eq_curve_guard=true, use_mae_guard=true | — | En kısıtlayıcı guard kombinasyonu |
| P10 | pw_sl_off_tp_rr_trailing | SL kapalı + TP=R + Trailing aktif | use_sl=false, use_tp=true, use_multi_tp=false, take_profit.mode=R, rr=2.0, use_trailing=true | use_tp=true, use_trailing=true | |

---

**Pairwise toplam: 10 case (P01–P10)**

---

## ÖZET

| Paket | Count |
|---|---|
| Core | 56 |
| Boundary | 39 |
| Pairwise | 10 |
| **Toplam** | **105** |

---

## INERT CASE UYARI LİSTESİ (Codex'in ürettiği yanlış case'ler)

Aşağıdaki Codex case'leri dependency kuralını ihlal ettiği için **geçersiz**dir:

| Codex case_id | Sorun |
|---|---|
| `parity_core_020_exit_filter_block_global_on` | `exit_on_filter_block=true` ama hiçbir filter aktif değil → inert |
| Herhangi bir exit_filter_block case'i `use_XXX_filter=false` ile | Üç koşuldan biri eksik → inert |
| TP mode/param case'leri `use_multi_tp=true` iken | Single TP path erişilemez → inert (multi TP override eder) |
| Child param case'leri parent=OFF iken | (örn. `time_stop.bars=1` ama `time_stop.enabled=false`) → inert |
| `consec_loss_reset_daily` case'i `use_consec_loss_guard=false` iken | Parent off → child inert |

---

## UYGULAMA NOTU

Bu listedeki her case için JSON üretilirken:
1. Baseline config'den başla
2. "Baseline'dan fark" kolonundaki değerleri uygula
3. "Aktif bağımlılık" kolonundaki parent'ların ON olduğunu doğrula
4. `canonical_config_hash` sadece aktif (davranışa etkili) alanlardan üret
5. `ui_expected_inputs` alanına TV UI'da yapılacak tam değişikliği yaz
