# WP-P0-09 Coverage Sweep

**Base SHA:** `fead492b0b87f207aa6e7a259372b9767d4301f9`

**Purpose:** prove that the canonicalization table covered the requested economic families and configuration surfaces. This is a source/configuration sweep, not a parity claim.

## 1. Scope and method

The sweep inspected only the lane-authorized subjects and prior evidence:

- A default configuration and consumers: `01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py`, `runner.py`, `exits.py`, `position_sizer.py`, `position_manager.py`, `instrument.py`, `rounding.py`, and `types.py`.
- B configuration and consumers: `02_MTC_BACKTEST/src/config/defaults.py`, `src/engine/mtc_runner.py`, `src/engine/mtc_state.py`, and `src/modules/`.
- Pine inputs and execution reference: `01_MTC_PROJECT/01_PINE/MTC_V2.pine`.
- WP-P0-06 corpus inventory, WP-P0-04 contract README/types, the architecture decision brief, and the WP-P0 work-package plan.

Token-efficient searches were performed by exact symbol/prefix (`wt_`, `tw_`, sizing, stop, target, margin, confirmation, cooldown, time, fee, slippage, funding) and then the owning line ranges were read. No backtest, network call, or runtime mutation was performed.

Inventory counts at the base SHA:

| Surface | Count | Counting boundary |
|---|---:|---|
| A `DEFAULT_CONFIG` string keys | 192 | `core/config.py:28-246` |
| B typed field declarations | 205 | 17 config classes in `src/config/defaults.py:12-451`, including composite fields |
| Pine `input.*` declarations | 153 | full `MTC_V2.pine` input sweep |
| A `wt_*` keys | 13 | `core/config.py:226-238` |
| A `tw_*` keys | 7 | `core/config.py:58-64` |

## 2. A configuration sweep

Every one of the 192 A keys falls within a reviewed range below. “Decision IDs” point to the detailed authority in `CAPABILITY_CANONICALIZATION_TABLE.md`.

| A range | Configuration family | Decision IDs | Coverage result |
|---|---|---|---|
| `config.py:29-35` | direction, flip, regime, max entries, cooldown, warm-up override | C05, C06, C23 | Covered |
| `config.py:37-42` | raw signal source/settings | C01 | Covered |
| `config.py:43-55` | instrument, capital, tick/qty/minimums, margin profile | C08-C10, C22 | Covered |
| `config.py:58-64` | all seven `tw_*` keys | C31-C37 | Covered individually |
| `config.py:65-71` | fixed quantity, risk %, fallback, leverage, equity source, notional assertion | C07-C10 | Covered; dormant/ambiguous fields explicitly resolved |
| `config.py:72-128` | MA/slope/volume/ATR-vol/McGinley/HTF/MACD/range gates | C02, C23, C24 | Covered as declared-profile formulas plus readiness/failure rules |
| `config.py:129-144` | opposite/filter exit switches | C16 | Covered |
| `config.py:146-150` | candle/level handling | C01, C04, C20 | Covered |
| `config.py:153-178` | time exits, day/trade/guard/cooldown/recovery | C17, C18 | Covered; ownership split decided |
| `config.py:180-204` | confirmation, refresh, retest | C03, C04 | Covered; exact state machines decided |
| `config.py:206-224` | stop, TP, MultiTP | C11-C13, C19-C20 | Covered |
| `config.py:226-238` | all thirteen `wt_*` keys | C28-C30 | Covered exactly; all dispositioned |
| `config.py:239-245` | BE and trailing | C14, C15 | Covered |

Consumer/disposition findings from the sweep:

- `fixed_qty` is declared at `config.py:65` but current A sizing is risk/fallback driven (`position_sizer.py:35-68`). C07 makes it valid only under typed `FIXED_QTY`.
- `equity_source` is declared at `config.py:70`; A's runtime uses a realized/frozen sizing basis (`runner.py:1504-1525`). C07 moves provenance into the explicit sizing request.
- All thirteen `wt_*` keys are declarations in A with no A runtime consumers. Pine alone serializes them (`MTC_V2.pine:2008-2028`). C28-C30 enumerate and retire them from kernel ownership.
- Six `tw_*` keys have A economic branches. `tw_margin_call_split_entries` is read/stamped but no branch consumer was found. C31-C37 own all seven decisions and C35 expressly forbids fabricating a missing branch.

