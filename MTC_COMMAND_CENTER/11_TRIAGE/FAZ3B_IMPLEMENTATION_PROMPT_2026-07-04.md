# FAZ 3B IMPLEMENTATION PROMPT (for Claude — Opus or Fable, fresh session)

Approved: D013 (DECISIONS.md) + `00_AGENT_PROTOCOLS/FAZ3B_EXIT_SWEEP_SCOPE.md`.
Read both FIRST, plus AGENTS.md chain. Authorizes implementation + self-parity
regression ONLY. Sweep runs stay separately approval-gated.

## Task

Implement swept `exit_mode` in `03_QUANTLENS/tools/mega_walk_forward.py`
`simulate_slice` per the scope doc. Modes: `fixed_2R` (default), `fixed_3R`,
`trail_ema8` (absorbs the `is_trail` special case for
`QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL` — one code path; strategies
without an `ema_8` column skip trail mode as NA, never zeros), `opposite_channel`
(long exit when close < rolling `min(low, exit_len).shift(1)`; `exit_len`
internal knob, default 20; computed from the `lo` array inside simulate_slice).

Sweep axis = env `MEGA_EXIT_MODES` (comma list), default `fixed_2R` only.
`exit_mode` must NOT enter `GRIDS` — default trial counts and DSR unchanged.
Result rows gain `exit_mode` + `engine_version` fields ALWAYS.

## The gate (already in place — do not weaken)

`03_QUANTLENS/tools/faz3b_self_parity.py` + committed goldens
`tools/tests/goldens/faz3b/golden_cells.json` (42 rows, sha pinned, determinism
verified on 2026-07-04 by two identical independent runs of the pre-edit engine).

Order of work:
1. BEFORE editing: run `python faz3b_self_parity.py --verify` → must PASS
   (proves your environment reproduces the goldens).
2. Implement.
3. Harness update — ONLY this exact change is allowed: add
   `ALLOWED_NEW_KEYS = {"exit_mode", "engine_version"}` stripped alongside
   VOLATILE_KEYS during canonicalization, PLUS an assertion that every row has
   `exit_mode == "fixed_2R"` when run in default mode. NOTHING else in the
   harness may change. Goldens must NOT be recaptured. Any other harness edit
   or a recapture = you are cheating the gate = STOP.
4. `--verify` → must PASS (numeric byte-identity at fixed_2R).
5. Unit tests for the new modes (tools/tests/): 3R target math; trail exits at
   next open when close < ema8; trail NA-skip without ema_8 column;
   opposite_channel exit level correctness incl. shift(1) no-lookahead; a
   MEGA_EXIT_MODES parse test.
6. `py_compile` engine; focused tests green; self-parity PASS — all three in
   the report.

## Boundaries

No Pine/parity/MTC_V2/`02_MTC_BACKTEST`/`07_ADAPTERS`/`06_SCHEMAS`. No sweep
run (not even "small"). No GRIDS content change. No gate/threshold change. No
promotion artifacts. Commit on `feature/strategy-param-specs` (or dedicated
`feature/faz3b-exit-mode` if Barış prefers), exact paths only. After commit:
Codex adversarial review (Gate 5), then Barış approves the diff; the first
Stage-1 discovery run needs a separate written approval with the pre-registered
run design (single-asset-class subset + trimmed grids + research_robust tier,
per scope §DSR discipline).
