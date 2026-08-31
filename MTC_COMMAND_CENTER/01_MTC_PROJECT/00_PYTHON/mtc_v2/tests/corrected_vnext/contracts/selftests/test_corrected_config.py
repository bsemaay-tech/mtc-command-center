from __future__ import annotations

import pytest

from mtc_v2.core.config import DEFAULT_CONFIG, resolve_config, validate_config


SHA_A = "a" * 64
SHA_B = "b" * 64


def corrected_config() -> dict[str, object]:
    return {
        "kernel_semantics_version": "2.0.0",
        "instrument_record_id": "SYNTH-INSTRUMENT-RULE2-08-RED-V1",
        "instrument_record_sha256": SHA_A,
        "cost_schedule_id": None,
        "cost_schedule_sha256": None,
        "funding_schedule_id": "SYNTH-FUNDING-RULE2-08-V1",
        "funding_schedule_sha256": SHA_B,
        "same_bar_collision_policy_id": "TARGET_FIRST",
        "slippage_model_id": "BPS_OF_REFERENCE_V1",
    }


def test_legacy_defaults_and_resolution_are_unchanged() -> None:
    resolved = resolve_config({})
    assert resolved["instrument_symbol"] == "UNKNOWN"
    assert resolved["instrument_price_tick"] == 0.01
    assert resolved["instrument_min_notional"] == 0.0
    assert "kernel_semantics_version" not in DEFAULT_CONFIG
    assert "kernel_semantics_version" not in resolved


def test_corrected_resolution_has_no_implicit_economic_defaults() -> None:
    config = corrected_config()
    validate_config(config)
    resolved = resolve_config(config)

    for key in (
        "instrument_symbol",
        "instrument_point_value",
        "instrument_price_tick",
        "instrument_qty_step",
        "instrument_min_qty",
        "instrument_min_notional",
        "instrument_contract_multiplier",
    ):
        assert key not in resolved


def test_explicit_corrected_runtime_value_survives_for_record_identity_check() -> None:
    config = corrected_config()
    config["instrument_price_tick"] = 0.5
    resolved = resolve_config(config)
    assert resolved["instrument_price_tick"] == 0.5


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("same_bar_collision_policy_id", "nearest"),
        ("slippage_model_id", "ZERO"),
        ("instrument_record_sha256", "A" * 64),
        ("funding_schedule_sha256", "short"),
    ],
)
def test_corrected_policy_model_and_digest_values_are_exact(key: str, value: object) -> None:
    config = corrected_config()
    config[key] = value
    with pytest.raises(ValueError):
        validate_config(config)


def test_cost_schedule_identity_is_both_null_or_both_present() -> None:
    config = corrected_config()
    config["cost_schedule_id"] = "COST-1"
    with pytest.raises(ValueError):
        validate_config(config)


def test_corrected_only_config_keys_require_exact_v2_selector() -> None:
    config = corrected_config()
    config.pop("kernel_semantics_version")
    with pytest.raises(ValueError):
        validate_config(config)

