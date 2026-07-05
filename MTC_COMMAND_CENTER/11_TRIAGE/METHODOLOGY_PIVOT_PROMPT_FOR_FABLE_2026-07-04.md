# Görev: Metodoloji tıkanıklığı hakkında bağımsız inceleme + net öneri

> Bu prompt kendi kendine yeter. Repo'yu taramana gerek yok — karar için gereken tüm teknik bağlam aşağıda. Kod dosyası açman gerekmez; istersen sadece doğrulama için 1-2 dosyaya bakabilirsin, ama zorunlu değil.

## Rolün
Sen Claude Fable'sın. MTC Command Center adlı bir quant strateji backtest/optimizasyon platformunda 4 gecelik sistematik bir araştırma yapıldı ve **yapısal bir tavana** çarpıldı. Senden istenen: aşağıdaki kanıtı bağımsız incele, önceki AI'nın "strateji eklemeyi bırak, metodolojiyi düzelt" teşhisini **onayla veya çürüt**, ve **net, önceliklendirilmiş tek bir öneri** ver. Sonra, kullanıcı (Barış) onayına bağlı olarak, uygulamayı yapacak başka bir ajan için **eksiksiz bir uygulama promtu** hazırla.

Kullanıcı senden "evet/hayır" değil, **kendi analizini** istiyor. Önceki AI'nın öneri listesini tekrar etme — eleştir, önceliklendir, gerekiyorsa itiraz et.

---

## 1. Sistem nasıl çalışıyor (motor + validasyon)

**Araştırma motoru:** `mega_walk_forward.py` (QuantLens). Her strateji için:
- Bir **parametre grid'i** (örn. Donchian: kanal uzunluğu × ATR çarpanı = N node) süpürülür.
- Her (strateji × sembol × timeframe × grid-node × walk-forward-fold) bir **hücre (cell)** üretir.
- Case sayısı ≈ Σ_strateji(grid_size) × semboller × TF'ler × fold'lar. Tipik gece ~1M–4M hücre.

