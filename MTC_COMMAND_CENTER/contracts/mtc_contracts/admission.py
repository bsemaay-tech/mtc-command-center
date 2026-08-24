"""Eligibility-verdict and immutable environment-admission record shapes."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import model_validator

from .base import ContractModel, NonEmptyStr, Sha256, require_utc
from .lineage import Environment, EnvironmentLineage


class VerdictOutcome(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"


class EligibilityState(str, Enum):
    SHADOW_ELIGIBLE = "SHADOW_ELIGIBLE"
    TESTNET_PAPER_ELIGIBLE = "TESTNET_PAPER_ELIGIBLE"
    LIVE_CANDIDATE = "LIVE_CANDIDATE"
    LIMITED_LIVE_APPROVED = "LIMITED_LIVE_APPROVED"


class EligibilityCheckResult(ContractModel):
    """Machine-readable check result; BLOCKED is distinct from FAIL and PASS."""

    check_id: NonEmptyStr
    threshold: Any | None
    measured_value: Any | None
    outcome: VerdictOutcome
    dataset_hash: Sha256 | None
    deployment_identity_hash: Sha256
    timestamp: datetime
    environment_lineage: EnvironmentLineage
    blocked_reason: NonEmptyStr | None = None

    @model_validator(mode="after")
    def validate_result(self) -> EligibilityCheckResult:
        require_utc(self.timestamp)
        if self.outcome is VerdictOutcome.BLOCKED and not self.blocked_reason:
            raise ValueError("BLOCKED check must name what is missing")
        return self


class EligibilityVerdictSet(ContractModel):
    verdict_set_id: NonEmptyStr
    target_state: EligibilityState
    check_set_version: NonEmptyStr
    candidate_id: NonEmptyStr
    package_hash: Sha256
    deployment_identity_hash: Sha256
    evaluation_run_hash: Sha256
    results: tuple[EligibilityCheckResult, ...]
    outcome: VerdictOutcome
    timestamp: datetime
    issuer: NonEmptyStr
    environment_lineage: EnvironmentLineage

    @model_validator(mode="after")
    def validate_timestamp(self) -> EligibilityVerdictSet:
        require_utc(self.timestamp)
        return self


class AdmissionAuthority(str, Enum):
    ENVIRONMENT_ADMISSION = "ENVIRONMENT_ADMISSION"
    PROMOTION = "PROMOTION"


class AdmissionDecisionType(str, Enum):
    SHADOW_ELIGIBLE = "SHADOW_ELIGIBLE"
    PAPER_ELIGIBLE = "PAPER_ELIGIBLE"
    TESTNET_ELIGIBLE = "TESTNET_ELIGIBLE"
    PROMOTED = "PROMOTED"


EXACT_ADMITTED_ENVIRONMENTS = {
    AdmissionDecisionType.SHADOW_ELIGIBLE: frozenset({Environment.FORWARD_SHADOW}),
    AdmissionDecisionType.PAPER_ELIGIBLE: frozenset({Environment.INTERNAL_PAPER}),
    AdmissionDecisionType.TESTNET_ELIGIBLE: frozenset(
        {Environment.INTERNAL_PAPER, Environment.EXCHANGE_TESTNET}
    ),
    AdmissionDecisionType.PROMOTED: frozenset(
        {Environment.MAINNET, Environment.LIMITED_LIVE}
    ),
}


class AdmissionDecision(ContractModel):
    """Immutable identity-bound decision naming its exact admitted environment set."""

    decision_id: NonEmptyStr
    candidate_id: NonEmptyStr
    package_hash: Sha256
    deployment_identity_hash: Sha256
    authority: AdmissionAuthority
    decision: AdmissionDecisionType
    admits_to_environments: tuple[Environment, ...]
    reason: NonEmptyStr
    evidence_references: tuple[NonEmptyStr, ...]
    eligibility_verdict_set_id: NonEmptyStr
    leakage_record_id: NonEmptyStr | None = None
    simulator_class: NonEmptyStr
    unsimulated_controls_hash: Sha256
    timestamp: datetime
    approver: NonEmptyStr
    previous_state: NonEmptyStr
    new_state: NonEmptyStr
    check_set_version: NonEmptyStr
    environment_lineage: EnvironmentLineage

    @model_validator(mode="after")
    def validate_exact_admission(self) -> AdmissionDecision:
        require_utc(self.timestamp)
        if (
            frozenset(self.admits_to_environments)
            != EXACT_ADMITTED_ENVIRONMENTS[self.decision]
        ):
            raise ValueError(
                f"{self.decision.value} must name its exact environment set"
            )
        if self.decision is AdmissionDecisionType.PROMOTED:
            if self.authority is not AdmissionAuthority.PROMOTION:
                raise ValueError("PROMOTED requires Promotion Authority")
        elif self.authority is not AdmissionAuthority.ENVIRONMENT_ADMISSION:
            raise ValueError(
                "sub-live admission requires Environment Admission Authority"
            )
        return self
