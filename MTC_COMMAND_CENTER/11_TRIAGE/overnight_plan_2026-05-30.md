# Overnight Plan — 2026-05-30 → 2026-05-31

**Hedef**: 1,000,000+ backtest case'i 8 saatte, insan müdahalesi olmadan.
**Mod**: Autonomous (kickoff sonrası uyuyabilirsin).
**Çıktı**: Sabah hazır olacak Markdown raporu + sıralanmış candidate listesi.

---

## Why this is feasible

Repo'da zaten `01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/tools/mega_walk_forward.py` var — "Overnight Edition" başlığıyla. Şu an çalıştırınca:
- **Mevcut**: 18 strateji (11 prototyped + 7 generic) × 17 sembol × 5 TF × ~80 param × 3 fold = **~367K case**
- **Hedef**: + 15 yeni candidate (bu turn'de onaylananlar) × aynı matris × 6 fold + genişletilmiş param gridler = **1,346,400 case**

Mevcut runner multiprocessing pool kullanıyor (`from multiprocessing import Pool, cpu_count`). Genişletme: yeni candidate'ları runner'ın STRATEGY_LIB'ine ekle, param grid'leri büyüt, fold sayısını 3→6'ya çıkar.

---

## Yeni onaylanmış candidate listesi (bu turn'de)

### Promosyonlu (A: 7 + Andrew = 8)
| id | source | type |
|---|---|---|
| `QL_VCP_RICHARD_1D` | QLR_Tm0dkf8_giA | full strategy |
| `QL_VCP_MINERVINI_1D` | QLR_M_tD6X0CSOI | full strategy (canonical) |
| `QL_DEEPAK_153_FILTER_1D` | QLR_lpjTNygfnzM | filter overlay |
| `QL_SELL_RULES_MARKET_WIZARDS_OVERLAY` | QLR_UD7gipBWnuY | exit overlay |
| `QL_CONNELL_EVENT_DRIVEN_GAP_1D` | QLR_kao-hhaQnig | catalyst strategy (gap+volume proxy) |
| `QL_CONNELL_EVENT_DRIVEN_GAP_5M` | QLR_kao-hhaQnig | intraday variant |
| `QL_AVWAP_BRIAN_PARENT` | QLR_UmLa9FAlMgw | parent (4 sub-cases) |
| _Christian parent_ | QLR_Lot25-2fb-4 | parent (4 sub-cases) |

### Brian Shannon AVWAP sub-cases (4)
- `QL_AVWAP_BRIAN_GAP_RECLAIM_5M`
- `QL_AVWAP_BRIAN_STAGE2_EMERGING_1D`
- `QL_AVWAP_BRIAN_INTRADAY_OR_5M`
- `QL_AVWAP_BRIAN_EARNINGS_ANCHOR_1D`

### Christian Flanders sub-cases (4)
- `QL_EPISODIC_PIVOT_CHRISTIAN_5M`
- `QL_TRAIL_20MA_CHRISTIAN_1D`
- `QL_VCP_EARLY_ENTRY_CHRISTIAN_1D`
- `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M`

### Pro Swing Ep 2 split (3)
- `QL_LAUNCHPAD_PROSWING_1D`
- `QL_HIGHEST_VOLUME_EDGE_PROSWING_1D`
- `QL_RS_PHASE_DAYS_PROSWING_OVERLAY`

### Deepak corpus (3, 1 dedupe'lu)
- `QL_DEEPAK_153_FILTER_1D` (yukarıda)
- `QL_DEEPAK_259_RISK_OVERLAY`
- `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY`

**Toplam yeni unique candidate: 19** (Brian parent ve Christian parent kendi sub-case'lerine eşit, çift saymıyoruz)

---

## Stage 1 — Spec materialization (autonomous, ~30 dk)

**Görev**: 19 yeni candidate için spec dosyalarını ve prototip skeleton'larını üret.

**Çıktı dosyaları**:
- `06_QUANTLENS_LAB/06_PROMOTED_TO_PARITY/<id>/producer_spec.json` (19 dosya, draft)
- `06_QUANTLENS_LAB/04_PYTHON_PROTOTYPES/<id>_prototype.py` (19 dosya, rule placeholder ile)

**Kural kodları**: Her prototip skeleton'u, ilgili `promotion_packets_2026-05-30.md` veya `split_packet_2026-05-30.md` veya `deepak_comparison_2026-05-30.md`'den **HIGH confidence** etiketli kuralları içerir. MEDIUM/LOW confidence kuralları yorum satırı olarak eklenir.

**Autonomous mu?** Evet — orchestrator script tüm dosyaları otomatik oluşturur.

---

## Stage 2 — Runner extension (autonomous, ~15 dk)

**Görev**: `mega_walk_forward.py`'a 19 yeni candidate'ı strategy library olarak ekle.

**Yapılacak**:
1. `STRATEGY_LIB` listesine 19 yeni entry ekle (her biri Stage 1'deki prototip dosyasından `signal_long_entry`, `signal_long_exit` import eder)
2. Her candidate için **default param grid** (50 kombo): rule paketinden çıkarılan parametreler etrafında ızgara
3. Fold sayısı: `WALK_FORWARD_FOLDS = 3` → `6` (mevcut + ek 3 OOS fold)
4. `MAX_WORKERS = min(cpu_count(), 8)` (yoğunluk kontrolü)

**Autonomous mu?** Evet — orchestrator runner'ı düzenler (geri-alınabilir patch).

---

## Stage 3 — Matrix planı

| katman | sayı |
|---|---|
| Stratejiler | 18 (mevcut) + 19 (yeni) = **37** |
| Semboller | 17 (BTC/ETH/SOL/BNB/XRP/ADA/AVAX/MATIC/LINK/LTC/DOT/ATOM/UNI/AAVE/FIL/NEAR/APT) |
| Zaman dilimleri | 5 (15m, 1h, 2h, 4h, 1D) |
| Parametre kombo / strateji | 50 (ortalama; bazıları 30, bazıları 100) |
| Walk-forward folds | 6 |
| **Toplam case** | **37 × 17 × 5 × 50 × 6 = 943,500** + Andrew Connell 5m varyantı + AVWAP 5m varyantı dahil ≈ **1,050,000+** ✅ |

8 saat × 3600 sn = 28,800 sn → **~37 case/sn ortalama** → 8 worker × ~5 case/sn = uygun (mevcut runner her case'i 0.1-0.3 sn'de çevirir).

---

## Stage 4 — Run (autonomous, 6-7 saat)

**Komut**:
```powershell
cd "C:/LAB/tradingview-lab/01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/tools"
Start-Process powershell -ArgumentList @("-NoExit","-Command","python mega_walk_forward.py 2>&1 | Tee-Object -FilePath overnight_run.log")
```

**Veya**: bizim orchestrator script (aşağıda) kickoff yapar.

**Davranış**:
- Multiprocessing Pool (8 worker)
- Her case bağımsız (parallel-safe)
- Sonuçlar `streaming_results.jsonl`'e satır satır yazılır
- Hata olunca case'i atla, log'la, devam et
- Her saatte bir checkpoint (`checkpoint_HH.json`)

**Kesinti durumu**: orchestrator script `--resume` flag'i ile son checkpoint'ten devam eder.

---

## Stage 5 — Aggregation + report (autonomous, son 30 dk)

**Görev**: Tüm `streaming_results.jsonl` satırlarını oku, candidate başına metrik tablosu üret, Deflated Sharpe + multi-test correction uygula.

**Çıktılar**:
- `06_QUANTLENS_LAB/05_BACKTEST_RESULTS/OVERNIGHT_2026-05-31/results.json`
- `06_QUANTLENS_LAB/05_BACKTEST_RESULTS/OVERNIGHT_2026-05-31/morning_report.md`
- `06_QUANTLENS_LAB/05_BACKTEST_RESULTS/OVERNIGHT_2026-05-31/top_50_by_DSR.csv`

**Morning report içeriği**:
- En iyi 50 candidate (Deflated Sharpe p-value < 0.05)
- Her candidate'in en iyi 3 (symbol × timeframe × param) kombosu
- Robustness flags: walk-forward consistency, fold variance
- "Promote to parity" önerileri (DSR + min trade count + min PF + max DD)
- "Reject" önerileri (DSR p-value ≥ 0.05)

---

## Autonomous execution — kickoff komutu

Sen kickoff'tan sonra hiçbir şey yapmazsın. Plan:

```powershell
cd "C:/LAB/tradingview-lab/MTC_COMMAND_CENTER"
python 11_TRIAGE/overnight_orchestrator.py --dry-run     # Önce dry-run gör
python 11_TRIAGE/overnight_orchestrator.py --apply       # Onaylayınca apply
```

`overnight_orchestrator.py` şu sırayla çalışır:
1. Stage 1: spec + prototype dosyalarını üret
2. Stage 2: `mega_walk_forward.py`'a yeni strateji entry'lerini ekle (git-revertable patch)
3. Stage 3: dry-run mod manifest'i göster, gerçek case sayısını rapor et
4. **Eğer `--apply` ile çalıştırıldı**: Stage 4 başlatılır → `nohup`-benzeri Windows arka plan başlatma
5. Background process tamamlandığında otomatik Stage 5 tetiklenir

---

## Recovery & safety

| Senaryo | Davranış |
|---|---|
| Sistem reboot olur | Orchestrator `--resume` ile son checkpoint'ten devam |
| Bir candidate sürekli hata verir | Case'i quarantine'e taşı, log'la, ondan sonraki ile devam |
| Disk alanı dolu | Stream batch flush + eski log compress |
| 8 saat aşılır | Her hour-checkpoint'te kalan iş tahmini → 7 saatte hala yarısı varsa otomatik parametreyi azalt (param grid yarıya) |
| Critical Python error | Crash dump kaydet, 30 sn bekle, child process restart |

---

## Honest limitations

1. **Prototip skeleton'ları kuralları "ilk geçiş" implementasyonla içerir**. Yani `QL_VCP_MINERVINI_1D` örneğin "2+ ardışık daralma + breakout + 21EMA stop" implementasyonuna sahip. Ama Minervini'nin tam SEPA filtresinin tüm detayları (RS line dynamics, follow-through day, breadth filter) ilk turda yok. İlk gece 1M case bu kabataslak implementasyonu test eder. **Sabah sıralanmış sonuç gelir; en üstteki ~10-20 candidate için ikinci turda gerçek rule code yazılır.**

2. **`QL_RS_PHASE_DAYS_PROSWING_OVERLAY`** filter overlay olduğu için tek başına çalışmaz — başka strateji ile kombine edilir. Orchestrator bunu **overlay × 5 entry strategy** olarak çoğaltır.

3. **Pip independence**: yeni candidate'ların hiçbiri MTC_V2 core'una dokunmaz. Hepsi yeni dosyalar / yeni STRATEGY_LIB entry'leri. Pine kodu değişmez.

4. **Network**: yerel veri kullanır. Internet gerekmez.

5. **Sabah kontrolün gerekecek noktalar**:
   - DSR p-value < 0.05 olan candidate'lar (gerçek)
   - Çok yüksek getiri (>100% yıllık) → muhtemelen look-ahead bug
   - 0 trade üretenler → entry rule fazla katı
   - >50% trade üretenler → rule fazla gevşek

---

## Estimated timeline (kickoff = 23:00 yerel)

| saat | aktivite | toplam case |
|---|---|---|
| 23:00 | Stage 1 başlar | 0 |
| 23:30 | Stage 2 başlar | 0 |
| 23:45 | Stage 3 dry-run | 0 |
| 23:50 | Stage 4 başlar (workers up) | 0 |
| 00:50 | Saat 1 checkpoint | ~130K |
| 03:00 | Yarı yol | ~525K |
| 06:00 | Saat 7 | ~920K |
| 06:45 | Stage 5 başlar | ~1.05M |
| 07:00 | morning_report.md hazır | DONE |

**Senin tek görevin**: 23:00'da kickoff komutunu çalıştır, sabah `morning_report.md`'i aç.

---

## Onay bekleyen tek karar

Bu planı `--apply` ile başlatayım mı, yoksa önce orchestrator'ı yazıp `--dry-run` çıktısını sana göstereyim?

**Önerim**: Önce orchestrator'ı yazıyorum (Stage 1 + 2 + 3 implementasyonu). Sen `--dry-run` çıktısını gözle. **Senin onayınla** `--apply` çalıştırır ve gece başlar.
