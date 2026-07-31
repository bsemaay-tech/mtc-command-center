# FAZ 3B Stage-2 Gate-5 Adversarial Findings

**Reviewer:** Codex GPT-5
**Date:** 2026-07-13
**Target:** `00_AGENT_PROTOCOLS/FAZ3B_STAGE2_CONFIRM_PREREG_2026-07-13.md`
**Overall verdict:** **FATAL — D016 must not be issued against the current draft.**

This is a paper-only adversarial review. **No backtest, smoke test, runner, CPCV,
PBO, multi-window tool, pytest suite, or strategy process was executed.** I read
source and existing JSON/Markdown artifacts only.

The two decisive breaks are independent:

1. All six proposed decision symbols already have `GEN_KELTNER_BREAKOUT` 1h
   results on the same 2020-07-27 through 2026-06-26 observations. They are not
   held out.
2. The current CPCV and multi-window tools do not pass `exit_mode` to
   `simulate_slice`, whose default is `fixed_2R`. They therefore cannot validate
   a `trail_ema8` candidate as specified. The PBO tool also consumes rows across
   cells, not a per-configuration return matrix for one cell.

“FATAL” below means the present pre-registration cannot receive D016 until the
listed edit is applied and re-reviewed; it does not mean the research question
itself is permanently invalid.

## A. Winner-extraction correctness — FINDING

The winner itself is correct. The raw Stage-1 row is
`GEN_KELTNER_BREAKOUT/AAPL/1h/trail_ema8`, has `trial_count=5`, and gives
`best_params={ema_len:50, atr_len:10, mult:2.0}`
(`03_QUANTLENS/research/faz3b_stage1_20260705/pass2_1h/MEGA_walk_forward_results.json:44775-44790`).
The same row is `STRONG_PASS`, `grid_stride=3`, `dsr_p_value=0.6201`, and not a
BH-FDR survivor (`.../MEGA_walk_forward_results.json:44860-44867`). Its lockbox
values are 49 trades, +19.038%, PF 1.873, maxDD -6.826%, and sharpe_pt 0.193729
(`.../MEGA_walk_forward_results.json:44807-44821`). The fixed-2R twin is 25
trades and `INSUFFICIENT_TRADES` (`.../MEGA_walk_forward_results.json:44617-44631,44670-44677`).

The stride artifact is real. The engine selects
`grid[::3][:len(grid)//3]`, so 16 entries yield exactly 5, not 6
(`03_QUANTLENS/tools/mega_walk_forward.py:131-141`). With the original grid order
(`mega_walk_forward.py:316-322`), Stage-1 evaluated indices 0, 3, 6, 9, and 12.
The proposed 12-set grid contains only four of those (0, 6, 9, 12); **8/12
Stage-2 configurations were never evaluated in Stage-1**. Calling all 12
“winner neighbors” conceals new discovery degrees of freedom.

## B. Grid narrowness honesty — FATAL

The proposed Cartesian grid is 12/16 = **75%** of the original search space
(`FAZ3B_STAGE2_CONFIRM_PREREG_2026-07-13.md:73-104`). It chooses the best of 12
at each row, so it is a fresh optimization with only `mult=3.0` removed, not a
fixed-candidate confirmation. Eight of the 12 configurations were unseen in
Stage-1, as shown in A. A neighborhood-stability diagnostic does not require
allowing cross-term configurations to replace the frozen winner.

A confirmatory design can score the frozen winner as the decision configuration
and use a one-axis star only as non-selecting sensitivity evidence:

| Role | `ema_len` | `atr_len` | `mult` |
|---|---:|---:|---:|
| Decision configuration | 50 | 10 | 2.0 |
| Diagnostic neighbor only | 20 | 10 | 2.0 |
| Diagnostic neighbor only | 50 | 20 | 2.0 |
| Diagnostic neighbor only | 50 | 10 | 1.5 |
| Diagnostic neighbor only | 50 | 10 | 2.5 |

The four diagnostics must not replace the decision configuration or rescue a
failed primary result. If best-of-12 selection is retained, the document must
say “Stage-2 discovery” and require a later untouched confirmation; it cannot
award `robust_final` here.

## C. Held-out genuineness — FATAL

