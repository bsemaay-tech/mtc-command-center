# MTC V2 Architecture — Deep Audit Prompt (Round 2)

> **Talimatlar:**
> 1. Raporun başına kullandığın model numarasını yaz (örn: `**Model:** gpt-5.3-codex`)
> 2. Raporun sonuna `--- RAPOR BİTTİ ---` yaz
> 3. Bu doküman **READ-ONLY**. Hiçbir dosyada değişiklik yapma, sadece rapor hazırla.
> 4. Raporunu `C:\LAB\tradingview-lab\00_MASTER_TEMPLATE\MTC_V2\AUDIT_5\` klasörüne kaydet
> 5. Dosya adı sadece model numarası / model adı olsun
>    - örn: `gpt-5.3-codex.md`
>    - boşluk ve dosya adında geçersiz karakterler yerine `_` veya `-` kullan
>    - aynı isimde dosya varsa üzerine yazma, `_2`, `_3` ekleyerek yeni dosya oluştur
> 6. **Bu ikinci tur audit.** İlk turda 5 farklı LLM audit yaptı ve önerileri uygulandı.
>    Şimdi çok daha detaylı, V1 kod tecrübesi ve parity sürecinden derslerle zenginleştirilmiş bir audit bekleniyor.

---

## GÖREV TANIMI

MTC V2, modüler bir trading stratejisi framework'üdür. Pine Script (TradingView) ve Python (local backtest) olarak paralel geliştirilir. Aşağıda:

1. **MTC_V2_ARCHITECTURE.md** — Güncel mimari spesifikasyon (Round 1 audit önerileri uygulanmış hali)
2. **V1 Pine Script Analizi** — MASTER_TEMPLATE_CORE.pine'ın (5616 satır) detaylı teknik özeti
3. **V1 Onaylanmış Bug Listesi** — 6 bağımsız olarak doğrulanmış bug
4. **Parity Deneyimi** — 439 test case ile Pine/Python parity sürecinden edinilen dersler

Bunları kullanarak V2 mimarisini **satır satır** audit et. Özellikle:
- V1'de yaşanan her bug'ın V2 mimarisinde çözülüp çözülmediğini kontrol et
- Parity sürecinde karşılaşılan sorunların V2'de tekrar etme riskini değerlendir
- V1'in 5616 satıra şişmesine neden olan mimari hataları V2'de tespit et

---

## RAPOR FORMATI (13 bölüm)

### 1. GENEL DEĞERLENDİRME
Güçlü yanlar, olgunluk seviyesi (1-10), Round 1'den bu yana iyileşme.

### 2. V1 BUG KONTROLÜ (6 bug × V2 karşılığı)
Her V1 bug için:
- Bug ID ve özeti
- V2 mimarisinde bu sorun çözülmüş mü?
- Çözülmemişse: somut öneri

### 3. KRİTİK SORUNLAR (yeni bulgular)
Round 1'de yakalanmamış veya hâlâ çözülmemiş kritik sorunlar.

### 4. TUTARSIZLIKLAR
Doküman içindeki çelişkiler (farklı bölümlerde farklı imza, farklı davranış tanımı vb.)

### 5. EKSİK TANIMLAR
Kodlamaya geçildiğinde belirsizlik yaratacak tanımsız alanlar.

### 6. INTERFACE KONTRATI ANALİZİ (derin)
Her interface için:
- İmza yeterliliği
- Edge case'leri karşılıyor mu
- V1'deki karşılığıyla karşılaştırma

### 7. KONFİGÜRASYON ANALİZİ (derin)
- Parametre isimlendirme tutarlılığı
- Default değerlerin güvenliği
- Radio bool validasyon eksikleri
- V1 ile parametre eşleştirme tablosu

### 8. EXECUTION MODEL ANALİZİ
- Entry/exit sırası doğru mu (V1'deki A-1 bug bağlamında)
- Intrabar SL/TP ambiguity kuralı yeterli mi
- allow_flip + pyramiding etkileşimi
- Trailing/BE ownership modeli

### 9. PARİTY RİSK ANALİZİ
V1 parity sürecinden dersler ışığında:
- HTF veri hizalama riskleri
- Warmup/indicator seeding farklılıkları
- Broker reporting normalizasyonu
- History window sensitivity
- Float precision/rounding

### 10. PINE SCRIPT SPESİFİK RİSKLER
V1'in 5616 satıra şişme nedenleri ve V2'de tekrar etme riski.

### 11. PYTHON BACKTEST SPESİFİK RİSKLER
Performans, vektörel hesaplama, state yönetimi.

### 12. GELİŞTİRME SIRASI (L0-L25) ANALİZİ
Katman bağımlılıkları, eksik katmanlar, öneri.

### 13. ÖNERİLER VE İYİLEŞTİRMELER (tablo)
| Öneri | Gerekçe | Öncelik | V1 Referans |

---

## KAYNAK 1: MTC_V2_ARCHITECTURE.md (Güncel — Round 1 Sonrası)

```markdown
# MTC V2 — Full Architecture Specification

