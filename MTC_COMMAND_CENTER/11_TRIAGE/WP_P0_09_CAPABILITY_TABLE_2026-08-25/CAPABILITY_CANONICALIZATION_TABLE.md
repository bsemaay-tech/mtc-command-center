# WP-P0-09 Capability Canonicalization Table

**Date:** 2026-08-25

**Lane:** Q

**Audit tier:** T0 analysis

**Base SHA:** `fead492b0b87f207aa6e7a259372b9767d4301f9`

**Status:** DECIDED — specification only; no runtime or Pine code changed

## 1. Authority and interpretation

This table is the semantic authority requested by WP-P0-09. It compares:

- **A:** `01_MTC_PROJECT/00_PYTHON/mtc_v2/`, the kernel seed.
- **B:** `02_MTC_BACKTEST/src/engine/mtc_runner.py` and its modules.
- **Pine:** `01_MTC_PROJECT/01_PINE/MTC_V2.pine`, the TradingView reference.

Paths in citations are relative to `MTC_COMMAND_CENTER/`. In the detail sections, the shorthand `core/...` means `01_MTC_PROJECT/00_PYTHON/mtc_v2/core/...`, `defaults.py` means `02_MTC_BACKTEST/src/config/defaults.py`, and an unprefixed `PARITY_CORPUS_INVENTORY.md` means `11_TRIAGE/WP_P0_06_PARITY_CORPUS_2026-08-24/PARITY_CORPUS_INVENTORY.md`. A line citation identifies the inspected base-SHA implementation; it is not a claim of repo-wide parity. The WP-P0-06 corpus explicitly found that A and B were tested against different subjects/oracles and therefore does not support a repo-wide parity percentage (`11_TRIAGE/WP_P0_06_PARITY_CORPUS_2026-08-24/PARITY_CORPUS_INVENTORY.md:8-14,110-120`).

“Chosen implementation” means the semantic source to preserve or build toward:

- **A:** retain A semantics.
- **A-corrected:** use A's structure but correct the stated defect.
- **NEW:** neither current implementation is sufficiently explicit/correct; WP-P0-10 must pin the decided rule before migration.
- **RETIRE:** not a canonical kernel capability; preserve only long enough to reproduce a legacy branch before its authorized removal package.

This is not a move plan. WP-P0-09 expressly requires decisions before code movement (`11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:370-380`).

## 2. Decision index

| ID | Economically meaningful capability | Canonical result | Chosen implementation | WP-P0-10 fixture |
|---|---|---|---|---|
| C01 | Raw signal production, conflict, direction | Close-bar tri-state signal; conflict emits no intent | A | GF-01 |
| C02 | Entry gates, readiness, signal filters | Deterministic gate order; required-but-unready fails closed | A-corrected | GF-02 |
| C03 | Confirmation and refresh | First event counts as bar 1; refresh resets to 1 | NEW | GF-03 |
| C04 | Level retest confirmation | Frozen anchor, bounded age, explicit invalidation | NEW | GF-04 |
| C05 | Direction, regime lock, opposite signal, flip | Exit first; same-close reversal only when explicitly enabled | A-corrected | GF-05 |
| C06 | Pyramiding, adds, entry spacing, exit cooldown | Separate add spacing from post-exit cooldown | NEW | GF-06 |
| C07 | Sizing methods and equity provenance | Contract-defined request; no implicit fallback method | A-corrected + contract | GF-07 |
| C08 | Contract multiplier | Multiplier belongs in risk, notional, PnL, and margin math | A-corrected | GF-08 |
| C09 | Tick/quantity rounding and minimums | Adverse stop rounding; half-up targets; quantity floor; reject below minima | A | GF-09 |
| C10 | Leverage and margin/liquidation | Cap by leverage; simulate liquidation only from frozen venue rules | NEW | GF-10 |
| C11 | Fixed/ATR/swing stops | Previous completed bars; standing touch order; adverse gap fills at open | A-corrected | GF-11 |
| C12 | Percent/ATR/R targets | Standing target; favorable gap fills at open; R requires stop | A | GF-12 |
| C13 | MultiTP | TP1 partial then TP2 remainder; no double-counting | A | GF-13 |
| C14 | Break-even | Close-triggered, next-bar-effective, monotonic stop revision | A-corrected | GF-14 |
| C15 | Trailing stop | ATR distance, close-triggered, next-bar-effective, trail owns stop | A-corrected | GF-15 |
| C16 | Opposite/filter exits | Protective exits first; then opposite; then ordered filter/time exits | A | GF-16 |
| C17 | Bar/time/PnL exits | Open-trade unrealized PnL; calendar-defined end boundaries | A-corrected | GF-17 |
| C18 | Session/day limits, guards, recovery | Behavioral limits in kernel; account vetoes in Guardian | NEW ownership split | GF-18 |
| C19 | Same-bar stop/target collision | Explicit policy; canonical default `STOP_FIRST` | A | GF-19 |
| C20 | Fill assumptions and gaps | Native protective/target touch semantics with explicit gap rules | A | GF-20 |
| C21 | Same-bar re-entry after any exit | Reversal only for a valid opposite decision; no re-entry after risk exit | A-corrected | GF-21 |
| C22 | Fees, slippage, funding | Frozen venue fee/slippage/funding inputs; never silently zero | NEW | GF-22 |
| C23 | Warm-up, evaluation boundary, terminal handling | Deterministic dependency warm-up; no implicit flatten | NEW | GF-23 |
| C24 | Invalid values, boundary equality, short symmetry | Fail closed; open thresholds; mirror long/short | A-corrected | GF-24 |
| C25 | Timestamp discipline | Venue timestamps authoritative, UTC internal, no host-local economics | Already decided ticket #45 | GF-25 |
| C26 | Duplicate/reordered bars, revisions, idempotence | Stable bar/intent identities; exact duplicates no-op; drift blocks | NEW + contracts | GF-26 |
| C27 | Restart and missed-decision recovery | Replay state; act only through interval+45 s freshness bound | Already decided ticket #45 | GF-27 |
| C28 | WunderTrading route-code inputs (5 `wt_*`) | Bridge-owned routing; retire from kernel/Pine | RETIRE | GF-28 |
| C29 | WunderTrading order payload inputs (4 `wt_*`) | Replace with typed intent/sizing contracts | RETIRE | GF-29 |
| C30 | WunderTrading protective flags (4 `wt_*`) | Bridge venue policy, not kernel economic state | RETIRE | GF-30 |
| C31 | `tw_audit_semantics_mode` | Reproduce legacy branches, then retire master semantic switch | RETIRE | GF-31 |
| C32 | `tw_reversal_reentry_mode` | Replace with the explicit C05/C21 policy | RETIRE | GF-32 |
| C33 | `tw_reversal_reentry_delay_bars` | Replace with explicit post-decision timing; retire key | RETIRE | GF-33 |
| C34 | `tw_margin_call_mode` | Replace guessed TradingView approximation with venue model | RETIRE | GF-34 |
| C35 | `tw_margin_call_split_entries` | No consumer: retire as stamped-only configuration | RETIRE | GF-35 |
| C36 | `tw_be_semantics_mode` | Replace modes with C14's one explicit rule | RETIRE | GF-36 |
| C37 | `tw_trailing_semantics_mode` | Replace modes with C15's one explicit rule | RETIRE | GF-37 |

