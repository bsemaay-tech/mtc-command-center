# WAL capture-ordering repair-2 evidence — 2026-08-25

## Scope and authority

- Owner-authorized scope remains the Bridge WAL/SQLite capture tool and its tests, T0 audited, nothing else.
- Repair round: **2 of maximum 3**.
- Branch: `fix/wal-capture-ordering-20260825`.
- Base before Lane W: `46f5bafbf82f3366c8bc7ee08f6f0eee08d46138`.
- Round-1 fix: `4b711d9c` (`fix(bridge-tools): complete WAL capture init before drift boundary (owner-authorized T0)`).
- Repair parent / CI rider: `67a53a32803f2c5e72ca921f23ad62569c284e5d`.
- Writable product/test files: `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` and `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py` only.
- Evidence files: this file and `LANE_REPORT.md` only.
- No trading, Pine, parity, MTC, schema, deployment, host, credential, broker, exchange, or economic surface was changed or contacted.

The repair contract and required findings came from the full Codex xhigh verdict at
`C:\tmp\LANE_PROMPTS_20260824\AUDIT_W_T0_CODEX_RUN.log`.

## Audited range and completed Linux rider

The round-1 audit covered the two Bridge files, these two evidence files, and the CI rider at HEAD `67a53a32`.
The auditor independently verified:

- `test_order_state.py` was unchanged (`b5b6a29e…` before/after).
- `.github/workflows/ci.yml` was the identical `3394d9ff…` blob carried from PR-125.
- GitHub run `32806840756` matched branch `fix/wal-capture-ordering-20260825` and head `67a53a32`.
- Ubuntu used Python `3.12.14` and completed `2 failed, 1356 passed`; only the two explicitly excluded `test_order_state.py` CPython-GC tests failed.

This repair does not claim that prior run as proof for the new unpushed repair commit. The Lead must run fresh Linux CI and both T0 flagship audits after this commit.

## Local environment

```text
python=3.14.2 (tags/v3.14.2:df79316, Dec  5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)]
sqlite=3.50.4
platform=Windows-11-10.0.26200-SP0
```

## Inherited defect reproduced RED before the repair

The auditor's exact real-file attack was added first while the producer was still the inherited HEAD blob `2031c734…`: leave a live WAL/SHM source open, finish the read connection's schema initialization, then change the real SHM mode from `0666` to `0444` before the old caller-side boundary snapshot.

Command:

```powershell
python -m pytest tests/test_wal_state_bundle.py::test_shm_mode_flip_after_read_connection_initializes_fails_closed -q --tb=short -p no:cacheprovider
```

Real RED output:

```text
F                                                                        [100%]
tests\test_wal_state_bundle.py:316: in test_shm_mode_flip_after_read_connection_initializes_fails_closed
    assert rc == 2
E   assert 0 == 2
1 failed in 0.77s
```

The inherited tool therefore returned rc 0 / `CAPTURED` for the demonstrated `0666 -> 0444` SHM attack.

## Repair design and exact surviving effect classes

1. `_connect_readonly(..., capture_boundary=True)` now embeds the source boundary immediately after the fetched schema read and before the connection returns. This removes the old caller-visible post-initialization/pre-snapshot gap.
2. Arrival remains provenance for DB/WAL/SHM and the drift start for DB/WAL. The first authoritative SHM capture boundary is the embedded post-initialization snapshot.
3. An SHM that already exists on arrival is still identity-guarded across initialization. Presence, device, inode, mode, and exact size must remain unchanged; DB and WAL bytes plus every metadata field must be identical. SQLite's initialization may change SHM content hash with consequent mtime/ctime, or advance only its timestamp before the embedded boundary. No identity/presence/size/mode change is tolerated.
4. After the embedded SHM boundary, the only SHM exemption is a content-hash change with consequent mtime/ctime movement while presence, device, inode, mode, and exact size remain unchanged and DB/WAL bytes plus every metadata field are identical. Timestamp-only movement after the boundary is not exempt.
5. A WAL absent at arrival may be materialized only as a stable, regular, zero-byte file whose mode equals the source DB mode. Any wrong mode, nonzero size, within-hash movement, or later metadata change remains drift.
6. The tool docstring names the exact files and effect classes. It no longer falsely claims that SQLite cannot materialize or update sidecars during a read-only connection.

