# BFV blob-fence verification against repaired WP-I tip

Date: 2026-08-16  
Audit tier: T2 documentation/evidence verification. The lane contract requires
self-execution and forbids sub-delegation, so no model audit was dispatched.

Status: read-only verification only. This report is not merge acceptance,
authorization, deployment evidence, or permission for any host, network, service,
broker/exchange, trading, push, or merge-to-master action. The task establishes
that boundary explicitly. (`C:\tmp\lane_kick\BFV.md:46`)

## Verdict

**PASS for the 33-path blob-content fence.** The current repaired WP-I tip
`7d4e9a96e07b34a0c3d92315912d7818168b830b` changes no fenced path relative to
the old repaired tip `6c746b65411d5e646da407614f95f8a1174f3a5a`.
The re-derived union is still 33 paths with the same classification:
**9 Gate-A-only + 1 WP-I-only + 2 changed-by-both + 21 WP-I-stale**. All 33
independently derived final OIDs equal the recorded values. **Blob-row
disagreements: 0.** The recorded table and its embedded 33-row recipe also agree
internally.

**The runbook's two-conflict-hunk prediction is CONFIRMED against the current
tips.** The current and old repaired tips produce byte-for-byte identical legacy
`git merge-tree` output: 16,359 lines, two `changed in both` sections, three
`added in remote` sections, six marker lines, and two conflict-start markers,
both in `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py`. The runbook predicts
the same file and the same import and schema-assertion hunks.
(`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:7`)

**Usability boundary:** the OID fence is current and usable unchanged as the
blob-content gate of a current-tip merge check. It is **not a complete standalone
merge acceptance test**. Its short recipe enforces the 33 listed rows but does
not detect a changed path outside the union, even though its prose says such a
path is a stop. The full runbook separately enforces the exact first-parent scope.
(`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:135`;
`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:150`;
`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:603`)

No fence OID needs regeneration. To make the existing documents themselves
current-tip artifacts, refresh the frozen WP-I identity/provenance from
`6c746b65...` to `7d4e9a96...` everywhere it controls the runbook's starting
commit, topology assertions, merge-tree command, first-parent expectation, and
final parent-order check. Keep the 33 OIDs and two synthesis hashes unchanged.
If the short fence recipe is intended to stand alone as a full merge acceptance
test, regenerate **the checker section only** so it also pins the current input
identities and enforces the exact candidate first-parent delta/no outside-union
paths. The runbook's `$ExpectedChanged`/`$ActualChanged` comparison is the already
specified enforcement pattern. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:603`)

## Source resolution and method

The detached worktree at `C:\RO` does not contain the recorded fence or the
self-confirming-pattern document. Both were resolved read-only from
`codex/rp7-r1-r4-repair-20260815`; the fence was introduced by commit
`cd735760d32158d4ef97e3bc4b9524c95f35f77b`. The merge-runbook blob is identical
at detached `HEAD` and that branch (`6a2799f0605e874a3bcc1c6602bd89379f1f8b12`).
No missing working-tree file was treated as evidence.

The task supplied the current Gate-A and repaired-tip identities and required
derivation before comparison. (`C:\tmp\lane_kick\BFV.md:9`;
`C:\tmp\lane_kick\BFV.md:17`; `C:\tmp\lane_kick\BFV.md:18`)
I first masked all existing OIDs while obtaining the path universe. I then ran
read-only Git against the supplied identities, derived the union and every source
blob, rebuilt the two synthesized blobs from current source bytes in memory, and
only then parsed and compared the recorded OIDs.

Resolved inputs:

| Name | Current derived identity | Recorded identity | Result |
|---|---|---|---|
| `M = origin/master` | `637307e83951ffe23e768ed8e50ddaf8712b0660` | `637307e83951ffe23e768ed8e50ddaf8712b0660` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:7`) |
| `G = Gate-A` | `2ce41e34bceb599d80af24c5c33d835820ec321b` | `2ce41e34bceb599d80af24c5c33d835820ec321b` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:8`) |
| `W = repaired WP-I` | `7d4e9a96e07b34a0c3d92315912d7818168b830b` | `6c746b65411d5e646da407614f95f8a1174f3a5a` | **DISAGREE: identity moved** (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:9`) |
| `B = merge-base(G,W)` | `4d2228cf8985ce755c398cceff23f777a99d5404` | `4d2228cf8985ce755c398cceff23f777a99d5404` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:10`) |

Commands used for identity, universe, and direct source blobs:

```powershell
git rev-parse origin/master
git rev-parse 2ce41e34bceb599d80af24c5c33d835820ec321b
git rev-parse 7d4e9a96
git rev-parse codex/bridge-suite-anomaly-repairs-20260815
git merge-base 2ce41e34bceb599d80af24c5c33d835820ec321b 7d4e9a96

