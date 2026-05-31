# QuantLens Transcript Intake Report — 004 / 068

## 1. Metadata

- **Report ID:** `INTAKE_004_M_tD6X0CSOI`
- **Source URL:** `https://youtu.be/M_tD6X0CSOI?si=7w03YALv0bHJJJUE`
- **Normalized URL:** `https://www.youtube.com/watch?v=M_tD6X0CSOI`
- **Video ID:** `M_tD6X0CSOI`
- **Title:** `The Perfect VCP Trading Setup with Mark Minervini`
- **Series / Theme:** TraderLion / Ultimate Trading Guide style interview — Mark Minervini, VCP, correction leadership, market breadth, progressive exposure
- **Channel:** `UNKNOWN_CHANNEL`
  - Transcript içinde host ve podcast bağlamı var; fakat kanal adı ve kanal id güvenilir metadata olarak ayrıca verilmedi. Intake kuralına göre `UNKNOWN_CHANNEL` kullanıldı.
- **Source transcript file:** `The Perfect VCP Trading Setup with Mark Minervini.md`
- **Prompt file used:** `00_quantlens_transcript_intake_prompt.md`
- **Generated date:** `2026-05-03`
- **Transcript hash method:** lowercase + whitespace-normalized SHA256 over full transcript text
- **Transcript hash:** `eafb37522f8a4f418558d50601fbb1f6f554dbac164ed8ac8d061ae65114acfb`

---

## 2. Intake Verdict

- **Classification:** `CANDIDATE`
- **Codex Status Önerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Candidate Priority:** `P0 / P1 — High-value core momentum candidate`
- **Usefulness Score:** `10 / 10`
- **Coding Readiness Score:** `8 / 10`
- **MTC_V2 Fit Score:** `9 / 10`
- **Wiki Note Also Valuable:** `YES`

### Verdict Summary

Bu transcript kesinlikle `WIKI_ONLY` değildir. İçerik; doğrudan kodlanabilir **VCP + relative strength + correction leader + progressive exposure** sistem mantığı veriyor.

Ana fikir:

> Market correction döneminde tamamen uzaklaşmak yerine lider adaylarını taramak gerekir. En iyi adaylar, correction sırasında en az düşen, relative strength çizgisi yeni high yapan, market diplerinden en hızlı yeni high bölgesine dönen, base/VCP içinde sıkışan ve follow-through / accumulation sonrası düşük riskli entry veren hisselerdir. İlk pilot pozisyonlar çalışırsa exposure hızlı ama kademeli artırılır.

Bu video, önceki 002 ve 003 raporlarıyla çok güçlü şekilde birleşir:

- `002` entry tactic library sağlar.
- `003` edge/setup framework sağlar.
- `004` correction sonrası **lider seçimi + VCP timing + progressive exposure** katmanını tamamlar.

QuantLens açısından bu rapor, isolated Python research prototype için yüksek öncelikli candidate olarak işlenmelidir.

---

## 3. Duplicate / Registry Check

### Current Environment Check

- `_registry/youtube_video_index.csv` dosyası bu konuşmada verilmedi.
- `channel_blacklist.yaml` dosyası bu konuşmada verilmedi.
- `channel_quality_registry.csv` dosyası bu konuşmada verilmedi.

### Result

- **Duplicate status:** `NOT_VERIFIED_AGAINST_REPO_REGISTRY`
- **Current conversation duplicate:** `NO_DUPLICATE_DETECTED`
- **Known current batch conflict:** `NO`
  - `001` video id: `Lot25-2fb-4`
  - `002` video id: `oZH6_XRxtDc`
  - `003` video id: `NwgJQyoUAaI`
  - Bu video id: `M_tD6X0CSOI`
- **Action:** Gerçek repo'ya yazılmadan önce Codex registry dosyalarını okuyup `video_id` ve `transcript_hash` ile duplicate kontrolünü tekrar yapmalıdır.

