# Evidence-policy profiles — fast, balanced, conservative

**Authority:** owner decision **OD-20260906-6**. Engineering derives the numbers; the owner is asked
only for a genuine risk-appetite or waiting-time trade-off.

**What this is.** Three complete, internally consistent settings of every open number in
`p021_readiness_rules.py` except the two measure-first groups, each number carrying its derivation
from the measurements in `CADENCE_MEASUREMENT.md`. One profile is recommended. The document ends with
the exact minimal list of decisions that genuinely need the owner: there are **two**.

**What this is not.** Not an approval, not a build, not a promotion. `implementation_authorized`
for WP-P0-21 stays `false`. Nothing here makes any strategy ready.

---

## 1. Preserved decisions — recorded here so no profile can quietly move them

| Decision | Status in all three profiles |
|---|---|
| `single_trade_loss_risk_unit_multiple_max = 1` | unchanged, identical in all three |
| `day_trade_count_min = 30` — provisional policy **v1** | unchanged, identical in all three. Not re-asked. |
| Divergence and gap limits set only **after** measurement | no profile sets a value; §5 gives the procedure and the decision rule |
| Internal paper testing and exchange-testnet proof are two separate requirements, neither substituting for the other | unchanged |
| Unexplained reconciliation breaks: zero tolerance | unchanged |
| No strategy becomes live-ready from a short forward test alone | unchanged; the forward window is one of fourteen live-gate preconditions and satisfies none of the other thirteen |
| Day forward period must be **shorter**, swing and position **longer** (decision 130) | structurally enforced: every day period below is shorter than every swing period, which is shorter than every position period |

---

## 2. The derivation rules, stated once and applied three times

Only four rules produce every number below. Where a rule cannot be applied because the measurement
does not exist, that is said at the number, not hidden.

**Rule 1 — the backtest floor is about statistics, so it is measured per series.**
A backtest trade-count minimum exists to make a performance estimate mean something. Trades on one
instrument are the closest thing available to independent observations, so the floor is checked
against a single `(strategy, asset, timeframe)` series with no pooling. Each candidate value is
reported with the **share of measured series that clear it** — the direct measure of "does this ban
the category".

**Rule 2 — the forward floor is about operations, so it is counted pooled.**
Owner decision 130 splits the forward test's job: for swing and position it proves the machinery
works while robust backtest evidence carries the edge. Operational proof is per *order*: each forward
trade independently exercises entry, fill, stop handling, exit and reconciliation. Those exercises
are additive across instruments even though their *returns* are correlated. Forward trades are
therefore counted across the candidate's **declared, frozen** instrument universe.

This one rule is worth more than any threshold choice in this document: it takes the median swing
candidate from **71 weeks** to reach 12 forward trades down to **8 weeks**, by counting correctly
rather than by lowering the bar. It is an engineering decision and needs nothing from the owner.

The absolute floor under Rule 2 is **8 forward trades**, from coverage rather than statistics: two
directions × two exit reasons (stop and target) × two observations each = 8. Below eight, at least
one of those four combinations is guaranteed unexercised.

**Rule 3 — the forward *period* is the slower of three clocks.**

```
forward_period = max(
    T_count      = pooled p50 days for that type to reach forward_trade_count_min,
    T_cycle      = K × the type's median per-series inter-entry interval,
    T_operational= 14 days
)                                       rounded up to whole weeks
```

- `T_count` stops the period being shorter than the evidence it demands.
- `T_cycle` guarantees that a **single** instrument shows K complete trade cycles, so the count is not
  met purely by breadth. `K = 3` fast, `4` balanced, `6` conservative.
- `T_operational = 14 days` is the smallest window containing at least two weekends, two week
  boundaries and one exchange maintenance cycle. **This is engineering judgment, not a measurement**,
  and it is the only such value in this document. It binds only for the day type, where both measured
  clocks are shorter than two weeks.