> Bu doküman Codex audit için hazırlanmıştır.
> Kodlamaya geçmeden önce mimari kararların doğruluğu, tutarsızlıklar ve eksikler kontrol edilmelidir.

---

## 1. Sistem Özeti

MTC V2, modüler bir trading stratejisi framework'üdür.
İki platform üzerinde **paralel ve parity-first** olarak geliştirilir:

| Platform | Dil | Amaç |
|----------|-----|-------|
| TradingView | Pine Script v6 | Canlı trade + görselleştirme |
| Local Backtest | Python 3.11+ | Hızlı backtest + optimizasyon |

**Temel kurallar:**
- Parametre isimleri iki platformda **birebir aynı**
- Her feature katman katman eklenir, parity bozulmadan ilerlenir
- Her modül kendi indikatörünü kendi hesaplar, modüller arası veri bağımlılığı yok
- Tüm entry/exit kararları `barstate.isconfirmed` (bar close) ile gated — **no-repaint**

---

## 2. Pipeline Mimarisi

Her bar'da aşağıdaki pipeline **yukarıdan aşağıya sıralı** çalışır:

```
┌─────────────────────────────────────────────────────────┐
│  BAR DATA (OHLCV + timestamp)                           │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  0. GLOBAL CONFIG                                       │
│     enable_long, enable_short, allow_flip,              │
│     regime_lock, max_entries, cooldown_bars              │
│                                                         │
│     → Sabit parametreler, hesaplama yok                 │
│     → Pipeline'ın geri kalanı bu config'i okur          │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  1. SIGNAL PRODUCER                                     │
│                                                         │
│     Input:  bar (OHLCV)                                 │
│     Output: RawSignal { long: bool, short: bool }       │
│                                                         │
│     ┌──────────────────────┐                            │
│     │ signal_mode seçimi:  │                            │
│     │  • Supertrend        │  ← kendi ATR hesaplar      │
│     │  • RangeFilterHybrid │  ← kendi ADX/Chop/RSI/BB   │
│     │  • CandlePattern     │  ← kendi formasyon tespiti │
│     └──────────────────────┘                            │
│                                                         │
│     Kurallar:                                           │
│     - Tek aktif producer (config ile seçilir)           │
│     - Aynı indikatör Gate'te farklı params ile          │
│       bağımsız instance olarak kullanılabilir            │
│     - Producer kendi indikatörünü hesaplar,             │
│       dışarıya bağımlılık yok                           │
└───────────────────────┬─────────────────────────────────┘
                        │ RawSignal
                        ▼
┌─────────────────────────────────────────────────────────┐
│  2. SIGNAL TRANSFORM PIPELINE                           │
│                                                         │
│     Input:  RawSignal + bar                             │
│     Output: TransformResult { long: bool, short: bool,  │
│               waiting: bool, reason: str }              │
│                                                         │
│     Sıralı zincir (her biri opsiyonel):                 │
│     ┌──────────────────┐    ┌─────────────────────┐     │
│     │ Confirmation     │ →  │ Level Retest        │     │
│     │ (swing break     │    │ (destek/dirence     │     │
│     │  bekle + timeout)│    │  retest bekle)      │     │
│     └──────────────────┘    └─────────────────────┘     │
│                                                         │
│     Kurallar:                                           │
│     - STATEFUL: state tutar (waiting, level, timer)     │
│     - Timeout → sinyal düşer                            │
│     - Bir transform onaylarsa, çıktısı sonrakine girer  │
│     - Transform OFF ise input=output (pass-through)     │
│     - Yeni transform eklemek = zincire yeni halka       │
└───────────────────────┬─────────────────────────────────┘
                        │ TransformedSignal
                        ▼
┌─────────────────────────────────────────────────────────┐
│  3. ENTRY GATES (AND kapısı)                            │
│                                                         │
│     Input:  bar + portfolio_state                       │
│     Output: GateResult { long_ok: bool,                 │
│               short_ok: bool, reason: str }             │
│                                                         │
│  3A. FİLTRELER (fiyat/indikatör bazlı, stateless)       │
│     ┌─────────────────────────────────────────────┐     │
│     │ MA Filter          │ close vs MA            │     │
│     │ MA Slope Filter    │ MA eğimi yeterli mi    │     │
│     │ McGinley Filter    │ close vs McGinley      │     │
│     │ HTF Trend Filter   │ HTF MA üstü/altı      │     │
│     │ MACD Regime Line   │ MACD > 0 / < 0         │     │
│     │ MACD Cross State   │ MACD/signal cross      │     │
│     │ MACD Histogram     │ hist yön/büyüklük      │     │
│     │ MACD Zero Distance │ min mesafe kontrolü    │     │
│     │ MACD HTF Bias      │ HTF MACD yön filtresi  │     │
│     │ Volume Filter      │ vol >= SMA * mult      │     │
│     │ ADX Filter         │ ADX vs threshold       │     │
│     │ Choppiness Filter  │ Chop vs threshold      │     │
│     │ ATR Vol Floor      │ ATR >= baseline * mult │     │
│     │ Momentum Filter    │ ATR body / ROC(1)      │     │
│     │ CandlePattern Gate │ engulfing/hammer vb.   │     │
│     │ Level Proximity    │ desteğe/dirence yakın? │     │
│     │ Session Filter     │ named session kontrolü │     │
│     └─────────────────────────────────────────────┘     │
│                                                         │
│  3B. GUARD'LAR (portföy bazlı, externally-stateful)      │
│     ┌─────────────────────────────────────────────┐     │
│     │ Daily Loss Limit   │ günlük kayıp limiti    │     │
│     │ Max Trades/Day     │ günlük trade sayısı    │     │
│     │ Max Drawdown       │ equity peak vs current │     │
│     │ Consecutive Loss   │ ardışık kayıp sayısı   │     │
│     │ Trade Cooldown     │ son çıkıştan beri bar  │     │
│     │ Equity Curve       │ equity vs equity SMA   │     │
│     │ MAE Guard          │ pozisyon içi max kayıp │     │
│     └─────────────────────────────────────────────┘     │
│                                                         │
│     Kurallar:                                           │
│     - Guard'lar kendi state tutmaz, PortfolioState okur  │
│     - Tüm gate'ler AND ile birleşir                     │
│     - Herhangi biri false → entry engellenir            │
│     - Filtreler: yön bilgisi var (long_ok ≠ short_ok)   │
│     - Guard'lar: çoğu yönsüz (ikisini birden bloklar)  │
│     - Guard recovery modları:                            │
│       • Bars: N bar bekle → otomatik resume              │
│       • Signals: N sinyal bekle → resume                 │
│       Virtual trade recovery KULLANILMAZ                 │
│     - Yeni gate eklemek = yeni fonksiyon + AND'e ekle   │
└───────────────────────┬─────────────────────────────────┘
                        │ signal AND all_gates_ok
                        ▼
┌─────────────────────────────────────────────────────────┐
│  4. POSITION MANAGER                                    │
│                                                         │
│     Input:  filtered_signal + position_state            │
│     Output: can_open: bool                              │
│                                                         │
│     Karar mantığı:                                      │
│     ┌─────────────────────────────────────────────┐     │
│     │ enable_long/short   → yön izni              │     │
│     │ regime_lock         → aynı yönde tekrar?    │     │
│     │ allow_flip          → aynı barda çevir?     │     │
│     │ max_entries         → pyramid limiti         │     │
│     │ cooldown_bars       → entry arası bekleme    │     │
│     └─────────────────────────────────────────────┘     │
│                                                         │
│     Entry Mode = SIGNAL (Edge modu kaldırıldı)          │
│     Signal + regime_lock = Edge ile aynı davranış       │
│                                                         │
│     State:                                              │
│     - last_signal_dir (son onaylı sinyal yönü)          │
│     - current_entries_long / short                      │
│     - last_entry_bar                                    │
│     - position_size, position_side                      │
└───────────────────────┬─────────────────────────────────┘
                        │ can_open = true
                        ▼
┌─────────────────────────────────────────────────────────┐
│  5. POSITION SIZING                                     │
│                                                         │
│     Input:  entry_price, sl_price, equity, config       │
│     Output: qty (lot büyüklüğü)                        │
│                                                         │
│     Hesaplama:                                          │
│     ┌─────────────────────────────────────────────┐     │
│     │ risk_pct            → equity * risk% / sl_dist│    │
│     │ fallback_size       → SL OFF ise sabit %     │     │
│     │ max_leverage_cap    → qty üst limiti          │     │
│     │ equity_source       → realized / unrealized  │     │
│     │ notional_assert     → güvenlik kontrolü      │     │
│     └─────────────────────────────────────────────┘     │
│                                                         │
│     SL hesabı burada da gerekir (qty için).             │
│     calc_sl() TEK FONKSİYON — hem burada hem            │
│     Exit Rules'da aynı fonksiyon çağrılır (DRY).        │
└───────────────────────┬─────────────────────────────────┘
                        │ qty
                        ▼
┌─────────────────────────────────────────────────────────┐
│  6. ENTRY EXECUTION                                     │
│                                                         │
│     Pine:   strategy.entry(id, direction, qty)          │
│     Python: engine.open_position(side, qty, entry_price)│
│                                                         │
│     + SL/TP emirleri hemen yerleştirilir                 │
│       (strategy.exit ile veya engine state ile)          │
│     + WunderTrading JSON alert gönderilir (Pine)        │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  7. EXIT RULES (pozisyon açıkken, her bar çalışır)      │
│                                                         │
│     Input:  position + bar                              │
│     Output: ExitResult { should_exit: bool,             │
│               reason: str }                             │
│                                                         │
│  7A. PRICE-BASED                                        │
│     ┌─────────────────────────────────────────────┐     │
│     │ Stop Loss (radio — biri seçilir)             │     │
│     │   ○ SL ATR          │ ATR * mult             │     │
│     │   ○ SL Percent      │ entry * pct            │     │
│     │   ○ SL Swing+ATR    │ swing low/high + ATR   │     │
│     │   Biri seçilince diğerleri grey/inactive      │     │
│     │   calc_sl() TEK FONKSİYON — seçime göre hesap│     │
│     │                                             │     │
│     │ Take Profit (radio — biri seçilir)           │     │
│     │   ○ Single TP ATR   │ ATR * mult             │     │
│     │   ○ Single TP %     │ entry * pct            │     │
│     │   ○ Single TP R     │ sl_dist * R multiple   │     │
│     │   ○ Multi-TP        │ TP1 partial + TP2 full │     │
│     │   Biri seçilince diğerleri grey/inactive      │     │
│     │   Single ve Multi karşılıklı exclusive        │     │
│     │                                             │     │
│     │ Break Even                                  │     │
│     │   Trigger: price reaches be_trigger * R      │     │
│     │   Action: SL → entry + buffer               │     │
│     │                                             │     │
│     │ Trailing Stop                               │     │
│     │   Start: price reaches trail_start * R       │     │
│     │   Trail: ATR-based distance, follows price   │     │
│     └─────────────────────────────────────────────┘     │
│                                                         │
│  7B. TIME-BASED                                         │
│     ┌─────────────────────────────────────────────┐     │
│     │ Time Stop        │ bars_since_entry >= N    │     │
│     │ End of Day       │ session close            │     │
│     │ End of Week      │ friday close             │     │
│     │ Condition: Always / Profit Only / Loss Only │     │
│     └─────────────────────────────────────────────┘     │
│                                                         │
│  7C. SIGNAL-BASED                                       │
│     ┌─────────────────────────────────────────────┐     │
│     │ OPP_SIGNAL       │ karşı sinyal geldi       │     │
│     │ FILTER_BLOCK     │ filtre blokladı          │     │
│     │   Per-filter toggles:                       │     │
│     │   MA, MA Slope, McGinley, HTF Trend,        │     │
│     │   Volume, ATR Vol, Range Filter             │     │
│     └─────────────────────────────────────────────┘     │
│                                                         │
│     Öncelik sırası (ilk tetiklenen kazanır):            │
│     SL/TP/BE (broker) → OPP_SIGNAL → FILTER_BLOCK      │
│       → TIME_STOP → TRAILING                           │
│                                                         │
│     closeRequestedThisBar flag ile                      │
│     aynı barda çift çıkış engellenir                    │
└───────────────────────┬─────────────────────────────────┘
```

