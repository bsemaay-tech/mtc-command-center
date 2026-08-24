# WP-P0-04 Contracts Package v0 — Lane E Report

## Status

- Date: 2026-08-25
- Worktree: `C:\WPP004_20260825`
- Branch: `feature/wp-p0-04-contracts-20260825`
- Implementer: Codex, acting as the counterpart IMPLEMENTER for the Claude Fable Lead
- Audit tier: **T1** — schemas that will later govern money-moving code
- Gate status: Gates 3–4 implementation/self-QA complete; **READY FOR LEAD GATE 5**, not accepted or merged
- Package commit: `2c37b42db03cdec675f426f5956ec33f97685ebd`
- Repair round 1 status: Gates 3-4 implementation/self-QA complete;
  **READY FOR LEAD T1 RE-AUDIT ROUND 2**, not accepted or merged
- Base at lane start: `4691a9dd843f05948b271a88972c94a3bdce13a7`
- Current `origin/master` observed at close: `776f0349f85279971d1ed985001e9d3f00f9758e`
  (the isolated lane is three upstream commits behind; no rebase/merge was attempted because the Lead owns integration sequencing)

## Delivered

Versioned, immutable Pydantic v2 schemas under `MTC_COMMAND_CENTER/contracts/`:

- `SizingRequest` and `BoundSizingIntent`, with exactly four normalized methods and `SOURCE_DEFINED` provenance only.
- `OrderIntent`, `ExitIntent`, `StrategyPackage`, frozen instrument metadata, and `AccountSnapshot`.
- Canonical `candidate_id`, `package_hash`, `evaluation_run_hash`, `deployment_identity_hash`, `trial_id`, `run_id`, and `family_id` formulae.
- `RiskBucket`, member/allocation policy, Guardian policy, and the seven exact Guardian veto classes.
- Optimizer-independent `TrialRecord` and selected-artifact manifest.
- Machine-readable eligibility check/verdict types and immutable admission decisions, including the exact `PAPER_ELIGIBLE → {INTERNAL_PAPER}` split.
- Environment/evidence lineage, the seven freshness states, worker/environment evidence windows and gaps, two-way-interim/three-way reconciliation records, and lifecycle event/writer identities.
- Contract version handshake, `NOT_EXPRESSIBLE` missing-rule record with named/versioned substitute, and deterministic per-bucket sizing-batch shape.
- Semver `0.1.0`, changelog, package README, compatibility tests, and read-only simulator/Bridge consumer source checks.

No Pine, parity, MTC_V2, Bridge runtime, or `06_SCHEMAS` file was modified. No consumer was wired, no threshold chosen, and no trading behaviour was implemented.

## Acceptance-gate self-QA

| Requirement | Evidence | Result |
|---|---|---|
| Versioned independent package | `pyproject.toml`, `__version__`, `CHANGELOG.md` | PASS |
| Exact four sizing methods | enum and compatibility fence | PASS |
| Exactly one matching request constant | four positive fixtures plus mismatch/multiple-field rejections | PASS |
| Reject snapshot/account/bucket/policy/result fields | eight explicit forbidden-field fixtures plus `extra="forbid"` | PASS |
| `SOURCE_DEFINED` provenance only | compiled-native fixture; fifth runtime method rejected | PASS |
| Immutable exact admission sets incl. paper | four admission fixtures plus widening rejection | PASS |
| Full map-#79 vocabularies/shapes | exact freshness/veto/writer enums and reconciliation/window fixtures | PASS |
| Every numerical policy threshold `[OPEN]` | optional threshold fields and fail-closed schema documentation | PASS |
| Simulator and Bridge consumer contracts | AST checks over canonical simulator and Bridge sources, read-only | PASS |
| Deliberate breaking change fails | D026 RED/GREEN transcript below | PASS |
| Built release artifacts | wheel and sdist hashes below | PASS |
| Install from artifact, never path | isolated venv wheel install and neutral-directory import below | PASS |

## Full test and lint output

Commands:

```powershell
& 'C:\tmp\wp_p0_04_tooling_20260825\Scripts\python.exe' -m ruff check .
& 'C:\tmp\wp_p0_04_tooling_20260825\Scripts\python.exe' -m pytest -vv
```

Real output:

