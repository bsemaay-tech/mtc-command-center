Status: RUNBOOK — NOT EXECUTED, NOT AUTHORIZED TO EXECUTE

# Bridge release integration merge runbook — 2026-08-15

## Critical prediction and operating boundary

**The repaired input does produce textual conflict markers.** Read-only
`git merge-tree` against repaired WP-I commit `6c746b65` predicts two conflict
hunks, both in
`IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py`: one import hunk and one
schema-version assertion hunk. It predicts zero markers in
`IBKR_PAPER_BRIDGE/deploy/linux/README.md`, although that file still requires a
semantic status correction. No other conflict path is predicted.

This corrects the older zero-marker prediction made before the repair commit
existed. The accepted design's repair-branch caveat anticipated that the WAL
test could become a real both-changed file and prescribed the resolution used
below: start from the complete Gate-A test and replay only the accepted anomaly
repair. Any marker or conflict outside that exact WAL test is unanticipated and
is a hard stop.

This document is a T2 documentation/evidence artifact. The future integrated
candidate is still T0. Nothing here authorizes execution, deployment, host or
network contact, a service action, credentials, broker/exchange contact, ARM,
orders, TESTNET/mainnet, Pine/parity/MTC/trading changes, merge to `master`, or
push. When separately authorized, the operator must run these commands exactly
and must stop rather than improvise whenever this runbook says `STOP`.

## 1. Frozen inputs and read-only evidence

| Name | Exact identity |
|---|---|
| Runbook-authoring worktree | `C:\MRGRUN`, detached at `93479b0e5923b8288ba47dd0dcc5cf8ebf0e096f` |
| `origin/master` (`M`) | `637307e83951ffe23e768ed8e50ddaf8712b0660` |
| Gate-A (`G`) | `2ce41e34bceb599d80af24c5c33d835820ec321b` |
| Repaired WP-I (`W`) | `6c746b65411d5e646da407614f95f8a1174f3a5a` |
| Merge base (`B`) | `4d2228cf8985ce755c398cceff23f777a99d5404` |

The authoring preflight was run exactly as follows:

```powershell
git -C C:\MRGRUN rev-parse HEAD
git -C C:\MRGRUN status --porcelain
git -C C:\MRGRUN symbolic-ref -q --short HEAD
```

Real output:

```text
93479b0e5923b8288ba47dd0dcc5cf8ebf0e096f
<no status output>
<no symbolic-ref output; rc=1, detached HEAD>
```

Frozen-object and topology commands:

```powershell
git -C C:\MRGRUN rev-parse origin/master
git -C C:\MRGRUN rev-parse 2ce41e34bceb599d80af24c5c33d835820ec321b
git -C C:\MRGRUN rev-parse 6c746b65
git -C C:\MRGRUN merge-base 6c746b65 2ce41e34
git -C C:\MRGRUN merge-base --is-ancestor origin/master 2ce41e34
git -C C:\MRGRUN merge-base --is-ancestor 2ce41e34 6c746b65
git -C C:\MRGRUN merge-base --is-ancestor 6c746b65 2ce41e34
```

Real output:

```text
637307e83951ffe23e768ed8e50ddaf8712b0660
2ce41e34bceb599d80af24c5c33d835820ec321b
6c746b65411d5e646da407614f95f8a1174f3a5a
4d2228cf8985ce755c398cceff23f777a99d5404
master_ancestor_of_G_rc=0
G_ancestor_of_W_rc=1
W_ancestor_of_G_rc=1
```

The three-way union contains 33 Bridge paths. Gate-A also differs from the
merge base at root `.gitattributes`, but repaired WP-I already has the exact
same blob, so the merge must not change that outside-union path:

```powershell
git -C C:\MRGRUN rev-parse 2ce41e34:.gitattributes
git -C C:\MRGRUN rev-parse 6c746b65:.gitattributes
```

```text
49c0fbe4f5f995ebaa9fc4e16b2da29c5389087b
49c0fbe4f5f995ebaa9fc4e16b2da29c5389087b
```

Read-only prediction command:

```powershell
git -C C:\MRGRUN merge-tree `
  4d2228cf8985ce755c398cceff23f777a99d5404 `
  6c746b65411d5e646da407614f95f8a1174f3a5a `
  2ce41e34bceb599d80af24c5c33d835820ec321b
```

The real output is 16,359 lines. The exact parsed result was:

```text
MERGE_TREE_RC=0
MERGE_TREE_LINE_COUNT=16359
changed in both=2
added in remote=3
CHANGED_BOTH_PATH=IBKR_PAPER_BRIDGE/deploy/linux/README.md MARKER_LINES=0
CHANGED_BOTH_PATH=IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py MARKER_LINES=6
CONFLICT_HUNK_COUNT=2
```

The two marker hunks are exactly:

```diff
 import sqlite3
+<<<<<<< .our
 from contextlib import closing
+=======
+import struct
+import threading
+>>>>>>> .their
```

```diff
     assert inv["app_state"] == "DISARMED"
+<<<<<<< .our
     assert inv["schema_version"] == source_schema_row[0]
