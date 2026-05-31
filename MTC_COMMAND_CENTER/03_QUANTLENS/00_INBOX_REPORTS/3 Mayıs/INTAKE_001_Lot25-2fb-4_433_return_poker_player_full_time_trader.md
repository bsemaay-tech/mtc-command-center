# QuantLens Transcript Intake Report — 001 / 068

## 1. Metadata

- **Report ID:** `INTAKE_001_Lot25-2fb-4`
- **Source URL:** `https://youtu.be/Lot25-2fb-4?si=YHKVb3kJfybusO5o`
- **Normalized URL:** `https://www.youtube.com/watch?v=Lot25-2fb-4`
- **Video ID:** `Lot25-2fb-4`
- **Title:** `433% Return in 1 Year From Poker Player to Full Time Trader`
- **Guest / Main Trader:** Christian Flanders
- **Channel:** `UNKNOWN_CHANNEL`  
  - Transcript includes podcast references, but no reliable channel metadata was provided in the file. Per intake rule, use `UNKNOWN_CHANNEL` when channel info is missing.
- **Source transcript file:** `433% Return in 1 Year From Poker Player to Full Time Trader.md`
- **Prompt file used:** `00_quantlens_transcript_intake_prompt.md`
- **Generated date:** `2026-05-03`
- **Transcript hash method:** lowercase + whitespace-normalized SHA256 over full transcript text
- **Transcript hash:** `d86b69d41ff2b4ad7b546f8965ea13ddf3dbf9b1f39056b5bfa80b1b683c8754`

---

## 2. Intake Verdict

- **Classification:** `CANDIDATE`
- **Codex Status Önerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Candidate Priority:** `P1 — High value, but not direct Pine-first`
- **Usefulness Score:** `9 / 10`
- **Coding Readiness Score:** `7 / 10`
- **MTC_V2 Fit Score:** `7.5 / 10`
- **Wiki Note Also Valuable:** `YES`

### Verdict Summary

Bu video yalnızca trader psikolojisi veya röportaj notu değildir. İçinde kodlanabilir bir strateji adayı vardır: **Episodic Pivot / Opening Range Breakout + Progressive Exposure risk scaling**.

En güçlü uygulanabilir fikir:

> Büyük katalizör sonrası gap yapan, güçlü hacimle açılan, tercihen tüm zamanların zirvesi civarında olan hisseyi ilk 5 dakikalık opening range high üstünde almak; stop’u günün/ilk range’in dibine koymak; pozisyon riskini son performansa göre artırıp azaltmak.

Bu nedenle `WIKI_ONLY` değil, `CANDIDATE` olarak işlenmelidir. Ancak videodaki psikoloji, drawdown kontrolü, trade review, position sizing ve “ne zaman bırakmalı / ne zaman küçülmeli” dersleri ayrıca Trader Wiki’ye de aktarılmaya değerdir.

---

## 3. Duplicate / Registry Check

### Current Environment Check

- `_registry/youtube_video_index.csv` dosyası bu konuşmada verilmedi.
- `channel_blacklist.yaml` dosyası bu konuşmada verilmedi.
- `channel_quality_registry.csv` dosyası bu konuşmada verilmedi.

### Result

- **Duplicate status:** `NOT_VERIFIED_AGAINST_REPO_REGISTRY`
- **Current conversation duplicate:** `NO_DUPLICATE_DETECTED`
- **Action:** Bu rapor için yeni candidate önerisi üretildi; gerçek repo’ya işlenmeden önce Codex’in registry dosyalarını okuyup `video_id` ve `transcript_hash` üzerinden tekrar kontrol etmesi gerekir.

