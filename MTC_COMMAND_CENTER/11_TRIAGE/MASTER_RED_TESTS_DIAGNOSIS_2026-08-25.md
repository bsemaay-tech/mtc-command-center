# Master-red Bridge test diagnosis — 2026-08-25

## Scope and disposition

This is the diagnose-only half of Lane N. No Bridge runtime, WAL tool, test
fixture, ledger, schema, or KVM2 evidence file was edited. The two failures
below were reproduced independently from the help-test repair and remain red.

Audit tier for the combined lane is T1 because the separate fix half changes a
Bridge test. This diagnosis is T2 documentation; the higher tier governs the
work package.

## 1. Canonical ledger artifact hash mismatch

Failing node:

```text
tests/test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate
kvm2_ledger_validator.LedgerValidationError: publishable artifact hash mismatch
```

### Exact mismatching row and bytes

The canonical ledger contains one row. It is row 1, task
`KVM2-P0-04A-PREP`, and names this publishable artifact:

```text
MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
```

| Value | SHA-256 |
|---|---|
| Ledger row `artifact_sha256` | `f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e` |
| Current Windows working-tree bytes | `b6580e31c0a794a83455ce1cfc4efb17a061a34bbe0e9c5b7df1feeb3064114a` |
| Git blob bytes at `HEAD` | `f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e` |
| Current bytes normalized from CRLF to LF | `f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e` |

The working file has 36 CRLF pairs and zero lone LF line endings. Git reports:

```text
i/lf    w/crlf  attr/text=auto
```

The ledger is therefore correct for the repository/Git artifact. The failing
hash is caused by checkout transformation under the root `* text=auto` rule,
not by a semantic edit to `ledger_schema.json`.

### History and first-red boundary

`git log --follow` for both `ledger_schema.json` and
`EVIDENCE_LEDGER.jsonl` names only one commit:

```text
6fe0130f45f3c821e230ee30d1e61f548741a6a1
feat(kvm2): complete Cycle 4 VPS bridge readiness
```

That commit introduced both files. No later commit changed the artifact in the
current history. Its parent `423897b7` contains neither failing test file. A
detached Windows spot check at `6fe0130f` produced:

```text
1 failed, 1 passed
FAILED test_canonical_ledger_and_all_three_row_fixtures_validate
PASSED test_invariants_preserve_risk_and_history
```

Thus the ledger test is Windows-red from its introduction at `6fe0130f`.
On the master first-parent line, the test first appears through merge
`f61ed91919110e8856b2bc309c2c807365bb5fea`, where it is also red. A later
detached check at `fbb05d7f` remains red.

The existing repair evidence in
`GATE_A_REPAIR_VALIDATION_2026-08-02.md` independently records that an LF-clean
Linux payload clears this ledger failure while a Windows `core.autocrlf=true`
working copy retains it. This agrees with the hashes measured above.

### Recommended repair — not executed

Pin this identity-bearing artifact to LF in `.gitattributes`:

```gitattributes
MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json text eol=lf
```

Do not replace the ledger hash with the CRLF hash; that would make the
repository blob and Linux/package artifact wrong. Add a regression check that
proves a fresh Windows checkout hashes to the recorded LF identity and perform
the required deployed-artifact-identity verification. Commits `ebb750da` and
`6c746b65` contain prior, unmerged examples of this exact LF pin, but any repair
must be reviewed against current master rather than cherry-picked blindly.

## 2. WAL bundle schema-version mismatch

Failing node:

```text
tests/test_wal_state_bundle.py::test_invariants_preserve_risk_and_history
AssertionError: assert '4' == '2'
```

### Exact data flow

1. The `source_db` fixture constructs `Store(db)` and calls `_seed(store)`.
2. `_seed()` calls `store.initialize()` without a target version.
3. `Store.initialize()` defaults to `SCHEMA_VERSION_BASELINE`, which is `4`,
   and `_initialize_v4_fresh()` writes meta row `schema_version = "4"`.
4. `tools/wal_state_bundle.py::collect_invariants()` reads that exact meta row
   through `_meta(conn, "schema_version")`.
5. `create_bundle()` places the collected value in the manifest's
   `invariants` object.
6. The test then compares the faithfully preserved value to the stale literal
   `"2"`.

The fixture producer is therefore `tests/test_wal_state_bundle.py::_seed()`
through `bridge.store.db.Store.initialize()`. The bundle producer is
`tools/wal_state_bundle.py::create_bundle()`, with
`collect_invariants()` providing the value. The tool is not inventing or
upgrading the schema version.

### What changed and first-red boundary

Commit `65eaedb0f72ec6e7cfd6cb955ec1792052f295e2` (`feat(bridge): protect or
flatten partial fills`) moved the Store operational baseline to v4 before the
WAL test existed on its feature branch.

The historical executions isolate the merge interaction:

| Commit | Ledger node | WAL node | Meaning |
|---|---|---|---|
| `6fe0130f` | FAIL on Windows | PASS | Both tests are introduced, but this feature branch still initializes schema v2. |
| `f61ed919` | FAIL on Windows | **FAIL (`4 != 2`)** | The KVM2 feature is merged with the Bridge line already carrying `65eaedb0` and default v4. This is the WAL first-red commit. |
| `fbb05d7f` | FAIL on Windows | FAIL (`4 != 2`) | Both failures persist late in the current lineage. |
| `12b58b29` | FAIL on Windows | FAIL (`4 != 2`) | Current Lane N state after the unrelated help-test fix. |

The WAL failure is genuine repository-state/test-expectation drift created by
merge `f61ed919`, not a Python 3.14 behavior change. The decisive facts are
application-level: the default argument is the integer baseline `4`, the fresh
initializer writes the string `"4"`, and the bundle tool reads that row.
Existing Ubuntu 24.04 / Python 3.12.3 evidence in
`GATE_A_REPAIR_VALIDATION_2026-08-02.md` includes the same stale
`schema_version == "2"` case among the Linux failures. Commit `df00634f` also
records that this inherited assertion failed identically on both platforms and
that the corrected WAL test passed under Python 3.12.3. Python 3.12 is not
installed in this Lane N Windows checkout, so no new 3.12 run is claimed.

### Recommended repair — not executed

Make the preservation assertion compare the bundle invariant with the source
database's pre-capture `meta.schema_version`, after asserting that the source
row exists. That directly tests the named property—preserving source state—and
remains valid if an explicitly seeded fixture uses another supported schema.
Commit `6c746b65` contains a prior, unmerged example of that form. A weaker but
current-default-only alternative is comparison with
`str(SCHEMA_VERSION_BASELINE)`, as in unmerged commit `ebb750da`.

The repair's regression evidence should deliberately make the bundle report a
schema value different from the source and show the assertion RED, then show it
GREEN with faithful source-to-bundle preservation. Do not change Store schema
logic or the WAL bundle tool to satisfy the stale literal.

## Verification summary

Current focused reproductions:

```text
ledger node: 1 failed
WAL node:    1 failed (`4 != 2`)
```

Current full suite after the separate help-test repair:

```text
2 failed, 1379 passed, 1 warning in 110.49s
```

The only failures are the two nodes diagnosed above. No recommended repair in
this document was applied.
