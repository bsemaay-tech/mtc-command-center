# Gate-A-forward 33-path blob fence

Status: standalone read-only checking artifact. It records a tree fence only; it is not acceptance or authorization. The source runbook is likewise explicitly unexecuted and unauthorizing. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:1`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:22`)

## Frozen inputs and derivation result

- `M = 637307e83951ffe23e768ed8e50ddaf8712b0660` (`origin/master`). (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:34`)
- `G = 2ce41e34bceb599d80af24c5c33d835820ec321b` (Gate-A). (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:35`)
- `W = 6c746b65411d5e646da407614f95f8a1174f3a5a` (repaired WP-I). (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:36`)
- `B = 4d2228cf8985ce755c398cceff23f777a99d5404` (merge base). (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:37`)

The Bridge union is 33 paths. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:79`) I re-derived the union from `git diff --name-only B G -- IBKR_PAPER_BRIDGE` plus `git diff --name-only B W -- IBKR_PAPER_BRIDGE`, classified each path by comparing its `B`, `M`, `G`, and `W` blobs, and obtained **9 Gate-A-only + 1 WP-I-only + 2 changed-by-both + 21 WP-I-stale = 33**, with zero unclassified paths. The move from the older 10/1/1/21 design shape to 9/1/2/21 is the repaired WAL test: the runbook explicitly says that repair makes it a real both-changed file and records two changed-by-both paths, README and WAL. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:13`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:17`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:361`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:362`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:15`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:18`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:107`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:110`)

For every exact-source row below, the final OID was independently obtained with `git rev-parse <source-rev>:<path>`, the derivation method recorded by the runbook. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:470`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:475`) The two rows that the runbook labels synthesized were independently rebuilt in memory from source blobs obtained by `rev-parse`; their final Git blob OIDs were then calculated from the transformed bytes. The runbook also distinguishes those two synthesized identities from exact-source identities. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:477`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:497`)

**Runbook comparison: PASS -- 0 disagreements across 33 rows.** The independently derived values below match the runbook fence row-for-row. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:512`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:546`)

`Source line` means the frozen tree line that supplies the required bytes. `G exact` and `W exact` are direct tree blobs; `synthesized` names the prescribed bounded synthesis.

## Gate-A-only -- 9 paths

| Path | Source line | Exact expected blob OID | Evidence |
|---|---|---|---|
| `IBKR_PAPER_BRIDGE/bridge/app.py` | `G:<path>` exact | `572c4178fe804da17601eefd898027e9261492e6` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:515` |
| `IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template` | `G:<path>` exact | `c03d6e47ab57c00ef95f4122607fc7ba88119e35` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:524` |
| `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh` | `G:<path>` exact | `db11010a24edfbb96ba80ec1fbe1db3ff29193c9` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:525` |
| `IBKR_PAPER_BRIDGE/deploy/linux/package.sh` | `G:<path>` exact | `add6478d33cce8d929d58f895407abe01d51da20` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:526` |
| `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template` | `G:<path>` exact | `c18232549d96aa200d8c7f796e64de743288940c` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:529` |
| `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh` | `G:<path>` exact | `5cfefd709202ff504ae7b7fc3504b8c0b00900b6` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:530` |
| `IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py` | `G:<path>` exact | `ce0ae7c24f795dc8e5d56bf7cca82e1a75351402` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:536` |
| `IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py` | `G:<path>` exact | `64e25888ba67a6b706bbf5c9d5e5feb8f12a98b2` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:539` |
| `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` | `G:<path>` exact | `26c077e650ab88ba2086efa3a80790769bc055b1` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:546` |

## WP-I-only -- 1 path

| Path | Source line | Exact expected blob OID | Evidence |
|---|---|---|---|
| `IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md` | `W:<path>` exact | `8db2e6dd7e782c96f585f6672c4489c4ce5c1488` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:528` |

## Changed-by-both -- 2 paths

| Path | Source line | Exact expected blob OID | Evidence |
|---|---|---|---|
| `IBKR_PAPER_BRIDGE/deploy/linux/README.md` | synthesized: three-way `B/W/G` README merge plus exact status/history correction | `4069904b7707da9efa875661769fc29435504b33` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:527` |
| `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py` | synthesized: `G:<path>` exact base plus accepted A2 repair | `12b17ab595dad24fcff6397d0689effadbfe2f67` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:545` |

The independent synthesis reproduced `README_AUTO_MERGE_OID=f1803b54ee987e94182eb8c4f24af490f27d4162`, final README OID `4069904b7707da9efa875661769fc29435504b33`, and final WAL OID `12b17ab595dad24fcff6397d0689effadbfe2f67`. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:505`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:509`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:497`)

