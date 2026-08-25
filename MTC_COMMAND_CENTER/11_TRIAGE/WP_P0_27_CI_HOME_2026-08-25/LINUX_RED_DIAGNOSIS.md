# Lane R - Linux CI failure diagnosis

**Status:** DIAGNOSIS COMPLETE; DOWNSTREAM REPAIR STATUS UPDATED

**Role:** Codex implementer under Claude Lead

**Audit tier:** T2 for this documentation-only lane. The later repair to the protected
Bridge persistence/cutover tool was a separate T0 lane.

**Evidence target:** GitHub Actions run `32781394607`, PR #125, commit
`3899d6f984ddc7c41b632e99e616941524b0cec1`

**Environment:** `ubuntu-latest`, CPython 3.12.14

**Scope:** diagnose only; no Bridge source or test was edited.

## 2026-08-25 downstream repair status

- The WAL product defect diagnosed here is fixed and merged on `master` through merge
  `110305c0`. The fix includes D026 coverage for the capture-ordering bug and mutation-proven
  SHM identity-field coverage.
- The two GC-referent test defects diagnosed here are fixed on
  `fix/gc-referent-tests-20260825` at `25eac11c`, pending audit and not yet merged. This branch
  must not duplicate that repair.
- The final GC repair skips only the Enum-internal member dictionary whose keys are contained in
  `_value_`, `_name_`, `__objclass__`, and `_sort_order_`. It does not stop at the Enum member.
  A first attempt that stopped at the member was shown to lose real coverage on 3.12, 3.13 and
  3.14.
- The original CPython 3.12 attribution below was too narrow. A later standalone CPython 3.13.13
  probe also exposed the Enum-member dictionary through `gc.get_referents`; any CI matrix entry
  on 3.13 is inside the blast radius.
- With the GC fix applied, the GC lane recorded the whole Bridge suite as
  `1370 passed, 1 warning`. The package gate still cannot claim green on `master` until that
  fix merges and the suite runs green there.

## Executive conclusion

The 25 failures have two root causes:

| Failure family | Count | Classification | Conclusion |
|---|---:|---|---|
| `test_order_state.py:400` and `:418` | 2 | **TEST defect** | The tests confuse interpreter GC-introspection details with mutability of the mapping's policy data. CPython 3.12 and a later standalone CPython 3.13.13 probe expose each `Enum` member's runtime dictionary through `gc.get_referents`; this is not bounded to 3.12. The immutable holder and the behavior-changing attack tests remain sound. Fix: `25eac11c`, pending audit and not merged. |
| `test_wal_state_bundle.py` | 23 | **PRODUCT defect** | **SERIOUS: the Linux deployment path was genuinely unsafe/unusable.** The capture opened a WAL database but only executed `SELECT 1`, which did not attach/read the database. On the Linux deployment stack, the first real read occurred after the drift bracket opened, and SQLite's own WAL/SHM initialization was misclassified as an external writer. Fixed and merged through `110305c0`. |

The WAL result was not acceptable baseline noise. `wal_state_bundle.py` is the
state-capture tool used by the ordered single-writer cutover, where
`--allow-live-source` is intentionally forbidden. In the diagnosed form, a normal
Linux capture could fail closed even when no external writer existed. Conversely,
weakening the detector by ignoring WAL/SHM changes would risk accepting a genuinely
moving source. The repair must distinguish tool-created SQLite sidecar activity from
real source drift without removing the safety fence.

## Evidence acquisition and identity

The requested command was executed verbatim:

```powershell
gh run view 32781394607 --repo bsemaay-tech/mtc-command-center --log-failed
```

The failed step ran:

```text
python -m pytest IBKR_PAPER_BRIDGE/tests -q
```

GitHub reported:

```text
pythonLocation: /opt/hostedtoolcache/Python/3.12.14/x64
25 failed, 1326 passed, 1 warning in 57.21s
Process completed with exit code 1
```

