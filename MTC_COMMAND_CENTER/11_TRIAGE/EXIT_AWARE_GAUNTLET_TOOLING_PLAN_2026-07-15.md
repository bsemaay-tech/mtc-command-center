# Exit-Aware Gauntlet Tooling — Implementation Plan (2026-07-15)

Author: Claude Fable 5. Status: **PLAN ONLY — not approved to build.** Requires Barış
approval + its own Gate-5 adversarial review before any code is written or run. This
document specifies the change so approval can be a concrete yes/no.

## 1. Why this exists

Gate-5 review of the FAZ 3B Stage-2 draft (`11_TRIAGE/CODEX_GATE5_FINDINGS_FAZ3B_STAGE2_2026-07-13.md`,
findings §F/§G/§J) proved the promotion gauntlet is **exit-blind**: `cpcv_validator.py`,
`multiwindow_oos.py`, and `probabilistic_pbo.py` never pass a row's `exit_mode` into
`simulate_slice`, whose default is `fixed_2R` (`mega_walk_forward.py:82,648`). Any gauntlet run
on a `trail_ema8` candidate therefore silently scores `fixed_2R` behaviour. PBO additionally has
no per-configuration return matrix — it treats each CPCV *row* (different symbol/exit) as a
competing configuration, which is statistically wrong for confirming one cell.

The FAZ 3B deferred forward pre-registration
(`00_AGENT_PROTOCOLS/FAZ3B_STAGE2_FORWARD_CONFIRM_PREREG_2026-07-13.md` §8) names this tooling as
a **hard prerequisite** before any forward evaluation (earliest 2028-07-14). It is also required
for *any* future exit-mode confirmation, not just FAZ 3B. Building it now is idle-time prep; it
changes no default behaviour and authorises no run.

## 2. Scope and non-goals

**In scope:** thread `exit_mode` through the three gauntlet tools; add a per-cell
configuration×period return matrix generator for PBO; stamp `exit_mode` into every output and
candidate id; fix the two correctness defects Gate-5 flagged (generated vs literal neighbours;
insufficient-trade neighbours silently dropped).

**Non-goals / hard rails:**
- **Default `fixed_2R` behaviour stays byte-identical.** `exit_mode` defaults to
  `DEFAULT_EXIT_MODE`; existing rows without an `exit_mode` field score exactly as today.
- Self-parity gate `03_QUANTLENS/tools/faz3b_self_parity.py --verify` must stay byte-identical
  green afterwards; goldens are NOT recaptured.
- No engine (`mega_walk_forward.py` `simulate_slice`) logic change — it already accepts
  `exit_mode`; only its callers change. Protected scopes (Pine, parity, MTC_V2, `02_MTC_BACKTEST`,
  `07_ADAPTERS`, `06_SCHEMAS`) untouched.
- Building/testing the tool authorises NO backtest, smoke, gauntlet, or FAZ 3B run. Passing the
  tool's own tests is not strategy evidence.

## 3. Per-tool changes (exact, grounded in current code)

### 3.1 `cpcv_validator.py`

- `load_rows` (line 62): today filters `PASS/STRONG_PASS` with `best_params`. Add: carry
  `row.get("exit_mode", DEFAULT_EXIT_MODE)` forward (do not drop rows lacking it — default).
- `validate_candidate` (line 65-69): after `params = row["summary"]["best_params"]`, read
  `exit_mode = row.get("exit_mode", mw.DEFAULT_EXIT_MODE)`; thread it into `evaluate_split`.
- `evaluate_split` (line 45-46): the call
  `mw.simulate_slice(df, sig, stop, strategy, start, end, direction=direction)` gains
  `exit_mode=exit_mode`. Add `exit_mode` as a function parameter.
- Output (line 129 `split_results`, and the candidate summary): stamp `"exit_mode": exit_mode`
  on the result dict AND each split row, so an auditor can detect a silent substitution.

### 3.2 `multiwindow_oos.py`

- `score_window` (line 58-59): `M.simulate_slice(df, sig, stop, strategy, s, e, return_trades=True)`
  gains `exit_mode=exit_mode`; add the parameter and thread `r["exit_mode"]` from the caller.
