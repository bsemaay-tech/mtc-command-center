# QuantLens Transcript Intake Report — GHZBv1W4-II

## 1. Executive Decision

- **Final Classification:** `CANDIDATE`
- **Codex Status Önerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Primary Candidate ID:** `QL_CAND_20260503_GHZBV1W4II_WILLIAMS_OOPS_VOL_BREAKOUT`
- **Secondary Wiki Note Önerisi:** Evet — `11_TRADER_WIKI/01_RISK_MANAGEMENT` ve `05_BACKTESTING_AND_OPTIMIZATION`
- **Confidence:** Medium-High
- **Ana gerekçe:** Transcript içinde kodlanabilir trade mantıkları var: volatility breakout, Oops Reversal, comparative strength, weekly setup + daily execution, fixed-percent risk sizing, protective stop, trailing stop ve no-average-down risk kuralı.
- **Ana uyarı:** Larry Williams eski pit-session / açılış gap yapısının elektronik piyasalarda zayıfladığını açıkça belirtiyor. Bu yüzden candidate doğrudan production strateji değil; önce Python prototype ve piyasa/sessiyon bazlı geçerlilik testi gerektirir.

## 2. Source Metadata

- **Source URL:** https://youtu.be/GHZBv1W4-II?si=de5dq3ybVKbtFD-b
- **Normalized URL:** https://www.youtube.com/watch?v=GHZBv1W4-II
- **Video ID:** `GHZBv1W4-II`
- **Title:** `11,300% Return in One Year Interview with Larry Williams`
- **Guest:** Larry Williams
- **Host / Program:** TraderLion / TrailLine podcast olarak transcript içinden çıkarıldı; kanal ID mevcut değil.
- **Channel Quality State:** `UNKNOWN`
- **Transcript File:** `/mnt/data/11,300% Return in One Year Interview with Larry Williams.md`
- **Transcript Character Count:** `72092`
- **Approx. Word Count:** `14436`
- **Normalized Transcript SHA256:** `c4a4eb3439509a5dcf32bae58380d73ed2cbe06ca04ac95227d1bc91b87d7ab4`
- **Raw File SHA256:** `84fa986bc4d0a9f9a72b79fba172c3cd1088bba29c90186a1163c93a84d1e94b`
- **Processed Date:** 2026-05-03

## 3. Prompt Compliance Check

- `01_PINE/MTC_V2.pine` değiştirilmedi.
- Production Python runner dosyaları değiştirilmedi.
- Backtest veya optimization çalıştırılmadı.
- Büyük CSV, data bundle, cache veya optimization result oluşturulmadı.
- Secret, API key, webhook, broker hesabı veya exchange key kullanılmadı.
- Bu rapor sadece intake / sınıflandırma raporudur.

## 4. Duplicate / Registry Check

### Current Conversation Scope

- Aynı video ID bu konuşmada daha önce işlenen iki videodan farklıdır:
  - `rdmjsbDVuoU`
  - `6aOnCK1gv2w`
  - Bu video: `GHZBv1W4-II`
- Transcript hash mevcut oturumdaki diğer dosyalardan farklı görünmektedir.

### Repo Scope Limitation

- `_registry/youtube_video_index.csv`, `channel_blacklist.yaml`, `channel_quality_registry.csv` dosyalarına erişim yok.
- Bu nedenle repo-genel duplicate ve kanal blacklist kontrolü kesin olarak doğrulanamadı.
- Repo içinde çalıştırılacak Codex aşamasında önce registry kontrolü yapılmalı.

## 5. Classification Rationale

Bu video `WIKI_ONLY` değil, çünkü sadece psikoloji / risk dersi anlatmıyor; aynı zamanda doğrudan kodlanabilir setup mantıkları veriyor:

1. **Volatility Breakout:** Opening price etrafında yukarı/aşağı bracket kurma ve büyük range günü yakalama fikri.
2. **Oops Reversal:** Piyasa önceki günün low seviyesinin altında açılıp tekrar o low seviyesini geri alırsa long; simetrik short versiyonu da test edilebilir.
3. **Comparative Strength:** Aynı ailedeki en güçlü varlığı long, en zayıf varlığı short tarafında seçme.
4. **Weekly Setup + Daily Trigger:** Haftalık COT/seasonality/valuation/preponderance setup; günlük grafikte breakout veya short-term higher-low trigger.
5. **Risk & Trade Management:** Fixed-percent risk, small positions + big trends, no averaging down, protective stop, target + trailing stop.