### Registry Row Draft

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,first_seen_at,last_seen_at,process_count
M_tD6X0CSOI,https://www.youtube.com/watch?v=M_tD6X0CSOI,"The Perfect VCP Trading Setup with Mark Minervini",UNKNOWN_CHANNEL,CANDIDATE,CAND_20260503_MINERVINI_VCP_CORRECTION_LEADERS_M_tD6X0CSOI,eafb37522f8a4f418558d50601fbb1f6f554dbac164ed8ac8d061ae65114acfb,2026-05-03,2026-05-03,1
```

---

## 4. Channel Quality Check

- **Channel:** `UNKNOWN_CHANNEL`
- **Blacklist decision:** `NO_BLACKLIST_DECISION`
- **Reason:** Kanal adı / kanal id güvenilir şekilde verilmediği için blacklist veya watchlist kararı verilmedi.
- **Suggested quality update after repo check:** Eğer kanal daha önce işlenmemişse `UNKNOWN`; bu video sonucu çok güçlü candidate olduğu için `candidate_count += 1`.
- **Batch pattern note:** 002, 003 ve 004 aynı eğitim ekosisteminden geliyorsa kanal `GOOD` durumuna adaydır; fakat kanal id doğrulanmadan otomatik karar verilmemelidir.

---

## 5. Strategy Candidate

### Candidate ID

`CAND_20260503_MINERVINI_VCP_CORRECTION_LEADERS_M_tD6X0CSOI`

### Candidate Name

**Minervini VCP Correction Leader + Progressive Exposure System**

### Strategy Family

- Momentum leadership
- VCP / volatility contraction
- Relative strength leadership
- Market correction recovery
- Breadth-aware regime filter
- Progressive exposure / pilot-buy scaling
- Tight-risk breakout continuation

### Primary Market

- **Best native fit:** US equities
- **Reason:** Transcript; S&P 500, Nasdaq, Russell 2000, IBD 50, 50/200-day breadth, IPOs, earnings/growth leaders, bases and VCP structures üzerine kurulu.
- **Crypto adaptation:** Possible but secondary. Crypto'da earnings, industry group ve IPO lifecycle katmanları yoktur; fakat VCP, RS, market-regime ve progressive exposure mantığı OHLCV + benchmark yapısıyla uyarlanabilir.

---

## 6. Core Thesis Extracted

### 6.1 Corrections Are Research Windows

Correction sırasında tamamen tatil moduna geçmek doğru değildir. En büyük leverage fırsatları, correction boyunca güçlü kalan ve correction biterken ilk yeni high yapan hisselerde oluşur.

Kodlanabilir çıkarım:

```text
During correction:
  scan universe daily
  rank stocks by relative strength preservation
  detect stocks close to 52-week/new high
  detect bases/VCP tightening
  wait for market confirmation + stock breakout
```

### 6.2 Stocks Lead Groups; Groups Confirm Market Strength

Transcriptte önemli sıralama şudur:

```text
1. En iyi hisseleri bul.
2. Aynı grupta çok sayıda güçlü hisse varsa group/theme gücü onaylanır.
3. Birden fazla güçlü grup varsa market breadth / participation onaylanır.
```

Bu, “önce sektör seç, sonra hisse ara” yaklaşımının tersidir. Candidate için daha doğru workflow:

```text
stock_leadership_scan -> group_cluster_detection -> market_participation_confirmation
```

### 6.3 Follow-Through Day Alone Is Not Enough

Market follow-through / accumulation varsa bile rastgele hisse alınmaz. Mutlaka:

- stock base'den çıkıyor olmalı,
- yapı tight olmalı,
- right-sized risk olmalı,
- RS veya leadership kanıtı olmalı.

### 6.4 Strategy Must Be Better Than the Trader

Transcriptte “strateji senden daha iyi olabilir; mesele disiplinle uygulamak” fikri çok güçlü. Bu, QuantLens için şu anlama gelir:

```text
Discretionary expert patternleri deterministic detector + rule set haline getir.
Sonra trader intervention'ını azalt.
```

---

## 7. Extracted System Modules

## 7.1 Market Breadth / Participation Regime Filter

### Concept

Indexler birkaç mega-cap tarafından yukarı taşınırken breadth bozulabilir. Bu durumda breakout başarısı düşebilir. Transcriptte özellikle yüzde olarak 50-day ve 200-day moving average üzerinde olan hisse oranları kullanılıyor.

### Candidate Logic

```text
pct_above_50 = count(close > sma(close, 50)) / universe_count
pct_above_200 = count(close > sma(close, 200)) / universe_count

