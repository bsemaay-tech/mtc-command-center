# MTC V2 Architecture Deep Audit Prompt — Round 3 / Local-Code Access

> Bu prompt, VS Code / Codex / local workspace erişimi olan; V1 kodunu, README'leri, eski audit raporlarını ve güncel mimariyi okuyabilen modeller içindir.

## Talimatlar

1. Raporun başına kullandığın model numarasını yaz:
   - Örnek: `**Model:** gpt-5-codex`
2. Raporun sonuna `--- RAPOR BİTTİ ---` yaz.
3. Bu çalışma **READ-ONLY audit + report** çalışmasıdır.
   - Kaynak kodu, README'leri, mimariyi, eski raporları değiştirme.
   - Sadece audit raporunu oluştur.
4. Raporunu şu klasöre kaydet:
   - `C:\LAB\tradingview-lab\00_MASTER_TEMPLATE\MTC_V2\AUDIT_6\`
5. Dosya adı yalnızca model adı / model numarası olsun:
   - Örnek: `gpt-5-codex.md`
6. **Mevcut dosyaların üzerine kesinlikle yazma.**
   - Aynı isim varsa `_2`, `_3`, `_4` ekleyerek yeni dosya oluştur.
7. Rapor markdown formatında olsun.
8. Audit son derece derin, savunulabilir ve satır-satır olmalı. Yüzeysel özet istemiyorum.

---

## Görev

`C:\LAB\tradingview-lab\00_MASTER_TEMPLATE\MTC_V2_ARCHITECTURE.md` dosyasının **güncel halini** audit et.

Audit yalnız mimari “doğru mu?” kontrolü olmasın. Şunları birlikte değerlendir:

- parity'yi en kolay, en ucuz ve en deterministik şekilde nasıl kurarız?
- modülerlik gerçekten sürdürülebilir mi, yoksa ileride tekrar V1 benzeri mega-dosya / state-dağınıklığı üretir mi?
- optimize kod üretimi için hangi kontratlar eksik?
- Pine + Python iki platformda da uygulanabilirlik ne kadar güçlü?
- mevcut mimari “base scope” ile “silent scope cut” alanlarını yeterince ayırıyor mu?
- önceki raporlarda önerilmiş ama hâlâ uygulanmamış veya kısmen uygulanmış maddeler doğru sebeple mi uygulanmadı?

---

## Okunacak Kaynaklar

Mutlaka oku:

1. `C:\LAB\tradingview-lab\00_MASTER_TEMPLATE\MTC_V2_ARCHITECTURE.md`
2. `C:\LAB\tradingview-lab\00_MASTER_TEMPLATE\MTC_V2\` klasörü ve tüm alt klasörleri
3. Özellikle:
   - `AUDIT_2\`
   - `AUDIT_3\`
   - `AUDIT_4\`
   - `AUDIT_5\`
   - `ARŞİV\`
   - konsolide audit dosyaları
   - önceki deep audit prompt dosyaları
4. Workspace içindeki V1 Pine kaynakları, README'ler, parity notları ve V1 analiz / bug referansları
5. V1 ana Pine dosyası ve onunla ilişkili açıklayıcı belgeler

Sıfır bayt placeholder dosyaları raporunda not düşebilirsin ama içerik kaynağı kabul etme.

---

## Bu Turun Özel Odağı

Audit'i özellikle şu üç eksen etrafında derinleştir:

### A. Parity kolaylığı

- parity'yi kurmak için minimum gerekli kontratlar neler?
- bar snapshot, HTF alignment, warmup, price-exit ambiguity, broker normalization, rounding, session/DST, history-window sensitivity alanlarında hâlâ açık risk var mı?
- parity harness daha az özel-case ile çalışacak hale nasıl gelir?
- test katman sırası doğru mu?
- “base parity profile” ile “advanced execution profiles” yeterince ayrılmış mı?

### B. Modülerlik dayanıklılığı

- mimari gerçekten modüler mi, yoksa kâğıt üstünde modüler görünüp runner / state / config tarafında tekrar merkezileşiyor mu?
- hangi modüller gelecekte şişmeye en açık?
- hangi interface'ler zamanla hidden coupling üretir?
- hangi state alanları ownership belirsizliği yaratıyor?
- hangi dosyalar gelecekte V1’deki gibi bloat / spaghetti riski taşır?

### C. Optimize kod üretilebilirliği

- bu mimariye göre üretilecek Pine ve Python kodu performanslı olur mu?
- per-bar object churn, state mutation, snapshot üretimi, HTF lookup, repeated indicator access, config validation, working-exit rebuild, partial exit lifecycle açısından darboğazlar var mı?
- hangi yerlerde codegen / manifest / schema-first yaklaşım gerekli?
- hangi kontratlar implementasyon sırasında gereksiz branching'i veya duplicate code'u önler?

---

## Önceki Raporlardan Özellikle Takip Edilecek Konular

Aşağıdaki alanlar daha önce raporlarda defalarca gündeme geldi. Her birini kontrol et ve son durumda:
- `uygulandı`
- `kısmen uygulandı`
- `uygulanmadı ama doğru sebeple`
- `uygulanmadı ve hâlâ açık risk`
olarak sınıflandır.

### Büyük ölçüde uygulanmış görünen ama regresyon riski taşıyanlar

- V1 A-1: TIME_STOP sonrası same-bar entry
- V1 B-1: trailing exit reset eksikliği
- V1 D-1: hardcoded string / id drift
- V1 E-1: trailing stop güncellenirken TP bacaklarının stale kalması
- V1 C-1: raw signal marker vs real entry marker
- monotonic pyramid SL merge
- raw OPP_SIGNAL same-bar flip akışı

### Kısmen uygulanmış veya yeniden audit edilmesi gerekenler

- warmup sırasında pipeline'ın gerçekten seed edilmesi
- same-bar `TP1 + TP2`, `TP1 + TIME_STOP`, `TP1 + OPP_SIGNAL`, `partial + full close` lifecycle'ı
- `working_exit_reference_qty` / rebased multi-TP semantics
- `completed_exit_ids` ile pyramid rebuild davranışı
- `decision.side`, `same_bar_reentry_allowed`, `pending_side` alanlarının gerçekten otorite olup olmadığı
- `FILTER_BLOCK` ile `category="filter"` ilişkisinin yeterliliği
- `exit_on_filter_block` master toggle tasarımı
- session-aware HTF carry
- `initial_risk_per_unit` freeze semantiği

### Bilinçli olarak uygulanmamış olabilecek öneriler

Bunları “neden uygulanmadı?” diye özellikle yorumla. Kör şekilde “eksik” deme; gerekçeyi analiz et.

1. V1 advanced confirmation opsiyonlarının tamamının geri getirilmesi
   - Muhtemel neden: base scope'u sade tutup parity ve modülerliği korumak
2. V1 MACD advanced modlarının tamamının geri getirilmesi
   - Muhtemel neden: PPO / diagnostic trigger / advanced hist modları base scope dışı bırakıldı
3. Range master gate ailesinin aynen taşınması
   - Muhtemel neden: producer ve independent gate rolleri ayrıldı
4. Virtual trade guard recovery'nin geri getirilmesi
   - Muhtemel neden: parity ve state explosion maliyeti
5. Python HTF akışında `shift(1)`'in kaldırılması
   - Muhtemel neden: Pine `request.security(close[1])` semantiği ile çelişmesi
6. Ayrı `time_stop_cooldown_bars` alanının base scope'a zorunlu eklenmesi
   - Muhtemel neden: pulse-based signal contract ile riskin azaltıldığı varsayımı
7. Flat dict config'in tamamen nested config / manifest yapısına çevrilmesi
   - Muhtemel neden: Pine ile parametre parity'si ve input yüzeyi uyumu
8. Agresif default değişiklikleri (`fallback_size_pct`, `cooldown_bars`, vb.)
   - Muhtemel neden: bunların mimari değil strateji-policy kararı olması

Bu maddelerde mimarinin kararı doğru mu, yanlış mı, yoksa yarım mı kaldı açıkça yaz.

---

## Zorunlu Çıktı Formatı

Raporunu aşağıdaki bölümlerle hazırla.

### 1. Genel Hüküm
- mimarinin mevcut olgunluk skoru (1-10)
- parity readiness skoru
- modularity robustness skoru
- implementation readiness skoru

### 2. Executive Findings
- yalnız en kritik 10 bulgu
- her bulgu için: önem seviyesi (`P0`, `P1`, `P2`), kısa başlık, tek paragraf açıklama

### 3. Önceki Rapor Ledger'ı
Tablo:
| Konu | İlk Kaynak/Rapor | Mevcut Durum | Neden Uygulanmadı / Nasıl Uygulandı | Hüküm |

Burada özellikle uygulanmayan veya kısmen uygulanan öneriler için “neden uygulanmadı” kısmı güçlü olmalı.

### 4. V1 Bug Re-check
Her doğrulanmış V1 bug için:
- V2'de gerçekten kapanmış mı?
- mimari sözleşme yeterli mi?
- implementasyonda yeniden açılma riski var mı?

### 5. Parity Deep Dive
Zorunlu alt başlıklar:
- HTF alignment
- warmup/seeding
- broker normalization
- session/DST
- history window sensitivity
- float/rounding
- same-bar composite exits
- execution profile drift riski

### 6. Modularity Deep Dive
Zorunlu alt başlıklar:
- interface ownership
- hidden coupling
- state ownership
- config surface explosion
- Pine file growth risk
- Python engine complexity risk

### 7. Performance / Optimization Audit
Zorunlu alt başlıklar:
- per-bar allocation ve object churn
- indicator registry / caching
- HTF snapshot cost
- exit engine complexity
- partial exit / rebuild maliyeti
- Pine compile/runtime/resource pressure
- Python vectorization vs stateful loop dengesi

### 8. Interface Contract Audit
Her interface için ayrı ayrı:
- yeterli mi?
- fazla mı zayıf?
- fazla mı geniş?
- test edilebilir mi?
- parity dostu mu?

İncelenecekler:
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

### 9. Config Contract Audit
Zorunlu alt başlıklar:
- naming consistency
- radio validation
- dependency validation
- scale/percent consistency
- Pine/Python parity friendliness
- flat dict risk vs manifest/codegen ihtiyacı

### 10. Development Order Audit
- mevcut L0-L25 sırası doğru mu?
- eksik katman var mı?
- parity maliyetini düşürmek için sıra değişmeli mi?

### 11. Silent Scope Cuts
- V1'de olan ama V2 base scope dışında bırakılan özellikler
- bunların bilinçli mi, tehlikeli mi, yoksa yanlış anlaşılmaya açık mı olduğu

### 12. Applied-vs-Not-Applied Judgment
Bu bölüm zorunlu.

İki tablo hazırla:

Tablo A:
| Öneri | Neden Uygulanmış | Doğru Karar mı? | Not |

Tablo B:
| Öneri | Neden Uygulanmamış | Doğru Karar mı? | Eğer yanlışsa ne yapılmalı? |

### 13. Önceliklendirilmiş İyileştirme Planı
Tablo:
| Öneri | Neden | Etki | Uygulama Zorluğu | Öncelik |

### 14. Kod Üretim Rehberi
Mimariden koda geçerken LLM / insan geliştirici için en kritik 15 uygulama kuralını yaz.
Özellikle:
- parity bozmayan kurallar
- modülerliği bozmayan kurallar
- optimize kod üreten kurallar

### 15. Nihai Hüküm
- “Bu mimari doğrudan implementasyona hazır mı?”
- “Önce hangi 5 boşluk kapanmalı?”
- “Parity-first hedefi şu haliyle gerçekçi mi?”

---

## Özel İnceleme Zorunluluğu

Şu soruları mutlaka cevapla:

- `PriceExitEngine + ExitResult` mevcut hali yeterli mi, yoksa tam bir event-plan modeline mi ihtiyaç var?
- `shift(1)` + session-aware carry şu haliyle Pine semantiğini gerçekten karşılıyor mu?
- pulse-based producer kontratı tüm producer tipleri için savunulabilir mi?
- `completed_exit_ids` ve `working_exit_reference_qty` parity'yi gerçekten kapatıyor mu?
- flat config uzun vadede sürdürülebilir mi?
- `AUDIT_2`–`AUDIT_5` raporlarından hâlâ haklı olup dokümana girmemiş hangi öneriler kaldı?
- V1 kod tecrübesine göre hangi bölüm tekrar şişmeye en aday?
- aynı mimariyle Pine ve Python’da bağımsız geliştiriciler çalışsa hangi sözleşmeler yüzünden drift olur?

---

## Disiplin

- Bulgularını dosya/satır referansı ile yaz.
- “Eksik” dediğin her konuda ya somut risk ya somut implementasyon problemi belirt.
- “Bu öneri uygulanmamış ama doğru” diyorsan nedenini savun.
- “Bu öneri uygulanmalı” diyorsan parity, modülerlik ve performans etkisini ayrı ayrı değerlendir.
- Genel laflardan kaçın.
- Rapor derin olsun; tekrar eden cümleler olmasın.

