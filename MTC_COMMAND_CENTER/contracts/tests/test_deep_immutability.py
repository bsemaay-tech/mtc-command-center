from datetime import UTC, datetime
from decimal import Decimal

import pytest

from mtc_contracts import (
    AccountSnapshot,
    EligibilityCheckResult,
    EnvironmentLineage,
    InstrumentMetadata,
    StrategyPackage,
    TrialRecord,
    VolatilityTargetParams,
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


def test_strategy_package_account_snapshot_and_volatility_params_are_deeply_immutable():
    source_spec = {"entry": {"rules": ["breakout"]}}
    package = StrategyPackage(
        candidate_id="QLC-20260824-1234abcd",
        family_id="FAM-1234abcd1234abcd",
        package_hash="3" * 64,
        kernel_version="kernel-v1",
        kernel_code_sha="4" * 64,
        spec=source_spec,
        exact_params={"lookbacks": [20, 50]},
        modules_enabled=["stop"],
        substitute_catalogue_versions={"missing-risk": "1.0.0"},
        instrument_metadata=InstrumentMetadata(
            symbol="BTCUSDT",
            tick_size=Decimal("0.10"),
            lot_size=Decimal("0.001"),
            min_qty=Decimal("0.001"),
            min_notional=Decimal(5),
            contract_multiplier=Decimal(1),
        ),
        bar_close_only=True,
    )
    snapshot = AccountSnapshot(
        snapshot_id="5" * 64,
        taken_at=datetime(2026, 8, 24, tzinfo=UTC),
        account_id="paper-1",
        equity=Decimal(10000),
        available_margin=Decimal(8000),
        bucket_capital={"bucket-1": Decimal(5000)},
        open_exposure=Decimal(1000),
        margin_used=Decimal(200),
        positions={"BTCUSDT": Decimal(2)},
    )
    volatility = VolatilityTargetParams(
        target_volatility=Decimal("0.10"),
        estimator_id="ewma-20",
        estimator_params={"span": 20},
    )

    source_spec["entry"]["rules"].append("source-alias-mutation")
    assert package.spec["entry"]["rules"] == ("breakout",)
    assert StrategyPackage.model_validate_json(package.model_dump_json()) == package

    mutation_attempts = (
        lambda: package.spec["entry"]["rules"].append("late-rule"),
        lambda: package.exact_params["lookbacks"].append(100),
        lambda: package.substitute_catalogue_versions.__setitem__("other", "2.0.0"),
        lambda: snapshot.bucket_capital.__setitem__("bucket-1", Decimal(0)),
        lambda: snapshot.positions.__setitem__("BTCUSDT", Decimal(3)),
        lambda: volatility.estimator_params.__setitem__("span", 30),
    )
    for mutate in mutation_attempts:
        with pytest.raises((AttributeError, TypeError)):
            mutate()


def test_trial_and_check_arbitrary_payload_containers_are_deeply_immutable():
    trial = TrialRecord(
        run_id=f"{'6' * 64}.RESEARCH.1",
        candidate_id="QLC-20260824-1234abcd",
        package_hash="7" * 64,
        deployment_identity_hash="8" * 64,
        evaluation_run_hash="9" * 64,
        family_id="FAM-1234abcd1234abcd",
        trial_id=f"{'9' * 64}.{'a' * 64}.1",
        param_hash="a" * 64,
        exit_mode="fixed_2R",
        search_regime="grid",
        preregistered_space_hash="b" * 64,
        trial_index_in_family=1,
        family_size=10,
        parameters={"filters": {"periods": [10, 20]}},
        modules_enabled=["stop"],
        modules_enabled_count=1,
        fold_test_returns=[1.0],
        fold_test_sharpes=[0.4],
        fold_test_trades=[12],
        rejection_reasons=[],
        classification="PASS",
        simulator_class="CANONICAL",
        unsimulated_controls_hash="c" * 64,
        environment_lineage=lineage(),
    )
    check_payload = {
        "check_id": "robustness",
        "threshold": {"windows": [3, 6]},
        "measured_value": {"windows": [3, 6]},
        "outcome": "PASS",
        "dataset_hash": "d" * 64,
        "deployment_identity_hash": "8" * 64,
        "timestamp": datetime(2026, 8, 24, tzinfo=UTC),
    }
    if "environment_lineage" in EligibilityCheckResult.model_fields:
        check_payload["environment_lineage"] = lineage()
    check = EligibilityCheckResult(**check_payload)

    mutation_attempts = (
        lambda: trial.parameters["filters"]["periods"].append(30),
        lambda: check.threshold["windows"].append(9),
        lambda: check.measured_value.__setitem__("status", "changed"),
    )
    for mutate in mutation_attempts:
        with pytest.raises((AttributeError, TypeError)):
            mutate()