## 3. Detailed decisions and golden-fixture specifications

### C01 — Raw signal production, conflict, and direction

- **A behavior:** computes raw long/short conditions and suppresses simultaneous long+short signals before gates (`01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:352-449,495-512`).
- **B behavior:** runs a separately configured signal pipeline inside its ordered bar loop (`02_MTC_BACKTEST/src/engine/mtc_runner.py:35-48,927-1185`).
- **Pine reference:** builds the close-bar signal/gate lifecycle and resolves signal conflict before entries (`01_MTC_PROJECT/01_PINE/MTC_V2.pine:943-1119,1741-1820`).
- **Disagreement:** implementations do not share a proven signal oracle; WP-P0-06 records A HTF/confirmation discrepancies and B dynamic-confirmation mismatches.
- **Canonical semantics and reason:** a completed bar produces exactly one of `LONG`, `SHORT`, or `NONE`. Simultaneous true conditions produce `NONE` plus a conflict reason. Direction permission is applied after conflict resolution. This preserves deterministic A/Pine behavior without inventing signal precedence.
- **Chosen implementation:** **A**, subject to the later confirmation corrections in C03/C04.
- **GF-01:** input bars cause `(long,short)` of `(1,0)`, `(0,1)`, `(1,1)`, `(0,0)` under `Both`, `Long`, and `Short`; expected decisions are respectively `LONG/SHORT/NONE/NONE`, with forbidden directions `NONE` and conflict reason `SIGNAL_CONFLICT`. No order quantity is evaluated for `NONE`.

### C02 — Entry gates, readiness, and signal filters

- **A behavior:** evaluates indicators, readiness, filter gates, and a fixed guard order before entry (`core/runner.py:352-492,708-820`).
- **B behavior:** has a distinct default/filter tree and a dynamic warm-up calculation (`02_MTC_BACKTEST/src/config/defaults.py:12-68,141-221`; `src/engine/mtc_runner.py:515-579`).
- **Pine reference:** evaluates trend/momentum/volatility/session/readiness gates in the chart strategy (`01_MTC_PROJECT/01_PINE/MTC_V2.pine:943-1119`).
- **Disagreement:** gate formulas/defaults and readiness differ; A/Pine can treat an unavailable optional expression as neutral while global readiness is separate, whereas B derives a clamped warm-up.
- **Canonical semantics and reason:** enabled gates are evaluated in a frozen order and fail closed when their required input is non-finite or not warmed. Disabled gates are neutral. The decision artifact records every gate result and the first blocking reason. This prevents an unready indicator from becoming an accidental pass.
- **Chosen implementation:** **A-corrected** at the unready boundary; gate equations remain those of the declared strategy profile.
- **GF-02:** one otherwise-valid long signal is evaluated with each gate disabled, enabled/true, enabled/false, and enabled/NaN. Expected: `PASS`, `PASS`, `BLOCK(reason=<gate>)`, `BLOCK(reason=<gate>_UNREADY)`. Reordering configuration keys must not change the result or reason.

### C03 — Confirmation and refresh

- **A behavior:** maintains pending confirmations and optional same-direction refresh (`core/runner.py:824-892`).
- **B behavior:** has its own confirmation defaults/state flow (`02_MTC_BACKTEST/src/config/defaults.py:47-68`); WP-P0-06 found two unresolved dynamic-confirmation cases 402/416 (`PARITY_CORPUS_INVENTORY.md:48-68`).
- **Pine reference:** confirmation/refresh logic is in `MTC_V2.pine:1684-1739`; the A corpus found refresh/confirmation mismatches in cases 134, 153, 154, and 155 (`PARITY_CORPUS_INVENTORY.md:31-46`).
- **Disagreement:** refresh age/count behavior can erase pulse signals or emit at different bars.
- **Canonical semantics and reason:** the initiating raw event is confirmation bar **1**. Each subsequent qualifying close increments the count. A same-direction refresh replaces the anchor and resets count to **1**, never 0. Opposite raw signal cancels the pending candidate. Emission occurs once when count reaches `confirm_bars`; entry gates are re-evaluated on the emission bar. This gives pulses an observable, bounded lifecycle.
- **Chosen implementation:** **NEW** explicit state machine, not an A/B blend.
- **GF-03:** `confirm_bars=3`, raw long on bars 10 and 11, qualifying holds through 13. Expected pending counts `1,1,2`, emit long on bar 13 only. With refresh off: `1,2,emit` on bar 12. An opposite raw signal on bar 12 cancels long and begins short at count 1.

### C04 — Level retest confirmation

- **A behavior:** has a separate retest state/timeout flow (`core/runner.py:894-927`).
- **B behavior:** folds confirmation into its independent runner/config implementation (`02_MTC_BACKTEST/src/config/defaults.py:47-68`; `src/engine/mtc_runner.py:927-1185`).
- **Pine reference:** retest confirmation participates in the confirmation block (`MTC_V2.pine:1684-1820`).
- **Disagreement:** corpus case 154 emitted 27 versus 44 trades, proving anchor/timeout semantics are not aligned (`PARITY_CORPUS_INVENTORY.md:40-44`).
- **Canonical semantics and reason:** freeze the initiating signal's level and direction. Age is 0 on the anchor bar. A retest is valid only on bars `1..timeout_bars`, must touch/cross the frozen level in the configured direction, and must close back on the confirming side. A new same-direction anchor replaces it only when refresh is enabled; opposite signal invalidates it.
- **Chosen implementation:** **NEW** explicit state machine.
- **GF-04:** long anchor level 100 at bar 20, timeout 3. Bar 21 low 100/high 102/close 101 emits; bar 24 identical does not. A bar that touches 100 but closes 99 does not emit. Refresh at bar 22 changes frozen level to 103 and resets age 0.

### C05 — Direction, regime lock, opposite signal, and flip

- **A behavior:** position admission enforces direction/max entries/regime (`core/position_manager.py:79-142`); runner exits on opposite signal and may flip or defer (`core/runner.py:516-539,592-607,928-940`).
- **B behavior:** exposes direction, flip, pyramid, and same-bar knobs but refuses several non-unit configurations (`02_MTC_BACKTEST/src/config/defaults.py:283-323`; `src/engine/mtc_runner.py:136-154`).
- **Pine reference:** opposite-signal handling is `MTC_V2.pine:1468-1499`, with flip/entry handling at `1741-1921`.
- **Disagreement:** A/Pine can carry a deferred reversal when same-bar flipping is disabled; B has separate re-entry controls and unresolved same-bar flip evidence.
- **Canonical semantics and reason:** an opposite valid decision closes the old position first. If `allow_same_close_reversal=true`, the opposite entry may fill at that same close after sizing against post-exit realized equity. If false, no stale deferred decision is carried: a later entry requires a fresh valid decision. Regime lock blocks new/add decisions but never blocks risk-reducing exits.
- **Chosen implementation:** **A-corrected** by deleting semantic dependence on a stale deferred flip.
- **GF-05:** long 1 at 100 receives valid short at close 95. With reversal on: outputs `EXIT_LONG@95` then `ENTER_SHORT@95`, distinct intent IDs. With off: only exit; no entry next bar unless that bar independently emits short. Regime lock blocks an add but not the exit.

