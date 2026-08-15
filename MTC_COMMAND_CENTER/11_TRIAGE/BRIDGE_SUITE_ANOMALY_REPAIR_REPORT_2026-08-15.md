# Bridge suite anomaly repair report - 2026-08-15

Status: **IMPLEMENTER COMPLETE - NOT INDEPENDENTLY ACCEPTED**

Worktree: `C:\P10FIX`

Branch: `codex/bridge-suite-anomaly-repairs-20260815`

Starting commit: `678d4be22ddde2201948de0d60343c1edfa85a06`

Audit tier: **T1**. This is local, non-economic Bridge test/infrastructure work, and A1
affects deployed-artifact identity. No host, network, deployment, service, credential,
broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, merge, push, or
economic action occurred. No file under `MTC_COMMAND_CENTER/11_TRIAGE/WPI_*` was modified.

## Starting-state proof

Before any work:

```text
> git rev-parse HEAD
678d4be22ddde2201948de0d60343c1edfa85a06

> git status --porcelain

> git branch --show-current
codex/bridge-suite-anomaly-repairs-20260815
```

The required provisional baseline packet was read in full before design or editing:
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md`.

## Pre-change full-suite evidence

Exact command, from repository root:

```powershell
$env:PYTHONUTF8='1'
python -m pytest IBKR_PAPER_BRIDGE\tests -q -p no:cacheprovider
```

Exact summary and return code:

```text
rc=1
2 failed, 1019 passed, 1 warning in 89.05s (0:01:29)
```

The two failures were:

```text
FAILED IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate
FAILED IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py::test_invariants_preserve_risk_and_history
```

The warning was the already-known installed-dependency `StarletteDeprecationWarning` from
`fastapi/testclient.py` about `httpx`.

## A1 - LF/CRLF-ambiguous artifact hash

### Root cause

`EVIDENCE_LEDGER.jsonl` records the SHA-256 of the committed LF bytes of
`ledger_schema.json`, while the root `* text=auto` rule checked that file out as CRLF on
Windows. `validate_ledger.py` deliberately hashes raw working-tree bytes. The same logical
JSON therefore had two byte identities:

| form | bytes | SHA-256 |
|---|---:|---|
| Git object (LF) | 867 | `f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e` |
| pre-repair Windows working tree (CRLF) | 903 | `b6580e31c0a794a83455ce1cfc4efb17a061a34bbe0e9c5b7df1feeb3064114a` |

That makes the byte-exact validator platform-dependent. Re-recording the CRLF hash was
rejected because it would make the ledger wrong on the Linux deployment target.

### Options considered

1. Add an exact-path `.gitattributes` rule, `text eol=lf`, so this artifact has one byte
   identity in every checkout.
2. Normalize text-classified artifacts inside the validator before hashing.

Option 2 was rejected. It would weaken the validator from a raw-byte identity check into a
normalized-text identity check. Specifically, a change between LF and CRLF bytes would no
longer be detected, even though those are distinct publishable artifact bytes. It would
also broaden the policy from this one known artifact to every text-classified artifact the
validator sees.

### Chosen repair and scope

Option 1 was chosen. Repository history shows this exact narrow rule was previously used
and independently validated in commit `ebb750dafd71c5d1293a9524846a00cd33b212bc` before it
was absent from the present base. The rule affects only
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json`: Git treats that one
path as text and uses LF for checkout/export. It does not change the validator, ledger,
schema content, other JSON files, or repository-wide line-ending behavior.

Because attributes do not retroactively rewrite an existing checkout, the schema file was
refreshed to its unchanged committed content after adding the rule. It has no content diff
and no staged blob change.

### Exact A1 diff

```diff
diff --git a/.gitattributes b/.gitattributes
index dfe07704..49c0fbe4 100644
--- a/.gitattributes
+++ b/.gitattributes
@@ -1,2 +1,3 @@
 # Auto detect text files and perform LF normalization
 * text=auto
+MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json text eol=lf
```

