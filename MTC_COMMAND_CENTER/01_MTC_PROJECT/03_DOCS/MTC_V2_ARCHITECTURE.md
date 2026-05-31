# MTC_V2 Architecture

## 1. System Summary

MTC_V2 is a parity-first trading strategy framework developed in parallel on:
- TradingView Pine Script
- Local Python runner

Canonical ownership:
- Pine owner: `01_MASTER TEMPLATE_V2/01_PINE/MTC_V2.pine`
- Python owner: `01_MASTER TEMPLATE_V2/00_PYTHON/mtc_v2/*`

Current approved execution direction:
- default canonical profile: `close_only_deterministic_v2`
- legacy explicit-only profile: `raw_close_only_v1`

Core invariants:
- parameter names must match across Pine and Python
- no new feature is considered complete while parity is broken
- signal, transform, gate, and entry logic are close-bar decisions
- protective exits may trigger intrabar, but Python emulates them deterministically from OHLC
- workbook `Properties` are source of truth for export-faithful TradingView audits
- workbook `Properties` symbol and timeframe are also source of truth for local PineTS/Python audit routing; a local pass on another market is not a valid TradingView audit

### 2026-04-28 Optimization Consolidation

- Optimizer infrastructure, data bundle creation, and dataset usage rules are ready as research infrastructure.
- Big overnight multi-asset optimization is partial: `168337 / 6615000` split evaluations completed, with `144` robust medium candidates and `0` robust strict candidates.
- A later detached 12h producer-only seed extraction completed `282255 / 378000` evaluations with `0` failed evaluations and `0` duplicate conflicts under `reports/optimization/12h_backtesting_session/`.
- Optimization uses external dataset manifests, preserved `source_type`, and stable `evaluation_key` rows.
- Optimization output is research-only and does not change Pine defaults or claim TradingView release parity.
- The external optimization data bundle must remain outside the portable handoff zip.
- Worker scaling benchmark recommends explicit `--max-workers 16` for the next big resume; `20+` workers are not approved without a new benchmark.
- Long optimization must run as a detached PowerShell process because Codex UI closure can abort foreground terminal work.
- Large optimization runs must pin numeric-library threads to 1 and preserve `resume_registry.sqlite`.

## 2. Pipeline Overview

The canonical per-bar pipeline is:

1. Global config
2. Signal producer
3. Signal transforms
4. Entry gates
5. Position sizing
6. Entry decision
7. Exit engine
8. State/accounting update
9. Artifact generation

The pipeline must remain ordered. New features must attach to the correct layer rather than being inserted ad hoc.

## 3. Global Config

Global config is the single source of truth for runtime parameters.

Important global controls:
- `enable_long`
- `enable_short`
- `allow_flip`
- `regime_lock`
- `max_entries`
- `cooldown_bars`
- `signal_mode`

Rules:
- config is read-only during a run
- no runtime mutation of user parameters
- Pine and Python must interpret the same parameter names with the same meaning

## 4. Signal Producer Contract

Producer input:
- confirmed bar data

Producer output:
- `long: bool`
- `short: bool`
- optional reason metadata

Rules:
- only one active producer at a time
- producer owns its own signal logic
- producer should emit pulse/event-style signals, not persistent position state
- dual-true long and short should be normalized away before leaving the producer

Known producer path in active export work:
- `Supertrend`

Selectable producer draft:
- `Range Filter` exists as a non-default selectable draft producer
- `Supertrend` remains the default producer
- `Range Filter` must be selected explicitly with `signal_mode = "Range Filter"`
- local feature parity for the Range Filter surface has passed
- no TradingView release-audit claim exists for Range Filter yet

Known scaffold:
- `st_use_ha` is not truly implemented yet
- current HA path intentionally yields no-trade behavior instead of real Heikin Ashi support

## 5. Signal Transform Contract

Transforms are stateful, optional post-producer stages.

Examples:
- confirmation
- level retest

Rules:
- each transform receives the previous stage output
- OFF means pass-through
- ON may introduce waiting state and timeout state
- transform state must be explicit and deterministic

### Confirm Transform (L18) — Signal Producer Compatibility Warning

Confirm Transform is designed for **pulse-based signal producers** — producers that emit `true` only on the flip/signal bar and `false` on all subsequent bars.

