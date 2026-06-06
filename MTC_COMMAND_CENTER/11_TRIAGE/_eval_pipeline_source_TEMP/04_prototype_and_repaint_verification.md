# 3. Prototype / Strategy Code

## Amaç

Stratejinin ilk kodlanabilir versiyonunu üretmek.

---

# Çıktılar

```text
- Pine Script strategy prototype
- Python backtest implementation veya MTC-compatible strategy module
- Parameter file
- Strategy metadata
- Signal contract draft
- Test dataset definition
```

---

# Minimum Kodlama Gereklilikleri

```text
- Entry rules implemented
- Exit model implemented or delegated to MTC_v2
- No manual interpretation
- Bar close / intrabar behavior explicit
- Fees and slippage configurable
- Long / short / flat state explicit
- Version number included
```

---

# 4. Repaint / Lookahead Verification

## Amaç

Gate 1’de yapılan preliminary repaint değerlendirmesini kod üzerinde doğrulamak.

---

# Kontrol Listesi

```text
- Sinyal sadece kapanmış mumda mı oluşuyor?
- barstate.isconfirmed gerekiyor mu?
- request.security kullanılıyorsa lookahead güvenli mi?
- Higher timeframe veri [1] ile mi kullanılıyor?
- Pivot / fractal sinyalleri kaç bar sonra kesinleşiyor?
- ZigZag veya sonradan değişen yapı var mı?
- TradingView replay testte sinyal kayboluyor mu?
- Python backtest ile Pine sinyalleri eşleşiyor mu?
- Intrabar hesaplama ile bar-close hesaplama farkı var mı?
```

---

# Sonuç Sınıfları

```text
VERIFIED_SAFE:
Kod repaint/lookahead açısından güvenli görünüyor.

SAFE_WITH_DELAY:
Sinyal gecikmeli ama güvenli şekilde kullanılabilir.

NEEDS_MODIFICATION:
Kodda repaint/lookahead riski var, düzeltme gerekir.

REJECT_REPAINT:
Strateji güvenli şekilde test edilemez.
```

---

# Hard Fail

```text
REJECT_REPAINT sonucu alınırsa Gate 2’ye geçilmez.
```
