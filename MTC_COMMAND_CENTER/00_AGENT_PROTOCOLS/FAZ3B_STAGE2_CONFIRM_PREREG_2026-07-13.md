# FAZ 3B — STAGE-2 CONFIRMATION RUN PRE-REGISTRATION (BLOCKED — GATE-5 FATAL, NOT APPROVABLE)

> Status: **BLOCKED BY GATE-5 ADVERSARIAL REVIEW (2026-07-13) — this draft can NEVER
> receive D016.** Codex findings
> (`11_TRIAGE/CODEX_GATE5_FINDINGS_FAZ3B_STAGE2_2026-07-13.md`, commit `1859910c`) were
> independently verified by Fable on the raw artifacts and code the same day. The two
> unfixable-by-editing defects: (1) **all six proposed "held-out" symbols already have
> GEN_KELTNER_BREAKOUT 1h × 16-trial rows on the identical 2020-07-27→2026-06-26 window**
> in `05_BACKTEST_RESULTS/overnight_multiasset_2026-06-29/` (the June-29 sweep covered ALL
> 51 bundle symbols at Keltner 1h — no untouched 1h symbol exists in this bundle); the §3
> virginity claim relied on `RESEARCH_RUN_REGISTRY.json`, which is an incomplete ledger,
> not an evidence inventory — drafting error acknowledged by the author (Fable).
> (2) **the §6 gauntlet is not executable as written:** `cpcv_validator.py` and
> `multiwindow_oos.py` never pass `exit_mode` into `simulate_slice` (default `fixed_2R`),
> so they would silently score the wrong exit; `probabilistic_pbo.py` has no
> per-configuration return matrix. Confirmation of this family requires a NEW
> pre-registration on genuinely untouched data (pre-frozen forward window or new dataset)
> plus exit-aware gauntlet tooling under its own review. This document is retained
> unedited below as the honest record of what was proposed and why it failed review.
> No run, no smoke test, no runner-script code, no engine edit is or ever was authorized.
> Written 2026-07-13 by Claude Fable 5; Gate-5 review by Codex GPT-5; review audited and
> this banner added by Claude Fable 5.
>
> Format follows `FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md` for continuity.
> Binding parents: D013 (two-stage DSR discipline), D015 (Stage-1 approval; Stage-2
> separately gated), `FAZ3B_EXIT_SWEEP_SCOPE.md` §DSR discipline, Stage-1 report
> `03_QUANTLENS/research/faz3b_stage1_20260705/STAGE1_REPORT.md`,
> standard `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md`.

## 1. Motivation — Stage-1 evidence (verified from result JSONs, not from the report)

Stage-1 (980 jobs, D015, 2026-07-05) confirmed H1 at discovery tier: 3 new-exit-mode
cells reached `research_robust` (union-adjusted DSR ≥ 0.50 ∧ trades ≥ 30) where the same
cell at `fixed_2R` did not. Exactly ONE is clean:

| Cell | Result (re-read 2026-07-13 from `pass2_1h/MEGA_walk_forward_results.json`) |
|---|---|
| GEN_KELTNER_BREAKOUT × AAPL × 1h × trail_ema8 | classification **STRONG_PASS**, best_params `{ema_len: 50, atr_len: 10, mult: 2.0}`, lockbox OOS net **+19.04%** (net after slippage +16.74%), 49 trades, PF 1.87, maxDD −6.83%, sharpe_pt 0.1937, engine dsr_p 0.6201 (diagnostic), **union-adjusted DSR 0.581** (report method), trial_count 5 (stride 3), boot_p 0.164, bh_fdr_survivor false, robust_final false |
| Same cell at fixed_2R | INSUFFICIENT_TRADES (25 trades), engine dsr_p 0.6222 — not research_robust |