(Section 3-11 dahil tam doküman dosyadan okunmalıdır: `C:\LAB\tradingview-lab\00_MASTER_TEMPLATE\MTC_V2_ARCHITECTURE.md`)

**NOT:** Yukarıdaki pipeline özeti kısaltılmıştır. Tam dokümanı dosyadan oku — özellikle şu bölümler kritik:
- Section 4b: Execution Model & Intrabar Kuralları
- Section 4c: HTF Veri Kuralları
- Section 6.4: ExitRule + ExitContext
- Section 6.7: Core Data Types (Bar, Position, PortfolioState)
- Section 7: Konfigürasyon (tüm parametreler)
- Section 8: Bar Loop (exit-first order)
- Section 11: Audit Kontrol Listesi

---

## KAYNAK 2: V1 Pine Script Teknik Analizi (5616 satır)

### Genel Yapı
MASTER_TEMPLATE_CORE.pine v2.2.0-LibRefactor, Pine Script v6, 6 kütüphane import eder:
- `LIB_Signal_Supertrend_Fix`, `LIB_Signal_RangeFilter`, `LIB_ConfirmationLayer`
- `LIB_MATH_HELPERS`, `LIB_SLTP_HELPERS`, `LIB_WUNDERTRADING_HELPERS`

### Execution Config
```pine
strategy(..., calc_on_every_tick=false, process_orders_on_close=true,
         pyramiding=5, commission=0.04%, slippage=5)
```

