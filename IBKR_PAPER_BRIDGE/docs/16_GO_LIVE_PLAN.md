# 16_GO_LIVE_PLAN — Crypto Paper Bridge: P0 kapanışından P2 canlı testnet döngüsüne

Tarih: 2026-07-12. Yazar: Claude (denetçi + icracı). Bu doküman **model-bağımsız yürütme
planıdır**: Claude kredisi bittiğinde HERHANGİ bir model (Codex, Sonnet, DeepSeek vb.) kaldığı
yerden, Barış'a soru sormadan devam edebilmelidir. Türkçe gövde + İngilizce teknik terimler
bilinçlidir; kod/commit İngilizce yazılır.

> **"Canlı" bu planda = Hyperliquid TESTNET üzerinde kesintisiz paper-trading döngüsü (PREREG
> P2).** MAINNET/GERÇEK PARA BU PLANIN DIŞINDADIR ve üçlü kilit arkasında yasaktır; mainnet için
> Barış'tan AYRI, açık, yazılı onay gerekir. Hiçbir model bu planı mainnet'e genişletemez.

---

## §0. ONAY KAYDI (Barış, 2026-07-12 — sohbet içi, bağlayıcı)

Barış şunları PEŞİNEN onayladı; görev başına yeniden onay İSTENMEZ:

1. Bu plandaki TÜM yerel kod işleri (W, B, C görevleri).
2. P0 smoke'un **sınırlı** testnet denemeleri — geçene kadar tekrarlanabilir; her deneme: tek
   script koşusu, ~$11-12 notional, market'ten uzak resting emir, tam temizlik, dürüst log.
3. B6 "yakın-market mini fill smoke" (tek küçük gerçek fill + SL koruması + kapanış zinciri).
4. **FAZ D'NİN TAMAMI**: P2 başlatma, dashboard/API üzerinden ARM dahil. ("ben FAz D de
   yapılacak herşeyi şimdiden onaylıyorum" — Barış, 2026-07-12.)
5. Her adımda AI_memory dosyalarını güncelleyip SORMADAN devam etme talimatı.

İnsan girdisi SADECE şu noktalarda istenir (§0-İ):
- İ1: Telegram bot token + chat id üretimi (B5) — Barış üretir, env'e koyar, chat'e yazmaz.
- İ2: P2 boyunca bilgisayarın 7/24 açık kalması (uyku kapalı) — Barış fiziksel olarak sağlar.
- İ3: Mainnet'e dair HER ŞEY — bu planda yok, sorulmaz, yapılmaz.
- İ4: QuantLens/MCC tarafına strateji kaydı (golden, P3 için) — ayrı onay ister.

## §1. YÜRÜTME KURALLARI (her model için, değiştirilemez)

1. Repo: `C:\LAB\Tradingview_LAB_CLEAN`. Branch: `feature/ibkr-bridge-final`. Bir hook HEAD'i
   tool çağrıları arasında master'a döndürür → HER commit tek komutta:
   `git checkout feature/ibkr-bridge-final && git add <tam yollar> && git commit -m "..."`.
2. `HL_API_WALLET_KEY` ASLA yazdırılmaz/loglanmaz; sadece uzunluk/varlık kontrolü. Commit öncesi
   değişen dosya+loglarda `[0-9a-fA-F]{64,}` grep'i = sıfır eşleşme. (Hesap ADRESİ loglanabilir.)
3. Kimlik çözümü: `bridge/settings.py` önce süreç env, yoksa/bozuksa `HKCU\Environment` registry
   fallback (E1). Yeni süreçlerde env eksik olabilir — fallback bunun için var.
4. TESTNET-ONLY. `HL_LIVE_ACK` boş kalır. `network: testnet` değişmez.
5. Testler İKİ CWD'den de yeşil olmalı: repo kökü (`python -m pytest IBKR_PAPER_BRIDGE/tests -q`)
   ve `IBKR_PAPER_BRIDGE/` içi. `PYTHONUTF8=1` şart. Mevcut taban: **98 passed**.