```text
All checks passed!
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0 -- C:\tmp\wp_p0_04_tooling_20260825\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\WPP004_20260825\MTC_COMMAND_CENTER\contracts
configfile: pyproject.toml
testpaths: tests
collecting ... collected 41 items

tests/test_compat.py::test_v0_public_compatibility_fence PASSED          [  2%]
tests/test_compat.py::test_handshake_refuses_version_skew_at_the_schema_boundary PASSED [  4%]
tests/test_compat.py::test_not_expressible_source_rule_requires_versioned_named_substitute PASSED [  7%]
tests/test_compat.py::test_every_public_contract_model_emits_json_schema PASSED [  9%]
tests/test_consumers.py::test_simulator_source_retains_the_read_only_contract_projection_seam PASSED [ 12%]
tests/test_consumers.py::test_bridge_source_retains_the_order_projection_and_protection_seams PASSED [ 14%]
tests/test_identity.py::test_identity_formulae_are_deterministic_and_canonicalize_json_key_order PASSED [ 17%]
tests/test_identity.py::test_environment_lineage_is_excluded_from_all_three_hash_formulae PASSED [ 19%]
tests/test_identity.py::test_readable_identity_formulae_pin_their_components PASSED [ 21%]
tests/test_orders_and_package.py::test_authorized_order_has_exact_quantity_and_no_resize_state PASSED [ 24%]
tests/test_orders_and_package.py::test_rejected_order_has_reason_and_no_executable_quantity PASSED [ 26%]
tests/test_orders_and_package.py::test_exit_intent_is_explicitly_reduce_only PASSED [ 29%]
tests/test_orders_and_package.py::test_strategy_package_and_account_snapshot_are_frozen_identity_bound_shapes PASSED [ 31%]
tests/test_risk_admission_execution.py::test_numeric_policy_thresholds_default_open_and_document_fail_closed PASSED [ 34%]
tests/test_risk_admission_execution.py::test_freshness_and_guardian_vocabularies_are_exact PASSED [ 36%]
tests/test_risk_admission_execution.py::test_freshness_event_keeps_open_threshold_explicit PASSED [ 39%]
tests/test_risk_admission_execution.py::test_admission_decisions_name_the_exact_environment_set[SHADOW_ELIGIBLE-environments0] PASSED [ 41%]
tests/test_risk_admission_execution.py::test_admission_decisions_name_the_exact_environment_set[PAPER_ELIGIBLE-environments1] PASSED [ 43%]
tests/test_risk_admission_execution.py::test_admission_decisions_name_the_exact_environment_set[TESTNET_ELIGIBLE-environments2] PASSED [ 46%]
tests/test_risk_admission_execution.py::test_admission_decisions_name_the_exact_environment_set[PROMOTED-environments3] PASSED [ 48%]
tests/test_risk_admission_execution.py::test_no_admission_decision_can_widen_another PASSED [ 51%]
tests/test_risk_admission_execution.py::test_evidence_window_gap_and_three_way_reconciliation_are_identity_scoped PASSED [ 53%]
tests/test_risk_admission_execution.py::test_lifecycle_event_admits_exactly_four_writer_classes PASSED [ 56%]
tests/test_sizing.py::test_each_normalized_method_accepts_exactly_its_request_constant[RISK_AT_STOP-requested_risk_fraction-value0] PASSED [ 58%]
tests/test_sizing.py::test_each_normalized_method_accepts_exactly_its_request_constant[FIXED_QTY-requested_fixed_qty-value1] PASSED [ 60%]
tests/test_sizing.py::test_each_normalized_method_accepts_exactly_its_request_constant[FIXED_NOTIONAL-requested_fixed_notional-value2] PASSED [ 63%]
tests/test_sizing.py::test_each_normalized_method_accepts_exactly_its_request_constant[VOLATILITY_TARGET-vol_target_params-value3] PASSED [ 65%]
tests/test_sizing.py::test_sizing_method_is_exactly_the_four_normalized_values PASSED [ 68%]
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[snapshot_id] PASSED [ 70%]
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[allocation_policy_version] PASSED [ 73%]
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[account_equity] PASSED [ 75%]
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[bucket_capital] PASSED [ 78%]
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[proposed_qty] PASSED [ 80%]
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[authorized_qty] PASSED [ 82%]
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[final_qty] PASSED [ 85%]
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[notional_result] PASSED [ 87%]
tests/test_sizing.py::test_request_field_must_match_method_and_be_the_only_request_value PASSED [ 90%]
tests/test_sizing.py::test_source_defined_is_provenance_only_on_a_compiled_native_request PASSED [ 92%]
tests/test_sizing.py::test_bound_intent_preserves_the_complete_request_and_only_binds_identity PASSED [ 95%]
tests/test_trials_and_eligibility.py::test_trial_record_carries_all_identity_search_gate_and_environment_groups PASSED [ 97%]
tests/test_trials_and_eligibility.py::test_blocked_check_is_distinct_and_names_what_is_missing PASSED [100%]

============================= 41 passed in 0.23s ==============================
```

