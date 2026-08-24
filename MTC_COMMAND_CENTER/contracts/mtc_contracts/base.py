"""Shared primitives for the immutable v0 contract models."""

from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import datetime
from typing import Annotated, Any, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

CONTRACT_VERSION = "0.1.0"
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

Sha256 = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
NonEmptyStr = Annotated[str, Field(min_length=1)]


class FrozenDict(dict[Any, Any]):
    """Serializable dictionary whose normal mutation API always raises."""

    __slots__ = ()

    @staticmethod
    def _immutable(*args: Any, **kwargs: Any) -> None:
        raise TypeError("contract containers are immutable")

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    pop = _immutable
    popitem = _immutable
    setdefault = _immutable
    update = _immutable

    def __ior__(self, other: Any) -> Self:
        self._immutable(other)
        return self

    def __copy__(self) -> Self:
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> Self:
        return self


def _deep_freeze(value: Any) -> Any:
    """Detach and recursively freeze JSON-like containers after validation."""

    if isinstance(value, Mapping):
        return FrozenDict({key: _deep_freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_deep_freeze(item) for item in value)
    if isinstance(value, (set, frozenset)):
        return frozenset(_deep_freeze(item) for item in value)
    return value


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

    @model_validator(mode="after")
    def deep_freeze_containers(self) -> Self:
        """Freeze nested containers and detach them from caller-owned inputs."""

        for field_name in type(self).model_fields:
            value = getattr(self, field_name)
            frozen_value = _deep_freeze(value)
            if frozen_value is not value:
                object.__setattr__(self, field_name, frozen_value)
        return self


def require_utc(value: datetime) -> datetime:
    """Reject naive timestamps at contract boundaries."""

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    return value
