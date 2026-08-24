"""Optimizer-independent TrialRecord and selected-artifact manifest shapes."""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Literal

from pydantic import Field, model_validator

from .base import ContractModel, NonEmptyStr, Sha256
from .lineage import EnvironmentLineage


class TrialRecord(ContractModel):
    """One optimizer-independent catalog row; every identity is explicit."""

    run_id: NonEmptyStr
    candidate_id: NonEmptyStr
    package_hash: Sha256
    deployment_identity_hash: Sha256
    evaluation_run_hash: Sha256
    family_id: NonEmptyStr
    trial_id: NonEmptyStr
    param_hash: Sha256
    exit_mode: NonEmptyStr

    search_regime: Literal["grid", "tpe", "random"]
    preregistered_space_hash: Sha256
    trial_index_in_family: int = Field(ge=0)
    family_size: int = Field(gt=0)
    parameters: dict[str, Any]
    modules_enabled: tuple[NonEmptyStr, ...]
    modules_enabled_count: int = Field(ge=0)

    fold_test_returns: tuple[float, ...]
    fold_test_sharpes: tuple[float, ...]
    fold_test_trades: tuple[int, ...]

    lockbox_return_pct: float | None = None
    lockbox_sharpe: float | None = None
    lockbox_maxdd: float | None = None
    lockbox_trades: int | None = None
    lockbox_pf: float | None = None
    lockbox_expectancy_R: float | None = None
    lockbox_win_rate: float | None = None
    bh_return_pct: float | None = None
    excess_alpha: float | None = None
    dsr_p_value: float | None = None
    dsr_robust: bool | None = None
    bh_fdr_survivor: bool | None = None
    cpcv_pass_ratio: float | None = None
    pbo: float | None = None
    net_after_slippage_pct: float | None = None
    fee_bps_used: Decimal | None = None
    slippage_model_id: NonEmptyStr | None = None

    simulator_class: NonEmptyStr
    unsimulated_controls_hash: Sha256
    classification: NonEmptyStr
    rejection_reasons: tuple[NonEmptyStr, ...]

    is_pareto: bool = False
    is_top_k: bool = False
    is_robust: bool = False
    is_promoted: bool = False
    is_pinned: bool = False
    has_full_artifacts: bool = False
    environment_lineage: EnvironmentLineage

    @model_validator(mode="after")
    def validate_module_count(self) -> TrialRecord:
        if self.modules_enabled_count != len(self.modules_enabled):
            raise ValueError("modules_enabled_count must equal modules_enabled length")
        return self


class ArtifactManifest(ContractModel):
    package_hash: Sha256
    deployment_identity_hash: Sha256
    evaluation_run_hash: Sha256
    dataset_hash: Sha256
    kernel_version: NonEmptyStr
    simulator_class: NonEmptyStr
    simulator_version: NonEmptyStr
    unsimulated_controls_hash: Sha256
    allocation_policy_version: NonEmptyStr
    environment_lineage: EnvironmentLineage