**Rule 4 — the count and the period both bind.** A candidate passes when it has run for the period
**and** produced the count. Fast candidates are period-bound; slow ones are count-bound. §6 reports
which of the snapshot's strategies fall on which side, per profile.

---

## 3. The three profiles

Numbers marked **†** are extrapolated, not measured — no position-type strategy exists anywhere in
the snapshot (`CADENCE_MEASUREMENT.md` §4.1).

| Open number | Blocker | fast | balanced | conservative |
|---|---|---:|---:|---:|
| `day_trade_count_min` *(preserved policy v1)* | — | **30** | **30** | **30** |
| `swing_trade_count_min` | B-03 | 20 | **30** | 40 |
| `position_trade_count_min` | B-03 | 8 † | **12 †** | 20 † |
| `stop_loss_ceiling` (fraction of account equity) | B-04 | 0.667 % | **0.50 %** | 0.25 % |
| `day_forward_trade_count_min` | B-10 | 12 | **20** | 30 |
| `day_forward_period` | B-10 | 2 weeks (14 d) | **3 weeks (21 d)** | 5 weeks (35 d) |
| `swing_forward_trade_count_min` | B-10 | 8 | **12** | 20 |
| `swing_forward_period` | B-10 | 13 weeks (91 d) | **17 weeks (119 d)** | 25 weeks (175 d) |
| `position_forward_trade_count_min` | B-10 | 8 † | **12 †** | 20 † |
| `position_forward_period` | B-10 | 39 weeks (273 d) † | **52 weeks (364 d) †** | 78 weeks (546 d) † |
| `normal_market_condition_count_min` | B-10 | 2 | **2** | 3 |
| — its `occupancy_min` | B-10 | 5 % | **10 %** | 10 % |
| — its `trades_per_condition_min` | B-10 | 2 | **3** | 3 |
| `gap_ratio_max` | B-02 | **measure first — §5.1** | | |
| `divergence_tolerance` | B-06 | **measure first — §5.2** | | |
| `divergence_window_length` | B-07 | **measure first — §5.2** | | |
| `divergence_min_paired_observations` | B-07 | **measure first — §5.2** | | |

---

## 4. Where each number comes from

### 4.1 `swing_trade_count_min` — 20 / **30** / 40

The measured achievability, per series, over the swing class's median 1 974-day (5.4-year) backtest
span:

| floor | measured share of the 127 swing series that clear it |
|---:|---:|
| 12 | 93.7 % |
| **20** | **84.3 %** |
| **30** | **75.6 %** |
| **40** | **68.5 %** |
| 50 | 41.7 % |

**Balanced sets 30** for one reason: it keeps the *statistical* bar identical to the day class's
preserved 30, so a swing strategy is judged on the same evidentiary strength as a day strategy. Owner
decision 129 asked for separate rules "reflecting their slower trade frequency" — but the frequency
difference is a *calendar* problem, and it is answered by the forward period, not by weakening the
backtest estimate. Keeping 30 costs 24.4 % of measured swing series; letting them in at 20 buys 8.7
percentage points of population at the price of a 22 % wider confidence interval on every swing
expectancy (`√(30/20) = 1.22`).

**Fast sets 20** to buy that population. **Conservative sets 40**, which drops to 68.5 % — the last
value before the cliff at 50, where the class more than halves.

### 4.2 `position_trade_count_min` — 8 † / **12 †** / 20 †

**No position-type strategy exists in the snapshot**, so this is extrapolated. Every step is
arithmetic on a measured quantity:

| step | value | source |
|---|---|---|
| measured swing duty cycle (hold ÷ inter-entry), p50 | 0.3333 | measured, 127 series |
| position boundary holding time | 720 h = 30 d | definition, design §(a) |
| ⇒ inter-entry at the boundary | 30 ÷ 0.3333 = 90 d | arithmetic |
| ⇒ trade rate at the boundary | 4.06 trades/year | arithmetic |
| longest backtest span in the snapshot (swing p50) | 1 974 d = 5.4 y | measured |
| **⇒ maximum backtest trades a boundary position series can show** | **22** | arithmetic |

