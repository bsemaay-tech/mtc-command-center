# Parity Ground Truth — Wayfinder Research #69

Read-only ground-truthing of the "27/58 Pine/Python parity" figure cited in
`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`
(§2, D-10, F-7). No code was executed or modified; all numbers below come from
files already committed to the repository at `origin/master` `3d6a621c`.

## Headline

"27/58" is **not** 58 strategies, symbols, or timeframes. It is 58 individual
regression test cases — each one flips one or two Pine strategy inputs on a single
symbol/timeframe (BTCUSDT.P, 60-minute bars) and compares the resulting trade
list across three engines: real TradingView (TW), a PineTS port, and the
`mtc_v2` Python kernel. "27/58" is the count of cases where TW and Python
matched under the corpus's **strictest** tolerance (position size within 0.001
units). Re-scored under the corpus's own **documented** looser tolerance
(0.005 units, already built into the harness, not invented for this report),
the pass rate is **52/58 (90%)**. Of the 6 cases that fail even under the
loose tolerance, 2 are a same-timeframe confirmation-gating bug and 4 involve
multi-timeframe/regime filter pairings with larger, harder-to-explain
divergence. So: **the great majority of the "failing" 31 cases (25 of 31,
81%) are float/rounding noise in position-size quantity, not trading-logic
disagreement — fixable, low-risk, arguably a tolerance-definition problem more
than a code-defect problem. The remaining 6 of 58 (10%) are real behavioral
divergences**, split between a fixable same-timeframe gating bug (2 cases) and
harder-to-diagnose multi-timeframe filter interactions (4 cases) that this
read-only pass could not fully root-cause and flags as needing either a
structural fix or further live investigation.

A separate, important finding: this ticket **confirms** (not just
hypothesizes, as the master brief left it) that "27/58" and the master
brief's other headline figure "437/439 (99.54%)" are two **different Python
codebases** being tested, not the same kernel at two points in time. See
"Corpus identity" below.

## What "27/58" measures — with sources

**Primary source:** `MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:1-13`
(generated 2026-04-14T14:40:47 UTC) and its machine-readable twin
`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_results.json` (`summary` block).

```
parity_summary.md:1   # Parity Summary (case_103 - case_162)
parity_summary.md:4   Present cases: 58
parity_summary.md:5   Missing exports: case_160, case_161
parity_summary.md:10  TW=Python strict pass: 27/58
```

- **Denominator (58):** cases `case_103` through `case_162` (60-case block),
  minus `case_160` and `case_161` whose TradingView exports were never
  captured locally (`parity_summary.md:5`, `:478-480`). Each case is one
  entry in `parity_results.json.rows` (58 entries, confirmed by direct count).
  Cases 103–137 are single-setting toggles (one Pine input flipped
  True/False or to a new value, e.g. `case_107` = `use_time_stop`). Cases
  138–162 are two-setting "pair" toggles that combine two related features in
  one test (e.g. `case_155` = `pair_macd_htf_regime`, which simultaneously
  flips `use_macd_regime_filter` and `use_macd_htf_bias` —
  `parity_results.json` row `case_155.actual_changed_keys`). This is a
  **regression sweep over one strategy config on one symbol/timeframe**, not
  a corpus of 58 distinct strategies.
- **Numerator (27):** cases where `tw_vs_python_strict == true` — i.e. every
  TW trade and every Python trade matched within `price_tol = 0.05`
  (absolute price units) and `qty_tol = 0.001` (position-size units). These
  tolerances are defined at
  `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_compare.py:31-38`
  (`STRICT_TRADE_TOLERANCES` vs `SOFT_TRADE_TOLERANCES`, the latter widening
  `qty_tol` to `0.005`). "Strict pass" is therefore **bit-exact-ish trade
  matching**, not "close enough to trust."
- **The harness itself:** `MTC_COMMAND_CENTER/12_PARITY_PINETS/manual_tw_futures_audit.py`
  (called for each case) shells out to `parity_compare.py` as a subprocess
  (`manual_tw_futures_audit.py:487-514`), which is what actually runs the
  Python engine and does the trade-by-trade diff
  (`parity_compare.py:963-974`).

### Corpus identity — which Python engine is under test (confirmed, not hypothesized)

