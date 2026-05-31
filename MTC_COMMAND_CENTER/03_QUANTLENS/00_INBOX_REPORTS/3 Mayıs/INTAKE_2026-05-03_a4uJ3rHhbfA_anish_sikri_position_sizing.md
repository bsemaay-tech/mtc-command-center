# QuantLens Transcript Intake Report — Anish Sikri / The Art of Position Sizing

## 1. Metadata

- **Source URL:** https://youtu.be/a4uJ3rHhbfA?si=hD9z9rji3O6XbMnj
- **Normalized URL:** https://www.youtube.com/watch?v=a4uJ3rHhbfA
- **Video ID:** `a4uJ3rHhbfA`
- **Title:** `The Art of Position Sizing with Anish Sikri | US Investing Championship Top Contender`
- **Channel:** `UNKNOWN_CHANNEL`
- **Transcript file:** `The Art of Position Sizing with Anish Sikri  US Investing Championship Top Contender.md`
- **Transcript SHA256:** `5902a529d835019053893591a6fc58ab27f810f3ae4c7746b1a650029b234306`
- **Approx. word count:** `21,447`
- **Intake date:** 2026-05-03
- **Duplicate status:** `NOT_DUPLICATE_IN_CURRENT_SESSION`
- **Repo registry duplicate check:** `NOT_VERIFIED_REPO_NOT_AVAILABLE`
- **Channel blacklist check:** `NOT_VERIFIED_REPO_NOT_AVAILABLE`
- **Final classification:** `SALVAGE`
- **Codex status suggestion:** `SALVAGE_ONLY`
- **Module ID suggestion:** `QL_RISK_2026-05-03_a4uJ3rHhbfA_ANISH_POSITION_SIZING`

---

## 2. Executive Summary

Bu transcript doğrudan bir **entry signal producer** değildir. Ana değer, Anish Sikri'nin küçük hesap üzerinden anlattığı **position sizing, risk budget, progressive exposure, descale/upscale, stop discipline ve earnings risk yönetimi** yaklaşımıdır.

Bu yüzden dosya `CANDIDATE` olarak strateji üretmemeli; ancak MTC_V2'nin **Position Sizing**, **PortfolioState**, **Position Manager** ve kısmen **Exit Rules** katmanına ileride eklenecek çok değerli bir risk modülü olarak saklanmalıdır.

Ana fikir çok net:

> Önce küçük pozisyonla piyasayı test et; traction gelirse büyüt; kayıplar gelirse küçül; toplam hesabın riskini sabit tut; stop ve position size birlikte çalışsın.

---

## 3. Decision

### Final Verdict: `SALVAGE`

Bu video `SALVAGE` olarak işlenmeli çünkü:

- Kodlanabilir buy/sell stratejisi tek başına verilmemiştir.
- Asıl konu trade giriş sinyali değil, pozisyon büyüklüğü ve risk yönetimidir.
- Ancak MTC_V2 için doğrudan kullanılabilecek **position sizing engine** fikirleri vardır.
- Küçük hesap, 25% blok, 1/8 ve 1/16 probe size, loss streak descale, profit streak upscale, earnings cushion gibi kurallar sistemleştirilebilir.

### Neden `CANDIDATE` değil?

- CLF, COIN, HZNP, UPWK örnekleri entry setup anlatıyor; fakat bu video onların strateji reçetesini tam tanımlamıyor.
- Girişler genellikle “proper buy point”, “50-day bounce”, “VCP cheat area”, “breakout” gibi daha önceki sistemlerden alınmış varsayımlar.
- Videonun benzersiz katkısı giriş sinyali değil; **girişten sonra risk ve pozisyon büyüklüğü nasıl yönetilir** sorusudur.

### Neden `WIKI_ONLY` değil?

- İçerik sadece teorik psikoloji veya genel tavsiye değil.
- MTC_V2 içinde kodlanabilir bir **sizing / portfolio guard module** olarak değerlendirilebilir.
- Bu nedenle Trader Wiki notu da çıkarılabilir; fakat ana kayıt `SALVAGE_ONLY` risk modülü olmalıdır.

---

## 4. Extracted Risk / Sizing Components

## 4.1 Account Risk Budget — `ANISH_ACCOUNT_RISK_BUDGET_V1`

### Kaynak Fikir

Toplam hesap riski küçük tutulmalı. Anish örneklerinde `1.25%` ile `2.50%` toplam hesap riski ana referans olarak kullanılıyor. 10.000 USD hesapta bu 125–250 USD risk anlamına geliyor.

