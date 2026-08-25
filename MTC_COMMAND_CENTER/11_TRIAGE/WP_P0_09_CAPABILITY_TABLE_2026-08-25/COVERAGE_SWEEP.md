# WP-P0-09 Coverage Sweep

**Lane input base SHA:** `fead492b0b87f207aa6e7a259372b9767d4301f9`

**Evidence base for this revision:** `ac873ae7ba835a3b719e3a0485a9d45eb2fe3a90` (repair rounds 1 and 2)

**Purpose:** prove that `CAPABILITY_CANONICALIZATION_TABLE.md` covered the requested economic families, the full configuration surface, **and the modules omitted from the first sweep**. This is a source and configuration sweep. It is not a parity claim.

**Citation convention:** identical to `CAPABILITY_CANONICALIZATION_TABLE.md` §1.1 — every path is repo-root-relative and complete, and a `` `:N-M` `` token continues the most recent full path **on the same line**.

## 1. Scope, method, and what repair round 1 widened

### 1.1 Inspected subjects

| Implementation | Modules inspected in repair round 1 | Lines |
|---|---:|---:|
| **A** `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/` | `config.py`, `runner.py`, `exits.py`, `position_manager.py`, `position_sizer.py`, `instrument.py`, `rounding.py`, `types.py`, **`confirmation.py`**, **`gates.py`**, **`htf.py`**, **`ma.py`**, `indicators.py`, `results.py` | 5,252 |
| **B** `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/` | `config/defaults.py`, `engine/mtc_runner.py`, `engine/mtc_state.py`, `engine/indicators.py`, **`engine/fee_model.py`**, **`engine/fills.py`**, `engine/metrics.py`, `engine/__init__.py`, `modules/confirmation_layer.py`, `modules/risk/*.py`, `modules/filters/*.py`, `modules/signals/*.py` | — |
| **Pine** | `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine` | 2,079 |

The **bold** modules are the ones the audit required be swept and that the first revision did not open. Their findings are in §4. Module names in the second column are **inventory entries relative to the directory in the first column**, carry no line numbers, and are not citations; every citation elsewhere in this document is a complete repo-root-relative path or a same-line continuation of one.

### 1.2 Prior evidence inspected

`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_06_PARITY_CORPUS_2026-08-24/PARITY_CORPUS_INVENTORY.md`, `MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md`, `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md`, the two named B case files, `MTC_COMMAND_CENTER/contracts/README.md`, `MTC_COMMAND_CENTER/contracts/mtc_contracts/*.py`, `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`, `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md`, `MTC_COMMAND_CENTER/11_TRIAGE/WAYFINDER_DECISION_FOLD_2026-08-23.md`, and `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_04_CONTRACTS_2026-08-25/LANE_REPORT.md`.

### 1.3 Method

Exact-symbol and exact-prefix searches (`wt_`, `tw_`, `l18b_`, `entry_mode`, `first_bar_requires_edge`, `fee_model`, `FillsEngine`, `equity_source`, `fallback_size_pct`, sizing, stop, target, margin, confirmation, cooldown, session, fee, slippage, funding), then the owning line ranges were read in full. No backtest, no network call, no runtime mutation, no execution of project code.

### 1.4 Reproducible surface counts

