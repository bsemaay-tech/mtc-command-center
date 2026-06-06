# Hardcoded Path Rewrite TODO

Status: **Phase 5 active scripts rewritten and smoke verified (2026-05-31)**.
Below sections are kept as audit trail of what was rewritten.

## Phase 5 outcome (2026-05-31)
Rewritten in clean tree, parity smoke AUTO_002 PASS after rewrite:
- RUN_MTC_BACKTEST.ps1 (absolute path)
- run_pinets.mjs, validate_syntax.mjs (`__dirname`-relative)
- run_tracker_ready_cases.py, run_2025_audit.py (REPO_ROOT shift + path strings)
- tools/parity/run_planned_cases.py, run_python_parity.py, build_case_queue.py,
  read_tracker.py, tw_apply_case.py, tw_collect_result.py
  (parents[2] → parents[4] + path strings)

Smoke evidence: docs/migration_manifests/phase5_path_rewrite_smoke_AUTO_002.log

## Deferred — QuantLens references (116 hits across 57 files)
Bulk rewrite deferred because each anchor (MCC_ROOT.parent vs REPO_ROOT vs
mcc_root.parent vs tpl_root vs root.parent) has different semantics and a
naive string replace would create double-MTC_COMMAND_CENTER paths.

### Reactivated 2026-05-31 for transcript backfill
- `MTC_COMMAND_CENTER/11_TRIAGE/ingest.py`
- `MTC_COMMAND_CENTER/11_TRIAGE/generate_worklist.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/paths.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/registry_reader.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/pipeline_reader.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/audit_reader.py`

These now resolve QuantLens through the clean-tree `MTC_COMMAND_CENTER/03_QUANTLENS`
layout first, with legacy `01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB` kept as fallback.
Verification: `python -m pytest tests` in `08_DASHBOARD_APP/apps/api` passed 32/32;
`11_TRIAGE/ingest.py` dry-run is idempotent after backfill.