Manifest schema, capture mode, online backup, invariant collection, and trading/Pine/MTC/parity behavior are unchanged.

## Repair-2 attack matrix on the repository producer

Every safety test drives the public `create` CLI seam and asserts rc 2, verdict `INVALID`, `source_changed_during_capture`, the exact changed component, and no retained bundle artifacts.
The mode and empty-WAL permission attacks change the real temporary files. The inode, size, and presence arms inject the corresponding stable filesystem snapshot at the same CLI seam because Windows will not rename or unlink SQLite's mapped SHM; their detector-disabled TEMP mutants prove that each assertion discriminates on that signal.

| Attack | Test node | Repository result |
|---|---|---|
| Auditor's real SHM mode flip `0666 -> 0444` during the minimized initialization interval | `test_shm_mode_flip_after_read_connection_initializes_fails_closed` | `INVALID`, `changed_components=["shm"]` |
| SHM inode swap during initialization | `test_shm_initialization_identity_or_presence_attack_fails_closed[inode_swap]` | `INVALID`, `changed_components=["shm"]` |
| SHM exact-size change during initialization | `test_shm_initialization_identity_or_presence_attack_fails_closed[size_change]` | `INVALID`, `changed_components=["shm"]` |
| SHM deletion during initialization | `test_shm_initialization_identity_or_presence_attack_fails_closed[deletion]` | `INVALID`, `changed_components=["shm"]` |
| SHM deletion then creation after the boundary | `test_shm_deletion_then_creation_after_boundary_fails_closed` | `INVALID`, `changed_components=["shm"]` |
| Empty WAL created at wrong mode (`0666 -> 0444`) | `test_empty_wal_created_with_metadata_drift_fails_closed` | `INVALID`, `changed_components=["wal"]` |
| Exact permitted existing-SHM hash + timestamp self-effect | `test_capture_drift_allows_only_existing_shm_readmark_content_change` | no drift |
| Exact permitted stable zero-byte WAL at DB mode | `test_capture_drift_ignores_read_open_empty_wal_materialization` | no drift |
| Quiesced delayed-attach capture | `test_quiesced_capture_completes_wal_attach_before_drift_boundary` | `CAPTURED`, then `VALID` |

## D026 mutant construction, identities, and exact diffs

Each mutant was a fresh isolated copy of the final producer at
`$env:TEMP\LANE_W_D026_R2_20260825\<name>\tools\wal_state_bundle.py`.
The producer SHA-256 was:

```text
e9bb0ed85238adb04645fc16a75b5e37feb8a18091f6c33c0da6df94ed9bfc7c
```

Construction skeleton actually used:

```powershell
$mutantRoot = Join-Path $env:TEMP 'LANE_W_D026_R2_20260825'
$producer = 'C:\WPPWALFIX_20260825\IBKR_PAPER_BRIDGE\tools\wal_state_bundle.py'
$names = @(
  'ordering_old', 'writer_blind', 'inode_blind', 'mode_blind',
  'sidecar_blind', 'shm_mode_blind', 'shm_inode_blind',
  'shm_presence_blind', 'empty_wal_metadata_blind'
)
foreach ($name in $names) {
  $toolDir = Join-Path $mutantRoot "$name\tools"
  New-Item -ItemType Directory -Path $toolDir | Out-Null
  Copy-Item -LiteralPath $producer -Destination (Join-Path $toolDir 'wal_state_bundle.py')
}
```

The exact changes below were applied to those copies. The post-mutation identities were:

| Mutant | SHA-256 | Disabled signal |
|---|---|---|
| `ordering_old` | `e79d6b48c85daf244c6b893631d74b60622481f558334d97c1566354c10f2d77` | fetched schema initialization |
| `writer_blind` | `c9650983c4c961c36e019af7b2475ca0e51aff0266541f6f7aa35c711a8b9a64` | all capture drift |
| `inode_blind` | `55759e62a6384076aec9f60b1975c4d8e5632b1f8fa82e6e712ff17b5a96ffbc` | inode metadata comparison |
| `mode_blind` | `ab86a6ffb2e829bbad98a092a04743c0bd0ead12448a2129b7216a9f72196345` | permission-mode comparison |
| `sidecar_blind` | `826e05b5d06dc8f01835e70def0fb87ba51da4def3e7ac9580b1a90b58aec2fa` | all SHM component comparison |
| `shm_mode_blind` | `826e05b5d06dc8f01835e70def0fb87ba51da4def3e7ac9580b1a90b58aec2fa` | all SHM comparison for mode attack |
| `shm_inode_blind` | `826e05b5d06dc8f01835e70def0fb87ba51da4def3e7ac9580b1a90b58aec2fa` | all SHM comparison for inode/size attacks |
| `shm_presence_blind` | `826e05b5d06dc8f01835e70def0fb87ba51da4def3e7ac9580b1a90b58aec2fa` | all SHM comparison for presence attack |
| `empty_wal_metadata_blind` | `6bfd4804832e675c034cf7b7d3a23ff1e385f76f878ddfc33ff74031a2440aab` | expected-mode equality for empty WAL |

