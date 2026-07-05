# CODEX GATE-5 PROMPT — Faz 3b nit-fix diff + Stage-1 sweep pre-registration (2026-07-05)

You are Codex, running an ADVERSARIAL Gate-5 review in `C:\LAB\Tradingview_LAB_CLEAN`,
branch `feature/strategy-param-specs`. Read `AGENTS.md` + `_AI_MEMORY/START_HERE.md` first.
Never trust any report in this prompt — re-derive everything from git and by running commands.

## Context

- Faz 3b engine diff `cb8bf5a3` was audited by Claude Fable (PASS WITH NITS) and approved by
  Barış → D014 (`ff2cfe6e`). Roles now reversed: Claude wrote the items below, YOU audit.
- D013 scope: `00_AGENT_PROTOCOLS/FAZ3B_EXIT_SWEEP_SCOPE.md`. Sweep still not approved.

## Review object A — nit-fix commit `a6342810`

Claims to close audit nits 1-2 (short-path tests + NA-config guard). Verify adversarially:

1. `git show a6342810` — files must be ONLY `mega_walk_forward.py` +
   `tests/test_faz3b_exit_modes.py`. No GRIDS content change, no gate/threshold change,
   no Pine/parity/MTC_V2/`02_MTC_BACKTEST`/`07_ADAPTERS`/`06_SCHEMAS`.
2. Engine change must be ONLY: `config_has_na()` helper + skip-NA-config guard in
   `_worker_impl` + `SKIPPED_NA_EXIT_MODE` classification for all-NA cells + `na_configs`
   counter. Check the guard cannot fire at `fixed_2R` (NA requires `use_trail` and a missing
   `ema_8` column; `build_signals` always adds `ema_8` — confirm line ~339).
3. Short-path tests: check the 3 new tests actually pin SHORT semantics (direction="short"):
   stop-first ordering preserved, trail exit on `close > ema`, channel exit on
   `close > rolling max(high,20).shift(1)` with an explicit lookahead bug-case
   (bar's own high excluded). Try to construct a counter-example the tests miss.
4. Run yourself:
   - `python -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_faz3b_exit_modes.py -q` → 10/10
   - `python MTC_COMMAND_CENTER/03_QUANTLENS/tools/faz3b_self_parity.py --verify` → must PASS,
     42 rows, sha256 `be8561ff…` (byte-identical; goldens NOT recaptured —
     `git log --oneline -- "**/golden_cells.json"` must show only `75da649c`).
   - `python -m py_compile MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py`

## Review object B — Stage-1 pre-registration design

`00_AGENT_PROTOCOLS/FAZ3B_STAGE1_SWEEP_PREREG_2026-07-05.md`. Attack it on:

1. **Trial-budget honesty (A17/D013):** 3 new modes × stride-3 grid ≈ 1.0× today's
   trials/cell. Is the arithmetic right (1122 param sets, stride-3 ≈ 374)? Is skipping
   fixed_2R re-runs legitimate, or does reusing historical baselines create an
   apples-to-oranges comparison (same bundle? same engine? same folds?)? Check whether the
   existing fixed_2R history for the 7-symbol/10m cells was produced from the SAME Alpaca
   bundle and comparable engine rev.
2. **DSR accounting:** does "state total historical trials per cell" adequately guard
   against selection-effect underestimation, or must Stage-1 DSR be computed against the
   union of all trials? Recommend concretely.
3. **Scope discipline:** single asset class honored? Any hidden multi-class leak (ETFs)?
   micro-price exclusion correctly N/A?
4. **`MEGA_GRID_STRIDE` design:** default-off env knob + `grid_stride` row field + harness
   `ALLOWED_NEW_KEYS` addition — is that harness edit acceptable, or does adding another
   stripped key erode the parity gate? Propose tighter alternative if so.
5. **STOP rules + H0:** are they falsifiable and complete? Anything missing (e.g., runtime
   cap, disk, worker crash semantics)?
6. **Gate hygiene:** does the doc anywhere smuggle in authorization to run? It must not —
   run approval is Barış's separate sentence (→ D015).

## Output format

Write `11_TRIAGE/CODEX_GATE5_REPORT_FAZ3B_STAGE1_2026-07-05.md`:
- Verdict A (nit-fix diff): PASS / PASS WITH NITS / FAIL + evidence (commands + output).
- Verdict B (Stage-1 design): APPROVE-AS-IS / APPROVE-WITH-CHANGES (list exact edits) / REJECT.
- Every finding: file:line + concrete failure scenario. No praise, no filler.
- Do NOT edit engine/tests/design files yourself; do NOT run any sweep or smoke test.
- Commit only your report file (explicit path staging, never `git add .`).
