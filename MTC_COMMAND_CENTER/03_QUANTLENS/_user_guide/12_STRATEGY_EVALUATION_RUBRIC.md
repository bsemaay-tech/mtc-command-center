# Strategy Evaluation Rubric (canonical) — SP-004

Status: **DRAFT (Phase 0A deliverable)**. Authored 2026-06-04 by Claude (Opus 4.8).
Migrated + corrected from `11_TRIAGE/_eval_pipeline_source_TEMP/` (Turkish draft).
Implements Phase 0A of [10_STRATEGY_SCORECARD_REDESIGN_PLAN.md](10_STRATEGY_SCORECARD_REDESIGN_PLAN.md).

**Owner sign-off: COMPLETE (Barış 2026-06-04).** D1-D6 resolved (see §"Owner
decisions"). Notable: D1 = Gate 1B uniform **/100 PASS≥75** (not the /50 draft);
D3 = parity is **advisory, not a hard gate** (Pine layer may be retired for direct
Python/Binance execution). Final numeric bands (D5) still set in Phase 1.5 from real
data. This unblocks Phase 2 scoring lock.

This document is the **source of truth** the scoring engine (Phase 2,
`presentation_reader`) and the artifact writers (Phase 1) implement against. It is
spec only — no code, no Pine/MTC/parity change.

---

## Design principles

1. **Separate gates, never one number.** Four scored gates + hard-fail flags.
   Never recollapse to a single composite. The old `build_scorecard()` flat 100
   blend is the defect this replaces (it scored funnel position, not edge).
2. **A gate is N/A until its phase data exists.** No Gate 2 score before a
   backtest artifact; no Gate 3 score before an integration/readiness artifact.
   The UI shows "not evaluated", never a fake number.
3. **Status envelope on every metric.** Each metric =
   `{value, status, reason, source_path}` (`status_envelope.schema.json`). Only
   `status==OK` scores. `N_A | NOT_COMPUTED | INSUFFICIENT_DATA |
   INSUFFICIENT_TRADES | TOOL_FAILED` grey the sub-criterion and block the gate
   from reaching pass — they are **never** auto-zeroed or auto-failed. A failed
   CPCV/PBO tool is `TOOL_FAILED`, not a 0.
4. **Hard-fail gates are kill switches.** `REJECT_REPAINT` zeroes everything
   downstream. `PBO>=0.5` marks Gate 2 `OVERFIT_SUSPECT` and blocks promotion (but
   keeps the idea — not archived). **Parity is advisory, not a kill switch** (D3):
   a mismatch raises `PARITY_WARNING` for later review but does NOT block promotion
   — the Pine layer may be retired for direct Python/Binance execution.
5. **Every sub-criterion maps to an emittable field.** No criterion is scored
   from human vibes at runtime. Gate 1 / 1B read existing row/audit/source
   fields; Gate 2 reads `evaluation_artifact_v1`; Gate 3 reads
   `production_readiness_artifact_v1`.

Min-pass: each gate **75/100** (Gate 1B also **75/100**, uniform — D1 signed off).

---

## Owner decisions (resolved in this draft as recommendations)

| # | Decision | Resolved value (Barış 2026-06-04) | Status |
|---|---|---|---|
| D1 | Gate 1B scoring mode | **/100, PASS ≥75** — uniform with Gates 1/2/3 (CONDITIONAL 60–74, FAIL <60). *(Changed from /50 draft.)* | ✅ SIGNED |
| D2 | PBO ≥0.5 policy | **Gate 2 `OVERFIT_SUSPECT`, blocks promotion, keeps idea** (not reject) | ✅ SIGNED |
| D3 | Parity | **Advisory, NOT a hard gate.** Mismatch → `PARITY_WARNING` + revisit note; does NOT block promotion. Pure-Python strategies → `N_A`. *(Rationale: Pine may be retired for direct Python/Binance execution.)* | ✅ SIGNED |
| D4 | Gate 3 source | **Separate `production_readiness_artifact_v1`**; Gate 3 N/A until it exists | ✅ SIGNED |
| D5 | Final numeric bands | **Set in Phase 1.5 from observed distributions** — bands in §Gate 2 are provisional anchors only | ⏳ DEFERRED (confirmed) |
| D6 | English thesis title | AI-drafted per strategy, Barış may override | ✅ SIGNED |

---

## Gate 1 — Candidate Intake / 100

Question: *Is this worth coding and backtesting?* No performance scored here (no
backtest yet). Reads source/transcript/audit fields.

| # | Category | Pts |
|---|---|--:|
| 1.1 | Rule clarity & determinism | 25 |
| 1.2 | Algorithmic codability | 20 |
| 1.3 | Preliminary repaint / lookahead risk | 15 |
| 1.4 | Trade lifecycle definition | 15 |
| 1.5 | Data & backtest feasibility | 10 |
| 1.6 | Execution realism (preliminary) | 10 |
| 1.7 | Strategy edge hypothesis | 5 |
| | **Total** | **100** |

Field mapping (source = `01_candidate_metadata.yaml` / `producer_spec.json` /
audit row):

| Sub-criterion | Pts | Source field / rule |
|---|--:|---|
| 1.1 Entry rule explicit | 6 | `producer_spec.entry_pseudo` non-empty & deterministic |
| 1.1 Exit approach explicit | 5 | `exit_pseudo` non-empty OR `mtc_exit_delegated=true` |
| 1.1 long/short/flat defined | 4 | `direction` + `strategy_type` set |
| 1.1 same-bar collision rule | 4 | `opposite_signal_behavior` present |
| 1.1 parameters explicit | 3 | `rules_high_confidence` enumerate numeric params |
| 1.1 no human interpretation | 3 | `has_deterministic_rules=true` (audit) |
| 1.2 writable in Pine/Python | 5 | `codable=true` / not flagged `manual_visual` |
| 1.2 no manual trendline/eyeball | 5 | classification not `MANUAL_VISUAL_REVIEW_ONLY` |
| 1.2 all inputs numeric/boolean | 4 | derived from rules_high_confidence types |
| 1.2 modelable as state machine | 3 | `state_machine_definable` flag (Phase 0A: add to spec) |
| 1.2 TV==Python logic reproducible | 3 | not flagged closed-source/proprietary |
| 1.3 signal from closed bar only | 4 | `preliminary_repaint_class` ∈ {LOW_RISK} → 4 |
| 1.3 low future-bar risk | 4 | repaint class (LOW=4, MEDIUM=2, HIGH=0) |
| 1.3 HTF lookahead manageable | 3 | `uses_htf` + `htf_safe` flags |
| 1.3 no risky pivot/fractal/zigzag | 2 | `risky_structure=false` |
| 1.3 realtime≈backtest likely | 2 | repaint class derived |
| 1.4 entry signal clear | 3 | `entry_pseudo` present |
| 1.4 logical exit OR delegated clear | 3 | `exit_pseudo` OR `mtc_exit_delegated` |
| 1.4 opposite-signal behavior clear | 3 | `opposite_signal_behavior` |
| 1.4 re-entry/cooldown/pyramiding clear | 2 | `reentry_policy` |
| 1.4 flat/long/short state clear | 2 | `state_model` |
| 1.4 backtest exit model chosen | 2 | `backtest_exit_model` |
| 1.5 required data available | 3 | `data_check.verify_actual_range` OK |
| 1.5 granularity available | 2 | timeframe in available set |
| 1.5 indicators computable on history | 2 | not future-dependent |
| 1.5 cost model addable | 2 | always true for OHLCV (1) + fee config (1) |
| 1.5 enough trade potential | 1 | heuristic from rule frequency |
| 1.6 order type clear | 2 | `order_type` |
| 1.6 entry timing clear | 2 | `signal_timing` |
| 1.6 spread/slippage estimable | 2 | liquid symbol set |
| 1.6 no anti-liquidity assumption | 1 | manual flag |
| 1.6 intrabar uncertainty manageable | 1 | repaint class |
| 1.6 no extreme latency dependence | 2 | `latency_sensitive=false` |
| 1.7 sensible market hypothesis | 3 | `strategy_thesis_en` present |
| 1.7 expected regime stated | 2 | `expected_regime` present |

Bands (decision thresholds): 85–100 strong · 75–84 good · 60–74 doubtful ·
40–59 weak · 0–39 reject. **Min pass 75.**

**Gate 1 hard-fail** (any one ⇒ fail): uncodable · requires human interpretation ·
entry rule undefined · trade lifecycle undefined · explicit repaint/lookahead ·
no data for testing · signal bar undefined · purely visual. Each recorded in
`gate_1_hard_fail` + reason.

---

## Gate 1B — MTC Feasibility / 100 (PASS ≥75)  [D1 — SIGNED OFF: uniform /100]

Question: *Can this be represented in MTC_v2 at a basic level?* Coarse yes/no-ish
feasibility — **not** the production-grade contract (that is Gate 3 §6.1).

**Boundary vs Gate 3 (de-dup, audit AUDIT fix):**
- **Gate 1B** = "representable *at all*?" — coarse, pre-backtest, cheap.
- **Gate 3 §6.1** = "production-*grade* contract?" — precise timing, collision,
  unique id, metadata, post-integration.
- A strategy can pass Gate 1B (representable) yet score low Gate 3 (contract not
  production-ready). They are different questions at different phases → no double
  counting.

| Criterion | Pts | Source field |
|---|--:|---|
| Signal reducible to long/short/close/flat | 20 | `signal_reducible` |
| Entry-only vs full strategy clear | 16 | `strategy_type` |
| No conflict with MTC risk engine | 20 | `risk_engine_conflict=false` |
| Convertible to alert format | 16 | `alert_convertible` |
| Modelable as state machine | 16 | `state_machine_definable` |
| Adaptable to MTC standard params | 12 | `mtc_param_mappable` |
| **Total** | **100** | |

Derived verdict (D1 — uniform with all gates): **≥75 PASS · 60–74 CONDITIONAL (fix
spec gaps first) · <60 FAIL (no backtest).** The Final Decision Matrix Gate 1B
column uses this derived verdict.

**Gate 1B hard-fail:** needs manual decision · signal format undefined · conflicts
with risk engine · state untrackable · no alert producible.

---

## Hard gate — Repaint / Lookahead verification

Code-level verification of the Gate 1.3 preliminary read. Result class drives
downstream:

| Result | Effect |
|---|---|
| `VERIFIED_SAFE` | proceed, no penalty |
| `SAFE_WITH_DELAY` | proceed, **−3 penalty in Gate 2 §5.5** (delayed-fill realism) |
| `NEEDS_MODIFICATION` | **block Gate 2**, return to prototype (NOT rejected) |
| `REJECT_REPAINT` | **hard fail — zeroes all downstream gates**, status REJECTED |

Stored in `evaluation_artifact_v1.hard_flags.repaint_status`. Until verified:
`NOT_VERIFIED` ⇒ Gate 2 may compute but promotion blocked.

---

## Soft gate — Pine⇄Python parity (advisory)  [D3 — SIGNED OFF: advisory, not hard-block]

Parity checks whether the Pine and Python implementations produce matching signals
on the same data. **Barış decision (2026-06-04): advisory, NOT a hard kill-switch.**
Rationale: the Pine layer may be retired in favor of running the strategy directly
from Python via the Binance API, so parity must not block a strategy that may never
ship as Pine.

| `parity_status` | Effect |
|---|---|
| `PASS` | Pine == Python confirmed; no flag |
| `WARN` (was `FAIL`) | mismatch recorded as `PARITY_WARNING` + "revisit later" note; **does NOT block promotion** |
| `N_A` | no Pine counterpart (pure-Python strategy) or not yet run — no penalty |

Source: `PINETS_PARITY_RESULT.json` verdict → `flags.parity_status` (advisory). A
`WARN` surfaces in the UI as a caution badge and is queued for later review; it
never zeroes a gate or blocks forward testing. **Schema note (Phase 1):** move this
field out of `hard_flags` into an advisory `flags` block in
`evaluation_artifact_v1.schema.json`.

---

## Gate 2 — Backtest Evidence / 100  (reads `evaluation_artifact_v1`)

Question: *Does the backtest show real, risk-adjusted, robust, benchmark-beating
edge?* **Rebalanced** from the source draft: Regime 5→10, Performance 20→18,
Trade-sample 15→12 (keeps /100); robustness made metric-driven (Sharpe, Sortino,
recovery, WFO, CPCV, PBO added — all absent from the source draft).

| # | Category | Pts |
|---|---|--:|
| 5.1 | Performance quality | 18 |
| 5.2 | Risk / drawdown behavior | 20 |
| 5.3 | Trade sample quality | 12 |
| 5.4 | Robustness / overfitting | 20 |
| 5.5 | Cost-after realism | 10 |
| 5.6 | Benchmark comparison | 10 |
| 5.7 | Regime analysis | 10 |
| | **Total** | **100** |

Field mapping (all from `evaluation_artifact_v1`, status envelope, only OK scores):

**5.1 Performance — 18**
| Sub | Pts | metric |
|---|--:|---|
| Net profit positive & material | 3 | `net_profit_pct` / `return_pct_compound` |
| Profit factor strong | 4 | `profit_factor` |
| Expectancy positive | 3 | `expectancy_r` |
| Sharpe acceptable | 3 | `sharpe` *(NEW)* |
| Sortino acceptable | 2 | `sortino` *(NEW)* |
| Equity curve healthy | 3 | `equity_curve_health` |

**5.2 Risk / drawdown — 20**
| Max drawdown acceptable | 5 | `max_drawdown_pct` |
| Recovery factor | 4 | `recovery_factor` *(NEW)* |
| Consecutive losses reasonable | 3 | `max_consecutive_losses` |
| Return / MaxDD ratio | 4 | `ret_dd_ratio` *(NEW)* |
| No single period wipes account | 4 | `worst_window_drawdown_pct` |

**5.3 Trade sample — 12** (minimums by `strategy_type`, table below)
| Trade count adequate | 4 | `trades` vs type-min |
| Test duration adequate | 3 | `calendar_days` vs type-min |
| Multiple regimes covered | 2 | `regime_coverage_count` |
| Not few-big-trade dependent | 2 | `top_trade_concentration` |
| Long/short balance not extreme | 1 | `long_short_ratio` |

**5.4 Robustness / overfitting — 20**
| Parameter stability | 4 | `param_stability_score` |
| OOS doesn't collapse | 3 | `oos_return_pct` |
| Walk-forward verdict | 3 | `wfo_pass` *(NEW, robust ≥ ceil(folds/2))* |
| CPCV verdict | 4 | `cpcv_pass_ratio` *(NEW)* |
| PBO (overfit prob) | 4 | `pbo` *(NEW; ≥0.5 ⇒ OVERFIT_SUSPECT)* |
| Works across periods | 2 | `multi_window_pass` |

**5.5 Cost-after realism — 10** (apply −3 here if `SAFE_WITH_DELAY`)
| Survives commission | 3 | `net_after_fees_pct` |
| Survives slippage | 3 | `net_after_slippage_pct` |
| Spread doesn't kill | 2 | derived |
| Avg trade large vs costs | 2 | `avg_trade_vs_cost` |

**5.6 Benchmark — 10** (B&H same symbol/TF/window/fee; risk-adjusted)
| Better risk-adjusted vs B&H | 3 | `benchmark.beats_bh_risk_adjusted` / `excess_alpha_pct` |
| MaxDD meaningfully < B&H | 2 | `max_drawdown_pct` vs `bh_max_drawdown_pct` |
| Return/MaxDD better than B&H | 2 | `ret_dd_ratio` vs `bh_ret_dd_ratio` |
| Similar/better return, lower exposure | 2 | exposure-adjusted |
| Beats simple EMA benchmark | 1 | `benchmark.beats_ema_benchmark` |

**5.7 Regime — 10** *(raised 5→10)*
| Trend/range/high-vol/low-vol split done | 4 | `regime.regime_breakdown_present` |
| Weak regime known | 3 | `regime.weak_regime_identified` |
| No catastrophic regime | 3 | `regime.worst_regime_return_pct` *(NEW)* |

**Provisional bands [D5 — finalize Phase 1.5]:**

| metric | 5 | 3 | 1 | 0 |
|---|---|---|---|---|
| Max drawdown | <15% | <25% | <40% | ≥40% |
| Sharpe | >1.5 | >1.0 | >0.5 | ≤0.5 |
| Sortino | >2.0 | >1.3 | >0.7 | ≤0.7 |
| Profit factor | >1.8 | >1.4 | >1.1 | ≤1.1 |
| Recovery factor | >3 | >2 | >1 | ≤1 |
| Return / MaxDD | >3 | >2 | >1 | ≤1 |
| PBO | <0.2 | <0.35 | <0.5 | ≥0.5 → OVERFIT_SUSPECT |

Trade-count / duration minimums (§5.3):

| Type | Min duration | Min trades |
|---|---|--:|
| Scalping | 6–12 mo | 1000+ |
| Intraday | 1 yr | 300+ |
| Swing | 3 yr | 100+ |
| Position | 5 yr | 30–50+ |

Bands: 85–100 strong · 75–84 good · 60–74 weak-but-improvable · 40–59 insufficient
· 0–39 reject. **Min pass 75.**

**Gate 2 hard-fail:** negative after fees/slippage · no meaningful edge vs B&H ·
OOS fully collapses · breaks on small param change · unacceptable max DD · too few
trades for type · too short for type · profit from a few big trades · equity rose
in a single market period only · `PBO>=0.5` (→ OVERFIT_SUSPECT, blocks promotion).

---

## Gate 3 — MTC Production Readiness / 100  (reads `production_readiness_artifact_v1`)  [D4]

Question: *Can this run safely, observably, and inside the MTC_v2 automation
pipeline?* **Stays N/A until `production_readiness_artifact_v1` exists** — backtest
output cannot supply alert/state/risk/monitoring evidence. The scorecard must say
"not evaluated until integration", never invent a number.

| # | Category | Pts | artifact group |
|---|---|--:|---|
| 6.1 | Signal contract (production-grade) | 25 | `signal_contract` |
| 6.2 | Alert / execution adapter | 20 | `alert_adapter` |
| 6.3 | State synchronization | 15 | `state_sync` |
| 6.4 | MTC risk-engine compatibility | 15 | `risk_engine_compat` |
| 6.5 | Monitoring / logging / debug | 10 | `monitoring` |
| 6.6 | Fail-safe / operational safety | 10 | `fail_safe` |
| 6.7 | Versioning / reproducibility | 5 | `reproducibility` |
| | **Total** | **100** | |

Sub-criteria + per-field mapping enumerated in
`production_readiness_artifact_v1.schema.json` (one envelope per item). Bands:
85–100 strong · 75–84 minor adapter gaps · 60–74 clarify contract/adapter first ·
40–59 high integration risk · 0–39 do not run in MTC_v2. **Min pass 75.**

**Gate 3 hard-fail:** unreliable alert · no duplicate-signal guard · broker/strategy
state can't match · exit/reduceOnly ambiguous · no signal contract · insufficient
debug metadata · no fail-safe · conflicts with risk engine.

---

## Final Decision Matrix (synced to D1 Gate 1B verdict)

Parity column is **advisory only** (D3): `PASS`/`WARN`/`N_A` never change the
Decision; a `WARN` just attaches a `PARITY_WARNING` badge for later review.

| Gate 1 | Gate 1B | Repaint | Parity (advisory) | Gate 2 | Gate 3 | Decision |
|--:|---|---|---|--:|--:|---|
| 75+ | PASS (≥75) | SAFE | PASS/WARN/N_A | 75+ | 75+ | Forward test / paper trade |
| 85+ | PASS | SAFE | PASS/WARN/N_A | 85+ | 85+ | Strong — controlled forward test |
| 75+ | PASS | SAFE | PASS/WARN/N_A | 75+ | <75 / N_A | Good strategy; MTC integration incomplete |
| 75+ | PASS | SAFE | any | <75 | — | Weak backtest; not promoted |
| 75+ | PASS | any | any | 75+ (PBO≥0.5) | — | OVERFIT_SUSPECT — promotion blocked, idea kept |
| 75+ | CONDITIONAL (60–74) | — | — | — | — | Improve spec before backtest |
| 75+ | FAIL (<60) | — | — | — | — | Not MTC-feasible; no backtest |
| <75 | — | — | — | — | — | Weak candidate for coding/backtest |
| any | any | REJECT_REPAINT | — | — | — | REJECTED (everything zeroed) |
| any | any | any | WARN | promoted | — | promotion proceeds; `PARITY_WARNING` noted for later review |

---

## Strategy status labels

`IDEA → SPEC_DRAFT → SPEC_READY → BACKTEST_READY → PROTOTYPE_CODED →
REPAINT_VERIFIED → BACKTEST_PASSED → PARITY_VERIFIED → MTC_READY → FORWARD_TEST`.
Off-ramps: `REJECTED` (any hard-fail), `ARCHIVED` (low-priority but kept),
`OVERFIT_SUSPECT` (Gate 2 PBO block).

---

## Schemas (Phase 0A)

- `06_SCHEMAS/status_envelope.schema.json` — per-metric envelope.
- `06_SCHEMAS/evaluation_artifact_v1.schema.json` — Gate 2 inputs.
- `06_SCHEMAS/production_readiness_artifact_v1.schema.json` — Gate 3 inputs.
- `03_QUANTLENS/_templates/strategy_evaluation_record_template.yaml` — per-strategy record.

---

## Changes vs source draft (`_eval_pipeline_source_TEMP/`)

1. Translated to English; made every sub-criterion map to an emittable field.
2. Gate 1B set to **/100, PASS ≥75** (uniform with all gates) [D1 — signed off, changed from /50 draft]; criteria rescaled ×2; decision-matrix column synced.
3. Gate 1B vs Gate 3 §6.1 overlap **de-duplicated** with an explicit boundary note.
4. Gate 2 **rebalanced** (Regime 5→10; Perf 20→18; Sample 15→12) to stay /100.
5. Gate 2 robustness made **metric-driven**: added Sharpe, Sortino, recovery
   factor, WFO verdict, CPCV verdict, PBO (all absent from source draft).
6. Benchmark tightened to **same symbol/TF/window/fee + risk-adjusted excess_alpha
   + multi-window**.
7. **Repaint** result classes wired to effects; `SAFE_WITH_DELAY` = −3 Gate 2
   penalty; `NEEDS_MODIFICATION` = block→prototype (not reject).
8. **Parity** set as an **advisory** soft gate (`PASS`/`WARN`/`N_A`), NOT a hard pass/fail — mismatch raises `PARITY_WARNING` for later review but never blocks promotion [D3 — signed off; Pine may be retired for direct Python/Binance execution].
9. **PBO≥0.5 → OVERFIT_SUSPECT** (blocks promotion, keeps idea) [D2].
10. **Gate 3** split to its own `production_readiness_artifact_v1`; stays N/A until
    integration evidence exists [D4].
11. Record template gains `strategy_thesis_en/tr`, `gate_{1,2,3}_hard_fail` +
    reasons, `backtest_run_id`, `evaluation_artifact_version`, `phase_current`.

`_eval_pipeline_source_TEMP/` is retained as reference; deleted only in Phase 5.