### C06 — Pyramiding, adds, entry spacing, and post-exit cooldown

- **A behavior:** cooldown is measured from last entry, allows configured same-side adds, calculates weighted average, tightens stop, and rewrites exit state (`core/position_manager.py:79-227`).
- **B behavior:** declares pyramiding settings but rejects values other than one in the runner (`defaults.py:283-323`; `mtc_runner.py:136-154`).
- **Pine reference:** permits many strategy entries and implements basket adds/average price (`MTC_V2.pine:7,1821-1921`).
- **Disagreement:** `cooldown_bars` ambiguously means spacing-after-entry in A but after-exit in Pine flows; B effectively disables pyramiding.
- **Canonical semantics and reason:** use two named concepts: `entry_spacing_bars` between same-side entries and `post_exit_cooldown_bars` after a full close. Adds are same-side only, obey total leverage/risk caps, update weighted average, may only tighten the shared stop, and rebuild only unfilled target legs against the new basket. Both default to zero; pyramiding defaults to one.
- **Chosen implementation:** **NEW** explicit vocabulary, retaining A's basket arithmetic.
- **GF-06:** enter 1@100 then add 2@110: expected qty 3 and average `106.6666667`. An existing long stop 95 cannot move to 94. With entry spacing 2, add on next bar blocks and add two bars later passes. After full exit, post-exit cooldown 2 blocks exactly the next two decision bars.

### C07 — Sizing methods and equity provenance

- **A behavior:** computes risk-at-stop with fallback notional, leverage cap, and minimums; `fixed_qty`/`equity_source` are declared but not the controlling arithmetic (`core/config.py:65-71`; `core/position_sizer.py:35-68`; `core/runner.py:1504-1525`).
- **B behavior:** supports initial/realized balance selection, a minimum stop-distance floor, and a different implicit fallback (`src/engine/mtc_runner.py:2632-2686`; `src/modules/risk/position_sizer.py:53-114`).
- **Pine reference:** risk sizing and fallback are `MTC_V2.pine:339-361`.
- **Disagreement:** fallback behavior, equity source, stop floor, and declared fixed quantity differ. The contract already requires exactly one normalized method and source-defined provenance (`contracts/README.md:10-17`; `contracts/mtc_contracts/sizing.py:17-21,39-97`).
- **Canonical semantics and reason:** emit one `SizingRequest` method: `RISK_AT_STOP`, `FIXED_QTY`, `FIXED_NOTIONAL`, or `PCT_EQUITY_NOTIONAL`. There is no silent method fallback. Risk-at-stop uses an explicit authoritative equity snapshot/provenance and rejects a missing/nonpositive stop distance. `fixed_qty` is meaningful only under `FIXED_QTY`.
- **Chosen implementation:** **A-corrected + the WP-P0-04 sizing contract**; allocation remains outside the kernel.
- **GF-07:** equity 10,000, risk 1%, entry 100, stop 95, multiplier 1 => requested qty 20. Missing stop => `NON_EXPRESSIBLE/MISSING_STOP`, not fallback. `FIXED_QTY=3` => 3 independent of equity. `FIXED_NOTIONAL=1,000` at 100 => raw 10. Each output includes snapshot ID and source.

### C08 — Contract multiplier

- **A behavior:** includes multiplier in notional cap and PnL, but omits it from the risk-at-stop denominator (`core/position_sizer.py:35-68`; `core/position_manager.py:254-355`; `core/instrument.py:8-27`).
- **B behavior:** its position sizer also divides risk by raw price distance without multiplier (`src/modules/risk/position_sizer.py:53-77`).
- **Pine reference:** risk sizing uses `syminfo.pointvalue`, while cap sizing also uses `contract_multiplier` (`MTC_V2.pine:339-361`).
- **Disagreement:** A/B oversize non-unit-multiplier instruments relative to Pine.
- **Canonical semantics and reason:** `risk_per_unit = abs(entry-stop) * contract_multiplier`; notional, PnL, fees where applicable, margin, and leverage use the same frozen instrument multiplier. This dimensional identity is mandatory.
- **Chosen implementation:** **A-corrected** to Pine's dimensionally valid risk equation.
- **GF-08:** equity 10,000, risk 1%, entry 100, stop 95, multiplier 10 => qty 2 and risk 100. A deliberate multiplier omission must produce qty 20 and fail RED.

### C09 — Tick/quantity rounding and minimums

- **A behavior:** centralizes tick and quantity rounding, applies adverse stop rounding, half-up target rounding, quantity floor, and min-quantity/notional checks (`core/rounding.py:6-33`; `core/exits.py:175-275`; `core/position_sizer.py:35-68`).
- **B behavior:** infers precision and floors quantity inside the runner (`src/engine/mtc_runner.py:2664-2686`).
- **Pine reference:** uses mintick/mincontract helpers but cannot reliably enforce venue min-notional metadata (`MTC_V2.pine:240-253,339-361`).
- **Disagreement:** fixed `1e-6` precision and missing min-notional handling produce different quantities.
- **Canonical semantics and reason:** use frozen instrument metadata. Stops round away from the protected position (long down, short up); targets round half-up to nearest tick; quantities floor to step so risk is never increased. Reject, rather than round up, when the floored quantity is below min quantity or min notional.
- **Chosen implementation:** **A**.
- **GF-09:** tick .25: long stop 99.87 => 99.75, short stop 100.13 => 100.25, target 101.125 => 101.25. Raw qty 1.239 with step .01 => 1.23. At price 10, qty .9 with min qty 1 or min notional 20 => rejection reason(s), never qty promotion.

### C10 — Leverage and margin/liquidation

- **A behavior:** caps entry notional by configured leverage and optionally runs a TradingView-like margin approximation selected by `tw_margin_call_mode` (`core/position_sizer.py:35-68`; `core/runner.py:1411-1502`).
- **B behavior:** applies entry commission and its own approximate margin liquidation with hard-coded factors (`src/engine/mtc_runner.py:631-772,2393-2430`).
- **Pine reference:** declares no explicit `margin_long`/`margin_short` parameters in the strategy declaration (`MTC_V2.pine:7`).
- **Disagreement:** A and B approximations are not the same venue model and Pine does not establish either as authoritative.
- **Canonical semantics and reason:** leverage cap is an allocation constraint. Forced liquidation is simulated only when a frozen venue/instrument margin schedule defines initial margin, maintenance margin, mark price, liquidation fee, and partial/full liquidation rules. Missing rules produce `MARGIN_MODEL_UNAVAILABLE`; they never trigger a fabricated margin call.
- **Chosen implementation:** **NEW** venue model; retain A/B only as named legacy fixtures.
- **GF-10:** cap fixture: equity 1,000, leverage 2, multiplier 1, price 100 => max qty 20. Venue fixture supplies maintenance 10%, mark series, fee, and partial-liquidation rule and asserts the exact first liquidation bar/qty/equity. Same bars without venue rules emit `MARGIN_MODEL_UNAVAILABLE` and no liquidation.