The central virginity claim at pre-reg lines 62-71 is false. The existing
`03_QUANTLENS/05_BACKTEST_RESULTS/overnight_multiasset_2026-06-29/MEGA_walk_forward_results.json`
contains `GEN_KELTNER_BREAKOUT` 1h rows for **every proposed decision symbol**,
each with 16 trials and the same observation window:

| Symbol | Existing JSON evidence | Rows | Window | Prior trials |
|---|---|---:|---|---:|
| AMD | `.../MEGA_walk_forward_results.json:486500-486506` | 8,877 | 2020-07-27 14:00 to 2026-06-26 19:00 UTC | 16 |
| DIA | `.../MEGA_walk_forward_results.json:491163-491169` | 8,852 | same | 16 |
| GOOGL | `.../MEGA_walk_forward_results.json:496041-496047` | 8,876 | same | 16 |
| IWM | `.../MEGA_walk_forward_results.json:497956-497962` | 8,884 | same | 16 |
| META | `.../MEGA_walk_forward_results.json:500145-500151` | 8,876 | same | 16 |
| NFLX | `.../MEGA_walk_forward_results.json:501294-501300` | 8,877 | same | 16 |

Those rows are fixed-2R and `INSUFFICIENT_TRADES` (21-25 lockbox trades in the
parsed rows). Symbol-newness is therefore absent, not merely weakened by
correlation. The registry did not protect against this: it lists only five
research runs (`05_REGISTRY/RESEARCH_RUN_REGISTRY.json:6-65`) and omits the
June-29 artifact. The pre-launch registry check was not an exhaustive evidence
inventory.

Even without the direct collision, DIA/IWM share the same market regime as
SPY/QQQ and the four stocks are tech/growth-clustered. “At least one of six” can
therefore succeed on one correlated regime rather than independent
generalization. A genuine confirmation should require an untouched temporal
window or dataset frozen before inspection, and confirmation from at least two
predefined diversity groups.

## D. Trial arithmetic and family completeness — FATAL

The displayed arithmetic is internally correct:

`16 + (3 × floor(16/3)) + (4 × floor(16/3)) + (14 × 12)`
`= 16 + 15 + 20 + 168 = 219`.

The five-trial Stage-1 count is real, not convenient reconstruction: the Stage-1
pre-reg specified the capped floor selector (`FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md:41-50`),
the engine implements it (`mega_walk_forward.py:131-141`), and the AAPL rows
stamp `trial_count=5` and `grid_stride=3` (Stage-1 JSON:44591,44673 and
44781,44863).

The **family is nevertheless incomplete**. The exact six proposed cells already
contributed at least `6 × 16 = 96` Keltner trials in the June-29 artifact. Under
the draft's own additive convention, `219 + 96 = 315` is only a lower bound,
before classifying numerous older Keltner result artifacts. A read-only scan
found `GEN_KELTNER_BREAKOUT` in many unregistered June result files; the five-run
registry is not an adequate family ledger. Every inspected/reported Keltner
search that influenced continuation must be inventoried, deduplicated, and
included or explicitly excluded with a statistical reason.

The claim that N=219 “already pays” for selecting the maximum over six cells is
also unsupported (`FAZ3B_STAGE2_CONFIRM_PREREG_2026-07-13.md:183-197`). The DSR
function deflates one observed Sharpe using a trial count; it does not perform a
six-cell maximum test (`mega_walk_forward.py:1507-1525`). A mechanical 6-way
Bonferroni confidence rule would be:

`du_family = 1 - min(1, 6 × (1 - du_cell))`, require `du_family >= 0.95`,
which is equivalent to `du_cell >= 0.9916667` for a one-cell success. Requiring
confirmations in at least two predefined, non-overlapping diversity groups is a
useful additional generalization condition, not a substitute for complete trial
accounting.

## E. Union-DSR reproducibility — FATAL

The Stage-1 report supplies inputs and a prose pool description, but no exact
formula, inclusion manifest, missing-row policy, sample-standard-deviation
choice, or rounding order (`03_QUANTLENS/research/faz3b_stage1_20260705/STAGE1_REPORT.md:54-61`).
Two independent implementers cannot reproduce four decimals from pre-reg lines
138-143.