6. Her görev sonunda: commit + `docs/03_STATUS.md` güncelle + görev tamamlandıysa bu dosyada
   ilgili kutuyu `[x]` yap (tek satır edit) + önemli kilometre taşlarında
   `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`'ye tarihli bölüm ekle
   (format: `## [MODEL] YYYY-MM-DD — konu`).
7. Rapor dürüstlüğü: başarısızlık başarı gibi yazılmaz; testnet koşularının tam JSON log'u
   `docs/p0_smoke_log.json` / rapor dosyasına eklenir. "Geçti" demek için kanıt gösterilir.
8. Tasarım FINAL: `docs/01_ARCHITECTURE.md` (testnet şerhleriyle) bağlayıcı. Yeniden tasarım
   yok; sapma = bu dosyaya tarihli not.
9. LLM runtime çağrıları (Grok regime / Claude veto) P2 başlangıcında KAPALI (C3'te karar
   kayıtlı). Backtest/Pine/parity/MCC değişikliği bu planın dışı.

## §2. MEVCUT DURUM (2026-07-12 gecesi)

- P1 (mock runtime) denetimden geçti. 98 test yeşil.
- P0 denemeleri 1-6: kimlik → unified bakiye → fiyat kuralı → grouping katmanları sırayla
  çözüldü. Deneme 6'da giriş emri gerçek deftere OTURDU (`resting oid 56380800181`), SL child
  `"waitingForFill"` string durumu döndü; katı parser bunu hata sayıp temizledi. **Kanıtlanmış
  gerçek format:** `statuses: [{"resting": {oid, cloid}}, "waitingForFill"]`, grouping =
  `normalTpsl` (giriş paketi), `positionTpsl` sadece mevcut pozisyonu yeniden korumak için.
- Kalan tek P0 engeli: `waitingForFill`/`waitingForTrigger` pending-child durumunun normal
  kabulü (görev W1).

## §3. GÖREV MERDİVENİ

Sıra bağlayıcıdır; [x] işaretli olan bitmiştir. Her görevde "Kabul" karşılanmadan sonrakine
geçilmez.

### FAZ W — P0 kapanışı

- [x] **W1. waitingForFill/waitingForTrigger desteği** (`bridge/broker/hyperliquid.py`,
  `tools/smoke_p0.py`)
  - `_extract_statuses`: liste içindeki string durumlardan `waitingForFill`/`waitingForTrigger`
    → `{"pending_child": "<string>"}` marker dict'ine normalize edilir; TANINMAYAN string hâlâ
    hata (ham cevapla).
  - `_verify_positioned_orders`: pending-child marker'lı rol open_orders'ta görünmese de
    AÇIKLANMIŞ sayılır → satır `status="WAITING_CHILD"`, `oid=None`. (normalTpsl child, parent
    iptalinde borsaca otomatik iptal edilir.)
  - Smoke `verify_open_orders`: sadece WAITING_CHILD olmayan cloid'lerin görünürlüğü zorunlu;
    bekleyen child'lar `pending_children` olarak loglanır.
  - Smoke `modify_stop`: pending child'da modify borsaca reddedilebilir → try/except, başarısız
    olursa WARN adımı (`modify_stop_pending_skipped`) ve devam (PREREG P0 kriterlerinde modify
    yok). İptal sırası: ÖNCE entry (parent) — child otomatik düşer; sonra kalan owned cloid'ler.
  - Testler: `[{resting},{...}"waitingForFill"]` fikstürü → entry oid'li + SL WAITING_CHILD;
    bilinmeyen string → hata; parent-cancel-kills-child davranışını simüle eden smoke birim testi.
  - Kabul: iki CWD'den tam suite yeşil (>98); secret grep temiz.
