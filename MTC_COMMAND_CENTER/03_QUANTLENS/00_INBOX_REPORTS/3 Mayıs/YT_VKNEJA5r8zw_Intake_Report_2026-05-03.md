# YouTube Strategy Intake Report — VKNEJA5r8zw

## 1. Metadata

- **Report Date:** 2026-05-03
- **Source URL Provided:** https://youtu.be/VKNEJA5r8zw?si=292-FpdSVMBtGpva
- **Normalized URL:** https://www.youtube.com/watch?v=VKNEJA5r8zw
- **Video ID:** `VKNEJA5r8zw`
- **Transcript File:** `/mnt/data/+969% Return in 1 Year The Pullback Strategy of a Trading Champion.md`
- **Transcript Normalized SHA256:** `337688e922fa15deede83a6e89fd19b40e7f6ab1a79e08803f2d439ffc7e5032`
- **Title From File:** `+969% Return in 1 Year The Pullback Strategy of a Trading Champion`
- **Featured Trader / Speaker:** Martin Luke
- **Podcast / Host Mentioned:** Richard Moglen / TraderLion-style podcast context
- **Channel:** `UNKNOWN_CHANNEL`
  - Transcript mentions the podcast context, but does not provide a reliable channel ID.
  - Per intake rule, exact channel-level blacklist decision should not be made without channel registry data.
- **Language / Transcript Quality:** English transcript with Turkish timestamp text; usable, but contains OCR/transcription artifacts.
- **Video Length From Transcript:** approximately 4h 09m
- **Primary Topic:** Pullback trend-following strategy, tight stops, low win-rate/high-R approach, AVWAP/EMA support entries, market feedback and overtrading control.

---

## 2. Intake Decision

- **Classification:** `CANDIDATE`
- **Codex Status Suggestion:** `READY_FOR_PYTHON_PROTOTYPE`
- **Pine Implementation Now:** `NO`
- **Trader Wiki Note:** `YES_AS_SECONDARY_NOTE`
- **Candidate Priority:** `HIGH`
- **Usefulness Score:** `9/10`
- **Reason:** The transcript contains repeatable and partially codable trading rules: pullback entries into EMA/AVWAP/support, tight stop placement, risk-per-trade sizing, low win-rate/high-R math, market-condition adaptation, partial profit-taking, and explicit bad-trade filters.

This should not go directly into Pine. First step should be a Python research prototype and manual/semiautomatic labeling against historical intraday + daily data. The rules depend heavily on market regime, intraday opening behavior, and discretionary quality filters, so a naive Pine conversion would likely overfit or misrepresent the strategy.

---

## 3. Duplicate / Registry Status

### Current Conversation Check

- Previous processed video in this conversation: `q43pkYBo1hU`
- Current video: `VKNEJA5r8zw`
- Current transcript hash prefix: `337688e922fa15de`
- Result: `NOT_DUPLICATE_IN_CURRENT_BATCH`

### Repo Registry Check

- `_registry/youtube_video_index.csv`: **not accessible in this ChatGPT environment**
- `channel_blacklist.yaml`: **not accessible in this ChatGPT environment**
- `channel_quality_registry.csv`: **not accessible in this ChatGPT environment**

### Required Codex Repo Action

Before creating a repo candidate folder, Codex must check:

```text
_registry/youtube_video_index.csv
channel_blacklist.yaml
channel_quality_registry.csv
```

If `video_id = VKNEJA5r8zw` or matching `transcript_hash = 337688e922fa15deede83a6e89fd19b40e7f6ab1a79e08803f2d439ffc7e5032` already exists, Codex must stop and report duplicate instead of creating a new candidate.

---

## 4. Channel Quality Decision

- **Channel State:** `UNKNOWN`
- **Reason:** Exact channel ID is not provided in transcript file.
- **Blacklist Decision:** `NO_BLACKLIST_DECISION`
- **Watchlist Decision:** `NO_WATCHLIST_DECISION`
- **Quality Signal:** Positive at content level. This is a long-form interview with a trading champion and includes many operational details.

Suggested registry update if repo checks pass:

```csv
video_id,normalized_url,status,codex_status,channel,transcript_hash,first_seen_at,last_seen_at,process_count
VKNEJA5r8zw,https://www.youtube.com/watch?v=VKNEJA5r8zw,CANDIDATE,READY_FOR_PYTHON_PROTOTYPE,UNKNOWN_CHANNEL,337688e922fa15deede83a6e89fd19b40e7f6ab1a79e08803f2d439ffc7e5032,2026-05-03,2026-05-03,1
```

---

## 5. Executive Summary

The video describes Martin Luke's pullback-focused swing trading approach after a very high-return US Investing Championship year. The key idea is not buying random breakouts, but waiting for strong stocks or themes to pull back into support areas and then entering with very tight risk.

Core elements:

1. **Trend-following base:** Trade names already showing strength, preferably in active/hot sectors.
2. **Pullback entry:** Prefer entries near daily/intraday support instead of chasing breakout extension.
3. **EMA structure:** Use 9/21/50/150 EMAs across multiple timeframes.
4. **Anchored VWAP:** Use AVWAP as a contextual support/resistance tool.
5. **Tight stop:** Mostly under 2.5% to 3%; often low of day or entry candle low.
6. **Risk sizing:** Around 0.5% portfolio risk per trade on average.
7. **Position size:** Often 25% to 30% position size; smaller for microcaps due to gap risk.
8. **Exit logic:** Sell partials into strength at approximately 3R to 5R, or trail if market/portfolio cushion is strong.
9. **Market feedback:** Trade more when pullbacks are working; trade less in choppy conditions.
10. **Mistake filter:** Avoid revenge trading, long/short flipping, shorting too aggressively when broad market is still strong, and taking subpar hourly-only pullbacks.

This is one of the more promising transcripts so far because it includes both a codable setup and the failure conditions.

---

## 6. Strategy Candidate

### Candidate ID

```text
YT_CAND_2026_05_03_VKNEJA5r8zw_PULLBACK_AVWAP_TIGHT_STOP
```

### Candidate Name

```text
Pullback AVWAP Tight-Stop Trend Strategy
```

### Strategy Family

- Swing trading
- Trend following
- Pullback continuation
- Intraday reversal after early shakeout
- Tight-stop / low-win-rate / high-R system

### Direction

- Primary: `LONG`
- Secondary: `SHORT`
- Short side should be researched later because the transcript reports overtrading and bad short-side behavior during the December drawdown.
- First Python prototype should focus on long-side rules only.

---

## 7. Extracted Trading Logic

### 7.1 Universe Filter

Preferred universe:

- US stocks and ETFs.
- Fast-moving stocks.
- Stocks in active/hot sectors.
- High dollar volume.
- Names moving with a theme or group.
- Avoid oversized positions in microcaps due to gap-down / short-report risk.
- ETFs may be used for market tests or extreme reversal trades.

Possible codable universe filters:

```text
price >= configurable_min_price
avg_dollar_volume >= configurable_min_adv
atr_pct >= configurable_min_atr_pct
sector/theme momentum proxy >= threshold
exclude_microcap_if_gap_risk_filter_enabled
```

### 7.2 Market Regime Filter

The method works best when the market rewards pullbacks. Transcript examples point to:

- QQQ or broad market riding rising 9 EMA / 21 EMA.
- IWM relative strength can invalidate aggressive broad-market shorting.
- Breadth improving supports adding exposure.
- Choppy markets require fewer trades, not earlier profit-taking.

Prototype market filter ideas:

```text
market_close > EMA_21
EMA_9 > EMA_21 or EMA_21 rising
market_breadth_proxy improving
avoid_new_trades_if_recent_strategy_feedback_negative
avoid_new_trades_if index chopping around flat EMA_9/EMA_21
```

### 7.3 Long Setup A — Daily EMA Pullback Continuation

Core idea:

1. Stock is in an uptrend.
2. It pulls back into daily 9 EMA or 21 EMA.
3. It holds support or reclaims after shakeout.
4. Entry happens near support, not after extension.
5. Stop is tight under low of day / entry candle / support.

Possible rules:

```text
trend_ok =
    close > EMA_50
    AND EMA_9 > EMA_21
    AND EMA_21 > EMA_50 or EMA_50 rising

pullback_ok =
    low <= EMA_9 * (1 + touch_tolerance)
    OR low <= EMA_21 * (1 + touch_tolerance)
    OR low <= AVWAP * (1 + touch_tolerance)

reversal_ok =
    close > open
    OR close > prior_bar_high on intraday trigger
    OR price reclaims opening range high after early undercut

entry =
    next bar open / close after confirmation
```