+=======
+    # The merged TS-P1 chain moved the operational baseline from v2 to v4;
+    # this assertion was never updated with Store.initialize()'s default.
+    assert inv["schema_version"] == str(SCHEMA_VERSION_BASELINE)
+>>>>>>> .their
```

The first parent already carries `.gitattributes` repair A1. The WAL resolution
below carries repair A2 by querying the fixture source's schema version and
asserting the manifest matches it. `test_linux_deployment.py` itself was not
changed by the repair commit and therefore remains the exact Gate-A blob.

## 2. Exact operator command sequence

### 2.1 Set frozen variables and prove the frozen objects

Run in PowerShell. Do not alter any value.

```powershell
$SourceRepo = 'C:\MRGRUN'
$IntegrationPath = 'C:\BRIDGE_RELEASE_INTEGRATION_20260815'
$IntegrationBranch = 'integration/bridge-release-20260815'
$Master = '637307e83951ffe23e768ed8e50ddaf8712b0660'
$GateA = '2ce41e34bceb599d80af24c5c33d835820ec321b'
$RepairedWpi = '6c746b65411d5e646da407614f95f8a1174f3a5a'
$Base = '4d2228cf8985ce755c398cceff23f777a99d5404'

function Assert-Exact([string]$Label, [string]$Actual, [string]$Expected) {
    if ($Actual -cne $Expected) {
        throw "STOP: $Label expected '$Expected' but observed '$Actual'."
    }
    Write-Output "$Label=$Actual"
}

if (Test-Path -LiteralPath $IntegrationPath) {
    throw "STOP: target path already exists: $IntegrationPath"
}
git -C $SourceRepo show-ref --verify --quiet "refs/heads/$IntegrationBranch"
if ($LASTEXITCODE -eq 0) {
    throw "STOP: branch already exists: $IntegrationBranch"
}
if ($LASTEXITCODE -ne 1) {
    throw "STOP: show-ref returned unexpected rc=$LASTEXITCODE"
}
Write-Output 'TARGET_PATH=<absent>'
Write-Output 'TARGET_BRANCH=<absent>'

Assert-Exact 'MASTER' (git -C $SourceRepo rev-parse 'origin/master^{commit}') $Master
Assert-Exact 'GATE_A' (git -C $SourceRepo rev-parse "$GateA^{commit}") $GateA
Assert-Exact 'REPAIRED_WPI' (git -C $SourceRepo rev-parse "$RepairedWpi^{commit}") $RepairedWpi
Assert-Exact 'MERGE_BASE' (git -C $SourceRepo merge-base $RepairedWpi $GateA) $Base

git -C $SourceRepo merge-base --is-ancestor $Master $GateA
if ($LASTEXITCODE -ne 0) { throw 'STOP: origin/master is not an ancestor of Gate-A.' }
git -C $SourceRepo merge-base --is-ancestor $GateA $RepairedWpi
if ($LASTEXITCODE -ne 1) { throw 'STOP: Gate-A/WP-I ancestry changed.' }
git -C $SourceRepo merge-base --is-ancestor $RepairedWpi $GateA
if ($LASTEXITCODE -ne 1) { throw 'STOP: WP-I/Gate-A ancestry changed.' }

$GateAttributes = git -C $SourceRepo rev-parse "$GateA`:.gitattributes"
$WpiAttributes = git -C $SourceRepo rev-parse "$RepairedWpi`:.gitattributes"
Assert-Exact 'GATE_A_GITATTRIBUTES' $GateAttributes '49c0fbe4f5f995ebaa9fc4e16b2da29c5389087b'
Assert-Exact 'WPI_GITATTRIBUTES' $WpiAttributes '49c0fbe4f5f995ebaa9fc4e16b2da29c5389087b'
```

Expected output is the labels followed by the exact identities above, absent
target path/branch, and both `.gitattributes` values equal to `49c0fbe4…`.
The source worktree's historical authoring state is already recorded in §1;
`git worktree add` consumes frozen objects, not its working-tree files. Any
thrown `STOP` terminates the procedure.

### 2.2 Reproduce the merge-tree prediction before creating anything

```powershell
$Prediction = @(git -C $SourceRepo merge-tree $Base $RepairedWpi $GateA)
if ($LASTEXITCODE -ne 0) {
    throw "STOP: merge-tree returned rc=$LASTEXITCODE"
}

$ChangedBoth = @($Prediction | Where-Object { $_ -eq 'changed in both' })
$AddedRemote = @($Prediction | Where-Object { $_ -eq 'added in remote' })
$MarkerLines = @($Prediction | Where-Object {
    $_ -match '^\+?<<<<<<< |^\+?=======|^\+?>>>>>>> '
})

Write-Output "MERGE_TREE_LINE_COUNT=$($Prediction.Count)"
Write-Output "CHANGED_IN_BOTH_COUNT=$($ChangedBoth.Count)"
Write-Output "ADDED_IN_REMOTE_COUNT=$($AddedRemote.Count)"
Write-Output "CONFLICT_MARKER_LINE_COUNT=$($MarkerLines.Count)"