The engine's actual convention is precise: Euler-Mascheroni expected-maximum
Sharpe, default skew 0 and kurtosis 3, denominator based on `n_trades-1`, and a
normal CDF (`mega_walk_forward.py:1507-1525`). Its pool uses selected
`best_train_sharpe_pt` values, excludes `NO_DATA/ERROR/SKIPPED_RULE`, and uses
`np.std(..., ddof=1)` (`mega_walk_forward.py:1678-1695`). The pre-reg neither
copies these conventions nor identifies the exact rows in its cross-run pool.
Pooling 10m and 1h selected-winner Sharpe values also mixes horizons without a
written justification.

Finally, the `du(trail)-du(fixed) >= 0.10` rule has no sampling-error or economic
calibration. A difference between two nonlinear confidence transforms is not
evidence that the exit itself added return. The safe categorical rule is:
trail clears and fixed does not = EXIT-INCREMENTAL; both clear = POCKET-ONLY.
Remove the decorative 0.10 escape hatch unless a paired, pre-specified return
difference test is added and independently reviewed.

## F. CPCV gauntlet feasibility — FATAL

There are 6 groups and `C(6,2)=15` test-group combinations. With about 8,850
bars, each group is about 1,475 bars and each two-group test covers about 2,950.
The existing AAPL trail row has 49 trades in the terminal quarter (about 2,219
bars), so enough trades are plausible, but cannot be guaranteed from aggregate
counts. A 70% threshold means at least **11/15** splits must pass.

The Donchian artifact does not demonstrate fold infeasibility. It says
“Candidates evaluated: 0” (`donchian_crypto_ladder_2026-07-13/cpcv/CPCV_VALIDATION_REPORT.md:3-8`)
and its JSON is an empty result list (`.../cpcv/cpcv_results.json:1-4`) because
the source had no PASS/STRONG_PASS row. The validator prefilters exactly those
classifications (`03_QUANTLENS/tools/cpcv_validator.py:59-62`). No Donchian CPCV
split was evaluated.

More importantly, the validator is not exit-aware. It reads `best_params` but
not `exit_mode` (`cpcv_validator.py:65-70`), then calls `simulate_slice` without
an exit argument (`cpcv_validator.py:45-56,96-109`). The simulator's default is
`fixed_2R`, and trail behavior only activates when `exit_mode="trail_ema8"`
(`mega_walk_forward.py:648,659-665`). Thus CPCV invoked on a trail result would
silently score fixed-2R behavior. The output also omits `exit_mode`, preventing
an audit from detecting the substitution.

`N_A`, `INSUFFICIENT_DATA`, or `TOOL_FAILED` is not mapped in the decision table.
For an EXIT-INCREMENTAL cell, any non-OK or insufficient gauntlet result must be
defined as gauntlet failure and therefore A-prime, not treated as neutral or
waived.

## G. PBO/CSCV feasibility — FATAL

The engine result row persists only the selected best configuration and summary
returns. It does not provide a 12-config by common-subperiod return matrix. The
current PBO loader treats each CPCV **row** as a candidate and uses its
`split_results` as columns (`03_QUANTLENS/tools/probabilistic_pbo.py:16-29`). For
Stage-2 those rows are different symbols/modes, not competing configurations on
one common price series; the candidate ID even omits `exit_mode` (`probabilistic_pbo.py:16-17`).

The estimator requires at least two candidates and two splits
(`probabilistic_pbo.py:46-52`). With 15 CPCV combination columns it drops one,
uses 14, and creates `C(14,7)/2 = 1,716` complement-unique partitions, not an
unspecified 100,000-run design (`probabilistic_pbo.py:54-70`). Worse, those 15
columns are overlapping two-group CPCV returns, not the disjoint base
subperiod-return columns assumed by CSCV.

PBO therefore needs a new, explicitly budgeted artifact. For each confirming
cell and exit, persist the frozen winner plus four diagnostic-star configurations
by six common, non-overlapping chronological groups: a 5-by-6 return matrix.
CSCV then has `C(6,3)/2 = 10` complement-unique 3/3 partitions. Candidate IDs
must include strategy, symbol, timeframe, exit mode, and literal parameters.
No cross-symbol or cross-exit row may be treated as a configuration competitor.
Until exit-aware matrix generation and its audit contract exist, outcome A is
unreachable.

## H. Confound-rule falsifiability — FINDING

