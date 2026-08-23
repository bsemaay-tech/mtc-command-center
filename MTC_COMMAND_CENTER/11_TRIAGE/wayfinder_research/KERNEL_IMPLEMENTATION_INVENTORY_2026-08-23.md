# Kernel Implementation Inventory (wayfinder #68, map #67)

Read-only research ticket. Answers: how many independent trade-logic implementations does this
repo hold, what does each implement, who calls it, how do they diverge, and how active is each.
Everything below is verified directly against source on `master` `3d6a621c` (branch cut point),
inside worktree `C:\WFK1`. No trading code, backtest, or server was executed.

**Prior claim under test:** `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`
F-1 asserts **five** independent implementations of "what is a trade." That count is **confirmed**
for the architecturally-significant, actively-referenced set. One citation inside F-1 (a commit
hash) is wrong and is corrected below (§5). Two additional, much smaller, self-declared
non-production research-batch simulators were also found outside the "five" (§6) — they do not
change the substantive picture but are worth recording since the ticket asked to verify the count
independently rather than trust the prose.

---

## 1. The five, verified

| # | Implementation | Path | Size (verified `wc -l`) | Last commit touching it (verified) |
|---|---|---|---|---|
| 1 | **Pine strategy** | `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine` | 2,079 lines | `77a10e65` 2026-05-31 "init: migrated from tradingview-lab archive" |
| 2 | **MTC_V2 Python kernel** | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/` | 698+587+605+355+70+1,698 = ~4,013 core lines across `config.py`(698) `exits.py`(587) `gates.py`(605) `position_manager.py`(355) `position_sizer.py`(70) `runner.py`(1,698) | `77a10e65` 2026-05-31 — **see §5, brief cites a different hash** |
| 3 | **Second Python MTC engine** | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/` | `engine/mtc_runner.py` = 2,789 lines, plus `modules/risk/position_sizer.py`, `sl_calculator.py`, `tp_calculator.py`, eight filter modules | `b5ed1afa` 2026-06-06 "Complete S1-S7 parallel sprint" |
| 4 | **Research simulator** | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py` → `simulate_slice()` at line 648 | 1,857 lines | `bcecdce0` 2026-07-13 "feat(quantlens): register bridge parity subject keltner_trail_ema8" |
| 5 | **Live executor** | `IBKR_PAPER_BRIDGE/bridge/` | 46,906 lines incl. tests (`store/db.py` 6,894; `engine/orders.py` 3,663; `broker/hyperliquid.py` 2,265; `engine/reconcile.py` 1,665; `engine/risk.py` 730) | `d71bc073` 2026-08-17 "feat(bridge): add interactive Help system map" |

**Independence re-verified:** `grep -rln "mtc_v2" MTC_COMMAND_CENTER/02_MTC_BACKTEST --include=*.py`
returns exactly `parity_compare.py` and `run_2025_audit.py` (parity tooling only — the engine
itself imports none of it). `grep -rln "import mtc_v2|from mtc_v2" IBKR_PAPER_BRIDGE` returns
**zero files**. Confirmed independently, not merely re-quoted.

---

## 2. What each one implements

### #1 — Pine strategy (`MTC_V2.pine`)
- Full lifecycle inline: indicator state (§3), entry/exit signal logic, an L6 position-sizing
  function `calc_l6_qty()` (lines 339–361), a state machine for multi-TP/break-even/trailing
  stops (`l6_tp1_price_state`, `l6_be_active_state`, `l6_trail_active_state`, etc. — plotted for
  debug at lines 1975–2005), and a live order-dispatch section (§9, see §4 below).
- Runs **inside TradingView's own charting engine**, not invoked by any script in this repo. It is
  loaded manually onto a TradingView chart by the owner.
- Costs/fees: modeled by TradingView's own strategy tester settings (external to this repo; not
  independently verified here — out of scope, TradingView-side).

### #2 — MTC_V2 Python kernel (`mtc_v2/core/`)
- `runner.py` (1,698 lines) drives the bar loop; `gates.py` (605) — entry/filter gates;
  `exits.py` (587) — stop/TP/trailing/break-even/time-exit state machine (`update_protective_stop_owner`,
  `sync_working_exit_stops`, `_evaluate_stop_hit` — line 136, 167, 362); `position_manager.py` (355)
  — basket/position bookkeeping; `position_sizer.py` (70) — L6 risk-based quantity (`calc_qty`,
  lines 24–70).
- **No commission/slippage/fee code anywhere in `mtc_v2/core/`** — confirmed by grep for
  `commission|fee_pct|fee_bps|slippage` across the directory: zero matches. The kernel is
  deliberately I/O- and cost-free (matches the brief's later architectural framing of K as
  "bars + config → intent").
- Called by: research/optimization tooling in `01_MTC_PROJECT/tools/` (`run_mtc_overnight_optimization.py`,
  `run_12h_backtesting_session.py`, `run_big_overnight_multiasset_optimization.py`,
  `run_mtc_multidataset_walkforward_optimization.py`, `run_worker_scaling_benchmark.py`,
  `runner_metrics_adapter.py`), its own test suite (`01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/*`,
  ~15 files), parity oracles (`01_MTC_PROJECT/parity_oracles/`), and — read-only, as artifacts —
  the dashboard (`08_DASHBOARD_APP/apps/api/mcc_readonly/mtc_v2_reader.py`, see the stale-path
  finding in §7).

### #3 — Second Python MTC engine (`02_MTC_BACKTEST/src/`)
- `engine/mtc_runner.py` (2,789 lines) is a second, independently-written Pine port with its own
  stop-hit detectors (`_long_stop_hit`/`_short_stop_hit`, lines 592/597), its own trailing-stop and
  time-stop logic (`_time_stop_would_trigger`, line 479), and its own risk stack:
  `modules/risk/position_sizer.py`, `sl_calculator.py`, `tp_calculator.py`, plus eight filter
  modules, plus `engine/fee_model.py` — a full commission+slippage model (see §3).
- Called by: its own CLI (`src/cli/run_backtest.py`, `mtc_engine_validate.py`), its own optimizer
  (`optimizer_v0/search.py`, `optimize/runner.py`), ~10 analysis scripts under `scripts/`
  (`trade_microscope.py`, `robustness_runner.py`, `parity_regression.py`, etc.), its own test suite
  (12 files under `tests/`), and its own **Streamlit dashboard**, `02_MTC_BACKTEST/app.py`
  ("MTC Python Backtest & Optimization System" — confirmed by reading the file header). Results are
  also surfaced read-only into the main dashboard via `08_DASHBOARD_APP/.../backtest_reader.py`
  and `optimization_reader.py` (both point at `03_QUANTLENS/05_BACKTEST_RESULTS`).

### #4 — Research simulator (`mega_walk_forward.py`)
- `simulate_slice()` (line 648) is a **different economic model**, not a Pine port: it drives a
  parameter-grid screen (rolling-lookback / ATR-multiple stops built per strategy family, e.g.
  `low.rolling(stop_lookback).min()`), applies a single flat round-trip cost
  (`COST_BPS = 8.0` at line 64, applied as `cost = COST_BPS / 10000.0` at line 655), and — per the
  brief's F-4, not independently re-verified here in depth — discards per-trial trade detail.
- Called by ~20+ overnight/batch runner scripts in `03_QUANTLENS/tools/` and `11_TRIAGE/`
  (`overnight_orchestrator.py`, `overnight_v2_runner.py`, `strat_extra_runner.py`,
  `cpcv_validator.py`, `focused_validation.py`, `multiwindow_oos.py`, `finalize_bootstrap_bh.py`,
  and more). Per `AGENTS.md` (per the brief; not re-verified word-for-word here) this is the
  **canonical, promotion-deciding research engine**. Results land in
  `03_QUANTLENS/05_BACKTEST_RESULTS`, surfaced read-only via the same dashboard readers as #3
  (`backtest_reader.py`, `scorecard_reader.py`, `registry_reader.py`) — the dashboard does not
  distinguish which of #3/#4 produced a given result directory.

### #5 — Live executor (`IBKR_PAPER_BRIDGE/bridge/`)
- `engine/risk.py` (`RiskEngine`, `RiskConfig`) — sizing + a real gate chain (consecutive-loss,
  leverage, stop-distance, stop-side, min-order, notional cap, margin cap — lines 361–408).
  `engine/orders.py` (3,663 lines) — idempotent order placement, **native `reduce_only` stop
  orders** placed on the real venue (not a simulated hit check — confirmed by grep: `reduce_only`
  appears at orders.py lines 502, 509, 635, 756, 1564, 4260, 5343, 5898, including
  `flatten_reduce_only` / `kill_flatten_reduce_only` safety primitives). `broker/hyperliquid.py`
  (2,265 lines) — real exchange integration. `engine/reconcile.py` (1,665 lines) — partial-fill /
  restart reconciliation.
- Strategy plug-in wired in `bridge/app.py`: `KeltnerTrailEma8`
  (`bridge/engine/strategies/keltner_trail_ema8.py`) — self-documented at line 12 as
  **"Plumbing test subject only, not a promotion claim."** It emits only a `Signal`
  (direction/ref_price/stop_loss/take_profit — no `qty`); all sizing, gating and order mechanics
  are the Bridge's own. This is a signal generator plugged into implementation #5, **not a sixth
  implementation** — it does not carry its own sizing/fee logic.
- Costs: real exchange fees at fill time — there is no in-repo cost *model* for the Bridge because
  it isn't simulating; it pays what the venue charges.
- Called by: `bridge/app.py` (FastAPI service, `BridgeEngine` + `HyperliquidBroker`/`MockBroker` +
  `Store` (SQLite) + `RiskEngine`), its own dashboard/help surface
  (`bridge/static/help_map.json`, referenced by owner-facing tooling per memory —
  `KVM2_RUNKIT/Start-BridgeDashboard.cmd`, not itself part of this repo tree), and read-only status
  surfaced into the main dashboard via `liveops_reader.py` (reads a status snapshot file,
  `03_STATUS/LIVEOPS_STATUS.json`, not the Bridge's SQLite store directly — confirmed by reading
  the file, lines 11–22).

---

## 3. Divergence spot-checks (verified against source, not prose)

### 3a. Position sizing — three different formulas, confirmed
- **Pine** (`MTC_V2.pine:351`): `raw_qty := risk_amount / (per_unit_risk * contract_multiplier)`
  — includes the contract multiplier in the divisor.
- **MTC_V2 kernel** (`mtc_v2/core/position_sizer.py:47`): `raw_qty = risk_amount / per_unit_risk`
  — **omits** `contract_multiplier` from the same calculation (the same function *does* use it in
  the leverage cap, lines 52–54, and the notional check, line 66 — present in the caps, absent
  from the raw quantity). For any instrument with `contract_multiplier != 1`, Pine and the kernel
  return different sizes from identical inputs. Confirmed by direct read of both files.
- **Bridge `RiskEngine`** (`bridge/engine/risk.py:380-381`): `raw_qty = risk_dollars / stop_distance`
  — a third, independent formula with its own default risk percentage
  (`risk_pct_per_trade = 0.005` at line 37, i.e. 0.5%) versus the kernel's default 1.0%
  (`mtc_v2/core/config.py:66-67`, not independently re-verified line-by-line here but consistent
  with the checked-in default pattern). Two percent points apart on otherwise-identical inputs.
- **Second engine** (`02_MTC_BACKTEST/src/modules/risk/position_sizer.py:34-77`) adds a **fourth**
  distinct wrinkle none of the other three carry: a minimum stop-distance floor,
  `min_sl_dist = max(entry_price * 0.001, mintick * 10.0)`, applied *before* the risk-amount
  division (lines 60–67) — a safety clamp that doesn't exist in the kernel's `calc_qty` or in
  Pine's inline `calc_l6_qty`.
- **Notional gate asymmetry, confirmed:** the kernel rejects to 0 when
  `rounded_qty * entry * contract_multiplier < instrument.min_notional`
  (`position_sizer.py:66-68`); Pine's `calc_l6_qty` (lines 339-361) gates only on `min_qty`
  (`syminfo.mincontract`), **no notional gate exists in the Pine function** — confirmed by reading
  the full function body.

### 3b. Stop handling — a real mechanism split, not just a formula difference
- **Bridge:** stops are **real, venue-side `reduce_only` orders** — the position is protected by an
  order sitting on the exchange, independent of whether the bridge process is even running.
- **MTC_V2 kernel and the second engine:** stops are **simulated, bar-by-bar hit checks** against
  an in-memory `active_stop_price` (`mtc_v2/core/exits.py:278-368`, `_evaluate_stop_hit` at line
  362) or `sl_price`/`trailing_stop` (`02_MTC_BACKTEST/src/engine/mtc_runner.py:592-2491`) — no
  order exists anywhere; a backtest bar simply crosses a price and the code marks the trade closed.
  These are two independently-written state machines (owner tags: `STOP_OWNER_TRAIL`,
  `STOP_OWNER_BE` in the kernel) doing conceptually the same thing for two different Pine ports.
- **Research simulator:** stops are **parametric**, not stateful — a rolling-lookback low or an
  ATR-multiple offset computed once per configuration
  (`mega_walk_forward.py:398-399` `stop = low.rolling(stop_lookback).min()`), swept across a grid.
  There is no break-even/multi-TP/trailing state machine in `simulate_slice()` comparable to #2/#3.
- Net: three genuinely different *mechanisms* for "what is a stop" (real order / simulated
  state-machine hit-check / parametric grid input), not merely three parameter sets.

### 3c. Fee/cost treatment — verified, all different
- **MTC_V2 kernel:** none. Zero fee/commission/slippage code in `mtc_v2/core/` (grep-confirmed).
- **Second engine:** `02_MTC_BACKTEST/src/engine/fee_model.py` — `commission_percent` (default
  0.04% of notional, applied **separately on entry and exit**, `FeeConfig` line 23-27) plus
  `slippage_ticks` (default 5 ticks, applied as a signed price adjustment via
  `adjust_entry_price`/`adjust_exit_price`, lines 149-191) — a two-part, per-side, tick-aware model.
- **Research simulator:** a single flat round-trip cost, `COST_BPS = 8.0` (line 64) applied as
  `cost = COST_BPS / 10000.0` (line 655) — one number, no slippage in the fill path (a separate
  `SLIPPAGE_BPS_PER_SIDE = 2.0` at line 65 is explicitly commented as "additional post-hoc
  slippage stress, separate from existing COST_BPS fee model" — i.e. a stress overlay, not part of
  the base simulation).
- **Bridge:** no model — it pays whatever Hyperliquid actually charges at fill.
- **Pine:** whatever TradingView's own strategy-tester commission/slippage settings are configured
  to (external UI state, not in this repo — not independently verified here).

---

## 4. The WunderTrading `alert()` path (Pine, implementation #1)

Confirmed by direct read of `MTC_V2.pine`:
- Section header at line 2008: `// SECTION 9 - WUNDERTRADING ALERT DISPATCH (L25)`.
- Arming condition, line 2010:
  `l25_any_code_set = wt_enter_long_code != "" or wt_exit_long_code != "" or wt_enter_short_code != "" or wt_exit_short_code != "" or wt_exit_all_code != ""`.
- Entry dispatch, line 2020: `alert('{"code":"'+l25_entry_code+'","order_type":"'+wt_order_type+'",...}', alert.freq_once_per_bar_close)`.
- Exit dispatch, line 2028: `alert('{"code":"'+l25_exit_code+'","reduce_only":true}', ...)`.
- The five `wt_*_code` inputs all default to `""` (lines 176-180, `input.string("", ...)`), so
  **with default/shipped inputs, no alert ever fires** — the path is armed purely by the owner
  typing a non-empty string into a TradingView indicator-settings text field on a live chart. There
  is no separate boolean "enable" switch, no second confirmation, and — because this is a Pine
  `alert()` call consumed by TradingView's own alert-webhook mechanism — **nothing in this repo can
  observe whether it is currently armed on any given live chart.**
- Confirmed consumerless in Python: `mtc_v2/core/config.py` declares 13 `wt_*` keys (per the
  brief's F-8, not re-counted line-by-line here) and grepping `wt_` in `runner.py`/`exits.py`
  finds nothing; `02_MTC_BACKTEST/src/` and `IBKR_PAPER_BRIDGE/bridge/` have zero WunderTrading
  references (grep-confirmed, both directories return no matches for `wundertrading` case-insensitive
  other than `04_SHARED/modules/LIB_WUNDERTRADING_HELPERS.pine`, a shared Pine helper library, and
  the docs/manifests already indexed by the brief).
- This matches the master brief's F-8 finding exactly, independently re-derived here from source
  rather than taken on trust.

---

## 5. Correction to the master brief's F-1 citation

The brief cites the MTC_V2 Python kernel's last-touch commit as `5923c20c` (2026-05-31). That
commit **exists** in this repo but its message is *"fix(test): rewrite legacy paths in
test_manual_tw_futures_audit.py"* and its diff touches only a hardcoded-path fix in a single test
file (`test_manual_tw_futures_audit.py`) — it does **not** touch anything under `mtc_v2/core/`
(confirmed via `git show --stat`). The actual (and only) commit touching `mtc_v2/core/` in this
repo's history is `77a10e65` (2026-05-31, "init: migrated from tradingview-lab archive") — the
same commit that last touched the Pine file. The **date** in the brief (2026-05-31) is coincidentally
right; the **hash** is wrong. All other F-1 commit hashes (`b5ed1afa`, `bcecdce0`, `d71bc073`) were
independently re-verified against `git log`/`git show` and are correct.

---

## 6. Beyond the five: two dormant, self-declared non-production simulators

Not part of the "five" and not architecturally significant, but found while checking the count
independently rather than assuming it:

- **`MTC_COMMAND_CENTER/03_QUANTLENS/research/strategy_batch_2026_05_03/shared/backtest_utils.py`**
  (`run_signal_backtest`, 97 lines) — a small standalone signal-to-PnL loop used by
  `strategy_batch_2026_05_03/run_batch.py` to triage ~12 QuantLens candidate strategies on
  2026-05-03. Byte-identical (same md5) to the copy under
  `strategy_batch_2026_05_03_AUDITED/shared/backtest_utils.py`, so this is one implementation
  duplicated into an audited-copy directory, not two. **Last touch: `77a10e65` (2026-05-31 migration
  commit) — untouched since the repo was created**, i.e. frozen/dormant.
- **`MTC_COMMAND_CENTER/03_QUANTLENS/research/overnight_intake_batch_2026_05_03/run_overnight_batch.py`**
  (`run_strategy()`, line 1233; file is 1,605 lines) — a second, separate one-off batch runner with
  its own per-candidate trade loops and its own flat `ROUND_TRIP_COST_PCT` cost constant. Its own
  generated README explicitly states: *"This is Python-only first-pass triage. It is not Pine-ready
  and not production integration."* **Last touch: also `77a10e65`, same frozen migration commit.**

Neither is imported by, or feeds, any of the five architecturally-live implementations, any runner
outside its own one-off batch, or the dashboard's promotion/registry readers. Both are best
understood as archived research exhaust from a single 2026-05-03 intake sprint, not live kernel
candidates. This inventory did not exhaustively audit every per-candidate strategy file under
`03_QUANTLENS/research/**` (dozens of `CANDIDATE_*`/`strategy_batch_*` directories exist across
`_CLEAN`/`_AUDITED`/`_5M_RERUN` variants) — that would be a much larger, separate research pass;
the two engines above are the only distinct **simulation loops** found, the rest being data/config
variants consumed by one of those two loops or by #4.

---

## 7. A live wiring gap found in passing (dashboard side, not kernel side)

`08_DASHBOARD_APP/apps/api/mcc_readonly/mtc_v2_reader.py:18` resolves
`mtc_root = root.parent / "01_MASTER TEMPLATE_V2"`. That directory **does not exist** in this repo
— the current path is `MTC_COMMAND_CENTER/01_MTC_PROJECT` (confirmed: `ls MTC_COMMAND_CENTER`
shows `01_MTC_PROJECT`, no `01_MASTER TEMPLATE_V2`). This looks like a stale reference surviving a
past rename; `build_mtc_v2_readiness()` would resolve against a nonexistent path. Flagged for
awareness — out of scope to fix under a read-only research ticket, and not verified beyond the one
grep/read pass above (no test run against the dashboard was performed).

---

## 8. Answer to the ticket's question

**The audit's "FIVE" is confirmed** for the architecturally-significant set: Pine strategy, MTC_V2
Python kernel, the second `02_MTC_BACKTEST` Python engine, the `mega_walk_forward.py` research
simulator, and the `IBKR_PAPER_BRIDGE` live executor. All five are independently written, none
imports another's trade-logic code, and all five are actively referenced by at least one runner,
test suite, or dashboard reader as of this repo's `master` tip. Three concrete divergences were
spot-checked and confirmed by reading code, not prose: position sizing (four distinct formulas
across the five, once the second engine's stop-floor clamp is counted), stop handling (a real
venue-side order vs. two independently-written simulated hit-detectors vs. a parametric grid
input), and fee treatment (none / two-part per-side model / flat round-trip bps / real exchange
fees / TradingView-tester-external). The Pine `alert()` → WunderTrading dispatch path is real,
unconditional once armed, defaults to inert, and is unobservable from this repo once a chart sets
a non-empty code — exactly as the master brief's F-8 states, independently re-derived here. One
citation error in the brief's F-1 table (a wrong commit hash for the kernel, not affecting the
date or the count) is corrected in §5. Two additional but dormant, self-declared non-production,
frozen-since-migration research-batch simulators exist outside the "five" (§6) and do not change
the substantive picture the reference-implementation doctrine needs to resolve.