### Registry Row Draft

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,first_seen_at,last_seen_at,process_count
Lot25-2fb-4,https://www.youtube.com/watch?v=Lot25-2fb-4,"433% Return in 1 Year From Poker Player to Full Time Trader",UNKNOWN_CHANNEL,CANDIDATE,CAND_20260503_EP_PROGRESSIVE_EXPOSURE_Lot25_2fb_4,d86b69d41ff2b4ad7b546f8965ea13ddf3dbf9b1f39056b5bfa80b1b683c8754,2026-05-03,2026-05-03,1
```

---

## 4. Channel Quality Check

- **Channel:** `UNKNOWN_CHANNEL`
- **Blacklist decision:** `NO_BLACKLIST_DECISION`
- **Reason:** Kanal adı / kanal id güvenilir şekilde verilmediği için blacklist veya watchlist kararı verilmedi.
- **Suggested quality update after repo check:** Eğer kanal daha önce işlenmemişse `UNKNOWN`; bu video sonucu faydalı olduğu için `candidate_count += 1`.

---

## 5. Strategy Candidate

## Candidate ID

`CAND_20260503_EP_PROGRESSIVE_EXPOSURE_Lot25_2fb_4`

## Candidate Name

**Episodic Pivot Momentum + Progressive Exposure Risk Scaling**

## Strategy Family

- Momentum
- Breakout
- Opening Range Breakout
- Episodic Pivot
- CANSLIM / Minervini-style leadership stock trading
- Adaptive position sizing / anti-martingale exposure control

## Primary Market

- **Best native fit:** US equities
- **Reason:** Setup depends heavily on catalysts, earnings gaps, premarket volume, opening range behavior, all-time-high context, and individual stock leadership.
- **Crypto adaptation:** Possible but secondary. Crypto lacks daily earnings gaps and stock-specific catalysts, so direct transfer to BTC/ETH perpetuals would require a different catalyst/proxy model.

---

## 6. Core Strategy Logic

### 6.1 Primary Setup — Episodic Pivot / Opening Range Breakout

#### Required Conditions

1. **Catalyst / news shock**
   - Earnings surprise, pre-announcement, FDA approval, business deal, sector shock, or comparable high-impact event.
   - If no structured catalyst data exists, proxy with abnormal gap + abnormal volume.

2. **Gap / thrust condition**
   - Stock gaps up materially, ideally `>= 10%`.
   - Premarket or opening volume is unusually high.

3. **Opening range condition**
   - Define first `5m` candle after regular session open.
   - Candidate long trigger: price breaks above first 5m high.
   - Aggressive variant: first `1m` opening range can be tested separately for very high-volume cases.

4. **Stop condition**
   - Initial stop at first 5m low or low of day.
   - Alternative: low of previous day for VCP-style entries before the gap continuation.

5. **Trend / leadership filter**
   - Prefer stocks at, above, or very near all-time highs.
   - Avoid low-quality bottom-fishing “stocks going down”.

6. **Volume behavior**
   - Volume should dry up on pullbacks/declines.
   - Volume should increase on rallies/breakouts.

#### Entry Rule Draft

```text
LONG if:
  regular_session_open is active
  AND gap_up_pct >= gap_threshold
  AND opening_volume_zscore >= volume_threshold
  AND price breaks above opening_range_high
  AND stock is near all-time high or recent 52-week high
  AND market regime is supportive
```

#### Initial Stop Draft

```text
initial_stop = opening_range_low
risk_per_share = entry_price - initial_stop
```

#### Invalid Setup

```text
Reject trade if:
  risk_per_share <= 0
  OR spread/liquidity is poor
  OR gap fades below opening range low before entry
  OR market breadth is extremely extended and failing
```

---

## 7. Secondary Strategy Layer — VCP / Power Play / High Tight Flag

The video also describes a second setup family:

- VCP breakout
- Power play
- High tight flag
- Episodic pivot out of VCP or power play

### Key Conditions

1. Tightening price contractions.
2. Volume dries up during declines.
3. Volume expands on rallies.
4. Price is near all-time high or major high.
5. Breakout through pivot / resistance.
6. Stop near low of day, previous day low, or pattern low depending on setup.

### Coding Difficulty

- **Episodic Pivot ORB:** medium difficulty.
- **VCP pattern detection:** high difficulty.
- **Power Play / High Tight Flag:** medium-high difficulty.

Recommended development order:

1. Build episodic pivot ORB prototype first.
2. Add all-time-high / 52-week-high gate.
3. Add abnormal volume and gap filters.
4. Add progressive exposure sizing.
5. Only after stable results, research VCP / power play pattern detection.

---

## 8. Progressive Exposure / Anti-Martingale Sizing

### Core Idea

- When losing: reduce risk aggressively.
- When winning and account has cushion: increase risk on A+ setups.
- Small losses are acceptable; compounding happens when size is applied to the best setups.

### Position Sizing Draft

```text
base_risk_pct = 0.25% to 0.50%
normal_risk_pct = 0.50% to 1.00%
A_plus_risk_pct = 1.00% to 2.00%

