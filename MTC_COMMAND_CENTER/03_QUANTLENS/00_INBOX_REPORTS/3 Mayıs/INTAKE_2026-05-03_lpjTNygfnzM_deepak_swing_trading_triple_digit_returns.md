# QuantLens Transcript Intake Report

## Metadata

- **Intake ID:** `INTAKE-2026-05-03-lpjTNygfnzM`
- **Candidate ID:** `QL-CAND-20260503-lpjTNygfnzM`
- **Source URL:** https://www.youtube.com/watch?v=lpjTNygfnzM
- **Original URL in file:** `https://youtu.be/lpjTNygfnzM?si=-jxk_6fLAUXzmVNH`
- **Video ID:** `lpjTNygfnzM`
- **Title:** `153% Return in 1 Year - Simple Swing Trading Strategies for Achieving Triple Digit Returns`
- **Speaker / Trader:** Deepak / Deepak Upal *(transcript OCR/ASR içinde isim bazen “deac / deac upal” gibi geçiyor)*
- **Channel:** TraderLion / TraderLion Podcast *(transcript içinde “Trine / Trailline” gibi ASR bozulmaları var)*
- **Transcript file:** `153% Return in 1 Year - Simple Swing Trading Strategies for Achieving Triple Digit Returns.md`
- **Generated at:** `2026-05-03T18:47:42`
- **Transcript SHA256:** `f9621cd779434886442271093a63968ef0263d269af49605cf122e5d6a0c45cf`
- **Transcript Hash Short:** `f9621cd779434886`

---

## Final Classification

- **Classification:** `CANDIDATE`
- **Codex Status Onerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Strategy Usefulness Score:** `8.7 / 10`
- **Trader Wiki Usefulness Score:** `8.5 / 10`
- **Action:** Python prototype / feature-contract seviyesinde izole test önerilir.
- **Pine'a geçiş:** Şimdilik **hayır**. Önce Python tarafında atomik setup testleri yapılmalı.

### Neden CANDIDATE?

Bu transcript sadece genel trader psikolojisi değil; kodlanabilir, test edilebilir ve MTC_V2 mimarisine parçalı olarak aktarılabilecek net kurallar içeriyor:

- Trend/momentum lider hisselerde swing trading.
- Tema + lider seçimi.
- 50/200 MA trend filtresi.
- ATR / volatilite filtresi.
- Minimum fiyat / likidite filtresi.
- Progressive exposure / çalışan pozisyona ekleme.
- Liderlerde 3–5 hisseye yoğunlaşma.
- Tek trade ve toplam portföy risk limitleri.
- VIX + put/call tabanlı endeks bounce setup'ı.
- Post-earnings drift / tight flag continuation setup'ı.
- Stop-loss non-negotiable kuralı.
- Earnings öncesi risk azaltma / çıkış kuralı.

Bu nedenle video `WIKI_ONLY` değil; doğrudan candidate workflow'a alınmalı.

---

## Prompt Rule Compliance

Aşağıdaki işlemler **yapılmadı**:

- `01_PINE/MTC_V2.pine` değiştirilmedi.
- Production Python runner dosyaları değiştirilmedi.
- Backtest çalıştırılmadı.
- Optimization çalıştırılmadı.
- Büyük CSV, cache, data bundle veya optimization result oluşturulmadı.
- Secret / API key / broker / webhook bilgisi yazılmadı.
- Mevcut repo registry dosyalarına erişim olmadığı için gerçek registry update yapılmadı.

Bu rapor sadece transcript intake ve candidate değerlendirme çıktısıdır.

---

## Duplicate Check

### Conversation-Level Check

- Aynı conversation içinde daha önce yüklenen dosyalarla başlık/video ID düzeyinde duplicate görünmüyor.
- Video ID: `lpjTNygfnzM`
- Normalize URL: `https://www.youtube.com/watch?v=lpjTNygfnzM`
- Transcript hash: `f9621cd779434886`

### Repo Registry Check