**Therefore 30 is impossible and 22 is the ceiling.** A strategy at the class boundary tops out at 22
trades over the longest history available, and a genuinely slower one — a 90-day holder — gets about
7. Any floor of 30 bans the category, which decision 129 forbids.

- **Fast 8** — the Rule 2 coverage floor; the lowest number that can exercise both directions and both
  exit reasons twice.
- **Balanced 12** — half the measured ceiling of 22, leaving room for strategies materially slower
  than the boundary.
- **Conservative 20** — within one or two trades of the ceiling. This is deliberately near-prohibitive
  and its consequence is stated as such in §6: at 20, only position strategies sitting almost exactly
  on the swing boundary are evaluable on a 5-year history.

**These three numbers must be re-derived the first time a real position strategy exists.** They are
the only values in this document not backed by a direct measurement.

### 4.3 `stop_loss_ceiling` — 0.667 % / **0.50 %** / 0.25 %

Unit: the maximum fraction of total account equity that one stop-out may cost. Enforced as the
ceiling on `risk.risk_pct_per_trade` (`IBKR_PAPER_BRIDGE/bridge/engine/risk.py:37`, used at `:379`).
Full reasoning, and the owner-facing form of this question, are in `RISK_POLICY_EXPLAINER.md` §4.

The derivation in one line: two existing guards, `max_daily_loss_pct = 0.02` and
`max_consecutive_losses = 3` (`risk.py:38,45`), bound the coherent range at
`3 × ceiling ≤ 2 %`, i.e. **ceiling ≤ 0.667 %**. Above that the consecutive-loss guard can never fire.

- **Fast 0.667 %** — the top of the coherent range; the consecutive-loss guard fires at exactly the
  daily limit.
- **Balanced 0.50 %** — the value the bridge is **already configured to** and that a recorded
  deployment window already used (`DEPLOY_TSP1007_WINDOW_D1_2026-07-19.md:51`). No new number is
  minted. Three stop-outs cost 1.5 %, so the consecutive-loss guard fires cleanly before the daily
  one.
- **Conservative 0.25 %** — eight consecutive stop-outs inside the daily limit. It also shrinks
  position notional: at the widest declared stop measured in the snapshot (25.5 % of entry price), a
  position sizes down to 1 % of equity and can start tripping `min_order_usd` (`risk.py:384`).

All three are strictly below the 1 % allocated-capital cap, which is what safeguard D-07 requires.

### 4.4 `day_forward_trade_count_min` — 12 / **20** / 30, and `day_forward_period` — 2 / **3** / 5 weeks

Counts, under Rule 2, pooled: **12 / 20 / 30**. The floor of 8 is exceeded in every profile because
day strategies are cheap in evidence and expensive in nothing.

Period, under Rule 3, using the measured day class (62 series, 6 strategies):

| clock | fast | balanced | conservative |
|---|---:|---:|---:|
| `T_count` — per-series p50 days to reach the count | 12.0 d | 20.1 d | 30.1 d |
| `T_cycle` — K × 1.0 d median inter-entry | 3 d | 4 d | 6 d |
| `T_operational` | 14 d | 14 d | 14 d |
| **max, rounded up to weeks** | **2 wk (14 d)** | **3 wk (21 d)** | **5 wk (35 d)** |

`T_count` uses the **per-series** figure, not the pooled one, deliberately. Pooled, a day strategy
reaches 20 trades in **4 days** at the class median — the count would be met by breadth in under a
week. Requiring that a single instrument would typically have produced the count keeps the window
honest.

**All three are shorter than 8 weeks**, satisfying decision 130's "use a shorter forward-testing
period" for day strategies. `T_operational` is the binding clock at the fast profile, and it is the
one engineering-judgment value in this document.

