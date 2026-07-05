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

- **Swept modes: `fixed_3R`, `trail_ema8`, `opposite_channel` — three NEW modes only for 10m.**
  `fixed_2R` is NOT re-run at 10m: byte-identical history already exists. Baseline
  comparability was AUDITED 2026-07-05 (see §3b): data + engine chain verified.
- **Exception — 1h cells run `fixed_2R` TOO** (4 modes at 1h): the 6yr sweep was 10m-only,
  so 1h has NO fixed_2R baseline. Cost: +140 jobs at stride-3 grid (≈ ⅓ of a historical
  full-grid pass) — accounted in the budget below.
- **Grid trim: capped floor-selector per strategy (Codex Gate-5 edit #1).** For each
  strategy take the first `floor(len(grid)/3)` entries of `grid[::3]` — exact arithmetic:
  372 configs total (vs naive `grid[::3]` = 376, which with 3 modes = 1128 = 100.53% and
  up to +2 trials on non-divisible grids like GEN_KELTNER_BREAKOUT 16→6). Capped selector:
  3 modes × 372 = **1116 new-mode trials aggregate = 99.5% of today's 1122 — strict
  non-exceedance holds per strategy and in aggregate.**
- **Trim mechanism (small engine addition, part of this approval):** env knob
  `MEGA_GRID_STRIDE` (int, default 1 = full grid, unset = today's behavior), implemented as
  the capped floor-selector above. Rules: default must be byte-identical (self-parity
  `--verify` must PASS after the edit, goldens NOT recaptured); GRIDS content itself is NOT
  edited; stride recorded in every result row (`grid_stride` field).
- **Parity-harness handling of `grid_stride` (Codex Gate-5 edit #4 — NOT a blind strip):**
  the harness must ASSERT `grid_stride == 1` (or field absent) on every default-mode row
  BEFORE canonicalization, exactly like the existing `exit_mode == fixed_2R` assertion.
  Only after that assertion may the field be stripped for byte-identity. A default-mode
  bug that silently trims the grid must fail the gate, not be stripped away.
- **DSR accounting (Codex Gate-5 edit #3 — selection-ADJUSTED, not just annotated):**
  the engine's within-run DSR (`grid_n`-based) is a DIAGNOSTIC only. **H1 acceptance uses a
  union-adjusted DSR** computed at report level with trial family =
  `historical_fixed2R_trials_per_strategy + stage1_new_trials_per_strategy` for each cell
  (report field `dsr_union_adjusted`). A cell counts as `research_robust` for H1 ONLY on
  the union-adjusted value; within-run DSR appearing ≥0.50 alone is labeled
  "screen only, not H1 acceptance". The report still states total historical trials/cell.

### 3b. Baseline comparability audit (done 2026-07-05, Claude Fable)

The "reuse fixed_2R history as baseline" claim was verified, not assumed:

- **Data identical:** all 7 symbols' 10m normalized CSVs are md5-IDENTICAL between the
  sweep's bundle (`native_us_equities_10m_alpaca_2026-06-28`) and Stage-1's bundle
  (`native_multiasset_alpaca_2026-06-28`); manifest row counts match (57,420–57,730/symbol).
- **Engine chain result-equivalent at fixed_2R:** sweep ran at `39b51db2`. Since then:
  `206bc9ff` (+12 lines, stderr warning only — no computation change), `cb8bf5a3` (Faz 3b —
  fixed_2R byte-identity PROVEN by self-parity goldens captured pre-edit), `a6342810`
  (defensive NA guard, unreachable at fixed_2R; parity re-verified PASS). GRIDS untouched
  throughout.
- **Gap found → §3 exception:** the 6yr sweep contains ZERO 1h rows; 1h fixed_2R baseline
  must be produced inside Stage-1 itself.

Jobs total: 20 strat × 7 sym × (10m × 3 modes + 1h × 4 modes) = **980** (was 840).

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
   # NOTE: --symbol is a REPEATABLE flag (argparse action="append"), NOT a comma list.
   # Pass 1 (10m, 3 new modes):
   $env:MEGA_EXIT_MODES     = "fixed_3R,trail_ema8,opposite_channel"
   $env:MEGA_GRID_STRIDE    = "3"
   python MTC_COMMAND_CENTER\03_QUANTLENS\tools\mega_walk_forward.py --symbol SPY --symbol QQQ --symbol AAPL --symbol MSFT --symbol NVDA --symbol AMZN --symbol TSLA --tf 10m
   # Pass 2 (1h, 4 modes incl. fixed_2R baseline — no 1h history exists, §3b):
   $env:MEGA_EXIT_MODES     = "fixed_2R,fixed_3R,trail_ema8,opposite_channel"
   python MTC_COMMAND_CENTER\03_QUANTLENS\tools\mega_walk_forward.py --symbol SPY --symbol QQQ --symbol AAPL --symbol MSFT --symbol NVDA --symbol AMZN --symbol TSLA --tf 1h
   ```
   Jobs = 20×7×(3 + 4) = **980**; checkpointed (4-tuple keys), resumable.
4. Outputs: `03_QUANTLENS/research/faz3b_stage1_<timestamp>/`; morning report per
   `07_BACKTEST_AND_OPTIMIZATION_RULES.md` standard, plus a per-exit-mode leaderboard vs the
   fixed_2R historical baseline for the same cells.

## 7. STOP rules (completed per Codex Gate-5 edit #5)

- Self-parity fails after the stride edit → STOP, no run.
- Smoke-test cell shows unstamped/malformed rows → STOP.
- Any `SKIPPED_NA_EXIT_MODE` on >10% of cells → STOP and investigate (should be ~0:
  `build_signals` adds `ema_8` everywhere).
- Run crashes twice at the same checkpoint → STOP, hand to triage; never hand-edit results.
- **Baseline proof missing** → STOP: before launch, the named fixed_2R baseline artifact
  (6yr-sweep result JSON) must exist and the §3b md5 data-identity table must be re-checked.
- **Row-count mismatch** → STOP: final output must contain exactly 980 rows unless every
  missing row is explained by `NO_DATA` / `SKIPPED_RULE` classification rows.
- **Stalled run** → STOP: supervisor heartbeat stale >30 min with no checkpoint progress.
- **Wall-clock cap** → STOP: smoke-test extrapolation sets the cap (est. cells × time/cell
  × 1.5 safety); run exceeding it is killed at the next checkpoint, partial output goes to
  triage.
- **Disk floor** → STOP: <10 GB free before launch, or <5 GB at any supervisor check.
- **Unexplained ERROR rows** → STOP: any worker `ERROR` classification not attributable to
  known `NO_DATA`/rule-skip causes.
- **Partial results are NEVER H1 evidence** — only a complete, row-count-verified run
  feeds the H1/H0 decision.

## 8. What this approval does NOT cover

Stage-2 confirmation run; any GRIDS content change; any gate/threshold change; any promotion;
any crypto or multi-class run; Pine/parity/MTC_V2/`02_MTC_BACKTEST`/`07_ADAPTERS`/`06_SCHEMAS`.

## 9. Sign-off

- [x] Codex Gate-5 adversarial review DONE 2026-07-05 (`11_TRIAGE/CODEX_GATE5_REPORT_FAZ3B_STAGE1_2026-07-05.md`):
      Verdict A (nit-fix `a6342810`) = PASS WITH NITS — A-nit closed by same-bar SHORT
      stop-priority test (11/11 green). Verdict B = APPROVE-WITH-CHANGES — all 5 required
      edits applied in this revision (#1 capped floor-selector arithmetic, #2 1h fixed_2R
      baseline pass [independently found+fixed pre-report], #3 union-adjusted DSR for H1,
      #4 grid_stride assert-before-strip, #5 completed STOP rules).
- [ ] Barış written approval sentence → recorded as D015 in DECISIONS.md