## D026 deliberate breaking-change proof

Mutation: add `SOURCE_DEFINED = "SOURCE_DEFINED"` as a fifth runtime member of `SizingMethod`. This reproduces the exact contract break forbidden by the amended §5.4/§5.5 rule. The mutation was applied to production source, tested, and then removed.

RED command:

```powershell
python -m pytest tests/test_compat.py::test_v0_public_compatibility_fence -q
```

RED real output:

```text
F                                                                        [100%]
================================== FAILURES ===================================
_____________________ test_v0_public_compatibility_fence ______________________

    def test_v0_public_compatibility_fence():
        assert CONTRACT_VERSION == __version__ == "0.1.0"
>       assert tuple(item.value for item in SizingMethod) == (
            "RISK_AT_STOP",
            "FIXED_QTY",
            "FIXED_NOTIONAL",
            "VOLATILITY_TARGET",
        )
E       AssertionError: assert ('RISK_AT_STO...URCE_DEFINED') == ('RISK_AT_STO...ILITY_TARGET')
E         Left contains one more item: 'SOURCE_DEFINED'

tests\test_compat.py:17: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_compat.py::test_v0_public_compatibility_fence - AssertionEr...
1 failed in 0.34s
```

GREEN command after removing the mutation:

```powershell
python -m pytest tests/test_compat.py::test_v0_public_compatibility_fence -q
```

GREEN real output:

```text
.                                                                        [100%]
1 passed in 0.17s
```

Classification: verified D026 closure evidence, not supplemental. The compatibility fence discriminates on the public enum itself, not on an unrelated string or return code.

## Build and artifact-only installation proof

Build command:

```powershell
& 'C:\tmp\wp_p0_04_tooling_20260825\Scripts\python.exe' -m build --outdir 'C:\tmp\wp_p0_04_artifacts_20260825' .
```

Result: `Successfully built mtc_contracts-0.1.0.tar.gz and mtc_contracts-0.1.0-py3-none-any.whl`.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `mtc_contracts-0.1.0-py3-none-any.whl` | 17,366 | `17D349D10E0B7FC030D4592BBF00FAD9269821F1FC90AFDB0958E75B07FB5136` |
| `mtc_contracts-0.1.0.tar.gz` | 20,629 | `355DCF4DA8758C8F173B59D02E521B3AD7F6625F34ECB5D8FBCC7388D08A083C` |

Install command (wheel artifact only; no source-path install):

```powershell
python -m venv 'C:\tmp\wp_p0_04_install_20260825'
& 'C:\tmp\wp_p0_04_install_20260825\Scripts\python.exe' -m pip install --force-reinstall 'C:\tmp\wp_p0_04_artifacts_20260825\mtc_contracts-0.1.0-py3-none-any.whl'
```

Neutral-directory import command (`workdir=C:\tmp`, preventing source-tree shadowing):

```powershell
& 'C:\tmp\wp_p0_04_install_20260825\Scripts\python.exe' -c "import mtc_contracts; from mtc_contracts import RiskBucket, TrialRecord; print('version='+mtc_contracts.__version__); print('module='+mtc_contracts.__file__); print('risk_fields='+','.join(RiskBucket.model_fields)); print('trial_has_modules_enabled_count='+str('modules_enabled_count' in TrialRecord.model_fields))"
```

Real output:

```text
version=0.1.0
module=C:\tmp\wp_p0_04_install_20260825\Lib\site-packages\mtc_contracts\__init__.py
risk_fields=contract_version,bucket_id,allocation_policy_version,capital_allocation,max_gross_exposure,max_bucket_leverage,max_daily_loss,max_drawdown,max_concurrent,correlation_cap,session_rule,evaluation_cadence,members,venue_binding
trial_has_modules_enabled_count=True
```

Artifacts and temporary venvs remain under `C:\tmp`; they are not staged or committed.

## Dependency and licence ledger input

No dependency was added to the repository outside `MTC_COMMAND_CENTER/contracts/pyproject.toml`. Metadata below was read from the dedicated tooling/install venv after installation.

### Runtime

| Dependency | Installed/proved version | Licence |
|---|---:|---|
| `pydantic` | 2.13.4 | MIT |
| `pydantic-core` (transitive) | 2.46.4 | MIT |
| `annotated-types` (transitive) | 0.8.0 | MIT |
| `typing-extensions` (transitive) | 4.16.0 | PSF-2.0 |
| `typing-inspection` (transitive) | 0.4.4 | MIT |

### Local build/test tooling

