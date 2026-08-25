# WAL capture-ordering fix evidence — 2026-08-25

## Scope and authority

- Owner authorization: "I authorize the WAL state-bundle capture-ordering fix: the Bridge's WAL/SQLite capture tool and its tests, T0 audited, nothing else."
- Audit tier: **T0** — protected Bridge persistence/cutover tooling on the Linux deployment path.
- Branch: `fix/wal-capture-ordering-20260825`.
- Base: `46f5bafbf82f3366c8bc7ee08f6f0eee08d46138`.
- Writable product/test files: `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` and `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py` only.
- Evidence files: this file and `LANE_REPORT.md` only.
- Explicit exclusion: the two CPython-GC failures in `test_order_state.py` were not edited.

The merged diagnosis was read from
`origin/feature/wp-p0-27-ci-home-20260825:MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/LINUX_RED_DIAGNOSIS.md`.

## Environment and honest proof boundary

```text
python=3.14.2 (tags/v3.14.2:df79316, Dec  5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)]
sqlite=3.50.4
platform=Windows-11-10.0.26200-SP0
```

Windows does not naturally reproduce the Linux/SQLite ordering defect. The focused test emulates the diagnosed deployment behavior through SQLite's authorizer: constant expressions do not mark a main-database read, while a schema-table read does. Ubuntu CI after the candidate commit is the Lead's required platform proof; it was not available or claimed in this implementer lane.

## Fix design

1. Before SQLite connects to a source with a non-empty WAL, a read-only preflight requires a regular, readable, whole-region SHM whose duplicated WAL-index header is initialized, version-valid, checksum-valid, and salt-linked to that exact WAL. Missing, truncated, zero-filled, or unrelated SHM state fails before any SQLite connection can rebuild it.
2. `_connect_readonly()` executes and fetches `SELECT name FROM sqlite_master LIMIT 1` before returning. This completes main-database/WAL attachment before `source_snapshot_before` opens the drift boundary.
3. The drift detector itself is unchanged. DB/WAL/SHM snapshots still compare presence, device, inode, permission mode, size, mtime, ctime, SHA-256, and within-hash metadata movement. No new exemption or platform conditional was added.
4. Manifest schema, capture mode, invariant collection, online backup, and trading/Pine/MTC/parity behavior are unchanged.

## Pre-edit Windows baseline

Command:

```powershell
cd C:\WPPWALFIX_20260825\IBKR_PAPER_BRIDGE
python -m pytest tests/test_wal_state_bundle.py -q --ignore=TSP1009B.pytest_tmp_s1r1
```

Output:

```text
.........................................                                [100%]
41 passed in 7.10s
```

This is compatibility baseline evidence only; it is not Linux defect-closure evidence.

## D026 mutant definitions

Each mutant is an isolated copy under `$env:TEMP\LANE_W_D026_20260825\<name>\tools\wal_state_bundle.py`. Every run printed `wal.__file__` first, proving that pytest imported the mutant rather than the repository producer.

| Mutant | Deliberately disabled behavior |
|---|---|
| `ordering_old` | Replaced the fetched schema read with the old `conn.execute("SELECT 1")`. |
| `writer_blind` | Forced `_capture_changed_components()` to return `[]`. |
| `inode_blind` | Removed `inode` from compared before/after snapshot metadata. |
| `mode_blind` | Removed `mode` from compared before/after snapshot metadata. |
| `sidecar_blind` | Removed `shm` from `_changed_snapshot_components()` iteration. |

The executed command loop was:

```powershell
$repoBridge = 'C:\WPPWALFIX_20260825\IBKR_PAPER_BRIDGE'
$testFile = "$repoBridge\tests\test_wal_state_bundle.py"
$cases = @(
  @{Name='ordering_old'; Node='test_quiesced_capture_completes_wal_attach_before_drift_boundary'},
  @{Name='writer_blind'; Node='test_concurrent_writer_during_capture_fails_closed'},
  @{Name='inode_blind'; Node='test_capture_metadata_and_sidecar_drift_fails_closed[inode_replacement]'},
  @{Name='mode_blind'; Node='test_capture_metadata_and_sidecar_drift_fails_closed[permission_mode_change]'},
  @{Name='sidecar_blind'; Node='test_capture_metadata_and_sidecar_drift_fails_closed[sidecar_mutation]'}
)
foreach ($case in $cases) {
  Write-Output "MUTANT=$($case.Name)"
  $env:PYTHONPATH = "$env:TEMP\LANE_W_D026_20260825\$($case.Name);$repoBridge"
  python -c "from tools import wal_state_bundle as wal; print(wal.__file__)"
  python -m pytest "$testFile::$($case.Node)" -q --tb=line -p no:cacheprovider
  Write-Output "pytest_rc=$LASTEXITCODE"
}
```

