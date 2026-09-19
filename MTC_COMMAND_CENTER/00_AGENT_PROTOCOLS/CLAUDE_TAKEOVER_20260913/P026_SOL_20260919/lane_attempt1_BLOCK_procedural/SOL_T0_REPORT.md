# Independent T0 Review — WP-P0-26 Completion-Marker Repair

Reviewer: `gpt-5.6-sol`, `xhigh` (second flagship, independent read). I did not read an `*OPUS_T*_REPORT.md` or a Lead adjudication of the Opus report.

## Verified identities

- COMPUTED worktree HEAD: `2e03a6694c4456ac5066f3789d8a7e049a2f047d` (required final pin: match).
- Review base: `fcac0ac67cf2682693ad28138b1a56e15a0846f2` (`fcac0ac6`).
- `git diff 505af399db1152910661b40e7e20fa517852e05d 2e03a6694c4456ac5066f3789d8a7e049a2f047d --stat` showed exactly one file: `RESTORE_DRILL_EVIDENCE.md`, 9 deletions.
- The seven candidate code/doc paths have no byte delta from `505af399` to `2e03a669` (path-limited diff was empty).
- `RESTORE_DRILL_EVIDENCE.md` has no byte delta from `e114ed31` to `2e03a669`; the unauthorized dated note was therefore removed as ordered by `OD-20260919-P026-EVID-B-1`.
- `fcac0ac6..2e03a669 --name-status` contains exactly seven `M` entries, no adds or deletes: five under `MTC_COMMAND_CENTER/tools/opsa/` (`README.md`, `backup.py`, `opsa_common.py`, `restore.py`, `test_opsa.py`) and the two authorized repo-root P0-30 files.
- Pinned runtime reported `Python 3.12.12`.

SHA-256 of the six executable/test subject files at the computed HEAD:

| File | SHA-256 |
|---|---|
| `MTC_COMMAND_CENTER/tools/opsa/backup.py` | `01e732150efba155e4ea7a481c97cca340ed8f6801086bf0a3dd0bc647aa01f2` |
| `MTC_COMMAND_CENTER/tools/opsa/restore.py` | `beb8e79063d21adb0429f5d0e58111058887abe6f3b18d5d9b5355c476aa43f6` |
| `MTC_COMMAND_CENTER/tools/opsa/opsa_common.py` | `e2b3d386abdb42852fe005be9ac451bf7f89770d5892ec056c1738f0fd8063e1` |
| `MTC_COMMAND_CENTER/tools/opsa/test_opsa.py` | `c125d536ab0850bbd7b0f50532e8975c3ec8a4eeb4f7782f000586bebd2c8988` |
| `p030_closed_partition_backup_adapter.py` | `60a0e7af31d884ebfa349313cf0795422cb2622ef7325e729389e1b40d51bcd9` |
| `check_p030_closed_partition_backup_adapter.py` | `ef777b3f46aa92b3eb84abe41b87d4d5d36fcbf7499514a5eb4df2fc90324d2a` |

The controlling plan at `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:577-588` requires automated second-location copying, protected evidence never deleted, and D026 RED/GREEN restoration. The local slice is governed more narrowly by the 2026-09-07 scope packet sections 2-5 plus the later owner rows for the adapter and documentation.

## Per-clause conformance

