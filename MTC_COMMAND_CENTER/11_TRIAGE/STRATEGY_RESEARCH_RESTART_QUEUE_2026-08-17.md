# Strategy Research Restart Queue — 2026-08-17

> **Status:** evidence-based planning record only. No preregistration, strategy
> implementation, Pine/MTC change, data download, backtest, paper trade, or live
> action is authorized by this report.
>
> **Scope:** the smallest useful restart packages supported by current repository
> evidence. The purpose is to avoid spending time on deterministic reruns or on
> strategies whose required data or definitions do not yet exist.

## 1. Current evidence changes the restart plan

The correct next step is **not** to rerun the existing strategy library:

- The completed multi-asset run evaluated 20 strategies across 51 symbols and
  seven timeframes (7,140 rows) and found `robust_final=0`:
  `MTC_COMMAND_CENTER/05_REGISTRY/RESEARCH_RUN_REGISTRY.json:4-18`.
- The historical roadmap consequently identifies **new strategy logic** as the
  productive path and warns that deterministic re-sweeps return the same null
  evidence:
  `MTC_COMMAND_CENTER/_AI_MEMORY/archive/NEXT_STEPS_pre-2026-08-01.md:732-734`.
- The runbook records that deterministic repetition creates zero new information:
  `MTC_COMMAND_CENTER/11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md:398` and `:456`.
- A single-cell survivor is insufficient; cross-symbol consistency requires at
  least five cells:
  `MTC_COMMAND_CENTER/11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md:187` and `:240`.

## 2. Fastest safe order

1. Reconcile the historical research truth ledger.
2. Freeze the LBR Three-Bar Breakout research question and obtain the owner choice
   on long-only versus symmetric long/short scope.
3. After explicit approval, implement and validate that one narrow package.
4. Run its seven-cell governed discovery only after its preregistration and gates
   are complete.
5. Consider the ROC2 overlay only if the Three-Bar baseline justifies it.
6. Prepare the daily price-volume/VCP lane only after its data and definition gaps
   are resolved.

## 3. Restart packages

### Package 0 — historical research truth ledger

**Classification:** safe preparation; documentation/evidence work; no compute.

**Problem discovered**

`RESEARCH_RUN_REGISTRY.json` records completed runs, including the 7,140-row
multi-asset sweep and FAZ3B Stage 1:
`MTC_COMMAND_CENTER/05_REGISTRY/RESEARCH_RUN_REGISTRY.json:4-30`.
However, the companion backtest registry is empty:
`MTC_COMMAND_CENTER/05_REGISTRY/RESEARCH_BACKTEST_REGISTRY.json:1-5`.
The strategy workflow requires both run and backtest summaries to be registered:
`MTC_COMMAND_CENTER/_AI_MEMORY/STRATEGY_RESEARCH_WORKFLOW.md:37-38`.

This gap makes it too easy to repeat an old experiment and too easy to undercount
the historical trial family used by DSR.

**Safe next deliverable**

Build an artifact-level ledger from existing accepted result files. Each unique
evaluation should record at least:

- strategy and variant identity;
- symbol and timeframe;
- literal parameter values;
- data file hash and scored observation window;
- exit mode and cost model;
- artifact path and run identity;
- disposition: null, research-only, rejected, blocked, or eligible for a genuinely
  new follow-up.

Deterministic duplicates may be marked as duplicates only when their complete
identity tuple matches. Registry absence is not evidence that an evaluation did
not occur; the FAZ3B forward preregistration explicitly requires an artifact scan:
`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE2_FORWARD_CONFIRM_PREREG_2026-07-13.md:114-127`.

**Risk and gates**

- Expected tier: T2 evidence package.
- No strategy code, data acquisition, or backtest is needed.
- Registry edits, if later authorized, must be reviewed against the artifact
  ledger rather than inferred from filenames alone.

### Package 1 — LBR Three-Bar Breakout, 4h US-equity discovery

**Classification:** highest-value genuinely new research candidate.

**Exact evidence-supported scope**