**Supertrend is a level/state-based producer**: `long_raw` stays `true` for the entire uptrend. This makes most Confirm Transform sub-options non-functional:

| Sub-option | Behavior with Supertrend |
|---|---|
| `Confirm Bars = 1` | No-op — entry fires on flip bar as usual |
| `Confirm Bars > 1` | **0 trades** — entry edge detection misses the delayed arm |
| `Close Must Cross` | No-op — close is already on correct side at flip bar |
| `Req Raw Still True` | No-op — `long_raw` is true for entire trend |
| `Refresh New Raw` | **0 trades in Pine/PineTS** + Python parity bug (Python ignores this flag) |

**Conclusion:** With Supertrend, the only working config is `Confirm Bars=1` with no sub-options, which is identical to OFF. The feature will become meaningful when a pulse-based producer is added (e.g., a producer that emits only on crossover events).

**Known parity bug:** `refresh_on_new_raw=true` causes 0 trades in Pine/PineTS but 131 trades in Python — Python does not implement this flag. Must be fixed before this sub-option is exported in any parity case.

## 6. Gate Contract

Gates are close-bar filters applied after transforms and before entry sizing.

Examples already present in the project:
- MA filter
- MA slope
- HTF trend
- McGinley
- Volume
- ADX
- Chop
- ATR floor
- MACD family
- Momentum
- Session
- Candle pattern
- Level proximity

Rules:
- gates do not own position state
- gate output is candidate permission, not trade execution
- a gate must not silently substitute a different timeframe or data source when requested data is unavailable

## 7. Position Sizing Contract

Sizing happens only after producer and gate decisions are complete.

Canonical sizing outputs:
- candidate qty
- candidate notional

Main controls:
- `risk_per_long_pct`
- `risk_per_short_pct`
- `fallback_size_pct`
- `max_leverage_cap`
- stop mode inputs

Rules:
- `% risk` means risk at stop, not position size as a percent of account
- if stop distance is small, requested qty may be large
- `max_leverage_cap` is an internal sizing cap, not broker margin
- TradingView broker margin is separate and must match externally

Critical leverage rule:
- `max_leverage_cap` limits notional to `equity * max_leverage_cap`
- it does not override TradingView `Properties > Margin`
- parity requires:
  - `TV Margin % = 100 / max_leverage_cap`

Examples:
- `max_leverage_cap = 5` -> `TV Margin = 20%`
- `max_leverage_cap = 100` -> `TV Margin = 1%`

## 8. Entry Decision Contract

Entry decision consumes:
- gated directional candidate
- current state
- sizing result

Rules:
- no entry with `qty <= 0`
- `allow_flip = false` forbids immediate reverse entry on the same decision path
- `max_entries` and `cooldown_bars` must behave deterministically
- same input state must produce the same entry decision on both Pine and Python

## 9. Exit Engine Contract

Exit engine owns protective and strategic exits.

Important exit families:
- opposite signal exit
- stop loss
- take profit
- break even
- trailing stop
- time stop
- guard exits

Canonical rules:
- close-bar decisions own strategic exits
- intrabar protective exits are allowed, but Python must emulate them with deterministic OHLC rules
- exit reasons must be normalized across Pine, Python, and TradingView audits

## 10. Execution Model and Intrabar Rules

Current canonical direction is close-only deterministic ownership.

Meaning:
- strategic trade lifecycle decisions are owned at bar close
- intrabar ambiguity must be resolved deterministically
- no hidden dependence on TradingView live broker internals for canonical correctness

Legacy path:
- `raw_close_only_v1` remains available only for explicit legacy or research use

## 11. HTF Data Contract

Higher-timeframe data must follow prior-closed semantics.

Rules:
- requested HTF data must represent the last fully closed HTF bar
- unavailable HTF data must remain unavailable
- lower-than-chart HTF requests must not silently fall back to LTF behavior
- PineTS and Python must use the same HTF alignment rules

Practical consequence:
- missing mock data for `2h`, `4h`, or `1d` can block PineTS-side parity even when Python and TradingView are still comparable

Current open HTF-sensitive issues:
- `case_032`: daily HTF McGinley lifecycle mismatch
- `case_039`: HTF ADX 240 mismatch
- `case_040`: HTF ADX D mismatch
- `case_044`: HTF Chop 240 mismatch
- `case_045`: HTF Chop 120 mismatch