### 7.4 Long Setup B — Opening Shakeout Reclaim

Observed behavior in transcript:

- A stock gaps up or opens strong.
- It gets slammed in first 30 to 60 minutes.
- It takes out low of day or opening range breakout traders.
- It later finds support and reclaims opening range high.
- Entry can be a one-minute reversal / opening-range-high reclaim / intraday breakout.

Prototype intraday trigger:

```text
premarket_or_open_strength = gap_up OR opening_range_strength

shakeout =
    first_30_to_60_min_low < opening_range_low
    AND price touches/reclaims intraday EMA/VWAP/support

reclaim =
    price closes above opening_range_high
    OR price breaks intraday consolidation high after reclaim

stop =
    low_of_day
    OR entry_candle_low

reject entry if:
    entry_price > low_of_day * 1.03
```

The transcript explicitly says he avoids entries more than about 3% above low of day or ideal entry point. This is valuable because it prevents chasing.

### 7.5 Long Setup C — Extreme ETF / Parabolic Reversal

Special case:

- Market/index is extremely stretched below a short-term EMA after panic.
- Example: around 20% below 1-hour EMA in the intro description.
- Entry at reversal or opening-range reclaim.
- Exit into strength quickly due to huge volatility.

This should be a separate prototype, not mixed with the normal pullback system.

Candidate name:

```text
TQQQ_PANIC_REVERSAL_1H_EMA_EXTENSION
```

Suggested status:

```text
SALVAGE_AS_SEPARATE_EXPERIMENT
```

### 7.6 Short Setup — Pullback Into Resistance

The transcript says short-side pullbacks are conceptually similar:

- Short at resistance.
- Use declining EMA / AVWAP / resistance level.
- Avoid shorting merely because small caps are weak if broad market remains strong.
- Avoid hourly-only weak setups when daily structure does not confirm.

For initial QuantLens/MTC work, keep this as future research. Do not combine long and short in first pass.

---

## 8. Exit and Position Management Logic

### 8.1 Initial Stop

Common stop sources:

```text
low_of_day
entry_candle_low
support_low
below AVWAP / EMA support with small buffer
```

Hard risk constraints:

```text
stop_pct <= 3.0%
preferred_stop_pct <= 2.5%
absolute_max_stop_pct <= 5.0%
risk_per_trade ~= 0.5% of portfolio equity
```

### 8.2 Position Sizing

Transcript sizing model:

```text
position_notional_pct = risk_per_trade_pct / stop_distance_pct
```

Example:

```text
risk_per_trade = 0.5%
stop_distance = 2.0%
position_size = 25% of portfolio
```

Suggested Python prototype sizing:

```python
risk_cash = equity * risk_pct
stop_distance = abs(entry - stop)
shares = floor(risk_cash / stop_distance)
notional = shares * entry
notional_pct = notional / equity
```

Safety caps:

```text
max_position_notional_pct = 30% default
microcap_max_position_notional_pct = 20%
max_total_exposure_pct = 100% for first prototype
margin_enabled = false for first prototype
```

The transcript discusses exposure up to about 280%, but this must not be used in the first systematic prototype. Margin should only be tested after the base signal has robust expectancy.

### 8.3 Profit Taking

Transcript exit behavior:

- Sell partials into strength around 3R to 5R.
- Sometimes do not take partials if market is strong and existing portfolio cushion is large.
- Sometimes trail the whole position.
- In fast panic-reversal trades, close quickly into strength.

Prototype exit variations:

```text
Variant A:
    TP1 at 3R, sell 50%
    trail remaining by EMA_9 or swing low

Variant B:
    TP1 at 5R, sell 50%
    trail remaining by EMA_9 or low of prior 2 bars

Variant C:
    no fixed TP
    exit on close below EMA_9 / EMA_21 / swing low

Variant D:
    fast reversal mode:
        sell all at 8R-13R or end-of-day, whichever first
```

### 8.4 Bad-Trade Guardrails

From December drawdown analysis:

```text
do_not_flip_long_short_same_day_after_losses
do_not_trade_more_when market_feedback_negative
do_not_short_hourly_pullback_without_daily_confirmation
do_not_enter_if_price_more_than_3pct_above_low_of_day
do_not_overweight small/microcap weakness as broad-market bearish signal
reduce trades in choppy market
```

These are highly useful for MTC_V2 as guards rather than entry rules.

---

## 9. MTC_V2 Mapping

### Reusable Existing MTC_V2 Components

Likely reusable:

- Position sizing with risk percentage.
- SL calculation and initial stop placement.
- TP / partial exit logic.
- Break-even and trailing stop modules.
- Entry gates:
  - MA / EMA gate.
  - HTF trend gate.
  - ATR volatility floor.
  - Volume / dollar-volume gate.
  - Session gate.
  - Level proximity gate.
- Portfolio guards:
  - max entries.
  - cooldown bars.
  - regime lock.
  - recovery after losses.
- Exit-first canonical rule.

### New/Extended Research Components Needed

```text
producer_pullback_avwap_v1
intraday_opening_shakeout_detector_v1
avwap_support_proximity_gate_v1
market_feedback_guard_v1
anti_overtrade_flip_guard_v1
entry_chase_distance_guard_v1
theme_strength_proxy_v1
```

### Pine Timing Warning

This video uses multi-timeframe and intraday behavior. Do not implement first in Pine because:

- AVWAP anchor selection can become ambiguous.
- Opening range / low-of-day behavior is intraday-dependent.
- Daily + intraday parity requires careful synchronization.
- Stop entries and same-bar behavior can diverge between Pine and Python.
- Tight stops make parity errors very costly.

---

## 10. Python Prototype Plan

### Phase 1 — Data Requirements

Minimum data:

```text
1m or 5m OHLCV for US stocks / ETFs
daily OHLCV for same tickers
market proxy: QQQ, SPY, IWM
sector/theme proxy if available
earnings/news calendar optional for later
```

### Phase 2 — Indicators

Calculate:

```text
EMA_9, EMA_21, EMA_50, EMA_150 on daily and intraday
dollar_volume = close * volume
ATR and ATR%
opening range high/low
low of day
anchored VWAP variants:
    AVWAP from earnings gap
    AVWAP from swing low
    AVWAP from recent major high/low
```

### Phase 3 — Long Pullback Prototype

Start with daily pullback only:

```text
entry:
    daily trend_ok
    pullback touches EMA_9/EMA_21/AVWAP/support
    intraday reclaim trigger
    entry distance from low_of_day <= 3%

stop:
    min(low_of_day, entry_candle_low) minus buffer

sizing:
    risk_per_trade = 0.5%
    max_position = 30%
    no margin

exit:
    50% at 3R or 5R
    trailing remainder by EMA_9 / swing low
```

### Phase 4 — Strategy Variants

Run separately:

```text
A. daily EMA9 pullback
B. daily EMA21 pullback
C. AVWAP pullback
D. opening shakeout reclaim
E. extreme ETF reversal
```

Do not mix all conditions initially. Each setup needs separate expectancy.

### Phase 5 — Robustness Checks

```text
in-sample / out-of-sample split
bull / bear / choppy regime split
large-cap vs small-cap split
high dollar-volume vs low dollar-volume split
gap-up vs non-gap-up split
stop distance buckets: 1.0%, 1.5%, 2.0%, 2.5%, 3.0%
TP buckets: 3R, 5R, trailing-only
```

### Phase 6 — Failure Analysis

Specifically analyze:

```text
false support touches
support chop
entry too far from low of day
post-gap failure
same-day long/short flipping
loss streak behavior
December-style overtrading simulation
```

---

## 11. Candidate Expected Edge Hypothesis

Primary hypothesis:

```text
Strong stocks in strong themes that pull back into rising EMA/AVWAP support and reclaim intraday structure produce asymmetric R-multiple opportunities when entered near low-of-day with tight stops.
```

Secondary hypothesis:

```text
The strategy's edge is not high win rate. The edge comes from tight invalidation, strong R-multiple outliers, and avoiding choppy-market overtrading.
```

Key success metric should not only be win rate. Use:

```text
expectancy_per_trade_R
median_loss_R
tail_winner_R
profit_factor
max_drawdown
drawdown_duration
trade_count during choppy regimes
R contribution by top 5% winners
```

