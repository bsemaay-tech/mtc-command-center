# CODEX GATE-5 REPORT - Faz 3b nit-fix diff + Stage-1 pre-registration

Date: 2026-07-05
Reviewer: Codex GPT-5
Branch observed: `feature/strategy-param-specs`
Review objects: commit `a6342810`; `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md`

## Verdict A - nit-fix diff `a6342810`: PASS WITH NITS

### Evidence

- `git show --name-status --format=fuller a6342810`:
  - `M MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py`
  - `M MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_faz3b_exit_modes.py`
- `git diff --numstat a6342810^ a6342810`:
  - `29 0 MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py`
  - `95 0 MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_faz3b_exit_modes.py`
- Protected-path check: `git diff-tree --no-commit-id --name-only -r a6342810 | rg "(GRIDS|\.pine|parity|MTC_V2|02_MTC_BACKTEST|07_ADAPTERS|06_SCHEMAS)"` -> `NO_PROTECTED_PATHS`.
- `git show --unified=0 a6342810 -- .../mega_walk_forward.py | rg "GRIDS|robust_final|MIN_TRADES|PASS|threshold|deflated|..."` showed only `config_has_na`, `na_configs`, and `SKIPPED_NA_EXIT_MODE` additions; no GRIDS/gate/threshold change.
- `git log --oneline -- "**/golden_cells.json"` -> only `75da649c feat(faz3b): self-parity gate live - goldens captured pre-edit, determinism proven`.
- Verification:
  - `python -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_faz3b_exit_modes.py -q` -> `10 passed in 1.11s`.
  - `python MTC_COMMAND_CENTER/03_QUANTLENS/tools/faz3b_self_parity.py --verify` -> `PASS - 42 rows match golden sha256=be8561ffeb4c4a9f...`.
  - `python -m py_compile MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py` -> exit 0, no output.

### Findings

1. [Nit] SHORT stop-first ordering is implemented but not actually pinned by the new short tests.
   - Evidence:
     - Engine SHORT branch checks stop before trail/channel/target at `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py:637-650`.
     - New fixed short test sets `lo[22] = 96.9` and leaves high below the 101 stop at `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_faz3b_exit_modes.py:182-199`.
     - New trail and channel short tests also avoid same-bar stop conflicts at `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_faz3b_exit_modes.py:202-241`.
   - Failure scenario: a future refactor could reverse same-bar SHORT stop/target priority while these tests still pass, because none creates a bar where `hi[cur] >= stop_price` and `lo[cur] <= target` simultaneously.
   - Impact: test-coverage nit only. Current engine order is correct.

2. NA-config guard is correctly defensive and should not fire in the normal `fixed_2R` worker path.
   - Evidence:
     - `build_signals` always adds `ema_8` before strategy-specific logic at `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py:336-339`.
     - NA requires `use_trail` and missing `ema_8` at `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py:583-590`.
     - `_worker_impl` calls `build_signals` before every simulated slice and skips any NA config before fold means at `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py:1214-1235`.
     - All-NA cells return explicit `SKIPPED_NA_EXIT_MODE` at `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py:1243-1250`.
   - Failure scenario tested adversarially: direct `simulate_slice(..., exit_mode="fixed_2R")` can still produce NA only for the native trail strategy if the caller bypasses `build_signals` and omits `ema_8`; `_worker_impl` does not do that.

## Verdict B - Stage-1 pre-registration design: APPROVE-WITH-CHANGES

Required edits before D015 approval:

1. Fix the trial-budget arithmetic and stop saying trials/cell do not exceed today's level.
   - Evidence:
     - Prereg claims stride-3 full grid `1122 -> approx 374`, and `3 modes x grid/3 ~= 1.0x` at `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md:39-41`.
     - Current `GRIDS` are 20 strategies, `sum_grid = 1122`. A literal `grid[::3]` gives `sum_stride3 = 376`; `3 * 376 = 1128`, ratio `1.0053475935828877`.
     - Per-strategy cells can exceed current trials: e.g. `GEN_KELTNER_BREAKOUT` 16 -> 6 stride configs -> 18 new-mode trials; `GEN_TRIPLE_EMA_STACK` 8 -> 3 stride configs -> 9 new-mode trials.
   - Failure scenario: A17 accounting is reported as "not exceeding today" while selected strategy cells are actually +1 or +2 trials before adding any historical fixed_2R selection context.
   - Exact edit: replace line 40-41 with exact arithmetic: `grid[::3] = 376 configs; 3 modes = 1128 effective new-mode trials across the strategy library (100.53% of full-grid aggregate), with up to +2 trials for non-divisible strategy grids.` If strict non-exceedance is required, define a capped selector using `floor(len(grid)/3)` per strategy; that gives 372 configs and 1116 new-mode trials aggregate.

