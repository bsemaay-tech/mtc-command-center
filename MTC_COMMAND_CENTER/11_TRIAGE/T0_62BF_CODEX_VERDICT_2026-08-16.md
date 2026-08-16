# T0 Gate-5 acceptance audit — Codex verdict

## Audit header

- Model identity reported by runtime/dispatch: `gpt-5.6-sol`
- Reasoning effort: `xhigh`
- Start (UTC+3): `2026-08-16 11:54:19 +03:00`
- Stop (UTC+3): `2026-08-16 12:02:36 +03:00`
- Working directory: `C:\BRIDGE_RELEASE_INTEGRATION_20260815`
- Audit tier: `T0`
- Session: fresh, independent, read-only; no sub-delegation

## 1. Subject identity — PASS

First post-contract Git observations:

```text
HEAD=62bf661b065dec5b5d9895d83575581fe369252d
TREE=e2cb5dadd1537e933460aeecd5cdcf343c31d7d0
PARENT1=7d4e9a96e07b34a0c3d92315912d7818168b830b
PARENT2=2ce41e34bceb599d80af24c5c33d835820ec321b
BRANCH=integration/bridge-release-20260815
STATUS=<empty>
```

All identities and parent order match the frozen subject. `git show -s --format=%P HEAD` returned exactly two parents in the order shown above.

## 2. Thirty-three-path blob fence — PASS

The runbook was read from `codex/rp7-r1-r4-repair-20260815`; its observed blob was `6a2799f0605e874a3bcc1c6602bd89379f1f8b12`. The §4 table parsed to exactly 33 rows. Independent `git rev-parse HEAD:<path>` output:

```text
BLOB_OK IBKR_PAPER_BRIDGE/bridge/api/routes.py 140bf003ecbcb6b7f47822c15f2dbdb83118f0df
BLOB_OK IBKR_PAPER_BRIDGE/bridge/app.py 572c4178fe804da17601eefd898027e9261492e6
BLOB_OK IBKR_PAPER_BRIDGE/bridge/broker/base.py 0698e4862ea6390c0cec5db34b85602d336e33e1
BLOB_OK IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py 855a17cd83c7d176576d810be5d520dbf1e5eba4
BLOB_OK IBKR_PAPER_BRIDGE/bridge/broker/mock.py 295c0a9cd06a0ca6b36cb4e691dab54555cc5670
BLOB_OK IBKR_PAPER_BRIDGE/bridge/engine/engine.py 0c115ff18489108daa015c35c1ef1e85bc2bbbf0
BLOB_OK IBKR_PAPER_BRIDGE/bridge/engine/orders.py 608a3afe1015c7a98e08f7d4f1bb08ea8cebae89
BLOB_OK IBKR_PAPER_BRIDGE/bridge/engine/reconcile.py ea3ff95d93e92ef2e224c5fa9ad18e1b64fab4b0
BLOB_OK IBKR_PAPER_BRIDGE/bridge/engine/types.py 2927968d7bfc5253e2011172610a8ff7ca676647
BLOB_OK IBKR_PAPER_BRIDGE/bridge/store/db.py ae5eb1b7ab2a9a6240932958c73ba4acdfe2a30e
BLOB_OK IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template c03d6e47ab57c00ef95f4122607fc7ba88119e35
BLOB_OK IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh db11010a24edfbb96ba80ec1fbe1db3ff29193c9
BLOB_OK IBKR_PAPER_BRIDGE/deploy/linux/package.sh add6478d33cce8d929d58f895407abe01d51da20
BLOB_OK IBKR_PAPER_BRIDGE/deploy/linux/README.md 4069904b7707da9efa875661769fc29435504b33
BLOB_OK IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md 8db2e6dd7e782c96f585f6672c4489c4ce5c1488
BLOB_OK IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template c18232549d96aa200d8c7f796e64de743288940c
BLOB_OK IBKR_PAPER_BRIDGE/deploy/linux/verify.sh 5cfefd709202ff504ae7b7fc3504b8c0b00900b6
BLOB_OK IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md a09b22bedb4e1a4e0ce9dc943983dd6cf399674d
BLOB_OK IBKR_PAPER_BRIDGE/docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md b02694c2e64061480843a8d76361d72034d46010
BLOB_OK IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md 23480737ee802bdad7c03a93e06d5989e22cfb58
BLOB_OK IBKR_PAPER_BRIDGE/README.md cfc15b212121b4a9f3adac3d18f02574c5aa74e7
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_api.py 40d31925ac93c4bfe13a877f060b5abaf6c0cd6e
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py ce0ae7c24f795dc8e5d56bf7cca82e1a75351402
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py 817afe17b00c5a7525e5d422b965fe260b802006
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py 3851340462fe0269a019bbbd2608e4db97d9ce8b
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py 64e25888ba67a6b706bbf5c9d5e5feb8f12a98b2
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_mock_broker.py bed96cea0f31cc7a7010ca790b0d03f219ab9c2a
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py 9e50c1b51cd6d60967f5481adfeda9779815efd9
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py 7b0b9ea36dd8b15108f6befcbcb00015ed2f51fb
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_reconciliation.py 9e6b015d84371c50b92bf25b12ee1f80c64bb581
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_store.py d911d983f0b76f752836ae220bc4ec61f04b98a2
BLOB_OK IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py 12b17ab595dad24fcff6397d0689effadbfe2f67
BLOB_OK IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py 26c077e650ab88ba2086efa3a80790769bc055b1
FENCE_ROW_COUNT=33
FENCE_MISMATCH_COUNT=0
```

