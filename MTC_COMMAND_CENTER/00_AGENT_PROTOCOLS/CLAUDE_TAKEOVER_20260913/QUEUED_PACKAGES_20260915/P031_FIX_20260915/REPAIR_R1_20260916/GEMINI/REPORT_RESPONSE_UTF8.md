# WP-P0-31 Milestone-1 T0 Repair Round 1 Detection Review

**Reviewer Model:** Gemini 3.8 Flash (High)  
**Role:** Independent Read-Only Detection Reviewer (`SUPPLEMENTAL_UNEXECUTED`)  
**Commit Evaluated:** `e9e37aec` on branch `feature/p031-m1-20260913-refresh` (base `48bd70de`)  
**Subject:** T0 repair of finding F-1 (OD-7 revocation invariant fencing)  

---

## (a) Guard-Order Walk for the OLD-Identity Admission

### 1. State Prior to Admission Attempt
In [`test_post_refresh_admission_cannot_reuse_the_revoked_deployment_identity`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R1_20260916/subject/test_p031_lifecycle_ledger_HEAD_lines_2500-2680.py#L89-L167):
1. `self.build_to_rung(self.ledger, candidate_id, "revoked-identity", "SHADOW_ELIGIBLE")` advances candidate `QLC-20260916-revoked-identity` through `CAPTURED -> TRIAGED -> CANDIDATE -> FROZEN -> SHADOW` under `PACKAGE_A` and `DEPLOYMENT_A`.
2. `self.registrar.append(...)` appends a registrar refresh event (`is_registrar_refresh` = True, `event_type="FROZEN"` under `DEPLOYMENT_B` at offset 6).
3. Post-refresh `current` state:
   - `current_state`: `"FROZEN"`
   - `package_hash`: `PACKAGE_A`
   - `deployment_identity_hash`: `DEPLOYMENT_B`

### 2. Guard Walk on the Candidate (`e9e37aec`)
The test attempts `self.append_authority_event` with:
- `event_id`: `"revoked-identity-readmission-old"`
- `event_type`: `"SHADOW_ELIGIBLE"`
- `writer_class`: `ENVIRONMENT_ADMISSION_AUTHORITY`
- `previous_state`: `"FROZEN"`
- `next_state`: `"SHADOW"`
- `package_hash`: `PACKAGE_A`
- `deployment_identity_hash`: `DEPLOYMENT_A`
- `check_set_version`: `"shadow-eligibility.v1"`
- `timestamp`: `BASE_TIME + timedelta(seconds=7)`

Tracing sequentially through [`p031_lifecycle_ledger.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R1_20260916/sources/p031_lifecycle_ledger_HEAD_lines_640-880.py#L15-L200):
- **Lines 15–16 (`:654-655`):** `evidence_references` present (`"fixture://matrix/..."`). Pass.
- **Line 18 (`:657`):** Not a `CHALLENGE`. Pass.
- **Line 21 (`:660`):** `actual_state` is `"FROZEN"` (not `"RETIRED"`). Pass.
- **Line 23 (`:662`):** `SHADOW_ELIGIBLE` in `AUTHORITY_EVENTS[ENVIRONMENT_ADMISSION_AUTHORITY]`. Pass.
- **Line 25 (`:664`):** `event.previous_state` (`"FROZEN"`) == `actual_state` (`"FROZEN"`). Pass.
- **Line 27 (`:666`):** Monotonic timestamp (offset 7 > 6). Pass.
- **Lines 30–35 (`:669-674`):** `is_registrar_refresh` is False.
- **Lines 36–47 (`:675-686`):** Guard `DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED` checks `actual_state in {"SHADOW", "TESTNET", "LIVE_CANDIDATE", "LIVE", "SUSPENDED"}`. Since `actual_state` is `"FROZEN"`, **does NOT fire**.
- **Line 49 (`:688`):** Not `DEMOTED`. Pass.
- **Lines 55–60 (`:694-699`):** Transition `("FROZEN", "SHADOW_ELIGIBLE", "SHADOW")` is present in `LADDER_TRANSITIONS`. Pass.
- **Lines 61–82 (`:700-721`):** Not `RESUMED` or `PROMOTED`. Pass.
- **Lines 84–102 (`:723-741`):** `check_set_version` (`"shadow-eligibility.v1"`) matches `active_check_sets["shadow_eligibility"]`. Pass.
- **Lines 103–134 (`:742-773`):** Triggers and catalog preconditions pass.
- **Lines 139–144 (`:778-783`):** `evaluation_run_hash` generated; `failing_checks` empty. Pass.
- **Lines 145–157 (`:784-796`):** Evaluation run unused and fresh. Pass.
- **Lines 161–183 (`:800-822`):** `writer_class` is not `REGISTRAR`. Moves to `else:` branch.
- **Lines 185–186 (`:824-825`):** `package_hash` and `deployment_hash` are both non-None. `LADDER_IDENTITY_INCOMPLETE` **does NOT fire**.
- **Lines 187–192 (`:826-831`):** `frozen_package` is `PACKAGE_A`; `package_hash` is `PACKAGE_A`. `PACKAGE_IDENTITY_MISMATCH` **does NOT fire**.
- **Lines 193–194 (`:832-833`):**
  ```python
  if current_deployment is not None and deployment_hash != current_deployment:
      raise ValueError("DEPLOYMENT_IDENTITY_MISMATCH")
  ```
  `current_deployment` is `DEPLOYMENT_B` (non-None). `deployment_hash` is `DEPLOYMENT_A`. Since `DEPLOYMENT_A != DEPLOYMENT_B`, **`ValueError("DEPLOYMENT_IDENTITY_MISMATCH")` FIRES FIRST**.

### 3. Guard Walk on Mutant M-2 (Lines 832–833 removed)
If lines 193–194 are removed:
- **Lines 195–196 (`:834-835`):** `if deployment_hash in retired_deployments:`. The registrar refresh to `FROZEN` under a new composite does not record a `RETIRED` event, nor does it add `DEPLOYMENT_A` to `retired_deployments`. `DEPLOYMENT_IDENTITY_RETIRED` **does NOT fire**.
- **Lines 197–199 (`:836-838`):** `owner = deployment_owners.get(deployment_hash)`. `DEPLOYMENT_A` was previously bound to candidate `QLC-20260916-revoked-identity`, which matches `event.candidate_id`. `DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE` **does NOT fire**.
- **Lines 203–207 (`:842-846`):** Returns `(PACKAGE_A, DEPLOYMENT_A)`. The event is **ACCEPTED**. The candidate transitions to `SHADOW` and `deployment_identity_hash` reverts to `DEPLOYMENT_A`.

This confirms mutant M-2 raises no exception, causing `self.assertRaisesRegex(ValueError, "DEPLOYMENT_IDENTITY_MISMATCH")` to fail with `AssertionError: ValueError not raised`, exactly as recorded in [`sources/LEAD_RED_ARM_mutant_M2_guard_removed.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R1_20260916/sources/LEAD_RED_ARM_mutant_M2_guard_removed.txt#L1-L5).

---

## (b) Findings

**No findings (0 REQUIRED, 0 NIT).**

- **F-1 Invariant Verification:**
  The new test [`test_post_refresh_admission_cannot_reuse_the_revoked_deployment_identity`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R1_20260916/subject/test_p031_lifecycle_ledger_HEAD_lines_2500-2680.py#L89-L167) covers all 4 necessary invariant properties:
  1. Old identity refused specifically by `DEPLOYMENT_IDENTITY_MISMATCH`.
  2. Candidate state remains `FROZEN` with `deployment_identity_hash = DEPLOYMENT_B`.
  3. No admission record appended to replay:
     ```python
     self.assertEqual(
         [
             record.event.event_id
             for record in self.ledger.replay()
             if record.event.candidate_id == candidate_id
             and record.event.event_type == "SHADOW_ELIGIBLE"
         ],
         ["revoked-identity-shadow_eligible"],
     )
     ```
     This queries `self.ledger.replay()` across all persisted records, ensuring zero admission records were written from the failed attempt.
  4. New identity accepted and recorded: admission under `DEPLOYMENT_B` succeeds, transitions state to `SHADOW`, and records `DEPLOYMENT_B`.
- **First read NITs (N-1..N-10):**
  N-1 through N-10 are documentation corrections, test naming adjustments, or non-blocking protocol observations. None are REQUIRED for Milestone 1 acceptance.

---

## (c) EXACT Read Coverage

All required reads were executed strictly within `_gemini_packets_20260913/P031_R1_20260916` using the native `view_file` tool with windows of ≤ 150 lines:

1. `PACKET_SHA256SUMS.txt`: lines 1–11 (complete)
2. `subject/DIFF_48bd70de_e9e37aec.patch`: lines 1–91 (complete)
3. `subject/DIFF_STAT_48bd70de_e9e37aec.txt`: lines 1–3 (complete)
4. `subject/COMMIT_e9e37aec.txt`: lines 1–31 (complete)
5. `subject/test_p031_lifecycle_ledger_HEAD_lines_2500-2680.py`: lines 1–150; continuation lines 151–182 (complete)
6. `subject/test_p031_lifecycle_ledger_HEAD_lines_1-420_helpers.py`: lines 1–150; continuation lines 151–300; continuation lines 301–421 (complete)
7. `sources/p031_lifecycle_ledger_HEAD_lines_640-880.py`: lines 1–150; continuation lines 151–242 (complete)
8. `sources/OPUS_T0_REPORT_attempt1_48bd70de.md`: lines 334–417; lines 418–480; lines 480–596; lines 597–611 (complete coverage of F-1, NITs N-1..N-10, NOT VERIFIED, and Summary)
9. `sources/LEAD_GUARD_R1.txt`: lines 1–18 (complete)
10. `sources/LEAD_PYTEST_GREEN_R1.txt`: lines 1–2 (complete)
11. `sources/LEAD_RED_ARM_mutant_M2_guard_removed.txt`: lines 1–5 (complete)

---

## (d) NOT VERIFIED

1. **Test Execution:** As a `SUPPLEMENTAL_UNEXECUTED` reviewer, this agent did not execute `pytest`, Python interpreters, or shell commands. Test outcomes (110 passed GREEN, 1 failed RED on M-2) were verified directly from the Lead test logs and code logic trace.
2. **Worktree & Repository State:** No Git commands (`git diff`, `git status`) or external workspace files outside the packet were inspected.
3. **Pre-existing Lint Findings:** The 36 pre-existing ruff lint findings noted in `COMMIT_e9e37aec.txt` were not independently audited.

---

## (e) Review Verdict JSON

```json
{
  "part": "P031_R1_GEMINI",
  "verdict": "PASS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "finding_F1": "CLOSED",
  "first_guard_to_fire": "p031_lifecycle_ledger.py:832-833 (DEPLOYMENT_IDENTITY_MISMATCH)",
  "mutant_would_accept": true,
  "findings": [],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