| Authority clause | Code evidence | Assessment |
|---|---|---|
| Packet §4: “Each successful backup run emits a per-run immutable `RUN_MANIFEST.jsonl` … plus `COMPLETE.json` … only after every readback hash passes.” | `backup.py:123-126` accumulates per-run records; `:196-209` records the readback result; `:214-232` writes completion evidence only with no errors and writes the terminal global record afterward; `:240-283` creates manifest then marker and binds the marker to the manifest SHA-256. | **IMPLEMENTED-AS-WRITTEN**, except for literal atomic publication, separated below. |
| Packet §4: “A partial/interrupted run has NO marker.” | `backup.py:220-226` does not call the writer when errors already exist; a completion-write failure becomes a run error; independent interrupted and missing-store arms both left no `COMPLETE.json` and no `RUN_MANIFEST.jsonl`. | **IMPLEMENTED-AS-WRITTEN.** |
| Packet §4: completion files are “never rewritten.” | `opsa_common.py:153-170` uses `open(..., "xb")`, flush, and `fsync`; existing files raise `FileExistsError`. The immutability test passes. | **IMPLEMENTED-AS-WRITTEN.** |
| Packet §4: completion files are “written atomically.” | `opsa_common.py:153-165` publishes the final path before the write completes; there is no temporary file plus rename. `README.md:63-66` now says this plainly under `OD-20260918-P026-N2-DOC-1`. | **PARTIAL against the literal 2026-09-07 wording; accepted/documented by the later owner choice.** O_EXCL gives exclusive creation and immutability, not atomic visibility. A crash between the manifest write and marker write leaves a durable `RUN_MANIFEST.jsonl`, no marker, and (because the call has not returned) no successful global `run_end`; restore refuses it. A crash during marker writing can leave a torn marker, but JSON parsing/digest validation and the successful-`run_end` requirement prevent it being mistaken for a complete run. |
| Packet §4: restore uses one explicit completed run; `--latest` removed; no ID errors. | `restore.py:50-69` refuses `None` and uses exact equality, `:158-165` requires an exact manifest ID, and `:300-318` requires `--run`; no `--latest` argument exists. | **IMPLEMENTED-AS-WRITTEN.** Prefix IDs are refused with rc 3; missing IDs are argparse rc 2 at the CLI and rc 3 at the API boundary. |
| Packet §4: matching marker + per-run manifest; no execution on mismatch. | `opsa_common.py:185-222` checks marker/schema/run ID/digest. `restore.py:72-124` additionally requires exactly one successful `run_end`, equality with global file records/counts, matching per-file readbacks, and the two operative marker claims. `restore.py:197-206` executes this gate before any backup hash check or target write. | **IMPLEMENTED-AS-WRITTEN.** No requested fail-open shape bypassed the gate. |
| Packet §4: restore refuses backup hash mismatch. | `restore.py:127-137`, `:253-297`; tampered backup tests returned rc 1 and did not restore the corrupt file. | **IMPLEMENTED-AS-WRITTEN.** |
| Packet §4: additive only; other interfaces unchanged. | Global `run_start`/file/dir/skipped/`run_end` shapes remain unchanged; `backup.py:286-294` retains its CLI; heartbeat/watchdog bytes are outside the diff. Completion evidence is additive. | **IMPLEMENTED-AS-WRITTEN** for named interfaces. Restore’s explicit-run contract is the intended breaking change. |
| Packet §5 fixture falsifications 1-4. | `test_opsa.py:161-497`; current suite is 39/39. Historical RED and independent arms are below. | **IMPLEMENTED-AS-WRITTEN.** |
| Packet §§2/6 file ceiling. | The original five-file ceiling was broadened by `OD-20260915-P026-ADAPTER-LEAD-1` for the two root adapter files and by `OD-20260918-P026-N2-DOC-1` for README documentation. The evidence-doc change was removed by `OD-20260919-P026-EVID-B-1`. | **BROADER THAN THE ORIGINAL PACKET, but exactly covered by later owner decisions.** |

## Fail-open hunt

I found no restore path that accepts any requested incomplete-run shape:

| Shape | Observed current behavior |
|---|---|
| Marker copied from another run | rc 3, `run_not_complete`, marker names another run. |
| Marker digest rebound to a per-run manifest listing fewer files | rc 3, per-run/global disagreement. |
| Per-run manifest edited after marker creation | rc 3, per-run manifest hash mismatch. |
| `errors > 0` backup | rc 1, global `run_end=partial`, no marker or per-run manifest. |
| Dry run | rc 0, no global manifest and no `runs/` directory, hence no marker. |
| Hand-made pair for a run with partial or absent `run_end` | rc 3 on the global `run_end` rule. |
| Copied restore root without `runs/` | rc 3, completion marker absent. |
| Run ID supplied as a prefix | rc 3, run ID not found; selection is exact equality. |
| Marker `readback != all_match` | rc 3, marker claim refusal. |
| Marker `run_manifest != RUN_MANIFEST.jsonl` | rc 3, marker claim refusal. |

The pair digest is also preserved through the adapter: `p030_closed_partition_backup_adapter.py:566-575` reads the original marker and per-run manifest bytes, and `:589-601` writes those exact bytes into the isolated root. It does not fabricate completion evidence. The isolated global manifest is the previously validated byte snapshot, and both adapter restore calls at `:716-722` and `:746-752` go through `restore.run_restore` and therefore `verify_completion_evidence`.

## RED/GREEN evidence

| Test/fence | RED on relevant pre-fix bytes? | GREEN at `2e03a669` |
|---|---|---|
| `test_roundtrip_byte_identical` completion-file assertions | Yes: old backup produced no marker (`1` failure in the 5F/4E run). | Pass. |
| `test_restore_without_explicit_run_id_fails_closed` | Yes: old API restored the latest run (`0 != 3`). | Pass; API rc 3 and CLI rejects `--latest`. |
| `test_interrupted_run_has_no_completion_marker_and_restore_refuses` | Yes: three sub-failures; old restore accepted the partial run in both modes and the target existed. | Pass. |
| `test_completed_run_restores_by_explicit_id_including_copied_run_directory` | Yes: old backup produced no `COMPLETE.json` (`FileNotFoundError`). | Pass. |
| `test_tampered_marker_or_run_manifest_is_refused` | Yes for the completion feature: old backup produced no `RUN_MANIFEST.jsonl` (`FileNotFoundError`). The final two claim checks are separately load-bearing: disabling either yielded exactly one failure with rc `0 != 3`. | Pass. |
| `test_partial_run_declaring_files_but_having_no_records_fails_closed` | Yes: two old-module errors were `JSONDecodeError` because the old implementation emitted no structured completion-gate report. These are the new arms reaching missing old behavior, not import errors. | Pass. |
| `test_hand_made_completion_evidence_cannot_revive_a_run_the_tool_did_not_close` | Yes on slice-2 `8d4056c5`: `3` failures + `1` error; the interrupted hand-made pair was verified/restored with rc 0 and created the target. | Pass after the slice-3 `run_end` gate. |
| Reserved completion-file store IDs | Yes on `6ac9cfb7` common: two subtest failures, old rc 1 vs required pre-write rc 3. | Pass. |
| Adapter carries completion evidence | Yes on the slice-1 adapter with the final 45-test checker: `6` failures + `3` errors = 9 failing tests; isolated restores lacked completion evidence. | `Ran 45 tests … OK`. |

One positive test is non-discriminating on the old modules: `test_newest_run_is_restored_only_by_its_explicit_id` also passes pre-fix because explicit `--run` already existed. It proves explicit-ID round trips but not removal of `--latest`; the separate no-ID/CLI test and the independent original-defect arm provide that RED evidence.

Historical suite results reproduced independently in `C:\tmp\SOL_P026_SCRATCH\sol_t0_2e03a669`:

- `fcac0ac6` backup/restore + `6ac9cfb7` common/test: `Ran 37 tests`, `FAILED (failures=5, errors=4)`. The four errors were two missing completion-file `FileNotFoundError`s and two structured-report `JSONDecodeError`s, not import failures.
- `8d4056c5` backup/restore + `d81b07f6` common/test: `Ran 39 tests`, `FAILED (failures=3, errors=1)`.
- `6ac9cfb7` common + reserved-ID test: `Ran 1 test`, `FAILED (failures=2)`.
- `6ac9cfb7` adapter + final checker/current OPS-A: `Ran 45 tests`, `FAILED (failures=6, errors=3)`.