### HTF Data Hub (lines 895-1024)
Centralized `request.security()` cache. Tek fetch per unique timeframe, cascade deduplication.
`htf_confirm_all` gate tüm HTF timeframe'leri için `barstate.isconfirmed` kontrol eder.

### Filter Stack
7 filtre AND ile birleşir → `allowLong / allowShort`:
- MA, MA Slope, McGinley, MACD Hub (6 sub-gate), HTF Trend, Volume, ATR Vol Floor

### MACD Filter Hub (lines 1802-1907)
En karmaşık tek filtre. 6 alt-gate: regime, cross-state, histogram, hist mode, zero-distance, HTF bias.
HTF MACD `_line[1]` offset ile repaint koruması.

### Confirmation Layer (lines 2748-2997)
Pivot-based swing break + momentum. Dynamic level updates (TIGHTEN_ONLY vs ANY).
RAW event mode, session gating, tie-breaking. Warmup patch (FIX B1-02).

### Entry Logic (lines 3012-3098)
- **Edge mode**: `false→true` transition only
- **Signal mode**: Entry whenever signal active
- **Pending queue**: `allow_flip=OFF` iken karşı sinyal queue'ya alınır
- **Regime lock** (FIX REGIME-1): `lastSignalDir_tracked[1]` ile same-bar self-block engellenir
- **Separate pyramid limits**: Edge → `edge_max_pyramid_positions`, Signal → `signal_mode_max_entries + cooldown`