breadth_warning = pct_above_200 < 0.50
                  AND index_close near_or_above_recent_high

breadth_danger = pct_above_200 < 0.40
                 AND index_making_new_high_or_diverging
```

### Regime States

```text
MARKET_REGIME:
  SUPPORTIVE:
    index above ma50 and ma200
    breadth improving
    accumulation/follow-through visible
    leaders breaking out

  NEUTRAL:
    index recovering but breadth mixed
    few leaders emerging
    pilot exposure only

  HOSTILE:
    distribution dominant
    breadth below danger thresholds
    leaders failing / watchlist deteriorating
    no new aggressive exposure
```

### MTC_V2 Mapping

- `Entry Gate`: `market_regime_gate`
- `PortfolioState guard`: reduce exposure when hostile
- `Position Sizing`: max risk / max position tier depends on regime

---

## 7.2 Correction Leader Detector

### Concept

En iyi liderler correction sırasında en az düşer veya market diplerinden çok hızlı yeni high bölgesine döner.

### Candidate Logic

```text
market_drawdown = index_close / rolling_max(index_close, correction_window) - 1
symbol_drawdown = close / rolling_max(close, correction_window) - 1

relative_drawdown_strength = symbol_drawdown - market_drawdown
near_high = close >= rolling_max(close, 252) * (1 - max_distance_from_high)

correction_leader = market_drawdown <= -correction_threshold
                    AND symbol_drawdown > market_drawdown
                    AND near_high
```

Recommended parameters for research only:

```text
correction_window = 60 to 120 trading days
correction_threshold = 8% to 12%
max_distance_from_high = 25%  # transcriptte "within 25% of a new high" vurgusu var
```

### Stronger Version

```text
first_to_new_high = days_since_market_low <= 10/18/30
                    AND close >= rolling_max(close, 252)

fast_recovery_score = 1 / max(days_to_new_high_after_market_low, 1)
```

### Examples from Transcript

- AMGN: correction lows sonrası yeni high ve büyük winner
- FICO: correction lows sonrası explosive action
- PTON: 18 gün içinde new high
- CSCO: 10 gün içinde new high
- DOCU: 10 gün içinde new high
- CMG: correction sırasında RS high + VCP maturity

---

## 7.3 Relative Strength New High Detector

### Concept

RS line yeni high yapıyorsa, hisse markete göre liderdir. Fiyat yeni high yapmasa bile RS line yeni high yapabilir; market düşerken hisse yatay kalsa bile outperform eder.

### Candidate Logic

```text
rs_line = close / benchmark_close
rs_new_high_252 = rs_line >= rolling_max(rs_line, 252)
rs_new_high_63 = rs_line >= rolling_max(rs_line, 63)

rs_leader = rs_new_high_63 OR rs_new_high_252
```

### Quality Enhancers

```text
price_near_high = close >= rolling_max(close, 252) * 0.75
price_above_ma50 = close > sma(close, 50)
rs_slope_positive = linreg_slope(rs_line, 20) > 0
```

### MTC_V2 Mapping

- `Entry Gate`: `RS_new_high_gate`
- `Setup score`: add score when RS line new high before price breakout
- `Regime-aware`: RS is most valuable during correction / early recovery

---

## 7.4 VCP / Volatility Contraction Setup Detector

### Concept

VCP; base içinde volatilitenin ve range'in daralması, arzın azalması, fiyatın tight hale gelmesi ve pivot civarında düşük riskli entry vermesidir.

### Candidate Logic Draft

```text
range_pct = (high - low) / close
atr_pct = atr(14) / close
volume_ratio = sma(volume, 5) / sma(volume, 50)

