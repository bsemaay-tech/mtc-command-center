# Next Action

## Recommended Next Step (2026-06-01 DeepSeek V4 Pro)
Q Trend → **FILTER_OVERLAY**. Mevcut stratejilere confirmation/guard filter olarak bağlanabilir.
Diğer 4 indikatör (QQE, UT Bot, Pivot SuperTrend, Lorentzian) SALVAGE_ONLY — henüz split edilmedi.

## Q Trend Classification
- **Rol:** FILTER_OVERLAY (confirmation / guard)
- **Standalone edge:** Yok (backtest: cross-fold tutarsız, yüksek DD)
- **Kullanım:** `change_up` trend yönü filtresi, `strong_buy` kalite filtresi
- **Pine:** `00_INBOX_REPORTS/1 Haziran/Stg Q Trend/Q Trend.pine`
- **Python:** `overnight_v2_runner.py` → `_qtrend_signal()`

## QQE Signals Classification (2026-06-01 gece — Claude Sonnet 4.6)

Pine kaynak repo'da bulunmadı. QQE formülü (standart: double-smooth RSI + ATR band) Python'a implement edildi: `overnight_v2_runner.py → QL_QQE_SIGNALS`.

**Backtest sonuçları:**
- SOLUSDT 2h (108 param, full run): fold +53.9% avg ama lockbox **-14.7%** PF=0.91 → FAIL (fold-to-lockbox gap: overfitting)
- BTCUSDT 4h (single call): lockbox +14% PF=1.76 ama 17 trade → INSUFFICIENT_TRADES

**Klasifikasyon: FILTER_OVERLAY** (Q Trend ile aynı)  
Standalone edge yok. Overselective (az trade) veya folds-lockbox uyuşmazlığı var.  
Kullanım: RSI momentum konfirmasyon filtresi olarak entegre edilebilir.

**Devam Koşulu:**  
QL_QQE_SIGNALS overnight loop'a eklendi (43. strateji). Yeterli iter sonrası robust PASS görünürse yeniden değerlendir.

## Remaining Indicators (UT Bot, Pivot SuperTrend, Lorentzian)
- **UT Bot Alert** (Quant Nomad): ATR trailing stop alert. Implementasyon: atr_factor * ATR trailing band. Barış Pine kaynağı sağlarsa Python'a eklenebilir.
- **Pivot Point SuperTrend** (lonesome the blue): Pivot hesabı + SuperTrend kombine. Barış Pine kaynağı sağlarsa Python'a eklenebilir.
- **Lorentzian Classification** (JD Horty): ML tarzı — Lorentzian distance ile KNN. Complex implementation, Barış önceliklendirir.

**Pickup trigger:** Barış her biri için Pine source sağlar veya backtest önceliği verir.
