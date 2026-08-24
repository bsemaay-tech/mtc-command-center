from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from mtc_contracts import (
    AdmissionDecision,
    AdmissionDecisionType,
    AllocationPolicy,
    Environment,
    EnvironmentLineage,
    EvidenceGapRecord,
    EvidenceWindow,
    FreshnessEvent,
    FreshnessState,
    GuardianPolicy,
    GuardianVetoClass,
    LifecycleEvent,
    LifecycleWriterClass,
    ReconciliationMode,
    ReconciliationRecord,
    RiskBucket,
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


def test_numeric_policy_thresholds_default_open_and_document_fail_closed():
    bucket = RiskBucket(bucket_id="bucket-1", allocation_policy_version="allocation-v1")
    policy = AllocationPolicy(version="allocation-v1", bucket_ids=["bucket-1"])
    guardian = GuardianPolicy(version="guardian-v1", threshold_source_version="risk-v1")
    assert bucket.capital_allocation is None
    assert policy.max_total_exposure is None
    assert guardian.repeated_veto_flap_threshold is None
    for model in (RiskBucket, AllocationPolicy, GuardianPolicy):
        assert "fail-closed" in (model.__doc__ or "").lower()


def test_freshness_and_guardian_vocabularies_are_exact():
    assert {state.value for state in FreshnessState} == {
        "FRESH",
        "AGING",
        "STALE",
        "UNKNOWN",
        "DRIFT",
        "DEGRADED",
        "RECOVERING",
    }
    assert {veto.value for veto in GuardianVetoClass} == {
        "BUCKET_CAP",
        "CORRELATION",
        "STALENESS",
        "VENUE_STATE",
        "DAILY_LOSS",
        "PROTECTION_UNPLACEABLE",
        "POLICY_ERROR",
    }


def test_freshness_event_keeps_open_threshold_explicit():
    event = FreshnessEvent(
        domain="MARKET",
        state="UNKNOWN",
        observed_at=datetime(2026, 8, 24, tzinfo=UTC),
        source_timestamp=None,
        age_ms=None,
        freshness_threshold_ms=None,
        worker_id="worker-1",
        environment="FORWARD_SHADOW",
    )
    assert event.freshness_threshold_ms is None
    assert "fail-closed" in (FreshnessEvent.__doc__ or "").lower()


@pytest.mark.parametrize(
    ("decision", "environments"),
    [
        ("SHADOW_ELIGIBLE", ["FORWARD_SHADOW"]),
        ("PAPER_ELIGIBLE", ["INTERNAL_PAPER"]),
        ("TESTNET_ELIGIBLE", ["INTERNAL_PAPER", "EXCHANGE_TESTNET"]),
        ("PROMOTED", ["MAINNET", "LIMITED_LIVE"]),
    ],
)
def test_admission_decisions_name_the_exact_environment_set(decision, environments):
    record = AdmissionDecision(
        decision_id="decision-1",
        candidate_id="QLC-20260824-1234abcd",
        package_hash="3" * 64,
        deployment_identity_hash="4" * 64,
        authority="PROMOTION" if decision == "PROMOTED" else "ENVIRONMENT_ADMISSION",
        decision=decision,
        admits_to_environments=environments,
        reason="all frozen checks passed",
        evidence_references=["evidence://verdict-1"],
        eligibility_verdict_set_id="verdict-set-1",
        leakage_record_id=None,
        simulator_class="CANONICAL",
        unsimulated_controls_hash="5" * 64,
        timestamp=datetime(2026, 8, 24, tzinfo=UTC),
        approver="automatic-authority",
        previous_state="TRIAGED",
        new_state=decision,
        check_set_version="checks-v1",
        environment_lineage=lineage(),
    )
    assert record.decision is AdmissionDecisionType(decision)
    assert set(record.admits_to_environments) == {
        Environment(item) for item in environments
    }


def test_no_admission_decision_can_widen_another():
    with pytest.raises(ValidationError):
        AdmissionDecision.model_validate(
            {
                "decision_id": "decision-1",
                "candidate_id": "QLC-20260824-1234abcd",
                "package_hash": "3" * 64,
                "deployment_identity_hash": "4" * 64,
                "authority": "ENVIRONMENT_ADMISSION",
                "decision": "PAPER_ELIGIBLE",
                "admits_to_environments": ["INTERNAL_PAPER", "EXCHANGE_TESTNET"],
                "reason": "invalid widening",
                "evidence_references": ["evidence://verdict-1"],
                "eligibility_verdict_set_id": "verdict-set-1",
                "simulator_class": "CANONICAL",
                "unsimulated_controls_hash": "5" * 64,
                "timestamp": datetime(2026, 8, 24, tzinfo=UTC),
                "approver": "automatic-authority",
                "previous_state": "TRIAGED",
                "new_state": "PAPER_ELIGIBLE",
                "check_set_version": "checks-v1",
                "environment_lineage": lineage().model_dump(),
            }
        )


def test_evidence_window_gap_and_three_way_reconciliation_are_identity_scoped():
    window = EvidenceWindow(
        window_id="window-1",
        worker_id="worker-1",
        environment="EXCHANGE_TESTNET",
        deployment_identity_hash="4" * 64,
        started_at=datetime(2026, 8, 24, tzinfo=UTC),
        ended_at=None,
        status="OPEN",
        outage_threshold_ms=None,
        environment_lineage=lineage(),
    )
    gap = EvidenceGapRecord(
        gap_id="gap-1",
        window_id=window.window_id,
        worker_id=window.worker_id,
        environment=window.environment,
        deployment_identity_hash=window.deployment_identity_hash,
        gap_started_at=datetime(2026, 8, 24, 1, tzinfo=UTC),
        gap_ended_at=None,
        reason="worker death",
        explained=False,
        reconciliation_record_id=None,
        invalidates_window=True,
        environment_lineage=lineage(),
    )
    reconciliation = ReconciliationRecord(
        reconciliation_id="recon-1",
        mode="THREE_WAY",
        worker_id="worker-1",
        environment="EXCHANGE_TESTNET",
        deployment_identity_hash="4" * 64,
        observed_at=datetime(2026, 8, 24, 2, tzinfo=UTC),
        intended_or_authorized_hash="6" * 64,
        store_hash="7" * 64,
        venue_hash="8" * 64,
        status="DIVERGED",
        breaks=["POSITION"],
        environment_lineage=lineage(),
    )
    assert gap.invalidates_window is True
    assert reconciliation.mode is ReconciliationMode.THREE_WAY


@pytest.mark.parametrize(
    ("model", "payload"),
    [
        (
            EvidenceWindow,
            {
                "window_id": "window-1",
                "worker_id": "worker-1",
                "environment": "EXCHANGE_TESTNET",
                "deployment_identity_hash": "4" * 64,
                "started_at": datetime(2026, 8, 24, tzinfo=UTC),
                "ended_at": None,
                "status": "OPEN",
            },
        ),
        (
            EvidenceGapRecord,
            {
                "gap_id": "gap-1",
                "window_id": "window-1",
                "worker_id": "worker-1",
                "environment": "EXCHANGE_TESTNET",
                "deployment_identity_hash": "4" * 64,
                "gap_started_at": datetime(2026, 8, 24, tzinfo=UTC),
                "gap_ended_at": None,
                "reason": "worker death",
                "explained": False,
                "reconciliation_record_id": None,
                "invalidates_window": True,
            },
        ),
        (
            ReconciliationRecord,
            {
                "reconciliation_id": "recon-1",
                "mode": "THREE_WAY",
                "worker_id": "worker-1",
                "environment": "EXCHANGE_TESTNET",
                "deployment_identity_hash": "4" * 64,
                "observed_at": datetime(2026, 8, 24, tzinfo=UTC),
                "intended_or_authorized_hash": "6" * 64,
                "store_hash": "7" * 64,
                "venue_hash": "8" * 64,
                "status": "MATCHED",
                "breaks": [],
            },
        ),
    ],
)
def test_execution_evidence_records_require_environment_lineage(model, payload):
    with pytest.raises(ValidationError):
        model.model_validate(payload)


def test_lifecycle_event_admits_exactly_four_writer_classes():
    assert {writer.value for writer in LifecycleWriterClass} == {
        "REGISTRAR",
        "ENVIRONMENT_ADMISSION_AUTHORITY",
        "PROMOTION_AUTHORITY",
        "MULTI_WORKER_SUPERVISOR",
    }
    event = LifecycleEvent(
        event_id="event-1",
        event_type="ADMISSION",
        writer_id="admission-authority-1",
        writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
        previous_state="TRIAGED",
        next_state="SHADOW_ELIGIBLE",
        candidate_id="QLC-20260824-1234abcd",
        package_hash="3" * 64,
        deployment_identity_hash="4" * 64,
        reason="accepted eligibility evidence",
        trigger=None,
        evidence_references=["evidence://decision-1"],
        timestamp=datetime(2026, 8, 24, tzinfo=UTC),
    )
    assert event.writer_class is LifecycleWriterClass.ENVIRONMENT_ADMISSION_AUTHORITY