---

## 12. Risk / Suspicious Claim Review

### High-Risk Elements

- 969% annual return is extraordinary and should not be treated as normal or repeatable.
- Very tight stops can create many small losses and behavioral slippage.
- Low win-rate systems can be psychologically hard to execute.
- Margin up to ~280% exposure is unsuitable for first systematic prototype.
- Pullback behavior is regime-dependent and may fail in choppy or distribution markets.
- Manual AVWAP anchor choice can introduce lookahead bias if not explicitly defined.

### Research Risks

- Overfitting to 2025 market behavior.
- Survivorship bias if only popular winners are tested.
- Lookahead bias in theme/leader selection.
- Intraday data quality issues.
- Same-bar stop/target ambiguity.
- Gap-down risk not represented correctly if only regular-session intraday data is used.

---

## 13. Classification Rationale

### Why Not `STOP`

The transcript is not purely motivational and not empty. It contains detailed trading rules, setups, risk management, and failure modes.

### Why Not `REJECT`

The video is long but useful. It provides enough concrete material for prototype extraction.

### Why Not `WIKI_ONLY`

There is codable strategy logic:

- EMA pullback.
- AVWAP pullback.
- opening range reclaim.
- stop placement.
- R-based partial exits.
- risk sizing.
- anti-chase filter.
- overtrading guards.

Therefore it should be a candidate, with secondary wiki notes.

### Why `CANDIDATE`

The system has clear strategy components that can be modeled and tested in Python before any Pine conversion.

---

## 14. Suggested Repo Output Paths

If Codex registry checks pass, suggested folder:

```text
YOUTUBE_STRATEGY_INTAKE/candidates/YT_CAND_2026_05_03_VKNEJA5r8zw_PULLBACK_AVWAP_TIGHT_STOP/
```

Suggested files:

```text
README.md
intake_report.md
source_metadata.yaml
strategy_spec.md
research_questions.md
python_prototype_plan.md
mtc_v2_mapping.md
risk_notes.md
transcript_excerpt_index.md
```

Suggested wiki note:

```text
YOUTUBE_STRATEGY_INTAKE/11_TRADER_WIKI/05_BACKTESTING_AND_OPTIMIZATION/TW_2026-05-03_PULLBACK_TIGHT_STOPS_MARTIN_LUKE.md
```

---

## 15. Codex Next Action

### Immediate Next Action

```text
1. Check repo registry duplicate status.
2. If not duplicate, create candidate folder.
3. Save this report as intake_report.md.
4. Save raw transcript reference path.
5. Create strategy_spec.md from Section 7 and Section 8.
6. Create python_prototype_plan.md from Section 10.
7. Do not modify 01_PINE/MTC_V2.pine.
8. Do not modify production Python runner.
9. Do not run backtest or optimization yet.
```

### Research Priority

```text
Priority 1:
Daily EMA9/EMA21 pullback long prototype with low-of-day stop and 3R/5R partial exits.

Priority 2:
Opening shakeout reclaim prototype.

Priority 3:
AVWAP support pullback prototype.

Priority 4:
Market feedback / anti-overtrading guard.

Priority 5:
Short-side resistance pullback prototype.
```

---

## 16. Files Created / Not Modified

### Created by this ChatGPT step

```text
/mnt/data/YT_VKNEJA5r8zw_Intake_Report_2026-05-03.md
```

### Not modified

```text
01_PINE/MTC_V2.pine
Production Python runner files
Backtest data folders
Optimization result folders
Repo registries
Secrets / API keys / broker settings
```

---

## 17. Final Verdict

```text
VERDICT: CANDIDATE
CODEX_STATUS: READY_FOR_PYTHON_PROTOTYPE
PINE_NOW: NO
PRIMARY_SETUP: LONG_PULLBACK_EMA_AVWAP_TIGHT_STOP
SECONDARY_SETUP: OPENING_SHAKEOUT_RECLAIM
RESEARCH_VALUE: HIGH
RISK_LEVEL: HIGH_DUE_TO_TIGHT_STOPS_AND_MARGIN_DISCUSSION
NEXT_ACTION: CREATE_RESEARCH_CANDIDATE_AFTER_REPO_DUPLICATE_CHECK
```