- [x] **W2. P0 deneme 7** — `PYTHONUTF8=1 python IBKR_PAPER_BRIDGE/tools/smoke_p0.py` (repo
  kökünden; PowerShell tercih ama E1 sayesinde şart değil). Beklenen: connect → account →
  candles → place (normalTpsl; entry resting + SL waiting) → verify → (modify dene, olmazsa
  WARN) → cancel → verify_cleanup → disconnect, `result: PASS`.
  - Başarısızsa: C2 ham cevabı loglar, C3 temizler; hatayı W1 tarzı yerel düzeltme + yeni deneme
    (onay §0-2 kapsamında) — döngü geçene kadar, her deneme raporlanır.
  - Kabul: `p0_smoke_log.json` PASS; `docs/14_P0_SMOKE_REPORT.md`'ye deneme bölümü eklendi;
    "P0 exit criteria MET" beyanı raporda.
- [x] **W3. P0 kapanış kaydı** — `03_STATUS.md`, `00_PREREG.md`'ye tarihli "P0 MET" notu,
  GLOBAL_HANDOFF bölümü, mimari şerh güncellemesi (kanıtlanmış cevap şekilleri).

### FAZ B — P2 öncesi zorunlu sağlamlaştırma (hepsi yerel; B6 hariç ağ yok)

- [x] **B1. Gerçek WS kopma tespiti → otomatik reconnect** (`bridge/broker/hyperliquid.py`,
  `bridge/engine/bars.py`)
  - SDK `Info`'nun ws yöneticisinden kopma sinyali yakala (ws_manager thread'inin ölümü /
    on_close callback'i / son mesaj yaşı). En sağlam taşınabilir yöntem: BarFeed watchdog'una
    "ws sağlık yoklaması" ekle — `broker.ws_alive()` (Info ws thread is_alive + son herhangi-
    mesaj yaşı) false ise `BarFeed.reconnect()` OTOMATİK tetiklenir (mevcut backoff 5→60 s).
  - Reconnect sonrası: re-subscribe (mevcut `resubscribe()`), ilk mumda dedupe (mevcut), açık
    pozisyon varsa SL doğrulaması → yoksa `reprotect_position` (mevcut) → o da olmazsa flatten.
  - Testler: sahte ws-ölümü → reconnect çağrıldı; reconnect başarısız × N → DATA_STALE/DISARM.
  - Kabul: suite yeşil; drill güncellemesi.
- [x] **B2. Reconciler eşleştirme fallback'leri** (`bridge/engine/orders.py`)
  - Sıra: cloid → `order_ref` → muhafazakâr öznitelik (coin+side+type+triggerPx+sz). Belirsiz
    eşleşme = WARN, dokunma (spec §6.5). Testler: her kademe + belirsizlik.
- [x] **B3. Gerçek user-event payload doğrulaması** — TAMAM 2026-07-13: probe aracı + B6 sırasında 5 gerçek payload yakalandı (`docs/user_events_probe.json`); parser gerçek fill/orderUpdate fikstürleriyle testli (`test_real_captured_*`).
  - `tools/probe_user_events.py`: bağlan, `userEvents`+`orderUpdates` abone ol, 60-120 sn dinle,
    gelen HER mesajın redakte ham şeklini `docs/user_events_probe.json`'a yaz, kapan. (B6
    sırasında gerçek fill mesajı da buraya düşecek.) Parser'ı gerçek şekle göre düzelt.
  - Kabul: probe dosyası commit'li; `_parse_fill_event`/`_parse_order_update` gerçek şekle karşı
    testli.
- [ ] **B4. Paper-mode uçtan uca prova (ARM YOK — read-only ağ)**
  - `python -m bridge.app` `mode: paper` ile başlat (config'te `mode: paper` zaten default;
    broker factory HyperliquidBroker'ı seçmeli — seçmiyorsa factory'yi tamamla: `dry_run` →
    MockBroker, `paper` → HyperliquidBroker(testnet)).
  - Doğrula: warmup mumları geldi; canlı mum aboneliği akıyor; saat-başı bar kapanışı gerçek
    akışta tetikleniyor (1-2 bar bekle); dashboard Overview/Trading gerçek testnet verisi
    gösteriyor; reconcile-before-ARM temiz; DISARMED kalıyor (ARM edilmez!).
  - Kanıt: `docs/screenshots/paper_probe_*.png` + `docs/03_STATUS.md` notu + events log kesiti.