| Surface | Count | Command run from the repository root |
|---|---:|---|
| A `DEFAULT_CONFIG` string keys | 192 | `grep -c '^    "' MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py` |
| …all inside the dict literal | 192 | `sed -n '28,246p' … \| grep -c '^    "'` |
| B configuration classes | 17 | `grep -n "^class " MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py` |
| B annotated field declarations | 205 | `grep -cE "^    [A-Za-z_][A-Za-z_0-9]*[ ]*:" MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py` |
| Pine `input.*` declarations | 153 | `grep -c "input\." MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine` |
| A `wt_*` keys | 13 | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:226-238` |
| A `tw_*` keys | 7 | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:58-64` |
| A `l18b_*` keys (+ `use_l18b_confirmation`) | 14 (+1) | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:184-197` |

The previous revision reported the B field count as 205 without a command; the command above reproduces it exactly. A looser pattern requiring a space after the colon returns 202, because three declarations use different spacing — the 205 figure is the one that matches the class definitions.

## 2. A configuration sweep — all 192 keys by contiguous range

**Two coverage gaps in the previous revision are corrected here.** Its declared ranges were `29-35, 37-42, 43-55, 58-64, 65-71, 72-128, 129-144, 146-150, 153-178, 180-204, 206-224, 226-238, 239-245`, which left **`debug_mode` at line 36** and **`level_proximity_lookback` at line 151** outside every range. `level_proximity_lookback` is an economically active gate parameter and is corpus case 106. The ranges below are contiguous from 29 to 245 and therefore cannot hide a key.

| A range | Configuration family | Decision IDs | Coverage result |
|---|---|---|---|
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:29-35` | direction, flip, regime lock, max entries, cooldown, warm-up override | C05, C06, C23 | Covered; `cooldown_bars` re-scoped as entry spacing by C06 |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:36` | `debug_mode` | — | **Non-economic**, dispositioned in §7 |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:37-42` | signal mode and Supertrend/range-filter parameters | C01 | Covered |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:43-55` | instrument metadata, capital, margin percentages, execution profile | C08-C10, C20, C22 | Covered; the close-only default is decided by C20 |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:56-64` | all seven `tw_*` keys and their comment block | C31-C37 | Covered individually; C31 is the master gate |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:65-71` | fixed quantity, risk %, fallback %, leverage cap, equity source, notional assert | C07-C10 | Covered; C07 re-decided in repair round 1 |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:72-128` | MA, slope, McGinley, volume, ADX, Chop, ATR-volatility, MACD, HTF, momentum, session gates | C02, C40, C41 | Covered; the HTF and MA/MACD equation axes are now C40/C41, not C02 |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:129-151` | opposite-signal exit, nine filter-block exits, candle-pattern and level-proximity gates **including `level_proximity_lookback` at `:151`** | C02, C16 | Covered; previous gap closed |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:152-178` | time exits, daily loss, max trades, drawdown, consecutive loss, equity curve, MAE, trade cooldown, guard recovery | C17, C18, C06 | Covered; ownership split decided |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:179-197` | N-bar confirmation transform, refresh, `use_l18b_confirmation` and the fourteen `l18b_*` keys | C03, **C38** | Covered; the `l18b_*` scaffold is a new explicit disposition |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:198-204` | `require_raw_still_true`, `refresh_on_new_raw`, level-retest transform | C03, C04 | Covered |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:205-224` | stop mode flags and parameters, target mode and parameters, MultiTP | C11-C13, C19, C20 | Covered |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:225-238` | all thirteen `wt_*` keys | C28-C30 | Covered exactly; all dispositioned |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:239-245` | break-even and trailing | C14, C15 | Covered |

Consumer and disposition findings, each corrected against the source in this round:

- `fixed_qty` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:65`) is not merely dormant — `validate_config` **rejects** any value other than `1.0` (`:457-462`). C07 makes it meaningful only under the typed `FIXED_QTY` method.
- `equity_source` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:70`) and `use_notional_assert` (`:71`) are **overwritten to constants** in `resolve_config` before validation, so neither is selectable behaviour at all (`:614-618`). The previous revision described `equity_source` as a runtime choice; it is not.
- `margin_long_pct` / `margin_short_pct` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:53-54`) are **derived from `max_leverage_cap`** when not explicitly supplied (`:619-624`), which is why C10 rejects A's margin approximation as venue authority.
- All thirteen `wt_*` keys are declarations with no A runtime consumer, with two precise exceptions recorded in C30: `wt_use_tp` and `wt_use_sl` participate in configuration validation (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:581-584`). The five route codes are additionally the only `wt_*` keys A never type-checks (`:226-230` versus `:569-580`).
- Six `tw_*` keys have real A economic branches; `tw_margin_call_split_entries` is read twice and consumed by no branch (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:133`, `:1050-1057`). C35 forbids fabricating the missing branch.
- **All fifteen `l18b_*` keys are inert.** They are declared and validated (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:184-197`, `:403-416`) and wired into the runner (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:353-361`), but every step function returns the raw signal unchanged (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/confirmation.py:93-114`, `:117-131`, `:134-152`). This is the third-behaviour finding; see §5.

## 3. B configuration sweep — all 17 classes, 205 fields

| B class and range | Configuration family | Decision IDs | Coverage result |
|---|---|---|---|
| `SupertrendConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:12-18` | primary signal | C01, C23 | Covered |
| `RangeFilterConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:21-33` | range signal parameters | C01, C02 | Covered |
| `ConfirmationConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:36-68` | **pivot swing-break + momentum FSM** | **C38** (and C03/C04 for the A/Pine transform) | Covered; re-attributed in this round |
| `StopLossConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:71-84` | fixed / ATR / swing stop | C11, C19, C20 | Covered |
| `TakeProfitConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:87-95` | percent / ATR / R target | C12, C19, C20 | Covered |
| `BreakEvenConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:98-103` | BE trigger and buffer | C14 | Covered |
| `MultiTPConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:106-112` | TP1 fraction, TP2 | C13 | Covered |
| `TrailingConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:115-121` | activation and R distance | C15 | Covered; ATR-versus-R decided |
| `RiskConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:124-138` | risk %, leverage cap, fallback %, equity mode, notional assert, daily limits | C07-C10, C18 | Covered; C07 re-decided |
| `FilterConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:141-221` | MA, slope, volume, ATR-vol, McGinley, HTF trend, MACD hub, range regime, and five HTF timeframe fields | C02, C40, C41 | Covered; HTF and equation axes split out |
| `GuardConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:224-253` | drawdown, loss streak, cooldown, equity curve, MAE, four-mode recovery | C18 | Covered; ownership and counted-event decided |
| `TimeStopConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:256-268` | bars, EOD, EOW, condition, calendar timezone | C17, C25 | Covered |
| `ExitFilterBlockConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:271-280` | seven per-filter exit triggers | C16 | Covered |
| `TradeConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:283-323` | direction, flip, opposite/filter exit, regime lock, **`entry_mode`**, pyramid and signal-mode entries, same-bar re-entry, **`first_bar_requires_edge`** | C05, C06, C16, C21, **C39** | Covered; `entry_mode` and `first_bar_requires_edge` are new explicit rows |
| `StrategyConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:326-348` | capital, margin percentages, commission, slippage, mintick, pyramiding, terminal close | C08-C10, C22, C23 | Covered |
| `ParityConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:351-403` | fill contract, debug export, pre-roll, eval-start and terminal actions | C19, C20, C23 | Covered; two fields are **non-economic**, see §7 |
| `MTCConfig` `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:406-451` | composite routing of the sixteen sub-configs | C01-C41 | Covered through the component classes |

B-specific non-canonical behaviours, each carried to a decision rather than lost in the grouping:

| B behaviour | Resolving citation | Decision |
|---|---|---|
| swing stop includes the decision bar | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/risk/sl_calculator.py:135-142` | C11 |
| ATR NaN → `0.01`, swing ATR NaN → `0` | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/risk/sl_calculator.py:94-95`, `:152-153` | C11, C24 |
| R target with no stop → percent target | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/risk/tp_calculator.py:163-165` | C12 |
| TP ATR NaN → `0.01` | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/risk/tp_calculator.py:132-133` | C12, C24 |
| nearest-extreme intrabar path, ties to high-first | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py:612-619` | C19 |
| fixed `1e-6` quantity truncation, no min-qty, no min-notional | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py:2684-2690` | C09 |
| minimum stop-distance floor before dividing | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/risk/position_sizer.py:64-70` | C07, C24 |
| hard-coded `1.104` / `0.97` maintenance multipliers | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py:36`, `:644-649` | C10, C34 |
| affordability gate degenerated to `equity > 0` | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py:674-690` | C10 |
| `0.04`% commission and five-tick slippage defaults | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:334-335` | C22 |
| clamped `5×`-RMA warm-up, floor 200, ceiling 2000 | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py:511-513`, `:515-579` | C23 |
| eval-start and terminal flatten defaulting to true | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:387-403` | C23 |
| intrabar-extreme BE and R-distance trailing | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py:2450-2478`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/risk/tp_calculator.py:253-275` | C14, C15 |
| master `exit_on_filter_block` toggle | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:290` | C16 |
| guard order and counted event differ from A | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py:333-380` | C18 |
| `Signal`-mode adds survive the pyramiding refusal | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py:136-154`, `:1390-1402` | C06 |
| right-labelled HTF resample with no period shift | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/filters/htf_trend_filter.py:71-96` | C40 |
| first-value-seeded `ewm` EMA | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/indicators.py:22-29` | C41 |

## 4. The four omitted modules the audit required, swept in full

### 4.1 A `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/confirmation.py` (152 lines)

| Finding | Citation | Economically meaningful? | Disposition |
|---|---|---|---|
| `AdvancedConfirmationState` and its snapshot type exist, and the module docstring states it is "intentionally non-invasive by default" pending a later port | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/confirmation.py:8-28`, `:31-43` | No — state only | Retired with C38 |
| `apply_swing_break_confirmation` returns `raw` unchanged whether enabled or disabled | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/confirmation.py:93-114` | **No** — proven inert | C38 retirement; GF-38 field 8 proves inertness |
| `apply_confirmation_momentum` likewise | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/confirmation.py:117-131` | No | C38 |
| `finalize_advanced_confirmation_signal` composes the two and returns `raw` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/confirmation.py:134-152` | No | C38 |
| Fifteen configuration keys are declared and validated for this inert path | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:184-197`, `:403-416` | No | **RETIRE** (C38) |

### 4.2 A `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py` (605 lines)

| Finding | Citation | Economically meaningful? | Disposition |
|---|---|---|---|
| **Every** gate returns `long_ok=True, short_ok=True` when its required input is `None` — eighteen distinct sites | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:33-34`, `:49-55`, `:74-80`, `:96-97`, `:116-117`, `:139-140`, `:163-164`, `:182-183`, `:197-198`, `:212-213`, `:244-245`, `:307-310`, `:338-341`, `:392-393`, `:401-402`, `:440-441`, `:487-488`, `:583-586` | **Yes** — an unready gate permits entry | C02 (fail closed) |
| HTF trend gate **substitutes the raw HTF close for the MA** when the tracker is not ready | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:395-402` | **Yes** — a different series is compared | **C41** (new row) |
| MACD histogram gate substitutes `0.0` for a missing previous histogram in `RISING` modes — **and this reproduces the tracked Pine**, which does the same (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:999-1002`), so it is a Pine-faithful behaviour that C41 rejects on economic grounds, not an A-only defect | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:212-231`, `:217` | **Yes** | **C41** |
| HTF buffer applied multiplicatively and **loosely**: long needs `close > ma × (1 − buf)` — likewise Pine-faithful (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:1040-1042`) and likewise rejected | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:404-406` | **Yes** — a positive buffer loosens instead of tightening | **C41** |
| HTF trend gate passes unconditionally while the HTF **snapshot** is unready (distinct from the raw-close substitution above, which applies when the snapshot is ready and the tracker is not) — also Pine-faithful (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:1040-1042`) | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:392-393` | **Yes** — an unready HTF gate permits entry | C02, **C41** |
| Nine gate-name constants and two extra gate names define the filter-exit ladder membership | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:14-24`, `:258-259`, `:361`, `:420-421`, `:521` | Yes — ordering | C16 |
| Candle-pattern equations (engulf, hammer, shooting star) are hard-coded, with fewer than two bars passing through | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:262-299`, `:307-310` | Yes | C02 |
| Level-proximity gate: `near(level)` is a symmetric percentage band around the swing high/low | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:331-354` | Yes | C02, C04 |
| Session table hard-codes four named sessions with IANA zones; an unknown name **passes through** | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:514-519`, `:588-598` | **Yes** | C18, C25 |
| Session string parser defaults an absent zone to UTC | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:547-563` | Yes | C25 |
| Momentum gate: `ATR_BODY` and `ROC_1` equations, each passing through when its input is unavailable | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:456-507` | Yes | C02, C41 |

### 4.3 A `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/htf.py` (197 lines)

| Finding | Citation | Economically meaningful? | Disposition |
|---|---|---|---|
| Only six timeframe strings are accepted; anything else raises | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/htf.py:18-25`, `:37-42` | Yes | **C40** |
| Resample is `label="left", closed="left"` with incomplete trailing bars dropped | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/htf.py:101-103` | Yes | **C40** |
| The alignment offset is **inferred from the first two resampled bars**, not from the declared timeframe | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/htf.py:144-149` | **Yes** — a leading data gap mis-shifts the whole series | **C40** |
| Fewer than two HTF bars yields an all-NaN frame | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/htf.py:133-142` | Yes | **C40** |
| A requested HTF shorter than the LTF returns all-`None` rather than a configuration error | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/htf.py:175-179` | Yes | **C40** |
| Daily/weekly chart-timezone anchoring accepts only `UTC±offset`; a named zone silently becomes UTC | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/htf.py:75-96` | **Yes** — day and week boundaries move | **C40**, C25 |
| The prior-closed `request.security(..., expr[1], lookahead_off)` contract is documented in the module itself | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/htf.py:6-11`, `:107-127` | Yes | **C40** (adopted as canonical) |