### A1 byte and SHA-256 proof

Exact command:

```powershell
& 'C:\Program Files\Git\bin\bash.exe' -lc "git -C /c/P10FIX cat-file -s 'HEAD:MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json'; git -C /c/P10FIX cat-file -p 'HEAD:MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json' | sha256sum; wc -c < /c/P10FIX/MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json; sha256sum /c/P10FIX/MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json"
```

Real output:

```text
867
f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e *-
867
f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e */c/P10FIX/MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
```

Attribute/eol verification:

```text
> git check-attr text eol -- MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json: text: set
MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json: eol: lf

> git ls-files --eol -- MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
i/lf    w/lf    attr/text eol=lf       MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
```

The raw Git object and raw working-tree file are both 867 bytes and have the same SHA-256.

## A2 - stale schema-version assertion

### Root cause

The `source_db` fixture calls `Store.initialize()` without an explicit target, so the
fixture database uses the current baseline schema v4. `wal_state_bundle.py` reads that
database's `meta.schema_version` and correctly records `"4"` in the bundle invariants. The
test still asserted the obsolete literal `"2"`.

### Options considered

1. Change the literal from `"2"` to `"4"`.
2. Compare against `SCHEMA_VERSION_BASELINE` from the product module.
3. Query `meta.schema_version` directly from the fixture's source database and compare the
   produced manifest value with that independently observed source value.

Option 1 would go stale at the next intentional baseline migration. Option 2 is
tautological because the same product constant determines fixture initialization; it does
not independently prove faithful recording. Option 3 was chosen because it tests the real
contract: bundle output must equal the source database it captured.

### Exact A2 diff

```diff
diff --git a/IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py b/IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
index edc02108..91db6c40 100644
--- a/IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
+++ b/IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
@@ -8,6 +8,7 @@ from __future__ import annotations
 import json
 import sqlite3
+from contextlib import closing
 from datetime import UTC, datetime, timedelta
 from pathlib import Path
@@ -313,12 +314,18 @@ def test_bundle_never_contains_a_wal_shm_trio(tmp_path, bundle_dir, capsys):
 def test_invariants_preserve_risk_and_history(source_db, bundle_dir, capsys):
+    with closing(sqlite3.connect(source_db)) as source:
+        source_schema_row = source.execute(
+            "SELECT value FROM meta WHERE key = 'schema_version'"
+        ).fetchone()
+    assert source_schema_row is not None
+
     rc, _ = create(source_db, bundle_dir, capsys)
     assert rc == 0
     inv = read_manifest(bundle_dir)["invariants"]
     assert inv["app_state"] == "DISARMED"
-    assert inv["schema_version"] == "2"
+    assert inv["schema_version"] == source_schema_row[0]
     assert inv["open_trades"] == 1
     assert inv["live_orders"] == 1
     assert inv["closed_trades"] == 3
```

`closing(...)` is used because a SQLite connection's context manager handles transactions
but does not close the Windows file handle.

### A2 discriminating-power proof

The proof created a database and bundle only inside a temporary directory, saved the
manifest's original bytes, changed only
`manifest["invariants"]["schema_version"]` to `"999"`, executed the same independent
source-versus-manifest comparison, required RED, restored the original manifest bytes in a
`finally` block, and required GREEN. The temporary directory was removed automatically.

Exact command:

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONPATH='IBKR_PAPER_BRIDGE'
@'
import json
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path

from bridge.store.db import Store
from tools import wal_state_bundle as wal

