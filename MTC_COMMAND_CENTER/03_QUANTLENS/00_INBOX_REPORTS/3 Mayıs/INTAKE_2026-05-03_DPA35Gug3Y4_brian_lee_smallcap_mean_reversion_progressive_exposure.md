# QuantLens Transcript Intake Report

## 1. Metadata

- **Intake ID:** `INTAKE_2026-05-03_DPA35Gug3Y4`
- **Source URL:** `https://youtu.be/DPA35Gug3Y4?si=tgHSwpjijUJECVZU`
- **Normalized URL:** `https://www.youtube.com/watch?v=DPA35Gug3Y4`
- **Video ID:** `DPA35Gug3Y4`
- **Title:** `Gamer Trades $5k into over $1 Million with just a 30% Win Rate - Brian Lee Trades`
- **Primary Person / Speaker:** Brian Lee
- **Channel:** `TraderLion / TraderLion Podcast` *(inferred from transcript text; exact channel registry not available in this intake environment)*
- **Transcript File:** `Gamer Trades $5k into over $1 Million with just a 30% Win Rate - Brian Lee Trades.md`
- **Generated At:** `2026-05-03`
- **Transcript Hash SHA256:** `65842d19d3ef431e28c238bdd2b68a1518f019a25d2497b23c2f96e9dedd9133`

---

## 2. Duplicate / Registry Check

### Available Check Scope

This intake was checked only against the transcript files currently available in this conversation/session:

- `_AAX1ylNbIE` — `10 Lessons from Market Wizards & Trading Legends`
- `RTHRh_GLwH8` — `100% Trading Returns - How to become a Super Trade with Mark Ritchie`
- `kao-hhaQnig` — `103% Return in 1 Year The Simple Event Driven Trading Setup`
- `DPA35Gug3Y4` — current transcript

### Result

- **Duplicate by video_id:** No duplicate found in currently available prior files.
- **Duplicate by transcript hash:** No duplicate found in currently available prior files.
- **Registry file `_registry/youtube_video_index.csv`:** Not available here, so repo-level duplicate check could not be completed.
- **Final duplicate status:** `NOT_DUPLICATE_WITHIN_AVAILABLE_CONTEXT`

---

## 3. Channel Quality / Blacklist Check

### Available Check Scope

Repo files were not available:

- `channel_blacklist.yaml` not available.
- `channel_quality_registry.csv` not available.

### Session-Level Observation

Within the available session, the TraderLion-style interview transcripts processed so far have produced useful `CANDIDATE` outputs. If these are all from the same channel, the session-level quality state would lean:

```text
GOOD_WITHIN_AVAILABLE_CONTEXT
```

This is **not** a registry write. It is only an intake observation.

---

## 4. Classification

- **Verdict:** `CANDIDATE`
- **Codex Status Suggestion:** `READY_FOR_PYTHON_PROTOTYPE`
- **Strategy Candidate Type:** Short-side small-cap parabolic gap mean-reversion with progressive exposure
- **Wiki Value:** High, especially risk management / drawdown control / volatility tax.
- **Usefulness Score:** `8.5 / 10`
- **Confidence:** `MEDIUM_HIGH`
- **Implementation Risk:** `HIGH`
- **Reason for High Implementation Risk:** The edge depends on intraday liquidity, short availability, borrow/locate constraints, halts, hard-to-borrow fees, SSR behavior, news/filing context, and realistic slippage modelling. These must be modelled before trusting any backtest.

### Why Not WIKI_ONLY?

This transcript contains strong psychology and risk-management lessons, but it also contains a codable trade framework:

- pre-market / intraday large gap detection;
- small-cap / parabolic extension filtering;
- four-pillar filter: technicals, fundamentals, news, cycle;
- short-side mean-reversion bias;
- no blind shorting into a parabolic move;
- first supply / failed bounce / lower-high confirmation;
- progressive exposure into winners only;
- R-based sizing;
- volatility-tax-aware drawdown controls;
- max ticker / daily risk concepts;
- systematic cover signals.