| Dependency | Installed/proved version | Licence |
|---|---:|---|
| `build` | 1.5.0 | MIT |
| `pytest` | 9.1.1 | MIT |
| `ruff` | 0.16.4 | MIT |
| `setuptools` | 84.0.0 | MIT |
| `wheel` | 0.48.0 | MIT |
| `pip` | 26.2.1 | MIT |
| `packaging` (transitive) | 26.3 | Apache-2.0 OR BSD-2-Clause |
| `pyproject-hooks` (transitive) | 1.2.0 | MIT |
| `iniconfig` (transitive) | 2.3.0 | MIT |
| `pluggy` (transitive) | 1.6.0 | MIT |
| `Pygments` (transitive) | 2.21.0 | BSD-2-Clause |
| `colorama` (transitive) | 0.4.6 | BSD |

## Exact staged files

Package commit `2c37b42db03cdec675f426f5956ec33f97685ebd` staged exactly these 23 files:

```text
MTC_COMMAND_CENTER/contracts/.gitignore
MTC_COMMAND_CENTER/contracts/CHANGELOG.md
MTC_COMMAND_CENTER/contracts/README.md
MTC_COMMAND_CENTER/contracts/mtc_contracts/__init__.py
MTC_COMMAND_CENTER/contracts/mtc_contracts/admission.py
MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py
MTC_COMMAND_CENTER/contracts/mtc_contracts/execution.py
MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py
MTC_COMMAND_CENTER/contracts/mtc_contracts/lineage.py
MTC_COMMAND_CENTER/contracts/mtc_contracts/orders.py
MTC_COMMAND_CENTER/contracts/mtc_contracts/package.py
MTC_COMMAND_CENTER/contracts/mtc_contracts/protocol.py
MTC_COMMAND_CENTER/contracts/mtc_contracts/risk.py
MTC_COMMAND_CENTER/contracts/mtc_contracts/sizing.py
MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py
MTC_COMMAND_CENTER/contracts/pyproject.toml
MTC_COMMAND_CENTER/contracts/tests/test_compat.py
MTC_COMMAND_CENTER/contracts/tests/test_consumers.py
MTC_COMMAND_CENTER/contracts/tests/test_identity.py
MTC_COMMAND_CENTER/contracts/tests/test_orders_and_package.py
MTC_COMMAND_CENTER/contracts/tests/test_risk_admission_execution.py
MTC_COMMAND_CENTER/contracts/tests/test_sizing.py
MTC_COMMAND_CENTER/contracts/tests/test_trials_and_eligibility.py
```

The report commit stages only this `LANE_REPORT.md`. Its SHA cannot be embedded in its own bytes; it is printed in the lane handoff immediately after commit.

## Open issues / Lead actions

1. The Claude Fable Lead must perform the independent T1 Gate-5 inspection and acceptance; the implementer has not self-accepted the package.
2. The Lead must reconcile the isolated lane with the three newer `origin/master` commits before integration. No merge, rebase, push, or release tag was attempted here.
3. All numeric policy/freshness/window thresholds deliberately remain `[OPEN]`; downstream consumers must fail closed when unset.
4. Consumer wiring, allocator/Guardian enforcement, lifecycle storage, admission authority, and Bridge/runtime changes remain downstream packages and are not part of this schema-only delivery.
5. No package release was pushed. The locally built `0.1.0` wheel/sdist prove buildability and artifact-only installation; release publication belongs to Lead/owner sequencing.

## Repair round 1 - 2026-08-25

### Scope and disposition

Audit tier remains **T1**; this is repair round 1 of the maximum 2. All four
Lead-reproduced required findings are repaired:

1. `ContractModel` now detaches and recursively freezes mappings, sequences and
   sets after validation. The universal base applies to every public contract;
   behavioral tests exercise every contract type that can retain an arbitrary or
   dictionary payload: `StrategyPackage`, `AccountSnapshot`,
   `VolatilityTargetParams`, `TrialRecord`, and `EligibilityCheckResult`. JSON
   serialization and validation round-trip remain supported.
2. `EnvironmentLineage` is required on `EvidenceWindow`, `EvidenceGapRecord`,
   `ReconciliationRecord`, and the swept individual `EligibilityCheckResult`.
   The other evidence artifacts already carried it: `EvidenceIdentity`,
   `EligibilityVerdictSet`, `AdmissionDecision`, `TrialRecord`, and
   `ArtifactManifest`.
3. The lineage-exclusion test now calls each real hash function with its complete
   valid argument set and two different lineage values. The three cases are
   independently parameterized so a mutation to any one preimage is detected.
4. Every direct runtime/test/build dependency is exact-pinned with `==` in
   `pyproject.toml`. `constraints.txt` pins the complete recorded direct and
   transitive environment, is consumed by the documented install commands, and
   is included in the sdist through `MANIFEST.in`.

