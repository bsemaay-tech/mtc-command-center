# 6. Gate 3 — MTC Production Readiness Score / 100

## Amaç

Bu aşama şu soruya cevap verir:

```text
Bu strateji MTC_v2 içinde güvenli, izlenebilir ve otomasyon pipeline’ına uygun şekilde çalıştırılabilir mi?
```

Bu aşama backtestten sonra yapılır.

---

# Gate 3 Puanlama Tablosu

| Kategori | Puan |
|---|---:|
| 1. Signal contract uygunluğu | 25 |
| 2. Alert / execution adapter uygunluğu | 20 |
| 3. State synchronization | 15 |
| 4. MTC risk engine tam uyum | 15 |
| 5. Monitoring / logging / debug | 10 |
| 6. Fail-safe / operational safety | 10 |
| 7. Versioning / reproducibility | 5 |
| **Toplam** | **100** |

---

# 6.1. Signal Contract Uygunluğu — 25 Puan

| Alt Kriter | Puan |
|---|---:|
| Strateji net sinyal üretiyor: long, short, close, flat | 6 |
| Sinyal zamanı net: bar close, intrabar, confirmed signal vb. | 5 |
| Aynı mumda çakışma davranışı tanımlı | 4 |
| Sinyal unique ID / timestamp / symbol / timeframe ile tanımlanabilir | 4 |
| Entry ve logical exit ayrı işaretlenebilir | 3 |
| Strategy metadata üretilebilir | 3 |
| **Toplam** | **25** |

## Örnek Signal Contract

```json
{
  "strategy_id": "ema_rsi_breakout_v1",
  "symbol": "BTCUSDT",
  "timeframe": "15m",
  "signal": "LONG_ENTRY",
  "bar_time": "2026-06-02T12:00:00Z",
  "confirmed": true,
  "reason": "EMA20>EMA50 + RSI>55 + breakout"
}
```

---

# 6.2. Alert / Execution Adapter Uygunluğu — 20 Puan

| Alt Kriter | Puan |
|---|---:|
| TradingView alert JSON’a çevrilebilir | 5 |
| Entry / exit / reduceOnly ayrımı yapılabilir | 4 |
| Duplicate alert engellenebilir | 3 |
| Bot tarafında market/limit/close emri üretilebilir | 3 |
| Partial fill / failed order durumları MTC tarafından yönetilebilir | 3 |
| Alert mesajı deterministik ve parse edilebilir | 2 |
| **Toplam** | **20** |

---

# 6.3. State Synchronization — 15 Puan

| Alt Kriter | Puan |
|---|---:|
| Strategy state ile broker/bot position state karşılaştırılabilir | 4 |
| Flat / long / short durumu net takip edilebilir | 4 |
| Missed alert durumunda yeniden senkronize edilebilir | 3 |
| Aynı anda birden fazla pozisyon mantığı açık | 2 |
| Restart sonrası strateji durumu yeniden hesaplanabilir | 2 |
| **Toplam** | **15** |

---

# 6.4. MTC Risk Engine Tam Uyum — 15 Puan

| Alt Kriter | Puan |
|---|---:|
| MTC default SL / TP / trailing ile çalışabilir | 4 |
| Strateji özel stop istiyorsa bunu açıkça verebilir | 3 |
| Reverse / re-entry / cooldown davranışı MTC’ye aktarılabilir | 3 |
| Pyramiding destekleniyor mu, yasak mı net | 2 |
| Risk engine ile çelişen özel emir mantığı yok | 3 |
| **Toplam** | **15** |

---

# 6.5. Monitoring / Logging / Debug — 10 Puan

| Alt Kriter | Puan |
|---|---:|
| Sinyal sebebi loglanabilir | 3 |
| Parametreler loglanabilir | 2 |
| Backtest trade ile live alert eşleştirilebilir | 2 |
| Hata ayıklamak için yeterli metadata üretilebilir | 2 |
| Versiyon numarası taşır | 1 |
| **Toplam** | **10** |

---

# 6.6. Fail-safe / Operational Safety — 10 Puan

| Alt Kriter | Puan |
|---|---:|
| Strateji MTC circuit breaker ile uyumlu | 2 |
| Max daily loss kuralı ile çelişmez | 2 |
| Manual override durumunda davranışı net | 2 |
| Exchange/bot hata durumlarında güvenli kalabilir | 2 |
| Beklenmeyen sinyal durumunda no-trade / flat davranışı tanımlı | 2 |
| **Toplam** | **10** |

---

# 6.7. Versioning / Reproducibility — 5 Puan

| Alt Kriter | Puan |
|---|---:|
| Strategy version sabitlenmiş | 1 |
| Parameter set kaydedilmiş | 1 |
| Backtest dataset ve tarih aralığı kaydedilmiş | 1 |
| Fee/slippage varsayımları kaydedilmiş | 1 |
| Aynı sonuç tekrar üretilebilir | 1 |
| **Toplam** | **5** |

---

# Gate 3 Karar Eşikleri

| Puan | Karar |
|---:|---|
| 85–100 | MTC_v2 entegrasyonuna güçlü şekilde uygun. |
| 75–84 | Entegrasyona uygun. Küçük adapter eksikleri giderilmeli. |
| 60–74 | MTC’ye alınmadan önce signal contract / adapter netleştirilmeli. |
| 40–59 | Entegrasyon riski yüksek. |
| 0–39 | MTC_v2 içinde çalıştırılmamalı. |

---

# Gate 3 Minimum Geçiş

```text
Minimum pass score: 75 / 100
```

---

# Gate 3 Hard Fail Sebepleri

```text
- Alert güvenilmez.
- Duplicate signal kontrolü yok.
- Broker state ile strategy state eşleşemiyor.
- Exit / reduceOnly ayrımı belirsiz.
- Signal contract yok.
- Log/debug için yeterli metadata yok.
- Fail-safe davranışı yok.
- MTC risk engine ile çelişiyor.
```