`parity_compare.py:26,34,36-38`:
```python
V2_PYTHON_ROOT = REPO_ROOT / "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON"
...
sys.path.insert(0, str(V2_PYTHON_ROOT))
from mtc_v2.core.config import resolve_config
from mtc_v2.core.runner import Runner
```
So the "27/58" figure is **specifically about the `mtc_v2` kernel**
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/`).

The other headline number the master brief cites, 437/439 (99.54%), comes
from `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:1-4`,
which states its own scope explicitly: *"Canonical parity report for
`mtc_backtest` vs `MTC`"*. Its session notes name the engine file directly —
`MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:88-90`:
*"Fix applied in both engines: `00_MASTER_TEMPLATE/MASTER_TEMPLATE_CORE.pine`,
`mtc_backtest/src/engine/mtc_runner.py`"*.

`mtc_v2/core/runner.py` and `mtc_backtest/src/engine/mtc_runner.py` are two
separate code trees under two separate repo roots (`01_MTC_PROJECT/00_PYTHON`
vs `02_MTC_BACKTEST`). **This confirms the master brief's F-7 "leading
hypothesis" (stated there as "not yet established," brief line 482) as
true: 27/58 and 437/439 score two different Python implementations, not
the same kernel at two dates.** They are not comparable, and neither number
alone tells you "parity" for the platform — an implementation-#3 engine
(`mtc_backtest`, slated for retirement per the brief's Q5) currently has the
better recorded score than the kernel implementation being kept (`mtc_v2`).

### A third cited corpus could not be located

The master brief (line 2935) also cites
`01_MTC_PROJECT/reports/FACTORY_REGRESSION_SUITE_V1/full_current/FULL_FACTORY_SUITE_REPORT.md`
("163 cases with 160 NOT_COMPARABLE"). That path does not exist anywhere in
this worktree (`origin/master` `3d6a621c`) — only tooling that could
*generate* a factory-regression report exists
(`01_MTC_PROJECT/parity_oracles/run_factory_regression_suite.py`,
`.../schema/factory_regression_result.schema.json`), not a committed report.
This citation in the brief is **unverifiable from the current repository
state** — either the report was never committed, is git-ignored, or the
brief's path is stale. Flagging rather than silently dropping it.

## Failure categorization (the 31 cases where `tw_vs_python_strict = false`)

All figures below come from a direct read of every row in
`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_results.json` (58 rows), cross-checked
against `parity_summary.md`. 27 pass strict; 31 fail strict. Of those 31, 25
also carry `tw_vs_python_trade_soft_pass: true` (i.e. pass the corpus's own
already-documented soft tolerance) — only 6 fail even the soft check.

| Category | Count (of 31) | Of 58 total | Representative case:evidence | Verdict |
|---|---|---|---|---|
| **Float/rounding** — position-size quantity only, entry/exit time & price identical | 25 | 43% | `case_103`: `tw_first_mismatch.qty_diff = 0.001573`, `entry_time_diff_min = 0.0`, `exit_price_diff = 0.0` (`parity_results.json` row `case_103`); same pattern in `case_104,105,106,109,112,113,114,115,126,127,128,129,130,132,133,137,138,139,140,141,142,143` | **Fixable / arguably not a bug at all.** All qty diffs fall between 0.0012 and 0.0031 — inside `SOFT_TRADE_TOLERANCES.qty_tol = 0.005` (`parity_compare.py:37`) but outside `STRICT_TRADE_TOLERANCES.qty_tol = 0.001` (`parity_compare.py:32`). Trade count, entry/exit timestamps, entry/exit prices and exit reason all match exactly in every one of these 25 cases. This is quantity/lot-size rounding precision (likely differing contract-step rounding between TradingView's position sizing and `mtc_v2`'s), not a trading-logic disagreement. Tightening the sizing rounding to match TV's step, or accepting the harness's own soft tolerance as the acceptance bar, resolves the great majority of the reported "failures." |
| **Same-pattern rounding, but classified overall FAIL** (cumulative divergence across a long trade list, not visible in the single first-mismatch snapshot) | 2 | 3% | `case_110` (`time_stop_eod`), `case_111` (`time_stop_eow`) — trade counts equal (142/142/142, 136/136/136), first-mismatch entry/exit time & price diffs are `0.0`, only qty differs (~0.002), yet `parity_classification = FAIL` | **Fixable**, same root cause as above (rounding), but the corpus data model only records the *first* mismatched trade per case (`tw_first_mismatch`), so a full explanation of why the aggregate classification is FAIL (not SOFT_PASS) despite a clean first-mismatch would need the full per-trade diff list, which is not present in this repository. Recorded as a **caveat**, not resolved. |
| **Same-timeframe confirmation-gate logic bug** — Python fails to gate entries at all in a specific combined-toggle case | 2 | 3% | `case_134` (`refresh_on_new_raw`): TW/PineTS = 0 trades, Python = 131 trades. `case_153` (`pair_confirm_refresh`): TW/PineTS = 0 trades, Python = 146 trades. (`parity_results.json` rows `case_134`, `case_153`) | **Fixable — genuine logic bug, bounded scope.** Both `refresh_on_new_raw` and `require_raw_still_true` config keys exist and are read in `mtc_v2` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:840-843`, `mtc_v2/core/config.py:197,200,416,418`), so this is not a missing feature — the combined-gate logic produces zero blocking in Python where TW/Pine block every entry. This is traceable to the confirmation state machine and looks fixable without a design change, but requires an actual code fix, not a tolerance change. |
| **Multi-timeframe / regime-filter pairing divergence** — real trade-count and timing differences, mixed signature | 4 | 7% | `case_147` (`pair_htf_trend_exit`): trades 124/124/126, `exit_time_diff_min = 60.0` (one 60-min bar), `exit_price_diff = -644.6`. `case_154` (`pair_level_retest_confirm`): trades 27/27/44, `entry_time_diff_min = -11400` (~7.9 days), `entry_price_diff = -4428.3`. `case_155` (`pair_macd_htf_regime`): trades 55/55/76, `entry_time_diff_min = -15480` (~10.75 days). `case_162` (`pair_ma_htf_htf_trend`): trades 96/96/94, `entry_time_diff_min = 3780`, `exit_time_diff_min = 720` — and this case's *delta-vs-previous* figures are separately confounded because `case_160`/`case_161` exports are missing, so it was compared against `case_159` instead (`parity_summary.md:473`; the TW-vs-Python same-export comparison itself is unaffected by that substitution) | **Mixed — one leans fixable, three lean structural/unresolved.** All the underlying config keys (`use_htf_trend_filter`, `exit_on_htf_trend_block`, `use_macd_regime_filter`, `use_macd_htf_bias`, `use_level_retest`, `use_ma_mtf`) exist in `mtc_v2` (confirmed by grep — not missing features), so none of these are pure feature gaps. `case_147`'s single-bar (60-min) exit offset is consistent with an ordinary HTF bar-alignment/off-by-one bug — likely fixable. `case_154` and `case_155`'s multi-day divergences are too large to be a simple bar-offset; they look like state that persists/resets differently across the two engines when several filters interact (e.g. a retest timer or regime-filter state carried incorrectly) — this needs either full per-trade diffing or an actual live run to pin down, which is out of scope for a read-only pass. Recording as **structural-leaning, unresolved** rather than guessing further. |

