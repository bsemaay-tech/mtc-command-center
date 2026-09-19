# Independent T0 Review - WP-P0-26

## Review outcome

The candidate passes every mandated GREEN check and most of the completion-evidence contract, but it has one fail-open integrity defect: `verify_completion_evidence()` authenticates only `file` records while restore later acts on unauthenticated global-manifest `dir` records. An independent arm changed only a directory record in the global manifest; restore returned `0`, created the forged directory, omitted the genuine directory from the digest-bound per-run manifest, and reported `status: ok`. This is a REQUIRED spec finding.

Review counts:

| Axis | REQUIRED | NIT |
|---|---:|---:|
| Standards | 0 | 0 |
| Spec | 1 | 2 |

## Verified identities

- Source worktree: `C:\tmp\P026_REPAIR_20260915`
- Computed candidate HEAD: `2e03a6694c4456ac5066f3789d8a7e049a2f047d`
- Review base: `fcac0ac6`
- Prior docs-only baseline: `e114ed31`
- NIT slice: `505af399`
- `git diff 505af399 2e03a669 --stat` showed exactly one path, `RESTORE_DRILL_EVIDENCE.md`, with 9 deletions. An explicit `git diff 505af399 2e03a669 --` over all seven final subject paths was empty, so the candidate subject bytes are identical to `505af399`.
- `git diff fcac0ac6 2e03a669 --name-status` showed exactly seven modified files and no additions:
  - `MTC_COMMAND_CENTER/tools/opsa/README.md`
  - `MTC_COMMAND_CENTER/tools/opsa/backup.py`
  - `MTC_COMMAND_CENTER/tools/opsa/opsa_common.py`
  - `MTC_COMMAND_CENTER/tools/opsa/restore.py`
  - `MTC_COMMAND_CENTER/tools/opsa/test_opsa.py`
  - `p030_closed_partition_backup_adapter.py`
  - `check_p030_closed_partition_backup_adapter.py`
- No protected path changed. `watchdog.py`, the global manifest record shapes, and the backup CLI are unchanged in this candidate delta.
- Mandated interpreter: `C:\tmp\P020_IMPL_20260912\01a0924d-2c4b-7da1-99e1-24e2a7c7685c\.venv\Scripts\python.exe`, Python `3.12.12`.

Computed SHA-256 values:

| Subject file | SHA-256 |
|---|---|
| `MTC_COMMAND_CENTER/tools/opsa/backup.py` | `01e732150efba155e4ea7a481c97cca340ed8f6801086bf0a3dd0bc647aa01f2` |
| `MTC_COMMAND_CENTER/tools/opsa/restore.py` | `beb8e79063d21adb0429f5d0e58111058887abe6f3b18d5d9b5355c476aa43f6` |
| `MTC_COMMAND_CENTER/tools/opsa/opsa_common.py` | `e2b3d386abdb42852fe005be9ac451bf7f89770d5892ec056c1738f0fd8063e1` |
| `MTC_COMMAND_CENTER/tools/opsa/test_opsa.py` | `c125d536ab0850bbd7b0f50532e8975c3ec8a4eeb4f7782f000586bebd2c8988` |
| `p030_closed_partition_backup_adapter.py` | `60a0e7af31d884ebfa349313cf0795422cb2622ef7325e729389e1b40d51bcd9` |
| `check_p030_closed_partition_backup_adapter.py` | `ef777b3f46aa92b3eb84abe41b87d4d5d36fcbf7499514a5eb4df2fc90324d2a` |

## Clause-by-clause packet conformance