The current per-cell categories are exhaustive and mutually exclusive when both
bars and DSR values exist:

| `bar(trail)` | `bar(fixed)` | Current DSR condition | Category |
|---:|---:|---|---|
| 0 | 0 | irrelevant/undefined | NEITHER |
| 0 | 1 | irrelevant/undefined | BASE-ONLY |
| 1 | 0 | fixed DSR may be undefined | EXIT-INCREMENTAL |
| 1 | 1 | `du_t >= du_f + 0.10` | EXIT-INCREMENTAL |
| 1 | 1 | `du_t < du_f + 0.10` | POCKET-ONLY |

The aggregate precedence also resolves EXIT plus BASE and POCKET plus BASE
(`FAZ3B_STAGE2_CONFIRM_PREREG_2026-07-13.md:244-258`). The remaining judgment
calls are operational: A versus A-prime is undefined for a non-OK gauntlet, and
“positive category” is not explicitly enumerated. The 0.10 branch is also
statistically unjustified as discussed in E.

Use the simpler revised truth table: trail=1/fixed=0 is EXIT-INCREMENTAL;
trail=1/fixed=1 is POCKET-ONLY; trail=0/fixed=1 is BASE-ONLY; neither is NEITHER.
Then aggregate mechanically: any EXIT with at least one fully passed gauntlet =
A; otherwise any EXIT = A-prime; else any POCKET = B; else any BASE = B-prime;
else trail research-robust = C; else D. Any STOP event overrides all as E.

## I. Decision table and STOP interaction — FATAL

The pre-launch rule permits replacing a contaminated symbol or dropping to five
cells (`FAZ3B_STAGE2_CONFIRM_PREREG_2026-07-13.md:204-210`). That changes the
pre-registered family and decision multiplicity after approval. It conflicts
with the mid-run row-count exception (`...:227-242`) and is self-authorizing.
The current contamination is six of six, so this is not hypothetical.

Other non-mechanical branches:

- Row count may differ from 14 if gaps are “explained,” while outcome E says any
  STOP rule makes the run void. Exactly which explanations avoid E is unstated.
- “Crashes twice” silently permits one retry, although relaunch is said to need
  fresh approval.
- The smoke is one trail row, while the full job is 14 rows. “Smoke-extrapolated
  cap ×1.5” does not state whether the multiplier is 14, whether startup is
  deducted, or whether worker count must match.
- Smoking GOOGL exposes a decision-cell metric before the family run. A
  plumbing smoke should use the non-evidence AAPL reference and must not inspect
  performance fields.

Require exactly 14 stamped rows and zero `NO_DATA`, `SKIPPED_*`, or `ERROR`
rows. The first crash, data collision, invalid row, or tool failure is E and
requires an amended pre-reg plus new approval. For a two-mode AAPL smoke using
the same worker settings, define `full_cap_seconds = ceil(1.5 × 7 ×
smoke_seconds)` and record both values before launch.

## J. Gate hygiene — FATAL

The header correctly says D016 is absent and no run/runner is authorized
(`FAZ3B_STAGE2_CONFIRM_PREREG_2026-07-13.md:3-8`), and outcome A only proposes a
forward-paper entry to Baris (`...:246-254,260-269`). Those rails are sound.

The replacement/drop language in section 9 is nevertheless an unauthorized
scope-change mechanism. The runner specification also asserts only the grid,
not the full approved contract (`...:103-122,199-223`). It must assert the exact
ordered symbols, `1h` only, both ordered exit modes, literal grid roles, stride
unset/1, canonical manifest resolved path plus content hash, clean engine commit,
empty new output directory, expected 14 job keys, and zero extra strategy/TF
values. The smoke must be non-evidentiary and isolated from the full output.

The “standard” multi-window tool is another hidden behavior change: it ignores
row `exit_mode` when simulating (`03_QUANTLENS/tools/multiwindow_oos.py:111-137`),
so it defaults to fixed-2R, and it invents numeric ±20%/25% neighbors rather than
using the pre-registered grid (`multiwindow_oos.py:68-85`). Its stability
denominator excludes neighbors with too few trades (`multiwindow_oos.py:131-142`),
which can inflate the pass rate. It cannot be used for this trail gauntlet
without an exit-aware, literal-neighbor contract.