## 3. B configuration sweep

Every B config class and its economic fields were assigned below. Utility/model-validator code after the configuration block is not a configuration capability.

| B class/range | Configuration family | Decision IDs | Coverage result |
|---|---|---|---|
| `SupertrendConfig`, `defaults.py:12-18` | primary signal | C01, C23 | Covered |
| `RangeFilterConfig`, `:21-33` | range signal/filter parameters | C01, C02 | Covered |
| `ConfirmationConfig`, `:36-68` | confirmation, dynamic level, refresh, session | C03, C04, C18 | Covered |
| `StopLossConfig`, `:71-84` | fixed/ATR/swing stop | C11, C19-C20 | Covered |
| `TakeProfitConfig`, `:87-95` | percent/ATR/R target | C12, C19-C20 | Covered |
| `BreakEvenConfig`, `:98-103` | BE trigger/buffer | C14 | Covered |
| `MultiTPConfig`, `:106-112` | TP1 fraction/TP2 | C13 | Covered |
| `TrailingConfig`, `:115-121` | activation and R distance | C15 | Covered; ATR-vs-R disagreement decided |
| `RiskConfig`, `:124-138` | risk sizing, leverage, equity mode, daily/trade limits | C07-C10, C18 | Covered |
| `FilterConfig`, `:141-221` | all entry filters/HTF/range modes | C02, C23-C24 | Covered |
| `GuardConfig`, `:224-253` | drawdown, loss streak, cooldown, equity/MAE, recovery | C18 | Covered; kernel/Guardian ownership decided |
| `TimeStopConfig`, `:256-268` | bars/EOD/EOW/PnL/timezone | C17, C25 | Covered |
| `ExitFilterBlockConfig`, `:271-280` | filter exits | C16 | Covered |
| `TradeConfig`, `:283-323` | direction/flip/opposite/pyramid/re-entry | C05, C06, C16, C21 | Covered |
| `StrategyConfig`, `:326-348` | capital, margin, fees, slippage, tick, pyramid, terminal close | C08-C10, C22-C23 | Covered |
| `ParityConfig`, `:351-403` | touch/close, debug, pre-roll, eval/terminal actions | C19-C20, C23 | Covered; legacy vs canonical labeling required |
| `MTCConfig`, `:406-451` | composite routing | C01-C24 | Covered through component classes |

B-specific noncanonical behaviors were not lost in grouping:

- current-bar swing and ATR `.01` fallbacks: C11;
- target `.01`/2% fallback: C12;
- nearest-extreme collision heuristic: C19;
- fixed `1e-6` quantity precision and min-stop-distance floor: C07/C09/C24;
- hard-coded approximate margin constants: C10/C34;
- entry/exit commission and tick slippage defaults: C22;
- clamped dynamic warm-up and evaluation boundary behavior: C23;
- high/low BE and R-distance trailing: C14/C15;
- global filter-exit switch/fallback: C16.

## 4. Pine input and execution sweep

The 153 Pine inputs were swept by functional group and their execution consumers were inspected. The primary economic ranges are:

| Pine range | Family | Decision IDs |
|---|---|---|
| `MTC_V2.pine:16-94` | signal, direction, sizing, exits, gates, guards, timing | C01-C24 |
| `MTC_V2.pine:95-101` | all seven constant `tw_*` declarations | C31-C37 |
| `MTC_V2.pine:102-175` | confirmation, filters, guard/time extensions, stop/target details | C02-C24 |
| `MTC_V2.pine:176-188` | all thirteen `wt_*` inputs | C28-C30 |
| `MTC_V2.pine:240-361` | tick/qty/stop/target/sizing functions | C07-C13, C24 |
| `MTC_V2.pine:943-1119` | signal gates/session/readiness | C01-C04, C18, C23 |
| `MTC_V2.pine:1143-1921` | BE/trail/exits/time/guards/confirmation/entries | C03-C06, C11-C21 |
| `MTC_V2.pine:2008-2028` | WunderTrading alert serializer | C28-C30 |