## Independent RED arms

Pinned interpreter for all Python commands:

`C:\tmp\P020_IMPL_20260912\01a0924d-2c4b-7da1-99e1-24e2a7c7685c\.venv\Scripts\python.exe`

### Current candidate fail-open matrix

CWD: `C:\tmp\SOL_P026_SCRATCH\sol_t0_2e03a669`

Command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
<pinned-python> independent_red_arms.py current
```

Exit 0. Exact concise observations:

```text
{"arm": "interrupted_explicit_restore", "backup_rc": 1, "error": "run_not_complete", "marker": "absent", "restore_rc": 3, "target": "absent"}
{"arm": "marker_digest_tamper", "detail": "per-run manifest hash mismatch", "error": "run_not_complete", "restore_rc": 3}
{"arm": "errors_gt_zero", "backup_rc": 1, "errors": 1, "marker": "absent", "run_end": "partial", "run_manifest": "absent"}
{"arm": "gate_order_missing_marker_claims", "first_refusal": "global run_end partial", "restore_rc": 3}
{"arm": "marker_own_claims", "observed": [["readback", 3], ["run_manifest", 3]]}
{"arm": "unchecked_marker_bytes_claim", "completion_marker": "verified", "declared_bytes": -1, "restore_rc": 0}
{"arm": "per_run_lists_fewer_files", "first_refusal": "per-run/global disagreement", "restore_rc": 3}
{"arm": "marker_from_another_run", "error": "run_not_complete", "restore_rc": 3}
{"arm": "copied_root_without_runs", "error": "run_not_complete", "restore_rc": 3}
{"arm": "run_id_prefix", "restore_rc": 3, "result": "not found"}
{"arm": "dry_run", "backup_rc": 0, "manifest": "absent", "runs": "absent"}
{"arm": "all_public_api_modes_reach_gate", "check_only_rc": 0, "gate_calls": 2, "restore_rc": 0}
```

The gate-order arm forged a digest-valid pair for a partial run with both new marker fields absent. The first refusal was still the unsuccessful global `run_end`, confirming `restore.py:80-90` precedes the NIT-1 checks at `:118-123`.

### Original defect on `fcac0ac6`

CWD: `C:\tmp\SOL_P026_SCRATCH\sol_t0_2e03a669`

Command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
<pinned-python> independent_red_arms.py base
```

Exit 0 from the harness; the old restore CLI itself returned 0 for the partial latest run:

```text
{"arm": "prefixed_latest_selects_partial", "latest_file_records": 1, "latest_run_end": "partial", "partial_backup_rc": 1, "restore_cli_rc": 0, "restore_cli_status": "ok", "selected_run": "opsa-20260919T110951.188Z"}
```

This reproduces the packet §3 defect directly: old `restore.py --latest --check-only` selected the greatest started run even though its `run_end` was partial.

### NIT-1 load-bearing mutants

CWDs:

- `C:\tmp\SOL_P026_SCRATCH\sol_t0_2e03a669\mutant_readback`
- `C:\tmp\SOL_P026_SCRATCH\sol_t0_2e03a669\mutant_manifest`

Command in each:

```powershell
<pinned-python> -m unittest test_opsa.BackupRestoreTests.test_tampered_marker_or_run_manifest_is_refused -v
```

Observed:

- Readback check disabled: `Ran 1 test`, `FAILED (failures=1)`, at `refused("declares readback='partial'")`, `AssertionError: 0 != 3`.
- Run-manifest-name check disabled: `Ran 1 test`, `FAILED (failures=1)`, at `refused("names run_manifest='OTHER.jsonl'")`, `AssertionError: 0 != 3`.

## Mandated GREEN checks