Known confound (Stage-1 report, "Honest confound"): the first-ever 1h fixed_2R baseline
pass itself produced 3 research_robust STRONG_PASS cells (KELTNER/SPY du 0.685,
KELTNER/QQQ du 0.599, MACD_BULL_CROSS/QQQ du 0.617). Part of the Stage-1 signal is
therefore **the 1h timeframe, not the exit knob**. Stage-2 must distinguish "trail_ema8
adds value" from "KELTNER-1h pocket".

Excluded from Stage-2 (per Stage-1 report §What-next item 2): the two FAIL-classified H1
cells (KELTNER/AMZN/trail_ema8, STOCH/AAPL/opposite_channel). They may only enter a
future pre-reg after their fold-criteria misses are explained in writing and Barış
accepts. This document does not cover them.

## 2. Pre-registered hypotheses

Stage-2 is a CONFIRMATION run. It asks one question on data the candidate family has
never touched, with `robust_final` (DSR ≥ 0.95 ∧ BH-FDR ∧ PASS) judged here and only
here (D013).

- **H1 (exit is incremental):** on held-out symbols at 1h, GEN_KELTNER_BREAKOUT with
  `trail_ema8` on the pre-registered narrow grid clears the full `robust_final` bar
  (§6) on ≥1 decision cell where `fixed_2R` on the SAME narrow grid at the same cell
  does not (or trails it by the §7 margin).
- **H0 (accept and close the family):** no decision cell clears `robust_final` at
  trail_ema8 → the Stage-1 AAPL result does not generalize; the family stays research
  at best (§10 outcomes C/D) and gets no third run on this data.
- **H_confound (pocket, not exit):** decision cells clear `robust_final` at BOTH exit
  modes with margin < 0.10 → the KELTNER-1h pocket is real but the exit knob is not
  incremental; the Faz 3b exit hypothesis concludes negative-incremental (§10 outcome B).

## 3. Scope — every axis fixed BEFORE the run

| Axis | Value | Justification |
|---|---|---|
| Strategy (1) | GEN_KELTNER_BREAKOUT only | the sole clean STRONG_PASS Stage-1 H1 family; adding others = discovery, not confirmation |
| Timeframe (1) | 1h only | H1 confirmed at 1h; H0 held at 10m (zero research_robust in any mode) — re-running 10m would be a third bite; other TFs would be new discovery |
| Exit modes (2) | `trail_ema8` (candidate, FROZEN per D013) + `fixed_2R` (confound control ONLY, not a candidate) | fixed_2R on the identical narrow grid at every cell is the only way to measure the exit's incremental value on held-out data |
| Symbols (6 held-out + 1 reference) | **Held-out/decision: GOOGL, META, AMD, NFLX** (stocks — same asset class as AAPL) **+ DIA, IWM** (index ETFs — tests whether the SPY/QQQ pocket generalizes) · **Reference (non-evidence): AAPL** | none of the 6 appeared in the 6yr US-equities 10m sweep, Stage-1, or any registered GEN_KELTNER run — verified against `RESEARCH_RUN_REGISTRY.json` 2026-07-13 and re-verified pre-launch (§9 step 0). AAPL runs only as a continuity reference row and is **never confirmation evidence** |
| Bundle | `native_multiasset_alpaca_2026-06-28` via `MEGA_BUNDLE_MANIFEST` | canonical primary bundle. All 6 held-out symbols verified in the manifest 2026-07-13 at 1h: 8,852–8,884 bars each, `ohlcv_validation_status: PASS`, 2020-07-27 → 2026-06-26 — same window as Stage-1 cells |
| Grid | 12-config narrow grid (§4), stride 1 (no `MEGA_GRID_STRIDE`) | D013: winner ± 1 neighbor, exact sets enumerated below |

**Decision cells (fixed now):** the 6 held-out symbols × 1h × trail_ema8 = **6 decision
cells**. Only these can confirm H1. The 6 fixed_2R twins exist for the §7 confound rule.
The 2 AAPL rows are reference only. Held-out honesty note: option (b) "same symbols,
untouched timeframe (30m/2h)" was considered and REJECTED as primary evidence — same
underlying price paths as Stage-1 cells; weaker independence. Option (a) new symbols,
same class, same TF is the design.

