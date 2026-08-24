from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from mtc_contracts import (
    EligibilityCheckResult,
    EligibilityState,
    EligibilityVerdictSet,
    EnvironmentLineage,
    TrialRecord,
    VerdictOutcome,
)


def lineage():
    return EnvironmentLineage(
        python_version="3.14.2",
        dependency_lockfile_hash="1" * 64,
        os_name="Windows",
        os_version="11",
        golden_suite_hash="2" * 64,
        golden_suite_bit_identical=True,
    )


def test_trial_record_carries_all_identity_search_gate_and_environment_groups():
    trial = TrialRecord(
        run_id=f"{'3' * 64}.RESEARCH.1",
        candidate_id="QLC-20260824-1234abcd",
        package_hash="4" * 64,
        deployment_identity_hash="5" * 64,
        evaluation_run_hash="6" * 64,
        family_id="FAM-1234abcd1234abcd",
        trial_id=f"{'6' * 64}.{'7' * 64}.1",
        param_hash="7" * 64,
        exit_mode="fixed_2R",
        search_regime="grid",
        preregistered_space_hash="8" * 64,
        trial_index_in_family=1,
        family_size=10,
        parameters={"period": 20},
        modules_enabled=["stop", "target"],
        modules_enabled_count=2,
        fold_test_returns=[1.0, -0.5],
        fold_test_sharpes=[0.4, -0.1],
        fold_test_trades=[12, 9],
        rejection_reasons=[],
        classification="PASS",
        simulator_class="CANONICAL",
        unsimulated_controls_hash="9" * 64,
        environment_lineage=lineage(),
    )
    assert trial.deployment_identity_hash == "5" * 64
    assert trial.environment_lineage.os_name == "Windows"


def test_blocked_check_is_distinct_and_names_what_is_missing():
    check = EligibilityCheckResult(
        check_id="data-quality-gap-ratio",
        threshold=None,
        measured_value=None,
        outcome="BLOCKED",
        dataset_hash="a" * 64,
        deployment_identity_hash="b" * 64,
        timestamp=datetime(2026, 8, 24, tzinfo=UTC),
        blocked_reason="gap threshold is [OPEN]",
        environment_lineage=lineage(),
    )
    verdict = EligibilityVerdictSet(
        verdict_set_id="verdict-set-1",
        target_state="SHADOW_ELIGIBLE",
        check_set_version="checks-v1",
        candidate_id="QLC-20260824-1234abcd",
        package_hash="c" * 64,
        deployment_identity_hash="b" * 64,
        evaluation_run_hash="d" * 64,
        results=[check],
        outcome="BLOCKED",
        timestamp=datetime(2026, 8, 24, tzinfo=UTC),
        issuer="eligibility-engine",
        environment_lineage=lineage(),
    )
    assert check.outcome is VerdictOutcome.BLOCKED
    assert verdict.target_state is EligibilityState.SHADOW_ELIGIBLE
    assert verdict.outcome is VerdictOutcome.BLOCKED


def test_eligibility_check_result_requires_its_own_environment_lineage():
    with pytest.raises(ValidationError):
        EligibilityCheckResult(
            check_id="data-quality-gap-ratio",
            threshold=None,
            measured_value=None,
            outcome="BLOCKED",
            dataset_hash="a" * 64,
            deployment_identity_hash="b" * 64,
            timestamp=datetime(2026, 8, 24, tzinfo=UTC),
            blocked_reason="gap threshold is [OPEN]",
        )
