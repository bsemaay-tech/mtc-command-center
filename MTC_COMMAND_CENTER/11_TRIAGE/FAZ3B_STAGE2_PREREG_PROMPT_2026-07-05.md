# PROMPT — Faz 3b STAGE-2 pre-registration + gated confirmation run

You are a fresh Claude (or Codex) session in `C:\LAB\Tradingview_LAB_CLEAN`.
Read `AGENTS.md` + `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md` first.
Work on branch `feature/faz3b-stage1-sweep` (or a new `feature/faz3b-stage2` off master
if #stage1 was merged — check `git log --oneline master -3` first).
NEVER commit to master directly. Never `git add .` — explicit paths only.

## Context (verified state, do not re-derive)

- Faz 3b chain D013 → D014 → D015 complete. Engine has swept `exit_mode`
  (`fixed_2R|fixed_3R|trail_ema8|opposite_channel`, env `MEGA_EXIT_MODES`) and
  `MEGA_GRID_STRIDE` (capped floor-selector). Self-parity gate
  (`03_QUANTLENS/tools/faz3b_self_parity.py --verify`) is byte-identical green; goldens
  committed, NEVER recapture them.
- Stage-1 discovery result (read BOTH before anything):
  1. `03_QUANTLENS/research/faz3b_stage1_20260705/STAGE1_REPORT.md`
  2. `00_AGENT_PROTOCOLS/FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md`
- **Stage-2 candidate family: GEN_KELTNER_BREAKOUT × trail_ema8 × 1h.** Primary cell
  AAPL (Stage-1: STRONG_PASS, union-DSR 0.581, 49 trades, +19.0% OOS at fixed_2R-grid
  stride 3). Known confound: 1h fixed_2R itself has robust KELTNER cells on SPY/QQQ —
  Stage-2 must be designed so it can DISTINGUISH "exit adds value" from "KELTNER-1h
  pocket".
- The two FAIL-classified Stage-1 H1 cells (KELTNER/AMZN/trail_ema8,
  STOCH/AAPL/opposite_channel) are NOT Stage-2 candidates unless you first explain their
  fold-criteria misses in writing and Barış accepts.

## YOUR TASK — in this exact order, each step gated

### Step 1 — Draft Stage-2 pre-registration (docs only, no run)

Write `00_AGENT_PROTOCOLS/FAZ3B_STAGE2_CONFIRM_PREREG_<date>.md`. D013 Stage-2 rules are
binding: **pre-registered NARROW grid = Stage-1 winner ± 1 neighbor per knob; exit_mode
FROZEN to trail_ema8; DSR ≥ 0.95 judged HERE and only here; held-out scope.** Your design
must answer, explicitly:

1. **Winner params:** extract the Stage-1 selected best config for KELTNER/AAPL/1h/
   trail_ema8 from `faz3b_stage1_20260705/pass2_1h/MEGA_walk_forward_results.json`
   (`summary.best_params` or equivalent field — inspect the row). Grid = that winner ± 1
   neighbor per numeric knob from the ORIGINAL GRIDS neighborhood (NOT new values).
   Enumerate the exact param sets in the doc — no formulas, the literal list.
2. **Held-out scope:** Stage-1 consumed SPY,QQQ,AAPL,MSFT,NVDA,AMZN,TSLA × 10m,1h on
   `native_multiasset_alpaca_2026-06-28`. Propose held-out data honestly — options to
   weigh: (a) different symbols same class (e.g. DIA, IWM, GOOGL, META from the same
   bundle — verify they exist in the manifest first), (b) same symbols on an untouched
   timeframe (2h/30m — weaker: same underlying paths), (c) both. State which cells decide
   DSR ≥ 0.95 BEFORE running. AAPL itself is NOT held-out — it may appear only as a
   reference row, never as confirmation evidence.
3. **Confound control:** every Stage-2 cell runs BOTH `trail_ema8` AND `fixed_2R` (same
   narrow grid) so the exit's incremental value is measured on held-out data. Decision
   rule: exit confirmed only if trail_ema8 clears the gate where fixed_2R does not, or
   beats it by a pre-stated margin — write the exact rule.
4. **Trial accounting (A17):** narrow grid × 2 modes × cells — state the exact trial
   count and the union family (Stage-1 + historical + Stage-2) used for the final DSR.
   Stage-2 DSR must be union-adjusted, same method as Stage-1 report (script logic is in
   the Stage-1 report's "DSR method note").
5. **STOP rules:** copy the Stage-1 set (row count, stamping, SKIPPED_NA, heartbeat,
   wall-clock from smoke, disk ≥10GB, unexplained ERROR, partials-never-evidence) and add:
   any Stage-2 cell whose data overlaps Stage-1 evidence cells voids that cell.
6. **Outcome mapping, pre-committed:** DSR ≥ 0.95 ∧ BH-FDR ∧ PASS on held-out →
   `robust_final` candidate → next step is FORWARD_PAPER queue per
   `_AI_MEMORY/LIVE_TRADING_GATE.md` + D-decisions (production phased, Pine-parity +
   dry-run first — NOT live). Below that but union-DSR ≥ 0.50 on held-out → stays
   research, no third bite at the same family without new data. Below that → family dead,
   write the negative result honestly.
7. **Command block:** exact env + CLI. REMEMBER: `--symbol` is a REPEATABLE flag
   (`--symbol AAPL --symbol DIA …`), comma-join silently yields NO_DATA. `MEGA_EXIT_MODES`
   IS comma-separated. Grid mechanism: Stage-2's narrow grid is NOT in GRIDS — decide and
   document the mechanism (options: a temporary `MEGA_GRID_OVERRIDE_JSON` env knob added
   to the engine under self-parity protection, or a one-off runner script that monkeypatches
   GRIDS[strategy] before main() — prefer the runner script: zero engine edit). If you DO
   edit the engine, self-parity `--verify` must PASS byte-identical after, and the edit is
   part of what Barış approves.

### Step 2 — Adversarial review

Write a Codex Gate-5 prompt (`11_TRIAGE/CODEX_GATE5_PROMPT_FAZ3B_STAGE2_<date>.md`)
covering: winner-extraction correctness, held-out genuineness (no leakage from Stage-1
evidence), trial arithmetic, confound-control rule falsifiability, gate hygiene (doc must
not self-authorize the run). Hand to Barış to run Codex. Apply every required edit.

### Step 3 — Barış approval

Present the reviewed pre-reg. His explicit written sentence → record as D016 in
`_AI_MEMORY/DECISIONS.md`. **NO RUN before D016 exists.**

### Step 4 — Execute (only after D016)

Smoke 1 cell → verify stamping + runtime → full run (foreground-monitored or supervisor)
→ STOP-rule verification → morning report per
`03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md` → commit results +
handoff write-back (GLOBAL_HANDOFF.md, prefix `## [MODEL] YYYY-MM-DD — topic`).

## Hard rules

- Protected scopes untouched: Pine, parity, MTC_V2, `02_MTC_BACKTEST`, `07_ADAPTERS`,
  `06_SCHEMAS`. Goldens never recaptured. GRIDS content never edited in place.
- Never trust prior reports — verify Stage-1 numbers you rely on by re-reading the result
  JSONs yourself.
- Every commit: explicit paths, feature branch, conventional message.
- Nothing in Stage-2 authorizes paper/live trading. `robust_final` → FORWARD_PAPER queue
  is itself a separate human gate.