### 4.5 `swing_forward_trade_count_min` — 8 / **12** / 20, and `swing_forward_period` — 13 / **17** / 25 weeks

Counts, pooled: **8 / 12 / 20**. Fast sits exactly on the Rule 2 coverage floor and may not go lower.

Period, under Rule 3, using the measured swing class (127 series, 14 strategies):

| clock | fast | balanced | conservative |
|---|---:|---:|---:|
| `T_count` — pooled p50 days to reach the count | 36.0 d | 53.9 d | 89.9 d |
| `T_cycle` — K × 29.0 d median inter-entry | 87 d | 116 d | 174 d |
| `T_operational` | 14 d | 14 d | 14 d |
| **max, rounded up to weeks** | **13 wk (91 d)** | **17 wk (119 d)** | **25 wk (175 d)** |

`T_cycle` binds in all three, which is the correct outcome: a swing strategy that has been running for
only as long as its own trade cycle has shown nothing repeatable. Every swing period is longer than
every day period, satisfying decision 130's "allow a longer calendar period".

### 4.6 `position_forward_*` — 8 † / **12 †** / 20 †, and 39 † / **52 †** / 78 † weeks

Counts mirror swing, for the same Rule 2 reason. Period, under Rule 3, on the extrapolated 90-day
inter-entry interval from §4.2 and a 10-instrument universe:

| clock | fast | balanced | conservative |
|---|---:|---:|---:|
| `T_count` — pooled over 10 instruments | 72 d | 108 d | 180 d |
| `T_cycle` — K × 90.0 d † | 270 d | 360 d | 540 d |
| **max, rounded up to weeks** | **39 wk (273 d)** | **52 wk (364 d)** | **78 wk (546 d)** |

**Say the consequence out loud: the balanced position forward window is one year.** That is not a
policy preference, it is arithmetic on a 90-day holding cycle. The alternative — a position forward
window short enough to be comfortable — would be a window in which the strategy has not completed four
trade cycles on any instrument, and it would prove nothing. The honest answer to "how do I approve a
position strategy faster" is not a smaller number here; it is a wider declared universe, which shrinks
`T_count` but never `T_cycle`.

### 4.7 `normal_market_condition_count_min` — 2 / **2** / 3

The owner's binding words are "**more than one** normal market condition" (decision 130), so 2 is the
floor and no profile may go below it.

The measurement that drives everything else here: **the existing coverage metric is saturated.**
`regime_coverage_count` is **4 out of 4 in all 45 readiness artefacts in the snapshot** — every single
candidate. A minimum of 2, 3 or even 4 set against that metric would be satisfied automatically. The
number would be decoration, and raising it would be worse than useless because it would look like a
tightening.

So the number is not where the strength is. The strength is in the definition
(`P021_ENGINEERING_DESIGN_V2.md` §b.2): a condition counts as covered only when it occupies at least
`occupancy_min` of the window's **normal** bars *and* the candidate took at least
`trades_per_condition_min` trades whose entry bar carried that label.

| | fast | balanced | conservative |
|---|---:|---:|---:|
| distinct conditions required | 2 | **2** | 3 |
| `occupancy_min` | 5 % | **10 %** | 10 % |
| `trades_per_condition_min` | 2 | **3** | 3 |

`trades_per_condition_min = 2` is the smallest count that can contain both a win and a loss; 3 gives a
majority. Balanced keeps the count at 2 and spends its strictness on the two floors instead, because
requiring a **third** distinct condition makes approval depend on the weather: with four exclusive
labels, a market that simply never enters `CONSOLIDATING` during the window leaves a candidate waiting
for an event it does not control. Conservative accepts exactly that cost, deliberately.

**Caveat, stated because it is load-bearing.** This requires the price-only labeller
(`classify_regimes`, `create_optimization_data_bundle.py:372`) plus the two fixes in design §b.2, and
**no output of it exists anywhere in the snapshot**. Until it has been run, this number is defined and
uncomputed — a defined number that refuses is exactly the fail-closed behaviour the catalogue already
has.