if rolling_drawdown > dd_limit:
    risk_pct = min_risk_pct
elif recent_loss_streak >= loss_streak_limit:
    risk_pct = min_risk_pct
elif month_pnl_pct > cushion_threshold and setup_quality == A_PLUS:
    risk_pct = A_plus_risk_pct
else:
    risk_pct = base_or_normal_risk_pct
```

### Portfolio Guard Draft

```text
if monthly_drawdown_pct <= -max_monthly_dd:
    block_new_entries = true
    allowed_risk_pct = min_risk_pct

if rolling_last_10_trades_win_rate is poor:
    reduce_risk_tier()

if account_equity_new_high and market_regime_good:
    allow_next_risk_tier()
```

### Important

This is not a normal indicator filter. It belongs in **PortfolioState / Position Sizing / Risk Guard** logic, because it depends on realized PnL, drawdown, loss streak, and account cushion.

---

## 9. Exit Logic

### Initial Protective Exit

- Stop at opening range low / low of day.
- If entry is VCP/power play before gap continuation, stop can be previous day low or pattern low.

### Break-even / Risk Reduction

- If breakout fails quickly, reduce size incrementally instead of all-or-nothing exits.
- If price returns to entry after strong initial move, partial exit is acceptable.

### Trailing Exit Candidates

The transcript mentions multiple trailing ideas:

- 10-day moving average
- 20-day moving average
- 50-day moving average for longer position-trading style
- Sell into strength when extension becomes extreme
- Adjust selling rules depending on market condition

### Prototype Exit Order

Recommended first Python prototype:

```text
1. Hard stop at opening_range_low
2. Optional break-even after +1R or +2R
3. Trail using 10 EMA or 20 EMA after trend matures
4. Time stop if no follow-through after N bars/days
5. Optional extension profit-taking when price is excessive ATR multiple above moving average
```

---

## 10. MTC_V2 Mapping

### Signal Producer

`producer_episodic_pivot_orb_v1`

Produces raw long pulse when:

- gap / abnormal move detected
- opening range high breaks
- volume confirms
- ATH / leadership gate passes

### Signal Transform Pipeline

Potential transforms:

- Confirmation: wait for close above opening range high.
- Retest: optional retest of opening range high after breakout.
- No intrabar discretionary entry in parity mode unless deterministic OHLC rules are defined.

### Entry Gates

Recommended gates:

- `ATH_OR_52W_HIGH_GATE`
- `VOLUME_EXPANSION_GATE`
- `MA_TREND_GATE`
- `MARKET_REGIME_GATE`
- `LIQUIDITY_GATE`
- `SPREAD_GATE`
- `SESSION_GATE_US_RTH`
- `BREADTH_NOT_OVERHEATED_GATE`

### Position Manager

- Allow long entries only for first prototype.
- No shorting in v1.
- Use cooldown to avoid repeated failed ORB attempts.
- Prevent same-bar re-entry after stop.

### Position Sizing

Add a portfolio-aware sizing layer:

- risk tier based on monthly PnL cushion
- reduce tier after loss streak
- reduce tier in drawdown
- A+ setup cap
- max gross exposure cap

### Exit Rules

MTC_V2 can reuse:

- initial SL
- BE
- trailing stop
- time stop
- partial exit logic if available

### Pine Timing Warning

This strategy is sensitive to session open and intraday candles. Pine implementation should come later. First validate deterministic Python logic using intraday equity data.

---

## 11. Data Requirements

### Required for Proper Backtest

- US equity daily OHLCV
- US equity intraday 1m or 5m OHLCV
- Adjusted prices / split handling
- Regular session open time
- Premarket gap data if available
- Liquidity / dollar volume
- 52-week high or all-time high series
- Market index regime data: SPY / QQQ
- Breadth proxy if available
- Optional catalyst data: earnings calendar, news, FDA, guidance, upgrades

### Minimum Feasible Prototype Without Catalyst Data

If no news/catalyst feed exists:

```text
proxy_catalyst = gap_up_pct >= 10% AND first_5m_volume >= X times average_5m_volume
```

This is weaker than true catalyst tagging but enough for first research.

---

## 12. Backtest Risks / False Positives

### Major Risks

1. **Survivorship bias**
   - Studying only big winners like NVDA / SMCI can inflate expectations.

2. **Lookahead bias**
   - All-time-high and catalyst data must be computed only as of the trade date.

3. **Catalyst ambiguity**
   - Without news/earnings labels, gap filters may include low-quality pump moves.

4. **Slippage and opening volatility**
   - Opening range breakouts can have severe slippage.

5. **Liquidity constraints**
   - Large position sizing must be capped by dollar volume and spread.

6. **Overfitting to bull markets**
   - This strategy likely works best during strong equity momentum regimes.

7. **Crypto transfer risk**
   - Direct crypto transfer is not guaranteed because equities have earnings gaps and session opens.

---

## 13. Python Prototype Plan

### Phase 1 — Research Dataset

- Build small equity dataset first.
- Use known momentum names plus broad universe sample.
- Include delisted names if possible.

### Phase 2 — Signal Definition

Implement:

```text
opening_range_high_5m
opening_range_low_5m
gap_up_pct
relative_volume
near_52w_high
near_ath
market_regime
```

### Phase 3 — Trade Simulation

- Entry at breakout above opening range high.
- Stop at opening range low.
- Position size by fixed risk first.
- Then add progressive exposure.

### Phase 4 — Scoring

Score by:

- CAGR
- max drawdown
- profit factor
- expectancy in R
- average R
- median R
- tail winners contribution
- drawdown recovery time
- performance by market regime

### Phase 5 — Robustness

- Test across years.
- Test across market regimes.
- Test gap thresholds: 5%, 7.5%, 10%, 15%.
- Test opening range: 1m, 5m, 15m.
- Test stop variants.
- Test fixed risk vs progressive exposure.

---

## 14. Trader Wiki Extraction

Even though this is a candidate, it should also produce a Trader Wiki note.

### Suggested Wiki Path

`11_TRADER_WIKI/01_RISK_MANAGEMENT/TW_2026-05-03_PROGRESSIVE_EXPOSURE_433_RETURN_POKER_TO_TRADER.md`

### Wiki Topics

- Progressive exposure
- Anti-martingale sizing
- Drawdown control
- Trading psychology
- Quitting / stopping after poor performance
- A+ setup sizing
- Learning from trade review
- Avoiding revenge trading
- Stop discipline

### Key Lessons

1. Do not trade the same size in all market regimes.
2. Increase size only when there is account cushion and setup quality is high.
3. Cut size quickly during drawdown.
4. Every repeated mistake eventually becomes expensive.
5. Trade review is required to identify which setups deserve size.
6. Stop losses are non-negotiable.
7. Holding big winners is psychologically difficult and should be systematized.

---

## 15. Risky / Suspicious Claims

- The headline return `433%` is extraordinary and should not be treated as normal expectancy.
- NVDA / SMCI examples are exceptional outlier leaders; the strategy may depend on rare market conditions.
- “Buy stocks going up” is valid as a philosophy but insufficient as a complete quantitative rule without regime, liquidity, entry, stop, and sizing constraints.
- Aggressive exposure such as 100%+ account allocation is unsuitable without strict liquidity, leverage, and risk caps.
- Trading for a living is explicitly described as very difficult; do not infer beginner suitability.

---

## 16. Files / Repo Actions

### Files Created in This Chat

- `INTAKE_001_Lot25-2fb-4_433_return_poker_player_full_time_trader.md`

### Files Not Modified

- `01_PINE/MTC_V2.pine`
- Production Python runner files
- Backtest result files
- Optimization result files
- `_registry/youtube_video_index.csv`
- `channel_blacklist.yaml`
- `channel_quality_registry.csv`

### Recommended Repo Actions for Codex Later

1. Check registry for `video_id = Lot25-2fb-4`.
2. Check registry for transcript hash duplicate.
3. If not duplicate, create candidate folder.
4. Add candidate metadata only; do not modify MTC_V2 yet.
5. Create a research issue/plan for `producer_episodic_pivot_orb_v1`.
6. Create separate Trader Wiki note for progressive exposure.

---

## 17. Final Decision

```text
Classification: CANDIDATE
Codex Status: READY_FOR_PYTHON_PROTOTYPE
Primary Candidate: Episodic Pivot Momentum + Progressive Exposure Risk Scaling
Secondary Value: Trader Wiki note for risk management and psychology
Pine Now: NO
Python Prototype First: YES
Backtest Now: NO, only after candidate spec and dataset plan are created
MTC_V2 Direct Patch: NO
```

