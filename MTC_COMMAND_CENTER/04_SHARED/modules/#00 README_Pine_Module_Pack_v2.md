# 📦 Pine Module Pack v2 – Kullanım Kılavuzu

> **AI-ready, Non-repainting**  
> Pine Script v5/v6 strateji sistemleri için standart modül kütüphanesi.  
> **Engine Integration:** MASTER_TEMPLATE_CORE.pine (v2.2.0-LibRefactor, Pine v6)
> **Module Compatibility:** Pine v5 modules integrated via TradingView libraries (Supertrend, Range Filter, Confirmation Layer)

**Güncelleme (24 Ocak 2026 – v1.3.9-rf-patch):**
- Supertrend, Range Filter ve Confirmation katmanı TradingView **library** olarak ayrıldı.
- **Signal mode consolidation**: Sadece 2 mode aktif — Supertrend ve Range Filter Hybrid (diğer 8 mode prune edildi; reintegrate için Module Pack v2 mevcut)
- Export edilen fonksiyonlar içinde `request.security()` ifadesi **argümanlara bağlı olamaz**; HTF hesapları host scriptte yapılmalı.
- İmport örneği: `import bsemaay3/LIB_Signal_Supertrend_Fix/1 as ST`.
- Not: Orijinal `LIB_Signal_Supertrend` yayını gizlendiği için aktif yayın adı `LIB_Signal_Supertrend_Fix`.
- Section 11 doc sync: Exit Stats & Filter Block Tags API referansı (core tarafında `exitReasonStats[]`, `fbBlocked[]`, `fbWin[]`, `fbLoss[]`).
- Supertrend library fix: classic wick handling + level signals restored to match pre-library behavior.

**Güncelleme (25 Ocak 2026 – v1.3.9-rf-patch):**
- Core engine UI tooltips expanded; debug regression fingerprint added (engine-only, module pack unchanged).
- Warning fix: cache `ta.change(strategy.closedtrades)` into `closedTradesChanged` to avoid conditional execution warnings (engine-only).

**Güncelleme (26 Ocak 2026 – v1.3.9-rf-patch):**
- HTF bar-close confirmation + bar-close entry gate added to prevent intrabar drift/ghost orders (engine-only).

**Güncelleme (01 Şubat 2026 – v2.2.0-LibRefactor):**
- **Library Migration**: Helper functions moved to `LIB_MATH`, `LIB_SLTP`, `LIB_WT` libraries.
- **Strict Casting**: `float(na)` required for library calls to satisfy type safety.
- **Cleanup**: Modularized codebase (~800 lines reduced).

---

## 🆕 CURRENT MTC SIGNAL MODES (v2.2.0-LibRefactor)

### ✅ Active Signal Modes (Ready to Use)

| Mode | Library | Adapters | Inputs Group | Use Case |
|------|---------|----------|--------------|----------|
| **Supertrend** (MODE_SUPERTREND=1) | [LIB_Signal_Supertrend.pine](LIB_Signal_Supertrend.pine) | Section 4 (MODE_SUPERTREND case) | grpSignalST | ATR-based trend reversal; optional Heikin Ashi |
| **Range Filter Hybrid** (MODE_RANGE_FILTER=20) | [LIB_Signal_RangeFilter.pine](LIB_Signal_RangeFilter.pine) | Section 4 (MODE_RANGE_FILTER case) | grpSignalRF | Regime-adaptive: ADX+Chop trending, BB+RSI ranging |
| **None** (MODE_NONE=0) | N/A | N/A | N/A | Signals disabled; engine runs on filters/guards only |

### ❌ Pruned Signal Modes (v1.3.8 → v1.3.9-rf-patch)

These 8 modes were removed from core to reduce complexity. **Code preserved in Module Pack v2** for reintegration if needed:

| Removed Mode | Reason | Recovery |
|--------------|--------|----------|
| EMA Cross (MODE_EMA_CROSS=2) | Unused in v1.3.x; simple alternative to Supertrend | Find `f_emaCross_v1()` in [#01 Pine_Module_Pack_v2.md](#01%20Pine_Module_Pack_v2.md) |
| Donchian Breakout (MODE_DONCHIAN=3) | Channel-based, overlaps Range Filter | Find `f_donchian_signal()` in Module Pack v2 |
| MACD Signal (MODE_MACD=4) | Superseded by MACD Filter Hub (confirmation layer) | MACD Hub available in grpFilters |
| RSI Reversal (MODE_RSI=5) | Replaced by Range Filter's RSI component | RS component in `LIB_Signal_RangeFilter` |
| Bollinger Bands (MODE_BBANDS=6) | Replaced by Range Filter's BB mean reversion | BB logic in `LIB_Signal_RangeFilter` |
| Stochastic (MODE_STOCH=7) | Overlaps secondary confirmation role | Use `f_secondaryConfirm_v1` as filter instead |
| Williams %R (MODE_WILLIAMS=8) | Limited unique edge | Use `f_secondaryConfirm_v1` for similar logic |
| Parabolic SAR (MODE_PSAR=9) | Rarely used; kept as learning example | Find `f_psar_signal()` in Module Pack v2 |

### 🔄 How to Re-add a Pruned Mode

If you need EMA Cross or another pruned mode:

1. **Find the code**: Search [#01 Pine_Module_Pack_v2.md](#01%20Pine_Module_Pack_v2.md) for function (e.g., `f_emaCross_v1`)
2. **Add inputs**: Copy inputs to Section 1, group = grpSignalEMA, active = (mode == "EMA Cross")
3. **Add function**: Copy function to Section 2 (after grpSignalRF inputs, before f_trailing)
4. **Add mode constant**: `int MODE_EMA_CROSS = 2`
5. **Update dropdown**: Add "EMA Cross" to `signal_mode` options
6. **Add case in Section 4.1**:
   ```pine
   else if signal_mode == "EMA Cross"
       [_line, _dir, _long, _short] = f_emaCross_v1(close, ema_fast_len, ema_slow_len)
       signalLine := _line
       signalDir  := _dir
       longSignal_raw := _long
       shortSignal_raw := _short
   ```

---

## 🤖 LLM / AI ASSISTANT TALİMATLARI

> **Bu bölümü ilk oku!** Eğer bu dosyayı okuyan bir AI asistansan (GPT, Claude, Copilot, vb.),
> aşağıdaki talimatları takip et.

### 🎯 Current MTC Configuration (v1.3.9-rf-patch)

**Active signal modes in MASTER_TEMPLATE_CORE.pine:**
- ✅ **Supertrend** (ATR trend reversal)
- ✅ **Range Filter Hybrid** (ADX+Chop+BB regime-adaptive)
- ✅ **None** (signals disabled)

**When a user asks to add/change a signal mode:**
- If they ask for "EMA Cross", "Donchian", "MACD", "RSI", "Bollinger Bands", "Stochastic", "Williams %R", or "Parabolic SAR" → These were pruned. **See "How to Re-add a Pruned Mode" section above** for recovery steps.
- If they ask for something else → Check [#01 Pine_Module_Pack_v2.md](#01%20Pine_Module_Pack_v2.md) for the module definition, then follow integration workflow below.

### 📁 Dosya Haritası

```
20_MODULES_REUSABLE/
├── #01 Pine_Module_Pack_v2.md              ← KAYNAK: 45 modülün kod tanımları
├── LIB_Signal_Supertrend.pine              ← Active library
├── LIB_Signal_RangeFilter.pine             ← Active library
├── LIB_ConfirmationLayer.pine              ← Confirmation layer library
└── ...

00_MASTER_TEMPLATE/
├── MASTER_TEMPLATE_CORE.pine               ← HEDEF: Modüllerin entegre edileceği strateji (v1.3.9-rf-patch)
└── #00 README_Pine_Module_Pack_v2.md       ← BU DOSYA: Kullanım kılavuzu
├── MASTER_TEMPLATE_CORE_README.md          ← Engine contract + Section structure
└── CHANGELOG.md                            ← Session history (including v1.3.9-rf-patch and v1.3.8)
```

### 🎯 Temel İş Akışı

Kullanıcı bir modül eklemeni istediğinde:

1. **Check availability:** Is it one of the 2 active modes (Supertrend, Range Filter Hybrid)? No → Check if it's pruned (8 modes listed above). Yes → Use "How to Re-add" section.
2. **Modül kodunu bul:** `#01 Pine_Module_Pack_v2.md` dosyasından fonksiyon tanımını oku
3. **Helper kontrolü:** `f__confirmed()`, `f__ma()`, `f__clamp01()` mevcut mu kontrol et
4. **Modülü ekle:** MASTER_TEMPLATE_CORE.pine → **Section 2** (fonksiyonlar bölümü)
5. **Input ekle:** Gerekli parametreler için Section 1'e input.xxx() ekle
6. **Section 4'te çağır:** Module adapter pattern'e yeni case ekle
7. **signal_mode seçeneklerini güncelle:** input.string options dizisine ekle
8. **Update CHANGELOG.md** after the change (see [.github/copilot-instructions.md](../../.github/copilot-instructions.md) for documentation workflow)

### ❌ YAPMA

- Section 4'te `strategy.entry()`, `strategy.exit()`, `strategy.close()` ÇAĞIRMA
- Section 5, 6'yı DEĞİŞTİRME (Risk engine, visualization)
- `longSignal_raw` ve `shortSignal_raw` dışında başka sinyal değişkeni OLUŞTURMA
- Modül çağrısında HTF request.security() için lookahead_on KULLANMA

### ✅ YAP

- Section 4'te SADECE `longSignal_raw` ve `shortSignal_raw` değişkenlerini ata
- Tüm modülleri Section 2'ye, `f_trailing()` fonksiyonundan ÖNCE ekle
- Standart arayüzü kullan: `[line, dir, longRaw, shortRaw]`
- Input'ları grpSignal grubuna ekle

### � Understanding MTC Code Structure for LLMs

**Master Template Core (MTC)** is a ~4.5k-line Pine Script v6 engine divided into strict sections:

| Section | Lines | Purpose | Edit Policy |
|---------|-------|---------|-------------|
| **Section 1** | ~400 | Input groups and user parameters | ✅ EDIT when adding new signal mode (add inputs for new mode parameters) |
| **Section 2** | ~1500 | Function definitions (helpers, signal modules, risk calcs) | ✅ EDIT when adding new signal module (add function before `f_trailing()`) |
| **Section 3** | ~800 | Derived filters, guards, warmup bars | ⚠️ EDIT SPARINGLY (understand existing dependencies) |
| **Section 4 (SIGNAL PLUGIN)** | ~400 | **Signal adapter socket** — maps active signal mode to `longSignal_raw` / `shortSignal_raw` | ✅ EDIT ONLY Section 4.1 (add case for new mode) |
| **Sections 5+** | ~1200 | Risk engine, SL/TP/BE/Multi-TP, trailing, daily limits, trade manager, alerts | ❌ NEVER EDIT |

**Critical constraint**: Section 4 is the **signal plugin interface**. Must output **exactly**:
- `longSignal_raw: bool` — raw long signal before filters
- `shortSignal_raw: bool` — raw short signal before filters

Then the engine applies filters (MA, filters, guards) → final `longSignal`/`shortSignal` that drives trade logic.

**Default ONLY edit Section 4.1 when adding new signal modes.** Examples:

- **Supertrend mode** (active): Section 4.1 uses `LIB_Signal_Supertrend` library, unpacks output to `longSignal_raw`/`shortSignal_raw`
- **Range Filter Hybrid** (active): Section 4.1 uses `LIB_Signal_RangeFilter` library, same pattern
- **Future EMA Cross** (if re-added): Add new case in Section 4.1 calling `f_emaCross_v1()`, assign outputs

### �📋 Section 4 Değişken Referansı

| Değişken | Yazılabilir mi? | Açıklama |
|----------|-----------------|----------|
| `longSignal_raw` | ✅ := | Ana long sinyal (modül çıkışı) |
| `shortSignal_raw` | ✅ := | Ana short sinyal (modül çıkışı) |
| `signalLine` | ✅ := | Görselleştirme için plot line (generic) |
| `signalDir` | ✅ := | Yön göstergesi (+1/-1) |
| `longSignal` | ❌ DOKUNMA | Final sinyal (filtreler uygulanmış) |
| `shortSignal` | ❌ DOKUNMA | Final sinyal (filtreler uygulanmış) |
| `longEdge` | ❌ DOKUNMA | Edge trigger (tekrar girişi önler) |
| `shortEdge` | ❌ DOKUNMA | Edge trigger |

---

## ⚠️ CRITICAL GOTCHAS (KRİTİK UYARILAR)

> **Bu bölümü mutlaka oku!** Aşağıdaki gotcha'lar sık yapılan hatalar ve beklenmeyen davranışlardır.

### 1️⃣ HTF (Higher Timeframe) Filter Lag

```
⚠️ HTF filters update ONLY when the HTF bar closes!
```

- `f_htfTrendFilter_v1` ve benzeri HTF modülleri, LTF (lower timeframe) chart'ta kullanıldığında **intrabar değişebilir** ama HTF bar kapanana kadar **confirm olmaz**.
- Backtest'te görünen HTF crossover, live trade'de 1-2 HTF bar gecikebilir.
- **Öneri:** HTF filters'ı primary signal DEĞİL, confirmation olarak kullan.

### 2️⃣ NA Propagation (Silent Failures)

```
⚠️ na values can silently break boolean chains!
```

- Modül çıkışları na içerirse: `longRaw and na = na` (false DEĞİL, na!)
- Bu durum `longSignal_raw` ve `shortSignal_raw`'ı bozabilir.
- **Kontrol:** Modül fonksiyonlarında `not na()` guard'ları olduğundan emin ol.
- **Etkilenen modüller:** `f_srProximity_v1`, `f_pullbackEntry_v1`, `f_rsiDivergence_v1` (warmup döneminde)

### 3️⃣ Dir Semantics: Signals vs Guards

```
⚠️ dir meaning differs between signal modules and guard modules!
```

| Modül Tipi | dir = +1 | dir = -1 | dir = 0 |
|------------|----------|----------|---------|
| **Signal** (A/B) | Bullish trend | Bearish trend | Neutral |
| **Guard** (C/D) | **ALLOW** trade | **BLOCK** trade | N/A |

- Guard modülünü (ör: `f_maxDrawdownGuard_safe`) trend indicator olarak KULLANMA!
- Guard'ın `dir = -1` olması "bearish" DEĞİL, "trading halted" demektir.

### 4️⃣ Module Dependencies

```
⚠️ Some modules require warmup bars before producing valid signals!
```

- ATR-based modüller: `atrLen` kadar bar bekler
- Pivot-based modüller (`f_srProximity_v1`, `f_rsiDivergence_v1`): `swingLen * 2` bar bekler
- MA-based modüller: `maLen` kadar bar bekler
- **Öneri:** MASTER_TEMPLATE_CORE `warmupBars` değişkenini kontrol et.

### 5️⃣ Guard Modules Need Adapter Layer

```
⚠️ Guard modules (C category) use strategy.* internally!
```

- `f_dailyLossLimit_v1`, `f_maxDrawdownGuard_v1` vb. ENGINE-DEPENDENT'tir.
- Bunları Section 4'te doğrudan ÇAĞIRMA!
- **Doğru kullanım:** Section 3.5 Guard Adapter Layer'da `*_safe` versiyonlarını kullan.

---

## 🔗 MULTI-MODULE WORKFLOW (Çoklu Modül Entegrasyonu)

### Senaryo 1: Primary Signal + Filter Modules

```pine
// Section 4.1 - Primary signal
[_line, _dir, _long, _short] = f_supertrend_signal(...)
signalLine := _line
signalDir  := _dir

// Filter modules (confirmation)
[_, _, htfLongOk, htfShortOk] = f_htfTrendFilter_v1(close, "240", 50, "EMA", false, false)
[_, _, volOk, _]              = f_volumeAboveAvg_v1(20, 1.2, false)
[_, _, adxOk, _]              = f_adxRegime_v1(14, 20)

// Combine: primary signal + filters
longSignal_raw  := _long  and htfLongOk  and volOk and adxOk
shortSignal_raw := _short and htfShortOk and volOk and adxOk
```

### Senaryo 2: Quality Score Aggregation

```pine
// Multiple confirmation signals
[_, _, s1L, s1S] = f_htfTrendFilter_v1(...)
[_, _, s2L, s2S] = f_adxRegime_v1(...)
[_, _, s3L, s3S] = f_volumeAboveAvg_v1(...)
[_, _, s4L, s4S] = f_candlePattern_v1(...)
[_, _, s5L, s5S] = f_vwapConfluence_v1(...)

// Aggregate via quality score
[_, _, qualityLongOk, qualityShortOk] = f_signalQualityScore_v1(s1L, s2L, s3L, s4L, s5L, false)

longSignal_raw  := qualityLongOk
shortSignal_raw := qualityShortOk
```

### Senaryo 3: Adding a New Signal Mode

**Step 1:** Section 1 - Input ekle
```pine
signal_mode = input.string("Supertrend", "Signal Mode", 
     options = ["Supertrend", "Range Filter Hybrid (ADX+Chop+BB)", "MyModule", "None"],  // ← ekle
     ...)
     
mymodule_param = input.int(20, "MyModule Param", group = grpSignal)  // ← ekle
```

**Step 2:** Section 2 - Modül fonksiyonunu ekle
```pine
// f_donchian_signal() sonrasına, f_trailing() öncesine ekle
f_myModule_v1(...) =>
    // ... modül kodu ...
    [line, dir, longRaw, shortRaw]
```

**Step 3:** Section 4.1 - Adapter'a case ekle
```pine
    else if signal_mode == "MyModule"
        [_line, _dir, _long, _short] = f_myModule_v1(mymodule_param)
        signalLine := _line
        signalDir  := _dir
        longSignal_raw := _long
        shortSignal_raw := _short
```

### Senaryo 4: Disabling a Module via Toggle

```pine
// Section 1
use_htf_confirm = input.bool(true, "Use HTF Confirmation", group = grpSignal)

// Section 4.1
[_, _, htfL, htfS] = f_htfTrendFilter_v1(...)
bool htfLongOk  = use_htf_confirm ? htfL : true   // bypass if disabled
bool htfShortOk = use_htf_confirm ? htfS : true

longSignal_raw := _long and htfLongOk
```

---

## 🎯 Genel Bakış

Bu paket, Pine Script v5 stratejilerinde kullanılmak üzere tasarlanmış **modüler sinyal ve filtre** koleksiyonudur.

### Temel Özellikler

| Özellik | Açıklama |
|---------|----------|
| **Standart Arayüz** | Tüm modüller `[line, dir, longRaw, shortRaw]` döndürür (Libraries: 7-10 extended values) |
| **Non-repainting** | `barstate.isconfirmed` ile bar kapanışında sinyal |
| **Emir vermez** | Modüller sadece sinyal üretir, `strategy.entry/exit` çağırmaz |
| **Engine Integration** | Section 4.1 (SIGNAL PLUGIN) aracılığıyla MTC'ye entegre edilir |
| **Pine Versions** | MTC Engine: Pine v6 | Libraries: Pine v6 | Module Pack v2: Pine v5 (legacy modules) |

---

## 📐 Standart Modül Arayüzü

### Core Interface (Module Pack v2 - Legacy Modules)

```pine
[line, dir, longRaw, shortRaw] = f_moduleName_v1(...)
```

| Dönüş | Tip | Açıklama |
|-------|-----|----------|
| `line` | `float` | Görselleştirme için plot değeri |
| `dir` | `int` | Yön: `+1` (bullish), `-1` (bearish), `0` (nötr) |
| `longRaw` | `bool` | Long sinyal (true/false) |
| `shortRaw` | `bool` | Short sinyal (true/false) |

### Library Extended Interface (TradingView Libraries - v1.3.9+)

Libraries return **extended values** for visualization and debugging:

**LIB_Signal_Supertrend** (7 return values):
```pine
[line, dir, longRaw, shortRaw, aux1, aux2, aux3] = ST.sig_supertrend(...)
```
- `aux1-3`: Internal state variables for advanced visualization

**LIB_Signal_RangeFilter** (7 return values):
```pine
[line, dir, longRaw, shortRaw, bbUpper, bbLower, bbBasis] = RF.sig_rangefilter(...)
```
- `bbUpper/bbLower/bbBasis`: Bollinger Band levels for plotting

**LIB_ConfirmationLayer** (10 return values):
```pine
[conf_longSignal_confirmed, conf_shortSignal_confirmed, 
 conf_waitLong, conf_waitShort, 
 conf_longLevel, conf_shortLevel, 
 conf_waitLongStartBar, conf_waitShortStartBar, 
 conf_longLevelUpdatedThisBar, conf_shortLevelUpdatedThisBar] = CL.apply_confirmation(...)
```
- See [LIB_ConfirmationLayer.pine](../20_MODULES_REUSABLE/LIB_ConfirmationLayer.pine) for full parameter list (33 inputs)

---

## 🔧 Helper Fonksiyonlar

Modüllerin kullandığı yardımcı fonksiyonları kodunuza eklemeniz gerekir:

```pine
//@version=5

// Bar kapanış kontrolü (repaint koruması)
f__confirmed(_cond) =>
    barstate.isconfirmed ? _cond : false

// Çoklu MA tipi desteği
f__ma(_src, _len, _type) =>
    _type == "EMA" ? ta.ema(_src, _len) :
    _type == "WMA" ? ta.wma(_src, _len) :
    _type == "RMA" ? ta.rma(_src, _len) :
    _type == "HMA" ? ta.hma(_src, _len) :
    ta.sma(_src, _len)

// 0-1 aralığına sınırlama
f__clamp01(x) =>
    math.max(0.0, math.min(1.0, x))
```

---

## 📂 Modül Kategorileri

> **Not:** Modül kodları `#01 Pine_Module_Pack_v2.md` dosyasında bulunur.
> Her modül `// ────────────────` ile ayrılmıştır.
>
> **⚠️ v1.3.9-rf-patch Uyarı:** Aşağıdaki 45 modülün tamamı henüz v1.3.9-rf-patch ile test edilmemiştir.
> **Currently Active & Tested:**
> - **Signal modules**: LIB_Signal_Supertrend, LIB_Signal_RangeFilter (libraries)
> - **Confirmation Layer**: LIB_ConfirmationLayer (library)
> - **Filter modules**: MA Filter, MA Slope Filter, HTF Trend, Volume, ATR Volatility Floor, MACD Filter
> - **Guard modules**: Daily Loss, Consecutive Loss, Equity Curve, MAE guards
>
> **Module Pack v2 modules (45 total)** are preserved for **optional reintegration** via Section 2/4 adapter pattern.
> Use "How to Re-add a Pruned Mode" section above if you need one of the 8 removed signal modes.

### A. Giriş & Çıkış Kalitesi Modülleri (14 adet)

| # | Modül | Amaç | Örnek Kullanım |
|---|-------|------|----------------|
| 1️⃣ | `f_htfTrendFilter_v1` | HTF trend filtresi | `[l,d,long,short] = f_htfTrendFilter_v1(close, "240", 50, "EMA", true, true)` |
| 2️⃣ | `f_volumeAboveAvg_v1` | Hacim ortalamanın üstünde mü? | `[l,d,ok,ok] = f_volumeAboveAvg_v1(20, 1.2, false)` |
| 3️⃣ | `f_secondaryConfirm_v1` | RSI/MACD onay | `[l,d,long,short] = f_secondaryConfirm_v1(close, true, 14, 70, 30, true, 12, 26, 9, false)` |
| 4️⃣ | `f_atrVolFilter_v1` | ATR volatilite filtresi | `[l,d,ok,ok] = f_atrVolFilter_v1(14, 0.5, true)` |
| 5️⃣ | `f_sessionFilter_v1` | Seans filtresi | `[l,d,ok,ok] = f_sessionFilter_v1("0930-1600:12345", 5)` |
| 6️⃣ | `f_adxRegime_v1` | ADX trend gücü filtresi | `[l,d,ok,ok] = f_adxRegime_v1(14, 20)` |
| 7️⃣ | `f_candlePattern_v1` | Mum formasyonu onayı | `[l,d,long,short] = f_candlePattern_v1("Engulfing", 0.5, true)` |
| 8️⃣ | `f_srProximity_v1` | S/R yakınlık filtresi | `[l,d,long,short] = f_srProximity_v1(close, 10, 1.0)` |
| 9️⃣ | `f_bbSqueezeBreak_v1` | Bollinger sıkışma kırılımı | `[l,d,long,short] = f_bbSqueezeBreak_v1(20, 2.0, 3.0)` |
| 🔟 | `f_rsiDivergence_v1` | RSI uyumsuzluk | `[l,d,long,short] = f_rsiDivergence_v1(close, 14, 5)` |
| 11 | `f_maTrend_v1` | MA trend ve cross | `[l,d,long,short] = f_maTrend_v1(close, "EMA", 20, 50, true)` |
| 12 | `f_vwapConfluence_v1` | VWAP uyumu | `[l,d,long,short] = f_vwapConfluence_v1(true)` |
| 13 | `f_pullbackEntry_v1` | Geri çekilme girişi | `[l,d,long,short] = f_pullbackEntry_v1(close, 20, 2.0)` |
| 14 | `f_signalQualityScore_v1` | Sinyal kalite skoru | `[l,d,ok,ok] = f_signalQualityScore_v1(sig1, sig2, sig3, sig4, sig5, true)` |

### B. Stop/TP & Yönetim Modülleri (10 adet)

| Modül | Amaç |
|-------|------|
| `f_atrStopAdvisor_v1` | ATR bazlı stop mesafesi |
| `f_partialTPAdvisor_v1` | Kısmi TP seviyeleri |
| `f_breakEvenAdvisor_v1` | Break-even tetikleme |
| `f_timeExitAdvisor_v1` | Zaman bazlı çıkış |
| `f_trailingAdvisor_v1` | Trailing stop hesaplama |
| `f_volAdaptiveTP_v1` | Volatiliteye uyumlu TP |
| `f_oppositeSignalExit_v1` | Ters sinyal çıkışı |
| `f_sessionCloseExit_v1` | Seans kapanış çıkışı |
| `f_fibTargetsAdvisor_v1` | Fibonacci hedefleri |
| `f_psarTrailAdvisor_v1` | Parabolic SAR trailing |
| `f_chandelierAdvisor_v1` | Chandelier exit |

### C. Drawdown & Sermaye Koruma Modülleri (8 adet)

| Modül | Amaç |
|-------|------|
| `f_dailyLossLimit_v1` | Günlük kayıp limiti |
| `f_consecutiveLossHalt_v1` | Ardışık kayıp durdurma |
| `f_maxDrawdownGuard_v1` | Maksimum drawdown koruması |
| `f_dailyTradeCap_v1` | Günlük işlem sayısı limiti |
| `f_volPositionScaler_v1` | Volatilite bazlı pozisyon ölçekleme |
| `f_equityCurveFilter_v1` | Equity eğrisi filtresi |
| `f_weekendBlocker_v1` | Hafta sonu engelleyici |
| `f_correlationGuard_v1` | Korelasyon koruması |

### D. Risk Yönetimi Modülleri (9 adet)

| Modül | Amaç |
|-------|------|
| `f_kellyFraction_v1` | Kelly kriteri hesaplama |
| `f_volAdjSizer_v1` | Volatilite ayarlı pozisyon boyutu |
| `f_maxExposureGuard_v1` | Maksimum açık pozisyon koruması |
| `f_cooldownAfterTrade_v1` | İşlem sonrası bekleme |
| `f_maeGuard_v1` | Maximum Adverse Excursion koruması |
| `f_stressMode_v1` | Stres modu tetikleyici |
| `f_badRegimeDetector_v1` | Kötü piyasa rejimi algılayıcı |
| `f_liquidityFilter_v1` | Likidite filtresi |

### E. Tasarım & Test Araçları (3 adet)

| Modül | Amaç |
|-------|------|
| `f_debugPlots_v1` | Debug görselleştirme |
| `f_repaintCheck_v1` | Repaint kontrolü |
| `f_feeSlippageModel_v1` | Komisyon/slippage modeli |

---

## 🚀 Hızlı Başlangıç

### 1. Modülleri Kopyalayın

`#01 Pine_Module_Pack_v2.md` dosyasından ihtiyacınız olan modülleri stratejinizin **Section 2 (Fonksiyonlar)** bölümüne kopyalayın.

### 2. Section 4'te Kullanın

```pine
// ════════════════════════════════════════════════
// 4) SIGNAL PLUGIN
// ════════════════════════════════════════════════

// Inputs
htfTf   = input.timeframe("240", "HTF", group="Signal")
htfLen  = input.int(50, "HTF MA Len", group="Signal")
adxTh   = input.float(20, "ADX Threshold", group="Signal")

// Modül çağrıları
[_, dHtf, longHtf, shortHtf] = f_htfTrendFilter_v1(close, htfTf, htfLen, "EMA", true, false)
[_, dAdx, adxOkL, adxOkS]    = f_adxRegime_v1(14, adxTh)
[_, dVol, volOkL, volOkS]    = f_volumeAboveAvg_v1(20, 1.2, false)

// Sinyalleri birleştir
longSignal_raw  := longHtf and adxOkL and volOkL
shortSignal_raw := shortHtf and adxOkS and volOkS
```

### 3. Sinyal Kalitesi Skoru Kullanımı

Birden fazla onayı tek bir skora dönüştürmek için:

```pine
// 5 onay sinyalinden kalite skoru üret
[_, _, qualityOkL, qualityOkS] = f_signalQualityScore_v1(
    longHtf,    // sig1: HTF trend
    adxOkL,     // sig2: ADX gücü
    volOkL,     // sig3: Hacim onayı
    sessOkL,    // sig4: Seans içi
    rsiOkL,     // sig5: RSI onayı
    true        // showVis
)

// Kalite skoru >= 0.6 (en az 3/5 onay) olduğunda sinyal ver
longSignal_raw := qualityOkL
```

---

## ⚠️ Önemli Kurallar

1. **Modüller emir vermez** – Sadece `longRaw` / `shortRaw` boolean döndürür
2. **Repaint güvenliği** – Tüm sinyaller `barstate.isconfirmed` ile korunur
3. **Section 4'te kalın** – `strategy.entry/exit/close` çağrısı yapmayın
4. **Helper'ları unutmayın** – `f__confirmed`, `f__ma`, `f__clamp01` gerekli

---

## 📋 Modül Parametre Detayları

### HTF Trend Filter
```pine
f_htfTrendFilter_v1(src, htf, baseLen, maType, strict, showVis)
```
| Param | Tip | Varsayılan | Açıklama |
|-------|-----|------------|----------|
| `src` | series | close | Kaynak seri |
| `htf` | string | "240" | Üst zaman dilimi (4H) |
| `baseLen` | int | 50 | MA uzunluğu |
| `maType` | string | "EMA" | MA tipi: EMA, SMA, WMA, RMA, HMA |
| `strict` | bool | true | Crossover/under gereksin mi? |
| `showVis` | bool | true | Görselleştirme açık mı? |

### Volume Above Average
```pine
f_volumeAboveAvg_v1(len, minMult, showVis)
```
| Param | Tip | Varsayılan | Açıklama |
|-------|-----|------------|----------|
| `len` | int | 20 | Ortalama hesaplama periyodu |
| `minMult` | float | 1.2 | Minimum çarpan (volume/avg >= minMult) |
| `showVis` | bool | false | Ratio değerini plot et |

### ADX Regime Filter
```pine
f_adxRegime_v1(len, th)
```
| Param | Tip | Varsayılan | Açıklama |
|-------|-----|------------|----------|
| `len` | int | 14 | ADX periyodu |
| `th` | float | 20 | Minimum ADX eşiği |

---

## 🔗 MASTER_TEMPLATE_CORE ile Entegrasyon

Bu modüller, `MASTER_TEMPLATE_CORE.pine` dosyasının **Section 4** bölümünde kullanılmak üzere tasarlanmıştır.

### ✅ Uyumluluk Durumu (v1.3.2+)

| Özellik | Durum | Açıklama |
|---------|-------|----------|
| Pine Version | ✅ v5/v6 | MTC: v6, Libraries: v6, Module Pack: v5 |
| Standart Arayüz | ✅ Uyumlu | `[line, dir, longRaw, shortRaw]` (4 değer) / Libraries: 7-10 değer |
| Helper: `f__confirmed()` | ✅ Eklendi | Repaint koruması için |
| Helper: `f__ma()` | ✅ Eklendi | Multi-MA desteği |
| Helper: `f__clamp01()` | ✅ Eklendi | 0-1 sınırlama |
| Section 4 Adapter | ✅ Hazır | Modül seçici pattern |

### 🏗️ MASTER_TEMPLATE_CORE Section Yapısı (v1.3.9-rf-patch)

```
MASTER_TEMPLATE_CORE.pine (~4.5k satır)
├── Section 1: INPUTS (line ~75-400)
│   ├── grpTrade   - Trade yönü
│   ├── grpSignalMain - Signal mode seçimi (Supertrend / Range Filter Hybrid / None)
│   ├── grpSignalST - Supertrend parametreleri (LIB_Signal_Supertrend ile)
│   ├── grpSignalRF - Range Filter parametreleri (LIB_Signal_RangeFilter ile)
│   ├── grpFilter  - Filtreler (MA, MA Slope, HTF, Volume, ATR Vol, MACD)
│   ├── grpRange   - Range & Volatility filters (Entry pause)
│   ├── grpRisk    - Risk yönetimi
│   ├── grpSLTP    - Stop/TP ayarları
│   └── grpGuard   - Guard filters (Daily Loss, Equity Curve, MAE, etc.)
│
├── Section 2: FUNCTIONS (line ~600-2100)
│   ├── Helper'lar (f__confirmed, f__ma, f__clamp01)
│   ├── Core helpers (f_ma, f_sl_price, f_tp_price, f_calc_qty)
│   ├── Filter functions (f_mcginley, f_ma_filter, f_htf_trend)
│   ├── Risk functions (daily loss, consecutive loss, equity curve)
│   └── f_trailing() — çoğu inline; libraries: LIB_Signal_Supertrend, LIB_Signal_RangeFilter
│
├── Section 3: FILTER OUTPUTS & WARMUP (line ~2100-2900)
│   ├── Derived filter outputs (allowLong, allowShort)
│   ├── Guard adapter layer (engine-dependent modules)
│   └── Warmup bars calculation
│
├── Section 4: SIGNAL PLUGIN ★★★ LLM SADECE 4.1'İ DÜZENLER ★★★
│   ├── 4.0 - Variable definitions (longSignal_raw, shortSignal_raw, signalLine, signalDir)
│   ├── 4.1 - MODULE ADAPTER ← BURAYA YENİ MODE EKLE
│   │   ├── if signal_mode == "Supertrend" → LIB_Signal_Supertrend kullan
│   │   ├── else if signal_mode == "Range Filter Hybrid" → LIB_Signal_RangeFilter kullan
│   │   └── else (None mode) → signals false
│   ├── 4.2 - FINAL SIGNALS (DOKUNMA!) — signalLine/signalDir ile combine
│   └── 4.3 - EDGE TRIGGERS (DOKUNMA!)
│
├── Section 5: RISK ENGINE (DOKUNMA!) - Günlük limitler, pozisyon boyutu, SL/TP/BE/Trailing
│
└── Section 6: VISUALIZATION & EXIT STATS (DOKUNMA!) - Plotlar, alertler, istatistikler
```

**v1.3.9-rf-patch Önemli Notlar:**
- Signal modules artık **libraries**: LIB_Signal_Supertrend, LIB_Signal_RangeFilter
- Modülleri Section 2'ye kopyalamak gerekmiyor (import ile)
- Section 4.1'de **library output'ı** socket değişkenlerine ata
- Confirmation Layer (v1.3.7+) da library: LIB_ConfirmationLayer (optional, default OFF)

### Mimari

```
┌─────────────────────────────────────────┐
│  MASTER_TEMPLATE_CORE.pine              │
├─────────────────────────────────────────┤
│  Section 1: Inputs                      │
│  Section 2: Functions ← Modüller buraya │
│             ├─ f__confirmed()           │
│             ├─ f__ma() / f__clamp01()   │
│             └─ f_xxx_v1() modülleri     │
│  Section 3: Filters                     │
│  Section 4: Signal Plugin ← Çağrılar    │
│  Section 5: Risk Engine                 │
│  Section 6: Visualization               │
└─────────────────────────────────────────┘
```

### Örnek: Module Pack v2 Modülü Ekleme

**Adım 1:** Modülü Section 2'ye kopyalayın (helper'lardan sonra)

```pine
// Section 2'de, f_trailing() fonksiyonundan ÖNCE ekleyin:

f_htfTrendFilter_v1(src, htf, baseLen, maType, strict, showVis) =>
    _htfClose = request.security(syminfo.tickerid, htf, close, barmerge.gaps_off, barmerge.lookahead_off)
    _ma = f__ma(_htfClose, baseLen, maType)
    _bull = strict ? (close > _ma and ta.crossover(close, _ma)) : close > _ma
    _bear = strict ? (close < _ma and ta.crossunder(close, _ma)) : close < _ma
    longRaw  = f__confirmed(_bull)
    shortRaw = f__confirmed(_bear)
    dir  = longRaw ? 1 : shortRaw ? -1 : 0
    line = showVis ? (close - _ma) : na
    [line, dir, longRaw, shortRaw]
```

**Adım 2:** Section 4'te çağırın

```pine
// Section 4'te:
[_, _, htfLong, htfShort] = f_htfTrendFilter_v1(close, "240", 50, "EMA", true, false)

longSignal_raw  := htfLong
shortSignal_raw := htfShort
```

### 📝 Tam Entegrasyon Örneği: Yeni Modül Ekleme

Diyelim ki `f_htfTrendFilter_v1` modülünü yeni bir signal_mode olarak eklemek istiyorsunuz:

**1. Section 1'e input ekle:**
```pine
// signal_mode options'a "HTF Trend" ekle
signal_mode = input.string("Supertrend", "Signal Mode", 
     options = ["Supertrend", "EMA Cross", "Donchian", "HTF Trend", "None"],  // ← "HTF Trend" eklendi
     ...)

// HTF parametreleri
htf_signal_tf  = input.timeframe("240", "HTF Signal TF", group = grpSignal)
htf_signal_len = input.int(50, "HTF Signal MA Len", group = grpSignal)
```

**2. Section 2'ye modülü ekle:**
```pine
// f_donchian_signal() fonksiyonundan SONRA, f_trailing()'den ÖNCE

f_htfTrendFilter_v1(src, htf, baseLen, maType, strict, showVis) =>
    _htfClose = request.security(syminfo.tickerid, htf, close, barmerge.gaps_off, barmerge.lookahead_off)
    _ma = f__ma(_htfClose, baseLen, maType)
    _bull = strict ? (close > _ma and ta.crossover(close, _ma)) : close > _ma
    _bear = strict ? (close < _ma and ta.crossunder(close, _ma)) : close < _ma
    longRaw  = f__confirmed(_bull)
    shortRaw = f__confirmed(_bear)
    dir  = longRaw ? 1 : shortRaw ? -1 : 0
    line = showVis ? (close - _ma) : na
    [line, dir, longRaw, shortRaw]
```

**3. Section 4 adapter'a yeni case ekle:**
```pine
// 4.1 – MODULE ADAPTER bloğunun içinde
    else if signal_mode == "HTF Trend"
        [_line, _dir, _long, _short] = f_htfTrendFilter_v1(close, htf_signal_tf, htf_signal_len, "EMA", true, false)
        supertrendLine := _line
        supertrendDir  := _dir
        longSignal_raw := _long
        shortSignal_raw := _short
```

---

## 📝 Versiyon Geçmişi

| Versiyon | Tarih | Değişiklikler |
|----------|-------|---------------|
| v2.0 | 2025-12 | 45 modül, 5 kategori, HTF 4H varsayılan |
| v1.0 | 2025-11 | İlk sürüm: 3 temel modül |

---

## 📄 Lisans

Bu modül paketi, kişisel ve ticari kullanım için serbesttir.  
Kaynak gösterimi takdir edilir.

---

*Pine Module Pack v2 – MASTER_TEMPLATE_CORE Ekosistemi*
