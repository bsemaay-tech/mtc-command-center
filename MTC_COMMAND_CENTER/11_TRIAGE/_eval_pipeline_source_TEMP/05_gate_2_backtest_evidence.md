# 5. Gate 2 — Backtest Evidence Score / 100

## Amaç

Bu aşama şu soruya cevap verir:

```text
Backtest sonucu stratejinin gerçekten potansiyeli olduğunu gösteriyor mu?
```

---

# Gate 2 Puanlama Tablosu

| Kategori | Puan |
|---|---:|
| 1. Performans kalitesi | 20 |
| 2. Risk / drawdown davranışı | 20 |
| 3. Trade sample kalitesi | 15 |
| 4. Robustness / overfitting dayanıklılığı | 20 |
| 5. Maliyet sonrası gerçekçilik | 10 |
| 6. Benchmark comparison | 10 |
| 7. Rejim analizi | 5 |
| **Toplam** | **100** |

---

# 5.1. Performans Kalitesi — 20 Puan

| Alt Kriter | Puan |
|---|---:|
| Net profit pozitif ve anlamlı | 3 |
| Profit Factor güçlü | 4 |
| Expectancy pozitif | 4 |
| Average trade maliyetlerden sonra yeterli | 3 |
| Equity curve sağlıklı | 3 |
| Long/short performansı ayrı ayrı kabul edilebilir | 3 |
| **Toplam** | **20** |

---

# 5.2. Risk / Drawdown Davranışı — 20 Puan

| Alt Kriter | Puan |
|---|---:|
| Max drawdown kabul edilebilir | 5 |
| Consecutive losses makul | 4 |
| Drawdown sonrası toparlanma var | 4 |
| Equity curve uzun süre yatay veya çöküşte kalmıyor | 3 |
| Tek bir kötü dönemde hesabı mahvetmiyor | 4 |
| **Toplam** | **20** |

---

# 5.3. Trade Sample Kalitesi — 15 Puan

| Alt Kriter | Puan |
|---|---:|
| Trade count strateji tipine göre yeterli | 4 |
| Test süresi strateji tipine göre yeterli | 4 |
| Farklı piyasa rejimleri kapsanmış | 3 |
| Kazanç birkaç büyük trade’e bağlı değil | 2 |
| Long/short veya market dağılımı aşırı dengesiz değil | 2 |
| **Toplam** | **15** |

---

# Trade Count + Süre Kriterleri

| Strateji Tipi | Minimum Süre | Daha İyi Süre | Minimum Trade | Daha Güçlü Örneklem |
|---|---:|---:|---:|---:|
| Scalping | 6–12 ay | 1–2 yıl | 1000+ | 2000–5000+ |
| Intraday | 1 yıl | 2–3 yıl | 300+ | 500–1000+ |
| Swing | 3 yıl | 5 yıl+ | 100+ | 200–300+ |
| Position / Long-term | 5 yıl | 8–10 yıl | 30–50+ | 100+ |

---

# Trade Sample Değerlendirme Prensibi

```text
Trade count tek başına yeterli değildir.
Trade count + calendar duration + market regime coverage birlikte değerlendirilmelidir.
```

---

# 5.4. Robustness / Overfitting Dayanıklılığı — 20 Puan

| Alt Kriter | Puan |
|---|---:|
| Parametreler küçük değişince sistem bozulmuyor | 5 |
| Out-of-sample testte tamamen çökmez | 4 |
| Walk-forward test yapılabilir veya yapılmış | 3 |
| Farklı piyasa dönemlerinde çalışır | 3 |
| Benzer marketlerde makul davranır | 3 |
| Çok fazla optimize edilmiş özel parametre yok | 2 |
| **Toplam** | **20** |

---

# 5.5. Maliyet Sonrası Gerçekçilik — 10 Puan

| Alt Kriter | Puan |
|---|---:|
| Komisyon eklenince hâlâ çalışıyor | 3 |
| Slippage eklenince hâlâ çalışıyor | 3 |
| Spread etkisi stratejiyi öldürmüyor | 2 |
| Average trade maliyetlere göre yeterince büyük | 2 |
| **Toplam** | **10** |

---

# 5.6. Benchmark Comparison — 10 Puan

| Alt Kriter | Puan |
|---|---:|
| Buy & Hold’a göre daha iyi risk-adjusted sonuç | 3 |
| Max drawdown Buy & Hold’dan anlamlı düşük | 2 |
| Return / Max Drawdown oranı daha iyi | 2 |
| Daha düşük exposure ile benzer veya daha iyi getiri | 2 |
| Basit benchmark stratejilere karşı üstünlük | 1 |
| **Toplam** | **10** |

---

# Kullanılacak Benchmark Seti

```text
1. Buy & Hold
2. Cash / No Trade
3. Simple EMA 50/200 trend-following strategy
4. Same market, same period, same fee/slippage settings
```

---

# Benchmark Değerlendirme Notu

Sadece net kâr karşılaştırması yeterli değildir.

Karşılaştırılacak metrikler:

```text
- Net return
- Max drawdown
- Return / Max Drawdown
- Exposure-adjusted return
- Sharpe
- Sortino
- Profit factor
- Recovery factor
```

---

# 5.7. Rejim Analizi — 5 Puan

| Alt Kriter | Puan |
|---|---:|
| Trend / range / yüksek volatilite / düşük volatilite ayrımı yapılmış | 3 |
| Stratejinin hangi rejimde zayıf olduğu biliniyor | 2 |
| **Toplam** | **5** |

---

# Gate 2 Karar Eşikleri

| Puan | Karar |
|---:|---|
| 85–100 | Güçlü backtest adayı. Forward test / paper trade aşamasına geçebilir. |
| 75–84 | İyi aday. Daha fazla robustness testi gerekebilir. |
| 60–74 | Zayıf ama geliştirilebilir. Mantık gözden geçirilmeli. |
| 40–59 | Backtest sonucu yetersiz. Araştırma arşivine alınabilir. |
| 0–39 | Reddedilmeli. |

---

# Gate 2 Minimum Geçiş

```text
Minimum pass score: 75 / 100
```

---

# Gate 2 Hard Fail Sebepleri

```text
- Komisyon/slippage sonrası sistem negatife dönüyor.
- Buy & Hold’a göre hiçbir anlamlı avantaj yok.
- Out-of-sample test tamamen çöküyor.
- Parametreler küçük değişince sistem bozuluyor.
- Max drawdown kabul edilemez seviyede.
- İşlem sayısı strateji tipine göre çok az.
- Test süresi strateji tipine göre çok kısa.
- Kazanç birkaç büyük trade’e bağlı.
- Equity curve sadece tek bir piyasa döneminde yükselmiş.
```