git diff --name-only $B $G -- IBKR_PAPER_BRIDGE
git diff --name-only $B $W -- IBKR_PAPER_BRIDGE
git rev-parse "$G`:<path>"
git rev-parse "$W`:<path>"
```

Observed identity/universe result:

```text
M=637307e83951ffe23e768ed8e50ddaf8712b0660
G=2ce41e34bceb599d80af24c5c33d835820ec321b
W=7d4e9a96e07b34a0c3d92315912d7818168b830b
B=4d2228cf8985ce755c398cceff23f777a99d5404
merge-base(M,G)=637307e83951ffe23e768ed8e50ddaf8712b0660
merge-base(M,W)=4d2228cf8985ce755c398cceff23f777a99d5404
UNION_COUNT=33
```

The recorded document describes the same union and classification method but
against the older repaired tip. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:12`)

## Full re-derived fence

`G exact` and `W exact` mean the shown OID came directly from
`git rev-parse <current-rev>:<path>`. `Synth(G,W)` means the source blob OIDs
were first obtained by `rev-parse`, the source bytes reproduced those OIDs under
`git hash-object --stdin`, and the guarded deterministic current-source
transformation was hashed without using the recorded final OID as input. The
runbook itself distinguishes exact-source from synthesized rows.
(`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:470`;
`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:477`)

### Gate-A-only — 9 paths

| Path | Source | Re-derived OID | Recorded OID | Comparison |
|---|---|---|---|---|
| `IBKR_PAPER_BRIDGE/bridge/app.py` | G exact | `572c4178fe804da17601eefd898027e9261492e6` | `572c4178fe804da17601eefd898027e9261492e6` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:24`) |
| `IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template` | G exact | `c03d6e47ab57c00ef95f4122607fc7ba88119e35` | `c03d6e47ab57c00ef95f4122607fc7ba88119e35` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:25`) |
| `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh` | G exact | `db11010a24edfbb96ba80ec1fbe1db3ff29193c9` | `db11010a24edfbb96ba80ec1fbe1db3ff29193c9` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:26`) |
| `IBKR_PAPER_BRIDGE/deploy/linux/package.sh` | G exact | `add6478d33cce8d929d58f895407abe01d51da20` | `add6478d33cce8d929d58f895407abe01d51da20` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:27`) |
| `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template` | G exact | `c18232549d96aa200d8c7f796e64de743288940c` | `c18232549d96aa200d8c7f796e64de743288940c` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:28`) |
| `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh` | G exact | `5cfefd709202ff504ae7b7fc3504b8c0b00900b6` | `5cfefd709202ff504ae7b7fc3504b8c0b00900b6` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:29`) |
| `IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py` | G exact | `ce0ae7c24f795dc8e5d56bf7cca82e1a75351402` | `ce0ae7c24f795dc8e5d56bf7cca82e1a75351402` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:30`) |
| `IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py` | G exact | `64e25888ba67a6b706bbf5c9d5e5feb8f12a98b2` | `64e25888ba67a6b706bbf5c9d5e5feb8f12a98b2` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:31`) |
| `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` | G exact | `26c077e650ab88ba2086efa3a80790769bc055b1` | `26c077e650ab88ba2086efa3a80790769bc055b1` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:32`) |

### WP-I-only — 1 path

| Path | Source | Re-derived OID | Recorded OID | Comparison |
|---|---|---|---|---|
| `IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md` | W exact | `8db2e6dd7e782c96f585f6672c4489c4ce5c1488` | `8db2e6dd7e782c96f585f6672c4489c4ce5c1488` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:38`) |

### Changed-by-both — 2 paths

| Path | Source | Re-derived OID | Recorded OID | Comparison |
|---|---|---|---|---|
| `IBKR_PAPER_BRIDGE/deploy/linux/README.md` | Synth(G,W) | `4069904b7707da9efa875661769fc29435504b33` | `4069904b7707da9efa875661769fc29435504b33` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:44`) |
| `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py` | Synth(G,W) | `12b17ab595dad24fcff6397d0689effadbfe2f67` | `12b17ab595dad24fcff6397d0689effadbfe2f67` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:45`) |

### WP-I-stale — 21 paths

