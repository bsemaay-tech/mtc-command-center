Model Numarası: Gemini-3.1-Pro-High
RAPOR BAŞLADI

## 1. Executive Verdict
Bu Pine Script kodu (MTC_V2 Parity), execution determinizmi ve Python ile eşleşme (parity) konusunda ekstrem düzeyde dikkatle tasarlanmış çok sofistike bir state machine mimarisine sahiptir. Kodun "close_only" (bar kapanışı kararları) ve OHLC pesimistik modellemeleri parity_safe bir temel oluşturmada çok başarılıdır. Ancak, son uygulanan patch'ler sonrasında kodun mevcut durumu yeniden analiz edildiğinde; **Deferred Flip** ve **Guard Recovery (Signals Mode)** sorunlarının başarılı bir şekilde düzeltildiği görülmüştür. Ne yazık ki, **Regime Lock** hatası (kalıcı deadlock) ve **Confirm Transform (Refresh on New Raw)** semantik uyuşmazlığı varlığını korumaktadır. Deployment için hala "Strict Bug-Fix" gerektirmektedir.

## 2. Audit Coverage Statement
- Kodu uygulanan son patch sonrasında section-by-section line numaralarına bakarak yeniden inceledim.
- Deferred Flip replay mekanizmasının `_rep_ok` değişkeni ile baştan filtrelere (L12) tabi tutulduğu ve regate edildiği doğrulandı.
- Guard Recovery "Signals" modunda `l16_signal_passed` yerine `l21_final_candidate != 0` pulse yapısının kullanılarak hatanın çözüldüğü kanıtlandı.
- Regime lock mekanizmansının hala çıkışlarda (`:= 0`) sıfırlanmadığı kesin olarak (static analiz ile) doğrulandı.

## 3. Feature Coverage Matrix
| ID | Feature | Section / Owner | Inputs / States Read | States Written | Verdict | Severity | Evidence | Parity Risk | Notes |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 01 | Strategy header/config | Sec 1 | UI Config | internal constants | WORKS_AS_INTENDED | LOW | Line 7 | LOW | process_orders_on_close=true parity için kritik |
| 02 | Supertrend producer | Sec 5 | st_atr, prev states, close | st_dir, st_line, raw_reason | WORKS_AS_INTENDED | LOW | Line 531-611 | LOW | Yalnızca flip barlarında raw_long/short pulse üretiyor! |
| 03 | ATR warmup | Sec 5 | st_tr_sum, count, prev | st_atr | WORKS_AS_INTENDED | LOW | Line 547-564 | LOW | SMA-to-RMA warmup math doğru |
| 04 | HTF indicators | Sec 5 -> Sec 7 | st_atr, adx_htf vb. | state vars | WORKS_AS_INTENDED | LOW | Line 745+ | MED | Python ile Pine arasında "her LTF barında recalculate" uyumlu |
| 05 | Regime lock | Sec 7 | l4_pos, candidate | l4_regime_lock_side | BUG | CRITICAL | Line 1743, 1809 | HIGH | İlk işlemden sonra yönü sonsuza kadar kilitliyor, asla sıfırlanmıyor |
| 06 | allow_flip | Sec 7 | l4_opp_exit, allow_flip | deferred_flip_side | WORKS_AS_INTENDED | LOW | Line 1698-1707 | LOW | [PATCHED] Artık replay barında gate'ler `_rep_ok` üzerinden doğrulandıktan sonra aday işleniyor. |
| 07 | deferred flip | Sec 7 | deferred state, flat | l21_raw_long/short | WORKS_AS_INTENDED | LOW | Line 1698 | LOW | Bypasses bug'ı düzeltildi, gate check eklendi. |
| 08 | Guard recovery | Sec 7 | breach_status, mode | active, count | WORKS_AS_INTENDED | LOW | Line 1754-1758 | LOW | [PATCHED] Artık sürekli level yerine `l21_final_candidate != 0` ile spesifik pulse bazlı sayım yapıyor. |
| 09 | Multi-TP | Sec 7 | active TP1/2 prices | tp states | WORKS_AS_INTENDED | LOW | Line 1267-1294 | LOW | Handles partial qty scale-out and updates states |
| 10 | BE & Trailing | Sec 7 | mark_basis, r_multiple| active_stop_price | WORKS_AS_INTENDED | LOW | Line 1094-1118 | LOW | Stop update logic correctly promotes owners |
| 11 | Opposite signal exit | Sec 7 | candidate, pos_side | pos=0, states clear | WORKS_AS_INTENDED | LOW | Line 1414-1445 | LOW | |
| 12 | Guard States | Sec 7 | equity/mae inputs | guard limits | WORKS_AS_INTENDED | LOW | Line 1599-1605 | LOW | MAE/Consecutive loss solid |
| 13 | Confirmation transform | Sec 7 | raw_signal, history | armed states | BUG | HIGH | Line 1656-1661 | HIGH | Pulse producer nedeniyle `refresh_on_new_raw` trade'lerin açılmasını imkansız kılıyor (0 bars error). |

## 4. Critical Findings

### [CRITICAL] Regime Lock Permanently Blocks Reversal Trading (DEVAM EDİYOR)

**Alan:**  
Execution (Section 7) - Entry Decision

**Verdict:**  
BUG

