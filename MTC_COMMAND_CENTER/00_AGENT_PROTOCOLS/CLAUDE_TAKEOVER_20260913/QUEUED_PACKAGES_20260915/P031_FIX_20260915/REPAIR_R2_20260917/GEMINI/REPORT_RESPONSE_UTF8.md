# Supplemental Read-Only Review: WP-P0-31 Milestone-1 T0 Repair Round 2 (Commit `61c56148`)

- **Target Commit**: `61c56148` on `feature/p031-m1-20260913-refresh` (base candidate `e9e37aec`)
- **Reviewer Role**: `gemini-3.8-flash-high` (Detection Reviewer, `SUPPLEMENTAL_UNEXECUTED`)
- **Evidence Baseline**: Read-only static analysis of packet `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R2_20260917`

---

## 1. Guard-Order Walks and Mutation Fencing Analysis

### 1.1 Trace & Guard Walk: Test 1 (`test_registrar_refresh_cannot_adopt_the_candidates_own_retired_identity`)

Test source: [`test_p031_lifecycle_ledger_HEAD_lines_2580-2830.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R2_20260917/subject/test_p031_lifecycle_ledger_HEAD_lines_2580-2830.py#L101-L188).

#### Preparatory Steps Walk
1. **`build_to_rung(..., "SHADOW_ELIGIBLE")`**:
   - Registrar appends `CAPTURED` ($t=0$), `TRIAGED` ($t=1$), `CANDIDATE` ($t=2$), `FROZEN` ($t=3$, `package_hash=PACKAGE_A`, `deployment_identity_hash=None`).
   - Admission authority appends `SHADOW_ELIGIBLE` ($t=4$, `package_hash=PACKAGE_A`, `deployment_identity_hash=DEPLOYMENT_A`, `offset=4`).
   - In replay bookkeeping ([`lines 124-125`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R2_20260917/sources/p031_lifecycle_ledger_HEAD_lines_1000-1140_replay_bookkeeping.py#L124-L125)), `deployment_owners.setdefault(DEPLOYMENT_A, candidate_id)` binds `DEPLOYMENT_A` to `candidate_id`. `current_state` is `SHADOW`. Accepted.
2. **`append_authority_event(..., "RETIRED")`**:
   - `writer_class="MULTI_WORKER_SUPERVISOR"` at $t=5$. `previous_state="SHADOW"`.
   - Passes transition `("SHADOW", "RETIRED", "RETIRED")` in ladder transitions.
   - Replay bookkeeping ([`lines 126-131`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R2_20260917/sources/p031_lifecycle_ledger_HEAD_lines_1000-1140_replay_bookkeeping.py#L126-L131)): adds `DEPLOYMENT_A` to `retired_deployments` and `PACKAGE_A` to `retired_packages[candidate_id]`. `current_state` becomes `RETIRED`. Accepted.
3. **`registrar.append(..., "RE_ENTRY")`**:
   - `actual_state == "RETIRED"`. Event carries `trigger="OWNER_EXTERNAL_CHANGE"`, valid one-sentence reason `"The venue replaced its matching engine."`, fresh evaluation run hash, and timestamp $t=6$.
   - Passes `:719-725` (packet `:119-125`).
   - Line `:801-802` (packet `:201-202`) returns `(None, None)`. `current_state` becomes `CANDIDATE`. Accepted.
4. **`registrar.append(..., "FROZEN")` (Re-freeze)**:
   - Registrar FROZEN from `CANDIDATE` at $t=7$ with `package_hash=PACKAGE_B`. `is_registrar_refresh` is `False` (`actual_state` is `CANDIDATE`).
   - `package_hash=PACKAGE_B` is checked against `retired_packages[candidate_id]` (`{PACKAGE_A}`). `PACKAGE_B not in {PACKAGE_A}`, so `:819-820` does not fire. Returns `(PACKAGE_B, None)`. Accepted.
5. **`append_authority_event(..., "SHADOW_ELIGIBLE")` (Re-admission)**:
   - Admission authority at $t=8$ with `package_hash=PACKAGE_B`, `deployment_identity_hash=DEPLOYMENT_B`.
   - `PACKAGE_B` matches frozen package. `DEPLOYMENT_B` is not in `retired_deployments` (`{DEPLOYMENT_A}`).
   - Bookkeeping binds `deployment_owners[DEPLOYMENT_B] = candidate_id`.
   - `current_state` is `SHADOW`, package is `PACKAGE_B`, deployment identity is `DEPLOYMENT_B`. Accepted.

All preparatory transitions are valid and accepted without tripping any ledger guard.

#### Refresh Step on Candidate
Registrar append at $t=9$: `previous_state="SHADOW"`, `next_state="FROZEN"`, `package_hash=PACKAGE_B`, `deployment_identity_hash=DEPLOYMENT_A`.
- At this point, `current` is `{'candidate_id': candidate_id, 'current_state': 'SHADOW', 'package_hash': PACKAGE_B, 'deployment_identity_hash': DEPLOYMENT_B}`.
- `writer_class` is `REGISTRAR`, `event_type == "FROZEN"`, `actual_state == "SHADOW"` $\implies$ `is_registrar_refresh` is **`True`** ([`lines 30-35`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R2_20260917/sources/p031_lifecycle_ledger_HEAD_lines_640-880.py#L30-L35)).
- Guard `:805-811` (`DEPLOYMENT_REFRESH_IDENTITY_INVALID`, packet lines 166-172):
  `deployment_hash` is not None (`DEPLOYMENT_A`), `current` is present, `package_hash == current["package_hash"]` (`PACKAGE_B == PACKAGE_B`), and `deployment_hash != current["deployment_identity_hash"]` (`DEPLOYMENT_A != DEPLOYMENT_B`). Condition evaluates to **`False`** (does not fire).
- Guard `:812-813` (`DEPLOYMENT_IDENTITY_RETIRED`, packet lines 173-174):
  `deployment_hash in retired_deployments` evaluates to **`True`** because `DEPLOYMENT_A` was added to `retired_deployments` at step 2.
- **First Guard to Fire**: `DEPLOYMENT_IDENTITY_RETIRED` (`:812-813`).

#### Behavior on Mutant `:812-813` (Lines 173-174 removed)
- Next guard `:814-816` (`DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE`, packet lines 175-177):
  `owner = deployment_owners.get(DEPLOYMENT_A)` resolves to `candidate_id`. Condition `owner != event.candidate_id` evaluates to **`False`**. Does NOT rescue or refuse.
- `elif deployment_hash is not None` (line 178) is skipped (`is_registrar_refresh` is `True`).
- Guard `:819-820` (`RETIRED_PACKAGE_IDENTITY`, packet lines 180-181):
  `package_hash` is `PACKAGE_B`. `retired_packages[candidate_id]` is `{PACKAGE_A}`. `PACKAGE_B not in {PACKAGE_A}`. Does NOT rescue or refuse.
- Ladder checks (`:824-839`, packet lines 185-200) are skipped (`writer_class is REGISTRAR`).
- Transition validation completes and returns `(PACKAGE_B, DEPLOYMENT_A)`.
- **Mutant Result**: The refresh is **ACCEPTED** by the ledger. The test fails with `AssertionError: ValueError not raised` as proven by `sources/LEAD_RED_R2_M4_refresh_retired_guard_removed.txt`. Test 1 specifically fences guard `:812-813`.

---

### 1.2 Trace & Guard Walk: Test 2 (`test_registrar_refresh_cannot_adopt_another_candidates_identity`)

Test source: [`test_p031_lifecycle_ledger_HEAD_lines_2580-2830.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R2_20260917/subject/test_p031_lifecycle_ledger_HEAD_lines_2580-2830.py#L190-L243).

#### Preparatory Steps Walk
1. `build_to_rung` for `CANDIDATE_B` to `SHADOW_ELIGIBLE` under `PACKAGE_B` / `DEPLOYMENT_B` ($t=0 \dots 4$).
   - `deployment_owners[DEPLOYMENT_B] = CANDIDATE_B`.
   - `states[CANDIDATE_B]` has state `SHADOW`, package `PACKAGE_B`, deployment `DEPLOYMENT_B`.
2. `build_to_rung` for `CANDIDATE_A` to `SHADOW_ELIGIBLE` under `PACKAGE_A` / `DEPLOYMENT_A` ($t=0 \dots 4$).
   - `deployment_owners[DEPLOYMENT_A] = CANDIDATE_A`.
   - `states[CANDIDATE_A]` has state `SHADOW`, package `PACKAGE_A`, deployment `DEPLOYMENT_A`.
3. **Sequencing / Timestamp Non-Collision**:
   - Bookkeeping line 114 ([`sources/p031_lifecycle_ledger_HEAD_lines_1000-1140_replay_bookkeeping.py:114`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R2_20260917/sources/p031_lifecycle_ledger_HEAD_lines_1000-1140_replay_bookkeeping.py#L114)) stores timestamps partitioned by candidate: `last_timestamps[event.candidate_id] = event.timestamp`. Monotonicity check in `:667` is checked against `last_timestamps.get(event.candidate_id)`. Independent candidate fixture offsets do not collide.
   - Writer sequence counts per `(writer_class, writer_id)` increment smoothly across calls.

#### Refresh Step on Candidate
Registrar refresh of `CANDIDATE_A` at $t=6$: `previous_state="SHADOW"`, `next_state="FROZEN"`, `candidate_id=CANDIDATE_A`, `package_hash=PACKAGE_A`, `deployment_identity_hash=DEPLOYMENT_B`.
- `current` is `states[CANDIDATE_A]`: `current_state="SHADOW"`, `package_hash=PACKAGE_A`, `deployment_identity_hash=DEPLOYMENT_A`.
- `is_registrar_refresh` is **`True`**.
- Guard `:805-811` (`DEPLOYMENT_REFRESH_IDENTITY_INVALID`, packet lines 166-172):
  `deployment_hash == DEPLOYMENT_B != current["deployment_identity_hash"]` (`DEPLOYMENT_A`), `package_hash == current["package_hash"]`. Condition is `False`. Does not fire.
- Guard `:812-813` (`DEPLOYMENT_IDENTITY_RETIRED`, packet lines 173-174):
  `DEPLOYMENT_B in retired_deployments` evaluates to `False` (`retired_deployments` is empty). Does not fire.
- Guard `:814-816` (`DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE`, packet lines 175-177):
  `owner = deployment_owners.get(DEPLOYMENT_B)` $\implies$ `CANDIDATE_B`.
  `owner is not None and owner != event.candidate_id` (`CANDIDATE_B != CANDIDATE_A`) evaluates to **`True`**.
- **First Guard to Fire**: `DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE` (`:814-816`).

#### Behavior on Mutant `:814-816` (Lines 175-177 removed)
- Line 178 is skipped.
- Line 180 (`RETIRED_PACKAGE_IDENTITY`): `retired_packages.get(CANDIDATE_A)` is empty. Does not fire.
- Ladder checks skipped for registrar.
- Returns `(PACKAGE_A, DEPLOYMENT_B)`.
- **Mutant Result**: The refresh is **ACCEPTED** by the ledger. Two candidates share `DEPLOYMENT_B` (one FROZEN, one SHADOW). The test fails with `AssertionError: ValueError not raised` as proven by `sources/LEAD_RED_R2_M7_refresh_bound_guard_removed.txt`. Test 2 specifically fences guard `:814-816`.

---

## 2. Invariant Assertion Completeness

Both tests assert the full invariant:
1. **Refusal Code**: Fenced via exact regex in `assertRaisesRegex` (`"DEPLOYMENT_IDENTITY_RETIRED"` and `"DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE"`).
2. **Current State Unchanged**:
   - Test 1: `candidate_id` remains in `SHADOW`, package `PACKAGE_B`, deployment `DEPLOYMENT_B`.
   - Test 2: claimant `CANDIDATE_A` remains `SHADOW`, `PACKAGE_A`, `DEPLOYMENT_A`; holder `CANDIDATE_B` remains `SHADOW`, `PACKAGE_B`, `DEPLOYMENT_B`.
3. **Replay Lineage**:
   - Test 1 verifies replay records for `candidate_id` contain strictly `["refresh-retired-frozen", "refresh-retired-refreeze"]` (no failed refresh record written).
   - Test 2 verifies replay records across the ledger contain strictly `["refresh-foreign-holder-frozen", "refresh-foreign-claimant-frozen"]` (no failed refresh record written for either candidate).

---

## 3. Scope and Record Honesty

### Scope Verification
- [`DIFF_STAT_e9e37aec_61c56148.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R2_20260917/subject/DIFF_STAT_e9e37aec_61c56148.txt) shows exactly 1 file changed: 158 insertions, 2 deletions.
- [`DIFF_e9e37aec_61c56148.patch`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R2_20260917/subject/DIFF_e9e37aec_61c56148.patch) touches only `test_p031_lifecycle_ledger.py`.
- The 2 deletions (`-2`) are strictly the two docstring lines in `test_post_refresh_admission_cannot_reuse_the_revoked_deployment_identity`:
  - `Lane-3` $\rightarrow$ `Lane-1` (correcting lane citation per N-12).
  - `:832-833` line pin $\rightarrow$ `the ladder-path guard` (durable citation per N-12).
- The 158 insertions (`+158`) comprise the 2 updated docstring lines + 156 lines containing the two new test methods.
- Zero changes to ledger source code or contracts.

### Record Honesty
- **REPRO**: Pre-repair test run with mutants removed confirms both mutants passed all 110 tests (`110 passed, 1 skipped, 167 subtests passed in 19.54s / 24.18s`, exit=0) in `LEAD_REPRO_F2_M4_*.txt` and `LEAD_REPRO_F2_M7_*.txt`.
- **RED**: Each mutant produces exactly `1 failed, 111 passed, 1 skipped, 167 subtests passed` (exit=1), failing solely on its designated test method in `LEAD_RED_R2_M4_*.txt` and `LEAD_RED_R2_M7_*.txt`.
- **GREEN**: Unmutated candidate + tests produces `112 passed, 1 skipped, 167 subtests passed in 28.47s` (exit=0) and contracts `50 passed in 0.24s` (exit=0) in `LEAD_PYTEST_GREEN_R2.txt`.
- Repo Guard passes with clean staging (`LEAD_GUARD_R2.txt`).

---

## 4. Status of Carried NITs N-1..N-13

- **N-1 through N-10**: Dispositioned in Round 1; re-read by Opus T0 round 2 and confirmed not required for M1 acceptance.
- **N-11** (CRLF vs LF hash pin): Working-tree artifact; commit blob OID is immutable.
- **N-12** (Docstring citation drift): **Resolved directly** in this commit's -2/+2 edit.
- **N-13** (Reversibility of OD-7 revocation): Design question for M1 acceptance packet; does not block code correctness.
- None of N-1..N-13 are REQUIRED for M1 acceptance.

---

## 5. Findings

No REQUIRED or NIT findings identified in commit `61c56148`. Finding F-2 is fully CLOSED.

---

## 6. Exact Read Coverage

All reads performed natively via `view_file` strictly within `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R2_20260917`:
- `PACKET_SHA256SUMS.txt`: lines 1–15 (complete)
- `subject/DIFF_STAT_e9e37aec_61c56148.txt`: lines 1–3 (complete)
- `subject/COMMIT_61c56148.txt`: lines 1–40 (complete)
- `subject/DIFF_e9e37aec_61c56148.patch`: lines 1–150, 151–181 (complete; 1 continuation)
- `subject/test_p031_lifecycle_ledger_HEAD_lines_2580-2830.py`: lines 1–150, 151–252 (complete; 1 continuation)
- `subject/test_p031_lifecycle_ledger_HEAD_lines_1-420_helpers.py`: lines 1–140, 141–280, 281–421 (complete; 2 continuations)
- `sources/p031_lifecycle_ledger_HEAD_lines_640-880.py`: lines 1–150, 151–242 (complete; 1 continuation)
- `sources/p031_lifecycle_ledger_HEAD_lines_1000-1140_replay_bookkeeping.py`: lines 1–142 (complete)
- `sources/OPUS_T0_REPORT_attempt2_e9e37aec.md`: lines 291–336, 403–546, 580–599 (all specified ranges complete)
- `sources/LEAD_GUARD_R2.txt`: lines 1–18 (complete)
- `sources/LEAD_PYTEST_GREEN_R2.txt`: lines 1–12 (complete)
- `sources/LEAD_RED_R2_M4_refresh_retired_guard_removed.txt`: lines 1–96 (complete)
- `sources/LEAD_RED_R2_M7_refresh_bound_guard_removed.txt`: lines 1–44 (complete)
- `sources/LEAD_REPRO_F2_M4_refresh_retired_guard_removed.txt`: lines 1–10 (complete)
- `sources/LEAD_REPRO_F2_M7_refresh_bound_guard_removed.txt`: lines 1–10 (complete)

---

## 7. Not Verified

- Dynamic execution of tests or commands (reviewer role is `SUPPLEMENTAL_UNEXECUTED`, read-only).
- Repository files outside `_gemini_packets_20260913/P031_R2_20260917`.
- Unread line ranges in `sources/OPUS_T0_REPORT_attempt2_e9e37aec.md` (lines 1–290, 337–402, 547–579).

---

```json
{
  "part": "P031_R2_GEMINI",
  "verdict": "PASS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "finding_F2": "CLOSED",
  "first_guard_to_fire_test1": "DEPLOYMENT_IDENTITY_RETIRED (ledger :812-813)",
  "first_guard_to_fire_test2": "DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE (ledger :814-816)",
  "mutant_812_would_accept": true,
  "mutant_814_would_accept": true,
  "findings": [],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