### Kodlanabilir Tanım

```text
equity = current account equity
max_account_risk_pct = 0.0125 to 0.0250
max_account_risk_cash = equity * max_account_risk_pct
```

Her trade için teorik maksimum kayıp:

```text
trade_risk_cash = position_notional * stop_pct
```

Trade sadece şu koşulda kabul edilir:

```text
trade_risk_cash <= available_risk_budget_cash
```

### MTC_V2 Mapping

- `POSITION SIZING`
- `PortfolioState.available_risk_budget`
- `ENTRY EXECUTION` öncesi final notional check

---

## 4.2 25% Block Position Model — `ANISH_BLOCK_SIZER_V1`

### Kaynak Fikir

Optimal tam pozisyon bloğu yaklaşık `25%` hesap büyüklüğü olarak anlatılıyor. Bu, 10.000 USD hesapta 2.500 USD pozisyon anlamına gelir. Bu modelde dört tam pozisyon maksimum standart portföy olarak düşünülebilir.

### Kodlanabilir Parametreler

```text
base_block_pct = 0.25
max_standard_positions = 4
max_single_position_pct = 0.50
```

### Önemli Yorum

Anish `50%` üstü tek pozisyonu risk-of-ruin açısından tehlikeli görüyor. Geçmişte 75% gibi pozisyonların tehlikeli olduğunu örnekliyor. Bu yüzden:

```text
hard_max_position_pct = 0.50
preferred_position_pct = 0.25
```

### MTC_V2 Mapping

- `max_position_pct_per_symbol`
- `max_total_long_exposure`
- `max_entries`
- `notional cap`

---

## 4.3 Probe Size / Market Test Mode — `ANISH_PROBE_SIZE_V1`

### Kaynak Fikir

Yeni başlayan veya choppy piyasada doğrudan 25% pozisyona girmek yerine 1/8 veya 1/16 hesap büyüklüğüyle piyasayı test etmek öneriliyor.

### Kodlanabilir Boyutlar

```text
full_block = 25% of equity
half_block = 12.5% of equity
quarter_probe = 6.25% of equity
```

10.000 USD hesap örneği:

```text
25% block = 2,500 USD
12.5% probe = 1,250 USD
6.25% micro probe = 625 USD
```

### Trigger Mantığı

Başlangıçta veya kötü feedback dönemlerinde:

```text
if no_profit_cushion or loss_streak_active:
    size_mode = MICRO_PROBE or HALF_BLOCK
```

Traction geldikçe:

```text
if recent_trades_profitable and equity_above_recent_high:
    size_mode = HALF_BLOCK -> FULL_BLOCK
```

---

## 4.4 Loss Streak Descale — `ANISH_DESCALE_ON_LOSSES_V1`

### Kaynak Fikir

Birbirini izleyen kayıplarda pozisyon boyutu otomatik küçültülmeli. Anish spreadsheet örneklerinde kayıplar gelince 25% bloktan 12.5%, sonra 6.25% gibi küçük boyutlara iniyor.

### Kodlanabilir State

```text
consecutive_losses
rolling_trade_pnl_pct
rolling_realized_r
equity_drawdown_from_local_peak
current_size_multiplier
```

### Örnek Kural

```text
if consecutive_losses >= 1:
    size_multiplier = min(size_multiplier, 0.50)

if consecutive_losses >= 2:
    size_multiplier = min(size_multiplier, 0.25)

if consecutive_losses >= 3:
    size_multiplier = 0.25
    allow_new_entries = PROBE_ONLY
```

Burada `0.25` multiplier, 25% block'un 1/4'ü anlamına gelir; yani toplam hesapta yaklaşık 6.25% pozisyon.

### Alternatif Daha Basit Kural

```text
if rolling_last_5_trades_pnl < 0:
    size_mode = HALF_BLOCK

if rolling_last_10_trades_pnl < 0:
    size_mode = MICRO_PROBE
```

### MTC_V2 Mapping

- `PortfolioState` içinde loss-streak tracking
- `POSITION SIZING` risk multiplier
- `Position Manager` yeni entry throttle

---

## 4.5 Profit Traction Upscale — `ANISH_UPSCALE_ON_TRACTION_V1`

### Kaynak Fikir

Kârlar gelmeye başladığında ve trade feedback olumluysa pozisyon büyütülür. Fakat bu büyüme kör leverage değildir; önce cushion oluşmalı.