**Why it matters:**  
`regime_lock` (Line 18) claims to "keep trading on current regime side until reset". Yeni patch'te `allow_flip` ve `guard recovery` düzeltilmesine rağmen, `l4_regime_lock_side_state` değişkeni pozisyon açılışlarında (`:= 1` veya `:= -1`) set edildikten SONRA herhangi bir trade kapanışında (Stop, TP, Reverse) `:= 0` olarak ASLA sıfırlanmıyor. Kodun statik yapısında L922'deki tanım haricinde sıfırlandığı yer bulunmuyor. Strateji trend dönse dahi sonsuza kadar ilk girdiği yönde kilitli kalıyor.

**Evidence:**  
Line 1743: `bool l4_regime_lock_blocks_entry = regime_lock and l21_final_candidate != 0 and l4_regime_lock_side_state != 0 and l4_regime_lock_side_state != l21_final_candidate`  
Line 1809: `l4_regime_lock_side_state := 1`
Line 1860: `l4_regime_lock_side_state := -1`

**Minimal fix direction:**  
Çıkışlarda (Line 1346-1377 Exit Blocks ve Line 1463-1488) ve pozisyon sıfıra döndüğünde `l4_regime_lock_side_state := 0` sıfırlama işlemi yapılmalı veya SuperTrend yön (`st_direction`) değiştirdiğinde sıfırlanmalı.

### [HIGH] Confirmation Transform 'Refresh On New Raw' Blokajı (DEVAM EDİYOR)

**Alan:**  
Confirmation Transform (Sec 7 / L18)

**Verdict:**  
BUG

**Why it matters:**  
Pine içerisindeki SuperTrend `long_raw` değişkenini yalnızca flip bar'ında "TRUE" (yani pulse) yapmaktadır. `refresh_on_new_raw` algoritmasının içinde:
`bool l18b_new_long_raw = long_raw and not l18b_prev_raw_long` (Line 1658) şartı bulunur. SuperTrend zaten bir pulse olduğu için, `long_raw`'un TRUE olduğu bar (`new_long_raw`) her zaman TRUE olur. Bu şart, tam da Confirm sayacının yukarı saymaya başlaması gereken barda sayacı 0'lar (`l18_confirm_bars_count_state := 0`). Pulse barı bir sonraki barda `false` olacağı için de sayaç hiçbir zaman `confirm_bars` eşiğine ulaşamaz ve strateji 0 trade üretir. Python parite testlerinde de " Pine causes 0 trades" olarak dokümante edilmiştir.

## 5. Patched Features: Works As Intended

### [PATCHED] Deferred Flip Replays Stale Candidate Without Re-gating
- **Eski Durum:** İleri atılan (deferred) `allow_flip=false` trade'i bir sonraki barda güncel filtrelere bakmadan direkt açılıyordu.
- **Yeni Durum:** Line 1700-1704 arasına muazzam ve mükemmel çalışan bir `bool _rep_ok` lojiği eklendi. Tüm `l12_` filtreleri replay barında tekrar üzerinden geçiriliyor. Stale Filter (çürümüş filtre) bypass'ı engellendi.

### [PATCHED] Guard Recovery 'Signals Mode' is instantly depleted
- **Eski Durum:** Supertrend bar süresince `long_gated` üretirse Guard Recovery Timer bir trend dalgasında anında 0'a düşüyordu.
- **Yeni Durum:** Line 1754'te sayaç `if l21_final_candidate != 0` şartına bağlandı. Pine script içinde SuperTrend "pulse" olarak çalıştığı için, sadece flip yaşandığında 1 adet eksiltme yapıyor. Stratejiyi doğru şekilde regüle ederek backtest sahtekarlığını önledi.

## 6. Must-Test Scenarios

### Test 1 — Regime Lock Absolute Deadlock (Hala Patlak)
- **Setup**: `regime_lock=true`, `enable_long=true`, `enable_short=true`. Market goes up, hits SL, market goes down.
- **Trigger**: Next short pulse.
- **Expected Behavior**: Entry short.
- **What may fail**: Completely blocks short due to `l4_regime_lock_side_state` staying stuck at `1`.

### Test 2 — Refresh On New Raw Mute (Hala Patlak)
- **Setup**: `use_confirm_transform=true`, `refresh_on_new_raw=true`, `confirm_bars=2`.
- **Expected Behavior**: 2 bar sonra işleme girmesi.
- **What may fail**: Strateji 0 trade açar. Çünkü 0. barda sayaç pulse aldığı an sıfıra atanır. (Pulse + Refresh incompatibility).

## 7. Severity Table

| ID | Severity | Area | Title | Behavior Change Risk | Parity Risk | Live Risk | Fix Priority |
|:---|:---|:---|:---|:---|:---|:---|:---|
| 01 | CRITICAL | Entry execution | Regime Lock never resets | High | Low (both buggy) | High | 1 |
| 02 | HIGH     | Signal Transform| Refresh on new raw blocks trades| High | High | Low | 2 |
| 03 | RESOLVED | Entry execution | Deferred Flip bypassed gates | None | None | None | - |
| 04 | RESOLVED | Guard Recovery  | Signals mode logic flaw | None | None | None | - |

## 8. Final Verdict
VERDICT: DEVAM EDEN RİSK.

Koda uygulanan son yamalar (Deferred Flip Re-gating ve Guard Recovery Signals düzelteçleri) MÜKEMMEL seviyede doğru mantıkla uygulanmış olup kodun stabilitesini aşırı derece yükseltmiştir. Ancak `regime_lock`'in hiçbir zaman release edilmediği unutulmuştur.
Bir sonraki yama adımında öncelik:
1. Full exit durumlarında `l4_regime_lock_side_state := 0` eklenmesidir.

RAPOR BİTTİ