### 4.4 B `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fee_model.py` (347 lines)

| Finding | Citation | Economically meaningful? | Disposition |
|---|---|---|---|
| **The module has no importer anywhere in the production tree**; `engine/__init__.py` exports neither it nor `fills` | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/__init__.py:3-17` | **No — not wired** | **Legacy non-authority.** No capability row; recorded here |
| `notional = price × quantity` omits the contract multiplier | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fee_model.py:122-124` | Would be, if wired | C08 (as an arithmetic RED) |
| Slippage is applied adversely on both entry and exit, and commission is charged on the **adjusted** price | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fee_model.py:149-191`, `:193-247` | Would be | C22 (arithmetic reference) |
| `tick_size_source ∈ {"exchange","fixed"}` is declared but `from_config` never reads it | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fee_model.py:42-45`, `:100-107` | **No — no consumer** | Non-economic dead configuration; §7 |
| **No funding model of any kind exists in the module** | whole file | **Yes, by absence** | C22 (`COST_MODEL_UNAVAILABLE`) |
| `calculate_net_pnl` computes gross PnL from nominal prices and subtracts round-trip cost including slippage — algebraically equal to filling at slipped prices | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fee_model.py:278-309` | Would be | C22; no defect found |

### 4.5 B `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fills.py` (556 lines)

| Finding | Citation | Economically meaningful? | Disposition |
|---|---|---|---|
| **No production importer.** The only reference in the repository is one test | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/tests/test_fill_contract_baseline.py:3-6` | **No — not wired** | **Legacy non-authority.** No capability row |
| Declares a four-value `SameBarConflictPolicy` — `WORST_CASE`, `BEST_CASE`, `SL_PRIORITY`, `TP_PRIORITY` — and a resolver | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fills.py:36-47`, `:172-220` | Would be, if wired | C19. **This module is the likely origin of the previous revision's false claim that A exposes a selectable collision policy; it is B's dead module, and A hard-codes stop-first** |
| Declares `FillType`, `BarData`, `FillResult`, `PositionState`, `FillPolicy` | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fills.py:24-101` | No | Legacy |
| `check_sl_hit` / `check_tp_hit` / `check_trailing_stop_hit` and their fill-price helpers | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fills.py:102-171`, `:221-244` | Would be | C11, C12, C20 |
| `get_entry_fill_price(use_next_open=True)` — a next-open entry convention that neither live engine uses | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fills.py:245-264` | Would be | C20 (recorded as an unused alternative) |
| `FillsEngine.update_trailing_stop` / `update_break_even` / `evaluate_exits` / `evaluate_entry` | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fills.py:265-556` | Would be | C14, C15, C16, C20 |

**Disposition statement for §4.4 and §4.5.** Neither module is reachable from any runner, CLI or script in the production tree, so neither can produce an economic result today. They are therefore dispositioned as **legacy, non-authority** rather than given capability rows: a row would assert that a live capability exists where none does. Their contents are nonetheless carried into the decisions above as arithmetic references and as D026 RED sources, and `COVERAGE_SWEEP.md` records them so a future re-wiring cannot arrive unnoticed. Both fall inside the WP-P0-19/WP-P0-23 legacy-removal scope discussion, not inside WP-P0-09's decision scope.

## 5. The third confirmation behaviour, stated honestly

The previous revision described confirmation as a two-way A-versus-B disagreement handled inside C03 and C04. That was not truthful. **Three distinct behaviours exist at the evidence base**, and one of them was hidden by a module name.

| # | Behaviour | Where it lives | Is it economically active? |
|---|---|---|---|
| 1 | **N-bar count transform** — direction change resets the count, a same-direction bar increments, refresh resets, a close-cross test can reset, arming is one-shot | A `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:824-892` and Pine `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:1684-1739` | **Yes** — decided by C03 |
| 2 | **Pivot swing-break + momentum FSM** — confirmed pivots with a left/right window, wait state, dynamic level updates, timeout, pivot age, tie rule, break buffer, deferred break | B only: `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/confirmation_layer.py:13-34`, `:104-105`, `:175-411`; configuration at `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:36-68` | **Yes** — decided by the new C38 |
| 3 | **`l18b_*` pass-through scaffold** — a state container, a snapshot, three step functions, fifteen configuration keys, and no effect | A only: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/confirmation.py:93-114`, `:117-131`, `:134-152`; keys at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:184-197` | **No** — proven inert; retired by C38 with GF-38 field 8 as the proof obligation |

Two consequences follow, and both are recorded rather than glossed:

1. **The table must not read as though A implements behaviour 2.** It does not. A's only confirmation capability is behaviour 1, plus a level-retest transform (C04) that is a proximity band rather than a retest (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:914-919`).
2. **B's two unresolved corpus cases belong to behaviour 2, not to behaviour 1.** The previous revision mapped cases 402 and 416 to C03/C04, which are A's transforms. That attribution is corrected in §10.3.

