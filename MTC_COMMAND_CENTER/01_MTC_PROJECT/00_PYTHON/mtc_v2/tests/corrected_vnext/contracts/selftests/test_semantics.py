from __future__ import annotations

import os

import pytest

from mtc_v2.core.semantics import (
    REFUSED_UNSUPPORTED_SEMANTICS_ID,
    SemanticsId,
    UnsupportedSemanticsId,
    resolve_semantics_id,
)


def _resolve_with_test_mutant(value: object) -> SemanticsId:
    """Equivalent modified copy used only to prove the alias test can go RED."""

    if os.environ.get("P012_MUTANT_ACCEPT_VERSION_ALIAS") == "1" and value == "latest":
        return resolve_semantics_id("1.0.0")
    return resolve_semantics_id(value)


@pytest.mark.parametrize("value", ["1.0.0", "2.0.0"])
def test_exact_registered_semantics_ids_are_selected(value: str) -> None:
    assert resolve_semantics_id(value) == SemanticsId(value)


@pytest.mark.parametrize(
    "value",
    [
        None,
        "",
        "latest",
        "legacy",
        "corrected",
        "1",
        "1.0",
        "1.x",
        ">=1.0.0",
        "^1.0.0",
        "3.0.0",
        1,
        1.0,
    ],
)
def test_missing_unknown_alias_range_and_implicit_versions_are_refused(value: object) -> None:
    with pytest.raises(UnsupportedSemanticsId) as caught:
        _resolve_with_test_mutant(value)

    assert caught.value.refusal_code == REFUSED_UNSUPPORTED_SEMANTICS_ID
