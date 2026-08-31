from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from mtc_v2.tests.corrected_vnext.verify_bceg import (
    GateRefusal,
    compare_documents,
    load_json_exact,
    validate_corrected_event_surface,
    validate_input_envelope,
    validate_legacy_unpadded,
)


FIXTURES = Path(__file__).parent


def refusal(check_id: str, action) -> None:
    with pytest.raises(GateRefusal) as caught:
        action()
    assert caught.value.check_id == check_id


def test_identical_pair_compares_equal_on_every_node() -> None:
    left = load_json_exact(FIXTURES / "node_equal_left.json")
    right = load_json_exact(FIXTURES / "node_equal_right.json")
    assert compare_documents(left, right) is None


def test_one_node_difference_is_predetected_exactly() -> None:
    left = load_json_exact(FIXTURES / "node_equal_left.json")
    right = load_json_exact(FIXTURES / "node_one_diff.json")
    difference = compare_documents(left, right)
    assert difference is not None
    assert difference[0] == "/a/1"


@pytest.mark.parametrize(
    ("fixture", "check_id"),
    [("duplicate_key.json", "JSON_DUPLICATE_KEY"), ("nonfinite.json", "JSON_NON_FINITE")],
)
def test_strict_json_refusals(fixture: str, check_id: str) -> None:
    refusal(check_id, lambda: load_json_exact(FIXTURES / fixture))


def test_version_shaped_surface_refusals() -> None:
    padded = load_json_exact(FIXTURES / "padded_legacy.json")
    refusal("LEGACY_SCHEMA_PADDED", lambda: validate_legacy_unpadded(padded))
    sequenced = load_json_exact(FIXTURES / "wrong_sequence.json")
    refusal("CORRECTED_SEQUENCE_INVALID", lambda: validate_corrected_event_surface(sequenced))


@pytest.mark.parametrize(
    ("fixture", "check_id"),
    [
        ("input_unknown_top.json", "INPUT_UNKNOWN_TOP_LEVEL_MEMBER"),
        ("input_corrected_in_legacy.json", "INPUT_CORRECTED_ONLY_IN_LEGACY_ARM"),
        ("input_f64_wrong_case.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_short.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_nonquiet.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_outside.json", "INPUT_F64BITS_OUTSIDE_SELECTOR"),
    ],
)
def test_section_22_input_refusals(fixture: str, check_id: str) -> None:
    document = load_json_exact(FIXTURES / fixture)
    refusal(check_id, lambda: validate_input_envelope(document))


def test_input_digest_mismatch_refusal() -> None:
    path = FIXTURES / "input_valid.json"
    document = load_json_exact(path)
    wrong_digest = "0" * 64
    assert hashlib.sha256(path.read_bytes()).hexdigest() != wrong_digest
    refusal(
        "INPUT_DIGEST_MISMATCH",
        lambda: validate_input_envelope(document, path=path, expected_digest=wrong_digest),
    )


def test_valid_section_22_input() -> None:
    path = FIXTURES / "input_valid.json"
    document = load_json_exact(path)
    validate_input_envelope(
        document,
        path=path,
        expected_digest=hashlib.sha256(path.read_bytes()).hexdigest(),
    )
