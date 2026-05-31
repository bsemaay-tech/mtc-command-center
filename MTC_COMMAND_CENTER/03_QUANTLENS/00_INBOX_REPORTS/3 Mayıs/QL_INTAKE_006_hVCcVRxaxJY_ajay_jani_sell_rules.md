# QuantLens Transcript Intake Report — 006

## 1. Intake Verdict

- **Video ID:** `hVCcVRxaxJY`
- **Normalized URL:** https://www.youtube.com/watch?v=hVCcVRxaxJY
- **Original URL:** https://youtu.be/hVCcVRxaxJY?si=G4BHCvH-VUG_Y91_
- **Transcript file:** `The Only Sell Rules You Need to Trade Ajay Jani.md`
- **Transcript hash:** `dedf65d06d87f44e45654ee784468ef934183db3b6bb641a87b0477a1f3863b1`
- **Primary classification:** `CANDIDATE`
- **Codex status recommendation:** `READY_FOR_PYTHON_PROTOTYPE`
- **Candidate type:** `EXIT_RULES / POSITION_MANAGEMENT_OVERLAY`
- **Standalone entry producer?** Hayır. Bu video daha çok sell-rule ve winner-hold yönetimi verir.
- **MTC_V2 relevance:** Çok yüksek. MTC_V2'nin `EXIT RULES`, `POSITION MANAGER`, `HTF/WEEKLY alignment`, `risk/open-risk control`, `partial harvesting` ve `leader-hold mode` katmanlarına doğrudan bağlanabilir.
- **Usefulness score:** `9/10`
- **Implementation priority:** `P1`
- **Recommended candidate ID:** `CAND_006_AJAY_JANI_SELL_RULES_10WEEK_V1`

## 2. Duplicate / Registry Decision

### Duplicate Check Result

- `video_id` daha önceki intake sırasındaki bilinen videolardan farklı.
- Transcript hash yeni görünüyor.
- Aynı başlık + aynı video_id + aynı transcript kombinasyonu görülmedi.
- **Duplicate status:** `NOT_DUPLICATE`

### Registry Recommendation

`_registry/youtube_video_index.csv` için önerilen kayıt:

```csv
video_id,normalized_url,title,channel,status,codex_status,transcript_hash,candidate_id,first_seen_at,last_seen_at,process_count
hVCcVRxaxJY,https://www.youtube.com/watch?v=hVCcVRxaxJY,The Only Sell Rules You Need to Trade Ajay Jani,UNKNOWN_CHANNEL,CANDIDATE,READY_FOR_PYTHON_PROTOTYPE,dedf65d06d87f44e45654ee784468ef934183db3b6bb641a87b0477a1f3863b1,CAND_006_AJAY_JANI_SELL_RULES_10WEEK_V1,2026-05-03,2026-05-03,1
```

> Kanal adı transcript içinde podcast bağlamıyla anlaşılabilir; ancak güvenilir channel id verilmediği için `UNKNOWN_CHANNEL` kabul edildi. Blacklist kararı verilmemelidir.

## 3. High-Level Summary

Bu transcript, giriş setup üreticisinden çok **sell rules / position management / winner-hold discipline** üzerine değerli bir adaydır. Ajay Jani'nin ana fikri şudur:

- Entry sinyali trading başarısının en önemli parçası değildir.
- Asıl edge, **risk yönetimi**, **nasıl çıkılacağı**, **kazananı ne kadar tutacağın**, **open-risk kontrolü** ve **duygusal kararların kurallarla sınırlandırılmasıdır**.
- Standart kazançların çoğu 20–25% civarında hasat edilebilir.
- Gerçek liderlerde ise 10-week / 40-week weekly trend kuralları kullanılarak daha büyük hareket yakalanabilir.
- Büyük liderlerin çoğu her zaman climax-top ile bitmez; sık görülen sonlanma şekillerinden biri **failed late-stage base breakout** olabilir.
- Liderlerde 20–25% sert pullback normal olabilir; 30% off-top fail-safe olarak ele alınmalıdır.
- Climax top tespiti için nicel checklist önerilir; transcriptte tüm kriterler verilmediğinden bu bölüm prototipte `NEEDS_RESEARCH / CONFIGURABLE CHECKLIST` olarak tasarlanmalıdır.

## 4. Why This Is a Candidate

### Aday olarak kabul edilme nedenleri

Bu video doğrudan kodlanabilir şu kural ailelerini veriyor:

1. **Initial loss control**
   - Kaybeden trade'ler hızlı kapatılır.
   - İlk risk çoğunlukla pivot / entry seviyesine göre tanımlanır.
   - Failed base breakout için 8% pivot altı exit mantığı var.

2. **Profit harvesting**
   - Standart trade'lerde 20–25% kazanç alımı.
   - Ama her pozisyon otomatik satılmaz; true leader için hold-mode devreye girebilir.

3. **10-week leader hold rule**
   - Büyük liderler çoğunlukla 10-week moving average üstünde kalır.
   - 10-week altı haftalık kapanış sayısı exit trigger olarak kullanılabilir.
   - 1 yıldan kısa ve 1 yıldan uzun hold dönemleri için farklı tolerans.

4. **40-week violation**
   - Büyük lider ana hareket sırasında 40-week altı kapanış yapmamalıdır.
   - 40-week altı kapanış ciddi trend bozulması olarak kabul edilir.

5. **30% off-top sell**
   - Lider hisse zirveden 30% düzeltirse satış.
   - Bu, büyük kazancı geri vermeyi sınırlayan hard fail-safe olabilir.

6. **Climax-top exit**
   - Eric Kroll tarzı climax top checklist.
   - 12 civarı kriterden aynı gün 6 tanesi veya iki ardışık günde 5 kriter sinyal verirse exit.
   - Transcript tüm alt kriterleri vermediği için bağımsız araştırma gerekir.

7. **Open-risk control**
   - Kârda bekleyen pozisyonun trailing stopu, ilk pozisyon riskinden çok daha geniş open-risk yaratabilir.
   - Bu nedenle 20–25% profit harvesting, portföy riskini sıfırlamak / yeniden düşük riskli setup'a döndürmek açısından mantıklı.

## 5. Extracted Core Rules

## 5.1 Entry Universe / Watchlist Context

Ajay'in kendi trading modeli giriş tarafında da bazı filtreler içeriyor; bu video ana olarak sell-rule videosu olsa da şu entry-context notları alınmalı:

### Weekly screening

- Screening çoğunlukla **weekly chart** üzerinden yapılır.
- Hazırlık genelde hafta sonu yapılır.
- Ready-list en fazla yaklaşık 10 isimdir.
- Daily chart daha sonra pivot, early entry, alert placement için kullanılır.

### Preferred stock categories

1. **Multi-year base + right-side tightening**
   - 2 yıl veya daha uzun basing.
   - Sağ tarafta tightening / supply drain.
   - Breakout sonrası büyük move potansiyeli.

2. **IPO near bear-market end or early new bull**
   - Bear market sonu veya yeni cycle başında çıkan IPO'lar.
   - İlk düzgün base / IPO base.

3. **Established leader setting up again**
   - Daha önce liderlik göstermiş hisse.
   - Higher-level base.
   - Yeni breakout veya pullback entry.

### Fundamental filters

- Down earnings / negative earnings genelde istenmez.
- Negative earnings varsa en az **50% sales growth** aranır.
- Triple-digit earnings ve sales tercih edilir.
- Daily dollar volume yüksek olmalı.
- Yüksek fiyatlı ve likit hisseler düşük fiyatlı hisselere göre daha çok tercih edilir.

## 5.2 Position Building Rule

Ajay klasik O'Neil tarzı kademeli pozisyon inşasını kullanıyor.

Örnek:

- Full target position: `20% NAV`
- Initial buy: `10% NAV`
- First add: `6% NAV`
- Second add: `4% NAV`

Bu yaklaşık olarak şu mantığa denk gelir:

```text
initial_position = 0.50 * full_position
add_1 = 0.30 * full_position
add_2 = 0.20 * full_position
```

MTC_V2 karşılığı:

- `max_entries` / add-on logic ile uyumlu.
- Add sadece trade çalıştıktan sonra yapılmalı.
- Add seviyeleri pivot/flat-base/secondary-base ile tanımlanmalı.
- Add sonrası basket stop / working exits yeniden senkronize edilmeli.

## 5.3 Standard Profit Harvest Rule

Ajay'in kritik dersi:

- Birçok trade için **20–25% gain** seviyesinde kâr almak mantıklı.
- Özellikle power-from-pivot yoksa veya hisse true leader olarak sınıflandırılmıyorsa bu disiplin portföyü korur.
- Bu sadece “kâr almak” değil; open-risk'i yeniden düşürme mekanizmasıdır.

