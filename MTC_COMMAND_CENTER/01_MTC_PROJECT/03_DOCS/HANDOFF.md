# HANDOFF — MTC V2

_Last updated: 2026-05-29_

## Current State

| Area | State |
|---|---|
| Repo root | `C:\LAB\tradingview-lab` |
| Active MTC root | `01_MASTER TEMPLATE_V2` |
| Pine | `01_PINE/MTC_V2.pine` |
| Python | `00_PYTHON/mtc_v2/` |
| Export suite | `05_PARITY/MTC_V2_TW_EXPORT_CASE_SUITE_V2.csv` + `TW_EXPORT_CASES_V2/` |
| Parity tracker CSV | `05_PARITY/MTC_V2_PARITY_CASES.csv` |
| Portable handoff | `MTC_V2_PORTABLE_HANDOFF/` — intentionally tracked in git |
| Legacy tv_manual_inputs | Removed from git and disk (`4852cee5`). Do not reference. |
| `mtc_backtest/` | Legacy — NOT parity owner for MTC V2 work |
| Execution direction | `close_only_deterministic_v2` |

## Recent Commits

```text
ed016e32 docs: update handoff to reflect AUTO_061 L22 PASS and window fix
4eb97447 fix(L22): align candle_pattern_lookback window with Pine barssince semantics
65be548c docs: refresh handoff and portable package
64e774c6 feat: add case_163 L22 Candle Pattern Lookback parity case
4af32d71 feat: bootstrap Range Filter optimization POC
096c35c9 fix: surface internal lifecycle failures in factory regression summary
4852cee5 chore: add portable handoff to source and remove stale legacy parity exports
7be55c3d fix: normalize Swing+ATR case plan overrides
```

## Validation Known Green (as of 4eb97447)

```text
160 tests passed  (parity_oracles + 00_PYTHON/mtc_v2/tests)
Range Filter feature parity: FEATURE_TRACE_PASS
Independent reference oracle: REFERENCE_PASS
Factory regression: fail_count=0, internal_fail_count=0
AUTO_061 L22 candle_pattern_lookback: PASS — 4/4 trades, zero-diff metrics
```

## Active Backlog

| Priority | Item | Status |
|---|---|---|
| 1 | **TW export for `case_163`** — `use_candle_pattern_gate=true`, `candle_pattern_lookback=5`, `exit_on_candle_pattern_block=true`. Place xlsx in `TW_EXPORT_CASES_V2/case_163/`, mark READY. Then run `python parity_compare.py --tracker-case AUTO_061 --fetch-fresh`. | Waiting on user |
| 2 | **TW re-export for `case_134` and `case_153`** — PineTS/Python PASS (146/146), stale 2026-04-14 exports | Waiting on user |
| 3 | **TW export for `case_160` and `case_161`** | MISSING_EXPORT |
| 4 | **Range Filter optimization smoke** — job: `optimization/jobs/smoke/range_filter_producer_only_seed_smoke.yml`. Requires data bundle at `MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427/`. | Ready to run |
| 5 | `case_124` / `case_125` re-export parity verify | Deferred |

## Bug Fixes Closed (2026-05-29)

Four Python runner bugs fixed; all cases now PineTS/Python PASS:

1. **Exit reason label map** (`PYTHON_REASON_MAP` in `parity_compare.py`): `"eod"→"EOD_EXIT"`, `"eow"→"EOW_EXIT"`. Fixes `case_110` / `case_111`.

2. **L18 one-shot fire reset missing** (`runner.py`): Pine resets arm/count/direction state after each confirmed fire. Python was missing this reset, causing repeated L18 confirms. Fixed.

3. **Deferred flip set from pre-L21 signal** (`runner.py` opp exit block): `_deferred_flip_side` was sourced from pre-L18/L21 `gated_candidate_side`, bypassing L21 retest suppression. Moved to post-L18+L21 `gated`. Fixes `case_154`.

4. **L18 output gated with `gated.short` instead of `gate_short_ok`** (`runner.py`): For pulse-only producers (Supertrend), `raw.short=False` on hold bars broke the confirmation count. Changed to `gate_results` directly. Fixes `case_134` / `case_153` (Python 0→146 trades).

5. **L22 `candle_pattern_lookback` window off by one** (`runner.py`): `_candle_history.append(bar)` runs *after* `_evaluate_entry_gates()`, so the current bar was absent from the gate window. Pine's `ta.barssince(pattern) < lookback` counts from bar[0] (current bar). Fix prepends current bar at the call site and slices to last `(lookback+1)` entries. AUTO_061: PASS. (`4eb97447`)