### Entry/Exit Order
```
1. Position flat reset (line 3718)
2. OPP_SIGNAL exit (lines 3738-3773) — RAW sinyaller kullanır
3. FILTER_BLOCK exits (lines 3782-3861) — per-filter granular
4. TIME_STOP exit (lines 3869-3910) — bar duration + EOD/EOW
5. Entry execution (lines 4259-4368) — Long first, then short
6. Break-Even state machine (lines 4394-4406) — trailing NOT active ise
7. Trailing stop (lines 4455-4504) — SL ownership alır
```

### Pyramid SL Merging
Monotonic: long SL = `math.max(existing, new)`, short SL = `math.min(existing, new)`.
Pyramid add sadece sıkılaştırabilir, genişletemez.

### Guard Recovery (lines 2216-2631)
Modes: Bars, Signals, Manual, Virtual Trade.
Virtual Trade recovery = tam SL/TP/BE/Trailing simülasyonu.
**Sorun**: Virtual trade entry sadece Signal modunda çalışır — Edge modunda recovery hiç tamamlanmaz.

### Time Stop Loop Prevention (FIX A-3)
`timeStopCooldownUntilBar = bar_index + time_stop_bars` ile "Always" signal modunda sonsuz döngü engellenir.

### Trailing/BE Ownership
BE ve Trail karşılıklı exclusive. Trail aktifleşince BE kalıcı olarak dondurulur.
**Sorun** (Bug E-1): Trail SL güncellerken TP1/TP2'nin `stop=` parametresi güncellenmez — stale değerle kalır.