| Clause | Result | Independent evidence |
|---|---|---|
| Successful backup emits immutable per-run `RUN_MANIFEST.jsonl` and `COMPLETE.json` only after readback succeeds | PASS | `backup.py:214-232,240-283` defers completion evidence until `errors` is empty, writes the manifest first, records its SHA-256 in the marker, and makes a failed evidence write force `run_end.status = partial`. Exclusive `xb` creation at `opsa_common.py:153-165` prevents overwrite. GREEN round-trip tests pass. |
| Per-run evidence describes the completed run | PARTIAL / REQUIRED | The marker binds the per-run manifest digest, and file records are compared, but `restore.py:97-103` compares only `file` records. Restore consumes `dir` records from the unbound global manifest at `restore.py:245-251`. The independent directory-mismatch arm demonstrated a successful false reconstruction. |
| Completion artifacts are written atomically | OWNER-RATIFIED DOCUMENTED DEVIATION | `write_once_bytes()` uses direct `open(..., "xb")`, `write`, `flush`, and `fsync`, with no temporary file and rename (`opsa_common.py:153-165`), so a power loss can leave a torn file. `README.md:63-66` now states this accurately under `OD-20260918-P026-N2-DOC-1`. The loader fails closed on absent, torn, unreadable, or digest-mismatched evidence; the independent crash-window arm confirmed refusal. |
| Partial/interrupted run has no usable completion marker and restore refuses it | PASS for safety; NIT for prose | Normal error and simulated interrupted arms produced no marker and restore rc `3`. A forced crash between the two evidence writes left `RUN_MANIFEST.jsonl` but no marker and restore rc `3`. Direct writes can also leave a torn marker, which the loader refuses. `backup.py:15-19` and `opsa_common.py:41-43` overstate this as leaving neither artifact; see NIT-1. |
| Restore requires one explicit completed run ID; `--latest` is gone | PASS | `restore.py:50-69,154-165` rejects a missing or unknown exact run ID. Independent missing-ID and prefix-ID arms returned rc `3`. The base reproduction selected a newer partial run through `--latest` and returned rc `0`, proving the old defect. |
| Restore fails closed for absent/tampered/mismatched completion evidence | PASS for tested file/marker cases; directory mismatch is the REQUIRED exception | Candidate arms refused: missing marker, marker/per-run digest mismatch, marker naming another run, false `readback`, wrong manifest name, fewer per-run file records, copied root without `runs/`, unsuccessful global `run_end`, and backup-file hash mismatch. The sole discovered fail-open path is the unverified directory-record set. |
| Marker fields are fully checked | PASS | `restore.py:104-123` checks file count, terminal count, per-run readbacks, marker `readback`, and marker manifest name. The NIT-1 mutant disabling the `readback` check made its fence fail. |
| Existing interfaces remain additive except named explicit-run change | PASS with known consumer propagation | Backup CLI, store layout, hash algorithm, append-only global manifest, and heartbeat behavior are unchanged. The only executable external caller was updated to carry the original completion bytes and call explicit-run restore. |
| Required falsifications exist and fail before the fix | PASS | Independent pre-fix and intermediate-slice executions reproduced the required RED states; details are below. |
| Fake/fixture boundary | PASS | All executions used temporary local fixtures. No credentials, external host, network service, schedule, provider, deployment, or operational drill was used. |

## Fail-open and ordering analysis

| Scenario | Candidate result |
|---|---|
| Interrupted backup before completion evidence | rc `1`; no marker; restore rc `3` |
| Crash after per-run manifest but before marker | manifest present, marker absent, global `run_end = partial`; restore rc `3` |
| Forged evidence on a globally partial run | refused first on global `run_end.status = partial`, preserving gate precedence |
| Marker digest tampered | restore rc `3`, per-run manifest hash mismatch |
| Per-run manifest edited after marker | restore rc `3`, digest mismatch |
| Marker names another run | restore rc `3` |
| Marker says `readback = partial` | restore rc `3` |
| Marker names another manifest | restore rc `3` |
| Per-run/global file sets differ | restore rc `3` |
| Copied backup root lacks `runs/<run_id>` evidence | restore rc `3` |
| Explicit ID is only a prefix | restore rc `3`, no fuzzy selection |
| Dry run | rc `0`, no backup root or marker |
| Backup ends with errors | rc `1`, no marker |
| Per-run/global directory sets differ | **restore rc `0`; forged directory created; genuine directory omitted; false `status = ok`** |

The NIT-5 expression is dead by static proof: `backup.py:227` defines `status = "ok" if not errors else "partial"`, and `backup.py:237` returns success exactly when `not errors`. Any former extra `status == "ok"` term was redundant.

## RED/GREEN evidence

All commands used the mandated Python unless the command is the standalone Ruff executable.