**Execution modeli (GLOBAL, SABİT — hiçbir şey optimize etmiyor):**
- Giriş: sinyal barından **sonraki barın açılışı** (next-bar-open, lookahead-safe).
- Stop: girişte sabitlenir (stratejiye göre ATR veya swing).
- Hedef: sabit **2R** (risk'in 2 katı).
- Zaman limiti: **96 bar** (HOLDING_BAR_LIMIT) — dolmadan çıkılmazsa piyasa fiyatından kapanır.
- Maliyet: 8 bps (COST_BPS).
- **Bu exit modeli her strateji için aynı ve hiçbir parametresi süpürülmüyor.**

**4-gate validasyon:**
```
robust_final = PASS  ∧  bh_fdr_survivor  ∧  dsr_robust
```
- **PASS**: hücre temel performans + yeterli-trade eşiğini geçti (aksi: INSUFFICIENT_TRADES / FAIL / NO_DATA).
- **bh_fdr_survivor**: Benjamini-Hochberg FDR çoklu-test düzeltmesinden sağ çıktı (tüm hücreler havuzunda).
- **dsr_robust**: **Deflated Sharpe Ratio** (Bailey & López de Prado) eşiği geçti. Kurumsal bar `dsr_p_value ≥ 0.95`, araştırma barı `≥ 0.50`. Şu an **0.95** kullanılıyor.
- Determinizm: bootstrap seed = `md5(strategy|symbol|tf)` → **aynı sweep'i tekrar koşmak sıfır yeni bilgi verir** (aynı sonuç). Bütçeyi tekrar-koşuyla doldurmak anlamsız.

**DSR nedir / neden kritik:** Deflated Sharpe, gözlenen Sharpe'ı **kaç konfigürasyon denendiğine** göre cezalandırır. Trial sayısı ≈ grid boyutu. Yani grid ne kadar genişse, DSR'ın 0.95 barını geçmek o kadar zor (ham edge devasa değilse). Bu, **A17 anti-pattern'i**: *grid genişletmek DSR'ı KÖTÜLEŞTİRİR.*

---

## 2. Test edilen evren

- **Semboller:** 51 sembol tek bir "multiasset" ailesinde havuzlanmış — likit US equities (AAPL, GOOGL, AMD...), ETF'ler (SPY, QQQ, LQD, IEF...), VE micro-price crypto (SHIBUSD, DOGEUSD, UNIUSD...).
- **Timeframe'ler:** 7 TF (10m/15m/30m/1h/2h/4h/1D civarı).
- **Fold:** 3–6 walk-forward fold.
- **Strateji evreni:** 51 mevcut archetype (klasik: Donchian/Turtle, EMA pullback, MACD, RSI, BB, golden-cross vb.) + son gece eklenen **12 tamamen-yeni archetype**.

---

## 3. 4 gecelik sonuç (asıl kanıt)

| Gece | Kapsam | Sonuç |
|---|---|---|
| 07-01 | Turtle varyantları + heavy tier | robust_final **0** (derin CPCV+PBO≈0 bile) |
| 07-02 | Tüm executable evren (~51 archetype) + varyantlar, 11,781 hücre | robust_final **0** |
| 07-03 | **12 GENUINELY-NEW archetype** (kütüphanenin hiç kullanmadığı sinyaller: volume climax, session gaps, volatility-regime switch, **gerçek per-session VWAP**, inside-bar breakout, range-expansion), 4284 hücre, 6 fold | robust_final **0** |

**Kümülatif: 63 archetype (51 mevcut + 12 yeni), tüm asset/TF'lerde robust_final = 0.**

**Kritik nüans — gate'ler HİÇ hizalanmıyor:**
- Birkaç yeni archetype tek tek hücrelerde **DSR 0.99** vurdu (RANGE_EXPANSION_THRUST / LQD-30m; HIGH_PROXIMITY_PULLBACK / AMD-2h; VOL_REGIME_SWITCH 0.88 / GOOGL-1h).
- **AMA hepsi INSUFFICIENT_TRADES hücrelerinde** — yani DSR barını tam da trade sayısının güvenilmeyecek kadar az olduğu yerde geçiyor (küçük-örneklem lotaryası).
- Trade sayısı yeterli olduğu her yerde DSR çöküyor.
- Bu arada en yüksek getiriler (RELVOL SHIBUSD +166%) dsr=0'da oturuyor (micro-price compounding artifact / overfit).
- Yani "yüksek DSR + düşük trade" = edge DEĞİL.

---

## 4. Önceki AI'nın teşhisi (senin sınayacağın hipotez)

**Teşhis:** Yeni mantık + yeni sinyal kaynakları da 0 verince, darboğaz **strateji seçimi değil, yapısal/metodolojik.** Dört kök neden öne sürüldü:

1. **A17 — DSR trial-count deflation:** grid ≥ ~15 node → 0.95 barı neredeyse ulaşılamaz. Neredeyse her şeyi tek başına kapatıyor.
2. **Sabit exit (2R / 96-bar / next-open):** hiçbir şey tarafından optimize edilmiyor. *Muhtemel asıl bağlayıcı kısıt* — giriş mantığı ne kadar iyi olursa olsun, tavanlanmış ve ayarlanmamış bir exit'i yenemez.
3. **Micro-price crypto (SHIB/DOGE/UNI):** compounding artifact'lar her leaderboard'un tepesini domine ediyor, BH-FDR/DSR havuzunu kirletiyor.
4. **Multi-asset pooling:** 51 heterojen sembol tek ailede, herhangi bir per-regime edge'i seyreltiyor.

**Önerilen yol (metodoloji, daha çok strateji değil) — önceliklendirmeyi SEN yapacaksın:**
- **(a)** Micro-price crypto'yu hariç tut / winsorize et → yeniden skorla. *(onaysız, hızlı)*
- **(b)** Sert **MIN_TRADES floor** + araştırma-robust **DSR ≥ 0.50** barı (0.95 yerine). *(onaysız, hızlı)*
- **(c)** **Exit'i süpürülen knob yap** (2R vs 3R vs trailing vs ters-kanal) — bu **engine-core `simulate_slice` değişikliği** = **Faz 3b, ONAY GEREKTİRİR**. En yüksek kaldıraç olduğu iddia ediliyor (sabit exit en olası gerçek tavan).
- **(d)** Tek asset-class subset (sadece likit US equities) — 51-sembol havuzlama yerine. *(onaysız)*

---

## 5. Kısıtlar (uygulama promtunu yazarken bunlara uy)

- **ASLA sonuç uydurma:** `backtest_profile_result.json` / `top_results.json` elle yazılmaz. Gerçek koşu yoksa sonuç yoktur.
- **Robust olmayan hiçbir şey promote edilmez** (`robust_final` şart).
- **Git disiplini:** `master`'da çalışılmaz — önce `feature/<scope>` branch. Sadece açık, tam dosya yolları stage'lenir (`git add .`/`-A` YASAK). `checkout`/`reset --hard`/`stash`/`--no-verify`/`push --force` onaysız YASAK. (Repo, tool çağrıları arasında HEAD'i master'a geri çeviren bir hook'a sahip — commit'i inline checkout+add+commit ile yap.)
- **Korumalı scope'lar (Barış onayı şart):** `02_MTC_BACKTEST`, `07_ADAPTERS`, `01_PINE`, `MTC_V2`, `06_SCHEMAS`, `.git`. **Engine-core `simulate_slice` bu kapsamda → (c) seçeneği onay-kapılı.**
- Pine/parity/trading-logic onaysız düzenlenmez. Alpaca anahtarı paper-only.
- **Token disiplini:** mekanik işi mümkünse ucuz ajana (DeepSeek) devret.

---

## 6. Senden istenen çıktı (tam olarak bu sırayla)

**A) Bağımsız inceleme.** Teşhisi sına. Özellikle:
- 4 kök nedenin gerçekten bağımsız mı yoksa iç içe mi (örn. sabit-exit ve DSR-deflation aynı madalyonun iki yüzü mü)?
- "Ceiling metodolojik" sonucu kanıttan **gerçekten** çıkıyor mu, yoksa alternatif bir açıklama var mı (örn. bu asset/TF/exit rejiminde gerçekten sistematik edge yok — yani "metodoloji" değil "piyasa" tavanı)?
- İnsufficient-trades'teki yüksek-DSR nüansı senin yorumunda ne anlama geliyor?
- Gözden kaçan 5. bir faktör var mı?

**B) Net öneri.** Süs yok. Hangi değişiklik(ler), hangi sırayla, neden. Özellikle: **onaysız (a/b/d) paketini önce mi koşmalı** (mevcut 63 archetype'ı temiz metodolojiyle yeniden-skorlar; belki bazıları bu barda robust çıkar), yoksa doğrudan **(c) exit-knob onayına mı** gitmeli? Beklenen bilgi kazancını gerekçelendir.

**C) Onaya bağlı ajan promtu.** Barış "onaylıyorum" derse uygulamayı yapacak ajan için **eksiksiz, kendi kendine yeten bir prompt** yaz. İçermeli: tam adım listesi, dokunulacak dosyalar, hangi adımın onay-kapılı olduğu (engine-core), doğrulama kriteri (nasıl "işe yaradı" denecek — hangi metrik, hangi hücre sayısı), ve yukarıdaki tüm kısıtların (sonuç-uydurma-yasak, git disiplini, robust-final-şart) tekrarı. Onaysız (a/b/d) ve onaylı (c) için **ayrı** bloklar yap ki Barış kısmi onay verebilsin.

Türkçe cevap ver, teknik terimleri İngilizce koru.