## 6. Pine input and execution sweep

The 153 `input.*` declarations were swept by functional group and their execution consumers inspected.

| Pine range | Family | Decision IDs |
|---|---|---|
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:7` | `strategy()` declaration: `process_orders_on_close=true`, `pyramiding=100`, no margin, no commission, no slippage | C06, C10, C20, C22 |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:16-94` | signal, direction, sizing, exits, gates, guards, timing inputs | C01-C24 |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:95-101` | the seven `tw_*` constants, all consumerless | C31-C37 |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:102-175` | confirmation, filters, guard and time extensions, stop/target detail | C02-C24, C40, C41 |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:176-188` | the thirteen `wt_*` inputs | C28-C30 |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:240-361` | tick/quantity helpers, stop and target functions, `calc_l6_qty` | C07-C13, C24 |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:943-1119` | signal gates, session, readiness | C01-C04, C18, C23, C40 |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:1143-1921` | BE, trailing, price exits, opposite and filter exits, time exits, guards, confirmation, entries | C03-C06, C11-C21, C38 |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:2005` | HTF trend line plot — the prior-closed state A's module documents | C40 |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:2008-2028` | WunderTrading alert serialiser, including the two `alert()` calls | C28-C30 |

Two absence findings from the Pine sweep, both load-bearing:

- No production-cost or venue-margin authority exists in the `strategy()` declaration (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:7`), so C10 and C22 fail closed rather than treating absent settings as an authoritative zero.
- Pine's L18 block is the **N-bar count transform**, not a pivot FSM (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:1684-1739`), and its `l18b_*` fragment operates on that same transform's state (`:1709-1718`). Pine therefore does not corroborate behaviour 2 of §5.

## 7. Non-economic dispositions

The Lead's correction is applied here: a purely non-economic setting gets an **explicit disposition with reasoning in this sweep**, not a capability row. Each row below was checked to its consumer, and each is dispositioned because that consumer cannot change an economic result.