Fix on demand when a specific QuantLens script is invoked. Most hits are in
one-shot research batch scripts that already produced their evidence and will
not be re-run. Active code that would need rewrite:
- MTC_COMMAND_CENTER/11_TRIAGE/*.py (5 file)
- MTC_COMMAND_CENTER/03_QUANTLENS/tools/*.py (~5 file)
- MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/*.py (~6 file)

Full list: docs/migration_manifests/phase2_quantlens_06_quantlens_lab_hits.csv

## Deferred — one-shot legacy scripts (outside Phase 6 active-18 list)

Identified during Phase 6 audit follow-up (2026-05-31). These scripts hold
absolute legacy paths but are not on the active runtime path:

### update_tracker.py
- Location: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/update_tracker.py`
- Line 3: `xlsx_path = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\05_PARITY\MTC_V2_PARITY_CASE_TRACKER.xlsx"`
- Purpose: one-shot xlsx append for AUTO_047/048/049 case rows (already
  executed, evidence committed in tracker history)
- Reason for deferral: not invoked by any active runner; xlsx target file
  itself absent from clean tree (see CHECK 8 fix — CSV is source of truth);
  rewriting now would only produce dead code targeting a missing file
- Action on next use: if this script is ever revived, rewrite `xlsx_path` to
  the clean-tree equivalent (`MTC_COMMAND_CENTER/01_MTC_PROJECT/05_PARITY/MTC_V2_PARITY_CASE_TRACKER.xlsx`)
  AND first generate the xlsx target (currently CSV-only)

### update_parity_files.py
- Location: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/update_parity_files.py`
- Line 3: `csv_file = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\05_PARITY\MTC_V2_PARITY_CASES.csv"`
- Purpose: one-shot column-adder for the tracker CSV. Appends 30+ guard /
  filter columns to `MTC_V2_PARITY_CASES.csv`. Already executed — the
  target columns are present in the current CSV header.
- Reason for deferral: not invoked by any active runner; target CSV schema
  already extended; re-running would duplicate columns
- Action on next use: if this script is ever revived, rewrite `csv_file` to
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/05_PARITY/MTC_V2_PARITY_CASES.csv`
  AND add an idempotency check (skip columns that already exist) before
  re-execution

---

## Phase 1 original five (rewritten in Phase 2 by Codex)

## add_htf_cols.py
| Line | Matched path | Current text | Proposed clean mapping |
|---|---|---|---|
| 3 | `C:\LAB\tradingview-lab` | `csv_path = r'C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\05_PARITY\MTC_V2_PARITY_CASES.csv'` | `C:\LAB\Tradingview_LAB_CLEAN` |
| 3 | `01_MASTER TEMPLATE_V2` | `csv_path = r'C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\05_PARITY\MTC_V2_PARITY_CASES.csv'` | `MTC_COMMAND_CENTER\01_MTC_PROJECT` |

## add_l12_cases.py
| Line | Matched path | Current text | Proposed clean mapping |
|---|---|---|---|
| 25 | `01_MASTER TEMPLATE_V2` | `TRACKER_CSV = REPO_ROOT / "01_MASTER TEMPLATE_V2/05_PARITY/MTC_V2_PARITY_CASES.csv"` | `MTC_COMMAND_CENTER\01_MTC_PROJECT` |
| 26 | `01_MASTER TEMPLATE_V2` | `TRACKER_XLSX = REPO_ROOT / "01_MASTER TEMPLATE_V2/05_PARITY/MTC_V2_PARITY_CASE_TRACKER.xlsx"` | `MTC_COMMAND_CENTER\01_MTC_PROJECT` |

## mtc_bridge.mjs
| Line | Matched path | Current text | Proposed clean mapping |
|---|---|---|---|
| 90 | `mtc_backtest` | `TV_MERGED_DIR = resolve(__dirname, 'mtc_backtest/parity_suite_350/tv_manual_inputs/merged');` | `MTC_COMMAND_CENTER\02_MTC_BACKTEST` |
| 124 | `01_MASTER TEMPLATE_V2` | `const PINE_PATH = resolve(__dirname, '01_MASTER TEMPLATE_V2/01_PINE/MTC_V2.pine');` | `MTC_COMMAND_CENTER\01_MTC_PROJECT` |

## optimize.py
| Line | Matched path | Current text | Proposed clean mapping |
|---|---|---|---|
| 26 | `mtc_backtest` | `# ─── Sys path: resolve mtc_backtest as package root ──────────────────────────` | `MTC_COMMAND_CENTER\02_MTC_BACKTEST` |
| 28 | `mtc_backtest` | `MTC_ROOT  = REPO_ROOT / "mtc_backtest"` | `MTC_COMMAND_CENTER\02_MTC_BACKTEST` |
| 45 | `110_MTC_BACKTEST_OPTİMİZASYON_DİZİNLERİ` | `REPO_ROOT / "110_MTC_BACKTEST_OPTİMİZASYON_DİZİNLERİ/data/processed_hist/binance_usdm/BTCUSDT.P/1h.parquet",` | `MTC_COMMAND_CENTER\02_MTC_BACKTEST\data\optimization` |

## parity_compare.py
| Line | Matched path | Current text | Proposed clean mapping |
|---|---|---|---|
| 24 | `01_MASTER TEMPLATE_V2` | `V2_PYTHON_ROOT = REPO_ROOT / "01_MASTER TEMPLATE_V2/00_PYTHON"` | `MTC_COMMAND_CENTER\01_MTC_PROJECT` |
| 25 | `01_MASTER TEMPLATE_V2` | `PINE_SOURCE = REPO_ROOT / "01_MASTER TEMPLATE_V2/01_PINE/MTC_V2.pine"` | `MTC_COMMAND_CENTER\01_MTC_PROJECT` |
| 26 | `01_MASTER TEMPLATE_V2` | `TRACKER_WORKBOOK_PATH = REPO_ROOT / "01_MASTER TEMPLATE_V2/05_PARITY/MTC_V2_PARITY_CASE_TRACKER.xlsx"` | `MTC_COMMAND_CENTER\01_MTC_PROJECT` |
| 27 | `01_MASTER TEMPLATE_V2` | `TRACKER_WORKBOOK_FALLBACK_PATH = REPO_ROOT / "01_MASTER TEMPLATE_V2/05_PARITY/MTC_V2_PARITY_CASE_TRACKER_close_only_wave1_pending.xlsx"` | `MTC_COMMAND_CENTER\01_MTC_PROJECT` |
| 28 | `01_MASTER TEMPLATE_V2` | `TRACKER_CSV_PATH = REPO_ROOT / "01_MASTER TEMPLATE_V2/05_PARITY/MTC_V2_PARITY_CASES.csv"` | `MTC_COMMAND_CENTER\01_MTC_PROJECT` |
| 1592 | `mtc_backtest` | `help="Optional flat 00_PYTHON config overrides JSON. Legacy nested mtc_backtest cases are not supported.",` | `MTC_COMMAND_CENTER\02_MTC_BACKTEST` |

## Phase 2 QuantLens Addendum

Legacy QuantLens path mapping is separate from the `01_MASTER TEMPLATE_V2` MTC project mapping:

| Legacy source path | Clean target path | Rule |
|---|---|---|
| `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB` | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS` | Rewrite QuantLens references directly to `MTC_COMMAND_CENTER\03_QUANTLENS`; do not inherit the `MTC_COMMAND_CENTER\01_MTC_PROJECT` mapping. |

## Phase 4 Addendum — late-restored root scripts (2026-05-31)

These six scripts were missed by the Phase 0 hardcoded-path scan and copied byte-identical from legacy after the AUTO_002 smoke run. None were rewritten in place; rewrite policy still pending Barış approval.

### parity_test.py
No hardcoded path hits. No rewrite needed.

### run_2025_audit.py
| Line | Matched path | Current text | Proposed clean mapping |
|---|---|---|---|
| 28 | `01_MASTER TEMPLATE_V2` | `V2_PYTHON_ROOT = REPO_ROOT / "01_MASTER TEMPLATE_V2/00_PYTHON"` | `MTC_COMMAND_CENTER\01_MTC_PROJECT` |
| 29 | `01_MASTER TEMPLATE_V2` | `PINE_SOURCE = REPO_ROOT / "01_MASTER TEMPLATE_V2/01_PINE/MTC_V2.pine"` | `MTC_COMMAND_CENTER\01_MTC_PROJECT` |
| 30 | `01_MASTER TEMPLATE_V2` | `TRACKER_WORKBOOK = REPO_ROOT / "01_MASTER TEMPLATE_V2/05_PARITY/MTC_V2_PARITY_CASE_TRACKER.xlsx"` | `MTC_COMMAND_CENTER\01_MTC_PROJECT` |
| 31 | `01_MASTER TEMPLATE_V2` | `TRACKER_CSV = REPO_ROOT / "01_MASTER TEMPLATE_V2/05_PARITY/MTC_V2_PARITY_CASES.csv"` | `MTC_COMMAND_CENTER\01_MTC_PROJECT` |
| 32 | `mtc_backtest` | `DATA_FILE = REPO_ROOT / "mtc_backtest/data/BTCUSDT_1h_20180701_20260308.parquet"` | `MTC_COMMAND_CENTER\02_MTC_BACKTEST\data` |

### RUN_MTC_BACKTEST.ps1
| Line | Matched path | Current text | Proposed clean mapping |
|---|---|---|---|
| 1 | `C:\LAB\tradingview-lab` + `mtc_backtest` | `Set-Location "C:\LAB\tradingview-lab\mtc_backtest"` | `Set-Location "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\02_MTC_BACKTEST"` |

ABSOLUTE legacy path — script will fail outright until rewritten.

### run_pinets.mjs
| Line | Matched path | Current text | Proposed clean mapping |
|---|---|---|---|
| 25 | `01_MASTER TEMPLATE_V2` | `const PINE_PATH = resolve(__dirname, '01_MASTER TEMPLATE_V2/01_PINE/MTC_V2.pine');` | `__dirname/../01_MTC_PROJECT/01_PINE/MTC_V2.pine` (script is now in `02_MTC_BACKTEST/`, so navigate up + sideways) |

### run_tracker_ready_cases.py
| Line | Matched path | Current text | Proposed clean mapping |
|---|---|---|---|
| 10 | `01_MASTER TEMPLATE_V2` | `TRACKER_CSV = REPO_ROOT / "01_MASTER TEMPLATE_V2/05_PARITY/MTC_V2_PARITY_CASES.csv"` | `MTC_COMMAND_CENTER\01_MTC_PROJECT` |

### validate_syntax.mjs
| Line | Matched path | Current text | Proposed clean mapping |
|---|---|---|---|
| 23 | `01_MASTER TEMPLATE_V2` | `const PINE_PATH = resolve(__dirname, '01_MASTER TEMPLATE_V2/01_PINE/MTC_V2.pine');` | `__dirname/../01_MTC_PROJECT/01_PINE/MTC_V2.pine` |