if ($Prediction.Count -ne 16359 -or
    $ChangedBoth.Count -ne 2 -or
    $AddedRemote.Count -ne 3 -or
    $MarkerLines.Count -ne 6) {
    throw 'STOP: merge-tree prediction differs from the frozen analysis.'
}
```

Expected:

```text
MERGE_TREE_LINE_COUNT=16359
CHANGED_IN_BOTH_COUNT=2
ADDED_IN_REMOTE_COUNT=3
CONFLICT_MARKER_LINE_COUNT=6
```

If any count differs, or inspection shows a marker outside
`tests/test_wal_state_bundle.py`, stop and escalate before branch creation.

### 2.3 Create the isolated integration worktree and branch

```powershell
git -C $SourceRepo worktree add -b $IntegrationBranch $IntegrationPath $RepairedWpi
if ($LASTEXITCODE -ne 0) { throw 'STOP: worktree/branch creation failed.' }

Assert-Exact 'INTEGRATION_START_HEAD' (git -C $IntegrationPath rev-parse HEAD) $RepairedWpi
Assert-Exact 'INTEGRATION_BRANCH' (git -C $IntegrationPath branch --show-current) $IntegrationBranch
$InitialStatus = @(git -C $IntegrationPath status --porcelain)
if ($InitialStatus.Count -ne 0) {
    $InitialStatus
    throw 'STOP: new integration worktree is not clean.'
}
Write-Output 'INTEGRATION_STATUS=<empty>'
```

Expected Git output begins with:

```text
Preparing worktree (new branch 'integration/bridge-release-20260815')
HEAD is now at 6c746b65 test(bridge): repair suite anomaly assertions
```

The three assertions must then print the repaired SHA, the exact branch name,
and empty status. A different subject-line presentation is cosmetic; a
different SHA, branch, return code, or status is `STOP`.

### 2.4 Start the Gate-A-forward merge

```powershell
git -C $IntegrationPath merge --no-ff --no-commit $GateA
$MergeRc = $LASTEXITCODE
Write-Output "MERGE_RC=$MergeRc"
if ($MergeRc -ne 1) {
    throw 'STOP: expected the known WAL content conflict and merge rc=1.'
}

$Unmerged = @(git -C $IntegrationPath diff --name-only --diff-filter=U)
$ExpectedUnmerged = @('IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py')
$UnmergedDelta = @(Compare-Object $ExpectedUnmerged $Unmerged)
$Unmerged
if ($UnmergedDelta.Count -ne 0) {
    $UnmergedDelta
    throw 'STOP: unmerged-path set differs from the one anticipated WAL test.'
}
```

Expected merge result is `rc=1`, with Git reporting automatic merge of the
Linux README and a content conflict only in
`IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py`, followed by:

```text
MERGE_RC=1
IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
```

The precise human-facing Git progress text is **MUST BE OBSERVED AT RUN TIME**;
the return code and unmerged-path set above are the binding prediction. If the
merge succeeds without the expected conflict, or names any other conflict,
stop. Do not continue with a different resolution.

### 2.5 Apply the two pre-resolved synthesized results

First replace the conflicted WAL test with the exact Gate-A blob in both index
and worktree:

```powershell
$WalPath = 'IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py'
git -C $IntegrationPath restore --source=$GateA --staged --worktree -- $WalPath
if ($LASTEXITCODE -ne 0) { throw 'STOP: could not restore the Gate-A WAL-test base.' }
```

Then run this exact bounded transformer. It writes only the Linux README and
the WAL test inside the integration worktree. Every replacement is guarded by
an exact one-match assertion, and it writes UTF-8/LF bytes.

```powershell
@'
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1])

def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    print(f"{label}_MATCH_COUNT={count}")
    if count != 1:
        raise SystemExit(f"STOP: {label} expected one match, observed {count}")
    return text.replace(old, new)

readme_path = root / "IBKR_PAPER_BRIDGE/deploy/linux/README.md"
readme = readme_path.read_bytes().decode("utf-8")
for required in (
    "MTC_BRIDGE_START_MODE=credential_free_disarmed",
    "| `SECURITY_BASELINE.md` | WP-I pre-Gate-A pinned inventory,",
    "It is PRE-GATE-A / STATIC ONLY and is not an Ubuntu, built-payload,",
):
    if required not in readme:
        raise SystemExit(f"STOP: merged README lacks required text: {required}")

readme = replace_once(
    readme,
    "- Status: **PREPARATION ONLY \u2014 nothing here has been executed on any host.**",
    "- Status: **INTEGRATION PENDING \u2014 see the candidate-scoped execution history below; the newly integrated SHA has not been executed or accepted.**",
    "README_STATUS",
)
readme = replace_once(
    readme,
    "- These assets have **never been executed**, on KVM2 or anywhere else. No\n"
    "  Ubuntu run, no `install.sh` invocation, no `systemctl` call has happened.\n"
    "  Test coverage in `tests/test_linux_deployment.py` is structural only.\n",
    "- `SECURITY_BASELINE.md` remains dated historical evidence for the old WP-I\n"
    "  static baseline; it does not establish the status of these integrated bytes.\n"
    "  Exact candidate `2ce41e34bceb599d80af24c5c33d835820ec321b` was installed\n"
    "  and executed on the disposable Gate-A staging host and passed A-0 through A-9\n"
    "  under the boundary recorded in\n"
    "  `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A9_PASS_FINAL_2026-08-09D.md`.\n"
    "  The newly integrated SHA has not been installed, run, or accepted and must\n"
    "  repeat the full gate before any acceptance claim.\n",
    "README_HISTORY_PARAGRAPH",
)
readme_path.write_bytes(readme.encode("utf-8"))

