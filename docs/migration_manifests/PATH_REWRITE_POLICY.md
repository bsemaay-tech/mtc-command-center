# Hardcoded Path Rewrite Policy

- Decision date: 2026-05-31
- Authority: ratifies the de-facto stance enforced by Phase 1 / Phase 2 / Phase 5
- Phase 6 audit checks addressed: CHECK 6 (active-script hardcoded path scan) — already PASS

## Verdict

**Active set: zero-tolerance, all rewrites complete.**
**Deferred set: fix-on-demand, no bulk rewrite.**

## Active Set Definition

The "active set" is the 18 scripts that are actually invoked by:

- `parity_compare.py` and its imports
- `mtc_bridge.mjs`, `run_pinets.mjs`, `validate_syntax.mjs`
- `pine_trades.py`
- `run_planned_cases.py` and the `tools/parity/*.py` runners
- `run_2025_audit.py`, `run_tracker_ready_cases.py`, `parity_test.py`
- `RUN_MTC_BACKTEST.ps1`
- `optimize.py`, `add_l12_cases.py`, `add_htf_cols.py`

Phase 6 CHECK 6 verified **0 hits** for `01_MASTER TEMPLATE_V2` and
`C:\LAB\tradingview-lab` across all 18. Phase 6 CHECK 7 verified **13/13**
`REPO_ROOT`-using scripts resolve to `C:\LAB\Tradingview_LAB_CLEAN`. The
remaining 3 use `__dirname`-relative or script-local anchors and need no
`REPO_ROOT` definition.

## Deferred Set

Three categories, all documented in
`MTC_COMMAND_CENTER\02_MTC_BACKTEST\hardcoded_path_rewrite_TODO.md`:

### 1. QuantLens references (116 hits across 57 files)

- **Reason for defer:** each anchor pattern (`MCC_ROOT.parent`, `REPO_ROOT`,
  `mcc_root.parent`, `tpl_root`, `root.parent`) has different semantics. A
  naive bulk string-replace would produce double-`MTC_COMMAND_CENTER`
  paths and silently break path resolution.
- **Active subset that would need rewrite first when re-activated:**
  - `MTC_COMMAND_CENTER/11_TRIAGE/*.py` (~5 files)
  - `MTC_COMMAND_CENTER/03_QUANTLENS/tools/*.py` (~5 files)
  - `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/*.py` (~6 files)
- **Inactive subset:** ~40 one-shot research batch scripts that produced
  their evidence and will not be re-run.
- **Hit inventory:**
  `docs/migration_manifests/phase2_quantlens_06_quantlens_lab_hits.csv`

### 2. One-shot legacy scripts

- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/update_tracker.py` (line 3)
- Already documented in
  `MTC_COMMAND_CENTER/02_MTC_BACKTEST/hardcoded_path_rewrite_TODO.md`
  under "Deferred — one-shot legacy scripts".

### 3. Future discoveries

Any newly-discovered hardcoded path that isn't on the active path falls
under the deferred set unless the script is being re-activated.

## Trigger To Rewrite A Deferred Item

Rewrite if **any one** condition holds:

1. The script is about to be invoked (manually or by a runner).
2. The script is imported by a script on the active path.
3. The script is referenced by a runbook or scheduled job that will
   actually run.

If none of the three hold, the deferred-status remains. The cost of a
broken hardcoded path in dead code is zero; the cost of a naive bulk
rewrite that doubles-up `MTC_COMMAND_CENTER` paths is high (silent
filesystem misses, hard-to-diagnose `FileNotFoundError`).

## Rewrite Procedure (When Triggered)

1. Locate every hardcoded segment using:
   ```powershell
   Select-String -Path <script> -Pattern 'tradingview-lab|01_MASTER TEMPLATE_V2|mtc_backtest|06_QUANTLENS_LAB|110_MTC_BACKTEST_OPTİMİZASYON_DİZİNLERİ'
   ```
2. Map per the table in
   `MTC_COMMAND_CENTER/02_MTC_BACKTEST/hardcoded_path_rewrite_TODO.md`
   (Phase 2 mapping + Phase 2 QuantLens addendum).
3. Apply rewrite.
4. Run AUTO_002 smoke (or the most specific parity case the rewritten
   script affects) and confirm:
   - FINAL VERDICT: PASS
   - 0 new "Tracker workbook missing" or similar regressions
5. Save smoke log under `docs/migration_manifests/phase5_<scriptname>_smoke.log`.
6. Update `hardcoded_path_rewrite_TODO.md` to move the entry from
   "Deferred" to "Phase 5+ rewrites".
7. Commit:
   `fix(<area>): rewrite hardcoded paths in <script> + AUTO_002 smoke PASS`.

## What This Policy Does NOT Authorize

- **No bulk rewrite of the 116 QuantLens hits.** Per-script analysis only.
- **No rewrite of inactive one-shot scripts** (like `update_tracker.py`)
  unless they are being revived.
- **No changes to Pine source, MTC trading logic, or parity rules** — those
  are governed by `AGENTS.md` and require explicit approval.

## Sign-off Reference

Phase 1 verification artifacts reviewed at this decision time:

- `docs/migration_manifests/phase1_apply_summary.json`
  - copied_files: 11,093
  - dedupe_skipped_files: 1,597
  - excluded_items: 98
  - mtc_command_center_files_verified: 406
  - root_scripts_copied: 5 (add_htf_cols.py, add_l12_cases.py,
    mtc_bridge.mjs, optimize.py, parity_compare.py) — Phase 4 then
    restored 6 more from legacy (parity_test.py, run_2025_audit.py,
    RUN_MTC_BACKTEST.ps1, run_pinets.mjs, run_tracker_ready_cases.py,
    validate_syntax.mjs) per
    `phase4_late_root_scripts_restore.csv`.
- `docs/migration_manifests/phase1_residual_inventory.csv`
  - 7 phase1_root_generated (AGENTS.md, CLAUDE.md, GEMINI.md, README.md,
    verify_migration.ps1, .chatgpt-instructions.md, .cursorrules) — all
    present and verified
  - 9 phase1_manifest (audit trail under docs/migration_manifests/) — all
    present
  - 101 phase1_generated_or_unmapped — all generated by Phase 1 apply or
    intentionally-unmapped legacy files (per-project _AI_MEMORY handoffs,
    QuantLens strategy READMEs, etc.)

All categories accounted for. Phase 1 review: **PASS**.
