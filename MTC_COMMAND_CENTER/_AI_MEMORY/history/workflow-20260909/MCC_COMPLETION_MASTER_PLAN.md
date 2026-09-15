# MCC Completion — Master Work Plan

> **Merge provenance:** Claude (ana plan) + Codex (UI komponentleri, Gate3 Evidence
> Contract, delegation split, readiness report) + DeepSeek V4 Pro (mevcut-durum
> sayıları, doğrulama). Üç plan 2026-06-06'da birleştirildi.

> **Amaç:** `MTC Command Center ARCHITECTURE.md` (v2.3) ile tasarlanan mimariyi
> tamamen bitirmek + 63 stratejinin her birini pipeline'da gidebildiği kadar
> ilerletmek. Hazırlayan: Claude Opus 4.8, 2026-06-06.
>
> **Kapsam (Barış'ın 4 maddesi):** (A) UI eksikleri, (B) tüm stratejilerin
> pipeline'da ilerletilmesi, (C) Gate3 tamamlanması, (D) gece-üretimi tüm bilginin
> UI'da görünmesi.
>
> **Disiplin (architecture sabit kuralları — değişmez):** read-only-first,
> no live trading MVP'de, MTC_V2.pine / MTC_v2 core'a onaysız dokunma yok,
> her executed sonuç lineage'lı, schema-validated yazımlar, single-writer.
>
> **Dürüstlük çerçevesi (bu sezonun bulguları):** "İlerlet" ≠ "promote et".
> Çoğu aday DSR-floored (istatistik duvarı) → onlar dürüstçe FORWARD_PAPER /
> SALVAGE'da durur. Gate3 backtest değil **entegrasyon** işi. Plan bunu kabul eder.

---

## PROGRESS — 2026-06-06 (Claude, otonom)

**DONE:**
- ✅ **B1** pipeline envanteri → `PIPELINE_STATE.md` (176 row; 11 backtested, 86 walk-forward-gerek, 76 park; promotable 0). DeepSeek'in 196/22/22 sayıları düzeltildi.
- ✅ **C1 Gate3 builder** → `enrich_gate3_evidence.py` (honest, spec-derivable→OK, integration→N_A). Gate3 **30→46/100 INCOMPLETE** uygulandı: final_gate2 (38) + heavy_tier (72) + new_strategies (2). promotable=0 (doğru). C0a contract'a uygun.
- ✅ **D1 auto-export** → `backtest_reader.py` run subdir'lerini otomatik tarıyor (8 run görünür, dupe yok, 35 test PASS). Manuel kopya bitti.
- ✅ **Gece altyapısı** → `mcc_night_tail.sh` (CPCV15+PBO+eval+Gate2+all-gate+C1+scorecard_v2+alpha+morning+D1-verify, uçtan-uca test) + `night_runner.sh` (smoke→sweep→tail→release) + `NIGHT_BATCHES.md`.
- ✅ **3 karar kapandı** (C0a/C0b/promosyon) → memory + plan.

**SCOPED (sıradaki):** A1 (producer_spec.json üretimi — 06_PROMOTED_TO_PARITY boş, "Not defined yet" kökü; N1 batch) · N5 (86'dan codeable audit) · A5-A7/D4 (Codex UI) · C2/C3 (Barış onayı).

---

## 0. Mevcut durum (grounded, 2026-06-06)

| Katman | Durum |
|---|---|
| **Architecture** | v2.3 yazılı, sağlam. Implementation MVP-1'i geçti. |
| **Dashboard readers** | 20+ reader mevcut (backtest, scorecard, quantlens, pipeline, parity, optimization, research, registry, liveops, pine_builder, mtc_v2...). |
| **UI (app.js, 2200 satır)** | SP-005 Wave A/B/C DONE: detail page, QuantLens verdict card, scorecard_v2 gate render. Ama strateji alanları çoğu **"Not defined yet"** (producer_spec'ler placeholder). |
| **Gate scorers** | score_gate1 / 1b / 2 / 3 / all_gates HEPSİ mevcut + audited. |
| **Gate2** | Metrikler tam (6 enrichment commit). Fresh sweep'te scorable: 53/72 PASS (heavy_tier). |
| **Gate1/1B** | Sadece coded MEGA evidence'tan skorlanıyor → OK ama intake/feasibility artifact'leri eksik. |
| **Gate3** | **BLOCKER. `score_gate3.py` var ama `production_readiness_artifact` ÜRETEN builder YOK.** Tüm scorecard'lar Gate3=INCOMPLETE → promotable=0. |
| **Strateji envanteri** | Registry 63. Engine GRIDS 43 (+1 yeni STG056). 63'ün çoğu producer_spec `review_needed`. |
| **Pipeline (per pipeline_reader, N5'te doğrula)** | ~196 row · 22 backtested · 22 promoted · 1 pre_parity (LINK) · **0 integrated**. Gate1/1B 38/38 OK. Dashboard 14 tab functional. |
| **Gece-veri → UI** | backtest_reader top-level `*_results.json` glob'lar. heavy_tier + new_strategies elle export edildi → görünür. Loop'lar OTOMATIK export etmiyor; scorecard_v2 auto-link kısmi. |
| **Pine Builder / Parity** | Reader'lar var; STG→Pine draft akışı işletilmemiş. |

---

## Workstream A — UI / Dashboard tamamlanması

**Hedef:** Architecture §12'deki 15 modülün hepsi gerçek veriyle dolu; "Not defined
yet" yerlerin maksimumu gerçek içerikle dolsun; boş-durum'lar dürüst kalsın.

### A1 | Strateji içerik doldurma (producer_spec) — UI'daki "Not defined yet" kökü
- **Problem:** 63 stratejinin producer_spec/metadata alanları `review_needed` → UI'da entry/exit/stop/TP/trailing hep "Not defined yet". RESEARCH-002 bu.
- **İş:** Her `STGxxx/07_deterministic_spec.md` zaten dolu (kontrol edildi — STG056/057 vb. detaylı). Bir **spec→metadata extractor** yaz: `07_deterministic_spec.md` + `01_candidate_metadata.yaml`'dan entry/exit/stop/TP/trailing/avoid alanlarını doldur, `build_strategy_research_registry.py`'yi besle. Generated registry'yi elle düzenleme (AGENTS.md).
- **AI:** DeepSeek (extractor) + Claude audit. **Bağımlı:** yok. **Kabul:** registry regen sonrası ≥40 stratejide entry/exit/stop dolu; dashboard'da "Not defined yet" oranı düşsün; `node --check` + API testleri PASS.

### A2 | Gece-run scorecard'larını UI'a bağla (otomatik)
- **Problem:** scorecard_v2 sadece belirli run'lara link'li; heavy_tier/new_strategies kartları kısmi.
- **İş:** `scorecard_reader.py`'yi tüm `05_BACKTEST_RESULTS/*/scorecard_v2/` dizinlerini tarayacak şekilde genişlet (en yeni run'ı tercih et, base strategy id ile audit/pipeline row'a bağla). WS-D ile beraber.
- **AI:** Claude. **Bağımlı:** D1. **Kabul:** dashboard snapshot heavy_tier 72 + new_strategies 2 kartını gate durumlarıyla gösteriyor.

### A3 | Eksik dashboard modülleri envanteri + boş-durum
- **İş:** §12'nin 15 modülünü tek tek denetle (Home, Task Board, Parity Matrix, Case Explorer, Backtest Lab, Optimization Lab, QuantLens Intake, Strategy Registry, Pine Builder, Reports Center, Data Health, Worker Monitor, AI Handoff, LiveOps, Settings). Her biri: reader var mı? UI render var mı? boş-durum dürüst mü? Bir **GAP_MATRIX.md** üret.
- **AI:** Claude (read-only audit). **Bağımlı:** yok. **Kabul:** 15 modül × {reader, UI, veri, boş-durum} matrisi; eksikler task'a dönüşür.

### A4 | Strategy Research Lab sekmeleri (Missing Metadata / Triage / Variant)
- **İş:** A1 sonrası "Missing Metadata" sekmesi azalan review_needed'ı yansıtsın; Triage Worklist + Variant Log canlı.
- **AI:** Codex/Claude. **Bağımlı:** A1. **Kabul:** üç sekme gerçek registry verisiyle dolu.

### A5 | Backtest Evidence görselleri (Codex) — strateji detayında
- **İş:** Strateji detay sayfasına her hücre için kanıt görselleri: **MEGA run özeti ·
  CPCV sonucu · PBO · B&H/EMA benchmark · slippage stress · regime breakdown ·
  param-stability · worst-window drawdown.** Veri zaten eval artifact + scorecard_v2'de
  var (Gate2 enrichment commitleri). Sadece render.
- **AI:** Codex/Claude. **Bağımlı:** A2, D2. **Kabul:** bir hücre kartında 8 kanıt bloğu görünür; veri yoksa dürüst boş-durum.

### A6 | "Why not promotable" paneli (Codex)
- **İş:** Her strateji için **neden promote edilemiyor** panelini açıkça göster:
  Gate3 missing · Gate2 fail · missing source · insufficient evidence ·
  schema/artifact missing. `scorecard_v2.gate_summary.blocking`'den türet.
- **AI:** Claude. **Bağımlı:** A2. **Kabul:** her non-promotable kart blocker'ını tek bakışta gösteriyor.

### A7 | Filtreler (Codex)
- **İş:** Liste/grid filtreleri: Gate2 OK · Gate3 incomplete · promotable false ·
  strongest candidates · blocked-by-source · blocked-by-production-readiness.
- **AI:** Codex. **Bağımlı:** A2/A6. **Kabul:** filtreler doğru alt-kümeyi getiriyor.

### A8 | Global kabul kriteri (Codex)
- Dashboard, **dosya açmadan** şu soruyu cevaplamalı: *"en iyi ne, ne bloke, neden,
  sıradaki aksiyon ne?"* — Workstream A'nın bütününün tek cümlelik acceptance'ı.

---

## Workstream B — Tüm stratejilerin pipeline'da ilerletilmesi

**Hedef:** 63 stratejinin her birini gidebildiği en ileri gate'e taşı. Pipeline:
`INTAKE → TRIAGE → PYTHON_PROTOTYPE → BACKTEST(Gate2) → CPCV/PBO → DECISION(reject/salvage/forward-paper/promote)`.

### B1 | Pipeline durum envanteri (her strateji nerede?)
- **İş:** 63 strateji × mevcut gate durumu tablosu. Kaynaklar: registry current_status, eval artifacts, scorecard_v2. Bir **PIPELINE_STATE.md** üret: her strateji için en ileri gate + sıradaki aksiyon + blocker.
- **AI:** Claude. **Kabul:** 63 satır, her birinde next-action.

### B2 | Kodlanabilir ama engine-dışı stratejileri kodla (monkey-patch)
- **Durum:** STG056 DONE (`strat_extra_runner.py`). Kalan READY_FOR_* adaylar: STG057 (LBR), STG054 (fishhook), STG047 (smallcap short). STG052 (CANSLIM) **veri yok** (fundamentals) → kodlanamaz, dürüstçe işaretle.
- **İş:** Her uygun strateji için `strat_extra_runner.py` pattern'iyle signal+grid ekle → sweep → CPCV/PBO/Gate2. **Threshold/pattern judgment gereken yerlerde (STG057 ROC2 eşiği vb.) Barış pre-register etmeli** (sonuç görüp eşik seçmek = cherry-pick, DSR geçersiz).
- **AI:** Claude (kodlama) + Barış (pre-registration). **Bağımlı:** B1. **Kabul:** her kodlanan strateji bir run dir + scorecard üretir; verdict dürüst (çoğu DSR-floored beklenir).

### B3 | Dar pre-registered confirmation grid (DSR kurtarma)
- **Problem:** Geniş discovery DSR'ı öldürüyor (A17/C7 — heavy_tier'de 0/72 geçti). Tek istatistiksel-geçerli yol: en az-zayıf hücrelere (DEEPAK_SNAPBACK TRX 2h DSR 0.42, vb.) **Barış'ın önceden kaydettiği** dar hipotez grid'i.
- **İş:** Barış 3-5 hücre için hipotez+dar grid pre-register eder → confirmation run → DSR yeniden ölç. Geçen olursa FORWARD_PAPER adayı.
- **AI:** Barış (pre-register) + Claude (run). **Bağımlı:** B1. **Kabul:** confirmation run raporu; DSR≥0.50 geçen hücre listesi (muhtemelen küçük/sıfır — dürüst).

### B4 | Forward-paper observation kuyruğu
- **İş:** DSR-floored ama CPCV-robust + alpha-pozitif adayları (architecture §12.7 pipeline'da PROMOTE_TO_FORWARD_PAPER) live-bar OOS toplamak üzere işaretle. Pine/MTC/live YOK — sadece gözlem kaydı.
- **AI:** Barış karar + Claude kayıt. **Kabul:** forward-paper listesi + her biri için neden.

---

## Workstream C — Gate3 production-readiness tamamlanması (ASIL BLOCKER)

**Hedef:** Promotable=0 tıkacını kaldır. Gate3 = backtest değil, **MTC entegrasyon
evidence**'ı (signal_contract /25, alert_adapter /20, state_sync /15,
risk_engine_compat /15, monitoring /10, fail_safe /10, reproducibility /5).

### C0a | KARAR: `APPROVE GATE3 EVIDENCE CONTRACT` (Codex — policy, kolay onay)
- **Politika:** Gate3 sadece **gerçek** signal/alert/state/risk/fail-safe evidence'tan
  OK işaretlenir — backtest sonucundan ASLA türetilmez. Evidence yoksa INCOMPLETE kalır.
  (Schema zaten bunu emrediyor; bu onay sözleşmeyi resmileştirir → C1'i açar.)
- **Bu tek onay C1'i (spec-derivable builder) bloke etmeyi kaldırır.**

### C0b | KARAR: "Production" kapsamı (scope — zor karar)
- Gate3 hedefi **(a)** MTC_V2.pine parity'ye hazırlık mı, **(b)** canlı broker/webhook
  entegrasyonu mu? Architecture "no live trading in MVP" → muhtemelen (a) + dry-run adapter.
  Bu karar C2/C3/E'nin derinliğini belirler (C1 buna bağlı değil — hemen başlanabilir).

### C1 | Gate3 artifact builder (spec-türetilebilir kısımlar)
- **İş:** `build_production_readiness_artifact.py` yaz. `production_readiness_artifact_v1.schema.json`'a göre, **dürüstçe coded evidence'tan türetilebilenleri** doldur:
  - `reproducibility` /5 (param_set_saved, dataset_window_saved, cost_assumptions_saved, rerun_reproducible) → eval artifact + MEGA config'ten **OK**.
  - `signal_contract` kısmen (emits_long_short_close_flat, signal_timing_defined, entry_logical_exit_separable) → producer_spec'ten türetilebilir.
  - `monitoring` kısmen (params_loggable, carries_version) → mevcut.
  - Geri kalan (alert_adapter, state_sync, fail_safe, risk_engine_compat) → **N_A/NOT_COMPUTED** (fabricate etme — schema bunu emrediyor).
- **AI:** DeepSeek (builder) + Claude audit. **Bağımlı:** C0a (sadece policy onayı — scope beklemez). **Kabul:** schema-valid artifact'ler; score_gate3 INCOMPLETE→kısmi puan (dürüst), promotable hâlâ 0 ama Gate3 "ne eksik" net.

### C2 | MTC risk-engine compat evidence (MEV köprüsü)
- **İş:** `risk_engine_compat` /15 için → MEV-001 (mtc_engine_validate) zaten var. Bir shortlist producer'ı light-risk profille MTC engine'den geçir → works_with_mtc_default_sl_tp_trail vb. evidence üret. MEV-002 bu.
- **AI:** Claude + Barış onay. **Bağımlı:** C0, C1, B-shortlist. **Kabul:** ≥1 producer için risk_engine_compat OK evidence.

### C3 | Alert adapter + state sync + fail-safe (dry-run, architecture §12.14)
- **İş:** En ağır kısım. Architecture'ın izin verdiği sınırda (dry-run sandbox, no live webhook): TV alert JSON şeması, entry/exit/reduce-only ayrımı, duplicate guard, broker-state karşılaştırma mantığı, circuit-breaker uyumu — **kod + test, canlı emir YOK**. signal-quorum/command-dash referans.
- **AI:** Codex (adapter kod) + Claude review + Barış onay (her aşama). **Bağımlı:** C0 (b şıkkı seçilirse), C1. **Kabul:** dry-run adapter testleri; alert_adapter/state_sync/fail_safe evidence OK; **gerçek webhook yok**.

### C4 | Gate3 → scorecard → UI
- **İş:** C1-C3 evidence'ı `score_gate3` + `score_all_gates`'ten geçir → scorecard_v2 güncelle → UI Gate3 kartı dolsun.
- **AI:** Claude. **Bağımlı:** C1-C3. **Kabul:** en az shortlist adaylarında Gate3 OK/kısmi; promotable hesabı dürüst yansıyor.

---

## Workstream D — Gece-veri → UI görünürlüğü (otomasyon)

**Hedef:** Hiçbir gece çıktısı elle kopyalama gerektirmeden UI'da görünsün.

### D1 | Loop/run otomatik dashboard export
- **Problem:** backtest_reader top-level `*_results.json` glob'lar ama run'lar subdir'e yazıyor. Bu sezon elle kopyaladım.
- **İş:** Tüm run script'lerine (heavy_night, strat_extra, overnight loop'lar) gece-sonu **top-level `<run>_results.json` export** adımı ekle (runbook §6.4 step 4 zaten istiyor). Veya backtest_reader'ı recursive yap (`**/MEGA_walk_forward_results.json`).
- **AI:** Claude. **Kabul:** yeni run otomatik dashboard'da COMPLETED.

### D2 | Tüm artifact tiplerini UI'a bağla
- **İş:** CPCV/PBO/alpha/morning-report/eval-artifact'lerin her biri için UI'da bir görünüm (Backtest Lab / Optimization Lab detayında). Şu an MEGA results + scorecard görünüyor; cpcv/pbo/alpha raporları link'li değil.
- **AI:** Codex/Claude. **Bağımlı:** A3 gap matrix. **Kabul:** bir run kartından cpcv/pbo/alpha/morning-report açılabiliyor.

### D3 | Heartbeat / worker monitor canlı
- **İş:** §12.12 Worker Monitor — `overnight_runs/_heartbeat.json`'u oku, aktif/son gece run durumunu göster.
- **AI:** Codex. **Kabul:** dashboard son gece run'ının stage/status'unu gösteriyor.

### D4 | "Night Run Detail" sayfası (Codex) — gece-run başına 1 sayfa
- **İş:** Her gece run'ı için tek sayfa: özet kartları (süre, worker, pass/fail,
  candidate sayısı) · artifact linkleri (MEGA/CPCV/PBO/alpha/morning) · candidate
  tablosu · validation checklist (CPCV/PBO/Gate2/all-gate done mu) · next actions ·
  watchdog/heartbeat durumu. Codex item-4.
- **AI:** Codex/Claude. **Bağımlı:** D1/D2. **Kabul:** herhangi bir gece run'ından sonra UI rapor avlamadan run'ı gösteriyor.

---

## Workstream E — Promosyon hattı (architecture'ın izin verdiği son nokta)

**Hedef:** Gate1-3 geçen (varsa) adayı Pine Builder → parity plan → MTC entegrasyon
PLANI'na kadar taşı. **Onaysız .pine/core yazımı YOK.**

### E1 | Pine Builder akışı (§12.9)
- **İş:** Bir promoted/forward-paper adayı için standalone `*_REVIEW.pine` + PINE_COMPILE_CHECKLIST + PARITY_PLAN üret (pine-mcp referanslı). MTC_V2.pine'a dokunma. Handoff Paste Block ile compile sonucu al.
- **AI:** Claude (Pine) + Barış (compile). **Bağımlı:** B/C'den ≥1 aday. **Kabul:** standalone Pine draft + compile checklist; .pine untouched.

### E2 | Parity plan
- **İş:** Python prototip ↔ PineTS ↔ TV export parity planı (architecture §18.1). Sadece plan + ilk karşılaştırma; promote kararı Barış'ta.
- **AI:** Claude/Codex + Barış. **Kabul:** parity plan dokümanı.

---

## Workstream F — Gece çalışmaları / overnight execution

**Hedef:** A-E iş kuyruğunu otonom gece seanslarıyla ilerlet. Makine uyurken
boşa beklemesin (A19), ama determinizm tuzağına da düşmesin (tekrar = sıfır bilgi).

### F0 | Gece disiplini (her gece zorunlu — bu sezonun dersleri)
- **Determinizm farkındalığı:** `seed=md5(strat|sym|tf)` (mega:1130). Aynı sweep'i
  tekrar koşma = sıfır bilgi (A19/C4/C7). Loop-pad YASAK. Her gece **genuinely-new** iş.
- **Smoke gate (HARD):** her batch'ten önce 1-2 hücre dummy → "all jobs done" + JSON
  kanıtı olmadan tam batch başlatma (runbook §2.4).
- **Deadline cap + makineyi bırak:** batch bitince idle-keep-awake YOK (A19). Erken
  biterse bir sonraki batch'e geç veya dur.
- **PBO dikkat (A20):** derin CPCV'de PBO'yu 15-split CPCV'den besle (C(44,22) OOM).
- **Auto-export (D1):** gece-sonu top-level `<run>_results.json` + dashboard verify.
- **Kapanış zorunlu (runbook §6.4):** aggregate/alpha + morning report + dashboard
  refresh + lessons arşivi + handoff/NEXT_STEPS/SESSION_LOG. Eksikse gece tamamlanmamış.
- **Sınır:** Pine/MTC/parity/live YOK; promotion iddiası YOK; commit Barış'ta.

### F1 | Gece-batch kuyruğu (otonom-uygun, onaysız işler)
Sıralı, her batch self-contained + deadline-capped. Determinizm yüzünden hepsi
**bir kez** koşar (tekrar yok):

| Batch | İş | WS | Süre tahmini | Yeni-bilgi mi? |
|---|---|---|---|---|
| **N1** | spec→metadata extractor + registry regen (DeepSeek dispatch + audit) | A1 | ~1-2h | ✅ UI içeriği |
| **N2** | Kodlanabilir engine-dışı stratejileri ekle + sweep + CPCV/PBO/Gate2 (STG057/054/047, threshold-free kısımlar) | B2 | her biri ~30-60dk | ✅ yeni hücreler |
| **N3** | Gate3 artifact builder + TÜM mevcut run'lara uygula (spec-derivable evidence) | C1 | ~1-2h | ✅ Gate3 kısmi puan |
| **N4** | Auto-export + tüm tarihsel run'ları dashboard'a relink (cpcv/pbo/alpha/morning) | D1/D2 | ~1h | ✅ UI görünürlük |
| **N5** | Pipeline-state envanteri + GAP_MATRIX (read-only audit) | B1/A3 | ~30dk | ✅ yol haritası |
| **N6** | Heavy-validation tier (yeni stratejiler dahil) — derin CPCV + alpha, dürüst rapor | B/F | wall-clock'a göre | ✅ daha sıkı OOS |

**Bir gecede:** N5 (envanter) → N1 (içerik) → N3 (Gate3 builder) → N4 (görünürlük)
mantıklı tek-gece zinciri (hepsi onaysız, düşük risk). N2/N6 ayrı gece (kodlama + ağır compute).

### F2 | Gece-batch ON İZNİ gereken işler (Barış pre-register etmeden gece koşma)
- **B3 confirmation grid** — hipotez/grid önceden kaydedilmeli (cherry-pick = DSR geçersiz).
- **C3 alert/state/fail-safe adapter** — entegrasyon kodu, her aşama onay.
- **E1/E2 Pine/parity** — standalone bile olsa Barış compile/karar.
Bunlar gece **otonom başlatılmaz**; Barış input verince gece koşulabilir.

### F3 | Gece orchestration altyapısı (tekrar kullanılabilir)
- Bu sezon üretilen `heavy_night_*.sh` + `heavy_night_report.py` + `strat_extra_runner.py`
  pattern'i şablon. Her gece için: batch script (deadline + heartbeat + auto-export +
  kapanış) + background waiter (harness completion notify) + ScheduleWakeup fallback.
- **Tek seferlik iyileştirme:** generic `night_runner.sh <batch-list>` — batch kuyruğunu
  sırayla koşar, her birinin smoke-gate'ini geçer, biterse makineyi bırakır.
- **AI:** Claude. **Kabul:** bir komutla N-batch zinciri koşar, sabah tam closure hazır.

---

## Kritik yol & sıralama

```
C0 (Barış kararı: production tanımı)  ──┐
A3 (gap matrix) ─┐                      │
B1 (pipeline state) ─┐                  │
A1 (spec→metadata) ──┴─→ A2/A4 (UI dolum)│
D1 (auto-export) ─────→ D2/D3 (UI bağlama)
                                         ├─→ C1 (Gate3 builder, spec-derivable)
                                         ├─→ C2 (MEV risk-compat)
                                         └─→ C3 (alert/state/fail-safe dry-run) ─→ C4 ─→ E1/E2
B2/B3/B4 (strateji ilerletme) — A1/B1 sonrası, Barış pre-registration ile
```

**Hızlı kazanımlar (bu hafta, düşük risk, onaysız):** A1, A3, B1, D1, D2, C1.
**Karar bekleyen (Barış):** C0 (production tanımı), B3 (confirmation grid hipotezi),
C2/C3/E (entegrasyon onayları).

---

## Delegation matrix (Codex split)

| Aktör | Sahiplenir |
|---|---|
| **DeepSeek** (mekanik, dispatch) | artifact envanter taramaları · JSON/schema validation · missing-field audit · rapor extraction · tek-dosya helper script · UI veri-şekli audit · candidate tablo completeness · spec→metadata extractor (A1) · Gate3 builder iskeleti (C1) |
| **Claude** (orkestratör/yargı) | mimari karar · Gate3 evidence policy uygula · faithful strateji kodlama (B2) · gerçek-veri audit (DeepSeek çıktısına asla güvenme) · gece orchestration · kapanış/handoff |
| **Codex** | dashboard UI komponentleri (A5-A7, D4) · production-readiness adapter kodu (C3) · controlled write/commit · architecture audit |
| **Barış** | C0a/C0b kararları · B3 pre-registration · C2/C3 entegrasyon onayı · promosyon eşiği · final approve |

## Final deliverable — Command Center Readiness Report (Codex)

Tüm workstream'ler sonrası tek **MCC_READINESS_REPORT.md**: her strateji pipeline
state'i · gate dağılımı · promotable sayısı + her birinin blocker'ı · gece-ops
durumu · UI coverage (15 modül) · kalan iş. **Kapanış acceptance'ı.**

---

## Barış kararları

**KAPANANLAR (2026-06-06):**
1. ✅ **C0a — GATE3 EVIDENCE CONTRACT ONAYLANDI:** Gate3 yalnız gerçek
   signal/alert/state/risk/fail-safe evidence'tan OK; backtest'ten asla türetilmez;
   evidence yoksa INCOMPLETE. → C1 builder AÇIK.
2. ✅ **C0b — "Production" kapsamı: ÖNCE (a) Pine-parity hazırlığı + dry-run, SONRA (b)
   canlı broker** (ayrı onaylı ileri faz). C2/C3 dry-run olarak modellenir, gerçek webhook yok.
3. ✅ **Promosyon eşiği: FORWARD_PAPER.** DSR<0.50 ama CPCV-robust + alpha-pozitif adaylar
   `PROMOTE_TO_FORWARD_PAPER_TRADE` olarak işaretlenir (live-bar OOS gözlem; Pine/MTC/live yok).

**AÇIK (inventory/shortlist sonrası Barış'a gelecek):**
4. **B3 — Confirmation grid:** hangi hücreler + dar grid hipotezi (pre-register şart). N5/B1 shortlist'i sonrası.
5. **C2/C3 — Entegrasyon onayı:** MEV producer seçimi + dry-run alert adapter'a yeşil ışık. C1 sonrası.

---

## Dürüst beklenti (yanıltma yok)

- Çoğu strateji **promote edilemeyecek** — DSR duvarı gerçek. "İlerlet" = her birini
  dürüst en-ileri gate'ine taşımak (çoğu SALVAGE/FORWARD_PAPER'da duracak). Bu başarısızlık değil, disiplin.
- Gate3 tam yeşil = sadece gerçek entegrasyon evidence'ı ile. Spec'ten türetilebilen
  kısımlar (C1) doldurulur; alert/state/fail-safe (C3) emek ister ve **canlı trade yok**.
- UI "tamamlanması" = boş-durumların dürüst + mevcut tüm verinin görünür olması;
  olmayan veriyi uydurmak değil.

_Bağlı dosyalar: [[NEXT_STEPS]], `MTC Command Center ARCHITECTURE.md` §12/§6.x,
`03_QUANTLENS/_user_guide/12_STRATEGY_EVALUATION_RUBRIC.md`,
`11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md`._
```