| Command and cwd | Observed |
|---|---|
| `<pinned-python> -m unittest test_opsa -v` from `MTC_COMMAND_CENTER/tools/opsa` | Exit 0; `Ran 39 tests in 1.557s`; `OK`. |
| `<pinned-python> check_p030_opsa_heartbeat_adapter.py` from worktree root | Exit 0; `Ran 10 tests in 0.089s`; `OK`. |
| `<pinned-python> check_p030_closed_partition_backup_adapter.py` from worktree root | Exit 0; `Ran 45 tests in 4.573s`; `OK`. |
| `<pinned-python> -m ruff check --select E9,F821,F811,F401,F841 MTC_COMMAND_CENTER/tools/opsa` from worktree root | **Exit 1: `<pinned-python>: No module named ruff`.** This is the literal command required by the brief. |
| `C:\tmp\wp_p0_04_tooling_20260825\Scripts\ruff.exe check --no-cache --select E9,F821,F811,F401,F841 MTC_COMMAND_CENTER/tools/opsa` from worktree root | Supplemental only: Ruff `0.16.4`, exit 0, `All checks passed!`. It does not erase the mandated-environment failure. |

`PYTHONDONTWRITEBYTECODE=1` was set for test runs so the read-only subject worktree did not receive bytecode writes.

## Contract-change blast radius

Runtime consumers found by read-only repository search:

| Consumer | Result |
|---|---|
| `MTC_COMMAND_CENTER/tools/opsa/restore.py` CLI | Routes through `run_restore`, then the single completion gate. |
| `p030_closed_partition_backup_adapter.py:716-722,746-752` | Only non-test Python consumer. It performs check-only then restore through the same gate. The slice-2 byte-for-byte evidence copy is technically sound and preserves the digest binding. It cannot restore a run bare `restore.py --run` would refuse. |
| `restore.select_run` | Used only inside `run_restore` plus its unit test. No other runtime caller. |
| Readers of OPS-A `runs/<run_id>/` | OPS-A backup/restore, their tests, and the P0-30 adapter only. Unrelated IBKR API routes named `/runs/{run_id}` are a different domain. |

The shared-archive isolation mutant still fails for the intended reason: the checker accepts the adapter’s generic `P026 restore failed` only when captured stderr contains `per-run manifest file records differ from the global manifest`. The current 45-test checker passes, so a generic broken restore cannot satisfy that mutant.

Documents left with the old interface are historical evidence, not runtime consumers:

- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md:119-120,152` retains pre-change `--latest` transcript/reproduction commands. The final pin deliberately restores this file to its `e114ed31` blob under `OD-20260919-P026-EVID-B-1`; the compatibility note is deferred to the separately authorized follow-up slice.
- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/LANE_REPORT.md:37-40` describes the original `--latest`/`--run` interface. It is a dated delivery record, not the current usage guide.
- The active `tools/opsa/README.md:60-69` is current: explicit `--run`, both completion files, and the O_EXCL/non-atomic behavior are documented. “Re-backed-up under a NEW run id” describes the operator’s next backup invocation, not an automatic retry; the Lead record states the same, so I do not find an overclaim there.

## Scope and protected paths

- `fcac0ac6..e114ed31`: exactly seven files, 692 insertions / 56 deletions.
- `fcac0ac6..d81b07f6`: exactly the six code/test files, 687 insertions / 53 deletions.
- `fcac0ac6..2e03a669`: the same final seven modified files, no new file.
- No changed path is under `02_MTC_BACKTEST`, `07_ADAPTERS`, `01_PINE`, any `MTC_V2`/parity path, `06_SCHEMAS`, or `.git`.
- `watchdog.py` and heartbeat emission are untouched by this candidate. The earlier watchdog half is outside this delta.
- The global `manifest.jsonl` record types/shapes are unchanged. Completion evidence is stored separately under each run directory.
- `backup.py` CLI arguments are unchanged.
- `NoDeleteGuaranteeTests` passed in the 39-test suite. I found no credential/environment read, external network, SSH/SFTP, scheduling, host contact, or provider action in the changed tools.

