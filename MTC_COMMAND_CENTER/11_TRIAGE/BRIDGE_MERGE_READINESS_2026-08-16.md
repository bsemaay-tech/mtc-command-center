Status: MERGE READINESS REPORT — READ-ONLY — NO MERGE PERFORMED

# Bridge suite-repairs merge readiness — 2026-08-16

Audit tier: T3 report/checkpoint self-verification. No model audit or sub-delegation was used.

Scope boundary: this report uses only the repository snapshot at `C:\RO`, detached at `c84497c885e16e1111fc3005d7cb9a82a34fb907`, and its already-present committed refs and objects. No fetch, status, checkout, merge, index write, worktree creation, test run, commit, push, host/network/service action, or economic action was performed. Therefore “current” below means **current in this detached snapshot**, not current on the remote server. The lane contract requires exactly that boundary (`C:\tmp\lane_kick\MR1.md:40-43`).

## Document resolution

The snapshot's Bridge index identifies the release chain and says that the corrected runbook supersedes the integration design for current mechanics (`MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_DOCUMENT_INDEX_2026-08-16.md:98-100`):

- Integration design: `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md` (`MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_DOCUMENT_INDEX_2026-08-16.md:105`).
- Merge runbook: `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md` (`MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_DOCUMENT_INDEX_2026-08-16.md:106`).
- Standalone fence: `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md`; its frozen inputs are `M`, `G`, `W`, and `B` (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:5-10`).

The design requires freezing the exact accepted repair commit and creating the integration branch from **that repaired WP-I tip** (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:209-215`). The runbook freezes repaired WP-I as `6c746b65…` (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:31-37`).

## Current precondition table

Every `HELD` result below comes from a fresh read-only Git command, not from repeating the runbook's claim. This applies the project's anti-self-confirmation rule: the expectation and observation must not come from the same process (`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-64`).

| Runbook precondition | State | Fresh Git evidence from `C:\RO` | Assessment |
|---|---|---|---|
| Snapshot is the specified detached snapshot | HELD | `git rev-parse HEAD` → `c84497c885e16e1111fc3005d7cb9a82a34fb907`; `git symbolic-ref -q --short HEAD` → no output, `rc=1` | Establishes the lane's evidence boundary, not remote freshness. |
| `origin/master` is frozen `M=637307e8…` | HELD | `git rev-parse refs/remotes/origin/master^{commit}` → `637307e83951ffe23e768ed8e50ddaf8712b0660` | Matches the runbook input (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:34`). |
| Gate-A is frozen `G=2ce41e34…` | HELD | `git rev-parse refs/heads/codex/gate-a-disarmed-start-mode^{commit}` → `2ce41e34bceb599d80af24c5c33d835820ec321b`; `git cat-file -t 2ce41e34…` → `commit` | The local Gate-A branch still points at the frozen object (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:35`). |
| The repaired WP-I **current branch tip** equals frozen `W=6c746b65…` | **NOT HELD** | `git rev-parse refs/heads/codex/bridge-suite-anomaly-repairs-20260815^{commit}` → `7d4e9a96e07b34a0c3d92315912d7818168b830b`; the remote-tracking ref resolves to the same `7d4e9a96…` | The runbook still starts from and expects parent 1 to be `6c746b65…` (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:149-155`; `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:772-773`). Exact input identity drift is a stated stop (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:789-792`). |
| Frozen repaired object `6c746b65…` still exists and remains in current branch lineage | HELD, but insufficient to cure tip drift | `git cat-file -t 6c746b65…` → `commit`; `git merge-base --is-ancestor 6c746b65… 7d4e9a96…` → `rc=0`; `git show -s --format=%P 7d4e9a96…` → `6c746b65411d5e646da407614f95f8a1174f3a5a` | The new tip is the direct child of the frozen repair commit. Object existence is not current-tip identity. |
| Merge base is frozen `B=4d2228cf…` | HELD for both old and current repaired commits | `git merge-base 6c746b65… 2ce41e34…` → `4d2228cf8985ce755c398cceff23f777a99d5404`; `git merge-base 7d4e9a96… 2ce41e34…` → the same OID | Topology did not drift (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:177-187`). |
| `M` is an ancestor of `G`; `G` and current `W` are mutually non-ancestor | HELD | `git merge-base --is-ancestor M G` → `rc=0`; `… G Wcurrent` → `rc=1`; `… Wcurrent G` → `rc=1` | Matches the required topology (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:182-187`). |
| Gate-A and repaired WP-I carry the pinned `.gitattributes` blob | HELD | `git rev-parse G:.gitattributes` → `49c0fbe4f5f995ebaa9fc4e16b2da29c5389087b`; both `6c746b65:.gitattributes` and `7d4e9a96:.gitattributes` → the same OID | Matches the runbook's exact object gate (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:189-192`). |
| Target integration branch `integration/bridge-release-20260815` is absent | HELD | `git show-ref --verify --quiet refs/heads/integration/bridge-release-20260815` → `rc=1` | This is the exact absent-ref return expected by the runbook (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:167-175`). |
| Target path `C:\BRIDGE_RELEASE_INTEGRATION_20260815` is absent | **UNCHECKABLE** under the Git-only evidence rule | `git worktree list --porcelain` has no registration for that path, but Git cannot prove that an unregistered ordinary filesystem path does not exist | The runbook uses `Test-Path` for this precondition (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:164-166`). A read-only filesystem probe such as `Test-Path -LiteralPath 'C:\BRIDGE_RELEASE_INTEGRATION_20260815'` is needed; it was not run because every held result in this lane must be Git-produced (`C:\tmp\lane_kick\MR1.md:48-51`). |
| Current-tip `merge-tree` retains the frozen aggregate shape | HELD | `git merge-tree B 7d4e9a96… G` → `rc=0`, `16,359` lines, `2` `changed in both`, `3` `added in remote`, `6` marker lines, `2` conflict starts | Matches the runbook's binding prediction (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:201-238`). The complete output SHA-256 was `33bf43c964712e5d9aa163248104d70886ce47ba8d98fec35474b99ba4d9f942` for both `W=6c746b65…` and current `W=7d4e9a96…`; this digest compares command outputs, not source working-tree bytes. |
| Conflict markers remain confined to the two predicted WAL hunks | HELD as a read-only prediction | Parsing the current-tip Git output gave `README.md: marker lines=0`; `tests/test_wal_state_bundle.py: marker lines=6, conflict starts=2` | No other changed-by-both section contained a marker. This independently confirms the file/hunk boundary stated at `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:7-20`. |
| Three-way Bridge universe remains exactly 33 paths with the repaired shape | HELD | Independent `git diff --name-only B G -- IBKR_PAPER_BRIDGE` → `32` paths; `git diff --name-only B Wcurrent -- IBKR_PAPER_BRIDGE` → `3` paths; sorted union → `33`. Object classification → `9 Gate-A-only + 1 WP-I-only + 2 changed-by-both + 21 WP-I-stale`, `0 other` | Matches the runbook/fence universe, derived before reading the recorded OIDs (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_BLOB_FENCE_2026-08-15.md:12-16`). |

## Execution-time conditions that cannot be established now

The runbook also makes the following conditions mandatory before or after an actual merge. They are not facts about the current committed tips and cannot honestly be marked held in this no-merge lane. The runbook itself says these values must be observed at run time (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:296-299`; `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:767-778`).