Bu nedenle ana sınıflandırma `CANDIDATE`; fakat risk yönetimi ve trader psikolojisi bölümleri ayrıca Trader Wiki’ye alınmaya değer.

## 6. Strategy Candidates

### Candidate A — Williams Opening Volatility Breakout

**Candidate ID:** `QL_CAND_20260503_GHZBV1W4II_VOL_BREAKOUT_OPEN`

**Core Idea:**

Açılış fiyatı etrafında yukarı ve aşağı bir breakout bandı oluşturulur. Fiyat açılıştan sonra bandın bir tarafını kırarsa, büyük range günü yakalama hedeflenir.

**Transcript Edge Kaynağı:**

- Büyük up-range günlerin çoğu low civarında açılıp high civarında kapandığı; büyük down-range günlerin de high civarında açılıp low civarında kapandığı anlatılıyor.
- Williams açılış fiyatını önemli kabul ediyor ve açılışın biraz üstü/altı bracket mantığıyla kırılan yöne trade fikrini anlatıyor.
- Ancak elektronik piyasalar ve pit-session gap’lerinin kaybolması nedeniyle bu setup’ın eski kadar pratik olmadığını söylüyor.

**Prototype Rules — Long:**

```text
session_open = current regular-session open
range_ref = prior_day_atr OR prior_day_range OR n-day avg true range
upper_trigger = session_open + k * range_ref
lower_trigger = session_open - k * range_ref

IF price crosses above upper_trigger
AND market/session filter is active
AND liquidity filter passes
THEN open long
initial_stop = session_open OR lower_trigger OR technical swing low
exit = target OR trailing stop OR end-of-session/time stop
```

**Prototype Rules — Short:**

```text
IF price crosses below lower_trigger
AND market/session filter is active
AND liquidity filter passes
THEN open short
initial_stop = session_open OR upper_trigger OR technical swing high
exit = target OR trailing stop OR end-of-session/time stop
```

**Key Parameters:**

- `k`: 0.05–0.50 ATR / range multiplier test grid.
- `range_ref`: prior day range, ATR(5), ATR(10), ORB range, session gap-adjusted range.
- `session_type`: equities RTH, futures Sunday open, crypto daily UTC open, crypto exchange day open.
- `hold_mode`: intraday close, N-bar hold, trailing stop, target + trail.
- `avoid_chop`: ADX / ATR expansion / market regime filter.

**Best Test Markets:**

- US equities with real overnight gaps.
- Index futures Sunday night sessions.
- Crypto pairs only if daily open convention creates meaningful impulse; otherwise lower priority.

**Risk:**

- The guest explicitly says this was much stronger in old pit-session markets. Modern 24h/electronic data may produce weaker edge.

---

### Candidate B — Oops Reversal Reclaim

**Candidate ID:** `QL_CAND_20260503_GHZBV1W4II_OOPS_REVERSAL`

**Core Idea:**

Gap-down veya open-below-prior-low durumunda fiyat önceki low seviyesini geri alırsa long reversal. Simetrik olarak open-above-prior-high ve prior high altına geri dönüş short reversal.

**Prototype Rules — Long:**

```text
prev_low = low[1]
open_gap_condition = open < prev_low
reclaim_trigger = prev_low

IF open_gap_condition
AND high crosses above prev_low
AND optional relative/comparative strength filter passes
THEN open long at reclaim_trigger or next bar open
initial_stop = session_low OR open_low OR reclaim_trigger - x * ATR
exit = target OR trailing stop OR close below reclaim level OR N-bar time stop
```

**Prototype Rules — Short:**

```text
prev_high = high[1]
open_gap_condition = open > prev_high
reclaim_trigger = prev_high

IF open_gap_condition
AND low crosses below prev_high
AND optional weakness filter passes
THEN open short
initial_stop = session_high OR open_high OR reclaim_trigger + x * ATR
exit = target OR trailing stop OR close above reclaim level OR N-bar time stop
```