### Kodlanabilir State

```text
profit_cushion_pct = (equity - recent_equity_floor) / recent_equity_floor
rolling_win_rate
rolling_avg_gain_pct
rolling_avg_loss_pct
```

### Örnek Kural

```text
if consecutive_wins >= 2 and profit_cushion_pct > 0:
    size_multiplier = min(size_multiplier * 2, 1.0)
```

Tam block'a geçme:

```text
if equity > previous_equity_high and rolling_last_5_trades_pnl > 0:
    size_mode = FULL_BLOCK
```

Agresif mod için ek koşul:

```text
if market_regime == CONFIRMED and rolling_last_10_trades_pnl > threshold:
    allow_full_block = true
else:
    allow_full_block = false
```

### Uyarı

Anish, Paul Tudor Jones'un “en büyük kayıplar iyi dönemlerden sonra gelir” fikrine çok önem veriyor. Bu yüzden upscale modunda **max risk cap** ve **drawdown kill-switch** mutlaka kalmalı.

---

## 4.6 Stop Percentage and Technical Stop Alignment — `ANISH_STOP_ALIGNMENT_V1`

### Kaynak Fikir

Stop yüzdesi keyfi seçilmemeli; proper buy point ve teknik stop ile uyumlu olmalı. Genel bant:

- Yeni başlayan / klasik CANSLIM: 5–8% maksimum
- Anish'in güncel swing yaklaşımı: ortalama kayıp yaklaşık 2.8–3%
- Çok agresif büyük pozisyonlarda: stop daha da sıkı olmalı

### Kodlanabilir Tanım

```text
technical_stop_pct = abs(entry_price - stop_price) / entry_price
```

Pozisyon büyüklüğü:

```text
position_notional = min(
    equity * base_block_pct * size_multiplier,
    max_account_risk_cash / technical_stop_pct
)
```

Trade reject koşulları:

```text
if technical_stop_pct > max_allowed_stop_pct:
    reject_trade("STOP_TOO_WIDE")

if technical_stop_pct <= 0:
    reject_trade("INVALID_STOP")
```

### MTC_V2 Mapping

- `calc_sl()` ile ortak stop mesafesi
- `POSITION SIZING` içinde stop-based notional calculation
- `ENTRY GATES` içinde stop-too-wide gate

---

## 4.7 Average Gain / Average Loss Awareness — `ANISH_EXPECTANCY_AWARE_EXIT_V1`

### Kaynak Fikir

Anish kendi sayılarının farkında: ortalama kazanç %7–10 civarı, ortalama kayıp ~%2.8–3 civarı örnekleniyor. Bu nedenle %7–10 arası hızlı kazanç geldiğinde, özellikle choppy markette kârı kilitleme eğilimi var.

### Kodlanabilir Kullanım

Bu direkt take-profit olarak kaba uygulanmamalı; ama exit manager için regime-aware kâr alma bandı olabilir.

```text
if market_regime == CHOPPY and unrealized_gain_pct >= avg_gain_target_pct:
    take_partial_or_exit = true
```

Parametreler:

```text
avg_gain_target_pct = 0.07 to 0.10
avg_loss_target_pct = 0.028 to 0.03
```

### MTC_V2 Mapping

- `EXIT RULES`: partial TP / discretionary proxy
- `PortfolioState`: strategy statistics tracking

---

## 4.8 Earnings Cushion Guard — `ANISH_EARNINGS_CUSHION_GUARD_V1`

### Kaynak Fikir

Earnings'e kârsız veya küçük kârla girmek riskli. Anish, earnings öncesi trade tutulacaksa yaklaşık %10 kâr cushion gerektiğini söylüyor. Aksi durumda trade kapatma veya azaltma tercih ediliyor.

### Kodlanabilir Kural

```text
if days_to_earnings <= earnings_guard_days:
    if unrealized_gain_pct < required_earnings_cushion_pct:
        block_new_entry = true
        reduce_or_exit_existing = true
```

Parametreler:

```text
earnings_guard_days = 5 to 10
required_earnings_cushion_pct = 0.10
```

### Veri Gereksinimi

- OHLCV tek başına yeterli değildir.
- Earnings calendar gerekir.
- İlk prototype'da bu modül opsiyonel veya placeholder olabilir.

---

## 4.9 Liquidity / Price Filter — `ANISH_LIQUIDITY_FILTER_V1`

### Kaynak Fikir