| Field | Proposed frozen value |
|---|---|
| Candidate | `QL_LBR_THREE_BAR_BREAKOUT_v0` |
| Timeframe | `4h` / source `240m` |
| Universe | `AAPL`, `MSFT`, `NVDA`, `AMZN`, `TSLA`, `GOOGL`, `META` |
| Data | `native_multiasset_alpaca_2026-06-28` primary bundle |
| First baseline exit | canonical engine fixed 2R, if the owner selects the smallest scope |
| Promotion status | research only; no automatic Pine/MTC/Bridge promotion |

The source gives a compact objective pattern:

- current bar range is inside the combined high/low range of the prior two bars;
- long trigger breaks above the three-bar high;
- short trigger breaks below the three-bar low;
- supported timeframes are `1D` and `240m`.

Evidence:
`MTC_COMMAND_CENTER/03_QUANTLENS/00_INBOX_REPORTS/3 Mayıs/2026-05-03_kTqKRi-j9kM_quantlens_linda_raschke_sell_rules_trade_management_intake.md:271-307`.
The source further describes it as easy to code and compare with simple inside-bar
baselines at `:309-311`.

**Data sufficiency**

The seven proposed 4h files are all Alpaca IEX, RTH-only, adjusted, volume-bearing,
OHLCV `PASS`, and contain 1,990 bars:

| Symbol | Manifest evidence |
|---|---|
| AAPL | `MTC_COMMAND_CENTER/03_QUANTLENS/data/native_multiasset_alpaca_2026-06-28/manifests/dataset_manifest.json:616-624` |
| MSFT | same manifest `:742-750` |
| NVDA | same manifest `:868-876` |
| AMZN | same manifest `:994-1002` |
| TSLA | same manifest `:1120-1128` |
| GOOGL | same manifest `:1246-1254` |
| META | same manifest `:1372-1380` |

The engine minimum is 1,500 bars:
`MTC_COMMAND_CENTER/11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md:182`.
The primary bundle selection rule and full bundle description are at
`MTC_COMMAND_CENTER/03_QUANTLENS/data/README.md:22-26`.

**Required preregistration and gates**

Before implementation or execution, freeze:

1. long-only partial discovery or faithful symmetric long/short scope;
2. exact inside-range equality rules and breakout fill convention;
3. optional ATR-compression and market-regime filters as OFF for the first
   baseline, or include them as a separately counted trial family;
4. one exit contract; do not compare every listed exit without accounting for
   the enlarged search family;
5. fixed universe, timeframe, costs, warmup, folds, lockbox, minimum trades and
   STOP rules;
6. variant identity in `VARIANT_LOG_REGISTRY.json` as required by
   `MTC_COMMAND_CENTER/_AI_MEMORY/STRATEGY_RESEARCH_WORKFLOW.md:30-31`.

If approved, the implementation should be isolated from Pine, MTC, Bridge and the
frozen V1 deployment lane. Local non-economic strategy-runner work is expected to
be T1 after Gate-1 classification. Any shared short-side engine change needs its
own explicit protected-scope approval and review.

Execution evidence must include the complete mandatory research gates described
in section 4 below. A one-cell smoke may verify plumbing but cannot support an
edge claim.

### Package 2 — LBR ROC2 as a paired incremental filter

**Classification:** conditional follow-up; do not run before Package 1.

**Exact proposed scope**

- Candidate/module: `QL_LBR_ROC2_REVERSAL_v0`.
- Role: a timing filter over the frozen Package-1 Three-Bar baseline, not a
  standalone oscillator strategy.
- Data/universe/timeframe: the identical seven US-equity symbols and 4h files
  from Package 1.
- Comparison: paired baseline versus baseline-plus-ROC2 under identical execution,
  cost and observation contracts.

The source supports 1D/240m and describes the two-period ROC reversal at
`MTC_COMMAND_CENTER/03_QUANTLENS/00_INBOX_REPORTS/3 Mayıs/2026-05-03_kTqKRi-j9kM_quantlens_linda_raschke_sell_rules_trade_management_intake.md:429-467`.
It explicitly warns that ROC2 is a **timing filter, not a complete strategy** at
`:469-471`.

