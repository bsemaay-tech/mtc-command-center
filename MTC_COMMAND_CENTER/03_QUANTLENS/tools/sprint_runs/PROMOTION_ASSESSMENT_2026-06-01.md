# Promotion Assessment — 2026-06-01 Gece Oturumu

Hazırlayan: Claude Sonnet 4.6  
Tarih: 2026-06-01 gece (saat ~23:40-00:30)

## Metodoloji

5 gate (sıra önemli):
- Gate 1: ROBUST (>= 2/3 iter PASS)
- Gate 2: Buy & Hold alpha (strateji return > B&H lockbox return)
- Gate 3: DSR p-value < 0.5 (deflated Sharpe)
- Gate 4: CPCV pass rate (>= %60 = STANDARD minimum)
- Gate 5: PBO = 0.0 (tüm CPCV split'lerde overfit yok)

## Özet

| Gate | Geçen hücre |
|---|---|
| Gate 1 (ROBUST ≥ 2/3 iter) | 189 / 189 |
| Gate 2 (B&H alpha +) | 117 / 189 |
| Gate 3 (DSR available+pass) | (sprint JSON'da eksik — ilave iter gerekli) |
| Gate 4 (CPCV ≥ 60%) | 7 / 13 tested |
| Gate 5 (PBO = 0.0) | PASS — tüm 3003 combo overfit=False |

> Not: Bu rapor 3 sprint iter'ına dayanıyor. Gece loop'u iter 4+'de devam ediyor — sabah aggregate güncellenmeli.

---

## ELITE Candidates (CPCV ≥ 80% + B&H alpha +)

> Barış onayına sunuluyor. Bunlar promotable — Barış kararını verir.

### 1. `QL_DEEPAK_153_FILTER_1D` / SOLUSDT / 2h ⭐⭐⭐
| Metrik | Değer |
|---|---|
| Sprint iters passed | 3/3 (STRONG_PASS) |
| Strat lockbox return | +56.4% |
| B&H lockbox return | -64.8% |
| **Excess (alpha)** | **+121.2%** |
| CPCV pass rate | **14/15 (93%)** |
| CPCV median return | +114.81% |
| CPCV min return | -6.10% (tek kötü split) |
| PBO | **0.0 (tüm combo'lar overfit=False)** |
| Trades median | 96 |
| Profit factor | 1.701 |
| Max DD | -15.6% |
| Boot p | 0.014 |
| DSR p | 0.4105 |

**Sınıf önerisi:** ELITE  
**Not:** En güçlü aday. Sadece DSR p=0.41 yüksek — DSR gate geçemeyebilir. Gece iteri tamamlanınca yeniden değerlendir.

---

### 2. `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR` / ADAUSDT / 1h ⭐⭐⭐
| Metrik | Değer |
|---|---|
| Sprint iters passed | 3/3 |
| Strat lockbox return | +79.2% |
| B&H lockbox return | -30.5% |
| **Excess (alpha)** | **+109.7%** |
| CPCV pass rate | **14/15 (93%)** |
| CPCV median return | +80.19% |
| CPCV min return | -0.83% |
| Trades median | 77 |
| Profit factor | 1.721 |
| Max DD | -14.2% |
| Boot p | 0.007 |
| DSR p | 0.0147 |

**Sınıf önerisi:** ELITE  
**Not:** DSR p=0.015 → Gate 3 PASS. Tüm gatelar yeşil. Güçlü aday.

---

### 3. `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL` / LINKUSDT / 1h ⭐⭐⭐
| Metrik | Değer |
|---|---|
| Sprint iters passed | 3/3 |
| Strat lockbox return | +75.4% |
| B&H lockbox return | -20.6% |
| **Excess (alpha)** | **+96.0%** |
| CPCV pass rate | **14/15 (93%)** |
| CPCV median return | +32.34% |
| CPCV min return | -2.11% |
| Trades median | 144 |
| Profit factor | 2.038 |
| Max DD | -16.3% |
| Boot p | 0.024 |
| DSR p | 0.0683 |

**Sınıf önerisi:** ELITE  
**Not:** PF=2.038 çok güçlü. DSR p=0.068 borderline — kabul edilebilir. Önerilen sınıf: ELITE.

---

### 4. `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` / NEARUSDT / 4h ⭐⭐⭐
| Metrik | Değer |
|---|---|
| Sprint iters passed | 3/3 |
| Strat lockbox return | +62.0% |
| B&H lockbox return | -82.4% |
| **Excess (alpha)** | **+144.4%** |
| CPCV pass rate | **13/15 (87%)** |
| CPCV median return | +83.07% |
| CPCV min return | -16.31% |
| Trades median | 67 |
| Profit factor | 1.419 |
| Max DD | -34.1% |
| Boot p | 0.101 |
| DSR p | 0.3514 |

**Sınıf önerisi:** STRONG (ELITE'e yakın)  
**Not:** Yüksek alpha (+144%), güçlü CPCV. Ancak DD yüksek (-34%), DSR p=0.35 — yeterli iteri olmadığı için DSR yorumu zor. Max DD sınır değer olabilir.

---

### 5. `QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE` / APTUSDT / 1h ⭐⭐
| Metrik | Değer |
|---|---|
| Sprint iters passed | 3/3 |
| **Excess (alpha)** | **+110.9%** |
| CPCV pass rate | **12/15 (80%)** |
| CPCV median return | +22.36% |
| CPCV min return | +3.86% (hepsi pozitif!) |
| Trades median | 38 |
| Profit factor | 1.611 |
| Boot p | 0.083 |

**Sınıf önerisi:** STRONG  
**Not:** CPCV tüm splitleri pozitif (min +3.86%) — nadiren görülür. Trade count düşük (38), daha fazla iter lazım.

---

### 6. `QL_DEEPAK_153_FILTER_1D` / ETHUSDT / 2h ⭐⭐
| Metrik | Değer |
|---|---|
| Sprint iters passed | 3/3 |
| **Excess (alpha)** | **+74.1%** |
| CPCV pass rate | **12/15 (80%)** |
| CPCV median return | +41.72% |
| CPCV min return | -13.34% |
| Profit factor | 1.658 |
| Boot p | 0.002 |
| DSR p | 0.3955 |

**Sınıf önerisi:** STRONG  
**Not:** Aynı strateji farklı sembol — SOLUSDT 2h ile birlikte değerlendir. DSR p yüksek — daha fazla itera gerekli.

---

## STANDARD Candidates (CPCV 40-60%)

### 7. `QL_SELL_RULES_MARKET_WIZARDS_OVERLAY` / ARBUSDT / 4h
- CPCV: 9/15 (60%), excess +110.2%, PF 1.571
- **Sınıf: STANDARD** (STRONG sınırında)

### 8. `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK` / NEARUSDT / 1h
- CPCV: 8/15 (53%), excess +128.2%, PF 1.732
- **Sınıf: STANDARD** (daha fazla iter gerekli)

### 9. `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` / OPUSDT / 2h
- CPCV: 8/15 (53%), excess +153.2%, PF 2.167
- **Sınıf: STANDARD** (PF çok iyi, daha fazla iter gerekli)

### 10. `GEN_MACD_BULL_CROSS` / SOLUSDT / 15m
- CPCV: 6/15 (40%), excess +117.7%, yüksek DD (-27.2%)
- **Sınıf: WATCH** (borderline STANDARD)

---

## FAIL (CPCV < 40% veya B&H negatif)

| Strateji | Sembol | TF | CPCV | Sebep |
|---|---|---|---|---|
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | OPUSDT | 1h | 20% | CPCV FAIL |
| `GEN_RSI_OVERSOLD_REVERSAL` | LTCUSDT | 1h | 33% | CPCV borderline FAIL |
| 72 TRXUSDT/XRP hücreleri | çeşitli | çeşitli | — | B&H alpha negatif |

---

## Barış İçin Aksiyon Listesi

| Öncelik | Aksiyon | Strateji | Not |
|---|---|---|---|
| 🔴 YÜKSEK | Promote ELITE onayı | SP500_TWO_CANDLE ADAUSDT 1h | Tüm gatelar güçlü, DSR p=0.015 |
| 🔴 YÜKSEK | Promote ELITE onayı | 8EMA_EXIT_TRAIL LINKUSDT 1h | PF=2.038, tüm gatelar güçlü |
| 🟡 ORTA | Sabah iteri kontrol et, ELITE karar | DEEPAK_153 SOLUSDT 2h | DSR yüksek — gece iter sonrası yeniden bak |
| 🟡 ORTA | STRONG/ELITE karar | OPEN_RANGE NEARUSDT 4h | Yüksek alpha ama yüksek DD |
| 🟢 DÜŞÜK | STRONG karar | CANDLESTICK_7 APTUSDT 1h | Trade count düşük, izle |
| 🟢 DÜŞÜK | STANDARD karar | DEEPAK_153 ETHUSDT 2h | DSR yüksek — daha fazla iter |

---

## Gece Loop Durumu

Sabah 06:00 deadline. Process PID 34672 çalışıyor.  
Sabah log: `overnight_runs/night_loop_2026-06-01.log`  
Her iter: `sprint_runs/v2_night_iter_N_*.json`

Sabah yapılacak:
1. `python aggregate_overnight_iters.py --runs-dir sprint_runs --out sprint_runs/SPRINT_AGGREGATED_REPORT_v2.md`
2. `python buy_hold_baseline.py --sprint-dir sprint_runs --out sprint_runs/BH_BASELINE_v2.md`
3. Bu raporu güncelle — promotion kararları ver
