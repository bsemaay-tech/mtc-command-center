# QuantLens Transcript Intake Report

## 1. Metadata

- **Source file:** `5 Simple & Effective Trading Setups of Market Wizards.md`
- **Source URL:** https://youtu.be/lTiR1pc82EE?si=mvvql0aCc1yj_UO0
- **Normalized URL:** https://www.youtube.com/watch?v=lTiR1pc82EE
- **Video ID:** `lTiR1pc82EE`
- **Title:** `5 Simple & Effective Trading Setups of Market Wizards`
- **Channel:** `UNKNOWN_CHANNEL`
- **Report date:** 2026-05-03
- **Transcript hash SHA256:** `e7bdb6d61f99cc1a5c6fdd021f3da12af7f5e59e8fa47153d2ab2d1e0f7f759e`
- **Transcript hash short:** `e7bdb6d61f99`

## 2. Registry / Duplicate / Channel Quality Status

### Duplicate Check

- **Status:** `NOT_VERIFIED_AGAINST_REPO_REGISTRY`
- `_registry/youtube_video_index.csv` dosyası bu konuşmada verilmediği için gerçek repo duplicate kontrolü yapılamadı.
- Bu konuşma içinde şu ana kadar işlenen transcriptler bazında **duplicate görünmüyor**.
- Codex repo içinde çalıştırıldığında ilk kontrol sırası şu olmalı:
  1. `video_id == lTiR1pc82EE` daha önce var mı?
  2. `transcript_hash == e7bdb6d61f99cc1a5c6fdd021f3da12af7f5e59e8fa47153d2ab2d1e0f7f759e` daha önce var mı?
  3. Aynı kanal + benzer başlık + benzer transcript var mı?

### Channel Quality / Blacklist

- **Channel:** `UNKNOWN_CHANNEL`
- Transcript içinde güvenilir kanal adı/id bilgisi bulunmadığı için blacklist/watchlist kararı verilmedi.
- Tek video üzerinden kanal blackliste alınmamalı.

## 3. Final Classification

- **Classification:** `CANDIDATE`
- **Codex Status Önerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Candidate Type:** `MULTI_SETUP_SOURCE`
- **Primary Market:** ABD hisse senetleri / growth stocks / momentum equities
- **Secondary Market:** Futures / FX / emtia için COT crowded positioning setup
- **MTC_V2 Direct Fit:** `PARTIAL`
- **Python Prototype Fit:** `HIGH`
- **Pine Direct Fit:** `MEDIUM`

Bu transcript kodlanabilir trade stratejileri içeriyor; ancak tek bir strateji olarak değil, birkaç ayrı setup ailesi olarak ele alınmalı. İlk etapta Pine'a geçirilmemeli. Önce Python araştırma/prototip katmanında ayrı hipotezler olarak test edilmeli.

## 4. Kısa Özet

Video, “Market Wizards” tarzı trader setup’larından oluşan çok kaynaklı bir strateji derlemesi gibi duruyor. Ana fikirler:

- Tight base / VCP / pivot breakout ile düşük riskli momentum girişi.
- Episodic Pivot: beklenmeyen güçlü haber, earnings veya guidance sonrası gap ve güçlü satış büyümesi.
- Reversal Extension: aşırı aşağı uzama + yüksek zaman dilimi support + volatilite daralması sonrası dönüş.
- COT crowded positioning: futures piyasasında spekülatörlerin aşırı tek taraflı konumlandığı yerde, kötü/iyi haberin fiyatı artık hareket ettirememesi üzerine ters yönlü trade.
- High-tight flag / low-tight flag / rocket base gibi güçlü momentum sonrası sınırlı düzeltme setup’ları.

## 5. Ana Strateji Adayları

### Candidate A — Tight Base / VCP / Pivot Breakout

- **Candidate ID önerisi:** `YT_lTiR1pc82EE_A_TIGHT_BASE_VCP_PIVOT`
- **Codability:** `HIGH`
- **Setup mantığı:** Büyük bir base veya yükselen yapı içinde sağ tarafta sıkışma; daralan volatilite; pivot/squat high/reversal recovery seviyesinin yukarı kırılması.
- **Giriş:**
  - Daily chart ana karar zaman dilimi.
  - Weekly trend kontrolü yardımcı filtre.
  - Pivot veya squat high üstü kırılım.
  - Gap varsa pivot seviyesinden çok uzak olmamalı.
  - Tercihen volume average üstü ve strong close.