No Pine, parity, MTC_V2, Bridge runtime, `06_SCHEMAS`, trading logic, threshold,
or consumer-wiring surface was changed.

### D026 - deep-immutability RED/GREEN

The exact pre-fix source was copied to
`C:\tmp\wp_p0_04_repair_r1_prefix_20260825_001`; the final regression-test bytes
were run against that temporary copy.

RED command:

```powershell
Set-Location C:\tmp\wp_p0_04_repair_r1_prefix_20260825_001
& C:\tmp\wp_p0_04_tooling_20260825\Scripts\python.exe -m pytest -q --tb=line tests/test_deep_immutability.py
```

RED real output:

```text
FF                                                                       [100%]
================================== FAILURES ===================================
E   AssertionError: assert ['breakout', ...ias-mutation'] == ('breakout',)

      Left contains one more item: 'source-alias-mutation'
      Use -v to get more diff
C:\tmp\wp_p0_04_repair_r1_prefix_20260825_001\tests\test_deep_immutability.py:68: AssertionError: assert ['breakout', ...ias-mutation'] == ('breakout',)
E   Failed: DID NOT RAISE any of (AttributeError, TypeError)
C:\tmp\wp_p0_04_repair_r1_prefix_20260825_001\tests\test_deep_immutability.py:130: Failed: DID NOT RAISE any of (AttributeError, TypeError)
=========================== short test summary info ===========================
FAILED tests/test_deep_immutability.py::test_strategy_package_account_snapshot_and_volatility_params_are_deeply_immutable
FAILED tests/test_deep_immutability.py::test_trial_and_check_arbitrary_payload_containers_are_deeply_immutable
2 failed in 0.14s
```

GREEN command on repaired source:

```powershell
& C:\tmp\wp_p0_04_tooling_20260825\Scripts\python.exe -m pytest -q --tb=line tests/test_deep_immutability.py
```

GREEN real output:

```text
..                                                                       [100%]
2 passed in 0.11s
```

Classification: verified D026 closure evidence. The tests mutate the actual
stored nested containers and also mutate a caller-owned input after construction;
they do not discriminate on a string literal or unrelated exception.

### Required evidence-lineage RED/GREEN

The final lineage tests were also executed against the exact pre-fix temporary
copy above.

RED command:

```powershell
& C:\tmp\wp_p0_04_tooling_20260825\Scripts\python.exe -m pytest -q --tb=line tests/test_risk_admission_execution.py::test_evidence_window_gap_and_three_way_reconciliation_are_identity_scoped tests/test_risk_admission_execution.py::test_execution_evidence_records_require_environment_lineage tests/test_trials_and_eligibility.py::test_eligibility_check_result_requires_its_own_environment_lineage
```

RED real output:

```text
FFFFF                                                                    [100%]
================================== FAILURES ===================================
E   pydantic_core._pydantic_core.ValidationError: 1 validation error for EvidenceWindow
    environment_lineage
      Extra inputs are not permitted [type=extra_forbidden, input_value=EnvironmentLineage(contra...uite_bit_identical=True), input_type=EnvironmentLineage]
        For further information visit https://errors.pydantic.dev/2.13/v/extra_forbidden
C:\tmp\wp_p0_04_repair_r1_prefix_20260825_001\tests\test_risk_admission_execution.py:148: pydantic_core._pydantic_core.ValidationError: 1 validation error for EvidenceWindow
E   Failed: DID NOT RAISE ValidationError
C:\tmp\wp_p0_04_repair_r1_prefix_20260825_001\tests\test_risk_admission_execution.py:241: Failed: DID NOT RAISE ValidationError
E   Failed: DID NOT RAISE ValidationError
C:\tmp\wp_p0_04_repair_r1_prefix_20260825_001\tests\test_risk_admission_execution.py:241: Failed: DID NOT RAISE ValidationError
E   Failed: DID NOT RAISE ValidationError
C:\tmp\wp_p0_04_repair_r1_prefix_20260825_001\tests\test_risk_admission_execution.py:241: Failed: DID NOT RAISE ValidationError
E   Failed: DID NOT RAISE ValidationError
C:\tmp\wp_p0_04_repair_r1_prefix_20260825_001\tests\test_trials_and_eligibility.py:90: Failed: DID NOT RAISE ValidationError
=========================== short test summary info ===========================
FAILED tests/test_risk_admission_execution.py::test_evidence_window_gap_and_three_way_reconciliation_are_identity_scoped
FAILED tests/test_risk_admission_execution.py::test_execution_evidence_records_require_environment_lineage[EvidenceWindow-payload0]
FAILED tests/test_risk_admission_execution.py::test_execution_evidence_records_require_environment_lineage[EvidenceGapRecord-payload1]
FAILED tests/test_risk_admission_execution.py::test_execution_evidence_records_require_environment_lineage[ReconciliationRecord-payload2]
FAILED tests/test_trials_and_eligibility.py::test_eligibility_check_result_requires_its_own_environment_lineage
5 failed in 0.12s
```