wal_path = root / "IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py"
wal = wal_path.read_bytes().decode("utf-8")
wal = replace_once(
    wal,
    "import sqlite3\nimport struct",
    "import sqlite3\nfrom contextlib import closing\nimport struct",
    "WAL_IMPORT_CLOSING",
)
wal = replace_once(
    wal,
    "from bridge.store.db import SCHEMA_VERSION_BASELINE, Store",
    "from bridge.store.db import Store",
    "WAL_REMOVE_STALE_BASELINE_IMPORT",
)
wal = replace_once(
    wal,
    "def test_invariants_preserve_risk_and_history(source_db, bundle_dir, capsys):\n"
    "    rc, _ = create(source_db, bundle_dir, capsys)\n",
    "def test_invariants_preserve_risk_and_history(source_db, bundle_dir, capsys):\n"
    "    with closing(sqlite3.connect(source_db)) as source:\n"
    "        source_schema_row = source.execute(\n"
    "            \"SELECT value FROM meta WHERE key = 'schema_version'\"\n"
    "        ).fetchone()\n"
    "    assert source_schema_row is not None\n\n"
    "    rc, _ = create(source_db, bundle_dir, capsys)\n",
    "WAL_DYNAMIC_SOURCE_QUERY",
)
wal = replace_once(
    wal,
    "    # The merged TS-P1 chain moved the operational baseline from v2 to v4;\n"
    "    # this assertion was never updated with Store.initialize()'s default.\n"
    "    assert inv[\"schema_version\"] == str(SCHEMA_VERSION_BASELINE)\n",
    "    assert inv[\"schema_version\"] == source_schema_row[0]\n",
    "WAL_DYNAMIC_ASSERTION",
)
wal_path.write_bytes(wal.encode("utf-8"))

for path in (readme_path, wal_path):
    oid = subprocess.check_output(
        ["git", "-C", str(root), "hash-object", "--", str(path)], text=True
    ).strip()
    print(f"{path.relative_to(root).as_posix()}={oid}")
'@ | python - $IntegrationPath
if ($LASTEXITCODE -ne 0) { throw 'STOP: bounded synthesis failed.' }
```

Expected output:

```text
README_STATUS_MATCH_COUNT=1
README_HISTORY_PARAGRAPH_MATCH_COUNT=1
WAL_IMPORT_CLOSING_MATCH_COUNT=1
WAL_REMOVE_STALE_BASELINE_IMPORT_MATCH_COUNT=1
WAL_DYNAMIC_SOURCE_QUERY_MATCH_COUNT=1
WAL_DYNAMIC_ASSERTION_MATCH_COUNT=1
IBKR_PAPER_BRIDGE/deploy/linux/README.md=4069904b7707da9efa875661769fc29435504b33
IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py=12b17ab595dad24fcff6397d0689effadbfe2f67
```

Stage only those two resolved files:

```powershell
git -C $IntegrationPath add -- `
  'IBKR_PAPER_BRIDGE/deploy/linux/README.md' `
  'IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py'
if ($LASTEXITCODE -ne 0) { throw 'STOP: staging the two resolutions failed.' }

$StillUnmerged = @(git -C $IntegrationPath diff --name-only --diff-filter=U)
if ($StillUnmerged.Count -ne 0) {
    $StillUnmerged
    throw 'STOP: unmerged paths remain.'
}
git -C $IntegrationPath diff --cached --check
if ($LASTEXITCODE -ne 0) { throw 'STOP: whitespace errors or conflict markers remain.' }
```

Expected output is empty. Any output or nonzero return is `STOP`.

## 3. Exact README status correction

The automatic merge preserves Gate-A's unit-owned start-mode paragraph and
WP-I's `SECURITY_BASELINE.md` inventory/limitation, but it also preserves two
false unqualified execution claims. The transformer above replaces the top
status line and replaces the old known-limitations paragraph with exactly:

```text
- `SECURITY_BASELINE.md` remains dated historical evidence for the old WP-I
  static baseline; it does not establish the status of these integrated bytes.
  Exact candidate `2ce41e34bceb599d80af24c5c33d835820ec321b` was installed
  and executed on the disposable Gate-A staging host and passed A-0 through A-9
  under the boundary recorded in
  `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A9_PASS_FINAL_2026-08-09D.md`.
  The newly integrated SHA has not been installed, run, or accepted and must
  repeat the full gate before any acceptance claim.