The run API identifies the PR head as
`3899d6f984ddc7c41b632e99e616941524b0cec1`. The diagnostic worktree HEAD was
the same SHA, and the four relevant source/test files have no difference from the
CI commit. The log contains exactly 25 failed node IDs: two order-state tests and
23 WAL-bundle tests; no third failure family exists.

Local contrast was limited to native Windows, as required (no WSL or Docker):

```text
Python 3.14.2
2 focused GC-container tests: 2 passed
2 behavior-changing GC attack tests: 2 passed
test_wal_state_bundle.py: 41 passed
```

This contrast must not be overclaimed as an OS-only experiment because Python and
the bundled SQLite version also differ. The order-state mechanism is proven to be
Python-version-dependent. The WAL mechanism is conditional on the SQLite/filesystem
behavior of the Linux deployment stack, which is the environment that matters.

## Failure family 1 - order-state GC referents

### Failing tests

- `test_gc_referents_of_transitions_contain_no_mutable_container`
  (`test_order_state.py:397-400`)
- `test_gc_referents_of_raw_aliases_contain_no_mutable_container`
  (`test_order_state.py:415-418`)

### Evidence chain

1. `ORDER_STATE_TRANSITIONS` and `RAW_ORDER_STATUS_ALIASES` are instances of
   `_ImmutableMapping`, a zero-slot tuple subclass (`bridge/engine/types.py:145-204`).
   Their owned data is tuples, `frozenset`s, strings, and `OrderState` members.
2. The test helper `_transitive_gc_referents()` (`test_order_state.py:375-394`)
   performs an untyped breadth-first traversal of every object returned by
   `gc.get_referents()`. It stops only at `type` objects; it does not treat Enum
   instances or other runtime-owned objects as traversal boundaries.
3. On CI's CPython 3.12, `gc.get_referents(OrderState.MEMBER)` exposes the member's
   implementation dictionary. A later standalone CPython 3.13.13 probe exposed the same class
   of member dictionary, so the exposure is not bounded to 3.12. The failure output proves the
   identity of those dictionaries: the first contains `_value_`, `_name_`, `__objclass__`, and
   `_sort_order_`. The transition walk reports 11 dictionaries (one per state), and the alias
   walk reports 8 reachable member dictionaries.
4. Those dictionaries are not a mutable list/dict backing `_ImmutableMapping`.
   They belong to Python's Enum objects, which are policy values stored inside the
   immutable holder.
5. The local platform-pass was itself misleading. On local CPython 3.14,
   `OrderState.OPEN.__dict__` still exists and has the same four keys, but
   `gc.get_referents(OrderState.OPEN)` no longer returns that dictionary. The test
   passes because GC traversal changed, not because the product became more immutable. The first
   attempted fix then stopped at the Enum member and lost coverage for mutable containers
   reachable through an Enum member on 3.12, 3.13 and 3.14; the final repair skips only the
   Enum-internal dictionary.
6. The immediately adjacent behavior tests at `test_order_state.py:403-412` and
   `:421-430` try to mutate every dict/list found by the same traversal and then
   re-check `can_transition()` / `normalize_raw_order_status()`. They are absent
   from the CI failed-node list, so both passed on CPython 3.12. They also passed
   in the focused local run.
7. Direct holder attacks are separately covered: item assignment, normal attribute
   assignment, and `object.__setattr__` are rejected. Those tests also passed in CI.

### Classification

**TEST defect, twice.** The assertion `mutable == []` is interpreter-GC conditional
and broader than the security property it is meant to establish. It inspects CPython
object-graph implementation details beyond the immutable holder's owned storage and
therefore produces a false failure on the deployment interpreter. No evidence in run
32781394607 shows that either policy can be changed through the exported mappings. The fix at
`25eac11c` preserves visibility of mutable policy containers and skips only Enum-internal member
dictionaries; it is pending audit and not yet merged.

### Repair status

1. The first attempted repair treated `Enum` members as atomic values, just as the helper already
   treated `type` objects as terminal. That was shown to lose real coverage for mutable containers
   reachable through Enum members on 3.12, 3.13 and 3.14.
