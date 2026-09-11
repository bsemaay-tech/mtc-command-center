# WP-P0-21 engineering design v2.1 — taxonomies, metrics, contracts

**Authority:** owner decision **OD-20260906-6** (`C:\tmp\OWNER_DECISIONS_20260906_1240.md`, section
"P0-21"): engineering defines the taxonomies, metrics, formulas and policy-version contracts; the
owner is asked only for a genuine risk-appetite or waiting-time trade-off.

**Status:** design only. Nothing here is built, merged, run against a candidate, or accepted. No
backtest, optimisation or server was run to produce it. `implementation_authorized` for WP-P0-21
remains `false`; the corrected engine is accepted only as a **synthetic-only milestone**
(OD-20260906-2) with production economics fail-closed.

**Primary subject.** `MTC_COMMAND_CENTER/03_QUANTLENS/tools/p021_readiness_rules.py` — 7 checks, 14
open numbers, blockers B-02…B-22. **It is not on the snapshot's main line.** It exists only on
`origin/feature/wp-p0-21-readiness-rules`, commit `a63bd4b0` ("feat(p021): add fail-closed readiness
rule catalogue", 243 lines, 2026-09-04). `git ls-files | grep p021` on `HEAD` (`94cb4822`) returns
nothing. Every reference below is to that commit's copy, read with `git show`.

## Change log — v2.1

- **Opus T0 item (a):** added `BLOCKED_UNMEASURABLE_HOLD` to the normative classifier, carried its
  zero-median constant in `strategy_type_policy_set.taxonomy`, and stated the measured series caught
  by all four refusals.
- **Opus T0 item (b):** replaced the stale day-class decoupling figures in §a.3 with the corrected
  post-refusal measurements.
- **Opus T0 item (c):** corrected the mixed-holding-profile refusal count from the stale value to the
  measured value.
- **Opus T0 item (d):** corrected the day-class strategy list and the 5-minute blind-spot fraction;
  CRABEL is now stated as refused on 1D data.
- **Opus T0 contract-field nit:** added `occupancy_min`, `trades_per_condition_min`, and the three §e.3
  method identities to the policy-set contract.
- **Opus T0 catalogue-name nit:** documented the `day_trade_count_min` to
  `day_trade_count_starting_rule` mapping.
- **Opus T0 risk-explainer nit:** labelled 0.39 % as a p10 observation rather than a minimum in
  `RISK_POLICY_EXPLAINER.md`.
- **Gemini 3.7 round 1:** PASS; it raised no additional nit.

### Binding decisions preserved, never re-asked

| Decision | Preserved as | Where it lands in this design |
|---|---|---|
| `single_trade_loss_risk_unit_multiple_max = 1` | unchanged limit | §(a) policy set; `RISK_POLICY_EXPLAINER.md` §1 rule B |
| `day_trade_count_min = 30` | **provisional policy v1**, kept | §(a) policy set; identical in all three profiles |
| Divergence and gap limits set only **after** measurement | unchanged | §(c) and §(d) define the measurement, not the limit |
| The 1 % risk / no-leverage rule ≠ `stop_loss_ceiling` | unchanged | separate document, `RISK_POLICY_EXPLAINER.md` |
| OD-20260826-3 — promotions need real DSR / BH-FDR / `robust_final` / positive-alpha gates | unchanged | out of scope here; P0-21 is the readiness floor, not the promotion bar |
| OD-20260826-5 — evidenced status implies no acceptance | unchanged | every artefact below carries status, never a verdict |

---

## (a) Strategy-type taxonomy and the `strategy_type_policy_set` contract (B-22)

### a.1 Why a taxonomy is needed at all, and the evidence that it is missing

Owner addendum-32 decision **129** requires per-type minimum-evidence rules and decision **130**
requires per-type forward-evidence rules (both folded into the design draft at W297,
`W297_P021_FOLD_REPORT.md` §4–§5). Nothing in the system computes a type today.

Measured, not assumed: the evaluation artefact schema **already declares the field and never fills
it**. Across all 45 `*.readiness.json` files under `MTC_COMMAND_CENTER/03_STATUS/`, the value of
`strategy_type` is `null` in every one (verified by reading all 45; see `LANE_REPORT.md` for the
command). Example: `03_STATUS/dry_run_evidence_2026-06-06/QL_FAM_MOMENTUM_CONTINUATION__BTCUSDT__4h.readiness.json:8`.

So B-22 is not "add a field". The field exists. B-22 is "define what fills it".

### a.2 The unit that gets classified

The promotion pipeline already evaluates **one strategy on one instrument on one timeframe**. The
readiness artefacts are named and keyed that way — `"strategy_id": "QL_FAM_MOMENTUM_CONTINUATION|BTCUSDT|4h"`.
The taxonomy therefore classifies a **series**: the triple `(strategy_id, asset, timeframe)`,
optionally further split by `variant` and `parameter_set` where the trade record carries them.

A strategy is **not** classified as a whole. A single rule set can be a day strategy on 5-minute bars
and a swing strategy on daily bars; forcing one label onto both would be a category error, and the
measurement in `CADENCE_MEASUREMENT.md` shows the same strategy families landing in different classes
at different timeframes.

### a.3 The two axes, and why they must not be collapsed into one

Two different measurable quantities are both called "speed" in ordinary talk, and they are decoupled
in the real records:

| Axis | Measured quantity | What it governs |
|---|---|---|
| **Holding-time axis** | distribution of `exit_time − entry_time` | market-exposure character: overnight risk, reaction latency, what "a day trader" means |
| **Cadence axis** | trades per unit calendar time | the rate at which *evidence* accrues, hence every waiting-time number |

Measured decoupling (`evidence/profile_derivation_inputs.txt:1,12,16`): among the **62 series** labelled
`day` — every one of which closes its typical trade inside **2 hours** — the trade rate spans
**0.0426 to 29.8251 trades/day** between the first and third quartile, a **700-fold** range. To
produce 30 trades, the p75 waiting time is **704.1 days** and the p25 waiting time is **1.0 day**.
They are the same "type" and their evidence budgets differ by a factor of 700
(`CADENCE_MEASUREMENT.md:181-186`).

**Design consequence.** `strategy_type` is defined on the **holding-time axis only**, because that is
the axis the owner's words describe ("day", "swing", "position") and the axis that is stable for a
given rule set. Every *number* that involves waiting is then derived from the candidate's **own
measured cadence**, with the per-type value acting as a floor and a cap. This is what makes the
per-type scalars in the readiness catalogue honest instead of arbitrary.

### a.4 The deterministic classification rule

Inputs: the closed-trade record for one series. Nothing else. No human judgement, no strategy
metadata, no name matching.

```
for each closed trade t:
    hold_hours(t) = (exit_time(t) - entry_time(t)) / 3600 s

    bucket(t) = "day"       if   0 <= hold_hours(t) <  24
                "swing"     if  24 <= hold_hours(t) < 720
                "position"  if       hold_hours(t) >= 720

n          = count of trades with both timestamps parseable and hold_hours >= 0
dominant   = the bucket holding the most trades
dominance  = count(dominant) / n
median_hold_hours = median(hold_hours)

strategy_type =
    REFUSE("BLOCKED_NEGATIVE_HOLD")          if any trade has exit before entry
    REFUSE("BLOCKED_INSUFFICIENT_SAMPLE")    if n < 10
    REFUSE("BLOCKED_UNMEASURABLE_HOLD")      if median_hold_hours == 0
    REFUSE("BLOCKED_MIXED_HOLDING_PROFILE")  if dominance < 0.80
    dominant                                 otherwise
```

**Every constant, with its reason.**

| Constant | Value | Why exactly this |
|---|---|---|
| day/swing boundary | **24 h, strict** | A day-trading strategy is one that does not carry a position overnight. In a 24/7 market the operational equivalent is "closed inside one calendar day". Strict `<` matters: a one-daily-bar hold is exactly 24.0 h and it *does* carry a full overnight, so it is swing. This is not cosmetic — it moves CANDIDATE_004 (8 105 trades, median hold exactly 24.00 h) out of the day class, and with it the day class's maximum median hold drops from 24 h to **2 h**. |
| swing/position boundary | **720 h (30 days)** | The owner's own language is "days or weeks" against "months" (`W297_P021_FOLD_REPORT.md:110-119`). One calendar month is the only non-arbitrary point between "weeks" and "months". |
| zero-median refusal | **median hold = 0 h** | A record whose typical trade has identical entry and exit timestamps carries no measurable holding duration. Calling it `day` would classify the recording convention, not the strategy, so it refuses as `BLOCKED_UNMEASURABLE_HOLD`. |
| `dominance ≥ 0.80` | four trades in five | A label is a claim about the typical trade. A series that is 55 % intraday and 45 % multi-week is not a day strategy with noise, it is two behaviours in one record, and its waiting-time arithmetic would be wrong for both. 0.80 is engineering's choice; **the sensitivity is published**: at 0.80 it refuses **13 of 253 series** (`evidence/cadence_tables.md:45,48`); the refusal is a `BLOCKED`, never a silent default. |
| `n ≥ 10` | ten trades | Below ten, `dominance` moves by more than 0.10 per trade, so the 0.80 test is decided by single trades. Ten is the smallest count at which one trade cannot flip the label. |

**Measured refusal mapping.** On the 253 de-duplicated series, the priority-ordered classifier produces
the following mutually exclusive outcomes (`evidence/cadence_measurements.json` and
`evidence/cadence_tables.md:40-48`):

| Refusal | Series caught by the rule |
|---|---|
| `BLOCKED_NEGATIVE_HOLD` | **0** series; no measured row exits before entry |
| `BLOCKED_INSUFFICIENT_SAMPLE` | **25** series: CANDIDATE_001 (6), CANDIDATE_011 (3), CANDIDATE_012 (1), KELL_WEDGE (2), LINDA_5SMA (1), MARTIN_LUKE (6), QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 (4), SLINGSHOT (1), and STG046_qlr_r215f4fj7v8 (1) |
| `BLOCKED_UNMEASURABLE_HOLD` | **26** 1D series: CRABEL (17; all of its measured series) and CANDIDATE_003 (9); none is labelled `day` |
| `BLOCKED_MIXED_HOLDING_PROFILE` | **13** series: CANDIDATE_001 (1), CANDIDATE_003 (1), CANDIDATE_012 (3), QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 (1), QL_LINDA_5SMA_RS_PULLBACK_v0 (5), STG001_ql_alpha_ada_two_candle_sr_1h (1), and STG003_ql_alpha_ltc_rsi_oversold_1h (1) |

The remainder is labelled: 62 `day`, 127 `swing`, and 0 `position`. This matches the measurement's
CRABEL finding and normative refusal (`CADENCE_MEASUREMENT.md:194-201`).

**Two properties this rule has on purpose.** It never guesses — four named refusals, each naming its
reason, matching the fail-closed style of `p021_readiness_rules.py`. And it is a pure function of the
trade record, so two independent implementations must agree byte-for-byte, which is what
`P021.DETERMINISTIC_REPLAY` demands of everything else.

**One property it does not have.** It cannot classify a strategy that has never traded. A brand-new
candidate has no type until it has ten closed trades in the frozen backtest. That is correct
behaviour and it is the reason the type is an **input** to `P021.BASIC_FAILURE_FLOOR`, computed
upstream from the backtest record, not something that check derives for itself.

### a.5 The `strategy_type_policy_set` contract (B-22)

One immutable, hashed object per policy version. It carries every per-type number, the shared
coverage fields, and the method identities needed to interpret them.

```jsonc
{
  "schema": "p021.strategy_type_policy_set/v1",
  "policy_id": "p021-evidence-policy",
  "profile": "balanced",                  // fast | balanced | conservative
  "taxonomy": {
    "day_max_hours": 24.0,                // strict upper bound
    "swing_max_hours": 720.0,             // strict upper bound
    "dominance_min": 0.80,
    "sample_min": 10,
    "unmeasurable_hold_median_hours": 0.0, // equality triggers refusal
    "classified_unit": "strategy_id|asset|timeframe|variant|parameter_set"
  },
  "types": {
    "day":      { "trade_count_min": 30, "forward_trade_count_min": null,
                  "forward_period_days": null },
    "swing":    { "trade_count_min": null, "forward_trade_count_min": null,
                  "forward_period_days": null },
    "position": { "trade_count_min": null, "forward_trade_count_min": null,
                  "forward_period_days": null }
  },
  "shared": {
    "single_trade_loss_risk_unit_multiple_max": 1,
    "stop_loss_ceiling_equity_fraction": null,
    "normal_market_condition_count_min": null,
    "occupancy_min": null,
    "trades_per_condition_min": null,
    "gap_ratio_max": null,
    "divergence_tolerance": null,
    "divergence_window_length_days": null,
    "divergence_min_paired_observations": null
  },
  "methods": {
    "regime_method_version": "rule_based_market_regime_v2",
    "gap_method_version": "data_gap_ratio_m2_v1",
    "divergence_method_version": "p021_divergence_v1"
  },
  "provenance": {
    "day_trade_count_min": "owner provisional policy v1, preserved OD-20260906-6",
    "single_trade_loss_risk_unit_multiple_max": "owner decided initial rule, preserved"
  },
  "version": "p021pol-v1:<sha256 of the canonical serialisation of everything above>"
}
```

**Rules of the object, all enforceable and all fail-closed.**

1. `null` means *unset*, and unset means **refuse**. There is no default, no fallback, no inherited
   value from another type. This is the existing behaviour of `p021_readiness_rules.py`
   (`_refusal()` and `validate_catalog()`) and the object must not weaken it.
2. `day.trade_count_min = 30` is present because it is the owner's provisional policy v1. Its
   `provenance` entry says so. It is never silently copied into `swing` or `position`.
   The design/profile name `day_trade_count_min` maps to this contract field and then to the upstream
   catalogue key `day_trade_count_starting_rule`; all three names refer to the same preserved value,
   **30** (`evidence/upstream_verification.txt:40`).
3. `version` is computed exactly the way the repository already computes an immutable policy
   version — see §(e).
4. A candidate's evaluated `strategy_type` and the `policy_set.version` used to judge it are both
   recorded on the result. A result produced under a different version does not count, exactly as
   `PRIOR_IDENTITY` evidence does not count at the live gate
   (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:3116`).
5. **Neither independent side may infer a candidate's type.** It is an input both are given, per the
   W297 fold's site 2 requirement (`W297_P021_FOLD_REPORT.md` §4 site 2).

### a.6 One taxonomy, three packages

W297 §9 records the cross-draft constraint: **P0-13, P0-20 and P0-21 must share one taxonomy**, and
the versioned-policy carrier must be one construct, not two (P0-20 decision 127 introduces the same
idea for risk and leverage). This design deliberately reuses the existing `DurableRiskPolicy` /
`ExposureRiskPolicy` version construct (§(e)) rather than minting a second mechanism. If P0-13 adopts
a different taxonomy, **this one loses**, and B-22 must be reopened rather than the two reconciled
after the fact.

---

## (b) Normal-market-condition taxonomy

### b.1 What already exists (do not duplicate either of these)

**Labeller 1 — `compute_regime_analysis`**, `03_QUANTLENS/tools/mega_walk_forward.py:1117-1224`.
Four **overlapping** buckets: `trend`, `range`, `high_vol`, `low_vol`. Trend is
`close != ema200 and adx14 >= 20`; range is `adx14 < 20`; the volatility buckets are ATR14 against
the **25th and 75th percentile of the lockbox window itself**. It labels the entry bar of each trade
and exports `regime_coverage_count`.

Three properties make it unusable as the basis of a coverage requirement, and one of them is
measured:

- **It saturates.** `regime_coverage_count` is **4 in all 45 readiness artefacts in the snapshot** —
  every single one. A `normal_market_condition_count_min` of 2, 3 or even 4 set against this metric
  would be satisfied by every candidate that has ever been evaluated. The number would be decoration.
  (Distribution of `weak_regime_identified` across the same 45: `high_vol` 20, `range` 20, `trend` 5.)
- **`trend` and `range` are exact complements.** `close[i] != ema200[i]` is a float inequality on two
  independently computed doubles; it is true in practice always. So the first bucket collapses to
  `adx14 >= 20` and the second to `adx14 < 20`. Every trade lands in exactly one of them, which is
  why coverage ≥ 2 comes free the moment a strategy has any volatility spread at all.
- **It is window-relative.** The ATR percentiles come from the lockbox slice. "High volatility" in a
  calm year and in a violent year are different absolute things wearing the same label, so a backtest
  label and a forward label are not comparable — which is precisely the comparison
  `normal_market_condition_count_min` exists to support.

**Labeller 2 — `classify_regimes`**, `01_MTC_PROJECT/tools/create_optimization_data_bundle.py:372-460`.
Per **bar**, from **price only**, four **exclusive** labels `TRENDING` / `RANGING` / `CHOPPY` /
`CONSOLIDATING`, from three statistics on a trailing window: `trend_strength` (net move ÷ path move —
the efficiency ratio), `range_compression` (window range ÷ mean close) and `rolling_volatility`
(stdev of bar returns). It carries `METHOD_VERSION = "rule_based_market_regime_v1"` and its window is
strictly trailing (`closes[start : index+1]`), so it is causal — no lookahead.

**This is the right base and it is adopted.** It is deterministic, price-only, exclusive, causal,
already versioned, and it labels *bars* rather than *trades*, which means it describes what the
market did rather than where the strategy happened to trade.

**No output of it exists in the snapshot.** `find` for `*regime*.csv` and `*_gaps.csv` returns
nothing: the bundle tool has never been run, or its outputs were never committed. So the labeller is
code without data.

### b.2 What must be added, and why each addition is necessary

`rule_based_market_regime_v1` labels *conditions*. It has no concept of *normal*. Three additions:

**Addition 1 — an explicit abnormality filter.** A bar is **not normal** if any of the following
holds. All are computable from price and volume alone and all are causal.

| Exclusion | Test | Why |
|---|---|---|
| `EXTREME_MOVE` | \|close/close[−1] − 1\| ≥ 8 × the trailing-window median absolute bar return | Flash moves, listings, de-pegs. A strategy that survived one is not evidenced for normal trade. |
| `VOLUME_COLLAPSE` | volume ≤ 0.1 × trailing-window median volume, or volume = 0 | Illiquid or halted. Fills in the record are fiction. |
| `DATA_GAP_ADJACENT` | the bar sits within one bar of a gap as defined in §(d) | The indicator windows spanning the hole are computed on absent data. |
| `STALE_PRICE` | `high == low == open == close` for ≥ 3 consecutive bars | Feed frozen. |
| `WARMUP` | fewer than `lookback` bars precede it | `classify_regimes` already emits `CONSOLIDATING` with `confidence 0.25` here; it must be excluded, not counted. |

The 8× and 0.1× multipliers are engineering choices; they are **relative to the same trailing window
the labeller already uses**, so they inherit its timeframe-relativity rather than adding a new
absolute constant.

**Addition 2 — make the volatility threshold scale-free.** `classify_regimes` compares
`rolling_volatility` against the absolute constant `0.006` (`:409`, `:412`). Per-bar return standard
deviation is not comparable across timeframes: the same market at 5-minute and daily resolution
produces values an order of magnitude apart. Two 5-minute series and one daily series in the snapshot
would therefore be labelled by different effective rules. Replace the absolute test with the
window's own quantile — the same fix `compute_regime_analysis` already applies to ATR — and record
the change as `rule_based_market_regime_v2`. **`v1` must not be silently mutated**; it carries a
`METHOD_VERSION` for exactly this reason.

**Addition 3 — a coverage definition that cannot saturate.** A condition `c` counts as **covered** by
an evidence window iff, restricted to bars labelled normal:

```
occupancy(c)   = normal bars labelled c / all normal bars in the window   >=  occupancy_min
trades_in(c)   = closed trades whose ENTRY bar is normal and labelled c   >=  trades_per_condition_min
```

and

```
normal_market_conditions_covered = | { c : covered(c) } |
```

Both floors are needed. Without `occupancy_min`, a label that occurred for six bars in a year counts.
Without `trades_per_condition_min`, a condition the strategy sat out entirely counts as "covered" —
which is the exact defect in the existing metric, where coverage is a property of the *market*, not
of the *evidence*.

Values for the two floors are per profile in `EVIDENCE_POLICY_PROFILES.md`. The owner's binding word
"**more than one** normal market condition" (decision 130) sets the floor for
`normal_market_condition_count_min` at **2**; no profile may go below it.

### b.3 How "conditions covered" is evidenced

The evidence is a file, not a claim. Per candidate, per window:

```jsonc
{
  "schema": "p021.condition_coverage/v1",
  "window": { "start": "...", "end": "...", "immutable_start_declared_at": "..." },
  "labeller": { "method_version": "rule_based_market_regime_v2",
                "lookback_bars": 42, "timeframe": "4h" },
  "dataset_hash": "sha256:...",              // §(f)
  "bars_total": 0, "bars_normal": 0,
  "excluded": { "EXTREME_MOVE": 0, "VOLUME_COLLAPSE": 0, "DATA_GAP_ADJACENT": 0,
                "STALE_PRICE": 0, "WARMUP": 0 },
  "per_condition": [ { "condition": "TRENDING", "normal_bars": 0, "occupancy": 0.0,
                       "entry_trades": 0, "covered": false, "reason": "occupancy 0.03 < 0.10" } ],
  "normal_market_conditions_covered": 0,
  "policy_set_version": "p021pol-v1:..."
}
```

The per-bar label series behind it is written out too, so the count is recomputable by a third party
from the dataset alone. A coverage claim with no recomputable label series is not evidence.

---

## (c) Divergence: metric (B-05), alignment (B-07), provenance (B-20)

Owner instruction preserved: **measure first, then set the limit.** This section defines what to
measure and how; it sets no tolerance. It also states why the measurement cannot be run today.

### c.1 The alignment method comes first, because it changes the metric (B-07)

The naive framing — "compare the backtest's results with what really happened" — cannot be made
precise, because backtest trades and forward trades are different trades taken at different times.
There is nothing to pair.

**The alignment that does work: replay the frozen strategy over the forward window itself.** Take the
identical frozen artefact (`deployment_identity_hash`), run it in simulation over exactly the bars the
forward period covered, and compare that against the forward record.

Same instruments. Same bars. Same signals. Now trades correspond one-to-one, and pairing is exact:

> A **paired observation** is one `(instrument, entry_bar_timestamp, intent_id)` that appears in both
> the replayed simulation and the forward record.

This alignment also splits the difference into two parts that mean completely different things:

| Part | What it is | Expected size | Governed by |
|---|---|---|---|
| **Decision divergence** | intents present on one side and absent on the other, or present at different bars | **zero** | already zero-tolerance under `P021.DETERMINISTIC_REPLAY` and `P021.LOOKAHEAD_PREFIX` (`intent_mismatch_count_max = 0`) |
| **Execution divergence** | the same intent, a different realised outcome — slippage, fees, queue position, partial fills | non-zero always | this is what `divergence_tolerance` is for |

Collapsing these two into one number is the mistake that makes the tolerance unanswerable. A strategy
that took *different trades* is broken; a strategy that took *the same trades slightly worse* is
normal. Only the second is a tolerance question.

### c.2 The divergence metric (B-05)

**Unit.** Per-trade net return expressed in **multiples of the trade's own declared risk unit (R)**.
Not per cent. Per cent of what is ambiguous — the research artefacts apply it to full equity because
the simulator has no sizing at all, so a percentage comparison between a sizing-free simulation and a
sized forward account measures the sizing, not the strategy.

**If a candidate declares no risk unit, R is undefined and the check REFUSES.** It does not fall back
to per cent. This is `risk_unit_source.B04`, already listed as a missing rule on
`P021.BASIC_FAILURE_FLOOR`.

**Primary statistic — one-sided standardised expectancy shift.** Over the `n` paired observations,
with `d_i = R_forward,i − R_replay,i`:

```
D1 = mean(d) / ( stdev(d) / sqrt(n_eff) )
```

Dimensionless, signed, negative when the forward side is worse. `n_eff` is a **block-corrected**
effective sample size, not `n` — see failure mode 6.

**Secondary statistic — distribution shift.** The two-sample Kolmogorov–Smirnov statistic `D2` on the
paired `R_forward` and `R_replay` samples, in `[0, 1]`. It catches a shape change with an unchanged
mean: the same average outcome delivered by a fatter loss tail.

**Third, mandatory, and not a tolerance — the cost decomposition.** For each paired observation,
`d_i` is split into `slippage_i + fee_i + timing_i + residual_i` using the recorded fills on both
sides. A divergence explained entirely by a fee schedule the replay did not know about is a
provenance defect, and it must be repaired rather than tolerated. **`residual` is the part the
tolerance applies to.**

### c.3 Failure modes, each with the guard that answers it

| # | Failure mode | Guard |
|---|---|---|
| 1 | Tiny `n` makes `D1` explode or collapse | `divergence_min_paired_observations`; below it, `BLOCKED`, never `PASS` |
| 2 | Candidate declares no risk unit | REFUSE (`risk_unit_source.B04`); no per-cent fallback |
| 3 | Replay uses a different cost model from the forward account | provenance §c.4 pins both; mismatch is `BLOCKED`, not divergence |
| 4 | Forward runs a subset of the backtest universe | alignment restricts the replay to exactly the forward instrument set; the frozen universe is declared before the window opens |
| 5 | Window chosen after seeing the outcome | immutable pre-registered start; the same rule the paper-soak lane already carries (`MASTER_..._BRIEF:3116`) |
| 6 | Nearby trades are correlated; naive `stdev/√n` understates the error | `n_eff` from non-overlapping calendar blocks of length ≥ the series' median holding time; `n_eff ≤ n` always |
| 7 | A strategy that does *better* forward gets failed | the tolerance is **one-sided** — only `D1 ≤ −tolerance` fails. A large positive `D1` raises `INVESTIGATE`, because unexplained outperformance usually means the replay is wrong |
| 8 | Fewer trades forward than replayed, so pairing succeeds on a biased subset | unpaired intents are decision divergence (§c.1) and are counted separately, at zero tolerance; they can never be dropped quietly |
| 9 | Clock skew mislabels which bar an intent belongs to | provenance records the clock source and offset on both sides; skew above one bar is `BLOCKED` |
| 10 | Replay is not deterministic, so "the same" run differs | `P021.DETERMINISTIC_REPLAY` runs first; divergence does not run until it passes |

### c.4 Provenance (B-20) — what must be on the record for the comparison to mean anything

Both sides, recorded before the comparison, never reconstructed afterwards:

| Field | Both sides? | Why |
|---|---|---|
| `deployment_identity_hash` | yes, must be **equal** | different identity ⇒ different economic system; evidence marked `PRIOR_IDENTITY` does not count |
| `dataset_hash` (§f) | yes, must be **equal** | the replay must see the bars the forward account saw |
| `cost_model_id` + fee/slippage schedule identity | yes | feeds the §c.2 decomposition |
| `policy_set.version` (§e) | yes, must be **equal** | numbers changed mid-window ⇒ two windows, not one |
| `window.start`, declared and immutable, plus the declaration timestamp | yes | failure mode 5 |
| clock source and measured offset | yes | failure mode 9 |
| `intent_stream_hash` | yes | ties the pairing to the artefact `P021.DETERMINISTIC_REPLAY` already hashes |
| instrument universe, frozen | yes | failure mode 4 |
| replay engine build identity | replay only | so the replay can itself be reproduced |

### c.5 The measurement procedure that must run before any limit is set

1. `P021.DETERMINISTIC_REPLAY` passes on the candidate — two clean runs, identical intent stream.
2. A forward window runs to completion under a pre-registered immutable plan, on a frozen universe.
3. The frozen artefact is replayed over that window's exact bars, under the same `dataset_hash`.
4. Pair by `(instrument, entry_bar, intent_id)`. Report unpaired intents on both sides **first**.
5. If unpaired intents ≠ 0 — stop. That is decision divergence and no tolerance applies to it.
6. Decompose each paired `d_i`; report `slippage`, `fee`, `timing`, `residual` separately.
7. Compute `D1` on `residual` with block-corrected `n_eff`, and `D2` on the paired distributions.
8. Repeat across every candidate that has a completed window, and publish the **distribution** of
   `D1`, `D2` and `n_eff` across candidates.
9. **Only then** is a tolerance chosen — from that distribution, as the owner instructed.

### c.6 The decision rule for the tolerance, stated now so step 9 is mechanical

No number is set here. The rule is:

> `divergence_tolerance` = the `D1` value at the **10th percentile** of the observed cross-candidate
> distribution of `D1`, from candidates whose `P021.DETERMINISTIC_REPLAY` passed and whose unpaired
> intent count was zero — floored at `−2.0` standard errors.

Rationale: it makes the tolerance a statement about the *observed* spread of honest execution
difference rather than a guess, and the `−2.0` floor stops an unusually well-behaved first cohort
from setting a tolerance so tight that ordinary slippage fails everything later.

`divergence_window_length` and `divergence_min_paired_observations` follow from cadence rather than
from the divergence measurement, and their decision rules are in `EVIDENCE_POLICY_PROFILES.md` §5.

### c.7 Why this cannot be run today

Not one of the three inputs exists.

- **No accepted engine** for step 1 beyond the synthetic-only milestone. Every check in the catalogue
  still lists `accepted_corrected_engine.B01` as a missing rule.
- **No completed forward window anywhere in the snapshot.** Across all 45 `*.readiness.json` files,
  `intake.realtime_eq_backtest` is `false` in **45 of 45**, and `monitoring.backtest_to_live_matchable`
  is `N_A` with the note *"No live comparison exists; dry-run evidence only."* in **43 of 45**. The
  remaining 2 record a signal-parity pass whose own note says *"This does not prove broker fills or
  live data-feed drift."* No file matching `*paper_soak*`, `*shadow*` or `*forward_evidence*` exists;
  the `walkforward_results.csv` files are walk-forward **optimisation over history**, not forward
  testing.
- **`dataset_hash` is never populated** (§f), so step 3's "same bars" condition cannot even be
  asserted.

**The owner's "measure first" instruction is correct and currently uncarryable.** What this section
removes is the excuse: the definitions no longer block it.

---

## (d) Gap-ratio formula (B-17)

### d.1 A naming collision that must be settled first

"Gap" means two unrelated things in this repository:

- a **data gap** — bars missing from a price history (`create_optimization_data_bundle.py:316-330`);
- a **price gap** — the jump between one bar's close and the next bar's open, a *feature* several
  strategies trade (`gap_pct_thresh` in the QuantLens prototypes, `gap_pct_min: 20` in
  `CAND_BRIAN_LEE_SMALLCAP_GAP_MR_SHORT_V1`).

`gap_ratio_max` in `P021.DATA_QUALITY` is the **first** one. The field is renamed in all new writing
to **`data_gap_ratio_max`**; the catalogue key stays `gap_ratio_max` so the existing refusal wiring
in `p021_readiness_rules.py` is untouched.

### d.2 The three sensible counting methods

Let a series have timestamps `t_0 < … < t_{m-1}`, nominal step `s`, and a gap wherever
`Δ_j = t_{j+1} − t_j > 1.5 s` (the threshold already used at `create_optimization_data_bundle.py:318`).

| Method | Formula | What it is sensitive to |
|---|---|---|
| **M1 — gap-event ratio** | `count(Δ_j > 1.5 s) / (m − 1)` | *how often* the feed broke |
| **M2 — missing-bar ratio** | `Σ_j (round(Δ_j / s) − 1) / expected_bars`, where `expected_bars = round((t_{m-1} − t_0)/s) + 1` | *how many decision opportunities* are absent |
| **M3 — missing-time ratio** | `Σ_j (Δ_j − s) / (t_{m-1} − t_0)` | *how much wall-clock time* is absent |

They disagree, badly, and by design. One three-month hole in five years of 5-minute data:
**M1 ≈ 0.000002** (one event among half a million), **M2 ≈ 4.9 %**, **M3 ≈ 4.9 %**. A limit of 1 %
passes under M1 and fails under M2 and M3 — on identical bytes. This is exactly the problem the
fifteen-numbers packet identified: *"the counting method can be chosen later to make anything pass"*.

### d.3 The chosen method: **M2, the missing-bar ratio**

Three reasons, in order:

1. **It matches what the consuming checks are indexed by.** `P021.LOOKAHEAD_PREFIX`,
   `P021.REPAINT_CLOSED_BAR` and deterministic replay all operate on *bars*: a decision per bar, an
   intent per bar. A missing bar is exactly one missing decision. A ratio in the same unit as the
   thing it protects is auditable; a ratio in a different unit needs a conversion argument every time.
2. **M1 cannot distinguish severity at all.** One missing bar and a three-month outage are one event
   each. Any limit set on M1 is a limit on feed flakiness, not on data completeness.
3. **M3 is nearly identical to M2 on fixed-step data and worse on anything else.** For a constant `s`
   they agree to within one bar per gap. They diverge for session-based instruments — where the
   overnight close is legitimately absent — and M3 would then need a session calendar the repository
   does not have. The existing US-equity-session decision (D005) means such instruments are in scope
   eventually. M2 with a session-aware `expected_bars` is a smaller change than M3 with a full
   calendar.

**M1 and M3 are still computed and published**, because the number that matters to the owner one day
is "how bad is my worst hole", and M1 answers "how often" while M3 answers "how long". Only M2 is
compared against `gap_ratio_max`.

### d.4 The exact definition, including its edges

```
data_gap_ratio(series) =
      sum over j of max(0, round(Δ_j / s) - 1)
    / (round((t_last - t_first) / s) + 1)

where  Δ_j = t_{j+1} - t_j,  counted only for  Δ_j > 1.5 s
```

- **Scope** is one `(instrument, timeframe, [t_first, t_last])` series. There is no cross-instrument
  average: averaging hides the broken one.
- **Leading and trailing absence is not a gap.** A history that starts late because the instrument
  did not exist is a shorter history, not a holed one. It is reported as `coverage_days` and judged
  by the trade-count floors, not here.
- **Duplicate timestamps are not gaps.** They are counted separately and already have their own
  zero-tolerance limit (`duplicate_timestamp_count_max = 0`).
- **`Δ_j < s`** (a bar arriving early) is an ordering fault, covered by
  `out_of_order_timestamp_count_max = 0`, not by this ratio.
- **`round`, not `int`.** `create_optimization_data_bundle.py:324` uses `int(delta / expected_step) - 1`,
  which truncates: a 1.9-step gap yields 0 missing bars. `round` yields 1, which is correct.
- The **1.5 s** detection threshold is inherited unchanged from the existing tool so the two agree.

### d.5 The defect that must be fixed before the scan is worth running

`TIMEFRAME_SECONDS = {"15m": 900, "1h": 3600, "2h": 7200, "4h": 14400, "1D": 86400}`
(`create_optimization_data_bundle.py:51`). **There is no `5m` entry.** When `expected_step` is
`None`, the gap loop at `:315` is skipped entirely and the tool reports `has_gaps: false`,
`gap_count: 0`, `expected_bars: null` — a clean bill of health produced by not looking.

This is not hypothetical. **Five of the six day-class strategies, representing 61 of 62 day-class
series, trade 5-minute bars**: CANDIDATE_008, CANDIDATE_009, HIGHBETA_PROXY, LBR_COIL, and ORB_8AM.
The sixth is STG002_ql_alpha_link_8ema_1h on 1-hour bars. CRABEL is not day-class: all 17 of its
measured series are on 1D bars and refuse as `BLOCKED_UNMEASURABLE_HOLD`
(`evidence/cadence_measurements.json`; `evidence/cadence_tables.md:6,15-16,23-29,36,46`). The gap scan
is therefore blind on **5/6 day strategies (61/62 day series)** — exactly the timeframe where most of
the fastest strategies live. Also missing: `1m`, `5m`, `30m`, `6h`, `12h`, `1W`.

**An unknown timeframe must raise, not return silently.** Fail-closed, like everything else in this
package.

### d.6 The scan that must run before the owner sees a number

1. Fix `TIMEFRAME_SECONDS` (add the missing steps; raise on unknown). Fix `int` → `round`.
2. Enumerate every `(instrument, timeframe)` series any catalogued candidate depends on.
3. For each, compute M1, M2 and M3, plus `coverage_days`, the largest single gap in bars, and the
   date of that gap. Record `dataset_hash` (§f) alongside each.
4. Publish the **distribution of M2** across series, plus the ten worst series named individually.
5. **Only then** is `gap_ratio_max` chosen.

**Decision rule, stated now so step 5 is mechanical:**

> `gap_ratio_max` = the smallest value that admits at least 80 % of the scanned series, rounded up to
> the next 0.1 %, and never above 5 %.

Rationale: it is set from the data as instructed, it keeps the research pipeline alive (the
fifteen-numbers packet's "too low" failure), and the 5 % hard cap stops a badly holed corpus from
ratifying its own poor quality (the "too high" failure). If the 80 % rule and the 5 % cap conflict,
that is a finding about the data, not a number to relax: the scan output says so and the limit is not
set.

**Not run in this lane.** No `*_gaps.csv` exists anywhere in the snapshot, and running the bundle
tool would be a data-producing run this lane has no authority for.

---

## (e) Policy-version contracts

### e.1 Reuse, do not invent

The repository already has an immutable, hashed, versioned policy object with a fail-closed consumer:
`DurableRiskPolicy` (`IBKR_PAPER_BRIDGE/bridge/engine/types.py:1327-1378`) and its sibling
`ExposureRiskPolicy` (`:1381`). The construction is:

```python
payload = json.dumps({...values as float.hex()...}, sort_keys=True, separators=(",", ":"))
version = f"rpol-v1:{hashlib.sha256(payload.encode('utf-8')).hexdigest()}"
```

and the consumer refuses to carry state across a version change —
`if daily_state.policy_version != self.policy.version:` (`bridge/engine/risk.py:153`), and the same
for the exposure policy at `:182`. The header comment at `risk.py:51-53` states the intent verbatim:
*"Versioned configuration values, not permanent constants: a later owner-approved change creates a
new immutable ExposureRiskPolicy version."*

That is exactly what B-22 asks for. **P0-21 adopts the identical construction** with the prefix
`p021pol-v1:`. W297 §9 requires one mechanism across P0-20 and P0-21; this satisfies it.

### e.2 The five contract rules

1. **Canonical serialisation.** `json.dumps(sort_keys=True, separators=(",", ":"))`, every float as
   `float.hex()`. Float text formatting is not stable across languages; the hex form is exact. Copied
   from `types.py:1361-1370` rather than re-derived.
2. **Hash covers everything, including the profile name and the taxonomy constants.** Changing
   `dominance_min` from 0.80 to 0.75 changes the version, because it changes which candidates are
   which type, which changes which numbers apply to them.
3. **Pinning.** Every readiness result records the `policy_set.version` it was judged under. A result
   whose version differs from the current policy is `EXPIRED`, not `PASS` — the same treatment
   `PRIOR_IDENTITY` evidence gets at the live gate. A change to any number therefore requires fresh
   relevant evidence, which is the rule decision 129/130 demanded (`W297_P021_FOLD_REPORT.md` §6).
4. **Consumption without defaults.** `p021_readiness_rules.py` must take the policy set as a
   **required argument**. Concretely, extending its existing `validate_catalog()`:
   - every name in `EXPECTED_OPEN_NUMBER_NAMES` must be present as a key — a *missing key* is a
     catalogue error and raises;
   - a key whose value is `null` is *unset*, and every rule wired to it emits `REFUSED` with the
     existing `_refusal()` reason string;
   - there is no `dict.get(name, default)` anywhere in the module, no `or` fallback, no environment
     variable, and no per-type inheritance;
   - the current `self_check()` already proves a **modified copy** is detected (it removes
     `gap_ratio_max` from the refusal wiring and asserts the failure). One test is added per number:
     with that number set and every other unset, exactly the rules wired to it change status, and the
     overall record stays `ready: False`.
5. **Owner-set values carry provenance, engineering-set values carry a derivation.** The `provenance`
   block distinguishes them, so a later reader can tell `day.trade_count_min = 30` (the owner's
   provisional policy v1) from a value engineering computed. Neither may be edited without a new
   version.

### e.2a The contract demonstrated, minting no value

`tools/policy_set_demo.py` builds the policy set with **all fourteen catalogue numbers `null`** —
carrying only the two decisions the owner has already made and asked to have preserved — and proves
the three properties by running them (`evidence/policy_set_demo.txt`,
`evidence/policy_set_unset_example.json`):

```
PROPERTY 1  version stable under recomputation                      True
PROPERTY 2  taxonomy.dominance_min 0.80 -> 0.75  version differs     True
            types.swing.trade_count_min null -> 30  version differs  True
            shared.stop_loss_ceiling null -> 0.005  version differs  True
PROPERTY 3  catalogue numbers total 14, still unset 14, defaults 0
```

Unset version: `p021pol-v1:e5aa48468911d42347e033037f4f12bd7de39e94f89a99f721d9daec8084cda0`.
The demo selects no value; it is evidence that the contract is implementable and fail-closed, not a
proposed policy.

### e.2b The current module already satisfies rule 4, verified by running it

`tools/verify_upstream_catalogue.py` extracts the blob from `a63bd4b0` into `OUTPUT_ROOT`
(sha256 `54a5a91113d17752613a21c21dc72c543f867d863545825a8c7a131a972c80ec`, 10 780 bytes, 243 lines)
and runs it (`evidence/upstream_verification.txt`):

```
SELF-CHECK PASS: 7 checks all refuse readiness
OPEN NUMBERS: 14
MODIFIED COPY DETECTED: gap_ratio_max refusal wiring removed
READY=False                                     exit=0

checks 7 · open numbers 14 · REFUSED 7 of 7 · ready False
implementation_authorized False · accepted_engine_precondition NOT_MET_OVERRIDDEN_FOR_THIS_BOUNDED_BUILD
blockers on the open numbers: B-02 B-03 B-04 B-06 B-07 B-10
occurrences of '.get(' 0 · 'default=' 0 · 'os.environ' 0 · 'getenv' 0
```

(The four occurrences of `" or "` are inside question and display strings —
`", ".join(...) or "none"` in `_print_owner_view` and the refusal text — not value fallbacks.)

So the module has no default today. Rule 4 is a constraint on the change that adds the policy-set
argument, not a repair of a present defect.

### e.3 What is versioned besides the numbers

Three method identities travel with the policy set, because a number means nothing without the method
that produced the quantity it limits:

| Identity | Current value | Consumed by |
|---|---|---|
| `regime_method_version` | `rule_based_market_regime_v2` (v1 exists, §b.2 addition 2) | `normal_market_condition_count_min` |
| `gap_method_version` | `data_gap_ratio_m2_v1` (§d.4) | `gap_ratio_max` |
| `divergence_method_version` | `p021_divergence_v1` (§c.2) | `divergence_tolerance` |

Changing a method version changes the policy-set version, which expires the evidence. That is
intended: a tolerance measured with one metric is not a tolerance for another.

---

## (f) Dataset hash contract (B-13)

### f.1 What exists

The field already exists and is already carried end to end. `BacktestResult.dataset_hash: str | None`
(`01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:110`), emitted into every optimizer row
(`:122`), and required to be preserved by
`01_MTC_PROJECT/docs/optimization/OPTIMIZER_INFRASTRUCTURE_RULES.md:23`: *"Result rows must preserve
`config_hash`, `dataset_hash`, `dataset_id`, and `run_id` where available."*

**And it is never computed.** The only assignments in the snapshot are two test fixtures —
`dataset_hash="data"` and `dataset_hash="hash"` (`mtc_v2/tests/test_runner_metrics_api.py:27,118`).
No production code path produces a value; `P021.DATA_QUALITY` sets `dataset_hash_required: True` and
therefore refuses.

**So B-13 is a missing construction, not a missing field.** This design defines the construction and
adds no new field, per the spec's instruction to reference existing definitions rather than duplicate
them.

### f.2 The construction

```
dataset_hash = "ds-v1:" + sha256( canonical_bytes )
```

where `canonical_bytes` is, in order and with no separators beyond those shown:

```
"p021.dataset/v1\n"
instrument_id            "\n"     # exchange-qualified, e.g. BINANCE:BTCUSDT
timeframe                "\n"     # canonical token: 1m 5m 15m 30m 1h 2h 4h 6h 12h 1D 1W
first_timestamp_utc      "\n"     # RFC3339, UTC, whole seconds
last_timestamp_utc       "\n"
row_count                "\n"
then, for each row in ascending timestamp order:
    timestamp_utc "," open.hex() "," high.hex() "," low.hex() "," close.hex() "," volume.hex() "\n"
```

**Every choice, with its reason.**

| Choice | Reason |
|---|---|
| `float.hex()` for all six numeric fields | exact and language-stable; the same convention `DurableRiskPolicy` already uses (`types.py:1364-1366`). Decimal text differs by formatter and by locale. |
| ascending timestamp order, enforced | the hash must not depend on file ordering; ordering faults are already zero-tolerance under `out_of_order_timestamp_count_max = 0` |
| instrument, timeframe and the window bounds inside the preimage | two different slices of one feed must not collide; `dataset_id` alone is a name, not an identity |
| `row_count` inside the preimage | a truncated file cannot collide with its own prefix |
| no adjustment factors, no cost model, no strategy parameters | those belong to `config_hash` and `deployment_identity_hash`. One hash, one meaning. |
| `ds-v1:` prefix | the algorithm is versioned; a future change produces `ds-v2:` and does not silently invalidate stored evidence |
| **derived columns excluded** | indicators are recomputable from OHLCV; including them would make the hash depend on the indicator library version |

### f.3 Who computes it and when

At **bundle build time**, once, by the producer that already scans the file for duplicates, ordering
and OHLCV validity (`create_optimization_data_bundle.py`) — the same pass, no second read. It is
written into the bundle manifest beside the existing `expected_bars`, `gap_count` and
`duplicate_timestamp_count` fields, and the values of M1/M2/M3 from §(d) are recorded next to it, so
a series' identity and its quality travel together.

Every consumer takes the hash as given and **verifies rather than recomputes** when it must: recompute
on ingest, compare, and refuse on mismatch. A consumer that recomputes silently and proceeds turns a
tamper signal into a no-op.

### f.4 What it is not

`dataset_hash` is **not** `deployment_identity_hash`. The live gate binds evidence to the second one
(`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:3116`), which additionally covers the
allocator, Guardian policy, risk-bucket policy, runtime policy, protection semantics, broker adapter
and cost lineage. `dataset_hash` answers exactly one question — *were these the same bars?* — and it
is one input to that larger identity. Conflating them would let a policy change hide behind unchanged
data.

---

## Open engineering items this design does not close

| Item | Why it stays open | Who |
|---|---|---|
| B-01 accepted corrected engine | accepted as a **synthetic-only milestone** only (OD-20260906-2); production economics stay fail-closed, and every check in the catalogue still lists `accepted_corrected_engine.B01` as missing | not this lane |
| B-08 `state_allowance_matrix`, B-19 `control_hash_contract` | `P021.UNSIMULATED_CONTROLS` prerequisites; untouched by OD-20260906-6 | P0-21 engineering |
| B-12 `decision_domain`, B-21 `intent_hash_contract`, B-16 `forming_bar_runtime_proof` | replay/repaint prerequisites; §(c) depends on B-21 for `intent_id` and consumes it rather than defining it | P0-12 / P0-21 |
| B-09 testnet leg result ids, producers, carriers | carried forward unchanged from v1.11 (`W297_P021_FOLD_REPORT.md` §8) | P0-21 engineering |
| Merging `p021_readiness_rules.py` to the main line | it is on an unmerged branch; nothing in this design changes that | Lead |