```

The exact replacement status line is:

```text
- Status: **INTEGRATION PENDING — see the candidate-scoped execution history below; the newly integrated SHA has not been executed or accepted.**
```

This correction transfers no acceptance to the integrated SHA.

## 4. The 33-path blob fence

For exact-source rows, the OID was derived with:

```powershell
git -C C:\MRGRUN rev-parse '2ce41e34bceb599d80af24c5c33d835820ec321b:<path>'
git -C C:\MRGRUN rev-parse '6c746b65411d5e646da407614f95f8a1174f3a5a:<path>'
```

The two synthesized OIDs were derived by feeding the exact guarded transforms
to `git hash-object --stdin`; the original-byte control reproduced each source
OID first. Real synthesis output was:

```text
README_GATE_A_REVPARSE=f3f1d75e7e4369609cd0eb299466b2ceb62a0a16
README_GATE_A_HASH_OBJECT=f3f1d75e7e4369609cd0eb299466b2ceb62a0a16
README_STATUS_MATCH_COUNT=1
README_INVENTORY_MATCH_COUNT=1
README_HISTORY_PARAGRAPH_MATCH_COUNT=1
README_LIMITATION_MATCH_COUNT=1
README_SYNTHESIZED_BYTES=9964
README_SYNTHESIZED_OID=4069904b7707da9efa875661769fc29435504b33
WAL_GATE_A_REVPARSE=07de7b206f56c7442c3ea07ec160dc7ef2497415
WAL_GATE_A_HASH_OBJECT=07de7b206f56c7442c3ea07ec160dc7ef2497415
WAL_IMPORT_CLOSING_MATCH_COUNT=1
WAL_REMOVE_STALE_BASELINE_IMPORT_MATCH_COUNT=1
WAL_DYNAMIC_SOURCE_QUERY_MATCH_COUNT=1
WAL_DYNAMIC_ASSERTION_MATCH_COUNT=1
WAL_SYNTHESIZED_BYTES=55292
WAL_SYNTHESIZED_OID=12b17ab595dad24fcff6397d0689effadbfe2f67
```

As a separate control, the README section emitted by legacy `merge-tree` was
applied in memory to repaired WP-I's `our` blob, then the operator transform's
two replacements were applied. Real output:

```text
README_AUTO_MERGE_OID=f1803b54ee987e94182eb8c4f24af490f27d4162
README_AUTO_HAS_START_MODE=True
README_AUTO_HAS_WPI_INVENTORY=True
README_AUTO_HAS_WPI_LIMITATION=True
README_TRANSFORMED_AUTO_OID=4069904b7707da9efa875661769fc29435504b33
```

| Path | Required blob OID | Source |
|---|---|---|
| `IBKR_PAPER_BRIDGE/bridge/api/routes.py` | `140bf003ecbcb6b7f47822c15f2dbdb83118f0df` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/bridge/app.py` | `572c4178fe804da17601eefd898027e9261492e6` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/bridge/broker/base.py` | `0698e4862ea6390c0cec5db34b85602d336e33e1` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py` | `855a17cd83c7d176576d810be5d520dbf1e5eba4` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/bridge/broker/mock.py` | `295c0a9cd06a0ca6b36cb4e691dab54555cc5670` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/bridge/engine/engine.py` | `0c115ff18489108daa015c35c1ef1e85bc2bbbf0` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/bridge/engine/orders.py` | `608a3afe1015c7a98e08f7d4f1bb08ea8cebae89` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/bridge/engine/reconcile.py` | `ea3ff95d93e92ef2e224c5fa9ad18e1b64fab4b0` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/bridge/engine/types.py` | `2927968d7bfc5253e2011172610a8ff7ca676647` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/bridge/store/db.py` | `ae5eb1b7ab2a9a6240932958c73ba4acdfe2a30e` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template` | `c03d6e47ab57c00ef95f4122607fc7ba88119e35` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh` | `db11010a24edfbb96ba80ec1fbe1db3ff29193c9` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/deploy/linux/package.sh` | `add6478d33cce8d929d58f895407abe01d51da20` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/deploy/linux/README.md` | `4069904b7707da9efa875661769fc29435504b33` | Synthesized: automatic README merge plus exact status/history correction |
| `IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md` | `8db2e6dd7e782c96f585f6672c4489c4ce5c1488` | Repaired WP-I exact |
| `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template` | `c18232549d96aa200d8c7f796e64de743288940c` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh` | `5cfefd709202ff504ae7b7fc3504b8c0b00900b6` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md` | `a09b22bedb4e1a4e0ce9dc943983dd6cf399674d` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md` | `b02694c2e64061480843a8d76361d72034d46010` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md` | `23480737ee802bdad7c03a93e06d5989e22cfb58` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/README.md` | `cfc15b212121b4a9f3adac3d18f02574c5aa74e7` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/tests/test_api.py` | `40d31925ac93c4bfe13a877f060b5abaf6c0cd6e` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py` | `ce0ae7c24f795dc8e5d56bf7cca82e1a75351402` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py` | `817afe17b00c5a7525e5d422b965fe260b802006` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py` | `3851340462fe0269a019bbbd2608e4db97d9ce8b` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py` | `64e25888ba67a6b706bbf5c9d5e5feb8f12a98b2` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/tests/test_mock_broker.py` | `bed96cea0f31cc7a7010ca790b0d03f219ab9c2a` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py` | `9e50c1b51cd6d60967f5481adfeda9779815efd9` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py` | `7b0b9ea36dd8b15108f6befcbcb00015ed2f51fb` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/tests/test_reconciliation.py` | `9e6b015d84371c50b92bf25b12ee1f80c64bb581` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/tests/test_store.py` | `d911d983f0b76f752836ae220bc4ec61f04b98a2` | Gate-A exact |
| `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py` | `12b17ab595dad24fcff6397d0689effadbfe2f67` | Synthesized: Gate-A exact base plus accepted A2 repair |
| `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` | `26c077e650ab88ba2086efa3a80790769bc055b1` | Gate-A exact |

### 4.1 Execute the index fence and exact scope check

Run after staging the two resolutions and before tests or commit:

```powershell
$FenceText = @"
IBKR_PAPER_BRIDGE/bridge/api/routes.py`t140bf003ecbcb6b7f47822c15f2dbdb83118f0df
IBKR_PAPER_BRIDGE/bridge/app.py`t572c4178fe804da17601eefd898027e9261492e6
IBKR_PAPER_BRIDGE/bridge/broker/base.py`t0698e4862ea6390c0cec5db34b85602d336e33e1
IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py`t855a17cd83c7d176576d810be5d520dbf1e5eba4
IBKR_PAPER_BRIDGE/bridge/broker/mock.py`t295c0a9cd06a0ca6b36cb4e691dab54555cc5670
IBKR_PAPER_BRIDGE/bridge/engine/engine.py`t0c115ff18489108daa015c35c1ef1e85bc2bbbf0
IBKR_PAPER_BRIDGE/bridge/engine/orders.py`t608a3afe1015c7a98e08f7d4f1bb08ea8cebae89
IBKR_PAPER_BRIDGE/bridge/engine/reconcile.py`tea3ff95d93e92ef2e224c5fa9ad18e1b64fab4b0
IBKR_PAPER_BRIDGE/bridge/engine/types.py`t2927968d7bfc5253e2011172610a8ff7ca676647
IBKR_PAPER_BRIDGE/bridge/store/db.py`tae5eb1b7ab2a9a6240932958c73ba4acdfe2a30e
IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template`tc03d6e47ab57c00ef95f4122607fc7ba88119e35
IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh`tdb11010a24edfbb96ba80ec1fbe1db3ff29193c9
IBKR_PAPER_BRIDGE/deploy/linux/package.sh`tadd6478d33cce8d929d58f895407abe01d51da20
IBKR_PAPER_BRIDGE/deploy/linux/README.md`t4069904b7707da9efa875661769fc29435504b33
IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md`t8db2e6dd7e782c96f585f6672c4489c4ce5c1488
IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template`tc18232549d96aa200d8c7f796e64de743288940c
IBKR_PAPER_BRIDGE/deploy/linux/verify.sh`t5cfefd709202ff504ae7b7fc3504b8c0b00900b6
IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md`ta09b22bedb4e1a4e0ce9dc943983dd6cf399674d
IBKR_PAPER_BRIDGE/docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md`tb02694c2e64061480843a8d76361d72034d46010
IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md`t23480737ee802bdad7c03a93e06d5989e22cfb58
IBKR_PAPER_BRIDGE/README.md`tcfc15b212121b4a9f3adac3d18f02574c5aa74e7
IBKR_PAPER_BRIDGE/tests/test_api.py`t40d31925ac93c4bfe13a877f060b5abaf6c0cd6e
IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py`tce0ae7c24f795dc8e5d56bf7cca82e1a75351402
IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py`t817afe17b00c5a7525e5d422b965fe260b802006
IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py`t3851340462fe0269a019bbbd2608e4db97d9ce8b
IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py`t64e25888ba67a6b706bbf5c9d5e5feb8f12a98b2
IBKR_PAPER_BRIDGE/tests/test_mock_broker.py`tbed96cea0f31cc7a7010ca790b0d03f219ab9c2a
IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py`t9e50c1b51cd6d60967f5481adfeda9779815efd9
IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py`t7b0b9ea36dd8b15108f6befcbcb00015ed2f51fb
IBKR_PAPER_BRIDGE/tests/test_reconciliation.py`t9e6b015d84371c50b92bf25b12ee1f80c64bb581
IBKR_PAPER_BRIDGE/tests/test_store.py`td911d983f0b76f752836ae220bc4ec61f04b98a2
IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py`t12b17ab595dad24fcff6397d0689effadbfe2f67
IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py`t26c077e650ab88ba2086efa3a80790769bc055b1
"@

$Fence = @($FenceText -split '\r?\n' | Where-Object { $_ } | ForEach-Object {
    $parts = $_ -split "`t", 2
    [pscustomobject]@{ Path = $parts[0]; Oid = $parts[1] }
})
if ($Fence.Count -ne 33) { throw "STOP: fence row count is $($Fence.Count), not 33." }

