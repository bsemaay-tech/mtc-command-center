from datetime import date

import pytest

from mtc_contracts import (
    compute_deployment_identity_hash,
    compute_evaluation_run_hash,
    compute_family_id,
    compute_package_hash,
    make_candidate_id,
    make_run_id,
    make_trial_id,
)


def test_identity_formulae_are_deterministic_and_canonicalize_json_key_order():
    first = compute_package_hash(
        spec_json={"z": 2, "a": 1},
        kernel_code_sha="1" * 64,
        exact_params_json={"period": 20, "enabled": True},
        modules_enabled_json=["stop", "target"],
        substitute_catalogue_versions_json={"missing-risk": "1.0.0"},
        instrument_metadata_json={"symbol": "BTCUSDT", "tick": "0.10"},
    )
    second = compute_package_hash(
        spec_json={"a": 1, "z": 2},
        kernel_code_sha="1" * 64,
        exact_params_json={"enabled": True, "period": 20},
        modules_enabled_json=["stop", "target"],
        substitute_catalogue_versions_json={"missing-risk": "1.0.0"},
        instrument_metadata_json={"tick": "0.10", "symbol": "BTCUSDT"},
    )
    assert first == second
    assert len(first) == 64


@pytest.mark.parametrize(
    ("function", "identity_args"),
    [
        (
            compute_package_hash,
            {
                "spec_json": {},
                "kernel_code_sha": "1" * 64,
                "exact_params_json": {},
                "modules_enabled_json": [],
                "substitute_catalogue_versions_json": {},
                "instrument_metadata_json": {},
            },
        ),
        (
            compute_evaluation_run_hash,
            {
                "package_hash": "2" * 64,
                "dataset_manifest_sha": "3" * 64,
                "cost_model_json": {},
                "simulator_class": "CANONICAL",
                "simulator_version": "1",
                "evaluation_config_json": {},
            },
        ),
        (
            compute_deployment_identity_hash,
            {
                "package_hash": "2" * 64,
                "allocator_code_sha": "4" * 64,
                "allocation_policy_version": "allocation-v1",
                "guardian_code_sha": "5" * 64,
                "guardian_policy_json": {},
                "risk_bucket_policy_json": {},
                "economic_policy_json": {},
                "runtime_policy_json": {},
                "protection_semantics_json": {},
                "broker_adapter_id": "adapter",
                "broker_adapter_version": "1",
                "cost_lineage_json": {},
            },
        ),
    ],
    ids=("package", "evaluation", "deployment"),
)
def test_environment_lineage_is_excluded_from_all_three_hash_formulae(
    function, identity_args
):
    windows_lineage = {
        "python_version": "3.14.2",
        "dependency_lockfile_hash": "a" * 64,
        "os_name": "Windows",
        "os_version": "11",
    }
    linux_lineage = {
        "python_version": "3.14.2",
        "dependency_lockfile_hash": "b" * 64,
        "os_name": "Linux",
        "os_version": "6.8",
    }
    windows_hash = function(**identity_args, environment_lineage=windows_lineage)
    linux_hash = function(**identity_args, environment_lineage=linux_lineage)
    assert windows_hash == linux_hash
    assert len(windows_hash) == 64


def test_readable_identity_formulae_pin_their_components():
    candidate = make_candidate_id(date(2026, 8, 24), {"source": "transcript-7"})
    family = compute_family_id(
        source_provenance={"source": "transcript-7"},
        producer="normalizer-v2",
        parameter_neighbourhood={"period": [18, 22]},
    )
    assert candidate.startswith("QLC-20260824-")
    assert family.startswith("FAM-")
    assert make_trial_id("a" * 64, "b" * 64, 7) == f"{'a' * 64}.{'b' * 64}.7"
    assert make_run_id("c" * 64, "FORWARD_SHADOW", 2) == f"{'c' * 64}.FORWARD_SHADOW.2"