| Setting | Declared at | Consumer | Why non-economic | Disposition |
|---|---|---|---|---|
| `debug_mode` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:36` (validated `:262`) | Populates a debug-metadata dictionary and nothing else (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:1050-1064`) | The dictionary is written after every economic decision on the bar and is read by no branch; no fill, quantity, price, reason or state hash depends on it | **Non-economic.** Keep as an observability flag outside the economic configuration surface; excluded from the frozen package hash. No capability row |
| `export_debug_csv` | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:362-365` | Post-run CSV export | Emits a file after the run completes; no decision reads it | **Non-economic.** Same disposition |
| `debug_dir` | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:366` | Output path for the above | A filesystem path | **Non-economic.** Same disposition |
| `tick_size_source` | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fee_model.py:42-45` | **None** — `from_config` copies `commission_percent`, `slippage_ticks` and `tick_size`, and never reads the selector (`:100-107`) | A provenance selector with no reader cannot alter any number | **Non-economic dead configuration.** Retire with the legacy module (§4.4); if the module is ever re-wired, tick provenance must come from frozen instrument metadata under C09 |
| `use_notional_hard_assert` (A's `use_notional_assert`) | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:71` | **Overwritten to `False` before validation** (`:614-618`) | It cannot be set to `True` at runtime, so it selects nothing in A | **Non-economic in A.** In B it *is* economic (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py:2678-2682`) and is covered by C07 |
| `equity_source` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:70` | **Overwritten to `"Realized"` before validation** (`:614-618`) | Same reason | **Non-economic in A**; the provenance question is decided by C07 |
| `instrument_symbol` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:43` | Carried into frozen metadata (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/instrument.py:8-27`) | An identity label; no arithmetic depends on it | **Identity, not economics.** Belongs to C26's bar-identity tuple, not to a separate row |
| `instrument_point_value` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:44` | Stored on the metadata record and not used in any A arithmetic; A's arithmetic uses `contract_multiplier` | Duplicate of the multiplier concept with no reader | **Non-economic duplicate.** C08 makes `contract_multiplier` the single dimensional authority; `point_value` is retired |

**Explicitly not added as capability rows**, on the Lead's instruction and because the required omitted-module sweep produced no economically meaningful behaviour that forces them: snapshot drift handling, the allocator/Guardian internal split, venue order-edge behaviour, and debug configuration. Snapshot identity is already carried by C07's `BoundSizingIntent` and C26's identity rules; the allocator/Guardian split is WP-P0-04's decided ownership, restated in C07 and C18 rather than re-decided.

## 8. Negative and absence sweep

Each row is a search that returned nothing, with the command that reproduces it from the repository root.

| Search | Result | Meaning | Decision |
|---|---|---|---|
| `grep -rn "wt_" MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/` | no match | B has no WunderTrading capability | C28-C30 |
| `grep -rn "tw_" MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/` | no match | B has no TradingView compatibility switches | C31-C37 |
| `grep -rn "wt_\|tw_" MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/ --include=*.py` excluding `core/config.py` | `tw_*` matches only in `core/position_sizer.py`, `core/exits.py`, `core/runner.py`; **zero `wt_*` matches** | A's thirteen `wt_*` keys have no runtime consumer; six `tw_*` keys do | C28-C30, C31-C37 |
| `grep -n "tw_" MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine` | matches only at `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:95-101` | Pine declares the constants and branches on none of them | C31-C37 |
| `grep -rn "tw_margin_call_split_entries" MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:62`, `:286`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:133`, `:1057` | Read twice, consumed by no branch | C35 |
| `grep -rn "fee_model\|FeeModel\|FillsEngine" MTC_COMMAND_CENTER/02_MTC_BACKTEST/ --include=*.py` excluding the two modules themselves | one hit, in `tests/test_fill_contract_baseline.py` | Both modules are unreachable from the production tree | §4.4, §4.5 |
| `grep -rn "funding" MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fee_model.py` | no match | No funding model exists in the only cost module | C22 |
| `find MTC_COMMAND_CENTER -iname "*MASTER_ARCHITECTURE*"` | one file: `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md` | `_AI_MEMORY/MASTER_ARCHITECTURE_DECISIONS_AND_TARGET_STATE_2026-08-19.md` does not exist | Citation repair, `LANE_REPORT.md` |
| `git log --all --diff-filter=A --name-only -- "*MASTER_ARCHITECTURE_DECISIONS*"` | no output | The file exists in no Git ref either | Citation repair |
| durable intent/revision ledger in A, B or Pine | none found | Replay safety needs contract-defined identity | C26, C27 |
| authoritative funding schedule in A, B or Pine | none found | Absence cannot mean zero production cost | C22 |
| venue margin schedule in A, B or Pine | none found | Both margin approximations are fabricated | C10, C34 |

## 9. Required-family checklist

| Required family | Decision coverage |
|---|---|
| Entries and raw direction | C01, C05, C39 |
| Exits and opposite signal | C13, C16-C21 |
| Fixed / ATR / swing stops | C11 |
| ATR trailing and break-even | C14, C15 |
| Percent / ATR / R targets and MultiTP | C12, C13 |
| Sizing request, ownership, contract multiplier | C07, C08 |
| Quantity, tick and min-notional boundaries | C09, C24 |
| Time stops | C17 |
| Session and day limits, cooldowns | C06, C18 |
| Signal gating, confirmation, refresh, retest | C02, C03, C04, C38 |
| Same-bar flip and re-entry | C05, C21, C32, C33 |
| Gap and same-bar fill assumptions | C19, C20 |
| Fees, slippage, funding | C22 |
| Margin, leverage, liquidation | C10, C34, C35 |
| Warm-up, evaluation boundary, terminal behaviour | C23 |
| Restart and missed bars | C25, C26, C27 |
| Timestamp discipline | C25 |
| Duplicate and reordered bars | C26 |
| Cancel, revision, idempotence | C26 |
| Short symmetry, invalid and boundary values | C24 |
| Higher-timeframe series and alignment | **C40** |
| Indicator equations, seeds and readiness substitution | **C41** |
| Entry-event semantics | **C39** |
| All 13 `wt_*` | C28-C30 |
| All 7 `tw_*` | C31-C37 |
| All 15 `l18b_*` | **C38** |

Every required family is covered. No family is deferred by the WP-P0-09 timebox.

## 10. WP-P0-06 corpus evidence, mapped case by case

The previous revision mapped the 23 soft-pass cases as one aggregate row to "C07-C09" and mapped the two B cases to the wrong capability. Both are replaced. **Every one of the 23 soft-pass cases and every one of the 8 unresolved A failures appears exactly once below, with its own evidence citation, its own capability, and its own discriminating fixture.**

### 10.1 What the corpus actually records — the structural facts that determine attribution

