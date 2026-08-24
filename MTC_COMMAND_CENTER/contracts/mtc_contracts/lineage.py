"""Environment, simulator, and unsimulated-control lineage shapes."""

from __future__ import annotations

from enum import Enum

from .base import ContractModel, NonEmptyStr, Sha256


class Environment(str, Enum):
    FORWARD_SHADOW = "FORWARD_SHADOW"
    INTERNAL_PAPER = "INTERNAL_PAPER"
    EXCHANGE_TESTNET = "EXCHANGE_TESTNET"
    LIMITED_LIVE = "LIMITED_LIVE"
    MAINNET = "MAINNET"


class EnvironmentLineage(ContractModel):
    """Evidence lineage kept alongside, and explicitly outside, identity hashes."""

    python_version: NonEmptyStr
    dependency_lockfile_hash: Sha256
    os_name: NonEmptyStr
    os_version: NonEmptyStr
    golden_suite_hash: Sha256
    golden_suite_bit_identical: bool


class UnsimulatedControl(ContractModel):
    control_id: NonEmptyStr
    required_for_promotion: bool
    reason: NonEmptyStr


class EvidenceIdentity(ContractModel):
    candidate_id: NonEmptyStr
    package_hash: Sha256
    deployment_identity_hash: Sha256
    evaluation_run_hash: Sha256 | None = None
    environment_lineage: EnvironmentLineage
