"""Exact, alias-free kernel-semantics identity selection."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


REFUSED_UNSUPPORTED_SEMANTICS_ID = "REFUSED_UNSUPPORTED_SEMANTICS_ID"
_SUPPORTED_VALUES = ("1.0.0", "2.0.0")


class UnsupportedSemanticsId(ValueError):
    """Raised whenever selection is missing, implicit, aliased, or unknown."""

    refusal_code = REFUSED_UNSUPPORTED_SEMANTICS_ID

    def __init__(self, value: object) -> None:
        self.value = value
        super().__init__(f"{self.refusal_code}: {value!r}")


@dataclass(frozen=True, slots=True, order=True)
class SemanticsId:
    """One exact registered semantic-version identity."""

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str or self.value not in _SUPPORTED_VALUES:
            raise UnsupportedSemanticsId(self.value)

    def __str__(self) -> str:
        return self.value


SEMANTICS_REGISTRY: Mapping[str, SemanticsId] = MappingProxyType(
    {value: SemanticsId(value) for value in _SUPPORTED_VALUES}
)


def resolve_semantics_id(value: object) -> SemanticsId:
    """Return the exact registered identity or one closed refusal.

    No default, alias, range syntax, shortened version, or coercion is accepted.
    """

    if isinstance(value, SemanticsId):
        registered = SEMANTICS_REGISTRY.get(value.value)
        if registered is not None:
            return registered
        raise UnsupportedSemanticsId(value.value)
    if type(value) is not str:
        raise UnsupportedSemanticsId(value)
    try:
        return SEMANTICS_REGISTRY[value]
    except KeyError as exc:
        raise UnsupportedSemanticsId(value) from exc