## Audit Rules

- TradingView workbook `Properties` sheet = source of truth for all parity configs.
- `manual_tw_futures_audit.py` derives symbol/TF from workbook `Properties`; no hard-coded `BTCUSDT`.
- PineTS and Python must run on identical workbook-derived config.
- `List of trades` sheet = oracle for trade parity and outcome parity.
- Per new case: (1) verify workbook settings → (2) verify expected trade/outcome effect vs baseline → (3) run parity.
- `TV Margin % = 100 / max_leverage_cap` (5x → 20%, 100x → 1%).
- If PineTS/Python reports PASS but workbook symbol differs from local run symbol, audit is invalid; fix and rerun.
- Do not run multiple `parity_compare.py --fetch-fresh` jobs in parallel (shared `data/mtc_signals.json`).
- Do not claim TradingView release parity from optimization output.

## Baseline

- Workbook: `TW_EXPORT_CASES_V2/case_001/MTC_V2_BINANCE_BTCUSDT.P_2026-04-05_f6b77.xlsx`
- Settings: `Max Lev=5`, `SL Mode=ATR`, `Margin long/short=20%/20%`, `Commission=0`, `Slippage=0`
- Audit contracts: trade strict pass, trade soft pass, outcome strict pass, outcome soft pass.

## Case Block Summary

| Block | Cases | Parity Status |
|---|---|---|
| HTF Trend | 021–025 | TW/Python strict PASS; PineTS blocked when HTF mocks unavailable |
| MA Slope | 026–028 | PineTS/Python strict PASS; TW vs local drift-only |
| McGinley | 029–032 | `case_032` refreshed strict PASS; export-faithful `McGinley HTF TF=D` |
| Volume | 033–035 | TW/PineTS/Python trade strict PASS; outcome TV-accounting fail |
| ADX | 036–040 | Refreshed `case_039/040` strict PASS; export-faithful `ADX HTF TF=D` for 040 |
| Chop | 041–045 | Refreshed `case_044/045` strict PASS; export-faithful `Chop HTF TF=D` for 045 |
| ATR Vol Floor | 046–049 | TW/PineTS/Python counts match; drift-only strict fail |
| MACD Gates | 050–055 | TW/PineTS/Python counts match; drift-only strict fail |
| MACD Params | 056–059 | Same pattern; `case_055` re-export changed `macd_fast_len: 12→18`; `case_056–059` branch uses `zero_dist_min=5.0` |
| Confirm / Retest | 103–162 | 50/58 PASS; `case_134/153` PineTS/Python PASS but stale TW; `case_160/161` MISSING_EXPORT |
| L22 Candle Pattern | 163 / AUTO_061 | PineTS/Python PASS; TW export pending |

## Deferred / Informational

- Small TW vs local qty drift remains in several ATR/leverage cases; lifecycle already understood as drift-only.
- Outcome soft pass blocked by TradingView excursion/accounting semantics.
- `case_054` is not a bug: `Zero Dist Min=0` is a tautology by design.
- `st_use_ha` remains scaffold-only; no real HA support.
- `case_007` is `DEFERRED` pending `L18c / trend_rearm_add` approval; do not harmonize status without explicit decision.
- Range Filter optimization POC: seed regions defined, no TW release parity claim. Data bundle required at `MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427/` (ignored by git).
- Factory regression `internal_fail_count` / `no_internal_failures` added; `full_suite_safe_to_run_next` is false when `internal_fail_count > 0`.
- Gate release audit (optional delayed entry after gate block): prompt at `04_AUDIT/CLAUDE_PENDING_GATE_RELEASE_AUDIT_v2.md`. Deferred.
- Big overnight multi-asset optimization partial (`168k/6.6M` evals); resume from `reports/optimization/big_overnight_multiasset/resume_registry.sqlite` with `--max-workers 16`. Not current priority.

## Resume Order

1. This file → `RUNBOOK.md` → `MTC_V2_ARCHITECTURE.md`
2. `05_PARITY/MTC_V2_TW_EXPORT_CASE_SUITE_V2.csv`
3. `05_PARITY/MTC_V2_PARITY_CASES.csv`
4. `reports/tracker_cases/<case>/parity_compare.json` (if last run matters)