### C11 — Fixed, ATR, and swing stops

- **A behavior:** computes percent/ATR/swing stops from prior history and adverse tick rounding; touch mode includes gap-open fills (`core/exits.py:175-210,353-447`).
- **B behavior:** ATR NaN may fall back to `0.01`, and swing includes the current bar (`src/modules/risk/sl_calculator.py:68-76,87-102,125-162`).
- **Pine reference:** stop calculations use completed prior bars (`MTC_V2.pine:283-309`).
- **Disagreement:** current-bar swing leakage and fabricated ATR fallback change stop distance and size.
- **Canonical semantics and reason:** percent and ATR stops use finite bar-close inputs; swing lookback excludes the decision bar. Missing ATR/history blocks the entry. A protective stop is a standing order active from the next tradable instant after entry; touch fills at stop, except a gap beyond it fills at the adverse open.
- **Chosen implementation:** **A-corrected** only to make next-instant activation and failure reasons explicit.
- **GF-11:** long decision close 100, prior lows `[98,97,99]`, current low 90, swing buffer 0 => stop 97, not 90. ATR missing => entry blocked. Existing stop 95 with next open 90 => fill 90; open 97 then low 94 => fill 95.

### C12 — Percent, ATR, and R targets

- **A behavior:** implements percent/ATR/R targets, half-up tick rounding, and favorable gap-open fills (`core/exits.py:213-275,450-491`).
- **B behavior:** can fabricate ATR `.01` or a 2% target when an R target lacks a stop (`src/modules/risk/tp_calculator.py:73-80,155-173`).
- **Pine reference:** target calculation is `MTC_V2.pine:311-319`.
- **Disagreement:** B silently changes target method when inputs are missing.
- **Canonical semantics and reason:** the configured target method is not substituted. Missing ATR or stop blocks target creation. Targets are standing orders; favorable gaps fill at the open, otherwise at target touch.
- **Chosen implementation:** **A**.
- **GF-12:** long entry 100, stop 95, R=2 => target 110. Missing stop => `TARGET_UNAVAILABLE/MISSING_STOP`. Target 110 with next open 112 => fill 112; open 108/high 111 => fill 110. Mirror for short.

### C13 — MultiTP

- **A behavior:** creates TP1 fraction and TP2 for the remaining position, processes TP1 before TP2, and avoids a phantom remainder (`core/exits.py:213-275,450-550`; `core/position_manager.py:254-355`).
- **B behavior:** can record two closed-trade fragments and uses a deferred-stop path after partial TP (`src/engine/mtc_runner.py:2259-2385`).
- **Pine reference:** TP1/TP2 close-only lifecycle is `MTC_V2.pine:1204-1348`.
- **Disagreement:** trade-record granularity and same-bar partial/stop handling differ.
- **Canonical semantics and reason:** one position lifecycle may have execution fragments. TP1 closes `initial_or_rebased_open_qty * tp1_fraction`, capped by current qty; TP2 closes all remainder. Fees/PnL accrue per fill, but metrics retain one lifecycle ID. Stop remains active for the remainder. Same-bar ambiguity follows C19.
- **Chosen implementation:** **A** lifecycle model.
- **GF-13:** qty 10, TP1 fraction .4, TP1 105, TP2 110. Touch only TP1 => fill 4 and remain 6. Next target touch => fill 6 and lifecycle closes. Gap above both under ordered-open model fills TP1 4 at open then TP2 6 at the same open, with one lifecycle/two fills.

### C14 — Break-even

- **A behavior:** updates trailing first and applies BE only when trailing does not own the stop; modes can alter trigger semantics (`core/exits.py:278-350`; `core/runner.py:1241-1409`).
- **B behavior:** uses high/low-based BE triggering (`src/modules/risk/tp_calculator.py:193-250`; `src/engine/mtc_runner.py:2450-2480`).
- **Pine reference:** uses close-triggered BE and monotonic stop updates (`MTC_V2.pine:1143-1172`).
- **Disagreement:** intrabar-high versus close trigger and same-bar effectiveness can create lookahead-like exits.
- **Canonical semantics and reason:** BE trigger is evaluated at completed close using entry-to-initial-stop R. A revision becomes active on the next bar, never retroactively on the trigger bar. It may only tighten the stop. If trailing is enabled and active, trailing owns stop revision.
- **Chosen implementation:** **A-corrected** to one mode and next-bar effectiveness.
- **GF-14:** long entry 100, initial stop 95, trigger 1R. Bar high 106/close 104 does not arm; later close 105 arms stop 100 for next bar. If that trigger bar low was 99, no BE exit. Next bar low 99 exits 100.

### C15 — Trailing stop

- **A behavior:** local trailing uses ATR distance, is monotonic, and has priority over BE (`core/exits.py:278-350`).
- **B behavior:** trails by R-distance and updates after price-exit evaluation (`src/modules/risk/tp_calculator.py:253-320`; `src/engine/mtc_runner.py:2450-2561`).
- **Pine reference:** uses ATR-distance, close-triggered trailing (`MTC_V2.pine:1143-1172`).
- **Disagreement:** ATR versus R distance and activation/effectiveness timing differ.
- **Canonical semantics and reason:** once close reaches the configured activation R, compute an ATR-distance candidate from that close, adverse-round it, and activate it next bar. Stop revisions are monotonic. Trail owns the stop while active; BE cannot loosen or replace it.
- **Chosen implementation:** **A-corrected** for next-bar effectiveness.
- **GF-15:** long entry 100/stop 95, activation 1R, ATR 2, distance 1.5 ATR. Close 106 creates candidate 103 active next bar. Trigger-bar low 102 does not exit at 103. Later lower close cannot reduce 103; short case mirrors upward rounding.

### C16 — Opposite-signal and filter exits

- **A behavior:** protective exits precede opposite and nine ordered filter exits (`core/runner.py:550-665`).
- **B behavior:** has a global filter-exit master/fallback and separate exit flow (`src/config/defaults.py:271-280`; `src/engine/mtc_runner.py:400-437,2432-2448`).
- **Pine reference:** opposite and filter exits are `MTC_V2.pine:1468-1542`.
- **Disagreement:** B's master switch/fallback can enable behavior absent from A/Pine; reason priority differs.
- **Canonical semantics and reason:** protective fills win first. If none, a valid opposite signal exits next, followed by individually enabled filter exits in a frozen documented order. There is no hidden master fallback. One bar emits at most one full-exit reason.
- **Chosen implementation:** **A**.
- **GF-16:** a long bar simultaneously touches stop, has opposite signal, and has two filter exits: expected stop only. Without stop: opposite only. Without opposite: first configured filter in canonical order only. Disabled filter never fires even if a master-like legacy field is true.