### Why important for QuantLens

MTC_V2'de bu şu şekilde test edilebilir:

```text
if gain_pct >= profit_harvest_threshold and not leader_hold_mode:
    exit_reason = PROFIT_HARVEST_20_25
```

Config önerisi:

```yaml
profit_harvest_enabled: true
profit_harvest_pct: 0.22
profit_harvest_mode:
  - FULL_EXIT
  - PARTIAL_EXIT
  - REDUCE_TO_CORE
```

## 5.4 Power From Pivot / Hold-8-Weeks Context

Transcriptte doğrudan “power from pivot” fikri var:

- Eğer hisse pivot sonrası güçlü hareket etmiyorsa 20–25% satış mantıklı.
- Eğer güçlü hareket varsa veya true leader davranışı gösteriyorsa daha uzun tutulabilir.
- Ajay, bazı durumlarda 8 hafta tutmayı ve sonra değerlendirmeyi anlatıyor.

Prototype notu:

```text
power_from_pivot = close >= pivot_price * 1.20 within 3 weeks
```

Ancak transcriptte buna ait tüm nüanslar yok. O'Neil rule olarak bilinen bu fikir prototipte optional olmalı.

## 5.5 10-Week Hold Rule

Ana candidate modülünün kalbi budur.

### Base idea

True leader hareketinde hisse çoğunlukla 10-week moving average üstünde kalır.

Weekly basis:

```text
week_close >= sma_10_week
```

### Rule set

#### Hold duration < 1 year

- Eğer breakout sonrası hold süresi 1 yıldan azsa:
  - 10-week altında **iki ardışık haftalık kapanış** beklenebilir.
  - Sonra bu iki haftanın low seviyesi veya buna 5–7% cushion stop seviyesi olarak kullanılabilir.

Pseudo:

```python
if hold_weeks < 52:
    if weekly_close_below_10w_count_consecutive >= 2:
        stop_level = min(low_of_two_below_weeks) * (1 - cushion_pct)
        if close <= stop_level:
            exit("TEN_WEEK_RULE_CONFIRMED_BREAK")
```

#### Hold duration >= 1 year

- Eğer breakout'tan beri 1 yıldan fazla geçmişse:
  - İlk weekly close below 10-week sell trigger olabilir.

Pseudo:

```python
if hold_weeks >= 52:
    if weekly_close < sma_10w:
        exit("TEN_WEEK_RULE_AFTER_ONE_YEAR")
```

### Important MTC_V2 parity note

Bu weekly rule daily/intraday backtestte uygulanırken HTF repaint riski doğurur.

Pine/Python parity için:

- Weekly close sadece tamamlanmış haftadan sonra bilinmeli.
- Daily bar içinde henüz tamamlanmamış haftalık SMA/kapanış exit trigger olarak kullanılmamalı.
- Python'da `resample('W-FRI')` veya borsa haftasına göre weekly close kullanılmalı.
- Pine tarafında `request.security()` kullanılacaksa prior-closed weekly semantics zorunlu olmalı.

## 5.6 40-Week Violation Rule

Ajay'in net kuralı:

- Lider hisse ana move boyunca 40-week altında kapanmamalıdır.
- 40-week altında kapanış trendin bozulması olarak kabul edilir.
- Bu stop çoğu zaman daha geç ama daha yapısal bir exit sinyalidir.

Prototype:

```python
if weekly_close < sma_40w:
    exit("FORTY_WEEK_VIOLATION")
```

MTC_V2 risk:

- Weekly SMA alignment kesin olmalı.
- Exit-first pipeline'da protective exits ile çakışırsa reason priority belirlenmeli.

Önerilen priority:

```text
1. HARD_SL
2. 30PCT_OFF_TOP
3. 40W_VIOLATION
4. FAILED_BASE_8PCT_BELOW_PIVOT
5. 10W_RULE
6. CLIMAX_TOP
7. PROFIT_HARVEST
```

Bu priority kesin değildir; prototipte test edilmelidir.

## 5.7 30% Off-Top Rule

Ajay'in diğer hard fail-safe'i:

```text
if close <= highest_close_since_entry * 0.70:
    exit("THIRTY_PERCENT_OFF_TOP")
```

Alternatif:

```text
if low <= highest_high_since_entry * 0.70:
    exit intrabar using OHLC path policy
```

MTC_V2 için daha deterministik olan:

- `highest_high_since_entry` bazlı protective stop
- OHLC deterministic intrabar policy
- Bar-close mode'da `close` ile confirmed exit

Parametreler:

```yaml
off_top_exit_enabled: true
off_top_pct: 0.30
off_top_basis: HIGHEST_HIGH  # or HIGHEST_CLOSE
```

Bu kural özellikle büyük lideri tutarken portföyün açık kârını korumak için önemlidir.

## 5.8 Failed Base Breakout Rule

Transcriptte güçlü bir fikir var:

- Büyük liderler çoğu zaman climax top ile değil, late-stage failed base breakout ile biter.
- Uzun süre taşınan hisse yeni base kurup breakout yaparsa ve sonra pivotun 8% altına düşerse çık.

Prototype:

```python
if leader_hold_mode and new_base_breakout_detected:
    active_late_base_pivot = pivot_price

if active_late_base_pivot is not None:
    if close <= active_late_base_pivot * 0.92:
        exit("FAILED_BASE_8PCT_BELOW_PIVOT")
```

Bu kural için eksik taraf:

- `new_base_breakout_detected` mekanik tanımı transcriptte tam verilmedi.
- VCP/pivot module veya existing MTC producer output'u ile entegre edilmeli.
- İlk etapta manuel annotation / prototype-only event olarak tutulabilir.

## 5.9 Climax Top Rule

Ajay, Eric Kroll'dan aldığı climax top checklist'i nicelleştirdiğini anlatıyor.

Transcriptte verilen özet:

- Yaklaşık 12 kriter var.
- Aynı gün 6 kriter tetiklenirse climax top.
- İki ardışık günde 5 kriter tetiklenirse climax top.
- Gap-and-crap tarzı reversal da kriterlerden biridir.

Prototype skeleton:

```python
criteria_count_today = sum([
    largest_volume_period,
    price_extension_from_ma,
    wide_range_reversal,
    gap_up_reversal,
    largest_daily_gain_cluster,
    acceleration_after_long_run,
    close_near_low_after_gap,
    exhaustion_volume,
    adr_multiple_range,
    consecutive_up_days,
    percent_above_10w_extreme,
    percent_above_50d_extreme,
])

if criteria_count_today >= 6:
    exit("CLIMAX_TOP_CHECKLIST_6")
elif criteria_count_today >= 5 and criteria_count_yesterday >= 5:
    exit("CLIMAX_TOP_CHECKLIST_5X2")
```

### Important caveat

Transcript tüm 12 kriteri açıkça vermiyor. Bu nedenle:

- Bu modül doğrudan production'a alınmamalı.
- İlk prototype'ta sadece `climax_candidate_score` olarak hesaplanmalı.
- Historical model-book chartları üzerinde validasyon yapılmalı.
- False positive oranı ölçülmeli.

## 6. Strategy Candidate Design

## Candidate Name

`leader_hold_exit_overlay_v1`

## Purpose

Momentum/growth entry producer'larından gelen trade'lerde:

- Standart trade'i 20–25% arası hasat etmek.
- Gerçek liderlerde kârı daha uzun süre taşımak.
- Büyük lideri gereksiz erken satmamak.
- Ama open equity'yi tamamen geri vermemek için 10w/40w/30% off-top/failed-base/climax rules kullanmak.

## Intended Inputs

```yaml
entry_price
entry_date
position_side
current_close
current_high
current_low
weekly_close
weekly_low
sma_10w
sma_40w
highest_high_since_entry
highest_close_since_entry
pivot_price
new_base_pivot_price
hold_weeks
profit_pct
leader_hold_mode
power_from_pivot_flag
weekly_close_below_10w_consecutive_count
climax_score
```

## Intended Outputs

```yaml
exit_decision:
  should_exit: bool
  exit_type: FULL_EXIT | PARTIAL_EXIT | REDUCE_TO_CORE | HOLD
  reason_code: string
  stop_level: float | null
  evidence:
    - metric_name
    - metric_value
```

## Reason Codes

```text
PROFIT_HARVEST_20_25
TEN_WEEK_RULE_CONFIRMED_BREAK
TEN_WEEK_RULE_AFTER_ONE_YEAR
FORTY_WEEK_VIOLATION
THIRTY_PERCENT_OFF_TOP
FAILED_BASE_8PCT_BELOW_PIVOT
CLIMAX_TOP_CHECKLIST_6
CLIMAX_TOP_CHECKLIST_5X2
NO_EXIT_LEADER_HOLD_INTACT
```