Exact unique diffs (`sidecar_blind` and the three attack-named SHM mutants intentionally share the same diff and hash):

```diff
# ordering_old
-        conn.execute("SELECT name FROM sqlite_master LIMIT 1").fetchone()
+        conn.execute("SELECT 1")
```

```diff
# writer_blind
 def _capture_changed_components(
     arrival: dict[str, dict[str, Any]],
     before: dict[str, dict[str, Any]],
     after: dict[str, dict[str, Any]],
 ) -> list[str]:
     """Return capture drift once, in deterministic component order."""
+    return []
```

```diff
# inode_blind
     for component in ("db", "wal", "shm"):
+        before_component = json.loads(json.dumps(before[component]))
+        after_component = json.loads(json.dumps(after[component]))
+        for state in (before_component, after_component):
+            for metadata_key in ("metadata_before_hash", "metadata_after_hash"):
+                state.get(metadata_key, {}).pop("inode", None)
         if (
-            before[component] != after[component]
+            before_component != after_component
```

```diff
# mode_blind
     for component in ("db", "wal", "shm"):
+        before_component = json.loads(json.dumps(before[component]))
+        after_component = json.loads(json.dumps(after[component]))
+        for state in (before_component, after_component):
+            for metadata_key in ("metadata_before_hash", "metadata_after_hash"):
+                state.get(metadata_key, {}).pop("mode", None)
         if (
-            before[component] != after[component]
+            before_component != after_component
```

```diff
# sidecar_blind / shm_mode_blind / shm_inode_blind / shm_presence_blind
-    for component in ("db", "wal", "shm"):
+    for component in ("db", "wal"):
```

```diff
# empty_wal_metadata_blind
-        and wal_metadata.get("mode") == database_metadata.get("mode")
+        and wal_metadata.get("mode") is not None
```