2. Retain the behavioral attack tests and direct assignment/replacement tests. They
   assert the real contract: callers cannot change transition or normalization behavior.
3. The accepted candidate approach on `fix/gc-referent-tests-20260825` skips only dictionaries
   whose keys are contained in `_value_`, `_name_`, `__objclass__`, and `_sort_order_`.
4. The GC lane recorded D026 RED/GREEN evidence for the original broad-helper failure and for the
   Enum-member blind spot, then recorded `1370 passed, 1 warning` for the whole Bridge suite with
   the fix applied. That is not master-gate evidence until the branch passes audit and merges.

## Failure family 2 - WAL/SHM capture drift

### Primary symptom

The first two failures preserve the product report in their assertion output:

```text
verdict: INVALID
exit_code: 2
failures: ['source_changed_during_capture']
changed_components: ['wal', 'shm']
```

The report's `drift_evidence` contains `arrival`, `before`, and `after` snapshots.
Each present file snapshot includes `device`, `inode`, `mode`, `size_bytes`,
`mtime_ns`, and `ctime_ns`, plus a SHA-256 and `changed_during_hash`. The abbreviated
pytest representation explicitly shows `ctime_ns` fields while identifying `wal`
and `shm` as the changed components; the database component reports
`changed_during_hash: False`.

### Platform-conditional mechanism

1. The `source_db` fixture creates a real `Store`, and `Store.initialize()` puts the
   database in WAL mode (`bridge/store/db.py:745`). The fixture closes the store before
   capture. After a clean close, SQLite may checkpoint/remove the sidecars, leaving the
   main `bridge.db` as the arrival state.
2. `create_bundle()` takes `source_snapshot_arrival` before opening SQLite
   (`wal_state_bundle.py:602-607`). This correctly records provenance before the tool
   can affect the directory.
3. `_connect_readonly()` opens `mode=ro` and executes only `SELECT 1`
   (`wal_state_bundle.py:211-240`). A constant expression reads no database page or
   schema table. The code assumes this establishes the WAL attachment, but it does not
   on the CI/deployment stack.
4. `create_bundle()` then takes `source_snapshot_before` immediately after connection
   setup (`wal_state_bundle.py:618-628`). Because no real database read has occurred,
   this snapshot is too early.
5. The next operations - `PRAGMA integrity_check`, foreign-key inspection, invariant
   queries, and `src.backup(dst)` (`wal_state_bundle.py:629-650`) - are real database
   reads. On the Linux SQLite stack they attach the WAL and create/update the `-wal`
   and `-shm` artifacts needed for the WAL index, read marks, and locking coordination.
6. The after snapshot is taken while the source connection is still open
   (`wal_state_bundle.py:651`). It therefore sees WAL/SHM state that was absent or
   different in the premature before snapshot.
7. Linux `st_ctime_ns` is inode status-change time, not creation time. Sidecar creation
   or metadata change therefore supplies legitimate new/different ctime evidence. On
   Windows, `st_ctime` has historically represented creation-time semantics, and
   Windows file-sharing/locking plus a different Python/SQLite build can materialize
   the sidecars at another point. The raw `ctime_ns` values are evidence of distinct
   filesystem states; they are not proof of an external writer.
8. `_file_snapshot()` compares all stable metadata and hashes before/after each file
   read (`wal_state_bundle.py:416-453`). `_changed_snapshot_components()` then compares
   each complete snapshot dictionary (`:465-477`). Any presence, metadata, hash, or
   within-hash change marks the component changed.
9. `_capture_changed_components()` emits components in the fixed order
   `db`, `wal`, `shm` (`wal_state_bundle.py:480-510`). Therefore the logged ordering
   `['wal', 'shm']` is deterministic presentation order, not evidence that WAL changed
   temporally before SHM or that two independent writers acted.