### C17 — Bar/time/PnL exits

- **A behavior:** bar count is explicit, but profit/loss time exits read `last_realized_pnl`; EOD/EOW are hard-coded transition/hour rules (`core/runner.py:667-704`).
- **B behavior:** uses current unrealized PnL and configurable timezone series (`src/config/defaults.py:256-268`; `src/engine/mtc_runner.py:439-504`).
- **Pine reference:** uses current open-trade PnL and day/week boundaries (`MTC_V2.pine:1544-1605`).
- **Disagreement:** A's realized-PnL input is the wrong position; local timezone/hard-coded Friday hours are not portable.
- **Canonical semantics and reason:** `Bars` counts completed bars since fill; `Profit/Loss` examines current unrealized PnL at the decision close. EOD/EOW exits occur at the last scheduled bar close of the frozen venue/session calendar. For 24/7 profiles, day/week are UTC. Missing calendar blocks those modes.
- **Chosen implementation:** **A-corrected** using Pine/B's open-position PnL concept and C25 time discipline.
- **GF-17:** fill at bar 5 with `Bars=3` exits at bar 8 close. Prior realized +100/current unrealized -10 with Loss threshold -5 exits; it must not pass from prior realized PnL. A Friday session-calendar last bar exits; a hard-coded 21:00 bar outside that calendar must not decide the result.

### C18 — Session/day limits, guards, and recovery

- **A behavior:** computes session/day guard state, trade counts, consecutive outcomes, recovery signals, and admission order (`core/runner.py:708-820,941-953`).
- **B behavior:** resets day/consecutive state and evaluates its own guards (`src/engine/mtc_runner.py:254-398`).
- **Pine reference:** session gating and guards are `MTC_V2.pine:1056-1087,1607-1681`.
- **Disagreement:** ownership and timezone reset semantics differ; account-wide facts cannot be authoritative inside one strategy worker. WP-P0-04 defines Guardian veto vocabulary (`contracts/mtc_contracts/risk.py:17-24,35-109`).
- **Canonical semantics and reason:** kernel owns strategy-local max trades/day, entry spacing/post-exit cooldown, session eligibility, equity-curve/MAE signal guards, and declared recovery mode. Portfolio/account daily loss, drawdown, consecutive-loss, exposure, and kill vetoes belong to PortfolioSimulator/Guardian. Session calendars use authoritative timestamps and frozen named calendars, never host locale.
- **Chosen implementation:** **NEW ownership split**, with A gate order as the local baseline.
- **GF-18:** third entry after `max_trades_per_day=2` is blocked while exits remain allowed; next canonical session day resets count. Injected Guardian veto blocks entry with its reason but cannot suppress a stop exit. Same timestamp evaluated on hosts in two timezones yields identical session/day result.

### C19 — Same-bar stop/target collision

- **A behavior:** touch mode exposes an explicit collision policy and defaults to pessimistic stop-first (`core/exits.py:353-379`).
- **B behavior:** uses a nearest-extreme/path heuristic (`src/engine/mtc_runner.py:2159-2258`).
- **Pine reference:** current close-only code resolves explicit collision stop-first (`MTC_V2.pine:1305-1320`).
- **Disagreement:** OHLC cannot prove intrabar order; B's inferred path can select a target where A selects the stop.
- **Canonical semantics and reason:** every run records one of `STOP_FIRST`, `TARGET_FIRST`, or `SUBBAR_UNKNOWN`. Acceptance default is `STOP_FIRST`. `SUBBAR_UNKNOWN` yields an unresolved/interval result unless sub-bar evidence is supplied; it must not guess a path.
- **Chosen implementation:** **A**.
- **GF-19:** long stop 95/target 105 on O=100,H=106,L=94,C=101. Expected STOP_FIRST => fill 95; TARGET_FIRST => fill 105; SUBBAR_UNKNOWN => no scalar PnL and reason `AMBIGUOUS_INTRABAR_ORDER`. Mutation to nearest-extreme must fail the default fixture.

### C20 — Fill assumptions and gaps

- **A behavior:** touch mode handles adverse stop gaps and favorable target gaps; close-only mode fills at close (`core/exits.py:353-491`).
- **B behavior:** applies separate touch/close and TradingView heuristic plus tick slippage (`src/engine/mtc_runner.py:581-629,2159-2208`).
- **Pine reference:** strategy is configured `process_orders_on_close=true` and implements close-only fills (`MTC_V2.pine:7,1120,1174-1348`).
- **Disagreement:** Pine-compatible close-only fills are not faithful to native standing protective orders.
- **Canonical semantics and reason:** canonical execution uses standing touch semantics: stop gap fills at worse open, target gap at better open, otherwise at order price. Market decisions fill at the declared decision close unless execution venue policy says next open. Close-only behavior remains a named legacy profile, never an implicit default.
- **Chosen implementation:** **A** touch mode; A close-only is a legacy fixture.
- **GF-20:** four rows pin stop normal touch, stop adverse gap, target normal touch, and target favorable gap for both long and short. A fifth profile fixture proves `LEGACY_CLOSE_ONLY` fills the same crossed stop at close and is labeled non-canonical.

### C21 — Same-bar re-entry after exits

- **A behavior:** protective/filter/time exits set a block flag; opposite exits can allow a flip (`core/runner.py:550-704,928-1041`).
- **B behavior:** exposes same-bar re-entry controls and protective re-entry modes (`src/config/defaults.py:283-323`; `src/engine/mtc_runner.py:136-154`).
- **Pine reference:** exit ordering precedes entry logic (`MTC_V2.pine:1174-1820`).
- **Disagreement:** the same OHLC can exit and re-enter under configurable B/TW modes, and the corpus notes a pending same-bar flip rerun.
- **Canonical semantics and reason:** stop, target, margin, filter, time, or Guardian exit blocks all new entries for that bar. Only an opposite-signal full exit may reverse at the same close, and only under C05 with a valid post-gate opposite decision. This prevents a risk exit from becoming an accidental re-risk event.
- **Chosen implementation:** **A-corrected** to remove legacy protective re-entry modes.
- **GF-21:** a stop plus fresh same-direction signal produces exit only. A TP plus opposite signal also produces exit only. An opposite-signal exit with reversal enabled produces the ordered exit/entry pair; with reversal disabled, exit only.

### C22 — Fees, slippage, and funding

