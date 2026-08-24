"""Shared primitives for the immutable v0 contract models."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

CONTRACT_VERSION = "0.1.0"
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

Sha256 = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
NonEmptyStr = Annotated[str, Field(min_length=1)]


class ContractModel(BaseModel):
    """Immutable, strict-at-the-boundary base for every v0 contract shape."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
        validate_default=True,
    )

    contract_version: str = Field(default=CONTRACT_VERSION, pattern=r"^0\.1\.0$")

    @field_validator("contract_version")
    @classmethod
    def contract_version_must_match(cls, value: str) -> str:
        if value != CONTRACT_VERSION:
            raise ValueError(
                f"contract version mismatch: expected {CONTRACT_VERSION}, got {value}"
            )
        return value


def require_utc(value: datetime) -> datetime:
    """Reject naive timestamps at contract boundaries."""

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    return value