GREEN command on repaired source: identical test selection.

GREEN real output:

```text
.....                                                                    [100%]
5 passed in 0.12s
```

### D026 - discriminating identity-exclusion RED/GREEN

The repaired package and final test were copied to
`C:\tmp\wp_p0_04_repair_r1_identity_mutant_20260825_001`. In that temporary
copy only, the auditor's mutation was applied: `environment_lineage` was added
to the named preimage passed to `_hash_named_parts` in each of the three hash
functions.

RED command:

```powershell
Set-Location C:\tmp\wp_p0_04_repair_r1_identity_mutant_20260825_001
& C:\tmp\wp_p0_04_tooling_20260825\Scripts\python.exe -m pytest -q --tb=line tests/test_identity.py::test_environment_lineage_is_excluded_from_all_three_hash_formulae
```

RED real output:

```text
FFF                                                                      [100%]
================================== FAILURES ===================================
E   AssertionError: assert '5d39a65a5160...326f669694ddf' == '5a7a65e05c9b...2a8e09f1f6f4d'

      - 5a7a65e05c9b35eb7f52e3160c70906a1031133c92d4e9f09a32a8e09f1f6f4d
      + 5d39a65a516022adde5c6843e2080ca69fbd456e5638fbae72c326f669694ddf
C:\tmp\wp_p0_04_repair_r1_identity_mutant_20260825_001\tests\test_identity.py:99: AssertionError: assert '5d39a65a5160...326f669694ddf' == '5a7a65e05c9b...2a8e09f1f6f4d'
E   AssertionError: assert '4227818b1d2f...7e901a77b2dc9' == 'e8698dddb02c...94e1ecabc31e2'

      - e8698dddb02ce4e5e8db60465ec9620cafe2840b409a1f58e0294e1ecabc31e2
      + 4227818b1d2f19c7ad1cce1f68238bb1e692d89756a08a7ffce7e901a77b2dc9
C:\tmp\wp_p0_04_repair_r1_identity_mutant_20260825_001\tests\test_identity.py:99: AssertionError: assert '4227818b1d2f...7e901a77b2dc9' == 'e8698dddb02c...94e1ecabc31e2'
E   AssertionError: assert '66861f4ef42c...623c641b812a9' == '85191b876a49...71c8d32b49135'

      - 85191b876a49405a533a4fb5e9e6836d7db4a67c264c4ab4e1571c8d32b49135
      + 66861f4ef42c03aa203f7bb325b90acd4b02e1729eac9d9d651623c641b812a9
C:\tmp\wp_p0_04_repair_r1_identity_mutant_20260825_001\tests\test_identity.py:99: AssertionError: assert '66861f4ef42c...623c641b812a9' == '85191b876a49...71c8d32b49135'
=========================== short test summary info ===========================
FAILED tests/test_identity.py::test_environment_lineage_is_excluded_from_all_three_hash_formulae[package]
FAILED tests/test_identity.py::test_environment_lineage_is_excluded_from_all_three_hash_formulae[evaluation]
FAILED tests/test_identity.py::test_environment_lineage_is_excluded_from_all_three_hash_formulae[deployment]
3 failed in 0.13s
```

GREEN command on real repaired source: identical test selection.

GREEN real output:

```text
...                                                                      [100%]
3 passed in 0.12s
```

Classification: verified D026 closure evidence for all three formulae. Each
call supplies every required semantic argument; the only varied value is the
environment lineage.

### Exact dependency enforcement

Direct pins enforced in `pyproject.toml`:

```text
setuptools==84.0.0
wheel==0.48.0
pydantic==2.13.4
pytest==9.1.1
ruff==0.16.4
build==1.5.0
```

`constraints.txt` additionally exact-pins the recorded transitive set:
`pydantic-core==2.46.4`, `annotated-types==0.8.0`,
`typing-extensions==4.16.0`, `typing-inspection==0.4.4`,
`packaging==26.3`, `pyproject-hooks==1.2.0`, `iniconfig==2.3.0`,
`pluggy==1.6.0`, `Pygments==2.21.0`, `colorama==0.4.6`, and
`pip==26.2.1`, plus the project itself at `0.1.0`. The compatibility suite
checks that every direct declaration is an exact pin and is covered by the
constraints file.