### ATR Vol Floor Architectural Issue
`use_range_filters` master gate'ine bağlı DEĞİL — bağımsız çalışır. Dokümantasyonda "FIX NEEDED" notu var.

### Script Resource Pressure
500 label limiti, 5 table limiti yakınında. `ENABLE_*` compile-time gate'leri ile feature toggle.

---

## KAYNAK 3: V1 Onaylanmış Bug Listesi (PEER_AUDIT_CLAUDE.md)

### BUG A-1: TIME_STOP Sonrası Entry Gate Eksikliği [HIGH]
TIME_STOP `closeRequestedThisBar=true` set eder ama `f_process_entry()` bu flag'i kontrol etmez.
`canOpenLong` TIME_STOP'tan ÖNCE hesaplanır → TIME_STOP bar'ında hatalı entry oluşur.

### BUG A-2: TIME_STOP Reset Sonrası TP Üzerine Yazma [MEDIUM]
`f_reset_exit_state()` tp1Series=na yapar → pyramid na-guard `na(tp1Series)=true` → yeni TP değeri yazılır.
A-1 fix edilirse otomatik çözülür.

### BUG B-1: Trailing Exit'te f_reset_exit_state() Eksik [HIGH]
5 exit path'ten sadece trailing'de `f_reset_exit_state()` çağrılmıyor.
1-bar stale state window oluşur (sonraki bar'da flat-reset düzeltir).

### BUG D-1: f_apply_break_even'da Hardcoded String [MEDIUM]
`"Long TP1"` literal string kullanılıyor, `EXIT_ID_LONG_TP1` constant değil.
Rename riski → orphaned order.

### BUG E-1: Trailing SL Güncellemesinde TP1/TP2 stop= Güncellenmez [MEDIUM]
Trail SL'yi günceller ama TP1/TP2 exit'lerinin `stop=` parametresi stale kalır.
Ani reversalde stale stop'tan partial exit riski.

### BUG C-1: BUY/SELL Label Raw Sinyali Gösteriyor [MEDIUM/UX]
Plotshape `longSignal_raw` kullanıyor, `canOpenLong` değil. Confirmation + filtreler sonrası gerçek entry'den 7+ bar önce label görünür.

---

## KAYNAK 4: Parity Deneyimi (439 Case Suite)

### Parity Başarı Oranı
- 437/439 PASS (RAW_STRICT), 2 MISMATCH (case 402, 416 — TV export truncation)
- CLIP_OVERLAP: 439/439 (100%)

### Karşılaşılan Temel Sorunlar

**1. History Window Sensitivity (CRITICAL)**
TradingView'ın "effective history window" (chart'ın başlangıç noktası) indicator seeding'i etkiler.
EMA-200 gibi uzun lookback'li indikatörler, farklı history start ile farklı değerler üretir.
Python backtester sabit dataset kullanır → parity bozulur.
Çözüm: warmup_bars hard-block + indicator pre-computation.