The synthesized README and WAL OIDs match the two contract-pinned values exactly.

## 3. First-parent scope — PASS

```text
FIRST_PARENT_PATH_COUNT=32
EXPECTED_FIRST_PARENT_PATH_COUNT=32
FIRST_PARENT_SCOPE_DELTA_COUNT=0
OUTSIDE_IBKR_FIRST_PARENT_COUNT=0
```

Observed exact path set:

```text
IBKR_PAPER_BRIDGE/bridge/api/routes.py
IBKR_PAPER_BRIDGE/bridge/app.py
IBKR_PAPER_BRIDGE/bridge/broker/base.py
IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py
IBKR_PAPER_BRIDGE/bridge/broker/mock.py
IBKR_PAPER_BRIDGE/bridge/engine/engine.py
IBKR_PAPER_BRIDGE/bridge/engine/orders.py
IBKR_PAPER_BRIDGE/bridge/engine/reconcile.py
IBKR_PAPER_BRIDGE/bridge/engine/types.py
IBKR_PAPER_BRIDGE/bridge/store/db.py
IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template
IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh
IBKR_PAPER_BRIDGE/deploy/linux/package.sh
IBKR_PAPER_BRIDGE/deploy/linux/README.md
IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template
IBKR_PAPER_BRIDGE/deploy/linux/verify.sh
IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md
IBKR_PAPER_BRIDGE/docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md
IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md
IBKR_PAPER_BRIDGE/README.md
IBKR_PAPER_BRIDGE/tests/test_api.py
IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py
IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py
IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py
IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py
IBKR_PAPER_BRIDGE/tests/test_mock_broker.py
IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py
IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py
IBKR_PAPER_BRIDGE/tests/test_reconciliation.py
IBKR_PAPER_BRIDGE/tests/test_store.py
IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py
```

This is the 33-row fence minus `IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md`, with nothing else.

## 4. Resolution correctness — PASS

### WAL test

`git diff 2ce41e34... HEAD -- IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py` reported only `9` additions and `4` deletions. Actual-byte inspection showed exactly:

- add `from contextlib import closing`;
- remove only `SCHEMA_VERSION_BASELINE` from the import;
- add `with closing(sqlite3.connect(source_db))` and `SELECT value FROM meta WHERE key = 'schema_version'` before the existing `create(...)` call;
- assert the row exists and replace only the stale baseline comment/assertion with `assert inv["schema_version"] == source_schema_row[0]`.

No other hunk exists. Real count controls:

```text
WAL_IMPORT_CLOSING_COUNT=1
WAL_STALE_IMPORT_TOKEN_COUNT=0
WAL_CLOSING_CONNECT_COUNT=1
WAL_DYNAMIC_SELECT_COUNT=1
WAL_DYNAMIC_ASSERT_COUNT=1
```

### Linux README

The full 159-line HEAD blob was read. Real count controls:

```text
README_START_MODE_COUNT=1
README_SECURITY_INVENTORY_COUNT=1
README_STATIC_LIMITATION_COUNT=1
README_INTEGRATION_PENDING_COUNT=1
README_GATEA_SHA_COUNT=1
README_GATEA_EVIDENCE_COUNT=1
README_INTEGRATED_NOT_RUN_COUNT=1
README_SUBJECT_SHA_LITERAL_COUNT=0
```

The only positive candidate-specific execution history names exact Gate-A `2ce41e34bceb599d80af24c5c33d835820ec321b` and `GATE_A_A9_PASS_FINAL_2026-08-09D.md`. The integrated candidate is explicitly described as not executed, installed, run, or accepted. No text transfers execution or acceptance to `62bf661b...`.

