# MTC V2 Architecture Deep Audit Prompt — Round 3 / Web-No-Code-Access

> Bu prompt, web ortamında çalışan ve repo içindeki V1 kodunu, eski audit raporlarını veya README dosyalarını doğrudan göremeyen modeller içindir.
>
> Bu promptun sonuna kullanıcı ayrıca `MTC_V2_ARCHITECTURE.md` içeriğini ekleyecek.

## Talimatlar

1. Raporun başına kullandığın model numarasını yaz:
   - Örnek: `**Model:** o3`
2. Raporun sonuna `--- RAPOR BİTTİ ---` yaz.
3. Bu bir **read-only audit** çalışmasıdır.
4. Eğer bulunduğun ortam dosya yazmayı desteklemiyorsa raporu doğrudan markdown olarak üret.
5. Eğer dosya yazabiliyorsan ve kullanıcı açıkça isterse:
   - `C:\LAB\tradingview-lab\00_MASTER_TEMPLATE\MTC_V2\AUDIT_6\`
   - üzerine yazmadan, yeni dosya oluşturarak kaydet.

---

## Görev

Bir trading framework mimarisini audit edeceksin.

Audit hedefin yalnız hata bulmak değil. Şunları birlikte değerlendireceksin:

- parity'yi kolaylaştırma
- modülerliği sertleştirme
- optimize ve sürdürülebilir kod üretimi
- base-scope ile advanced-scope ayrımını netleştirme
- önceki auditlerden uygulanmayan önerilerin neden uygulanmadığını açıklama

Bu mimari Pine Script (TradingView) ve Python backtester için parity-first geliştiriliyor.

---

## Elindeki Bağlam Özeti

Sen repo içindeki tüm dosyaları göremiyorsun. Bu nedenle aşağıdaki özet bağlamı input gerçeği olarak kullan.

### V1 hakkında bilinenler

- V1 Pine ana dosyası yaklaşık 5616 satırlık büyük bir monolitti.
- V1’de sinyal, filtre, confirmation, guard recovery, execution, visualization ve HTF logic aynı ekosistemde büyüdü.
- V1 parity süreci 439 test case ile yürütüldü.
- V1’de doğrulanmış bug sınıfları:
  - TIME_STOP sonrası hatalı same-bar entry
  - trailing exit path reset eksikliği
  - hardcoded string/order id riski
  - trailing stop güncellenince TP bacaklarının stale kalması
  - raw signal marker ile gerçek entry marker karışması

### Parity sürecinden bilinen ana dersler

- HTF alignment en kritik alanlardan biri
- history window sensitivity ciddi risk
- warmup / indicator seeding farkları gerçek parity kırıcı
- broker reporting satır asimetrisi normalizasyon gerektiriyor
- same-bar flip ve partial/full close kümeleri özel dikkat istiyor
- float precision ve rounding toleransları formalize edilmeli

### Güncel mimarinin bilinen yönleri

Aşağıdaki kararların önemli kısmı güncel mimaride var veya kısmen var:

- exit-first runner
- `block_new_entries_this_bar` / `closed_this_bar_reason`
- protective stop owner modeli (`INITIAL_SL`, `BE`, `TRAIL`)
- monotonic pyramid stop merge
- `working_exits` kavramı
- raw pulse tabanlı producer yaklaşımı
- `pending_side`
- `decision.side`
- `same_bar_reentry_allowed`
- `PriceExitEngine` benzeri birleşik price-exit owner yaklaşımı
- `working_exit_reference_qty`
- `completed_exit_ids`
- session-aware HTF carry
- warmup sırasında read-only pipeline seeding

### Önceki auditlerden uygulanmış görünen kararlar

- V1 A-1 sınıfı için exit-first order
- V1 B-1 için tek `state.close_position(...)` mutasyon kapısı
- V1 D-1 için enum/constant yaklaşımı
- V1 E-1 için working-exit stop sync
- V1 C-1 için marker taxonomy
- HTF `shift(1)` no-repaint semantiğinin açık yazılması
- session/DST kontratının güçlendirilmesi

### Önceki auditlerden uygulanmamış veya bilerek dışarıda bırakılmış olabilecek konular

Bunları raporunda ayrıca değerlendir ve “neden uygulanmadı?” diye yorumla:

1. V1 advanced confirmation seçeneklerinin tümü geri getirilmedi
   - muhtemel neden: base scope'u sade tutmak, parity maliyetini azaltmak
2. V1 MACD advanced modlarının tamamı taşınmadı
   - muhtemel neden: PPO/diagnostic çeşitliliğinin base scope'u gereksiz karmaşıklaştırması
3. V1 range master family aynen taşınmadı
   - muhtemel neden: producer ve gate rollerini ayırmak
4. Virtual trade guard recovery geri getirilmedi
   - muhtemel neden: büyük parity ve state maliyeti
5. Python HTF akışından `shift(1)` kaldırılmadı
   - muhtemel neden: Pine `request.security(close[1])` semantiğini koruma ihtiyacı
6. Flat config tamamen nested manifest'e çevrilmedi
   - muhtemel neden: Pine/Python parametre parity yüzeyi
7. Ayrı `time_stop_cooldown_bars` zorunlu base feature olmadı
   - muhtemel neden: pulse signal contract ile loop riskinin azaltıldığı varsayımı
8. Bazı agresif default değişiklikleri yapılmadı
   - muhtemel neden: bunların mimari değil strateji policy kararı sayılması

Senin görevin bunların doğru gerekçe olup olmadığını değerlendirmek.

---

## Audit Odağı

Raporu özellikle şu üç eksen etrafında kur:

### 1. Parity kolaylığı

- parity için gereksiz karmaşıklıklar neler?
- hangi kontratlar parity'yi ucuz ve deterministik hale getiriyor?
- hangi alanlarda hâlâ gizli drift riski var?

### 2. Modülerlik

- hangi interface'ler güçlü?
- hangi interface'ler ileride hidden coupling yaratır?
- bu mimari V1 gibi yeniden şişer mi?

### 3. Optimize kod üretimi

- Pine tarafında resource / file bloat / complexity riski
- Python tarafında object churn / loop maliyeti / cache ownership riski
- codegen, schema, manifest, snapshot, test harness açısından hangi iyileştirmeler gerekir?

---

## Zorunlu Rapor Yapısı

### 1. Genel Hüküm
- mimarinin olgunluk skoru
- parity readiness
- modularity robustness
- implementation readiness

### 2. En Kritik 10 Bulgu
Her bulgu için:
- önem seviyesi (`P0`, `P1`, `P2`)
- kısa başlık
- net açıklama

### 3. Prior Recommendation Tracking
Tablo:
| Öneri / Konu | Muhtemel Kaynak | Uygulanmış mı? | Uygulanmadıysa Muhtemel Neden | Hüküm |

### 4. V1 Bug Re-check
- önceki V1 bug sınıfları bu mimaride gerçekten kapanmış mı?
- yeniden açılma riski var mı?

### 5. Parity Deep Dive
Zorunlu alt başlıklar:
- HTF alignment
- warmup/seeding
- broker normalization
- session/DST
- history window sensitivity
- float/rounding
- same-bar partial/full lifecycle

### 6. Modularity Deep Dive
- interface ownership
- state ownership
- hidden coupling
- scope boundary
- file growth risk

### 7. Performance / Optimization Deep Dive
- Pine compile/runtime/resource pressure
- Python runtime / allocation / lookup cost
- per-bar snapshot cost
- working-exit rebuild cost
- config/schema overhead

### 8. Interface Audit
İncele:
- `SignalProducer`
- `SignalTransform`
- `Gate`
- `ExitRule`
- `ProtectiveOrderManager`
- `PositionManager`
- `PositionSizer`
- `Bar`
- `Position`
- `PortfolioState`
- `WorkingExit`

### 9. Applied vs Not Applied Judgment
İki tablo:

Tablo A:
| Karar | Neden uygulanmış olabilir | Doğru mu? | Not |

Tablo B:
| Karar | Neden uygulanmamış olabilir | Doğru mu? | Eğer yanlışsa ne yapılmalı? |

### 10. Silent Scope Cuts
- base scope dışında bırakılmış ama yanlış anlaşılmaya açık alanlar

### 11. Önceliklendirilmiş İyileştirme Planı
Tablo:
| Öneri | Gerekçe | Parity Etkisi | Modülerlik Etkisi | Performans Etkisi | Öncelik |

### 12. Kod Üretim Rehberi
Bu mimariden koda geçerken uyulması gereken en kritik 15 kuralı yaz.

### 13. Nihai Hüküm
- doğrudan implementasyona hazır mı?
- önce hangi 5 boşluk kapanmalı?
- parity-first hedefi gerçekçi mi?

---

## Özel Sorular

Mutlaka cevapla:

- `PriceExitEngine` benzeri birleşik owner, same-bar composite exit sorununu gerçekten çözer mi?
- `working_exit_reference_qty` + `completed_exit_ids` yeterli mi?
- pulse-based signal contract tüm producer tipleri için savunulabilir mi?
- flat config uzun vadede sürdürülebilir mi?
- hangi kararlar modülerliği korumak için bilinçli scope cut, hangileri eksik bırakılmış tasarım borcu?
- parity'yi kolaylaştırmak için mimarinin hangi 5 noktasını daha da sertleştirmek gerekir?

---

## Disiplin

- Yüzeysel konuşma istemiyorum.
- Somut risk, somut örnek, somut öneri ver.
- “Uygulanmamış ama doğru karar” diyorsan nedenini savun.
- “Eksik” diyorsan parity / modülerlik / performans etkisini ayrı ayrı anlat.

---

## Son Not

Bu promptun sonuna kullanıcı güncel `MTC_V2_ARCHITECTURE.md` içeriğini ekleyecek.
Audit'ini yalnız bu prompt + eklenen mimari üzerinden yap.