| Runbook condition | State | What would be needed |
|---|---|---|
| New worktree starts at the selected repaired commit, on the exact integration branch, with an empty status | UNCHECKABLE | Separately authorized `git worktree add`, branch creation, and status inspection (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:240-265`). These are prohibited here. |
| Real merge returns `rc=1` and exactly one unmerged WAL path | UNCHECKABLE | Execute the real merge in the isolated integration worktree (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:267-299`). `merge-tree` is prediction evidence, not execution evidence. |
| Deterministic README/WAL resolutions are applied to index/worktree, all guards match once, and no unmerged path or whitespace error remains | UNCHECKABLE for an actual candidate | Apply and stage the prescribed resolution after the real merge (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:301-440`). The transforms were replayed in memory below only to derive fence OIDs. |
| Integrated index has exactly the fenced 33 blobs and exactly the expected 32-path first-parent delta, with no outside-union change | UNCHECKABLE | A real integrated index/candidate is required (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:548-618`). The current input trees can establish the expected values, not the future candidate's compliance. |
| Integrated index contains exactly 17 `credential_free_disarmed` occurrences across six paths | UNCHECKABLE | A real integrated index is required for the runbook's `git grep --cached` check (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:622-657`). |
| Full integrated suite reports exactly `1360 passed, 1 warning` | UNCHECKABLE | Build the exact integrated candidate and run the mandated suite (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:659-692`). No suite was run here. |
| Tests leave no unstaged/untracked changes and the post-suite fence still passes | UNCHECKABLE | Run the suite against the integrated worktree, inspect its resulting repository state, and repeat the index fence (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:694-714`). |
| Commit hook succeeds; merge commit has the exact two parents/order, exact branch tip, 32-path scope, clean final state, and observed SHA/tree | UNCHECKABLE | A separately authorized merge commit and its post-commit checks are required (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:716-778`). A commit is explicitly prohibited in this lane. |

These expected run-time observations are mandatory later, but they are not additional current-tip drift findings. The current blockers are listed in the final section.

## Independent 33-row blob-fence verification

Result: **PASS — 33/33 object OIDs match; 0 missing paths; 0 extra recorded paths; 0 OID mismatches.**

Method, deliberately independent of last night's `BFV_BLOB_FENCE_VERIFY.md`:

1. Derive the 33-path universe from fresh committed-tree `git diff` output for `B..G` and `B..Wcurrent`.
2. Before loading recorded OIDs, derive 31 exact-source rows with `git rev-parse <commit>:<path>`: Gate-A supplies 30 rows and current repaired WP-I supplies `SECURITY_BASELINE.md`.
3. Obtain the two changed-by-both source blobs with `git cat-file blob`, apply the runbook's guarded deterministic transformations entirely in memory, and send the resulting bytes to `git hash-object --stdin` **without `-w`**. Each guarded replacement matched exactly once. The README automatic-merge replay produced OID `f1803b54ee987e94182eb8c4f24af490f27d4162`; final README was `9,964` bytes/OID `4069904b7707da9efa875661769fc29435504b33`; final WAL was `55,292` bytes/OID `12b17ab595dad24fcff6397d0689effadbfe2f67`.
4. Only after derivation, parse the 33 recorded OIDs from the committed runbook table (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:512-546`) and compare exact sets and values.