Bridge-parity registration itself is isolated correctly. The normal Keltner grid
and signal branch remain separate (`mega_walk_forward.py:316-322,525-531`);
`keltner_trail_ema8` is a distinct grid entry and explicit-select-only set
(`mega_walk_forward.py:324-330,347-377`); default strategy selection filters that
set (`mega_walk_forward.py:1623-1639`). Commit `6442b000` therefore does not, by
these code paths, alter explicit `GEN_KELTNER_BREAKOUT` behavior. This does not
repair the separate gauntlet defects above.

## REQUIRED EDITS BEFORE D016

1. **Replace the status sentence at lines 7-8.** Use: “Drafted by Claude Fable
   5 before any Stage-2 execution. Codex Gate-5 review is recorded separately;
   this draft is not audited or approvable until every blocking finding is
   applied and re-reviewed.”

2. **Replace section 3's six-symbol scope and decision-cell paragraph.** Use:
   “GOOGL, META, AMD, NFLX, DIA, and IWM are disqualified: prior
   GEN_KELTNER_BREAKOUT 1h rows exist on the identical 2020-07-27 through
   2026-06-26 observation series. No replacement may be selected under this
   pre-registration. A new draft must freeze a genuinely untouched dataset or
   post-2026-06-26 window after an exhaustive result-artifact inventory. If no
   untouched data exists, any run is replication/research only and cannot award
   Stage-2 `robust_final`.” Add a table naming the evidence lines in C.

3. **Add a diversity rule to the replacement scope.** Use: “Confirmation
   requires successful decision cells from at least two predefined diversity
   groups (for example, single-stock and broad-market ETF) and no group may be
   defined or changed after results are visible. A one-cell success remains
   research evidence only.”

4. **Replace section 4's best-of-12 decision grid with the five-row table in B.**
   Add: “Only `{50,10,2.0}` decides the primary confirmation. The four one-axis
   star neighbors are diagnostics; they cannot replace the primary, select a
   best configuration, or rescue a failed primary. Cross-term neighbors are not
   run.” Recalculate all row/trial counts after the held-out scope is replaced.

5. **Replace section 8 with an artifact-level family ledger.** The table must
   include artifact path, run date, data window, symbols, timeframe, exit,
   literal configurations, count, whether metrics were inspected, and an
   include/exclude reason. Add the June-29 six-cell minimum of 96 omitted trials.
   State that N is not final until the full historical Keltner inventory is
   attached; do not retain 219. Registry absence is not an exclusion reason.

6. **Add an explicit six-cell multiplicity formula, adjusted to the eventual
   number of decision cells.** If a one-cell success remains allowed, use:
   “`du_family = 1 - min(1, m × (1-du_cell))`; require `du_family >= 0.95`.
   For m=6, `du_cell >= 0.9916667`.” This is separate from trial-family N and
   from the two-group diversity rule.

7. **Replace the DSR prose with a literal algorithm.** Copy the equations from
   `mega_walk_forward.py:1507-1525`; define `SR`, `T`, `N`, gamma, skew=0,
   kurtosis=3, `Phi`, missing-value behavior, `ddof=1`, and rounding only after
   the final CDF. Attach the exact pool-row manifest. For a 1h decision, compute
   sigma from the enumerated comparable 1h Keltner pool; do not silently mix
   horizons. Preserve other historical attempts in N where they influenced
   selection.

8. **Replace section 7's 0.10 rule and section 10 precedence.** Use the revised
   truth table and aggregate algorithm in H. Both modes passing is POCKET-ONLY;
   trail passing while fixed fails is EXIT-INCREMENTAL. A STOP event overrides
   all categories as E.

9. **Insert an exit-aware gauntlet prerequisite before any execution approval.**
   Use: “Current `cpcv_validator.py` and `multiwindow_oos.py` are ineligible for
   trail evidence because they default simulations to fixed-2R. Before D016, a
   separate code-review specification must require `row.exit_mode` to be passed
   into every simulation and stamped into every output/candidate ID. Literal
   pre-registered neighbors only; insufficient-trade neighbors remain in the
   denominator as failures. No gauntlet result without this contract has
   evidentiary weight.”