## WP-I-stale -- 21 paths

| Path | Source line | Exact expected blob OID | Evidence |
|---|---|---|---|
| `IBKR_PAPER_BRIDGE/bridge/api/routes.py` | `G:<path>` exact | `140bf003ecbcb6b7f47822c15f2dbdb83118f0df` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:514` |
| `IBKR_PAPER_BRIDGE/README.md` | `G:<path>` exact | `cfc15b212121b4a9f3adac3d18f02574c5aa74e7` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:534` |
| `IBKR_PAPER_BRIDGE/bridge/broker/base.py` | `G:<path>` exact | `0698e4862ea6390c0cec5db34b85602d336e33e1` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:516` |
| `IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py` | `G:<path>` exact | `855a17cd83c7d176576d810be5d520dbf1e5eba4` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:517` |
| `IBKR_PAPER_BRIDGE/bridge/broker/mock.py` | `G:<path>` exact | `295c0a9cd06a0ca6b36cb4e691dab54555cc5670` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:518` |
| `IBKR_PAPER_BRIDGE/bridge/engine/engine.py` | `G:<path>` exact | `0c115ff18489108daa015c35c1ef1e85bc2bbbf0` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:519` |
| `IBKR_PAPER_BRIDGE/bridge/engine/orders.py` | `G:<path>` exact | `608a3afe1015c7a98e08f7d4f1bb08ea8cebae89` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:520` |
| `IBKR_PAPER_BRIDGE/bridge/engine/reconcile.py` | `G:<path>` exact | `ea3ff95d93e92ef2e224c5fa9ad18e1b64fab4b0` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:521` |
| `IBKR_PAPER_BRIDGE/bridge/engine/types.py` | `G:<path>` exact | `2927968d7bfc5253e2011172610a8ff7ca676647` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:522` |
| `IBKR_PAPER_BRIDGE/bridge/store/db.py` | `G:<path>` exact | `ae5eb1b7ab2a9a6240932958c73ba4acdfe2a30e` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:523` |
| `IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md` | `G:<path>` exact | `a09b22bedb4e1a4e0ce9dc943983dd6cf399674d` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:531` |
| `IBKR_PAPER_BRIDGE/docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md` | `G:<path>` exact | `b02694c2e64061480843a8d76361d72034d46010` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:532` |
| `IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md` | `G:<path>` exact | `23480737ee802bdad7c03a93e06d5989e22cfb58` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:533` |
| `IBKR_PAPER_BRIDGE/tests/test_api.py` | `G:<path>` exact | `40d31925ac93c4bfe13a877f060b5abaf6c0cd6e` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:535` |
| `IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py` | `G:<path>` exact | `817afe17b00c5a7525e5d422b965fe260b802006` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:537` |
| `IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py` | `G:<path>` exact | `3851340462fe0269a019bbbd2608e4db97d9ce8b` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:538` |
| `IBKR_PAPER_BRIDGE/tests/test_mock_broker.py` | `G:<path>` exact | `bed96cea0f31cc7a7010ca790b0d03f219ab9c2a` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:540` |
| `IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py` | `G:<path>` exact | `9e50c1b51cd6d60967f5481adfeda9779815efd9` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:541` |
| `IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py` | `G:<path>` exact | `7b0b9ea36dd8b15108f6befcbcb00015ed2f51fb` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:542` |
| `IBKR_PAPER_BRIDGE/tests/test_reconciliation.py` | `G:<path>` exact | `9e6b015d84371c50b92bf25b12ee1f80c64bb581` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:543` |
| `IBKR_PAPER_BRIDGE/tests/test_store.py` | `G:<path>` exact | `d911d983f0b76f752836ae220bc4ec61f04b98a2` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:544` |

## Short candidate-tree verification recipe

Set `$Candidate` to a candidate commit or tree OID and run from PowerShell. This is read-only: it resolves blobs from the candidate tree, stops at the first absent/mismatched path, and otherwise prints one PASS. The runbook requires all 33 rows to match and treats any absent or mismatched row as a stop. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:593`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:595`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:598`)