| Path | Source | Re-derived OID | Recorded OID | Comparison |
|---|---|---|---|---|
| `IBKR_PAPER_BRIDGE/bridge/api/routes.py` | G exact | `140bf003ecbcb6b7f47822c15f2dbdb83118f0df` | `140bf003ecbcb6b7f47822c15f2dbdb83118f0df` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:53`) |
| `IBKR_PAPER_BRIDGE/README.md` | G exact | `cfc15b212121b4a9f3adac3d18f02574c5aa74e7` | `cfc15b212121b4a9f3adac3d18f02574c5aa74e7` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:54`) |
| `IBKR_PAPER_BRIDGE/bridge/broker/base.py` | G exact | `0698e4862ea6390c0cec5db34b85602d336e33e1` | `0698e4862ea6390c0cec5db34b85602d336e33e1` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:55`) |
| `IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py` | G exact | `855a17cd83c7d176576d810be5d520dbf1e5eba4` | `855a17cd83c7d176576d810be5d520dbf1e5eba4` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:56`) |
| `IBKR_PAPER_BRIDGE/bridge/broker/mock.py` | G exact | `295c0a9cd06a0ca6b36cb4e691dab54555cc5670` | `295c0a9cd06a0ca6b36cb4e691dab54555cc5670` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:57`) |
| `IBKR_PAPER_BRIDGE/bridge/engine/engine.py` | G exact | `0c115ff18489108daa015c35c1ef1e85bc2bbbf0` | `0c115ff18489108daa015c35c1ef1e85bc2bbbf0` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:58`) |
| `IBKR_PAPER_BRIDGE/bridge/engine/orders.py` | G exact | `608a3afe1015c7a98e08f7d4f1bb08ea8cebae89` | `608a3afe1015c7a98e08f7d4f1bb08ea8cebae89` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:59`) |
| `IBKR_PAPER_BRIDGE/bridge/engine/reconcile.py` | G exact | `ea3ff95d93e92ef2e224c5fa9ad18e1b64fab4b0` | `ea3ff95d93e92ef2e224c5fa9ad18e1b64fab4b0` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:60`) |
| `IBKR_PAPER_BRIDGE/bridge/engine/types.py` | G exact | `2927968d7bfc5253e2011172610a8ff7ca676647` | `2927968d7bfc5253e2011172610a8ff7ca676647` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:61`) |
| `IBKR_PAPER_BRIDGE/bridge/store/db.py` | G exact | `ae5eb1b7ab2a9a6240932958c73ba4acdfe2a30e` | `ae5eb1b7ab2a9a6240932958c73ba4acdfe2a30e` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:62`) |
| `IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md` | G exact | `a09b22bedb4e1a4e0ce9dc943983dd6cf399674d` | `a09b22bedb4e1a4e0ce9dc943983dd6cf399674d` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:63`) |
| `IBKR_PAPER_BRIDGE/docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md` | G exact | `b02694c2e64061480843a8d76361d72034d46010` | `b02694c2e64061480843a8d76361d72034d46010` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:64`) |
| `IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md` | G exact | `23480737ee802bdad7c03a93e06d5989e22cfb58` | `23480737ee802bdad7c03a93e06d5989e22cfb58` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:65`) |
| `IBKR_PAPER_BRIDGE/tests/test_api.py` | G exact | `40d31925ac93c4bfe13a877f060b5abaf6c0cd6e` | `40d31925ac93c4bfe13a877f060b5abaf6c0cd6e` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:66`) |
| `IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py` | G exact | `817afe17b00c5a7525e5d422b965fe260b802006` | `817afe17b00c5a7525e5d422b965fe260b802006` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:67`) |
| `IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py` | G exact | `3851340462fe0269a019bbbd2608e4db97d9ce8b` | `3851340462fe0269a019bbbd2608e4db97d9ce8b` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:68`) |
| `IBKR_PAPER_BRIDGE/tests/test_mock_broker.py` | G exact | `bed96cea0f31cc7a7010ca790b0d03f219ab9c2a` | `bed96cea0f31cc7a7010ca790b0d03f219ab9c2a` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:69`) |
| `IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py` | G exact | `9e50c1b51cd6d60967f5481adfeda9779815efd9` | `9e50c1b51cd6d60967f5481adfeda9779815efd9` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:70`) |
| `IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py` | G exact | `7b0b9ea36dd8b15108f6befcbcb00015ed2f51fb` | `7b0b9ea36dd8b15108f6befcbcb00015ed2f51fb` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:71`) |
| `IBKR_PAPER_BRIDGE/tests/test_reconciliation.py` | G exact | `9e6b015d84371c50b92bf25b12ee1f80c64bb581` | `9e6b015d84371c50b92bf25b12ee1f80c64bb581` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:72`) |
| `IBKR_PAPER_BRIDGE/tests/test_store.py` | G exact | `d911d983f0b76f752836ae220bc4ec61f04b98a2` | `d911d983f0b76f752836ae220bc4ec61f04b98a2` | MATCH (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:73`) |

## Synthesized-row derivation evidence

The direct source-byte controls were:

```text
README_G_REVPARSE=f3f1d75e7e4369609cd0eb299466b2ceb62a0a16
README_G_HASH_STDIN=f3f1d75e7e4369609cd0eb299466b2ceb62a0a16
README_WOLD_REVPARSE=666b79d834f50433cd0cba7c88224fb674fdbb56
README_WOLD_HASH_STDIN=666b79d834f50433cd0cba7c88224fb674fdbb56
README_W_REVPARSE=666b79d834f50433cd0cba7c88224fb674fdbb56
README_W_HASH_STDIN=666b79d834f50433cd0cba7c88224fb674fdbb56
WAL_G_REVPARSE=07de7b206f56c7442c3ea07ec160dc7ef2497415
WAL_G_HASH_STDIN=07de7b206f56c7442c3ea07ec160dc7ef2497415
WAL_WOLD_REVPARSE=91db6c407c60752ba95abd366029a88bba9036a5
WAL_WOLD_HASH_STDIN=91db6c407c60752ba95abd366029a88bba9036a5
WAL_W_REVPARSE=91db6c407c60752ba95abd366029a88bba9036a5
WAL_W_HASH_STDIN=91db6c407c60752ba95abd366029a88bba9036a5
```

Every guarded current-source replacement matched exactly once:

```text
README_REPLAY_W_INVENTORY_MATCH_COUNT=1
README_REPLAY_W_LIMITATION_MATCH_COUNT=1
README_STATUS_MATCH_COUNT=1
README_HISTORY_MATCH_COUNT=1
README_SYNTH_BYTES=9964
README_SYNTH_OID=4069904b7707da9efa875661769fc29435504b33
WAL_IMPORT_CLOSING_MATCH_COUNT=1
WAL_REMOVE_STALE_BASELINE_IMPORT_MATCH_COUNT=1
WAL_DYNAMIC_SOURCE_QUERY_MATCH_COUNT=1
WAL_DYNAMIC_ASSERTION_MATCH_COUNT=1
WAL_SYNTH_BYTES=55292
WAL_SYNTH_OID=12b17ab595dad24fcff6397d0689effadbfe2f67
```

The runbook defines the bounded synthesis and requires one match for each
replacement; the final hash above was computed from current transformed bytes,
not copied from its expected-output block.
(`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:301`;
`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:324`;
`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:407`)

## Every disagreement with the recorded version

There is exactly one current-input disagreement and zero blob-row disagreements:

| Item | Re-derived/current value | Recorded value | Effect |
|---|---|---|---|
| Repaired WP-I commit identity | `7d4e9a96e07b34a0c3d92315912d7818168b830b` | `6c746b65411d5e646da407614f95f8a1174f3a5a` | Provenance/runbook start is stale; no fenced OID changes. |

The recorded runbook explicitly freezes `W=6c746b65...`.
(`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:36`)
The current tip's only old-to-new change is:

```text
A  MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md
```

The same diff restricted to `IBKR_PAPER_BRIDGE` is empty. Direct `rev-parse`
controls also show that both changed-by-both source blobs are identical at old
and current repaired tips. The added audit record identifies itself as the
independent T1 audit and records an accepting `PASS-WITH-NITS` verdict.
(`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:1`;
`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:5`)

No recorded path has a derived-vs-recorded OID disagreement. No classification
changed. No synthesized byte count or hash changed. The recorded document's
33-row table and embedded 33-row recipe have zero internal OID disagreements.

## Current-tip conflict prediction cross-check

Executed read-only for both repaired tips:

```powershell
git merge-tree `
  4d2228cf8985ce755c398cceff23f777a99d5404 `
  7d4e9a96e07b34a0c3d92315912d7818168b830b `
  2ce41e34bceb599d80af24c5c33d835820ec321b
```

Parsed results:

```text
OLD_RC=0
OLD_LINE_COUNT=16359
OLD_CHANGED_BOTH=2
OLD_ADDED_REMOTE=3
OLD_MARKER_LINES=6
OLD_CONFLICT_HUNKS=2
CURRENT_RC=0
CURRENT_LINE_COUNT=16359
CURRENT_CHANGED_BOTH=2
CURRENT_ADDED_REMOTE=3
CURRENT_MARKER_LINES=6
CURRENT_CONFLICT_HUNKS=2
OLD_CURRENT_DELTA_LINES=0
```

The current `changed in both` headers identify only:

```text
IBKR_PAPER_BRIDGE/deploy/linux/README.md       marker lines=0
IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py marker lines=6
```

The two current WAL conflicts are the import choice (`closing` versus
`struct`/`threading`) and the dynamic source-schema assertion versus the stale
baseline assertion. These are exactly the two hunks printed by the runbook.
(`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:114`;
`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:126`)

**Prediction verdict: CONFIRMED, not merely repeated.** The expected shape came
from the runbook; the observed shape came from a fresh current-tip `merge-tree`
parse. The added T1 audit commit does not alter the prediction.

## Self-confirming-check analysis

The governing defect pattern is a check that can pass without proving its claim.
(`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:12`)
It requires asking what makes the check fail, where the expected value came from,
and whether the property is enforced or merely asserted.
(`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:47`;
`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:58`;
`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:63`)

| Check | What concrete state makes it fail? | Source of expected value | Enforced or asserted? |
|---|---|---|---|
| Input identity resolution | A supplied/local ref resolves to a different commit or cannot resolve. | Task-supplied exact identities plus Git object resolution, not the recorded fence. | Enforced in this verification by exact `rev-parse` comparison. No network freshness claim is made. |
| 33-path universe | A path exists in either `B..G` or `B..W` Bridge diff but is absent from the union, or the unique count is not 33. | Union of two independently executed scoped Git diffs. | Enforced in this verification by set union and count. |
| 31 exact-source fence rows | Any path is absent or its current source-tree OID differs from the later-read recorded OID. | Current `G:<path>` or `W:<path>` tree object. | Enforced by `rev-parse` and exact comparison. |
| Two synthesized rows | Any source bytes fail their rev-parse/hash control, any guarded replacement count is not one, or the computed result hash differs from the recorded value. | Current Git source blobs plus the runbook-defined deterministic resolution. | Enforced during derivation; every source control matched and every replacement count was one. |
| Repaired-tip movement | `git diff 6c746b65 7d4e9a96 -- IBKR_PAPER_BRIDGE` reports a path, or any current W source OID differs from old W. | The two actual Git trees, not the claim that an audit "should" be docs-only. | Enforced; scoped diff was empty and source controls matched. |
| Conflict prediction | Current merge-tree has a different changed-both path set, marker distribution, or hunk count. | Runbook prediction compared with fresh current-tip merge-tree output. | Enforced for this verification by parsing sections and marker contexts; prediction confirmed. The runbook's preflight code enforces counts, while marker location at prediction time still depends on inspection. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:209`) |
| Embedded short candidate-tree recipe | Candidate is unresolvable, row count differs from 33, a path is absent, or a listed OID differs. | Frozen independent OID table, now revalidated against current G/W. | Listed-row checks are enforced. **Exact merge scope is only asserted:** an extra changed path outside the 33-row universe does not make this recipe fail. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:124`; `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:135`) |

The last row is the important limitation. A candidate may satisfy all 33 OID
comparisons while carrying an unrelated extra change. Therefore the blob list is
a valid, independently sourced content fence, but the embedded recipe must be
paired with the runbook's exact-scope/topology gates—or expanded to enforce them—
before anyone describes it as a complete merge acceptance test. This is precisely
the distinction between an enforced property and an asserted one.

## Regeneration decision

1. **33 fence OIDs:** do not regenerate; all 33 are current and match.
2. **Two synthesis hashes:** do not regenerate; current G/W reconstruction
   reproduces both byte counts and OIDs.
3. **Conflict prediction:** do not change; fresh current-tip output confirms it.
4. **Fence provenance header:** refresh `W` from `6c746b65...` to `7d4e9a96...` and
   record that the audit-only tip movement leaves the union and all fence rows
   unchanged.
5. **Executable merge runbook, if it is to target current W:** regenerate every
   frozen/current-tip-dependent command, assertion, starting-commit reference,
   first-parent expectation, and final parent-order expectation that currently
   pins `6c746b65...`; rerun its frozen-output captures against `7d4e9a96...`.
   The observed conflict/fence values can remain only after that regenerated
   artifact records the new current-tip derivation.
6. **Standalone acceptance checker, if desired:** regenerate the short checker
   section to add current input/topology pins and exact first-parent scope/no
   outside-union enforcement. This is checker regeneration, not OID regeneration.

The runbook already states that any changed file outside the union is a stop and
implements a 32-path staged first-parent comparison.
(`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:615`)
It also explicitly says the runbook is unexecuted and unauthorized, so this
verification does not upgrade it to execution evidence or authorization.
(`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:1`)