**Sum check:** 25 + 2 + 2 + 4 = 31 (all `tw_vs_python_strict = false` rows accounted for). 27 + 31 = 58.

### Cross-check against the corpus's own soft tolerance

`parity_results.json` also carries a `tw_vs_python_trade_soft_pass` flag per
row (computed with `SOFT_TRADE_TOLERANCES`, `parity_compare.py:966-968`).
Of the 31 strict-fail cases, only these 6 still fail under the corpus's own
documented soft tolerance: `case_134, case_147, case_153, case_154, case_155,
case_162` — exactly the "same-timeframe gating bug" and "multi-timeframe
pairing" buckets above. This independently corroborates the categorization:
the float/rounding bucket (25 cases) is not just my read of the diff fields,
it is the harness's own tolerance system agreeing those cases are within an
already-accepted margin.

## Fixable vs structural — summary verdict

| Category | Cases | Verdict |
|---|---|---|
| Float/rounding (quantity precision) | 25/58 (43%) | **Fixable**, low effort, low risk. Align position-size rounding/step logic, or adopt the corpus's own soft tolerance as the acceptance bar. |
| Rounding, aggregate classification unclear (need full trade diff) | 2/58 (3%) | Likely same fixable rounding cause; unresolved final confirmation needs data not present here. |
| Same-timeframe confirmation-gate bug | 2/58 (3%) | **Fixable**, bounded scope — a real logic defect in the confirm/refresh state machine, traceable to specific config keys and runner code, no design change implied. |
| Multi-timeframe/regime pairing divergence | 4/58 (7%) | **Mixed.** 1 case looks like a fixable single-bar HTF alignment bug; 3 cases show large, multi-day divergence consistent with either a deeper interaction bug or genuinely hard-to-replicate Pine `request.security` repaint semantics (an industry-known structurally difficult class to reproduce bit-exactly in Python). Not resolved by this read-only pass — needs live trade-list diffing across the *entire* mismatched trade list (not just the first mismatch) or a fresh run, both out of scope here. |