- **Risk / stop:**
  - İlk gün stop: breakout day low, previous day low veya matematiksel % stop.
  - Stop mesafesi ideal olarak yaklaşık `%5-%8` bandında kalmalı.
  - Breakout sonrası engulfing / megaphone genişleme / low kırılımı erken failure kabul edilebilir.
- **Exit / management:**
  - İlk 3, 5, 7, 10 gün “confirmation vs violation” takibi.
  - Follow-through yoksa azalt/çık.
  - Strong close + volume devam ederse hold/add senaryosu.
- **MTC_V2 bağlantısı:**
  - Producer: pivot breakout / range compression breakout.
  - Gates: MA trend, volume, ATR volatility floor, candle confirmation, HTF trend.
  - Exits: initial SL, BE, trailing, time stop, failure candle.

### Candidate B — Episodic Pivot: Growth / Turnaround Catalyst

- **Candidate ID önerisi:** `YT_lTiR1pc82EE_B_EP_GROWTH_TURNAROUND`
- **Codability:** `MEDIUM-HIGH`
- **Setup mantığı:** Piyasanın beklemediği bir catalyst, earnings veya guidance ile hisseyi yeniden fiyatlaması.
- **Long catalyst örnekleri:**
  - Sales growth sıçraması.
  - Guidance’ın anlamlı yukarı çekilmesi.
  - AI gibi güçlü piyasa hikâyesiyle birleşen gerçek fundamental kataliz.
  - Turnaround: uzun süre zayıf kalan şirketin satış/kârlılıkta sürpriz toparlanması.
- **Kural adayları:**
  - Gap day return threshold: örn. open-to-close veya close-to-prev-close büyük pozitif hareket.
  - Volume expansion.
  - Sales growth > `%39` gibi fundamental filtre; en az 2 çeyrek üst üste satış ivmesi daha güçlü sinyal.
  - Turnaround için önceki negatif/zayıf sales trend + yeni pozitif sales/earnings shock.
- **Risk:**
  - Catalyst’in önemli kısmı ilk gün fiyatlanabilir; extended gap chasing riski yüksek.
  - Fundamental data erişimi gerekir; sadece OHLCV ile eksik kalabilir.
- **MTC_V2 bağlantısı:**
  - MTC_V2 OHLCV tarafı catalyst gününden sonraki price/volume yapısını yönetebilir.
  - Fundamental catalyst filtresi Python research layer’da dış veriyle hesaplanmalı.
  - Pine'a geçirilirse catalyst sinyali manuel input/external screener listesi olarak daha gerçekçi.

### Candidate C — Reversal Extension into HTF Support

- **Candidate ID önerisi:** `YT_lTiR1pc82EE_C_REVERSAL_EXTENSION_HTF_SUPPORT`
- **Codability:** `HIGH`
- **Setup mantığı:** Daily timeframe’da aşırı aşağı uzama, weekly support veya 200MA gibi büyük destek alanına temas; ardından volatilite daralması ve 20MA çevresinde yeniden güçlenme.
- **Giriş:**
  - İlk aşırı düşüş gününde agresif dip alımı değil.
  - Snapback sonrası 10/20MA çevresinde consolidation beklenir.
  - Tight range bar / inside bar / unfilled gap / wedge pop gibi teyitler aranır.
  - Inside bar high kırılımı veya wedge pop giriş tetikleyicisi olabilir.
- **Stop:**
  - Probe küçük size ile yapılırsa discretionary stop.
  - Full position sonrası stop: inside bar low veya 20EMA altı.
  - Ignite bar oluşursa stop ignite bar low’a taşınır; risk hızlıca sıfıra yakınlanır.
- **MTC_V2 bağlantısı:**
  - Producer: reversal extension + inside bar breakout.
  - Gates: HTF support proximity, MA reclaim, candle pattern, ATR contraction.
  - Exits: initial SL, BE after ignite bar, trailing.

### Candidate D — COT Crowded Positioning Reversal