**Important Filters:**

- Market gap-down day only.
- Long side: asset must be stronger than benchmark / family during the gap.
- Short side: asset must be weaker than benchmark / family during the gap-up.
- Avoid low liquidity names.
- For equities, test RTH open. For crypto, define a synthetic open carefully.

**Priority:** High, because it is rule-based, simple, and easy to prototype.

---

### Candidate C — Comparative Strength Family Selector

**Candidate ID:** `QL_CAND_20260503_GHZBV1W4II_COMPARATIVE_STRENGTH_SELECTOR`

**Core Idea:**

Aynı ailedeki / sektör içindeki varlıkları karşılaştır. Long için düşüşlerde en iyi tutunan ve rallilerde en çok yükselen en güçlü varlığı seç. Short için rallilerde zayıf kalan ve düşüşlerde daha fazla çöken varlığı seç.

**Prototype Long Ranking:**

```text
family = group of correlated assets
score = w1 * relative_return_n
      + w2 * drawdown_resilience
      + w3 * rally_participation
      + w4 * trend_strength

long_candidate = highest score asset in family
```

**Prototype Short Ranking:**

```text
short_candidate = lowest score asset in family
```

**MTC_V2 Use Case:**

- Signal Producer bağımsız olabilir.
- Comparative strength bir **Entry Gate** veya **Universe Selector** olarak tasarlanmalı.
- Long/short tarafında farklı eşik kullanılabilir.

**Required Data:**

- Sector/family map veya symbol baskets.
- Benchmark pair veya same-family cross comparison.
- Rolling returns, drawdown, ATR-normalized performance.

**Priority:** Medium-High. Tek başına entry sistemi değil; ancak diğer setup’ları güçlendiren güçlü bir filtre olabilir.

---

### Candidate D — Weekly Setup + Daily Breakout Execution

**Candidate ID:** `QL_CAND_20260503_GHZBV1W4II_WEEKLY_SETUP_DAILY_TRIGGER`

**Core Idea:**

Haftalık grafikte preponderance-of-evidence setup aranır: COT/commercial positioning, seasonality, valuation, broad trend context. Günlük grafikte ise trendline break, recent high breakout, short-term higher low veya mechanical trendline trigger ile giriş yapılır.

**Prototype Long Flow:**

```text
weekly_bias_long = cot_commercial_buying
                AND seasonal_window_positive
                AND valuation_not_overextended
                AND market_family_strength_ok

daily_trigger = close > highest_high_n OR price breaks descending trendline OR higher_low_confirmed

IF weekly_bias_long AND daily_trigger
THEN open long
initial_stop = technical invalidation level
exit = target OR trailing stop
```

**Practical Constraint:**

- COT/seasonality/valuation veri entegrasyonu olmadan bu candidate tam test edilemez.
- İlk etapta yalnızca daily trigger + comparative strength varyantı test edilmeli.

**Priority:** Medium. Veri ihtiyacı yüksek.

---

### Candidate E — Williams Risk Kernel / Position Sizing Module

**Candidate ID:** `QL_RISK_20260503_GHZBV1W4II_FIXED_RISK_KERNEL`

**Core Idea:**

Entry setup’tan bağımsız olarak her trade’de önceden belirlenmiş equity yüzdesi kadar risk alınır. Stop mesafesi pozisyon büyüklüğünü belirler. Averaging down yasak. Kazanç arttıkça risk nominal olarak büyür; bu compounding yaratır.

**Prototype Formula:**

```text
equity = account_equity
risk_pct = configured risk percent
risk_amount = equity * risk_pct
stop_distance = abs(entry_price - stop_price)
qty = risk_amount / stop_distance
qty = min(qty, max_leverage_cap, liquidity_cap)
```

**Rules:**

- Stop mesafesi teknik invalidation seviyesine göre belirlenir.
- Stop çok uzaksa trade atlanır veya qty küçülür.
- Aynı kaybeden pozisyona averaging down yapılmaz.
- Winning trend için trailing stop veya target + trailing stop kullanılır.
- Bet size emotional threshold üstüne çıkıyorsa risk_pct düşürülür.

**MTC_V2 Bağlantısı:**