**2. Broker Reporting Asymmetry**
TV bazen tek exit row döner, Python 2 row (veya tersi). qty toplamları eşleşir.
Çözüm: `normalize_broker_reporting()` — qty summing ile collapse.

**3. MARGIN CALL + BE Cluster**
Aynı entry'den MARGIN CALL + BE row'ları çıkabilir. Platform farkı.
Çözüm: `normalize_margin_call_be_clusters()` — same-entry timestamp cluster collapse.

**4. OPP_SIGNAL Same-Bar Flip**
`allow_flip=True` iken aynı barda close+reopen. Execution order kritik.
V1'de `oppSignalFlipEntryThisBar` flag ile çözüldü.
V2'de exit-first order bu sorunu doğal olarak çözmeli.

**5. MarginCallLock — Capital Exhaustion**
Deep drawdown sonrası `strategy.equity < 5% * initial_capital` → kalıcı entry block.
Gerçekte hesap hâlâ trade edilebilir (küçük qty ile).
V1'de dynamic capital exhaustion guard ile düzeltildi.

**6. Range Filter Master Gate Inconsistency**
ATR Vol Floor, `use_range_filters` master toggle'ına bağlı değil.
Range filters OFF iken ATR Vol Floor hâlâ aktif kalıyor.

**7. Choppiness TR Source Inconsistency**
Chop True Range, ADX kaynaklarından hesaplanıyor — kendi HTF kaynağından değil.
Nadir durumlarda HTF chop değerleri sapabilir.

**8. Float Precision**
Python ve Pine Script arasında float hesaplamalarında 1e-10 civarı farklar oluşur.
Parity karşılaştırmada tolerans: price 1e-6 abs, qty 1e-4 rel.

---

## KONTROL LİSTESİ — Audit Sırasında Cevapla

Her maddeyi raporda açıkça değerlendir:

- [ ] V1 Bug A-1 (TIME_STOP entry gate): V2 exit-first order bu sorunu çözüyor mu?
- [ ] V1 Bug B-1 (trailing reset): V2 exit state management bunu karşılıyor mu?
- [ ] V1 Bug E-1 (trailing TP sync): V2 trailing/BE ownership modeli bunu çözüyor mu?
- [ ] Pyramid SL merging: V2'de monotonic merge tanımlı mı?
- [ ] Edge mode kaldırıldı: Pending queue mantığı V2'de gerekli mi?
- [ ] Guard recovery: Virtual trade kaldırılmış — Signals sayımı (gate-passed) doğru mu?
- [ ] HTF data alignment: `merge_asof(direction='backward')` yeterli mi yoksa off-by-one riski var mı?
- [ ] Warmup: Otomatik hesaplama `max(all_lookbacks)` yeterli mi? Nested indikatörler (EMA of EMA)?
- [ ] Session filter: DST geçişlerinde bar sınıflandırma hatalı olabilir mi?
- [ ] ATR Vol Floor: V2'de range filter master gate'ine bağlı mı?
- [ ] MACD 5-gate: Ortak MACD hesaplaması DRY ama `macd_gates.py` tek dosyada 5 gate → file büyüme riski?
- [ ] Config `cooldown_bars` vs `cooldown_bars_after_exit`: İkisi farklı şey mi? Çakışma riski?
- [ ] Multi-TP: `exit_pct` eklendi ama TP2 %100'ü mü alıyor yoksa kalanın %100'ünü mü?
- [ ] Flat dict config: 100+ parametre → Pydantic/schema validation olmadan hata riski?
- [ ] `closeRequestedThisBar` flag: V2'de bu pattern tanımlı mı (exit-first order bunu otomatik çözüyor mu)?

---

--- PROMPT BİTTİ ---