10. `create_bundle()` converts any changed component into
    `source_changed_during_capture`, returns exit 2, and discards the bundle
    (`wal_state_bundle.py:678-735`). This single failed prerequisite causes every
    downstream test that expects a stable initial capture to fail before reaching its
    intended assertion.

### Why this is a product defect, not a Linux-specific test assertion

The fixture is quiesced and the contract requires it to capture successfully without
`--allow-live-source`. The tests are right to require `rc == 0`. The product places its
capture boundary before it has completed its own SQLite/WAL initialization and then
interprets its own side effects as source-writer drift. Linux is the deployment platform,
so a Windows-only green result cannot waive this defect.

This is safety-critical in both directions:

- current behavior blocks a valid ordered cutover on the deployment host;
- simply ignoring WAL/SHM or removing `ctime_ns` would weaken detection of a real writer,
  inode replacement, permission/mode change, or sidecar mutation during capture.

### Every failing WAL test

All 23 are classified **PRODUCT**, with the same initial capture defect. The first six
exercise capture results directly; the remaining seventeen fail in prerequisite setup
before their own overwrite/verify scenario is reached.

| # | Failing node | Failure point / intended test not reached |
|---:|---|---|
| 1 | `test_create_then_verify_round_trip` | Primary `create()` returns 2/INVALID instead of 0/CAPTURED. |
| 2 | `test_manifest_records_online_backup_and_both_ends_integrity` | Primary capture fails; detailed drift report shows `wal`, `shm`. |
| 3 | `test_invariants_preserve_risk_and_history` | Stops at `assert rc == 0`; invariant assertions are not reached. |
| 4 | `test_manifest_leaks_no_path_or_identifier` | Stops at baseline capture; sanitization assertion is not reached. |
| 5 | `test_manifest_uses_a_canonical_source_name_not_the_input_name` | Renamed stable source is rejected before canonical-name checks. |
| 6 | `test_source_content_is_not_mutated` | Stops at capture rc; byte and arrival-sidecar assertions are not reached. |
| 7 | `test_create_refuses_to_overwrite_without_force` | The first bundle cannot be created, so overwrite refusal is not exercised. |
| 8 | `test_create_force_replaces_existing_bundle` | The first bundle cannot be created, so force replacement is not exercised. |
| 9 | `test_verify_corrupt_manifest_json_exit_3` | Baseline bundle creation fails before manifest corruption. |
| 10 | `test_verify_detects_missing_field` | Baseline bundle creation fails before field deletion. |
| 11 | `test_verify_rejects_unsupported_schema_version` | Baseline bundle creation fails before schema-version mutation. |
| 12 | `test_verify_rejects_manifest_controlled_path_before_file_access` | Baseline bundle creation fails before path tampering. |
| 13 | `test_verify_rejects_resigned_noncaptured_manifest` | Baseline bundle creation fails before verdict/exit-code mutation. |
| 14 | `test_verify_rejects_missing_nested_contract_field` | Baseline bundle creation fails before nested-field deletion. |
| 15 | `test_verify_detects_manifest_tamper` | Baseline bundle creation fails before unsigned tampering. |
| 16 | `test_verify_detects_bundle_hash_mismatch` | Baseline bundle creation fails before bundle byte mutation. |
| 17 | `test_verify_detects_invariant_drift_even_when_resigned` | Baseline bundle creation fails before database mutation/resigning. |
| 18 | `test_verify_detects_missing_bundle_db` | Baseline bundle creation fails before bundle deletion. |
| 19 | `test_verify_rejects_a_sidecar_next_to_the_bundle` | Baseline bundle creation fails before stray sidecar creation. |
| 20 | `test_verify_expected_hashes_must_match` | Baseline bundle creation fails before expected-hash checks. |
| 21 | `test_verify_requires_both_externally_recorded_expected_hashes` | Baseline bundle creation fails before required-argument checks. |
| 22 | `test_verify_rejects_malformed_expected_hash` | Baseline bundle creation fails before malformed-hash verification. |
| 23 | `test_verify_fails_closed_on_a_corrupt_bundle_database` | Baseline bundle creation fails before deliberate SQLite corruption. |