Repo içindeki `_registry/youtube_video_index.csv` dosyasına bu ortamdan erişim yok. Bu nedenle final repo seviyesinde duplicate kararı verilemez.

**Codex için gerekli kontrol:**

1. `_registry/youtube_video_index.csv` içinde `video_id == lpjTNygfnzM` var mı kontrol et.
2. Yoksa `transcript_hash == f9621cd779434886442271093a63968ef0263d269af49605cf122e5d6a0c45cf` var mı kontrol et.
3. Aynı kanal + benzer başlık + benzer transcript varsa `POSSIBLE_DUPLICATE` / `MANUAL_REVIEW` yap.
4. Duplicate değilse bu rapordaki candidate önerilerini işle.

**Bu ortam kararı:** `NOT_DUPLICATE_IN_CURRENT_UPLOAD_SET`

---

## Channel Quality / Blacklist Check

- Kanal: TraderLion / TraderLion Podcast.
- Bu conversation içinde aynı kanaldan gelen önceki videoların çoğu yüksek fayda / candidate seviyesinde görünüyor.
- Repo içindeki `channel_blacklist.yaml` ve `channel_quality_registry.csv` okunamadığı için final kanal kalite state'i repo tarafından doğrulanmalıdır.

**Bu ortam önerisi:** `GOOD` veya en az `UNKNOWN -> POSITIVE_SAMPLE`

**Blacklist kararı:** `BLACKLISTED değil` varsayımıyla işleme devam edilebilir.

---

## Kısa Özet

Video, Deepak Upal'ın triple-digit return hedefleyen agresif ama kurallı swing trading yaklaşımını anlatıyor. Sistem; güçlü piyasa dönemlerinde lider temaları bulup, en likit ve volatil lider hisselerde yoğunlaşarak, kısa/orta vadeli swingleri yakalamaya dayanıyor.

Ana mantık:

1. Önce genel piyasa rejimi uygun olmalı.
2. Temalar ve lider hisseler hızlı tespit edilmeli.
3. Hisse fiyatı 50/200 günlük ortalamaların üzerinde ve trendde olmalı.
4. Hisse yeterince pahalı, likit ve hareketli olmalı.
5. Setup sıkışma, shakeout, flag, post-earnings drift veya güçlü trend dönüşü olmalı.
6. Pozisyon başarılı oldukça progressive exposure ile ekleme yapılabilir.
7. Stop-loss değiştirilemez kuraldır.
8. Piyasa choppy ise nakit pozisyon da aktif tercih olmalıdır.
9. Büyük olaylar öncesinde agresiflik düşürülmelidir.

---

## Ana Strateji Adayları

## Candidate A — Theme Leader Swing Momentum Framework

### Amaç

Güçlü piyasa dönemlerinde, en güçlü temalardaki lider hisselerde kısa/orta vadeli swing hareketlerini yakalamak.

### Kodlanabilir Kurallar

#### Universe Filter

- Asset type: US stocks / liquid ETFs.
- Minimum price: `close > 75` USD.
- Excluded groups:
  - Biotech
  - Energy
  - Metals / Mining
  - Chinese ADRs
- Preferred groups:
  - Technology
  - Semiconductor
  - AI
  - Bitcoin / crypto proxies
  - Consumer discretionary
  - Retail
  - Market ETFs

#### Trend Filter

- `close > SMA/EMA 200`
- `close > SMA/EMA 50`
- `MA50 > MA200`
- MA50 ve MA200 yukarı eğimli olmalı.

#### Volatility Filter

- `ATR_percent >= 3%`
- ATR% = `ATR(n) / close * 100`

#### Market Regime Filter

- NASDAQ / QQQ / SPY trend pozitif.
- Choppy dönemde exposure düşür.
- En agresif dönemler: yıl içindeki 2–3 güçlü momentum penceresi.

#### Entry Trigger

Bir veya birden fazla:

- Downtrend line break.
- Prior-day high breakout.
- Tight flag breakout.
- Shakeout sonrası range reclaim.
- Earnings gap sonrası 6–10 gün sıkışma ve tekrar breakout.
- Strong theme leader rotation.

#### Exit

- Initial stop: setup low / prior day low / flag low.
- Profit taking:
  - 2R–4R arası partial veya full exit.
  - Hızlı hareketlerde strength'e satış.
  - Market bozulursa risk azalt.
- Earnings öncesi genellikle çık.

### MTC_V2 Mapping

- **Signal Producer:** `THEME_LEADER_BREAKOUT`
- **Entry Gates:**
  - MA Trend Gate
  - ATR Vol Floor Gate
  - Market Regime Gate
  - Sector/Theme Strength Gate
  - Liquidity/Price Gate
- **Position Manager:**
  - concentrated position support
  - portfolio risk cap
  - add-on only if trade is working
- **Exit Rules:**
  - initial SL
  - R multiple partial exit
  - event-risk exit
  - trendline/low break exit

### Test Priority

`HIGH`

---

## Candidate B — Progressive Exposure / Add-on Framework

### Amaç

İlk breakout çalışmaya başladıktan sonra pozisyonu kademeli artırmak. Broadcom örneğinde trader ilk alımdan sonra sonraki günlerde önceki gün yüksekleri geçildikçe ekleme yapıyor.

### Kodlanabilir Kurallar

#### Initial Entry

- Base/flag/downtrendline breakout.
- İlk pozisyon daha küçük veya orta boy.

#### Add-on Trigger

- `high > prior_day_high`
- `close > prior_day_high`
- veya opening gap above prior high + continuation.

#### Add-on Constraints

- Her add-on sonrası toplam açık risk tekrar hesaplanmalı.
- Add-on sadece pozisyon kârdaysa yapılmalı.
- Add-on'ların kendi stopları olabilir.
- Toplam portfolio risk cap aşılmamalı.

#### Exit

- Son eklenen parça daha kısa stop ile korunabilir.
- Güçlü 3–5 günlük move sonrası partial sell.
- Prior day low altında kalan kısım azaltılabilir.

### MTC_V2 Mapping

- **Position Manager:** add-on / pyramiding logic.
- **Position Sizing:** risk-budget aware add-on.
- **Exit Rules:** leg-level stop veya basket stop merge.
- **Parity Note:** Pine ve Python'da add-on ID / stop ownership net olmalı.

### Test Priority

`VERY_HIGH`

Bu candidate MTC_V2 için çok değerli, çünkü position management ve pyramiding motorunun gerçek hayattaki kullanımını test eder.

---

## Candidate C — Post-Earnings Drift / Flag Continuation

### Amaç

Beklenmedik güçlü earnings sonrası, gap-up yapan lider hissede ilk momentumdan sonra 6–10 günlük sıkışma / flag oluşunca continuation trade almak.

### Kodlanabilir Kurallar

#### Catalyst Filter

- Earnings sonrası gap-up.
- Volume spike: normal hacmin 4x–5x veya daha fazlası.
- Stock yeni lider adayı olmalı.
- Tercihen daha önce herkesin bildiği overcrowded isim değil; “unexpected strength” daha değerli.

#### Waiting Phase

- Gap sonrası hemen almak yerine 6–10 gün bekle.
- Pullback / sideways tightening / flag oluşumu takip edilir.
- Shakeout sonrası toparlanma olumlu sinyal.

#### Entry Trigger

- Flag upper boundary breakout.
- Prior day high breakout.
- Tight range breakout.

#### Exit

- Stop: flag low / shakeout low.
- Profit target: 2R–4R.
- Fast climactic move olursa strength'e satış.

### MTC_V2 Mapping

- **Signal Producer:** `POST_EARNINGS_FLAG_BREAKOUT`
- **Transform:** wait-after-event confirmation window
- **Entry Gates:** volume/catalyst proxy, ATR, trend, market regime
- **Exit:** R-multiple + trailing + event risk