## 7. MTC_V2 Integration Notes

### Best integration layer

Bu video bir signal producer değil. En doğru entegrasyon:

```text
7. EXIT RULES
```

İkinci etki alanı:

```text
4. POSITION MANAGER
5. POSITION SIZING
```

### Suggested MTC_V2 module

```text
exit_leader_hold_overlay
```

### Pipeline priority proposal

MTC_V2 exit-first yapısına uygun olarak:

1. Protective price exits: hard SL / catastrophic SL
2. Off-top fail-safe
3. 40-week violation
4. Failed-base 8% below pivot
5. 10-week rule
6. Climax top
7. Profit harvest
8. Opposite signal / filter block / time stop

### Parity-critical rules

- Weekly data must be prior-closed.
- Intrabar stop handling must be OHLC deterministic in Python.
- Pine `request.security()` kullanımı varsa no-lookahead zorunlu.
- Weekly close confirmed olmadan weekly exit sinyali üretilmemeli.
- `highest_high_since_entry` reset koşulları position lifecycle'a bağlı olmalı.
- Partial exit sonrası remaining core için stop seviyeleri yeniden hesaplanmalı.

## 8. Backtest / Prototype Hypotheses

Bu video için ilk Python prototype testlerinde şu hipotezler ölçülmeli:

### H1 — 20–25% profit harvesting vs hold-all

```text
Compare:
A) sell all at 22%
B) reduce to 50% at 22%, trail rest
C) no profit harvest, 10w only
```

Metrics:

- CAGR
- max drawdown
- profit factor
- average winner
- median winner
- largest giveback from peak open profit
- open-risk drawdown after +20% gain

### H2 — 10-week hold mode improves right-tail capture

Compare:

```text
A) 20–25% full exit
B) 10-week hold only after power-from-pivot
C) 10-week hold only after leader-score threshold
D) hybrid: 50–70% harvest at 22%, core rides 10w
```

### H3 — 30% off-top protects large open profits

Compare:

```text
A) 10w/40w only
B) 10w/40w + 30% off-top
C) 10w/40w + 25% off-top
D) 10w/40w + ATR-based off-top
```

### H4 — failed late-stage base rule exits earlier than 40w

Test:

```text
If new base breakout fails by 8% below pivot:
    does it reduce giveback without too many false exits?
```

### H5 — climax checklist value

Because checklist criteria are incomplete, prototype first as score:

```text
climax_score >= N
```

Then optimize N only after robust manual review.

## 9. Parameter Table

| Parameter | Default | Range | Notes |
|---|---:|---:|---|
| `profit_harvest_pct` | `0.22` | `0.20–0.25` | Standard gain harvest |
| `profit_harvest_mode` | `REDUCE_TO_CORE` | enum | Full/partial/core |
| `leader_hold_enabled` | `true` | bool | Enables 10w/40w logic |
| `power_from_pivot_pct` | `0.20` | `0.15–0.25` | Optional leader qualifier |
| `power_from_pivot_weeks` | `3` | `2–4` | O'Neil-style |
| `sma_10w_len` | `10` | fixed | Weekly MA |
| `sma_40w_len` | `40` | fixed | Weekly MA |
| `below_10w_weeks_before_1y` | `2` | `1–3` | Tolerance before 1 year |
| `below_10w_weeks_after_1y` | `1` | `1–2` | Tighter after 1 year |
| `ten_week_stop_cushion_pct` | `0.05` | `0.00–0.07` | Optional cushion |
| `off_top_pct` | `0.30` | `0.25–0.35` | Hard giveback exit |
| `failed_base_pct_below_pivot` | `0.08` | `0.06–0.10` | Late base failure |
| `climax_score_exit` | `6` | `5–8` | Needs research |
| `climax_score_two_day` | `5` | `4–6` | Needs research |

## 10. Coding Difficulty

- **Prototype difficulty:** Medium
- **Production difficulty:** High
- **Reason:** Weekly alignment, leader-mode state, late-base detection, climax checklist and partial exit interactions create parity risk.

### Easy parts

- 20–25% profit harvest
- 30% off-top rule
- 40-week close violation
- weekly 10w close count

### Hard parts

- power-from-pivot qualification
- detecting new base breakout after large move
- climax top checklist
- deciding when to switch from swing-mode to leader-hold-mode
- partial exit + open-risk accounting