## Standards

No documented repository standard is violated by the diff. Ruff 0.16.4 passes through the available standalone executable, the no-delete regression passes, and no actionable Fowler smell is introduced. The completion logic is centralized rather than duplicated, and the adapter delegates to the same gate.

There is one accuracy nit in a new comment/verification label (NIT-1 below); it is not a restore safety failure.

## Spec

The explicit-run/completion-evidence behavior is implemented and the requested original defect is demonstrably RED on `fcac0ac6` and GREEN now. The literal atomic-write word in the 2026-09-07 packet is not implemented, but the later owner decision explicitly selected documentation of the O_EXCL/fail-closed behavior instead of a code change. The final source scope is broader than the original packet only where later owner rows authorize it.

Spec axis: 0 REQUIRED, 1 NIT. Standards axis: 0 hard violations, 0 smell findings. The audit is nevertheless blocked by the unavailable mandated Ruff module in the pinned interpreter.

## Lead authorship and report honesty

Lead authorship does not change the technical result and does not require an extra mechanism beyond the frozen independent roster. It does mean the Lead’s own verification is corroboration, not acceptance; this report likewise accepts nothing by itself.

The supplied Lead record matches the diff and independently reproduced behavior on the material counts:

- Final OPS-A suite: 39 OK — reproduced.
- Original pre-fix completion suite: 5 failures + 4 errors — reproduced; errors are missing new completion artifacts/structured gate output, not import masking.
- Closed-partition adapter: 45 OK now — reproduced.
- Slice-1 adapter under the final checker: 9 of 45 failing (`6F + 3E`) — reproduced.
- Reserved-ID test on old common: two subtest failures — reproduced.
- Hand-made-evidence test on slice-2 restore/backup: `3F + 1E` — reproduced.
- NIT-1 disabled readback/run-manifest checks: one failure each — reproduced.
- Python 3.12.12 — reproduced.
- The Lead’s NIT record correctly identifies Ruff 0.16.4 at `C:\tmp\wp_p0_04_tooling_20260825\Scripts\ruff.exe`; the review brief’s separate assertion that Ruff is in the pinned Python venv is false in this environment.

## Findings

### NIT-1 — “every claim” is broader than what the verifier checks

`MTC_COMMAND_CENTER/tools/opsa/restore.py:113-117` says “every claim the marker makes about itself is checked,” but only `files`, `readback`, `run_manifest`, schema, run ID, and the manifest digest are validated. `backup.py:268-275` also writes `bytes`, `skipped`, `dirs`, timestamps, and `config`; those remain unchecked. My independent mutation set `bytes=-1` while preserving all safety bindings, and `--check-only` returned rc 0 with `completion_marker: verified`.

Consequence: no file can be restored outside the verified global/per-run records and hashes, so this is not a restore fail-open. The wording and `verified` label can, however, overstate verification of informational marker metadata. Minimum fix: narrow the comment/meaning of “verified” to the fields used for restore authorization, or validate the remaining marker metadata against the per-run/global evidence.

No REQUIRED code finding.

## NOT VERIFIED

- The brief-mandated pinned-Python Ruff command could not run successfully because that venv has no `ruff` module. The equivalent standalone Ruff 0.16.4 check passed, but the report contract says inability to execute a mandated command is `BLOCK`.
- No real power-loss crash was induced during `open(..., "xb")`; crash outcomes above are derived from the write ordering and independently tested failure states.
- No live host, external second location, scheduler, network, credential, phone notification, or operational restore drill was contacted or executed; all tests were local fixtures/scratch only.
- Protected CI, merge, deployment, and package acceptance were not run or granted.
- The repo guard and working-tree status were not run because the launch brief expressly forbids those Git/guard workflows in this read-only review.

VERDICT: BLOCK