### Test Priority

`HIGH`

---

## Candidate D — Leveraged Index Bounce Setup

### Amaç

Piyasa kısa vadede aşırı satışa geldiğinde QQQ / TQQQ gibi endeks veya leveraged ETF'lerde bounce trade almak.

### Transcriptteki Mantık

Trader, özellikle piyasa kötü giderken tekil hisse yerine endeks trade'lerini tercih ettiğini söylüyor. Tetikleyici olarak VIX spike, put/call ratio spike ve intraday toparlanma izleniyor.

### Kodlanabilir Kurallar

#### Setup Conditions

- QQQ / SPY son birkaç günde sert düşmüş.
- VIX intraday spike yapmış.
- VIX gün içinde geri çekilmeye başlamış.
- Put/call ratio tercihen `>= 1.0`; minimum `>= 0.9`.
- Index gap-down veya sert morning selloff sonrası toparlanma göstermeli.

#### Intraday Trigger

- 5m chart üzerinde opening low sonrası higher low.
- VIX lower half close / intraday fade.
- Entry: second higher low veya reclaim.

#### Stop

- Half stop: opening low.
- Half stop: most recent intraday higher-low.
- VIX kapanışa doğru tekrar yükselirse lighten up.

#### Exit

- 1–3 günlük bounce.
- 1R–2R hızlı profit alınabilir.
- Büyük event varsa partial cash tutulur.

### MTC_V2 Mapping

- Bu setup ana MTC_V2 daily swing motorundan ayrı, intraday-aware prototype olarak test edilmeli.
- Pine günlük stratejiye hemen taşınmamalı.
- Python prototype için 5m + daily combined data gerekir.

### Test Priority

`MEDIUM_HIGH`

### Risk

- Leveraged ETF decay/slippage.
- Gap risk.
- Reversal timing zorluğu.
- VIX ve put/call verisi dış veri gerektirir.

---

## Candidate E — Concentrated Leader Rotation / Cash Concentration Risk Model

### Amaç

3–5 lider hissede yoğunlaşmak; ama piyasa choppy olduğunda nakitte yoğunlaşmayı da aktif pozisyon olarak kabul etmek.

### Kodlanabilir Kurallar

- Max active names: `3–5`
- Strongest name allocation can exceed equal weight.
- Example logic:
  - Best leader: 40–70% gross allocation
  - Others: 10–20%
  - Cash: variable
- Total open portfolio risk:
  - Preferred: `7–8%`
  - Hard cap configurable.
- Single trade risk:
  - Preferred: `1–2%`
  - Exceptional trades can be higher but prototype default conservative kalmalı.

### MTC_V2 Mapping

- PortfolioState guard.
- Max portfolio risk cap.
- Max concurrent positions.
- Market regime based exposure multiplier.
- Cash-as-position concept.

### Test Priority

`HIGH`

---

## Candidate F — Simple Rule Gate Pack

Bu video özellikle rule pack üretmek için çok uygun.

### Rule Pack

```yaml
rule_pack_id: DEEPAK_SIMPLE_SWING_RULES_V1
price_min_usd: 75
atr_percent_min: 3.0
close_above_ma50: true
close_above_ma200: true
ma50_above_ma200: true
avoid_earnings_hold: true
preferred_max_names: 5
portfolio_risk_target: 0.07_to_0.08
single_trade_risk_default: 0.01_to_0.02
sell_if_not_working: true
rebuy_allowed_if_reclaims: true
add_to_losers: false
```

### Test Priority

`VERY_HIGH`

Bu rule pack, MTC_V2 entry gates ve portfolio guards için doğrudan kullanılabilir.

---

## Evidence from Transcript

Aşağıdaki noktalar candidate kararını destekliyor:

- Trader, top 10 hissenin kazançların yaklaşık %63–65'ini ürettiğini ve çok fazla hisseye ihtiyaç olmadığını söylüyor.
- Stop-loss'u agresif trading için non-negotiable kural olarak tanımlıyor.
- 50/200 MA trend filtreleri, fiyat > 75 USD, ATR% >= 3, belirli sektörlere odaklanma gibi açık kurallar veriyor.
- Portfolio risk için yaklaşık %7–8; single trade risk için genelde %1–2 bandı veriyor.
- 3–5 hisseye yoğunlaşma ve en güçlü isimde daha büyük allocation öneriyor.
- Broadcom örneğinde progressive exposure / prior-day-high add-on davranışı anlatılıyor.
- MicroStrategy leveraged ETF örneğinde hızlı momentum trade + same/next-day profit taking anlatılıyor.
- QQQ / TQQQ bounce setup'ında VIX spike, put/call ratio ve 5m higher-low mantığı veriliyor.
- 2024 derslerinde patience, cash, event-risk öncesi agresifliği azaltma, chart/model book çalışması vurgulanıyor.

---

## MTC_V2 / Algo Trading İçin Bağlantı

Bu transcript MTC_V2 açısından özellikle şu alanlara katkı sağlar:

### 1. Entry Gates

- MA trend gate.
- ATR volatility floor.
- Price/liquidity gate.
- Theme/leader strength gate.
- Market regime gate.

### 2. Position Manager

- Concentrated portfolio.
- Add-on / pyramiding.
- Working trade confirmation.
- Rebuy after reclaim.
- No add to losers.

### 3. Sizing

- Single trade risk cap.
- Portfolio risk cap.
- Leverage-aware gross exposure.
- Event-risk de-risking.

### 4. Exit Engine

- Initial stop.
- Prior-day-low stop.
- Flag low stop.
- Partial profit taking at R multiples.
- Earnings avoidance exit.
- VIX condition failure exit for index bounce setup.

### 5. Optimization / Parity

Bu stratejiler optimize edilirken candidate atomları ayrı tutulmalı:

- Trend leader filter pack.
- Progressive add-on module.
- Post-earnings flag continuation.
- Index bounce setup.
- Portfolio concentration / risk throttle.

Her atom ayrı test edilmeden tek birleşik strateji yapılmamalı.

---

## Riskli veya Şüpheli İddialar

- %153 gibi return'ler yüksek piyasa uyumu, agresif risk, margin ve güçlü momentum rejimi gerektirir.
- Leverage ve leveraged ETF kullanımı küçük hesaplarda hızlı zarar üretebilir.
- “3–5 hisseye yoğunlaşma” güçlü sonuç verebilir ama drawdown riskini ciddi artırır.
- `ATR >= 3%` filtresi volatiliteyi yükseltir; slippage ve gap riskini de yükseltir.
- Sell-before-earnings kuralı mantıklı fakat earnings gap winner'larını kaçırabilir.
- VIX / put-call bounce setup'ı dış veri ve intraday veri gerektirir; daily-only Pine parity için dikkatli tasarlanmalı.
- Sector blacklistleri kişisel deneyime dayanıyor; sistematik olarak doğrulanmadan hard-coded yapılmamalı.
- Büyük hesap için minimum fiyat/liquidity mantığı doğru olabilir; küçük hesaplarda farklı sonuç verebilir.

---

## Proposed Candidate Registry Entry

```csv
candidate_id,video_id,status,title,channel,classification,codex_status,primary_setup,usefulness_score,transcript_hash
QL-CAND-20260503-lpjTNygfnzM,lpjTNygfnzM,NEW,153% Return in 1 Year - Simple Swing Trading Strategies for Achieving Triple Digit Returns,TraderLion,CANDIDATE,READY_FOR_PYTHON_PROTOTYPE,Theme Leader Swing Momentum + Progressive Exposure,8.7,f9621cd779434886442271093a63968ef0263d269af49605cf122e5d6a0c45cf
```

---

## Proposed Video Index Entry