## 12. TradingView Export Audit Contract

TradingView export audit is not the daily development loop. It is a frozen oracle workflow.

Source of truth:
- workbook `Properties`
- workbook `List of trades`

Required order:
1. verify workbook settings
2. compare expected trade-count and outcome effect versus baseline or relevant previous case
3. run parity
4. update tracker

Audit layers:
- strict trade parity
- soft trade parity
- strict outcome parity
- soft outcome parity

Tracker owner:
- `01_MASTER TEMPLATE_V2/05_PARITY/MTC_V2_TW_EXPORT_CASE_TRACKER.xlsx`

Suite owners:
- `01_MASTER TEMPLATE_V2/05_PARITY/MTC_V2_TW_EXPORT_CASE_SUITE_V2.csv`
- `01_MASTER TEMPLATE_V2/05_PARITY/MTC_V2_TW_EXPORT_CASE_SUITE_V2.json`

Release rule:
- TradingView export remains the final external release audit
- local PineTS/Python/reference-oracle parity can qualify work for release audit, but does not replace it

## 12A. Generic Feature Parity Factory Contract

The Generic Feature Parity Factory is mandatory for new or changed feature behavior.

Required flow:
1. define or update the feature contract
2. implement the isolated Python and PineTS feature surfaces
3. emit normalized feature traces
4. compare feature parity at the supported local levels
5. pass the acceptance gate before integration into canonical Pine/Python behavior

Rules:
- feature parity must pass before integration
- existing validated features should not be re-POC'd unnecessarily
- feature factory work must stay additive until the contract and trace evidence are stable
- a feature is not production-ready only because an isolated POC ran once

Current factory surfaces:
- controlled Supertrend surface
- Range Filter producer surface

## 12B. PineTS and Python Oracle Roles

PineTS role:
- PineTS is the local `L0`/`L1`/`L2`/`L3` feature, indicator, and signal oracle
- PineTS is not the final `L4`/`L5`/`L6` lifecycle authority unless lifecycle rows are explicitly emitted and normalized
- PineTS mismatch should first be treated as a signal, adapter, transpilation, HTF, or warmup investigation target

Python engine role:
- the Python MTC engine remains the local lifecycle, backtest, and optimization owner
- Python owns local `L4`/`L5`/`L6` comparisons when PineTS cannot emit lifecycle rows
- Python lifecycle ownership does not remove the need for TradingView release audit on promotion candidates

## 12C. Independent Reference Oracle Layer

The Independent Reference Oracle Layer is a small feature-level expected-value calculator.

Rules:
- it must not import the production implementation it checks
- it cross-checks the independent expected trace against Python and PineTS feature traces
- it works at feature-trace level, not full strategy lifecycle level
- it is not a replacement for TradingView final audit

Current status:
- Range Filter reference oracle passed against the available local traces

## 12D. Factory Regression Suite

The Factory Regression Suite is a local regression accelerator for factory-runnable cases.

Current limitations:
- coverage is low
- only controlled Supertrend and Range Filter surfaces are factory-runnable
- FULL dry-run classification must not be interpreted as full parity coverage
- a real FULL run is not useful until more feature trace surfaces are added

Use:
- use FAST or inventory classifications to find what is locally comparable
- do not claim `L4`/`L5`/`L6` PineTS lifecycle parity unless PineTS emits those lifecycle rows

## 12E. Optimization Loop, Scoring, and Cross-Market Validation

Optimization is a future layer after parity gates.

Current status:
- the optimization plan exists as documentation at `03_DOCS/PLANS/MTC_V2_OPTIMIZATION_LOOP_SCORING_CROSS_MARKET_PLAN.md`
- optimizer tooling, dataset manifests, resume/de-dup registry, and worker scaling benchmark reports now exist as research infrastructure

Rules:
- optimization must never bypass feature parity
- no optimization job should modify `01_PINE/MTC_V2.pine` or production Python behavior
- optimization jobs should consume approved local data and emit separate artifacts
- overnight optimization jobs must run through detached process templates, not foreground Codex UI terminal sessions
- the next big resume uses explicit `--max-workers 16` with thread pinning
- TradingView release audit remains the final promotion step

## 12F. Data and Dataset Contract

Portable handoff data must be explicitly labeled by source and purpose.