## 11. Risk / Failure Modes

### Overfitting risk

High if climax checklist or late-stage base detection is optimized too aggressively.

### Regime risk

10-week hold rules may work best for true growth leaders and strong bull phases. Choppy markets may underperform unless entry/regime filters are strong.

### False hold risk

A stock that is not a true leader may be held too long if leader-mode is triggered incorrectly.

Mitigation:

```text
leader_hold_mode only if:
- high liquidity
- strong fundamentals or strong theme
- strong RS / momentum
- successful breakout
- preferably power-from-pivot or very strong early follow-through
```

### False exit risk

10-week weekly closes can be volatile around holidays / shortened weeks / market-wide corrections.

Mitigation:

- Use weekly confirmed close.
- Test 1-week vs 2-week close-below logic.
- Add breadth/regime context before full exit? Optional; avoid too much complexity in v1.

## 12. Trader Wiki Value

Bu video `CANDIDATE` olsa da Trader Wiki için de çok değerlidir.

Recommended wiki note:

```text
11_TRADER_WIKI/01_RISK_MANAGEMENT/TW_2026-05-03_sell_rules_open_risk_10week_hold_ajay_jani.md
```

Topic:

```text
Risk / position sizing / sell rules / holding winners
```

Wiki tags:

```text
sell-rules, open-risk, 10-week-rule, 40-week-rule, climax-top, profit-harvest, growth-stocks, ONeil, lifecycle-trade
```

## 13. Evidence Anchors From Transcript

Key transcript anchors:

- `0:11–0:17` — Getting out and protecting capital is more important than entry signal.
- `0:18–0:24` — 30% off top rule.
- `0:24–0:31` — Most leaders may top with failed base breakout, not always climax top.
- `15:02–16:39` — Van Tharp / coin-flip lesson and money management.
- `17:05–19:15` — Holding periods, win rate around 35%, win/loss about 4:1.
- `19:21–20:13` — Weekly screening and ready list up to 10 names.
- `20:36–21:56` — Three preferred stock categories.
- `22:16–23:56` — Fundamental quality rules and concentrated portfolio.
- `24:01–25:20` — Position building: 10%, 6%, 4% style.
- `32:03–35:14` — 10-week hold study, leaders and pullbacks.
- `37:59–38:43` — First close below 10-week after >1 year.
- `40:43–41:14` — Do not change rules intraday/weekday; add rules on weekend only.
- `46:36–50:29` — Take most gains at 20–25 and open-risk explanation.
- `51:39–55:49` — 30% off-top, 40-week sell, failed-base 8% below pivot.
- `56:18–58:53` — Climax top checklist concept.
- `1:01:21–1:04:33` — How to develop trading studies and repeatable sell rules.

## 14. Final Decision

### Final classification

```text
CANDIDATE
```

### Codex status

```text
READY_FOR_PYTHON_PROTOTYPE
```

### Candidate scope

```text
Exit-rule and position-management overlay for growth/momentum strategies.
```

### Not recommended as

```text
Standalone entry strategy producer.
```

### Recommended next action

Create Python prototype module only:

```text
research/prototypes/exit_leader_hold_overlay_v1/
```

Suggested files:

```text
exit_leader_hold_overlay.py
leader_hold_state.py
weekly_alignment.py
test_exit_leader_hold_overlay.py
README.md
```

No Pine implementation yet. First step should be deterministic Python prototype + fixture tests using synthetic OHLC/weekly scenarios.

## 15. Files Touched / Not Touched

### Created by this intake report

```text
QL_INTAKE_006_hVCcVRxaxJY_ajay_jani_sell_rules.md
```

### Not touched

```text
01_PINE/MTC_V2.pine
production Python runner files
backtest engine
optimization engine
CSV/data bundle/cache
broker/exchange/webhook/secret files
```

## 16. Next Action for Codex

Use this transcript as a module candidate and create a **Python-only deterministic prototype** for:

```text
leader_hold_exit_overlay_v1
```

Do not modify Pine. Do not run optimization. Do not backtest full datasets. Start with unit tests and synthetic OHLC/weekly fixtures:

1. Profit harvest at 22%.
2. 10-week rule below-close sequence.
3. 40-week violation.
4. 30% off-top fail-safe.
5. Failed base 8% below pivot.
6. Climax score placeholder.
7. Partial/core reduction state handling.
8. Weekly prior-closed alignment.