No canonical production-cost or venue-margin authority was found in Pine's `strategy()` declaration (`MTC_V2.pine:7`); C10 and C22 therefore fail closed instead of treating absent settings as authoritative zero.

## 5. Required-family checklist

| Required family from lane specification / architecture fixture list | Decision coverage |
|---|---|
| Entries and raw direction | C01, C05-C07 |
| Exits and opposite signal | C13, C16-C21 |
| Fixed/ATR/swing stops | C11 |
| ATR trailing and break-even | C14-C15 |
| Percent/ATR/R TP and MultiTP | C12-C13 |
| Sizing and contract multiplier | C07-C09 |
| Quantity/tick/min-notional boundaries | C09, C24 |
| Time stops | C17 |
| Session/day limits and cooldowns | C06, C18 |
| Signal gating/confirmation/refresh/retest | C02-C04 |
| Same-bar flip/re-entry | C05, C21, C32-C33 |
| Gap and same-bar fill assumptions | C19-C20 |
| Fees, slippage, funding | C22 |
| Margin/leverage/liquidation | C10, C34-C35 |
| Warm-up/evaluation/terminal behavior | C23 |
| Restart/missed bar | C25-C27 |
| Timestamp discipline | C25 |
| Duplicate/reordered bars | C26 |
| Cancel/revision/idempotence | C26 |
| Short symmetry and invalid/boundary values | C24 |
| All 13 `wt_*` | C28-C30 |
| All 7 `tw_*` | C31-C37 |

All requested families are covered. No family is deferred by the WP-P0-09 timebox.

## 6. WP-P0-06 unresolved corpus evidence mapped to decisions

| Existing evidence | Inventory citation | Canonical decision / required fixture |
|---|---|---|
| A case 110 EOD strict mismatch | `PARITY_CORPUS_INVENTORY.md:31-46` | C17 / GF-17 |
| A case 111 EOW strict mismatch | same | C17 / GF-17 |
| A case 134 refresh: TV/PineTS 0 vs A 131 | same | C03 / GF-03 |
| A case 147 HTF exit 124 vs 126 | same | C02/C16 / GF-02, GF-16 |
| A case 153 confirmation refresh 0 vs 146 | same | C03 / GF-03 |
| A case 154 retest 27 vs 44 | same | C04 / GF-04 |
| A case 155 MACD HTF 55 vs 76 | same | C02 / GF-02 |
| A case 162 MA HTF/trend 96 vs 94 | same | C02 / GF-02 |
| A 23 soft-pass quantity mismatches | `PARITY_CORPUS_INVENTORY.md:20-46` | C07-C09 / GF-07..09 |
| B dynamic confirmation cases 402/416 | `PARITY_CORPUS_INVENTORY.md:48-68` | C03/C04 / GF-03, GF-04 |
| B same-bar flip rerun pending | same | C05/C21 / GF-05, GF-21 |

The old corpus remains evidence of disagreement, not an oracle for the newly decided semantics.

## 7. Negative/absence sweep

| Search/result | Meaning | Decision |
|---|---|---|
| No `wt_*` match in B runner/modules | B has no WT payload capability | C28-C30 |
| No `tw_*` match in B runner/modules | B has no TW compatibility switches | C31-C37 |
| Pine `tw_*` only at constant declarations `:95-101` | Pine has no corresponding branches | C31-C37 |
| A `wt_*` only in config declaration/validation evidence | A has dead accepted config, not runtime behavior | C28-C30 |
| `tw_margin_call_split_entries` has no economic branch | Do not invent branch | C35 |
| No authoritative funding schedule in A/B/Pine | Absence cannot mean zero production cost | C22 |
| No shared durable intent/revision ledger in A/B/Pine | Replay safety needs contract-defined identity | C26-C27 |

## 8. Coverage conclusion

The decision table covers all 192 A configuration keys by range, every B typed configuration class/field family, all 153 Pine input declarations by group, every mandatory economic family, all 13 `wt_*` keys, and all 7 `tw_*` keys. The sweep found no uncovered risky capability family. This conclusion is about **decision coverage only**; it is not runtime acceptance, parity, or trading approval.