Current Binance chart CSV decision:
- Binance chart CSV data is included for local development and future optimization planning
- the current included CSV is `05_PARITY/01_TW_CHART_DATA/BINANCE_BTCUSDT.P, 60_consolidated_stable.csv`
- it is a BTCUSDT.P 1h TradingView chart export for Binance
- final package target should follow `data/chart/binance/<symbol>/<timeframe>/<original_csv_filename>`

Future data rules:
- other crypto symbols and timeframes can be added later under the same structure
- TradingView audit XLSX workbooks are not chart CSV data
- TradingView audit XLSX workbooks remain review-needed or belong in a separate audit bundle
- downloaded exchange data and TradingView chart exports must not be mixed without source labels

## 13. Broker Model Contract

Broker model concerns:
- margin
- leverage
- liquidation or margin-call semantics
- commission and slippage when relevant

Rules:
- Pine internal `max_leverage_cap` and TradingView broker margin are separate concepts
- export-faithful parity must respect the broker settings shown in the workbook
- mismatch between `max_leverage_cap` and TV margin can create false divergence

Examples already seen:
- `Max Lev = 5` with `Margin = 1%` is inconsistent
- `Max Lev = 5` with `Margin = 20%` is consistent

## 14. Session and DST Contract

Session and timezone behavior must be explicit.

Rules:
- chart/export timezone must be handled as fixed input in audits
- session filters must not depend on implicit local machine timezone
- DST-sensitive logic must be deterministic and testable

Current export audit convention:
- `UTC+3`

## 15. Equity Snapshot Contract

Sizing snapshots must be explicit.

Current simplified direction:
- legacy `equity_source` user option was removed from UI/export surface
- runtime behavior is fixed to realized-equity sizing

Reason:
- the old option created complexity with little practical value in the current strategy profile

## 16. File Structure

Primary files:
- Pine canonical:
  - `01_MASTER TEMPLATE_V2/01_PINE/MTC_V2.pine`
- Python canonical:
  - `01_MASTER TEMPLATE_V2/00_PYTHON/mtc_v2/core/config.py`
  - `01_MASTER TEMPLATE_V2/00_PYTHON/mtc_v2/core/runner.py`
  - `01_MASTER TEMPLATE_V2/00_PYTHON/mtc_v2/core/htf.py`
  - `01_MASTER TEMPLATE_V2/00_PYTHON/mtc_v2/core/position_sizer.py`
  - `01_MASTER TEMPLATE_V2/00_PYTHON/mtc_v2/core/gates.py`
- Audit and parity:
  - `parity_compare.py`
  - `01_MASTER TEMPLATE_V2/05_PARITY/manual_tw_futures_audit.py`
  - `01_MASTER TEMPLATE_V2/05_PARITY/manual_tw_lifecycle_audit.py`

## 17. Interface Contracts

The following conceptual interfaces must stay stable across Pine and Python:

- raw signal
- transformed signal
- gated candidate
- sizing result
- entry decision
- exit event
- normalized trade row

Each layer should have one clear owner.

## 18. Config Families

Main config groups:
- global execution toggles
- signal producer params
- transform params
- gate params
- sizing params
- stop and TP params
- guard params
- session and HTF params

Rules:
- remove dead UI research knobs from user/export surface
- keep only meaningful user-facing controls in the export suite
- internal research toggles may remain code-side, but not as normal UI parameters

Already removed or fixed-to-default from user/export surface:
- `equity_source`
- `use_notional_assert`
- `execution_profile_id`
- `tw_*` research knobs

## 19. Runner Order

Canonical runner order per bar:
1. load bar and time context
2. update HTF caches
3. compute producer signal
4. apply transforms
5. apply gates
6. evaluate strategic exits
7. evaluate protective exits
8. size candidate entries
9. apply entry rules
10. update state, equity, trade ledger
11. emit diagnostics and artifacts

Any deviation from this order must be justified and mirrored across Pine and Python.

## 20. Layer Order

Use this sequence for new development or audits:

1. producer correctness
2. transform correctness
3. close-bar gates
4. HTF gate correctness
5. sizing correctness
6. exit correctness
7. guard correctness
8. export-faithful TradingView audits

When multiple open issues exist:
- prioritize lifecycle divergence over drift-only issues
- prioritize source-of-truth workbook mismatches over planned-case assumptions
- prioritize HTF contract mismatches over accounting-column drift