Anish düşük kaliteli, düşük fiyatlı, likiditesi zayıf hisselerden kaçınmayı vurguluyor. Örnek eşikler:

- Ortalama hacim: yaklaşık 200.000 share ve üzeri
- Minimum fiyat: 10 USD üzeri tercih
- Daha iyi sweet spot: 50 USD ve üzeri hisseler

### Kodlanabilir Gate

```text
if close < min_price:
    reject_trade("PRICE_TOO_LOW")

if avg_volume_20 < min_avg_volume:
    reject_trade("INSUFFICIENT_LIQUIDITY")
```

Varsayılanlar:

```text
min_price = 10
preferred_price = 50
min_avg_volume_20 = 200000
```

Daha iyi versiyon:

```text
avg_dollar_volume_20 = avg_volume_20 * close
```

ve min dollar volume kullanılmalıdır.

---

## 5. Trade Examples Extracted

## 5.1 CLF Trade

### Setup Type

- 50-day moving average bounce
- Low-volume pullback
- Cheat area / VCP-style early entry

### Risk Management

- Stop below 50-day area / prior technical level
- Tight stop, around 2–5% zone
- Fast gain captured; 20% in two days example

### System Lesson

Bu örnek entry signal'dan çok şunu gösterir:

```text
If fast gain >= average_gain_band in choppy market:
    take_profit_or_reduce
```

---

## 5.2 COIN Trade

### Setup Type

- Bitcoin theme proxy
- Breakout through pivot
- Aggressive entry with roughly 3% stop

### Risk Management

- Bad fill due to strong volume/spread expansion olumlu sinyal olarak yorumlanıyor.
- Ertesi gün %7–10 bandında kâr alınmış.

### System Lesson

Theme momentum trade'lerinde hızlı kâr geldiğinde, özellikle choppy markette pozisyon taşımak yerine realized gain tercih edilebilir.

---

## 5.3 HZNP Trade

### Setup Type

- Breakout around pivot area
- Fast shakeout next day
- Recovery within first 10–30 minutes

### Risk Management

- Stop roughly 2–3% below breakout / prior day low.
- Stock recovery yapmazsa exit.
- Ertesi gün trade çalışmadığı için yaklaşık -2.97% civarında çıkış.

### System Lesson

```text
if breakout fails and does not recover quickly:
    exit_or_reduce
```

Bu, OHLC daily sistemde zor kodlanır; intraday confirmation gerektirir. Daily-only prototype'da close-based failed breakout kullanılabilir.

---

## 5.4 UPWK Trade

### Setup Type

- Choppy pattern
- 50-day support/bounce
- Earnings yaklaşırken kısa vadeli trade

### Risk Management

- Earnings öncesi kâr varsa azalt / kâr kilitle.
- Kâr yoksa earnings'e trade taşınmamalı.
- %22 kâr varsa en azından partial almak mantıklı görülüyor.

### System Lesson

Earnings cushion guard için iyi örnek:

```text
if days_to_earnings <= guard and gain < cushion:
    exit_before_earnings
```

---

## 6. Proposed Python Prototype

## 6.1 Prototype Goal

Bu transcript'ten üretilecek ilk Python işi bir trade entry strategy değil, **position sizing overlay** olmalıdır.

Amaç:

```text
Given an existing signal stream, compare:
A) fixed size baseline
B) 25% block sizing
C) Anish probe/descale/upscale sizing
D) Anish + earnings guard + liquidity filter
```

---

## 6.2 Inputs

```text
equity_start
signal_stream
entry_price
stop_price
exit_price
symbol
avg_volume
price
optional days_to_earnings
market_regime
```

`signal_stream` mevcut strategy producer'lardan gelebilir:

- Range Filter
- Supertrend
- CANSLIM proxy
- Oliver Kell swing producer
- EP / flag producer

Bu risk modülü sinyali üretmez; sinyali **boyutlandırır veya reddeder**.

---

## 6.3 Core Sizing Function

```python
def calc_anish_position_size(
    equity: float,
    entry_price: float,
    stop_price: float,
    base_block_pct: float = 0.25,
    size_multiplier: float = 1.0,
    max_account_risk_pct: float = 0.0125,
    max_position_pct: float = 0.50,
) -> dict:
    stop_pct = abs(entry_price - stop_price) / entry_price
    max_risk_cash = equity * max_account_risk_pct
    block_notional = equity * base_block_pct * size_multiplier
    risk_limited_notional = max_risk_cash / stop_pct
    hard_cap_notional = equity * max_position_pct
    notional = min(block_notional, risk_limited_notional, hard_cap_notional)
    qty = int(notional // entry_price)
    return {
        "stop_pct": stop_pct,
        "max_risk_cash": max_risk_cash,
        "notional": notional,
        "qty": qty,
        "risk_cash": qty * entry_price * stop_pct,
    }
```