- **Candidate ID önerisi:** `YT_lTiR1pc82EE_D_COT_CROWDED_REVERSAL`
- **Codability:** `MEDIUM`
- **Setup mantığı:** Futures piyasasında spekülatörler aşırı long/short olduğunda; beklenen fundamental haber geldiği halde piyasa artık o yönde devam edemiyorsa ters yönlü squeeze trade.
- **Giriş mantığı:**
  - COT verisinde large/small speculators tarihsel uç seviyede.
  - Crowded tarafı destekleyen haber gelmesine rağmen fiyat devam etmiyor.
  - “News failure” veya reversal day tetikleyici.
- **Stop:**
  - Crowded short’a karşı long alındıysa reversal day low altı.
  - Crowded long’a karşı short alındıysa reversal day high üstü.
- **Exit:**
  - COT positioning neutral bölgeye dönünce edge biter; pozisyon kapatılır.
  - Alternatif: price stop veya trailing stop.
- **MTC_V2 bağlantısı:**
  - MTC_V2 içinde native COT yok; Python research layer’da dış seri gerekir.
  - Pine tarafında ancak haftalık COT import/manuel data veya sembol dışı veri entegrasyonu ile mümkün.
  - Bu setup position trading/longer-term sleeve için daha uygun.

### Candidate E — High-Tight Flag / Low-Tight Flag / Rocket Base

- **Candidate ID önerisi:** `YT_lTiR1pc82EE_E_HIGH_TIGHT_FLAG_ROCKET_BASE`
- **Codability:** `HIGH`
- **Setup mantığı:** Önce güçlü momentum pole’u; sonra sınırlı düzeltme ve flag/base; devam hareketi beklenir.
- **Kural adayları:**
  - High-tight flag: yaklaşık `%90+` yükseliş, `8 hafta veya daha kısa`; correction yaklaşık `%25` veya daha az.
  - Low-tight flag / rocket base: daha düşük momentum veya daha derin/daha uzun base varyantları.
  - Relative strength line yükseliyor olmalı.
  - Büyük kırmızı volume barları istenmez.
  - New / CANSLIM “N” faktörü: yeni ürün, yeni kategori, yeni hikâye, yeni catalyst.
- **Risk:**
  - Çok hızlı hareket eden hisselerde slippage ve spread etkisi büyür.
  - Setup ölçüleri “spirit of the rule” içeriyor; tam mekanik eşiklerde overfit riski var.
- **MTC_V2 bağlantısı:**
  - Producer: flag breakout / base high reclaim.
  - Gates: trend alignment, relative strength proxy, volume quality, ATR contraction.
  - Exits: daily low failure, BE after 15% move, trailing.

## 6. Önceliklendirme

| Rank | Candidate | Neden |
|---:|---|---|
| 1 | `A_TIGHT_BASE_VCP_PIVOT` | MTC_V2 mevcut filtre/SL/TP/position management yapısına en kolay bağlanır. |
| 2 | `C_REVERSAL_EXTENSION_HTF_SUPPORT` | OHLCV ile kodlanabilir; HTF support + contraction + inside bar mantığı net. |
| 3 | `E_HIGH_TIGHT_FLAG_ROCKET_BASE` | Momentum equity için güçlü; ama parametrelerde overfit riski var. |
| 4 | `D_COT_CROWDED_REVERSAL` | Position trading sleeve için değerli; dış veri/COT pipeline gerekir. |
| 5 | `B_EP_GROWTH_TURNAROUND` | Alpha potansiyeli yüksek; fakat fundamental/catalyst veri ihtiyacı nedeniyle ilk Python prototipi daha karmaşık. |

## 7. Python Prototype Planı

### İlk Prototip: Candidate A + C

Önce sadece OHLCV ile test edilebilen iki setup prototiplenmeli:

1. `TIGHT_BASE_VCP_PIVOT`
2. `REVERSAL_EXTENSION_HTF_SUPPORT`

Minimum feature set:

- Daily OHLCV.
- Weekly HTF trend/support proxy.
- Moving averages: 10/20/50/200.
- ATR / percent range contraction.
- Inside bar detection.
- Pivot high / base high reclaim.
- Volume average ratio.
- Stop: swing low / inside bar low / ATR / percent.
- Exit: time stop, BE, trailing, failure day.

### İkinci Prototip: Candidate E

- Momentum pole detection.
- Flag correction depth.
- Flag duration.
- RS proxy: symbol return vs benchmark return.
- Breakout with volume filter.

### Üçüncü Prototip: Candidate D

