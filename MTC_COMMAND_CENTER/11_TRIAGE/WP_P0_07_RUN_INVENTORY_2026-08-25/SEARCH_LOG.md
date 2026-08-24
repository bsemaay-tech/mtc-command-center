# Search Log — WP-P0-07

## Boundary

- Worktree: `C:\WPP007_20260825`
- Branch: `feature/wp-p0-07-run-inventory-20260825`
- Audit tier: **T2**
- Read scope: this worktree only.
- Write scope: this package directory only.
- No network, Docker/WSL, other AI CLI, backtest, optimization, engine import, or research artefact generation was used.

Commands below are PowerShell unless shown otherwise. Python was used only as a read-only standard-library JSON parser after the full PowerShell parse exceeded 30 seconds; it did not import or execute repository code.

## 1. Orientation and named-source sweep

```powershell
git status --short --branch
git branch --show-current
git rev-parse HEAD
rg -n --hidden --glob '!\.git/**' --glob '*.md' 'WP-P0-07|O-14|zero strict survivors|F-22' MTC_COMMAND_CENTER
```

Observed start: clean branch `feature/wp-p0-07-run-inventory-20260825` at `0aa57ef66aa66999b6cac8e368095ca51a3d1d18`.

The lane prompt named `05_BACKTEST_RESULTS/` without the `03_QUANTLENS/` prefix. Directory discovery corrected the physical path:

```powershell
Get-ChildItem -LiteralPath 'MTC_COMMAND_CENTER' -Directory -Recurse -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match '^(05_BACKTEST_RESULTS|research)$' -or $_.Name -match 'BACKTEST_RESULTS' }
```

Result roots:

- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS`
- `MTC_COMMAND_CENTER/03_QUANTLENS/research`

Registry reads:

```powershell
Get-Content -Raw MTC_COMMAND_CENTER/05_REGISTRY/RESEARCH_RUN_REGISTRY.json
Get-Content -Raw MTC_COMMAND_CENTER/05_REGISTRY/RESEARCH_BACKTEST_REGISTRY.json
Get-Content -Raw MTC_COMMAND_CENTER/05_REGISTRY/VARIANT_LOG_REGISTRY.json
```

Observed: six run-level registry entries; the backtest registry has `generated_at: null` and `results: []`.

## 2. Physical-tree and record-path discovery

Immediate research-directory enumeration:

```powershell
Get-ChildItem -LiteralPath 'MTC_COMMAND_CENTER/03_QUANTLENS/research' -Directory
```

Run/result path discovery across tracked records:

```powershell
rg -o --no-filename --glob '*.md' --glob '*.json' --glob '*.csv' `
  '03_QUANTLENS[/\\]05_BACKTEST_RESULTS[/\\][A-Za-z0-9_.-]+' MTC_COMMAND_CENTER |
  Sort-Object -Unique
```

This surfaced historical run IDs absent from the six-entry registry, including the enrichment chain, confirmation runs, template runs, full sweeps, night loops, and resilient/archetype families.

Path-independent run-tree discovery:

```powershell
Get-ChildItem -LiteralPath 'MTC_COMMAND_CENTER/03_QUANTLENS/tools' -Directory -Recurse |
  Where-Object { $_.Name -match '(?i)run|result' } |
  Select-Object FullName
```

Unprompted trees found:

- `tools/night_runs`
- `tools/overnight_runs`
- `tools/smoke_runs`
- `tools/sprint_runs`

This is the required real-world proof that the enumeration finds recorded evidence it was not told about. The first three hold final result files; `sprint_runs/cpcv_input_top_alpha.json` is a derived 13-row result selection rather than an independent run.

## 3. Complete parse of directly available final JSONs

The PowerShell `ConvertFrom-Json` pass over the large corpus exceeded the 30-second command ceiling. The replacement parser was bounded to the exact discovered roots and read only `results` arrays:

```powershell
@'
import json
from pathlib import Path

roots = [
    Path(r'MTC_COMMAND_CENTER/03_QUANTLENS/tools/overnight_runs'),
    Path(r'MTC_COMMAND_CENTER/03_QUANTLENS/tools/night_runs'),
    Path(r'MTC_COMMAND_CENTER/03_QUANTLENS/tools/smoke_runs'),
    Path(r'MTC_COMMAND_CENTER/03_QUANTLENS/research'),
]

records = []
for root in roots:
    for path in root.rglob('*.json'):
        if root.name == 'research' and path.name != 'MEGA_walk_forward_results.json':
            continue
        if path.name == 'MEGA_walk_forward_partial.json':
            continue
        try:
            payload = json.loads(path.read_text(encoding='utf-8'))
        except Exception:
            continue
        rows = payload.get('results') if isinstance(payload, dict) else None
        if not isinstance(rows, list):
            continue
        trials = [row.get('trial_count') for row in rows
                  if isinstance(row, dict) and isinstance(row.get('trial_count'), (int, float))]
        records.append({
            'path': path.as_posix(),
            'generated_utc': payload.get('generated_utc'),
            'rows': len(rows),
            'trial_rows': len(trials),
            'trial_sum': sum(trials),
            'strict_present': sum(isinstance(row, dict) and 'robust_final' in row for row in rows),
            'strict_survivors': sum(isinstance(row, dict) and row.get('robust_final') is True for row in rows),
        })

print(len(records))
print(sum(record['strict_survivors'] for record in records))
'@ | python -
```