- Position Sizing katmanı ile doğrudan uyumlu.
- `calc_sl` benzeri DRY stop fonksiyonlarıyla kullanılmalı.
- PortfolioState tarafında max exposure ve liquidation/margin risk ayrı korunmalı.

**Priority:** High, fakat yeni strateji değil; risk-management kernel.

## 7. Entry / Exit / Risk Extraction

### Entry Concepts

- Opening price breakout bracket.
- Prior day low/high reclaim reversal.
- Same-family comparative strength confirmation.
- Weekly setup alignment, daily trigger execution.
- Trendline break / recent high breakout / higher-low confirmation.

### Exit Concepts

- Protective stop placed at technical invalidation area.
- If target reached, take profit.
- If target not reached, trail protective stop.
- Big trend = give trade time; trend function is time.
- Stop must be in the market before walking away.

### Risk Concepts

- Bet small, catch large moves.
- Fixed percent of equity per trade.
- Position size derives from stop distance.
- Do not average down.
- Avoid oversized illiquid trades because liquidity affects both execution and psychology.
- Trade platform/order entry mistakes are a real operational risk; double-check orders.

## 8. MTC_V2 Integration Notes

### Safe Integration Layer

This content should not touch `01_PINE/MTC_V2.pine` immediately. First create isolated Python prototypes/contracts.

Recommended internal modules:

```text
06_QUANTLENS_LAB/candidates/QL_CAND_20260503_GHZBV1W4II_WILLIAMS_OOPS_VOL_BREAKOUT/
  README.md
  candidate_spec.yaml
  research_notes.md
  prototype_plan.md
  src/
    oops_reversal.py
    opening_vol_breakout.py
    comparative_strength.py
    risk_kernel.py
  tests/
    test_oops_reversal.py
    test_opening_vol_breakout.py
    test_position_sizing.py
```

### Where It Fits in MTC_V2 Architecture

- **Signal Producer:**
  - `OopsReversalProducer`
  - `OpeningVolatilityBreakoutProducer`
- **Entry Gates:**
  - `ComparativeStrengthGate`
  - `LiquidityGate`
  - `SessionGapGate`
  - `Trend/ADX/ATR expansion Gate`
- **Position Sizing:**
  - Fixed percent risk based on stop distance.
- **Position Manager:**
  - No averaging down rule.
  - Optional same-day no-reentry after stopout.
- **Exit Rules:**
  - Protective stop.
  - Target + trailing stop.
  - Time stop for non-follow-through reversals.

### Parity Considerations

- Session open definitions must be deterministic.
- For stocks, RTH open vs premarket matters.
- For futures, Sunday night session requires exchange calendar handling.
- For crypto, “open” is artificial; define UTC daily open or exchange session anchor.
- Gap rules require explicit previous session high/low, not just rolling daily OHLC if session boundaries differ.
- Intrabar fill ambiguity must be controlled via OHLC-deterministic ordering.

## 9. Backtest Design Recommendations

### Phase 1 — Pure Candidate Isolation

- Implement only rule detection and signal marking.
- No MTC_V2 production runner change.
- Generate trace outputs for:
  - `open`
  - `prev_high`
  - `prev_low`
  - `gap_condition`
  - `reclaim_trigger`
  - `entry_price`
  - `initial_stop`
  - `risk_qty`
  - `exit_reason`

### Phase 2 — Market-Specific Validation

Run separately:

1. US equities with true gaps.
2. Index futures with Sunday session test.
3. Crypto daily synthetic open test.
4. Crypto intraday session-anchor test.

### Phase 3 — Filter Ablation

Test with and without:

- Comparative strength filter.
- Liquidity filter.
- ATR expansion filter.
- Market regime filter.
- Time-of-day/session filter.

### Phase 4 — Robustness

- Walk-forward periods.
- Bull/bear/sideways regime split.
- Slippage stress.
- Gap-through-stop stress.
- Parameter stability around `k` and stop/target settings.

## 10. Scoring

