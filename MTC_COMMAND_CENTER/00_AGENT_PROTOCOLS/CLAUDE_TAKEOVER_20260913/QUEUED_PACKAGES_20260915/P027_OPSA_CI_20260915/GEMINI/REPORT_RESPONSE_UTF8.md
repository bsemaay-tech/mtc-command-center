# Supplemental Read-Only Detection Review: WP-P0-27 OPS-A Tests CI Workflow

**Reviewer Model:** Gemini 3.8 Flash (High)  
**Role:** Independent Read-Only Detection Reviewer (`SUPPLEMENTAL_UNEXECUTED`)  
**Target Commit:** `63b7bbe0981bddafb94018a3520f3c5c82e8e4f4` (PR #194, base master `fcac0ac6`)  
**Canonical Package Path:** `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915`  
**Audit Tier Context:** Informational check prior to T1 exact-Opus lane 5 review (`OD-20260915-P027-T1-WEDOPUS-1`)  

---

## 1. Least Privilege Table

Evaluation of [.github/workflows/opsa-tests.yml](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml) against the repository CI conventions established in [.github/workflows/ci.yml](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/ci_fcac0ac6.yml):

| Configuration Item | Subject Path & Lines | Subject Setting | [ci_fcac0ac6.yml](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/ci_fcac0ac6.yml) Convention | Relation | Verdict |
|---|---|---|---|---|---|
| **Top-level permissions** | [opsa-tests_63b7bbe0.yml#L21-L22](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml#L21-L22) | `permissions:`<br>`  contents: read` | `permissions:`<br>`  contents: read` (lines 11-12) | EQUAL | **PASS** (least privilege, read-only token) |
| **Triggers (`on:`)** | [opsa-tests_63b7bbe0.yml#L13-L19](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml#L13-L19) | `pull_request:` `master`<br>`push:` `master` | `pull_request:` `master`<br>`push:` `master` (lines 3-9) | EQUAL | **PASS** (no `schedule`, no `pull_request_target`, no `workflow_dispatch`) |
| **Concurrency group** | [opsa-tests_63b7bbe0.yml#L24-L26](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml#L24-L26) | `opsa-tests-${{ github.workflow }}-${{ github.event.pull_request.number \|\| github.ref }}` | `ci-${{ github.workflow }}-${{ github.event.pull_request.number \|\| github.ref }}` (lines 14-16) | DIFFERENT (job-specific prefix) | **PASS** (prevents cross-workflow cancellation while retaining standard per-PR grouping) |
| **Checkout Action & Pin** | [opsa-tests_63b7bbe0.yml#L42-L43](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml#L42-L43) | `actions/checkout@v4` | `actions/checkout@v4` (line 27) | EQUAL | **PASS** (standard major version pin) |
| **Credential Persistence** | [opsa-tests_63b7bbe0.yml#L44-L45](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml#L44-L45) | `with:`<br>`  persist-credentials: false` | `with:`<br>`  persist-credentials: false` (lines 28-29) | EQUAL | **PASS** (prevents token exfiltration) |
| **Setup Python Action & Pin** | [opsa-tests_63b7bbe0.yml#L47-L50](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml#L47-L50) | `actions/setup-python@v5`<br>`python-version: "3.12"` | `actions/setup-python@v5`<br>`python-version: "3.12"` (lines 31-34) | EQUAL | **PASS** (standard major pin, Python 3.12) |
| **Runner OS** | [opsa-tests_63b7bbe0.yml#L31](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml#L31) | `runs-on: windows-2025` | `runs-on: ubuntu-24.04` (line 21) | DIFFERENT | **PASS** (GitHub-hosted Windows runner required because OPS-A tools operate on Windows) |
| **Timeout** | [opsa-tests_63b7bbe0.yml#L32](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml#L32) | `timeout-minutes: 10` | `timeout-minutes: 20` (line 22) | DIFFERENT | **PASS** (tighter timeout bound; identical to [research-gates_fcac0ac6.yml#L35](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/research-gates_fcac0ac6.yml#L35)) |
| **Secrets access** | [opsa-tests_63b7bbe0.yml](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml) | None referenced (`grep secrets`: 0 hits) | None (0 hits) | EQUAL | **PASS** (zero secret references) |
| **External Network / Dependencies** | [opsa-tests_63b7bbe0.yml#L53-L55](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml#L53-L55) | None (installs zero packages; stdlib only) | Uses `pip install --require-hashes` (lines 37-39) | DIFFERENT (hermetic / stdlib only) | **PASS** (no network access, no hosts or external venues contacted) |

---

## 2. Correctness of What Runs

1. **Target Working Directory & Command:**
   - [opsa-tests_63b7bbe0.yml#L54](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml#L54): `working-directory: MTC_COMMAND_CENTER/tools/opsa`
   - [opsa-tests_63b7bbe0.yml#L55](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml#L55): `run: python -m unittest test_opsa -v`
   - The test invocation executes standard library `unittest` directly against `test_opsa.py` inside the tool root.

2. **Test Method Count in [test_opsa_fcac0ac6.py](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/test_opsa_fcac0ac6.py):**
   Inspection of all test classes and method definitions reveals exactly **33 test cases**:
   - [`BackupRestoreTests`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/test_opsa_fcac0ac6.py#L55-L282) (13 tests):
     1. `test_roundtrip_byte_identical` (line 72)
     2. `test_manifest_append_only_across_runs` (line 87)
     3. `test_dry_run_writes_nothing` (line 100)
     4. `test_missing_store_reports_error_not_success` (line 106)
     5. `test_restore_refuses_tampered_backup` (line 113)
     6. `test_check_only_detects_corruption_writes_nothing` (line 125)
     7. `test_latest_selects_newest_run` (line 140)
     8. `test_nonexistent_run_is_check_failure_not_empty_success` (line 154)
     9. `test_partial_run_declaring_files_but_having_no_records_fails_closed` (line 166)
     10. `test_restore_rejects_plain_parent_store_id_before_any_outside_write` (line 197)
     11. `test_restore_cli_missing_store_id_is_structured_check_failure_without_writes` (line 259)
     12. `test_restore_cli_empty_path_is_structured_check_failure_without_writes` (line 264)
     13. `test_backup_rejects_percent_encoded_parent_store_id_without_writes` (line 270)
   - [`HeartbeatPathTests`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/test_opsa_fcac0ac6.py#L283-L300) (1 test):
     14. `test_heartbeat_rejects_traversal_absolute_and_drive_ids_without_writes` (line 284)
   - [`WatchdogTests`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/test_opsa_fcac0ac6.py#L302-L515) (16 tests):
     15. `test_fresh_heartbeat_ok` (line 332)
     16. `test_stale_heartbeat_silent` (line 339)
     17. `test_missing_expected_id_alerts` (line 347)
     18. `test_unreadable_heartbeat_is_check_failed_not_ok` (line 355)
     19. `test_bad_timestamp_is_check_failed` (line 362)
     20. `test_future_timestamp_is_check_failed` (line 371)
     21. `test_empty_state_dir_is_check_failed_not_ok` (line 378)
     22. `test_missing_state_dir_is_check_failed` (line 382)
     23. `test_local_log_notifier_writes_event` (line 387)
     24. `test_missing_state_dir_yields_rc3_and_exactly_one_notifier_event` (line 397)
     25. `test_empty_state_dir_no_expect_notifies_check_failed` (line 416)
     26. `test_invalid_now_is_check_failed_not_traceback` (line 430)
     27. `test_per_id_outcomes_still_notify_per_id` (line 446)
     28. `test_silence_bound_is_required_and_has_no_ratified_default` (line 461)
     29. `test_alert_recovery_alert_emits_all_three_transitions_once_each` (line 480)
     30. `test_corrupt_dedupe_state_fails_safe_by_re_alerting` (line 503)
   - [`NoDeleteGuaranteeTests`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/test_opsa_fcac0ac6.py#L517-L544) (1 test):
     31. `test_no_delete_calls_in_opsa_tools` (line 527)
   - [`TimestampTests`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/test_opsa_fcac0ac6.py#L546-L555) (2 tests):
     32. `test_parse_roundtrip` (line 547)
     33. `test_parse_rejects_naive` (line 552)

   **Comparison with Evidence Note:**
   The evidence note ([P027_OPSA_CI_EVIDENCE_20260915.md](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/P027_OPSA_CI_EVIDENCE_20260915.md) line 9 and 15) states "Ran 33 tests -> OK" and "33 tests on fcac0ac6". The module test count matches the evidence claim exactly.

3. **Windows Long Paths Precedence:**
   - Step 1 ([opsa-tests_63b7bbe0.yml#L39-L40](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml#L39-L40)): `Enable long paths for the checkout` runs `git config --system core.longpaths true`.
   - Step 2 ([opsa-tests_63b7bbe0.yml#L42-L45](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml#L42-L45)): `Check out repository` (`actions/checkout@v4`).
   - Confirmed: `git config --system core.longpaths true` is placed strictly **before** checkout, preventing Windows path length truncation (`MAX_PATH` 260 chars).

4. **Fail-Closed Behavior (`continue-on-error`):**
   - Neither the job nor the steps contain `continue-on-error: true`.
   - Any test failure properly propagates non-zero exit codes to fail the job (verified by the failure of step `OPS-A unit tests` in run 34983897746).

---

## 3. Evidence Honesty

Comparison between captured JSON/log artifacts and claims in [P027_OPSA_CI_EVIDENCE_20260915.md](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/P027_OPSA_CI_EVIDENCE_20260915.md):

| Artifact / Property | Value in Captured Artifact | Claim in Evidence Note | Match Verdict |
|---|---|---|---|
| **GREEN Run ID & Conclusion** | ID: `34983809921`<br>Conclusion: `success`<br>CreatedAt: `2026-09-15T14:45:35Z`<br>([opsa_tests_run_34983809921_GREEN.json](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/opsa_tests_run_34983809921_GREEN.json)) | Run `34983809921` on `63b7bbe0`: `success` (14:45:35Z) | **EXACT MATCH** |
| **GREEN Run Commit & Workflow** | Head SHA: `63b7bbe0981bddafb94018a3520f3c5c82e8e4f4`<br>Job Name: `OPS-A tests (Python 3.12, Windows)` | Commit `63b7bbe0`; job `opsa-tests` context `OPS-A tests (Python 3.12, Windows)` | **EXACT MATCH** |
| **RED Run ID & Conclusion** | ID: `34983897746`<br>Conclusion: `failure`<br>Head SHA: `e9314079865ce5c9267d6e7b1437f40f0d79f073`<br>([opsa_tests_run_34983897746_RED.json](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/opsa_tests_run_34983897746_RED.json)) | Demo PR #195 run `34983897746` `FAILURE` at step `OPS-A unit tests` | **EXACT MATCH** |
| **PR #194 State** | `number`: 194<br>`state`: `OPEN`<br>`isDraft`: `false`<br>`mergeStateStatus`: `CLEAN`<br>`headRefOid`: `63b7bbe0...`<br>([pr194_state.json](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/pr194_state.json)) | PR #194 OPEN, not draft, `mergeStateStatus: CLEAN` | **EXACT MATCH** |
| **PR #195 State at Capture** | `number`: 195<br>`state`: `OPEN`<br>`isDraft`: `true`<br>`mergeStateStatus`: `BLOCKED`<br>`headRefOid`: `e9314079...`<br>([pr195_state_RED.json](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/pr195_state_RED.json)) | Draft PR #195 `mergeStateStatus: BLOCKED` (from pending required `Bridge suite (Python 3.12)` check; later closed unmerged and branch deleted) | **EXACT MATCH** |

### RED Arm Excerpt Analysis ([RED_RUN_34983897746_failed_excerpt.txt](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/RED_RUN_34983897746_failed_excerpt.txt))
- **Failed Step:** `OPS-A unit tests`
- **Output:**
  ```text
  AssertionError: deliberate WP-P0-27 D026 red probe for the OPS-A tests workflow (2026-09-15); never merged
  Ran 34 tests in 0.985s
  FAILED (failures=1)
  ```
- **Nature of Failure:** Real test failure resulting from an injected probe assertion (`CiRedProbeTests.test_ci_red_probe`, asserting `False`). The runner infrastructure, longpaths setup, checkout, Python 3.12 runtime, and test harness all operated normally.

---

## 4. Blast Radius Assessment

1. **Ruleset Protection Invariance:**
   - Adding or modifying a workflow file inside `.github/workflows/` cannot mutate GitHub repository ruleset configuration.
   - Master branch protection ruleset **21444962** ("Protect master - required CI") strictly requires:
     1. `Bridge suite (Python 3.12)`
     2. `pine-alert-guard`
   - The check context published by this workflow is `OPS-A tests (Python 3.12, Windows)`.
   - Because `OPS-A tests (Python 3.12, Windows)` is not a member of ruleset 21444962, this check is strictly **informational**. A failure of this job cannot block merging into `master`. (In PR #195, the captured `BLOCKED` status was entirely due to the required `Bridge suite (Python 3.12)` being in a pending state `""`, as confirmed in [pr195_state_RED.json](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/pr195_state_RED.json)).

2. **Claims in Copied Documents:**
   - All copied packet documents ([opsa-tests_63b7bbe0.yml](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml) lines 7-10, [COMMIT_HEAD.txt](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/COMMIT_HEAD.txt) lines 13-14, [P027_OPSA_CI_EVIDENCE_20260915.md](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/P027_OPSA_CI_EVIDENCE_20260915.md) lines 8 and 13, [CI_POLICY_CT13.md](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/CI_POLICY_CT13.md) lines 5 and 20, [DECISIONS_rows_P027.md](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/DECISIONS_rows_P027.md) row `OD-20260915-BUILD-ABC-1`) consistently and explicitly state that this workflow is informational and not required. None of the documents claim otherwise.

---

## 5. Scope Verification

Inspection of [DIFF_STAT_fcac0ac6_HEAD.txt](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/DIFF_STAT_fcac0ac6_HEAD.txt) and [DIFF_fcac0ac6_HEAD.diff](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/DIFF_fcac0ac6_HEAD.diff):
- **Diff Stat:**
  ```text
   .github/workflows/opsa-tests.yml | 55 ++++++++++++++++++++++++++++++++++++++++
   1 file changed, 55 insertions(+)
  ```
- Exactly **one new file** (`.github/workflows/opsa-tests.yml`) is added. No other repository files are touched or modified.

---

## 6. Exact Read Coverage & Verification Limits

### Complete Native Read Log (All files under `_gemini_packets_20260913/P027_OPSA_20260915`)
1. [PACKET_SHA256SUMS.txt](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/PACKET_SHA256SUMS.txt): lines 1–16 (complete)
2. [subject/opsa-tests_63b7bbe0.yml](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/opsa-tests_63b7bbe0.yml): lines 1–56 (complete)
3. [subject/DIFF_fcac0ac6_HEAD.diff](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/DIFF_fcac0ac6_HEAD.diff): lines 1–62 (complete)
4. [subject/DIFF_STAT_fcac0ac6_HEAD.txt](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/DIFF_STAT_fcac0ac6_HEAD.txt): lines 1–3 (complete)
5. [subject/COMMIT_HEAD.txt](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/subject/COMMIT_HEAD.txt): lines 1–24 (complete)
6. [sources/P027_OPSA_CI_EVIDENCE_20260915.md](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/P027_OPSA_CI_EVIDENCE_20260915.md): lines 1–18 (complete)
7. [sources/RED_RUN_34983897746_failed_excerpt.txt](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/RED_RUN_34983897746_failed_excerpt.txt): lines 1–5 (complete)
8. [sources/opsa_tests_run_34983809921_GREEN.json](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/opsa_tests_run_34983809921_GREEN.json): lines 1–2 (complete)
9. [sources/opsa_tests_run_34983897746_RED.json](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/opsa_tests_run_34983897746_RED.json): lines 1–2 (complete)
10. [sources/pr194_state.json](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/pr194_state.json): lines 1–2 (complete)
11. [sources/pr195_state_RED.json](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/pr195_state_RED.json): lines 1–2 (complete)
12. [sources/ci_fcac0ac6.yml](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/ci_fcac0ac6.yml): lines 1–56 (complete)
13. [sources/research-gates_fcac0ac6.yml](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/research-gates_fcac0ac6.yml): lines 1–60 (required range read)
14. [sources/test_opsa_fcac0ac6.py](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/test_opsa_fcac0ac6.py):
    - Initial view: lines 1–60
    - Continuation 1: lines 61–210
    - Continuation 2: lines 211–360
    - Continuation 3: lines 361–510
    - Continuation 4: lines 511–559 (complete, all 33 tests verified)
15. [sources/CI_POLICY_CT13.md](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/CI_POLICY_CT13.md): lines 1–40 (required range read)
16. [sources/DECISIONS_rows_P027.md](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915/sources/DECISIONS_rows_P027.md): lines 1–5 (complete)

### NOT VERIFIED (Unexecuted Scope)
- As a read-only supplemental reviewer under `SUPPLEMENTAL_UNEXECUTED` status, I did not and cannot execute GitHub Actions runners, query live GitHub APIs, inspect live GitHub repository settings/rulesets directly, or execute tests on live systems.
- Acceptance of workflow files is audit tier T1 and belongs exclusively to the Wednesday exact-Opus lane 5 review (`OD-20260915-P027-T1-WEDOPUS-1`).

---

## 7. Findings

No findings with severity REQUIRED or NIT were identified. The workflow complies with least privilege, correctly sequences longpaths checkout on Windows, exercises the exact 33 unit tests, preserves existing required rulesets, and accurately reflects all captured run evidence.

---

```json
{"part": "P027_OPSA_GEMINI", "verdict": "PASS", "evidence_class": "SUPPLEMENTAL_UNEXECUTED", "test_count_in_module": 33, "findings": [], "required_scope_unread": []}
```
GEMINI_READ_ONLY_OK