The tests that deliberately expect drift, or pass `--allow-live-source`, remain green.
That is consistent with the diagnosis: the detector and failure plumbing work, but the
capture boundary wrongly includes activity caused by the capture tool itself.

### Repair status - implemented and merged

This recommendation was later implemented in the T0 WAL lane and merged to `master` through
`110305c0`. The merged fix uses a real fetched schema read before the drift boundary, keeps
writer drift detection after the boundary, and adds mutation-proven coverage for the ordering bug
and SHM identity fields. The historical repair criteria were:

1. Before opening SQLite, fail closed on source states that a read-only open cannot
   safely consume without creating/rebuilding WAL-index state - especially a non-empty
   hot WAL with missing, truncated, unrelated, or unusable SHM. This preflight must be
   read-only and must happen before any SQLite connection can modify the source directory.
2. In `_connect_readonly()`, replace the constant probe with a fetched read of a real,
   universally available schema table, such as
   `SELECT name FROM sqlite_master LIMIT 1`. Complete that read before
   `source_snapshot_before`, so SQLite's own WAL attachment falls outside the capture
   bracket.
3. Do not repair this by dropping `ctime_ns`, ignoring all WAL/SHM drift, moving the
   after snapshot past connection close, or enabling `--allow-live-source` for cutover.
   Each shortcut either hides a real writer or changes the approved cutover contract.
4. Add a Linux/Python-3.12 regression test for a stable closed WAL-mode source whose
   sidecars appear only at the first real database read. The test must observe semantics
   (for example, a SQLite authorizer/schema read), not discriminate on the literal text
   `SELECT 1`; a `SELECT 2` mutant must remain RED.
5. Add and falsify a real concurrent-writer test proving that moving initialization
   outside the bracket does not weaken detection after the bracket opens.
6. Add fail-closed tests for hot-WAL/missing-or-invalid-SHM states and prove the tool
   makes no connection and creates no source sidecar before refusal.
7. Apply D026 RED/GREEN evidence on the exact Linux deployment class and run the full
   Bridge suite. Because this is protected persistence/cutover behavior on the Linux
   deployment platform, the repair belonged in a separately authorized T0 lane with both
   required flagship auditors.

## Ranked hypotheses and disposition

| Rank | Hypothesis | Prediction | Result |
|---:|---|---|---|
| 1 | `SELECT 1` leaves WAL unattached until the first real read, placing tool-created sidecars inside the bracket. | Stable source: db remains stable, WAL/SHM change, capture returns INVALID; forcing a schema read before `source_snapshot_before` should remove false drift without ignoring later writer drift. | **Supported by log, ordering, source, and prior Linux evidence. Root cause; later fixed and merged through `110305c0`.** |
| 2 | An actual concurrent writer modified the fixture. | Database/invariants should also change or the failure should be intermittent. | **Rejected.** All 23 cases fail consistently; db reports stable, fixture is closed, changed components are deterministically WAL/SHM. |
| 3 | `ctime_ns` alone is a bad cross-platform assertion. | Removing/normalizing ctime alone would make otherwise identical sidecar snapshots equal. | **Insufficient and unsafe.** The sidecar lifecycle/presence itself moves; ctime is one evidence field, not the root ordering defect. |
| 4 | The 23 WAL tests contain independent Linux-only expectations. | Failures should reach distinct intended assertions and report distinct reasons. | **Rejected.** Every node stops at the same baseline `create()` result, exit 2 with `source_changed_during_capture`. |

## Scope and safety statement

The original Lane R diagnosis changed no WSL, Docker, host, service, credential, broker,
exchange, testnet/live, Pine, parity, MTC, schema, Bridge source, or test file. Its only local
execution was read-only/focused testing against temporary pytest data on Windows. Subsequent
repair work happened in separate lanes: WAL is fixed and merged through `110305c0`; GC-referent
tests are fixed at `25eac11c` and await audit/merge. This branch only updates the documentation.