Pinned-tooling install and integrity output:

```text
Requirement already satisfied: pip==26.2.1
Requirement already satisfied: build==1.5.0
Requirement already satisfied: pytest==9.1.1
Requirement already satisfied: ruff==0.16.4
Requirement already satisfied: setuptools==84.0.0
Requirement already satisfied: wheel==0.48.0
No broken requirements found.
```

### Final lint and full-suite output

Commands:

```powershell
& C:\tmp\wp_p0_04_tooling_20260825\Scripts\python.exe -m ruff check .
& C:\tmp\wp_p0_04_tooling_20260825\Scripts\python.exe -m pytest -vv
```

Real output:

```text
All checks passed!
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0 -- C:\tmp\wp_p0_04_tooling_20260825\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\WPP004_20260825\MTC_COMMAND_CENTER\contracts
configfile: pyproject.toml
testpaths: tests
collecting ... collected 50 items

tests/test_compat.py::test_v0_public_compatibility_fence PASSED
tests/test_compat.py::test_handshake_refuses_version_skew_at_the_schema_boundary PASSED
tests/test_compat.py::test_not_expressible_source_rule_requires_versioned_named_substitute PASSED
tests/test_compat.py::test_every_public_contract_model_emits_json_schema PASSED
tests/test_compat.py::test_all_direct_dependencies_are_exact_pins_covered_by_constraints PASSED
tests/test_consumers.py::test_simulator_source_retains_the_read_only_contract_projection_seam PASSED
tests/test_consumers.py::test_bridge_source_retains_the_order_projection_and_protection_seams PASSED
tests/test_deep_immutability.py::test_strategy_package_account_snapshot_and_volatility_params_are_deeply_immutable PASSED
tests/test_deep_immutability.py::test_trial_and_check_arbitrary_payload_containers_are_deeply_immutable PASSED
tests/test_identity.py::test_identity_formulae_are_deterministic_and_canonicalize_json_key_order PASSED
tests/test_identity.py::test_environment_lineage_is_excluded_from_all_three_hash_formulae[package] PASSED
tests/test_identity.py::test_environment_lineage_is_excluded_from_all_three_hash_formulae[evaluation] PASSED
tests/test_identity.py::test_environment_lineage_is_excluded_from_all_three_hash_formulae[deployment] PASSED
tests/test_identity.py::test_readable_identity_formulae_pin_their_components PASSED
tests/test_orders_and_package.py::test_authorized_order_has_exact_quantity_and_no_resize_state PASSED
tests/test_orders_and_package.py::test_rejected_order_has_reason_and_no_executable_quantity PASSED
tests/test_orders_and_package.py::test_exit_intent_is_explicitly_reduce_only PASSED
tests/test_orders_and_package.py::test_strategy_package_and_account_snapshot_are_frozen_identity_bound_shapes PASSED
tests/test_risk_admission_execution.py::test_numeric_policy_thresholds_default_open_and_document_fail_closed PASSED
tests/test_risk_admission_execution.py::test_freshness_and_guardian_vocabularies_are_exact PASSED
tests/test_risk_admission_execution.py::test_freshness_event_keeps_open_threshold_explicit PASSED
tests/test_risk_admission_execution.py::test_admission_decisions_name_the_exact_environment_set[SHADOW_ELIGIBLE-environments0] PASSED
tests/test_risk_admission_execution.py::test_admission_decisions_name_the_exact_environment_set[PAPER_ELIGIBLE-environments1] PASSED
tests/test_risk_admission_execution.py::test_admission_decisions_name_the_exact_environment_set[TESTNET_ELIGIBLE-environments2] PASSED
tests/test_risk_admission_execution.py::test_admission_decisions_name_the_exact_environment_set[PROMOTED-environments3] PASSED
tests/test_risk_admission_execution.py::test_no_admission_decision_can_widen_another PASSED
tests/test_risk_admission_execution.py::test_evidence_window_gap_and_three_way_reconciliation_are_identity_scoped PASSED
tests/test_risk_admission_execution.py::test_execution_evidence_records_require_environment_lineage[EvidenceWindow-payload0] PASSED
tests/test_risk_admission_execution.py::test_execution_evidence_records_require_environment_lineage[EvidenceGapRecord-payload1] PASSED
tests/test_risk_admission_execution.py::test_execution_evidence_records_require_environment_lineage[ReconciliationRecord-payload2] PASSED
tests/test_risk_admission_execution.py::test_lifecycle_event_admits_exactly_four_writer_classes PASSED
tests/test_sizing.py::test_each_normalized_method_accepts_exactly_its_request_constant[RISK_AT_STOP-requested_risk_fraction-value0] PASSED
tests/test_sizing.py::test_each_normalized_method_accepts_exactly_its_request_constant[FIXED_QTY-requested_fixed_qty-value1] PASSED
tests/test_sizing.py::test_each_normalized_method_accepts_exactly_its_request_constant[FIXED_NOTIONAL-requested_fixed_notional-value2] PASSED
tests/test_sizing.py::test_each_normalized_method_accepts_exactly_its_request_constant[VOLATILITY_TARGET-vol_target_params-value3] PASSED
tests/test_sizing.py::test_sizing_method_is_exactly_the_four_normalized_values PASSED
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[snapshot_id] PASSED
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[allocation_policy_version] PASSED
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[account_equity] PASSED
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[bucket_capital] PASSED
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[proposed_qty] PASSED
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[authorized_qty] PASSED
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[final_qty] PASSED
tests/test_sizing.py::test_snapshot_account_and_result_fields_are_rejected[notional_result] PASSED
tests/test_sizing.py::test_request_field_must_match_method_and_be_the_only_request_value PASSED
tests/test_sizing.py::test_source_defined_is_provenance_only_on_a_compiled_native_request PASSED
tests/test_sizing.py::test_bound_intent_preserves_the_complete_request_and_only_binds_identity PASSED
tests/test_trials_and_eligibility.py::test_trial_record_carries_all_identity_search_gate_and_environment_groups PASSED
tests/test_trials_and_eligibility.py::test_blocked_check_is_distinct_and_names_what_is_missing PASSED
tests/test_trials_and_eligibility.py::test_eligibility_check_result_requires_its_own_environment_lineage PASSED

============================= 50 passed in 0.21s ==============================
```

