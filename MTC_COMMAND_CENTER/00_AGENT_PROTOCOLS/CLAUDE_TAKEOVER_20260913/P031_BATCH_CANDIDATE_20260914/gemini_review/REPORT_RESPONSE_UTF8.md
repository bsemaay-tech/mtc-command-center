# Supplemental Read-Only Detection Review: WP-P0-31 M1 Lifecycle Ledger Engineering Batch (Candidate `96af3eb6`)

**Reviewer Identity:** Independent Detection Reviewer (`gemini-3.8-flash-high`)  
**Mode:** Supplemental Read-Only (`SUPPLEMENTAL_UNEXECUTED`)  
**Base Commit:** `c76043b92c70c9f79a6d06630c0896ebe73e68a1`  
**Candidate Commit:** `96af3eb6`  
**Authority:** [sources/DECISIONS_rows_P031.md](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/sources/DECISIONS_rows_P031.md) (`OD-20260914-P031-BATCH-GO-1`, `OD-20260914-P031-LIFECYCLE-1`)  
**Packet Inspected:** `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914`

---

## (a) Per-Item Classification Table

| Item | Option Text Quoted from Packet Excerpt | Diff Hunk Lines ([`subject/CANDIDATE_96af3eb6.diff`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff)) | Ledger File:Line ([`p031_lifecycle_ledger.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/sources/p031_lifecycle_ledger_96af3eb6.py)) | Classification |
|---|---|---|---|---|
| **OD-2** | **1B** (`:0451`, `:0454-0457`): *"The writer supplies `next_state`; the ledger validates that it is strictly below the current rung on the ladder order implied by `ledger:94-98` (`SHADOW` < `TESTNET` < `LIVE_CANDIDATE` < `LIVE`) and that `deployment_identity_hash` is unchanged... together with the two structural additions it requires — add `DEMOTED` to the `MULTI_WORKER_SUPERVISOR` authority set (`ledger:88-90`)... and add the corresponding descent tuples to `LADDER_TRANSITIONS`."* | `13`, `68`, `77-82`, `214-219`, `273-274`, `304-309` | `:42`, `:122`, `:134-139`, `:581-585`, `:682-687`, `:824-825` | **IMPLEMENTED-AS-ANSWERED** |
| **OD-5** | **4A** (`:0597`, `:0616-0617`): *"`REJECTED` carries an explicit writer-supplied `check_set_purpose` drawn from the declared set (`ledger:31-41`), validated against the candidate's current rung, with `check_set_version`, `evaluation_run_hash` and non-empty `failing_checks` all mandatory... restore `("REJECTED", "RE_ENTRY", "CANDIDATE")`."* | `20-31`, `39-45`, `51`, `244-247`, `277-278`, `323-326`, `361-365`, `395`, `414-416`, `445-449` | `:49-60`, `:70-76`, `:82`, `:600-603`, `:722-725`, `:765-769`, `:847`, `:868-870`, `:1038-1042` | **IMPLEMENTED-AS-ANSWERED** |
| **OD-6** | **5C** (`:0643`): *"Require the writer to supply the `check_set_version` of the gate whose slot is full, and take the target from that version's purpose instead of inferring it from `previous_state`."* | `14-19`, `76`, `221-231`, `248-251`, `279-283`, `319-322` | `:43-48`, `:133`, `:575-585`, `:604-607`, `:718-721` | **IMPLEMENTED-AS-ANSWERED** |
| **OD-7** | **6A** (`:0692`, `:0696`): *"A refresh is not a lifecycle event: the new composite re-enters through the ordinary door — the candidate returns to `FROZEN` under the new `deployment_identity_hash`, and revocation is expressed by the absence of admission records for that new identity. Prior windows stay readable and never count... naming `FROZEN` as the landing state... relaxation of `ledger:657-658` so a re-freeze may carry the new deployment identity."* | `46-50`, `291-296`, `374-388` | `:77-81`, `:663-668`, `:796-809` | **IMPLEMENTED-AS-ANSWERED** |
| **OD-9** | **5a-C** (`:0806`): *"Keep the transition, but gate it on a **sixth, owner-only trigger class** distinct from the five automatic ones, with a mandatory recorded one-sentence external-change reason, and keep every existing constraint (fresh evaluation run, identities cleared, retired identities permanently refused)."* | `59`, `114-119`, `346-354` | `:95`, `:261-266`, `:750-758` | **IMPLEMENTED-AS-ANSWERED** |
| **OD-10** | **5b-A** (`:0879`, `:0884-0897`): *"Ratify the implemented rule: one evaluation run may back any number of distinct check-set purposes within one epoch; cross-epoch and cross-candidate reuse stay refused... 1. `test:2192-2288` must gain real assertions before acceptance — the stored records' `check_set_purpose`, `check_set_version` and `evaluation_run_hash`, and the resulting `current_state`... 2. The report's `unresolved_lifecycle_contracts` list... omission should be closed... by recording the answer."* | `544`, `804-876`, `990`, `1412` | `:1453` (report text); [`test_p031_lifecycle_ledger.py:2372-2444`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L804-L876) | **IMPLEMENTED-AS-ANSWERED** |
| **OD-11** | **2C** (`:0281`): *"M1 keeps the opaque field, plus an optional configured catalog: when an accepted catalog is supplied, an `evaluation_run_hash` absent from it is refused; when none is supplied, the ledger fails closed on any record that claims catalog-backed evidence... narrowest reading... G1_SCOPE_AND_CONTRACT.md untouched."* | `86-90`, `98`, `106`, `128`, `136-138`, `155-166`, `175`, `178`, `187-189`, `334-341`, `396`, `455`, `463`, `472`, `484-485`, `492`, `504-505`, `512-513`, `521` | `:214`, `:238`, `:247`, `:320`, `:332-334`, `:387-397`, `:549-550`, `:738-745`, `:848`, `:1034`, `:1048`, `:1083`, `:1137`, `:1297`, `:1320`, `:1328`, `:1348`, `:1425` | **IMPLEMENTED-AS-ANSWERED** |
| **OD-1** | **3D** (`:0370`): *"Decouple. Keep the guard fail-closed and unratified, and amend the M1 acceptance line so a ratified worthiness version is a precondition of **writing a real `CAPTURED -> TRIAGED` record**, not of **accepting the ledger that stores it**... Changes no lifecycle semantics and ratifies nothing."* | `1-10`, `1416-1426` | N/A (Doc-only: [`DECISIONS.md:18`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L1-L10); [`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:298`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L1416-L1426); ledger code untouched) | **IMPLEMENTED-AS-ANSWERED** |
| **OD-4 / OD-8** | **3D-now / 7A** (`:0550`, `:0722`, `TASK:16`): *"ratify the current repository-wide refusal as the interim rule... Ratify the implemented rule: an `evaluation_run_hash` binds to exactly one `candidate_id` forever... the `unresolved_lifecycle_contracts` seven-string list in the ledger report... updated ONLY for the contracts this batch actually closes... each with the decision row id in the string; `CHALLENGE` stays UNRESOLVED."* | `528-546`, `702-707`, `970-992`, `1391-1415` | `:1443-1454` | **IMPLEMENTED-AS-ANSWERED** |
| **OD-3** | **2A** (`:0492`): `CHALLENGE` stays fail-closed pending WP-P0-04 carrying incumbent identity field. | `1386-1402` | `:650-651`, `:1444` | **IMPLEMENTED-AS-ANSWERED** |
| **OD-12** | **7-A**: Refresh behavior preserved on `c76043b9` base; no legacy import, cutover, or migration. | N/A | `:1433` | **IMPLEMENTED-AS-ANSWERED** |

---

## (b) RED/GREEN Test Verification Table per New Rule

| New Rule / Refusal Constraint | Error Raised | Diff Hunk / Ledger Line | RED Test Function (Exercises Refusal) | GREEN Test Function (Exercises Accepted Path) | Status & Arm Completeness |
|---|---|---|---|---|---|
| Demotion strict ladder descent | `DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT` | diff `309` / ledger `:687` | [`test_demoted_requires_strict_descent_and_keeps_deployment_identity`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L903-L915) (`test:2505-2516`) | [`test_demoted_requires_strict_descent_and_keeps_deployment_identity`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L884-L902) (`test:2484-2503`) | **COMPLETE** |
| Rejected check-set purpose mandatory | `CHECK_SET_PURPOSE_REQUIRED` | diff `246` / ledger `:602` | [`test_rejected_requires_purpose_hash_and_failing_checks`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L615-L646) (`test:697-718`) | [`test_rejected_requires_purpose_hash_and_failing_checks`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L657-L669) (`test:728-739`) | **COMPLETE** |
| Rejected evaluation run hash mandatory | `EVALUATION_RUN_HASH_REQUIRED` | diff `363` / ledger `:767` | [`test_rejected_requires_purpose_hash_and_failing_checks`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L621-L646) (`test:703-718`) | [`test_rejected_requires_purpose_hash_and_failing_checks`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L657-L669) (`test:728-739`) | **COMPLETE** |
| Rejected non-empty failing checks mandatory | `FAILING_CHECKS_REQUIRED` | diff `365` / ledger `:769` | [`test_rejected_requires_purpose_hash_and_failing_checks`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L628-L646) (`test:710-718`) | [`test_rejected_requires_purpose_hash_and_failing_checks`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L657-L669) (`test:728-739`) | **COMPLETE** |
| Rejected check-set purpose mismatch for rung | `CHECK_SET_PURPOSE_MISMATCH` | diff `326` / ledger `:725` | [`test_rejected_requires_purpose_hash_and_failing_checks`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L648-L655) (`test:719-727`) | [`test_rejected_requires_purpose_hash_and_failing_checks`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L657-L669) (`test:728-739`) | **COMPLETE** |
| Capacity withholding purpose mismatch for rung | `ADMISSION_WITHHELD_TARGET_UNRESOLVED` | diff `322` / ledger `:721` | [`test_admission_withheld_capacity_records_gate_purpose`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L736-L752) (`test:2006-2023`) | [`test_admission_withheld_capacity_records_gate_purpose`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L714-L726) (`test:1980-1993`) | **COMPLETE** |
| Registrar refresh identity invalid (same deployment identity) | `DEPLOYMENT_REFRESH_IDENTITY_INVALID` | diff `381` / ledger `:803` | [`test_deployment_refresh_returns_to_frozen_under_new_composite`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L922-L943) (`test:2523-2544`), [`test_deployment_refresh_registrar_path_is_available_at_every_deep_state`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L1132-L1145) (`test:2910-2924`) | [`test_deployment_refresh_returns_to_frozen_under_new_composite`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L944-L965) (`test:2545-2565`), [`test_deployment_refresh_registrar_path_is_available_at_every_deep_state`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L1146-L1162) (`test:2925-2940`) | **COMPLETE** (See Finding J-05 regarding package-hash and null-hash branches) |
| Retired re-entry trigger not `OWNER_EXTERNAL_CHANGE` or reason not 1 sentence | `RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED` | diff `351` / ledger `:755` | [`test_retired_reentry_requires_owner_external_change_reason`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L1244-L1265) (`test:4084-4103`) | [`test_every_ratified_reentry_trigger_returns_to_same_candidate`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L1213-L1222) (`test:4007-4017`) | **COMPLETE** |
| Non-retired re-entry using owner-only `OWNER_EXTERNAL_CHANGE` | `REENTRY_TRIGGER_INVALID` | diff `354` / ledger `:758` | [`test_retired_reentry_requires_owner_external_change_reason`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L1267-L1296) (`test:4117-4136`) | `test_every_ratified_reentry_trigger_returns_to_same_candidate` (with non-owner triggers on PARKED/CANDIDATE) | **COMPLETE** |
| Catalog-backed claim without configured catalog | `CATALOG_BACKED_EVIDENCE_WITHOUT_ACCEPTED_CATALOG` | diff `335` / ledger `:739` | [`test_catalog_backed_claim_fails_closed_without_catalog`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L1007-L1026) (`test:2777-2794`) | [`test_configured_catalog_refuses_absent_hash_and_accepts_present_hash`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L1027-L1048) (`test:2804-2818`) | **COMPLETE** |
| Evaluation run hash absent from configured catalog | `EVALUATION_RUN_HASH_NOT_IN_ACCEPTED_CATALOG` | diff `341` / ledger `:745` | [`test_configured_catalog_refuses_absent_hash_and_accepts_present_hash`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L1049-L1072) (`test:2826-2843`) | [`test_configured_catalog_refuses_absent_hash_and_accepts_present_hash`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L1027-L1048) (`test:2804-2818`) | **COMPLETE** |
| Configured catalog normalization validation | `ACCEPTED_EVALUATION_CATALOG_INVALID` | diff `162`, `165` / ledger `:393`, `:396` | **NONE** (no test in test suite exercises invalid string or malformed hash in catalog argument) | [`test_configured_catalog_refuses_absent_hash_and_accepts_present_hash`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L1027-L1048) | **MISSING RED ARM** (Finding J-01) |
| Evidence argument `catalog_backed` type validation | `CATALOG_BACKED_INVALID` | diff `188` / ledger `:550` | **NONE** (no test exercises non-bool `catalog_backed="true"` or `1`) | Implicitly covered on valid boolean values | **MISSING RED ARM** (Finding J-02) |
| Writer-supplied `check_set_purpose` unknown string on append | `CHECK_SET_PURPOSE_UNKNOWN` | diff `243` / ledger `:597` | **NONE** for append parameter (only pre-existing test for `active_check_sets` mapping at `:462`) | Valid purpose append | **MISSING RED ARM for append** |

---

## (c) Findings

### J-01 [CORRECTION] — Missing RED test for `ACCEPTED_EVALUATION_CATALOG_INVALID`
- **Location:** [`MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L548-L1415)
- **Evidence:** In [`p031_lifecycle_ledger.py:387-397`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/sources/p031_lifecycle_ledger_96af3eb6.py#L387-L397), [`LifecycleLedger._normalize_accepted_catalog`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/sources/p031_lifecycle_ledger_96af3eb6.py#L387-L397) introduces two distinct refusal branches raising `ValueError("ACCEPTED_EVALUATION_CATALOG_INVALID")`: (1) when `accepted_evaluation_catalog` is a string, bytes, or bytearray; and (2) when any hash element is not a string or fails `^[0-9a-f]{64}$`. Across all 1429 lines of [`subject/CANDIDATE_96af3eb6.diff`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff) and [`test_p031_lifecycle_ledger.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L548-L1415), neither refusal is exercised by any test. This violates the mandatory task rule: *"Every new rule has a RED test (refusal) and a GREEN test."*

### J-02 [CORRECTION] — Missing RED test for `CATALOG_BACKED_INVALID`
- **Location:** [`MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L548-L1415)
- **Evidence:** In [`p031_lifecycle_ledger.py:549-550`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/sources/p031_lifecycle_ledger_96af3eb6.py#L549-L550), [`LifecycleLedger._normalize_evidence`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/sources/p031_lifecycle_ledger_96af3eb6.py#L549-L550) adds:
  ```python
  if type(catalog_backed) is not bool:
      raise ValueError("CATALOG_BACKED_INVALID")
  ```
  No test in [`test_p031_lifecycle_ledger.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L548-L1415) asserts that non-boolean values (e.g. integer `1`, string `"true"`, or float `1.0`) raise `CATALOG_BACKED_INVALID`. This arm lacks a corresponding RED test.

### J-03 [NIT] — Semantic Edge-Case: `catalog_backed=True` with `evaluation_run_hash=None` Allowed When Catalog Is Configured
- **Location:** [`MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:738-745`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/sources/p031_lifecycle_ledger_96af3eb6.py#L738-L745)
- **Evidence:** In [`LifecycleLedger._validate_transition`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/sources/p031_lifecycle_ledger_96af3eb6.py#L738-L745):
  ```python
  if catalog_backed and self.accepted_evaluation_catalog is None:
      raise ValueError("CATALOG_BACKED_EVIDENCE_WITHOUT_ACCEPTED_CATALOG")
  if (
      self.accepted_evaluation_catalog is not None
      and evaluation_run_hash is not None
      and evaluation_run_hash not in self.accepted_evaluation_catalog
  ):
      raise ValueError("EVALUATION_RUN_HASH_NOT_IN_ACCEPTED_CATALOG")
  ```
  If `self.accepted_evaluation_catalog` is configured, an append supplying `catalog_backed=True` and `evaluation_run_hash=None` (valid for Registrar events such as `CAPTURED` or `TRIAGED`) bypasses both checks: line 738 is false because a catalog exists, and line 741 is false because `evaluation_run_hash` is None. Consequently, an authoritative or fixture event can claim catalog-backed evidence without providing any hash to verify against the catalog.

### J-04 [NIT] — Citation Error in `subject/REPORT.md` per-answer table for OD-2
- **Location:** [`subject/REPORT.md:39`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/REPORT.md#L39)
- **Evidence:** The per-answer table for OD-2 cites file:line `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:803` for the claim that `DEMOTED` enforces unchanged deployment identity. Opening line 803 reveals:
  ```python
  803: raise ValueError("DEPLOYMENT_REFRESH_IDENTITY_INVALID")
  ```
  This is the error for registrar deployment refresh (OD-7). Unchanged deployment identity for `DEMOTED` (issued by `MULTI_WORKER_SUPERVISOR`) is instead enforced at lines `824-825`:
  ```python
  824: if current_deployment is not None and deployment_hash != current_deployment:
  825:     raise ValueError("DEPLOYMENT_IDENTITY_MISMATCH")
  ```

### J-05 [NIT] — Partial Branch Coverage for `DEPLOYMENT_REFRESH_IDENTITY_INVALID`
- **Location:** [`MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:796-803`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/sources/p031_lifecycle_ledger_96af3eb6.py#L796-L803)
- **Evidence:** In `is_registrar_refresh`:
  ```python
  if (
      deployment_hash is None
      or current is None
      or package_hash != current.get("package_hash")
      or deployment_hash == current.get("deployment_identity_hash")
  ):
      raise ValueError("DEPLOYMENT_REFRESH_IDENTITY_INVALID")
  ```
  The tests [`test_deployment_refresh_returns_to_frozen_under_new_composite`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L917-L965) and [`test_deployment_refresh_registrar_path_is_available_at_every_deep_state`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff#L1074-L1202) test only `deployment_hash == current.get("deployment_identity_hash")` (same identity). The branches for `deployment_hash is None` and `package_hash != current.get("package_hash")` lack dedicated RED tests.

---

## (d) Exact Read Coverage

All views were conducted with `view_file` at $\le 150$ lines per view, continuing through all truncations:

1. [`C:/LAB/Tradingview_LAB_CLEAN/AGENTS.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/AGENTS.md): lines 1–64 (complete).
2. [`PACKET_SHA256SUMS.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/PACKET_SHA256SUMS.txt): lines 1–9 (complete).
3. [`sources/DECISIONS_rows_P031.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/sources/DECISIONS_rows_P031.md): lines 1–3 (complete).
4. [`subject/TASK_P31B_original.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/TASK_P31B_original.md): lines 1–28 (complete).
5. [`subject/INVENTORY.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/INVENTORY.md): lines 1–44 (complete).
6. [`subject/REPORT.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/REPORT.md):
   - lines 1–150
   - lines 151–300 (continuation 1)
   - lines 301–450 (continuation 2)
   - lines 451–469 (continuation 3; complete, 469 lines).
7. [`subject/CANDIDATE_96af3eb6.diff`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff):
   - lines 1–150 (initial chunk, offset 0–46080)
   - lines 1–150 (continuation 1, ContentOffset=46080 to end of chunk 1)
   - lines 151–300 (chunk 2)
   - lines 301–450 (chunk 3)
   - lines 451–600 (chunk 4)
   - lines 601–750 (chunk 5)
   - lines 751–900 (chunk 6)
   - lines 901–1050 (chunk 7)
   - lines 1051–1200 (chunk 8)
   - lines 1201–1350 (chunk 9)
   - lines 1351–1429 (chunk 10; complete, 1429 lines).
8. [`sources/P031_LIFECYCLE_DECISIONS_V4_excerpt.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/sources/P031_LIFECYCLE_DECISIONS_V4_excerpt.md):
   - lines 1–150 (chunk 1)
   - lines 151–300 (chunk 2)
   - lines 301–450 (chunk 3)
   - lines 451–600 (chunk 4)
   - lines 601–661 (chunk 5; complete, 661 lines).
9. [`sources/p031_lifecycle_ledger_96af3eb6.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/sources/p031_lifecycle_ledger_96af3eb6.py):
   - lines 1–150 (verified citations: `:42`, `:49`, `:85`, `:95`, `:122`, `:134`)
   - lines 300–450 (verified citations: `:320`, `:388`)
   - lines 670–820 (verified citations: `:680`, `:682`, `:718`, `:723`, `:738`, `:741`, `:751`, `:803`)
   - lines 810–860 (verified demotion identity validation: `:824-825`)
   - lines 920–970 (verified append state updates: `:935`)
   - lines 970–1000 (verified current-state commit)
   - lines 1030–1070 (verified replay evidence validation: `:1034`, `:1048`)
   - lines 1080–1130 (verified `_validated_history` and `deployment_owners`)
   - lines 1280–1310 (verified `backup_to` catalog propagation: `:1297`)
   - lines 1430–1460 (verified report citations: `:1443`, `:1446`).
10. [`subject/PROGRESS.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/PROGRESS.md): lines 1–10 (complete).
11. [`subject/CANDIDATE_96af3eb6.diff`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/CANDIDATE_96af3eb6.diff): lines 980–1100 (cross-check on catalog test definitions).

---

## (e) Non-Empty NOT VERIFIED

1. **No Execution Authority:** As an independent read-only reviewer operating under `SUPPLEMENTAL_UNEXECUTED`, no command execution, test runner invocation, subprocess execution, or Python interpreter execution was performed.
2. **Environment and Test Results:** The test suite results reported in [`subject/REPORT.md:113-135`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/REPORT.md#L113-L135) (106 tests, 105 passed, 1 skipped on Python 3.14.2 / pytest 9.0.2) and the absence of pinned Python 3.12 are reported verbatim from the builder's and Lead's records; they are not independently executed or verified by this reviewer.
3. **Cryptographic Hashes:** The hash digests in [`PACKET_SHA256SUMS.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/PACKET_SHA256SUMS.txt) and [`subject/REPORT.md:61-66`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_BATCH_20260914/subject/REPORT.md#L61-L66) were read and verified as document text; no terminal hashing tools were run.
4. **Git Tree and Lock State:** The permission denied error on `index.lock` preventing local commit by the builder lane was inspected in report text only; no Git mutations or repository lock checks were executed.
5. **Upstream Acceptance Blockers:** Provenance and acceptance for upstream milestones WP-P0-04, WP-P0-13, and active worthiness check-set ratification remain unverified and unresolved.

---

## (f) Required JSON Machine-Readable Verdict

```json
{
  "part": "P031_BATCH_GEMINI",
  "verdict": "REQUEST_CHANGES",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "findings": [
    {
      "id": "J-01",
      "severity": "CORRECTION",
      "file": "MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py",
      "line": 1027,
      "description": "Missing RED test exercising ValueError('ACCEPTED_EVALUATION_CATALOG_INVALID') for invalid catalog types or malformed hashes in LifecycleLedger._normalize_accepted_catalog."
    },
    {
      "id": "J-02",
      "severity": "CORRECTION",
      "file": "MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py",
      "line": 2775,
      "description": "Missing RED test exercising ValueError('CATALOG_BACKED_INVALID') when non-boolean values are passed to LifecycleLedger.append(catalog_backed=...)."
    },
    {
      "id": "J-03",
      "severity": "NIT",
      "file": "MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py",
      "line": 738,
      "description": "Semantic edge case: an append with catalog_backed=True and evaluation_run_hash=None is accepted without validation when accepted_evaluation_catalog is configured."
    },
    {
      "id": "J-04",
      "severity": "NIT",
      "file": "subject/REPORT.md",
      "line": 39,
      "description": "Per-answer table citation error for OD-2: cites p031_lifecycle_ledger.py:803 (DEPLOYMENT_REFRESH_IDENTITY_INVALID) instead of lines 824-825 (DEPLOYMENT_IDENTITY_MISMATCH)."
    },
    {
      "id": "J-05",
      "severity": "NIT",
      "file": "MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py",
      "line": 2517,
      "description": "Incomplete RED branch coverage for DEPLOYMENT_REFRESH_IDENTITY_INVALID: tests cover only same-deployment-identity, leaving package-hash-drift and missing-deployment-hash untested."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