contraction_1 = recent_swing_range_1 < prior_swing_range_1
contraction_2 = recent_swing_range_2 < prior_swing_range_2
volume_dryup = volume_ratio < 0.70
price_tight = rolling_std(close_pct_change, 5) < rolling_std(close_pct_change, 20)

vcp_setup = base_context
            AND contraction_1
            AND contraction_2
            AND volume_dryup
            AND price_tight
            AND close_near_base_high
```

### Pivot Trigger

```text
pivot_high = rolling_max(high, pivot_lookback)
breakout = close > pivot_high AND volume > sma(volume, 20)

vcp_trigger = vcp_setup AND breakout
```

### Stop Ideas

```text
initial_stop = min(last_contraction_low, short_range_low) - buffer
risk_pct = (entry_price - initial_stop) / entry_price
valid_risk = risk_pct <= max_risk_pct
```

Recommended initial research max risk:

```text
max_risk_pct = 2% to 6% depending on timeframe and stock volatility
```

---

## 7.5 Follow-Through + Stock Setup Confirmation

### Concept

Market follow-through day varsa ama kaliteli setup yoksa trade açılmamalı. Candidate şu şekilde ayrıştırılmalı:

```text
market_confirmation = follow_through_day OR accumulation_recovery_state
stock_confirmation = vcp_trigger OR base_breakout OR first_to_new_high_trigger

entry_allowed = market_confirmation AND stock_confirmation
```

### Follow-Through Day Approximation

Tam O'Neill FTD tanımı veri/kurala göre değişebilir. İlk prototype için basit approximation:

```text
follow_through_day = days_since_market_low >= 4
                     AND index_return >= min_followthrough_gain
                     AND index_volume > prior_day_volume
```

Bu approximation kesin O'Neill tanımı gibi iddia edilmemeli; sadece research tag'i olarak kullanılmalı.

---

## 7.6 Progressive Exposure Engine

### Concept

Trades çalışmıyorsa exposure artırılmaz; hatta düşürülür. Pilot buys çalışıyorsa exposure hızlı şekilde artırılabilir.

Transcriptte örnek davranış:

```text
initial toe-in-water exposure ≈ 25% total account
if working -> ramp to 50%
if still working and more setups -> 75% to 100%
```

### Candidate Logic

```text
portfolio_heat = sum(open_position_risk_pct)
realized_recent_R = sum(closed_trade_R over recent_window)
unrealized_R = sum(open_trade_R)
working_positions = count(open_positions with R >= min_working_R)
failed_recent_trades = count(closed_trades with R <= -1 over recent_window)

if market_regime == HOSTILE:
    max_gross_exposure = 0.00 to 0.25
elif market_regime == NEUTRAL:
    max_gross_exposure = 0.25 to 0.50
elif market_regime == SUPPORTIVE and pilot_trades_working:
    max_gross_exposure = 0.50 to 1.00
```

### Exposure Ramp Rule Draft

```text
pilot_trades_working = working_positions >= 1
                       AND unrealized_R >= +1R
                       AND failed_recent_trades <= threshold

ramp_allowed = market_regime == SUPPORTIVE
               AND pilot_trades_working
               AND watchlist_quality_score improving