10. **Specify CPCV scoring exactly.** Use: “Six contiguous groups, two test
    groups, 15 combinations, 1% embargo, minimum 30 trades per test combination,
    positive return, PF >=1, maxDD >-50%, and at least 11/15 passing combinations
    with median return >0. Any `N_A`, `INSUFFICIENT_DATA`, `TOOL_FAILED`, missing
    exit stamp, or fewer than 15 combinations is GAUNTLET_FAIL; an otherwise
    EXIT-INCREMENTAL cell maps to A-prime.” State honestly that the existing
    validator records purged train-bar counts but does not refit a model.

11. **Replace the PBO sentence with a matrix contract.** Use: “For each cell and
    exit independently, persist a configuration-by-base-period return matrix:
    frozen primary plus four literal star diagnostics by six identical,
    non-overlapping chronological groups. CSCV uses the 10 complement-unique 3/3
    partitions. Candidate ID includes strategy/symbol/timeframe/exit/literal
    params. Cross-symbol, cross-exit, and overlapping CPCV-combination rows are
    forbidden. Missing matrix or fewer than two configurations is
    GAUNTLET_FAIL.”

12. **Replace section 9 pre-launch substitution and STOP clauses.** Use: “The
    approved symbols, data window, grid roles, and row count are immutable. Any
    prior-result collision, missing dataset, first crash, `NO_DATA`, `SKIPPED_*`,
    `ERROR`, row count mismatch, or stamping mismatch is STOP/E. There is no
    substitution, cell drop, or automatic retry; amendment and fresh written
    approval are required.”

13. **Replace the smoke and runtime-cap clauses.** Use: “Smoke the non-evidence
    AAPL reference in both modes, write to a disposable isolated directory, and
    inspect stamping/runtime only—not performance. With identical worker
    settings, `full_cap_seconds = ceil(1.5 × 7 × smoke_seconds)` for 14 full rows
    versus two smoke rows. Record the computed cap before full launch.” Adapt the
    factor if the replacement scope changes.

14. **Expand the runner hard assertions.** Require exact ordered symbols,
    timeframe, both ordered modes, decision/diagnostic grid roles, stride
    unset/1, canonical resolved manifest plus hash, clean approved engine commit,
    empty new output path, exact job-key set/row count, and absence of extra
    strategies/TFs/modes. Smoke and full outputs must not share a checkpoint or
    result directory.

15. **Replace sign-off lines 276-279.** Point to
    `11_TRIAGE/CODEX_GATE5_FINDINGS_FAZ3B_STAGE2_2026-07-13.md`, list each applied
    required edit, and add a second adversarial re-review checkbox. D016 remains
    unchecked and impossible until that re-review says the FATAL findings are
    closed.

## NICE-TO-HAVE

1. Add a machine-readable pre-registration manifest containing the immutable
   symbol/window/config/job-key set and its digest; print that digest in every
   output.
2. Distinguish “selected-winner row,” “parameter trial,” “decision cell,” and
   “independent evidence unit” in a glossary. The current draft uses trial N to
   cover several different multiplicity problems.
3. Report sector/index-group outcomes and pairwise return correlations as
   descriptive context, never as a post-hoc reason to add/drop a cell.
4. Rename the present CPCV implementation in reports as a combinatorial temporal
   placement test unless/until its training/purge semantics are made explicit.

## What I could not verify without running

- No Stage-2 result exists, so I could not verify trade counts, returns, DSR,
  BH-FDR, runtime, or whether any new-data cell would pass.
- I could not determine actual CPCV per-combination trade sufficiency from an
  aggregate lockbox trade count; the 49-trade AAPL row only supports a rough
  feasibility estimate.
- I did not compute empirical correlations among symbols or sectors; the
  correlation warning is structural and secondary to the direct prior-result
  collision.
- I did not validate a replacement exit-aware CPCV/PBO/multi-window
  implementation because none is specified and executing or writing runner
  code is outside this review.
- The historical family inventory is demonstrably incomplete, but a final
  effective-trial N requires an approved deduplication rule for repeated runs
  and an artifact manifest. I therefore report 315 only as a proven lower bound
  under the draft's own additive convention, not as the corrected final N.

**Execution statement:** no run was performed. These findings authorize no
smoke, runner creation, backtest, gauntlet, paper trading, or live action. Fable
must synthesize and apply the required edits; D016 remains Baris's separate
written decision after re-review.