---

## 6.4 Size Mode State Machine

```text
MICRO_PROBE = 0.25 * base_block = 6.25% equity
HALF_BLOCK  = 0.50 * base_block = 12.5% equity
FULL_BLOCK  = 1.00 * base_block = 25% equity
```

State transitions:

```text
START -> MICRO_PROBE
MICRO_PROBE + traction -> HALF_BLOCK
HALF_BLOCK + traction -> FULL_BLOCK
FULL_BLOCK + loss -> HALF_BLOCK
HALF_BLOCK + loss -> MICRO_PROBE
MICRO_PROBE + continued loss -> TRADE_PAUSE or MICRO_ONLY
```

Traction definition options:

```text
consecutive_wins >= 2
or rolling_last_5_trades_pnl > 0
or equity > local_equity_high
```

Loss definition options:

```text
consecutive_losses >= 2
or rolling_last_5_trades_pnl < 0
or drawdown_from_local_high >= max_recent_dd
```

---

## 7. Backtest / Research Design

## 7.1 Do Not Optimize First

Önce tek dataset ve tek sinyal akışıyla deterministic replay yapılmalı.

### Minimum Research Steps

1. Fixed-size baseline oluştur.
2. Same entries/exits with Anish sizing overlay çalıştır.
3. Sadece position sizing değiştiği için trade list same-signal kalmalı.
4. Compare:
   - CAGR / total return
   - max drawdown
   - Ulcer index
   - risk of ruin proxy
   - average exposure
   - trade count
   - losing streak impact
   - recovery time after drawdown
5. Sonra farklı market regime dönemlerinde test et:
   - trending bull
   - choppy bull
   - bear market / correction
   - post-correction rally

---

## 7.2 Acceptance Criteria

Bu modül ancak şu şartlarda değerli sayılmalı:

- Max drawdown fixed-size baseline'a göre düşmeli.
- Büyük loss streak dönemlerinde equity korunmalı.
- Trending dönemlerde performansı tamamen boğmamalı.
- Trade count artışı makul kalmalı.
- Slippage/commission sonrası hâlâ anlamlı olmalı.
- Risk budget ihlali olmamalı.
- Position size hiçbir durumda hard cap üstüne çıkmamalı.

---

## 8. MTC_V2 Integration Mapping

| Transcript Fikri | MTC_V2 Katmanı | Not |
|---|---|---|
| 1.25–2.50% account risk | Position Sizing | risk_pct / available_risk_budget |
| 25% block | Position Sizing | base_notional_pct |
| 1/8 ve 1/16 probe | PortfolioState / Sizing | size_multiplier state |
| Loss streak descale | PortfolioState guard | recent_pnl / consecutive_losses |
| Profit traction upscale | Position Manager / Sizing | progressive exposure |
| Max 50% position | Position Sizing | hard notional cap |
| Average gain/loss awareness | Exit Rules | partial / TP band |
| Earnings cushion | Entry Gate / Exit Rule | requires external calendar |
| Liquidity and price filter | Entry Gate | min price / volume / dollar volume |
| Stops always placed | Exit Rules | immediate protective SL |

---

## 9. Risk / Suspicious Claims / Caveats

## 9.1 Toy Spreadsheet Risk

Spreadsheet örnekleri öğretici; fakat gerçek piyasada şu maliyetler dahil edilmemiş olabilir:

- Slippage
- Commission
- Borrow / margin costs
- Tax impact
- Gap risk
- Bad fills
- Partial fill risk
- Liquidity deterioration

Bu nedenle model doğrudan “100 trade ile %100 return” hedefi olarak alınmamalı. Önce realistic execution engine gerekir.

## 9.2 Same-Day / Next-Day Execution Dependency

Anish sık sık hızlı çıkıştan bahsediyor. Daily bar backtest, intraday stop/recovery davranışını tam yakalayamaz.

Gerekli ayrım:

```text
OHLC-daily deterministic approximation
vs.
intraday execution model
```

## 9.3 Over-Aggressive Upscale Risk