---

## 5. The two measure-first groups — procedure and decision rule, no number

Owner instruction preserved: measure first, then set the limit. Neither can be measured today, and
the reason is not the absence of a decision.

### 5.1 Gap (`gap_ratio_max`, B-02)

**Why no number.** The counting method was never fixed, and the three sensible methods disagree by
four orders of magnitude on the same bytes: one three-month hole in five years of 5-minute data scores
0.000002 under gap-event counting and 0.049 under missing-bar counting. A limit chosen before the
method is chosen means nothing.

**Method now fixed** (design §d.3): **M2, the missing-bar ratio**,
`Σ (round(Δ/s) − 1) ÷ expected_bars`, per `(instrument, timeframe, window)` series. M1 and M3 are
computed and published alongside but not compared against the limit.

**Procedure that must run first** (design §d.6): fix `TIMEFRAME_SECONDS` — **it has no `5m` entry**, so
the existing scan silently reports zero gaps for the timeframe every day-class strategy in the
snapshot trades on; change truncation to rounding; scan every catalogued series; publish the M2
distribution and name the ten worst series.

**Decision rule, so no judgment is needed afterwards:**

> `gap_ratio_max` = the smallest value admitting at least 80 % of scanned series, rounded up to the
> next 0.1 %, capped at 5 %. If the 80 % rule and the 5 % cap conflict, that is a finding about the
> data and the limit is **not** set.

### 5.2 Divergence (`divergence_tolerance` B-06, `divergence_window_length` and
`divergence_min_paired_observations` B-07)

**Why no number.** Three things are missing at once: an accepted engine beyond the synthetic-only
milestone; any completed forward window (45 of 45 readiness artefacts record
`realtime_eq_backtest: false`); and a populated `dataset_hash`, so "the same bars" cannot even be
asserted.

**Definitions now fixed** (design §c): align by replaying the frozen artefact over the forward
window's own bars, pair by `(instrument, entry_bar, intent_id)`, split the difference into **decision
divergence** (different trades — zero tolerance, already covered by `intent_mismatch_count_max = 0`)
and **execution divergence** (same trade, worse fill — the only part a tolerance applies to), and
measure the residual in **risk units (R)**, never in per cent.

**Decision rules, so step 9 of the procedure is mechanical:**

> `divergence_tolerance` = the `D1` value at the **10th percentile** of the observed cross-candidate
> distribution, from candidates whose deterministic replay passed and whose unpaired intent count was
> zero, floored at **−2.0** standard errors.

> `divergence_window_length` = the candidate's **own** measured days-to-`divergence_min_paired_observations`
> at its pooled forward rate, floored at the type's `forward_period` and capped at 4 × it. It is a
> per-candidate derived quantity, not a fixed calendar number, because the same window contains 20
> trades for one strategy and 2 for another — and *"a window that contains three trades measures
> nothing"*.

> `divergence_min_paired_observations` = the type's `forward_trade_count_min` under the chosen
> profile, never below **8**. Rationale: the same evidence that is sufficient to say the machinery
> works is the minimum sufficient to say the machinery works *the same*. Setting it below the forward
> count would create a check that runs on evidence too thin for the check beside it.

Under the balanced profile these evaluate to 20 (day), 12 (swing) and 12 † (position) paired
observations. **They are shown here as consequences of the profile, not as set values**; they take
effect only when the divergence measurement can actually run.

---

## 6. What each profile costs, in plain language

Computed, not estimated: `python tools/evaluate_profiles.py evidence/cadence_measurements.json
evidence/profile_consequences.txt`. "Wait" is `max(period, pooled time to reach the count)` for the
strategies actually measured in the snapshot.

### fast