with tempfile.TemporaryDirectory(prefix="lane-e-a2-") as raw:
    scratch = Path(raw)
    source_db = scratch / "source" / "bridge.db"
    bundle_dir = scratch / "bundle"

    store = Store(source_db)
    store.initialize()
    store.set_meta("app_state", "DISARMED")
    store.close()

    with closing(sqlite3.connect(source_db)) as source:
        source_schema_row = source.execute(
            "SELECT value FROM meta WHERE key = 'schema_version'"
        ).fetchone()
    assert source_schema_row is not None
    source_schema_version = source_schema_row[0]

    rc, _ = wal.create_bundle(
        source_db, bundle_dir, timestamp="2026-07-26T00:00:00Z"
    )
    assert rc == 0
    manifest_path = bundle_dir / wal.MANIFEST_NAME
    original_bytes = manifest_path.read_bytes()
    manifest = json.loads(original_bytes)

    print("SCRATCH_COPY=temporary-directory")
    print(f"SOURCE_SCHEMA_VERSION={source_schema_version}")
    print(
        "MANIFEST_SCHEMA_VERSION_BEFORE="
        f"{manifest['invariants']['schema_version']}"
    )

    manifest["invariants"]["schema_version"] = "999"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    mutated_schema_version = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )["invariants"]["schema_version"]
    print(f"MUTATED_MANIFEST_SCHEMA_VERSION={mutated_schema_version}")

    try:
        assert mutated_schema_version == source_schema_version
    except AssertionError:
        print("RED=AssertionError (mutated manifest differs from source database)")
    else:
        raise RuntimeError("mutation unexpectedly passed")
    finally:
        manifest_path.write_bytes(original_bytes)

    restored_schema_version = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )["invariants"]["schema_version"]
    assert restored_schema_version == source_schema_version
    print(f"RESTORED_MANIFEST_SCHEMA_VERSION={restored_schema_version}")
    print("GREEN=restored manifest matches source database")
'@ | python -
```

Real output and return code:

```text
rc=0
SCRATCH_COPY=temporary-directory
SOURCE_SCHEMA_VERSION=4
MANIFEST_SCHEMA_VERSION_BEFORE=4
MUTATED_MANIFEST_SCHEMA_VERSION=999
RED=AssertionError (mutated manifest differs from source database)
RESTORED_MANIFEST_SCHEMA_VERSION=4
GREEN=restored manifest matches source database
```

This demonstrates that the repaired assertion is not vacuous: a bundle that lies about
the captured database's schema version fails even though the source database remains v4.

## Focused repaired-test evidence

Exact command:

```powershell
$env:PYTHONUTF8='1'
python -m pytest IBKR_PAPER_BRIDGE\tests\test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate IBKR_PAPER_BRIDGE\tests\test_wal_state_bundle.py::test_invariants_preserve_risk_and_history -q -p no:cacheprovider
```

Real output:

```text
..                                                                       [100%]
2 passed in 0.83s
```

## Post-change full-suite evidence

Both runs used the same exact repository-root command as the baseline:

```powershell
$env:PYTHONUTF8='1'
python -m pytest IBKR_PAPER_BRIDGE\tests -q -p no:cacheprovider
```

Run 1:

```text
rc=0
1021 passed, 1 warning in 104.51s (0:01:44)
```

Run 2:

```text
rc=0
1021 passed, 1 warning in 88.60s (0:01:28)
```

Both warnings were the same installed-dependency `StarletteDeprecationWarning` described
in the pre-change run.

## Environment limitation and unverified items

```text
Python 3.14.2
pytest 9.0.2
IBKR_PAPER_BRIDGE/requirements.lock: pytest==9.1.1
```

These results are **provisional**. The lock pins pytest 9.1.1, while this machine has
pytest 9.0.2, and Python 3.14.2 is not the frozen target environment. The full suite must
be rerun at the exact release SHA in the frozen environment before deployment checklist
item 9 can be accepted.

No Linux/frozen-environment run, host action, deployment action, or independent Gate 5
acceptance was performed or claimed. This implementer does not accept its own work.

The resulting commit SHA cannot be embedded in the report bytes that the same commit
hashes. It is recorded immediately after commit with `git rev-parse HEAD` in the lane
completion handoff.