```

### MTC_V2 Mapping

- `PortfolioState`: owns recent R, open risk, gross exposure, realized/unrealized performance
- `Entry Guard`: `progressive_exposure_guard`
- `Position Sizing`: allowed risk tier changes based on exposure state

---

## 8. Candidate Architecture

```text
UNIVERSE SCAN
  ├─ Market Breadth / Regime
  │   ├─ pct_above_50d
  │   ├─ pct_above_200d
  │   ├─ index trend
  │   └─ accumulation / distribution approximation
  │
  ├─ Leadership Scan
  │   ├─ correction leader score
  │   ├─ RS new high score
  │   ├─ near 52-week high
  │   ├─ first off lows / fast recovery
  │   └─ IPO / magnitude play flag
  │
  ├─ Setup Scan
  │   ├─ VCP contraction
  │   ├─ base maturity
  │   ├─ price tightness
  │   ├─ volume dry-up
  │   └─ pivot proximity
  │
  ├─ Entry Trigger
  │   ├─ pivot breakout
  │   ├─ base breakout
  │   ├─ EP / gap optional integration
  │   └─ Ep3 entry tactic library optional
  │
  └─ Portfolio Exposure
      ├─ pilot buy
      ├─ working/not-working feedback
      ├─ scale to 50/75/100%
      └─ cut exposure if watchlist/holdings deteriorate
```

---

## 9. MTC_V2 Mapping

| Concept | MTC_V2 Layer | Recommended Treatment |
|---|---|---|
| Breadth divergence | Global Config / Market Regime Gate | External input or benchmark-universe calculation |
| Correction leader score | Entry Gate / Universe scanner | Pre-filter before producer signal |
| RS new high | Entry Gate | Strong candidate gate |
| VCP setup | Signal Producer or setup context producer | Build isolated detector first |
| Pivot breakout | Signal Producer trigger | Bar-close confirmed only |
| Tight risk / right size | Position sizing + SL | Use calculated stop from contraction low |
| Progressive exposure | PortfolioState guard | Scale max exposure only after trades work |
| Sell into strength | Exit Rules | Later phase; partial TP / extension logic |
| Watchlist deterioration | PortfolioState / Market Guard | Block new entries or reduce exposure |

### Important Pine Warning

Bu candidate doğrudan Pine'a gömülmemeli. VCP, breadth ve correction-leader scanning Pine içinde ağır olabilir. İlk aşamada Python research prototype daha uygundur.

---

## 10. Prototype Plan

### Phase 0 — No Repo Mutation Beyond Isolated Folder

Rules:

- `01_PINE/MTC_V2.pine` değiştirilmez.
- Production Python runner değiştirilmez.
- Backtest / optimization çalıştırılmaz.
- Büyük CSV / data bundle oluşturulmaz.

Suggested folder:

```text
06_QUANTLENS_LAB/research/minervini_vcp_004/
  README.md
  intake_notes.md
  feature_schema.md
  market_regime_breadth.py
  correction_leader.py
  rs_new_high.py
  vcp_detector.py
  progressive_exposure.py
  tests/
    test_rs_new_high.py
    test_vcp_detector.py
    test_progressive_exposure.py
```

### Phase 1 — Feature Detectors Only

Implement pure functions:

```python
calc_rs_line(symbol_close, benchmark_close)
is_rs_new_high(rs_line, lookback)
calc_pct_above_ma(universe_closes, ma_window)
detect_correction_leader(symbol_close, benchmark_close)
detect_vcp_contraction(ohlcv)
detect_vcp_pivot_breakout(ohlcv)
```

### Phase 2 — Manual Example Fixtures

Use hand-labeled examples from transcript:

```text
AMGN 1990
FICO correction recovery
PTON first-to-new-high
CSCO IPO / correction leader
DOCU RS leader
CMG VCP buy point
```

Do not claim test pass until real OHLCV data is provided.

### Phase 3 — Event Label Schema

```json
{
  "event_type": "MINERVINI_VCP_CORRECTION_LEADER",
  "video_id": "M_tD6X0CSOI",
  "candidate_id": "CAND_20260503_MINERVINI_VCP_CORRECTION_LEADERS_M_tD6X0CSOI",
  "symbol": "EXAMPLE",
  "timeframe": "1D",
  "market_regime": "CORRECTION | RECOVERY | UPTREND | HOSTILE",
  "breadth_pct_above_50": 0.0,
  "breadth_pct_above_200": 0.0,
  "rs_new_high": false,
  "price_near_high_pct": 0.0,
  "days_to_new_high_after_market_low": null,
  "vcp_score": 0,
  "pivot_price": 0.0,
  "entry_price": 0.0,
  "initial_stop": 0.0,
  "risk_pct": 0.0,
  "exposure_state": "PILOT | RAMP_50 | RAMP_75 | FULL | DEFENSIVE",
  "reason_codes": []
}
```

### Phase 4 — Validation Metrics

```text
Detector accuracy:
  - known example detected? yes/no
  - detected date within acceptable window?
  - false positive density per symbol/year

