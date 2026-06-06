# 1. Gate 1 — Candidate Intake Score / 100

## Amaç

Bu aşama şu soruya cevap verir:

```text
Bu stratejiyi kodlamaya ve backtest etmeye değer mi?
```

Bu aşamada performans puanlanmaz. Çünkü henüz backtest yapılmamıştır.

---

# Gate 1 Puanlama Tablosu

| Kategori | Puan |
|---|---:|
| 1. Kural netliği ve determinizm | 25 |
| 2. Algo kodlanabilirlik | 20 |
| 3. Preliminary repaint / lookahead risk | 15 |
| 4. Trade lifecycle definition | 15 |
| 5. Veri ve backtest yapılabilirliği | 10 |
| 6. Execution realism ön değerlendirme | 10 |
| 7. Strategy edge hypothesis | 5 |
| **Toplam** | **100** |

---

# 1.1. Kural Netliği ve Determinizm — 25 Puan

| Alt Kriter | Puan |
|---|---:|
| Entry rule explicit: giriş şartları net | 6 |
| Exit yaklaşımı net | 5 |
| Long / short / flat durumları tanımlı | 4 |
| Aynı mumda çakışma kuralları tanımlı | 4 |
| Parametreler net: EMA length, RSI threshold, ATR multiplier vb. | 3 |
| İnsan yorumu gerektirmiyor | 3 |
| **Toplam** | **25** |

---

# 1.2. Algo Kodlanabilirlik — 20 Puan

| Alt Kriter | Puan |
|---|---:|
| Kurallar Pine Script / Python ile doğrudan yazılabilir | 5 |
| Manuel trendline, göz kararı destek/direnç, subjektif pattern gerektirmez | 5 |
| Tüm girdiler sayısal, boolean veya açık koşul olarak ifade edilebilir | 4 |
| State machine olarak modellenebilir | 3 |
| TradingView ve Python backtest motorunda aynı mantık üretilebilir | 3 |
| **Toplam** | **20** |

---

# 1.3. Preliminary Repaint / Lookahead Risk — 15 Puan

Bu aşamada kesin doğrulama yapılmaz. Sadece ön risk puanı verilir.

| Alt Kriter | Puan |
|---|---:|
| Sinyal sadece kapanmış mum verisiyle oluşuyor gibi görünüyor | 4 |
| Gelecek mum bilgisi kullanma riski düşük | 4 |
| Higher timeframe kullanıyorsa lookahead riski yönetilebilir görünüyor | 3 |
| Pivot / fractal / zigzag / divergence gibi riskli yapı yok veya güvenli tanımlı | 2 |
| Real-time sinyal ile backtest sinyalinin uyumlu olma ihtimali yüksek | 2 |
| **Toplam** | **15** |

## Preliminary Repaint Risk Sınıfları

```text
LOW_RISK:
Standart close-based EMA, RSI, MACD, ATR gibi indikatörlere dayanır.

MEDIUM_RISK:
Higher timeframe, confirmation veya gecikmeli sinyal yapısı vardır ama yönetilebilir görünür.

HIGH_RISK:
Pivot, fractal, divergence, supply/demand, zigzag veya sonradan kesinleşen yapı kullanır.

UNKNOWN_NEEDS_CODE:
Transcript yeterli değildir. Kod veya replay testi gerekir.

REJECT_REPAINT:
Açık şekilde repaint, future leak veya hindsight mantığı vardır.
```

---

# 1.4. Trade Lifecycle Definition — 15 Puan

Bu başlık klasik risk yönetimi değildir. Amaç stratejinin işlem yaşam döngüsünü netleştirmektir.

| Alt Kriter | Puan |
|---|---:|
| Entry sinyali net | 3 |
| Logical exit var mı veya exit MTC’ye devredildi mi net | 3 |
| Opposite signal davranışı net | 3 |
| Re-entry / cooldown / pyramiding davranışı net | 2 |
| Flat / long / short state mantığı net | 2 |
| Backtestte hangi exit modelinin kullanılacağı net | 2 |
| **Toplam** | **15** |

## Kabul Edilebilir Tanım Örneği

```text
Strategy type: Entry-only signal strategy.
Exit model: MTC_v2 standard ATR SL + ATR TP + optional trailing stop.
Opposite signal: Close current position and optionally reverse.
Position sizing: Delegated to MTC_v2.
```

## Zayıf Tanım Örneği

```text
Videoda giriş anlatılıyor ama çıkış trader’ın kararına bırakılıyor.
```

---

# 1.5. Veri ve Backtest Yapılabilirliği — 10 Puan

| Alt Kriter | Puan |
|---|---:|
| Gerekli veri mevcut: OHLCV, volume, session vb. | 3 |
| Veri granularity uygun: 1m, 5m, 15m, 1h vb. | 2 |
| Göstergeler geçmiş veriyle hesaplanabilir | 2 |
| Komisyon / spread / slippage modele eklenebilir | 2 |
| Yeterli işlem üretme potansiyeli var | 1 |
| **Toplam** | **10** |

---

# 1.6. Execution Realism Ön Değerlendirme — 10 Puan

| Alt Kriter | Puan |
|---|---:|
| Emir tipi net: market, limit, stop, close-on-bar | 2 |
| İşlem açma zamanı net | 2 |
| Spread ve slippage etkisi tahmin edilebilir | 2 |
| Likiditeye aykırı varsayım yok | 1 |
| Intrabar belirsizlikleri yönetilebilir | 1 |
| Aşırı latency bağımlılığı yok veya açıkça kabul edilmiş | 2 |
| **Toplam** | **10** |

---

# 1.7. Strategy Edge Hypothesis — 5 Puan

| Alt Kriter | Puan |
|---|---:|
| Stratejinin mantıklı bir piyasa hipotezi var | 3 |
| Hangi piyasa rejiminde çalışması beklendiği belli | 2 |
| **Toplam** | **5** |

## Örnek

```text
Trend-following strategy.
Expected to perform better during high momentum and trending regimes.
Expected weakness: sideways / low-volatility markets.
```

---

# Gate 1 Karar Eşikleri

| Puan | Karar |
|---:|---|
| 85–100 | Güçlü aday. Kodlama ve backtest için uygun. |
| 75–84 | İyi aday. Küçük eksikler tamamlanıp backtest yapılabilir. |
| 60–74 | Şüpheli aday. Önce strateji tanımı iyileştirilmeli. |
| 40–59 | Zayıf aday. Kodlama/backtest zamanı harcamaya değmeyebilir. |
| 0–39 | Reddedilmeli. |

---

# Gate 1 Minimum Geçiş

```text
Minimum pass score: 75 / 100
```

---

# Gate 1 Hard Fail Sebepleri

Aşağıdakilerden biri varsa strateji Gate 1’i geçmemelidir:

```text
- Kodlanamaz.
- İnsan yorumu gerektirir.
- Entry rule belirsizdir.
- Trade lifecycle belirsizdir.
- Açık repaint / lookahead / future leak vardır.
- Test için gerekli veri yoktur.
- Hangi mumda sinyal ürettiği belli değildir.
- Strateji sadece görsel yoruma dayanır.
```