foreach ($row in $Fence) {
    $actual = git -C $IntegrationPath rev-parse ":$($row.Path)"
    if ($LASTEXITCODE -ne 0 -or $actual -cne $row.Oid) {
        throw "STOP: blob fence mismatch at $($row.Path): expected $($row.Oid), observed $actual"
    }
    Write-Output "BLOB_OK $($row.Path) $actual"
}

$ExpectedChanged = @($Fence.Path |
    Where-Object { $_ -ne 'IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md' } |
    Sort-Object)
$ActualChanged = @(git -C $IntegrationPath diff --cached --name-only | Sort-Object)
$ScopeDelta = @(Compare-Object $ExpectedChanged $ActualChanged)
Write-Output "STAGED_PATH_COUNT=$($ActualChanged.Count)"
if ($ActualChanged.Count -ne 32 -or $ScopeDelta.Count -ne 0) {
    $ScopeDelta
    throw 'STOP: staged path set is not exactly the expected 32-path first-parent delta.'
}
```

Expected: 33 `BLOB_OK` lines and `STAGED_PATH_COUNT=32`. The baseline is in the
33-row tree fence but is unchanged from the first parent, hence 32 staged
paths. A mismatch, missing row, extra row, or any changed file outside the
33-path union is `STOP`.

## 5. Verification before creating the merge commit

### 5.1 Credential-free DISARMED presence fence

Gate-A has 17 exact occurrences across six paths. The integrated index must
have the same path set and occurrence count:

```powershell
$ExpectedCredentialPaths = @(
    'IBKR_PAPER_BRIDGE/bridge/api/routes.py'
    'IBKR_PAPER_BRIDGE/bridge/app.py'
    'IBKR_PAPER_BRIDGE/deploy/linux/README.md'
    'IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template'
    'IBKR_PAPER_BRIDGE/deploy/linux/verify.sh'
    'IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py'
) | Sort-Object