```powershell
$Repo = 'C:\RO'
$Candidate = '<candidate-commit-or-tree-oid>'

$FenceText = @'
IBKR_PAPER_BRIDGE/bridge/api/routes.py|140bf003ecbcb6b7f47822c15f2dbdb83118f0df
IBKR_PAPER_BRIDGE/bridge/app.py|572c4178fe804da17601eefd898027e9261492e6
IBKR_PAPER_BRIDGE/bridge/broker/base.py|0698e4862ea6390c0cec5db34b85602d336e33e1
IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py|855a17cd83c7d176576d810be5d520dbf1e5eba4
IBKR_PAPER_BRIDGE/bridge/broker/mock.py|295c0a9cd06a0ca6b36cb4e691dab54555cc5670
IBKR_PAPER_BRIDGE/bridge/engine/engine.py|0c115ff18489108daa015c35c1ef1e85bc2bbbf0
IBKR_PAPER_BRIDGE/bridge/engine/orders.py|608a3afe1015c7a98e08f7d4f1bb08ea8cebae89
IBKR_PAPER_BRIDGE/bridge/engine/reconcile.py|ea3ff95d93e92ef2e224c5fa9ad18e1b64fab4b0
IBKR_PAPER_BRIDGE/bridge/engine/types.py|2927968d7bfc5253e2011172610a8ff7ca676647
IBKR_PAPER_BRIDGE/bridge/store/db.py|ae5eb1b7ab2a9a6240932958c73ba4acdfe2a30e
IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template|c03d6e47ab57c00ef95f4122607fc7ba88119e35
IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh|db11010a24edfbb96ba80ec1fbe1db3ff29193c9
IBKR_PAPER_BRIDGE/deploy/linux/package.sh|add6478d33cce8d929d58f895407abe01d51da20
IBKR_PAPER_BRIDGE/deploy/linux/README.md|4069904b7707da9efa875661769fc29435504b33
IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md|8db2e6dd7e782c96f585f6672c4489c4ce5c1488
IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template|c18232549d96aa200d8c7f796e64de743288940c
IBKR_PAPER_BRIDGE/deploy/linux/verify.sh|5cfefd709202ff504ae7b7fc3504b8c0b00900b6
IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md|a09b22bedb4e1a4e0ce9dc943983dd6cf399674d
IBKR_PAPER_BRIDGE/docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md|b02694c2e64061480843a8d76361d72034d46010
IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md|23480737ee802bdad7c03a93e06d5989e22cfb58
IBKR_PAPER_BRIDGE/README.md|cfc15b212121b4a9f3adac3d18f02574c5aa74e7
IBKR_PAPER_BRIDGE/tests/test_api.py|40d31925ac93c4bfe13a877f060b5abaf6c0cd6e
IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py|ce0ae7c24f795dc8e5d56bf7cca82e1a75351402
IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py|817afe17b00c5a7525e5d422b965fe260b802006
IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py|3851340462fe0269a019bbbd2608e4db97d9ce8b
IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py|64e25888ba67a6b706bbf5c9d5e5feb8f12a98b2
IBKR_PAPER_BRIDGE/tests/test_mock_broker.py|bed96cea0f31cc7a7010ca790b0d03f219ab9c2a
IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py|9e50c1b51cd6d60967f5481adfeda9779815efd9
IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py|7b0b9ea36dd8b15108f6befcbcb00015ed2f51fb
IBKR_PAPER_BRIDGE/tests/test_reconciliation.py|9e6b015d84371c50b92bf25b12ee1f80c64bb581
IBKR_PAPER_BRIDGE/tests/test_store.py|d911d983f0b76f752836ae220bc4ec61f04b98a2
IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py|12b17ab595dad24fcff6397d0689effadbfe2f67
IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py|26c077e650ab88ba2086efa3a80790769bc055b1
'@

$Fence = @($FenceText -split '\r?\n' | Where-Object { $_ } | ForEach-Object {
    $parts = $_ -split '\|', 2
    [pscustomobject]@{ Path = $parts[0]; Oid = $parts[1] }
})

if ($Fence.Count -ne 33) {
    Write-Output "BLOB_FENCE=FAIL reason=row-count expected=33 observed=$($Fence.Count)"
    exit 1
}

$CandidateTree = git -C $Repo rev-parse "$Candidate`^{tree}" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Output "BLOB_FENCE=FAIL reason=unresolvable-candidate candidate=$Candidate"
    exit 1
}

foreach ($row in $Fence) {
    $actual = git -C $Repo rev-parse "$Candidate`:$($row.Path)" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Output "BLOB_FENCE=FAIL path=$($row.Path) expected=$($row.Oid) observed=<absent>"
        exit 1
    }
    if ($actual -cne $row.Oid) {
        Write-Output "BLOB_FENCE=FAIL path=$($row.Path) expected=$($row.Oid) observed=$actual"
        exit 1
    }
}

Write-Output "BLOB_FENCE=PASS count=33 candidate_tree=$CandidateTree"
```

Expected success form: `BLOB_FENCE=PASS count=33 candidate_tree=<exact-tree-oid>`. A missing row, mismatch, or any changed file outside the 33-path union is a stop in the source runbook. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:615`, `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:618`)