Three facts read directly off the per-case blocks decide how each case must be attributed, and they were not stated in the previous revision:

1. **For all 23 soft-pass cases, TradingView, PineTS and Python report the *same* trade count, and `PineTS/Python = PASS`.** Only `TW/PineTS` and `TW/Python` fail. Example: case 103 records `Trades: TW=7 | PineTS=7 | Python=7` with `Parity: SOFT_PASS | TW/PineTS=FAIL | TW/Python=FAIL | PineTS/Python=PASS` (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:14-20`). The two Python-side engines agree with each other; the divergence is against the TradingView workbook, and the corpus inventory names its axis explicitly as a strict **quantity** mismatch under a `0.001` strict / `0.005` soft tolerance (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_06_PARITY_CORPUS_2026-08-24/PARITY_CORPUS_INVENTORY.md:27`, `:46`).
2. **The eight failures split into two classes.** Cases 110 and 111 have identical counts across all three engines with **all three** pairwise comparisons failing, including `PineTS/Python` — a timing and price divergence, not a selection divergence (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:70-76`, `:78-84`). Cases 134, 147, 153, 154, 155 and 162 record `TW/PineTS = PASS` with `PineTS/Python = FAIL` — Pine and PineTS agree and the **A implementation** diverges.
3. **Therefore each case has two axes, and both are named below:** the *varied capability*, which selects the trade population and, through the stop distance it changes, the sizing input; and the *divergence carrier* recorded by the corpus. Naming only the first would be untruthful about what failed; naming only the second would be the aggregate mapping the audit rejected.

### 10.2 The eight unresolved A failures

| Case | Varied setting | Corpus evidence | Capability that drives the divergence, cited to the implementing line | Discriminating fixture |
|---|---|---|---|---|
| `case_110` | `time_stop_eod` | TW 142 / PineTS 142 / Python 142; all three pairwise strict comparisons FAIL (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:70-76`) | **C17** — A fires EOD on the **first bar of the next calendar day**, from a UTC date-string comparison, rather than at the last scheduled bar close (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:687-691`) | **GF-17 R3** — asserts the exit lands on the Friday 21:45Z bar and fails RED against the next-day-open behaviour |
| `case_111` | `time_stop_eow` | TW 136 / PineTS 136 / Python 136; all three pairwise strict FAIL (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:78-84`) | **C17** — A's EOW is a hard-coded `weekday()==4 and hour>=21` UTC rule with no calendar (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:692-695`) | **GF-17 R4** — asserts `CALENDAR_UNAVAILABLE` where A fires from the hard-coded hour |
| `case_134` | `refresh_on_new_raw` | TW 0 / PineTS 0 / Python 131; `TW/PineTS=PASS`, `PineTS/Python=FAIL` (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:262-268`) | **C03** — A's refresh resets the confirmation count to **0**, not 1, which for a pulse producer suppresses or delays every emission; the source comment states the intent (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:840-847`) | **GF-03 R1** — the reset-to-1 rule emits on bar 13 where A's reset-to-0 emits on bar 14 |
| `case_147` | `pair_htf_trend_exit` | TW 124 / PineTS 124 / Python 126; `TW/PineTS=PASS` (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:366-372`) | **C40** primarily — A's HTF alignment offset is inferred from the first two resampled bars rather than from the declared timeframe (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/htf.py:144-149`) and the gate substitutes the raw HTF close when the MA is unready (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:395-402`); **C16** secondarily, because the HTF-trend filter exit is last in A's nine-branch ladder (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:653-656`) | **GF-40 R1 and R3** (alignment, and the declared-versus-inferred period, whose R3 bar table enumerates every resulting HTF bar) plus **GF-41 F4** (raw-close substitution) and **GF-16 R3/R4** (ladder order). **GF-02 is explicitly not sufficient here** |
| `case_153` | `pair_confirm_refresh` | TW 0 / PineTS 0 / Python 146; `TW/PineTS=PASS` (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:414-420`) | **C03** — the same reset-to-0 refresh path as case 134, exercised together with the direction-change branch (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:832-847`) | **GF-03 R1 and R3** |
| `case_154` | `pair_level_retest_confirm` | TW 27 / PineTS 27 / Python 44; `TW/PineTS=PASS` (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:422-428`) | **C04** — A's retest is a symmetric **proximity band at the close**, with no touch, no cross and no direction test, so it admits bars that never interacted with the level (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:914-919`) | **GF-04 R3** — a bar that closes inside the band but never reaches the level emits under A and must not emit under the decided rule |
| `case_155` | `pair_macd_htf_regime` | TW 55 / PineTS 55 / Python 76; `TW/PineTS=PASS` (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:430-436`) | **C41** primarily — A's MACD is built from an SMA-seeded EMA tracker while the HTF MA tracker is fed **once per LTF bar** with no de-duplication, so the declared length does not mean HTF bars (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/ma.py:320-373`, `:376-406`), and the histogram gate substitutes `0.0` for a missing previous value (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:217`). **Both of those A behaviours reproduce the tracked Pine** — the per-LTF-bar HTF feed at `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:895-901` and `:903-918`, the `0.0` substitution at `:999-1002` — so the divergence carried here is A against **B/PineTS**, not A against Pine, and C41 corrects both by deliberate decision rather than by parity repair. **C40** secondarily, for the HTF MACD visibility offset (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/htf.py:144-149`) | **GF-41 F1** (LTF seed, with the custom-Pine column asserted GREEN and B's `10.0, 15.0, 22.5, 31.25, 40.625` asserted RED), **F3** (histogram readiness, three distinct bar-4 verdicts) and **F2** (HTF sampling basis, where A and the built-in Pine HTF path agree and both fail RED), plus **GF-40 R1** (alignment). **GF-02 cannot discriminate an equation difference** |
| `case_162` | `pair_ma_htf_htf_trend` | TW 96 / PineTS 96 / Python 94; `TW/PineTS=PASS`; the effect column notes the comparison used `case_159` because 160 and 161 are missing (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:470-476`) | **C41** primarily — the HTF MA sampling basis and the **loose multiplicative buffer** `close > ma × (1 − buf)` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/ma.py:376-406`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:404-406`), both of which reproduce the tracked Pine (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:920-934`, `:1040-1042`) and are corrected by decision rather than by parity repair; **C40** secondarily for the alignment offset | **GF-41 F2** (sampling basis — A's `htf_ma` is `108.00` on the `09:00`–`11:00` bars against the decided `104.00`, and the built-in Pine HTF column matches A) and **F2b** (buffer sign — four distinct verdicts on the `08:00` bar: decided `(false,false)`, A `(true,true)`, built-in-Pine-HTF `(true,true)`, B `(false,true)`), plus **GF-40 R1** |

### 10.3 Corpus B's two unresolved cases — attribution corrected

The previous revision recorded these as "B dynamic confirmation cases 402/416" mapped to C03/C04 and GF-03/GF-04. C03 and C04 are **A's** N-bar transform and level-retest transform; B implements neither. The case files name the actual mapped configuration paths.

| Case | Mapped configuration path | Evidence | Corrected capability | Discriminating fixture |
|---|---|---|---|---|
| `402 parity_bnd_211_swing_right_bars_v03` | `confirmation.p_right = 14`, under the parent input "Use Confirmation: Swing Break + Momentum = On" (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/cases/parity_bnd_211_swing_right_bars_v03.json:115-145`); TradingView 123 versus Python 236 (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:33-42`) | Not "dynamic confirmation" — this is the **pivot right-bar window** of the swing-break FSM (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/confirmation_layer.py:13-34`, `:104-105`) | **C38** primarily; **C23** secondarily, because the case passes only after overlap clipping and is tagged `TV_EARLY_TRADE_END_CANDIDATE` with the raw-count-versus-overlap policy explicitly unresolved (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:167-173`, `:187-200`) | **GF-38 R2** — `p_right = 2` versus `4` changes the pivot confirmation bar and the wait-start bar; plus **GF-23 R3/R4** for the clip and terminal policy |
| `416 parity_bnd_217_dynamic_update_mode_v02` | `confirmation.dyn_update_mode = "ANY"` with `dynamic_level_while_waiting = true` (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/cases/parity_bnd_217_dynamic_update_mode_v02.json:115-135`); TradingView 129 versus Python 189 (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:44-52`) | The **dynamic level update while waiting** inside the same FSM, together with `defer_break_on_level_update` (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/confirmation_layer.py:310-337`, `:350-358`) | **C38** primarily; **C23** secondarily, same clip-policy reason | **GF-38 R3** — `ANY` versus `TIGHTEN_ONLY` with the deferred break asserted; plus **GF-23 R3/R4** |

Both cases also carry the corpus-level caveat that a later same-bar-flip fix touched both Pine and Python while the full re-run remained pending, so the aggregate is not post-fix regression evidence (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:83-96`). That caveat is why C05 and C21 hold the same-bar flip decision, and why neither B case is used as evidence for it.

### 10.4 The 23 soft-pass cases, one row each

Every row names the varied capability with the line that implements it, and the divergence carrier with the line that implements it. The carrier is the same for all 23 because the corpus records the same axis for all 23 — a strict TradingView-versus-Python **quantity** mismatch with matching trade counts — and it is stated once here rather than repeated: **C07 / C08 / C09**, carried by A's risk denominator omitting the contract multiplier (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_sizer.py:43-47`) where Pine includes it (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:339-348`), and by the step-floor and minima path (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_sizer.py:60-68`) against Pine's min-contract-only rule (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:359-361`). Fixtures **GF-07**, **GF-08** and **GF-09** discriminate that carrier; the per-case fixture column names what additionally discriminates the varied capability.

| Case | Varied setting | Corpus evidence | Varied capability, cited to its implementing line | Mechanism by which it reaches the quantity | Additional discriminating fixture |
|---|---|---|---|---|---|
| `case_103` | `use_candle_pattern_gate` | TW 7 / PineTS 7 / Python 7 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:14-20`) | **C02** — candle-pattern equations and the fewer-than-two-bars pass-through (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:262-299`, `:307-310`) | selects which bars become entries, and therefore which stop distances enter the sizer | **GF-02** (b)/(c)/(d) |
| `case_104` | `use_level_proximity_gate` | TW 16 / PineTS 16 / Python 16 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:22-28`) | **C02** — proximity band around the swing high/low (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:331-354`) | same | **GF-02** |
| `case_105` | `level_proximity_threshold_pct` | TW 60 / PineTS 60 / Python 60; recorded `expected 0.25 \| prev 2 \| actual 3` (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:30-36`) | **C02** — the threshold read at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:343` and applied at `:347-353` | same | **GF-02**; see the evidence-quality note in §10.5 |
| `case_106` | `level_proximity_lookback` | TW 24 / PineTS 24 / Python 24 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:38-44`) | **C02** — the window is the `_level_prox_history` deque length (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:242-244`, `:1044`, `:1210`); **this key was outside every declared range in the previous sweep** | same | **GF-02** with the lookback varied |
| `case_109` | `time_stop_condition` | TW 131 / PineTS 131 / Python 131 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:62-68`) | **C17** — the condition reads `last_realized_pnl`, the previous closed trade (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:677-685`) | changes which positions are exited early, changing the equity path the sizer reads | **GF-17 R2** |
| `case_112` | `use_daily_loss_limit` | TW 128 / PineTS 128 / Python 128 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:86-92`) | **C18** — daily-loss guard, first in A's ladder (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:763-769`) | blocks entries, changing the trade population and the realised-equity path | **GF-18** with the guard ladder asserted |
| `case_113` | `max_daily_loss_pct` | TW 108 / PineTS 108 / Python 108 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:94-100`) | **C18** — the same guard's threshold (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:766-768`) | same | **GF-18** |
| `case_114` | `use_max_trades_per_day` | TW 131 / PineTS 131 / Python 131 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:102-108`) | **C18** — A counts **closes**, not entries (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:746-747`, `:770-773`) | changes which entries survive, and the counted event differs from B's | **GF-18** — its RED is exactly this counter |
| `case_115` | `max_trades_per_day` | TW 83 / PineTS 83 / Python 83; recorded `expected 2 \| prev 3 \| actual 1` (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:110-116`) | **C18** — same counter and threshold | same | **GF-18**; see §10.5 |
| `case_126` | `guard_recovery_bars` | TW 131 / PineTS 131 / Python 131 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:198-204`) | **C18** — the `Bars` recovery countdown runs unconditionally once armed (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:796-811`) | controls when blocked entries resume | **GF-18** with recovery armed |
| `case_127` | `guard_recovery_signals` | TW 131 / PineTS 131 / Python 131; `Effect: NO`, trade delta `+0` (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:206-212`) | **C18** — the `Signals` recovery mode (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:802`, `:804-811`) | none observed in this case — the setting produced no trade-set change | **GF-18**; see §10.5 |
| `case_128` | `use_trade_cooldown` | TW 90 / PineTS 90 / Python 90 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:214-220`) | **C06** — post-exit cooldown, a separate term from `cooldown_bars` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:813-817`) | suppresses entries after exits | **GF-06** — its RED is the entry-spacing-versus-post-exit confusion |
| `case_129` | `cooldown_bars_after_exit` | TW 94 / PineTS 94 / Python 94 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:222-228`) | **C06** — the same term's length (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:816`) | same | **GF-06** |
| `case_130` | `use_confirm_transform` | TW / PineTS / Python counts equal (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:230-236`) | **C03** — the whole N-bar transform is gated on this key (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:827`) | delays every entry by up to `confirm_bars`, changing entry prices and stop distances | **GF-03 R2** |
| `case_132` | `confirm_close_crosses` | TW 131 / PineTS 131 / Python 131 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:246-252`) | **C03** — a failed close-cross resets the count to 0 on **any** bar (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:851-859`) | same | **GF-03** with the cross test enabled |
| `case_133` | `require_raw_still_true` | TW 131 / PineTS 131 / Python 131; `Effect: NO` (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:254-260`) | **C03** — the arming guard (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:860-866`) | none observed in this case | **GF-03**; see §10.5 |
| `case_137` | `retest_buffer_pct` | TW 131 / PineTS 131 / Python 131 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:286-292`) | **C04** — the proximity band width (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:914-919`) | widens or narrows which bars re-emit, changing entry prices | **GF-04 R3** — the band-versus-touch RED |
| `case_138` | `pair_sl_atr_be` | TW 125 / PineTS 125 / Python 125 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:294-300`) | **C11** ATR stop (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:191-196`) with **C14** BE (`:332-348`) | the ATR stop **is** the sizer's denominator, so this pair changes the quantity directly | **GF-11 R2** and **GF-14** |
| `case_139` | `pair_sl_atr_trail` | TW 134 / PineTS 134 / Python 134 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:302-308`) | **C11** with **C15** trailing (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:300-330`) | same | **GF-11 R2** and **GF-15** |
| `case_140` | `pair_sl_atr_tp_atr` | TW 134 / PineTS 134 / Python 134; trade delta `+0` (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:310-316`) | **C11** with **C12** ATR target (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:213-233`) | same | **GF-11 R2** and **GF-12 R3** |
| `case_141` | `pair_sl_atr_tp_r` | TW 134 / PineTS 134 / Python 134; trade delta `+0` (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:318-324`) | **C11** with **C12** R target, which depends on the stop (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:213-233`) | the R target is a function of the same denominator | **GF-12 R1 and R2** |
| `case_142` | `pair_sl_atr_tp_multi` | TW 161 / PineTS 161 / Python 161 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:326-332`) | **C11** with **C13** MultiTP (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:450-493`) | partial fills split one lifecycle into fragments whose quantities are compared individually | **GF-13 R1 and R2** |
| `case_143` | `pair_sl_percent_tp_percent` | TW 142 / PineTS 142 / Python 142 (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:334-340`) | **C11** percent stop (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:198-201`) with **C12** percent target (`:213-233`) | the percent stop is the denominator | **GF-11 R3** and **GF-12** |

