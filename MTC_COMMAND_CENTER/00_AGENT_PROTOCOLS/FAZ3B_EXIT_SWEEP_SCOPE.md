# FAZ 3B — SWEPT EXIT_MODE IN simulate_slice (APPROVED SCOPE)

> Approved by Barış 2026-07-04 with the exact sentence recorded in DECISIONS.md (D013).
> Authorizes IMPLEMENTATION + SELF-PARITY REGRESSION ONLY. Any sweep run remains
> separately approval-gated. Trading-logic change — DO_NOT_TOUCH behavior rule
> satisfied by this explicit approval.

## Why

All 63 validated archetypes shared one hardcoded exit (fixed 2R target, 96-bar
time stop, next-open, stop-first) that no optimization ever touched. The
2026-07-04 methodological-ceiling analysis flags this fixed exit as the likely
binding constraint. Faz 3b makes the exit a swept knob — the last high-leverage
experiment before concluding the universe has no extractable edge at these gates.

## Exact change

- File: `03_QUANTLENS/tools/mega_walk_forward.py`, `simulate_slice` + plumbing.
- New knob `exit_mode` ∈ { `fixed_2R` (default, byte-identical to today),
  `fixed_3R`, `trail_ema8`, `opposite_channel` }.
- `trail_ema8` ABSORBS the existing `is_trail` special case
  (`QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL`) — one code path, no
  duplicate. Strategies without an `ema_8` column: trail mode = skipped/NA,
  never zeros.
- `opposite_channel` v1: exit when close crosses the opposite rolling channel
  (`min(low, exit_len).shift(1)` for longs), `exit_len` a fixed small knob
  computed inside `simulate_slice` from the low array — no `build_signals`
  change in v1.
- **`exit_mode` is NOT added to `GRIDS`.** It is a separate sweep axis
  (env/CLI, e.g. `MEGA_EXIT_MODES`), default `fixed_2R` only — so default
  grid_n, trial counts, and DSR are unchanged, making self-parity achievable.
- Result rows gain `exit_mode` + `engine_version` so old/new outputs can never
  be silently mixed. Prior results remain valid as `fixed_2R` history.
- Unchanged: stop-first same-bar ordering, next-open entry, cost/slippage
  model, HOLDING_BAR_LIMIT, warmup, fold geometry, all gates.

## Non-negotiable safety gate — self-parity BEFORE any sweep

Golden baselines are captured from the CURRENT committed engine on a pinned
cell set (≥20 cells across strategies/symbols/TFs, including ≥1 `is_trail`
cell) BEFORE the engine is edited. The new engine with `exit_mode=fixed_2R`
must reproduce those baselines byte-identically (stable-field hash). Any diff
= STOP, no sweep. Harness: `03_QUANTLENS/tools/faz3b_self_parity.py`; goldens
committed under `03_QUANTLENS/tools/tests/goldens/faz3b/`.

## DSR discipline (A17)

- Stage 1 (discovery): exit knob ON, grids trimmed elsewhere so trials/cell do
  not exceed current levels; evaluated at the RESEARCH tier only.
- Stage 2 (confirmation): pre-registered narrow grid (winner ±1 neighbor,
  exit_mode frozen) on held-out scope; DSR ≥ 0.95 judged here only.
- Stage-2 grid must be registered in writing BEFORE the run.

## Approved companion package (items 2–4)

- **Micro-price exclusion:** runner/report level — micro-price compounding
  artifact symbols excluded from pooled leaderboards, quarantined section
  keeps them visible. No engine change.
- **Two-tier robustness label:** `research_robust` = MIN_TRADES ≥ 30 ∧ DSR ≥
  0.50 (Stage-1 filter ONLY). `robust_final` unchanged (DSR ≥ 0.95 ∧ BH-FDR ∧
  PASS) and remains the ONLY promotable tier.
- **Single-asset-class subsets:** Stage-1 discovery runs one asset class at a
  time; never 51-symbol pooled. Run-design rule, no code.

## Roles

Claude implements (tests-first; self-parity is test #1). Codex adversarial
review of the diff (Gate 5). Barış approves the diff landing AND separately
approves the first sweep. No cheap-model dispatch for the engine edit.
