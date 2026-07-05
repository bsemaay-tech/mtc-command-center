# FAZ 3B — STAGE-1 DISCOVERY SWEEP PRE-REGISTRATION (DRAFT — NOT APPROVED)

> Status: **DRAFT awaiting (1) Codex Gate-5 adversarial review, (2) Barış written approval.**
> No run, no smoke test, no engine edit for the grid-stride knob is authorized until Barış
> approves this document with an explicit sentence. Per D013/D014 the sweep gate is separate
> from the (already landed) engine-diff gate.
> Engine baseline: `mega_walk_forward.py` @ `a6342810` (Faz 3b engine `cb8bf5a3` + nit fixes).

## 1. Objective + pre-registered hypotheses

The 2026-07-04 methodological-ceiling analysis identified the hardcoded exit (fixed 2R,
96-bar time stop) as the likely binding constraint on the validated-archetype universe.
Stage-1 asks ONE question, discovery-tier only:

**H1:** at least one non-default exit_mode (`fixed_3R`, `trail_ema8`, `opposite_channel`)
produces ≥1 cell reaching `research_robust` (MIN_TRADES ≥ 30 ∧ DSR ≥ 0.50) on the
US-equities subset where the same strategy at `fixed_2R` does not.

**H0 (accept and stop):** no exit mode clears `research_robust` anywhere → the exit knob was
not the binding constraint; Faz 3b concludes negative and the universe-has-no-edge conclusion
stands at these gates.

## 2. Scope (single asset class — D013 item 4)

| Axis | Value | Rationale |
|---|---|---|
| Asset class | US equities/ETF only | single-class rule; micro-price crypto symbols structurally excluded (item 2) |
| Symbols (7) | SPY, QQQ, AAPL, MSFT, NVDA, AMZN, TSLA | identical to `US_EQUITIES_10M_ALPACA_6YR_SWEEP_2026-06-28` → direct comparability with existing fixed_2R history; GEN_DONCHIAN_BREAKOUT open lead lives here |
| Timeframes | 10m, 1h | 10m = where the open lead is; 1h = one slower confirm axis |
| Bundle | `native_multiasset_alpaca_2026-06-28` (PRIMARY) via `MEGA_BUNDLE_MANIFEST` | canonical per data README |
| Strategies | all 20 in `GRIDS` | exit hypothesis is universe-wide; per-strategy cherry-picking would be post-hoc |

## 3. Exit modes + trial budget (A17 discipline — D013)

- **Swept modes: `fixed_3R`, `trail_ema8`, `opposite_channel` — three NEW modes only.**
  `fixed_2R` is NOT re-run: byte-identical history already exists (self-parity proven), so
  re-running it would only inflate trials. Baseline comparisons use the existing
  fixed_2R results for the same cells.
- **Grid trim: stride-3 subsample of each strategy's GRIDS list (indices 0, 3, 6, …).**
  Full grid = 1122 param sets → stride-3 ≈ 374. Trials/cell = 3 modes × (grid/3) ≈ 1.0× the
  current per-cell trial count. **Net: trials/cell do NOT exceed today's level.**
- **Trim mechanism (small engine addition, part of this approval):** env knob
  `MEGA_GRID_STRIDE` (int, default 1 = full grid, unset = today's behavior). Implementation
  rules: default must be byte-identical (self-parity `--verify` must PASS after the edit,
  goldens NOT recaptured); GRIDS content itself is NOT edited; stride recorded in every
  result row (`grid_stride` field, stripped by the parity harness only if added to
  `ALLOWED_NEW_KEYS` — that harness edit is included in this approval).
- **DSR accounting:** DSR is computed by the engine per cell as today. The report must
  additionally state total historical trials per cell (existing fixed_2R full-grid runs +
  this run) so nobody mistakes Stage-1 DSR for a fresh-universe number.

## 4. Evaluation tier (D013 item 3)

- Stage-1 verdicts use **`research_robust` ONLY** (MIN_TRADES ≥ 30 ∧ DSR ≥ 0.50).
- **Nothing from Stage-1 is promotable.** `robust_final` (DSR ≥ 0.95 ∧ BH-FDR ∧ PASS) is
  judged ONLY in Stage-2 on a pre-registered narrow grid (winner ± 1 neighbor, exit_mode
  frozen, held-out scope). Stage-2 requires its own written pre-registration BEFORE that run.
- Buy-and-hold benchmark rows are produced as today; no gate/threshold changes.

## 5. Micro-price exclusion (D013 item 2)

This run is equities-only, so no micro-price symbol can enter. For the record, the standing
exclusion list for pooled leaderboards (report level, quarantined-but-visible section):
SHIBUSD, DOGEUSD, and any symbol whose median close < $0.01 in the run window.

## 6. Execution plan (AFTER approval only)

1. Implement `MEGA_GRID_STRIDE` + `grid_stride` row field + harness `ALLOWED_NEW_KEYS` add;
   re-run `faz3b_self_parity.py --verify` → must PASS byte-identical; commit.
2. **Smoke test (1 cell):** GEN_DONCHIAN_BREAKOUT × SPY × 10m × trail_ema8, stride 3 —
   verify row stamping (`exit_mode`, `engine_version`, `grid_stride`), runtime/cell estimate.
3. Full run under the run-progress supervisor (`run_emitter_supervisor.py` + `run_watchdog.py`):
   ```
   $env:MEGA_BUNDLE_MANIFEST = "<repo>\MTC_COMMAND_CENTER\03_QUANTLENS\data\native_multiasset_alpaca_2026-06-28\manifests\dataset_manifest.json"
   $env:MEGA_EXIT_MODES     = "fixed_3R,trail_ema8,opposite_channel"
   $env:MEGA_GRID_STRIDE    = "3"
   python MTC_COMMAND_CENTER\03_QUANTLENS\tools\mega_walk_forward.py --symbol SPY,QQQ,AAPL,MSFT,NVDA,AMZN,TSLA --tf 10m,1h
   ```
   Jobs = 20 strat × 7 sym × 2 tf × 3 modes = **840**; checkpointed (4-tuple keys), resumable.
4. Outputs: `03_QUANTLENS/research/faz3b_stage1_<timestamp>/`; morning report per
   `07_BACKTEST_AND_OPTIMIZATION_RULES.md` standard, plus a per-exit-mode leaderboard vs the
   fixed_2R historical baseline for the same cells.

## 7. STOP rules

- Self-parity fails after the stride edit → STOP, no run.
- Smoke-test cell shows unstamped/malformed rows → STOP.
- Any `SKIPPED_NA_EXIT_MODE` on >10% of cells → STOP and investigate (should be ~0:
  `build_signals` adds `ema_8` everywhere).
- Run crashes twice at the same checkpoint → STOP, hand to triage; never hand-edit results.

## 8. What this approval does NOT cover

Stage-2 confirmation run; any GRIDS content change; any gate/threshold change; any promotion;
any crypto or multi-class run; Pine/parity/MTC_V2/`02_MTC_BACKTEST`/`07_ADAPTERS`/`06_SCHEMAS`.

## 9. Sign-off

- [ ] Codex Gate-5 adversarial review of this design (prompt: `11_TRIAGE/CODEX_GATE5_PROMPT_FAZ3B_STAGE1_2026-07-05.md`)
- [ ] Barış written approval sentence → recorded as D015 in DECISIONS.md