Transcript'te Anish kendi hatalarını da gösteriyor: kazançlardan sonra büyük pozisyona geçip sonra loss streak yemek. Bu yüzden upscale modülü sınırsız olmamalı.

Gerekli güvenlik:

```text
max_total_open_risk
max_symbol_notional
max_daily_loss
max_weekly_loss
loss_streak_pause
```

## 9.4 Entry Quality Still Matters

Position sizing kötü sinyali iyi stratejiye dönüştürmez. Bu modül sadece risk ve exposure yönetir. Kullanılacağı signal producer ayrı test edilmelidir.

---

## 10. Trader Wiki Extraction

Bu dosya ayrıca Trader Wiki için çok uygun:

```text
Topic: 01_RISK_MANAGEMENT
Wiki status: WIKI_NOTE_RECOMMENDED
Suggested Wiki ID: TW_2026-05-03_RISK_MANAGEMENT_ANISH_POSITION_SIZING
Usefulness Score: 9/10
```

### Wiki Ana Dersler

- Küçük hesapta bile risk yüzdesi ciddiye alınmalıdır.
- Önce küçük test et; piyasa sana traction verirse büyüt.
- Kayıp serilerinde pozisyonu küçültmek psikolojik sermayeyi korur.
- Ortalama kazanç ve ortalama kaybını bilmeden position sizing kördür.
- Earnings'e kâr cushion olmadan girmek kumara döner.
- Pozisyon büyüdükçe stop daha sıkı ve execution daha disiplinli olmalı.

---

## 11. Suggested Registry Updates

Repo erişimi olmadığı için gerçek kayıt yapılamadı. Codex repo içinde çalışırken aşağıdaki gibi kayıt düşebilir.

### `_registry/youtube_video_index.csv`

```csv
video_id,normalized_url,title,channel,status,codex_status,transcript_hash,first_seen_at,last_seen_at,process_count,artifact_path
a4uJ3rHhbfA,https://www.youtube.com/watch?v=a4uJ3rHhbfA,The Art of Position Sizing with Anish Sikri | US Investing Championship Top Contender,UNKNOWN_CHANNEL,SALVAGE,SALVAGE_ONLY,5902a529d835019053893591a6fc58ab27f810f3ae4c7746b1a650029b234306,2026-05-03,2026-05-03,1,INTAKE_2026-05-03_a4uJ3rHhbfA_anish_sikri_position_sizing.md
```

### `channel_quality_registry.csv`

```csv
channel,status,total_processed,candidate_count,salvage_count,wiki_count,reject_count,stop_count,last_video_id,last_status
UNKNOWN_CHANNEL,UNKNOWN,1,0,1,1,0,0,a4uJ3rHhbfA,SALVAGE
```

---

## 12. Next Action

### Recommended Next Step

Bu transcript'ten immediate next action:

```text
Create isolated Python research module:
research/position_sizing/anish_position_sizing_overlay_v1.py
```

Bu modül mevcut signal stream'e uygulanmalı; yeni signal producer yazmamalı.

### Test Edilecek İlk Hipotez

```text
Anish-style probe/descale/upscale sizing overlay,
fixed-size baseline'a göre choppy periods sırasında drawdown'u azaltır;
confirmed trend periods sırasında exposure'u artırarak return'u tamamen boğmaz.
```

### Pine'a Geçiş Kararı

Şu anda Pine'a geçilmemeli. Önce Python'da state machine ve backtest overlay doğrulanmalı. Sonra MTC_V2 Position Sizing içine sadeleştirilmiş bir versiyon eklenebilir.

---

## 13. Files Created / Not Touched

### Created

- `INTAKE_2026-05-03_a4uJ3rHhbfA_anish_sikri_position_sizing.md`

### Not Touched

- `01_PINE/MTC_V2.pine`
- Production Python runner files
- Existing workflow files
- Existing registries
- Backtest outputs
- Optimization outputs
- CSV/data/cache files

---

## 14. Final Classification Block

```text
FINAL_CLASSIFICATION: SALVAGE
CODEX_STATUS: SALVAGE_ONLY
REASON: No standalone entry strategy; highly useful codable position sizing / risk management module.
MTC_V2_IMPACT: Position Sizing + PortfolioState + Position Manager + Exit Rules
PYTHON_PROTOTYPE: YES, AS OVERLAY MODULE
PINE_CHANGE_NOW: NO
BACKTEST_NOW: NO
OPTIMIZATION_NOW: NO
TRADER_WIKI: RECOMMENDED
```