| Evidence | Exact cwd and command | Result |
|---|---|---|
| Candidate OPS-A suite | cwd `C:\tmp\P026_REPAIR_20260915\MTC_COMMAND_CENTER\tools\opsa`; `python -m unittest test_opsa -v` | exit `0`; `Ran 39 tests in 1.691s`; `OK` |
| Heartbeat adapter | cwd `C:\tmp\P026_REPAIR_20260915`; `python check_p030_opsa_heartbeat_adapter.py` | exit `0`; `Ran 10 tests`; `OK` |
| Closed-partition adapter | cwd `C:\tmp\P026_REPAIR_20260915`; `python check_p030_closed_partition_backup_adapter.py` | exit `0`; `Ran 45 tests in 4.833s`; `OK` |
| Required Ruff rules | cwd `C:\tmp\P026_REPAIR_20260915`; `C:\tmp\wp_p0_04_tooling_20260825\Scripts\ruff.exe check --select E9,F821,F811,F401,F841 MTC_COMMAND_CENTER/tools/opsa` | Ruff `0.16.4`; exit `0`; `All checks passed!` |
| Original defect on base `fcac0ac6` | cwd `...\old_latest`; `python restore.py --config fixture/config.json --latest --check-only` | exit `0`; selected the newer partial run `opsa-20260102T000000.000Z`, verified its file, and reported `status: ok` |
| D026 slice-1 tests against base implementation | cwd `...\base_suite`; `python run_slice1_37.py` | `Ran 37 tests`; `FAILED (failures=5, errors=4)`. Failures/errors were behavioral: absent completion artifacts and old non-structured refusal paths, not imports or harness setup. |
| D026 slice-1 adapter checker against pre-adapter code | cwd `...\adapter_slice1_exact2`; `python check_p030_closed_partition_backup_adapter.py` | `Ran 45 tests`; `FAILED (failures=6, errors=3)` - 9 failing tests, matching the required pre-fix adapter RED. |
| Hand-made evidence fence against the intermediate slice | cwd `...\slice2_handmade`; two named unittest methods | `Ran 2 tests`; `FAILED (failures=3, errors=1)`. The intermediate implementation accepted the hand-made unclosed run in three arms. |
| Reserved store-name fence against the earlier common module | cwd `...\slice1_reserved`; one named unittest method | `Ran 1 test`; `FAILED (failures=2)`; both names returned rc `1` rather than the required rc `3`. |
| Marker `readback` mutant | cwd `...\nit1_readback`; one named unittest method with the check disabled | `Ran 1 test`; `FAILED (failures=1)` because the mutated restore returned rc `0` for `readback = partial`. |

These RED runs directly demonstrate that the added tests can detect the old defect and the later marker-field repair. The candidate GREEN runs use the exact pinned candidate bytes.

## Independent adversarial arms

Scratch root: `C:\tmp\SOL_P026_SCRATCH\sol_t0_2e03a669_xhigh`.

1. Candidate refusal matrix
   - cwd: `...\candidate_arms`
   - command: `python independent_red_arms.py`
   - exit: `0`
   - terminal result: `INDEPENDENT_ARMS_OK`
   - Covered interruption, gate ordering, digest tamper, post-marker manifest edit, wrong marker run ID, false marker readback, wrong manifest name, fewer file records, copied root without run evidence, prefix ID, dry run, and backup-error cases.

2. Two-write crash window
   - cwd: `...\candidate_arms`
   - command: `python crash_window_arm.py`
   - exit: `0`
   - output: `ARM manifest_marker_crash_window backup_rc=1 run_manifest=True marker=False run_end=partial restore_rc=3`

3. Directory-record disagreement - newly discovered REQUIRED arm
   - cwd: `...\candidate_arms`
   - command: `python dir_record_mismatch_probe.py`
   - exit: `0` (the probe itself completed)
   - output: `PROBE global_dir_record_mismatch original='genuine-empty-dir' forged='forged-empty-dir' restore_rc=0 original_restored=False forged_restored=True`
   - restore summary: `{"mode": "restore", "run_id": "opsa-20260919T124700.492Z", "status": "ok", "verified_against_manifest": 1, "restored": 1, "overwritten": 0, "dirs_recreated": 1, "errors": 0, "finished_at": "2026-09-19T12:47:00Z"}`

The third arm retained the genuine directory in the marker-digest-bound `RUN_MANIFEST.jsonl`, changed only the corresponding global-manifest `dir.rel`, and exercised the public `run_restore()` path. Path confinement still worked; the defect is integrity, not traversal: restore reconstructed a different directory tree and claimed success.

## Contract-change blast radius

Repository-wide searches for `restore.run_restore`, `restore.py`, `select_run`, `verify_completion_evidence`, `RUN_MANIFEST.jsonl`, and `COMPLETE.json` found:

- `p030_closed_partition_backup_adapter.py` is the only executable external caller of `restore.run_restore`; calls are at lines `716` and `746`.
- `_isolated_restore_inputs()` copies the source marker and per-run manifest byte-for-byte at lines `563-623`; it does not regenerate evidence and therefore preserves the digest relationship.
- `restore_verified_prefix()` performs check-only and actual restore against the isolated explicit run at lines `692-768`.
- The adapter checker's 45-test GREEN run exercises that propagated contract.
- Other hits are tests, README/runbook text, or historical documentation; no second executable consumer was found.
- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md:152` still shows the removed `--latest` interface. `OD-20260919-P026-EVID-B-1` explicitly removed the unowned note from this candidate and assigns its reapplication to a follow-up slice, so this is NIT-2 rather than a scope repair to make here.

## Scope and protected paths

- Base-to-candidate scope is exactly the seven modified paths listed under Verified identities; no file was added.
- The packet's original five-file ceiling was extended by `OD-20260915-P026-ADAPTER-LEAD-1` for the root adapter and checker. `OD-20260918-P026-N2-DOC-1` authorizes the README documentation of direct O_EXCL behavior. `OD-20260919-P026-EVID-B-1` requires the historical evidence-note change to be dropped from this candidate; the final pin does so.
- No `DO_NOT_TOUCH` or other protected path changed.
- No Git mutation, host contact, external call, credential access, scheduling, deployment, deletion, or operational drill was performed during this review.

## Standards axis

No REQUIRED or NIT standards violations were found in the reviewed delta. The new completion gate is localized, uses the existing return-code and structured-error conventions, retains path-confinement validation before writes, and propagates the explicit-run contract to the sole executable consumer. The directory-record defect below is a contract/correctness issue and is graded on the Spec axis.

## Spec axis

One REQUIRED and two NIT findings were found. The REQUIRED issue violates the fail-closed matching-evidence contract and is independently executable. The two NITs concern inaccurate or intentionally deferred documentation and do not independently make restore unsafe.

## Lead authorship and evidence honesty

- `OD-20260915-P026-REPAIR-LEAD-1` and `OD-20260915-P026-ADAPTER-LEAD-1` disclose the Lead as builder and explicitly require independent review; the Lead does not accept its own code.
- I independently computed HEAD and subject hashes, inspected the fixed-point diffs, ran all three mandated GREEN suites and Ruff, reproduced the original `--latest` defect, reproduced the D026 RED states, ran the NIT mutant, and added independent fail-open arms.
- The checked Lead verification records agree with the independently reproduced 37-test `5 failures + 4 errors`, adapter `6 failures + 3 errors`, 39-test GREEN, 45-test GREEN, and NIT-mutant failure.
- One prose claim in the implementation evidence is too strong: an interruption between the two exclusive writes can leave the per-run manifest. The independent crash-window arm demonstrates this. The README is honest about direct non-atomic writes and fail-closed recovery.
- No prior Opus T0 report or Lead adjudication of that report was read.

## Findings

### REQUIRED-1 - Restore authenticates file records but acts on unauthenticated directory records

`MTC_COMMAND_CENTER/tools/opsa/restore.py:97-103` compares only records whose type is `file`. The selected restore set contains both `file` and `dir` records (`restore.py:50-68`), and `restore.py:245-251` creates directories directly from the global manifest after the incomplete gate passes.

The independent probe changed only the global-manifest directory path after a successful backup, leaving the digest-bound per-run manifest unchanged. Restore returned `0`, created `forged-empty-dir`, did not create `genuine-empty-dir`, and reported `status: ok`. Thus a global-manifest record set can disagree with the per-run manifest while producing a successful, false reconstruction. This violates the explicit matching-evidence/fail-closed requirement and the candidate's own promise that the per-run manifest contains every file/dir/skipped record (`backup.py:15-18`).

Required repair: compare every operational record consumed by restore - at minimum both `file` and `dir`, with type-appropriate canonical fields - between the digest-bound per-run manifest and the global manifest before any restore action. Add a D026 test that changes only a global `dir` record and requires rc `3`, structured `run_not_complete`, and no target writes. Consider binding `skipped` records too because the per-run evidence claims to carry the full record set.

### NIT-1 - Interrupted-run prose promises that neither artifact can remain

`MTC_COMMAND_CENTER/tools/opsa/backup.py:15-19` and `opsa_common.py:41-43` say a partial/interrupted run leaves neither completion artifact. The direct two-write implementation can leave `RUN_MANIFEST.jsonl` without `COMPLETE.json`, and a power loss during direct marker creation can leave a torn marker. The safety behavior is correct because such runs are refused, and `README.md:63-66` accurately documents it. Align the inline prose in the follow-up slice with the actual guarantee: no valid completion marker means not complete.

### NIT-2 - Historical restore-drill command still uses removed `--latest`

`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md:152` still documents `restore.py ... --latest --check-only`. This is stale after the explicit-run contract. `OD-20260919-P026-EVID-B-1` deliberately drops the unowned edit from this candidate and assigns it to the P026 follow-up, so no current-candidate scope change is requested; ensure that authorized follow-up replaces it with an explicit `--run <run_id>` example.

## NOT VERIFIED

- No real power-loss/kernel-crash or filesystem-durability test was run; the crash-window result is a deterministic injected local failure, not a host-level power interruption.
- No production host, provider, credential, scheduler, service, external backup copy, or operational restore drill was exercised; the packet forbids them.
- No full repository/Bridge CI suite or first-party merge gate was run. Verification was limited to the three mandated suites, the mandated Ruff rules, fixed-point inspection, and independent local arms.
- Full-rule Ruff parity was not recomputed; only the review brief's required `E9,F821,F811,F401,F841` selection was run and passed.

VERDICT: REQUEST_CHANGES
