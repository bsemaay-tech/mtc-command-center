# WP-P0-08 Search Log

Date: 2026-08-25

Worktree: `C:\WPP008_20260825`

Branch: `feature/wp-p0-08-writer-inventory-20260825`

Starting HEAD: `0aa57ef66aa66999b6cac8e368095ca51a3d1d18`

## Method

The search was intentionally sink-first. It did not begin with known writer names such as `all_trials` or `trials.append`, because the master brief records that such a self-confirming grep missed real writers (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:400-414`).

Search roots:

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools`
- `MTC_COMMAND_CENTER/03_QUANTLENS/research`

Source extensions: `*.py`, `*.ps1`, `*.sh`, `*.js`, `*.ts`.

The inventory used four passes:

1. Enumerate every source file with `rg --files`.
2. Find generic persistence sinks without assuming an artifact name: pandas/columnar writers, CSV/JSON writers, SQLite/DuckDB connections, path writes and stream writes.
3. Cross-check the sink set against semantic terms (`trial`, `evaluation`, `trade`, `result`, `parameter_sweep`, walk-forward, equity, `run_id`) and separately search structured artifact extensions/names.
4. Read each surviving candidate at its record-construction and write sites; classify report/spec/registry/dataset/progress/test-only false positives explicitly.

## Commands and observed output

### 1. Enumerate the two source roots

```powershell
$tool = @(rg --files 'MTC_COMMAND_CENTER/03_QUANTLENS/tools' -g '*.py' -g '*.ps1' -g '*.sh' -g '*.js' -g '*.ts')
$research = @(rg --files 'MTC_COMMAND_CENTER/03_QUANTLENS/research' -g '*.py' -g '*.ps1' -g '*.sh' -g '*.js' -g '*.ts')
"RG_TOOLS_SOURCE_FILES=$($tool.Count)"
"RG_RESEARCH_SOURCE_FILES=$($research.Count)"
```

Observed:

```text
RG_TOOLS_SOURCE_FILES=118
RG_RESEARCH_SOURCE_FILES=172
```

### 2. Generic sink and semantic intersection

```powershell
$sink = 'to_csv|to_json|to_parquet|to_sql|write_csv|write_json|write_parquet|sqlite3\.connect|duckdb\.connect|csv\.(writer|DictWriter)|json\.dump|write_text|write_bytes|\.write\('
$sem = 'trial|evaluation|trade|result|parameter[_ -]?sweep|walk.?forward|equity|run_id'
$toolSink = @(rg -l -i --glob '*.py' --glob '*.ps1' --glob '*.sh' --glob '*.js' --glob '*.ts' $sink 'MTC_COMMAND_CENTER/03_QUANTLENS/tools')
$resSink = @(rg -l -i --glob '*.py' --glob '*.ps1' --glob '*.sh' --glob '*.js' --glob '*.ts' $sink 'MTC_COMMAND_CENTER/03_QUANTLENS/research')
$toolSem = @(rg -l -i --glob '*.py' --glob '*.ps1' --glob '*.sh' --glob '*.js' --glob '*.ts' $sem 'MTC_COMMAND_CENTER/03_QUANTLENS/tools')
$resSem = @(rg -l -i --glob '*.py' --glob '*.ps1' --glob '*.sh' --glob '*.js' --glob '*.ts' $sem 'MTC_COMMAND_CENTER/03_QUANTLENS/research')
$toolBoth = @($toolSink | Where-Object { $toolSem -contains $_ })
$resBoth = @($resSink | Where-Object { $resSem -contains $_ })
```

Observed:

```text
TOOLS_SINK_FILES=58
RESEARCH_SINK_FILES=39
TOOLS_SINK_AND_SEMANTIC_FILES=51
RESEARCH_SINK_AND_SEMANTIC_FILES=36
```

The 87-file intersection was a candidate set, not the answer. Manual source inspection removed report-only, registry, dataset, selection, test-fixture and intake/audit-administration false positives; these classes are accounted for in `WRITER_INVENTORY.md`.

### 3. Structured artifact-name cross-check

```powershell
rg -n -i --glob '*.py' \
  'trades?\.(csv|json|jsonl|parquet)|results?\.(csv|json|jsonl|parquet)|evaluations?\.(csv|json|jsonl|parquet)|trials?\.(csv|json|jsonl|parquet)|run_status\.json|best_params|params_json|trades_for_strategy' \
  'MTC_COMMAND_CENTER/03_QUANTLENS/tools' \
  'MTC_COMMAND_CENTER/03_QUANTLENS/research'
```

This independently exposed the legacy `parameter_sweep.csv`, `trades.csv`, `results.csv`, `all_evaluations.csv`, scorecard and audit-result families. It also verified the five examples already named by the brief and found additional writers without relying on those names.

### 4. Exact target-field cross-check

An AST-based read-only scan compared string keys in each sink-bearing Python file with the §11.2 field set. It confirmed that current files contain isolated aliases such as `candidate_id`, `classification`, `fold_test_sharpes`, `dsr_p_value`, `bh_fdr_survivor`, `pbo` and `excess_alpha`, but no file contains and persists the complete identity/search/lineage set. A separate sink search found no existing `to_parquet`, DuckDB or SQLite trial-catalog writer.

## Capability self-test: unknown planted writer

The acceptance test planted a temporary source file inside this package directory. It was deliberately absent from every known-writer list and contained two generic persistence mechanisms:

```python
def persist_surprise_trial_ledger(frame) -> None:
    frame.to_parquet(Path("surprise_trial_ledger.parquet"), index=False)
    sqlite3.connect("surprise_trial_ledger.sqlite").close()
```

The same generic sink sweep was run over the real toolchain plus the package directory:

```powershell
rg -n -i --glob '*.py' --glob '*.ps1' --glob '*.sh' --glob '*.js' --glob '*.ts' \
  'to_csv|to_json|to_parquet|to_sql|write_csv|write_json|write_parquet|sqlite3\.connect|duckdb\.connect|csv\.(writer|DictWriter)|json\.dump|write_text|write_bytes|\.write\(' \
  'MTC_COMMAND_CENTER/03_QUANTLENS' \
  'MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25' |
  rg 'wp_p0_08_discovery_probe\.py'
```

Observed output:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25\wp_p0_08_discovery_probe.py:8:    frame.to_parquet(Path("surprise_trial_ledger.parquet"), index=False)
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25\wp_p0_08_discovery_probe.py:9:    sqlite3.connect("surprise_trial_ledger.sqlite").close()
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