Therefore the correct classification is `CANDIDATE`, not `WIKI_ONLY`.

---

## 5. Executive Summary

This video is materially different from the first three intake files.

The first three were mainly long-side momentum / breakout / event-driven candidates. This one is primarily a **short-side intraday mean-reversion strategy** focused on highly extended small-cap gap runners.

The core idea is:

```text
Small-cap stock gaps up aggressively
+ volume/liquidity is high enough
+ move is parabolic / extended
+ fundamentals/news do not justify durable repricing
+ market cycle shows speculative crowd behavior
+ price shows first real supply / failed bounce / lower high
= initiate short starter

If the trade starts working:
    add progressively to the winner
    never add to the loser
    cover into logical downside targets / momentum exhaustion / time risk
```

The strongest research value for QuantLens is **not** simply “short big gap-ups.” The edge is the combination of:

1. extension;
2. weak or dilutive fundamentals;
3. noisy / low-quality catalyst;
4. crowd psychology;
5. delayed entry until supply appears;
6. progressive exposure only after price confirms.

This can be researched in Python first as a separate “short mean-reversion lab” before any Pine or MTC production integration.

---

## 6. Main Strategy Candidate

# Candidate: Small-Cap Parabolic Gap Mean-Reversion Short

## 6.1 Core Thesis

Small-cap stocks that gap up 20% to 300%+ on speculative news often overshoot fair value intraday. If the catalyst is weak, dilution risk is present, or the move is driven by crowd / squeeze mechanics rather than durable institutional repricing, the stock can mean-revert sharply after the first supply signal appears.

The trader does **not** short blindly into the vertical move. The preferred sequence is:

```text
Gap / parabolic extension
→ evaluate four pillars
→ wait for pullback / failed bounce / lower high
→ starter short
→ add only if structure confirms
→ cover at predefined levels or exhaustion
```

## 6.2 Strategy Direction

- **Primary direction:** Short.
- **Secondary long-side insight:** The same universe can produce momentum opportunities, but this candidate should be isolated as a short mean-reversion module first.
- **Holding period:** Intraday, typically several hours. Occasional swing for a few days is mentioned, but the main strategy should be prototyped intraday first.
- **Best market:** Highly active small-cap speculation cycles with enough volume/liquidity.

---

## 7. Setup Archetype

## 7.1 Universe Filter

Potential universe:

```text
US small-cap equities
+ large pre-market or intraday gap
+ high relative volume
+ tradable liquidity
+ shorting/borrow data available
```

Initial research filters:

```text
gap_pct >= 20%
premarket_or_intraday_relative_volume >= threshold
dollar_volume >= threshold
price >= minimum_price
float <= optional_smallcap_float_limit
borrow_available == true  # if data exists
halt_risk_flag tracked separately
```

Important: this strategy cannot be validated properly without realistic borrow/locate and slippage assumptions.

---

## 7.2 Four-Pillar Filter

Brian Lee describes a four-pillar analysis process. For QuantLens, convert this into a scoring matrix.

### Pillar 1 — Technicals

Look for:

- parabolic extension;
- very large gap;
- prior daily/weekly resistance;
- prior pivot levels;
- moving averages;
- higher-timeframe extension indicators;
- gap-fill potential;
- failed bounce / lower-high structure;
- momentum snap.

Possible scoring:

```text
technical_score =
    gap_score
  + extension_score
  + resistance_proximity_score
  + htf_overextension_score
  + failed_bounce_score
```

### Pillar 2 — Fundamentals

Look for weakness or dilution-prone structure:

- dilution / offerings;
- weak balance sheet;
- bankruptcy / delinquency / going-concern risk;
- biotech cash-burn structure;
- no durable revenue / product;
- prior reverse splits;
- low-quality fundamentals.