$CredentialPaths = @(git -C $IntegrationPath grep --cached -l --fixed-strings `
    'credential_free_disarmed' -- IBKR_PAPER_BRIDGE | Sort-Object)
$CredentialLines = @(git -C $IntegrationPath grep --cached -n --fixed-strings `
    'credential_free_disarmed' -- IBKR_PAPER_BRIDGE)
$CredentialDelta = @(Compare-Object $ExpectedCredentialPaths $CredentialPaths)

$CredentialPaths
Write-Output "CREDENTIAL_OCCURRENCE_COUNT=$($CredentialLines.Count)"
if ($CredentialDelta.Count -ne 0 -or $CredentialLines.Count -ne 17) {
    $CredentialDelta
    throw 'STOP: credential_free_disarmed presence differs from Gate-A.'
}
```

Expected: exactly the six paths above and
`CREDENTIAL_OCCURRENCE_COUNT=17`. The Gate-A evidence command actually run was:

```powershell
git -C C:\MRGRUN grep -n --fixed-strings credential_free_disarmed `
  2ce41e34bceb599d80af24c5c33d835820ec321b -- IBKR_PAPER_BRIDGE
```

### 5.2 Full local suite from repository root

The last accepted Windows figure of record at exact Gate-A was
`1360 passed, 1 warning`. The accepted WP-I repair changes no test-function
count; the integrated expected summary is therefore exactly
`1360 passed, 1 warning in <runtime>`. That expected integrated result has not
been executed in this authoring lane and **MUST BE OBSERVED AT RUN TIME**.

Run from the integration repository root with UTF-8 mode and pytest's cache
provider disabled:

```powershell
Set-Location -LiteralPath $IntegrationPath
$env:PYTHONUTF8 = '1'
$PytestOutput = @(python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests 2>&1)
$PytestRc = $LASTEXITCODE
$PytestOutput | ForEach-Object { Write-Output $_ }
$SuiteSummary = @($PytestOutput | Where-Object {
    $_ -match '^1360 passed, 1 warning in .+$'
})
if ($PytestRc -ne 0 -or $SuiteSummary.Count -ne 1) {
    throw "STOP: expected exactly '1360 passed, 1 warning in <runtime>'; rc=$PytestRc."
}
```

Expected final summary:

```text
1360 passed, 1 warning in <runtime>
```

Any passed-test count other than **1360** is a stop, not a rounding difference.
Any failure/error/skip/xpass/xfail count, a warning count other than **1**, a
nonzero return, or the absence/duplication of that summary is also a stop.

Prove that the test run did not alter the candidate:

```powershell
$Unstaged = @(git -C $IntegrationPath diff --name-only)
$Untracked = @(git -C $IntegrationPath ls-files --others --exclude-standard)
if ($Unstaged.Count -ne 0 -or $Untracked.Count -ne 0) {
    $Unstaged
    $Untracked
    throw 'STOP: the test run changed or created repository files.'
}

foreach ($row in $Fence) {
    $actual = git -C $IntegrationPath rev-parse ":$($row.Path)"
    if ($actual -cne $row.Oid) {
        throw "STOP: post-suite blob mismatch at $($row.Path)."
    }
}
Write-Output 'POST_SUITE_BLOB_FENCE=PASS'
```

Expected: `POST_SUITE_BLOB_FENCE=PASS` and no preceding path output.

## 6. Create and verify the branch-local merge commit

Only after every prior check passes:

```powershell
git -C $IntegrationPath commit -m 'Merge Gate-A into repaired WP-I release integration'
if ($LASTEXITCODE -ne 0) { throw 'STOP: merge commit failed; do not bypass hooks.' }

$IntegratedSha = git -C $IntegrationPath rev-parse HEAD
$IntegratedTree = git -C $IntegrationPath rev-parse 'HEAD^{tree}'
$Parents = @(git -C $IntegrationPath show -s --format='%P' HEAD) -split ' '

Write-Output "INTEGRATED_SHA=$IntegratedSha"
Write-Output "INTEGRATED_TREE=$IntegratedTree"
Write-Output "PARENT_1=$($Parents[0])"
Write-Output "PARENT_2=$($Parents[1])"

if ($Parents.Count -ne 2 -or
    $Parents[0] -cne $RepairedWpi -or
    $Parents[1] -cne $GateA) {
    throw 'STOP: merge-parent identity or order is wrong.'
}
Assert-Exact 'BRANCH_TIP' `
    (git -C $IntegrationPath rev-parse "refs/heads/$IntegrationBranch") `
    $IntegratedSha

foreach ($row in $Fence) {
    $actual = git -C $IntegrationPath rev-parse "HEAD`:$($row.Path)"
    if ($actual -cne $row.Oid) {
        throw "STOP: committed blob fence mismatch at $($row.Path)."
    }
}
Write-Output 'COMMITTED_BLOB_FENCE=PASS'

$CommittedChanged = @(git -C $IntegrationPath diff --name-only HEAD^1 HEAD | Sort-Object)
$CommittedScopeDelta = @(Compare-Object $ExpectedChanged $CommittedChanged)
Write-Output "COMMITTED_FIRST_PARENT_PATH_COUNT=$($CommittedChanged.Count)"
if ($CommittedChanged.Count -ne 32 -or $CommittedScopeDelta.Count -ne 0) {
    $CommittedScopeDelta
    throw 'STOP: committed first-parent scope differs from the exact 32-path delta.'
}

$FinalStatus = @(git -C $IntegrationPath status --porcelain)
if ($FinalStatus.Count -ne 0) {
    $FinalStatus
    throw 'STOP: integration worktree is not clean after commit.'
}
Write-Output 'FINAL_STATUS=<empty>'
Assert-Exact 'MASTER_UNCHANGED' (git -C $SourceRepo rev-parse origin/master) $Master
```

The commit command's branch-local commit SHA and tree OID cannot be known
without creating the merge commit. Both are **MUST BE OBSERVED AT RUN TIME** and
must be copied verbatim into later evidence. Required fixed output is:

```text
PARENT_1=6c746b65411d5e646da407614f95f8a1174f3a5a
PARENT_2=2ce41e34bceb599d80af24c5c33d835820ec321b
COMMITTED_BLOB_FENCE=PASS
COMMITTED_FIRST_PARENT_PATH_COUNT=32
FINAL_STATUS=<empty>
MASTER_UNCHANGED=637307e83951ffe23e768ed8e50ddaf8712b0660
```

This is the end of this runbook. Do not push, merge another branch, build an
artifact, contact a host, or claim acceptance. The new commit is only a local
integration candidate requiring the separately authorized T0 process and a
fresh full Gate-A run.

## 7. Stop list — halt and escalate, never improvise

Stop immediately on any of the following:

1. Any frozen commit, merge base, ancestry result, or `.gitattributes` blob
   differs from this runbook.
2. The integration path or branch already exists, or worktree creation does not
   start exactly from repaired WP-I `6c746b65…`.
3. `git merge-tree` differs from the recorded shape: two changed-in-both paths,
   three added-in-remote paths, and six marker lines/two hunks confined to
   `tests/test_wal_state_bundle.py`.
4. The real merge returns anything other than `rc=1`, or its unmerged-path set
   is anything other than the one WAL test.
5. A conflict marker appears anywhere except the two predicted WAL hunks, or
   any marker remains after the deterministic resolution.
6. Any guarded README/WAL replacement has a match count other than one, either
   synthesized blob OID differs, or the README lacks Gate-A start-mode text or
   WP-I baseline text.
7. Any row in the 33-path blob fence is absent or mismatched.
8. The staged or committed first-parent change set is not exactly the expected
   32 paths, including **any change outside the 33-path union**. Do not dismiss
   an outside-union path as metadata or merge noise.
9. `credential_free_disarmed` is not present exactly 17 times across the six
    recorded paths.
10. The full suite returns nonzero or reports anything other than exactly
    `1360 passed, 1 warning`. A different count is a stop, not a rounding
    difference.
11. Tests create an unstaged or untracked file, or change any fenced blob.
12. A commit hook fails. Do not use `--no-verify` or otherwise bypass it.
13. The merge commit does not have exactly two parents in the order repaired
    WP-I then Gate-A, its branch tip differs, its first-parent scope differs, or
    the final worktree is not clean.
14. The runtime integrated SHA or tree OID cannot be observed and recorded.
    Never substitute a guessed identity.
15. Any instruction or situation would require checkout/reset/stash of someone
    else's work, merge to `master`, push, deployment, host/network/service/
    credential/broker/exchange/ARM/order action, TESTNET/mainnet activity, or a
    Pine/parity/MTC/trading change. Those are outside this runbook's authority.

## 8. Final honesty boundary

This runbook was derived with read-only Git in `C:\MRGRUN`. No worktree or
branch was created, no merge was attempted, no index or ref was changed, no
suite was run against a synthesized integration tree, and no host or network
was contacted. The expected integrated suite count is a frozen acceptance
criterion derived from Gate-A's measured `1360 passed, 1 warning` baseline and
the repair's unchanged test-function count; it remains runtime evidence until
the exact integrated bytes produce it. The future merge commit and tree IDs are
also runtime observations, never guessed values.