## 5. Credential-string parity — PASS

The required command was run independently against both HEAD and Gate-A. Normalized distributions were identical:

```text
IBKR_PAPER_BRIDGE/bridge/api/routes.py:1
IBKR_PAPER_BRIDGE/bridge/app.py:7
IBKR_PAPER_BRIDGE/deploy/linux/README.md:1
IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:1
IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:1
IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py:4
IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py:2
HEAD_PATH_COUNT=7
HEAD_TOTAL=17
GATEA_PATH_COUNT=7
GATEA_TOTAL=17
PARITY_DELTA_COUNT=0
```

This independently reproduces the recorded runbook §5.1 authoring omission: Gate-A itself has seven paths, not six. The candidate matches Gate-A exactly, so this is not candidate drift and creates no candidate repair.

## 6. Full suite and post-run integrity — PASS

Executed from the repository root with `PYTHONUTF8=1`, exactly as required, with pytest cache disabled and all harness output redirected to an external disposable log:

```text
PYTEST_RC=0
SUITE_SUMMARY_MATCH_COUNT=1
1360 passed, 1 warning in 180.43s (0:03:00)
```

Only the suite summary line is quoted above. Post-run checks:

```text
POST_SUITE_STATUS=<empty>
POST_SUITE_HEAD=62bf661b065dec5b5d9895d83575581fe369252d
POST_SUITE_README_BLOB=4069904b7707da9efa875661769fc29435504b33
POST_SUITE_WAL_BLOB=12b17ab595dad24fcff6397d0689effadbfe2f67
POST_SUITE_GITATTRIBUTES=49c0fbe4f5f995ebaa9fc4e16b2da29c5389087b
```

## 7. D026 — PASS

No merge-authored regression test is offered as defect-closure evidence. Against exact Gate-A, HEAD changes only `tests/test_wal_state_bundle.py`, adds no `def test_...` line, and retains the same test-definition count:

```text
HEAD_VS_GATEA_TEST_DIFF_PATH_COUNT=1
M IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
NEW_TEST_DEF_LINES_VS_GATEA=0
HEAD_TEST_DEF_COUNT=957
GATEA_TEST_DEF_COUNT=957
```

The WAL edit is the accepted A2 repair replayed into an existing test, not a new closure test created by this merge. Therefore this merge introduces no new D026 RED/GREEN obligation.

## 8. Adversarial/self-confirming-check pass — PASS

Additional attacks and real outputs:

```text
GITATTRIBUTES=49c0fbe4f5f995ebaa9fc4e16b2da29c5389087b
FENCE_MODE_TYPE_CHECK_COUNT=33
FENCE_MODE_TYPE_MISMATCH_COUNT=0
PARENT_COUNT=2
CONFLICT_STAGE_COUNT=0
DIFF_CHECK_RC=0
HEAD_TRACKED_TEST_FILE_COUNT=29
GATEA_TRACKED_TEST_FILE_COUNT=29
HEAD_VS_GATEA_TEST_PATH_DELTA=0
HEAD_COLLECTION_CONFIG_COUNT=4
COLLECTION_CONFIG_DELTA_VS_GATEA=0
NO_RENAMES_RAW_DELTA_COUNT=32
NO_RENAMES_DELETE_COUNT=0
NO_RENAMES_OUTSIDE_IBKR_COUNT=0
NO_RENAMES_STATUS_DISTRIBUTION: A=3, M=29
```

The mode/type comparison closes the blob-fence gap where identical content could otherwise hide an executable-bit or symlink/type change. The independent `diff-tree --no-renames` pass closes rename-detection masking: it still finds exactly 32 expected paths, no deletion, and no outside-Bridge path. Exact test-file path parity, equal test-definition count, unchanged collection-control blobs, the exact collected/pass count, and clean post-suite status provide mutually independent collection-tampering controls.

Each required check has a discriminating failure: identity compares full OIDs and ordered parents; the fence requires 33 parsed rows and 33 exact OIDs; scope is compared as a set and again without rename detection; the synthesized files are checked both by OID and actual semantic delta; credential parity compares per-path distributions from both revisions; suite acceptance requires rc 0 plus one exact summary and post-run integrity; D026 checks the only Gate-A-relative test delta for newly added test definitions.

## Findings

- REQUIRED: none.
- NIT: none.

## Verdict

**PASS**

Candidate `62bf661b065dec5b5d9895d83575581fe369252d` satisfies every check in the T0 Codex audit contract with zero required repairs.