| Dimension | Score | Notes |
|---|---:|---|
| Codability | 8/10 | Oops Reversal and volatility breakout are directly rule-based. |
| Data Availability | 7/10 | Daily OHLC enough for Oops; intraday/session data better for fill quality. COT/seasonality requires extra data. |
| MTC_V2 Fit | 8/10 | Producer + gate + sizing + exit model fits existing architecture. |
| Edge Freshness Risk | 5/10 | Guest explicitly says pit-session edge degraded in modern electronic markets. |
| Risk Management Value | 9/10 | Fixed-percent sizing, no averaging down, liquidity psychology, stops are highly useful. |
| Immediate Pine Readiness | 4/10 | Too early; Python prototype first. |
| Overall Research Priority | 8/10 | Worth prototyping because rules are simple and historically important. |

## 11. Red Flags / Risky Claims

- **11,300% return context is extreme:** It came from very high risk and 30% equity risk per trade according to the transcript. This should not be used as a normal risk model.
- **Old market microstructure:** Opening volatility breakout was stronger when pit sessions had large overnight gaps. Modern electronic futures may not behave the same.
- **COT/seasonality integration:** These can become overfit if not validated across regimes and out-of-sample periods.
- **Fixed percent risk can still be aggressive:** Williams mentions high risk tolerance. MTC default should use much lower controlled risk.
- **Oops Reversal may require precise session definitions:** Bad session anchoring can create false historical signals.

## 12. Trader Wiki Extraction

### Suggested Wiki Note

```text
TW_2026-05-03_01_RISK_MANAGEMENT_larry_williams_small_positions_big_trends.md
```

### Wiki Topic

- `01_RISK_MANAGEMENT`
- `02_TRADING_PSYCHOLOGY`
- `05_BACKTESTING_AND_OPTIMIZATION`

### Wiki Summary

Larry Williams emphasizes that trend requires time, and the practical way to exploit big trends is to keep positions small enough to survive volatility and remain emotionally stable. Risk is not only a money-management problem; it is also emotional management. The transcript strongly warns against averaging down, overbetting, platform/order-entry mistakes, and expecting instant wealth.

## 13. Proposed Candidate Registry Row

```csv
candidate_id,video_id,title,status,codex_status,primary_setup,secondary_setup,channel,source_url,transcript_hash,created_at
QL_CAND_20260503_GHZBV1W4II_WILLIAMS_OOPS_VOL_BREAKOUT,GHZBv1W4-II,"11,300% Return in One Year Interview with Larry Williams",CANDIDATE,READY_FOR_PYTHON_PROTOTYPE,"Oops Reversal / Opening Volatility Breakout","Comparative Strength / Fixed Risk Kernel",UNKNOWN_CHANNEL,https://www.youtube.com/watch?v=GHZBv1W4-II,c4a4eb3439509a5dcf32bae58380d73ed2cbe06ca04ac95227d1bc91b87d7ab4,2026-05-03
```

## 14. Next Action for Codex

Do **not** edit Pine yet.

Give Codex this task:

```text
Create an isolated QuantLens candidate folder for Larry Williams Oops Reversal + Opening Volatility Breakout. Do not modify 01_PINE/MTC_V2.pine. Do not modify production Python runner. Do not run full optimization. First read registries for duplicate/channel checks. If not duplicate, create candidate_spec.yaml, research_notes.md, prototype_plan.md, and minimal pure-function Python modules for signal detection only. Include unit tests using synthetic OHLC fixtures for: gap below prior low then reclaim; gap above prior high then reject; opening bracket breakout long/short; fixed-percent risk sizing from stop distance. No backtest run yet.
```

## 15. Files Created / Not Touched

### Created by this intake step

- `INTAKE_2026-05-03_GHZBv1W4-II_larry_williams.md`

### Not touched

- `01_PINE/MTC_V2.pine`
- Production Python runner files
- Backtest / optimization output folders
- Registry CSV/YAML files
- Broker/exchange/webhook secrets

## 16. Final Verdict

This is a **valid QuantLens strategy candidate** because it contains multiple codable and historically meaningful trade structures. The highest priority prototype is **Oops Reversal**, followed by **Opening Volatility Breakout** with careful session handling. The risk-management lessons should also be saved as a Trader Wiki note.

**Final Classification:** `CANDIDATE`  
**Codex Status:** `READY_FOR_PYTHON_PROTOTYPE`  
**Production Readiness:** Not ready; isolated Python prototype first.