2. Name and prove the fixed_2R baseline artifacts before reusing them.
   - Evidence:
     - Prereg says fixed_2R is not re-run and existing fixed_2R results for the same cells are used at `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md:35-38`.
     - The cited 7-symbol historical report is 10m only: `MTC_COMMAND_CENTER/11_TRIAGE/US_EQUITIES_10M_ALPACA_6YR_SWEEP_2026-06-28.md:6` and `:18`.
     - Stage-1 scope includes both `10m` and `1h` at `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md:29`.
     - Data README says the primary multiasset bundle supersedes the older 7-symbol 10m bundle at `MTC_COMMAND_CENTER/03_QUANTLENS/data/README.md:26-27`.
     - Local hash check confirms the 7 old 10m CSVs are byte-identical to the primary bundle's 10m CSVs: SPY, QQQ, AAPL, MSFT, NVDA, AMZN, TSLA all `old_new_same=True`.
   - Failure scenario: Stage-1 reports non-default 1h wins "where fixed_2R does not" without a local, named fixed_2R 1h comparator from the same bundle/engine/folds.
   - Exact edit: add a baseline table with one row per timeframe:
     - `10m`: artifact `MTC_COMMAND_CENTER/03_QUANTLENS/data/native_us_equities_10m_alpaca_2026-06-28/full_sweep_2026-06-28/MEGA_walk_forward_results.json`; note old/new bundle CSV SHA256 equality for the 7 symbols.
     - `1h`: either name an existing artifact with same bundle/engine/folds, or require `fixed_2R` 1h baselines to be run inside D015 before comparisons. If no 1h baseline is approved, remove `1h` from Stage-1.

3. Make Stage-1 DSR selection-adjusted, not just annotated.
   - Evidence:
     - Prereg only requires the report to state historical trials per cell at `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md:48-50`.
     - Current engine DSR uses `grid_n = len(GRIDS[strat])` at `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py:1592-1608`; it does not include exit-mode multiplicity or historical fixed_2R selection.
     - Runbook A17 says wider search-space kills DSR and DSR is `grid_n` trial-count based at `MTC_COMMAND_CENTER/11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md:236` and `:396`.
   - Failure scenario: a trail/channel/fixed_3R cell clears `research_robust` using only within-run DSR, but the human-selected family was fixed_2R full-grid history plus three new exit modes. Merely printing total historical trials does not correct the selection-effect estimate.
   - Exact edit: require a `dsr_union_p_value` or `dsr_selection_adjusted` field for H1. Use `historical_fixed2R_trials_per_strategy + stage1_new_trials_per_strategy` as the candidate family for the H1 decision. Engine DSR may remain as a diagnostic, but `research_robust` for Stage-1 should be based on the union-adjusted value or explicitly labeled "screen only, not H1 acceptance."

4. Tighten the parity-harness allowance for `grid_stride`.
   - Evidence:
     - Prereg proposes adding `grid_stride` to parity harness `ALLOWED_NEW_KEYS` at `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md:42-47`.
     - Current harness allowlist is intentionally narrow: `ALLOWED_NEW_KEYS = {"exit_mode", "engine_version"}` at `MTC_COMMAND_CENTER/03_QUANTLENS/tools/faz3b_self_parity.py:66-69`, and it asserts `exit_mode == "fixed_2R"` before stripping at `MTC_COMMAND_CENTER/03_QUANTLENS/tools/faz3b_self_parity.py:103-113`.
   - Failure scenario: a default-mode bug emits `grid_stride = 3` or silently trims the grid while the parity harness strips `grid_stride`, weakening the gate.
   - Exact edit: do not add `grid_stride` as an unconditional stripped key. Add a pre-strip assertion that every default self-parity row has `grid_stride == 1` (or omit the field entirely when unset/default). Only after that assertion may the field be stripped for byte-identity.

5. Complete STOP rules before run approval.
   - Evidence:
     - Current STOP rules are only parity fail, malformed smoke rows, >10% `SKIPPED_NA_EXIT_MODE`, and two crashes at the same checkpoint at `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md:84-90`.
   - Failure scenario: run stalls without crashing, disk fills, output row count is short, or baseline comparator is absent; none is a STOP under the current text.
   - Exact edit: add STOP conditions for:
     - missing named fixed_2R baseline artifact/hash proof;
     - output row count not exactly 840 unless pre-explained by `NO_DATA`/`SKIPPED_RULE`;
     - supervisor heartbeat stale/no-progress threshold;
     - wall-clock cap from smoke extrapolation;
     - minimum free disk before launch and after completion;
     - any worker `ERROR` row not attributable to known `NO_DATA`/rule skip;
     - partial results must not be interpreted as H1 evidence.

### Non-findings

- Scope discipline is acceptable after edits: the listed symbols at `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md:27-31` are US exchange-traded equity/ETF instruments only; no commodity/bond/crypto ETF leak is present in the symbol list.
- Micro-price exclusion is correctly N/A for this symbol set and remains documented at `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md:60-64`.
- Gate hygiene is acceptable: the doc marks itself draft/not approved at `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md:1-7`, says execution is after approval at `:66`, and sign-off requires a Baris written approval sentence at `:97-100`.

## Commands run

```text
git status --short --branch
git show --name-status --format=fuller a6342810
git show --stat --oneline a6342810
git show --check --summary a6342810
git diff-tree --no-commit-id --name-only -r a6342810 | rg "(GRIDS|\.pine|parity|MTC_V2|02_MTC_BACKTEST|07_ADAPTERS|06_SCHEMAS)"
git diff --numstat a6342810^ a6342810
git diff --check a6342810^ a6342810
git log --oneline -- "**/golden_cells.json"
python -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_faz3b_exit_modes.py -q
python MTC_COMMAND_CENTER/03_QUANTLENS/tools/faz3b_self_parity.py --verify
python -m py_compile MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py
python -c "import sys; sys.path.insert(0,r'MTC_COMMAND_CENTER/03_QUANTLENS/tools'); import mega_walk_forward as m; ..."
Get-FileHash .../native_us_equities_10m_alpaca_2026-06-28/normalized/<SYM>_10m.csv
Get-FileHash .../native_multiasset_alpaca_2026-06-28/normalized/<SYM>_10m.csv
```

No sweep and no smoke test were run.