Current highest-priority open targets:
1. `case_039`
2. `case_040`
3. `case_044`
4. `case_045`

## 21. V1 vs V2 Difference

Important simplification:
- current V2 work treats TradingView export as an audit oracle, not the canonical execution owner
- canonical correctness is Pine vs Python under the approved close-only deterministic model
- TradingView parity is still valuable, but not the owner of architecture decisions

## 22. Audit Checklist

Before calling a case complete:
- workbook settings verified
- expected trade-count effect checked
- expected outcome effect checked
- parity run completed
- tracker updated
- handoff updated

Before calling a mismatch a code bug:
- confirm the observed workbook differs from planned or not
- confirm margin and leverage alignment
- confirm HTF mock data availability
- confirm the divergence is lifecycle-level, not only qty drift

## 23. What Not To Do

- do not infer export settings from old tracker text when the workbook exists
- do not treat TradingView export as daily workflow dependency
- do not use TradingView export as the normal feature development loop
- do not silently replace missing HTF data with lower timeframe data
- do not remove parity-visible settings from one side only
- do not move to the next layer while current parity is unresolved
- do not bypass the Generic Feature Parity Factory for new or changed features
- do not optimize before feature parity passes
- do not treat PineTS as `L4`/`L5`/`L6` lifecycle authority without emitted lifecycle rows
- do not include TradingView audit XLSX archives in the main portable package without review approval
- do not use live trading keys or API keys in portable handoff work

## 24. Optimizer Infrastructure Rules

- The official optimizer result interface is `00_PYTHON/mtc_v2/core/results.py` plus the non-breaking adapter `tools/runner_metrics_adapter.py`.
- Overnight optimization must use a resume/de-dup registry and include `evaluation_key` in every result row.
- `resume_registry.sqlite` is mandatory for resumed overnight runs and must survive detached-process restarts.
- Big overnight resumes must be launched through detached PowerShell scripts with heartbeat and stdout/stderr logs.
- The current worker benchmark recommendation is `--max-workers 16`; do not exceed 16 without a new benchmark.
- Required thread pinning for large runs: `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`.
- Duplicate evaluation rows must not be counted twice; conflicting duplicate result hashes must be reported.
- Coverage-aware scoring must reject unstable candidates with weak walk-forward, timeframe, or symbol coverage.
- Single-symbol optimization can be useful research, but it cannot produce a production-robust candidate by itself.

## 25. Optimization Dataset Source Of Truth

- Large optimization datasets live outside the portable handoff package in `C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427`.
- Optimizers must load `manifests/dataset_manifest.yml` or `manifests/dataset_manifest.json` and select by `dataset_id`.
- Optimizers must not hardcode CSV paths or scan `ARŞİV` directly except in explicit manifest discovery/update mode.
- `regimes/regime_registry.yml` or `regimes/regime_registry.json` is required when reporting robust-candidate performance by market regime.
- The data bundle is for research optimization and cross-market validation only; it is not final TradingView release parity data.
- Detailed rules are in `docs/optimization/DATASET_AND_REGIME_USAGE_RULES.md`.

## 26. Search-Space Reduction And Parameter Library

- New feature/filter optimization must use staged smart sampling rather than blind full-grid expansion.
- Methodology source: `docs/optimization/SEARCH_SPACE_REDUCTION_AND_SMART_SAMPLING.md`.
- Research seed source: `optimization/parameter_library/README.md`.
- Producer-only seed extraction precedes exit/risk refinement, filter/gate evaluation, regime mitigation, cross-asset/timeframe validation, walk-forward robustness, and candidate promotion.
- Applies to Supertrend, Range Filter, and future producers.
- Medium candidates are research seeds only; they cannot become Pine defaults or TradingView release claims.

## 27. Per-Asset/Timeframe Seed Ranking

Per-asset/per-timeframe seed ranking is now part of the optimization infrastructure boundary. Staged refinement must consume granular seed outputs from `optimization/parameter_library/` rather than aggregate-only candidate rows. Aggregate outputs remain useful for global summaries, but exit/risk and filter/gate research require asset/timeframe-local evidence, dataset/source metadata, and preserved evaluation keys. Smoke-derived seeds are research artifacts only and do not affect Pine/Python/PineTS strategy behavior.