Possible scoring:

```text
fundamental_short_score =
    dilution_risk
  + cash_burn_risk
  + weak_balance_sheet
  + low_revenue_quality
  + prior_financing_pattern
```

### Pillar 3 — News / Catalyst

Categorize the catalyst:

- press release;
- FDA / biotech trial headline;
- contract / partnership;
- merger/acquisition;
- sympathy theme;
- sector hype;
- social-media/speculative theme.

Important distinction:

```text
High-quality catalyst:
    large durable monetary impact
    acquisition / merger
    major approval
    credible revenue transformation

Low-quality catalyst:
    vague PR
    non-binding partnership
    small contract
    repeated promotional headline
    no clear monetary impact
```

Short setups are stronger when the price reaction is extreme but the news quality is weak.

### Pillar 4 — Cycle / Market Psychology

Look for:

- small-cap mania;
- repeated 300% to 500% runners;
- crowded momentum participation;
- short-squeeze environment;
- traders buying at any cost;
- broad risk-on / risk-off context.

This pillar should control aggressiveness, not just entry.

Example:

```text
if smallcap_mania_score is high:
    avoid early blind shorts
    require stronger confirmation
    reduce starter size
    allow wider parabolic extension before entry
```

---

## 8. Entry Model

## 8.1 Do Not Short Blindly

A key rule:

```text
Never short a stock only because it is up a lot.
```

The system should wait for at least minimal supply.

Minimum entry confirmation candidates:

```text
A. first meaningful pullback after parabolic extension
B. failed bounce after first pullback
C. lower high after failed bounce
D. break of intraday VWAP / key support
E. momentum snap after exhaustion candle
F. failed reclaim of prior high
```

## 8.2 Starter / Confirmation / Add Ladder

The transcript suggests staged exposure:

```text
starter signal
→ confirmation signal
→ add signal
→ additional add signal
→ cover signal
```

Prototype interpretation:

### Starter Short

```text
entry_1 =
    universe_filter_passed
    AND four_pillar_score >= threshold
    AND first_supply_detected
```

### Confirmation Add

```text
entry_2 =
    position_open
    AND price_below_entry_1
    AND lower_high_confirmed
    AND unrealized_R >= small_positive_threshold
```

### Additional Add

```text
entry_3 =
    position_open
    AND trend_down_intraday
    AND failed_reclaim_of_vwap_or_pivot
    AND position_risk_after_add <= max_ticker_risk
```

### Hard Rule

```text
Never add to losing short.
Only add when the trade is working.
```

---

## 9. Exit / Cover Model

The transcript gives several cover concepts:

- lagging moving averages;
- prior pivot levels;
- previous high / previous close;
- breakout levels;
- existing gaps;
- intraday pivot levels;
- SSR / short-sale restriction considerations;
- time of day;
- partial retracement expectations;
- momentum exhaustion;
- close-risk behavior.

Prototype cover targets:

```text
target_1 = prior_close
target_2 = intraday_pivot
target_3 = gap_fill_zone
target_4 = major_moving_average
target_5 = fixed_R_target
target_6 = time_stop_before_close
```

Suggested initial exit hierarchy:

```text
1. Protective stop / invalidation first.
2. Partial cover at 2R or first major pivot.
3. Additional cover at prior close / gap-fill area.
4. Exit if downside momentum stalls and reclaim occurs.
5. Mandatory flatten before close in first prototype.
```

---

## 10. Risk Management Model

## 10.1 R-Based Sizing

The transcript strongly emphasizes R-multiple thinking:

```text
1R = predefined account-risk amount for the trade.
```

Suggested prototype parameters:

```text
risk_per_trade_pct = 0.25% to 1.00%  # start conservative in backtest
max_risk_per_ticker_R = 4R
max_daily_loss_R = 6R to 8R
max_open_tickers = 4
max_total_intraday_exposure = configurable
```

Because the strategy can have a low win rate and large winners, the backtest should report:

```text
win_rate
avg_win_R
avg_loss_R
expectancy_R
max_consecutive_losses
max_daily_loss_R
max_drawdown_pct
profit_factor
tail_loss_events
```

## 10.2 Progressive Exposure

Core rule:

```text
Small when uncertain.
Bigger only when confirmed.
Biggest only on winners.
```

This maps well to MTC_V2’s `max_entries`, `allow_add`, and position manager concepts, but should be prototyped separately first.

Potential implementation:

```text
starter_size = 0.25R
confirmation_add = 0.50R
trend_add = 0.75R
max_total_planned_loss = 1.50R to 4.00R depending on model
```

## 10.3 Volatility Tax / Drawdown Control

This is one of the most useful non-entry lessons in the transcript.

Research note:

```text
High returns with uncontrolled drawdown are fragile.
A 50% drawdown requires 100% recovery.
A deeper drawdown creates psychological and mathematical damage.
```

Possible system controls:

```text
daily_loss_lockout = true
weekly_drawdown_throttle = true
risk_trails_equity = true
risk_reduces_after_losses = true
risk_increases_only_after new equity highs or rolling profit
```

## 10.4 Outlier-Day Withdrawal Logic

The trader discusses wiring out money after outlier days. This is not a trade entry/exit rule but can be useful for portfolio simulation.

Prototype as optional portfolio rule:

```text
if daily_profit_R >= outlier_day_threshold_R:
    withdraw_pct_of_profit = 50%
    reduce_next_day_compounded_risk_base accordingly
```

For research, this should be separated from pure strategy expectancy.

---

## 11. MTC_V2 / QuantLens Integration

## 11.1 Do Not Add Directly to Pine Now

This should **not** be added to `01_PINE/MTC_V2.pine` at intake stage.

Reasons:

- It is a short-side small-cap intraday strategy.
- It requires data that Pine may not reliably have:
  - borrow availability;
  - hard-to-borrow fees;
  - halt data;
  - filing/news quality;
  - pre-market scanner context;
  - realistic slippage;
  - SSR effects.
- Backtest without these can be dangerously overfit.

## 11.2 Python Prototype First

Recommended research path:

```text
research/strategy_candidates/smallcap_gap_mean_reversion_brian_lee/
```

Suggested files:

```text
README.md
candidate_spec.md
feature_schema.yml
data_requirements.md
prototype_plan.md
risk_model.md
known_failure_modes.md
```

## 11.3 Possible MTC_V2 Component Mapping

If later adapted into MTC architecture:

### Signal Producer

```text
producer_smallcap_gap_mean_reversion_v1
```

Inputs:

```text
gap_pct
relative_volume
dollar_volume
extension_score
resistance_proximity
htf_extension
supply_structure
news_quality_score
fundamental_short_score
cycle_score
```

### Signal Transform Pipeline

Useful transforms:

```text
wait_for_supply
failed_bounce_confirmation
lower_high_confirmation
vwap_reclaim_block
```

### Entry Gates

Potential gates:

```text
liquidity_gate
borrow_availability_gate
news_quality_gate
fundamental_short_gate
cycle_heat_gate
halt_risk_gate
spread_slippage_gate
session_time_gate
```

### Position Manager

Use existing MTC concepts:

```text
max_entries
add_only_if_profitable
block_add_if_losing
daily_loss_lockout
ticker_loss_lockout
```

### Position Sizing

Use R-based sizing:

```text
risk_pct
max_ticker_R
max_daily_R
equity_trailing_risk_base
```

### Exit Rules

Potential exit stack:

```text
protective_stop
partial_cover_R
prior_close_target
gap_fill_target
moving_average_target
time_stop
structure_reclaim_exit
```

---

## 12. Backtest Data Requirements

Minimum required data:

```text
1-minute OHLCV
pre-market OHLCV
daily OHLCV
float / market cap
share offering / dilution tags
news timestamps
filing timestamps
borrow availability if possible
halt timestamps if possible
spread / slippage proxy
SSR flag if possible
```

Without these, backtest results should be marked `LOW_TRUST`.

---

## 13. Initial Prototype Pseudocode

```python
for day in trading_days:
    candidates = scan_universe(
        gap_pct_min=20,
        dollar_volume_min=MIN_DOLLAR_VOLUME,
        price_min=MIN_PRICE,
        relative_volume_min=MIN_RVOL,
    )

    for symbol in candidates:
        features = build_features(symbol, day)

        if not borrow_available(symbol, day):
            continue

        score = (
            features.technical_extension_score
            + features.fundamental_short_score
            + features.news_weakness_score
            + features.cycle_score
        )

        if score < MIN_SHORT_SCORE:
            continue

        if features.high_quality_durable_catalyst:
            continue

        wait_until_supply_signal(symbol)

        if supply_signal in ["failed_bounce", "lower_high", "vwap_reject"]:
            open_short_starter(symbol, risk_R=STARTER_R)

        while position_open(symbol):
            update_structure(symbol)

            if trade_working(symbol) and add_signal(symbol):
                add_short(symbol, risk_R=ADD_R)

            if protective_stop_hit(symbol):
                cover_all(symbol, reason="STOP")

            elif target_hit(symbol):
                cover_partial(symbol, reason="TARGET")

            elif momentum_exhausted_or_time_stop(symbol):
                cover_remaining(symbol, reason="TIME_OR_EXHAUSTION")
```

---

## 14. Candidate Parameters for First Research Pass

```yaml
candidate_id: CAND_BRIAN_LEE_SMALLCAP_GAP_MR_SHORT_V1
direction: short
timeframe: 1m_primary_5m_context
holding_period: intraday
universe:
  asset_class: US_equities_smallcap
  gap_pct_min: 20
  min_price: 1.00
  min_dollar_volume: TBD
  min_relative_volume: TBD
entry:
  require_first_supply: true
  require_failed_bounce_or_lower_high: true
  allow_blind_short: false
  allow_premarket_entry: false_initially
risk:
  risk_unit: R
  starter_risk_R: 0.25
  confirmation_add_R: 0.50
  max_ticker_loss_R: 4.00
  max_daily_loss_R: 6.00
  add_to_losers: false
exit:
  partial_at_R: [2, 4, 6]
  prior_close_target: true
  gap_fill_target: true
  moving_average_target: true
  flatten_eod: true_initially
validation:
  require_borrow_model: true
  require_slippage_model: true
  require_halt_model: true
```

---

## 15. Expected Failure Modes

### F1 — Blind Shorting Into a Squeeze

Risk:

```text
Shorting only because price is up a lot can be fatal.
```

Mitigation:

```text
Require supply confirmation.
Use starter size only.
No add until position is working.
```

### F2 — Unrealistic Borrow / Locate Assumption

Risk:

```text
Best short candidates may be impossible or expensive to borrow.
```

Mitigation:

```text
Borrow availability gate.
Hard-to-borrow fee simulation.
Mark missing borrow data as LOW_TRUST.
```

### F3 — Slippage / Spread Underestimation

Risk:

```text
Small caps can have wide spreads and thin levels.
```

Mitigation:

```text
Volume participation cap.
Spread proxy.
Conservative market-order slippage.
```

### F4 — Halt / News Shock Risk

Risk:

```text
Parabolic small caps can halt and reopen far against the position.
```

Mitigation:

```text
Halt risk flag.
Max position size.
No oversized starter.
Gap-risk stress test.
```

### F5 — Overfitting to One Cycle

Risk:

```text
Small-cap mania cycles vary sharply.
```

Mitigation:

```text
Segment by cycle.
Walk-forward by year.
Separate hot-cycle and cold-cycle results.
```

### F6 — Short Bias During Real Fundamental Repricing