Trade outcome labels:
  - MFE_5d / 10d / 20d / 60d
  - MAE_5d / 10d / 20d / 60d
  - reached_2R_before_stop
  - reached_3R_before_stop
  - stopped_before_followthrough

Portfolio/exposure labels:
  - pilot trade success rate
  - ramp after pilot success vs immediate full exposure
  - drawdown reduction from progressive exposure
```

---

## 11. Potential Ruleset Draft

### Long Candidate Conditions

```text
market_regime != HOSTILE
AND stock_drawdown_from_high <= 25%
AND rs_line_new_high_63_or_252 == true
AND price_above_ma50 == true
AND vcp_setup_score >= threshold
AND pivot_breakout_confirmed_at_bar_close == true
AND risk_pct <= max_allowed_risk_pct
```

### Initial Stop

```text
stop = last_vcp_contraction_low - buffer
OR stop = short_range_low - buffer
```

### Entry

```text
entry = close on confirmed breakout bar
OR next_open after confirmed breakout
```

For parity-first research, use bar-close confirmed entry first. Intraday entry tactics can be later mapped from 002.

### Exposure

```text
if no current exposure and regime supportive:
    open pilot position only
if pilot open trade reaches +1R or closes constructively and new setups exist:
    allow next position / add exposure
if recent trades fail:
    reduce allowed exposure