- [x] **B5. Telegram notifier devreye alma** — **İNSAN GİRDİSİ İ1**
  - Barış'tan iste: BotFather'dan bot token + chat id; Windows USER env:
    `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`. (Değerler chat'e yazılmaz.)
  - Kod hazır değilse tamamla (`bridge/engine/notify.py` spec §6.7: fill/TRADE_CLOSED/WARN+/
    DISARM/KILL/regime + 6 saat heartbeat; fire-and-forget 5 sn timeout; env yoksa sessiz).
  - Kabul: stub-HTTP birim testleri + gerçek tek "bridge alive" mesajı (Barış telefonda gördüm
    der — İ1'in parçası).
- [x] **B6. Yakın-market mini fill smoke — PASS 2026-07-13** (`docs/fill_smoke_log.json`): market_open fill @64110 → positionTpsl SL gerçek defterde resting (**reprotect yolu borsada kanıtlı**, oid 56382516030) → reduce-only kapanış @64098 (pnl −0.00216 = spread) → temizlik doğrulandı. Notlar: (1) grouped-IOC giriş borsaca "could not immediately match" ile reddedildi (log tarihçesinde) — P2 engine akışı resting-LMT `place_bracket` kullandığından etkilenmez; (2) store-zincir kanıtı dürüst WARN ile P2 ilk trade'ine ertelendi. (tek gerçek fill — onaylı §0-3)
  - `tools/smoke_fill.py`: LONG BTC market-benzeri IOC girişi ~$11-12 (ya da market'in hemen
    altına LMT), doğal SL trigger'ı normalTpsl ile; fill geldiğinde: pozisyon görünür + SL
    resting doğrulanır; sonra `market_close` ile kapat; TRADE_CLOSED zinciri + fills tablosu
    dolu; tam JSON log. Tek koşu; her adım temizlik garantili.
  - Amaç: gerçek fill/pozisyon/trigger yaşam döngüsünü P2'den ÖNCE bir kez görmek; B3 parser'ını
    gerçek fill mesajıyla doğrulamak.
  - Kabul: log PASS; `fills`/`trades` satırları DB'de; rapora bölüm.

### FAZ C — Operasyon hazırlığı

- [ ] **C1. Host kararı — VARSAYILAN: yerel PC** (Barış aksini söylemedikçe). Gerekenler:
  uyku/hibernate kapalı (İ2), güç planı "yüksek performans", Windows Update yeniden başlatma
  saatleri P2 penceresi dışına. VPS'e taşıma P2 sonrası ayrı iş.
- [ ] **C2. Kalıcı süreç**: Task Scheduler görevi `MTC-Bridge-P2`: açılışta + çökmede yeniden
  başlat, `PYTHONUTF8=1`, çalışma dizini repo kökü, komut `python -m bridge.app`, stdout/err →
  `IBKR_PAPER_BRIDGE/data/logs/bridge_YYYYMMDD.log` (data/ git-ignored). Restart provası: süreci
  öldür → otomatik kalkıyor mu, KILLED/DISARMED kalıcılığı + reconcile-before-ARM doğru mu.
- [ ] **C3. Config dondurma (P2 profili)** — karar KAYITLI, uygulanacak değerler:
  `risk_pct_per_trade: 0.005`, `max_daily_loss_pct: 0.02`, `leverage: 1`,
  `max_consecutive_losses: 3`, `cooldown_minutes_after_loss: 120`, `tp_mode: none`,
  **`llm.regime_enabled: false`** (P2'de tek değişken azalt — Barış'ın genel onayı dahilinde
  kayıtlı karar; P2 ortasında AÇILMAZ), `veto_enabled: false`, `notify.telegram_enabled: true`.
  Config commit'lenir; P2 boyunca değişiklik YASAK (değişiklik = olay kaydı + P2 saatini
  sıfırlama riski).
- [ ] **C4. P2 başlatma provası (kuru)**: taze DB run'ı, reconcile temiz, ARM→DISARM→ARM
  akışı dashboard'dan MockBroker'da bir kez; sonra paper modda ARM ÖNCESİ son kontrol listesi
  (aşağıda D1) yeşil.

### FAZ D — P2: canlı testnet döngüsü (Barış TAMAMINI önceden onayladı — §0-4)

- [ ] **D1. ARM öncesi kontrol listesi** (hepsi otomatik doğrulanabilir):
  suite yeşil ×2 CWD · B1-B6 kapalı · C2 görevi aktif · C3 config commit'li · testnet bakiye
  ≥900 USDC · reconcile temiz · Telegram heartbeat çalışıyor · `p0_smoke_log.json` +
  `smoke_fill` PASS kayıtlı.
- [ ] **D2. ARM** — dashboard (127.0.0.1:8790) veya `POST /api/arm` (X-Confirm nonce ile).
  Onay: §0-4. ARM anı = P2 gün 0; `GLOBAL_HANDOFF` + `03_STATUS`'a kayıt.
- [ ] **D3. İzleme dönemi (≥10 takvim günü, 24/7)**:
  - Günlük (herhangi bir model, read-only): `/api/status`, `/api/events?severity=WARN`,
    equity eğrisi, açık pozisyon+SL tutarlılığı; anomali → Telegram zaten atmış olmalı.
  - Config DEĞİŞTİRİLMEZ; kod DEĞİŞTİRİLMEZ (kritik güvenlik hatası hariç — o zaman DISARM →
    düzelt → yeniden ARM ve 10 gün sayacı yeniden başlar; kararı ver, kaydet).
  - Abort kriterleri (PREREG §7) otomatik DISARM eder; DISARM olursa: sebep events'te,
    çözüm + yeniden ARM kaydı, "unattended" iddiası raporda dürüstçe düşülür.
- [ ] **D4. P2 çıkış denetimi** (herhangi bir model; şablon):
  ≥10 gün ARM'lı · sıfır "unexplained order state" (PREREG §5 taksonomisi) · WS kopmaları
  atlatıldı (events'te DISCONNECT→RECONNECT çiftleri) · günlük equity/risk_days dolu ·
  engine-vs-exchange equity sapması <%1 · rapor: `docs/17_P2_REPORT.md`.
- [ ] **D5. P2 kapanış kararı** — rapor Barış'a sunulur; P3'e geçiş (30 gün + slippage +
  parite) Barış onayı ister. **Parite için İ4 (QuantLens'e strateji kaydı) hâlâ açık.**

### FAZ SONRASI (bu planın dışında, hatırlatma)
- P3 değerlendirme (30 gün, slippage raporu, parite — golden şart).
- Mainnet: AYRI yazılı onay + üçlü kilit + `live_allowed` — bu plan asla yetki vermez.

## §4. HANDOFF PROTOKOLÜ (model değişiminde)

Devralan model sırayla okur:
1. Bu dosya (§3'te ilk `[ ]` görev = kaldığın yer).
2. `docs/03_STATUS.md` (anlık durum) ve `docs/14_P0_SMOKE_REPORT.md` (testnet tarihçesi).
3. `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md` son bölümler.
Sonra §1 kurallarına uyarak ilk açık görevi yapar; bitirince kutuyu işaretler, commit'ler,
STATUS+HANDOFF günceller, sormadan devam eder. Soru SADECE §0-İ noktalarında.

## §5. HIZLI KOMUT KARTI

```powershell
# testler (repo kökünden)
$env:PYTHONUTF8='1'; python -m pytest IBKR_PAPER_BRIDGE/tests -q
# P0 smoke (W2)
$env:PYTHONUTF8='1'; python IBKR_PAPER_BRIDGE/tools/smoke_p0.py
# uygulama (paper)
$env:PYTHONUTF8='1'; python -m bridge.app        # IBKR_PAPER_BRIDGE içinden
# dry-run demo
$env:PYTHONUTF8='1'; python -m bridge.app --dry-run
# secret taraması (commit öncesi)
rg -n "[0-9a-fA-F]{64,}" IBKR_PAPER_BRIDGE/docs IBKR_PAPER_BRIDGE/bridge IBKR_PAPER_BRIDGE/tools
```