## 4. Narrow grid — literal parameter sets (D013: winner ± 1 neighbor, no new values)

Stage-1 winner (extracted from `pass2_1h/MEGA_walk_forward_results.json`
`summary.best_params`, not from the report): `{ema_len: 50, atr_len: 10, mult: 2.0}`.
Original GRIDS axes (engine `grid_keltner_breakout()`): ema_len ∈ (20, 50) · atr_len ∈
(10, 20) · mult ∈ (1.5, 2.0, 2.5, 3.0). Winner ± 1 axis-step per knob, values taken from
the ORIGINAL axes only:

- ema_len 50 → {20, 50} (50 is the axis edge; the 2-value axis makes ±1 = whole axis)
- atr_len 10 → {10, 20} (same: 2-value axis)
- mult 2.0 → {1.5, 2.0, 2.5} (3.0 excluded — 2 steps from winner)

Full cartesian (12 sets — cartesian chosen over a 5-point star because the Robustness
Gate requires parameter-NEIGHBORHOOD stability, which needs the cross terms):

| # | ema_len | atr_len | mult |
|---|---|---|---|
| 1 | 20 | 10 | 1.5 |
| 2 | 20 | 10 | 2.0 |
| 3 | 20 | 10 | 2.5 |
| 4 | 20 | 20 | 1.5 |
| 5 | 20 | 20 | 2.0 |
| 6 | 20 | 20 | 2.5 |
| 7 | 50 | 10 | 1.5 |
| 8 | 50 | 10 | 2.0 | ← Stage-1 winner
| 9 | 50 | 10 | 2.5 |
| 10 | 50 | 20 | 1.5 |
| 11 | 50 | 20 | 2.0 |
| 12 | 50 | 20 | 2.5 |

No formulas at run time: the runner script embeds exactly this list and asserts
`len(grid) == 12` and content equality against this table before launching.

## 5. Grid mechanism — zero engine edit

Stage-2's narrow grid is NOT added to `GRIDS` (D013: GRIDS content never edited in
place). Mechanism: a one-off runner script
`03_QUANTLENS/tools/faz3b_stage2_runner.py` (written only AFTER D016) that imports
`mega_walk_forward`, replaces `GRIDS["GEN_KELTNER_BREAKOUT"]` in memory with the 12-set
list above, then invokes the engine main with pass-through CLI args. Chosen over a
`MEGA_GRID_OVERRIDE_JSON` engine knob because it requires **zero engine edit**: the
committed engine stays byte-identical, self-parity goldens stay untouched and are NOT
re-verified or recaptured. If ANY engine edit turns out to be necessary → STOP (§9),
back to Barış; that edit would need its own self-parity `--verify` PASS and becomes part
of what is approved.

Consequence for stamping: result rows carry `exit_mode`, `engine_version
= faz3b-exit-mode-v1`, `grid_stride` absent/1, and `trial_count == 12`; the runner
prints the injected grid into the run notes. Engine within-run `dsr_p_value` will use
`grid_n = 12` after the monkeypatch — it remains a DIAGNOSTIC only (§6).

## 6. Pre-registered metrics and gates

All gates below are the engine's existing ones — no threshold is changed by this doc.

- **MIN_TRADES:** ≥ 30 lockbox trades (`MIN_TRADES_FOR_PASS = 30`), else
  `INSUFFICIENT_TRADES`, never PASS.
- **Classification:** engine fold logic unchanged; decision requires ∈ {PASS, STRONG_PASS}.
- **Buy & hold baseline:** every row's `summary.buy_hold_lockbox` (produced as today);
  decision cells must show **positive excess alpha vs buy & hold over the identical
  lockbox window**. A cell that clears DSR but loses to buy & hold is
  `BETA_DISGUISED_AS_ALPHA` and does NOT confirm (Benchmark Gate).