```

### Exit / Partial Sell Into Strength

Transcript gives discretionary sell-into-strength guidance but not enough for strict first prototype. For now:

```text
phase_1_exit = initial_stop only + optional 2R/3R diagnostic labels
phase_2_exit = partial sell into strength after extension from MA / R multiple
```

Do not overfit exits in first implementation.

---

## 12. Risks / Suspicious or Non-Systematic Claims

### 12.1 Discretionary Pattern Recognition

Minervini-style VCP has many visual components. A naive detector may confuse random tight ranges with true institutional-quality VCP.

Mitigation:

```text
Require RS new high + near high + market recovery + volume dry-up + contraction sequence.
```

### 12.2 Survivorship Bias

Examples are mostly historic winners. Validation must run on full liquid universe, not only known winners.

### 12.3 Breadth Data Availability

`pct_above_50` and `pct_above_200` require universe-wide data. If data is unavailable, use ETFs/index proxies but mark as approximation.

### 12.4 US Equity Specificity

The strategy is US equities-native. For crypto, remove IPO/earnings/group-fundamental assumptions and test only RS/VCP/regime variants.

### 12.5 Overhead Supply Rule Ambiguity

Transcript mentions avoiding names down 40–50% from highs because of overhead supply, but exact threshold may vary. Use `<=25% from high` as initial research assumption, not final truth.

### 12.6 Follow-Through Day Approximation Risk

O'Neill FTD is not fully specified in transcript. Use a clearly labeled approximation until exact rules are defined.

### 12.7 Progressive Exposure Can Increase Drawdown If Trigger Is Weak

Exposure ramp must require real feedback from pilot trades. If ramp triggers on weak signals, system can become pro-cyclical at bad moments.

---

## 13. Trader Wiki Note Also Recommended

Bu video Trader Wiki'ye ayrıca alınmalı. Çünkü strateji yanında correction döneminde çalışma disiplini, breadth yorumlama, lider seçimi ve psikoloji açısından güçlü dersler içeriyor.

### Suggested Wiki Entry

- **Wiki status:** `ALSO_CREATE_WIKI_NOTE`
- **Topic:** `04_SYSTEM_DEVELOPMENT` + `05_BACKTESTING_AND_OPTIMIZATION` + `01_RISK_MANAGEMENT`
- **Suggested file name:** `TW_2026-05-03_04_SYSTEM_DEVELOPMENT_minervini_vcp_correction_leaders.md`

### Wiki Themes

- Correction dönemleri araştırma dönemidir.
- Liderler market cycle'ı önden haber verir.
- Stocklar gruplara, gruplar market sağlığına götürür.
- Follow-through day tek başına alım sinyali değildir; kaliteli setup gerekir.
- RS line yeni high, correction liderliğinin önemli işaretidir.
- İlk pilot trade çalışmadan exposure büyütülmez.
- Strateji sağlam olsa bile disiplin yoksa sonuç gelmez.

---

## 14. Codex Next Action

### Immediate Task

```text
Create isolated research folder for INTAKE_004 Minervini VCP correction-leader candidate.
Do not modify MTC_V2 Pine.
Do not modify production Python runner.
Do not run backtests or optimization.
Implement detector stubs and unit-test fixtures only for:
1. Market breadth / participation regime
2. Correction leader score
3. RS new high
4. VCP contraction
5. Pivot breakout
6. Progressive exposure state machine
```

### Suggested Codex Prompt

```text
Read INTAKE_004_M_tD6X0CSOI_the_perfect_vcp_trading_setup_mark_minervini.md.
Before making changes, inspect repo registry files for duplicate video_id=M_tD6X0CSOI and transcript_hash=eafb37522f8a4f418558d50601fbb1f6f554dbac164ed8ac8d061ae65114acfb.
If duplicate exists, stop and report duplicate details.
If not duplicate, create an isolated research folder under 06_QUANTLENS_LAB/research/minervini_vcp_004/.
Do not modify 01_PINE/MTC_V2.pine.
Do not modify production Python runner files.
Do not run backtests or optimization.
Implement feature-detector stubs and unit-test fixtures only for market breadth regime, correction leader score, RS new high, VCP contraction, pivot breakout, and progressive exposure state machine.
Prepare README.md with formulas, assumptions, event schema, manual example list, limitations, and next steps.
Also draft a Trader Wiki note for correction leadership, VCP, breadth divergence, and progressive exposure.
```

---

## 15. Files Created / Not Touched

### Created by this intake step

```text
INTAKE_004_M_tD6X0CSOI_the_perfect_vcp_trading_setup_mark_minervini.md
```

### Not touched

```text
01_PINE/MTC_V2.pine
Production Python runner files
Backtest data bundles
Optimization result folders
Broker / webhook / API key files
```

---

## 16. Final Decision

```text
Classification: CANDIDATE
Codex Status: READY_FOR_PYTHON_PROTOTYPE
Candidate Type: VCP correction-leader system + market regime + progressive exposure
Primary Implementation Target: Python research prototype
Pine Implementation: Later, only after detector validation
Registry Update Needed: Yes, after repo duplicate check
Trader Wiki Note: Yes, also recommended
```

Bu transcript, QuantLens için şu anda gelen ilk dört video içinde en değerli candidate'lardan biridir. Özellikle **VCP contraction**, **RS new high**, **correction leader ranking** ve **progressive exposure** birlikte kullanılırsa MTC_V2'nin mevcut SL/TP, position management ve filter yapısıyla ileride güçlü bir research branch oluşturabilir.