| | day (6 strategies) | swing (14 strategies) | position |
|---|---|---|---|
| backtest floor clears | 50/62 series (80.6 %) | 107/127 series (84.3 %) | no data † |
| reach the forward count inside the period | 3 of 6 | 10 of 14 | † |
| median wait | **2 weeks** | **13 weeks** | 39 weeks † |
| worst measured wait | 9 weeks (CANDIDATE_009) | 126 weeks (KELL_WEDGE) | † |

**What you get:** the shortest queue. A day candidate is judged in a fortnight.
**What you risk:** 12 forward trades is not many. A strategy can produce twelve good trades in one
market mood and look proven; the 5 % occupancy floor and 2-trade-per-condition floor are the weakest
of the three, so "two conditions covered" is the easiest to satisfy here. The swing backtest floor of
20 gives every swing expectancy a 22 % wider confidence interval than 30 would. **This profile's
characteristic failure is a false pass.**

### balanced *(recommended)*

| | day (6 strategies) | swing (14 strategies) | position |
|---|---|---|---|
| backtest floor clears | 50/62 series (80.6 %) | 96/127 series (75.6 %) | no data † |
| reach the forward count inside the period | 3 of 6 | 9 of 14 | † |
| median wait | **4 weeks** | **17 weeks** | 52 weeks † |
| worst measured wait | 15 weeks (CANDIDATE_009) | 189 weeks (KELL_WEDGE) | † |

**What you get:** a day candidate judged in about a month, a typical swing candidate in about four.
Swing keeps the same 30-trade statistical bar as day, so the two classes are judged on comparable
evidence rather than on comparable patience. Every number except the position group comes from a
measurement, and `stop_loss_ceiling` is a value the system is already running.
**What you risk:** five of fourteen measured swing strategies are count-bound and wait longer than
the period — and one of them, KELL_WEDGE, waits 189 weeks. That is not the profile's fault; KELL_WEDGE
trades 0.009 times a day on one instrument, and no policy makes that fast.

### conservative

| | day (6 strategies) | swing (14 strategies) | position |
|---|---|---|---|
| backtest floor clears | 50/62 series (80.6 %) | 87/127 series (68.5 %) | no data † |
| reach the forward count inside the period | 3 of 6 | 9 of 14 | † |
| median wait | **6 weeks** | **25 weeks** | 78 weeks † |
| worst measured wait | 23 weeks (CANDIDATE_009) | 314 weeks (KELL_WEDGE) | † |

**What you get:** 30 forward day trades and 20 forward swing trades, a third market condition
required, and a `stop_loss_ceiling` of 0.25 % that survives eight consecutive stop-outs inside the
daily limit.
**What you risk:** the swing backtest floor of 40 excludes 31.5 % of measured swing series. The third
required condition makes approval depend on a market state you do not control. `position_trade_count_min = 20`
sits within two trades of the extrapolated 22-trade ceiling, so on a 5-year history only position
strategies almost exactly on the swing boundary are evaluable at all. **This profile's characteristic
failure is a false fail** — good strategies never getting judged.

### One consequence common to all three, which is not a profile choice

`day_trade_count_min = 30` is the owner's preserved provisional policy v1 and is identical in all
three. Measured against it, **12 of 62 day series (19.4 %) do not reach 30 backtest trades**. That is
information about the preserved decision, not a request to revisit it.

---

## 7. Recommendation

**Adopt `balanced`.**

1. **Every number in it except the position group is a measurement or arithmetic on one.** Fast and
   conservative each move at least one number away from what the data supports in order to buy speed
   or caution.
2. **It keeps the statistical bar equal across types.** Swing and day both need 30 backtest trades.
   Owner decision 129's "slower trade frequency" is answered where it belongs — in the calendar
   period — rather than by accepting weaker evidence from slow strategies, which is how a slow
   strategy gets promoted on noise.
3. **Its `stop_loss_ceiling` mints no new number.** 0.50 % is what `bridge/engine/risk.py:37` is
   already set to and what a recorded deployment window already used, and it is the largest value that
   keeps `max_consecutive_losses = 3` alive inside `max_daily_loss_pct = 2 %`.