Complete concise output, with the expanded user TEMP prefix normalized back to `$env:TEMP`:

```text
MUTANT=ordering_old
$env:TEMP\LANE_W_D026_20260825\ordering_old\tools\wal_state_bundle.py
F                                                                        [100%]
E   AssertionError: {... 'changed_components': ['wal', 'shm'], ... 'exit_code': 2, 'failures': ['source_changed_during_capture'], 'verdict': 'INVALID'}
    assert 2 == 0
FAILED ...::test_quiesced_capture_completes_wal_attach_before_drift_boundary
1 failed in 0.62s
pytest_rc=1

MUTANT=writer_blind
$env:TEMP\LANE_W_D026_20260825\writer_blind\tools\wal_state_bundle.py
F                                                                        [100%]
E   assert 0 == 2
FAILED ...::test_concurrent_writer_during_capture_fails_closed
1 failed in 0.81s
pytest_rc=1

MUTANT=inode_blind
$env:TEMP\LANE_W_D026_20260825\inode_blind\tools\wal_state_bundle.py
F                                                                        [100%]
E   assert 0 == 2
FAILED ...::test_capture_metadata_and_sidecar_drift_fails_closed[inode_replacement]
1 failed in 1.24s
pytest_rc=1

MUTANT=mode_blind
$env:TEMP\LANE_W_D026_20260825\mode_blind\tools\wal_state_bundle.py
F                                                                        [100%]
E   assert 0 == 2
FAILED ...::test_capture_metadata_and_sidecar_drift_fails_closed[permission_mode_change]
1 failed in 0.90s
pytest_rc=1

MUTANT=sidecar_blind
$env:TEMP\LANE_W_D026_20260825\sidecar_blind\tools\wal_state_bundle.py
F                                                                        [100%]
E   assert 0 == 2
FAILED ...::test_capture_metadata_and_sidecar_drift_fails_closed[sidecar_mutation]
1 failed in 0.98s
pytest_rc=1
```

Interpretation:

- The old ordering makes the quiesced emulation fail exactly as diagnosed: rc 2, `INVALID`, changed WAL/SHM.
- Each fail-closed test becomes RED when its specific detection signal is removed; without detection the tool returns rc 0, which the test rejects.

## D026 GREEN on repository producer

Command:

```powershell
cd C:\WPPWALFIX_20260825\IBKR_PAPER_BRIDGE
python -m pytest `
  tests/test_wal_state_bundle.py::test_quiesced_capture_completes_wal_attach_before_drift_boundary `
  tests/test_wal_state_bundle.py::test_concurrent_writer_during_capture_fails_closed `
  "tests/test_wal_state_bundle.py::test_capture_metadata_and_sidecar_drift_fails_closed[inode_replacement]" `
  "tests/test_wal_state_bundle.py::test_capture_metadata_and_sidecar_drift_fails_closed[permission_mode_change]" `
  "tests/test_wal_state_bundle.py::test_capture_metadata_and_sidecar_drift_fails_closed[sidecar_mutation]" `
  -q --tb=line -p no:cacheprovider
```

Output:

```text
.....                                                                    [100%]
5 passed in 1.39s
focused_rc=0
```

The quiesced node asserts create rc 0 / `CAPTURED`, then verify rc 0 / `VALID`. The four safety nodes assert rc 2 / `source_changed_during_capture` and that neither bundle database nor manifest remains.

## Full local verification

Command and output:

```powershell
python -m pytest tests/test_wal_state_bundle.py -q --ignore=TSP1009B.pytest_tmp_s1r1
```

```text
................................................                         [100%]
48 passed in 9.23s
full_rc=0
```

```powershell
python -m compileall -q tools/wal_state_bundle.py tests/test_wal_state_bundle.py
```

```text
compileall_rc=0
```

```powershell
python -m ruff check tools/wal_state_bundle.py tests/test_wal_state_bundle.py
```

```text
C:\Python314\python.exe: No module named ruff
ruff_rc=1
```

Ruff is not installed in this interpreter, so no lint PASS is claimed.

```powershell
git diff --check
```

```text
diff_check_rc=0
```

## Implementer verdict and remaining acceptance work

Gate 4 self-QA: **PASS on Windows**, with D026 RED/GREEN demonstrated. Regression risk is concentrated in SQLite WAL-index format compatibility and platform-specific sidecar timing; the preflight uses SQLite's stable WAL/WAL-index header contract and accepts a genuine live Store WAL/SHM pair in the full test file.

This is not final T0 acceptance. The Lead must run Ubuntu CI on the committed branch and complete the required independent `claude-opus-5` xhigh plus `gpt-5.6-sol` xhigh reviews. No push, merge, deployment, host contact, broker action, ARM, order, TESTNET/mainnet, Pine, parity, MTC, schema, or `test_order_state.py` change occurred in this lane.