The identities and diffs were independently printed with:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath $mutantFile
git diff --no-index --unified=3 -- $producer $mutantFile
```

## D026 RED execution and real output

For each row, `PYTHONPATH` named the isolated mutant first; a separate Python process printed the actual imported file and its SHA-256 before pytest ran.

```powershell
$repoBridge = 'C:\WPPWALFIX_20260825\IBKR_PAPER_BRIDGE'
$testFile = "$repoBridge\tests\test_wal_state_bundle.py"
$neutralCwd = 'C:\tmp'
$cases = @(
  @{Name='ordering_old'; Node='test_quiesced_capture_completes_wal_attach_before_drift_boundary'},
  @{Name='writer_blind'; Node='test_concurrent_writer_during_capture_fails_closed'},
  @{Name='inode_blind'; Node='test_capture_metadata_and_sidecar_drift_fails_closed[inode_replacement]'},
  @{Name='mode_blind'; Node='test_capture_metadata_and_sidecar_drift_fails_closed[permission_mode_change]'},
  @{Name='sidecar_blind'; Node='test_capture_metadata_and_sidecar_drift_fails_closed[sidecar_mutation]'},
  @{Name='shm_mode_blind'; Node='test_shm_mode_flip_after_read_connection_initializes_fails_closed'},
  @{Name='shm_inode_blind'; Node='test_shm_initialization_identity_or_presence_attack_fails_closed[inode_swap]'},
  @{Name='shm_inode_blind'; Node='test_shm_initialization_identity_or_presence_attack_fails_closed[size_change]'},
  @{Name='shm_presence_blind'; Node='test_shm_initialization_identity_or_presence_attack_fails_closed[deletion]'},
  @{Name='shm_presence_blind'; Node='test_shm_deletion_then_creation_after_boundary_fails_closed'},
  @{Name='empty_wal_metadata_blind'; Node='test_empty_wal_created_with_metadata_drift_fails_closed'}
)
foreach ($case in $cases) {
  $mutantDir = Join-Path $mutantRoot $case.Name
  $expectedMutant = (Resolve-Path (Join-Path $mutantDir 'tools\wal_state_bundle.py')).Path
  $env:PYTHONPATH = "$mutantDir;$repoBridge"
  Push-Location $neutralCwd
  try {
    python -c "import hashlib; from pathlib import Path; from tools import wal_state_bundle as wal; actual=Path(wal.__file__).resolve(); expected=Path(r'$expectedMutant').resolve(); assert actual == expected, f'{actual} != {expected}'; print(f'import_asserted={actual} sha256={hashlib.sha256(actual.read_bytes()).hexdigest()}')"
    if ($LASTEXITCODE -ne 0) { throw 'mutant import assertion failed' }
    python -m pytest "$testFile::$($case.Node)" -q --tb=short -p no:cacheprovider
    Write-Output "pytest_rc=$LASTEXITCODE"
  }
  finally {
    Pop-Location
  }
}
```

Real concise output matrix:

| Mutant / node | Real failing observation | rc |
|---|---|---|
| `ordering_old` / quiesced attach | fixed expectation rc 0 saw `INVALID`, changed `wal`/`shm`; `assert 2 == 0` | 1 |
| `writer_blind` / concurrent writer | detector-disabled tool returned capture rc 0; `assert 0 == 2` | 1 |
| `inode_blind` / original inode replacement | detector-disabled tool returned capture rc 0; `assert 0 == 2` | 1 |
| `mode_blind` / original permission change | detector-disabled tool returned capture rc 0; `assert 0 == 2` | 1 |
| `sidecar_blind` / original sidecar mutation | detector-disabled tool returned capture rc 0; `assert 0 == 2` | 1 |
| `shm_mode_blind` / real SHM `0666 -> 0444` | detector-disabled tool returned capture rc 0; `assert 0 == 2` | 1 |
| `shm_inode_blind` / initialization inode swap | detector-disabled tool returned capture rc 0; `assert 0 == 2` | 1 |
| `shm_inode_blind` / initialization size change | detector-disabled tool returned capture rc 0; `assert 0 == 2` | 1 |
| `shm_presence_blind` / initialization deletion | detector-disabled tool returned capture rc 0; `assert 0 == 2` | 1 |
| `shm_presence_blind` / deletion then creation | detector-disabled tool returned capture rc 0; `assert 0 == 2` | 1 |
| `empty_wal_metadata_blind` / wrong-mode empty WAL | detector-disabled tool returned capture rc 0; `assert 0 == 2` | 1 |

Every run printed the matching `$env:TEMP\LANE_W_D026_R2_20260825\...\wal_state_bundle.py` import and the SHA-256 listed above. All eleven tests were RED for the intended behavior: the old ordering rejected a quiesced capture, while every disabled safety detector falsely returned rc 0.

## D026 GREEN on the repository producer

The same eleven nodes — the original five plus six repair-2 attack arms — were run against the repository producer:

```text
...........                                                              [100%]
11 passed in 1.76s
```

The quiesced node asserts create rc 0 / `CAPTURED`, then verify rc 0 / `VALID`. Every safety node asserts rc 2 / `INVALID` / `source_changed_during_capture` and no retained bundle database or manifest.

## Full local verification

```powershell
python -m pytest tests/test_wal_state_bundle.py -q --ignore=TSP1009B.pytest_tmp_s1r1
```

```text
......................................................                   [100%]
54 passed in 6.24s
full_rc=0
```

```powershell
python -m compileall -q tools/wal_state_bundle.py tests/test_wal_state_bundle.py
```

```text
compileall_rc=0
```

```powershell
git diff --check
```

```text
(no output)
diff_check_rc=0
```

No lint PASS is claimed because Ruff is not installed in this interpreter.

## Implementer verdict and remaining acceptance work

Gate 4 self-QA: **PASS on Windows**, including D026 RED/GREEN and the full scoped WAL suite. This is not final T0 acceptance. The Claude Lead must independently inspect the actual commit, run fresh Linux CI for the repair SHA, and complete the required `claude-opus-5` xhigh plus `gpt-5.6-sol` xhigh reviews within the T0 round cap.