4. **The waiting times are real and tolerable at the median**: four weeks for a day candidate,
   seventeen for a swing one. The strategies that wait far longer are slow strategies on narrow
   universes, and the correct fix for them is a wider declared universe, not a weaker policy.
5. **It is reversible cheaply.** The whole set is one hashed `strategy_type_policy_set` version
   (design §e). Changing profile is a new version and fresh relevant evidence, which is exactly the
   rule decision 129/130 already requires — no rework, no migration.

---

## 8. What genuinely needs the owner — two decisions, and nothing else

Everything else in this document is engineering: taxonomies, metrics, formulas, units, alignment,
provenance, pooling, the counting method, the policy-version contract. None of it is being asked.

### Decision 1 — how much of the account may a single stop-out cost?

**Plain explanation.** You already capped how much money a first live strategy is *given* (1 % of the
account, no leverage) and you already ruled that a trade may not lose more than it said it would risk.
Neither of those caps how much a trade is allowed to *say* it risks. That third number is
`stop_loss_ceiling`, and it is blank. While it is blank, the rule you already made cannot reject
anything, and live-gate precondition 10 reads `BLOCKED — the lower loss-at-stop cap is undefined`.

**Why it is yours.** It is a statement about your tolerance, not about the market. No measurement
produces it. Every engineering constraint on it has already been applied: the unit is fixed, the
enforcing field is identified, and the coherent range is bounded above at 0.667 % by two guards you
already have.

| Option | Consequence |
|---|---|
| 0.25 % | Eight consecutive stop-outs fit inside the 2 % daily limit. Wide-stop strategies size down to about 1 % of equity and start tripping the minimum order size. |
| **0.50 % — recommended** | Four consecutive stop-outs fit; the 3-loss guard fires first, as designed. Equals the value already configured and already deployed. Mints no new number. |
| 0.667 % | The top of the coherent range. Above it, `max_consecutive_losses = 3` becomes a guard that can never fire. |

**Recommendation: 0.50 %.**
**What it blocks while unanswered:** the `stop_loss_ceiling` half of `P021.BASIC_FAILURE_FLOOR`, and
the open half of live-gate precondition 10.
**What it does not unblock:** the other half of that check still waits on the swing and position
minimums, and thirteen other live-gate preconditions are untouched.

### Decision 2 — how long are you willing to wait per candidate?

**Plain explanation.** Longer forward windows and higher trade counts mean fewer bad strategies get
through and fewer good ones get judged. The whole trade-off collapses to one median number per class,
and the three profiles differ mainly in that number.

| Option | Median wait, day → swing → position | Characteristic failure |
|---|---|---|
| fast | 2 wk → 13 wk → 39 wk † | **false pass** — twelve forward trades in one market mood can look like proof |
| **balanced — recommended** | 4 wk → 17 wk → 52 wk † | balanced; five of fourteen measured swing strategies still wait longer than the period |
| conservative | 6 wk → 25 wk → 78 wk † | **false fail** — 31.5 % of swing series excluded, and position strategies effectively unevaluable |

**Recommendation: balanced**, for the five reasons in §7.
**What it blocks while unanswered:** the swing and position halves of `P021.BASIC_FAILURE_FLOOR`, and
all seven forward-evidence numbers, which is the whole `forward_evidence_refusal` block in
`p021_readiness_rules.py`.
**What it does not unblock:** the divergence and gap groups, which wait on measurement, not on you.

### If you answer neither

Both recommendations can be recorded as **policy v1, provisional** — reversible, versioned, visible —
in exactly the way `day_trade_count_min = 30` already is. The checker would then refuse on the two
measure-first groups only, instead of on all fourteen numbers. Nothing becomes ready either way: the
corrected engine is accepted only as a synthetic-only milestone, and `implementation_authorized` for
WP-P0-21 is still `false`.