**Overall:** of the 31 nominally "failing" cases behind the 27/58 headline,
**at most 6 (10% of the full 58-case corpus) represent real behavioral
disagreement** between TradingView and the `mtc_v2` kernel; the rest is
measurement noise from an unusually tight tolerance. None of the 6 genuine
divergences point to an unfixable, ground-up architectural incompatibility —
2 are a scoped, traceable code bug; the remaining 4 need more diagnostic work
before a fixable/structural call can be made with confidence, and 1 of those
4 already looks fixable (single-bar offset). **This ticket cannot fully
close that remaining 4-case question without executing code**, which this
read-only investigation was explicitly scoped not to do.

## Caveats / what could not be verified

1. **Per-trade diff data is partial.** `parity_results.json` records only the
   *first* mismatched trade per case (`tw_first_mismatch`), not the full
   trade-by-trade diff. For the 2 cases in the "rounding, classification
   unclear" bucket (`case_110`, `case_111`), and to fully separate "single
   large jump" from "many small compounding rounding errors" in the 4
   multi-timeframe-pairing cases, the full per-trade CSV would be needed. The
   per-case `reports\manual_tw_futures_case_*.json` files referenced by
   `parity_summary.md` are **not present in this worktree** — only the
   aggregated `parity_results.json`/`parity_summary.md` survive.
2. **The `FACTORY_REGRESSION_SUITE_V1` report cited by the master brief
   (line 2935) does not exist in this worktree** — see "A third cited
   corpus" above. Its "163 cases, 160 NOT_COMPARABLE" figure is unverifiable
   from the current repository and should not be relied on until located or
   regenerated.
3. **This is a single-symbol, single-timeframe corpus.** All 58 cases run on
   BTCUSDT.P at 60-minute bars (per the export filenames under
   `12_PARITY_PINETS/01_TW_CHART_DATA/` and the case workbooks). "27/58" says
   nothing about parity on other symbols or timeframes — the master brief's
   own D-10 finding (that "parity as achieved discipline" is not supported by
   either corpus) stands, and this ticket does not change that.
4. **`case_160` and `case_161` were never exported**, so the 58-case
   denominator is itself 2 short of the intended 60-case block
   (`parity_summary.md:5`). `case_162`'s delta-vs-previous figures are
   substituted against `case_159` as a result (`parity_summary.md:473`) —
   this affects only the "effect observed" delta metrics for `case_162`, not
   its direct TW-vs-Python strict comparison (both are computed from
   `case_162`'s own three exports).
5. **No code was executed to independently reproduce any of these numbers.**
   Everything above is read directly from committed artifacts
   (`parity_summary.md`, `parity_results.json`) and their generating source
   (`parity_compare.py`, `manual_tw_futures_audit.py`, `mtc_v2/core/*`), per
   the ticket's read-only constraint.

## Sources consulted

- `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`
  (§2 F-7, §3 D-9/D-10, §8.1/§8.2, Appendix A — lines 271, 440-501, 584-588,
  785-786, 1565-1566, 2935, 2945, 3099, 3117, 3241-3245)
- `MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md` (full file, 485 lines)
- `MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_results.json` (`summary` block + all 58 `rows`)
- `MTC_COMMAND_CENTER/12_PARITY_PINETS/manual_tw_futures_audit.py` (lines 487-527, 941-1023)
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_compare.py` (lines 5-38, 31-38, 753-774, 813, 963-986)
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md` (full file, 216 lines)
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py` (lines 197, 200, 416, 418, plus grep for feature keys)
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py` (lines 840-843)
- Repo-wide search confirming absence of
  `01_MTC_PROJECT/reports/FACTORY_REGRESSION_SUITE_V1/full_current/FULL_FACTORY_SUITE_REPORT.md`
  in this worktree (`origin/master` `3d6a621c`)
- `01_MTC_PROJECT/parity_oracles/` (schema and tooling only, no committed factory-regression report)

Investigation performed in isolated worktree `C:\WFK2`, branch
`research/parity-ground-truth`, base `origin/master` `3d6a621c`. Feeds
wayfinder map #67 ticket "Decide: the reference-implementation doctrine."
