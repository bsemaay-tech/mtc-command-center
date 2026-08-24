# WP-P0-08 Search Log

Date: 2026-08-25

Worktree: `C:\WPP008_20260825`

Branch: `feature/wp-p0-08-writer-inventory-20260825`

Starting HEAD: `0aa57ef66aa66999b6cac8e368095ca51a3d1d18`

## Method

The search was intentionally sink-first. It did not begin with known writer names such as `all_trials` or `trials.append`, because the master brief records that such a self-confirming grep missed real writers (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:400-414`).

Search root: all source trees under `MTC_COMMAND_CENTER/03_QUANTLENS/`:

- `tools/`
- `research/`
- `04_PYTHON_PROTOTYPES/`
- `strategies/`

Source extensions: `*.py`, `*.ps1`, `*.sh`, `*.js`, `*.ts`.

The inventory used four passes:

1. Enumerate every source file with `rg --files`.
2. Find generic persistence sinks without assuming an artifact name: pandas/columnar writers, CSV/JSON writers, SQLite/DuckDB connections, path writes and stream writes.
3. Cross-check the sink set against semantic terms (`trial`, `evaluation`, `trade`, `result`, `parameter_sweep`, walk-forward, equity, `run_id`) and separately search structured artifact extensions/names.
4. Read each surviving candidate at its record-construction and write sites; classify report/spec/registry/dataset/progress/test-only false positives explicitly.

## Commands and observed output

### 1. Enumerate the complete QuantLens source root

```powershell
$root = 'MTC_COMMAND_CENTER/03_QUANTLENS'
$source = @(rg --files $root -g '*.py' -g '*.ps1' -g '*.sh' -g '*.js' -g '*.ts')
"RG_ALL_SOURCE_FILES=$($source.Count)"
$source | ForEach-Object {
    $rel = $_ -replace '^MTC_COMMAND_CENTER[\\/]03_QUANTLENS[\\/]',''
    ($rel -split '[\\/]')[0]
} | Group-Object | Sort-Object Name | ForEach-Object { "$($_.Name)=$($_.Count)" }
```

Observed:

```text
RG_ALL_SOURCE_FILES=389
04_PYTHON_PROTOTYPES=20
research=172
strategies=79
tools=118
```

### 2. Generic sink and semantic intersection

```powershell
$sink = 'to_csv|to_json|to_parquet|to_sql|write_csv|write_json|write_parquet|sqlite3\.connect|duckdb\.connect|csv\.(writer|DictWriter)|json\.dump|write_text|write_bytes|\.write\('
$sem = 'trial|evaluation|trade|result|parameter[_ -]?sweep|walk.?forward|equity|run_id'
$sinkFiles = @(rg -l -i --glob '*.py' --glob '*.ps1' --glob '*.sh' --glob '*.js' --glob '*.ts' $sink $root)
$semanticFiles = @(rg -l -i --glob '*.py' --glob '*.ps1' --glob '*.sh' --glob '*.js' --glob '*.ts' $sem $root)
$both = @($sinkFiles | Where-Object { $semanticFiles -contains $_ })
"SINK_FILES=$($sinkFiles.Count)"
"SEMANTIC_FILES=$($semanticFiles.Count)"
"SINK_AND_SEMANTIC_FILES=$($both.Count)"
$sinkFiles | ForEach-Object {
    $rel = $_ -replace '^MTC_COMMAND_CENTER[\\/]03_QUANTLENS[\\/]',''
    ($rel -split '[\\/]')[0]
} | Group-Object | Sort-Object Name | ForEach-Object { "SINK_TREE_$($_.Name)=$($_.Count)" }
$both | ForEach-Object {
    $rel = $_ -replace '^MTC_COMMAND_CENTER[\\/]03_QUANTLENS[\\/]',''
    ($rel -split '[\\/]')[0]
} | Group-Object | Sort-Object Name | ForEach-Object { "BOTH_TREE_$($_.Name)=$($_.Count)" }
```

Observed:

```text
SINK_FILES=101
SEMANTIC_FILES=150
SINK_AND_SEMANTIC_FILES=90
SINK_TREE_04_PYTHON_PROTOTYPES=1
SINK_TREE_research=39
SINK_TREE_strategies=3
SINK_TREE_tools=58
BOTH_TREE_04_PYTHON_PROTOTYPES=1
BOTH_TREE_research=36
BOTH_TREE_strategies=2
BOTH_TREE_tools=51
```

The 90-file intersection was a candidate set, not the answer. Manual source inspection removed report-only, registry, dataset, selection, test-fixture and intake/audit-administration false positives; these classes are accounted for in `WRITER_INVENTORY.md`. The one sink-bearing strategy helper omitted from the semantic intersection was followed to its three call sites and accounted with the STG046 harness writer.

The widened roots added exactly four sink-bearing files beyond the original `tools/` and `research/` set:

- `04_PYTHON_PROTOTYPES/QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK_prototype.py` — inventory row;
- `strategies/STG046_qlr_r215f4fj7v8/python_visual_backtest_harness.py` — inventory row;
- `strategies/STG046_qlr_r215f4fj7v8/python_signal_model.py` — generic helper accounted with its harness caller;
- `strategies/STG002_ql_alpha_link_8ema_1h/compare_link_pinets_parity.py` — named parity/system-test exclusion.

No other prototype or strategy source file matched the sink pattern, so there is no unaccounted sibling writer of either shape.

### 3. Structured artifact-name cross-check

```powershell
rg -n -i --glob '*.py' \
  'trades?\.(csv|json|jsonl|parquet)|results?\.(csv|json|jsonl|parquet)|evaluations?\.(csv|json|jsonl|parquet)|trials?\.(csv|json|jsonl|parquet)|run_status\.json|best_params|params_json|trades_for_strategy' \
  'MTC_COMMAND_CENTER/03_QUANTLENS'
```

This independently exposed the legacy `parameter_sweep.csv`, `trades.csv`, `results.csv`, `all_evaluations.csv`, scorecard and audit-result families, plus the prototype `*_results.json`, STG046 debug CSVs and STG002 parity result in the widened roots. It also verified the five examples already named by the brief and found additional writers without relying on those names.

### 4. Exact target-field cross-check

An AST-based read-only scan compared string keys in each sink-bearing Python file with the §11.2 field set. It confirmed that current files contain isolated aliases such as `candidate_id`, `classification`, `fold_test_sharpes`, `dsr_p_value`, `bh_fdr_survivor`, `pbo` and `excess_alpha`, but no file contains and persists the complete identity/search/lineage set. A separate sink search found no existing `to_parquet`, DuckDB or SQLite trial-catalog writer.

## Capability self-test: unknown planted writer

The acceptance test planted a temporary source file inside this package directory. It was deliberately absent from every known-writer list and contained two generic persistence mechanisms:

```python
def persist_surprise_trial_ledger(frame) -> None:
    frame.to_parquet(Path("surprise_trial_ledger.parquet"), index=False)
    sqlite3.connect("surprise_trial_ledger.sqlite").close()
```

The same generic sink sweep was re-run over the widened, complete QuantLens source root plus the package directory:

```powershell
rg -n -i --glob '*.py' --glob '*.ps1' --glob '*.sh' --glob '*.js' --glob '*.ts' \
  'to_csv|to_json|to_parquet|to_sql|write_csv|write_json|write_parquet|sqlite3\.connect|duckdb\.connect|csv\.(writer|DictWriter)|json\.dump|write_text|write_bytes|\.write\(' \
  'MTC_COMMAND_CENTER/03_QUANTLENS' \
  'MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25' |
  rg 'wp_p0_08_discovery_probe\.py'
```

Observed output:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25\wp_p0_08_discovery_probe.py:6:    frame.to_parquet(Path("surprise_trial_ledger.parquet"), index=False)
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25\wp_p0_08_discovery_probe.py:7:    sqlite3.connect("surprise_trial_ledger.sqlite").close()
```

The probe was then deleted with `apply_patch`. Verification:

```powershell
Test-Path 'MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/wp_p0_08_discovery_probe.py'
```

Observed:

```text
False
```

The probe does not appear in Git status and will not be staged or committed.

## Search limitations and handling

- Static search cannot prove runtime reachability. This inventory therefore says what source can persist, not which historical command last invoked it.
- Helper functions can obscure the final filename. The sink-first pass followed helper calls such as `save_csv`, `write_json`, `write_text` and atomic writers to their call sites.
- Markdown and JSON serialization can resemble data persistence. Every candidate was inspected at the record-construction site before inclusion.
- Exact cloned writers were not silently collapsed: the three overnight-batch copies were hash-checked and are named together in the inventory; other similar-but-not-identical writers have separate rows.