Verbatim aggregate output:

```text
67
0
```

Grouped verification:

| File group | Files | Rows/file | Rows with `robust_final` | Recorded trials/file | `robust_final=true`/file |
|---|---:|---:|---:|---:|---:|
| `tools/overnight_runs` | 21 | 3,315 | 3,315 | 144,725 | 0 |
| `tools/night_runs` broad iterations | 41 | 3,655 | 3,655 | 163,679 | 0 |
| `tools/night_runs/confirm_2026-06-04` | 1 | 306 | 306 | 3,672 | 0 |
| final smoke result | 1 | 1 | 1 | 64 | 0 |
| FAZ3B pass 1 (10m) | 1 | 420 | 420 | 7,371 | 0 |
| FAZ3B pass 2 (1h) | 1 | 560 | 560 | 9,828 | 0 |
| Donchian ladder | 1 | 4 | 4 | 240 | 0 |

Every final-file result row has an explicit `robust_final` field; zero is not inferred from a missing key. The excluded smoke `MEGA_walk_forward_partial.json` is the same one-row in-progress record immediately preceding the final smoke result, not another completed run.

Derived sprint input check:

```text
path: tools/sprint_runs/cpcv_input_top_alpha.json
rows: 13
sum(results[*].trial_count): 572
rows with robust_final: 13
robust_final=true: 0
generated_utc: UNKNOWN — field absent
note: Filtered: top alpha cells for CPCV
```

## 4. Registry-path presence check

```powershell
$reg = Get-Content -Raw MTC_COMMAND_CENTER/05_REGISTRY/RESEARCH_RUN_REGISTRY.json | ConvertFrom-Json
$reg.research_runs | ForEach-Object {
  [pscustomobject]@{
    id = $_.research_run_id
    path = $_.run_dir
    present = Test-Path -LiteralPath ('MTC_COMMAND_CENTER/' + $_.run_dir)
  }
}
```

Present: FAZ3B and Donchian. Absent: multi-asset, Turtle, `overnight_full`, and archetypes. The physical `05_BACKTEST_RESULTS` tree contains one tracked derived profile JSON only.

## 5. Enumeration self-test (RED then GREEN)

A temporary nested file was added only under this lane directory:

`__enumeration_self_test__/UNANNOUNCED_RESULT_RECORD_7F3A.json`

The search was given neither that directory nor full filename.

### RED — default file discovery was incomplete

```powershell
$hits = rg --files MTC_COMMAND_CENTER |
  Where-Object { $_ -match '(?i)(run|result).*\.json$' }
$self = $hits | Where-Object { $_ -match '__enumeration_self_test__' }
```

Observed: `self_test_hits = 0`. Default `rg --files` respected ignore rules and missed the planted artefact.

### GREEN — ignore-independent discovery

```powershell
$hits = @(rg --files --hidden --no-ignore MTC_COMMAND_CENTER |
  Where-Object { $_ -match '(?i)(run|result).*\.json$' })
$self = @($hits | Where-Object { $_ -match '__enumeration_self_test__' })
[pscustomobject]@{
  candidate_count = $hits.Count
  self_test_hits = $self.Count
  found_path = ($self -join '; ')
}
```

Verbatim output:

```json
{
  "candidate_count": 386,
  "self_test_hits": 1,
  "found_path": "MTC_COMMAND_CENTER\\11_TRIAGE\\WP_P0_07_RUN_INVENTORY_2026-08-25\\__enumeration_self_test__\\UNANNOUNCED_RESULT_RECORD_7F3A.json"
}
```

The temporary file was then deleted. Verification output:

```json
{
  "temp_file_exists": false,
  "temp_dir_file_count": 0
}
```

## 6. Sampling rule

No directly available final result JSON was sampled: all 67 were parsed. Large Markdown/CSV legacy trees were handled systematically by top-level run directory and authoritative summary/report filenames rather than by reading every candidate-level report. When a legacy report did not expose configuration count, engine version, or the current strict-survivor field, the inventory records `UNKNOWN — <searched locations>`.