- **A behavior:** position PnL includes multiplier but no fee/slippage/funding ledger (`core/position_manager.py:254-355`).
- **B behavior:** defaults commission to 0.04% and slippage to five ticks, applies slippage at fills, and deducts entry/exit commission (`src/config/defaults.py:326-348`; `src/engine/mtc_runner.py:621-629,631-772`; `src/engine/mtc_state.py:349-437`).
- **Pine reference:** strategy declaration does not set commission, slippage, or funding (`MTC_V2.pine:7`).
- **Disagreement:** A/Pine effectively omit costs while B invents defaults; none models scheduled funding authoritatively.
- **Canonical semantics and reason:** each run must bind a frozen fee schedule (maker/taker and currency), slippage model, and funding schedule or explicitly declare `ZERO_COST_RESEARCH`. Fees are per execution fragment, slippage changes fill price, and funding accrues at venue timestamps while the position is held. Production evidence may not silently use zero.
- **Chosen implementation:** **NEW** explicit cost contract; B is only an arithmetic reference.
- **GF-22:** buy 2 at nominal 100 with +1 tick (.5) slippage, sell at nominal 110 with -1 tick, taker fee .1% each side: expected fills 100.5/109.5 and exact fee/PnL ledger. Holding across one supplied funding timestamp adds exactly one signed funding item; no schedule yields `COST_MODEL_UNAVAILABLE` unless research-zero is explicitly selected.

### C23 — Warm-up, evaluation boundary, and terminal handling

- **A behavior:** derives warm-up from configured dependencies and processes chronological bars (`core/runner.py:304-350`).
- **B behavior:** uses a dynamic `5x` RMA-style estimate clamped to 200–2000 and has preroll/evaluation-boundary options (`src/engine/mtc_runner.py:515-579,927-1185`).
- **Pine reference:** relies on series readiness plus its own warm-up/readiness inputs (`MTC_V2.pine:943-1119`).
- **Disagreement:** clamp-based warm-up changes the first actionable bar; implicit boundary flattening changes economic results.
- **Canonical semantics and reason:** warm-up is the exact maximum dependency requirement of the frozen indicator graph plus explicitly supplied pre-roll. The first actionable bar must have every enabled dependency ready. Evaluation start/end and terminal flattening are scenario fields; no position is silently flattened or clipped.
- **Chosen implementation:** **NEW** explicit scenario contract, using A dependency accounting.
- **GF-23:** a profile needing 20 completed bars emits no decision through bar 19 and may decide at 20. Supplying 20 pre-roll bars makes evaluation bar 0 actionable. Identical open position at terminal bar remains open unless `terminal_action=FLATTEN`, in which case one labeled terminal fill occurs.

### C24 — Invalid values, equality boundaries, and short symmetry

- **A behavior:** rejects invalid bars and centralizes rounding, but multiple comparisons live across runner/modules (`core/runner.py:1565-1575`; `core/rounding.py:6-33`).
- **B behavior:** has fixed-precision fallbacks and can manufacture small ATR/stop distances (`src/modules/risk/position_sizer.py:53-114`; `src/modules/risk/sl_calculator.py:87-102`).
- **Pine reference:** Pine arithmetic/`na` propagation differs from Python (`MTC_V2.pine:240-361`).
- **Disagreement:** NaN, zero, and equality cases can pass, fall back, or round differently.
- **Canonical semantics and reason:** non-finite/nonpositive price, equity, multiplier, tick, step, or required distance fails closed with a typed reason. Numeric policy thresholds are **open** unless a capability explicitly states otherwise. Every long fixture has a price-reflected short twin; allowed asymmetry must be declared, not accidental.
- **Chosen implementation:** **A-corrected** with WP-P0-04's fail-closed/open-boundary rule (`contracts/README.md:36-42`).
- **GF-24:** matrix for NaN/±inf/0 at each required numeric field expects typed rejection. Value exactly at an open threshold does not cross; epsilon beyond does. Reflect prices around 100 and directions; absolute risk, quantities, and reason codes must match.

### C25 — Timestamp discipline (ticket #45; incorporated, not re-decided)

- **A behavior:** bar state carries timestamp/index but does not define full venue identity discipline (`core/types.py:11-20`).
- **B behavior:** converts input timestamps to UTC but also exposes configurable timezones for time exits (`src/engine/mtc_runner.py:439-504,927-1185`).
- **Pine reference:** evaluates exchange/chart series time and named session inputs (`MTC_V2.pine:1056-1087,1544-1605`).
- **Disagreement:** local timezone/DST/configurable display time can leak into economic state.
- **Canonical semantics and reason:** per the already-decided WP-P0-09 plan row, venue candle timestamps are authoritative; internal timestamps are UTC; local timezone/DST never enters ledger, artifact, or hash state; timezone is display-only. Host NTP/drift alarm belongs to WP-P0-26. Local clock is used only to compute staleness relative to venue timestamp (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:378`; `11_TRIAGE/WAYFINDER_DECISION_FOLD_2026-08-23.md:22`).
- **Chosen implementation:** **ticket #45 decision**, unchanged.
- **GF-25:** the same venue bars processed under `UTC`, `Europe/Chisinau`, and `America/New_York` host locales produce byte-identical economic events/hashes. Display strings may differ outside the hashed object. A DST transition cannot change session membership when the frozen venue calendar is unchanged.

### C26 — Duplicate/reordered bars, cancel/revision ordering, and idempotence

- **A behavior:** expects chronological bars and has stateful orders but no complete external intent identity/revision protocol (`core/runner.py:314-350`; `core/types.py:11-20`).
- **B behavior:** converts and iterates its dataframe but does not provide the canonical cross-process idempotency contract (`src/engine/mtc_runner.py:927-1185`).
- **Pine reference:** alert dispatch is event text without a kernel-owned revision ledger (`MTC_V2.pine:2008-2028`).
- **Disagreement:** replay can duplicate orders; changed data at the same timestamp can silently rewrite history. WP-P0-04 supplies order/action/freshness vocabulary (`contracts/mtc_contracts/orders.py:18-49,52-127`; `contracts/mtc_contracts/execution.py:16-53`).
- **Canonical semantics and reason:** bar identity is `(venue,symbol,timeframe,open_timestamp_utc)`. Exact duplicate payload is a no-op. Same identity/different OHLCV is `BAR_DRIFT` and blocks. Live out-of-order bars block; recovery sorts a bounded authoritative replay before action. Intent ID is deterministic from deployment/worker/bar/action/position-lifecycle; revisions are monotonic. Duplicate intent/revision is no-op; stale revision/cancel cannot overwrite a newer state.
- **Chosen implementation:** **NEW + WP-P0-04 contracts**.
- **GF-26:** process bars 1,2,2(exact),3 => identical output to 1,2,3 and no duplicate intent. Bar 2 with changed close => `BAR_DRIFT`. Deliver revision 2 then 1 => state remains 2. Deliver cancel revision 3 twice => one cancellation. Mutation to random IDs must fail deterministic snapshot.

### C27 — Restart and missed-decision recovery (ticket #45; bound completed here)

- **A behavior:** is an in-memory chronological runner; it does not implement durable replay/action freshness (`core/runner.py:314-350`; `core/types.py:71-169`).
- **B behavior:** is a batch runner and likewise is not the restart authority (`src/engine/mtc_runner.py:927-1185`).
- **Pine reference:** chart execution does not define Bridge restart replay semantics (`MTC_V2.pine:2008-2028`).
- **Disagreement:** none of A/B/Pine safely decides when a decision discovered after downtime may still be acted on.
- **Canonical semantics and reason:** incorporate the already-decided policy: always replay missed bars to reconstruct state; act on a missed decision only within the existing freshness bound, otherwise skip/log explained divergence; first action is at the next actionable bar close (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:377`; `WAYFINDER_DECISION_FOLD_2026-08-23.md:22`). The exact bound is: `age = NTP-disciplined observation_utc - (venue_open_timestamp_utc + timeframe)`. `FRESH` is age `<15s`; `AGING` is `15s <= age <=45s`; both may act. `STALE` is `age >45s` and must not act. Thus the absolute deadline is `venue open + timeframe + 45s`, inclusive. This preserves the documented fresh/aging/no-economic-change policy (`_AI_MEMORY/MASTER_ARCHITECTURE_DECISIONS_AND_TARGET_STATE_2026-08-19.md:2297-2325`) without re-deciding the ticket.
- **Chosen implementation:** **ticket #45 decision** plus its required numeric bound.
- **GF-27:** for a 60s bar opened 12:00:00Z, decision close is 12:01:00Z. Restart observations at 12:01:14.999, :15.000, :45.000 emit once with FRESH/AGING/AGING; :45.001 reconstructs identical state but emits no order and logs `MISSED_DECISION_STALE`. Earliest later live decision may act only at its own close.