**Unresolved definitions**

The owner-approved preregistration must define before results are visible:

- “support or prior low nearby” and its short-side mirror;
- “ATR not extreme”;
- exact ROC2 turning condition;
- whether the package is symmetric or long-only;
- the paired trial family and acceptance rule.

**Risk and dependency**

- Depends on Package 1 producing a valid baseline, not necessarily a profitable
  one, that makes the incremental question meaningful.
- Strategy implementation and any run require explicit approval and T1 review.
- A negative result closes this exact overlay; it does not authorize another
  threshold search on the same evidence.

### Package 3 — daily price-volume quality filter plus VCP breakout

**Classification:** high-value future package; currently data- and
definition-blocked.

**Proposed research question**

Does the David Ryan price-volume accumulation/distribution module improve a
daily VCP/base-breakout baseline on the same seven liquid US stocks?

Candidate pair:

- `QL_CAND_2026-05-03_eWtY7uoJL0_RYAN_PRICE_VOLUME_STAGE` as a pattern-quality
  filter;
- `QL_VCP_BREAKOUT_DAILY_BASE_001` as the base producer.

Both have source/formula records but remain `NEEDS_CLARIFICATION`:
`MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/NEEDS_BACKTEST_SELECTOR.md:32`
and `:73`.

The Ryan strategy record identifies price-volume accumulation as its most reusable
element and describes higher-volume advances, lower-volume pullbacks, volume dry-up
and volume-spike breakout confirmation:
`MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG051_david_ryan_price_volume_stage/07_deterministic_spec.md:5-22`.
Its intended entry/exit skeleton and the requirement to define volume thresholds
objectively appear at `:26-40`.

**Data insufficiency today**

The primary bundle supplies adjusted daily volume, but the proposed stock daily
files contain only 1,487 bars. AAPL is representative:
`MTC_COMMAND_CENTER/03_QUANTLENS/data/native_multiasset_alpaca_2026-06-28/manifests/dataset_manifest.json:634-642`.
That is below the engine minimum of 1,500 bars
(`BACKTEST_OPTIMIZATION_RUNBOOK.md:182`). Therefore this package must not be run
against the present daily files.

**Safe preparation**

- specify a data-extension plan preserving provider, adjustment, session,
  timestamps and hashes;
- draft alternative objective definitions for volume expansion/dry-up, tight
  base, stage filter and exit;
- present those alternatives for owner selection before implementation.

**Approval boundary**

- External data download and any credential-handling route need separate explicit
  approval and T0 treatment.
- After data is frozen, offline strategy implementation remains a separate T1
  package.
- No result may be produced until the data and strategy preregistrations are both
  closed.

## 4. Mandatory gates for every authorized backtest package

Every future execution package must satisfy the canonical rules. At minimum:

1. physical data validation and an explicit `MEGA_BUNDLE_MANIFEST`; the default
   engine manifest is legacy and must not be trusted for new work
   (`BACKTEST_OPTIMIZATION_RUNBOOK.md:66-67`, `:145`);
2. explicit symbol and timeframe selection, because the manifest does not itself
   replace the hardcoded sweep universe (`BACKTEST_OPTIMIZATION_RUNBOOK.md:404`);
3. versioned variant registration
   (`STRATEGY_RESEARCH_WORKFLOW.md:30-31`);
4. next-bar execution, costs/slippage, warmup, rolling walk-forward, locked OOS and
   lockbox contracts frozen before results;
5. minimum trade count and cross-symbol consistency across at least five cells;
6. same-window buy-and-hold, strategy return and excess alpha reported separately
   (`07_BACKTEST_AND_OPTIMIZATION_RULES.md:83-96`);
7. bootstrap, BH-FDR, DSR and multi-window evidence
   (`07_BACKTEST_AND_OPTIMIZATION_RULES.md:50-51`, `:166-175`);