- **BH-FDR:** engine within-run Benjamini-Hochberg at **Q = 0.10** over the run's
  bootstrap p-values (family = all 14 rows with valid `boot_p_value`); decision requires
  `bh_fdr_survivor = true`.
- **DSR:** decision uses **union-adjusted DSR ≥ 0.95** computed at report level with the
  §8 trial family (N = 219), same recompute method as the Stage-1 report ("DSR method
  note": inputs `summary.lockbox_oos.sharpe_pt`, `num_trades`,
  `summary.best_train_sharpe_pt`; sr_std pooled across the family's KELTNER rows from
  Stage-1 pass1 + pass2 + Stage-2). Engine `dsr_p_value` (grid_n = 12 post-monkeypatch)
  is a diagnostic and is reported but never decides.
- **Stage-2 `robust_final` decision bar per cell:** classification PASS/STRONG_PASS ∧
  trades ≥ 30 ∧ `bh_fdr_survivor` ∧ union-DSR ≥ 0.95 ∧ excess alpha > 0.
  The engine-emitted `robust_final` field (within-run DSR N=12) remains an unmodified
  diagnostic field; the report must preserve it and separately label this union-adjusted
  Stage-2 decision.
- **Post-confirmation gauntlet (only if ≥1 decision cell clears the bar; thresholds
  fixed NOW):** on each confirming cell — **CPCV** (per rules-doc CPCV Gate: report
  group count, combinations, purge/embargo, minimum return, and trade-count failures;
  required: median OOS return > 0 ∧ pass rate **≥ 70%**, matching the existing
  forward-paper queue threshold); **PBO** via CSCV with `--max-combinations 100000`
  (D008), required **PBO <
  0.5** (D007: PBO ≥ 0.5 = OVERFIT_SUSPECT, blocks promotion); **multi-window** OOS
  stability (`multiwindow_oos.py` standard Q1/Q2/Q3/Q4/H2 windows, required: positive
  OOS in ≥3/5 windows with ≥15 trades in each positive window) plus parameter-neighborhood
  stability (≥70% of one-step neighbors retain positive lockbox return). Any gauntlet
  failure downgrades the outcome to §10 row C — no
  re-argument.

## 7. Confound control — exact decision rule

Every cell runs BOTH modes on the identical 12-set grid. Per decision cell, with
`bar(mode)` = the full robust_final bar of §6 and `du(mode)` = union-adjusted DSR:

- **EXIT-INCREMENTAL** ⇔ `bar(trail_ema8)` ∧ [ ¬`bar(fixed_2R)` ∨ (`bar(fixed_2R)` ∧
  `du(trail_ema8) ≥ du(fixed_2R) + 0.10`) ].
- **POCKET-ONLY** ⇔ `bar(trail_ema8)` ∧ `bar(fixed_2R)` ∧ `du(trail_ema8) <
  du(fixed_2R) + 0.10`.
- **BASE-ONLY** ⇔ ¬`bar(trail_ema8)` ∧ `bar(fixed_2R)` (exit hypothesis dead; base
  pocket noted).
- **NEITHER** ⇔ neither mode clears the bar.

The margin 0.10 is fixed now and will not be tuned after seeing results.

## 8. Trial accounting (A17) — union family fixed before the run

Rows: 1 strategy × 7 symbols × 1 TF × 2 modes = **14 result rows**. Trials: 14 × 12
configs = **168 Stage-2 trials** (144 on decision+twin cells, 24 on AAPL reference —
reference trials still COUNT in the family).

Union family for every Stage-2 union-adjusted DSR (per D013/A17, method identical to
Stage-1 report):

