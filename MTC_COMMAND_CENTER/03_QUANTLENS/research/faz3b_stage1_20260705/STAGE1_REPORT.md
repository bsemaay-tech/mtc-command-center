# FAZ 3B STAGE-1 DISCOVERY SWEEP — MORNING REPORT (2026-07-05)

**Classification: RESEARCH ONLY / NOT PROMOTABLE (research_robust tier, D013/D015).**
Pre-registration: `00_AGENT_PROTOCOLS/FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md` (approved D015).
Engine: `feature/faz3b-stage1-sweep` @ `b4b11daf` (Faz3b + MEGA_GRID_STRIDE, self-parity byte-identical).
Data: `native_multiasset_alpaca_2026-06-28`, 7 symbols (SPY QQQ AAPL MSFT NVDA AMZN TSLA), 10m + 1h.

## Run integrity (STOP rules — all clear)

| Check | Result |
|---|---|
| Row count | 980/980 exactly (Pass1 10m: 420; Pass2 1h: 560) ✓ |
| Unexplained NO_DATA/ERROR | 0 — the only NO_DATA block = SWING_1H_DUAL_RSI ×21 at 10m (needs daily-RSI maps; known) + its 1h equivalents; 0 ERROR rows ✓ |
| Stamping | 100% rows carry `exit_mode` + `engine_version=faz3b-exit-mode-v1` + `grid_stride=3` ✓ |
| SKIPPED_NA_EXIT_MODE | 0 (expected ~0) ✓ |
| Runtime | Pass1 139s, Pass2 39s (well under cap) ✓ |
| Disk | 330 GB free ✓ |
| Baseline proof | 7/7 symbol 10m CSVs md5-identical to 6yr-sweep bundle (pre-reg §3b) ✓ |
| Incident | First Pass-1 launch used comma-joined `--symbol` (flag is repeatable) → 60 all-NO_DATA rows, discarded, relaunched correctly. No computed results contaminated. |

## Headline

**H1 CONFIRMED at discovery tier: 3 new-exit-mode cells reach `research_robust`
(union-adjusted DSR ≥ 0.50 ∧ trades ≥ 30) where the SAME cell at fixed_2R does not.**
All signal is at **1h** — 10m (where the exit-ceiling hypothesis was born) produced
**zero** research_robust cells in any mode. `robust_final` (DSR ≥ 0.95): **0 cells**, as
always.

### H1 cells (new mode robust, fixed_2R not)

| Strategy | Symbol | TF | exit_mode | union-DSR | trades | OOS net% | class | fixed_2R same-cell |
|---|---|---|---|---|---|---|---|---|
| GEN_KELTNER_BREAKOUT | AAPL | 1h | trail_ema8 | **0.581** | 49 | +19.0 | **STRONG_PASS** | du 0.595, 25 tr (INSUFF) |
| GEN_KELTNER_BREAKOUT | AMZN | 1h | trail_ema8 | 0.528 | 49 | +27.5 | FAIL | du 0.422, 18 tr (INSUFF) |
| GEN_STOCH_OVERSOLD_CROSS | AAPL | 1h | opposite_channel | 0.542 | 36 | +27.8 | FAIL | du 0.292, 36 tr (FAIL) |

Only KELTNER/AAPL/trail_ema8 is a clean STRONG_PASS; the other two carry a FAIL
classification despite positive OOS (fold/criteria misses) — weaker evidence.

### Honest confound — 1h fixed_2R itself was never swept before

The 1h baseline pass (fixed_2R, first time ever at 1h on this universe) ALSO produced 3
research_robust cells: MACD_BULL_CROSS/QQQ (du 0.617, +27.1%), KELTNER/SPY (du 0.685,
+13.2%), KELTNER/QQQ (du 0.599, +17.3%) — all STRONG_PASS. So part of the new signal is
**the 1h timeframe, not the exit knob**. The exit knob's incremental contribution is the
3 H1 cells above (different symbols than the fixed_2R robust set; KELTNER family
dominates both).

### 10m verdict

Zero research_robust in any exit mode at 10m. The 2026-06-28 conclusion stands there:
more exits did not rescue 10m. **H0 holds at 10m; H1 holds at 1h.**

## DSR method note

Engine `dsr_p_value` = within-run diagnostic (grid_n = full GRIDS len — conservative).
H1 decisions used **union-adjusted DSR** per pre-reg §3: trial family per strategy-cell =
historical fixed_2R full grid + 3×floor(n/3) new trials at 10m; 4×floor(n/3) at 1h (no 1h
history). sr_std pooled per strategy across both passes. Recompute script inline in run
notes; inputs all present in result rows (`summary.lockbox_oos.sharpe_pt`, `num_trades`,
`summary.best_train_sharpe_pt`).

## What next (each step separately gated)

1. **Stage-2 candidate:** GEN_KELTNER_BREAKOUT × trail_ema8 × 1h family (AAPL primary;
   SPY/QQQ fixed_2R robustness suggests a KELTNER-1h pocket). Stage-2 needs its own
   written pre-registration (narrow grid winner ±1, exit frozen, held-out scope, DSR ≥
   0.95 judged there) BEFORE any run — per D013/D015.
2. The two FAIL-classified H1 cells: do NOT carry to Stage-2 unless their fold criteria
   misses are understood and pre-registered.
3. Nothing here is promotable. `robust_final` remains the only promotable tier.

## Artifacts

- `pass1_10m/MEGA_walk_forward_results.json` + report (420 rows)
- `pass2_1h/MEGA_walk_forward_results.json` + report (560 rows)
- Runtime totals: 178.7s engine time, 8 workers.