Risk:

```text
Some gap-ups are real repricing events.
```

Mitigation:

```text
News quality filter.
M&A / major approval / major contract exclusion.
Manual catalyst labels in early research.
```

---

## 16. Relationship to Previous Intake Candidates

## 16.1 Compared With Market Wizards / VCP Candidate

Previous candidate:

```text
Long-side high-quality leaders
+ tight base / VCP
+ 10/21 EMA reclaim
+ strict risk
```

Current candidate:

```text
Short-side small-cap speculative gap
+ parabolic extension
+ weak catalyst/fundamentals
+ supply confirmation
+ progressive exposure
```

They are structurally opposite and should not be mixed in the first prototype.

## 16.2 Compared With Mark Ritchie Candidate

Previous candidate:

```text
Low-risk breakout
+ add only when working
+ avoid losers
```

Shared principle:

```text
Add to winners, not losers.
Use low-risk entry.
Let winners cover many small losses.
```

Current candidate applies that principle to intraday short mean reversion.

## 16.3 Compared With Andrew Connell Candidate

Previous candidate:

```text
Event-driven long setup
+ catalyst
+ value area breakout
+ 2:1 reward/risk
```

Shared principle:

```text
Context matters.
News quality matters.
Technical confirmation matters.
```

Current candidate uses context/news in the opposite way: to identify when a gap reaction is likely overextended and fadeable.

---

## 17. Decision

### Final Verdict

```text
CANDIDATE
```

### Recommended Codex Status

```text
READY_FOR_PYTHON_PROTOTYPE
```

### Recommended Candidate ID

```text
CAND_BRIAN_LEE_SMALLCAP_GAP_MR_SHORT_V1
```

### Recommended Next Action

Create a separate Python research folder and write a strict feature/data specification before coding.

Do **not** implement in Pine yet.

---

## 18. Files / Systems Touched

### Created by this intake

```text
INTAKE_2026-05-03_DPA35Gug3Y4_brian_lee_smallcap_mean_reversion_progressive_exposure.md
```

### Not touched

```text
01_PINE/MTC_V2.pine
Production Python runner files
Backtest outputs
Optimization outputs
Registry files
CSV/data bundles/cache files
Secrets/API keys/webhooks
```

---

## 19. Codex Handoff Summary

Use this as the first Codex instruction if implementing the prototype later:

```text
Build only a research specification and Python prototype plan for
CAND_BRIAN_LEE_SMALLCAP_GAP_MR_SHORT_V1.

Do not edit 01_PINE/MTC_V2.pine.
Do not edit production Python runner files.
Do not run optimization.
Do not create large datasets.
Do not assume borrow availability or zero slippage.

The candidate is a short-side intraday small-cap parabolic gap mean-reversion model.
Core filters: gap >= 20%, high relative volume, parabolic extension, weak/dilutive fundamentals, weak or non-durable catalyst, small-cap hype cycle, prior resistance/HTF extension.
Entry must wait for supply: pullback, failed bounce, lower high, VWAP/pivot rejection.
Position management: starter -> confirmation add -> trend add; never add to losing positions.
Risk model: R-based sizing, max ticker R, max daily R, equity-trailing risk, volatility-tax controls.
Exit model: protective stop first, partial covers at R targets and prior pivots/previous close/gap-fill/moving averages, flatten EOD in v1.
Mark all results LOW_TRUST unless borrow, slippage, halt, and news-timestamp assumptions are explicit.
```

---

## 20. Notes for Trader Wiki Extraction

Even though this is a `CANDIDATE`, the following themes are valuable for Trader Wiki:

- Risk-first trading mindset.
- R-multiple thinking.
- Volatility tax and drawdown recovery.
- Add to winners, never losers.
- Systematize execution.
- Reduce ego after strong periods.
- Wire-out / profit extraction as business discipline.
- Low win rate can still work if average winner dominates average loser.