No working-tree file hash was used. This is load-bearing because the lane contract warns that `* text=auto` makes working-tree bytes ambiguous (`C:\tmp\lane_kick\MR1.md:23-27`). `git cat-file -e HEAD:MTC_COMMAND_CENTER/_AI_MEMORY/LESSONS.md` returned `rc=128`, and `git ls-tree` returned no path, so the optional `LESSONS.md` was absent from this snapshot.

| Path | Independently derived Git object OID | Source | Result |
|---|---|---|---|
| `IBKR_PAPER_BRIDGE/README.md` | `cfc15b212121b4a9f3adac3d18f02574c5aa74e7` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/bridge/api/routes.py` | `140bf003ecbcb6b7f47822c15f2dbdb83118f0df` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/bridge/app.py` | `572c4178fe804da17601eefd898027e9261492e6` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/bridge/broker/base.py` | `0698e4862ea6390c0cec5db34b85602d336e33e1` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py` | `855a17cd83c7d176576d810be5d520dbf1e5eba4` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/bridge/broker/mock.py` | `295c0a9cd06a0ca6b36cb4e691dab54555cc5670` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/bridge/engine/engine.py` | `0c115ff18489108daa015c35c1ef1e85bc2bbbf0` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/bridge/engine/orders.py` | `608a3afe1015c7a98e08f7d4f1bb08ea8cebae89` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/bridge/engine/reconcile.py` | `ea3ff95d93e92ef2e224c5fa9ad18e1b64fab4b0` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/bridge/engine/types.py` | `2927968d7bfc5253e2011172610a8ff7ca676647` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/bridge/store/db.py` | `ae5eb1b7ab2a9a6240932958c73ba4acdfe2a30e` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/deploy/linux/README.md` | `4069904b7707da9efa875661769fc29435504b33` | synthesized Git blob | MATCH |
| `IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md` | `8db2e6dd7e782c96f585f6672c4489c4ce5c1488` | current `W` exact | MATCH |
| `IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template` | `c03d6e47ab57c00ef95f4122607fc7ba88119e35` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh` | `db11010a24edfbb96ba80ec1fbe1db3ff29193c9` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/deploy/linux/package.sh` | `add6478d33cce8d929d58f895407abe01d51da20` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template` | `c18232549d96aa200d8c7f796e64de743288940c` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh` | `5cfefd709202ff504ae7b7fc3504b8c0b00900b6` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md` | `a09b22bedb4e1a4e0ce9dc943983dd6cf399674d` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md` | `b02694c2e64061480843a8d76361d72034d46010` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md` | `23480737ee802bdad7c03a93e06d5989e22cfb58` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/tests/test_api.py` | `40d31925ac93c4bfe13a877f060b5abaf6c0cd6e` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py` | `ce0ae7c24f795dc8e5d56bf7cca82e1a75351402` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py` | `817afe17b00c5a7525e5d422b965fe260b802006` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py` | `3851340462fe0269a019bbbd2608e4db97d9ce8b` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py` | `64e25888ba67a6b706bbf5c9d5e5feb8f12a98b2` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/tests/test_mock_broker.py` | `bed96cea0f31cc7a7010ca790b0d03f219ab9c2a` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py` | `9e50c1b51cd6d60967f5481adfeda9779815efd9` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py` | `7b0b9ea36dd8b15108f6befcbcb00015ed2f51fb` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/tests/test_reconciliation.py` | `9e6b015d84371c50b92bf25b12ee1f80c64bb581` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/tests/test_store.py` | `d911d983f0b76f752836ae220bc4ec61f04b98a2` | `G` exact | MATCH |
| `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py` | `12b17ab595dad24fcff6397d0689effadbfe2f67` | synthesized Git blob | MATCH |
| `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` | `26c077e650ab88ba2086efa3a80790769bc055b1` | `G` exact | MATCH |