- Line ~137 (`M.simulate_slice(df, sig2, stop2, strat, lb_s, n)`): same — add `exit_mode`.
- **Literal neighbours, not generated (Gate-5 §J / edit 9):** `perturb_params` (line 68) invents
  `×0.8/×1.25` numeric neighbours. For a pre-registered confirmation this is wrong — the neighbour
  set must be the exact literal star configs from the pre-registration. Add a mode where the
  caller supplies the literal neighbour list; the generated-perturbation path stays only for
  legacy exploratory use and must never feed a confirmation gauntlet.
- **Insufficient-trade neighbours count as failures (Gate-5 edit 9):** the stability denominator
  (line ~131-142) currently excludes low-trade neighbours, which can inflate the pass rate. Change:
  a neighbour with `< min_trades` is a *stability failure*, kept in the denominator.
- Stamp `exit_mode` into every emitted row/candidate id.

### 3.3 `probabilistic_pbo.py` + new matrix generator

- `candidate_id` (line 16-17): `f"{strategy}|{symbol}|{timeframe}"` → append `exit_mode` and the
  literal params, e.g. `strategy|symbol|tf|exit_mode|ema=..,atr=..,mult=..`.
- **Root fix (Gate-5 §G / edit 11):** `load_cpcv_matrix` (line 20-30) builds the candidate matrix
  from CPCV *rows* (different symbols/exits) using their `split_results` as columns. For confirming
  ONE cell this is invalid. Add a new generator
  `03_QUANTLENS/tools/pbo_matrix.py` (name TBD) that, for a single symbol+exit cell, produces a
  **configuration × common-period return matrix**: the frozen primary config plus the 4 literal
  star configs (rows) × six identical, non-overlapping chronological groups (columns), each cell =
  that config's return on that period, scored with the row's `exit_mode`. CSCV then uses the 10
  complement-unique 3/3 partitions. `probabilistic_pbo.py` consumes THIS matrix; it must refuse a
  matrix whose rows mix symbols or exits, or that has `< 2` configurations.

## 4. Cross-cutting invariants

- Every output file and candidate id carries `exit_mode`; a missing/`N_A` exit stamp on a
  confirmation input is a hard error, never a silent default.
- `DEFAULT_EXIT_MODE` fallback applies ONLY to legacy rows with no `exit_mode` field, preserving
  historical parity; a confirmation run must set it explicitly.
- No behavioural change to any default-mode run: prove with a before/after diff on an existing
  fixed_2R CPCV/multiwindow/PBO artifact (identical numbers).

## 5. Test plan (all offline, no strategy run)

1. **Parity:** run each tool on an existing `fixed_2R` result with NO `exit_mode` field → output
   byte-identical to pre-change (locked fixtures).
2. **Exit threading:** a synthetic row with `exit_mode="trail_ema8"` → assert the tool calls
   `simulate_slice(..., exit_mode="trail_ema8")` (spy/monkeypatch) and stamps it in output.
3. **Substitution guard:** a `trail_ema8` row scored without the stamp → tool errors, does not
   silently score fixed_2R.
4. **Literal neighbours:** multiwindow given a literal star list uses exactly those; the generated
   path is unreachable from the confirmation entrypoint.
5. **Insufficient-trade stability:** a low-trade neighbour lowers the pass rate (counted as fail),
   not excluded.
6. **PBO matrix:** generator emits a 5×6 matrix for one cell; PBO refuses mixed-symbol/exit rows
   and `<2` configs; CSCV yields 10 partitions.
7. `faz3b_self_parity.py --verify` byte-identical green.

## 6. Approval gates (in order, each separate)

1. Barış approves THIS plan → then code may be written on a feature branch.
2. Gate-5 adversarial review of the implementation (own prompt) — attack parity, stamping
   completeness, matrix correctness, the neighbour/denominator fixes.
3. Only after both: the tool is available. It still authorises no FAZ 3B run — the forward
   window (2028) and its own execution approval remain separate.

## 7. Effort estimate

Small-to-moderate: ~3 caller edits + 1 new matrix generator (~150 LOC) + ~7 tests. The risk is
entirely in the parity guarantee and the PBO matrix semantics, which is why it needs its own
Gate-5. No engine or protected-scope edits.