### C28 — WunderTrading route-code inputs (all five route `wt_*` keys)

- **A behavior:** declares `wt_enter_long_code`, `wt_exit_long_code`, `wt_enter_short_code`, `wt_exit_short_code`, and `wt_exit_all_code` with no consumers (`core/config.py:226-230`; architecture audit at `_AI_MEMORY/MASTER_ARCHITECTURE_DECISIONS_AND_TARGET_STATE_2026-08-19.md:559-571`).
- **B behavior:** scoped search found no `wt_*` references in the B runner/modules.
- **Pine reference:** declares the five codes (`MTC_V2.pine:176-180`) and uses them only in alert dispatch (`MTC_V2.pine:2008-2028`).
- **Disagreement:** Pine can arm an unaudited live route by typing a code, while A stores dead configuration and B has no capability.
- **Canonical semantics and reason:** these are Bridge/execution routing credentials, not strategy economics. Retire all five from kernel and Pine after reproduction; Bridge uses authenticated deployment/route identity. Empty codes must never mean implicit authorization. This matches the already-approved WP-P0-23 removal scope (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:539-544`).
- **Chosen implementation:** **RETIRE** all five; no canonical kernel replacement.
- **GF-28:** static disposition fixture enumerates the five keys exactly. Legacy Pine fixture: all empty => zero alerts; one populated action code => only the matching legacy action payload. Corrected-vNext contract fixture rejects route codes in kernel config and resolves route solely from an authenticated Bridge deployment fixture.

### C29 — WunderTrading order-payload inputs (all four payload `wt_*` keys)

- **A behavior:** declares `wt_order_type`, `wt_amount_type`, `wt_amount`, and `wt_leverage` without consumers (`core/config.py:231-234`).
- **B behavior:** scoped search found no `wt_*` references.
- **Pine reference:** declares these fields (`MTC_V2.pine:181-184`) and serializes them into alerts (`MTC_V2.pine:2008-2028`).
- **Disagreement:** Pine payload size/leverage can diverge from strategy-calculated position economics; A merely accepts the keys.
- **Canonical semantics and reason:** retire all four. Kernel emits typed `OrderIntent` plus `SizingRequest`; RiskAuthority returns approved allocation; Bridge translates to venue order type/quantity. Leverage is a risk/allocation input, not free alert text (`contracts/mtc_contracts/sizing.py:39-125`; `contracts/mtc_contracts/orders.py:27-49,52-101`).
- **Chosen implementation:** **RETIRE** all four in favor of WP-P0-04 contracts.
- **GF-29:** static fixture enumerates four keys. Legacy payload snapshot pins `market/quote/100/1`. Corrected fixture proves changing retired fields cannot change a canonical intent, while changing approved allocation quantity does; an unsupported limit semantic yields `NON_EXPRESSIBLE`, not a market fallback.

### C30 — WunderTrading protective flags (all four protective `wt_*` keys)

- **A behavior:** declares `wt_use_tp`, `wt_use_sl`, `wt_reduce_only`, and `wt_place_cond_orders` without consumers (`core/config.py:235-238`).
- **B behavior:** scoped search found no `wt_*` references.
- **Pine reference:** declares them (`MTC_V2.pine:185-188`) and places them into live alert payloads (`MTC_V2.pine:2008-2028`).
- **Disagreement:** payload flags can contradict kernel stop/target state and venue capabilities.
- **Canonical semantics and reason:** retire all four from strategy configuration. Protective intent derives from the canonical position lifecycle; reduce-only and conditional-order realization are Bridge/venue policy, validated against capabilities. No boolean can silently disable an economically required stop.
- **Chosen implementation:** **RETIRE** all four.
- **GF-30:** static fixture enumerates four keys. Legacy snapshot covers all-false/true permutations used by serializer. Corrected fixture supplies a long entry with required stop/target and proves Bridge translation is reduce-only for exits and creates supported conditional orders independent of retired booleans; unsupported protection blocks deployment.

### C31 — `tw_audit_semantics_mode`

- **A behavior:** required config selects `off` or `research`, changing quantity-rounding semantics (`core/config.py:58,282-288,470-490`; architecture audit `_AI_MEMORY/MASTER_ARCHITECTURE_DECISIONS_AND_TARGET_STATE_2026-08-19.md:581,598-610`).
- **B behavior:** no `tw_*` references.
- **Pine reference:** constant `"off"` only, with no consumer (`MTC_V2.pine:95`).
- **Disagreement:** a broad audit switch changes economics in A but is inert in Pine/absent in B.
- **Canonical semantics and reason:** reproduce both A branches, then retire the master switch. Precision is explicit instrument/profile metadata (C09), never an “audit” mode.
- **Chosen implementation:** **RETIRE** after legacy reproduction.
- **GF-31:** raw qty `1.234567`, instrument step `.01`: legacy `off` => `1.23`; legacy `research` => fixed `1e-6` floor `1.234567`. Corrected-vNext has only instrument step behavior and rejects the key.

### C32 — `tw_reversal_reentry_mode`

- **A behavior:** required mode controls local versus TradingView-like protective re-entry paths (`core/config.py:59,282-288,470-490`; `core/runner.py:1289-1409`).
- **B behavior:** no `tw_*` key, but separate same-bar re-entry knobs exist (`src/config/defaults.py:283-323`).
- **Pine reference:** constant `"local"` with no consumer (`MTC_V2.pine:96`).
- **Disagreement:** A offers multiple replay/re-entry economics with no Pine branch authority.
- **Canonical semantics and reason:** retire the compatibility mode. C05/C21 are the sole reversal/re-entry policy; protective exits never re-enter on the same bar.
- **Chosen implementation:** **RETIRE** after reproducing every accepted legacy enum value.
- **GF-32:** a stop bar plus raw entry signal is run under legacy `local`, `delay_after_protective_exit`, `carry_to_next_bar_after_protective_exit`, `next_bar_open_after_protective_exit_signal`, and `next_bar_close_after_protective_exit_signal` (`core/config.py:472-482`); snapshots pin A's exact output/fill bar and price. Corrected-vNext always emits exit only. Opposite-signal reversal is separately asserted under C05 and must be unaffected by this retired key.

### C33 — `tw_reversal_reentry_delay_bars`

- **A behavior:** required nonnegative delay participates in pending re-entry timing (`core/config.py:60,282-288`; `core/runner.py:1289-1409`).
- **B behavior:** no `tw_*` key; has unrelated re-entry controls.
- **Pine reference:** constant `0` with no consumer (`MTC_V2.pine:97`).
- **Disagreement:** only A assigns economic meaning, and only with a legacy mode.
- **Canonical semantics and reason:** retire it. Delayed stale decisions are forbidden by C05/C27; post-exit cooldown is the explicit C06 strategy concept and requires a fresh decision.
- **Chosen implementation:** **RETIRE** after branch reproduction.
- **GF-33:** legacy non-local mode with delays 0 and 2 pins A's earliest fill bars. Corrected-vNext with post-exit cooldown 2 blocks two bars and still requires a fresh third-bar decision; absence of that decision produces no entry.

### C34 — `tw_margin_call_mode`

- **A behavior:** selects `off` or a TradingView-style margin approximation (`core/config.py:61,282-288,470-490`; `core/runner.py:1411-1502`).
- **B behavior:** independently approximates margin liquidation with different constants (`src/engine/mtc_runner.py:631-772,2393-2430`).
- **Pine reference:** constant `"off"` without consumer and no strategy margin declaration (`MTC_V2.pine:7,98`).
- **Disagreement:** neither approximation is an authoritative shared venue model.
- **Canonical semantics and reason:** reproduce `off` and A's enabled legacy branch; then retire the key in favor of C10's frozen venue margin model.
- **Chosen implementation:** **RETIRE**.
- **GF-34:** one leveraged loss path runs legacy `tw_audit_semantics_mode=off, tw_margin_call_mode=off` (no margin exit) and `tw_audit_semantics_mode=research, tw_margin_call_mode=tradingview` (exact A partial/full result). Corrected-vNext with no venue schedule emits unavailable/no liquidation; supplied venue schedule produces C10's exact liquidation, demonstrably independent of this key.

### C35 — `tw_margin_call_split_entries`

- **A behavior:** required and stamped/read but no economic consumer was found (`core/config.py:62,282-288`; architecture audit `_AI_MEMORY/MASTER_ARCHITECTURE_DECISIONS_AND_TARGET_STATE_2026-08-19.md:587,591-593,598-610`).
- **B behavior:** no `tw_*` references.
- **Pine reference:** constant `false`, no consumer (`MTC_V2.pine:99`).
- **Disagreement:** the key implies a branch that does not exist; fabricating one is prohibited.
- **Canonical semantics and reason:** retire as non-capability after proving both booleans are behaviorally identical. It does not survive into canonical configuration.
- **Chosen implementation:** **RETIRE**, with no fabricated branch.
- **GF-35:** run the same legacy margin/add scenario with false and true; normalized events, fills, PnL, and state hash must be identical while config provenance differs. Static corrected fixture rejects the key. Any economic difference fails the disposition and reopens investigation.

### C36 — `tw_be_semantics_mode`

- **A behavior:** required mode selects local versus TradingView/confirmed BE timing (`core/config.py:63,282-288,470-490`; `core/exits.py:278-350`; `core/runner.py:1241-1409`).
- **B behavior:** no `tw_*` key and uses high/low BE semantics (`src/engine/mtc_runner.py:2450-2480`).
- **Pine reference:** constant `"local"` has no consumer; Pine BE is close-based (`MTC_V2.pine:100,1143-1172`).
- **Disagreement:** several trigger/effective-bar behaviors coexist.
- **Canonical semantics and reason:** reproduce each validated legacy mode, then retire the selector. C14 is the one canonical behavior.
- **Chosen implementation:** **RETIRE**.
- **GF-36:** one OHLC sequence runs `local`, `tradingview`, and `next_bar_confirmed` (`core/config.py:486-487`) and snapshots each exact stop revision/fill bar. Corrected-vNext must equal GF-14 regardless of removal of this key.

### C37 — `tw_trailing_semantics_mode`

- **A behavior:** required mode selects local versus alternate trailing timing (`core/config.py:64,282-288,470-490`; `core/exits.py:278-350`; `core/runner.py:1241-1409`).
- **B behavior:** no `tw_*` key and uses R-distance trailing (`src/modules/risk/tp_calculator.py:253-320`).
- **Pine reference:** constant `"local"` has no consumer; Pine uses ATR-close trailing (`MTC_V2.pine:101,1143-1172`).
- **Disagreement:** distance definition and effective-bar timing differ.
- **Canonical semantics and reason:** reproduce each validated legacy mode, then retire the selector. C15 is the one canonical behavior.
- **Chosen implementation:** **RETIRE**.
- **GF-37:** a sequence with intrabar activation but sub-threshold close, later qualifying close, and following-bar stop touch runs `local`, `tradingview`, and `next_bar_confirmed` (`core/config.py:488-490`). Snapshot each exact revision/fill bar; corrected-vNext must equal GF-15 and use ATR distance.

## 4. Cross-cutting acceptance rules for WP-P0-10

1. Every GF fixture must record source configuration, normalized bars, frozen instrument/venue metadata, normalized events/fills/state, and the final deterministic state hash.
2. Every long economic fixture gets a reflected short fixture unless this table explicitly declares an asymmetry.
3. Every fixture asserted as proof of a defect closure must satisfy D026: recorded RED against the exact pre-fix behavior or an equivalent deliberate mutation, then GREEN with the corrected behavior.
4. Legacy branch fixtures are descriptive only. They do not make a legacy behavior canonical.
5. Canonical and legacy outputs must be labeled separately; no blended aggregate is acceptance-bearing.
6. Unknown/non-expressible inputs fail closed with a typed reason. No fallback may silently change sizing, stop, target, margin, fill, or cost method.

## 5. Explicit non-decisions

- This document does not select production venues, broker credentials, live deployment topology, or concrete future host drift-alarm thresholds; WP-P0-26 owns the host/NTP mechanism.
- It does not claim current parity, approve trading, or authorize Pine/kernel/Bridge edits.
- It does not move code. WP-P0-10 must first construct and falsify the golden fixtures above; later packages may then use those tests as migration authority.