The fence's content values therefore remain valid for the current repaired branch tip. This does **not** make the runbook current: blob equivalence is weaker than exact release-input identity, and the runbook requires both.

## Drift found

1. **Repaired-tip identity drift:** `codex/bridge-suite-anomaly-repairs-20260815` moved from runbook-frozen `6c746b65411d5e646da407614f95f8a1174f3a5a` to `7d4e9a96e07b34a0c3d92315912d7818168b830b`. Git shows the latter is the direct child of the former and has subject `audit(bridge): T1 cross-model audit of the suite anomaly repairs`.
2. **Content effect of that drift:** `git diff --name-status 6c746b65… 7d4e9a96…` reports only `A MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md`; the same diff restricted to `IBKR_PAPER_BRIDGE` is empty. Thus merge topology, Bridge union, conflict prediction, `.gitattributes`, and every fence OID remain unchanged.
3. **Runbook enforcement gap:** the runbook assigns `$RepairedWpi` the literal old SHA and then compares `git rev-parse "$RepairedWpi^{commit}"` back to the same literal (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:149-180`). That check proves only that the old object resolves. It can pass while the named repaired branch points elsewhere, as it does now. This is the exact self-confirming defect class: expected and observed identity are not independent (`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:12-16`; `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:47-64`). A refreshed runbook must pin the intended current branch tip independently and use that exact SHA consistently for the start commit, merge-base capture, prediction, parent-1 expectation, and final branch-tip check.

## Verdict

**NOT-READY**

Blocking items:

1. The current repaired branch tip is `7d4e9a96…`, but the runbook's frozen start commit and required first parent remain `6c746b65…`. The runbook's own stop list makes frozen-input drift a hard stop (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:789-792`). The runbook must be regenerated or explicitly re-frozen for the intended current tip; preserving the same fence OIDs does not waive release identity.
2. The required absence of `C:\BRIDGE_RELEASE_INTEGRATION_20260815` is uncheckable with Git alone. Git proves only that no worktree is registered there. Before any separately authorized execution, a read-only filesystem existence check must establish literal path absence.

The later execution-time conditions remain mandatory observations during any separately authorized integration run, but no merge or acceptance decision is made here. The Lead decides whether and how to refresh the runbook.