- COT weekly dataset gerekir.
- Crowding percentile hesaplanmalı.
- News failure yerine ilk aşamada price reversal proxy kullanılabilir.

### Dördüncü Prototip: Candidate B

- Fundamental data gerekir: quarterly sales growth, earnings, guidance surprise.
- İlk aşamada gap + volume + post-earnings drift proxy ile eksik versiyon test edilebilir.

## 8. Backtest / Validation Notları

- İlk test **Pine değil Python** olmalı.
- Survivorship bias'a dikkat edilmeli; sadece bugün bilinen başarılı hisselerle test yapılmamalı.
- Equity universe gerekiyorsa tarihsel index membership veya geniş historical screener evreni gerekir.
- Slippage/spread özellikle thin momentum stocks için önemlidir.
- Earnings/fundamental data kullanılırsa point-in-time veri şarttır.
- Strategy validation mutlaka out-of-sample, cross-market ve farklı rejimlerle yapılmalı.

## 9. MTC_V2 ile Bağlantı

Bu transcript doğrudan MTC_V2’ye şu alanlarda fayda sağlar:

- **Signal producer fikirleri:** pivot breakout, inside bar breakout, flag breakout, reversal extension.
- **Entry gates:** trend alignment, HTF support, volume confirmation, volatility contraction, relative strength.
- **Position manager:** probe vs full position ayrımı gelecekte eklenebilir; mevcut MTC max_entries/add logic buna uyarlanabilir.
- **Exit rules:** failure candle, day low break, time stop, BE after ignite/strong move, trailing stop.
- **Regime:** momentum/growth equity rejimi için ayrı asset sleeve gerekebilir.

## 10. Riskli veya Şüpheli İddialar

- `%39 sales growth` eşiği her piyasa ve her sektör için sabit alpha üretmeyebilir; veri madenciliği riski var.
- “Spirit of the rule” anlatımı mekanik testte net eşiklere çevrilirken overfit doğurabilir.
- Video örnekleri çoğunlukla başarılı trade/case study örnekleri olabilir; selection bias yüksek.
- Intraday discretionary management anlatılmış; bunu daily OHLCV backtest’e doğrudan taşımak parity hatası yaratabilir.
- COT verisi haftalık ve gecikmelidir; day-trading değil orta/uzun vadeli pozisyonlama mantığına uygundur.

## 11. Trader Wiki Ayrımı

- **WIKI_ONLY değil.** Çünkü transcript kodlanabilir strategy candidate içeriyor.
- Buna rağmen şu konular Trader Wiki’ye ikincil not olarak çıkarılabilir:
  - Risk as selection tool.
  - Confirmation vs violation yaklaşımı.
  - Crowded positioning ve news failure kavramı.
  - Probe position vs full position yönetimi.

## 12. Önerilen Repo Çıktıları

Codex repo içinde çalıştığında önerilen dosyalar:

```text
06_QUANTLENS_LAB/youtube_intake/candidates/YT_lTiR1pc82EE/INTAKE_REPORT.md
06_QUANTLENS_LAB/youtube_intake/candidates/YT_lTiR1pc82EE/TRANSCRIPT.md
06_QUANTLENS_LAB/youtube_intake/candidates/YT_lTiR1pc82EE/strategy_hypotheses.yaml
06_QUANTLENS_LAB/youtube_intake/_registry/youtube_video_index.csv
06_QUANTLENS_LAB/youtube_intake/_registry/channel_quality_registry.csv
```

## 13. Dokunulmaması Gerekenler

Bu intake sonucunda şu dosyalara dokunulmamalı:

- `01_PINE/MTC_V2.pine`
- Production Python runner dosyaları
- Optimization result klasörleri
- Büyük CSV/data bundle/cache dosyaları
- Broker/exchange/webhook secret içeren dosyalar

## 14. Next Action

- Bu video **candidate olarak saklanmalı**.
- Codex gece çalışmasında önce `A_TIGHT_BASE_VCP_PIVOT` ve `C_REVERSAL_EXTENSION_HTF_SUPPORT` için OHLCV-only Python prototypes çıkarmalı.
- `B_EP_GROWTH_TURNAROUND` ve `D_COT_CROWDED_REVERSAL` ayrı veri ihtiyacı nedeniyle ikinci faza bırakılmalı.
- Pine implementasyonuna geçilmemeli; önce Python research report + minimum viable backtest sonuçları incelenmeli.