### Final rebuild and artifact-only installation

Build command:

```powershell
& C:\tmp\wp_p0_04_tooling_20260825\Scripts\python.exe -m build --no-isolation --outdir C:\tmp\wp_p0_04_repair_r1_artifacts_20260825_003 .
```

Real result:

```text
Successfully built mtc_contracts-0.1.0.tar.gz and mtc_contracts-0.1.0-py3-none-any.whl
mtc_contracts-0.1.0/CHANGELOG.md
mtc_contracts-0.1.0/constraints.txt
```

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `mtc_contracts-0.1.0-py3-none-any.whl` | 18,153 | `3F61CF2135D569DA234B1980A619EC510D6C183C5384B6C8A147B5D630F97F60` |
| `mtc_contracts-0.1.0.tar.gz` | 24,299 | `C966D6FB03ABB160BC5D9E9363D5B2F20E4AD7EB4734B2110BC0703EC4BBDCAF` |

Final artifact-only install used fresh venv
`C:\tmp\wp_p0_04_repair_r1_install_20260825_002`, exact constraints, and the
wheel above; the import check ran from neutral directory `C:\tmp`.

```text
Successfully installed annotated-types-0.8.0 mtc-contracts-0.1.0 pydantic-2.13.4 pydantic-core-2.46.4 typing-extensions-4.16.0 typing-inspection-0.4.4
No broken requirements found.
version=0.1.0
module=C:\tmp\wp_p0_04_repair_r1_install_20260825_002\Lib\site-packages\mtc_contracts\__init__.py
nested_mutation=RAISED
evidence_lineage_required=True
```

### Repair-round exact staged paths

The repair commit stages exactly these paths (verified with
`git diff --cached --name-only` before commit):

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_04_CONTRACTS_2026-08-25/LANE_REPORT.md
MTC_COMMAND_CENTER/contracts/CHANGELOG.md
MTC_COMMAND_CENTER/contracts/MANIFEST.in
MTC_COMMAND_CENTER/contracts/README.md
MTC_COMMAND_CENTER/contracts/constraints.txt
MTC_COMMAND_CENTER/contracts/mtc_contracts/admission.py
MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py
MTC_COMMAND_CENTER/contracts/mtc_contracts/execution.py
MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py
MTC_COMMAND_CENTER/contracts/pyproject.toml
MTC_COMMAND_CENTER/contracts/tests/test_compat.py
MTC_COMMAND_CENTER/contracts/tests/test_deep_immutability.py
MTC_COMMAND_CENTER/contracts/tests/test_identity.py
MTC_COMMAND_CENTER/contracts/tests/test_risk_admission_execution.py
MTC_COMMAND_CENTER/contracts/tests/test_trials_and_eligibility.py
```

Repair commit SHA is printed in the implementer handoff after commit because a
commit cannot contain its own SHA. No push, merge, rebase, tag, or release was
performed. The Claude Fable Lead retains T1 round-2 acceptance and integration
authority.