8. CPCV and PBO when enough history exists, with failure blocking promotion above
   research/sandbox status (`07_BACKTEST_AND_OPTIMIZATION_RULES.md:169-175`);
9. closed-bar signals and shifted rolling levels to prevent repaint/lookahead
   (`MTC_COMMAND_CENTER/_AI_MEMORY/STRATEGY_CODE_REVIEW_CHECKLIST.md:7-9`);
10. run and result registration
    (`STRATEGY_RESEARCH_WORKFLOW.md:37-38`);
11. a plain-language morning report that distinguishes `robust_final` from weaker
    discovery or research-only labels;
12. no Pine, MTC, Bridge, paper, testnet or live integration from research evidence
    without the later explicit gates for those surfaces.

Wide post-hoc grids are not a substitute for confirmation. The runbook requires
broad discovery to be followed by a narrow preregistered confirmation grid:
`MTC_COMMAND_CENTER/11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md:396` and `:400`.

## 5. Owner choices that materially change the plan

1. **Research destination:** should the immediate research remain source-faithful
   US equities, or should all new work be restricted to eventual Hyperliquid-
   compatible crypto? The proposed queue starts with US equities because that is
   where the selected source and sufficient data align.
2. **Three-Bar direction:** faithful symmetric long/short, or smaller long-only
   discovery explicitly labelled partial?
3. **Three-Bar exit:** canonical fixed 2R first, or another source-listed exit?
   Multiple exits create a larger trial family and must be counted accordingly.
4. **ROC2 definitions:** exact support/resistance proximity, ATR-extreme threshold,
   turning rule and direction.
5. **Daily-data extension:** approve or decline acquisition of sufficient daily
   US-equity history.
6. **Price-volume/VCP formulas:** exact volume comparison window, volume-spike
   threshold, tight-base definition, stage filter and exit.

No owner choice should be inferred after performance results are visible.

## 6. Do not restart

| Item | Why it should not be restarted | Evidence |
|---|---|---|
| US-equity 10m 8EMA | Complete parameter sweep was negative and the strategy was shelved | `MTC_COMMAND_CENTER/_AI_MEMORY/archive/NEXT_STEPS_pre-2026-08-01.md:786` |
| Existing 20-strategy multi-asset library | 7,140 rows, `robust_final=0`; deterministic rerun adds no information | `MTC_COMMAND_CENTER/05_REGISTRY/RESEARCH_RUN_REGISTRY.json:4-18`; archive `NEXT_STEPS...md:732-734` |
| Donchian Turtle structural-stop variant | Full 357-cell plus deep CPCV/PBO run found no systematic edge | archive `NEXT_STEPS...md:728-730` |
| LBR coil breakout | Already coded and evaluated, including CPCV; it is not a new candidate | `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/batch023_034_2026-06-07/MEGA_walk_forward_report.md:110,367`; `cpcv/CPCV_VALIDATION_REPORT.md:90` |
| Oliver Kell / STG056 | Already coded and swept; DSR remained near zero and it was not promoted | archive `NEXT_STEPS...md:942-947` |
| FAZ3B Keltner Stage 2 today | Future-data design is frozen; earliest evaluation is 2028-07-14 and current authority is passive accrual only | `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE2_FORWARD_CONFIRM_PREREG_2026-07-13.md:3-10`, `:270-278` |
| STG035 RSI confluence or STG041 EMA channel unchanged | Both are already engine baselines in the previously completed library; unchanged reruns are deterministic repeats | `MTC_COMMAND_CENTER/05_REGISTRY/STRATEGY_PARAM_SPECS.json` entries for the exact strategy IDs; completed library evidence above |

## 7. Bottom line

The fastest evidence-producing restart is:

**historical truth ledger → LBR Three-Bar owner decision and preregistration → one
isolated approved implementation → one governed seven-symbol 4h discovery → only
then a paired ROC2-filter decision.**

The daily price-volume/VCP package should remain in preparation until sufficient
daily data and objective formulas are frozen. Nothing in this queue is a trading,
promotion, Pine/MTC, Bridge, paper, testnet or live authorization.