### 10.5 Evidence-quality caveats recorded rather than smoothed over

- **Three soft-pass cases did not apply the setting they name.** Case 105 records `expected 0.25 | prev 2 | actual 3` and case 115 records `expected 2 | prev 3 | actual 1`; both have `Settings check: FAIL` with two recorded mismatches (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:30-36`, `:110-116`). Their independent variable is therefore not the declared one, and the mapping above names the capability, not the intended value.
- **Two soft-pass cases produced no trade-set effect at all.** Cases 127 and 133 record `Effect: NO` with a trade delta of `+0` and identical PnL (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:206-212`, `:254-260`), so they demonstrate the quantity axis but carry no information about the varied capability.
- **Every case records one accepted setup deviation**, the leverage cap of 5 and an inert confirmation mismatch (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:482-484`), so no case is a clean single-variable experiment.
- **Case 162's effect column was computed against `case_159`** because the `case_160` and `case_161` exports are absent (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:470-476`); the corpus records 58 of 60 planned exports (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_06_PARITY_CORPUS_2026-08-24/PARITY_CORPUS_INVENTORY.md:26`).
- **The corpus generation-time Pine and Python identities are `UNKNOWN`** and the tracked Pine snapshot is a different short-title (`MTCV2_1404` versus the corpus's `MTCV2_1304`) (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_06_PARITY_CORPUS_2026-08-24/PARITY_CORPUS_INVENTORY.md:22-23`). Every mapping above is therefore a mapping of *evidence of disagreement* onto a decided capability, never a claim that the corpus validates the decision.
- **The old corpus is not an oracle for the newly decided semantics.** C03's reset-to-1, C04's touch-and-close-back, C17's last-scheduled-bar EOD and C40/C41's declared alignment and equations are all *new* rules; the corpus can only show that the current implementations disagree, which is what it is used for here.

## 11. Coverage conclusion

The decision table covers all 192 A configuration keys under contiguous ranges with no gap, every one of B's 17 configuration classes and 205 field declarations, all 153 Pine input declarations by functional group, all 13 `wt_*` keys, all 7 `tw_*` keys, all 15 `l18b_*` keys, every mandatory economic family, and the five modules the audit required be swept. Four capabilities that the previous revision did not name — the pivot confirmation state machine, entry-event semantics, higher-timeframe series construction, and indicator equation and readiness authority — now carry explicit decisions as C38 through C41. Eight non-economic settings carry explicit dispositions with reasoning in §7 rather than capability rows.

This conclusion is about **decision coverage only**. It is not runtime acceptance, not parity, and not trading approval.