```csv
video_id,normalized_url,title,channel,status,classification,transcript_hash,first_seen_at,last_seen_at,process_count
lpjTNygfnzM,https://www.youtube.com/watch?v=lpjTNygfnzM,153% Return in 1 Year - Simple Swing Trading Strategies for Achieving Triple Digit Returns,TraderLion,CANDIDATE,CANDIDATE,f9621cd779434886442271093a63968ef0263d269af49605cf122e5d6a0c45cf,2026-05-03,2026-05-03,1
```

---

## Proposed Trader Wiki Note

Bu video candidate olduğu için ana çıktı strateji candidate olmalı. Ancak ek olarak Trader Wiki'ye aşağıdaki başlıkta ikincil not da çıkarılabilir:

- **Topic:** `04_SYSTEM_DEVELOPMENT`
- **Secondary Topics:** `01_RISK_MANAGEMENT`, `05_BACKTESTING_AND_OPTIMIZATION`
- **Wiki Note Title:** `TW_2026-05-03_04_SYSTEM_DEVELOPMENT_deepak_simple_swing_rules.md`

Wiki notuna alınacak ana dersler:

- Basit kurallar karmaşık kurallardan daha uygulanabilir olabilir.
- Stop-loss agresif trading'in değişmez koşuludur.
- Market rejimine göre agresiflik ayarlanmalı.
- En iyi dönemlerde risk alınır; choppy dönemlerde cash pozisyon da aktiftir.
- Model book / geçmiş liderleri incelemek setup gözünü geliştirir.
- Her trader kendi kişiliğine uygun style bulmalıdır.

---

## Recommended Next Action for Codex

### Step 1 — Repo Safety Check

- `_registry/youtube_video_index.csv` oku.
- `channel_blacklist.yaml` oku.
- `channel_quality_registry.csv` oku.
- Duplicate yoksa devam et.

### Step 2 — Candidate Folder Create

Önerilen klasör:

```text
YOUTUBE_STRATEGY_INTAKE/candidates/QL-CAND-20260503-lpjTNygfnzM_deepak_swing_trading/
```

### Step 3 — Feature Contracts Draft

Aşağıdaki contract draftları oluştur:

```text
feature_contracts/drafts/deepak_theme_leader_swing_v1.yml
feature_contracts/drafts/deepak_progressive_exposure_v1.yml
feature_contracts/drafts/deepak_post_earnings_flag_v1.yml
feature_contracts/drafts/deepak_index_bounce_v1.yml
feature_contracts/drafts/deepak_simple_rule_gate_pack_v1.yml
```

### Step 4 — Prototype Scope

İlk etapta Pine yok. Önce Python tarafında:

1. Data availability check.
2. Rule feasibility check.
3. No-lookahead signal generation.
4. Risk model simulation.
5. Small case-set manual audit.
6. Sonra MTC_V2’ye mapping kararı.

### Step 5 — Do Not Run Yet

Bu intake aşamasında backtest/optimization çalıştırma. Sadece candidate planı ve contract draftı üret.

---

## Files Created by This Intake

Bu ortamda oluşturulan dosya:

```text
/mnt/data/INTAKE_2026-05-03_lpjTNygfnzM_deepak_swing_trading_triple_digit_returns.md
```

## Files Not Touched

- `01_PINE/MTC_V2.pine`
- Production Python runner dosyaları
- Existing candidate registry
- Existing video index
- Channel blacklist / registry
- Backtest outputs
- Optimization outputs
- CSV/data/cache bundles

---

## Final Verdict

```text
VERDICT: CANDIDATE
CODEX_STATUS: READY_FOR_PYTHON_PROTOTYPE
PRIMARY_REASON: Kodlanabilir trend/momentum swing framework + explicit risk/position-management rules + concrete trade examples.
PINE_NOW: NO
PYTHON_PROTOTYPE_NOW: YES
WIKI_ONLY: NO
DUPLICATE: NOT_CONFIRMED_IN_REPO / NOT_DUPLICATE_IN_CURRENT_UPLOAD_SET
```