| Component | Trials |
|---|---|
| Historical 10m fixed_2R full grid (6yr sweep, GEN_KELTNER_BREAKOUT, 16 configs) | 16 |
| Stage-1 10m, 3 new modes × floor(16/3)=5 | 15 |
| Stage-1 1h, 4 modes × 5 | 20 |
| Stage-2, all rows incl. reference (14 × 12) | 168 |
| **N_union per evaluated cell** | **219** |

Including ALL Stage-2 trials in the family means the "≥1 of 6 decision cells" selection
in §10 is already paid for in the deflation — no post-hoc cell cherry-picking is
possible. Within-run engine DSR (N = 12) is diagnostic-only, labeled as such in the
report.

## 9. Execution plan (AFTER D016 only) + STOP rules

Order: **0. pre-launch verification → 1. runner script + grid assert → 2. smoke (1
cell) → 3. full run → 4. report.**

0. **Pre-launch verification (STOP gate):** (a) re-verify the 6 held-out symbols exist
   at 1h in the manifest with PASS status; (b) scan `05_BACKTEST_RESULTS/` +
   `03_QUANTLENS/research/` result JSONs + `RESEARCH_RUN_REGISTRY.json` for ANY prior
   GEN_KELTNER_BREAKOUT row on a held-out symbol — a hit voids that symbol (replace
   only from {SPY-family ETFs, remaining stocks in the bundle} with written note, or
   drop to 5 cells; silent substitution forbidden); (c) confirm engine worktree clean at
   the commit recorded in the run notes.
1. Runner script per §5; it must print the injected grid and hard-assert the 12 sets.
2. **Smoke (1 cell):** GOOGL × 1h × trail_ema8. Verify stamping (`exit_mode`,
   `engine_version`, `trial_count == 12`, `grid_stride` 1/absent), runtime/cell.
3. Full run:
   ```powershell
   $env:MEGA_BUNDLE_MANIFEST = "<repo>\MTC_COMMAND_CENTER\03_QUANTLENS\data\native_multiasset_alpaca_2026-06-28\manifests\dataset_manifest.json"
   $env:MEGA_EXIT_MODES     = "fixed_2R,trail_ema8"   # comma list IS correct for modes
   # NO MEGA_GRID_STRIDE (must stay unset -> stride 1)
   # --symbol is a REPEATABLE flag (append) — comma-join silently yields NO_DATA:
   python MTC_COMMAND_CENTER\03_QUANTLENS\tools\faz3b_stage2_runner.py --strategy GEN_KELTNER_BREAKOUT --symbol GOOGL --symbol META --symbol AMD --symbol NFLX --symbol DIA --symbol IWM --symbol AAPL --tf 1h
   ```
   Output: `03_QUANTLENS/research/faz3b_stage2_<timestamp>/`; register in
   `RESEARCH_RUN_REGISTRY.json`; morning report per rules-doc §10 standard.
4. Report includes: per-cell both-mode table, union-DSR arithmetic shown, buy&hold +
   excess alpha per cell, §7 rule applied mechanically, §10 outcome row cited.

**STOP rules (Stage-1 set carried over + Stage-2 additions).** Any hit = STOP, partial
output to triage, relaunch needs fresh approval:

- Row count ≠ 14 (unless every gap is an explained NO_DATA/SKIPPED_RULE row).
- Missing/incorrect stamping; `grid_stride` present ≠ 1; `trial_count` ≠ 12 on any
  computed row; runner grid assert fails.
- Any `SKIPPED_NA_EXIT_MODE` > 0 (ema_8 exists everywhere; expected exactly 0).
- ANY engine-file edit needed → STOP, back to approval (self-parity gate applies).
- Data overlap: any Stage-2 decision cell whose **same symbol + timeframe observation
  series** appeared in a Stage-1 evidence cell is VOID. Shared calendar timestamps across
  different symbols do not constitute overlap. AAPL is by construction reference-only,
  never evidence.
