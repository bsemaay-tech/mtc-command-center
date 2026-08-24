from datetime import UTC, datetime

import pytest
from pydantic import BaseModel, ValidationError

import mtc_contracts
from mtc_contracts import (
    CONTRACT_VERSION,
    ContractHandshake,
    MissingRuleRecord,
    SizingMethod,
    __version__,
)


def test_v0_public_compatibility_fence():
    assert CONTRACT_VERSION == __version__ == "0.1.0"
    assert tuple(item.value for item in SizingMethod) == (
        "RISK_AT_STOP",
        "FIXED_QTY",
        "FIXED_NOTIONAL",
        "VOLATILITY_TARGET",
    )


def test_handshake_refuses_version_skew_at_the_schema_boundary():
    handshake = ContractHandshake(
        component_id="kernel-1",
        component_role="KERNEL",
        declared_at=datetime(2026, 8, 24, tzinfo=UTC),
    )
    assert handshake.declared_contract_version == "0.1.0"
    with pytest.raises(ValidationError):
        ContractHandshake.model_validate(
            {**handshake.model_dump(), "declared_contract_version": "0.2.0"}
        )


def test_not_expressible_source_rule_requires_versioned_named_substitute():
    record = MissingRuleRecord(
        record_id="missing-1",
        candidate_id="QLC-20260824-1234abcd",
        source_rule_id="rule-7",
        source_rule_provenance="transcript:sha256:abc",
        reason="requires account equity",
        substitute="catalogue-fixed-qty-conservative",
        substitute_catalogue_version="catalogue-v1",
        substitute_sizing_method="FIXED_QTY",
    )
    for missing in ("substitute", "substitute_catalogue_version"):
        payload = record.model_dump()
        del payload[missing]
        with pytest.raises(ValidationError):
            MissingRuleRecord.model_validate(payload)


def test_every_public_contract_model_emits_json_schema():
    model_names = []
    for name in mtc_contracts.__all__:
        value = getattr(mtc_contracts, name)
        if isinstance(value, type) and issubclass(value, BaseModel):
            schema = value.model_json_schema()
            assert schema["title"] == name
            model_names.append(name)
    assert len(model_names) >= 25