- Run crashes twice at same checkpoint; supervisor heartbeat stale > 30 min without
  checkpoint progress; wall-clock > smoke-extrapolated cap × 1.5; disk < 10 GB at
  launch or < 5 GB during; any unexplained ERROR row.
- **Partial results are NEVER evidence in any direction.**

## 10. Decision table — every outcome pre-mapped to an action

| # | Outcome (mechanical, from §7 per decision cell) | Action |
|---|---|---|
| A | ≥1 decision cell EXIT-INCREMENTAL ∧ that cell passes the §6 gauntlet (CPCV ∧ PBO<0.5 ∧ multi-window) | `robust_final` confirmed → propose **FORWARD_PAPER queue** entry to Barış (separate human gate; production phased per standing decisions: Pine-parity + dry-run first — NOT live, NOT auto-promoted). Faz 3b exit hypothesis: CONFIRMED. |
| A′ | ≥1 EXIT-INCREMENTAL cell but gauntlet fails on every such cell | downgrade to row C treatment; gauntlet failure documented; no re-run of the gauntlet with tweaked settings. |
| B | ≥1 decision cell POCKET-ONLY (and no cell EXIT-INCREMENTAL) | KELTNER-1h base pocket confirmed on held-out; **exit hypothesis concludes NEGATIVE-incremental**. The fixed_2R base result may be handed to Barış for a SEPARATE decision (own gauntlet + own pre-reg if pursued); nothing auto-continues. |
| B′ | ≥1 decision cell BASE-ONLY (fixed_2R clears, trail doesn't) | exit hypothesis DEAD; same handling as B for the base pocket. |
| C | no cell clears `robust_final`, but ≥1 decision cell research_robust at trail_ema8 (union-DSR ≥ 0.50 ∧ trades ≥ 30) | family stays RESEARCH; recorded honestly; **no third run of this family without genuinely new data** (new symbols/window), and that would need a new pre-reg. |
| D | zero decision cells research_robust at trail_ema8 | family DEAD. Stage-1 AAPL result recorded as non-generalizing (selection artifact / pocket). Faz 3b concludes NEGATIVE; write the negative result in the registry + handoff. |
| E | any STOP rule fired | run VOID, zero evidentiary weight either way; triage; relaunch only via new approval. |

Ambiguity resolution: if cells land in different rows, precedence A > A′ > B > B′ (a
single EXIT-INCREMENTAL cell decides A/A′ regardless of other cells' pocket results);
C/D apply only when no cell reached any §7 positive category.

## 11. What Stage-2 will NOT claim

- No live or paper trading authorization — outcome A only puts a PROPOSAL in front of
  Barış; FORWARD_PAPER is itself a separate human gate (`LIVE_TRADING_GATE.md`).
- Nothing about other strategies, other exit modes, other timeframes (incl. 10m — H0
  stands there), other asset classes, or crypto.
- No claim from the AAPL reference rows, ever.
- `robust_final` ≠ proven live edge — it is the promotable-tier label, nothing more.
- No GRIDS change, no gate/threshold change, no engine behavior change, no Pine/parity/
  MTC_V2/`02_MTC_BACKTEST`/`07_ADAPTERS`/`06_SCHEMAS` work.
- The two FAIL-classified Stage-1 H1 cells remain out of scope.
- If H0/D lands: the conclusion is "this family does not generalize at these gates" —
  not "trailing exits are worthless" (one family, one TF, six symbols).

## 12. Sign-off

- [ ] Codex Gate-5 adversarial review (prompt to be written per
      `11_TRIAGE/FAZ3B_STAGE2_PREREG_PROMPT_2026-07-05.md` Step 2; report →
      `11_TRIAGE/CODEX_GATE5_REPORT_FAZ3B_STAGE2_<date>.md`); every required edit
      applied and re-listed here before approval.
- [ ] Barış written approval sentence → recorded as **D016** in
      `_AI_MEMORY/DECISIONS.md`. **NO RUN, NO RUNNER CODE before D016.**
